# Deno HTTP Static Server

## Standard Library File Server

```bash
deno run --allow-net --allow-read jsr:@std/http/file-server
```

Custom port:

```bash
deno run --allow-net --allow-read jsr:@std/http/file-server --port 8000
```

Serve a specific directory:

```bash
deno run --allow-net --allow-read jsr:@std/http/file-server /path/to/dir
```

Bind to all interfaces:

```bash
deno run --allow-net --allow-read jsr:@std/http/file-server --host 0.0.0.0
```

Features:
- Directory listing: Yes
- CORS: `--cors`
- HTTPS: `--cert` and `--key` flags
- Secure by default (requires explicit permission flags)
- No install needed, runs directly from JSR registry
- Default port: 4507

## Older Deno versions

For Deno versions before JSR support:

```bash
deno run --allow-net --allow-read https://deno.land/std/http/file_server.ts
```
