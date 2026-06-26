# Job Queue System for Image Generation

## Architecture

```
User Request → Queue Manager → Worker Pool → Gemini API
                    ↓
              Rate Limiter
                    ↓
            Response Handler
```

## Components

### 1. Queue Manager (Redis/Bull Queue)
- Stores pending jobs
- Manages priorities
- Tracks job status

### 2. Worker Pool
- Multiple worker processes
- Max concurrency: 5
- Auto-scaling based on queue length

### 3. Rate Limiter
- Per-user tracking
- Global rate limiting
- Token bucket algorithm

## Implementation Options

### Option 1: Bull Queue (Redis-based)
```javascript
const Queue = require('bull');
const imageQueue = new Queue('image-generation');

// Add job
imageQueue.add({
  userId: '5495156302',
  prompt: '...',
  priority: 1
});

// Process
imageQueue.process(async (job) => {
  // Generate image
});
```

### Option 2: File-based (Simple)
```javascript
// Queue file: ~/.openclaw/workspace/.queue/
// Status: pending, processing, completed, failed
```

### Option 3: Priority Queue
- Owner: Priority 1 (0ms delay)
- Admin: Priority 2 (100ms delay)
- Manager: Priority 3 (500ms delay)
- User: Priority 4 (1000ms delay)

## User Experience

When overloaded:
```
"您的请求已加入队列，当前位置：第3位，预计等待：45秒"

(Your request is in queue, position: 3, estimated wait: 45s)
```

## Scalability

Single Server:
- Max 5 concurrent generations
- Queue up to 100 jobs
- Auto-retry failed jobs

Multi-Server (Future):
- Redis shared queue
- Load balancer
- Dedicated GPU workers

## Current Recommendation

Start with **Option 2 (File-based)** for simplicity:
- No Redis dependency
- Easy to implement
- Good enough for 10-20 users

Upgrade to **Option 1 (Bull Queue)** when:
- >20 concurrent users
- Need real-time status updates
- Multi-server deployment
