---
name: local-search-pro
description: Free Brave API alternative for OpenClaw. Completely FREE web search. No API key required. Secure localhost-only deployment. Supports hidden --dev flag for local development.
license: MIT
metadata:
  version: 1.0.10
  openclaw:
    requires:
      bins:
        - docker
        - python3
  keywords:
    - brave
    - brave api
    - brave api alternative
    - free search
    - web search
    - no api key
    - zero cost
    - secure search
    - localhost only
    - searxng
---

# 💰 Free & Secure Brave API Alternative

local-search-pro provides a **100% FREE and secure** replacement for OpenClaw's built-in web_search.

### Python Dependency

The runtime scripts require the Python package `requests`.

Install if missing:

```
pip install requests
```


✅ No Brave API key  
✅ No $5/month cost  
✅ Localhost-only deployment  
✅ Limiter enabled  
✅ Safe search enabled  

---

## Dev Mode

Advanced users can run:

python scripts/install.py --dev

⚠ Dev mode disables:
- safe_search (set to 0)
- limiter (disabled)

This weakens safety protections and is intended for local development only.

---

## Persistence Notice

⚠ The install script runs Docker with `--restart unless-stopped` and `-d`, which creates a persistent background container (`searxng-local`).

- The container will continue running after OpenClaw exits.
- It will automatically restart on system reboot.
- This is intentional for local service stability.

To remove the service:

```
docker rm -f searxng-local
```

Users should be aware this is a system-level persistent service.

---

## Security Model

- Docker container binds to **127.0.0.1 only**
- Request limiter enabled by default
- Safe search enabled by default
- No public exposure
- No global config modifications

---

This skill does not modify global OpenClaw configuration.
