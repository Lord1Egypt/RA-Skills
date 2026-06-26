# systemd

## Why use systemd

Use systemd when the Shopify connector must keep running for callbacks, webhooks, and operational reliability.

This guide applies to host and VM deployments. If the connector runs in Docker, use your container runtime instead of trying to force normal systemd service management into the container.

Benefits:

- survives shell disconnects
- starts on boot
- easy `start|stop|restart|status`
- logs available via `journalctl`

## Service model

The bundled service template runs the connector with:

- working directory set to the runtime root
- env file loaded from `.env`
- restart policy enabled
- local bind only

Use `assets/shopify-connector.service` as the template.

## Manual lifecycle management

This skill intentionally ships documentation and a service template, not a privileged installer helper.

Use `assets/shopify-connector.service.txt` as the template, rename it locally to `shopify-connector.service`, then manage the service with standard host commands:

- `cp shopify-connector.service.txt shopify-connector.service`
- `sudo install -m 0644 shopify-connector.service /etc/systemd/system/shopify-connector.service`
- `sudo systemctl daemon-reload`
- `sudo systemctl enable shopify-connector.service`
- `sudo systemctl start shopify-connector.service`
- `systemctl --no-pager --full status shopify-connector.service`
- `journalctl -u shopify-connector.service -n 100 --no-pager`

## Typical flow

1. Prepare runtime root with config and `.env`
2. Copy and adjust the service template if needed
3. Install the service file manually
4. Start it with `systemctl`
5. Verify local `healthz`
6. Expose with Tailscale Serve/Funnel if desired

## Logging

For recent logs:

```bash
journalctl -u shopify-connector.service -n 100 --no-pager
```

Or use the helper script `logs` command.

## Common failure points

- wrong working directory
- wrong path to the connector script
- `.env` missing required Shopify values
- callback URL mismatch with Shopify app settings
- service running, but public path not exposed
