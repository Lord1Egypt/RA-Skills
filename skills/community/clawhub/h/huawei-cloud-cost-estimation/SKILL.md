---
name: huawei-cloud-cost-estimation
description: Estimates Huawei Cloud pre-order pricing via hcloud BSS — 包年/包月 与 按需，返回官网价（含折扣则附折后）。Use this skill whenever the user asks about Huawei Cloud / 华为云 / hcloud cost (报价/询价/多少钱/价格/quote/pricing/budget) for ECS/RDS/EVS/DCS/带宽/EIP, even if only spec+duration is given. Refuses cross-cloud (AWS/Azure/Aliyun), order placement, AK/SK intake.
compatibility: hcloud KooCLI 7.2+, BSS IAM with bss:order:view permission, outbound network; no agent auto-install
metadata:
  author: ontology-of-everything
  version: "1.0.2"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/ontology-of-everything/SemanticSkills/tree/main/skills/huawei-cloud-cost-estimation
    envVars:
      - {name: HUAWEICLOUD_SDK_AK, required: false}
      - {name: HUAWEICLOUD_SDK_SK, required: false}
      - {name: HUAWEICLOUD_SDK_REGION, required: false}
---

# 华为云成本估算

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud/BSS 响应为准。

确定性下单前询价：价格只能来自当次 hcloud 响应，**不臆造、不类比、不记忆**。

## Workflow

### Phase 1 · Analysis

1. **Parse** — 从需求抽取四元组 `cloud_service_type / resource_type / region / resource_spec` + 周期（period）或使用量（on-demand）。读 `references/semantic/catalog.yml` 路由到 `rfq-period-model.yml` 或 `rfq-ondemand-model.yml`。
2. **Clarify** — 命中下列任一即停下、一轮问完（带 2–4 候选）：

- 产品类目模糊（"便宜的数据库"）→ 列候选服务+典型规格+价位档
- 缺 `region` / 数量 / 周期或使用量
- ECS 未给 OS、RDS 未给引擎等多变种
- 线性产品（带宽/云硬盘/共享带宽）未给 `resource_size`

**Spec Review** — 取数前用一张小表回显：

| 项目 | 已确认 | 待补（要问） | 默认（要披露） |
| --- | --- | --- | --- |

- 任一 **never-assume**（region/周期/数量/线性 size）缺失 → 回到 Clarify，不进 Phase 2。
- 仅 **safe-default** 缺失（OS=linux、AZ=空、`fee_installment_mode=NA`）→ 披露后继续。
- **确认话术**：回显用口语四元组 + 周期/用量（如「ECS c6.2xlarge ×1，华北-北京，包年 1 年」），不暴露内部名（`RFQ_Line` / `pricing_mode=` / 内部 code）。

### Phase 2 · Estimation

1. **Query** — 按 `references/related-commands.md` 执行最小命令：period → `BSS/ListRateOnPeriodDetail`；on-demand → `BSS/ListOnDemandResourceRatings`。多产品一次性放进 `product_infos.N.*`。
2. **Calculate** — 多 `product_infos` 逐项展示再加和；跨万元乘法分步算。
3. **Verify** — 分项加和 = 总价；币种、`period_type`、`subscription_num` 与用户口径一致。
4. **Present** — 一句结论 + 分项 `[服务] [规格] [region] [数量×周期] = ¥<金额> [pricing_mode/币种]` + 加总 + 「非最终账单」声明。读数见 `related-commands.md` response_contract（默认官网价，有折扣附折后）。**Iteration**：换 region / 改规格 / 增删项 → 只重跑受影响项。

## Critical Rules

1. **Never guess prices** — 价格只能来自当次 hcloud 响应。
2. **Never silently default never-assume** — `region`/周期/数量/线性 `resource_size` 缺失必须问；safe-default（OS/AZ/`fee_installment_mode`）必须显式披露。
3. **Always label the basis** — 每行报价带 `pricing_mode / 币种 / 时长或使用量`。
4. **Never accept credentials in chat** — 用户粘 AK/SK/Token 立即拒收，指向 `references/cli-installation.md` 让用户自行 `hcloud configure`。
5. **Route, don't refuse blankly** — 历史账单 / 余额 / 对账 → 明确超出本技能（仅下单前询价），指向费用中心或 BSS 账单只读 API；非华为云 → 仅服务华为云 BSS；写操作 → 给控制台指引。
6. **BSS 端点** — 所有 `hcloud BSS` 调用固定 `--cli-region=cn-north-1`；`product_infos.N.region` 仍是资源部署区，勿与 CLI region 混用。

> 输出禁忌：对用户消息不用 GFM 表格（IM 渲染差），用 `·` 分项或编号。`product_infos` 等命令级陷阱（dot notation、无分页、code 大小写）见 `references/related-commands.md` 顶部。

## Reference Index（按需加载）

| 何时读 | 文件 |
| --- | --- |
| 每次 Phase 1 入口 | `references/semantic/catalog.yml` |
| period / on-demand 询价场景 | `references/semantic/rfq-{period,ondemand}-model.yml` + `rfq-shared-dimensions.yml` |
| 命令模板 / 字段对照 / 响应字段路径 / 维度查 code / flavor 查询 / 通用陷阱 | `references/related-commands.md` |
| 403 或权限问题 | `references/iam-policies.md` |
| hcloud 未就绪 | `references/cli-installation.md`（**仅转述给用户**，不代为执行） |
