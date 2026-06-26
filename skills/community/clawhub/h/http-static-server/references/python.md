# Python HTTP Static Server

## Python 3 (recommended)

The built-in `http.server` module is the simplest and most widely available option.

```bash
python3 -m http.server 8000
```

Bind to a specific address:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Serve a specific directory (Python 3.7+):

```bash
python3 -m http.server 8000 --directory /path/to/dir
```

Features:
- Directory listing: Yes
- HTTPS: No (use reverse proxy)
- Pre-installed on most Linux/macOS systems
- Bind-all: `--bind 0.0.0.0`

## Python 2 (legacy)

```bash
python -m SimpleHTTPServer 8000
```

Note: Python 2 is EOL since January 2020. Use Python 3 whenever possible.

## Twisted

A more full-featured option with production-grade capabilities.

Install:

```bash
pip install twisted
```

One-liner daemon:

```bash
twistd -n web -p 8000 --path .
```

Inline script:

```bash
python -c 'from twisted.web.server import Site; from twisted.web.static import File; from twisted.internet import reactor; reactor.listenTCP(8000, Site(File("."))); reactor.run()'
```

Features:
- Directory listing: Yes
- Supports HTTPS with certificates
- Production-grade event loop
- Requires `pip install twisted`
