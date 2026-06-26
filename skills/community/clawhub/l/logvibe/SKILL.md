# LogVibe

LogVibe colorizes HTTP status codes in log files to instantly highlight successes, redirects, client errors, and server errors directly in your terminal. Perfect for developers and sysadmins who need to scan logs quickly and catch issues at a glance.

## Usage

```bash
# Process a log file
python logvibe.py access.log

# Pipe logs directly
tail -f access.log | python logvibe.py

# Check a single line
echo "192.168.1.1 - - [10/Oct/2023:13:55:36] "GET /index.html HTTP/1.1" 404 203" | python logvibe.py
```

## Price

$2.50
