# Interactive Config Flow Pattern

> Applied by keep-me-update. Suitable for any skill needing user-specific
> setup (language, timezone, API keys, output paths, data sources).

## Principle

Skip hardcoded config blocks in SKILL.md and memory lookups. Instead,
ask the user during first trigger, persist answers to a local YAML file,
and reuse on subsequent triggers.

## Implementation

### Step 0 in SKILL.md

```
Step 0: 交互配置
  - 依次询问 N 个问题（4 max recommended）
  - 每问一条：先尝试系统检测，拿不到才问用户
  - 写入 {skill_dir}/user_config.yaml
  - 后续触发先读文件，缺字段才补问
```

### Config file structure

```yaml
# user_config.yaml
language: zh
timezone: Asia/Shanghai
output_mode: terminal
output_dir: ~/DailyENews/
```

### Detection order per field

| Field | System detection sources |
|-------|------------------------|
| language | `locale` command, Hermes config language |
| timezone | `readlink /etc/localtime`, `systemsetup -gettimezone`, `timedatectl` |
| output_dir | Only ask — no reliable system default |

### Pitfalls

- **Don't use agent `memory` tool for config.** Config lives in a file,
  independent of agent context lifetime and memory store.
- **Validate after reading.** On subsequent triggers, verify the file
  is valid YAML and all required fields exist. If corrupted, re-ask
  only the missing fields.
- **Rolling field additions.** When a skill version adds a new config
  field, the agent should detect it's missing and ask once.
