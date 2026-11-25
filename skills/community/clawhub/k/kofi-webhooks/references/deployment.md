# Deploy, verify, activate, and operate Ko-fi webhooks

This deployment option requires a Linux host with Python 3.10+, Nginx HTTPS, and systemd supporting `DynamicUser`, `StateDirectory`, and `LoadCredential`. Validate those features on the target host. The receiver itself is cross-platform. Hostnames, SSH identities, credentials, and delivery receipts are supplied by the user and remain outside this skill.

## Templates and scope

Resolve the following relative to the skill root:

- `scripts/kofi_webhooks.py`: stdlib HTTP receiver and private CLI reports.
- `scripts/render_deployment.py`: offline renderer; writes a new output directory and never installs, uploads, or contacts a service.
- `assets/kofi-webhooks.service.tmpl`: dynamic-user, loopback-only receiver, private state directory, systemd credential loading, production DB default, restart-on-failure, boot target.
- `assets/testing.conf.tmpl`: isolated test database override.
- `assets/nginx-location.conf.tmpl`: exact HTTPS `/kofi` POST route, body limit and timeouts; no public data-read route.

Render reviewable files locally before installation. For example (resolve the script relative to the skill directory):

```sh
python scripts/render_deployment.py --output ./rendered-kofi --name creator-payments --port 9191 --app-dir /srv/creator-payments --config-dir /etc/creator-payments --python /usr/bin/python3
```

Options have conventional Linux defaults, not a dependency on a particular account or server. `--name` controls the unit filename and systemd state-directory name; `--port` controls both receiver and proxy; the app/config paths and Python executable are configurable. The state directory is `/var/lib/<name>` because systemd manages `StateDirectory` there for a system service. Paths must be normalized absolute Linux paths without whitespace or systemd specifiers. For a different layout, adapt the unit and permissions together. Keep `%d/verification-token` intact: `%d` is a systemd credential-directory specifier.

The output contains a service unit, `testing.conf`, `nginx-location.conf`, and a secret-free `deployment.json` recording the selected values. Use that manifest throughout the steps below. It deliberately contains no domain or SSH account: choose an existing approved HTTPS host and endpoint such as `https://example.com/kofi`. Do not install `.tmpl` files directly or provision infrastructure merely to use this flow. Keep rendered host-specific artifacts outside the published skill.

## 1. Inspect and prepare

1. Read the supplied verification token from its private file; confirm nonempty without printing it. If it is missing, ask the user to save it locally from Ko-fi Webhooks. Never put it in the skill, Git, a command argument, logs, or the web root.
2. Inspect the selected host via SSH: Python 3.10+, existing HTTPS server block, `nginx -t`, current `/kofi` route, service/unit paths, and the selected backend port's availability. Stop first-install logic on existing deployment paths and inspect ownership/current state; do not overwrite unknown work.
3. Prepare the rendered helper installation, unit, test override, and exact-location insertion. Reuse approved public HTTPS with the backend bound only to `127.0.0.1` at the configured port; no new public backend port is needed. Keep `/healthz` internal. Check that the exact route does not conflict with existing configuration.
4. If deployment has not yet been authorized, present the endpoint and persistent-service changes for approval after preparation. Carry out previously authorized deployment steps without another permission loop.

## 2. Apply the authorized deployment

Take a byte-verified backup of the current Nginx file outside served roots. Keep a receipt of backup path and intended changes. Install:

| Resource | Location / permissions |
| --- | --- |
| Receiver | Manifest `app_dir` + `/kofi_webhooks.py`, root-owned 0755; parent directories traversable by service |
| Token directory | Manifest `config_dir`, root-owned 0700 |
| Token file | Manifest `config_dir` + `/verification-token.txt`, root-owned 0600 |
| Unit | Manifest `service` filename under the host's systemd system-unit directory, 0644 |
| Initial test override | Corresponding `<service>.d/testing.conf` in that system-unit directory, 0644 |
| State | Manifest `state_dir`, managed privately by systemd `StateDirectory` |

Transfer the token through encrypted SSH stdin (for example a Python subprocess reading the file and passing bytes as stdin), not shell interpolation, remote command text, or a publicly accessible staging file. `LoadCredential` supplies it to the dynamic service user; do not make the root token readable to everyone to fix service access.

Run `systemd-analyze verify` on the rendered unit, `systemctl daemon-reload`, and start the configured service. Verify internal `/healthz`. The test override must select `test-events.sqlite3` under the manifest's `state_dir` before any valid-token test POST.

Insert only the template's exact location into the chosen HTTPS server block. Do not replace whole site files from an old snapshot or add the route to every virtual host. Run `nginx -t` before reload. On failure restore the byte-verified original, validate it, and do not activate the broken configuration. Verify the existing homepage after reload. Enable the approved service; verify both `is-active` and `is-enabled` rather than treating start success as boot persistence.

## 3. External synthetic check, isolated from real payments

Confirm the effective service environment selects the test DB, then from outside the server:

1. Send a URL-encoded `data` field containing JSON to the HTTPS `/kofi` URL. Read the verification token from the private file at request time. Use a unique tracked synthetic `message_id`, `type=Donation`, `amount=1.00`, and `currency=EUR` (strings), with no real supporter data.
2. Require HTTP 200 and `accepted=true`. Replay the same message; require HTTP 200 and `duplicate=true` with exactly one new stored row overall.
3. Send a wrong-token event with another ID; require HTTP 403 and no new row.
4. Confirm the token field is absent from stored payloads without displaying payloads. Restart the receiver, check internal health, verify the row survived, and replay the same ID to confirm deduplication survives restart too.
5. Verify the original homepage still returns successfully. Record synthetic IDs, aggregate counts, HTTP outcomes, active/enabled status, and effective DB path; never record credentials or private supporter payloads in receipts.

An external synthetic pass proves HTTPS delivery mechanics, not that Ko-fi account settings are correct.

## 4. Verify a Ko-fi-originated test

Give the user the exact chosen HTTPS URL and direct them to save it at <https://ko-fi.com/manage/webhooks?src=sidemenu>, then use its test-payment function. If an authenticated browser is already authorized, the agent may perform the authorized settings/test actions there; otherwise let the user perform the account step. No real purchase is needed.

When the user reports saving or testing, inspect stored event IDs/UTC receipt times and the corresponding recent Nginx POST status without dumping supporter details. Exclude all known agent-generated synthetic IDs. Correlate the distinct authenticated delivery with the Ko-fi test action and HTTP 200. If origin is ambiguous, ask for a specific test action rather than declaring account connection verified. If no event has arrived, ask the user to use the test function; saving the URL alone is not evidence.

## 5. Activate production once, preserving tests

After the initial live test is verified:

1. Confirm this is a first activation and that the intended production DB does not contain existing payment history. Do not truncate or replace an existing production DB.
2. Move **only this deployment's** `testing.conf` outside the active drop-in directory into the private deployment backup. Keep the test DB and receipt. Do not remove other drop-ins.
3. Run `systemctl daemon-reload` and restart the configured service. Verify the effective environment selects `events.sqlite3` under the manifest's `state_dir`, internal health is OK, and the service is active and enabled.
4. Check production starts with zero records and test records remain unchanged. Do not insert synthetic events into production to prove it works. If real payments arrive during activation, inspect and preserve them instead of enforcing emptiness destructively.
5. Record the endpoint, live-delivery evidence, production DB path and startup status in workspace notes. Distinguish successful activation from historical-payment import or fulfillment automation, neither of which this receiver performs.

For later re-tests of an already-live receiver, do not casually switch the only endpoint to a test DB: real payments may arrive there too. Plan an isolated test route/receiver or explicitly account for all deliveries in a controlled window before returning to production. Preserve records; never infer test status from supporter names/emails or blindly copy all test rows into production.

## Operate an existing receiver

Obtain the actual SSH target/key and deployment manifest from the user's configuration. Perform reports on the host holding the live database. In the remote shell, assign `SERVICE`, `PYTHON`, `HELPER`, `PROD_DB`, and `PORT` from that configuration (`HELPER` is `app_dir` plus `/kofi_webhooks.py`; `PROD_DB` is `state_dir` plus `/events.sqlite3`). Then run:

```sh
sudo systemctl is-active "$SERVICE"
sudo systemctl is-enabled "$SERVICE"
sudo systemctl show "$SERVICE" --property=Environment --value
curl --fail --silent "http://127.0.0.1:${PORT}/healthz"
sudo "$PYTHON" -B "$HELPER" --db "$PROD_DB" summary
sudo "$PYTHON" -B "$HELPER" --db "$PROD_DB" list --limit 20
```

Keep `--db` before the subcommand. Exports use the same explicit production DB and a private, previously nonexistent output file. Default exports redact private fields; use `--include-private` only when the requested output calls for those fields. For DynamicUser state directories, use authorized administrative read access rather than weakening directory permissions.

Token rotation: replace the private token securely only when requested, restart to reload credentials, and coordinate the Ko-fi settings change. Never print or compare token contents in logs. Updating the local skill helper does not update the deployed copy; compare hashes and deploy an update only within the requested scope.

## Diagnose and recover

| Symptom | Next check |
| --- | --- |
| No delivery | Ko-fi URL saved and test actually sent; DNS/TLS; Nginx POST status; effective test/production DB |
| HTTP 403 | POST versus browser GET (GET is intentionally denied); token source and receiver restart after rotation |
| HTTP 400/411/413 | URL-encoded `data` JSON, Content-Length, required field types, body size |
| HTTP 502 | Unit active, credential loading, loopback listener, proxy destination |
| HTTP 503 | Private state directory access, disk availability, SQLite write/lock failure; storage must succeed before acknowledgement |
| Unexpected zero report | Remote production DB selected, not local default or test DB |

Use sanitized service logs and status metadata. A startup message reporting `live_delivery_verified=false` is not a durable connection-status record; the helper emits it on every start. Verify actual delivery receipts instead.

Rollback only this deployment: stop/disable its service if rollback is authorized, restore the verified matching Nginx backup, run `nginx -t`, then reload. Retain private token/state for review. Do not disable unrelated services or delete payment records. If a step fails, inspect partial state and recover it; do not rerun first-install scripts blindly.
