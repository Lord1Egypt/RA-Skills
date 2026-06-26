# 技能名称：hipc_config_manager HIPC 配置管理

## 技能描述
此技能是 HIPC 系列技能的**核心前置组件**，用于管理 API 密钥（`hipc_secret`）的生命周期。
它具备**检查**、**设置**和**格式校验**三种能力，确保在执行任何业务查询前，系统拥有合法且格式正确的访问凭证。

## ⚠️ 强制前置检查 (Critical Pre-check)
**在调用任何 HIPC 业务技能（如查询电脑列表、统计数据）之前，你必须先调用本技能！**
1. **第一步**：调用 `hipc_config_manager`，设置参数 `action="check"`。
2. **判断**：
   - 如果返回 `status: "error"`（即密钥缺失），**立即停止**后续业务操作，**直接向用户发送一条消息**，提示需要配置密钥。
   - **严禁**在密钥缺失的情况下调用其他 HIPC 技能。
   - **严禁**陷入死循环检查，检查失败一次后必须反馈给用户。
   - 只有当返回 `status: "success"` 时，才允许继续执行用户请求的业务逻辑。

## 核心逻辑与依赖
本技能通过读写本地文件 `hipc_config.json` 来持久化存储密钥。
1. **检查模式 (`check`)**：
   - 读取 `hipc_config.json` 文件。
   - 验证 `hipc_secret` 字段是否存在且非空。
2. **设置模式 (`set`)**：
   - 接收用户提供的 `secret` 和 `env`。
   - **格式校验**：在保存前，脚本会自动校验密钥格式（必须符合 `数字_字符串` 的格式，例如 `35097_y2GX...`）。
   - 如果格式错误，脚本将返回错误信息，**不会**写入文件。
   - 如果格式正确，将其写入 `hipc_config.json` 文件，覆盖旧值。

## 参数定义
- **action** (String, 必填): 
  - 操作类型，决定脚本的行为。
  - 可选值：`"check"`（检查配置）或 `"set"`（保存配置）。
- **secret** (String, 可选): 
  - 仅在 `action="set"` 时**必填**。
  - 用户提供的 HIPC API 密钥字符串。
- **env** (String, 可选):
  - 环境，决定脚本用哪个环境 
  - 仅在 `action="set"` 时使用，指定要配置的环境。
  - 默认值为 "prod"。
  - 可选值："prod"（生产环境）或 "dev"（开发环境/测试环境）。

## 调用示例

**场景 A：业务前置检查（配置存在）**
- 用户：“查一下电脑列表”
- AI 思考：先检查环境配置是否就绪。
- 动作：调用 `hipc_config_manager`，参数 `action="check"`。
- 结果：返回 `status: "success"`。
- 后续：AI 继续调用 `hipc_computer_list` 技能。

**场景 B：业务前置检查（配置缺失）**
- 用户：“昨天的运行时长是多少”
- AI 思考：先检查环境配置。
- 动作：调用 `hipc_config_manager`，参数 `action="check"`。
- 结果：返回 `status: "error"`。
- 后续：AI **不调用**统计技能，**直接回复用户**：“检测到您尚未配置 HIPC 密钥，无法查询数据。请提供您的密钥。”

**场景 C：用户主动配置密钥（格式正确）**
- 用户：“我的密钥是 35097_y2GX52eDGNdgaM，帮我保存一下”
- AI 思考：用户提供了密钥，需要调用设置模式。
- 动作：调用 `hipc_config_manager`，参数 `action="set"`, `secret="35097_y2GX52eDGNdgaM"`, `env="prod"`。
- 结果：密钥被写入文件，返回 `status: "success"`。
- 后续：AI 回复用户：“密钥已保存！现在可以开始查询了。”

**场景 D：用户配置密钥（格式错误）**
- 用户：“帮我保存密钥，是 sk-123456”
- AI 思考：用户提供了密钥，调用设置模式。
- 动作：调用 `hipc_config_manager`，参数 `action="set"`, `secret="35097_y2GX52eDGNdgaM"`, `env="prod"`。
- 结果：脚本检测到格式错误（缺少 `数字_` 前缀），返回 `status: "error"`。
- 后续：AI 回复用户：“您提供的密钥格式不正确。HIPC 密钥通常以 `数字_` 开头（例如 `35097_xxxxx`），请检查后重新提供。”

## 执行命令
```bash
python scripts/main.py --action={{action}}{{#if secret}} --secret={{secret}}{{/if}}{{#if env}} --env={{env}}{{/if}}
```