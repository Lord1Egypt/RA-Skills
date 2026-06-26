# webfs HTTP Static Server

## webfsd

```bash
webfsd -F -p 8000
```

Serve a specific directory:

```bash
webfsd -F -p 8000 -r /path/to/dir
```

Bind to specific address:

```bash
webfsd -F -p 8000 -b 0.0.0.0
```

Features:
- Directory listing: Yes
- Lightweight Unix-style server
- `-F` flag: run in foreground
- Supports virtual hosts
- CGI support

## Install

- Debian/Ubuntu: `apt install webfs`
- From source: Available on most Linux package managers

## Common flags

| Flag | Description |
|---|---|
| `-F` | Run in foreground |
| `-p PORT` | Listen port |
| `-r DIR` | Document root |
| `-b ADDR` | Bind address |
| `-f INDEX` | Index file name |
| `-n HOSTNAME` | Virtual hostname |

Note: `webfs` is a simple, lightweight HTTP server primarily found on Linux systems. It may not be available on macOS or Windows.
