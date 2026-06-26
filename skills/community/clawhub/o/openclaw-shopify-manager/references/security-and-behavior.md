# Security and behavior

This skill is intentionally narrow.

## What it does

- generates Shopify OAuth install URLs
- exchanges OAuth callback codes for Shopify offline access tokens
- validates Shopify callback and webhook HMAC signatures
- runs a small local HTTP server for `/healthz`, OAuth callback handling, and webhook receipt
- performs explicit Shopify Admin GraphQL reads and user-confirmed writes

## What it does not do

- no remote code execution
- no shelling out to download or run third-party installers
- no persistence outside the configured runtime directory
- no browser automation
- no credential exfiltration or forwarding to third-party services
- no background tunneling binary, SOCKS proxy, VPN client, or reverse shell
- no self-update or self-modifying behavior

## Default exposure model

- connector binds to `127.0.0.1` by default
- public HTTPS exposure is expected to be provided by the operator using existing infrastructure
- Tailscale usage in this skill is documentation for operator-managed ingress, not a bundled tunnel client

## Data handling

- OAuth tokens are stored locally in the operator-controlled runtime `.env`
- webhook logs record metadata plus a body checksum/size, not full payload bodies, unless the operator modifies the script
- OAuth state is one-time and removed after successful callback exchange

## Mutation posture

- default to read-first workflows
- mutation helpers exist for explicit Shopify content/product updates
- destructive or store-changing actions should require user confirmation in normal agent use
