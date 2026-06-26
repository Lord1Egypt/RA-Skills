# Preflyt

Post-deployment security scanner. Checks your live web app for exposed secrets, databases, source code, open ports, and missing security headers.

## What It Does

After your agent deploys an app, Preflyt scans the live URL from the outside (same perspective an attacker has) and reports misconfigurations in 30 seconds.

## How to Use

Your agent runs this after any deploy:
```bash
npx preflyt-check https://your-site.com
```

Or add the SKILL.md to your project and the agent picks it up automatically.

## Examples

- Agent deploys a Next.js app to Vercel, then runs `npx preflyt-check` to verify nothing is exposed
- Agent sets up a VPS backend, then scans for open database ports, exposed source code, and missing headers
- Agent deploys a vibe-coded app, scan detects the SQLite database is downloadable at {projectname}.db
- CI pipeline runs the check with `--fail` to block deploys with HIGH severity findings

## Requirements

- Node.js (for npx)
- Public URL to scan (no localhost)

## Troubleshooting

- **Scan blocked (403):** Site has bot protection enabled. Wait or scan manually at preflyt.dev
- **Timeout:** URL may not be reachable. Verify the deployment is live first
- **Rate limit:** Free tier is 3 scans. Use `--key` flag with a Pro license for unlimited
