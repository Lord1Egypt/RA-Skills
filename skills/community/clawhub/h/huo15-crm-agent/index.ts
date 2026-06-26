/**
 * 绿火 · CRM 销售员智能体 v0.2（拓客 / 获客 / 跟进 / 客户画像 / 销售话术）
 *
 * v0.2 新增（按拓客 SaaS 调研报告 takeaways）：
 *   ① sales_company_search / sales_company_detail —— 接入企查查 OpenAPI 做"工商底座"
 *   ② sales_intent_signals —— 财税行业意向信号识别（5 大类 40+ 条词典）
 *   ③ sales_pitch 升级 —— 接受 signals 参数生成"信号驱动话术"
 *
 * 行业领域包可插拔（industry_domain 配置），v0.1/v0.2 内置 finance_tax 财税领域包。
 *
 * 设计原则：
 *   - 绿火不直连 Odoo —— CRM 操作由 @huo15/huo15-huihuoyun-odoo 执行
 *   - 绿火只做瘦客户端 —— 企查查调用付费由用户账户买单，不缓存大量数据
 *   - 不引入 child_process（CLAUDE.md §6.2 红线）
 *   - 不内嵌爬虫 —— 公开网搜由 huo15-searxng / WebFetch 执行，绿火只解析结构
 *
 * 拓客闭环示例（v0.2 新链路）：
 *   1) 用户："找 30 家青岛医疗器械公司"
 *   2) 绿火 sales_company_search(city="青岛", keyword="医疗器械") → 候选 30 家
 *   3) 对每家 sales_company_detail → 工商详情
 *   4) sales_intent_signals(raw_texts=...) → 识别招聘 / 招标 / 风险信号
 *   5) sales_lead_score → 综合打分排序
 *   6) sales_pitch(signals=top_signals) → 信号驱动话术
 *   7) huihuoyun-odoo 的 odoo_crm_create + odoo_create_activity 批量入库 + 排活动
 *
 * 工具命名一律 sales_* 前缀，与 huihuoyun-odoo 的 odoo_* 工具互不冲突。
 */

import { definePluginEntry } from 'openclaw/plugin-sdk/plugin-entry';
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { registerSalesLeadScore } from './src/tools/sales_lead_score.js';
import { registerSalesLeadBrief } from './src/tools/sales_lead_brief.js';
import { registerSalesPitch } from './src/tools/sales_pitch.js';
import { registerSalesFollowupPlan } from './src/tools/sales_followup_plan.js';
import { registerSalesIndustryScan } from './src/tools/sales_industry_scan.js';
import { registerSalesCompanySearch } from './src/tools/sales_company_search.js';
import { registerSalesCompanyDetail } from './src/tools/sales_company_detail.js';
import { registerSalesIntentSignals } from './src/tools/sales_intent_signals.js';

export default definePluginEntry({
  id: 'crm-agent',
  name: '绿火 · CRM 销售员智能体（拓客 / 获客）',
  description:
    '绿火 —— 拓客 / 获客 / CRM 销售员智能体。行业领域包可插拔，v0.1/v0.2 内置 finance_tax 财税领域包。提供 8 个 sales_* 工具：lead 打分 / 客户画像简报 / 场景化话术 / 阶段化跟进计划 / 行业历法 / 企业检索 / 工商详情 / 意向信号识别。本身不直连 Odoo，所有 CRM 写入由同时已装的 @huo15/huo15-huihuoyun-odoo 执行。v0.2 起接入企查查 OpenAPI 做工商底座（需用户配 qichacha_api_key）。',
  register: (api: OpenClawPluginApi) => {
    // v0.1 既有
    registerSalesLeadScore(api);
    registerSalesLeadBrief(api);
    registerSalesPitch(api);
    registerSalesFollowupPlan(api);
    registerSalesIndustryScan(api);
    // v0.2 新增
    registerSalesCompanySearch(api);
    registerSalesCompanyDetail(api);
    registerSalesIntentSignals(api);

    api.logger.info(
      '[crm-agent / 绿火] v0.2.1 已加载 — 8 个工具：sales_lead_score / sales_lead_brief / sales_pitch / sales_followup_plan / sales_industry_scan / sales_company_search / sales_company_detail / sales_intent_signals。领域包：finance_tax。CRM 写入由 huihuoyun-odoo 执行；企业检索 / 详情通过企查查 OpenAPI（需配 qichacha_api_key）。',
    );
  },
});
