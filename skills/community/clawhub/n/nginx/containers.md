# Containers — nginx in Docker and Kubernetes

Container-side fundamentals (networks, volumes, resource limits) are the `docker` skill; this file is what changes about NGINX when it runs in one.

## The Container Contract

- Foreground only: the official image runs `nginx -g "daemon off;"`. A custom CMD that lets nginx daemonize makes PID 1 exit → the container "starts and immediately stops" with a clean exit code.
- Logs to the streams: the official image symlinks `/var/log/nginx/access.log → /dev/stdout` and `error.log → /dev/stderr`. Custom images replicate the symlinks or set the paths directly — a file inside the container is invisible to `docker logs` and fills the writable layer.
- `worker_processes auto` reads HOST CPUs, not the cgroup quota (SKILL.md Traps) — set it to the container's CPU limit explicitly.
- Reload without restart: `docker exec <c> nginx -s reload` (or signal HUP to PID 1). Restarting the container drops every in-flight connection for a config change that reload applies gracefully.

## DNS for Dynamic Backends

- Docker: embedded resolver at `127.0.0.11`; Compose service names resolve there. The startup-cache 502 and the variable+`resolver` fix are in `proxy.md` (The DNS Trap).
- Kubernetes: use the resolver from the pod's `/etc/resolv.conf` (CoreDNS ClusterIP) rather than hardcoding. Proxying to a Service ClusterIP is stable (the IP survives pod churn — the DNS trap mostly bites headless Services and ExternalName records).
- `resolver ... valid=10s` overrides TTL; without a `resolver` directive, variable-based `proxy_pass` fails at request time, not at startup — it looks fine until traffic arrives.

## Config Injection (official image templates)

- Files in `/etc/nginx/templates/*.template` pass through `envsubst` into `/etc/nginx/conf.d/` at startup — the supported way to inject ports/hosts per environment.
- The collision trap: `envsubst` substitutes every `${var}` whose name matches a DEFINED environment variable — an env var that happens to share a name with an nginx variable silently empties it in the rendered config. Scope substitution with `NGINX_ENVSUBST_FILTER` (regex of allowed names), and prefer `$host` (no braces) for nginx variables in templates since envsubst in this image only rewrites the `${...}` form it's told to.
- Debug a bad render by printing the OUTPUT, not the template: `docker exec <c> cat /etc/nginx/conf.d/default.conf`.

## Unprivileged & Read-Only

- Root is needed only to bind <1024 and read root-owned certs. For `runAsNonRoot` policies use `nginxinc/nginx-unprivileged` (listens on 8080, pid file relocated) or listen ≥1024 in your own image — the bind failure is `(13: Permission denied)` (`debug.md`).
- Read-only root filesystem: nginx still needs writable `/var/cache/nginx` (proxy/fastcgi temp and cache) and the pid location — mount tmpfs/emptyDir there, or large uploads and buffered responses start failing with write errors while small requests work.
- Client body spooling also writes to disk: `client_body_temp_path` must be on the writable mount when bodies exceed `client_body_buffer_size`.

## Kubernetes Specifics

- ConfigMap-mounted config: kubelet syncs changes with a delay (up to about a minute) and nginx does NOT reload itself when the file changes. Either roll the Deployment (config change = new pod, the clean default) or run a reloader sidecar that signals HUP.
- Probes: `location = /healthz { access_log off; return 200; }` — a static 200 answers "is nginx up". Only make the probe hit `proxy_pass` if you WANT the pod restarted when the backend is down (usually you don't — that's the backend's own probe's job).
- Graceful shutdown: on SIGTERM nginx (as shipped) quits gracefully, but long-lived WebSocket connections hold old workers — set `worker_shutdown_timeout` below the pod's `terminationGracePeriodSeconds` or pods hang in Terminating.
- Behind an ingress controller you are the SECOND proxy: realip must trust the ingress (`set_real_ip_from` the pod/ingress CIDR), `X-Forwarded-*` arrives pre-populated (append, don't overwrite), and WebSocket upgrade headers must be configured at BOTH hops (`proxy.md`).

## Compose Reference Shape

```yaml
services:
  nginx:
    image: nginx:1.27
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - certs:/etc/letsencrypt:ro
    depends_on:
      app: { condition: service_healthy }
```

- Mount config read-only — a compromised nginx that can rewrite its own config can re-route traffic.
- `depends_on` with a health condition prevents the startup-order 502 (nginx resolves and connects before the app listens); the resolver fix still applies for RESTARTS after startup.
- Pin the image minor version: nginx point releases change directive defaults rarely but visibly (`http2` directive form, `ssl_reject_handshake` availability — version floors are noted where they matter, e.g. `ssl.md`).
