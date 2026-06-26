---
name: mac-dev-staging
description: Turn a macOS machine into a local PHP/MariaDB staging server using the stock macOS Apache, Homebrew PHP 8.5, MariaDB, built-in SFTP, npm tooling, a local dev gateway surface, and optional nginx. Use when you want a Mac node to act like a local development or staging box for Joomla, WordPress, CodeIgniter, Laravel, or other PHP apps without improvising the stack every time.
metadata: {"openclaw":{"emoji":"🧪"}}
---

# Mac Dev Staging

Use this skill when you want a Mac to behave like a repeatable local development or staging server.

This skill is built around the stack you actually have on modern Apple Silicon Macs:

- stock macOS Apache (`/usr/sbin/httpd`)
- Homebrew PHP 8.5
- Homebrew MariaDB
- built-in macOS SSH/SFTP
- npm-managed JS tooling for local build/test workflows
- a development-local gateway surface that coexists with the main OpenClaw gateway
- optional Homebrew nginx

It does not assume a Linux-style package layout, and it does not pretend the Mac should behave exactly like your Ubuntu gateway.

## Use This Skill For

- local PHP staging on a Mac
- Joomla, WordPress, CodeIgniter, Laravel, and similar PHP apps
- enabling PHP 8.5 under the default macOS Apache
- adding MariaDB and a predictable local database setup
- generating vhost files and config snippets instead of hand-editing from memory
- exposing the project over SFTP for deploys, edits, and staging sync
- installing browser-sync and similar JS tooling in a predictable way
- testing a lightweight Mac-local gateway/controller without colliding with the main gateway
- optional nginx fronting or sidecar local testing

## Do Not Use This Skill For

- production internet-facing hosting
- replacing your main Linux gateway
- Docker-first local stacks when you explicitly want containers instead
- pretending the skill can bypass `sudo` for `/etc/apache2` edits

## Reality Check

On macOS, the hard part is not installing PHP or MariaDB. The hard part is making Apache config repeatable and not breaking your box.

This skill therefore follows a staged pattern:

1. detect current state
2. install or verify Homebrew services
3. render safe Apache config snippets
4. tell the operator exactly what needs `sudo`
5. verify the stack after changes
6. verify SFTP when file deployment is part of the workflow
7. keep receipts/logs for automation and staging actions

## Workflow

### 1. Detect The Current Stack

Run:

```bash
scripts/detect-stack.sh
scripts/detect-ports.sh
```

This checks:

- stock Apache version
- whether vhosts are enabled
- whether PHP is installed via Homebrew
- whether MariaDB is installed
- whether nginx is installed
- current `brew services` state
- port conflicts with the main gateway or local JS tooling

### 2. Install The Core Packages

Run:

```bash
scripts/bootstrap-brew.sh
scripts/bootstrap-npm-tooling.sh
```

This installs:

- `php`
- `mariadb`
- `nginx`
- local npm tooling such as `browser-sync`

It does not silently mutate `/etc/apache2`.

### 3. Render Apache + PHP Config

Generate the recommended Apache enablement snippet:

```bash
scripts/render-apache-php-snippet.sh
```

Generate a local vhost:

```bash
scripts/render-vhost.sh \
  --server-name mysite.test \
  --docroot /Users/you/Sites/mysite/public
```

These scripts print the config you should install under:

- `/etc/apache2/httpd.conf`
- `/etc/apache2/extra/httpd-vhosts.conf`

Applying those files still requires `sudo`.

### 4. Enable Services

For Homebrew-managed services:

```bash
brew services start php
brew services start mariadb
brew services start nginx
```

For stock Apache:

```bash
sudo apachectl restart
```

If you want a Mac-local development gateway that coexists with the main Ryzen gateway, render the recommended env first:

```bash
scripts/render-local-gateway-env.sh
```

Default rule:

- main Ryzen gateway stays on `192.168.88.11:18789`
- Mac local dev gateway binds loopback only
- Mac local dev gateway uses a non-conflicting test port such as `28789`

### 5. Verify

Run:

```bash
scripts/verify-stack.sh
```

This checks:

- Apache responds
- PHP CLI is present
- PHP module path is available
- MariaDB socket or TCP port is up
- nginx is running if expected
- expected local ports are either free or intentionally in use
- the local dev gateway test port does not collide with the production gateway

### 6. Enable And Verify SFTP

For staging boxes, SFTP is usually the simplest deploy path.

Check current state:

```bash
scripts/detect-sftp.sh
```

If Remote Login is off, enable it with macOS settings or:

```bash
sudo systemsetup -setremotelogin on
```

Recommended pattern:

- create or choose a dedicated staging user
- keep project files under that user’s home or a clearly owned shared path
- use SFTP for file sync, not broad shell access, when that is enough

Read [references/sftp-on-macos.md](references/sftp-on-macos.md) before exposing the box to other devices on your LAN.

### 7. Receipts And Controller Actions

This skill assumes staging operations should leave a trace.

Use the lightweight controller when you want one stable entrypoint for local service control, build steps, verification, port checks, or gateway ping tests:

```bash
scripts/controller.sh status
scripts/controller.sh verify
scripts/controller.sh build /Users/you/Sites/mysite build
scripts/controller.sh gateway-ping http://127.0.0.1:28789/
```

Use:

```bash
scripts/write-receipt.sh --action "bootstrap-brew" --status ok --detail "Installed php mariadb nginx"
scripts/write-receipt.sh --action "verify-stack" --status ok --detail "Apache php mariadb verified"
```

The receipt trail is for:

- Markdown viewers
- CRM or internal dashboards
- rollback and troubleshooting

Read [references/controller-surface.md](references/controller-surface.md) for the intended lightweight Mac control-plane pattern.

## Default Architecture

Recommended local staging layout:

- Apache on `:80` for the app
- PHP 8.5 loaded into Apache or via PHP-FPM
- MariaDB localhost-only
- SFTP on `:22` for deploy/sync
- optional nginx on `:8080` for alternate reverse-proxy testing
- npm-managed test services on explicit ports like `3000` or `5173`
- optional Mac-local dev gateway on `127.0.0.1:28789`

Keep it simple first. Add Proxy Manager later only if you have a real reason.

## Local Gateway Compatibility

The goal is not to replace the main Ryzen gateway. The goal is to let a Mac run a lightweight local development control surface without colliding with production orchestration.

Recommended rules:

- the main OpenClaw gateway remains the only LAN-facing shared gateway
- the Mac-local development gateway binds `127.0.0.1` only
- the Mac-local development gateway uses a non-default test port such as `28789`
- test controllers talk to the local Mac gateway or controller, not directly to the production gateway, unless the workflow explicitly needs that
- if the local gateway/controller is down, the Mac should still function as a normal node and local staging box

Use:

```bash
scripts/render-local-gateway-env.sh
```

to generate a repeatable local-only environment contract.

## Optional nginx / NPM

`nginx` is easy to support directly through Homebrew.

Nginx Proxy Manager is optional and should be treated as a separate layer, usually containerized. This skill does not auto-install NPM because that adds more moving parts than most local Mac staging setups need.

Read [references/nginx-and-npm.md](references/nginx-and-npm.md) before adding that layer.

## Security Rules

- Keep MariaDB bound to localhost unless you deliberately need remote access
- Treat the Mac as a staging box, not a public server
- Keep local vhosts under explicit hostnames like `mysite.test`
- Never write secrets into generated Apache configs
- Prefer a dedicated staging user for SFTP instead of sharing your main login broadly
- If SFTP is enough for a workflow, do not grant unnecessary shell access
- Do not expose the Mac’s staging stack directly to the public internet
- Keep the Mac-local dev gateway on loopback only by default
- Keep receipts for bootstrap, service changes, and test-controller actions
- Prefer explicit port checks before starting BrowserSync, Vite, nginx, or a local gateway
- If the controller or local gateway fails, the Apache/MariaDB staging stack should continue operating locally

## Files

- `scripts/detect-stack.sh`: inspect the current Mac stack
- `scripts/bootstrap-brew.sh`: install the core Homebrew packages
- `scripts/bootstrap-npm-tooling.sh`: install the baseline npm tooling for local staging workflows
- `scripts/controller.sh`: lightweight Mac-side controller for service/build/verify actions
- `scripts/detect-ports.sh`: check port conflicts for Apache, nginx, JS tooling, and the local gateway
- `scripts/render-apache-php-snippet.sh`: print the Apache PHP 8.5 enablement snippet
- `scripts/render-local-gateway-env.sh`: print a safe local-only gateway env contract
- `scripts/render-vhost.sh`: print a safe vhost block
- `scripts/verify-stack.sh`: verify the final stack
- `scripts/detect-sftp.sh`: inspect built-in macOS SSH/SFTP state
- `scripts/write-receipt.sh`: append auditable action receipts for staging/controller work
- `references/apache-layout.md`: notes on stock macOS Apache
- `references/sftp-on-macos.md`: safe SFTP setup notes for staging
- `references/nginx-and-npm.md`: when nginx or NPM is worth adding
- `references/controller-surface.md`: the lightweight Mac controller pattern
- `references/gateway-coexistence.md`: how to keep local gateway testing separate from the production gateway
