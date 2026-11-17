# SearXNG Plugin Setup

## Configuration

The SearXNG plugin (`web-searxng`) is a first-class Hermes web search backend.

### Prerequisites

- A running SearXNG instance (Docker: `searxng/searxng`, exposes port 8080)
- On this VPS: SearXNG runs in Docker, port 8888 mapped to container's 8080

### Setup

1. Set the URL in .env:
   hermes config set SEARXNG_URL http://localhost:8888

2. Set the web backend:
   hermes config set web.backend searxng

3. Enable the plugin (if not already):
   hermes plugins enable web-searxng

4. Restart the gateway:
   hermes gateway restart

### Troubleshooting

- SEARXNG_URL is not set: Run hermes config set SEARXNG_URL http://localhost:8888 and restart gateway
- Empty results: Check SearXNG logs via docker logs searxng
- Connection refused: Check container via docker ps | grep searxng
- Plugin reads from .env, not config.yaml. Use hermes config set to write to .env.

### Architecture

- web_search tool dispatches through agent/web_search_registry.py -> plugin registry
- SearXNGWebSearchProvider reads SEARXNG_URL from .env at runtime via get_env_value()
- No API key required
- Metasearches 70+ engines, works from VPS IPs without CAPTCHA
