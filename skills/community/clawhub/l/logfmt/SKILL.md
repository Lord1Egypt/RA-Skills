# LogFMT

A lightweight CLI tool that brings syntax highlighting to plain text logs in your terminal. LogFMT detects timestamps and log levels (ERROR, WARN, INFO, etc.) and applies readable colors, making debugging faster and less error-prone.

## Usage

```bash
# Colorize a log file
python logfmt.py app.log

# Pipe logs with tail
tail -f app.log | python logfmt.py

# Colorize current system logs
journalctl -f | python logfmt.py

# From stdin
cat error.log | python logfmt.py
```

## Price

$2.50
