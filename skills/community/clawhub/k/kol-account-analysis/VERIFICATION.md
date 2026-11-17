# 部署后验证包（Verification Package）

> 生成于 2026-08-21（v2.1.0）。有效期至 2026-11-19（T+90d），到期后应重新验证。
> 用法：用下列 prompt 真实触发一次，对比实际路由与 expected_sections；命中率下降即触发改进流程。

## Trigger Prompts（应触发本 skill）

| # | Prompt | 期望路由（应加载的文件） |
|---|--------|------------------------|
| T1 | "帮我深度分析一下这个抖音达人账号，看看他适合做什么内容，我们要合作推新品" | task-definition → platform-context → data-collection → data-sources → works-analysis → comments-analysis（→ batch-processing，若评论量大）→ collaboration-judgment + report-template |
| T2 | "分析这位小红书博主的作品和评论区，判断我们的商品应该以什么身份进入，适合什么合作形态" | 全五步，重点 platform-context + works-analysis + comments-analysis + collaboration-judgment（合作形态矩阵） |
| T3 | "做一份达人账号深度分析报告，评估他和我们品牌合作的风险，看看他是不是在上升期" | 全五步，重点 works-analysis（生命周期判定 3.3）+ collaboration-judgment（风险清单 + 五问 + 证据边界）+ report-template |
| T4 | "判断这个B站UP主现在处于什么生命周期阶段，我们的护肤品牌能不能让他做定制内容" | 全五步，重点 platform-context（B站校准）+ works-analysis（生命周期）+ collaboration-judgment（信任可迁移性 + 合作形态） |
| T5 | "帮我采集一下这个抖音达人的作品和评论数据，我要做深度分析" | 数据采集场景 → collection-playbook + scripts/collect_account.py + data-sources（T4 路径） |

## Anti-Trigger Prompts（不应触发本 skill）

| # | Prompt | 应由其他能力处理 |
|---|--------|----------------|
| A1 | "按粉丝量和CPM帮我筛一批达人，做个候选名单排序" | 批量筛选流程（本 skill 明确排斥） |
| A2 | "预测这次达人投放能带来多少GMV" | 效果预测（本 skill 明确排斥） |
| A3 | "帮我分析我们产品卖点应该怎么写进Brief" | 商品价值分析（本 skill 明确排斥） |

## 路由完整性检查点

1. 无任务定义句时是否拒绝进入翻作品阶段（Step 1 门控生效）
2. 无平台信息时是否主动确认平台并加载 platform-context.md 做信号校准
3. 无数据时是否路由到 data-sources.md 取数路径而非直接编造分析；T4 路径是否指向 collection-playbook + collect_account.py
4. 数据缺失时是否执行降级协议并声明证据缺口
5. 评论量大时是否启用 batch-processing.md 分工（统计不交给 LLM 数）
6. 报告是否含：五问 + 信任可迁移性 + 生命周期判定 + 合作形态建议 + 风险清单 + 证据边界 + 跨达人对比卡

## 稳定性容忍阈值

- 分析/知识类任务：质量偏差容忍 ≤ 5%（关键小数字计数错误、母题归因错列为不可容忍项）
- 路由失败（应触发未触发 / 不应触发而触发）：0 容忍
