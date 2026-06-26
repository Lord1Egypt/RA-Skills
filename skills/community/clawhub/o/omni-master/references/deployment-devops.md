# Deployment & DevOps

## Platforms (via ClawHub skills)
- **Vercel** — Frontend/serverless deployment
- **Railway** — Full-stack app hosting
- **Render** — Web services, databases
- **Deno Deploy** — Edge functions
- **Fly.io** — Container deployment
- **GPU Deploy** — ML model serving

## Containerization
```dockerfile
# Dockerfile basics
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
# Docker commands
docker build -t myapp .
docker run -p 3000:3000 myapp
docker compose up -d
docker logs container_id
```

## CI/CD Pipelines

### GitHub Actions
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
      - run: npm run deploy
```

## Infrastructure as Code
- Terraform for cloud resources
- Ansible for configuration management
- Docker Compose for local dev
- Kubernetes for orchestration

## Monitoring & Observability
- Application logs → centralized logging
- Health checks / uptime monitoring
- Error tracking (Sentry-style)
- Performance metrics (latency, throughput)
- Alerting thresholds

## Deployment Strategies
1. **Rolling** — Gradual instance replacement
2. **Blue/Green** — Two environments, switch traffic
3. **Canary** — Small percentage first, then expand
4. **Feature flags** — Decouple deploy from release

## Server Management
- SSH for remote administration
- Systemd for service management
- Nginx/Caddy for reverse proxy
- Let's Encrypt for TLS certificates
- Backup and restore procedures

## Best Practices
- Never deploy on Friday
- Automate everything repeatable
- Monitor after deploy
- Have rollback plan ready
- Document infrastructure decisions
