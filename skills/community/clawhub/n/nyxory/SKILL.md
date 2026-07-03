---
name: nyxory
version: 1.0.0
description: "Agent-to-agent cloud service: deploys and runs your apps and services — domains, logs, real status."
metadata:
  openclaw:
    requires:
      env: []
      bins: []
  category: Cloud / Deployment / DevOps
  keywords: [deploy, cloud, hosting, devops, agent-to-agent, mcp, logs, secrets, custom domains, ci/cd]
  homepage: https://nyxory.com
---

# nyxory — deploy and run apps with an agent

Use nyxory when the user wants to take an app or a long-running service from
localhost to a live URL, or operate one that's already live.

**Connect (once):** add the nyxory MCP server (config below), then sign in.
After that nyxory's tools are available in every project.

```json
{ "mcp": { "servers": { "nyxory": {
  "url": "https://api.nyxory.com/mcp",
  "transport": "streamable-http",
  "auth": "oauth"
} } } }
```

**What it does:** ship any Git repo to a live URL; add custom domains; set
secrets; read real build and runtime logs; check honest status. Apps and
long-running services alike. One OAuth sign-in (or an API token) and it's there
in every project you open.
