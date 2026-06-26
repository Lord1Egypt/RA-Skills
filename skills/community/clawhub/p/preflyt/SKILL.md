---
name: preflyt
description: >-
  Scan deployed web apps for security misconfigurations after every deploy.
  Checks for exposed .env files, databases, source code, open ports, missing
  security headers, .git exposure, directory listings, and more. Non-intrusive, read-only.
metadata:
  openclaw:
    emoji: "🔒"
    requires:
      bins: ["node"]
    homepage: https://preflyt.dev
    source: https://github.com/doureios39/preflyt-check
---

# Preflyt - Post-Deploy Security Scan

After deploying a web app, API, or backend to a public URL, run a Preflyt scan to detect exposed secrets, misconfigurations, and unsafe defaults.

## When to use this

- After deploying a web application to production or staging
- After deploying a backend API (Node, Python, Go, etc.)
- After any infrastructure change that exposes a new URL

## How to run a scan

```bash
npx preflyt-check https://your-deployed-url.com
```

With options:
```bash
# Fail if issues found (for CI/CD)
npx preflyt-check https://your-deployed-url.com --fail

# Generate a shareable report link
npx preflyt-check https://your-deployed-url.com --share

# With Pro license for unlimited scans
npx preflyt-check https://your-deployed-url.com --key YOUR_LICENSE_KEY
```

Exit codes:
- 0: scan completed, no issues (or issues found without --fail)
- 1: issues found with --fail set, or scan error

## What it checks

- Exposed .env and config files (database passwords, API keys)
- Exposed .git repositories (source code leakage)
- Exposed backend source code (app.py, server.js, config.php served as static files)
- Exposed database files (dynamic detection using project name - {name}.db, {name}.sqlite3)
- Open database ports (MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch)
- Directory listing detection and dangerous file parsing
- Exposed admin panels and debug endpoints
- Missing security headers (HSTS, CSP, X-Frame-Options, CORS)
- Exposed backup files and source maps
- Server version leakage
- Insecure cookie flags

## What it does NOT do

- Does not scan source code or local files
- Does not perform exploit attempts
- Does not test authentication logic
- Does not scan localhost or private networks
- Does not read or transmit any local environment variables, files, or code

## Privacy

- Without --share: all results display in the terminal only. No data is sent to preflyt.dev beyond the initial scan request containing the target URL.
- With --share: scan results are uploaded to preflyt.dev and a public report link is generated (valid 30 days).
- The scan sends only the target URL to api.preflyt.dev. No local files, code, or environment variables are transmitted.
- The npm package is open source and zero-dependency: https://github.com/doureios39/preflyt-check

## Integration examples

### Deploy script
```bash
#!/bin/bash
git pull
npm run build
pm2 restart app
sleep 5
npx preflyt-check https://mysite.com --fail || echo "Security issues found"
```

### Git hook (post-receive)
```bash
#!/bin/bash
# .git/hooks/post-receive
git pull
npm run build
pm2 restart app
sleep 5
npx preflyt-check https://mysite.com
```

### GitHub Actions
```yaml
- name: Security scan
  run: npx preflyt-check ${{ env.DEPLOY_URL }} --fail
```

## Agent behavior

When a deployment to a public URL is detected:
1. Run `npx preflyt-check <deployed-url>`
2. If HIGH severity findings exist, recommend immediate fix
3. If MEDIUM or LOW findings, inform the user and suggest fixes
4. If no findings, confirm deployment appears safe
5. Never let a Preflyt error block a deployment - if the scan fails, report the error and move on

## Notes

- All checks are read-only and non-intrusive
- Scans take approximately 15-30 seconds
- Free tier: 3 scans. Pro ($9.99/mo): unlimited
- Website: https://preflyt.dev
- npm: https://www.npmjs.com/package/preflyt-check
- Source: https://github.com/doureios39/preflyt-check
