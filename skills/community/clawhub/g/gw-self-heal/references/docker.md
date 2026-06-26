# Docker Self-Healing Setup

```dockerfile
FROM node:22-slim
RUN npm i -g openclaw

COPY openclaw.json /root/.openclaw/openclaw.json
COPY openclaw.json /root/.openclaw/openclaw.json.bak

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:3377/health || exit 1

CMD ["bash", "-c", "cp /root/.openclaw/openclaw.json.bak /root/.openclaw/openclaw.json.bak && openclaw gateway start --foreground"]
```

```bash
docker run -d --restart=always --name openclaw \
  -v openclaw-data:/root/.openclaw \
  openclaw-watchdog
```

`--restart=always` ensures Docker restarts the container on any crash.
Combine with the watchdog script inside the container for config-level recovery.
