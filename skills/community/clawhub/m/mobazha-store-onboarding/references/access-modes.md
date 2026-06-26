# Mobazha Access Modes

Quick reference for the three ways to run a Mobazha store. Each mode has different URLs, authentication, and MCP connection methods.

## Mode Comparison

| | SaaS Platform | VPS Standalone | NAT / Local |
|---|---|---|---|
| **What it is** | Hosted at `app.mobazha.org` | Docker on a VPS with public IP | Native binary or Docker on your own machine |
| **Who it's for** | Quick start, no server needed | Full control, custom domain | Personal use, development, LAN selling |
| **Admin URL** | `app.mobazha.org` (dashboard after login) | `https://shop.example.com/admin` or `http://<IP>/admin` | Docker: `http://localhost/admin`; Native: `http://localhost:5102/admin` |
| **Login method** | OAuth (Google, GitHub, or email) | Admin password (set during onboarding) | Admin password (set during onboarding) |
| **Onboarding** | UI wizard after first login | Setup Wizard at `/admin` (4 steps, API-automatable) | Same as VPS |
| **MCP connection** | SSE at `https://app.mobazha.org/platform/v1/mcp/sse` | SSE at `https://shop.example.com/platform/v1/mcp/sse` (or SSH tunnel) | SSE at `http://localhost:5102/platform/v1/mcp/sse` |
| **MCP auth** | API Token (from Admin > Settings > API) | Bearer Token (from `/platform/v1/auth/tokens`) | Bearer Token (same as VPS) |
| **Public access** | Always public via `app.mobazha.org` | Public via domain or IP | LAN only (unless Tor overlay or P2P enabled) |
| **Setup skill** | N/A (sign up online) | `standalone-setup` | `native-install` |

## Key Differences by Topic

### Authentication

- **SaaS**: Sign in with Google, GitHub, or email. No local password.
- **VPS / NAT**: Set an admin password on first visit to `/admin`. All API calls use Bearer Token obtained from `/platform/v1/auth/tokens`.

### MCP Token

- **SaaS**: Generate an API token from the admin dashboard (Settings > API).
- **VPS / NAT**: Obtain a Bearer token via the auth endpoint:

  ```
  POST /platform/v1/auth/tokens
  ```

### Network Access

- **SaaS**: Globally accessible. No firewall or DNS configuration needed.
- **VPS**: Accessible via public IP or custom domain. Requires port 80/443 open.
- **NAT**: Only accessible within the local network. For external access, options include:
  - Tor hidden service (see `tor-browsing` skill)
  - P2P network (other Mobazha nodes can find you)
  - Port forwarding or VPN (manual setup)

### Default Ports

| Service | SaaS | VPS Standalone | NAT / Local (Docker) | NAT / Local (native) |
|---------|------|---------------|---------------------|---------------------|
| Web UI | 443 (HTTPS) | 80/443 (Caddy proxy) | 80 (Caddy proxy) | 5102 |
| Gateway API | managed | same as web (proxied) | same as web (proxied) | 5102 |
| LibP2P | managed | 4001 | 4001 | 4001 |
