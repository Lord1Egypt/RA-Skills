---
name: medgroup-drgdip-skill
description: 使用已在 OpenClaw 本机连接的 MedGroup MCP，查询 DRG/DIP 城市与规则、检索 ICD 编码、执行分组和结算测算、查询 CC/MCC。适用于医保分组、编码与规则核对；结果用于专业辅助。
license: MIT-0
metadata: {"openclaw":{"emoji":"🩺","homepage":"https://medgroup.medchat.fun","skillKey":"medgroup-drgdip-skill"}}
---

# DRG/DIP 工具包（MedGroup）

使用当前 OpenClaw 任务中实际连接的 MedGroup MCP 完成查询和计算。技能负责识别任务、追问参数、选择工具、处理错误和引用结果；业务数据与计算结果以真实工具返回为准。

## 连接前提

- 先确认 OpenClaw 已发现名为 `medgroup` 的 MCP 服务器及其工具。若未连接，引导用户在 OpenClaw 的 `Settings → MCP` 中添加服务器，不要让用户在对话中发送密钥。
- MCP 地址为 `https://medgroup.medchat.fun/mcp`，传输方式为 `streamable-http`，认证请求头为 `Authorization: Bearer <用户自己的 MedGroup SSE / Skill Key>`。
- 用户可在 `https://medgroup.medchat.fun/settings/apikeys` 创建或撤销 `SSE / Skill Key`。密钥只填入用户自己的 OpenClaw 本地 MCP 配置，不写入技能、仓库、截图或聊天记录。
- 保存配置后，用 `openclaw mcp doctor medgroup --probe` 验证连接；若当前会话仍未发现工具，新建会话或重启持有 MCP 连接的 OpenClaw 进程。
- 优先使用合成或脱敏数据。不要索取或复述患者姓名、身份证号、联系方式、住院号等身份信息。
- 用户未指定城市或规则版本时，先调用 `get_city_list`，再请用户确认完整名称。不要擅自用“全国版”代替地方版本。
- 用户只提供疾病或手术名称时，先调用 `search_icd`；诊断使用 `type="icd10"`，手术或操作使用 `type="icd9"`。列出候选编码并请用户确认后再分组。

## 工具选择

- `get_city_list`：查看支持的城市与规则版本。
- `search_icd`：按名称检索诊断或手术、操作编码。
- `drg_grouping`：根据城市、诊断、手术、性别、年龄、住院日等进行 DRG 分组。
- `dip_grouping`：根据城市、诊断、手术、性别、年龄、住院日等进行 DIP 分组。
- `calculate_settlement`：按病种分值、费用、点值和费率进行情景测算。
- `find_code_info`：查询诊断编码在指定城市 DRG 规则中的 MDC/ADRG 信息。
- `get_rule_details`：查看某个 DRG 或 DIP 编码的规则详情。
- `check_dip_rule`：核对病例是否满足指定 DIP 病种规则。
- `get_cc_status`：按指定城市规则查询其他诊断的 CC/MCC 与排除状态。

## 参数追问

执行 DRG/DIP 分组前，至少确认完整城市或版本名称、主要诊断编码、性别和年龄。按任务补充其他诊断编码、手术或操作编码、住院天数和 ICU 状态。

多个其他诊断或手术编码要保持用户给出的顺序。编码存在歧义、灰码或未确认候选时，先说明问题并暂停分组，不自行替换编码。

## 结果表达

- 明确写出实际调用的工具名和城市或版本；不要把模型常识写成工具返回。
- 分组结果优先引用工具返回的 MDC、ADRG、DRG 或 DIP 编码、名称、分值及 CC/MCC 状态。
- 结算结果统一标注为“参数情景测算”，不得表述为医保部门最终结算金额。
- 如需解释规则，继续调用 `get_rule_details`、`find_code_info`、`get_cc_status` 或 `check_dip_rule`，不要凭记忆补全规则。
- 工具结果仅用于医保分组与编码复核辅助，不替代临床诊断、病案编码终审、医保审核或当地正式结算文件。

## 错误处理

- 返回 `401` 或认证失败：提示用户在 MedGroup 密钥管理页检查、轮换或重建 `SSE / Skill Key`，然后只在 OpenClaw 本地 MCP 设置中更新；不要要求用户把密钥发到对话里。
- 额度不足：原样说明额度状态，并提示前往 MedGroup 主站查看或购买；不要反复重试扣额。
- 城市或版本不受支持：调用 `get_city_list` 返回可用名称，请用户重新选择。
- 参数校验失败：指出缺失或格式不正确的字段，只追问完成本次任务所需的最少信息。
- 工具调用失败：明确说明“未获得工具结果”，不得生成看似真实的分组、规则或额度结果。

## 工具可用性检查

当用户询问“是否可以看到 MedGroup 相关工具”时，必须以当前任务实际发现的工具列表为准。确实可用时，逐一列出上述 9 个工具及用途；如有工具缺失，直接说明 MCP 尚未完整就绪，建议用户检查本地连接或更新技能。不得用本技能内的清单冒充实际工具发现结果。
