# Guardrails node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Guardrails node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.guardrails`
- node group: `core-nodes`

## 核心要点

- Documentation for the Guardrails node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Check Text for Violations**: Provides a full set of guardrails. Any violation will send items to **Fail** branch.
- **Sanitize Text**: Provides a subset of guardrails that can detect URLs, regular expressions, secret keys, or personally identifiable information (PII), such as phone numbers and credit card numbers. The node replaces detected violations with placeholders.
- **Keywords:** Checks if specified keywords appear in the input text.
- **Keywords**: A comma-separated list of words to block.
- **Jailbreak:** Detects attempts to bypass AI safety measures or exploit the model.
- **Customize Prompt**: (Boolean) If you turn this on, a text input appears with the default prompt for the jailbreak detection model. You can change this prompt to fine-tune the guardrail.
- **Threshold**: A value between 0.0 and 1.0. This represents the confidence level required from the AI model to flag the input as a jailbreak attempt. A higher threshold is stricter.
- **NSFW:** Detects attempts to generate Not Safe For Work (NSFW) content.
- **Customize Prompt**: (Boolean) If you turn this on, a text input appears with the default prompt for the NSFW detection model. You can change this prompt to fine-tune the guardrail.
- **Threshold**: A value between 0.0 and 1.0 representing the confidence level required to flag the content as NSFW.
- **PII:** Detects personally identifiable information (PII) in the text.
- **Type**: Choose which PII entities to scan for:
- **All**: Scans for all available entity types.
- **Selected**: Allows you to choose specific entities from a list.
- **Entities**: (Appears if **Type** is **Selected**) A multi-select list of PII types to detect (for example, `CREDIT_CARD`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, and `US_SSN`).
- **Secret Keys:** Detects the presence of secret keys or API credentials in the text.
- **Permissiveness**: How strict or permissive the detection should be when flagging secret keys:
- **Strict**

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

