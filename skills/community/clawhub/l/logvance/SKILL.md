# Logvance

Converts UTC or ISO-formatted timestamps in log files to local system time, making log analysis faster and more intuitive for developers and sysadmins.

## Usage

```bash
# Process a log file
python logvance.py app.log

# Pipe logs directly
journalctl -u myservice | python logvance.py

# Save to output file
python logvance.py server.log -o local_time.log
```

## Price

$2.50
