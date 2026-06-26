# LogSift

Quickly filter large log files by keyword or date range right from the command line — no more scrolling or manual searching.

## Usage

```bash
# Filter by keyword
log_sift application.log -k "ERROR" -k "timeout"

# Filter by date range
log_sift application.log --since "2023-05-01 14:00:00" --until "2023-05-01 15:00:00"

# From stdin
tail -n 1000 app.log | log_sift -k "failed" --since "2023-05-01"

# Mixed filtering
log_sift -k "Warning" --since "2023-05-01" server.log
```

## Price

$2.50
