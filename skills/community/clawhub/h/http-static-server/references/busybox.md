# BusyBox HTTP Static Server

## busybox httpd

```bash
busybox httpd -f -p 8000
```

Run in background (daemonize):

```bash
busybox httpd -p 8000
```

Serve a specific directory:

```bash
busybox httpd -f -p 8000 -h /path/to/dir
```

Bind to specific address:

```bash
busybox httpd -f -p 192.168.1.100:8000
```

Features:
- Directory listing: Yes
- Extremely lightweight (embedded/IoT-friendly)
- Available on most minimal Linux distributions
- CGI support: `-c httpd.conf`
- Foreground mode: `-f`
- No dependencies beyond BusyBox

## Configuration file (optional)

Create `httpd.conf` for access control:

```
# Deny access to hidden files
D:.*

# Allow specific IP range
A:192.168.1.0/24

# Custom MIME types
.json:application/json
```

```bash
busybox httpd -f -p 8000 -c httpd.conf
```
