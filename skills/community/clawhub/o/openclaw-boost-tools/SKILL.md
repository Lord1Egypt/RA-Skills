# bw-openclaw-boost - OpenClaw 效率提升工具包

## 概述

基于 Claude Code 架构分析开发的 OpenClaw 效率工具包，包含成本追踪、记忆管理、压缩系统、权限控制等功能。

## 版本

**v1.0.6** — 2026-04-03

## 文件结构

```
bw-openclaw-boost/
├── SKILL.md              # 本文件
├── version.json          # 版本信息
├── install.sh            # 安装脚本
├── launch.sh             # 统一启动器
└── tools/
    ├── cost_tracker.py         # 成本追踪（仅读取状态）
    ├── memory_relevance.py    # 相关性记忆检索
    ├── compaction_manager.py    # 多层压缩（仅读取状态）
    ├── permission_manager.py   # 权限管理（本地规则）
    ├── tool_tracker.py         # 工具执行追踪
    ├── coordinator.py          # 任务协调分析
    ├── dream_consolidation.py # 自动记忆整理（默认禁用）
    ├── slash_commands.py        # 斜杠命令（仅读取状态）
    ├── token_budget.py        # Token 预算监控
    ├── feature_flags.py        # 功能开关
    └── check_permission.sh     # 权限检查
```

## 安装

```bash
bash install.sh
```

安装后位于 `~/.openclaw/bw-openclaw-boost/`

## 安全设计

### 默认禁用的功能
以下功能默认关闭，需要手动启用：
- `stream_exec` — 可执行命令，建议仔细确认后再开启
- `dream_consolidation` — 会删除日志文件，需要备份后使用

### 启用危险功能
```bash
# 查看当前开关状态
python3 tools/feature_flags.py list

# 启用流式执行（谨慎）
python3 tools/feature_flags.py enable stream_exec

# 启用记忆整理（建议先备份）
python3 tools/feature_flags.py enable dream_consolidation
```

### 权限管理
- 所有 openclaw CLI 调用均为**只读操作**
- `permission_manager.py` 提供命令安全检查，但不会自动阻止

## 使用方式

### 安全工具（默认可用）
```bash
# 成本追踪（只读）
bash launch.sh cost

# 记忆检索
bash launch.sh memory

# Token 预算监控
bash launch.sh budget
```

### 需要谨慎的功能
```bash
# 流式执行（会执行命令）
python3 tools/stream_exec.py "ls" --timeout 10

# 记忆整理（会删除文件）
python3 tools/dream_consolidation.py run --force
```

## 依赖要求

- **Python 3** - 所有工具基于 Python 3
- **Bash** - 安装脚本和部分工具需要 Bash 环境
- **openclaw CLI** - 部分工具需要（仅读取状态）

## 安装前建议

1. **备份数据**
   ```bash
   cp -r ~/.openclaw ~/.openclaw.backup
   ```

2. **查看功能开关**
   ```bash
   python3 tools/feature_flags.py list
   ```

3. **先测试安全功能**
   ```bash
   bash launch.sh cost       # 成本追踪
   bash launch.sh memory     # 记忆检索
   ```

4. **再按需启用危险功能**
   ```bash
   python3 tools/feature_flags.py enable stream_exec
   ```

## 配置说明

- 所有配置文件存储在：`~/.openclaw/bw-openclaw-boost/`
- 不修改全局 `~/.openclaw/` 目录
- 记忆数据存储在：`~/.openclaw/bw-openclaw-boost/memory/`

## 安全特性

- ✅ 所有 openclaw CLI 调用均为只读
- ✅ coordinator 只做本地任务记录，不发送消息
- ✅ 危险功能默认禁用，需要手动确认开启
- ✅ 配置文件在技能目录内，不影响全局
- ✅ 无网络下载，无外部凭据要求
