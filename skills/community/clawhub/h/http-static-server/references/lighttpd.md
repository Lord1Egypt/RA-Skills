# lighttpd HTTP Static Server

## Inline configuration

```bash
lighttpd -Df - << EOF
server.document-root = "$PWD"
server.port = 8000
EOF
```

With directory listing:

```bash
lighttpd -Df - << EOF
server.document-root = "$PWD"
server.port = 8000
dir-listing.activate = "enable"
EOF
```

Bind to all interfaces:

```bash
lighttpd -Df - << EOF
server.document-root = "$PWD"
server.port = 8000
server.bind = "0.0.0.0"
EOF
```

Features:
- Directory listing: Configurable (`dir-listing.activate`)
- Production-grade lightweight server
- Low memory footprint
- Module system for extended functionality
- Flags: `-D` (don't daemonize), `-f` (config from file/stdin)

## With config file

Create `lighttpd.conf`:

```
server.document-root = "/path/to/dir"
server.port = 8000
server.bind = "0.0.0.0"
dir-listing.activate = "enable"
mimetype.assign = (
    ".html" => "text/html",
    ".css"  => "text/css",
    ".js"   => "text/javascript",
    ".json" => "application/json",
    ".png"  => "image/png",
    ".jpg"  => "image/jpeg"
)
```

```bash
lighttpd -Df lighttpd.conf
```

## Install

- macOS: `brew install lighttpd`
- Debian/Ubuntu: `apt install lighttpd`
- Alpine: `apk add lighttpd`
