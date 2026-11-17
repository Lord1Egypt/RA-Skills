# 2.0：受控动作资格检查

本版 controlled_action_readback=not_enabled。经营报告可以提出待批准建议，但不能据此执行后台动作；下文只保留未来扩展的检查规范。

`scripts/action_policy.py` 是执行前的纯检查模块，不调用平台、不创建审批、不获取密钥。返回 eligible_for_execution 也不等于已经执行，更不等于回读通过。实际 Connector Gateway 和可信宿主审批绑定仍需完成后方可对接生产。

## 输入及边界

由调用者传入 action、policy、objects、credential、snapshot、approval，并使用可信当前时间。action 必须使用 `omni-ecom.controlled-action@2.0`，记录实际生成它的专家团版本；旧 1.0 行动只可读取历史，不继承执行资格。所有客户、平台、账号、店铺和目标 ID 必须明确；目标仅接受 resource/platform_id。objects 是显式授权对象清单，不通过模糊店铺名或自然语言猜测对象。重复、停用、过期对象拒绝。

policy 包含 schema_version=2.0、client_scope、policy_id、revision、mode、object_max_age_seconds、snapshot_max_age_seconds，以及 operations。每个操作定义 resource 和允许 fields。枚举字段使用 allowed_values；数值字段同时定义 minimum、maximum、max_increase、max_decrease，缺任何边界则拒绝。预算、价格或库存能否执行取决于明确定义的操作与字段，不从用户泛泛“优化”推导写入授权。

credential 只传 credential_id/secret_ref 引用及状态、到期时间、精确的客户/平台/账号/店铺范围和操作 scope。不传密码、Cookie、token 或密钥值。当前检查按所请求操作核对 scope；尚未实现无写权限的人工辅助计划输入适配，不得为了通过检查授予额外写权限。

snapshot 是刚读回的目标状态，包含同样的客户/平台/账号/店铺/target、data、read_at 和 data 规范 JSON 的 source_fingerprint。网关必须实际读取它，不能由主理人填写“预计当前值”冒充读取结果。时间过期、跨目标或指纹不匹配均拒绝。

## 审批和模式

evaluate 的 bindings 绑定整个 action、policy、目标登记、凭证引用及读取快照的指纹。approval 必须使用独立的 `omni-ecom.approval-decision@2.0`，与 action 的生成版本一致，并引用同一 action_id/run_id/client_scope 和全部绑定指纹，明确 approval_id、actor、source_reference、decided_at、expires_at、state=approved。行动文件不能冒充审批，审批文件也不能冒充行动。

source_reference 必须由可信宿主定位到真实用户批准内容。该纯模块只能验证字段和指纹一致，不能独立鉴定普通 JSON 中的 actor 是否真人，不能用手工填 approved 代替授权。动作、策略或目标快照变更后原批准不自动适用。

- readonly：拒绝动作执行资格。
- assisted：只返回 assisted_plan_only，不能调用执行接口。
- controlled：没有明确审批返回 requires_approval；全部检查满足才返回 eligible_for_execution。
- 任意不符合项返回 denied，错误不回显凭证或原始输入值。

所有返回 executed=false。record 可把决定以 `omni-ecom.action-policy-decision@2.0` 写入已有运行账本，生成版本必须与原动作及运行账本一致；旧资格结论不能为当前调用提供依据。记录不写密钥引用原文，也不能作为执行、回读或最终 outcome 事件。

候选 [执行与恢复网关](action-gateway-v2.md) 已接入资格结果、持久提交占用、条件写入和只读回读，并核对 action 的生成版本与运行账本版本一致。生产审批确认器、真实平台接入、跨运行账本部署及回滚仍待完成；平台只读连接和受控写入真实验收不能由这些合成资格测试替代。

## 测试连接器的结果边界

MockPlatformConnector 的同一提交编号绑定完整请求及 dry_run 模式。修改内容或在预演/执行模式间切换必须使用新的、重新审批的请求，不能复用旧结果。MockPlatformConnector 自身的缓存只用于合成测试，不能承担真实执行防重。

真实动作必须经 `execution_store.py` 创建并由可信宿主固定的 SQLite 执行账本，再由 `ActionGateway` 在该账本中先提交唯一调用预留，之后才允许调用连接器。账本支持进程重启后恢复、并发连接互斥、同一请求幂等回放以及写后超时的只读回查；一旦调用结果不确定，不得自动再次提交。故障测试见 `scripts/action_gateway_smoke.py` 与 `scripts/execution_store_smoke.py`。这些测试仍是合成验证，不能替代真实平台动作验收。

回读必须有非空预期字段；缺失字段不能当成 null 匹配，布尔值不能当成数字匹配，非有限数值拒绝。内存修改及回读始终标记 simulated=true 和 synthetic_mock 证据类型，即使状态为 executed/verified，也不代表真实平台执行或验收。dry_run 单独表示是否仅预演。
