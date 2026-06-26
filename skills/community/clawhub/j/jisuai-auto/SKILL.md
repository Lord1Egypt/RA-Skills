---
name: jisuai-auto
description: 一键配置 OpenClaw 对接 aicodee.com MiniMax 模型中转服务。当用户需要配置、设置、激活 aicodee 的 MiniMax API 时触发。触发词：jisuai-auto、配置jisuai、配置爱代码、配置MiniMax。
---

# jisuai-auto

一键将 aicodee.com MiniMax 中转 API 配置到 OpenClaw。

## 工作流程

1. **从用户消息中提取 API 信息**（见下方详细规则）
2. **校验必填字段**：API Key 不能为空
3. **读取当前 openclaw.json**
4. **运行配置脚本**：`python scripts/configure.py --base-url <URL> --api-key <KEY>`
5. **脚本自动完成**：
   - 在 `models.providers` 下新增 `jisuaivauto` 提供商
   - 将 `agents.defaults.model.primary` 改为 `jisuaivauto/MiniMax-M2.7-highspeed`
6. **告知用户配置完成**

---

## 信息提取规则

### 提取顺序（优先级从高到低）

1. 先尝试从**代码块**（```...```）中提取
2. 再从**普通文本**中提取

### 字段提取

| 字段 | 匹配模式 | 示例 |
|------|----------|------|
| **API Base URL** | 正则：`(?:API\s*Base\s*URL|baseurl|base_url|接口地址|地址)[：:\s]*(\S+)` | `API Base URL：https://v2.aicodee.com` |
| **API Key** | 正则：`(?:API\s*Key|apikey|api_key|密钥|key)[：:\s]*((?:sk-\|sk3)[a-zA-Z0-9]{20,})` | `API Key：sk-3a099f856d7664c76c60905895c6a36f` |
| **模型名称** | 正则：`(?:模型名称|模型|model)[：:\s]*([^\s\n]+)`，取第一个 MiniMax 开头的 | `模型名称：MiniMax-M2.7-highspeed` |

### 默认值

- API Base URL：**必填**，从消息提取；无法提取时报错要求用户提供
- 模型名称：默认 `MiniMax-M2.7-highspeed`

### 常见变体兼容

- `API Base URL：`
- `API Base URL：`
- `baseurl:`
- `接口地址：`
- `API Key：`
- `apikey:`
- `密钥：`

### 提取示例

**输入（混乱格式）：**
```
API Base URL：https://v2.aicodee.com
API Key:sk-3a099f856d7664c76c60905895c6a36f
模型: MiniMax-M2.5-highspeed / MiniMax-M2.7-highspeed
```

**提取结果：**
- base-url = `https://v2.aicodee.com`
- api-key = `sk-3a099f856d7664c76c60905895c6a36f`
- model-id = `MiniMax-M2.5-highspeed`（取第一个 MiniMax 开头的）

---

## 错误处理

- **API Key 缺失**：告知用户「未找到 API Key，请确保消息中包含 API Key」
- **脚本执行失败**：回显错误信息，建议手动检查 openclaw.json

## 脚本用法

```bash
python scripts/configure.py --base-url "https://v2.aicodee.com" --api-key "sk-3a099f856d7664c76c60905895c6a36f" --provider-name "jisuaivauto"
```

**参数说明：**
- `--base-url`：API 服务器地址
- `--api-key`：**必填**，API Key
- `--provider-name`：提供商名称，默认 `jisuaivauto`
- `--model-id`：模型 ID，默认 `MiniMax-M2.7-highspeed`
