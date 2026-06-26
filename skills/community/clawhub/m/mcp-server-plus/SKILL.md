---
name: mcp-server-plus
description: "Enhanced MCP server creation with templates, security best practices, deployment guides, and monitoring. Supports multiple transport types (stdio, SSE, WebSocket) and deployment platforms."
metadata:
  author: opencode
  version: 2.0
  tags: mcp, server, api, deployment, security
  compatibility: opencode
  license: MIT
---

# MCP Server Plus

Enhanced MCP server creation with templates, security, deployment, and monitoring.

## Features

- **Server Templates**: Ready-to-use templates for common use cases
- **Security Best Practices**: Authentication, rate limiting, input validation
- **Deployment Guides**: Multiple platforms (Docker, Vercel, AWS)
- **Monitoring**: Health checks, logging, metrics
- **Transport Options**: stdio, SSE, WebSocket

## Quick Reference

| Use Case | Template | Transport |
|----------|----------|-----------|
| API wrapper | api-wrapper | SSE |
| Database access | database | stdio |
| File system | filesystem | stdio |
| Real-time | websocket | WebSocket |

## Server Templates

### API Wrapper Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  {
    name: "api-wrapper",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "fetch_data",
      description: "Fetch data from external API",
      inputSchema: {
        type: "object",
        properties: {
          endpoint: { type: "string" },
          params: { type: "object" },
        },
        required: ["endpoint"],
      },
    },
  ],
}));

// Handle tool calls
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "fetch_data") {
    const response = await fetch(args.endpoint, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${process.env.API_KEY}`,
      },
    });
    const data = await response.json();
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(data, null, 2),
        },
      ],
    };
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Database Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

const server = new Server(
  {
    name: "database",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "query",
      description: "Execute SQL query",
      inputSchema: {
        type: "object",
        properties: {
          sql: { type: "string" },
          params: { type: "array" },
        },
        required: ["sql"],
      },
    },
  ],
}));

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "query") {
    const result = await pool.query(args.sql, args.params);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            rows: result.rows,
            rowCount: result.rowCount,
          }, null, 2),
        },
      ],
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### File System Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import * as fs from "fs/promises";
import * as path from "path";

const server = new Server(
  {
    name: "filesystem",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "read_file",
      description: "Read file contents",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string" },
        },
        required: ["path"],
      },
    },
    {
      name: "write_file",
      description: "Write to file",
      inputSchema: {
        type: "object",
        properties: {
          path: { type: "string" },
          content: { type: "string" },
        },
        required: ["path", "content"],
      },
    },
  ],
}));

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "read_file") {
    const content = await fs.readFile(args.path, "utf-8");
    return {
      content: [
        {
          type: "text",
          text: content,
        },
      ],
    };
  }
  
  if (name === "write_file") {
    await fs.writeFile(args.path, args.content);
    return {
      content: [
        {
          type: "text",
          text: `File written successfully: ${args.path}`,
        },
      ],
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Security Best Practices

### Authentication

```typescript
// API key validation
const validateApiKey = (req) => {
  const apiKey = req.headers["x-api-key"];
  if (apiKey !== process.env.API_KEY) {
    throw new Error("Invalid API key");
  }
};

// OAuth2 validation
const validateOAuth = async (req) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) {
    throw new Error("Missing authorization token");
  }
  
  const user = await verifyToken(token);
  return user;
};
```

### Rate Limiting

```typescript
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests",
});

app.use(limiter);
```

### Input Validation

```typescript
import { z } from "zod";

const ToolInputSchema = z.object({
  endpoint: z.string().url(),
  params: z.object({}).optional(),
});

const validateInput = (input) => {
  return ToolInputSchema.parse(input);
};
```

### Environment Variables

```bash
# Required
API_KEY=your-api-key
DATABASE_URL=postgresql://user:pass@host/db

# Optional
PORT=3000
LOG_LEVEL=info
RATE_LIMIT=100
```

## Deployment Guides

### Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml
version: "3.8"
services:
  mcp-server:
    build: .
    ports:
      - "3000:3000"
    environment:
      - API_KEY=${API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped
```

### Vercel

```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server.js"
    }
  ]
}
```

### AWS Lambda

```javascript
// handler.js
const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { SSEServerTransport } = require("@modelcontextprotocol/sdk/server/sse.js");

exports.handler = async (event, context) => {
  const server = new Server(/* ... */);
  const transport = new SSEServerTransport("/messages", res);
  
  await server.connect(transport);
  
  return {
    statusCode: 200,
    body: JSON.stringify({ status: "connected" }),
  };
};
```

## Monitoring

### Health Checks

```typescript
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
  });
});
```

### Logging

```typescript
import winston from "winston";

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" }),
  ],
});
```

### Metrics

```typescript
import { Counter, Histogram } from "prom-client";

const requestCounter = new Counter({
  name: "mcp_requests_total",
  help: "Total number of MCP requests",
  labelNames: ["method", "status"],
});

const requestDuration = new Histogram({
  name: "mcp_request_duration_seconds",
  help: "Duration of MCP requests in seconds",
  labelNames: ["method"],
});
```

## Transport Options

### stdio

- Best for local communication
- Simple setup
- Low latency

### SSE (Server-Sent Events)

- Best for web applications
- HTTP-based
- Easy to proxy

### WebSocket

- Best for real-time communication
- Bidirectional
- Persistent connection

## Best Practices

1. **Use TypeScript** - Type safety and better tooling
2. **Validate inputs** - Always validate tool inputs
3. **Handle errors** - Return meaningful error messages
4. **Log operations** - Track tool usage and errors
5. **Rate limit** - Prevent abuse
6. **Use environment variables** - Never hardcode secrets
7. **Health checks** - Monitor server status
8. **Documentation** - Document tools and usage

## Common Issues

| Issue | Solution |
|-------|----------|
| Connection refused | Check server is running |
| Authentication failed | Verify API key |
| Timeout | Increase timeout or check network |
| Rate limited | Implement rate limiting |
| Memory leak | Monitor and restart periodically |
