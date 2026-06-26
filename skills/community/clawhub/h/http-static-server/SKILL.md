---
name: http-static-server
description: Start an ad-hoc HTTP static file server in the current directory using one-line commands across 25+ languages and tools. Auto-detects available runtimes and recommends the best option.
homepage: https://gist.github.com/willurd/5720255
{"author":"flowerwrong","version":"2026.3.10","sdk_version":"1.4.0","updated":"2026-03-10"}
---

# HTTP Static Server One-Liners

Start an ad-hoc HTTP static file server serving the current (or specified) directory.
Default: `http://localhost:8000`

Reference: <https://gist.github.com/willurd/5720255>
Detailed per-language docs: `{baseDir}/references/`

## When to use this skill

- User needs to quickly serve static files (HTML/CSS/JS/images) locally
- User asks "how do I start a local web server" or similar
- User wants to preview a static site, share files over LAN, or test frontend assets
- User needs a quick HTTP server for development or testing

## Quick Reference Table

| Language/Tool | Command | Dir Listing | Install Needed |
|---|---|---|---|
| **Python 3** | `python3 -m http.server 8000` | Yes | No |
| Python 2 | `python -m SimpleHTTPServer 8000` | Yes | No |
| Twisted | `twistd -n web -p 8000 --path .` | Yes | `pip install twisted` |
| **Node.js (npx)** | `npx http-server -p 8000` | Yes | No |
| Node.js (serve) | `npx serve -l 8000` | Yes | No |
| node-static | `npx node-static -p 8000` | No | No |
| **Deno** | `deno run --allow-net --allow-read jsr:@std/http/file-server` | Yes | No |
| **PHP** | `php -S 127.0.0.1:8000` | No | No |
| **Ruby** | `ruby -run -ehttpd . -p8000` | Yes | No |
| Ruby (WEBrick) | `ruby -rwebrick -e'WEBrick::HTTPServer.new(:Port=>8000,:DocumentRoot=>Dir.pwd).start'` | Yes | No |
| Ruby (adsf) | `adsf -p 8000` | No | `gem install adsf` |
| Ruby (Sinatra) | `ruby -rsinatra -e'set :public_folder,".";set :port,8000'` | No | `gem install sinatra` |
| **Go** | `go run github.com/goware/webify@latest -port 8000 .` | Yes | No |
| **Java 18+** | `jwebserver -d . -b 0.0.0.0 -p 8000` | Yes | No |
| Java (module) | `java -m jdk.httpserver -d . -b 0.0.0.0 -p 8000` | Yes | No |
| **Rust** | `miniserve -p 8000 .` | Yes | `cargo install miniserve` |
| Perl (Plack) | `plackup -MPlack::App::Directory -e 'Plack::App::Directory->new(root=>".");' -p 8000` | Yes | `cpan Plack` |
| Perl (Brick) | `perl -MHTTP::Server::Brick -e '$s=HTTP::Server::Brick->new(port=>8000);$s->mount("/"=>{path=>"."});$s->start'` | Yes | `cpan HTTP::Server::Brick` |
| Perl (Mojo) | `perl -MMojolicious::Lite -MCwd -e 'app->static->paths->[0]=getcwd;app->start' daemon -l http://*:8000` | No | `cpan Mojolicious::Lite` |
| Erlang | `erl -s inets -eval 'inets:start(httpd,[...]).'` | No | No |
| **Elixir** | `elixir --no-halt -e 'Application.start(:inets);:inets.start(:httpd,...)'` | No | No |
| BusyBox | `busybox httpd -f -p 8000` | Yes | No |
| lighttpd | `lighttpd -Df - <<< ...` | Configurable | `brew install lighttpd` |
| webfs | `webfsd -F -p 8000` | Yes | `apt install webfs` |
| Algernon | `algernon -x . :8000` | Yes | `brew install algernon` |
| Docker (Nginx) | `docker run --rm -v "$PWD":/usr/share/nginx/html:ro -p 8000:80 nginx` | Configurable | Docker |
| Docker (PHP) | `docker run -it --rm -v "$PWD":/app -w /app -p 8000:8000 php:8.2-cli php -S 0.0.0.0:8000` | No | Docker |
| PowerShell (Pode) | `Start-PodeStaticServer -Port 8000 -FileBrowser -Address 0.0.0.0` | Yes | `Install-Module Pode` |
| IIS Express | `iisexpress.exe /path:C:\MyWeb /port:8000` | No | Windows |

## Decision guide for the agent

1. **Detect runtimes**: Check which runtimes are available (`python3 --version`, `node --version`, `deno --version`, etc.).
2. **Default to Python 3** — pre-installed on most Linux/macOS systems.
3. **Node.js project context** — prefer `npx serve` or `npx http-server`.
4. **Deno project context** — use the `jsr:@std/http/file-server`.
5. **Minimal environment** (containers, embedded) — use `busybox httpd`.
6. **Windows without WSL** — use PowerShell (Pode) or IIS Express.
7. **Need features** (upload, auth, HTTPS) — recommend `miniserve` (Rust) or Algernon.
8. **No runtime available** — suggest Docker approach.
9. Always confirm the desired **port** (default 8000) and **directory** (default `.`).
10. For per-language details, flags, and advanced usage, see `{baseDir}/references/<language>.md`.

## Common options

| Need | Solution |
|---|---|
| Custom port | Replace `8000` with desired port in any command |
| Serve a specific directory | Append the path or use the tool's directory flag |
| Bind to all interfaces (LAN) | Use `0.0.0.0` as the bind address |
| CORS headers | `npx http-server --cors` or add middleware |
| HTTPS | `miniserve --tls-cert/--tls-key`, reverse proxy, or `openssl s_server` |
| Directory listings | Python, http-server, Plack, miniserve, BusyBox support by default |
| File upload | `miniserve --upload-files` |
| Authentication | `miniserve --auth user:password` |
| Docker (no local runtime) | See `{baseDir}/references/docker.md` |

## Per-language reference docs

Detailed documentation with full flags, install instructions, and advanced usage:

- `{baseDir}/references/python.md` — Python 3, Python 2, Twisted
- `{baseDir}/references/nodejs.md` — http-server, serve, node-static, inline
- `{baseDir}/references/deno.md` — std/http file-server
- `{baseDir}/references/php.md` — Built-in dev server, Docker
- `{baseDir}/references/ruby.md` — ruby -run, WEBrick, adsf, Sinatra
- `{baseDir}/references/go.md` — webify, inline Go
- `{baseDir}/references/rust.md` — miniserve, http
- `{baseDir}/references/java.md` — jwebserver, jdk.httpserver, inline
- `{baseDir}/references/perl.md` — Plack, HTTP::Server::Brick, Mojolicious
- `{baseDir}/references/erlang.md` — inets
- `{baseDir}/references/elixir.md` — :inets, Plug
- `{baseDir}/references/busybox.md` — busybox httpd
- `{baseDir}/references/docker.md` — Nginx, PHP, Python, Alpine
- `{baseDir}/references/powershell.md` — Pode, .NET HttpListener, IIS Express
- `{baseDir}/references/lighttpd.md` — inline config, config file
- `{baseDir}/references/webfs.md` — webfsd
- `{baseDir}/references/algernon.md` — static mode, Lua scripting
