# 2.0 运行质量观察

本版可留存真实任务运行记录，但 live_model_route_baseline=not_enabled：尚无已验收的跨模型真实基线，不提供已验证的模型优劣结论，不自动切换模型。

用于专家任务的质量记录、回放和同类历史对比，不负责调用模型 API、换模型或操作经营平台。它不代表已经积累两周真实基线，也不取代每份报告原有的来源、覆盖、深度、冲突和复核检查。

## 自动记录什么

`host_runtime.py` 在实际任务终态被登记后，自动追加 `omni-ecom.model-observation@2.0`。它绑定该次宿主观测文件、原始任务 ID、岗位、attempt、运行版本和审计事件；主理人不能把别的任务或旧版本的模型名称、费用抄过来。

宿主确实提供模型信息时，规范化终态观测可带 `model` 字段：`model_alias / model_name / model_version / prompt_version / input_tokens / output_tokens / latency_ms / cost / currency`。只保留明确获得的值；不要从 UI 的某个模型名称推断所有子任务都用了它，也不要用整个任务总时长代替模型推理时延。输入输出规模和费用不公开时为 null，实际零值可为 0；费用缺币种不做比较。`host-default` 表示沿用宿主设置的记录别名，不表示已知底层模型。

`quality_gate.py` 运行跨专家冲突扫描时追加 `omni-ecom.quality-observation@2.0`，记录有没有分歧、对应输入指纹及运行版本。相同稿件重复检查不重复增加样本；比较时按每份报告修订的最新扫描计算。监控中的“分歧率”不是“错误率”，不能因为专家存在分歧就判谁错。

终态没有暴露元数据时照常保留“未知”，不因此代写费用或阻断正确的经营分析。非法数字、缺币种等记为 partial/invalid 并带原因，不转成零。

## 导出与显式反馈

在本次运行完成或受阻后，可导出内部快照。若源观测、人工反馈或扫描输入变化，导出阻断，先排查；不要把重新计算出的新指纹补入旧审计记录。

```text
python scripts/behavior_audit.py snapshot --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT --output SNAPSHOT_PATH
```

需要统计人工纠正时，必须有本次真实用户反馈的可定位引用。主理人将反馈目标和结果留在本次运行目录：`run_id / client_scope / role / host / agent_task_id / attempt_id / outcome / observed_at / message_reference`。outcome 为 `corrected` 或 `accepted`。只有明确确认未需纠正，才能登记 accepted；用户没回复不等于 accepted。引用不能由主理人编造，不把完整聊天或客户业务明细拷入质量统计。

```text
python scripts/behavior_audit.py feedback --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT --source feedback/RECORD.json --output FEEDBACK_RECEIPT_PATH
```

人工反馈记录使用 `omni-ecom.human-feedback@2.0` 并绑定本次运行版本。成员未回传时不能登记其已被人工验收。人工纠正率只以有明确反馈的样本为分母；没有反馈时为未知。旧反馈记录只可作为历史阅读，不能直接进入当前质量分母。

## 历史对比

由主理人维护当前客户允许读取的显式运行列表，不递归搜索历史工作区。列表的 client_scope 必须与命令一致，每个 `run_dir` 是相对列表文件目录的路径，必须留在该目录下，且同一 run_id 不能重复。

```json
{
  "client_scope": "当前客户范围",
  "runs": [{"run_id": "真实运行ID", "run_dir": "runs/对应运行目录"}]
}
```

正式跨任务比较前，由用户或管理员在固定目录创建一次监测策略库，并为每个客户采用当前 2.0 策略。策略采用记录必须绑定策略指纹、上一版本指纹、操作者、可定位确认依据和带时区时间；同一版本不能覆盖。正常任务只能打开既有库，不得在报告目录中临时新建一套来绕过历史。

```text
python scripts/monitor_policy_store.py create --directory POLICY_STORE --client-scope CLIENT
python scripts/monitor_policy_store.py adopt --profile POLICY_STORE/monitor-policy-store.json --client-scope CLIENT --policy config/behavior-monitor.json --decision ADOPTION.json
python scripts/behavior_audit.py compare --history HISTORY_PATH --client-scope CLIENT --policy config/behavior-monitor.json --policy-store-profile POLICY_STORE/monitor-policy-store.json --split-at TIME_WITH_TIMEZONE --audit-run-dir RUN_DIR --audit-run-id RUN_ID --output audits/comparison-UNIQUE.json
```

输出路径相对 audit-run-dir。比较依据来自逐一检查过的 SQLite 记录和原始观测文件，不从手写“历史通过率”生成结论。

默认比较切分点前 14 天与后 7 天，窗口外样本计数列出但不混入结果。按任务类型、岗位、宿主、模型别名与证据类型分别比较；不同客户不能混用，合成测试和真实观测不能共享基线。当前规则还要求基线覆盖 14 个实际观测日、至少 28 个样本及当前至少 5 个样本；单日大量重复调用不能伪造两周基线。样本不足只返回 `baseline_collecting`。

每项比例附实际分母：无人工反馈不计为零，模型费用仅同币种比较，当前或基线该项有效样本不足时不作稳定性判断。历史均值、当前均值、绝对变化、阈值和模型配置是否变化都会列出；不会把“发现变化”写成“证明是模型升级导致”。

`config/behavior-monitor.json` 的阈值是候选初始值，不是生产验证结果。每次比较先要求固定策略库中的当前策略与本次文件逐字解析结果一致，再把策略版本、指纹及策略库引用写入运行审计；策略记录使用 `omni-ecom.behavior-monitor-policy@2.0`，对比记录使用独立的 `omni-ecom.behavior-monitor-comparison@2.0`。旧 1.0 策略可用 `monitor_policy_store.py import-legacy` 原字节归档，但固定为 `legacy_v1 / current_authority=false / legacy_permissions_inherited=false`，不能成为当前阈值或模型路线依据。

需要比较两个模型路线时，再运行 `scripts/model_route_guard.py`。它只接受同一客户、任务类型、岗位和宿主的两个独立模型 cohort；两边都必须来自策略白名单中的真实 WorkBuddy/Codex 观测，覆盖至少 14 个实际日期、基线至少 28 个样本、当前至少 5 个样本，三项基础质量指标都有足够分母，阈值还必须由人工升级为 `validated_live`。合成夹具、候选初始阈值、缺候选组、模型配置中途变化或任一组仍有漂移都会返回 `live_baseline_not_ready`。

条件齐备也只生成 `omni-ecom.model-route-assessment@2.0` 和 `manual_route_review_ready`，并列展示两组证据；它固定 `automatic_changes=false`、`host_model_changed=false`、`route_selection_applied=false`，需要用户或管理员另行批准并在宿主完成修改。当前没有两周真实样本，正式模型路由/灰度切换仍未验收，不能宣称已经自动调模。

## 如何处理结果

- `baseline_collecting`：继续真实记录，不声称“质量稳定”。
- `review_required`：先查看被标记任务的真实轨迹、回传与用户反馈，确认是模型、任务难度、数据缺口还是格式问题。在新的同类正式报告前处理问题或明确降级范围，不能静默忽略。
- `no_drift_in_observed_metrics`：仅表示可比较指标未超过初始阈值；仍要展示 unavailable_metrics，不代表所有质量维度都通过。

程序不自动更换模型、不重放写操作，也不建立后台定时任务。模型调整需遵守宿主与用户的选择权限；外部经营动作继续走独立审批。两周真实观测和生产阈值验收尚未完成时，保持候选状态。
