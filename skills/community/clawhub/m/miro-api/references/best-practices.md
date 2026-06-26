# Miro REST API - Best Practices

## Architecture & Design

### 1. API Client Pattern

Create a reusable client wrapper:

```javascript
class MiroClient {
  constructor(token, options = {}) {
    this.token = token;
    this.baseURL = 'https://api.miro.com/v2';
    this.timeout = options.timeout || 30000;
    this.retries = options.retries || 3;
  }
  
  async request(method, endpoint, data = null) {
    return this.retryWithBackoff(() =>
      fetch(`${this.baseURL}${endpoint}`, {
        method,
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        },
        body: data ? JSON.stringify(data) : null,
        timeout: this.timeout
      })
    );
  }
  
  async retryWithBackoff(fn, attempt = 0) {
    try {
      return await fn();
    } catch (error) {
      if (attempt < this.retries && this.isRetryable(error)) {
        const delay = Math.pow(2, attempt) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        return this.retryWithBackoff(fn, attempt + 1);
      }
      throw error;
    }
  }
  
  isRetryable(error) {
    return error.status === 429 || error.status >= 500;
  }
}

// Usage
const miro = new MiroClient(process.env.MIRO_TOKEN);
const boards = await miro.request('GET', '/boards');
```

### 2. Error Boundaries

Wrap API calls with proper error handling:

```javascript
async function safeApiCall(fn, context = '') {
  try {
    return await fn();
  } catch (error) {
    console.error(`API Error in ${context}:`, {
      message: error.message,
      status: error.status,
      code: error.response?.data?.code,
      details: error.response?.data?.details
    });
    
    throw new APIError(
      `Failed to ${context}: ${error.message}`,
      error.status,
      error.response?.data
    );
  }
}

// Usage
try {
  const boards = await safeApiCall(
    () => miro.get('/boards'),
    'fetch boards'
  );
} catch (error) {
  // Handle error gracefully
}
```

## Performance

### 1. Request Optimization

```javascript
// SLOW - Multiple sequential requests
const board = await miro.get(`/boards/${boardId}`);
const items = await miro.get(`/boards/${boardId}/items`);
const comments = await miro.get(`/boards/${boardId}/comments`);
// Total: 3+ seconds

// FAST - Parallel requests
const [board, items, comments] = await Promise.all([
  miro.get(`/boards/${boardId}`),
  miro.get(`/boards/${boardId}/items`),
  miro.get(`/boards/${boardId}/comments`)
]);
// Total: ~1 second
```

### 2. Batch Operations

Always use batch endpoints when available:

```javascript
// 100 items
const items = generateItems(100);

// SLOW - 100 requests, 10-30 seconds
for (const item of items) {
  await miro.post(`/boards/${boardId}/items`, item);
}

// FAST - 1 request, <1 second
await miro.post(`/boards/${boardId}/items/batch`, { items });
```

### 3. Pagination Optimization

```javascript
// Fetch only what you need
async function* listItems(boardId, limit = 100) {
  let cursor = null;
  
  do {
    const response = await miro.get(
      `/boards/${boardId}/items`,
      { params: { limit, cursor } }
    );
    
    for (const item of response.data.data) {
      yield item;
    }
    
    cursor = response.data.cursor;
  } while (cursor);
}

// Use generator to process items as they arrive
for await (const item of listItems(boardId)) {
  processItem(item);
  // Doesn't wait for all items to load
}
```

### 4. Connection Pooling

For Node.js with native HTTP client:

```javascript
const https = require('https');

const agent = new https.Agent({
  keepAlive: true,
  maxSockets: 50,
  maxFreeSockets: 10,
  timeout: 60000
});

// Reuse connections
const options = {
  agent,
  headers: {'Authorization': `Bearer ${TOKEN}`}
};
```

## Security

### 1. Token Management

```javascript
// DON'T - Ever commit tokens
const TOKEN = 'miro_pat_abc123'; // ❌ WRONG

// DO - Use environment variables
require('dotenv').config();
const TOKEN = process.env.MIRO_TOKEN; // ✅ CORRECT

// DO - Use secure storage
const token = await getSecretFromVault('miro/api-token');
```

### 2. Webhook Signature Verification

Always verify webhook authenticity:

```javascript
const crypto = require('crypto');

function verifyWebhookSignature(request, secret) {
  const signature = request.headers['x-miro-request-signature'];
  const body = request.rawBody;
  
  const hmac = crypto
    .createHmac('sha256', secret)
    .update(body)
    .digest('hex');
  
  const expectedSig = `sha256=${hmac}`;
  
  // Constant-time comparison to prevent timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSig)
  );
}
```

### 3. Rate Limit Protection

Prevent abuse with rate limiting on your endpoints:

```javascript
const rateLimit = require('express-rate-limit');

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per windowMs
  message: 'Too many requests from this IP'
});

app.use('/api/', apiLimiter);
```

### 4. Input Validation

Always validate input before sending to Miro:

```javascript
const Joi = require('joi');

const createItemSchema = Joi.object({
  type: Joi.string().valid('CARD', 'SHAPE', 'TEXT').required(),
  title: Joi.string().max(500).required(),
  position: Joi.object({
    x: Joi.number().required(),
    y: Joi.number().required()
  }).required()
});

async function createItem(boardId, data) {
  const { error, value } = createItemSchema.validate(data);
  
  if (error) {
    throw new ValidationError(error.details);
  }
  
  return miro.post(`/boards/${boardId}/items`, value);
}
```

## Reliability

### 1. Idempotency

Design operations to be idempotent:

```javascript
async function createOrGetBoard(name) {
  // Check if already exists
  const existing = await findBoardByName(name);
  if (existing) return existing;
  
  // Create new board
  const board = await miro.post('/boards', { name });
  return board;
}

// Safe to call multiple times - won't create duplicates
```

### 2. Retry Strategy

```javascript
async function retryWithBackoff(fn, maxRetries = 5) {
  const delays = [100, 500, 1000, 2000, 5000];
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      const isRetryable = error.status === 429 || error.status >= 500;
      const hasRetries = attempt < maxRetries;
      
      if (isRetryable && hasRetries) {
        const delay = delays[Math.min(attempt, delays.length - 1)];
        const jitter = Math.random() * 1000;
        await sleep(delay + jitter);
        continue;
      }
      
      throw error;
    }
  }
}
```

### 3. Circuit Breaker Pattern

Prevent cascading failures:

```javascript
class CircuitBreaker {
  constructor(fn, threshold = 5, timeout = 60000) {
    this.fn = fn;
    this.failures = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = Date.now();
  }
  
  async call(...args) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = 'HALF_OPEN';
    }
    
    try {
      const result = await this.fn(...args);
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}

const breaker = new CircuitBreaker(() => miro.get('/boards'));
```

## Monitoring & Observability

### 1. Structured Logging

```javascript
const logger = {
  info: (msg, context) => console.log(JSON.stringify({
    level: 'INFO',
    timestamp: new Date().toISOString(),
    message: msg,
    ...context
  })),
  error: (msg, error, context) => console.error(JSON.stringify({
    level: 'ERROR',
    timestamp: new Date().toISOString(),
    message: msg,
    error: error.message,
    stack: error.stack,
    ...context
  }))
};

logger.info('Fetching boards', { userId: 'user-123' });
```

### 2. Metrics Collection

```javascript
const metrics = {
  requests: 0,
  errors: 0,
  latencies: [],
  
  recordRequest(duration) {
    this.requests++;
    this.latencies.push(duration);
  },
  
  recordError() {
    this.errors++;
  },
  
  getStats() {
    const sorted = this.latencies.sort((a, b) => a - b);
    return {
      totalRequests: this.requests,
      totalErrors: this.errors,
      errorRate: this.errors / this.requests,
      avgLatency: sorted.reduce((a, b) => a + b, 0) / sorted.length,
      p95Latency: sorted[Math.floor(sorted.length * 0.95)],
      p99Latency: sorted[Math.floor(sorted.length * 0.99)]
    };
  }
};

async function trackedCall(endpoint) {
  const start = Date.now();
  try {
    return await miro.get(endpoint);
  } catch (error) {
    metrics.recordError();
    throw error;
  } finally {
    metrics.recordRequest(Date.now() - start);
  }
}
```

### 3. Health Checks

```javascript
async function healthCheck() {
  try {
    const response = await miro.get('/boards?limit=1');
    const remaining = response.headers['x-ratelimit-remaining'];
    
    return {
      status: 'healthy',
      api: 'up',
      rateLimit: {
        remaining,
        healthy: remaining > 100
      },
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}

// Check every 5 minutes
setInterval(healthCheck, 5 * 60 * 1000);
```

## Testing

### 1. Mock API Responses

```javascript
const mockMiro = {
  get: async (endpoint) => {
    if (endpoint === '/boards') {
      return {
        data: {
          data: [{ id: 'board-123', name: 'Test Board' }]
        }
      };
    }
  },
  post: async (endpoint, data) => {
    return { data: { id: 'item-456', ...data } };
  }
};

// Test with mock
await testCreateBoardItem(mockMiro);
```

### 2. Webhook Testing

```javascript
// Simulate webhook event
async function testWebhook() {
  const event = {
    type: 'item.created',
    data: {
      id: 'item-123',
      title: 'Test Item'
    }
  };
  
  const response = await fetch('http://localhost:3000/webhook/miro', {
    method: 'POST',
    body: JSON.stringify(event)
  });
  
  expect(response.status).toBe(200);
}
```

