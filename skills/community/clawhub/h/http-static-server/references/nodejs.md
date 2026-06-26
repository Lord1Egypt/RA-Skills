# Node.js HTTP Static Server

## npx http-server (zero-install, recommended)

```bash
npx http-server -p 8000
```

With CORS enabled:

```bash
npx http-server -p 8000 --cors
```

Features:
- Directory listing: Yes
- CORS support: `--cors`
- HTTPS: `--ssl --cert cert.pem --key key.pem`
- Caching: `-c-1` disables caching
- Gzip: `--gzip`

## npx serve

```bash
npx serve -l 8000
```

Features:
- Directory listing: Yes (with clean UI)
- Single-page app mode: `--single`
- CORS: `--cors`
- Configuration via `serve.json`

## Global install

```bash
npm install -g http-server
http-server -p 8000
```

## node-static

No directory listings.

```bash
npm install -g node-static
static -p 8000
```

Or inline:

```bash
npx node-static -p 8000
```

Features:
- Directory listing: No
- Efficient static file serving
- Custom headers support
- RFC 2616 compliant caching

## Inline Node.js script (no dependencies)

```bash
node -e "require('http').createServer((req,res)=>{require('fs').createReadStream('.'+req.url).pipe(res)}).listen(8000)"
```

Note: This is minimal and does not handle errors, MIME types, or directory listing.
