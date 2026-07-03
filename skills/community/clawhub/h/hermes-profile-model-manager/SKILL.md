---
name: profile-model-manager
description: "查看、更换和管理 Hermes 各 profile 的大模型配置（主模型、辅助模型、delegation 模型）。支持单个/批量操作、切换 provider、全 profile 一览。"
version: 2.1.2
author: 贾维斯
metadata:
  hermes:
    tags: [hermes, model, provider, profile, configuration]
    related_skills: [hermes-agent, auxiliary-model-config]
---

# Profile Model Manager

管理 Hermes 各 profile 的全部模型配置——主模型、辅助模型（vision / compression / web_extract / session_search）、delegation 模型。支持查看、切换、批量操作。

> **适用场景：** 需要查看或切换 Hermes 各 profile 的大模型时使用本 skill。
> **不适用场景：** 安装新 provider、配置 API Key（参见 `hermes-agent` skill）；管理 MCP 模型（参见 `native-mcp` skill）。

---

## 🤖 Agent 智能触发指引

**当用户说以下任何一种话时，Agent 应自动加载并使用本 skill：**

| 用户意图 | 触发关键词示例 |
|---|---|
| 查看当前模型 | "现在用的什么模型"、"模型配置"、"看看模型"、"model 配置" |
| 切换模型 | "换成 xxx 模型"、"切到 xxx"、"用 glm-5"、"换 provider" |
| 批量操作 | "所有 profile 都换成"、"统一切换"、"批量改模型" |
| 诊断问题 | "模型报错了"、"API key 找不到"、"切换不生效"、"context too small" |
| 辅助模型 | "vision 模型"、"compression"、"web_extract"、"session_search 模型" |
| delegation | "子 agent 用什么模型"、"delegation 模型"、"delegate 便宜点" |

**Agent 使用流程：**
1. 用户表达意图 → 加载本 skill
2. 先用 `bash ~/.hermes/scripts/profile-model-overview.sh` 展示当前状态
3. 根据意图执行对应操作
4. 操作后验证结果（见 §3 操作效果示例）
5. 如需重启 Gateway，主动提醒用户

---

## 0. 快速开始

**30 秒上手：**

```bash
# 查看所有 profile 模型全景
bash ~/.hermes/scripts/profile-model-overview.sh

# 查看单个 profile 详情
bash ~/.hermes/scripts/profile-model-overview.sh reasoner

# 预览切换到智谱的效果（不修改任何配置）
bash ~/.hermes/scripts/profile-model-overview.sh reasoner zhipu

# 确认执行：一键切换所有模型 + 自动重启 Gateway
bash ~/.hermes/scripts/profile-model-overview.sh reasoner --apply zhipu
```

**前置条件：**
- Hermes Agent 已安装（`hermes --version` 可用）
- 目标 provider 的 API Key 已配置在对应 profile 的 `.env` 中
- 切换后必须重启 Gateway 才能生效

---

## 1. 模型配置架构

每个 profile 的 `config.yaml` 中有三个模型相关配置块：

```yaml
model:          ← 主模型（对话用）
auxiliary:      ← 辅助模型（vision / compression / web_extract / session_search）
delegation:     ← 子 agent 模型（delegate_task 时使用）
```

### 1.1 主模型 `model:`

```yaml
model:
  default: mimo-v2.5-pro        # 模型名称
  provider: xiaomi               # provider 名称
  base_url: https://...          # API 端点（部分 provider 可省略）
  api_key: xxx                   # 可选，也可放 .env
  context_length: 200000         # 上下文窗口大小
  api_mode: chat_completions     # API 模式
```

### 1.2 辅助模型 `auxiliary:`

```yaml
auxiliary:
  vision:                        # 图片分析、截图识别
    provider: xiaomi
    model: mimo-v2-omni
    base_url: https://...
    timeout: 120
  compression:                   # 上下文压缩
    provider: xiaomi
    model: mimo-v2.5
    base_url: https://...
    timeout: 120
  web_extract:                   # 网页内容提取
    provider: xiaomi
    model: mimo-v2.5
    base_url: https://...
    timeout: 360
  session_search:                # 历史会话搜索
    provider: xiaomi
    model: mimo-v2.5
    base_url: https://...
    timeout: 30
    max_concurrency: 3
```

### 1.3 Delegation 模型 `delegation:`

```yaml
delegation:
  model: mimo-v2.5               # 空则继承主模型
  provider: xiaomi
  base_url: ''                   # 空则继承主模型 base_url
  reasoning_effort: ''
  max_iterations: 50
  max_concurrent_children: 3
```

---

## 2. 查看模型配置

```bash
# 查看 default profile 的完整配置
hermes config show

# 查看指定 profile 的主模型
cat ~/.hermes/profiles/<name>/config.yaml | grep -A5 "^model:"

# 查看指定 profile 的辅助模型
cat ~/.hermes/profiles/<name>/config.yaml | grep -A20 "^auxiliary:"

# 查看指定 profile 的 delegation 模型
cat ~/.hermes/profiles/<name>/config.yaml | grep -A10 "^delegation:"

# 一键查看所有 profile 模型全景
bash ~/.hermes/scripts/profile-model-overview.sh
```

**`hermes config show` 预期输出（片段）：**
```yaml
model:
  default: mimo-v2.5-pro
  provider: xiaomi
  base_url: https://token-plan-cn.xiaomimimo.com/v1
  context_length: 200000
  api_mode: chat_completions
auxiliary:
  vision:
    provider: xiaomi
    model: mimo-v2-omni
  compression:
    provider: xiaomi
    model: mimo-v2.5
  ...
```

**⚠️ 注意：** 如果 `cat` 命令返回空，说明 config.yaml 中没有该配置块。此时需要检查是否使用了正确的 profile 路径：`~/.hermes/profiles/<name>/config.yaml`（注意 `default` profile 的路径是 `~/.hermes/config.yaml`）。

---

## 3. 切换模型

### 3.1 切换单个 profile 的主模型

```bash
# 对 default profile（不加 -p 参数）
hermes config set model.default <model_name>
hermes config set model.provider <provider>
hermes config set model.base_url <base_url>

# 对其他 profile（必须加 -p <name>）
hermes -p <profile> config set model.default <model_name>
hermes -p <profile> config set model.provider <provider>
hermes -p <profile> config set model.base_url <base_url>
```

**操作效果示例：**
```bash
$ hermes -p reasoner config set model.default glm-5.1
✅ Set model.default = glm-5.1

$ hermes -p reasoner config set model.provider zhipu
✅ Set model.provider = zhipu
```

**切换后必须重启：**
```bash
hermes -p <profile> gateway restart
```

**重启效果：**
```bash
$ hermes -p reasoner gateway restart
🔄 Restarting gateway for profile 'reasoner'...
✅ Gateway restarted successfully
```

### 3.2 切换辅助模型

```bash
hermes config set auxiliary.vision.provider <provider>
hermes config set auxiliary.vision.model <model>
hermes config set auxiliary.vision.base_url <url>

hermes config set auxiliary.compression.provider <provider>
hermes config set auxiliary.compression.model <model>

hermes config set auxiliary.web_extract.provider <provider>
hermes config set auxiliary.web_extract.model <model>

hermes config set auxiliary.session_search.provider <provider>
hermes config set auxiliary.session_search.model <model>
```

Per-profile 用法同理加 `-p <name>`。

### 3.3 切换 Delegation 模型

```bash
hermes -p <profile> config set delegation.model <model>
hermes -p <profile> config set delegation.provider <provider>
```

设为空字符串即回到继承主模型的行为：
```bash
hermes -p <profile> config set delegation.model ""
hermes -p <profile> config set delegation.provider ""
```

### 3.4 批量操作所有 profile

```bash
# 切换所有 profile 主模型
for p in default cto diary genshin reasoner scout qian-duoduo; do
  if [ "$p" = "default" ]; then
    hermes config set model.default glm-5-turbo
    hermes config set model.provider zhipu
  else
    hermes -p "$p" config set model.default glm-5-turbo
    hermes -p "$p" config set model.provider zhipu
  fi
done
```

### 3.5 批量重启 Gateway

```bash
# 重启所有运行中的 profile
hermes profile list 2>/dev/null | grep "running" | awk '{print $1}' | sed 's/◆//' | while read p; do
  hermes -p "$p" gateway restart
done
```

### 3.6 操作后验证（重要！）

每次切换后，务必执行验证确认生效：

```bash
# 方法 1：查看配置是否写入成功
hermes -p <profile> config show | grep "default:" -A1

# 预期输出：
#   default: glm-5.1      ← 看到这里是新模型名就对了

# 方法 2：发送测试消息确认模型实际响应
hermes -p <profile> chat -q "你是什么模型？回答模型名称即可" -Q

# 方法 3：确认 Gateway 状态
hermes -p <profile> gateway status

# 预期输出：
# ◆ reasoner: running     ← 必须是 running
```

**⚠️ 如果验证方法 2 的回答仍是旧模型**，说明 Gateway 没有成功重启，请重新执行 `hermes -p <profile> gateway restart`。

---

## 4. Provider 速查表

| Provider | Env 变量 | Base URL | 说明 |
|---|---|---|---|
| `xiaomi` | `XIAOMI_API_KEY` | `https://token-plan-cn.xiaomimimo.com/v1` | 小米 MiMo |
| `zhipu` | `ZHIPU_API_KEY` | `https://open.bigmodel.cn/api/coding/paas/v4` | 智谱 Coding Plan（国内，订阅制） |
| `zhipu-direct` | `ZHIPU_API_KEY` | `https://open.bigmodel.cn/api/paas/v4` | 智谱 Direct API（国内，按量计费） |
| `zai` | `ZAI_API_KEY` | `https://api.z.ai/api/coding/paas/v4` | 智谱 Coding Plan（国际版，订阅制） |
| `zai-direct` | `ZAI_API_KEY` | `https://api.z.ai/api/paas/v4` | 智谱 Direct API（国际版，按量计费） |

**智谱四通道说明：**

- **`zhipu`** — 国内 Coding Plan，订阅制，仅限 Coding 工具环境，端点 `open.bigmodel.cn`
- **`zhipu-direct`** — 国内通用 Direct API，按量计费，无使用场景限制，可访问全部模型（含 glm-5.1）
- **`zai`** — 国际版 Coding Plan，订阅制，端点 `api.z.ai`
- **`zai-direct`** — 国际版通用 Direct API，按量计费，端点 `api.z.ai`

国内版和国际版使用不同的 API Key（`ZHIPU_API_KEY` vs `ZAI_API_KEY`），切换时需确认 `.env` 中有对应 key。

**自定义 Provider** 在 `config.yaml` 的 `custom_providers:` 中定义：
```yaml
custom_providers:
- name: zhipu
  base_url: https://open.bigmodel.cn/api/coding/paas/v4
  api_key: xxx
  api_mode: chat_completions
```

**⚠️ Base URL 规则：**
- 内置 provider（xiaomi/zhipu/openrouter 等）：`base_url` 可省略，Hermes 自动填充
- 自定义 provider：`base_url` **必须**显式指定，否则报错
- 切换 provider 时如果两个 provider 的 `base_url` 不同，**必须同时设置** `base_url`

---

## 5. 模型参考

### 智谱（国内 `zhipu` / 国际 `zai`）

以下模型同时适用于 `zhipu` / `zhipu-direct` / `zai` / `zai-direct` 四个 provider。

**Coding Plan 可用模型：**

| 模型 | 上下文 | 最大输出 | 适用场景 |
|---|---|---|---|
| `glm-5-turbo` | 200K | 128K | 通用对话，高性价比 |
| `glm-4.7` | 200K | 128K | 通用推理，支持 thinking 模式 |
| `glm-4.5-air` | 200K | 8K | 辅助模型专用，极致性价比 |

**Direct API 额外可用模型：**

| 模型 | 上下文 | 最大输出 | 适用场景 |
| `glm-5.1` | 200K | 128K | 复杂推理，最强能力 |
| `glm-5` | 200K | 128K | 通用推理 |

**端点差异：**

| Provider | Base URL | 可用模型 |
|---|---|---|
| `zhipu` | `open.bigmodel.cn/api/coding/paas/v4` | Coding Plan 模型 |
| `zhipu-direct` | `open.bigmodel.cn/api/paas/v4` | 全部模型 |
| `zai` | `api.z.ai/api/coding/paas/v4` | Coding Plan 模型 |
| `zai-direct` | `api.z.ai/api/paas/v4` | 全部模型 |
文档：https://docs.bigmodel.cn/cn/guide/start/model-overview

### 小米 MiMo

| 模型 | 上下文 | 适用场景 |
|---|---|---|
| `mimo-v2.5-pro` | 1M | 通用对话、长上下文 |
| `mimo-v2.5` | 1M | 辅助模型、高性价比 |
| `mimo-v2-omni` | — | 多模态（vision） |

---

## 6. 典型工作流

### 场景 1：临时切换测试模型

```bash
# 切到测试模型
hermes -p reasoner config set model.default glm-5.1
hermes -p reasoner config set model.provider zhipu
hermes -p reasoner gateway restart

# ✅ 验证切换成功
hermes -p reasoner config show | grep "default:" -A1
# 预期输出：
#   default: glm-5.1

# 测试模型是否正常响应
hermes -p reasoner chat -q "你好，请确认你的模型名称" -Q
# 预期输出应提到 glm-5.1 或智谱

# 测试完毕后切回
hermes -p reasoner config set model.default mimo-v2.5-pro
hermes -p reasoner config set model.provider xiaomi
hermes -p reasoner gateway restart

# ✅ 验证切回成功
hermes -p reasoner config show | grep "default:" -A1
# 预期输出：
#   default: mimo-v2.5-pro
```

### 场景 2：所有 profile 统一切换

```bash
# 批量切换
for p in default cto diary genshin reasoner scout qian-duoduo; do
  if [ "$p" = "default" ]; then
    hermes config set model.default glm-5-turbo
    hermes config set model.provider zhipu
  else
    hermes -p "$p" config set model.default glm-5-turbo
    hermes -p "$p" config set model.provider zhipu
  fi
done

# 批量重启
hermes profile list 2>/dev/null | grep "running" | awk '{print $1}' | sed 's/◆//' | while read p; do
  hermes -p "$p" gateway restart
done

# ✅ 验证全景
bash ~/.hermes/scripts/profile-model-overview.sh
# 预期：所有 profile 的 Model 列都显示 glm-5-turbo
```

### 场景 3：只改辅助模型

```bash
# 换一个更强的 vision 模型（主模型不变）
hermes config set auxiliary.vision.provider zhipu
hermes config set auxiliary.vision.model glm-5.1
hermes gateway restart

# ✅ 验证
hermes config show | grep -A3 "vision:"
# 预期输出：
#   vision:
#     provider: zhipu
#     model: glm-5.1
```

### 场景 4：Delegation 用便宜模型省钱

```bash
# delegation 用轻量模型，主模型保持强模型
hermes config set delegation.model glm-5-turbo
hermes config set delegation.provider zhipu
hermes gateway restart

# ✅ 验证 delegation 和主模型分离
hermes config show | grep -E "(default:|delegation)" -A2
# 预期：主模型仍为原模型，delegation 显示 glm-5-turbo
```

---

## 7. 异常处理与排错指南

### 🔴 错误 1："no API key found"

**症状：** 切换 provider 后发消息报错 `RuntimeError: no API key found for provider <name>`

**原因：** 每个 profile 有独立的 `.env` 文件，切换 provider 后目标 profile 中缺少对应 key。

**修复步骤：**
```bash
# Step 1: 确认哪个 profile 缺 key
grep "API_KEY\|_KEY=" ~/.hermes/profiles/<name>/.env

# Step 2: 检查目标 key 是否存在
grep "ZHIPU_API_KEY" ~/.hermes/profiles/<name>/.env
# 如果没有输出 → 缺少该 key

# Step 3: 添加缺失的 key（以智谱国内版为例）
echo "ZHIPU_API_KEY=your_key_here" >> ~/.hermes/profiles/<name>/.env

# Step 4: 重启 Gateway
hermes -p <profile> gateway restart
```

**预防：** 切换 provider 前先检查目标 profile 的 `.env`：
```bash
# 快速检查：目标 profile 是否有目标 provider 的 key
grep -l "ZHIPU_API_KEY" ~/.hermes/profiles/<name>/.env && echo "✅ 有智谱 key" || echo "❌ 缺智谱 key"
```

### 🔴 错误 2："context too small"

**症状：** compression 或 session_search 报错 `context too small` 或类似上下文不足的错误。

**原因：** compression 模型的 `context_length` 至少需要 16K，session_search 建议 32K+。

**修复步骤：**
```bash
# Step 1: 确认当前 compression 模型
hermes config show | grep -A5 "compression:"

# Step 2: 换成上下文足够的模型
hermes config set auxiliary.compression.model mimo-v2.5
hermes config set auxiliary.compression.provider xiaomi

# Step 3: 重启
hermes gateway restart
```

### 🔴 错误 3：切换不生效（模型仍是旧的）

**症状：** 执行了 `config set` 但发消息仍用旧模型。

**原因：** Gateway 未重启，或重启失败。

**排查步骤：**
```bash
# Step 1: 确认配置已写入
hermes -p <profile> config show | grep "default:"
# 如果显示的仍是旧模型 → config set 没成功，检查命令是否有报错

# Step 2: 确认 Gateway 状态
hermes -p <profile> gateway status
# 如果不是 running → Gateway 没启动，需要 start 而不是 restart

# Step 3: 强制重启
hermes -p <profile> gateway restart

# Step 4: 再次验证
hermes -p <profile> chat -q "你是什么模型？" -Q
```

### 🔴 错误 4：config set 报 YAML 格式错误

**症状：** `hermes config set` 返回 YAML parse error。

**原因：** config.yaml 中已有语法错误（缩进不对、特殊字符等）。

**修复步骤：**
```bash
# Step 1: 找到有问题的 profile
cat ~/.hermes/profiles/<name>/config.yaml | python3 -c "import sys,yaml; yaml.safe_load(sys.stdin)" 2>&1
# 会报出具体行号

# Step 2: 检查该行附近内容
sed -n '<行号-2>,<行号+2>p' ~/.hermes/profiles/<name>/config.yaml

# Step 3: 手动修复 YAML 语法后重新 config set
```

**预防：** 批量操作前备份配置：
```bash
cp ~/.hermes/profiles/<name>/config.yaml ~/.hermes/profiles/<name>/config.yaml.bak
```

### 🔴 错误 5：profile 名称不对

**症状：** `hermes -p <name> config set ...` 报错 `profile not found`。

**原因：** profile 名称区分大小写，或拼写错误。

**排查：**
```bash
# 列出所有 profile
hermes profile list

# 预期输出示例：
# ◆ default
# ◆ cto
# ◆ diary
# ◆ genshin
# ◆ reasoner
# ◆ scout
# ◆ qian-duoduo
```

### 🟡 错误 6：辅助模型设为空后行为异常

**症状：** 辅助模型字段留空后，某些功能（如图片识别）不工作。

**原因：** Hermes 会尝试 `auto` 模式自动匹配，但可能失败或选到不合适的模型。

**建议：** 始终显式配置所有辅助模型，尤其是 `vision` 和 `compression`。

### 🔴 错误 8：脚本全景模式只输出表头就退出（set -euo pipefail + awk 陷阱）

**症状：** `bash ~/.hermes/scripts/profile-model-overview.sh` 只输出表头和分隔线就退出（exit code 2），没有任何 profile 数据。

**原因：** 脚本使用 `set -euo pipefail`。`yaml_get()` 函数中的 `awk` 在 YAML 中找不到匹配行时返回 exit code 2。在 `set -e` 下，`var=$(awk ...)` 非零退出会导致整个脚本立即终止。

**修复：** 在 `yaml_get()` 函数的 awk 调用末尾添加 `|| true`：
```bash
# 修复前（会因 awk exit 2 导致脚本退出）
main_model=$(awk '...' "$file" 2>/dev/null)

# 修复后（无匹配时返回空字符串）
main_model=$(awk '...' "$file" 2>/dev/null || true)
```

**通用教训：** 在 `set -euo pipefail` 脚本中，所有**解析类**命令（awk/grep/sed 从文件提取值）的 command substitution 必须加 `|| true`，因为"没找到"是正常语义，不是错误。只有**操作类**命令（写文件、执行配置变更）的失败才应该触发 `set -e` 退出。

### 🔴 错误 9：awk 变量名 `sub` 与 gawk 内置函数冲突（3 层 YAML 解析失败）

**症状：** 详情模式中辅助模型全部显示 `(auto)`，即使 config.yaml 中已显式配置了 provider 和 model。

**原因：** `yaml_get()` 的 3 层嵌套版本使用 `sub` 作为 awk 变量名传入 `-v sub="^  vision:"`。`sub` 是 gawk 的内置函数名（用于字符串替换），gawk 拒绝将其作为变量名，报 `fatal: cannot use gawk builtin 'sub' as variable name`。由于这个错误被 `2>/dev/null || true` 吞掉了，脚本不会崩溃，但所有 3 层解析（`auxiliary.vision.model` 等）静默返回空。

**修复：** 将变量名从 `sub` 改为 `subsec`：
```bash
# 修复前（gawk 报错，静默返回空）
awk -v sub="^  vision:" '... $0 ~ sub ...'

# 修复后（正常匹配）
awk -v subsec="^  vision:" '... $0 ~ subsec ...'
```

**通用教训：** awk 中不要使用以下变量名，它们是 gawk 内置函数：`sub`, `gsub`, `match`, `split`, `sprintf`, `substr`, `tolower`, `toupper`, `close`, `system`, `fflush`, `delete`, `typeof`, `isarray`。安全做法是加后缀或前缀，如 `subsec`、`sub_pattern`。

### 🟡 错误 7：base_url 未设置导致请求发错地址

**症状：** 切换 provider 后请求发到了错误的 API 端点，返回 401 或连接超时。

**原因：** 自定义 provider 必须显式指定 `base_url`。

**修复：**
```bash
hermes -p <profile> config set model.base_url https://open.bigmodel.cn/api/coding/paas/v4
hermes -p <profile> gateway restart
```

---

## 8. 常见问题 (FAQ)

### Q1: 切换模型后为什么没生效？
**A:** 模型配置只对新 session 生效，已运行的 Gateway 必须重启：
```bash
hermes -p <profile> gateway restart
```
验证方法：`hermes -p <profile> gateway status` 确认状态为 `running`。

### Q2: 切换 provider 后报 "no API key found"？
**A:** 每个 profile 有独立的 `.env` 文件，需要确保目标 profile 的 `.env` 中有对应 key：
```bash
# 检查 key 是否存在
grep "ZHIPU\|XIAOMI\|DEEPSEEK" ~/.hermes/profiles/<name>/.env

# 如果没有，手动添加
echo "ZHIPU_API_KEY=your_key_here" >> ~/.hermes/profiles/<name>/.env
```

### Q3: 辅助模型设为空会怎样？
**A:** Hermes 会尝试 `auto` 模式自动匹配，但可能失败或选到不合适的模型。建议显式配置所有辅助模型，特别是 `vision` 和 `compression`。

### Q4: `hermes config set` 会覆盖其他字段吗？
**A:** 不会。`config set` 是逐字段 YAML merge，只修改指定的字段，不影响其他配置。

### Q5: compression 模型报错 "context too small"？
**A:** compression 模型的 `context_length` 至少需要 16K，否则压缩会失败。选择模型时注意其上下文窗口大小。

### Q6: default profile 的 `-p` 参数写法？
**A:** default profile **不加** `-p` 参数，其他 profile **必须加** `-p <name>`。这是最常见的错误。

### Q7: 如何确认切换后的模型实际生效了？
**A:**
```bash
# 方法 1：查看配置
hermes -p <profile> config show | grep "default:" -A1

# 方法 2：发送测试消息
hermes -p <profile> chat -q "你是什么模型？回答模型名称即可" -Q

# 方法 3：查看 Gateway 状态
hermes -p <profile> gateway status
```

### Q8: 批量切换后发现切错了，怎么回滚？
**A:** 如果操作前备份了配置：
```bash
# 恢复备份
cp ~/.hermes/profiles/<name>/config.yaml.bak ~/.hermes/profiles/<name>/config.yaml
hermes -p <profile> gateway restart
```
**预防：** 批量操作前务必执行备份命令（见 §3.4）。

### Q9: 自定义 provider 和内置 provider 的区别？
**A:**
- **内置 provider**（xiaomi/zhipu/openrouter 等）：`base_url` 和 `api_key` 的 env 变量名由 Hermes 自动识别，只需设置 `provider` 名即可
- **自定义 provider**：在 `custom_providers` 中定义，切换时必须同时设置 `base_url`

### Q10: Gateway restart 和 start 的区别？
**A:**
- `restart`：停止后重新启动，适用于已运行的 profile
- `start`：首次启动或停止后的启动
- 如果 `restart` 报错说没有运行中的进程，改用 `start`

---

## 9. 反模式与边界条件

### ❌ 反模式 1：只改 model 不改 provider

```bash
# ❌ 错误：模型名和 provider 不匹配
hermes config set model.default glm-5.1
# 但 provider 仍是 xiaomi → 请求会发到小米的 API 找 glm-5.1 → 报错

# ✅ 正确：同时切换
hermes config set model.default glm-5.1
hermes config set model.provider zhipu
```

### ❌ 反模式 2：切了 provider 不重启

```bash
# ❌ 错误：改了配置就以为生效了
hermes config set model.provider zhipu
# ...直接发消息 → 仍用旧 provider

# ✅ 正确：改完必须重启
hermes config set model.provider zhipu
hermes gateway restart
```

### ❌ 反模式 3：切换 provider 不检查 API Key

```bash
# ❌ 错误：直接切 provider
hermes -p diary config set model.provider zhipu

# ✅ 正确：先检查 key 存在
grep "ZHIPU_API_KEY" ~/.hermes/profiles/diary/.env && \
  hermes -p diary config set model.provider zhipu || \
  echo "❌ 先添加 ZHIPU_API_KEY 到 .env"
```

### ❌ 反模式 4：default profile 加了 -p 参数

```bash
# ❌ 错误
hermes -p default config set model.default glm-5.1
# 可能报错或行为不可预期

# ✅ 正确
hermes config set model.default glm-5.1
```

### ❌ 反模式 5：用 `sed ... | bash` 测试脚本

```bash
# ❌ 错误：管道执行时 $0 变成 'bash'，dirname "$0" 返回 /usr/bin
sed '14a\echo DEBUG' ~/.hermes/scripts/profile-model-overview.sh | bash

# ✅ 正确：直接执行
bash ~/.hermes/scripts/profile-model-overview.sh
# 或加 debug 用 bash -x
bash -x ~/.hermes/scripts/profile-model-overview.sh 2>&1 | head -50
```

**原因：** 管道传入 bash 时，`$0` 是 `bash` 而非脚本路径。脚本中 `SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"` 会解析到 `/usr/bin`，导致 `PRESETS_FILE` 路径错误。

### ⚠️ 边界条件 1：批量操作中某个 profile 失败

`for` 循环批量切换时，如果某个 profile 的 config.yaml 格式有误，该 profile 会失败但不影响其他。批量操作后**必须**检查所有 profile 的结果：
```bash
bash ~/.hermes/scripts/profile-model-overview.sh
# 逐行检查 Model 列是否全部正确
```

### ⚠️ 边界条件 2：compression 模型上下文不足

`compression` 和 `session_search` 对上下文大小有要求：
- compression：至少 16K
- session_search：建议 32K+
- 如果模型上下文太小，这些功能会静默失败或报错

### ⚠️ 边界条件 3：delegation 设为空字符串 vs 删除字段

```bash
# 设为空字符串 → 回到继承主模型的行为
hermes config set delegation.model ""

# 直接编辑 config.yaml 删除 delegation 整块 → 可能导致解析问题
# ❌ 不推荐直接编辑，用 config set
```

### ⚠️ 边界条件 4：.env 中有同名 key 时取最后一个

如果 `.env` 中有多行同一个 key（如两行 `ZHIPU_API_KEY=xxx`），Hermes 取**最后一个**。这可能是预期行为，也可能造成困惑。

---

## 10. 限制与注意事项

1. **API Key 隔离**：每个 profile 有独立 `.env`，切换 provider 前务必确认目标 key 存在
2. **Gateway 重启必须**：所有模型修改只对新 session 生效，已运行的 gateway 必须 `restart`
3. **辅助模型 context_length**：compression 至少需要 16K，session_search 建议 32K+
4. **批量操作不可逆**：批量切换前建议备份配置：`cp ~/.hermes/profiles/<name>/config.yaml ~/.hermes/profiles/<name>/config.yaml.bak`
5. **自定义 Provider 需要 base_url**：使用自定义 provider 时必须在 `config set` 中指定 `base_url`
6. **profile 名称区分大小写**：`Profile` ≠ `profile`，使用 `hermes profile list` 确认准确名称
7. **default profile 不加 -p**：对 default profile 操作时不加 `-p` 参数，这是最常见的错误

---

## 11. Profile Model Manager 脚本

脚本支持三种模式：

### 脚本部署

脚本源文件在 skill 目录中：`~/.hermes/profiles/<profile>/skills/profile-model-manager/scripts/`。使用前需部署到 `~/.hermes/scripts/`：

```bash
# 首次部署或更新脚本
SKILL_DIR="$HOME/.hermes/profiles/cto/skills/profile-model-manager/scripts"
cp "$SKILL_DIR/profile-model-overview.sh" ~/.hermes/scripts/
cp "$SKILL_DIR/provider-presets.json" ~/.hermes/scripts/
chmod +x ~/.hermes/scripts/profile-model-overview.sh
```

**⚠️ 脚本版本同步：** `~/.hermes/scripts/` 里的脚本是独立副本，不会随 skill 更新自动同步。每次更新 skill 后需要重新部署。检查版本是否同步：
```bash
# 比较文件大小即可快速判断
wc -c ~/.hermes/scripts/profile-model-overview.sh \
      ~/.hermes/profiles/cto/skills/profile-model-manager/scripts/profile-model-overview.sh
```

### 11.1 全景模式（无参数）

```bash
bash ~/.hermes/scripts/profile-model-overview.sh
```

显示所有 profile 的模型配置表格（主模型、Provider、Vision、Compression、WebExtract、Delegation）。

### 11.2 详情模式（单个 profile）

```bash
bash ~/.hermes/scripts/profile-model-overview.sh <profile>
```

显示指定 profile 的完整模型配置，包括主模型、所有辅助模型、delegation 的每个字段（provider / model / timeout / context_length 等）。

### 11.3 智能切换模式（一键配全）

```bash
# 预览模式：只显示变更对比，不修改任何配置
bash ~/.hermes/scripts/profile-model-overview.sh <profile> <provider>

# 执行模式：应用所有配置 + 重启 Gateway
bash ~/.hermes/scripts/profile-model-overview.sh <profile> --apply <provider>
```

脚本会根据 provider 预设，自动为所有角色分配合适的模型：

| 角色 | 说明 |
|---|---|
| 主模型 | 对话用，选该 provider 最强的通用模型 |
| vision | 图片识别，选多模态模型（无原生多模态则用主模型） |
| compression | 上下文压缩，选轻量高速模型 |
| web_extract | 网页内容提取，选轻量高速模型 |
| session_search | 历史会话搜索，选轻量高速模型 |
| delegation | 子 agent，选性价比高的模型 |

**预览输出示例：**
```
╔══════════════════════════════════════════════════════════╗
║  Profile: reasoner              Provider: zhipu           ║
╚══════════════════════════════════════════════════════════╝

  角色             当前值                    → 新值                     变更
  ──────────────────────────────────────────────────────────────────────────
  主模型           mimo-v2.5-pro             → glm-5-turbo              ✅
  provider         xiaomi                    → zhipu                      ✅
  vision           mimo-v2-omni              → glm-5-turbo              ✅
  compression      mimo-v2.5                 → glm-5-turbo              ✅
  web_extract      mimo-v2.5                 → glm-5-turbo              ✅
  session_search   mimo-v2.5                 → glm-5-turbo              ✅
  delegation       mimo-v2.5                 → glm-5-turbo              ✅

📋 以上为预览，未做任何修改。
💡 确认执行：bash $0 reasoner --apply zhipu
```

---

## 发布到 SkillHub

参见 `references/skillhub-and-github-publishing.md`（含 SkillHub Web 发布 + GitHub 仓库管理流程）。

## 脚本调试记录

参见 `references/script-debugging-log.md`（profile-model-overview.sh 的 bug 发现与修复过程）。
