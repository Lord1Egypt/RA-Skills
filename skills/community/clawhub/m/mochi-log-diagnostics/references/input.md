# Action contract

analyze: files1..20; optional includeBots default false, statuses integer list, pathContains, dateFrom/dateTo YYYY-MM-DD. Parses Apache/Nginx combined access format, JSONL with timestamp/time,level,status/statusCode,path/url,message/msg,ip/remote_addr,userAgent/user_agent,bytes, and ISO-prefixed plain level logs. Max32MiB decompressed/file,200000 lines total. IPs are counted but not saved in the report; route query strings removed. User-agent bot labels are heuristic; malformed lines are counted separately. JSON/CSV/HTML reports include hourly buckets, status levels, route counts and error signatures.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.
