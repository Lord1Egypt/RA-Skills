# http-static-server

An [OpenClaw](https://docs.openclaw.ai/tools/skills) skill that helps AI agents (and humans) quickly start an HTTP static file server using **one-line commands** across 25+ languages and tools.

Based on the classic gist: [Big list of http static server one-liners](https://gist.github.com/willurd/5720255)

## Install

```bash
openclaw install http-static-server
```

Or manually copy `SKILL.md` and the `references/` directory into your skills folder.

## Supported Languages & Tools

| Category | Tools |
|---|---|
| **Python** | http.server (3.x), SimpleHTTPServer (2.x), Twisted |
| **JavaScript** | http-server, serve, node-static (Node.js), Deno std |
| **Ruby** | ruby -run, WEBrick, adsf, Sinatra |
| **PHP** | Built-in dev server |
| **Go** | webify |
| **Rust** | miniserve, thecoshman/http |
| **Java** | jwebserver (18+), jdk.httpserver |
| **Perl** | Plack, HTTP::Server::Brick, Mojolicious |
| **Erlang/Elixir** | inets, Plug |
| **System** | BusyBox, lighttpd, webfs, Algernon |
| **Container** | Docker (Nginx, PHP, Python, Alpine) |
| **Windows** | PowerShell (Pode), IIS Express |

## Quick Start

The most common choices:

```bash
# Python (pre-installed on most systems)
python3 -m http.server 8000

# Node.js (zero-install via npx)
npx http-server -p 8000

# Deno
deno run --allow-net --allow-read jsr:@std/http/file-server

# PHP
php -S 127.0.0.1:8000

# Ruby
ruby -run -ehttpd . -p8000

# Java 18+
jwebserver -d . -p 8000

# Docker (no local runtime needed)
docker run --rm -v "$PWD":/usr/share/nginx/html:ro -p 8000:80 nginx
```

## Project Structure

```
.
├── SKILL.md              # Main skill file (frontmatter + quick reference + agent decision guide)
├── README.md             # This file
└── references/           # Detailed per-language documentation
    ├── python.md
    ├── nodejs.md
    ├── deno.md
    ├── php.md
    ├── ruby.md
    ├── go.md
    ├── rust.md
    ├── java.md
    ├── perl.md
    ├── erlang.md
    ├── elixir.md
    ├── busybox.md
    ├── docker.md
    ├── powershell.md
    ├── lighttpd.md
    ├── webfs.md
    └── algernon.md
```

## How It Works

When an AI agent receives a request like "start a local web server", this skill:

1. Checks which runtimes are available on the user's system
2. Recommends the best option (defaults to Python 3)
3. Provides the exact one-liner command
4. Offers alternatives if the preferred runtime isn't installed

The agent can also consult the detailed `references/` docs for advanced flags, HTTPS setup, CORS configuration, and more.

## Common Options

| Need | Solution |
|---|---|
| Custom port | Replace `8000` with desired port |
| Specific directory | Append the path or use the tool's `-d`/`-t` flag |
| LAN access | Bind to `0.0.0.0` |
| CORS | `npx http-server --cors` |
| HTTPS | `miniserve --tls-cert cert.pem --tls-key key.pem` |
| File upload | `miniserve --upload-files` |
| Authentication | `miniserve --auth user:password` |

## License

Public domain. The original gist is a community-maintained collection.
