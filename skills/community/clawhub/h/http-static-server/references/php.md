# PHP HTTP Static Server

## Built-in Development Server (PHP >= 5.4)

```bash
php -S 127.0.0.1:8000
```

Bind to all interfaces:

```bash
php -S 0.0.0.0:8000
```

Serve a specific directory:

```bash
php -S 127.0.0.1:8000 -t /path/to/dir
```

With a custom router script:

```bash
php -S 127.0.0.1:8000 router.php
```

Features:
- Directory listing: No
- HTTPS: No (use reverse proxy)
- Built into PHP since 5.4
- Supports PHP script execution
- Single-threaded (development use only)

## Docker PHP

Run without local PHP installation:

```bash
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp -p 8000:8000 php:8.2-cli php -S 0.0.0.0:8000
```

Note: The built-in PHP server is intended for development only. Do not use in production.
