---
name: model-manager
description: OpenClaw 模型配置管理技能。用于添加、删除、更新、查看、切换、检测模型配置。当用户需要：(1) 添加新模型到配置 (2) 删除模型 (3) 更新模型参数（contextWindow、maxTokens等）(4) 查看当前模型列表 (5) 切换主模型 (6) 检查模型可用状态（测试连接）(7) 修复模型配置问题时使用此技能。
---

# Model Manager

OpenClaw 模型配置管理技能，用于统一维护 `openclaw.json` 中的模型与 provider 配置。

## 适用场景

适合以下场景：
- 添加新的模型或 provider
- 删除失效或不再使用的模型
- 修正模型参数（如 `contextWindow`、`maxTokens`、`reasoning`）
- 切换 OpenClaw 默认主模型
- 检查模型连通性与可用状态
- 排查 `401 / 403 / 429 / 400 / 5xx` 等模型调用问题
- 批量整理和优化模型配置

## 核心能力

- 添加模型
- 删除模型
- 更新模型参数
- 查看当前模型列表
- 切换主模型
- 检查模型可用状态
- 并行测试模型连接
- 辅助定位常见错误码问题

## 配置文件位置

```text
C:\Users\Administrator\.openclaw\openclaw.json
```

## 常见用户请求示例

- “把主模型改成 `minmax/MiniMax-M2.7`”
- “检查所有模型状态”
- “测试模型连接”
- “给 `bailian2/qwen3-max-2026-01-23` 补上参数”
- “删除一个不用的 provider”
- “把不可用模型找出来”
- “查看当前配置了哪些模型”

## 工作流程

### 1. 添加模型

当用户提供模型信息时：

1. 读取当前配置：`gateway(action=config.get)`
2. 编辑配置文件添加模型到 `models.providers`
3. 可选：添加别名到 `agents.defaults.models`
4. 重启生效：`gateway(action=restart, note="...")`

#### 添加格式

```json
{
  "id": "model-id",
  "name": "Model Display Name",
  "reasoning": true,
  "input": ["text"],
  "contextWindow": 200000,
  "maxTokens": 8192
}
```

### 2. 删除模型

1. 读取配置
2. 从 `models.providers.<provider>.models` 删除模型
3. 从 `agents.defaults.models` 删除别名
4. 重启生效

### 3. 更新模型参数

1. 读取配置
2. 修改目标模型的参数
3. 重启生效

### 4. 查看模型列表

直接使用：`gateway(action=config.get)` 查看完整配置。

### 5. 切换主模型

切换默认使用的模型：

1. 读取配置确认目标模型存在
2. 修改 `agents.defaults.model.primary` 为目标模型 ID
3. 重启生效：`gateway(action=restart, note="主模型已切换为 xxx")`

#### 切换前检查

在切换主模型前应确认：
- 目标模型在当前配置中存在
- provider 配置完整
- 模型不是已知不可用状态（如果刚做过可用性检测）

#### 示例

用户说：
> “把主模型改成 `minmax/MiniMax-M2.7`”

操作：
编辑 `agents.defaults.model.primary` 从当前值改为 `"minmax/MiniMax-M2.7"`

### 6. 检查模型可用状态

测试当前配置中每个模型的连接状态，并按 **状态优先 + 能力排序** 显示结果。

#### 测试流程

1. 读取配置获取所有模型和 provider API key
2. **并行测试**：对所有模型同时发送 HTTP 测试请求（简单 completion，`max_tokens=5`）
3. 解析响应：
   - `200 OK` = 可用
   - `401/403` = 认证失败 / 权限问题
   - `429` = 速率限制
   - `400` = 参数、模型名或请求格式问题
   - `5xx` = 上游服务异常
4. 按 **状态分组**（可用 > RateLimit > 不可用），每组内按 **能力排序**（`contextWindow` 大 + `reasoning=true` 优先）

#### 并行测试实现

使用 PowerShell 的 `Start-Job` 或 OpenClaw 的 `exec` 工具并行执行：

```powershell
$jobs = @()
foreach ($model in $models) {
    $job = Start-Job -ScriptBlock {
        $result = Test-ModelConnection($model)
        return "$modelId | $capability | $status"
    }
    $jobs += $job
}
$results = Receive-Job -Job $jobs -Wait
```

**优势：** 11 个模型的测试时间可从 ~30 秒减少到 ~5 秒。

#### 测试请求格式

根据提供商 API 类型选择格式：

| API 类型 | Header | Endpoint |
|----------|--------|----------|
| openai-completions | `Authorization: Bearer <key>` | `/v1/chat/completions` |
| anthropic-messages | `x-api-key: <key>` | `/v1/messages` |

#### 排序规则

1. **状态优先**：✅ 可用 > ⚠️ RateLimit > ❌ 不可用
2. **能力排序**：`contextWindow` 大者优先，`reasoning=true` 优先

#### 输出格式

用户说：
> “检查可用状态”
或
> “测试模型连接”

按照 **模型名称 | 能力 | 状态** 格式显示：

```text
### ✅ 可用模型
bailian2/qwen3-max-2026-01-23 | 128K, reasoning | ✅ 可用
volcano/deepseek-v3.2 | 200K | ✅ 可用
volcano/glm-4.7 | 200K | ✅ 可用
bailian/glm-5 | 32K | ✅ 可用
bailian2/glm-5 | 32K | ✅ 可用

### ⚠️ RateLimit
minmax/MiniMax-M2.7 | 204K, reasoning | ⚠️ RateLimit

### ❌ 不可用
注册机/gpt-5-codex | 400K | ❌ 401
注册机/gpt-5.4 | 400K | ❌ 401
siliconflow/Pro/deepseek-ai/DeepSeek-V3.2 | 200K, reasoning | ❌ 401
siliconflow/zai-org/GLM-4.6 | 200K | ❌ 401
bailian/qwen1.5-32b-chat | 32K | ❌ 400
```

---
**格式：模型名称 | 能力 | 状态**

## 常见错误码解释

- `401 / 403`：API key 无效、过期、无权限，或 provider 认证配置错误
- `429`：达到速率限制，通常需要等待后重试
- `400`：模型名错误、参数不兼容、请求格式不符合 provider 要求
- `5xx`：上游服务异常，通常不是本地配置本身的问题

## v1.0.1 增强点

本版本相对 v1.0.0 的增强主要包括：

1. **补全发布说明**
   - 增加适用场景
   - 增加核心能力说明
   - 增加典型用户请求示例

2. **增强并行检测说明**
   - 明确并行测试方式
   - 明确排序规则
   - 明确状态分组逻辑

3. **增强错误处理说明**
   - 补充常见错误码解释
   - 强调切换主模型前的检查步骤
   - 强调修改后需重启生效

## 常用模型参考

参见 `references/model-info.md` 获取各 provider 支持的模型列表。

## 注意事项

- 每次修改后需要重启 Gateway：`gateway(action=restart)`
- JSON 文件不支持注释，编辑时注意移除 `//` 注释
- `contextWindow` 和 `maxTokens` 单位是 tokens
- `reasoning: true` 表示支持思考模式
- 修改主模型、provider、模型参数后，都应提醒用户重启生效
