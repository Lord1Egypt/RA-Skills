# 2.0：定向质疑及裁决回传

用于本次已接收的专家交接件出现 hard 冲突时。只联系冲突涉及的原专家任务，不重跑全团、不创建冒名角色。程序只记录宿主观察；正式验收仍需查看原生任务和消息，不能拿自己生成的 JSON 当成真实调用证明。

## 主理人准备并实际发送

先有当前 report.json（允许是候选稿）和 quality-inputs.json。后者指向实际接收的 sealed 文件。读取本轮身份、冲突指纹、已选专家集合指纹、基线指纹、round_id 及各岗位 targets：

```text
python scripts/challenge_runtime.py --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT context
```

对 targets 中每位岗位创建独立 request JSON，逐项复制 context 返回的 run_id、client_scope、team_version、report_revision、conflicts_sha256、selection_sha256、baseline_sha256、round_id，补充 agent_id、该岗位完整 conflict_ids 和具体 question。每位岗位一次覆盖其涉及的全部 hard 冲突。问题应给出冲突双方原文、允许的证据路径和本次输出路径，不预设期望答案。

通过宿主实际的 follow-up/恢复任务接口发送到该岗位原始任务 ID。等待和观察使用真实工具；工具不可用则阻断。不能将初次分析的 completed 状态当成本轮回复。

实际发送后保存新的启动观测文件：沿用 runtime-v2 中的 run_id/client_scope/host/task_id/state/source_reference/evidence_kind，增加 request_sha256。该值指向刚才实际发送的 request 文件；state 为本次 created/running。登记：

```text
python scripts/challenge_runtime.py --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT start --request REQUEST.json --observation START.json
```

相同轮次、岗位和请求的重复登记是幂等操作，不重复派工；改变问题不能绕过一轮限制。启动和终态观测必须分文件保存，不覆盖原始观察。

## 专家自己回复，主理人核对终态

回复 JSON 必须保留 request 中上述七个身份/指纹字段及 round_id、agent_id，增加 request_sha256、真实带时区 returned_at 和 answers。已知 agent_task_id 时填写原始 ID，不知道则由宿主观察绑定，不自行编造。

每个 conflict_id 恰好一个 answer：

```json
{"conflict_id":"本次实际冲突ID","position":"maintain 或 revise 或 insufficient_data","reason":"证据支持的理由、修改内容或具体缺口","evidence_ids":["本岗位交接件中实际存在的证据ID"]}
```

数据不足允许 evidence_ids 为空，但必须 position=insufficient_data 并说明原因。新数据超出本轮基线时，先锁定新来源再按修订流程重新分析，不能用虚构 ID 混入旧轮次。

主理人从该次真实回复定位 response 文件及指纹，另保存 completed 终态观测，包含 request_sha256、response_sha256 和真实 source_reference。不得替专家写答案或修改答案后重算指纹。随后：

```text
python scripts/challenge_runtime.py --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT accept --round-id ROUND --role ROLE --observation END.json --response RESPONSE.json
```

确认宿主 failed/cancelled 时，使用实际失败观测执行同入口的 fail 命令（不传 response）。观察超时不是失败，继续查询原任务。宿主 completed 但内容不合格会记为 challenge_rejected，结束等待但不算成功；缺文件等 I/O 问题先恢复读取。失败/拒绝后该轮不再追加第二次质疑，也不准主理人改写答案恢复为成功；报告保持阻断，说明需补资料或人工处理。

## 总监裁决、冻结与完成

每个裁决 verdict 增加 challenge_review，覆盖该冲突全部相关岗位，逐项包含 role、该次真实接收审计事件 return_event_hash、disposition（adopted/not_adopted/data_gap）及具体 reason。不能把回复状态直接等同于经营判断正确；数值还需按原始数据复算，未采纳意见和下游影响仍需说明。

质量检查自动核对真实任务 ID、所有请求/回复/观测指纹、证据 ID、回传完整性和上述裁决引用。其 challenges 字段列出绑定记录，文件进入冻结清单。主理人不得省略报告中的质疑参与和裁决摘要，交付复核员需核对报告表述与确切回复一致。

status 的 challenges_waiting 提供待查原任务，next_action=wait_existing_challenges；存在等待时不得启动最终复核或登记正式完成。通过合成测试不证明 WorkBuddy/Codex 实际工具已跑通。口径和趋势冲突按 [口径和趋势裁决](semantic-adjudication-v2.md) 重算并核对期间；因果互斥仍需独立证据审查，不能以一个算式冒充因果解释。
