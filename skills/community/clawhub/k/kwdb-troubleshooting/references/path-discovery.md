# Path Discovery

Discover evidence roots before deep analysis when the user does not provide them.

## Search Order

1. user-provided path
2. current case directory or attached files
3. ask the user for the fault time window if it is missing
4. for OOM or process-kill incidents only, inspect case-level system evidence such as `messages`, `syslog`, `dmesg`, or exported kernel logs with a targeted `oom` / `kwbase` grep
5. process launch arguments for `--log-dir`
6. process launch arguments for `--store`, then infer `store/logs`
7. default KWDB production log path
8. user-provided source repo path
9. ask the user whether to download the official repo for source-code analysis
10. ask the user for any remaining missing paths or tool access

## System Evidence Discovery

For OOM or process-kill incidents, prefer targeted system evidence checks before application logs.

Common places:

- case directory exports such as `messages`, `syslog`, or `dmesg`
- `/var/log/messages`
- `/var/log/syslog`
- `dmesg`

## Runtime Log Discovery

Prefer runtime configuration over guessed paths.

1. inspect the startup command first:

```bash
ps -ef | grep kaiwudb | grep --color=auto '\-\-log-dir'
```

2. if `--log-dir` is present, use that directory directly
3. if `--log-dir` is absent, inspect `--store`
4. if `--store` is present, check whether logs are under the store directory, usually `STORE_PATH/logs`
5. if neither startup parameter is visible or readable, fall back to default log paths

## Common Log Paths

- `/var/lib/kaiwudb/logs`
- `/var/log/messages`
- `/var/log/syslog`

## Source Repo Rules

- do not assume developer-local workspace paths as defaults
- if the source repo path is missing, ask the user whether to provide a local repo path or allow downloading `https://gitee.com/kwdb/kwdb`
- if the user declines source access, continue with logs and metrics only

## Metrics History Rules

- for performance incidents, use the `kwdb-mcp-server` `query-metrics-history` tool
- do not search the filesystem for a `metric_history` file
- if the tool is unavailable, ask the user for tool access or for exported metrics-history results

## Common Commands

```bash
ps -ef | grep kaiwudb | grep --color=auto '\-\-log-dir'
ps -ef | grep kaiwudb | grep --color=auto '\-\-store'
find /var/lib/kaiwudb -maxdepth 3 -type d -name logs 2>/dev/null
grep -iE 'oom|kwbase' /var/log/messages
grep -iE 'oom|kwbase' /var/log/syslog
dmesg -T | grep -iE 'oom|kwbase'
find /var/log -maxdepth 2 -type f \( -name messages -o -name syslog \) 2>/dev/null
git -C /path/to/repo branch --show-current
git -C /path/to/repo rev-parse HEAD
```

## Log Directory Rules

- prefer the explicit `--log-dir` value over every default or inferred path
- if only `--store` is available, inspect `STORE_PATH/logs` before broader search
- if neither flag is visible, try `/var/lib/kaiwudb/logs`
- do not fall back to developer-local paths unless the user explicitly provides them
- when multiple candidates exist, prefer the directory whose timestamps match the failure window
- for OOM or process-kill incidents, prefer the system evidence file whose targeted `oom` / `kwbase` matches line up with the failure window before reading service logs broadly

## Repo Selection Rules

- prefer the repo whose tree matches the source file suffix from the decisive log line
- if multiple repos match, prefer the repo the user names
- if the user does not name one, prefer the repo that most closely matches the runtime version or active workspace
- if no local repo can be confirmed, ask the user whether to download `https://gitee.com/kwdb/kwdb`; if declined, skip code correlation and say so explicitly

## Code Citation Rules

- for Go logs such as `kv/kvserver/closedts/provider/provider.go:166`, search for the same suffix in the chosen repo
- for C or C++ engine logs such as `ts_version.cpp:1173`, search the engine source tree first
- keep the final answer short, but include enough path detail in the evidence or source-localization section to make the next step executable
