# Controller Surface

Use this file when you need a lightweight Mac-side controller for staging work.

## Goal

Keep the controller small and boring.

It should be able to:

- start or stop local services
- run build steps
- render a local-only gateway/dev-controller env
- emit receipts for every action
- feed sandbox test data into a CRM or Markdown viewer

It should not try to become the production gateway.

## Minimal API Surface

Prefer a tiny action set:

- `status`
- `start <service>`
- `stop <service>`
- `restart <service>`
- `build <target>`
- `seed <fixture>`
- `verify`
- `receipt <action>`

That can be implemented as:

- a shell wrapper
- a local HTTP service bound to `127.0.0.1`
- or a small task runner

Avoid a large generic remote-exec surface.

## Authentication And Trust

- loopback only by default
- token or local-user trust when HTTP is used
- explicit action allowlist
- no public network exposure

If the controller talks to the Ryzen gateway, treat that as a separate trust boundary.

## Logging

Every action should leave a receipt containing:

- timestamp
- action
- target
- status
- short detail

Use `scripts/write-receipt.sh` for that baseline.

## Failure Mode

If the controller fails:

- Apache/PHP/MariaDB staging should keep running if already started
- SFTP should remain available if previously enabled
- the main Ryzen gateway should remain unaffected
