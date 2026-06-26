---
name: openclaw-m0-setup
description: 为 OpenClaw 安装云端 m0 记忆插件。当用户提供 Access Key（以 ak_ 开头）或提到「配置云端记忆」「安装记忆插件」「setup memory」时使用此 skill。
version: 0.2.2
metadata: {"openclaw":{"emoji":"🧠","requires":{"env":[],"bins":["curl","node"]}}}
---

# Cloud Memory (m0) 安装指南

为 OpenClaw 接入云端持久化记忆——对话开始前自动注入相关记忆、对话结束后自动提炼并写入新记忆。

## 前置信息

- `{AK}`: 用户的 Access Key（以 `ak_` 开头）
- `{ENDPOINT}`: `_{ENDPOINT}_`

`{AK}` 若用户未提供，按 Step 1c 创建。

---

## Step 0 — 识别宿主工具 & 检查版本

m0 插件要求宿主工具 **≥ 2026.2.2**。执行任何 shell 命令前，先通过以下方式确认 `{CLAW_CMD}`。

运行以下命令，扫描本地已安装的 claw 类工具：

```bash
for dir in $HOME/.*; do
  name=$(basename "$dir" | sed 's/^\.//')
  cfg="$dir/${name}.json"
  if [ -f "$cfg" ] && grep -ql '"gateway"' "$cfg" && grep -ql '"plugins"' "$cfg"; then
    echo "$name"
  fi
done
```

**根据输出结果决策：**

- **1 个候选**：直接将其作为 `{CLAW_CMD}`，无需询问用户，继续后续步骤。
- **多个候选**：向用户发送提问并等待回答，**在用户明确回答前不得执行任何后续步骤**：
  > 检测到本地安装了多个工具（如 `openclaw`、`homiclaw`）。请问你当前使用的是哪一个？
- **0 个候选**：向用户发送提问并等待回答，**在用户明确回答前不得执行任何后续步骤**：
  > 未检测到已安装的工具，请告诉我你使用的 CLI 命令名是什么？

确定 `{CLAW_CMD}` 后，先推导根目录（后续步骤均复用这两个变量）：

```bash
CLAW_ROOT=$({CLAW_CMD} config file 2>/dev/null | grep '\.json' | xargs dirname | sed "s|~|$HOME|")
```

**根据识别结果决定后续行为：**

- **`{CLAW_CMD}` 为 `openclaw`**：执行版本检查：
  ```bash
  openclaw --version
  ```
  输出形如 `OpenClaw 2026.3.13 (61d171a)`，提取第二个字段与最低要求 `2026.2.2` 比较：
  - 版本 ≥ 2026.2.2：继续执行后续步骤。
  - 版本 < 2026.2.2：**立即中止安装**，向用户发送：
    > ⚠️ 你当前的版本（`{CURRENT_VERSION}`）过低，无法运行 m0 插件。请先升级到 **2026.2.2 或更高版本**，再重新运行此安装流程。
    >
    > ```bash
    > openclaw update
    > ```

- **`{CLAW_CMD}` 不是 `openclaw`**：跳过版本检查，向用户发送提示并等待确认：
  > ⚠️ 检测到你使用的是 **`{CLAW_CMD}`**，而非原生 openclaw。m0 插件基于 openclaw 开发，在其他分支版本上可能存在兼容性问题。是否仍要继续安装？
  
  - 用户确认继续：执行后续步骤。
  - 用户取消：中止安装。

---

## Step 1 — 检查服务 & 获取 Access Key

### 1a. 确认服务正常

```bash
curl -s "{ENDPOINT}/health"
```

返回 `{"status":"ok"}` 说明服务运行正常，继续。否则告知用户先启动服务。

### 1b. 用户已有 AK — 验证有效性

若用户已提供 `{AK}`，执行验证：

```bash
curl -s "{ENDPOINT}/api/instances/{AK}/status"
```

**期望响应**（HTTP 200）：

```json
{ "ak": "ak_...", "name": "...", "status": "ready", "memory_count": 0 }
```

验证通过，记录 `{AK}`，跳到 Step 2。

若 HTTP 404：AK 无效，按下方步骤重新创建。

### 1c. 用户没有 AK — 创建新实例

```bash
curl -s -X POST "{ENDPOINT}/api/instances/" \
  -H "Content-Type: application/json" \
  -d '{"name": "openclaw-memory"}'
```

响应中的 `ak` 字段即为 `{AK}`，展示给用户并提示妥善保存。

---

## Step 2 — 安装 m0 插件

通过 ClawHub 包管理器安装（插件已发布至 ClawHub registry）：

```bash
clawhub install m0
```

如果 `clawhub` 未安装，先安装 CLI：

```bash
npm i -g clawhub
```

**验证安装**：

```bash
clawhub list
```

应当看到 `m0` 出现在已安装列表中。

---

## Step 3 — 配置插件

**重要**：必须用单次原子操作写入所有配置。不要多次执行 `{CLAW_CMD} config set` — 每次操作都会触发 gateway 重启，导致执行中途被中断。

### 3a. 提前通知用户

在写入配置前发送提示：
> Cloud Memory 插件即将完成配置。配置写入后 Gateway 会自动重启加载插件，届时我会自动验证并通知你结果。

### 3b. 创建 BOOT.md（重启后通知，条件性）

配置写入将触发 gateway 重启，终止当前执行。若当前环境有消息投递渠道，请在写入配置 **之前** 先创建 `BOOT.md`，让 gateway 重启后自动完成验证并通知用户。若运行在无投递渠道的纯 CLI 环境，跳过此步。

如需创建，确定以下信息：
- `{CHANNEL}` — 当前通信渠道（如 `dingtalk`、`telegram`、`slack` 等）
- `{TARGET}` — 消息投递目标（发送者的 user ID 或群组 ID）

写入 `${CLAW_ROOT}/workspace/BOOT.md`（将 `{CHANNEL}` 和 `{TARGET}` 替换为实际值）：

```markdown
# Cloud Memory 安装验证

Cloud Memory 插件已完成配置，Gateway 已重启。请立即执行：

1. 运行 `{CLAW_CMD} ltm health` 确认插件连接正常
2. 运行 `{CLAW_CMD} plugins list` 确认 m0 已加载并分配到 memory slot
3. 使用 message 工具发送安装完成的确认消息，必须指定 channel="{CHANNEL}" 和 target="{TARGET}"，内容包含验证结果
4. 删除此文件：rm ${CLAW_ROOT}/workspace/BOOT.md
```

### 3c. 原子配置写入

运行以下 Node.js 脚本（将 `{ENDPOINT}` 和 `{AK}` 替换为实际值）：

```bash
CLAW_ROOT=$({CLAW_CMD} config file 2>/dev/null | grep '\.json' | xargs dirname | sed "s|~|$HOME|")

node -e "
const fs = require('fs');
const clawRoot = '${CLAW_ROOT}';
const cfgPath = clawRoot + '/{CLAW_CMD}.json';
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));

if (!cfg.hooks) cfg.hooks = {};
if (!cfg.hooks.internal) cfg.hooks.internal = {};
cfg.hooks.internal.enabled = true;

if (!cfg.plugins) cfg.plugins = {};
cfg.plugins.enabled = true;

if (!cfg.plugins.allow) cfg.plugins.allow = [];
if (!cfg.plugins.allow.includes('m0'))
  cfg.plugins.allow.push('m0');

if (!cfg.plugins.load) cfg.plugins.load = {};
if (!cfg.plugins.load.paths) cfg.plugins.load.paths = [];
const pluginPath = clawRoot + '/extensions/m0';
if (!cfg.plugins.load.paths.includes(pluginPath))
  cfg.plugins.load.paths.push(pluginPath);

if (!cfg.plugins.slots) cfg.plugins.slots = {};
cfg.plugins.slots.memory = 'm0';

if (!cfg.plugins.entries) cfg.plugins.entries = {};
cfg.plugins.entries['m0'] = {
  enabled: true,
  config: {
    apiKey: '{AK}',
    baseUrl: '{ENDPOINT}',
    autoCapture: true,
    autoRecall: true,
    recallLimit: 10
  }
};

fs.writeFileSync(cfgPath, JSON.stringify(cfg, null, 2) + '\n');
console.log('Config written. Gateway will auto-restart.');
"
```

Gateway 检测到配置变更后约 30 秒内自动重启。重启后执行 BOOT.md 完成验证并通知用户。

**写入配置后不要再执行任何命令** — 执行会被 gateway 重启中断。BOOT.md 负责处理重启后的一切。

---

## Step 4 — 重启后验证（自动）

重启后通过 BOOT.md 自动完成验证。如需手动验证：

```bash
{CLAW_CMD} ltm health
{CLAW_CMD} plugins list
```

看到 `m0` 状态为 enabled、healthy 且 memory slot 已分配，即安装成功。

---

## 安装完成

告知用户：
> Cloud Memory 插件已安装并激活。OpenClaw 会在每次对话开始前自动检索相关记忆、对话结束后自动提炼并写入新记忆。
>
> 你也可以在对话中直接让我操作记忆：
> - 「记住我喜欢简洁的代码风格」→ 触发 memory_store
> - 「你还记得我的代码偏好吗」→ 触发 memory_search
> - 「更新那条关于代码风格的记忆」→ 触发 memory_update
> - 「删除那条记忆」→ 触发 memory_delete

---

## API 速查

所有记忆接口均需 `X-API-Key: {AK}` 请求头。

| 操作 | 方法 | Endpoint |
|------|------|----------|
| 验证 AK | GET | `/api/instances/{AK}/status` |
| 写入记忆 | POST | `/api/memories/capture` |
| 搜索记忆 | POST | `/api/memories/search` |
| 列出记忆 | GET | `/api/memories/` |
| 获取记忆 | GET | `/api/memories/{id}` |
| 更新记忆 | PUT | `/api/memories/{id}` |
| 删除记忆 | DELETE | `/api/memories/{id}` |
| 删除全部记忆 | DELETE | `/api/memories/` |

## 故障排除

| 症状 | 解决 |
|------|------|
| GET status 返回 404 | AK 无效，重新创建实例获取新 Key |
| 插件未出现在 plugins list | 运行 `clawhub install m0` 重新安装 |
| `ltm health` 失败 | 确认服务地址 `{ENDPOINT}` 可访问；检查 `baseUrl` 配置 |
| 搜索返回空 | 先写入一些记忆；确认实例状态为 ready |
| 对话结束后无新记忆 | 检查 `autoCapture` 是否为 true；查看宿主工具日志 |
