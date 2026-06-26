# EXO1 升级指南

## 前置条件

- EXO1 已有 OpenClaw + workspace
- EXO1 有 Python 3.9+
- 通过 Syncthing 共享 skills/ 目录

## 升级步骤

### 1. 同步 skill 到 EXO1

```bash
# EXO2 上
cp -r ~/.openclaw/workspace/skills/memcore ~/Syncthing_Data/exo1-sharing/skills/

# EXO1 上
cp -r ~/Syncthing_Data/exo1-sharing/skills/memcore ~/.openclaw/workspace/skills/
```

### 2. 安装

```bash
bash ~/.openclaw/workspace/skills/memcore/scripts/install.sh
```

### 3. 修改 AGENTS.md

在 `## Session Startup` 节追加减报流（参考下方模板）：

```markdown
5. ⚠️ 全量 MEMORY.md 按需读取（通过 python3 scripts/memcore/cli.py search 检索）
```

在 `## 散会机制` 节加第3步：

```markdown
3. MemCore 同步：python3 scripts/memcore/cli.py index && python3 scripts/memcore/cli.py induce && python3 scripts/memcore/cli.py feedback
```

### 4. 添加 cron 定时维护

```bash
# 04:00
python3 scripts/memcore/cli.py index && python3 scripts/memcore/cli.py induce && python3 scripts/memcore/cli.py feedback && python3 scripts/memcore/cli.py brief

# 16:00  
# 同上
```

### 5. 验证

```bash
python3 ~/.openclaw/workspace/scripts/memcore/cli.py stats
python3 ~/.openclaw/workspace/scripts/memcore/cli.py search "测试查询" -n 3
```

## 注意事项

- MEMORY.md 原文件不会被修改
- 所有数据存独立 SQLite
- 回退: `cp memcore_backup_*/AGENTS.md ~/.openclaw/workspace/`
