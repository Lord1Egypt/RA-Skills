---
name: omni-ecom
description: 全域电商经营专家团 v2.0.3；用于店铺诊断、周报/月报/年报、大促复盘和投流利润分析。识别完整授权报表，以真实多专家、数字来源复算与独立复核交付图表 PDF。
metadata:
  openclaw:
    requires:
      bins: [python]
    envVars:
      - name: OMNI_ECOM_CLIENT_REGISTRY
        required: false
        description: 用户明确授权的本机客户名称检查清单路径；不上传或内置客户清单。
      - name: CODEBUDDY_CONFIG_DIR
        required: false
        description: 仅 WorkBuddy 恢复检查及开发验收时使用的本机配置目录，不是平台凭证。
---

# 全域电商经营专家团

ClawHub 分发版，沿用原条目 `omni-ecom-skill`，专家团名称仍为 `omni-ecom`。启动前先读 [安装与宿主能力边界](references/clawhub-distribution.md)。本包不是 WorkBuddy 安装插件，也不自动为其他宿主增加子任务工具。当前运行协议仅实现 WorkBuddy 和 Codex；其他宿主先返回 `host_adapter_not_available`，不得扮演多个专家、伪造 ID 或宣布正式报告完成。

维护批次：20261014-r2；专家团仍为 v2.0.3。报告同时标注版本、维护批次和报告修订号；不将历史验收视为本批次新任务验收。

当前正式版：v2.0.3，上一正式版 v2.0.2。实际身份只取 version-info.json；候选版不得安装成正式版，也不能当客户交付。报告标注专家团版本及独立修订号 R1/R2，历史报告保持原身份。

用户提供客户范围、平台、期间、任务目的和原始导出报表即可；不需要平台 API。模型沿用用户选择。平台 API、后台动作/回读和真实跨模型路线基线均为 not_enabled；不把保留实验模块说成已启用。

主理人先读 [宿主运行协议](references/runtime-v2.md)，按 [流程修整](references/workflow-refinement.md) 执行。岗位按自己的任务卡和 [共同交接规范](references/expert-working-contract.md) 处理，不加载无关可选说明。

必须保留：
- 全量识别、归类、动态章节及覆盖检查。空表、未知类型、资料不足均有去向和影响，不静默丢弃。没有业务文件只交 intake_blocked，不伪造报告或专家。
- 来源副本绑定本次客户、运行、版本与指纹。原始业务文件按 run-scope 限制读取；当前状态仅用 run-journal.sqlite 与 host_runtime。
- 真实原表是经营事实来源；未知费用不填零、不编造花费或 ROI。买家转化率为同口径支付买家/去重访客，GMV/访客叫访客价值；ROAS 与利润 ROI 分开，缺匹配退款及完整成本不出净利润和预算结论。数字、公式与归因按 [来源复算](references/claim-sources-v2.md) 核对。
- 综合报告真实调用四位分析专家，原生完成和回传齐备后才并稿；WorkBuddy 用 TeamCreate/Agent，Codex 用 spawn_agent/wait_agent，工具和任务凭证不混用。模型选择不改变这些要求。明确单项问题才可走 single_point。
- 每位专家亲自填写分析，程序仅装配固定字段。首次 a1 符合正式 handoff；六题逐题有答案或有证据的限制，L2 拆解、必要的 L3/L4 和七项自检保留。每次只向团长回传一次，不与同级聊天。
- 团长核对数字、覆盖、深度与冲突；必要时只定向核查涉事岗位。因果判断按 [因果证据](references/causal-evidence-v2.md)，冲突裁决按 [裁决交付](references/decision-delivery-v2.md)，中断恢复用原任务 ID。只有已记录真实失败/拒收的岗位才可有限重试。
- 默认图表化 PDF。依据任务类型呈现结论、完整分析与行动；全量覆盖、来源和真实岗位贡献在证据附录可追踪。资料不足不补造经营图表或确定性结论。
- 先完成报告再冻结确切文件，由真实独立复核员核数字、覆盖、裁决和最终 PDF 每页；passed 且必改项为空才放行。程序指纹一致不能代替复核决定；复核员不改冻结文件。
- 公域范围检查、claim_guard、PDF验真、独立放行和 completion_gate 全部通过，且原生阶段已完成才展示最终交付。子任务未回传时主任务不能先完成。
- 新交接件、基线、数字索引、报告、复核、完成与阶段凭证均使用当前 2.0 契约并绑定生成版本；旧资料只读，不继承审批、执行或完成资格。[旧资料迁移](references/legacy-migration-v2.md) 仅在导入历史资料时读取。

发布 ZIP 包含 SKILL.md，通过 release_guard；真实发布按 [双宿主验收](references/release-acceptance-v2.md) 取得实际多专家、图表 PDF 和独立复核证据。候选验收使用 completion_gate.py --candidate-acceptance，状态 candidate_pipeline_complete；仅 released 且 release_ready=true 可签发正式完成，安装通过不代表客户报告完成。
