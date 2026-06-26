# Rust HTTP Static Server

## miniserve (recommended)

Install:

```bash
cargo install miniserve
```

Run:

```bash
miniserve -p 8000 .
```

Bind to all interfaces:

```bash
miniserve -p 8000 --interfaces 0.0.0.0 .
```

With authentication:

```bash
miniserve -p 8000 --auth user:password .
```

Features:
- Directory listing: Yes (with clean UI)
- File upload: `--upload-files`
- WebDAV support
- Authentication: `--auth`
- HTTPS: `--tls-cert` and `--tls-key`
- QR code for easy mobile access: `--qrcode`

## http (thecoshman/http)

Install:

```bash
cargo install https
```

Run:

```bash
http -p 8000
```

Features:
- Directory listing: Yes
- Simple and lightweight
- Automatic MIME type detection

## Using cargo without install

```bash
cargo install miniserve && miniserve -p 8000 .
```

Or via `cargo-binstall` for faster binary install:

```bash
cargo binstall miniserve
miniserve -p 8000 .
```
