# Real-Time & Event-Driven Systems

## WebSockets
### When to Use
- Real-time updates (chat, live data, notifications)
- Bidirectional communication needed
- Lower latency than HTTP polling

### Patterns
```javascript
// Server (Node.js)
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });
wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    wss.clients.forEach(client => client.send(data));
  });
});

// Client
const ws = new WebSocket('ws://localhost:8080');
ws.onmessage = (event) => console.log(event.data);
ws.send('hello');
```

## Server-Sent Events (SSE)
### When to Use
- Server → Client one-way streaming
- Live feeds, notifications, progress updates
- Simpler than WebSockets for one-way data

### Pattern
```javascript
// Server sends
res.writeHead(200, {
  'Content-Type': 'text/event-stream',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive'
});
res.write(`data: ${JSON.stringify(payload)}\n\n`);

// Client receives
const source = new EventSource('/stream');
source.onmessage = (e) => console.log(JSON.parse(e.data));
```

## Message Queues
### Concepts
- Producer: sends messages to queue
- Consumer: receives and processes messages
- Acknowledgment: confirms processing complete
- Dead letter: failed messages go to separate queue

### Tools
- Redis: lightweight, fast (PUB/SUB, Streams)
- RabbitMQ: full-featured, AMQP protocol
- Kafka: high-throughput, event streaming
- Bull/BullMQ: Redis-based job queue for Node.js

### Patterns
```python
# Redis queue (Python)
import redis
r = redis.Redis()

# Producer
r.lpush('tasks', json.dumps({'type': 'email', 'to': 'user@example.com'}))

# Consumer
while True:
    _, task = r.brpop('tasks')
    process(json.loads(task))
```

## Cron vs Event-Driven
| Use Case | Cron | Event-Driven |
|---|---|---|
| Daily report | ✅ | |
| On file change | | ✅ |
| Periodic health check | ✅ | |
| On user action | | ✅ |
| Scheduled cleanup | ✅ | |
| On webhook receipt | | ✅ |

## Webhooks
### Receiving
```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    verify_signature(request.headers, payload)
    process_event(payload)
    return '', 200
```

### Sending
- POST to registered URL
- Include HMAC signature for verification
- Retry with exponential backoff (1s, 2s, 4s, 8s)
- Include idempotency key

## Rate Limiting
```python
# Token bucket
class RateLimiter:
    def __init__(self, rate, capacity):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.time()
    
    def allow(self):
        now = time.time()
        self.tokens = min(self.capacity, 
                          self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```
