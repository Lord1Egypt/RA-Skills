# nginx and NPM

## nginx

Homebrew `nginx` is useful on a Mac when you want:

- reverse-proxy behavior closer to production
- alternate port testing
- static asset serving comparisons
- PHP-FPM fronting instead of Apache module mode

By default, Homebrew nginx listens on `8080` so it can run without sudo.

## Nginx Proxy Manager

Nginx Proxy Manager is optional for this skill.

Use it only when you actually need:

- many local hostnames
- a browser UI for proxy routing
- certificate testing in a more complex local setup

Do not make NPM the default for a simple local PHP staging server. It adds extra operational weight and is usually better as a separate Docker-based layer.
