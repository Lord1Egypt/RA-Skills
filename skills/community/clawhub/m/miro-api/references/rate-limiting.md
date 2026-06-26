# Miro REST API - Rate Limiting

## Limits

**Default Rate Limit:**
- 300 requests per minute (5 requests/second)
- 50,000 requests per month (quota)

**Tier-Based (with different plans):**
- Starter: 300 req/min, 50k req/month
- Business: 1000 req/min, 500k req/month
- Enterprise: Custom limits

## Rate Limit Headers

Every API response includes rate limit information:

```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 287
X-RateLimit-Reset: 1234567890
```

| Header | Meaning |
|--------|---------|
| `X-RateLimit-Limit` | Total requests allowed in time window |
| `X-RateLimit-Remaining` | Requests left before limit |
| `X-RateLimit-Reset` | Unix timestamp when limit resets |

## Checking Rate Limit Status

**cURL:**
```bash
curl -i https://api.miro.com/v2/boards \
  -H "Authorization: Bearer TOKEN" | grep X-RateLimit
```

**JavaScript:**
```javascript
const response = await axios.get('https://api.miro.com/v2/boards', {
  headers: {'Authorization': `Bearer ${TOKEN}`}
});

const limit = response.headers['x-ratelimit-limit'];
const remaining = response.headers['x-ratelimit-remaining'];
const reset = response.headers['x-ratelimit-reset'];

console.log(`Remaining: ${remaining}/${limit}`);
console.log(`Resets at: ${new Date(reset * 1000).toISOString()}`);
```

**Python:**
```python
response = requests.get(
  'https://api.miro.com/v2/boards',
  headers={'Authorization': f'Bearer {TOKEN}'}
)

limit = response.headers['X-RateLimit-Limit']
remaining = response.headers['X-RateLimit-Remaining']
reset = response.headers['X-RateLimit-Reset']

print(f"Remaining: {remaining}/{limit}")
```

## Handling Rate Limits

### 429 Too Many Requests

When you exceed the rate limit, Miro returns:

```
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
X-RateLimit-Reset: 1234567890

{
  "code": 429,
  "message": "Rate limit exceeded"
}
```

### Exponential Backoff Strategy

**Best Practice:** Wait and retry with exponential backoff

```javascript
async function callWithBackoff(fn, maxRetries = 5) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error.response?.status === 429) {
        const delayMs = Math.min(
          1000 * Math.pow(2, attempt) + Math.random() * 1000,
          30000 // Max 30 seconds
        );
        console.log(`Rate limited. Waiting ${delayMs}ms...`);
        await sleep(delayMs);
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}

const boards = await callWithBackoff(() => miro.get('/boards'));
```

## Strategies to Avoid Rate Limits

### 1. Batch Operations

**Instead of:** 100 separate POST requests
```javascript
// SLOW - 100 API calls
for (let i = 0; i < 100; i++) {
  await miro.post(`/boards/${boardId}/items`, { 
    type: 'CARD',
    title: `Task ${i}`
  });
}
// Uses 100 requests!
```

**Do this:** Single batch request
```javascript
// FAST - 1 API call
await miro.post(`/boards/${boardId}/items/batch`, {
  items: Array.from({length: 100}, (_, i) => ({
    type: 'CARD',
    title: `Task ${i}`
  }))
});
// Uses 1 request!
```

### 2. Pagination Efficiently

Don't fetch everything at once:

```javascript
// WASTEFUL - Could fetch 100k items per page
const allItems = [];
let cursor = null;

do {
  const response = await miro.get(`/boards/${boardId}/items`, {
    params: { limit: 100, cursor }
  });
  allItems.push(...response.data.data);
  cursor = response.data.cursor;
} while (cursor);

// EFFICIENT - Fetch as needed
async function* getItems(boardId) {
  let cursor = null;
  
  do {
    const response = await miro.get(`/boards/${boardId}/items`, {
      params: { limit: 100, cursor }
    });
    
    for (const item of response.data.data) {
      yield item;
    }
    
    cursor = response.data.cursor;
  } while (cursor);
}

// Use only what you need
for await (const item of getItems(boardId)) {
  if (item.type === 'CARD') {
    console.log(item.title);
  }
}
```

### 3. Cache Responses

```javascript
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function getCachedBoards() {
  const cacheKey = 'boards-list';
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  
  const boards = await miro.get('/boards');
  cache.set(cacheKey, {
    data: boards.data,
    timestamp: Date.now()
  });
  
  return boards.data;
}
```

### 4. Use Webhooks Instead of Polling

**Don't do this (polling):**
```javascript
// Check every 10 seconds = 8,640 requests/day
setInterval(async () => {
  const boards = await miro.get('/boards');
  // ...
}, 10000);
```

**Do this (webhooks):**
```javascript
// Register webhook once, get notified on changes
await miro.post(`/teams/${teamId}/webhooks`, {
  url: 'https://yourapp.com/webhook/miro',
  events: ['board.created', 'board.updated']
});

// Receive events in real-time, 0 requests!
```

### 5. Minimize Unnecessary Requests

```javascript
// WASTEFUL - Fetches board, then items separately
const board = await miro.get(`/boards/${boardId}`);
const items = await miro.get(`/boards/${boardId}/items`);

// EFFICIENT - Use sparse fieldsets if available
const board = await miro.get(`/boards/${boardId}?fields=id,name,owner`);
```

## Monitoring Rate Limit Usage

### Track Usage Over Time

```javascript
const usage = {
  requests: 0,
  rateLimitedAt: [],
  peakHour: new Map()
};

async function trackedCall(endpoint) {
  const response = await miro.get(endpoint);
  
  usage.requests++;
  const remaining = response.headers['x-ratelimit-remaining'];
  const hour = new Date().getHours();
  
  usage.peakHour.set(hour, (usage.peakHour.get(hour) || 0) + 1);
  
  if (remaining < 50) {
    console.warn(`Low on rate limit: ${remaining} remaining`);
  }
  
  return response.data;
}

// Analyze usage
console.log(`Total requests: ${usage.requests}`);
console.log('Usage by hour:', Object.fromEntries(usage.peakHour));
```

### Set Alerts

```javascript
const ALERT_THRESHOLD = 50; // Alert when <50 remaining

async function alertOnLowRateLimit(endpoint) {
  const response = await miro.get(endpoint);
  const remaining = parseInt(response.headers['x-ratelimit-remaining']);
  
  if (remaining < ALERT_THRESHOLD) {
    // Send alert (email, Slack, etc.)
    await sendAlert(
      `⚠️ Low rate limit: ${remaining} requests remaining`
    );
  }
  
  return response.data;
}
```

## Rate Limit Best Practices

1. **Check Headers Regularly**
   - Monitor X-RateLimit-Remaining
   - Plan ahead when approaching limit

2. **Implement Backoff**
   - Exponential backoff with jitter
   - Max 30-second wait time

3. **Batch When Possible**
   - Use `/batch` endpoints
   - Reduces request count

4. **Use Webhooks**
   - Real-time updates without polling
   - Zero API requests for notifications

5. **Cache Responses**
   - Store frequently accessed data
   - TTL-based cache expiration

6. **Optimize Queries**
   - Use sparse fieldsets
   - Limit pagination size
   - Filter on client side when possible

7. **Monitor Usage**
   - Track requests per hour/day
   - Set alerts for low remaining
   - Analyze peak usage patterns

8. **Contact Support**
   - Request higher limits if needed
   - Explain your use case
   - May qualify for Business/Enterprise plan

