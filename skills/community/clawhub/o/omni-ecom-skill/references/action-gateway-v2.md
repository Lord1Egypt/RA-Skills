# 2.0：持久执行与只读恢复

本模块为未启用扩展，v2.0.3 导出报表版不执行后台操作。以下规范不代表当前已取得接入、写入或执行权限。

用于已通过 [动作资格检查](action-policy-v2.md) 的平台动作。当前仅完成本地故障测试，真实平台适配器、可信宿主审批集成及回滚仍待验收；不得据此对真实店铺启用写入。

## 接入边界

`scripts/action_gateway.py` 提供 `ActionGateway`，使用本次显式指定的 Journal、已绑定客户/平台/账号/店铺的 connector、binding。不会搜索账号、读取密钥或创建批准。binding 还须指定 connector_id，由可信宿主根据真实连接建立，不能由模型填写即视为连接凭证。

默认 execution_enabled=false。调用方必须提供可信的 approval_verifier：根据宿主中可定位的真实用户批准，核对整份 approval 与 action，且返回布尔 true。不能用 `lambda: True`、仅检查 JSON 的 approved 或模型判断替代；合成测试中的确认器只用于明确标记的测试。当前没有已接好的生产确认器。

API 适配器须声明真实支持条件写入 conditional_write，并实现 execute 的 expected_data_sha256 参数：平台对象仍与预先读到的完整 data 指纹一致时才允许修改。不能把“先读再写”冒充原子条件写入；不支持的平台只能保留只读/辅助模式，不能绕过保护。现有 mock 实现的是锁保护的内存比较，不是平台接口证明。

## 调用与恢复

1. `execute(action, policy, objects, credential, snapshot, approval)` 先核对范围与历史记录。相同平台/账号/店铺/提交编号跨运行也不能重复占用；同一运行的同一 action_id 不能换编号再次提交。
2. 记录动作资格，检查可信批准，实际只读读取目标；credential 须同时具备明确读取权限，未授权读取就不查询。最新 data 必须与审批绑定的 snapshot 一致。
3. 在 SQLite 事务内保存 action_call_reserved 后，才进行可能修改对象的调用；再检查时效。并发另一调用者只看到已占用记录，不再次提交。API 模式须使用 [固定执行存储](execution-store-v2.md)，不同任务共用宿主固定入口，缺失或替换记录时停止。发布前还需落实双宿主配置、自动报告引用及安全恢复，不能另建空库绕过保护。
4. 接口正常返回还不算完成。必须核对返回的请求指纹、目标、编号、连接器身份及模拟标识，再独立读取目标状态。完全匹配才记录 verified；mock 的 verified 始终带 simulated=true。
5. 调用异常、返回无法绑定或进程中断，不能自动重发。`reconcile(action, credential)` 只读取，不执行。若已有绑定成功返回但回读中断，可重新读取验证；若没有可信成功返回，即使状态符合预期也保持 blocked / execution_uncertain，不能把别人的改动或超时后的不确定结果算成本次成功。
6. 已有 verified 的重复调用返回历史凭证及 observed_at，不宣称刚刚读取了平台。如果要确认最新状态，应按 [平台只读观察](platform-read-v2.md) 发起新的只读请求并生成独立凭证。

审批过期且尚未调用时记录 aborted，不修改平台。回读失败可在权限有效时再次只读核对。结果不确定时目前没有自动取消、自动回滚或平台请求状态查询；这些能力只能在真实适配器提供可靠依据后继续接入。

## 记录与限制

连续记录为：运行/客户 → action_policy_decision → action_call_reserved（动作、批准、调用 ID）→ returned / uncertain / aborted → readback（回读 ID、实际数据指纹、是否匹配）→ outcome。提交及接口观察使用 `omni-ecom.connector-call@2.0`，回读使用 `omni-ecom.action-readback@2.0`，最终结果使用 `omni-ecom.action-outcome@2.0`；三者不能互相冒充，并须与运行账本中的专家团版本一致。旧 1.0 记录仅可作为历史读取，不能证明当前调用、回读或结果。Journal 的 status 也会列出动作状态。普通 record 命令不能写 action_call_* 事件。

账本仅保留约束后的身份、指纹、状态和时间，不保存凭证引用原文、完整业务返回或异常原文。返回指纹是本地观察记录，不是平台签名或第三方独立证明；审批真实性与连接器正确性仍依赖可信宿主集成。现有哈希链不抵御有权重写数据库的攻击者。

故障测试见 `scripts/action_gateway_smoke.py`。它验证真实的 SQLite 重开、两个并发连接、模拟写后超时/进程中断、回读失败和恢复；所有平台状态与批准都是合成，不能计入真实平台验收。
