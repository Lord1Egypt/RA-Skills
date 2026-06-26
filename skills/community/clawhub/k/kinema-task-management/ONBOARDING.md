# Kinema's Task Management Onboarding

> 本文档指导 AI Agent 完成首次环境配置。按顺序执行，遇到问题时参考 Troubleshooting。

## Prerequisites | 前置条件

- OpenClaw 已运行，Agent 可执行文件系统操作
- OpenClaw cron 功能可用
- Bash 可用

## Step 1: 创建目录结构

### 检测

```bash
ls -d ~/.openclaw/workspace/kinema-tasks/active ~/.openclaw/workspace/kinema-tasks/archived ~/.openclaw/workspace/kinema-tasks/snapshots 2>&1
```

期望输出：三个目录路径（无错误）。

### 安装

```bash
mkdir -p ~/.openclaw/workspace/kinema-tasks/active
mkdir -p ~/.openclaw/workspace/kinema-tasks/archived
mkdir -p ~/.openclaw/workspace/kinema-tasks/snapshots
```

> ⚠️ 不要使用 brace expansion（`{a,b,c}`），部分 shell 环境不支持。

### 验证

```bash
ls -d ~/.openclaw/workspace/kinema-tasks/active ~/.openclaw/workspace/kinema-tasks/archived ~/.openclaw/workspace/kinema-tasks/snapshots
```

期望输出：三个目录路径。

## Step 2: 确定推送通道

### 说明

Cron 任务通过 `--channel` 和 `--to` 指定推送目标。不同通道的 `--to` 格式不同：

| 通道 | `--channel` 值 | `--to` 格式 | 来源 |
|------|---------------|------------|------|
| Discord | `discord` | `channel:{chat_id}` | Inbound metadata 的 `chat_id` 字段 |
| Telegram | `telegram` | Telegram chat ID | Inbound metadata 的 `chat_id` 字段 |
| Signal | `signal` | E.164 电话号码 | Inbound metadata 的 `chat_id` 字段 |

> ⚠️ **不要使用 `sender.id`**，`--to` 需要的是 `chat_id`（通道对话 ID），不是用户 ID。

### 提取方法

从当前 session 的 **Inbound Context（untrusted metadata）** JSON 中提取：

- `provider` → 填入 `--channel`
- `chat_id` → 填入 `--to`（无需额外处理，直接使用原始值）

示例（Discord DM）：
```json
{"chat_id": "channel:1485514207515512953", "channel": "discord", "provider": "discord"}
```
→ `--channel discord --to channel:1485514207515512953`

### 用户确认

提取到值后，**必须询问用户确认推送目标**：

```
"提取到当前对话：channel={provider}, to={chat_id}
推送目标使用当前通道，还是指定其他？"
```

根据用户回复确定最终值。如果当前 session 无 inbound metadata，必须询问用户。

> **参考文档**：OpenClaw cron delivery 配置详见 `/app/docs/automation/cron-jobs.md`

## Step 3: 安装辅助脚本

### 检测

```bash
ls ~/.openclaw/workspace/skills/kinema-task-management/scripts/
```

期望输出：`next-id.sh` `create-task.sh` `archive-task.sh` `snapshot.sh` `report.sh`

### 安装

辅助脚本随 skill 一起安装（`clawhub install` 或手动复制到 `skills/kinema-task-management/scripts/`）。

确保脚本可执行：

```bash
chmod +x ~/.openclaw/workspace/skills/kinema-task-management/scripts/*.sh
```

### 验证

```bash
~/.openclaw/workspace/skills/kinema-task-management/scripts/next-id.sh
```

期望输出：下一个可用任务 ID（如 `TASK-00001`）

## Step 4: 配置 Cron 任务

### 检测

```bash
openclaw cron list 2>&1 | grep -i "kinema-tasks"
```

期望输出：包含三条 cron 记录（archive-check、daily-report、write-snapshot）。

### 安装

**依次创建以下三个 cron 任务（将 `CHANNEL` 和 `TO_ID` 替换为 Step 2 获取的实际值）：**

#### 4.1 归档检查（每天 09:00 北京时间）

```bash
openclaw cron add \
  --name "kinema-tasks-archive-check" \
  --cron "0 9 * * *" \
  --tz Asia/Shanghai \
  --session isolated \
  --channel <CHANNEL> \
  --to <TO_ID> \
  --announce \
  --timeout-seconds 120 \
  --message "执行 KinemaTasks 归档检查：读取 ~/.openclaw/workspace/skills/kinema-task-management/SKILL.md 了解规范。扫描 ~/.openclaw/workspace/kinema-tasks/active/ 中所有 TASK-*.md 文件，检查 Metadata 表中'状态'字段。如果状态为 Done 或 Cancelled：1) 更新该文件的'最后更新'为今天日期（YYYY-MM-DD）2) 在 Changelog 追加记录（如 'YYYY-MM-DD 状态变更: Done → 移入 archived'）3) 将文件从 active/ 移动到 archived/。完成后输出归档摘要，如无需归档则输出'无待归档任务'。"
```

#### 4.2 每日早报（每天 09:01 北京时间）

```bash
openclaw cron add \
  --name "kinema-tasks-daily-report" \
  --cron "1 9 * * *" \
  --tz Asia/Shanghai \
  --session isolated \
  --channel <CHANNEL> \
  --to <TO_ID> \
  --announce \
  --timeout-seconds 180 \
  --message "执行 KinemaTasks 每日早报推送。读取 ~/.openclaw/workspace/skills/kinema-task-management/SKILL.md 了解完整规范。1) 调用 ~/.openclaw/workspace/skills/kinema-task-management/scripts/report.sh 获取结构化报告内容（不含摘要）2) 根据报告内容撰写 2-3 句话的状况摘要（新增/完成数量、紧急提醒、过期提醒等，非固定模板）3) 将摘要插入报告标题下方，组装完整报告 4) 直接发送完整报告到对话。注意：如果没有最近快照则跳过 diff 部分。日期使用北京时间。"
```

#### 4.3 写入快照（每天 09:02 北京时间）

```bash
openclaw cron add \
  --name "kinema-tasks-write-snapshot" \
  --cron "2 9 * * *" \
  --tz Asia/Shanghai \
  --session isolated \
  --channel <CHANNEL> \
  --to <TO_ID> \
  --announce \
  --timeout-seconds 120 \
  --message "执行 KinemaTasks 快照写入：读取 ~/.openclaw/workspace/skills/kinema-task-management/SKILL.md 了解规范。1) 扫描 ~/.openclaw/workspace/kinema-tasks/active/ 中所有 TASK-*.md 文件 2) 读取每个文件的 Metadata（标题、状态、优先级、领域、截止日期）3) 按 SKILL.md 中的快照格式生成 markdown 4) 写入 ~/.openclaw/workspace/kinema-tasks/snapshots/YYYY-MM-DD.md（使用今天北京时间日期）。输出写入确认和任务摘要统计。"
```

> **注意**：
> - `<CHANNEL>` 和 `<TO_ID>` 必须替换为 Step 2 获取的实际值
> - 三个 cron 使用 `--session isolated` 在独立 session 中运行，避免污染主 session 历史
> - `--announce` 将结果推送到指定通道
> - `--channel` 指定推送通道类型，`--to` 指定目标用户 ID
> - `--tz Asia/Shanghai` 直接使用北京时间（09:00），无需手动计算 UTC
> - 三个 cron 间隔 1 分钟（09:00 → 09:01 → 09:02），确保顺序执行

### 验证

```bash
openclaw cron list 2>&1 | grep -i "kinema-tasks"
```

期望输出：显示三条 cron 记录，名称分别为 `kinema-tasks-archive-check`、`kinema-tasks-daily-report`、`kinema-tasks-write-snapshot`。

## Step 5: 最终验证

```bash
# 检查目录
ls -la ~/.openclaw/workspace/kinema-tasks/

# 检查脚本
~/.openclaw/workspace/skills/kinema-task-management/scripts/next-id.sh

# 检查 cron
openclaw cron list 2>&1 | grep "kinema-tasks"
```

全部通过即可开始使用。

## Troubleshooting | 故障排除

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `next-id.sh: No such file` | Skill 未安装或路径错误 | 确认 skill 已安装到 `~/.openclaw/workspace/skills/kinema-task-management/` |
| `openclaw cron: command not found` | OpenClaw 版本不支持 cron | 升级 OpenClaw 到支持 cron 的版本 |
| `Permission denied` 脚本 | 脚本无执行权限 | `chmod +x scripts/*.sh` |
| cron 未执行 | cron 服务未启动 | 检查 OpenClaw gateway 状态：`openclaw gateway status`，检查 cron 列表：`openclaw cron list` |
| 目录不存在 | Step 1 未执行 | 重新执行 `mkdir -p` 创建三个目录（见 Step 1） |
| 推送未到达对话 | 缺少 `--channel` 或 `--to` | 重新创建 cron 任务，确保包含 `--channel` 和 `--to` 参数 |
| cron 参数格式错误 | 版本差异 | 运行 `openclaw cron add --help` 确认当前版本支持的参数 |
| `cron run` 用 name 报错 | 需要用 UUID | 用 `openclaw cron list --json` 获取 job id |
