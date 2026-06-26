# Natural-Language Parser Examples

Use with:
- `scripts/parse_nl_intent.py`

## Example 1

Input:

```text
给我设置一个3分钟的闹钟，3分钟后提醒我，我在泡面
```

Expected shape:
- `intentType: reminder`
- `scheduleType: at`
- `interval.normalized: 3m`
- `targetScope: main`

## Example 2

Input:

```text
每隔 5 分钟设个闹钟
```

Expected shape:
- `intentType: repeat-loop`
- `scheduleType: every`
- `interval.normalized: 5m`

## Example 3

Input:

```text
对当前 session 的 agent 做一个 prompt 注入，每隔 10 分钟 push 一下
```

Expected shape:
- `intentType: session-injection`
- `scheduleType: every`
- `interval.normalized: 10m`
- `targetScope: current-session`
- `deliveryMode: none`

## Example 4

Input:

```text
每天早上发个总结到 Discord
```

Expected shape:
- `intentType: scheduled-worker`
- `scheduleType: at`
- `deliveryMode: announce`
- `needsReview: true` (time + target still need structured confirmation)

## Example 5

Input:

```text
未来十分钟里面执行五次 crawl
```

Expected shape:
- `intentType: repeat-loop`
- `runCount: 5`
- `needsReview: true` (stop-condition derivation still needs confirmation)

## Usage

```bash
python3 scripts/parse_nl_intent.py <<'EOF'
对当前 session 的 agent 做一个 prompt 注入，每隔 10 分钟 push 一下
EOF
```
