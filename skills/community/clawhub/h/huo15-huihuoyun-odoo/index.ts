/**
 * 火一五·辉火云企业套件插件 v1.9
 *
 * 品牌口径：对外统一称"辉火云企业套件"。代码内部的类名/文件名/tool 名沿用
 * 历史标识符（OdooClient/odoo-client.ts/odoo_*），因为改动会破坏 agent
 * 历史 memory 与已部署配置；它们仅作为技术 id 存在，不进入用户可见文案。
 *
 * v1.9 品牌化：
 * - 所有用户可见文案（tool description、prompt hint、错误消息、通知文案）
 *   统一使用"辉火云企业套件"/"辉火云"
 * - 加入 prompt 硬规则：对外沟通时不得透露第三方商标
 *
 * v1.8：Project/Ticket/Chatter 闭环（+13 tools）
 * v1.7：Daily Inbox 闭环（活动/日历/邮件/附件/关注者/批量/撤销）
 * v1.6：跨渠道通知基座（企微/钉钉/飞书）+ per-agent 偏好 + 入站回复 + 知识库
 * v1.2：per-agent 凭据隔离
 */

import { definePluginEntry } from 'openclaw/plugin-sdk/plugin-entry';
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { OdooClient } from './src/modules/odoo-client.js';
import { NotificationPoller } from './src/modules/notification-poller.js';
import { ConfigManager } from './src/modules/config-manager.js';
import { notificationBus } from './src/modules/notification-bus.js';
import { toEnvelope } from './src/modules/notification-router.js';
import { PrefsManager, shouldDeliver, DEFAULT_PREFS } from './src/modules/notification-prefs.js';
import { EnvelopeCache } from './src/modules/envelope-cache.js';
import { mutationLog } from './src/modules/mutation-log.js';
import { mdToHtml } from './src/utils/md-to-html.js';
import { readFileSync, statSync } from 'node:fs';
import { basename } from 'node:path';
import type {
  OdooPluginConfig,
  SyncUpdate,
  NotificationEnvelope,
  NotificationPreferences,
  NotificationKind,
  NotificationPriority,
  InboundReply,
} from './src/types/index.js';
import { today, tomorrow } from './src/utils/date-utils.js';

const odooClients = new Map<string, OdooClient>();
const pollers = new Map<string, NotificationPoller>();
const configManager = new ConfigManager();
const prefsManager = new PrefsManager();
const envelopeCache = new EnvelopeCache();
let replyUnsubscribe: (() => void) | null = null;

// v1.19.0 ⭐ 完整工具速查 + 自然语言映射（按需通过 odoo_help 工具拉取，不再注入 system context）
// 之前 v1.18 这段会被 before_prompt_build hook 每次 LLM call 都注入到 prompt（~7900 字 / ~2000 tokens），
// 即使用户只是闲聊也注入，导致 TTFT（Time To First Token）严重拉高。
// v1.19 起改为按需调用：system context 只保留 6-8 个高频工具速查；LLM 需要扩展查找时调 odoo_help。
const ODOO_HELP_TEXT = `### 工具速查（共 189 个）

**基础**：odoo_connect · odoo_status · odoo_disconnect · odoo_whoami
**任务**：odoo_create_task · odoo_list_tasks · odoo_update_task · odoo_get_task_stages · odoo_task_assign
**活动**：odoo_create_activity · odoo_list_activities · odoo_activity_types · odoo_complete_activity · odoo_reschedule_activity
**日历**：odoo_create_event · odoo_calendar_today · odoo_update_event · odoo_cancel_event
**消息**：odoo_get_messages · odoo_send_message · odoo_message_post · odoo_message_log · odoo_message_history
**邮件**：odoo_send_email · odoo_email_templates · odoo_email_from_template
**附件**：odoo_attach_file · odoo_list_attachments · odoo_document_upload
**关注者**：odoo_follow · odoo_unfollow
**搜索**：odoo_search
**CRM**：odoo_crm_pipeline · odoo_crm_create · odoo_crm_update · odoo_crm_won · odoo_crm_lost
**项目**：odoo_project_overview · odoo_timesheet_log · odoo_project_create · odoo_project_update · odoo_milestone_create · odoo_milestone_done
**销售**：odoo_sale_orders · odoo_purchase_orders
**客服**：odoo_tickets · odoo_ticket_create · odoo_ticket_update · odoo_ticket_close · odoo_ticket_assign
**财务**：odoo_invoices
**联系人**：odoo_contacts · odoo_contact_create
**库存**：odoo_stock_levels · odoo_stock_pickings
**HR 基础**：odoo_employees · odoo_leaves · odoo_attendances
**HR 请假闭环（v1.11）**：odoo_leave_types · odoo_leave_create · odoo_leave_approve · odoo_leave_refuse · odoo_leave_allocate
**HR 报销闭环（v1.11）**：odoo_expenses · odoo_expense_create · odoo_expense_submit · odoo_expense_approve
**HR 招聘（v1.11+v1.12）**：odoo_applicants · odoo_applicant_move_stage · odoo_recruitment_stages · odoo_recruitment_refuse_reasons · odoo_recruitment_create_meeting
**HR 考核/工资/排班（v1.11+v1.12）**：odoo_appraisals · odoo_appraisal_action · odoo_payslips · odoo_payslip_validate · odoo_payslip_paid · odoo_payslip_cancel · odoo_planning_shifts · odoo_planning_publish · odoo_planning_unpublish
**HR 技能/远程/车队（v1.12）**：odoo_employee_skills · odoo_employee_skill_add · odoo_skills_catalog · odoo_homeworking_set · odoo_fleet_vehicles
**HR 员工生命周期（v1.13）**：odoo_employee_create · odoo_employee_update · odoo_employee_archive · odoo_employee_unarchive
**HR 仪表盘 / 组织架构（v1.13）**：odoo_hr_dashboard · odoo_employee_org_chart · odoo_employee_versions
**HR 部门 / 岗位 / 工作地点（v1.13）**：odoo_departments · odoo_department_create · odoo_jobs · odoo_job_create · odoo_work_locations
**HR 工时洞察（v1.13）**：odoo_timesheet_summary · odoo_timesheet_team
**HR Analytics 进阶（v1.14）**：odoo_attendance_analytics · odoo_leave_analytics · odoo_turnover_metrics
**HR 编排（v1.14）**：odoo_employee_onboarding · odoo_employee_offboarding · odoo_payslip_run_create
**工时审批（v1.14）**：odoo_timesheet_validate · odoo_timesheet_invalidate
**跨域仪表盘（v1.14）**：odoo_sales_dashboard · odoo_crm_pipeline_health · odoo_invoice_aging · odoo_helpdesk_dashboard · odoo_project_dashboard · odoo_my_workload
**个人视图（v1.15）**：odoo_my_overdues · odoo_my_today · odoo_my_unread
**CRM 智能助手（v1.15）**：odoo_crm_stale_leads · odoo_crm_next_action · odoo_sales_forecast
**跨模块桥（v1.15）**：odoo_helpdesk_to_task · odoo_lead_to_project · odoo_invoice_send_reminder
**库存深化（v1.15）**：odoo_stock_low_alerts · odoo_stock_by_location · odoo_stock_picking_validate · odoo_warehouse_dashboard
**多公司（v1.15）**：odoo_companies
**采购深化（v1.16）**：odoo_purchase_create · odoo_purchase_confirm · odoo_purchase_dashboard · odoo_vendor_bill_aging
**生产 MRP（v1.16）**：odoo_mo_list · odoo_mo_confirm · odoo_bom_query
**会计深化（v1.16）**：odoo_journal_entries · odoo_payment_register · odoo_chart_of_accounts
**智能洞察（v1.16）**：odoo_anomaly_detect · odoo_kpi_summary
**报表 / 数据导出（v1.16）**：odoo_pdf_report · odoo_export_csv
**流程自动化（v1.17）**：odoo_automations · odoo_cron_jobs · odoo_automation_create
**数据治理（v1.17）**：odoo_data_quality_partners · odoo_data_quality_products · odoo_data_quality_completeness · odoo_partners_merge
**批量操作（v1.17）**：odoo_batch_email · odoo_batch_archive · odoo_batch_assign
**集成 / 治理（v1.17）**：odoo_translate_record · odoo_custom_fields · odoo_user_create · odoo_user_groups
**Studio 元编程（v1.18）**：odoo_model_list · odoo_model_fields · odoo_model_create · odoo_field_create
**审计与变更追踪（v1.18）**：odoo_audit_log · odoo_login_history · odoo_field_history
**多公司联动（v1.18）**：odoo_company_switch · odoo_consolidated_dashboard
**通用报表（v1.18）**：odoo_pivot_data · odoo_email_log
**外部集成（v1.18）**：odoo_webhook_create · odoo_record_share_url · odoo_mail_queue
**审批工作流深化（v1.20）**：odoo_approval_categories · odoo_approval_create · odoo_approval_confirm · odoo_approval_my_pending
**数据克隆 / 导入（v1.20）**：odoo_record_clone · odoo_record_clone_with_lines · odoo_csv_import
**Mail 关注（v1.20）**：odoo_followers · odoo_subscribe · odoo_unsubscribe
**资源 / 工作时间（v1.20）**：odoo_resources · odoo_resource_calendar
**报表订阅 / 多语言（v1.20）**：odoo_report_schedule · odoo_translate_get
**审批**：odoo_approvals · odoo_approval_approve · odoo_approval_refuse
**助手**：odoo_daily_briefing · odoo_help
**通知基座**：odoo_notification_status · odoo_notification_channels · odoo_notification_test · odoo_notification_prefs · odoo_notification_reply
**知识库**：odoo_knowledge_search · odoo_knowledge_read · odoo_knowledge_create · odoo_knowledge_update · odoo_knowledge_append · odoo_knowledge_tree · odoo_knowledge_favorite · odoo_knowledge_trash
**批量/撤销**：odoo_bulk_update · odoo_undo_last

### 自然语言 → 工具映射（直接调用，无需询问用户）

| 用户说 | 调用工具 |
|--------|---------|
| 今天有什么工作 / 每日概况 | **odoo_daily_briefing** |
| 帮我写个待办 / 创建任务 | **odoo_create_task** |
| 今日截止任务 / 今天要做什么 | **odoo_list_tasks**(today_only=true) |
| 把任务 #X 标记完成 | **odoo_update_task**(stage_id=已完成阶段ID) |
| 提醒我… | **odoo_create_activity** |
| 安排会议 / 约个时间 | **odoo_create_event** |
| 查看商机 / 销售管道 | **odoo_crm_pipeline** |
| 新建商机 | **odoo_crm_create** |
| 这个商机赢了 / 标记赢单 | **odoo_crm_won** |
| 商机丢了 / 标记输单 | **odoo_crm_lost** |
| 项目进展 / 里程碑进度 | **odoo_project_overview** |
| 记录工时 X 小时 | **odoo_timesheet_log** |
| 查看工单 / 待处理问题 | **odoo_tickets** |
| 新建工单 / 提交问题 | **odoo_ticket_create** |
| 查发票 / 逾期应收 | **odoo_invoices**(overdue_only=true) |
| 查销售订单 | **odoo_sale_orders** |
| 查采购订单 | **odoo_purchase_orders** |
| 查客户 / 找联系人 | **odoo_contacts** |
| 添加新客户 | **odoo_contact_create** |
| 查库存 / 产品还有多少 | **odoo_stock_levels** |
| 调拨单 / 出入库 | **odoo_stock_pickings** |
| 查员工 / 某部门有谁 | **odoo_employees** |
| 请假记录 | **odoo_leaves** |
| 考勤 / 打卡 | **odoo_attendances** |
| 审批 / 待审批 | **odoo_approvals** |
| 查看消息 / 邮件通知 | **odoo_get_messages** |
| 查活动类型 | **odoo_activity_types** |
| 通知推送状态 / 企微/钉钉连上没 | **odoo_notification_status** |
| 测试一下通知推送 | **odoo_notification_test** |
| 列出已接入的渠道 | **odoo_notification_channels** |
| 关闭通知 / 别发待办了 / 夜里静音 / 只接收紧急 | **odoo_notification_prefs** |
| 模拟一次企微/钉钉回复写回系统 | **odoo_notification_reply** |
| 找一下关于 X 的知识库文章 / 搜知识库 | **odoo_knowledge_search** |
| 把这篇文章读给我 / 文章 #X 写了什么 | **odoo_knowledge_read** |
| 新建知识库文章 / 记一下这个到知识库 | **odoo_knowledge_create** |
| 改一下这篇文章的标题/正文 | **odoo_knowledge_update** |
| 追加到文章 X 末尾 / 往文章里补一段 | **odoo_knowledge_append** |
| 知识库长啥样 / 工作区里都有哪些文章 | **odoo_knowledge_tree** |
| 收藏这篇 / 取消收藏 | **odoo_knowledge_favorite** |
| 把这篇文章扔进回收站 / 删除文章 | **odoo_knowledge_trash** |
| 那个活动做完了 / 把提醒 #X 标记完成 | **odoo_complete_activity** |
| 活动挪到明天 / 提醒改到下周 | **odoo_reschedule_activity** |
| 我要关注这条任务/商机 / 加我进关注 | **odoo_follow** |
| 取消关注 / 别再给我推这条的变化 | **odoo_unfollow** |
| 今天有什么会 / 查今日日程 | **odoo_calendar_today** |
| 会议改时间 / 会议挪到 X 点 / 换会议室 | **odoo_update_event** |
| 取消这场会 / 把会议归档 | **odoo_cancel_event** |
| 发封邮件给客户 / 给 X 写封邮件 | **odoo_send_email** |
| 有哪些邮件模板 / 找商机相关的模板 | **odoo_email_templates** |
| 用模板发 / 用报价单模板发给他 | **odoo_email_from_template** |
| 把这份合同附到商机 / 上传附件 | **odoo_attach_file** |
| 这个商机/工单有哪些附件 | **odoo_list_attachments** |
| 上传到文档库 / 归档到文件夹 | **odoo_document_upload** |
| 把这批任务都改成完成 / 批量改阶段 | **odoo_bulk_update** |
| 撤销上一步 / 撤回刚才那个 / 改错了 | **odoo_undo_last** |
| 给商机/工单/任务下面留个进度说明 / 在 chatter 回一句 | **odoo_message_post** |
| 记一下备注 / 留个内部记录（不发邮件） | **odoo_message_log** |
| 这个记录都聊过什么 / 看看跟进历史 | **odoo_message_history** |
| 开个新项目 / 新建项目 | **odoo_project_create** |
| 改项目的负责人/日期/描述 | **odoo_project_update** |
| 给项目加个里程碑 / 新建里程碑 | **odoo_milestone_create** |
| 里程碑达成了 / 标记完成 | **odoo_milestone_done** |
| 把这批任务都交给张三 / 指派任务 | **odoo_task_assign** |
| 改工单的阶段/优先级/负责人 | **odoo_ticket_update** |
| 关闭工单 / 工单处理完了 | **odoo_ticket_close** |
| 把工单派给 X | **odoo_ticket_assign** |
| 批这条 / 审批通过 | **odoo_approval_approve** |
| 驳回 / 拒绝这条申请 | **odoo_approval_refuse** |
| 有哪些假可以请 / 请假类型 | **odoo_leave_types** |
| 我请假 / 帮 X 请病假 / 请假明天 | **odoo_leave_create** |
| 批了这条请假 / 准了某某的假 | **odoo_leave_approve** |
| 不批这个请假 / 拒了请假 | **odoo_leave_refuse** |
| 给某员工加假期 / 补调休额度 / 分配年假 | **odoo_leave_allocate** |
| 我的报销 / 待批的报销 / 看报销列表 | **odoo_expenses** |
| 我要报销 / 报销 X 元 / 报昨天的差旅 | **odoo_expense_create** |
| 把这条报销提交 / 提交我的报销 | **odoo_expense_submit** |
| 批了这条报销 / 拒绝报销 / 通过 X 的报销 | **odoo_expense_approve** |
| 招聘 pipeline / 候选人列表 / 某岗位有谁 | **odoo_applicants** |
| 把候选人推到面试 / 移动应聘者阶段 / 拒绝候选人 | **odoo_applicant_move_stage** |
| 招聘有哪些阶段 / 列出招聘 stage | **odoo_recruitment_stages** |
| 拒绝候选人有哪些理由 / 拒绝原因列表 | **odoo_recruitment_refuse_reasons** |
| 约这位候选人面试 / 给应聘者排个面试 | **odoo_recruitment_create_meeting** |
| 看考核 / 我要做的绩效 / 待评的人 | **odoo_appraisals** |
| 启动 / 完成 / 退回考核 | **odoo_appraisal_action** |
| 我的工资单 / 这个月工资 / 看薪资 | **odoo_payslips** |
| 验证工资单 / 工资单 done | **odoo_payslip_validate** |
| 工资发了 / 工资单标记已支付 | **odoo_payslip_paid** |
| 取消工资单 / 作废 | **odoo_payslip_cancel** |
| 我这周的班 / 排班 / 谁今天值班 | **odoo_planning_shifts** |
| 发布排班 / 公布班次 / 通知员工值班 | **odoo_planning_publish** |
| 撤销排班发布 / 班次回到草稿 | **odoo_planning_unpublish** |
| 看某员工的技能 / 我会什么 / 部门技能盘点 | **odoo_employee_skills** |
| 给员工加技能 / 录入技能等级 | **odoo_employee_skill_add** |
| 系统里有哪些技能 / 技能等级目录 | **odoo_skills_catalog** |
| 我明天远程 / 标记某天在家办公 / 周一在上海办公室 | **odoo_homeworking_set** |
| 我有哪辆车 / 公司车队 / 销售部的车 | **odoo_fleet_vehicles** |
| 入职新员工 / 录入张三 / 创建员工档案 | **odoo_employee_create** |
| 改张三的部门 / 换上级 / 改员工资料 / 加手机号 | **odoo_employee_update** |
| 离职 / 归档员工 / 停用 X | **odoo_employee_archive** |
| 返聘 / 启用员工 / 重新激活账号 | **odoo_employee_unarchive** |
| HR 仪表盘 / 人事概况 / 公司在编多少人 / 今天有谁请假 | **odoo_hr_dashboard** |
| 看看张三上面是谁 / 我下面有几个人 / 组织架构 / 上下级 | **odoo_employee_org_chart** |
| X 的合同历史 / 员工版本 / 调薪记录 | **odoo_employee_versions** |
| 有哪些部门 / 部门列表 / 部门树 | **odoo_departments** |
| 新建部门 / 加个部门 | **odoo_department_create** |
| 有哪些岗位 / 岗位列表 / 在招岗位 | **odoo_jobs** |
| 新开个岗位 / 创建职位 | **odoo_job_create** |
| 有哪些工作地点 / 办公室 / 远程地点 | **odoo_work_locations** |
| 我这个月工时 / 项目工时聚合 / 工时分布 | **odoo_timesheet_summary** |
| 我下属的工时 / 团队工时 / 谁工时少 | **odoo_timesheet_team** |
| 考勤分析 / 这个月谁工时最多 / 部门考勤分布 | **odoo_attendance_analytics** |
| 请假趋势 / 这个月请假数据 / 全公司请假统计 | **odoo_leave_analytics** |
| 入离职率 / 流失率 / 近 3 个月人员变动 | **odoo_turnover_metrics** |
| 入职新员工带账号带欢迎 / 一键入职 / 录入员工并建账号 | **odoo_employee_onboarding** |
| 一键离职 / 离职转移下属 / 离职流程 | **odoo_employee_offboarding** |
| 验证工时 / 批准工时 / lock 工时 | **odoo_timesheet_validate** |
| 撤销工时验证 / 解锁工时 | **odoo_timesheet_invalidate** |
| 销售概况 / 本月销售额 / Top 客户 | **odoo_sales_dashboard** |
| CRM 漏斗健康 / 商机分布 / 逾期商机 / 平均概率 | **odoo_crm_pipeline_health** |
| 应收账龄 / 账龄分析 / 谁欠款最多 / 90 天以上 | **odoo_invoice_aging** |
| 工单仪表盘 / 客服情况 / SLA 逾期 | **odoo_helpdesk_dashboard** |
| 项目仪表盘 / 项目总览 / 任务总数 | **odoo_project_dashboard** |
| 我手上还有多少活 / 我的工作负荷 / 我的待办全图 | **odoo_my_workload** |
| 创建本月工资批次 / 批量生成工资单 | **odoo_payslip_run_create** |
| 我有什么逾期的 / 我手上逾期项 / 哪些事过期了 | **odoo_my_overdues** |
| 我今天要做什么 / 今天的全部事 | **odoo_my_today** |
| 我有几条未读 / 未读消息 / @我的有没有看 | **odoo_my_unread** |
| 哪些商机停滞了 / 长时间没动的商机 / stale leads | **odoo_crm_stale_leads** |
| 这个商机下一步该做什么 / 给我建议 / 智能推荐 | **odoo_crm_next_action** |
| 销售预测 / 加权管道 / 我们这个季度大概能做多少 | **odoo_sales_forecast** |
| 把这个工单转任务 / 工单转项目 | **odoo_helpdesk_to_task** |
| 商机赢单建项目 / 商机转项目 | **odoo_lead_to_project** |
| 给客户发催款 / 发逾期提醒 | **odoo_invoice_send_reminder** |
| 库存预警 / 哪些产品要补货 / 缺货预警 | **odoo_stock_low_alerts** |
| 各个仓库库存 / 按库位看库存 | **odoo_stock_by_location** |
| 验收这条调拨单 / 出库确认 | **odoo_stock_picking_validate** |
| 仓库总览 / 待出库待入库 / 仓储情况 | **odoo_warehouse_dashboard** |
| 我属于几家公司 / 公司列表 / 看公司 | **odoo_companies** |
| 创建采购订单 / 下采购单 / 给某供应商下单 | **odoo_purchase_create** |
| 确认采购订单 / 把这个 PO 下单 | **odoo_purchase_confirm** |
| 采购仪表盘 / 本月采购 / 采购总览 | **odoo_purchase_dashboard** |
| 应付账龄 / 我们欠供应商多少 / 老的未付账单 | **odoo_vendor_bill_aging** |
| 生产订单 / MO 列表 / 在制单 | **odoo_mo_list** |
| 确认生产订单 / 把 MO 启动 | **odoo_mo_confirm** |
| 查 BOM / 物料清单 / 这个产品由什么组成 | **odoo_bom_query** |
| 看会计凭证 / 凭证列表 / journal 分录 | **odoo_journal_entries** |
| 登记付款 / 收款 / 给这张发票登记入账 | **odoo_payment_register** |
| 科目表 / 会计科目 / 看 chart of accounts | **odoo_chart_of_accounts** |
| 异常检测 / 系统有什么不对 / 全局健康检查 | **odoo_anomaly_detect** |
| 老板 KPI / 一句话给我看 KPI / 公司核心指标 | **odoo_kpi_summary** |
| 给我导这个 PO 的 PDF / 生成报表 PDF / 打印发票 | **odoo_pdf_report** |
| 导出 CSV / 把数据导出来 / 给我生成表格 | **odoo_export_csv** |
| 看自动化规则 / 系统里的 base.automation | **odoo_automations** |
| 看计划任务 / 看 cron / 哪些任务在跑 | **odoo_cron_jobs** |
| 创建自动化规则 / 加 trigger / 自动跑 | **odoo_automation_create** |
| 重复客户 / 查重 / 联系人查重 | **odoo_data_quality_partners** |
| 重复产品 / 重复 SKU | **odoo_data_quality_products** |
| 数据完整性 / 缺字段 / 资料完整度 | **odoo_data_quality_completeness** |
| 合并客户 / 合并联系人 / 把这两个 partner 合一起 | **odoo_partners_merge** |
| 批量发邮件 / 给一批客户发模板邮件 | **odoo_batch_email** |
| 批量归档 / 批量停用 / 批量激活 | **odoo_batch_archive** |
| 批量改经办人 / 批量重新分配 | **odoo_batch_assign** |
| 翻译这个字段 / 多语言 / 改成英文版 | **odoo_translate_record** |
| 自定义字段 / x_ 开头的 / Studio 字段 | **odoo_custom_fields** |
| 创建系统用户 / 给这个员工建账号 | **odoo_user_create** |
| 看用户权限 / 我有哪些组 / 用户组 | **odoo_user_groups** |
| 系统里有哪些模型 / 列模型 / Studio 模型 | **odoo_model_list** |
| 看某模型的字段 / 这模型有哪些字段 | **odoo_model_fields** |
| 创建自定义模型 / 加新表 / Studio 新建模型 | **odoo_model_create** |
| 加自定义字段 / 给模型加字段 | **odoo_field_create** |
| 这条记录改过什么 / 看变更历史 / 审计日志 | **odoo_audit_log** |
| 谁登录过 / 登录记录 / login history | **odoo_login_history** |
| 这字段改过几次 / 字段变更历史 | **odoo_field_history** |
| 切换公司 / 切到 X 公司 / 改公司 | **odoo_company_switch** |
| 集团合并报表 / 跨公司汇总 / 多公司视图 | **odoo_consolidated_dashboard** |
| 数据透视 / pivot / 按维度聚合 | **odoo_pivot_data** |
| 邮件日志 / 看邮件发送 / 邮件失败 | **odoo_email_log** |
| 配 webhook / 出站 webhook / 创建 webhook | **odoo_webhook_create** |
| 把这条记录链接发我 / 分享给客户 / portal 链接 | **odoo_record_share_url** |
| 邮件队列 / 邮件为啥没发 / mail queue 健康 | **odoo_mail_queue** |
| 有哪些审批分类 / 审批种类 / 公司审批流程 | **odoo_approval_categories** |
| 我要请假 / 提个采购申请 / 申请出差报销 | **odoo_approval_create** |
| 提交审批 / 把这条审批送出去 | **odoo_approval_confirm** |
| 我有几条要批的 / 待审批 / 我手上的审批 | **odoo_approval_my_pending** |
| 复制这条记录 / 克隆订单 / 拷贝产品 | **odoo_record_clone** |
| 深复制带子表 / 复制销售单含明细 | **odoo_record_clone_with_lines** |
| CSV 导入 / 批量导入数据 / 上传数据 | **odoo_csv_import** |
| 谁关注了这条 / 关注者列表 / followers | **odoo_followers** |
| 关注这个商机 / 订阅记录 / 加入关注 | **odoo_subscribe** |
| 取消关注 / 不再订阅 / 退订 | **odoo_unsubscribe** |
| 看资源 / 设备列表 / 会议室 | **odoo_resources** |
| 工作时间表 / 班表 / 一周工作时间 | **odoo_resource_calendar** |
| 定期发报表 / 自动发 PDF / 报表订阅 | **odoo_report_schedule** |
| 看现有翻译 / 这字段有几种语言 | **odoo_translate_get** |
| 查看当前用什么凭据 / 我的连接是哪套 / 为什么没问我密码 | **odoo_whoami** |
| 断开连接 / 退出系统 | **odoo_disconnect** |

### 常用数据模型（技术内部标识，不在正文中朗读）

project.task · project.project · project.milestone · mail.activity · calendar.event ·
crm.lead · crm.stage · sale.order · purchase.order · helpdesk.ticket · account.move ·
res.partner · hr.employee · hr.leave · hr.attendance · stock.quant · stock.picking ·
account.analytic.line · approval.request · planning.slot · knowledge.article ·
mail.template · mail.mail · mail.followers · ir.attachment · documents.document
`;

export default definePluginEntry({
  id: 'odoo',
  name: '火一五·辉火云企业套件插件',
  description: '自然语言操作辉火云企业套件，实施经理助手，per-agent 凭据隔离',

  register(api: OpenClawPluginApi) {
    // 不在启动时全局连接。每个 agent 的连接在 odoo_connect 时按需恢复。
    registerTools(api);
    registerHooks(api);

    // 订阅入站回复 —— 渠道收到用户回复后调用 bus.reply()，这里把文字写回 辉火云内部动态
    replyUnsubscribe?.();
    replyUnsubscribe = notificationBus.onReply(async (reply) => {
      await handleInboundReply(api, reply);
    });

    // v1.21.0: 启动期 fire-and-forget 预热 default agent 连接
    // 不阻塞 plugin load / gateway 启动；失败也不影响启动（hook 就显示"未连接"）。
    // 解决"零配置 + 单用户"场景：有 manifest/共享凭据时启动后几秒内自动恢复，
    // 不再依赖 hook 内同步 tryRestoreAgent（v1.20 之前每次 before_prompt_build
    // 都阻塞 RPC 是首字延迟 P50=16.4s 的真凶）。多 agent 场景下其他 agent 仍按
    // 需在 odoo_connect 时初始化。
    void tryRestoreAgent(api, 'default').then((client) => {
      if (client?.isAuthenticated()) {
        api.logger.info('[odoo] 启动期 default agent 预热成功（凭据已恢复，免手动 connect）');
      }
    }).catch((err) => {
      api.logger.warn(`[odoo] 启动期 default agent 预热失败（不影响启动，hook 会显示"未连接"）: ${err instanceof Error ? err.message : String(err)}`);
    });

    api.logger.info('[odoo] 辉火云企业套件插件 v1.22.0 已加载（per-agent 隔离 + 跨渠道通知基座 + 入站回复 + sale/purchase orders 按编号+明细一次取 + 异步预热不阻塞）');
  },
});

// ── 公共 API：供企微 / 钉钉 / 飞书等渠道插件作为依赖引入 ────────────────────
// 方式 A（推荐）：
//   import { notificationBus } from '@huo15/huo15-huihuoyun-odoo';
//   notificationBus.subscribe(env => { ... });
// 方式 B（无依赖解耦）：
//   const bus = (globalThis as any)[Symbol.for('openclaw.huo15.notification-bus.v1')];
export { notificationBus } from './src/modules/notification-bus.js';
export type {
  NotificationEnvelope,
  NotificationKind,
  NotificationPriority,
  ChannelTarget,
  ChannelTransport,
  DeliveryResult,
} from './src/types/index.js';

// ── 初始化客户端（per-agent）─────────────────────────────────────────────────
async function initOdooClient(
  api: OpenClawPluginApi,
  odooConfig: NonNullable<OdooPluginConfig['odoo']>,
  agentId: string = 'default',
): Promise<OdooClient> {
  const client = new OdooClient(odooConfig);
  await client.authenticate();
  odooClients.set(agentId, client);

  const syncConfig = ((api.pluginConfig ?? {}) as OdooPluginConfig).sync ?? {
    enabled: true, intervalSeconds: 30, channels: ['todo', 'activity', 'message'],
  };

  if (syncConfig.enabled !== false) {
    pollers.get(agentId)?.stop();
    const poller = new NotificationPoller(client);
    pollers.set(agentId, poller);
    poller.start((updates: SyncUpdate[]) => handleOdooUpdates(api, updates, agentId),
      { intervalSeconds: syncConfig.intervalSeconds, channels: syncConfig.channels });
  }

  api.logger.info(`[odoo] agent=${agentId} 已连接 ${odooConfig.url}，uid=${client.getUid()}`);
  return client;
}

/**
 * 尝试恢复 agent 连接 —— 走 fallback 链，静默失败。
 *
 * 查找顺序（v1.10 共享凭据模型）：
 *   1) `{agentId}.json`          该 agent 的独立凭据（private）
 *   2) `default.json`            共享凭据（首次 connect 默认写这里）
 *   3) legacy `odoo-config.json` 向下兼容
 *   4) `api.pluginConfig.odoo`   manifest 预填的静态凭据（零配置部署）
 *
 * 1-3 由 ConfigManager.load 内部处理；4 在这里兜底。
 * 只要任一层命中，就 init client 缓存在 odooClients[agentId] 下 —— 不同 agent
 * 命中同一份凭据时各自持有独立的 OdooClient 实例，session 隔离。
 */
async function tryRestoreAgent(api: OpenClawPluginApi, agentId: string): Promise<OdooClient | undefined> {
  if (odooClients.get(agentId)?.isAuthenticated()) return odooClients.get(agentId);

  // 1-3: ConfigManager 内置 fallback
  let saved = configManager.load(agentId);

  // 4: pluginConfig 兜底
  let sourceLabel: string;
  if (!saved?.odoo) {
    const fromManifest = (api.pluginConfig as OdooPluginConfig | undefined)?.odoo;
    if (!fromManifest) return undefined;
    saved = { odoo: fromManifest };
    sourceLabel = 'pluginConfig';
  } else {
    sourceLabel = configManager.getActiveSource(agentId);
  }

  try {
    api.logger.info(`[odoo] 恢复 agent=${agentId} 的连接（来源: ${sourceLabel}）...`);
    return await initOdooClient(api, saved.odoo!, agentId);
  } catch (err) {
    api.logger.error(`[odoo] agent=${agentId} 恢复失败（来源 ${sourceLabel}）: ${err instanceof Error ? err.message : String(err)}`);
    return undefined;
  }
}

// ── 工具辅助 ──────────────────────────────────────────────────────────────────
function getClient(ctx: Record<string, unknown>): OdooClient | undefined {
  const aid = getAgentId(ctx);
  const client = odooClients.get(aid);
  return client?.isAuthenticated() ? client : undefined;
}
function notConnected() {
  return { success: false, message: '未连接到辉火云企业套件，请先提供系统地址、用户名和密码进行连接。' };
}
function getAgentId(ctx: Record<string, unknown>) {
  return (ctx['agentId'] as string | undefined)?.trim() || 'default';
}
function stripHtml(html: string) {
  return String(html ?? '').replace(/<[^>]+>/g, '').trim().substring(0, 300);
}

/**
 * 把后端 read() 返回的字段值归一化为 write() 可接受的形式。
 *   - null / undefined / false → false
 *   - many2one: [id, "名称"]    → id（write 只收 id）
 *   - many2many: [id1, id2, …]  → [[6, false, [id1, id2, …]]]（write 要求 command tuple）
 *   - 其它标量：原样保留
 */
function normalizeFieldSnapshot(v: unknown): unknown {
  if (v === null || v === undefined || v === false) return false;
  if (Array.isArray(v)) {
    if (v.length === 2 && typeof v[0] === 'number' && typeof v[1] === 'string') {
      return v[0]; // many2one
    }
    if (v.every(x => typeof x === 'number')) {
      return [[6, false, v]]; // many2many
    }
  }
  return v;
}

/**
 * 有审计的 write：先读旧值快照，再 write，再把变更写入 mutation-log。
 * 用于所有用户触发的单/多记录更新，让"撤销上一步"可用。
 */
async function loggedWrite(
  client: OdooClient,
  ctx: Record<string, unknown>,
  args: {
    tool: string;
    model: string;
    ids: number[];
    values: Record<string, unknown>;
    summary: string;
  },
): Promise<void> {
  const fields = Object.keys(args.values);
  let before: Record<string, unknown>[] = [];
  if (fields.length > 0) {
    try {
      const recs = await client.read(args.model, args.ids, fields);
      before = args.ids.map(id => {
        const r = (recs.find(rr => rr['id'] === id) ?? {}) as Record<string, unknown>;
        const snap: Record<string, unknown> = { id };
        for (const f of fields) {
          snap[f] = normalizeFieldSnapshot(r[f]);
        }
        return snap;
      });
    } catch {
      before = []; // 快照失败 → 不可逆但不阻断 write
    }
  }
  await client.write(args.model, args.ids, args.values);
  mutationLog.append(getAgentId(ctx), {
    tool: args.tool,
    model: args.model,
    ids: args.ids,
    before,
    after: args.values,
    reversible: before.length === args.ids.length && before.length > 0,
    summary: args.summary,
  });
}

// ── 注册工具（共 190 个，含 v1.19 odoo_help）───────────────────────────────
// v1.20 ⭐ 引入工具分级（tier）——默认只暴露 30 个高频核心工具，节省 ~14000 tokens prompt schema
//   tier='core'（默认）：30 个高频工具直接可见，覆盖 80% 日常场景
//   tier='extended'：全部 204 个工具可见（v1.19/v1.20 全量行为）
//   tier='minimal'：仅 10 个最小集（仅核心连接和任务）
// 用户在 ~/.openclaw/openclaw.json 改 plugins.entries.odoo.config.tier 切换：
//   "plugins": { "entries": { "odoo": { "config": { "tier": "extended" } } } }
// odoo_help 工具始终注册（任何 tier），LLM 通过它按需查完整工具表。
const ODOO_TOOL_TIERS = {
  // 最小集（10）——仅连接和最核心任务
  minimal: new Set<string>([
    'odoo_connect', 'odoo_status', 'odoo_disconnect', 'odoo_whoami', 'odoo_help',
    'odoo_create_task', 'odoo_list_tasks', 'odoo_my_today',
    'odoo_search', 'odoo_daily_briefing',
  ]),
  // 核心 44 个（默认）——覆盖 80% 日常需求
  // v1.20.2: 加入 v1.20 14 个 tool（之前用 api.registerTool 直注册绕过 tier 系统，
  //          现已统一走 register helper；为保持 default 启用语义不变，纳入 core）
  core: new Set<string>([
    // 连接&状态 (5)
    'odoo_connect', 'odoo_status', 'odoo_disconnect', 'odoo_whoami', 'odoo_help',
    // 任务&活动 (8)
    'odoo_create_task', 'odoo_list_tasks', 'odoo_update_task', 'odoo_my_today', 'odoo_my_workload',
    'odoo_create_activity', 'odoo_calendar_today', 'odoo_complete_activity',
    // CRM (5)
    'odoo_crm_pipeline', 'odoo_crm_create', 'odoo_crm_update', 'odoo_crm_won', 'odoo_crm_lost',
    // 项目 (2)
    'odoo_project_overview', 'odoo_timesheet_log',
    // 客服 (2)
    'odoo_tickets', 'odoo_ticket_create',
    // 财务 (3)
    'odoo_invoices', 'odoo_sale_orders', 'odoo_purchase_orders',
    // 联系人 (2)
    'odoo_contacts', 'odoo_contact_create',
    // 检索/概况 (2)
    'odoo_search', 'odoo_daily_briefing',
    // 消息 (1)
    'odoo_message_post',
    // 审批工作流深化 (4) v1.20
    'odoo_approval_categories', 'odoo_approval_create', 'odoo_approval_confirm', 'odoo_approval_my_pending',
    // 记录克隆/批量导入 (3) v1.20
    'odoo_record_clone', 'odoo_record_clone_with_lines', 'odoo_csv_import',
    // Mail 关注/订阅 (3) v1.20
    'odoo_followers', 'odoo_subscribe', 'odoo_unsubscribe',
    // 资源/日历 (2) v1.20
    'odoo_resources', 'odoo_resource_calendar',
    // 报表订阅 (1) v1.20
    'odoo_report_schedule',
    // 多语言 (1) v1.20
    'odoo_translate_get',
  ]),
};

function registerTools(api: OpenClawPluginApi) {
  // 读 tier 配置
  const cfg = (api.pluginConfig ?? {}) as { tier?: 'minimal' | 'core' | 'extended' };
  const tier: 'minimal' | 'core' | 'extended' = cfg.tier ?? 'core';
  const allowedTools: Set<string> | null = tier === 'extended' ? null : ODOO_TOOL_TIERS[tier];

  let registeredCount = 0;
  let skippedCount = 0;

  // 包装 api.registerTool —— 仅注册 tier 内的工具
  // v1.20.2: 字段名适配 openclaw plugin SDK
  //   旧: { schema, handler }  → 新: { parameters, execute }
  //   不改 200+ 处 tool 定义，集中在 helper 一次转换
  //   触发：当时 SDK 校验 typeof tool.execute !== 'function' 直接判 malformed
  //         导致整个 plugin 50+ tool 被 loader 跳过，每次 plugin reload
  //         (~每 90s 一次) gateway prep 阶段多 5s+
  const toSdkTool = (opts: any) => {
    const { schema, handler, ...rest } = opts;
    return {
      ...rest,
      ...(schema !== undefined && { parameters: schema }),
      ...(handler !== undefined && { execute: handler }),
    };
  };

  const register = <T extends { name: string }>(opts: T) => {
    if (allowedTools === null || allowedTools.has((opts as any).name) || (opts as any).name === 'odoo_help') {
      api.registerTool(toSdkTool(opts) as unknown as Parameters<typeof api.registerTool>[0]);
      registeredCount += 1;
    } else {
      skippedCount += 1;
    }
  };

  // ══════════════════════════════════════════════════════
  // 连接 & 状态
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_connect',
    description: '连接辉火云企业套件。**默认按当前 sender_id 隔离保存**（每个企微/钉钉/飞书成员配自己的辉火云账号，与 Odoo 内部 RBAC 对齐：销售看销售的、管理员看管理员的）。仅当用户明确说"组织共用一个账号"/"配一次大家都用"时才传 shared=true（写入全员 fallback，会让 Odoo RBAC 失效，所有人看到的数据一致）。db 为可选，不传则自动检测（单库自动、多库返回列表）。',
    schema: {
      type: 'object',
      properties: {
        url:      { type: 'string', description: '辉火云企业套件 系统地址，如 https://www.huo15.com' },
        db:       { type: 'string', description: '数据库名称（可选，只有一个数据库时可省略）' },
        username: { type: 'string', description: '用户名（邮箱或登录名）' },
        password: { type: 'string', description: '密码' },
        shared:   { type: 'boolean', description: '可选，默认 false。false = 仅保存为当前 sender_id 专属凭据（推荐，权限按 Odoo 用户区分）；true = 保存为全员共享凭据（所有成员共用同一账号，Odoo RBAC 失效）。仅当用户明确说"组织共用"才传 true。' },
        private:  { type: 'boolean', description: '【已废弃，仅向下兼容 v1.22-】保留以兼容旧 agent memory；新调用请用 shared 参数（语义相反）。如同时传 private 和 shared，shared 优先。' },
      },
      required: ['url', 'username', 'password'],
    },
    async handler(
      params: { url: string; db?: string; username: string; password: string; shared?: boolean; private?: boolean },
      ctx: Record<string, unknown>,
    ) {
      const aid = getAgentId(ctx);
      let db = params.db;

      // 未指定 db 时自动检测
      if (!db) {
        try {
          const dbs = await OdooClient.listDatabases(params.url);
          if (dbs.length === 0) return { success: false, message: '该辉火云实例没有可用的数据库' };
          if (dbs.length === 1) {
            db = dbs[0];
          } else {
            return { success: false, needSelectDb: true, databases: dbs, message: `检测到 ${dbs.length} 个数据库，请告诉我要连接哪一个：${dbs.join('、')}` };
          }
        } catch {
          return { success: false, message: '无法自动检测数据库列表，请手动提供数据库名称（db 参数）' };
        }
      }

      const cfg = { url: params.url, db, username: params.username, password: params.password };
      // v1.23.0 默认反转：shared 显式传了用 shared，否则看 private 兼容（!private = agent），都没传 = agent
      let scope: 'shared' | 'agent';
      if (typeof params.shared === 'boolean') {
        scope = params.shared ? 'shared' : 'agent';
      } else if (typeof params.private === 'boolean') {
        // 旧参数兼容：private=true → agent（同 v1.22 行为），private=false → 旧默认是 shared，但 v1.23 默认改了，
        // 这里维持"显式传 private=false"的语义为 shared（仅兼容老 agent 主动传 false 的场景）。
        scope = params.private ? 'agent' : 'shared';
      } else {
        scope = 'agent';
      }
      try {
        await initOdooClient(api, cfg, aid);
        configManager.saveOdooConfig(cfg, aid, scope);
        const scopeMsg = scope === 'shared'
          ? '已保存为【组织共享凭据】—— 全员共用同一账号，Odoo 内部权限不再区分人。如要改回每人独立账号（推荐），让对方调 odoo_connect 不传 shared 即可。'
          : '已保存为【你自己的专属凭据】—— 只对当前 sender_id 生效，权限按你的 Odoo 账号区分（销售/管理员/财务等）。其他同事 @ 机器人时各自配自己的账号即可。';
        return {
          success: true,
          scope,
          message: `已成功连接到 ${params.url}（数据库: ${db}），欢迎使用辉火云企业套件！${scopeMsg}`,
        };
      } catch (e) { return { success: false, message: `连接失败: ${e instanceof Error ? e.message : String(e)}` }; }
    },
  });

  register({
    name: 'odoo_status',
    description: '检查辉火云企业套件连接状态',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const aid = getAgentId(ctx);
      const client = odooClients.get(aid);
      const info = client?.getSessionInfo();
      return { success: true, connected: client?.isAuthenticated() ?? false, agentId: aid, uid: info?.uid ?? null, username: info?.username ?? null, url: info?.url ?? null, polling: pollers.get(aid)?.getStatus() ?? null };
    },
  });

  register({
    name: 'odoo_disconnect',
    description: '断开当前会话的辉火云企业套件连接。默认安全模式：只清除当前 agent 的【独立凭据】（如有），不会影响组织的【共享凭据】。如需彻底清除全员共用的共享凭据（高危，会导致所有成员断开），传 force_shared=true。',
    schema: {
      type: 'object',
      properties: {
        force_shared: { type: 'boolean', description: '可选，默认 false。true = 同时清除组织共享凭据（影响所有成员）；false = 只断开当前会话，保留共享凭据' },
      },
    },
    async handler(p: { force_shared?: boolean } | undefined, ctx: Record<string, unknown>) {
      const aid = getAgentId(ctx);
      const sourceBefore = configManager.getActiveSource(aid);

      pollers.get(aid)?.stop();
      pollers.delete(aid);
      const client = odooClients.get(aid);
      if (client) {
        try { await client.destroy(); } catch { /* ignore */ }
        odooClients.delete(aid);
      }

      const hadOwn = configManager.clearOwnConfig(aid);
      let sharedCleared = false;
      if (p?.force_shared) {
        sharedCleared = configManager.clearSharedConfig();
      }

      let message: string;
      if (sharedCleared) {
        message = '⚠️ 已断开当前会话，并清除了组织【共享凭据】。所有渠道的 @ 机器人成员都需要重新连接。';
      } else if (hadOwn) {
        message = '已断开当前会话的【专属凭据】。组织共享凭据未受影响 —— 下一次 @ 机器人会自动 fallback 到共享凭据。';
      } else if (sourceBefore === 'shared' || sourceBefore === 'legacy') {
        message = '当前会话已从内存断开，但用的是组织【共享凭据】，已为你保留 —— 不影响其他成员。下一次 @ 机器人会自动重连。如需彻底清除共享凭据，调用 odoo_disconnect(force_shared=true)。';
      } else {
        message = '当前会话已断开。';
      }
      return { success: true, sharedCleared, hadOwnConfig: hadOwn, message };
    },
  });

  register({
    name: 'odoo_whoami',
    description: '查看当前 @ 机器人的会话使用的是哪套辉火云凭据 —— 共享凭据 / 当前会话专属 / manifest 静态预填 / 未连接。用于排查"为什么 @ 机器人时没问我密码？"或"我的连接是哪套？"等疑问。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const aid = getAgentId(ctx);
      const client = odooClients.get(aid);
      const connected = client?.isAuthenticated() ?? false;
      const source = configManager.getActiveSource(aid);
      const info = client?.getSessionInfo();
      const fromManifest = (api.pluginConfig as OdooPluginConfig | undefined)?.odoo;

      const sourceLabel: Record<string, string> = {
        agent: '当前会话专属凭据（{agentId}.json）',
        shared: '组织共享凭据（default.json，全员共用）',
        legacy: '历史遗留单文件凭据（odoo-config.json）',
        none: fromManifest ? 'manifest 静态预填（pluginConfig.odoo）' : '未连接（无任何凭据来源）',
      };

      return {
        success: true,
        connected,
        agentId: aid,
        source,
        sourceLabel: sourceLabel[source] ?? '未知',
        url: info?.url ?? null,
        username: info?.username ?? null,
        uid: info?.uid ?? null,
        sharedConfigExists: configManager.hasSharedConfig(),
        ownConfigExists: configManager.hasOwnConfig(aid),
        manifestConfigExists: !!fromManifest,
        message: connected
          ? `当前 @ 机器人会话已连接到 ${info?.url}（用户 ${info?.username}），凭据来源：${sourceLabel[source]}。`
          : `当前会话尚未连接。${configManager.hasSharedConfig() ? '组织有共享 fallback 凭据但当前 sender_id 还没自己配过，下一次操作会用共享凭据；建议你 odoo_connect 配自己的账号以获得对应权限。' : (fromManifest ? '插件 manifest 已预填凭据，下一次操作会自动连接。' : '需要先调用 odoo_connect 配置凭据（默认按你自己的 sender_id 隔离保存，权限按你的 Odoo 账号区分）。')}`,
      };
    },
  });

  // ══════════════════════════════════════════════════════
  // 任务 / 待办
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_create_task',
    description: '创建待办任务。用于"帮我写个待办"、"创建任务"等指令。',
    schema: {
      type: 'object',
      properties: {
        name:          { type: 'string', description: '任务名称（必填）' },
        description:   { type: 'string', description: '详细描述' },
        date_deadline: { type: 'string', description: '截止日期 YYYY-MM-DD' },
        priority:      { type: 'string', enum: ['0','1','2','3'], description: '优先级：0普通 1中 2高 3紧急' },
        project_id:    { type: 'number', description: '所属项目ID' },
        user_ids:      { type: 'array',  items: { type: 'number' }, description: '指派用户ID列表' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; description?: string; date_deadline?: string; priority?: '0'|'1'|'2'|'3'; project_id?: number; user_ids?: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const taskId = await client.createTask({ name: p.name, description: p.description, date_deadline: p.date_deadline, priority: p.priority, project_id: p.project_id, user_ids: p.user_ids });
        return { success: true, taskId, message: `待办「${p.name}」已创建，ID: ${taskId}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_list_tasks',
    description: '查看我的待办任务（To-Do 应用，私人任务，无项目）。默认只看进行中。',
    schema: {
      type: 'object',
      properties: {
        limit:          { type: 'number',  description: '上限，默认50' },
        project_id:     { type: 'number',  description: '指定项目ID（指定后切换到项目任务模式）' },
        today_only:     { type: 'boolean', description: '只看今日截止' },
        stage_state:    { type: 'string',  description: "任务状态：in_progress（进行中，默认）/ done（已完成）/ all（全部）" },
        state_filter:   { type: 'string',  description: "直接指定 state 值：01_in_progress / 02_changes_requested / 03_approved / 1_done / 1_canceled / 04_waiting_normal" },
        stage_id:       { type: 'number',  description: '指定具体阶段ID' },
        include_project: { type: 'boolean', description: 'true=同时包含项目任务（默认 false，仅待办私人任务）' },
      },
    },
    async handler(p: { limit?: number; project_id?: number; today_only?: boolean; stage_state?: string; state_filter?: string; stage_id?: number; include_project?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const tasks = await client.getMyTasks({ limit: p.limit, project_id: p.project_id, today_only: p.today_only, stage_state: p.stage_state as 'in_progress' | 'done' | 'all', state_filter: p.state_filter, stage_id: p.stage_id, include_project: p.include_project });
        return { success: true, count: tasks.length, tasks: tasks.map(t => ({ id: t['id'], name: t['name'], project: t['project_id'], deadline: t['date_deadline'], priority: t['priority'], stage_id: t['stage_id'], state: t['state'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_get_task_stages',
    description: '查看项目任务阶段列表（stage_id），用于 odoo_update_task 时指定正确的阶段ID。',
    schema: {
      type: 'object',
      properties: {
        project_id: { type: 'number', description: '项目ID（可选，不填则返回所有阶段）' },
      },
    },
    async handler(p: { project_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const stages = await client.getTaskStages(p.project_id);
        return { success: true, count: stages.length, stages: stages.map(s => ({ id: s['id'], name: s['name'], fold: s['fold'], is_done_stage: s['fold'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_update_task',
    description: '更新任务的阶段（状态）、截止日期、优先级等字段。通过 stage_id 改变任务的工作流状态。',
    schema: {
      type: 'object',
      properties: {
        task_id:       { type: 'number', description: '任务ID（必填）' },
        name:          { type: 'string', description: '新名称' },
        stage_id:      { type: 'number', description: '新阶段ID（stage_id），用于改变任务状态' },
        date_deadline: { type: 'string', description: '新截止日期 YYYY-MM-DD' },
        priority:      { type: 'string', enum: ['0','1','2','3'], description: '新优先级' },
        description:   { type: 'string', description: '新描述' },
        active:       { type: 'boolean', description: '任务激活状态，false=归档' },
      },
      required: ['task_id'],
    },
    async handler(p: { task_id: number; name?: string; stage_id?: number; date_deadline?: string; priority?: string; description?: string; active?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const values: Record<string, unknown> = {};
      if (p.name !== undefined) values['name'] = p.name;
      if (p.stage_id !== undefined) values['stage_id'] = p.stage_id;
      if (p.date_deadline !== undefined) values['date_deadline'] = p.date_deadline || false;
      if (p.priority !== undefined) values['priority'] = p.priority;
      if (p.description !== undefined) values['description'] = p.description;
      if (p.active !== undefined) values['active'] = p.active;
      if (Object.keys(values).length === 0) {
        return { success: true, message: `任务 #${p.task_id} 无需更新（未提供任何字段）` };
      }
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_update_task',
          model: 'project.task',
          ids: [p.task_id],
          values,
          summary: `更新任务 #${p.task_id}（字段：${Object.keys(values).join(', ')}）`,
        });
        return { success: true, message: `任务 #${p.task_id} 已更新（可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 活动 / 日历
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_create_activity',
    description: '创建活动提醒（关联到某条记录）。用于"提醒我明天开会"等。',
    schema: {
      type: 'object',
      properties: {
        res_model:        { type: 'string', description: '关联模型，如 project.task、crm.lead、res.partner' },
        res_id:           { type: 'number', description: '关联记录ID' },
        activity_type_id: { type: 'number', description: '活动类型ID（4=待办，1=邮件，2=电话，通过 odoo_activity_types 查询）' },
        summary:          { type: 'string', description: '活动摘要/标题' },
        note:             { type: 'string', description: '详细说明' },
        date_deadline:    { type: 'string', description: '截止日期 YYYY-MM-DD' },
        user_id:          { type: 'number', description: '负责人ID，默认当前用户' },
      },
      required: ['res_model', 'res_id', 'activity_type_id', 'date_deadline'],
    },
    async handler(p: { res_model: string; res_id: number; activity_type_id: number; summary?: string; note?: string; date_deadline: string; user_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createActivity(p);
        return { success: true, activityId: id, message: `活动「${p.summary ?? ''}」已创建` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_list_activities',
    description: '查看今日及逾期活动提醒。用于"我今天有什么活动"等。',
    schema: { type: 'object', properties: { limit: { type: 'number', description: '上限，默认30' } } },
    async handler(p: { limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const acts = await client.getTodayActivities({ limit: p.limit ?? 30 });
        return { success: true, count: acts.length, activities: acts.map(a => ({ id: a['id'], summary: a['summary'], deadline: a['date_deadline'], type: a['activity_type_id'], model: a['res_model'], state: a['state'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_activity_types',
    description: '查询辉火云企业套件可用的活动类型列表（获取 activity_type_id）',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const types = await client.getActivityTypes();
        return { success: true, types: types.map(t => ({ id: t['id'], name: t['name'], icon: t['icon'], category: t['category'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_create_event',
    description: '创建日历事件/会议。用于"安排一个会议"、"明天上午10点开产品评审"等。',
    schema: {
      type: 'object',
      properties: {
        name:        { type: 'string',                           description: '事件名称（必填）' },
        start:       { type: 'string',                           description: '开始时间 YYYY-MM-DD HH:MM:SS（必填）' },
        stop:        { type: 'string',                           description: '结束时间 YYYY-MM-DD HH:MM:SS（必填）' },
        description: { type: 'string',                           description: '描述/议程' },
        partner_ids: { type: 'array', items: { type: 'number' }, description: '参与人 partner ID 列表' },
      },
      required: ['name', 'start', 'stop'],
    },
    async handler(p: { name: string; start: string; stop: string; description?: string; partner_ids?: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createCalendarEvent(p);
        return { success: true, eventId: id, message: `日历事件「${p.name}」已创建，ID: ${id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 消息
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_get_messages',
    description: '查看未读消息和邮件通知。用于"查看我的消息"、"看看邮件"等。',
    schema: {
      type: 'object',
      properties: {
        type:        { type: 'string', enum: ['message','email'], description: 'message=chatter消息，email=邮件通知' },
        limit:       { type: 'number', description: '上限，默认20' },
        unread_only: { type: 'boolean', description: '只看未读，默认true' },
      },
    },
    async handler(p: { type?: 'message'|'email'; limit?: number; unread_only?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const limit = p.limit ?? 20;
      try {
        if (p.type === 'email') {
          const n = await client.getInboxNotifications({ limit });
          return { success: true, type: 'email', count: n.length, messages: n };
        }
        const msgs = p.unread_only !== false
          ? await client.getUnreadMessages({ limit })
          : (await client.searchRead('mail.message', [['message_type','!=','notification']], ['id','subject','body','author_id','date','model','res_id'], { limit })).records;
        return { success: true, type: 'message', count: msgs.length, messages: msgs.map(m => ({ id: m['id'], subject: m['subject'], body: stripHtml(String(m['body'] ?? '')), author: m['author_id'], date: m['date'], model: m['model'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_send_message',
    description: '向某条 辉火云记录发送 chatter 消息。',
    schema: {
      type: 'object',
      properties: {
        model:   { type: 'string', description: '目标模型，如 project.task、crm.lead、sale.order' },
        res_id:  { type: 'number', description: '目标记录ID' },
        body:    { type: 'string', description: '消息内容（支持HTML）' },
        subject: { type: 'string', description: '主题（可选）' },
      },
      required: ['model', 'res_id', 'body'],
    },
    async handler(p: { model: string; res_id: number; body: string; subject?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.call('mail.message', 'create', [{ model: p.model, res_id: p.res_id, body: p.body, subject: p.subject ?? '', message_type: 'comment', subtype_xmlid: 'mail.mt_comment' }]);
        return { success: true, messageId: id, message: `消息已发送，ID: ${id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 通用搜索
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_search',
    description: '通用搜索辉火云企业套件任意数据模型。用于"查客户"、"查销售订单"、"查库存"等。',
    schema: {
      type: 'object',
      properties: {
        model:  { type: 'string', description: '模型名：res.partner / project.task / crm.lead / sale.order / purchase.order / stock.quant / hr.employee / account.move 等' },
        domain: { type: 'array',  description: '搜索域 [[field, op, value], ...]' },
        fields: { type: 'array',  items: { type: 'string' }, description: '返回字段' },
        limit:  { type: 'number', description: '上限，默认20' },
        order:  { type: 'string', description: '排序，如 "create_date desc"' },
      },
      required: ['model'],
    },
    async handler(p: { model: string; domain?: unknown[]; fields?: string[]; limit?: number; order?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const r = await client.searchRead(p.model, (p.domain as [string,string,unknown][]) ?? [], p.fields ?? ['id','name'], { limit: p.limit ?? 20, order: p.order });
        return { success: true, count: r.length, records: r.records };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // CRM 商机
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_crm_pipeline',
    description: '查看 CRM 商机管道。用于"查看我的商机"、"销售管道情况"等。',
    schema: {
      type: 'object',
      properties: {
        limit:     { type: 'number',  description: '上限，默认30' },
        stage_id:  { type: 'number',  description: '按阶段ID筛选' },
        user_id:   { type: 'number',  description: '按销售员筛选' },
        type:      { type: 'string',  enum: ['lead','opportunity'], description: '线索或商机' },
        all_users: { type: 'boolean', description: '查看全部用户商机（不只是自己）' },
      },
    },
    async handler(p: { limit?: number; stage_id?: number; user_id?: number; type?: 'lead'|'opportunity'; all_users?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const uid = client.getUid() ?? 0;
      try {
        const leads = await client.getCrmPipeline({ limit: p.limit, stage_id: p.stage_id, user_id: p.all_users ? undefined : (p.user_id ?? uid), type: p.type });
        return { success: true, count: leads.length, pipeline: leads.map(l => ({ id: l['id'], name: l['name'], partner: l['partner_id'], stage: l['stage_id'], probability: l['probability'], revenue: l['expected_revenue'], deadline: l['date_deadline'], type: l['type'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_crm_create',
    description: '创建 CRM 商机或线索。用于"新建一个商机"等。',
    schema: {
      type: 'object',
      properties: {
        name:             { type: 'string', description: '商机名称（必填）' },
        type:             { type: 'string', enum: ['lead','opportunity'], description: '类型，默认 opportunity' },
        partner_id:       { type: 'number', description: '客户ID' },
        expected_revenue: { type: 'number', description: '预计收入' },
        probability:      { type: 'number', description: '赢单概率 0-100' },
        stage_id:         { type: 'number', description: '阶段ID' },
        date_deadline:    { type: 'string', description: '预计关单日期 YYYY-MM-DD' },
        description:      { type: 'string', description: '备注' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; type?: 'lead'|'opportunity'; partner_id?: number; expected_revenue?: number; probability?: number; stage_id?: number; date_deadline?: string; description?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createCrmLead(p);
        return { success: true, leadId: id, message: `${p.type === 'lead' ? '线索' : '商机'}「${p.name}」已创建，ID: ${id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_crm_update',
    description: '更新商机信息（阶段、金额、概率、截止日期等）。',
    schema: {
      type: 'object',
      properties: {
        lead_id:          { type: 'number', description: '商机ID（必填）' },
        name:             { type: 'string', description: '新名称' },
        stage_id:         { type: 'number', description: '新阶段ID' },
        expected_revenue: { type: 'number', description: '新预计收入' },
        probability:      { type: 'number', description: '新赢单概率 0-100' },
        date_deadline:    { type: 'string', description: '新截止日期 YYYY-MM-DD' },
        user_id:          { type: 'number', description: '新负责销售员ID' },
      },
      required: ['lead_id'],
    },
    async handler(p: { lead_id: number; name?: string; stage_id?: number; expected_revenue?: number; probability?: number; date_deadline?: string; user_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const values: Record<string, unknown> = {};
      if (p.name !== undefined) values['name'] = p.name;
      if (p.stage_id !== undefined) values['stage_id'] = p.stage_id;
      if (p.expected_revenue !== undefined) values['expected_revenue'] = p.expected_revenue;
      if (p.probability !== undefined) values['probability'] = p.probability;
      if (p.date_deadline !== undefined) values['date_deadline'] = p.date_deadline;
      if (p.user_id !== undefined) values['user_id'] = p.user_id;
      if (Object.keys(values).length === 0) {
        return { success: true, message: `商机 #${p.lead_id} 无需更新（未提供任何字段）` };
      }
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_crm_update',
          model: 'crm.lead',
          ids: [p.lead_id],
          values,
          summary: `更新商机 #${p.lead_id}（字段：${Object.keys(values).join(', ')}）`,
        });
        return { success: true, message: `商机 #${p.lead_id} 已更新（可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_crm_won',
    description: '将商机标记为赢单。用于"这个商机赢了"等。',
    schema: { type: 'object', properties: { lead_id: { type: 'number', description: '商机ID（必填）' } }, required: ['lead_id'] },
    async handler(p: { lead_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.setCrmWon([p.lead_id]);
        return { success: true, message: `商机 #${p.lead_id} 已标记为赢单` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_crm_lost',
    description: '将商机标记为输单/丢失。',
    schema: {
      type: 'object',
      properties: {
        lead_id:        { type: 'number', description: '商机ID（必填）' },
        lost_reason_id: { type: 'number', description: '丢单原因ID（可选）' },
      },
      required: ['lead_id'],
    },
    async handler(p: { lead_id: number; lost_reason_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.setCrmLost([p.lead_id], p.lost_reason_id);
        return { success: true, message: `商机 #${p.lead_id} 已标记为丢单` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 项目概览 & 工时
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_project_overview',
    description: '查看项目列表和里程碑进度。用于"项目情况"、"里程碑进度"等。',
    schema: {
      type: 'object',
      properties: {
        project_id:      { type: 'number',  description: '指定某个项目ID，不填则查全部' },
        show_milestones: { type: 'boolean', description: '是否同时返回里程碑，默认true' },
      },
    },
    async handler(p: { project_id?: number; show_milestones?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const [projects, milestones] = await Promise.all([
          client.getProjectOverview(p.project_id),
          p.show_milestones !== false ? client.getMilestones(p.project_id) : Promise.resolve([]),
        ]);
        return {
          success: true,
          projects: projects.map(pr => ({ id: pr['id'], name: pr['name'], partner: pr['partner_id'], manager: pr['user_id'], start: pr['date_start'], end: pr['date'], task_count: pr['task_count'], open_tasks: pr['open_task_count'], done_tasks: pr['closed_task_count'] })),
          milestones: milestones.map(m => ({ id: m['id'], name: m['name'], project: m['project_id'], deadline: m['deadline'], is_reached: m['is_reached'], tasks: m['task_count'], done_tasks: m['done_task_count'], overdue: m['is_deadline_exceeded'] })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_timesheet_log',
    description: '记录工时。用于"记录2小时工时"、"今天在项目A上工作了3小时"等。',
    schema: {
      type: 'object',
      properties: {
        name:       { type: 'string', description: '工作描述（必填）' },
        hours:      { type: 'number', description: '工时（小时）（必填）' },
        project_id: { type: 'number', description: '项目ID' },
        task_id:    { type: 'number', description: '任务ID' },
        date:       { type: 'string', description: '日期 YYYY-MM-DD，默认今天' },
      },
      required: ['name', 'hours'],
    },
    async handler(p: { name: string; hours: number; project_id?: number; task_id?: number; date?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.logTimesheet({ name: p.name, unit_amount: p.hours, project_id: p.project_id, task_id: p.task_id, date: p.date });
        return { success: true, timesheetId: id, message: `已记录 ${p.hours} 小时工时：「${p.name}」` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 销售 & 采购
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_sale_orders',
    description:
      '查询销售订单（sale.order）。支持三种用法：' +
      '(a) 列表浏览：limit + state + partner_id；' +
      '(b) **按订单编号查具体单**：name="S00016"（精确匹配，最常用）；' +
      '(c) 按记录 ID 直读：record_id=9。' +
      '⭐ 写合同 / 对账 / 回邮件这类需要明细的场景：**必传 include_lines=true**，' +
      '一次拿回 partner / 产品 / 数量 / 单价 / 折扣 / 小计 / 税额 / 合计 / 付款条件，' +
      '避免后续再发多次 RPC。**不要走 exec/curl 手写 JSON-RPC，本工具已经覆盖**。' +
      '返回字段含 amount_untaxed / amount_tax / amount_total / payment_term_id / currency_id；' +
      'include_lines=true 时每单挂 order_line[]（product_id, product_uom_qty, price_unit, ' +
      'discount, price_subtotal, price_total, price_tax）。',
    schema: {
      type: 'object',
      properties: {
        name:          { type: 'string', description: '订单编号（如 "S00016"），精确匹配。指定后 limit/state 通常无意义。' },
        record_id:     { type: 'number', description: '按 sale.order 记录 ID 直读（如 9）' },
        include_lines: { type: 'boolean', description: '是否同时拉订单明细行（sale.order.line），写合同/对账强烈建议 true。默认 false。' },
        limit:         { type: 'number', description: '上限，默认 20。仅列表场景使用。' },
        state:         { type: 'string', enum: ['draft','sent','sale','cancel'], description: '状态：draft=报价 sent=已发送 sale=销售订单 cancel=已取消' },
        partner_id:    { type: 'number', description: '按客户筛选' },
      },
    },
    async handler(
      p: { limit?: number; state?: string; partner_id?: number; name?: string; record_id?: number; include_lines?: boolean },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const orders = await client.getSaleOrders({
          limit: p.limit, state: p.state, partner_id: p.partner_id,
          name: p.name, record_id: p.record_id, include_lines: p.include_lines,
        });
        return {
          success: true,
          count: orders.length,
          orders: orders.map(o => ({
            id: o['id'],
            name: o['name'],
            partner: o['partner_id'],
            state: o['state'],
            date: o['date_order'],
            currency: o['currency_id'],
            amount_untaxed: o['amount_untaxed'],
            amount_tax: o['amount_tax'],
            amount_total: o['amount_total'],
            invoice_status: o['invoice_status'],
            payment_term: o['payment_term_id'],
            note: o['note'],
            order_line: o['order_line'],
          })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_purchase_orders',
    description:
      '查询采购订单（purchase.order）。支持三种用法：' +
      '(a) 列表浏览：limit + state；' +
      '(b) **按订单编号查具体单**：name="PO0001"（精确匹配）；' +
      '(c) 按记录 ID 直读：record_id=N。' +
      '⭐ 对账 / 写采购合同 / 回供应商邮件：**必传 include_lines=true**，' +
      '一次拿回 vendor / 产品 / 数量 / 单价 / 小计 / 税额 / 合计 / 计划到货，避免 N+1 RPC。' +
      '**不要走 exec/curl 手写 JSON-RPC，本工具已经覆盖**。',
    schema: {
      type: 'object',
      properties: {
        name:          { type: 'string', description: '订单编号（如 "PO0001"），精确匹配' },
        record_id:     { type: 'number', description: '按 purchase.order 记录 ID 直读' },
        include_lines: { type: 'boolean', description: '同时拉采购明细行（purchase.order.line），对账/合同强烈建议 true。默认 false。' },
        limit:         { type: 'number', description: '上限，默认 20。仅列表场景使用。' },
        state:         { type: 'string', enum: ['draft','sent','to approve','purchase','cancel'], description: '状态：draft=RFQ sent=已发送 to approve=待审批 purchase=采购订单 cancel=已取消' },
      },
    },
    async handler(
      p: { limit?: number; state?: string; name?: string; record_id?: number; include_lines?: boolean },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const orders = await client.getPurchaseOrders({
          limit: p.limit, state: p.state,
          name: p.name, record_id: p.record_id, include_lines: p.include_lines,
        });
        return {
          success: true,
          count: orders.length,
          orders: orders.map(o => ({
            id: o['id'],
            name: o['name'],
            vendor: o['partner_id'],
            state: o['state'],
            date: o['date_order'],
            planned_arrival: o['date_planned'],
            currency: o['currency_id'],
            amount_untaxed: o['amount_untaxed'],
            amount_tax: o['amount_tax'],
            amount_total: o['amount_total'],
            invoice_status: o['invoice_status'],
            payment_term: o['payment_term_id'],
            notes: o['notes'],
            order_line: o['order_line'],
          })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 客服工单（Helpdesk）
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_tickets',
    description: '查看客服工单列表。用于"查看工单"、"有哪些待处理问题"等。',
    schema: {
      type: 'object',
      properties: {
        limit:      { type: 'number',  description: '上限，默认30' },
        my_tickets: { type: 'boolean', description: '只看指派给我的工单，默认true' },
        priority:   { type: 'string',  enum: ['0','1','2','3'], description: '优先级筛选' },
        partner_id: { type: 'number',  description: '按客户筛选' },
        team_id:    { type: 'number',  description: '按团队筛选' },
      },
    },
    async handler(p: { limit?: number; my_tickets?: boolean; priority?: string; partner_id?: number; team_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const uid = client.getUid() ?? undefined;
      try {
        const tickets = await client.getHelpdeskTickets({ limit: p.limit, user_id: p.my_tickets !== false ? uid : undefined, priority: p.priority, partner_id: p.partner_id, team_id: p.team_id });
        return { success: true, count: tickets.length, tickets: tickets.map(t => ({ id: t['id'], ref: t['ticket_ref'], name: t['name'], team: t['team_id'], stage: t['stage_id'], priority: t['priority'], partner: t['partner_id'], sla_deadline: t['sla_deadline'], sla_fail: t['sla_fail'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_ticket_create',
    description: '创建客服工单。用于"帮我提交一个问题"、"新建工单"等。',
    schema: {
      type: 'object',
      properties: {
        name:        { type: 'string', description: '工单标题（必填）' },
        description: { type: 'string', description: '问题描述' },
        partner_id:  { type: 'number', description: '客户ID' },
        team_id:     { type: 'number', description: '处理团队ID' },
        priority:    { type: 'string', enum: ['0','1','2','3'], description: '优先级：0普通 1中 2高 3紧急' },
        user_id:     { type: 'number', description: '指派人员ID' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; description?: string; partner_id?: number; team_id?: number; priority?: '0'|'1'|'2'|'3'; user_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createHelpdeskTicket(p);
        return { success: true, ticketId: id, message: `工单「${p.name}」已创建，ID: ${id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 财务 / 发票
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_invoices',
    description: '查看发票/账单列表，支持查逾期应收。用于"查看发票"、"逾期未付款的"等。',
    schema: {
      type: 'object',
      properties: {
        limit:         { type: 'number',  description: '上限，默认20' },
        move_type:     { type: 'string',  enum: ['out_invoice','in_invoice','out_refund','in_refund'], description: '类型：out_invoice=客户发票 in_invoice=供应商账单' },
        payment_state: { type: 'string',  enum: ['not_paid','partial','paid','in_payment'], description: '付款状态' },
        overdue_only:  { type: 'boolean', description: '只看逾期未付发票' },
        partner_id:    { type: 'number',  description: '按客户/供应商筛选' },
      },
    },
    async handler(p: { limit?: number; move_type?: string; payment_state?: string; overdue_only?: boolean; partner_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const invoices = p.overdue_only
          ? await client.getOverdueInvoices()
          : await client.getInvoices({ limit: p.limit, move_type: p.move_type, payment_state: p.payment_state, partner_id: p.partner_id });
        return { success: true, count: invoices.length, invoices: invoices.map(i => ({ id: i['id'], name: i['name'], type: i['move_type'], partner: i['partner_id'], date: i['invoice_date'], due_date: i['invoice_date_due'], amount: i['amount_total'], payment_state: i['payment_state'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 联系人 / 客户（v1.2 新增）
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_contacts',
    description: '查询联系人/客户/供应商。用于"查客户"、"找供应商"、"搜索联系人"等。',
    schema: {
      type: 'object',
      properties: {
        keyword:       { type: 'string',  description: '按名称模糊搜索' },
        is_company:    { type: 'boolean', description: 'true=只看公司 false=只看个人' },
        customer_only: { type: 'boolean', description: '只看客户' },
        supplier_only: { type: 'boolean', description: '只看供应商' },
        limit:         { type: 'number',  description: '上限，默认30' },
      },
    },
    async handler(p: { keyword?: string; is_company?: boolean; customer_only?: boolean; supplier_only?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const contacts = await client.getPartners({ keyword: p.keyword, is_company: p.is_company, customer_rank: p.customer_only, supplier_rank: p.supplier_only, limit: p.limit });
        return { success: true, count: contacts.length, contacts: contacts.map(c => ({ id: c['id'], name: c['name'], email: c['email'], phone: c['phone'], mobile: c['mobile'], is_company: c['is_company'], city: c['city'], country: c['country_id'], parent: c['parent_id'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_contact_create',
    description: '创建联系人/客户/供应商。用于"添加新客户"、"创建联系人"等。',
    schema: {
      type: 'object',
      properties: {
        name:       { type: 'string',  description: '名称（必填）' },
        email:      { type: 'string',  description: '邮箱' },
        phone:      { type: 'string',  description: '电话' },
        mobile:     { type: 'string',  description: '手机' },
        is_company: { type: 'boolean', description: '是否公司，默认false' },
        city:       { type: 'string',  description: '城市' },
        street:     { type: 'string',  description: '街道/地址' },
        parent_id:  { type: 'number',  description: '所属公司ID（个人联系人时）' },
        is_customer:{ type: 'boolean', description: '标记为客户，默认true' },
        is_supplier:{ type: 'boolean', description: '标记为供应商，默认false' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; email?: string; phone?: string; mobile?: string; is_company?: boolean; city?: string; street?: string; parent_id?: number; is_customer?: boolean; is_supplier?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createPartner({
          name: p.name, email: p.email, phone: p.phone, mobile: p.mobile,
          is_company: p.is_company, city: p.city, street: p.street, parent_id: p.parent_id,
          customer_rank: (p.is_customer !== false) ? 1 : 0,
          supplier_rank: p.is_supplier ? 1 : 0,
        });
        return { success: true, contactId: id, message: `${p.is_company ? '公司' : '联系人'}「${p.name}」已创建，ID: ${id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 库存（v1.2 新增）
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_stock_levels',
    description: '查看库存水平。用于"查库存"、"产品XX还有多少"等。',
    schema: {
      type: 'object',
      properties: {
        keyword:     { type: 'string', description: '按产品名称模糊搜索' },
        product_id:  { type: 'number', description: '按产品ID筛选' },
        location_id: { type: 'number', description: '按库位筛选' },
        limit:       { type: 'number', description: '上限，默认50' },
      },
    },
    async handler(p: { keyword?: string; product_id?: number; location_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const stocks = await client.getStockLevels({ keyword: p.keyword, product_id: p.product_id, location_id: p.location_id, limit: p.limit });
        return { success: true, count: stocks.length, stock: stocks.map(s => ({ id: s['id'], product: s['product_id'], location: s['location_id'], lot: s['lot_id'], quantity: s['quantity'], reserved: s['reserved_quantity'], available: s['available_quantity'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_stock_pickings',
    description: '查看调拨单/出入库单。用于"查看待出库"、"调拨单情况"等。',
    schema: {
      type: 'object',
      properties: {
        limit: { type: 'number', description: '上限，默认20' },
        state: { type: 'string', enum: ['draft','waiting','confirmed','assigned','done','cancel'], description: '状态：assigned=就绪 waiting=等待 done=完成' },
        type:  { type: 'string', enum: ['incoming','outgoing','internal'], description: '类型：incoming=入库 outgoing=出库 internal=内部调拨' },
      },
    },
    async handler(p: { limit?: number; state?: string; type?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const pickings = await client.getStockPickings({ limit: p.limit, state: p.state, picking_type: p.type });
        return { success: true, count: pickings.length, pickings: pickings.map(pk => ({ id: pk['id'], name: pk['name'], partner: pk['partner_id'], type: pk['picking_type_id'], state: pk['state'], scheduled: pk['scheduled_date'], done: pk['date_done'], origin: pk['origin'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // HR 员工 / 考勤 / 请假（v1.2 新增）
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_employees',
    description: '查询员工列表。用于"查员工"、"某部门有谁"等。',
    schema: {
      type: 'object',
      properties: {
        keyword:       { type: 'string', description: '按名称模糊搜索' },
        department_id: { type: 'number', description: '按部门ID筛选' },
        limit:         { type: 'number', description: '上限，默认50' },
      },
    },
    async handler(p: { keyword?: string; department_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const emps = await client.getEmployees({ keyword: p.keyword, department_id: p.department_id, limit: p.limit });
        return { success: true, count: emps.length, employees: emps.map(e => ({ id: e['id'], name: e['name'], department: e['department_id'], job: e['job_id'], email: e['work_email'], phone: e['mobile_phone'], manager: e['parent_id'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_leaves',
    description: '查看请假记录。用于"我的请假记录"、"查看某人的请假"等。',
    schema: {
      type: 'object',
      properties: {
        employee_id: { type: 'number', description: '员工ID，不填则查当前用户' },
        state:       { type: 'string', enum: ['draft','confirm','validate1','validate','refuse'], description: '状态筛选' },
        limit:       { type: 'number', description: '上限，默认20' },
      },
    },
    async handler(p: { employee_id?: number; state?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const leaves = await client.getLeaves({ employee_id: p.employee_id, state: p.state, limit: p.limit });
        return { success: true, count: leaves.length, leaves: leaves.map(l => ({ id: l['id'], name: l['name'], employee: l['employee_id'], type: l['holiday_status_id'], from: l['date_from'], to: l['date_to'], days: l['number_of_days'], state: l['state'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_attendances',
    description: '查看考勤打卡记录。用于"我的考勤"、"打卡记录"等。',
    schema: {
      type: 'object',
      properties: {
        employee_id: { type: 'number', description: '员工ID，不填则查当前用户' },
        limit:       { type: 'number', description: '上限，默认20' },
      },
    },
    async handler(p: { employee_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getAttendances({ employee_id: p.employee_id, limit: p.limit });
        return { success: true, count: records.length, attendances: records.map(a => ({ id: a['id'], employee: a['employee_id'], check_in: a['check_in'], check_out: a['check_out'], worked_hours: a['worked_hours'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // HR 闭环（v1.11 新增 14 个）
  //   请假 5 + 报销 4 + 招聘 2 + 考核/工资/排班 3
  // ══════════════════════════════════════════════════════

  // ---------- 请假闭环（5 个） ----------

  register({
    name: 'odoo_leave_types',
    description: '查询请假类型列表（hr.leave.type），用于"有哪些假可以请"、"请假类型"。新建请假前先调一次拿到 holiday_status_id。',
    schema: {
      type: 'object',
      properties: {
        keyword: { type: 'string', description: '按名称模糊搜索' },
        limit:   { type: 'number', description: '上限，默认30' },
      },
    },
    async handler(p: { keyword?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const types = await client.getLeaveTypes({ keyword: p.keyword, limit: p.limit });
        return { success: true, count: types.length, leave_types: types.map(t => ({
          id: t['id'], name: t['name'], requires_allocation: t['requires_allocation'],
          validation: t['leave_validation_type'], unit: t['request_unit'], company: t['company_id'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_leave_create',
    description: '创建请假申请（hr.leave）。用于"我请假明天 / 我请假 5.1–5.3 / 帮某员工请病假"。日期格式 YYYY-MM-DD。先用 odoo_leave_types 查 holiday_status_id。',
    schema: {
      type: 'object',
      properties: {
        holiday_status_id:  { type: 'number', description: '请假类型 id（必填，从 odoo_leave_types 查）' },
        request_date_from:  { type: 'string', description: '开始日期 YYYY-MM-DD（必填）' },
        request_date_to:    { type: 'string', description: '结束日期 YYYY-MM-DD（必填，单日则与 from 相同）' },
        employee_id:        { type: 'number', description: '员工 id，不填默认为当前用户' },
        name:               { type: 'string', description: '请假事由说明' },
      },
      required: ['holiday_status_id', 'request_date_from', 'request_date_to'],
    },
    async handler(p: { holiday_status_id: number; request_date_from: string; request_date_to: string; employee_id?: number; name?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createLeave(p);
        return { success: true, id, message: `请假申请 #${id} 已提交，等待审批。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_leave_approve',
    description: '批准请假申请（hr.leave.action_approve）。会自动按 validation_type 推进到下一阶段（confirm→validate1→validate）。需要"我"是该请假的审批人。',
    schema: {
      type: 'object',
      properties: { leave_id: { type: 'number', description: '请假记录 id（必填）' } },
      required: ['leave_id'],
    },
    async handler(p: { leave_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.approveLeave(p.leave_id);
        return { success: true, message: `请假 #${p.leave_id} 已批准（按双重审批策略自动推进状态）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_leave_refuse',
    description: '拒绝请假申请（hr.leave.action_refuse）。',
    schema: {
      type: 'object',
      properties: { leave_id: { type: 'number', description: '请假记录 id（必填）' } },
      required: ['leave_id'],
    },
    async handler(p: { leave_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.refuseLeave(p.leave_id);
        return { success: true, message: `请假 #${p.leave_id} 已拒绝。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_leave_allocate',
    description: '【HR/管理员动作】给员工分配请假额度（hr.leave.allocation）。用于"给张三加 5 天年假"、"补一下王五本年度调休额度"。auto_approve=true 时会立即调 action_approve 直接生效（需要 hr_holidays.group_hr_holidays_user 权限）。',
    schema: {
      type: 'object',
      properties: {
        employee_id:       { type: 'number', description: '员工 id（必填）' },
        holiday_status_id: { type: 'number', description: '请假类型 id（必填）' },
        number_of_days:    { type: 'number', description: '分配天数（必填）' },
        name:              { type: 'string', description: '分配说明，如"2026 年初年假"' },
        date_from:         { type: 'string', description: '生效起始日期 YYYY-MM-DD，默认今天' },
        auto_approve:      { type: 'boolean', description: '是否创建后立即批准生效，默认 false（保留 draft 由其他人审批）' },
      },
      required: ['employee_id', 'holiday_status_id', 'number_of_days'],
    },
    async handler(p: { employee_id: number; holiday_status_id: number; number_of_days: number; name?: string; date_from?: string; auto_approve?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const { id, approved } = await client.createLeaveAllocation(p);
        return { success: true, id, approved,
          message: approved
            ? `已为员工 #${p.employee_id} 分配 ${p.number_of_days} 天假期（额度 #${id} 已批准生效）。`
            : `已为员工 #${p.employee_id} 创建 ${p.number_of_days} 天假期分配（#${id}），状态 draft 等待审批。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 报销闭环（4 个） ----------

  register({
    name: 'odoo_expenses',
    description: '查询报销列表（hr.expense）。用于"我的报销"、"待批的报销"。state 可筛 draft/submitted/approved/posted/paid/refused。',
    schema: {
      type: 'object',
      properties: {
        employee_id: { type: 'number', description: '员工 id，不填默认为当前用户' },
        state:       { type: 'string', enum: ['draft','submitted','approved','posted','paid','refused'], description: '状态筛选' },
        limit:       { type: 'number', description: '上限，默认30' },
      },
    },
    async handler(p: { employee_id?: number; state?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const expenses = await client.getExpenses(p);
        return { success: true, count: expenses.length, expenses: expenses.map(e => ({
          id: e['id'], name: e['name'], employee: e['employee_id'], product: e['product_id'],
          date: e['date'], amount: e['total_amount'], currency: e['currency_id'],
          state: e['state'], payment_state: e['payment_state'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_expense_create',
    description: '创建报销（hr.expense）。用于"我要报销 200 块的差旅"、"报销昨天的客户餐饮 350 元"。total_amount 是总金额（首选）。employee_id 不填则归到当前用户。',
    schema: {
      type: 'object',
      properties: {
        name:         { type: 'string', description: '报销描述（必填），如"客户餐饮"、"出差打车"' },
        total_amount: { type: 'number', description: '总金额（推荐填这个，简单直接）' },
        unit_amount:  { type: 'number', description: '单价（如果按数量计费）' },
        quantity:     { type: 'number', description: '数量，默认 1' },
        product_id:   { type: 'number', description: '报销品类 product_id，可选' },
        employee_id:  { type: 'number', description: '员工 id，不填默认当前用户' },
        date:         { type: 'string', description: '发生日期 YYYY-MM-DD，默认今天' },
        description:  { type: 'string', description: '详细说明' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; total_amount?: number; unit_amount?: number; quantity?: number; product_id?: number; employee_id?: number; date?: string; description?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createExpense(p);
        return { success: true, id, message: `报销 #${id} 已创建（草稿）。如需提交审批请调 odoo_expense_submit。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_expense_submit',
    description: '提交报销给经理审批（hr.expense.action_submit / action_submit_sheet）。用于"把这条报销提交"、"批量提交我所有 draft 报销"。',
    schema: {
      type: 'object',
      properties: { expense_ids: { type: 'array', items: { type: 'number' }, description: '报销 id 数组（必填）' } },
      required: ['expense_ids'],
    },
    async handler(p: { expense_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.submitExpense(p.expense_ids);
        return { success: true, message: `已提交报销 ${p.expense_ids.map(i => '#'+i).join(', ')} 给经理审批。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_expense_approve',
    description: '批准或拒绝报销（hr.expense.action_approve / action_refuse）。action="approve"/"refuse"。需要相应权限（团队审批人/财务）。',
    schema: {
      type: 'object',
      properties: {
        expense_ids: { type: 'array', items: { type: 'number' }, description: '报销 id 数组（必填）' },
        action:      { type: 'string', enum: ['approve', 'refuse'], description: '动作（必填）' },
        reason:      { type: 'string', description: '拒绝时的理由说明（可选，仅 refuse 用）' },
      },
      required: ['expense_ids', 'action'],
    },
    async handler(p: { expense_ids: number[]; action: 'approve' | 'refuse'; reason?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        if (p.action === 'approve') {
          await client.approveExpense(p.expense_ids);
          return { success: true, message: `报销 ${p.expense_ids.map(i => '#'+i).join(', ')} 已批准。` };
        }
        await client.refuseExpense(p.expense_ids, p.reason);
        return { success: true, message: `报销 ${p.expense_ids.map(i => '#'+i).join(', ')} 已拒绝${p.reason ? '（理由：' + p.reason + '）' : ''}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 招聘闭环（2 个） ----------

  register({
    name: 'odoo_applicants',
    description: '查询应聘者列表（hr.applicant）。用于"看招聘 pipeline"、"某岗位的候选人"、"等待面试的"。可按 job_id/stage_id 筛选；keyword 模糊匹配姓名/邮箱。',
    schema: {
      type: 'object',
      properties: {
        job_id:        { type: 'number', description: '招聘岗位 id（hr.job）' },
        stage_id:      { type: 'number', description: '招聘阶段 id（hr.recruitment.stage）' },
        keyword:       { type: 'string', description: '姓名/邮箱模糊搜索' },
        only_active:   { type: 'boolean', description: '只看活跃，默认 true（false 包括归档）' },
        limit:         { type: 'number', description: '上限，默认30' },
      },
    },
    async handler(p: { job_id?: number; stage_id?: number; keyword?: string; only_active?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const apps = await client.getApplicants(p);
        return { success: true, count: apps.length, applicants: apps.map(a => ({
          id: a['id'], name: a['partner_name'], email: a['email_from'], job: a['job_id'],
          stage: a['stage_id'], kanban: a['kanban_state'], priority: a['priority'],
          recruiter: a['user_id'], date_open: a['date_open'],
          last_stage_update: a['date_last_stage_update'],
          salary_expected: a['salary_expected'], salary_proposed: a['salary_proposed'],
          availability: a['availability'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_applicant_move_stage',
    description: '移动应聘者的招聘阶段或更改 kanban 状态（hr.applicant.write）。用于"把张三推进到面试阶段"、"标记候选人 #88 为 done"、"拒绝应聘者并填理由"。先用 odoo_search(model="hr.recruitment.stage") 查阶段 id；用 odoo_search(model="hr.applicant.refuse.reason") 查拒绝理由 id。',
    schema: {
      type: 'object',
      properties: {
        applicant_id:     { type: 'number', description: '应聘者 id（必填）' },
        stage_id:         { type: 'number', description: '目标阶段 id' },
        kanban_state:     { type: 'string', enum: ['normal','done','blocked'], description: 'Kanban 状态：normal=进行中 / done=可推进 / blocked=阻塞' },
        refuse_reason_id: { type: 'number', description: '拒绝理由 id（设置该字段意味着拒绝候选人）' },
      },
      required: ['applicant_id'],
    },
    async handler(p: { applicant_id: number; stage_id?: number; kanban_state?: 'normal' | 'done' | 'blocked'; refuse_reason_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.moveApplicantStage(p.applicant_id, {
          stage_id: p.stage_id, kanban_state: p.kanban_state, refuse_reason_id: p.refuse_reason_id,
        });
        const parts: string[] = [];
        if (p.stage_id) parts.push(`阶段→#${p.stage_id}`);
        if (p.kanban_state) parts.push(`状态→${p.kanban_state}`);
        if (p.refuse_reason_id) parts.push(`拒绝（理由 #${p.refuse_reason_id}）`);
        return { success: true, message: `候选人 #${p.applicant_id} 已更新：${parts.join('；') || '无变化'}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 考核 / 工资 / 排班（3 个） ----------

  register({
    name: 'odoo_appraisals',
    description: '查询员工考核列表（hr.appraisal）。state: 1_new=待启动 / 2_pending=进行中 / 3_done=完成。only_mine=true 时只看我作为 reviewer 的考核。',
    schema: {
      type: 'object',
      properties: {
        employee_id: { type: 'number', description: '被考核员工 id' },
        state:       { type: 'string', enum: ['1_new','2_pending','3_done'], description: '状态筛选' },
        only_mine:   { type: 'boolean', description: 'true=只看我作为 reviewer 的' },
        limit:       { type: 'number', description: '上限，默认20' },
      },
    },
    async handler(p: { employee_id?: number; state?: '1_new'|'2_pending'|'3_done'; only_mine?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const apps = await client.getAppraisals(p);
        return { success: true, count: apps.length, appraisals: apps.map(a => ({
          id: a['id'], employee: a['employee_id'], department: a['department_id'], job: a['job_id'],
          managers: a['manager_ids'], date_close: a['date_close'], state: a['state'],
          next_date: a['next_appraisal_date'], waiting_feedback: a['waiting_feedback'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_payslips',
    description: '查询工资单列表（hr.payslip）。需要 hr_payroll.group_hr_payroll_user 权限。state: draft/verify/done/paid/cancel。不填 employee_id 默认查当前用户。',
    schema: {
      type: 'object',
      properties: {
        employee_id:     { type: 'number', description: '员工 id，不填默认查当前用户' },
        state:           { type: 'string', enum: ['draft','verify','done','paid','cancel'], description: '状态筛选' },
        payslip_run_id:  { type: 'number', description: '所属批次 id（hr.payslip.run）' },
        limit:           { type: 'number', description: '上限，默认20' },
      },
    },
    async handler(p: { employee_id?: number; state?: 'draft'|'verify'|'done'|'paid'|'cancel'; payslip_run_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const slips = await client.getPayslips(p);
        return { success: true, count: slips.length, payslips: slips.map(s => ({
          id: s['id'], name: s['name'], employee: s['employee_id'],
          period_from: s['date_from'], period_to: s['date_to'], state: s['state'],
          basic: s['basic_wage'], gross: s['gross_wage'], net: s['net_wage'],
          currency: s['currency_id'], run: s['payslip_run_id'], paid: s['paid'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_planning_shifts',
    description: '查询排班 / 班次（planning.slot）。用于"我这周的班"、"客服团队这周排班"。date_from/to 默认今天到 7 天后。',
    schema: {
      type: 'object',
      properties: {
        employee_id:     { type: 'number', description: '员工 id 筛选' },
        department_id:   { type: 'number', description: '部门 id 筛选' },
        date_from:       { type: 'string', description: '起始日 YYYY-MM-DD，默认今天' },
        date_to:         { type: 'string', description: '结束日 YYYY-MM-DD，默认 7 天后' },
        only_published:  { type: 'boolean', description: '只看已发布的班次' },
        limit:           { type: 'number', description: '上限，默认50' },
      },
    },
    async handler(p: { employee_id?: number; department_id?: number; date_from?: string; date_to?: string; only_published?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const shifts = await client.getPlanningShifts(p);
        return { success: true, count: shifts.length, shifts: shifts.map(s => ({
          id: s['id'], employee: s['employee_id'], role: s['role_id'], department: s['department_id'],
          start: s['start_datetime'], end: s['end_datetime'], hours: s['allocated_hours'],
          state: s['state'], note: s['name'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // HR 行动力补完（v1.12 新增 14 个）
  //   工资单 3 + 考核 1 + 招聘 3 + 排班 2 + 技能 3 + 远程 1 + 车队 1
  // ══════════════════════════════════════════════════════

  // ---------- 工资单生命周期（3 个） ----------

  register({
    name: 'odoo_payslip_validate',
    description: '【HR/财务】验证工资单（hr.payslip.action_payslip_done），状态从 draft → done。需要 hr_payroll.group_hr_payroll_user 权限。批量传 ids。',
    schema: {
      type: 'object',
      properties: { payslip_ids: { type: 'array', items: { type: 'number' }, description: '工资单 id 数组（必填）' } },
      required: ['payslip_ids'],
    },
    async handler(p: { payslip_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.validatePayslip(p.payslip_ids);
        return { success: true, message: `工资单 ${p.payslip_ids.map(i => '#'+i).join(', ')} 已验证（draft → done）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_payslip_paid',
    description: '【HR/财务】标记工资单已支付（hr.payslip.action_payslip_paid），状态从 done → paid。需要 hr_payroll.group_hr_payroll_user 权限。',
    schema: {
      type: 'object',
      properties: { payslip_ids: { type: 'array', items: { type: 'number' }, description: '工资单 id 数组（必填）' } },
      required: ['payslip_ids'],
    },
    async handler(p: { payslip_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.markPayslipPaid(p.payslip_ids);
        return { success: true, message: `工资单 ${p.payslip_ids.map(i => '#'+i).join(', ')} 已标记为已支付。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_payslip_cancel',
    description: '【HR】取消工资单（hr.payslip.action_payslip_cancel），任何状态 → cancel。',
    schema: {
      type: 'object',
      properties: { payslip_ids: { type: 'array', items: { type: 'number' }, description: '工资单 id 数组（必填）' } },
      required: ['payslip_ids'],
    },
    async handler(p: { payslip_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.cancelPayslip(p.payslip_ids);
        return { success: true, message: `工资单 ${p.payslip_ids.map(i => '#'+i).join(', ')} 已取消。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 考核闭环（1 个） ----------

  register({
    name: 'odoo_appraisal_action',
    description: '推进绩效考核状态（hr.appraisal）。action="confirm" 启动（1_new→2_pending）；"done" 完成（2_pending→3_done）；"back" 退回草稿。',
    schema: {
      type: 'object',
      properties: {
        appraisal_id: { type: 'number', description: '考核 id（必填）' },
        action:       { type: 'string', enum: ['confirm', 'done', 'back'], description: '动作（必填）' },
      },
      required: ['appraisal_id', 'action'],
    },
    async handler(p: { appraisal_id: number; action: 'confirm' | 'done' | 'back' }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.appraisalAction(p.appraisal_id, p.action);
        const labelMap = { confirm: '已启动', done: '已完成', back: '已退回草稿' };
        return { success: true, message: `考核 #${p.appraisal_id} ${labelMap[p.action]}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 招聘助手（3 个） ----------

  register({
    name: 'odoo_recruitment_stages',
    description: '查询招聘阶段列表（hr.recruitment.stage）。给 odoo_applicant_move_stage 提供 stage_id。可按 job_id 筛选只属于某岗位的阶段。',
    schema: {
      type: 'object',
      properties: { job_id: { type: 'number', description: '岗位 id 筛选（可选）' } },
    },
    async handler(p: { job_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const stages = await client.getRecruitmentStages(p.job_id);
        return { success: true, count: stages.length, stages: stages.map(s => ({
          id: s['id'], name: s['name'], sequence: s['sequence'],
          hired_stage: s['hired_stage'], fold: s['fold'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_recruitment_refuse_reasons',
    description: '查询拒绝候选人的理由列表（hr.applicant.refuse.reason）。给 odoo_applicant_move_stage 的 refuse_reason_id 提供选项。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const reasons = await client.getApplicantRefuseReasons();
        return { success: true, count: reasons.length, refuse_reasons: reasons.map(r => ({ id: r['id'], name: r['name'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_recruitment_create_meeting',
    description: '为应聘者创建面试日历事件（calendar.event + applicant_id）。会自动把应聘者的 partner 和招聘官 partner 加为参会人；如果应聘者还没 partner_id 会自动建一个。start 是 YYYY-MM-DD HH:MM:SS，duration 单位为小时（默认 1）。',
    schema: {
      type: 'object',
      properties: {
        applicant_id: { type: 'number', description: '应聘者 id（必填）' },
        name:         { type: 'string', description: '会议标题，如"华为 ERP 项目岗位 - 一面"（必填）' },
        start:        { type: 'string', description: '开始时间 YYYY-MM-DD HH:MM:SS（必填，UTC 或本地，按 Odoo 时区设置）' },
        duration:     { type: 'number', description: '时长（小时），默认 1' },
        description:  { type: 'string', description: '会议说明' },
      },
      required: ['applicant_id', 'name', 'start'],
    },
    async handler(p: { applicant_id: number; name: string; start: string; duration?: number; description?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createApplicantMeeting(p.applicant_id, {
          name: p.name, start: p.start, duration: p.duration, description: p.description,
        });
        return { success: true, id, message: `面试事件 #${id} 已为候选人 #${p.applicant_id} 创建（${p.start}，${p.duration ?? 1}h）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 排班发布 / 取消发布（2 个） ----------

  register({
    name: 'odoo_planning_publish',
    description: '发布排班 / 班次（planning.slot）。notify=true（默认）会逐条调 action_send 自动给员工发邮件并置为 published；notify=false 则只 write state="published" 不发通知。',
    schema: {
      type: 'object',
      properties: {
        shift_ids: { type: 'array', items: { type: 'number' }, description: '排班 id 数组（必填）' },
        notify:    { type: 'boolean', description: '是否邮件通知员工，默认 true' },
      },
      required: ['shift_ids'],
    },
    async handler(p: { shift_ids: number[]; notify?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.publishPlanningShift(p.shift_ids, p.notify !== false);
        const tag = p.notify !== false ? '已发布并通知员工' : '已发布（未发通知）';
        return { success: true, message: `排班 ${p.shift_ids.map(i => '#'+i).join(', ')} ${tag}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_planning_unpublish',
    description: '【planning manager】取消发布排班，published → draft（planning.slot.action_unpublish）。需要 planning.group_planning_manager 权限。',
    schema: {
      type: 'object',
      properties: { shift_ids: { type: 'array', items: { type: 'number' }, description: '排班 id 数组（必填）' } },
      required: ['shift_ids'],
    },
    async handler(p: { shift_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.unpublishPlanningShift(p.shift_ids);
        return { success: true, message: `排班 ${p.shift_ids.map(i => '#'+i).join(', ')} 已取消发布（回到 draft）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 技能管理（3 个） ----------

  register({
    name: 'odoo_employee_skills',
    description: '查询员工技能列表（hr.employee.skill）。不填 employee_id 默认查当前用户；可按 skill_type_id 筛某类技能（如"编程语言"、"语言"）。',
    schema: {
      type: 'object',
      properties: {
        employee_id:   { type: 'number', description: '员工 id，不填默认当前用户' },
        skill_type_id: { type: 'number', description: '技能类型 id 筛选' },
        limit:         { type: 'number', description: '上限，默认50' },
      },
    },
    async handler(p: { employee_id?: number; skill_type_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const skills = await client.getEmployeeSkills(p);
        return { success: true, count: skills.length, employee_skills: skills.map(s => ({
          id: s['id'], employee: s['employee_id'], skill: s['skill_id'],
          skill_type: s['skill_type_id'], level: s['skill_level_id'], progress: s['level_progress'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_employee_skill_add',
    description: '给员工添加一项技能（hr.employee.skill）。需要 hr.group_hr_user 权限（员工自己也可以加自己的）。先用 odoo_skills_catalog 查 skill_type_id / skill_id / skill_level_id。',
    schema: {
      type: 'object',
      properties: {
        employee_id:    { type: 'number', description: '员工 id（必填）' },
        skill_type_id:  { type: 'number', description: '技能类型 id（必填，如"编程语言"）' },
        skill_id:       { type: 'number', description: '技能 id（必填，如"Python"）' },
        skill_level_id: { type: 'number', description: '技能等级 id（必填，如"高级"）' },
      },
      required: ['employee_id', 'skill_type_id', 'skill_id', 'skill_level_id'],
    },
    async handler(p: { employee_id: number; skill_type_id: number; skill_id: number; skill_level_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.addEmployeeSkill(p);
        return { success: true, id, message: `已为员工 #${p.employee_id} 添加技能 #${p.skill_id}（等级 #${p.skill_level_id}），记录 #${id}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_skills_catalog',
    description: '查询技能目录（hr.skill / hr.skill.type / hr.skill.level）。一次返回三类 master data 给上层调用方（odoo_employee_skill_add）拼参数用。可按 skill_type_id / keyword 筛选。',
    schema: {
      type: 'object',
      properties: {
        skill_type_id: { type: 'number', description: '只看某类技能下的 skill 和 level' },
        keyword:       { type: 'string', description: '技能名模糊搜索' },
        limit:         { type: 'number', description: 'skills 列表上限，默认50' },
      },
    },
    async handler(p: { skill_type_id?: number; keyword?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const cat = await client.getSkillsCatalog(p);
        return {
          success: true,
          skill_types: cat.skill_types.map(t => ({ id: t['id'], name: t['name'] })),
          skills: cat.skills.map(s => ({ id: s['id'], name: s['name'], type: s['skill_type_id'] })),
          skill_levels: cat.skill_levels.map(l => ({ id: l['id'], name: l['name'], progress: l['level_progress'], type: l['skill_type_id'] })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 远程办公（1 个） ----------

  register({
    name: 'odoo_homeworking_set',
    description: '设置员工某天的工作地点（hr.employee.location，hr_homeworking 模块）。用于"明天我远程"、"周一到周三在家办公"。同一员工同一天唯一约束，已有则覆盖。先用 odoo_search(model="hr.work.location") 查可选地点 id。',
    schema: {
      type: 'object',
      properties: {
        date:             { type: 'string', description: '日期 YYYY-MM-DD（必填）' },
        work_location_id: { type: 'number', description: 'hr.work.location id（必填，如"家"、"上海办公室"）' },
        employee_id:      { type: 'number', description: '员工 id，不填默认当前用户' },
      },
      required: ['date', 'work_location_id'],
    },
    async handler(p: { date: string; work_location_id: number; employee_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.setHomeworking(p);
        return { success: true, id, message: `已设置 ${p.date} 的工作地点为 location #${p.work_location_id}（hr.employee.location #${id}）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 车队（1 个） ----------

  register({
    name: 'odoo_fleet_vehicles',
    description: '查询公司车辆（fleet.vehicle）。用于"我有哪辆车"、"销售部的车"、"X 公司车队"。driver_user_id 按司机 res.users id 筛选；keyword 匹配车名/车牌。',
    schema: {
      type: 'object',
      properties: {
        driver_user_id: { type: 'number', description: '司机 res.users id 筛选' },
        keyword:        { type: 'string', description: '车辆名 / 车牌模糊搜索' },
        only_active:    { type: 'boolean', description: '只看活跃，默认 true' },
        limit:          { type: 'number', description: '上限，默认30' },
      },
    },
    async handler(p: { driver_user_id?: number; keyword?: string; only_active?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const vehicles = await client.getFleetVehicles(p);
        return { success: true, count: vehicles.length, vehicles: vehicles.map(v => ({
          id: v['id'], name: v['name'], plate: v['license_plate'], model: v['model_id'],
          driver: v['driver_id'], acquired: v['acquisition_date'],
          odometer: v['odometer'], odometer_unit: v['odometer_unit'],
          state: v['state_id'], company: v['company_id'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // HR 全生命周期治理（v1.13 新增 14 个）
  //   员工 CRUD 4 + 仪表盘 1 + 部门/岗位/地点 5 + 合同版本 1 + 工时洞察 2 + 组织架构 1
  // ══════════════════════════════════════════════════════

  // ---------- 员工 CRUD（4 个） ----------

  register({
    name: 'odoo_employee_create',
    description: '【HR】创建员工（hr.employee）。用于"入职新员工"、"录入张三"。需要 hr.group_hr_user 权限。Odoo 会按 name 自动建 resource.resource。建议同步填 work_email、department_id、job_id。',
    schema: {
      type: 'object',
      properties: {
        name:             { type: 'string', description: '员工姓名（必填）' },
        work_email:       { type: 'string', description: '工作邮箱' },
        work_phone:       { type: 'string', description: '工作座机' },
        mobile_phone:     { type: 'string', description: '工作手机' },
        job_title:        { type: 'string', description: '职位名称（自由文本）' },
        department_id:    { type: 'number', description: 'hr.department id' },
        job_id:           { type: 'number', description: 'hr.job id（招聘岗位）' },
        parent_id:        { type: 'number', description: '上级 hr.employee id' },
        coach_id:         { type: 'number', description: '导师 hr.employee id' },
        user_id:          { type: 'number', description: '关联的 res.users id（系统账号）' },
        work_location_id: { type: 'number', description: 'hr.work.location id' },
        company_id:       { type: 'number', description: '公司 id' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; work_email?: string; work_phone?: string; mobile_phone?: string; job_title?: string; department_id?: number; job_id?: number; parent_id?: number; coach_id?: number; user_id?: number; work_location_id?: number; company_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createEmployee(p);
        return { success: true, id, message: `员工 #${id}（${p.name}）已创建。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_employee_update',
    description: '【HR】修改员工资料（hr.employee.write）。用于"改张三的部门"、"换上级"、"加手机号"等。多字段一次更新。',
    schema: {
      type: 'object',
      properties: {
        employee_id:      { type: 'number', description: '员工 id（必填）' },
        name:             { type: 'string' },
        work_email:       { type: 'string' },
        work_phone:       { type: 'string' },
        mobile_phone:     { type: 'string' },
        job_title:        { type: 'string' },
        department_id:    { type: 'number' },
        job_id:           { type: 'number' },
        parent_id:        { type: 'number' },
        coach_id:         { type: 'number' },
        user_id:          { type: 'number' },
        work_location_id: { type: 'number' },
      },
      required: ['employee_id'],
    },
    async handler(p: { employee_id: number; [k: string]: unknown }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const { employee_id, ...rest } = p;
        if (Object.keys(rest).length === 0) return { success: false, message: '没有要更新的字段' };
        await client.updateEmployee(employee_id, rest);
        return { success: true, message: `员工 #${employee_id} 已更新（${Object.keys(rest).join(', ')}）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_employee_archive',
    description: '【HR】归档员工（active=false），用于"离职"、"停用 X 的账号"。员工不会被删除，可通过 odoo_employee_unarchive 恢复。',
    schema: {
      type: 'object',
      properties: { employee_id: { type: 'number', description: '员工 id（必填）' } },
      required: ['employee_id'],
    },
    async handler(p: { employee_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.archiveEmployee(p.employee_id);
        return { success: true, message: `员工 #${p.employee_id} 已归档（离职）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_employee_unarchive',
    description: '【HR】恢复已归档员工（active=true），用于"返聘"、"重新启用账号"。',
    schema: {
      type: 'object',
      properties: { employee_id: { type: 'number', description: '员工 id（必填）' } },
      required: ['employee_id'],
    },
    async handler(p: { employee_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.unarchiveEmployee(p.employee_id);
        return { success: true, message: `员工 #${p.employee_id} 已恢复（active=true）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- HR 仪表盘（1 个） ----------

  register({
    name: 'odoo_hr_dashboard',
    description: '【HR/管理】一句话拿到 HR 全局仪表盘：在编人数 + 部门人数分布 + 今日生日 + 今日请假人 + 待审请假/报销数 + 招聘漏斗 + 在招岗位数。read_group 聚合，单次调用全图。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const dash = await client.getHrDashboard();
        return { success: true, ...dash };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 部门 / 岗位 / 工作地点（5 个） ----------

  register({
    name: 'odoo_departments',
    description: '查询部门列表（hr.department）。complete_name 字段含完整层级（如"销售/华北销售/北京组"）。可按父部门 / keyword 筛。',
    schema: {
      type: 'object',
      properties: {
        keyword:   { type: 'string', description: '部门名模糊搜索' },
        parent_id: { type: 'number', description: '父部门 id（传 0 表示顶级部门）' },
        limit:     { type: 'number', description: '上限，默认100' },
      },
    },
    async handler(p: { keyword?: string; parent_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const depts = await client.getDepartments(p);
        return { success: true, count: depts.length, departments: depts.map(d => ({
          id: d['id'], name: d['name'], full_path: d['complete_name'],
          parent: d['parent_id'], manager: d['manager_id'],
          member_count: Array.isArray(d['member_ids']) ? d['member_ids'].length : 0,
          company: d['company_id'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_department_create',
    description: '【HR】创建部门（hr.department）。parent_id 不填则为顶级；manager_id 是部门经理 hr.employee.id。',
    schema: {
      type: 'object',
      properties: {
        name:       { type: 'string', description: '部门名（必填）' },
        parent_id:  { type: 'number', description: '上级部门 id' },
        manager_id: { type: 'number', description: '部门经理 hr.employee id' },
        company_id: { type: 'number', description: '公司 id' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; parent_id?: number; manager_id?: number; company_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createDepartment(p);
        return { success: true, id, message: `部门 #${id}（${p.name}）已创建。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_jobs',
    description: '查询岗位列表（hr.job）。可按部门筛。expected_employees 是该岗位的预期 / 已招人数。',
    schema: {
      type: 'object',
      properties: {
        department_id: { type: 'number', description: '部门 id 筛选' },
        only_active:   { type: 'boolean', description: '只看活跃，默认 true' },
        limit:         { type: 'number', description: '上限，默认100' },
      },
    },
    async handler(p: { department_id?: number; only_active?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const jobs = await client.getJobs(p);
        return { success: true, count: jobs.length, jobs: jobs.map(j => ({
          id: j['id'], name: j['name'], department: j['department_id'],
          expected: j['expected_employees'], company: j['company_id'], sequence: j['sequence'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_job_create',
    description: '【HR】创建岗位（hr.job）。用于"新开个销售经理岗位"。department_id 选填。',
    schema: {
      type: 'object',
      properties: {
        name:          { type: 'string', description: '岗位名（必填）' },
        department_id: { type: 'number', description: '所属部门 id' },
        sequence:      { type: 'number', description: '排序，默认 10' },
        company_id:    { type: 'number', description: '公司 id' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; department_id?: number; sequence?: number; company_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createJob(p);
        return { success: true, id, message: `岗位 #${id}（${p.name}）已创建。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_work_locations',
    description: '查询工作地点列表（hr.work.location）。给 odoo_homeworking_set 提供 work_location_id；location_type 可筛 home/office/other。',
    schema: {
      type: 'object',
      properties: {
        keyword:       { type: 'string', description: '地点名模糊搜索' },
        location_type: { type: 'string', enum: ['home', 'office', 'other'], description: '类型筛选' },
        limit:         { type: 'number', description: '上限，默认50' },
      },
    },
    async handler(p: { keyword?: string; location_type?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const locs = await client.getWorkLocations(p);
        return { success: true, count: locs.length, work_locations: locs.map(l => ({
          id: l['id'], name: l['name'], type: l['location_type'],
          address: l['address_id'], company: l['company_id'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 合同 / 版本（1 个） ----------

  register({
    name: 'odoo_employee_versions',
    description: '查询员工的版本历史（hr.version）。Odoo 19+ 把"合同"重组成员工的多个版本：每次升职/调薪/换部门都会留一条版本记录。wage/date_start/date_end 字段需要 hr_manager 权限才能读，无权时退化只显示基本字段。',
    schema: {
      type: 'object',
      properties: {
        employee_id: { type: 'number', description: '员工 id（必填）' },
        limit:       { type: 'number', description: '上限，默认30（按 date_version desc）' },
      },
      required: ['employee_id'],
    },
    async handler(p: { employee_id: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const versions = await client.getEmployeeVersions(p.employee_id, { limit: p.limit });
        return { success: true, count: versions.length, versions: versions.map(v => ({
          id: v['id'], name: v['name'], employee: v['employee_id'],
          date_version: v['date_version'], department: v['department_id'], job: v['job_id'],
          contract_type: v['contract_type_id'], wage: v['wage'],
          company: v['company_id'], active: v['active'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 工时洞察（2 个） ----------

  register({
    name: 'odoo_timesheet_summary',
    description: '本月工时按项目/任务/员工聚合（account.analytic.line + read_group）。默认查当前用户本月按项目分组。group_by 可选 project/task/employee。',
    schema: {
      type: 'object',
      properties: {
        employee_id: { type: 'number', description: '员工 id，不填默认当前用户' },
        date_from:   { type: 'string', description: '起始日 YYYY-MM-DD，默认本月初' },
        date_to:     { type: 'string', description: '结束日 YYYY-MM-DD，默认今天' },
        group_by:    { type: 'string', enum: ['project','task','employee'], description: '聚合维度，默认 project' },
      },
    },
    async handler(p: { employee_id?: number; date_from?: string; date_to?: string; group_by?: 'project'|'task'|'employee' }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const summary = await client.getTimesheetSummary(p);
        return { success: true, ...summary };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_timesheet_team',
    description: '【经理视角】查我的下属本月工时（按 hr.employee.parent_id = 我对应 employee_id 找直接下属，再聚合 account.analytic.line）。manager_id 不填默认当前用户对应的员工。',
    schema: {
      type: 'object',
      properties: {
        manager_id: { type: 'number', description: '经理 hr.employee id，不填默认当前用户' },
        date_from:  { type: 'string', description: '起始日 YYYY-MM-DD，默认本月初' },
        date_to:    { type: 'string', description: '结束日 YYYY-MM-DD，默认今天' },
        limit:      { type: 'number', description: '上限，默认100' },
      },
    },
    async handler(p: { manager_id?: number; date_from?: string; date_to?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const team = await client.getTeamTimesheets(p);
        const totalHours = team.reduce((s, r) => s + Number(r['hours'] ?? 0), 0);
        return { success: true, count: team.length, total_hours: totalHours, team };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 组织架构（1 个） ----------

  register({
    name: 'odoo_employee_org_chart',
    description: '查员工的组织架构上下文：经理 + 导师 + 直接下属列表 + 跨级下属总数。用于"看看张三上面是谁"、"我下面有几个人"。',
    schema: {
      type: 'object',
      properties: { employee_id: { type: 'number', description: '员工 id（必填）' } },
      required: ['employee_id'],
    },
    async handler(p: { employee_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const chart = await client.getEmployeeOrgChart(p.employee_id);
        return { success: true, ...chart };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // Analytics & Orchestration（v1.14 新增 14 个）
  //   HR Analytics 3 + 入离职编排 2 + 工时审批 2 + 跨域仪表盘 4 +
  //   项目分析 2 + 薪酬批次 1
  // ══════════════════════════════════════════════════════

  // ---------- HR Analytics 进阶（3 个） ----------

  register({
    name: 'odoo_attendance_analytics',
    description: '考勤分析（hr.attendance + read_group）。本月或指定区间内员工总工时分布、记录数、按员工聚合。可按部门或员工筛选。默认本月初到今天。',
    schema: {
      type: 'object',
      properties: {
        employee_id:   { type: 'number', description: '只看某员工' },
        department_id: { type: 'number', description: '按部门筛' },
        date_from:     { type: 'string', description: 'YYYY-MM-DD，默认本月初' },
        date_to:       { type: 'string', description: 'YYYY-MM-DD，默认今天' },
      },
    },
    async handler(p: { employee_id?: number; department_id?: number; date_from?: string; date_to?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getAttendanceAnalytics(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_leave_analytics',
    description: '请假趋势分析（hr.leave + read_group）。区间内按请假类型 + 状态分组，返回总天数。用于"本月谁请假最多"、"全公司请假数据"。',
    schema: {
      type: 'object',
      properties: {
        department_id: { type: 'number', description: '按部门筛' },
        date_from:     { type: 'string', description: 'YYYY-MM-DD，默认本月初' },
        date_to:       { type: 'string', description: 'YYYY-MM-DD，默认今天' },
      },
    },
    async handler(p: { department_id?: number; date_from?: string; date_to?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getLeaveAnalytics(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_turnover_metrics',
    description: '入离职率指标。根据 hr.employee.create_date / archive 状态计算近 N 天入职数、离职数，年化 turnover_rate 和 attrition_rate。默认窗口 90 天。',
    schema: {
      type: 'object',
      properties: { days: { type: 'number', description: '滑动窗口天数，默认90' } },
    },
    async handler(p: { days?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getTurnoverMetrics(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 入离职编排（2 个） ----------

  register({
    name: 'odoo_employee_onboarding',
    description: '【HR】入职编排：链式动作 = 创建员工 + 可选创建系统账号（res.users）+ 可选发送入职欢迎 chatter。比单独 odoo_employee_create 多覆盖账号绑定与欢迎流程。create_user=true 且 user_login 已填时会自动建账号。',
    schema: {
      type: 'object',
      properties: {
        name:             { type: 'string', description: '员工姓名（必填）' },
        work_email:       { type: 'string' },
        work_phone:       { type: 'string' },
        mobile_phone:     { type: 'string' },
        job_title:        { type: 'string' },
        department_id:    { type: 'number' },
        job_id:           { type: 'number' },
        parent_id:        { type: 'number', description: '上级 hr.employee id' },
        user_id:          { type: 'number', description: '已有的 res.users id（如已建过账号）' },
        work_location_id: { type: 'number' },
        company_id:       { type: 'number' },
        create_user:      { type: 'boolean', description: '是否同时建 res.users，默认 false' },
        user_login:       { type: 'string', description: '若 create_user=true 必填，新账号登录名' },
        welcome_message:  { type: 'string', description: '可选，入职欢迎语，会发到员工的 chatter' },
      },
      required: ['name'],
    },
    async handler(p: { name: string; [k: string]: unknown }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.employeeOnboarding(p as Parameters<typeof client.employeeOnboarding>[0]);
        return { success: true, ...result, message: `员工 #${result.employee_id}（${p.name}）入职已完成。${result.actions.join('；')}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_employee_offboarding',
    description: '【HR】离职编排：链式动作 = （可选）转移直接下属给 new_manager_id +（可选）拒掉所有未批的请假 +（可选）chatter 留言 + archive 员工。new_manager_id 不填则不转移。',
    schema: {
      type: 'object',
      properties: {
        employee_id:           { type: 'number', description: '离职员工 id（必填）' },
        new_manager_id:        { type: 'number', description: '把直接下属转给的新经理 hr.employee id' },
        leaving_message:       { type: 'string', description: 'chatter 留言（如"X 离职日期 YYYY-MM-DD，工作交接联系 ...）"' },
        refuse_pending_leaves: { type: 'boolean', description: '是否自动拒绝未批请假，默认 false' },
      },
      required: ['employee_id'],
    },
    async handler(p: { employee_id: number; new_manager_id?: number; leaving_message?: string; refuse_pending_leaves?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.employeeOffboarding(p);
        return { success: true, ...result, message: `员工 #${p.employee_id} 离职流程完成：${result.actions.join('；')}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 工时审批闭环（2 个） ----------

  register({
    name: 'odoo_timesheet_validate',
    description: '【经理 / timesheet_grid 模块】验证工时（account.analytic.line.action_validate_timesheet）。工时一旦 validated=true 后员工不能再改。要求 timesheet_grid 企业模块已安装。',
    schema: {
      type: 'object',
      properties: { line_ids: { type: 'array', items: { type: 'number' }, description: '工时行 id 数组（必填）' } },
      required: ['line_ids'],
    },
    async handler(p: { line_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.validateTimesheets(p.line_ids);
        return { success: true, message: `工时 ${p.line_ids.map(i => '#'+i).join(', ')} 已验证。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_timesheet_invalidate',
    description: '【经理 / timesheet_grid 模块】撤销工时验证（action_invalidate_timesheet）。validated=false 让员工可以重新编辑。',
    schema: {
      type: 'object',
      properties: { line_ids: { type: 'array', items: { type: 'number' }, description: '工时行 id 数组（必填）' } },
      required: ['line_ids'],
    },
    async handler(p: { line_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.invalidateTimesheets(p.line_ids);
        return { success: true, message: `工时 ${p.line_ids.map(i => '#'+i).join(', ')} 已撤销验证。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 跨域仪表盘（4 个） ----------

  register({
    name: 'odoo_sales_dashboard',
    description: '销售仪表盘（sale.order + read_group）。区间内总销售额、订单数、按状态分布、Top10 客户、待开票数、待发货数。默认本月初到今天。',
    schema: {
      type: 'object',
      properties: {
        date_from: { type: 'string', description: 'YYYY-MM-DD，默认本月初' },
        date_to:   { type: 'string', description: 'YYYY-MM-DD，默认今天' },
      },
    },
    async handler(p: { date_from?: string; date_to?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getSalesDashboard(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_crm_pipeline_health',
    description: 'CRM 漏斗健康（crm.lead + read_group）。返回阶段分布 / 销售员分布 / 平均概率 / 总管道金额 / 逾期商机数与金额。user_id 不填看全员；days_overdue 默认 0（今天前未跟进的算逾期）。',
    schema: {
      type: 'object',
      properties: {
        user_id:      { type: 'number', description: '只看某销售员 res.users id' },
        days_overdue: { type: 'number', description: '逾期容忍天数，默认 0（今天就算）' },
      },
    },
    async handler(p: { user_id?: number; days_overdue?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getCrmPipelineHealth(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_invoice_aging',
    description: '应收账款账龄分析（account.move）。把未付/部分付的客户发票按 0–30 / 31–60 / 61–90 / 90+ 天逾期分桶 + 未到期。可按客户筛。',
    schema: {
      type: 'object',
      properties: {
        partner_id: { type: 'number', description: '只看某客户 res.partner id' },
        company_id: { type: 'number', description: '公司 id' },
      },
    },
    async handler(p: { partner_id?: number; company_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getInvoiceAging(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_helpdesk_dashboard',
    description: 'Helpdesk 仪表盘（helpdesk.ticket + read_group）。未关闭工单数、按 stage / priority / 处理人分布、SLA 逾期数、紧急（priority=3）开放数。可按 team_id / user_id 筛。',
    schema: {
      type: 'object',
      properties: {
        team_id: { type: 'number', description: '客服团队 id' },
        user_id: { type: 'number', description: '处理人 res.users id' },
      },
    },
    async handler(p: { team_id?: number; user_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getHelpdeskDashboard(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 项目仪表盘 + 我的工作负荷（2 个） ----------

  register({
    name: 'odoo_project_dashboard',
    description: '项目仪表盘（project.project + project.task）。返回项目列表（含任务数）+ 任务总览（开放/完成/逾期）。可按 project_id 单独看一个项目。',
    schema: {
      type: 'object',
      properties: { project_id: { type: 'number', description: '只看某项目' } },
    },
    async handler(p: { project_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getProjectDashboard(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_my_workload',
    description: '我的工作负荷一览：当前 user 的开放任务数 / 逾期任务 / 待办活动 / 工单 / 待审批 / 今日日历。一句话回答"我手上还有多少活"。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getMyWorkload();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 薪酬批次（1 个） ----------

  register({
    name: 'odoo_payslip_run_create',
    description: '【HR】创建工资单批次（hr.payslip.run），可选 auto_generate=true 同时调 generate_payslips 批量生成 hr.payslip。需要 hr_payroll.group_hr_payroll_user 权限。',
    schema: {
      type: 'object',
      properties: {
        name:          { type: 'string', description: '批次名，如"2026 年 4 月工资"（必填）' },
        date_start:    { type: 'string', description: 'YYYY-MM-DD（必填）' },
        date_end:      { type: 'string', description: 'YYYY-MM-DD（必填）' },
        company_id:    { type: 'number' },
        employee_ids:  { type: 'array', items: { type: 'number' }, description: '员工 id 列表，配合 auto_generate' },
        auto_generate: { type: 'boolean', description: '是否立即生成 payslip 行，默认 false' },
      },
      required: ['name', 'date_start', 'date_end'],
    },
    async handler(p: { name: string; date_start: string; date_end: string; company_id?: number; employee_ids?: number[]; auto_generate?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.createPayslipRun(p);
        return { success: true, ...result, message: `批次 #${result.run_id} 创建完成（${result.payslip_count} 条 payslip）：${result.actions.join('；')}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 个人视图 + 跨域桥 + 库存深化 + 多公司 + 销售预测（v1.15 新增 14 个）
  //   个人视图 3 + CRM 智能 2 + 跨域桥 3 + 库存深化 4 + 多公司 1 + 预测 1
  // ══════════════════════════════════════════════════════

  // ---------- 个人视图（3 个） ----------

  register({
    name: 'odoo_my_overdues',
    description: '我的所有逾期项一览（任务 + 活动 + 工单 + 客户发票，4 域 Promise.all 并发）。一句话回答"我手上有什么逾期了"。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getMyOverdues();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_my_today',
    description: '我今天所有要做的事（今日截止任务 + 今日活动 + 今日日历 + 今日到期发票）。一句话回答"我今天要做什么"。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getMyToday();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_my_unread',
    description: '我所有未读消息（mail.notification + is_read=false + inbox 类型 + 我的 partner）。返回原始消息 + body 预览（去 HTML 截断 200 字）。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getMyUnread();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- CRM 智能助手（2 个） ----------

  register({
    name: 'odoo_crm_stale_leads',
    description: '查"长时间没动"的商机（probability < 100 且 date_last_stage_update < 今天-N 天）。默认阈值 14 天。可按销售员筛。',
    schema: {
      type: 'object',
      properties: {
        user_id:          { type: 'number', description: '只看某销售员' },
        days_no_activity: { type: 'number', description: '没动天数阈值，默认 14' },
        limit:            { type: 'number', description: '上限，默认 30' },
      },
    },
    async handler(p: { user_id?: number; days_no_activity?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getCrmStaleLeads(p);
        return { success: true, count: data.stale_leads.length, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_crm_next_action',
    description: '【智能助手】对单个商机给出"下一步该做什么"的建议。基于 stage 停留天数 + 是否有待办活动 + probability 三个维度做规则推荐，返回 recommendation + suggested_actions（具体调哪个工具）。',
    schema: {
      type: 'object',
      properties: { lead_id: { type: 'number', description: '商机 id（必填）' } },
      required: ['lead_id'],
    },
    async handler(p: { lead_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getCrmNextAction(p.lead_id);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 跨模块桥（3 个） ----------

  register({
    name: 'odoo_helpdesk_to_task',
    description: '把工单转化为项目任务（helpdesk.ticket → project.task）。会复制 name/description/partner_id/user_id；可选在工单 chatter 留下任务链接（默认 keep_chatter_link=true）。',
    schema: {
      type: 'object',
      properties: {
        ticket_id:          { type: 'number', description: '工单 id（必填）' },
        project_id:         { type: 'number', description: '目标项目 id（必填）' },
        task_name:          { type: 'string', description: '任务名，不填默认用 [来自工单 #X] + ticket name' },
        user_ids:           { type: 'array', items: { type: 'number' }, description: '任务经办人，不填用工单的 user_id' },
        keep_chatter_link:  { type: 'boolean', description: '是否在工单 chatter 留任务链接，默认 true' },
      },
      required: ['ticket_id', 'project_id'],
    },
    async handler(p: { ticket_id: number; project_id: number; task_name?: string; user_ids?: number[]; keep_chatter_link?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.helpdeskToTask(p);
        return { success: true, ...result, message: `工单 #${p.ticket_id} 已转任务 #${result.task_id}：${result.actions.join('；')}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_lead_to_project',
    description: '商机赢单后建项目（crm.lead → project.project）。复制 name/description/partner_id/user_id 到项目；可选 mark_won=true 顺手标记商机赢单（先调 action_set_won_rainbowman，失败兜底 write probability=100）。会在商机 chatter 留项目链接。',
    schema: {
      type: 'object',
      properties: {
        lead_id:      { type: 'number', description: '商机 id（必填）' },
        project_name: { type: 'string', description: '项目名，不填用商机 name' },
        partner_id:   { type: 'number', description: '客户 id，不填用商机 partner' },
        user_id:      { type: 'number', description: '项目经理，不填用商机 user_id' },
        mark_won:     { type: 'boolean', description: '是否同时标记商机赢单，默认 false' },
      },
      required: ['lead_id'],
    },
    async handler(p: { lead_id: number; project_name?: string; partner_id?: number; user_id?: number; mark_won?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.leadToProject(p);
        return { success: true, ...result, message: `商机 #${p.lead_id} 已转项目 #${result.project_id}：${result.actions.join('；')}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_invoice_send_reminder',
    description: '发送催款提醒（在 account.move chatter 写一条 partner 可见的消息）。默认正文自动包含发票号 + 逾期天数 + 未付金额；可用 custom_message 覆写。',
    schema: {
      type: 'object',
      properties: {
        invoice_id:     { type: 'number', description: '发票 id（必填）' },
        custom_message: { type: 'string', description: '自定义催款语，不填用默认模板' },
      },
      required: ['invoice_id'],
    },
    async handler(p: { invoice_id: number; custom_message?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.sendInvoiceReminder(p);
        return { success: true, ...result, message: result.actions.join('；') };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 库存深化（4 个） ----------

  register({
    name: 'odoo_stock_low_alerts',
    description: '查触发再订货预警的产品（stock.warehouse.orderpoint where qty_to_order > 0）。返回每条 orderpoint：产品 / 仓库 / min/max 库存 / 建议订货量。',
    schema: {
      type: 'object',
      properties: {
        warehouse_id: { type: 'number', description: '仓库 id 筛选' },
        limit:        { type: 'number', description: '上限，默认 50' },
      },
    },
    async handler(p: { warehouse_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getStockLowAlerts(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_stock_by_location',
    description: '按库位聚合库存（stock.quant + read_group on location_id）。每个库位返回总在手量、保留量、可用量、SKU 数。可按产品 / 库位 / 公司筛。',
    schema: {
      type: 'object',
      properties: {
        location_id: { type: 'number', description: '只看某库位' },
        product_id:  { type: 'number', description: '只看某产品' },
        company_id:  { type: 'number', description: '公司 id' },
      },
    },
    async handler(p: { location_id?: number; product_id?: number; company_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getStockByLocation(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_stock_picking_validate',
    description: '【仓库管理员】验证调拨单 / 出入库单（stock.picking.button_validate）。会按 immediate transfer 流程把状态推到 done。需要权限 stock.group_stock_user。',
    schema: {
      type: 'object',
      properties: { picking_id: { type: 'number', description: 'stock.picking id（必填）' } },
      required: ['picking_id'],
    },
    async handler(p: { picking_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.validatePicking(p.picking_id);
        return { success: true, message: `调拨单 #${p.picking_id} 已验证（按 immediate transfer 流程完成）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_warehouse_dashboard',
    description: '仓库仪表盘：仓库列表 + 待入库/待出库/待内部调拨/回单数。可按 warehouse_id 筛单一仓库。',
    schema: {
      type: 'object',
      properties: { warehouse_id: { type: 'number', description: '仓库 id 筛选' } },
    },
    async handler(p: { warehouse_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getWarehouseDashboard(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 多公司（1 个） ----------

  register({
    name: 'odoo_companies',
    description: '列我可访问的公司（res.company），含当前激活公司 + allowed_company_ids。用于"公司列表"、"我属于几家公司"、"切公司前先看有哪些"。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getCompanies();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 加权销售预测（1 个） ----------

  register({
    name: 'odoo_sales_forecast',
    description: '加权销售预测（crm.lead × probability + sale.order 已确认）。返回 weighted_pipeline = Σ(expected_revenue × probability/100)、原始 raw_pipeline、按 stage / 销售员分布、同窗口 confirmed sale.order 总额。horizon_days 默认 90。',
    schema: {
      type: 'object',
      properties: {
        user_id:      { type: 'number', description: '只看某销售员' },
        horizon_days: { type: 'number', description: '预测窗口天数，默认 90' },
      },
    },
    async handler(p: { user_id?: number; horizon_days?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getSalesForecast(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 业务深化 + 智能洞察 + 报表（v1.16 新增 14 个）
  //   采购 4 + MRP 3 + 会计 3 + 智能洞察 2 + 报表/导出 2
  // ══════════════════════════════════════════════════════

  // ---------- 采购深化 4 ----------

  register({
    name: 'odoo_purchase_create',
    description: '创建采购订单（purchase.order）。order_lines 是 [{product_id, product_qty, price_unit?, name?}, ...]。会自动按 partner_id 默认 vendor 设置 + create order_line 子记录。',
    schema: {
      type: 'object',
      properties: {
        partner_id:    { type: 'number', description: '供应商 res.partner id（必填）' },
        order_lines:   {
          type: 'array',
          description: '订单行数组（必填）',
          items: {
            type: 'object',
            properties: {
              product_id:  { type: 'number' },
              product_qty: { type: 'number' },
              price_unit:  { type: 'number' },
              name:        { type: 'string' },
            },
            required: ['product_id', 'product_qty'],
          },
        },
        date_planned:  { type: 'string', description: '计划交货日 YYYY-MM-DD HH:MM:SS' },
        notes:         { type: 'string' },
        company_id:    { type: 'number' },
      },
      required: ['partner_id', 'order_lines'],
    },
    async handler(p: { partner_id: number; order_lines: Array<{ product_id: number; product_qty: number; price_unit?: number; name?: string }>; date_planned?: string; notes?: string; company_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createPurchaseOrder(p);
        return { success: true, id, message: `采购订单 #${id} 已创建（${p.order_lines.length} 行，state=draft）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_purchase_confirm',
    description: '【采购员】确认采购订单（purchase.order.button_confirm），状态从 draft → purchase（下单）。多 id 优先一次批量调，失败 fallback 逐条 for-loop。',
    schema: {
      type: 'object',
      properties: { order_ids: { type: 'array', items: { type: 'number' }, description: '采购订单 id 数组（必填）' } },
      required: ['order_ids'],
    },
    async handler(p: { order_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.confirmPurchaseOrder(p.order_ids);
        return { success: true, message: `采购订单 ${p.order_ids.map(i => '#'+i).join(', ')} 已确认。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_purchase_dashboard',
    description: '采购仪表盘（purchase.order + read_group）。本月或指定区间总采购额、订单数、按状态分布、Top10 供应商、待收货数、待开账单数。',
    schema: {
      type: 'object',
      properties: {
        date_from: { type: 'string', description: 'YYYY-MM-DD，默认本月初' },
        date_to:   { type: 'string', description: 'YYYY-MM-DD，默认今天' },
      },
    },
    async handler(p: { date_from?: string; date_to?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getPurchaseDashboard(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_vendor_bill_aging',
    description: '应付账款账龄分析（账户 move_type=in_invoice）。0–30 / 31–60 / 61–90 / 90+ / 未到期 五桶。可按供应商筛。',
    schema: {
      type: 'object',
      properties: {
        partner_id: { type: 'number', description: '只看某供应商' },
        company_id: { type: 'number' },
      },
    },
    async handler(p: { partner_id?: number; company_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getVendorBillAging(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 生产 MRP 3 ----------

  register({
    name: 'odoo_mo_list',
    description: '查生产订单列表（mrp.production）。可按状态 / 产品 / 单号关键字筛。state: draft/confirmed/progress/to_close/done/cancel。',
    schema: {
      type: 'object',
      properties: {
        state:      { type: 'string', enum: ['draft','confirmed','progress','to_close','done','cancel'] },
        product_id: { type: 'number' },
        keyword:    { type: 'string', description: '生产单号 ilike 搜索' },
        limit:      { type: 'number', description: '默认30' },
      },
    },
    async handler(p: { state?: 'draft'|'confirmed'|'progress'|'to_close'|'done'|'cancel'; product_id?: number; keyword?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getMrpProductions(p);
        return { success: true, count: records.length, productions: records.map(r => ({
          id: r['id'], name: r['name'], product: r['product_id'], qty: r['product_qty'],
          state: r['state'], date_start: r['date_start'], date_finished: r['date_finished'],
          bom: r['bom_id'], priority: r['priority'], company: r['company_id'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_mo_confirm',
    description: '【生产计划员】确认生产订单（mrp.production.action_confirm），draft → confirmed。',
    schema: {
      type: 'object',
      properties: { mo_ids: { type: 'array', items: { type: 'number' }, description: '生产订单 id 数组（必填）' } },
      required: ['mo_ids'],
    },
    async handler(p: { mo_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.confirmMrpProduction(p.mo_ids);
        return { success: true, message: `生产订单 ${p.mo_ids.map(i => '#'+i).join(', ')} 已确认。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_bom_query',
    description: '查询 BOM（mrp.bom）+ 自动展开 bom_line_ids 子物料。可按产品 / BOM id 筛。返回每个 BOM 的 lines 数组（产品 + 用量 + 单位）。',
    schema: {
      type: 'object',
      properties: {
        product_id:      { type: 'number', description: '按 product.product 筛' },
        product_tmpl_id: { type: 'number', description: '按 product.template 筛' },
        bom_id:          { type: 'number', description: '按 BOM id 筛' },
        limit:           { type: 'number', description: '默认 30' },
      },
    },
    async handler(p: { product_id?: number; product_tmpl_id?: number; bom_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getBomQuery(p);
        return { success: true, count: data.boms.length, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 会计深化 3 ----------

  register({
    name: 'odoo_journal_entries',
    description: '查询会计凭证（account.move where move_type=entry）。区间默认本月。可按 journal / state 筛。',
    schema: {
      type: 'object',
      properties: {
        journal_id: { type: 'number', description: '日记账 id' },
        state:      { type: 'string', enum: ['draft','posted','cancel'] },
        date_from:  { type: 'string', description: 'YYYY-MM-DD' },
        date_to:    { type: 'string', description: 'YYYY-MM-DD' },
        limit:      { type: 'number', description: '默认 30' },
      },
    },
    async handler(p: { journal_id?: number; state?: 'draft'|'posted'|'cancel'; date_from?: string; date_to?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getJournalEntries(p);
        return { success: true, count: records.length, entries: records.map(r => ({
          id: r['id'], name: r['name'], date: r['date'], journal: r['journal_id'],
          state: r['state'], amount: r['amount_total_signed'], ref: r['ref'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_payment_register',
    description: '【会计】登记付款（走 account.payment.register wizard）。对一组 invoice 调 action_create_payments 自动创建 account.payment 并核销。amount 不填默认全额。',
    schema: {
      type: 'object',
      properties: {
        invoice_ids:    { type: 'array', items: { type: 'number' }, description: '发票 / 账单 id 数组（必填）' },
        amount:         { type: 'number', description: '付款金额，不填默认全额' },
        payment_date:   { type: 'string', description: 'YYYY-MM-DD，默认今天' },
        journal_id:     { type: 'number', description: '收款日记账 id（不填用默认）' },
        communication:  { type: 'string', description: '付款备注' },
      },
      required: ['invoice_ids'],
    },
    async handler(p: { invoice_ids: number[]; amount?: number; payment_date?: string; journal_id?: number; communication?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.registerPayment(p);
        return { success: true, ...result, message: result.actions.join('；') };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_chart_of_accounts',
    description: '查询会计科目表（account.account）。可按 keyword（code/name）+ account_type 筛。account_type 例：asset_cash, asset_receivable, liability_payable, expense, income。',
    schema: {
      type: 'object',
      properties: {
        keyword:      { type: 'string', description: 'code 或 name 模糊搜索' },
        account_type: { type: 'string', description: '科目类型，如 asset_cash / liability_payable' },
        company_id:   { type: 'number' },
        limit:        { type: 'number', description: '默认 100' },
      },
    },
    async handler(p: { keyword?: string; account_type?: string; company_id?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getChartOfAccounts(p);
        return { success: true, count: records.length, accounts: records.map(r => ({
          id: r['id'], code: r['code'], name: r['name'], type: r['account_type'],
          currency: r['currency_id'], reconcile: r['reconcile'], companies: r['company_ids'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 智能洞察 2 ----------

  register({
    name: 'odoo_anomaly_detect',
    description: '【运营智能】异常检测：自动扫描 6 类异常（库存负数 / 大额订单 / 老旧未付发票 / 堆积审批 / 停滞商机 / draft 工资单）。返回 anomalies[] 含 type / severity / count / description / sample_ids。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.detectAnomalies();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_kpi_summary',
    description: '【老板视角】一句话 7 大 KPI：本月销售额 + 应收余额 + 待处理工单 / SLA 逾期 + 在制生产订单 + 库存预警 + 待审工资单。Promise.all 7 并发。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getKpiSummary();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 报表 / 数据导出 2 ----------

  register({
    name: 'odoo_pdf_report',
    description: '生成 QWeb PDF 报表的下载 URL（不直接拉 base64，避免 RPC payload 爆炸）。报表名是 ir.actions.report 的 xml id（如 sale.action_report_saleorder, account.account_invoices, hr_payroll.action_report_payslip）。返回 url 让用户/客户端去下载。',
    schema: {
      type: 'object',
      properties: {
        report_ref:  { type: 'string', description: '报表 xml id，如 sale.action_report_saleorder（必填）' },
        record_ids:  { type: 'array', items: { type: 'number' }, description: '记录 id 数组（必填）' },
      },
      required: ['report_ref', 'record_ids'],
    },
    async handler(p: { report_ref: string; record_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const url = client.getPdfReportUrl(p.report_ref, p.record_ids);
        return {
          success: true, url, report_ref: p.report_ref, record_ids: p.record_ids,
          message: `报表下载链接：${url}\n（注意：需要用户已在浏览器登录辉火云 session）`,
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_export_csv',
    description: '任意模型导 CSV：传 model + fields[]（fields 数组）+ 可选 domain，返回 CSV 字符串。Many2one 字段会自动取 [id, "name"] 的 name。limit 默认 1000。',
    schema: {
      type: 'object',
      properties: {
        model:  { type: 'string', description: '模型技术名（必填）' },
        fields: { type: 'array', items: { type: 'string' }, description: '字段名数组（必填）' },
        domain: { type: 'array', description: 'Odoo domain 三元组数组（可选）' },
        limit:  { type: 'number', description: '默认 1000' },
        order:  { type: 'string', description: '排序，如 "create_date desc"' },
      },
      required: ['model', 'fields'],
    },
    async handler(p: { model: string; fields: string[]; domain?: unknown[]; limit?: number; order?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.exportCsv({
          model: p.model,
          fields: p.fields,
          // OdooClient.exportCsv expects Domain (array of triples / operator strings)
          // We accept any array shape from LLM and pass through
          domain: (p.domain ?? []) as Parameters<typeof client.exportCsv>[0]['domain'],
          limit: p.limit,
          order: p.order,
        });
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 自动化 + 数据治理 + 批量 + 集成（v1.17 新增 14 个）
  //   流程自动化 3 + 数据治理 4 + 批量操作 3 + 集成治理 4
  // ══════════════════════════════════════════════════════

  // ---------- 流程自动化（3 个） ----------

  register({
    name: 'odoo_automations',
    description: '查询自动化规则列表（base.automation）。可按 model_id 筛某模型上的自动化。返回每条规则的触发器、过滤条件、关联 server actions。',
    schema: {
      type: 'object',
      properties: {
        model_id:    { type: 'number', description: 'ir.model id 筛选' },
        only_active: { type: 'boolean', description: '只看活跃，默认 true' },
        limit:       { type: 'number', description: '默认 50' },
      },
    },
    async handler(p: { model_id?: number; only_active?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getAutomations(p);
        return { success: true, count: records.length, automations: records.map(r => ({
          id: r['id'], name: r['name'], model: r['model_id'], model_name: r['model_name'],
          trigger: r['trigger'], active: r['active'],
          filter_domain: r['filter_domain'], filter_pre_domain: r['filter_pre_domain'],
          time_field: r['trg_date_id'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_cron_jobs',
    description: '查询计划任务列表（ir.cron）。返回每个 cron 的下次执行时间、间隔、scheduler 用户、关联 server action。',
    schema: {
      type: 'object',
      properties: {
        only_active: { type: 'boolean', description: '只看活跃，默认 true' },
        limit:       { type: 'number', description: '默认 100' },
      },
    },
    async handler(p: { only_active?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getCronJobs(p);
        return { success: true, count: records.length, crons: records.map(r => ({
          id: r['id'], name: r['cron_name'], user: r['user_id'], active: r['active'],
          interval: `${r['interval_number']} ${r['interval_type']}`,
          next_call: r['nextcall'], action: r['ir_actions_server_id'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_automation_create',
    description: '【系统管理员】创建自动化规则（base.automation）。trigger 可选：on_create / on_write / on_create_or_write / on_unlink / on_change / on_time / on_time_created / on_time_updated。需要先准备好 server_action_ids（ir.actions.server）。',
    schema: {
      type: 'object',
      properties: {
        name:               { type: 'string', description: '规则名（必填）' },
        model_id:           { type: 'number', description: 'ir.model id（必填）' },
        trigger:            { type: 'string', enum: ['on_create','on_write','on_create_or_write','on_unlink','on_change','on_time','on_time_created','on_time_updated'], description: '触发器（必填）' },
        server_action_ids:  { type: 'array', items: { type: 'number' }, description: '关联的 ir.actions.server ids' },
        filter_domain:      { type: 'string', description: 'Odoo domain 字符串，如 [(\'state\',\'=\',\'done\')]' },
        active:             { type: 'boolean', description: '是否启用，默认 true' },
      },
      required: ['name', 'model_id', 'trigger'],
    },
    async handler(p: { name: string; model_id: number; trigger: 'on_create'|'on_write'|'on_create_or_write'|'on_unlink'|'on_change'|'on_time'|'on_time_created'|'on_time_updated'; server_action_ids?: number[]; filter_domain?: string; active?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createAutomation(p);
        return { success: true, id, message: `自动化规则 #${id}（${p.name}，${p.trigger}）已创建。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 数据治理（4 个） ----------

  register({
    name: 'odoo_data_quality_partners',
    description: '联系人重复检测（res.partner）。按 email / phone / name 分组找出现 > 1 次的值。返回 duplicate_groups[] 含 key + partner_ids + count，用于后续 odoo_partners_merge。',
    schema: {
      type: 'object',
      properties: {
        by:    { type: 'string', enum: ['email', 'phone', 'name'], description: '查重维度，默认 email' },
        limit: { type: 'number', description: '初步分组上限，默认 1000' },
      },
    },
    async handler(p: { by?: 'email'|'phone'|'name'; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.detectDuplicatePartners(p);
        return { success: true, count: data.duplicate_groups.length, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_data_quality_products',
    description: '产品重复检测（product.product）。按 default_code（SKU）/ barcode / name 分组。返回 duplicate_groups[] 含 key + product_ids + count。',
    schema: {
      type: 'object',
      properties: {
        by:    { type: 'string', enum: ['default_code', 'barcode', 'name'], description: '查重维度，默认 default_code' },
        limit: { type: 'number', description: '默认 1000' },
      },
    },
    async handler(p: { by?: 'default_code'|'barcode'|'name'; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.detectDuplicateProducts(p);
        return { success: true, count: data.duplicate_groups.length, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_data_quality_completeness',
    description: '字段完整性扫描：6 类常见"应填未填"（员工无 work_email / 员工无电话 / 员工无上级 / 公司联系人无 email / 客户无国家 / 产品无 SKU）。每项返 model + field + missing_count + severity + sample_ids。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.dataQualityCompleteness();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_partners_merge',
    description: '【数据治理】合并重复联系人（base.partner.merge.automatic.wizard._merge）。Odoo 安全限制：单次最多合并 3 个 partner。dst_partner_id 是保留的主记录，其他 partner 的关联（订单、发票、活动）会被转移过来。',
    schema: {
      type: 'object',
      properties: {
        partner_ids:     { type: 'array', items: { type: 'number' }, description: '要合并的 partner id 数组（2-3 个，必填）' },
        dst_partner_id:  { type: 'number', description: '保留的主 partner id，不填默认 partner_ids[0]' },
      },
      required: ['partner_ids'],
    },
    async handler(p: { partner_ids: number[]; dst_partner_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.mergePartners(p);
        return { success: true, ...result, message: result.actions.join('；') };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 批量操作（3 个） ----------

  register({
    name: 'odoo_batch_email',
    description: '【批量】按 domain 给一组记录发邮件（用 mail.template）。force_send=false 进队列，不阻塞。先用 odoo_email_templates 找 template_id。',
    schema: {
      type: 'object',
      properties: {
        model:       { type: 'string', description: '目标模型，如 res.partner / sale.order（必填）' },
        domain:      { type: 'array', description: 'Odoo domain 数组（必填）' },
        template_id: { type: 'number', description: 'mail.template id（必填）' },
        limit:       { type: 'number', description: '匹配上限，默认 100' },
      },
      required: ['model', 'domain', 'template_id'],
    },
    async handler(p: { model: string; domain: unknown[]; template_id: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.batchEmail({
          model: p.model, template_id: p.template_id, limit: p.limit,
          domain: p.domain as Parameters<typeof client.batchEmail>[0]['domain'],
        });
        return { success: true, ...result, message: result.actions.join('；') };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_batch_archive',
    description: '【批量】对一组记录批量改 active 字段（archive=false 归档 / activate=true 激活）。适用于任何带 active 字段的模型。',
    schema: {
      type: 'object',
      properties: {
        model:      { type: 'string', description: '模型技术名（必填）' },
        record_ids: { type: 'array', items: { type: 'number' }, description: '记录 id 数组（必填）' },
        activate:   { type: 'boolean', description: 'true=激活 / false=归档（默认 false）' },
      },
      required: ['model', 'record_ids'],
    },
    async handler(p: { model: string; record_ids: number[]; activate?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.batchArchive(p);
        return { success: true, ...result, message: `已对 ${result.count} 条 ${result.model} 记录设置 active=${result.activate}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_batch_assign',
    description: '【批量】把一组记录的经办人改成新的 user_id。适用于工单 / 任务 / 活动 / 商机等。任务用 field="user_ids"（多对多 replace），其他默认 "user_id"（多对一）。',
    schema: {
      type: 'object',
      properties: {
        model:      { type: 'string', description: '模型技术名（必填）' },
        record_ids: { type: 'array', items: { type: 'number' }, description: '记录 id 数组（必填）' },
        user_id:    { type: 'number', description: '新经办人 res.users id（必填）' },
        field:      { type: 'string', description: '默认 user_id，project.task 用 user_ids' },
      },
      required: ['model', 'record_ids', 'user_id'],
    },
    async handler(p: { model: string; record_ids: number[]; user_id: number; field?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.batchAssign(p);
        return { success: true, ...result, message: `已把 ${result.count} 条 ${result.model} 的 ${result.field} 改为 user #${result.user_id}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 集成 / 治理（4 个） ----------

  register({
    name: 'odoo_translate_record',
    description: '【多语言】给某条记录的某字段写多语言翻译（model.update_field_translations）。translations 是 { lang: value } 对象，如 { "zh_CN": "中文名", "en_US": "English Name" }。字段必须是 translate=True 的。',
    schema: {
      type: 'object',
      properties: {
        model:        { type: 'string', description: '模型技术名（必填）' },
        record_id:    { type: 'number', description: '记录 id（必填）' },
        field:        { type: 'string', description: '字段名（必填，必须是 translate=True 的）' },
        translations: { type: 'object', description: '语言代码 → 翻译值，如 { "zh_CN": "...", "en_US": "..." }（必填）' },
      },
      required: ['model', 'record_id', 'field', 'translations'],
    },
    async handler(p: { model: string; record_id: number; field: string; translations: Record<string, string> }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.translateRecord(p);
        return { success: true, ...result, message: `已为 ${result.model}#${result.record_id}.${result.field} 更新 ${result.updated_languages.length} 种语言翻译（${result.updated_languages.join(', ')}）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_custom_fields',
    description: '查询自定义字段（ir.model.fields where state=\'manual\'，即 x_* 开头的 Studio/手工字段）。可按 model 名称筛某模型，或按 keyword 搜字段名/描述。',
    schema: {
      type: 'object',
      properties: {
        model:   { type: 'string', description: '模型技术名筛选，如 res.partner' },
        keyword: { type: 'string', description: '字段名 / 描述模糊搜索' },
        limit:   { type: 'number', description: '默认 100' },
      },
    },
    async handler(p: { model?: string; keyword?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getCustomFields(p);
        return { success: true, count: records.length, fields: records.map(r => ({
          id: r['id'], name: r['name'], model: r['model'],
          description: r['field_description'], type: r['ttype'],
          required: r['required'], relation: r['relation'], help: r['help'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_user_create',
    description: '【系统管理员】创建系统用户（res.users）+ 可选关联到 hr.employee + 可选指定权限组。不传 password 时会用 Odoo 默认（需走"邀请邮件"流程让用户自己设密码）。',
    schema: {
      type: 'object',
      properties: {
        name:        { type: 'string', description: '用户名（必填）' },
        login:       { type: 'string', description: '登录名 / 邮箱（必填）' },
        email:       { type: 'string', description: '邮箱，不填默认用 login' },
        employee_id: { type: 'number', description: '关联到 hr.employee id' },
        group_ids:   { type: 'array', items: { type: 'number' }, description: '权限组 res.groups ids（直接赋）' },
        password:    { type: 'string', description: '初始密码，不填走邀请邮件流程' },
        company_id:  { type: 'number', description: '默认公司 id' },
      },
      required: ['name', 'login'],
    },
    async handler(p: { name: string; login: string; email?: string; employee_id?: number; group_ids?: number[]; password?: string; company_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.createUser(p);
        return { success: true, ...result, message: `用户 #${result.user_id}（${p.name}）已创建。${result.actions.join('；')}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_user_groups',
    description: '查某用户的所有权限组（res.users.groups_id → res.groups）。user_id 不填默认查当前用户。返回 full_name 包含 category（如"Sales / User: Own Documents Only"）。',
    schema: {
      type: 'object',
      properties: { user_id: { type: 'number', description: '用户 id，不填默认当前用户' } },
    },
    async handler(p: { user_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getUserGroups(p.user_id);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // Studio 元编程 + 审计 + 多公司 + 报表 + 集成（v1.18 新增 14 个）
  //   Studio 4 + 审计 3 + 多公司 2 + 报表 2 + 集成 3
  // ══════════════════════════════════════════════════════

  // ---------- Studio 元编程 4 ----------

  register({
    name: 'odoo_model_list',
    description: '查询 ir.model 模型列表。可按 keyword（模型名 / 描述）+ only_custom 筛选自定义模型 + transient 筛 wizard 模型。给上层定位某模型用。',
    schema: {
      type: 'object',
      properties: {
        keyword:     { type: 'string', description: '模型名 / 描述模糊搜索' },
        only_custom: { type: 'boolean', description: '只看自定义（state=manual）' },
        transient:   { type: 'boolean', description: '是否 wizard 类（TransientModel）' },
        limit:       { type: 'number', description: '默认 100' },
      },
    },
    async handler(p: { keyword?: string; only_custom?: boolean; transient?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getModels(p);
        return { success: true, count: records.length, models: records.map(r => ({
          id: r['id'], name: r['name'], model: r['model'],
          state: r['state'], info: r['info'],
          transient: r['transient'], abstract: r['abstract'], order: r['order'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_model_fields',
    description: '查某模型的所有字段（ir.model.fields）。可按 keyword 搜字段名/描述 + only_custom 筛 x_* 自定义字段。返回 ttype / required / relation / selection / translate 等元数据。',
    schema: {
      type: 'object',
      properties: {
        model:       { type: 'string', description: '模型技术名（必填）' },
        keyword:     { type: 'string', description: '字段名 / 描述模糊搜索' },
        only_custom: { type: 'boolean', description: '只看自定义字段' },
        limit:       { type: 'number', description: '默认 200' },
      },
      required: ['model'],
    },
    async handler(p: { model: string; keyword?: string; only_custom?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getModelFields(p.model, p);
        return { success: true, count: records.length, fields: records.map(r => ({
          id: r['id'], name: r['name'], description: r['field_description'],
          type: r['ttype'], required: r['required'], readonly: r['readonly'],
          relation: r['relation'], selection: r['selection'],
          state: r['state'], translate: r['translate'], help: r['help'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_model_create',
    description: '【系统管理员 / Studio】创建自定义模型（ir.model）。model 技术名必须 x_ 开头（Odoo 强制约束）。state 自动设为 manual。',
    schema: {
      type: 'object',
      properties: {
        name:      { type: 'string', description: '模型显示名（必填，如"客户回访记录"）' },
        model:     { type: 'string', description: '技术名（必填，必须 x_ 开头，如 x_customer_visit）' },
        transient: { type: 'boolean', description: '是否 wizard 模型，默认 false' },
        abstract:  { type: 'boolean', description: '是否抽象模型，默认 false' },
      },
      required: ['name', 'model'],
    },
    async handler(p: { name: string; model: string; transient?: boolean; abstract?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createModel(p);
        return { success: true, id, message: `自定义模型 #${id}（${p.model} - ${p.name}）已创建。如需加字段调 odoo_field_create。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_field_create',
    description: '【系统管理员 / Studio】给某模型加字段（ir.model.fields）。name 必须 x_ 开头。ttype 决定字段类型（many2one/many2many/one2many 必填 relation；selection 必填 selection）。',
    schema: {
      type: 'object',
      properties: {
        model:             { type: 'string', description: '目标模型技术名（必填）' },
        name:              { type: 'string', description: '字段技术名（必填，x_ 开头）' },
        field_description: { type: 'string', description: '字段显示名（必填）' },
        ttype:             { type: 'string', enum: ['char','text','integer','float','monetary','boolean','date','datetime','binary','selection','many2one','one2many','many2many','html'], description: '字段类型（必填）' },
        required:          { type: 'boolean', description: '是否必填，默认 false' },
        relation:          { type: 'string', description: 'many2one/many2many/one2many 必填，目标模型技术名' },
        selection:         { type: 'array', items: { type: 'array', items: { type: 'string' } }, description: 'selection 必填，[[key, label], ...]' },
        help:              { type: 'string', description: '提示文字' },
        translate:         { type: 'boolean', description: '是否多语言翻译' },
      },
      required: ['model', 'name', 'field_description', 'ttype'],
    },
    async handler(p: { model: string; name: string; field_description: string; ttype: 'char'|'text'|'integer'|'float'|'monetary'|'boolean'|'date'|'datetime'|'binary'|'selection'|'many2one'|'one2many'|'many2many'|'html'; required?: boolean; relation?: string; selection?: Array<[string,string]>; help?: string; translate?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createModelField(p);
        return { success: true, id, message: `字段 #${id}（${p.model}.${p.name}，${p.ttype}）已创建。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 审计与变更追踪 3 ----------

  register({
    name: 'odoo_audit_log',
    description: '查某条记录的全部变更历史（mail.message + mail.tracking.value 联表）。返回每次变更：date / author / field / old_value / new_value。',
    schema: {
      type: 'object',
      properties: {
        model:     { type: 'string', description: '模型技术名（必填）' },
        record_id: { type: 'number', description: '记录 id（必填）' },
        limit:     { type: 'number', description: '默认 100 条 message' },
      },
      required: ['model', 'record_id'],
    },
    async handler(p: { model: string; record_id: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getAuditLog(p);
        return { success: true, change_count: data.changes.length, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_login_history',
    description: '查用户登录历史（res.users.log，每次登录留一条）。可按 user_id 筛某用户，days 默认 30。',
    schema: {
      type: 'object',
      properties: {
        user_id: { type: 'number', description: '用户 id，不填默认当前用户' },
        days:    { type: 'number', description: '近 N 天，默认 30' },
        limit:   { type: 'number', description: '默认 100' },
      },
    },
    async handler(p: { user_id?: number; days?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getLoginHistory(p);
        return { success: true, count: records.length, logins: records.map(r => ({
          id: r['id'], user: r['user_id'], at: r['create_date'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_field_history',
    description: '【聚焦视图】查某条记录某个字段的所有变更历史。比 odoo_audit_log 更聚焦——只返这一个字段的 from→to 变化序列。用于"X 的 stage 变过几次"、"工资改过几次"。',
    schema: {
      type: 'object',
      properties: {
        model:      { type: 'string', description: '模型技术名（必填）' },
        record_id:  { type: 'number', description: '记录 id（必填）' },
        field_name: { type: 'string', description: '字段技术名（必填）' },
        limit:      { type: 'number', description: '默认 50' },
      },
      required: ['model', 'record_id', 'field_name'],
    },
    async handler(p: { model: string; record_id: number; field_name: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getFieldHistory(p);
        return { success: true, change_count: data.history.length, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 多公司联动 2 ----------

  register({
    name: 'odoo_company_switch',
    description: '切换当前用户激活的公司（写 res.users.company_id）。需要 user 在该公司的 allowed company list 里。后续所有 RPC 默认按新公司过滤。',
    schema: {
      type: 'object',
      properties: { company_id: { type: 'number', description: '目标公司 id（必填）' } },
      required: ['company_id'],
    },
    async handler(p: { company_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.switchCompany(p.company_id);
        return { success: true, ...result, message: `已切换到公司 #${result.new_company_id}（${result.new_company_name}）。${result.actions.join('；')}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_consolidated_dashboard',
    description: '【集团视角】跨公司聚合仪表盘：按 company_ids（不填用 user.company_ids）汇总每家公司的销售/应收/工单/在编 4 项 + 集团 grand_total。',
    schema: {
      type: 'object',
      properties: {
        company_ids: { type: 'array', items: { type: 'number' }, description: '公司 id 数组，不填用我的 allowed_company_ids' },
        date_from:   { type: 'string', description: 'YYYY-MM-DD，默认本月初' },
        date_to:     { type: 'string', description: 'YYYY-MM-DD，默认今天' },
      },
    },
    async handler(p: { company_ids?: number[]; date_from?: string; date_to?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getConsolidatedDashboard(p);
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 报表深化 2 ----------

  register({
    name: 'odoo_pivot_data',
    description: '通用 pivot 数据查询（read_group 通用入口）。measures 是 ["amount_total:sum", "qty:sum"] 这种"字段:聚合函数"。groupby 是 1-2 维分组字段。返回 rows + total 总计。',
    schema: {
      type: 'object',
      properties: {
        model:    { type: 'string', description: '模型技术名（必填）' },
        measures: { type: 'array', items: { type: 'string' }, description: '聚合字段，如 ["amount_total:sum"]（必填）' },
        groupby:  { type: 'array', items: { type: 'string' }, description: '分组维度（必填，1-2 个）' },
        domain:   { type: 'array', description: 'Odoo domain 过滤（可选）' },
        limit:    { type: 'number', description: '默认 200' },
        orderby:  { type: 'string', description: '排序，如 "amount_total desc"' },
      },
      required: ['model', 'measures', 'groupby'],
    },
    async handler(p: { model: string; measures: string[]; groupby: string[]; domain?: unknown[]; limit?: number; orderby?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getPivotData({
          model: p.model, measures: p.measures, groupby: p.groupby,
          domain: (p.domain ?? []) as Parameters<typeof client.getPivotData>[0]['domain'],
          limit: p.limit, orderby: p.orderby,
        });
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_email_log',
    description: '查邮件发送日志（mail.mail），按 state 筛 outgoing/sent/exception/cancel。days 默认 7。用于排查"邮件没发出去"。',
    schema: {
      type: 'object',
      properties: {
        state: { type: 'string', enum: ['outgoing','sent','received','exception','cancel'], description: '邮件状态' },
        days:  { type: 'number', description: '近 N 天，默认 7' },
        limit: { type: 'number', description: '默认 50' },
      },
    },
    async handler(p: { state?: 'outgoing'|'sent'|'received'|'exception'|'cancel'; days?: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getEmailLog(p);
        return { success: true, count: records.length, mails: records.map(r => ({
          id: r['id'], subject: r['subject'], from: r['email_from'], to: r['email_to'],
          state: r['state'], created: r['create_date'], sent: r['date'],
          failure_type: r['failure_type'], failure_reason: r['failure_reason'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 外部集成 3 ----------

  register({
    name: 'odoo_webhook_create',
    description: '【系统管理员】创建出站 Webhook：通过 ir.actions.server (state=webhook) + base.automation 触发器组合。当目标模型记录创建/更新/删除时 POST 到 webhook_url。',
    schema: {
      type: 'object',
      properties: {
        name:               { type: 'string', description: 'webhook 名（必填）' },
        model_id:           { type: 'number', description: 'ir.model id 监听的模型（必填）' },
        webhook_url:        { type: 'string', description: 'POST 目标 URL（必填）' },
        webhook_field_ids:  { type: 'array', items: { type: 'number' }, description: '要发送的 ir.model.fields ids（不填只发 _name）' },
        trigger:            { type: 'string', enum: ['on_create','on_write','on_create_or_write'], description: '触发器类型（必填）' },
        filter_domain:      { type: 'string', description: 'Odoo domain 字符串筛选触发条件' },
      },
      required: ['name', 'model_id', 'webhook_url', 'trigger'],
    },
    async handler(p: { name: string; model_id: number; webhook_url: string; webhook_field_ids?: number[]; trigger: 'on_create'|'on_write'|'on_create_or_write'; filter_domain?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.createWebhookAction({
          name: p.name, model_id: p.model_id, webhook_url: p.webhook_url,
          webhook_field_ids: p.webhook_field_ids,
          automation: { trigger: p.trigger, filter_domain: p.filter_domain },
        });
        return { success: true, ...result, message: result.actions.join('；') };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_record_share_url',
    description: '生成某条记录的分享链接：优先尝试 portal_url（mail.thread.portal_mixin 提供，外部可访问）+ 始终返回 backend_url（后台登录态访问）。用于"把这个商机/工单链接发给客户/同事"。',
    schema: {
      type: 'object',
      properties: {
        model:     { type: 'string', description: '模型技术名（必填）' },
        record_id: { type: 'number', description: '记录 id（必填）' },
      },
      required: ['model', 'record_id'],
    },
    async handler(p: { model: string; record_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getRecordShareUrl(p);
        const msg = data.portal_url
          ? `Portal 链接（外部可访问）：${data.portal_url}\n后台链接：${data.backend_url}`
          : `仅后台链接（该模型不支持 portal）：${data.backend_url}`;
        return { success: true, ...data, message: msg };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_mail_queue',
    description: '【运维】邮件队列健康检查：返回 outgoing 待发数、exception 失败数、今日已发数、+ 5 个待发样本 + 5 个失败样本（含 failure_reason）。一句话排查"为什么我的邮件没发出去"。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getMailQueue();
        return { success: true, ...data };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 审批发起 + 克隆 + 关注 + 资源 + 报表订阅 + 多语言（v1.20 新增 14 个）
  //   审批 4 + 克隆/导入 3 + Mail 关注 3 + 资源 2 + 报表订阅 1 + 多语言 1
  // ══════════════════════════════════════════════════════

  // ---------- 审批工作流深化 4 ----------

  register({
    name: 'odoo_approval_categories',
    description: '查审批分类列表（approval.category）。返回每个分类的 approval_minimum（需要几人审批）/ approval_type（请假/采购/差旅...）。给 odoo_approval_create 配料用。',
    schema: {
      type: 'object',
      properties: {
        keyword:     { type: 'string', description: '名称模糊搜' },
        only_active: { type: 'boolean', description: '只看活跃，默认 true' },
        limit:       { type: 'number', description: '默认 50' },
      },
    },
    async handler(p: { keyword?: string; only_active?: boolean; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getApprovalCategories(p);
        return { success: true, count: records.length, categories: records.map(r => ({
          id: r['id'], name: r['name'], minimum: r['approval_minimum'],
          type: r['approval_type'], company: r['company_id'],
          auto_seq: r['automated_sequence'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_approval_create',
    description: '【发起审批】创建审批请求（approval.request）+ 可选 auto_confirm=true 立即提交审批（状态从 new → pending）。reason / amount / quantity / location / partner_id 按分类需要选填。',
    schema: {
      type: 'object',
      properties: {
        category_id:   { type: 'number', description: '审批分类 id（必填）' },
        name:          { type: 'string', description: '审批主题，不填用 category 默认' },
        reason:        { type: 'string', description: '原因/详情（HTML 也可）' },
        date_start:    { type: 'string', description: '开始时间 YYYY-MM-DD HH:MM:SS（如请假）' },
        date_end:      { type: 'string', description: '结束时间' },
        quantity:      { type: 'number', description: '数量（如设备申请）' },
        amount:        { type: 'number', description: '金额（如报销）' },
        location:      { type: 'string', description: '地点（如出差）' },
        partner_id:    { type: 'number', description: '关联联系人' },
        auto_confirm:  { type: 'boolean', description: '是否立即提交审批，默认 false（保留 new 状态等待）' },
      },
      required: ['category_id'],
    },
    async handler(p: { category_id: number; name?: string; reason?: string; date_start?: string; date_end?: string; quantity?: number; amount?: number; location?: string; partner_id?: number; auto_confirm?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.createApprovalRequest(p);
        return { success: true, ...result, message: `审批请求 #${result.request_id} 已创建。${result.actions.join('；')}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_approval_confirm',
    description: '【发起人侧】把已创建（new 状态）的审批请求提交审批（action_confirm，new → pending）。批量传 ids。',
    schema: {
      type: 'object',
      properties: { request_ids: { type: 'array', items: { type: 'number' }, description: '审批请求 id 数组（必填）' } },
      required: ['request_ids'],
    },
    async handler(p: { request_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.confirmApprovalRequest(p.request_ids);
        return { success: true, message: `审批请求 ${p.request_ids.map(i => '#'+i).join(', ')} 已提交（new → pending）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_approval_my_pending',
    description: '【审批人视角】我手上待审批的请求（request_status=pending 且 approver_ids 包含当前用户）。一句话回答"我有几条要批的"。',
    schema: {
      type: 'object',
      properties: { limit: { type: 'number', description: '默认 30' } },
    },
    async handler(p: { limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getMyPendingApprovals(p);
        return { success: true, count: records.length, pending: records.map(r => ({
          id: r['id'], name: r['name'], category: r['category_id'],
          owner: r['request_owner_id'], date: r['date'],
          amount: r['amount'], reason: r['reason'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 数据克隆 / 导入 3 ----------

  register({
    name: 'odoo_record_clone',
    description: '浅复制一条记录（BaseModel.copy）。Odoo 内置方法，所有 model 都有。可用 overrides 字典覆盖某些字段（如 name "[Copy] xxx"）。注意 O2m 子表复制行为各 model 不同——简单 model 自动跟，复杂 model（sale.order/mrp.bom）建议用 odoo_record_clone_with_lines。',
    schema: {
      type: 'object',
      properties: {
        model:     { type: 'string', description: '模型技术名（必填）' },
        record_id: { type: 'number', description: '源记录 id（必填）' },
        overrides: { type: 'object', description: '覆盖字段，传给 copy(default=...)' },
      },
      required: ['model', 'record_id'],
    },
    async handler(p: { model: string; record_id: number; overrides?: Record<string, unknown> }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.cloneRecord(p);
        return { success: true, ...data, message: `${p.model} #${p.record_id} 已复制为 #${data.clone_id}。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_record_clone_with_lines',
    description: '深度复制带子表的记录。先 copy 主记录（清空子表），再读取源子表 + 用 [0,0,vals] 重新挂到新主记录。例：sale.order 用 line_field=order_line / line_model=sale.order.line。line_fields 列出要复制的子表字段名。',
    schema: {
      type: 'object',
      properties: {
        model:        { type: 'string', description: '主模型技术名（必填）' },
        record_id:    { type: 'number', description: '源主记录 id（必填）' },
        line_field:   { type: 'string', description: '主表上的 O2m 字段名（必填，如 order_line）' },
        line_model:   { type: 'string', description: '子表模型技术名（必填，如 sale.order.line）' },
        line_fields:  { type: 'array', items: { type: 'string' }, description: '子表要复制的字段名（必填）' },
        overrides:    { type: 'object', description: '主记录 copy 时的覆盖字段' },
      },
      required: ['model', 'record_id', 'line_field', 'line_model', 'line_fields'],
    },
    async handler(p: { model: string; record_id: number; line_field: string; line_model: string; line_fields: string[]; overrides?: Record<string, unknown> }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.cloneRecordWithLines(p);
        return { success: true, ...data, message: `${p.model} #${p.record_id} 深复制为 #${data.clone_id}（含 ${data.lines_copied} 行子表）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_csv_import',
    description: '【批量】把 CSV 行数据导入到任意 model。逐行 create，全数字字符串自动转 number / true|false 转 bool。返回 imported_ids[] 和 failed_rows[]。失败行不会回滚已成功的。',
    schema: {
      type: 'object',
      properties: {
        model:   { type: 'string', description: '目标模型（必填）' },
        headers: { type: 'array', items: { type: 'string' }, description: '字段名数组（必填，对应每列）' },
        rows:    { type: 'array', items: { type: 'array', items: { type: 'string' } }, description: '数据行二维数组（必填）' },
      },
      required: ['model', 'headers', 'rows'],
    },
    async handler(p: { model: string; headers: string[]; rows: string[][] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.importCsv(p);
        return { success: true, ...data,
          message: `已导入 ${data.imported_ids.length} 条；${data.failed_rows.length} 行失败。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- Mail 关注（3） ----------

  register({
    name: 'odoo_followers',
    description: '查某条记录的关注者列表（mail.followers）。每条记录可被多个 partner 关注，关注者会收到该记录的 chatter 通知。',
    schema: {
      type: 'object',
      properties: {
        model:     { type: 'string', description: '模型技术名（必填）' },
        record_id: { type: 'number', description: '记录 id（必填）' },
        limit:     { type: 'number', description: '默认 100' },
      },
      required: ['model', 'record_id'],
    },
    async handler(p: { model: string; record_id: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getFollowers(p);
        return { success: true, count: records.length, followers: records.map(r => ({
          id: r['id'], partner: r['partner_id'],
          model: r['res_model'], record_id: r['res_id'],
          subtypes: r['subtype_ids'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_subscribe',
    description: '订阅某条记录（mail_thread.message_subscribe）。partner_ids 不填默认订阅当前用户的 partner。订阅后该 partner 会收到记录的 chatter 通知。',
    schema: {
      type: 'object',
      properties: {
        model:        { type: 'string', description: '模型技术名（必填）' },
        record_id:    { type: 'number', description: '记录 id（必填）' },
        partner_ids:  { type: 'array', items: { type: 'number' }, description: '关注者 partner ids，不填默认订阅我自己' },
      },
      required: ['model', 'record_id'],
    },
    async handler(p: { model: string; record_id: number; partner_ids?: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.subscribeRecord(p);
        return { success: true, ...data, message: `已订阅 ${p.model} #${p.record_id}（partners: ${data.partner_ids.join(', ')}）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_unsubscribe',
    description: '取消订阅某记录（mail_thread.message_unsubscribe）。partner_ids 不填默认取消我自己的订阅。',
    schema: {
      type: 'object',
      properties: {
        model:        { type: 'string', description: '模型技术名（必填）' },
        record_id:    { type: 'number', description: '记录 id（必填）' },
        partner_ids:  { type: 'array', items: { type: 'number' }, description: '要取消的 partner ids，不填默认取消我自己' },
      },
      required: ['model', 'record_id'],
    },
    async handler(p: { model: string; record_id: number; partner_ids?: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.unsubscribeRecord(p);
        return { success: true, ...data, message: `已取消 ${p.model} #${p.record_id} 的订阅（partners: ${data.partner_ids.join(', ')}）。` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 资源 / 工作时间表 2 ----------

  register({
    name: 'odoo_resources',
    description: '查询资源列表（resource.resource）。resource_type 可筛 user（员工资源）或 material（设备/会议室/物料资源）。',
    schema: {
      type: 'object',
      properties: {
        keyword:       { type: 'string', description: '资源名模糊搜' },
        resource_type: { type: 'string', enum: ['user', 'material'], description: '类型筛选' },
        limit:         { type: 'number', description: '默认 50' },
      },
    },
    async handler(p: { keyword?: string; resource_type?: 'user' | 'material'; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const records = await client.getResources(p);
        return { success: true, count: records.length, resources: records.map(r => ({
          id: r['id'], name: r['name'], type: r['resource_type'],
          user: r['user_id'], company: r['company_id'],
          calendar: r['calendar_id'], tz: r['tz'],
          time_efficiency: r['time_efficiency'],
        })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_resource_calendar',
    description: '查工作时间表详情（resource.calendar）+ 自动展开 attendance_ids（每周班次：周几/几点开始/几点结束/上午下午）。用于"X 资源/员工的工作时间是怎么定义的"。',
    schema: {
      type: 'object',
      properties: { calendar_id: { type: 'number', description: 'resource.calendar id（必填）' } },
      required: ['calendar_id'],
    },
    async handler(p: { calendar_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getResourceCalendar(p.calendar_id);
        return { success: true, ...data,
          attendance_count: data.attendances.length };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 报表订阅 1 ----------

  register({
    name: 'odoo_report_schedule',
    description: '【自动化】定期发送 PDF 报表订阅。组合 ir.actions.server (state=code) + ir.cron 两对象，让 cron 周期性渲染 report_ref 报表 + 写入收件箱。interval_type: minutes/hours/days/weeks/months。',
    schema: {
      type: 'object',
      properties: {
        name:            { type: 'string', description: '订阅名（必填）' },
        report_ref:      { type: 'string', description: 'ir.actions.report xml id，如 sale.action_report_saleorder（必填）' },
        model:           { type: 'string', description: '报表对应模型，如 sale.order（必填）' },
        record_domain:   { type: 'string', description: 'Odoo domain 字符串筛选记录，如 "[(\'state\',\'=\',\'sale\')]"' },
        interval_number: { type: 'number', description: '间隔数（必填）' },
        interval_type:   { type: 'string', enum: ['minutes','hours','days','weeks','months'], description: '间隔单位（必填）' },
        next_call:       { type: 'string', description: '首次执行 YYYY-MM-DD HH:MM:SS' },
        user_id:         { type: 'number', description: 'scheduler 身份 res.users id' },
      },
      required: ['name', 'report_ref', 'model', 'interval_number', 'interval_type'],
    },
    async handler(p: { name: string; report_ref: string; model: string; record_domain?: string; interval_number: number; interval_type: 'minutes'|'hours'|'days'|'weeks'|'months'; next_call?: string; user_id?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.scheduleReportEmail(p);
        return { success: true, ...result, message: result.actions.join('；') };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ---------- 多语言 1 ----------

  register({
    name: 'odoo_translate_get',
    description: '读某条记录某字段的所有语言翻译（model.get_field_translations）。返回 { lang_code: value } 对象。和 odoo_translate_record（写）配套，用来"先看现有翻译再决定改不改"。',
    schema: {
      type: 'object',
      properties: {
        model:     { type: 'string', description: '模型技术名（必填）' },
        record_id: { type: 'number', description: '记录 id（必填）' },
        field:     { type: 'string', description: '字段名（必填，必须是 translate=True 的）' },
      },
      required: ['model', 'record_id', 'field'],
    },
    async handler(p: { model: string; record_id: number; field: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const data = await client.getRecordTranslations(p);
        return { success: true, ...data,
          lang_count: Object.keys(data.translations).length };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 审批（v1.2 新增）
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_approvals',
    description: '查看审批请求列表。用于"我的审批"、"待审批的"等。',
    schema: {
      type: 'object',
      properties: {
        my_requests: { type: 'boolean', description: '只看我提交的请求' },
        state:       { type: 'string', enum: ['new','pending','approved','refused','cancel'], description: '状态筛选' },
        limit:       { type: 'number', description: '上限，默认20' },
      },
    },
    async handler(p: { my_requests?: boolean; state?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const approvals = await client.getApprovals({ my_requests: p.my_requests, state: p.state, limit: p.limit });
        return { success: true, count: approvals.length, approvals: approvals.map(a => ({ id: a['id'], name: a['name'], category: a['category_id'], owner: a['request_owner_id'], status: a['request_status'], date: a['date'], amount: a['amount'], reason: a['reason'] })) };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 实施经理每日概况
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_daily_briefing',
    description: '实施经理每日工作概况：今日截止任务、到期活动、待处理工单、逾期发票、商机跟进、未读消息。用于"今天有什么工作"、"给我今日概况"等。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const briefing = await client.getDailyBriefing();
        const todayStr = today();
        const total = briefing.todayTasks.length + briefing.overdueActivities.length + briefing.openTickets.length;
        return {
          success: true,
          message: `${todayStr} 概况：${total} 项核心待处理`,
          briefing: {
            date: todayStr,
            today_tasks: { count: briefing.todayTasks.length, items: briefing.todayTasks.map(t => ({ id: t['id'], name: t['name'], project: t['project_id'], deadline: t['date_deadline'], priority: t['priority'] })) },
            activities:  { count: briefing.overdueActivities.length, items: briefing.overdueActivities.map(a => ({ id: a['id'], summary: a['summary'], deadline: a['date_deadline'], type: a['activity_type_id'], model: a['res_model'], state: a['state'] })) },
            tickets:     { count: briefing.openTickets.length, items: briefing.openTickets.map(t => ({ id: t['id'], ref: t['ticket_ref'], name: t['name'], priority: t['priority'], sla_fail: t['sla_fail'] })) },
            overdue_invoices: { count: briefing.overdueInvoices.length, items: briefing.overdueInvoices.map(i => ({ id: i['id'], name: i['name'], partner: i['partner_id'], due_date: i['invoice_date_due'], amount: i['amount_total'] })) },
            crm_followups:    { count: briefing.crmFollowUps.length, items: briefing.crmFollowUps.map(l => ({ id: l['id'], name: l['name'], partner: l['partner_id'], stage: l['stage_id'], revenue: l['expected_revenue'] })) },
            unread_messages:  { count: briefing.unreadMessages.length, items: briefing.unreadMessages.map(m => ({ id: m['id'], subject: m['subject'], author: m['author_id'], model: m['model'] })) },
          },
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // 通知基座（跨渠道）
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_notification_status',
    description: '查看辉火云企业套件通知总线状态：已注册的渠道 transport、订阅者数、最近一次 poll 时间、当前 agent 的偏好设置、信封溯源缓存大小。用于"通知推送情况"、"企微/钉钉有没有连上"等排查类问题。',
    schema: { type: 'object', properties: {} },
    async handler(_p: unknown, ctx: Record<string, unknown>) {
      const aid = getAgentId(ctx);
      const pollerStatus = pollers.get(aid)?.getStatus() ?? null;
      const prefs = prefsManager.load(aid);
      return {
        success: true,
        agentId: aid,
        bus: {
          subscribers: notificationBus.subscriberCount(),
          replySubscribers: notificationBus.replySubscriberCount(),
          transports: notificationBus.listTransports(),
        },
        poller: pollerStatus,
        prefs,
        cache: { envelopesTracked: envelopeCache.size() },
        hint: notificationBus.subscriberCount() === 0 && notificationBus.listTransports().length === 0
          ? '当前没有任何渠道插件订阅通知总线。请确认已加载企微/钉钉等插件，或检查它们的连接状态。'
          : undefined,
      };
    },
  });

  register({
    name: 'odoo_notification_channels',
    description: '列出当前已注册到通知总线的渠道（如企微、钉钉、飞书、webhook）。仅作为信息查询，真正的连接由各渠道插件自己管理。',
    schema: { type: 'object', properties: {} },
    async handler() {
      const transports = notificationBus.listTransports();
      return {
        success: true,
        count: transports.length,
        channels: transports,
        subscribers: notificationBus.subscriberCount(),
      };
    },
  });

  register({
    name: 'odoo_notification_test',
    description: '向通知总线发一条测试 envelope，验证企微/钉钉等渠道是否能收到。用于"测试一下通知"、"看看推送通不通"等。',
    schema: {
      type: 'object',
      properties: {
        title:   { type: 'string', description: '测试标题，默认"辉火云企业套件测试通知"' },
        summary: { type: 'string', description: '测试摘要，默认"这是一条由 odoo 插件发送的测试通知"' },
      },
    },
    async handler(p: { title?: string; summary?: string }, ctx: Record<string, unknown>) {
      const aid = getAgentId(ctx);
      const client = odooClients.get(aid);
      const odooUrl = client?.getSessionInfo().url;
      const envelope: NotificationEnvelope = {
        id: `odoo:${aid}:test:${Date.now()}`,
        source: 'odoo',
        agentId: aid,
        kind: 'message',
        action: 'test',
        priority: 'low',
        title: p.title ?? '辉火云企业套件测试通知',
        summary: p.summary ?? '这是一条由 odoo 插件发送的测试通知',
        body: p.summary ?? '如果你在企微 / 钉钉 / 飞书 里看到这条，说明渠道接通正常。',
        tags: ['odoo', 'test'],
        createdAt: Date.now(),
        origin: { url: odooUrl, model: 'test', resId: 0 },
      };
      await notificationBus.publish(envelope);
      return {
        success: true,
        dispatched: true,
        subscribers: notificationBus.subscriberCount(),
        transports: notificationBus.listTransports().map(t => t.name),
        envelopeId: envelope.id,
        message: notificationBus.subscriberCount() === 0
          ? '已发送，但当前总线没有订阅者 —— 渠道插件可能未加载。'
          : `已发送到 ${notificationBus.subscriberCount()} 个订阅者。`,
      };
    },
  });

  register({
    name: 'odoo_notification_prefs',
    description: '查看或更新当前用户的通知偏好。支持：启停总开关、只接收某些类型（todo/activity/message/email/calendar）、优先级下限、静音时段（24h 制，跨午夜 OK）。不传任何参数只做查询。urgent 级别永远绕过静音与优先级过滤。',
    schema: {
      type: 'object',
      properties: {
        enabled:      { type: 'boolean', description: '通知总开关，false=完全停掉' },
        kinds:        { type: 'array', items: { type: 'string', enum: ['todo','activity','message','email','calendar'] }, description: '允许发的种类，空数组=全开' },
        min_priority: { type: 'string', enum: ['low','normal','high','urgent'], description: '优先级下限，低于此级别的被丢弃（urgent 永远放行）' },
        quiet_start:  { type: 'string', description: '静音起始 HH:MM（传空字符串 "" 清除静音）' },
        quiet_end:    { type: 'string', description: '静音结束 HH:MM' },
        reset:        { type: 'boolean', description: 'true=重置为默认偏好' },
      },
    },
    async handler(
      p: { enabled?: boolean; kinds?: string[]; min_priority?: string; quiet_start?: string; quiet_end?: string; reset?: boolean },
      ctx: Record<string, unknown>,
    ) {
      const aid = getAgentId(ctx);
      if (p.reset) {
        prefsManager.clear(aid);
        return { success: true, agentId: aid, prefs: DEFAULT_PREFS, message: '偏好已重置为默认。' };
      }

      const current = prefsManager.load(aid);
      const patch: Partial<NotificationPreferences> = {};
      if (p.enabled !== undefined) patch.enabled = p.enabled;
      if (Array.isArray(p.kinds)) patch.kinds = p.kinds as NotificationKind[];
      if (p.min_priority) patch.minPriority = p.min_priority as NotificationPriority;
      if (p.quiet_start === '' || p.quiet_end === '') {
        patch.quietHours = undefined;
      } else if (p.quiet_start && p.quiet_end) {
        patch.quietHours = { start: p.quiet_start, end: p.quiet_end };
      }

      if (Object.keys(patch).length === 0) {
        return { success: true, agentId: aid, prefs: current, message: '当前偏好（未变更）' };
      }
      const updated = prefsManager.patch(patch, aid);
      return { success: true, agentId: aid, prefs: updated, message: '通知偏好已更新' };
    },
  });

  register({
    name: 'odoo_notification_reply',
    description: '手动模拟一次从渠道回到辉火云企业套件的入站回复 —— 渠道插件在收到用户回复后应调用这条逻辑（或直接 import notificationBus.reply）。给出 envelope_id + body，辉火云会在对应记录的内部动态里写一条消息。用于排查"企微回复能不能写回系统"。',
    schema: {
      type: 'object',
      properties: {
        envelope_id: { type: 'string', description: '被回复的 envelope id（从 odoo_notification_test 或实际通知里取）' },
        body:        { type: 'string', description: '回复正文（纯文本）' },
        channel:     { type: 'string', description: '渠道标识，默认 "manual"' },
        from_user:   { type: 'string', description: '回复人标识，可选' },
      },
      required: ['envelope_id', 'body'],
    },
    async handler(p: { envelope_id: string; body: string; channel?: string; from_user?: string }) {
      const reply: InboundReply = {
        envelopeId: p.envelope_id,
        channel: p.channel ?? 'manual',
        fromUser: p.from_user,
        body: p.body,
      };
      const result = await notificationBus.reply(reply);
      return { success: result.ok, handled: result.handled, errors: result.errors, message: result.ok ? `回复已分发给 ${result.handled} 个处理器。` : '回复未能成功投递，请检查辉火云企业套件是否连接、envelope_id 是否在缓存中（24h 内、500 条上限）。' };
    },
  });

  // ══════════════════════════════════════════════════════
  // 知识库（knowledge.article）
  // ══════════════════════════════════════════════════════

  register({
    name: 'odoo_knowledge_search',
    description: '搜索 辉火云知识库文章。支持关键词（匹配标题或正文）、分类（workspace/private/shared）、仅收藏、仅顶层、指定父文章。用于"找一下关于 X 的知识库文章"、"列出我收藏的"、"列出工作区顶层文章"。',
    schema: {
      type: 'object',
      properties: {
        keyword:         { type: 'string', description: '关键词，匹配文章标题或正文' },
        category:        { type: 'string', enum: ['workspace','private','shared'], description: '分类：workspace=工作区/private=私有/shared=共享' },
        only_favorite:   { type: 'boolean', description: '只列我收藏的' },
        only_roots:      { type: 'boolean', description: '只列顶层文章（parent_id=空）' },
        parent_id:       { type: 'number', description: '指定父文章 id，列其直接子节点' },
        include_trashed: { type: 'boolean', description: '包含回收站中的文章，默认 false' },
        limit:           { type: 'number', description: '上限，默认 30' },
      },
    },
    async handler(
      p: { keyword?: string; category?: 'workspace'|'private'|'shared'; only_favorite?: boolean; only_roots?: boolean; parent_id?: number; include_trashed?: boolean; limit?: number },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const recs = await client.searchKnowledgeArticles(p);
        return {
          success: true,
          count: recs.length,
          articles: recs.map(r => ({
            id: r['id'],
            name: r['name'],
            icon: r['icon'] || null,
            category: r['category'],
            parent: r['parent_id'],
            root: r['root_article_id'],
            has_children: r['has_article_children'],
            is_favorite: r['is_user_favorite'],
            favorite_count: r['favorite_count'],
            last_edition: r['last_edition_date'],
          })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_knowledge_read',
    description: '读取单篇知识库文章的完整正文（HTML）。用于"把这篇文章读给我"、"X 文章里写了什么"。body 可能较长，渲染时建议截断。',
    schema: {
      type: 'object',
      properties: {
        id:        { type: 'number', description: '文章 id（必填）' },
        plain:     { type: 'boolean', description: 'true=同时返回纯文本摘要（去 HTML）' },
        max_chars: { type: 'number', description: '正文最大字符数，0=不截断，默认 5000' },
      },
      required: ['id'],
    },
    async handler(p: { id: number; plain?: boolean; max_chars?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const rec = await client.readKnowledgeArticle(p.id);
        if (!rec) return { success: false, message: `文章 #${p.id} 不存在` };
        const maxChars = p.max_chars ?? 5000;
        const body = String(rec['body'] ?? '');
        const bodyOut = maxChars > 0 && body.length > maxChars ? body.substring(0, maxChars) + '…' : body;
        const result: Record<string, unknown> = {
          success: true,
          article: {
            id: rec['id'],
            name: rec['name'],
            icon: rec['icon'] || null,
            category: rec['category'],
            parent: rec['parent_id'],
            is_favorite: rec['is_user_favorite'],
            favorite_count: rec['favorite_count'],
            is_locked: rec['is_locked'],
            is_trashed: rec['to_delete'],
            last_edition: rec['last_edition_date'],
            internal_permission: rec['internal_permission'],
            body: bodyOut,
            body_truncated: bodyOut !== body,
          },
        };
        if (p.plain) {
          (result['article'] as Record<string, unknown>)['plain'] = stripHtml(body);
        }
        return result;
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_knowledge_create',
    description: '创建知识库文章。顶层文章必须指定 category（workspace=工作区/private=私有）。子文章传 parent_id，权限继承。body 支持 markdown（自动转 HTML）或直接传 HTML。',
    schema: {
      type: 'object',
      properties: {
        name:      { type: 'string', description: '文章标题' },
        body:      { type: 'string', description: '正文（markdown 或 HTML 皆可，检测到 HTML 标签时原样使用）' },
        icon:      { type: 'string', description: '图标 emoji' },
        parent_id: { type: 'number', description: '父文章 id（创建子文章时必传）' },
        category:  { type: 'string', enum: ['workspace','private','shared'], description: '顶层文章的分类，默认 private' },
      },
    },
    async handler(
      p: { name?: string; body?: string; icon?: string; parent_id?: number; category?: 'workspace'|'private'|'shared' },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const htmlBody = p.body ? mdToHtml(p.body) : '';
        const id = await client.createKnowledgeArticle({
          name: p.name,
          body: htmlBody,
          icon: p.icon,
          parent_id: p.parent_id,
          category: p.category,
        });
        return { success: true, articleId: id, message: `已创建文章 #${id}${p.name ? `「${p.name}」` : ''}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_knowledge_update',
    description: '更新知识库文章的标题、图标或正文。body 支持 markdown，传 HTML 时原样保留。想追加内容请用 odoo_knowledge_append。',
    schema: {
      type: 'object',
      properties: {
        id:   { type: 'number', description: '文章 id（必填）' },
        name: { type: 'string', description: '新标题' },
        body: { type: 'string', description: '新正文（markdown/HTML），覆盖旧内容' },
        icon: { type: 'string', description: '新图标 emoji，传空字符串清除' },
      },
      required: ['id'],
    },
    async handler(p: { id: number; name?: string; body?: string; icon?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.updateKnowledgeArticle(p.id, {
          name: p.name,
          body: p.body !== undefined ? mdToHtml(p.body) : undefined,
          icon: p.icon,
        });
        return { success: true, message: `文章 #${p.id} 已更新` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_knowledge_append',
    description: '在现有文章末尾追加一段内容（markdown 或 HTML）。适合"把刚才讨论的结论写进 X 文章"这种追加笔记的场景，不会覆盖原有内容。',
    schema: {
      type: 'object',
      properties: {
        id:      { type: 'number', description: '文章 id（必填）' },
        content: { type: 'string', description: '要追加的内容（markdown 或 HTML）' },
        with_divider: { type: 'boolean', description: '是否在追加前插入分隔线 <hr>，默认 false' },
      },
      required: ['id', 'content'],
    },
    async handler(p: { id: number; content: string; with_divider?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const html = (p.with_divider ? '<hr>' : '') + mdToHtml(p.content);
        await client.appendKnowledgeArticle(p.id, html);
        return { success: true, message: `已向文章 #${p.id} 追加 ${p.content.length} 字符` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_knowledge_tree',
    description: '展示知识库树结构（以 workspace/private 为根，递归最多 N 层）。用于"给我看下知识库长啥样"、"工作区里都有哪些文章"。',
    schema: {
      type: 'object',
      properties: {
        category:  { type: 'string', enum: ['workspace','private','shared'], description: '根分类，默认 workspace' },
        max_depth: { type: 'number', description: '最大深度，默认 3' },
        max_nodes: { type: 'number', description: '整棵树节点数上限，防爆炸，默认 150' },
      },
    },
    async handler(p: { category?: 'workspace'|'private'|'shared'; max_depth?: number; max_nodes?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const maxDepth = p.max_depth ?? 3;
      const maxNodes = p.max_nodes ?? 150;
      const category = p.category ?? 'workspace';
      try {
        type Node = { id: number; name: string; icon: string | null; is_favorite: boolean; children: Node[] };
        let visited = 0;
        const walk = async (parentId: number | false, depth: number): Promise<Node[]> => {
          if (depth > maxDepth || visited >= maxNodes) return [];
          const items = await client.searchKnowledgeArticles(parentId === false
            ? { category, only_roots: true, limit: 30 }
            : { parent_id: parentId as number, limit: 30 });
          const nodes: Node[] = [];
          for (const it of items) {
            if (visited >= maxNodes) break;
            visited += 1;
            nodes.push({
              id: it['id'] as number,
              name: String(it['name'] ?? ''),
              icon: (it['icon'] as string) || null,
              is_favorite: Boolean(it['is_user_favorite']),
              children: (it['has_article_children'] && depth < maxDepth)
                ? await walk(it['id'] as number, depth + 1)
                : [],
            });
          }
          return nodes;
        };
        const tree = await walk(false, 0);
        return { success: true, category, max_depth: maxDepth, nodes_visited: visited, tree };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_knowledge_favorite',
    description: '切换知识库文章的收藏状态（已收藏→取消，未收藏→收藏）。用于"收藏这篇"、"取消收藏 X"。',
    schema: {
      type: 'object',
      properties: {
        id: { type: 'number', description: '文章 id（必填）' },
      },
      required: ['id'],
    },
    async handler(p: { id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.toggleKnowledgeFavorite(p.id);
        // 回读当前状态返回给用户
        const rec = await client.readKnowledgeArticle(p.id);
        return { success: true, articleId: p.id, is_favorite: rec?.['is_user_favorite'] ?? null, message: `文章 #${p.id} 收藏状态已切换` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_knowledge_trash',
    description: '把文章送入回收站（或还原）。默认删除，restore=true 时恢复。辉火云回收站里的文章在 knowledge_article_trash_limit_days（默认 30 天）后才真正删除，所以是安全操作。',
    schema: {
      type: 'object',
      properties: {
        id:      { type: 'number',  description: '文章 id（必填）' },
        restore: { type: 'boolean', description: 'true=从回收站恢复；默认 false（送入回收站）' },
      },
      required: ['id'],
    },
    async handler(p: { id: number; restore?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        if (p.restore) {
          await client.restoreKnowledgeArticle(p.id);
          return { success: true, message: `文章 #${p.id} 已从回收站恢复` };
        } else {
          await client.trashKnowledgeArticle(p.id);
          return { success: true, message: `文章 #${p.id} 已送入回收站（30 天后物理删除）` };
        }
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ══════════════════════════════════════════════════════
  // v1.7 — Daily Inbox 闭环（活动/关注者/日历/邮件/附件/批量/撤销）
  // ══════════════════════════════════════════════════════

  // ── 活动闭环 ──────────────────────────────────────────
  register({
    name: 'odoo_complete_activity',
    description: '完成一条活动（闭环）。底层调用 mail.activity.action_feedback：活动从列表移除、反馈写入源记录内部动态。用于"那个催付款的活动做完了"、"把提醒 #X 标记完成，附言：客户已转账"。',
    schema: {
      type: 'object',
      properties: {
        activity_id: { type: 'number', description: '活动 id（必填，可通过 odoo_list_activities 查询）' },
        feedback:    { type: 'string', description: '完成反馈（可选，会写入源记录 chatter）' },
      },
      required: ['activity_id'],
    },
    async handler(p: { activity_id: number; feedback?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.completeActivity(p.activity_id, p.feedback);
        return { success: true, message: `活动 #${p.activity_id} 已完成` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_reschedule_activity',
    description: '把活动改到新日期。用于"那个提醒挪到明天"、"推迟到下周一"。需要先有活动 id。',
    schema: {
      type: 'object',
      properties: {
        activity_id:   { type: 'number', description: '活动 id（必填）' },
        date_deadline: { type: 'string', description: '新截止日期 YYYY-MM-DD（必填）' },
      },
      required: ['activity_id', 'date_deadline'],
    },
    async handler(p: { activity_id: number; date_deadline: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_reschedule_activity',
          model: 'mail.activity',
          ids: [p.activity_id],
          values: { date_deadline: p.date_deadline },
          summary: `活动 #${p.activity_id} 改期到 ${p.date_deadline}`,
        });
        return { success: true, message: `活动 #${p.activity_id} 已改到 ${p.date_deadline}（可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 关注者 ────────────────────────────────────────────
  register({
    name: 'odoo_follow',
    description: '关注某条记录（继承 mail.thread 的任何模型：project.task / crm.lead / helpdesk.ticket / sale.order / res.partner 等）。关注后该记录的新消息、活动会出现在 Inbox。不传 partner_ids 时默认关注我自己。',
    schema: {
      type: 'object',
      properties: {
        model:       { type: 'string', description: '数据模型名，如 "project.task"、"crm.lead"（必填）' },
        res_id:      { type: 'number', description: '记录 id（必填）' },
        partner_ids: { type: 'array', items: { type: 'number' }, description: '联系人 id 列表（可选，默认=当前用户的 partner_id）' },
      },
      required: ['model', 'res_id'],
    },
    async handler(p: { model: string; res_id: number; partner_ids?: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.followRecord(p.model, p.res_id, p.partner_ids);
        return { success: true, message: `已关注 ${p.model} #${p.res_id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_unfollow',
    description: '取消关注某条记录。partner_ids 可选，默认取消我自己。',
    schema: {
      type: 'object',
      properties: {
        model:       { type: 'string', description: '数据模型名（必填）' },
        res_id:      { type: 'number', description: '记录 id（必填）' },
        partner_ids: { type: 'array', items: { type: 'number' }, description: '联系人 id 列表（可选，默认=当前用户的 partner_id）' },
      },
      required: ['model', 'res_id'],
    },
    async handler(p: { model: string; res_id: number; partner_ids?: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.unfollowRecord(p.model, p.res_id, p.partner_ids);
        return { success: true, message: `已取消关注 ${p.model} #${p.res_id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 日历增强 ──────────────────────────────────────────
  register({
    name: 'odoo_calendar_today',
    description: '查今日会议/日程（覆盖 00:00–次日 00:00，含我是组织者或参与者）。用于"今天有什么会"、"今天几点开会"。',
    schema: {
      type: 'object',
      properties: {
        limit: { type: 'number', description: '上限，默认 30' },
      },
    },
    async handler(p: { limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const events = await client.getCalendarToday(p);
        return {
          success: true,
          count: events.length,
          events: events.map(e => ({
            id: e['id'], name: e['name'],
            start: e['start'], stop: e['stop'],
            duration: e['duration'], location: e['location'] || null,
            allday: e['allday'], organizer: e['user_id'],
          })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_update_event',
    description: '修改日历事件：改时间、地点、标题、描述、参与者。用于"会议挪到下午 3 点"、"把会议地点改到 301 会议室"。',
    schema: {
      type: 'object',
      properties: {
        event_id:    { type: 'number', description: '事件 id（必填）' },
        name:        { type: 'string', description: '新标题' },
        start:       { type: 'string', description: '新开始时间 YYYY-MM-DD HH:MM:SS' },
        stop:        { type: 'string', description: '新结束时间 YYYY-MM-DD HH:MM:SS' },
        location:    { type: 'string', description: '新地点' },
        description: { type: 'string', description: '新描述' },
        partner_ids: { type: 'array', items: { type: 'number' }, description: '新参与者 partner id 列表（整份替换）' },
      },
      required: ['event_id'],
    },
    async handler(p: { event_id: number; name?: string; start?: string; stop?: string; location?: string; description?: string; partner_ids?: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const values: Record<string, unknown> = {};
      if (p.name !== undefined) values['name'] = p.name;
      if (p.start !== undefined) values['start'] = p.start;
      if (p.stop !== undefined) values['stop'] = p.stop;
      if (p.location !== undefined) values['location'] = p.location;
      if (p.description !== undefined) values['description'] = p.description;
      if (p.partner_ids !== undefined) values['partner_ids'] = [[6, false, p.partner_ids]];
      if (Object.keys(values).length === 0) {
        return { success: true, message: `事件 #${p.event_id} 无需更新（未提供任何字段）` };
      }
      try {
        // partner_ids 的旧值比较复杂（many2many），这里还是走 loggedWrite 让大多数字段可撤销；
        // 如果只是改 partner_ids，快照里会记录原列表的 id 数组，undo 写回也可工作。
        await loggedWrite(client, ctx, {
          tool: 'odoo_update_event',
          model: 'calendar.event',
          ids: [p.event_id],
          values,
          summary: `更新事件 #${p.event_id}（字段：${Object.keys(values).join(', ')}）`,
        });
        return { success: true, message: `事件 #${p.event_id} 已更新（可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_cancel_event',
    description: '取消（归档）日历事件：active=false。数据保留在系统中不物理删除，可用 odoo_undo_last 还原。',
    schema: {
      type: 'object',
      properties: { event_id: { type: 'number', description: '事件 id（必填）' } },
      required: ['event_id'],
    },
    async handler(p: { event_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_cancel_event',
          model: 'calendar.event',
          ids: [p.event_id],
          values: { active: false },
          summary: `取消事件 #${p.event_id}`,
        });
        return { success: true, message: `事件 #${p.event_id} 已取消（active=false，可用 odoo_undo_last 还原）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 邮件 ──────────────────────────────────────────────
  register({
    name: 'odoo_send_email',
    description: '发送邮件（走 mail.mail，立即 send）。recipients 是收件人邮箱数组；body 支持 markdown（自动转 HTML）或 HTML。可选挂到某条 辉火云记录：res_model + res_id。',
    schema: {
      type: 'object',
      properties: {
        subject:        { type: 'string', description: '邮件主题（必填）' },
        body:           { type: 'string', description: '邮件正文（markdown 或 HTML，必填）' },
        recipients:     { type: 'array', items: { type: 'string' }, description: '收件人邮箱列表（必填）' },
        cc:             { type: 'array', items: { type: 'string' }, description: '抄送邮箱列表' },
        bcc:            { type: 'array', items: { type: 'string' }, description: '密送邮箱列表' },
        res_model:      { type: 'string', description: '关联模型（可选，如 "crm.lead"）' },
        res_id:         { type: 'number', description: '关联记录 id（可选）' },
        attachment_ids: { type: 'array', items: { type: 'number' }, description: 'ir.attachment id 列表（可选，先用 odoo_attach_file 或 odoo_document_upload 得到 id）' },
      },
      required: ['subject', 'body', 'recipients'],
    },
    async handler(
      p: { subject: string; body: string; recipients: string[]; cc?: string[]; bcc?: string[]; res_model?: string; res_id?: number; attachment_ids?: number[] },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      if (!p.recipients || p.recipients.length === 0) {
        return { success: false, message: '至少需要一个收件人（recipients）' };
      }
      try {
        const id = await client.sendEmail({
          subject: p.subject,
          bodyHtml: mdToHtml(p.body),
          recipients: p.recipients,
          cc: p.cc,
          bcc: p.bcc,
          res_model: p.res_model,
          res_id: p.res_id,
          attachment_ids: p.attachment_ids,
        });
        return { success: true, mail_id: id, message: `邮件已发送到 ${p.recipients.join(', ')}（mail.mail #${id}）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_email_templates',
    description: '列出邮件模板（mail.template）。可按 model 过滤，如"我有哪些商机相关的邮件模板"。',
    schema: {
      type: 'object',
      properties: {
        model:   { type: 'string', description: '限定模板的 model 字段（如 "crm.lead"）' },
        keyword: { type: 'string', description: '按模板名模糊匹配' },
        limit:   { type: 'number', description: '上限，默认 50' },
      },
    },
    async handler(p: { model?: string; keyword?: string; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const templates = await client.getEmailTemplates(p);
        return {
          success: true,
          count: templates.length,
          templates: templates.map(t => ({
            id: t['id'], name: t['name'],
            model: t['model'], subject: t['subject'],
            email_to: t['email_to'] || null,
            use_default_to: t['use_default_to'],
          })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_email_from_template',
    description: '用模板发邮件（mail.template.send_mail，force_send=true）。用于"用那个报价单模板发给客户"。template_id 从 odoo_email_templates 取。',
    schema: {
      type: 'object',
      properties: {
        template_id:  { type: 'number', description: '模板 id（必填）' },
        res_id:       { type: 'number', description: '目标记录 id，模板会渲染该记录的字段（必填，模板的 model 决定类型）' },
        email_values: { type: 'object', description: '可选的字段覆盖（如 {email_to: "alt@example.com"}）' },
      },
      required: ['template_id', 'res_id'],
    },
    async handler(p: { template_id: number; res_id: number; email_values?: Record<string, unknown> }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const result = await client.sendEmailFromTemplate(p.template_id, p.res_id, {
          force_send: true,
          email_values: p.email_values,
        });
        return { success: true, result, message: `模板 #${p.template_id} 已对 res_id=${p.res_id} 发送` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 附件 / 文档 ───────────────────────────────────────
  register({
    name: 'odoo_attach_file',
    description: '把本地文件上传为辉火云附件（ir.attachment）并挂到指定记录。用于"把这份合同 PDF 附到商机 #42"。path 传本地绝对路径，插件会读文件并 base64 编码。大文件（>5MB）请走 odoo_document_upload。',
    schema: {
      type: 'object',
      properties: {
        path:      { type: 'string', description: '本地文件绝对路径（必填）' },
        res_model: { type: 'string', description: '数据模型，如 "crm.lead"（必填）' },
        res_id:    { type: 'number', description: '记录 id（必填）' },
        name:      { type: 'string', description: '附件显示名（可选，默认=文件名）' },
        mimetype:  { type: 'string', description: 'MIME 类型（可选，默认 application/octet-stream）' },
      },
      required: ['path', 'res_model', 'res_id'],
    },
    async handler(p: { path: string; res_model: string; res_id: number; name?: string; mimetype?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const stat = statSync(p.path);
        if (stat.size > 10 * 1024 * 1024) {
          return { success: false, message: `文件 ${p.path} 大小 ${(stat.size / 1024 / 1024).toFixed(1)}MB，超过附件上限 10MB，请用 odoo_document_upload 传到文档应用` };
        }
        const buf = readFileSync(p.path);
        const datas = buf.toString('base64');
        const id = await client.attachFile({
          res_model: p.res_model,
          res_id: p.res_id,
          name: p.name || basename(p.path),
          datas_base64: datas,
          mimetype: p.mimetype,
        });
        return { success: true, attachment_id: id, size: stat.size, message: `附件 #${id} 已挂到 ${p.res_model} #${p.res_id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_list_attachments',
    description: '列出某条记录挂着的所有附件。用于"商机 #42 有哪些附件"、"那个合同有没有上传"。',
    schema: {
      type: 'object',
      properties: {
        model:  { type: 'string', description: '数据模型名（必填）' },
        res_id: { type: 'number', description: '记录 id（必填）' },
        limit:  { type: 'number', description: '上限，默认 50' },
      },
      required: ['model', 'res_id'],
    },
    async handler(p: { model: string; res_id: number; limit?: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const atts = await client.listAttachments(p.model, p.res_id, { limit: p.limit });
        const info = client.getSessionInfo();
        return {
          success: true,
          count: atts.length,
          attachments: atts.map(a => ({
            id: a['id'], name: a['name'],
            mimetype: a['mimetype'],
            size_bytes: a['file_size'],
            created: a['create_date'],
            created_by: a['create_uid'],
            download_url: `${info.url}/web/content/${a['id']}?download=true`,
          })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_document_upload',
    description: '上传文件到辉火云文档应用（documents.document），可指定 folder_id 归档。用于"把这份交接文档归到项目资料夹"。附件上限 20MB。',
    schema: {
      type: 'object',
      properties: {
        path:      { type: 'string', description: '本地文件绝对路径（必填）' },
        name:      { type: 'string', description: '显示名（默认=文件名）' },
        folder_id: { type: 'number', description: '归档文件夹 id（可选）' },
        tag_ids:   { type: 'array', items: { type: 'number' }, description: '标签 id 列表（可选）' },
        mimetype:  { type: 'string', description: 'MIME 类型（可选）' },
      },
      required: ['path'],
    },
    async handler(p: { path: string; name?: string; folder_id?: number; tag_ids?: number[]; mimetype?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const stat = statSync(p.path);
        if (stat.size > 20 * 1024 * 1024) {
          return { success: false, message: `文件 ${p.path} 大小 ${(stat.size / 1024 / 1024).toFixed(1)}MB，超过上限 20MB` };
        }
        const buf = readFileSync(p.path);
        const datas = buf.toString('base64');
        const id = await client.uploadDocument({
          name: p.name || basename(p.path),
          datas_base64: datas,
          mimetype: p.mimetype,
          folder_id: p.folder_id,
          tag_ids: p.tag_ids,
        });
        return { success: true, document_id: id, size: stat.size, message: `文档 #${id} 已上传到 documents.document` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 批量更新（带变更日志）─────────────────────────────
  register({
    name: 'odoo_bulk_update',
    description: '对同一模型的多条记录做同一组字段更新，写入变更日志，可用 odoo_undo_last 整体撤销。用于"把这批任务都改成已完成"、"这 10 个商机都挪到下一阶段"。谨慎：values 会对所有 ids 生效。',
    schema: {
      type: 'object',
      properties: {
        model:  { type: 'string', description: '数据模型名，如 "project.task"（必填）' },
        ids:    { type: 'array', items: { type: 'number' }, description: '记录 id 列表（必填，至少 1 条）' },
        values: { type: 'object', description: '要写入的字段对象，如 {stage_id: 5, priority: "2"}（必填，至少 1 个字段）' },
      },
      required: ['model', 'ids', 'values'],
    },
    async handler(p: { model: string; ids: number[]; values: Record<string, unknown> }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      if (!p.ids || p.ids.length === 0) return { success: false, message: 'ids 不能为空' };
      if (!p.values || Object.keys(p.values).length === 0) return { success: false, message: 'values 不能为空' };
      if (p.ids.length > 200) return { success: false, message: `一次最多 200 条，当前 ${p.ids.length} 条，拆分后再试` };
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_bulk_update',
          model: p.model,
          ids: p.ids,
          values: p.values,
          summary: `批量更新 ${p.model} × ${p.ids.length} 条（字段：${Object.keys(p.values).join(', ')}）`,
        });
        return {
          success: true,
          updated: p.ids.length,
          model: p.model,
          message: `已更新 ${p.ids.length} 条 ${p.model}（可用 odoo_undo_last 整体撤销）`,
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 撤销上一步 ────────────────────────────────────────
  register({
    name: 'odoo_undo_last',
    description: '撤销上一步可逆的 write（任务/商机/活动改期/事件更新/批量更新/…）。dry_run=true 时只预览不执行；list=true 时列出最近 10 条可撤销变更不执行。注意：只能撤销通过本插件工具做的 write，create/unlink 不在此范围。',
    schema: {
      type: 'object',
      properties: {
        dry_run: { type: 'boolean', description: 'true=只预览将撤销什么，不真正执行' },
        list:    { type: 'boolean', description: 'true=列出最近 10 条可撤销变更，不执行任何撤销' },
      },
    },
    async handler(p: { dry_run?: boolean; list?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const aid = getAgentId(ctx);

      if (p.list) {
        const recent = mutationLog.list(aid, { limit: 10, reversibleOnly: true });
        return {
          success: true,
          count: recent.length,
          entries: recent.map(e => ({
            id: e.id, tool: e.tool, model: e.model,
            ids: e.ids, timestamp: e.timestamp, summary: e.summary,
          })),
          message: recent.length === 0 ? '没有可撤销的变更' : `最近 ${recent.length} 条可撤销变更`,
        };
      }

      const last = mutationLog.findLastReversible(aid);
      if (!last) return { success: false, message: '没有可撤销的变更（mutation-log 为空或全部已撤销）' };

      if (p.dry_run) {
        return {
          success: true,
          preview: true,
          entry: {
            id: last.id, tool: last.tool, model: last.model, ids: last.ids,
            summary: last.summary, timestamp: last.timestamp,
            will_write_back: last.before,
          },
          message: `将撤销：${last.summary}`,
        };
      }

      // 真正撤销：按 id 把 before 快照写回
      const errors: string[] = [];
      let ok = 0;
      for (const snap of last.before) {
        const id = snap['id'] as number;
        const { id: _skip, ...values } = snap;
        void _skip;
        try {
          await client.write(last.model, [id], values);
          ok++;
        } catch (e) {
          errors.push(`#${id}: ${e instanceof Error ? e.message : String(e)}`);
        }
      }
      if (ok > 0) mutationLog.markUndone(aid, last.id);
      return {
        success: errors.length === 0,
        undone: ok,
        failed: errors.length,
        errors: errors.length > 0 ? errors : undefined,
        entry_id: last.id,
        message: errors.length === 0
          ? `已撤销：${last.summary}（${ok} 条记录还原到之前的值）`
          : `部分撤销失败：${ok}/${last.before.length} 成功，${errors.length} 失败`,
      };
    },
  });

  // ══════════════════════════════════════════════════════
  // v1.8 — Project / Ticket / Chatter 闭环
  // ══════════════════════════════════════════════════════

  // ── Chatter 沟通 ──────────────────────────────────────
  register({
    name: 'odoo_message_post',
    description: '在任意 mail.thread 记录（任务/商机/工单/订单/客户等）的 chatter 发评论。会触发邮件通知所有关注者。body 支持 markdown 或 HTML。用于"给客户在商机下留个进度说明"、"在工单里回客户一句"。内部记录（不发邮件）请用 odoo_message_log。',
    schema: {
      type: 'object',
      properties: {
        model:          { type: 'string', description: '数据模型名（必填），如 "crm.lead"、"project.task"、"helpdesk.ticket"' },
        res_id:         { type: 'number', description: '记录 id（必填）' },
        body:           { type: 'string', description: '消息正文（markdown 或 HTML，必填）' },
        subject:        { type: 'string', description: '主题（可选，邮件通知时显示）' },
        partner_ids:    { type: 'array', items: { type: 'number' }, description: '额外 @提及 / 通知的 partner id 列表（可选）' },
        attachment_ids: { type: 'array', items: { type: 'number' }, description: 'ir.attachment id 列表（先用 odoo_attach_file 得到 id）' },
      },
      required: ['model', 'res_id', 'body'],
    },
    async handler(
      p: { model: string; res_id: number; body: string; subject?: string; partner_ids?: number[]; attachment_ids?: number[] },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.postMessage(p.model, p.res_id, {
          bodyHtml: mdToHtml(p.body),
          subject: p.subject,
          partner_ids: p.partner_ids,
          attachment_ids: p.attachment_ids,
          as_log: false,
        });
        return { success: true, message_id: id, message: `已在 ${p.model} #${p.res_id} 发评论（mail.message #${id}，followers 会收到邮件通知）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_message_log',
    description: '在记录 chatter 留内部记录（log note，不发邮件）。用于"给这条记录加个备注"、"记录一下今天的沟通要点"。与 odoo_message_post 的区别：log 不通知 followers。',
    schema: {
      type: 'object',
      properties: {
        model:          { type: 'string', description: '数据模型名（必填）' },
        res_id:         { type: 'number', description: '记录 id（必填）' },
        body:           { type: 'string', description: '备注内容（markdown 或 HTML，必填）' },
        subject:        { type: 'string', description: '标题（可选）' },
        attachment_ids: { type: 'array', items: { type: 'number' }, description: 'ir.attachment id 列表（可选）' },
      },
      required: ['model', 'res_id', 'body'],
    },
    async handler(
      p: { model: string; res_id: number; body: string; subject?: string; attachment_ids?: number[] },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.postMessage(p.model, p.res_id, {
          bodyHtml: mdToHtml(p.body),
          subject: p.subject,
          attachment_ids: p.attachment_ids,
          as_log: true,
        });
        return { success: true, message_id: id, message: `已在 ${p.model} #${p.res_id} 留内部记录（#${id}，不通知 followers）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_message_history',
    description: '读取某条记录的 chatter 沟通历史（最新在前）。用于"这个商机跟进过什么"、"看看工单 #X 有哪些往来"。默认过滤掉系统通知。',
    schema: {
      type: 'object',
      properties: {
        model:                 { type: 'string', description: '数据模型名（必填）' },
        res_id:                { type: 'number', description: '记录 id（必填）' },
        limit:                 { type: 'number', description: '上限，默认 20' },
        include_notifications: { type: 'boolean', description: 'true=包含系统通知（自动关注、阶段变更等），默认 false' },
      },
      required: ['model', 'res_id'],
    },
    async handler(p: { model: string; res_id: number; limit?: number; include_notifications?: boolean }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const msgs = await client.getMessageHistory(p.model, p.res_id, p);
        return {
          success: true,
          count: msgs.length,
          messages: msgs.map(m => ({
            id: m['id'],
            date: m['date'],
            author: m['author_id'],
            email_from: m['email_from'] || null,
            subject: m['subject'] || null,
            type: m['message_type'],
            // 只给纯文本摘要，HTML 全文前端需要再查（避免单次响应爆炸）
            summary: stripHtml(String(m['body'] ?? '')),
          })),
        };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 项目 ──────────────────────────────────────────────
  register({
    name: 'odoo_project_create',
    description: '创建新项目。用于"开个新项目叫 XX"、"给客户 Y 建个实施项目"。privacy_visibility 决定可见范围：followers=仅关注者/employees=全体员工（默认）/portal=门户用户。',
    schema: {
      type: 'object',
      properties: {
        name:               { type: 'string', description: '项目名（必填）' },
        partner_id:         { type: 'number', description: '客户 partner id（可选）' },
        user_id:            { type: 'number', description: '项目负责人 user id（可选，默认=当前用户）' },
        date_start:         { type: 'string', description: '开始日期 YYYY-MM-DD' },
        date:               { type: 'string', description: '结束日期 YYYY-MM-DD' },
        description:        { type: 'string', description: '项目描述' },
        privacy_visibility: { type: 'string', enum: ['followers', 'employees', 'portal'], description: '可见范围' },
      },
      required: ['name'],
    },
    async handler(
      p: { name: string; partner_id?: number; user_id?: number; date_start?: string; date?: string; description?: string; privacy_visibility?: 'followers' | 'employees' | 'portal' },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createProject(p);
        return { success: true, project_id: id, message: `项目 #${id}（${p.name}）已创建` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_project_update',
    description: '更新项目字段：名称/负责人/起止日期/描述/归档等。支持 odoo_undo_last 撤销。',
    schema: {
      type: 'object',
      properties: {
        project_id:  { type: 'number', description: '项目 id（必填）' },
        name:        { type: 'string', description: '新名称' },
        user_id:     { type: 'number', description: '新负责人 user id' },
        partner_id:  { type: 'number', description: '新客户 partner id' },
        date_start:  { type: 'string', description: '新开始日期 YYYY-MM-DD' },
        date:        { type: 'string', description: '新结束日期 YYYY-MM-DD' },
        description: { type: 'string', description: '新描述' },
        active:      { type: 'boolean', description: 'active=false 归档项目' },
      },
      required: ['project_id'],
    },
    async handler(
      p: { project_id: number; name?: string; user_id?: number; partner_id?: number; date_start?: string; date?: string; description?: string; active?: boolean },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const values: Record<string, unknown> = {};
      if (p.name !== undefined) values['name'] = p.name;
      if (p.user_id !== undefined) values['user_id'] = p.user_id;
      if (p.partner_id !== undefined) values['partner_id'] = p.partner_id;
      if (p.date_start !== undefined) values['date_start'] = p.date_start || false;
      if (p.date !== undefined) values['date'] = p.date || false;
      if (p.description !== undefined) values['description'] = p.description;
      if (p.active !== undefined) values['active'] = p.active;
      if (Object.keys(values).length === 0) {
        return { success: true, message: `项目 #${p.project_id} 无需更新（未提供任何字段）` };
      }
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_project_update',
          model: 'project.project',
          ids: [p.project_id],
          values,
          summary: `更新项目 #${p.project_id}（字段：${Object.keys(values).join(', ')}）`,
        });
        return { success: true, message: `项目 #${p.project_id} 已更新（可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 里程碑 ────────────────────────────────────────────
  register({
    name: 'odoo_milestone_create',
    description: '为项目新建里程碑。用于"给项目 X 加一个 9 月底的交付里程碑"。',
    schema: {
      type: 'object',
      properties: {
        name:       { type: 'string', description: '里程碑名称（必填）' },
        project_id: { type: 'number', description: '所属项目 id（必填）' },
        deadline:   { type: 'string', description: '截止日期 YYYY-MM-DD' },
      },
      required: ['name', 'project_id'],
    },
    async handler(p: { name: string; project_id: number; deadline?: string }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        const id = await client.createMilestone(p);
        return { success: true, milestone_id: id, message: `里程碑 #${id}（${p.name}）已创建于项目 #${p.project_id}` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_milestone_done',
    description: '把里程碑标记为完成（写 is_reached=true + reached_date=today）。支持 odoo_undo_last 撤销。',
    schema: {
      type: 'object',
      properties: { milestone_id: { type: 'number', description: '里程碑 id（必填）' } },
      required: ['milestone_id'],
    },
    async handler(p: { milestone_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_milestone_done',
          model: 'project.milestone',
          ids: [p.milestone_id],
          values: { is_reached: true, reached_date: today() },
          summary: `里程碑 #${p.milestone_id} 标记为已完成`,
        });
        return { success: true, message: `里程碑 #${p.milestone_id} 已完成（reached_date=${today()}，可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 任务指派 ──────────────────────────────────────────
  register({
    name: 'odoo_task_assign',
    description: '指派一条或多条任务给一个/一批人（整份替换 user_ids）。用于"把这批任务都交给张三"、"加上李四一起做"。支持 odoo_undo_last 撤销。',
    schema: {
      type: 'object',
      properties: {
        task_ids: { type: 'array', items: { type: 'number' }, description: '任务 id 列表（必填，至少 1 条）' },
        user_ids: { type: 'array', items: { type: 'number' }, description: 'user id 列表（必填，整份替换）' },
      },
      required: ['task_ids', 'user_ids'],
    },
    async handler(p: { task_ids: number[]; user_ids: number[] }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      if (!p.task_ids || p.task_ids.length === 0) return { success: false, message: 'task_ids 不能为空' };
      if (!p.user_ids) return { success: false, message: 'user_ids 必填（传空数组表示清空）' };
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_task_assign',
          model: 'project.task',
          ids: p.task_ids,
          values: { user_ids: [[6, false, p.user_ids]] },
          summary: `指派 ${p.task_ids.length} 条任务给 user(${p.user_ids.join(',')})`,
        });
        return { success: true, updated: p.task_ids.length, message: `${p.task_ids.length} 条任务已指派（可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 工单闭环 ──────────────────────────────────────────
  register({
    name: 'odoo_ticket_update',
    description: '更新工单字段：名称/阶段/优先级/负责人/看板状态/截止。支持 odoo_undo_last 撤销。',
    schema: {
      type: 'object',
      properties: {
        ticket_id:    { type: 'number', description: '工单 id（必填）' },
        name:         { type: 'string', description: '新主题' },
        stage_id:     { type: 'number', description: '新阶段 id' },
        priority:     { type: 'string', enum: ['0', '1', '2', '3'], description: '0=普通 1=中 2=高 3=紧急' },
        user_id:      { type: 'number', description: '新负责人 user id' },
        kanban_state: { type: 'string', enum: ['normal', 'done', 'blocked'], description: '看板状态' },
        sla_deadline: { type: 'string', description: '新 SLA 截止时间 YYYY-MM-DD HH:MM:SS' },
      },
      required: ['ticket_id'],
    },
    async handler(
      p: { ticket_id: number; name?: string; stage_id?: number; priority?: string; user_id?: number; kanban_state?: string; sla_deadline?: string },
      ctx: Record<string, unknown>,
    ) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      const values: Record<string, unknown> = {};
      if (p.name !== undefined) values['name'] = p.name;
      if (p.stage_id !== undefined) values['stage_id'] = p.stage_id;
      if (p.priority !== undefined) values['priority'] = p.priority;
      if (p.user_id !== undefined) values['user_id'] = p.user_id;
      if (p.kanban_state !== undefined) values['kanban_state'] = p.kanban_state;
      if (p.sla_deadline !== undefined) values['sla_deadline'] = p.sla_deadline || false;
      if (Object.keys(values).length === 0) {
        return { success: true, message: `工单 #${p.ticket_id} 无需更新（未提供任何字段）` };
      }
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_ticket_update',
          model: 'helpdesk.ticket',
          ids: [p.ticket_id],
          values,
          summary: `更新工单 #${p.ticket_id}（字段：${Object.keys(values).join(', ')}）`,
        });
        return { success: true, message: `工单 #${p.ticket_id} 已更新（可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_ticket_close',
    description: '关闭工单：把 stage_id 改到该团队 fold=true 的第一个阶段（= 关闭列）。如果找不到关闭阶段会报错让用户先建一个。支持 odoo_undo_last 撤销。',
    schema: {
      type: 'object',
      properties: {
        ticket_id: { type: 'number', description: '工单 id（必填）' },
      },
      required: ['ticket_id'],
    },
    async handler(p: { ticket_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        // 先读 ticket 拿 team_id，再在 team 下找 fold=true 的阶段
        const tks = await client.read('helpdesk.ticket', [p.ticket_id], ['team_id', 'stage_id']);
        const t = tks[0];
        if (!t) return { success: false, message: `工单 #${p.ticket_id} 不存在` };
        const teamRef = t['team_id'];
        const teamId = Array.isArray(teamRef) && typeof teamRef[0] === 'number' ? teamRef[0] : undefined;
        const closedStage = await client.findHelpdeskClosedStage(teamId);
        if (!closedStage) {
          return { success: false, message: `团队 ${teamId ?? '(unset)'} 下找不到 fold=true 的关闭阶段。请先到辉火云客服应用里给这个团队建一个"已完成"阶段（fold=true）。` };
        }
        await loggedWrite(client, ctx, {
          tool: 'odoo_ticket_close',
          model: 'helpdesk.ticket',
          ids: [p.ticket_id],
          values: { stage_id: closedStage['id'] as number, kanban_state: 'done' },
          summary: `关闭工单 #${p.ticket_id}（stage_id → ${String(closedStage['name'])}）`,
        });
        return { success: true, stage: closedStage['name'], message: `工单 #${p.ticket_id} 已关闭（stage=${String(closedStage['name'])}，可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_ticket_assign',
    description: '指派工单给某位工程师。支持 odoo_undo_last 撤销。',
    schema: {
      type: 'object',
      properties: {
        ticket_id: { type: 'number', description: '工单 id（必填）' },
        user_id:   { type: 'number', description: '新负责人 user id（必填）' },
      },
      required: ['ticket_id', 'user_id'],
    },
    async handler(p: { ticket_id: number; user_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await loggedWrite(client, ctx, {
          tool: 'odoo_ticket_assign',
          model: 'helpdesk.ticket',
          ids: [p.ticket_id],
          values: { user_id: p.user_id },
          summary: `指派工单 #${p.ticket_id} 给 user #${p.user_id}`,
        });
        return { success: true, message: `工单 #${p.ticket_id} 已指派给 user #${p.user_id}（可用 odoo_undo_last 撤销）` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // ── 审批动作 ──────────────────────────────────────────
  register({
    name: 'odoo_approval_approve',
    description: '作为审批人批准一条审批请求（调 approval.request.action_approve）。用于"批了这条请假/采购申请"。注意：只能操作你本人是审批人的请求。',
    schema: {
      type: 'object',
      properties: { request_id: { type: 'number', description: '审批请求 id（必填）' } },
      required: ['request_id'],
    },
    async handler(p: { request_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.approveApprovalRequest(p.request_id);
        return { success: true, message: `审批请求 #${p.request_id} 已批准` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  register({
    name: 'odoo_approval_refuse',
    description: '作为审批人拒绝审批请求（调 approval.request.action_refuse）。用于"驳回这条申请"。',
    schema: {
      type: 'object',
      properties: { request_id: { type: 'number', description: '审批请求 id（必填）' } },
      required: ['request_id'],
    },
    async handler(p: { request_id: number }, ctx: Record<string, unknown>) {
      const client = getClient(ctx);
      if (!client) return notConnected();
      try {
        await client.refuseApprovalRequest(p.request_id);
        return { success: true, message: `审批请求 #${p.request_id} 已拒绝` };
      } catch (e) { return { success: false, message: String(e) }; }
    },
  });

  // v1.19.0 ⭐ 按需查工具（替代 system context 中的 7900 字工具表注入）
  // 不依赖 client 连接 — 即使 odoo 未连接，LLM 也能查工具表得知能做什么
  register({
    name: 'odoo_help',
    description: '按需查看辉火云企业套件全部 189 个工具的分类速查、自然语言映射表和数据模型清单。无参数 = 返回完整表（约 7900 字 / 2000 tokens）；传 keyword = 模糊匹配工具名/中文意图（如 "请假"/"task"/"CRM"/"知识库"）。LLM 不知道某个意图对应哪个工具时调此工具按需获取详细信息，避免每次 prompt 都注入完整工具表。',
    schema: {
      type: 'object',
      properties: {
        keyword: {
          type: 'string',
          description: '可选。模糊匹配工具名或中文意图（不区分大小写，按行匹配）。例如 "请假" 返回所有请假相关工具行；"CRM" 返回 CRM 分类。不传则返回完整工具表。',
        },
      },
    },
    async handler(params: { keyword?: string }) {
      const kw = params.keyword?.trim();
      if (!kw) {
        return {
          success: true,
          content: ODOO_HELP_TEXT,
          hint: '完整工具表已返回。下次可传 keyword 缩小范围（如 keyword="请假" 仅返回请假相关行）。',
        };
      }
      const lowerKw = kw.toLowerCase();
      const lines = ODOO_HELP_TEXT.split('\n');
      const matched = lines.filter(line => line.toLowerCase().includes(lowerKw));
      if (matched.length === 0) {
        return {
          success: false,
          message: `没有匹配 "${kw}" 的工具。试试调 odoo_help（不传 keyword）查看完整表，或换个关键词（如 "task"/"CRM"/"知识库"/"HR"）。`,
        };
      }
      return {
        success: true,
        keyword: kw,
        matchedLines: matched.length,
        content: matched.join('\n'),
      };
    },
  });

  if (tier === 'extended') {
    api.logger.info(`[odoo] ${registeredCount} 个工具已注册（v1.20 — tier=extended 全量 204 工具；v1.20 新增审批发起+克隆/导入+Mail 关注+资源工作时间+报表订阅+多语言读 14 个；含 v1.19 odoo_help、v1.18 Studio 元编程+审计+多公司）`);
  } else {
    api.logger.info(
      `[odoo] ${registeredCount} 个工具已注册（v1.20 — tier=${tier} 精简档位 / 跳过 ${skippedCount} 个不在 ${tier} 集合内的工具，节省 ~${Math.round(skippedCount * 80)} tokens schema）。完整 204 工具调 odoo_help 查；改 ~/.openclaw/openclaw.json 的 plugins.entries.odoo.config.tier="extended" 可恢复全量。`
    );
  }
}

// ── 注册 before_prompt_build 钩子 ─────────────────────────────────────────────
function registerHooks(api: OpenClawPluginApi) {
  api.on('before_prompt_build', async (_event: unknown, ctx: unknown) => {
    const aid = (ctx as { agentId?: string } | undefined)?.agentId?.trim() ?? 'default';
    const todayStr = today();
    const tomorrowStr = tomorrow();

    // v1.21.0: 只查内存缓存，**不再走 RPC**。
    // 旧版 v1.20-：每次 before_prompt_build 都调 tryRestoreAgent → 内部走
    // OdooClient.authenticate() RPC fetch（无 timeout）→ odoo 后端慢就阻塞 →
    // OpenClaw gateway 默认 15s timeout 强行掐断 → 用户实测首字延迟 P50=16.4s。
    // hook 是高频路径（每次 LLM prompt 构建前都触发），绝不能做重 IO。
    // 凭据恢复改成：① register() 启动期 fire-and-forget 预热 default agent；
    //              ② 用户主动调 odoo_connect 工具；
    //              ③ rpc() 加 AbortSignal.timeout(3000) 兜底（防其他路径再卡）。
    const client = odooClients.get(aid);

    if (!client?.isAuthenticated()) {
      const hasShared = configManager.hasSharedConfig();
      return {
        appendSystemContext: `
## 辉火云企业套件插件 — 未连接

> **品牌口径（硬规则）**：对外沟通时一律称"辉火云企业套件"或"辉火云"。
> 不得出现"Odoo"、"欧度"或任何第三方 ERP 商标；内部模型名（如 project.task）
> 和工具名（odoo_xxx）是技术标识符，仅在调试说明里出现，不要在面向用户的
> 正文里直接朗读。

> **凭据隔离规则（v1.23 默认反转）**：v1.23 起 odoo_connect **默认按当前
> sender_id 隔离**保存（每个企微/钉钉/飞书成员配自己的辉火云账号），与 Odoo
> 内部 RBAC 对齐 —— 销售看销售的数据，管理员看管理员的数据，权限不混淆。
> **绝不要主动建议"配一次全员共用"**，那会让 Odoo RBAC 失效（所有人看到的
> 数据完全一样，违背权限隔离初衷）。仅当用户明确说"组织内大家共用一个公共
> 只读账号"时，才用 odoo_connect(shared=true) 写入全员 fallback。

插件已加载，当前 agent (\`${aid}\`) 尚未连接到辉火云企业套件${hasShared ? '（组织有 shared fallback，但建议本 sender_id 配自己的账号以获得对应权限）' : ''}。当用户提到任何 ERP 相关操作（待办、任务、商机、客户、订单、工单、发票、会议、提醒、项目、工时、库存、员工、审批等），你应该：

1. **首先说明**："要使用辉火云企业套件，告诉我你的辉火云账号信息。每个同事用自己的账号，权限按你的 Odoo 角色区分（销售看销售的、管理员看管理员的）。"
2. 询问：
   - **公司系统地址**（URL）：例如 https://www.huo15.com
   - **用户名**（邮箱或登录名）
   - **密码**
3. **数据库名不需要主动询问** — odoo_connect 会自动检测（单库自动选、多库返列表）
4. 收集到 URL、用户名、密码后，调用 **odoo_connect**（默认就是 sender_id 隔离，不需要传 shared）
5. **绝不要**主动说"配一次全员通用"或"组织内所有同事都能用"。每个 sender_id 配自己的，是 v1.23 默认行为，也是用户期望的权限模型
6. 仅当用户明确说"我们组织共用一个 Odoo 公共账号"时才传 \`shared: true\`

示例引导话术："要使用辉火云企业套件，请告诉我你的账号：1) 系统地址 2) 用户名 3) 密码。每位同事用自己的账号配一次，系统按你的 Odoo 角色给权限。"

---

## 附件 / 文件内容判断 — 硬规则

> 用户上传压缩包/文档/Excel 让你建商机、创建任务、写工单等操作时：
>
> 1. **附件内容由用户负责**。不要解读"内容是不是跟商机字段对得上"、"这文件像不像 ERP 数据"。即便附件是工厂排产、菜单、随便一个 PDF，也直接按用户意图建记录。
> 2. 解压/读附件**仅用于提取用户明示的字段**（如用户说"客户名取里面表头第一行"），不主动做"内容相符性"判断后打回用户。
> 3. **正确的工作流**：先根据用户口头说的字段（公司名/金额/阶段等）调 \`odoo_crm_create\` 建商机 → 再用 \`odoo_attach_file\` 把附件挂到该 crm.lead → 完成回报"商机 #X 已创建并附上文件"。
> 4. 用户没说要看附件内容时**绝不主动解析后质疑**用户。常见错误回复：「我解压出来的内容跟商机对不上，你发错了吗？」 ❌ —— 这是越权。
> 5. 只有用户**明确问**"这附件是什么"时才解读内容。`.trim(),
      };
    }

    const info = client.getSessionInfo();
    const credSource = configManager.getActiveSource(aid);
    const credSourceLabel = credSource === 'agent' ? '当前 sender_id 专属凭据（推荐）'
      : credSource === 'shared' ? '组织共享 fallback 凭据（全员共用同一账号，Odoo RBAC 失效）'
      : credSource === 'legacy' ? '历史遗留凭据'
      : 'manifest 静态预填';
    return {
      appendSystemContext: `
## 辉火云企业套件 已连接

> **品牌口径**：对外称"辉火云企业套件"或"辉火云"，禁出现"Odoo"等第三方 ERP 商标。技术标识符（odoo_*、project.task）仅在调试里出现，面向用户的正文用中文业务术语（"任务"/"商机"/"工单"/"内部动态"）。

> **凭据隔离规则（v1.23 默认反转）**：当前凭据来源【${credSourceLabel}】。
> v1.23 起 odoo_connect 默认 sender_id 隔离（每人自己一份），与 Odoo 内部 RBAC 对齐。已连接后**不要再问 URL/用户名/密码**。
> 若 credSource=shared 且用户问"为什么权限不区分"——告诉他可以让每个同事各自调 odoo_connect 配自己账号即可（默认就是 sender_id 隔离，会覆盖 shared fallback）。
> 用户要换凭据时调 odoo_connect（默认就是 sender_id 隔离，不需要传 shared）；用户问"为什么没问密码"时调 odoo_whoami。

> **附件硬规则**：用户上传文件让你建商机/任务/工单时，**附件内容由用户负责**，不解读"内容是否相符"打回用户。直接按用户口头字段建记录 → \`odoo_attach_file\` 挂附件 → 回报完成。常见错误「解压看到内容跟商机对不上你发错了吗」❌ 是越权，绝不要这样答。

**用户：** ${info.username}（uid: ${info.uid}）| **系统：** ${info.url} | **agent：** ${aid}
**凭据来源：** ${credSourceLabel}
**今日：** ${todayStr} | **明日：** ${tomorrowStr}

### 高频工具（直接调用，识别意图后即用）

- 任务/活动：odoo_create_task / odoo_list_tasks / odoo_my_today / odoo_my_workload / odoo_create_activity / odoo_calendar_today
- CRM：odoo_crm_pipeline / odoo_crm_create / odoo_crm_won / odoo_crm_lost
- 项目：odoo_project_overview / odoo_timesheet_log
- 客服：odoo_tickets / odoo_ticket_create
- 财务：odoo_invoices / odoo_sale_orders / odoo_purchase_orders
- 联系人：odoo_contacts / odoo_contact_create
- 检索：odoo_search / odoo_daily_briefing
- 状态：odoo_whoami / odoo_disconnect

> **当前 tier=core（默认 30 个高频工具直接可见）。完整 190 个工具**（v1.18 含 HR / 库存 / 生产 / Studio 元编程 / 审计等深度场景）：调 \`odoo_help\`（无参 = 完整表；可传 keyword="请假"/"task"/"CRM"/"知识库" 等模糊匹配）按需获取。
> v1.20 起每次 prompt 节省 ~2000 字 system context + ~14000 tokens 工具 schema = **~16000 tokens 总省**。如需恢复 v1.18 全量行为：改 \`~/.openclaw/openclaw.json\` 的 \`plugins.entries.odoo.config.tier="extended"\`。

### 日期 & 字段规范

- date：YYYY-MM-DD（今天=${todayStr}，明天=${tomorrowStr}）
- datetime：YYYY-MM-DD HH:MM:SS（默认上午 09:00:00，下午 14:00:00）
- 优先级：0=普通 / 1=中 / 2=高 / 3=紧急
- Many2one 读返 [id, "名称"]，写传数字 id
- 阶段查 odoo_search(model="crm.stage") / 活动类型查 odoo_activity_types

### 常用数据模型

project.task · project.project · crm.lead · sale.order · purchase.order · helpdesk.ticket · account.move · res.partner · hr.employee · hr.leave · stock.picking · knowledge.article · mail.activity · calendar.event
`.trim(),
    };
  });

  api.logger.info('[odoo] before_prompt_build 钩子已注册（per-agent 隔离 / v1.19 system context 已瘦身 ~6500 字 → 调 odoo_help 按需取详）');
}

// ── 处理后端更新通知 ──────────────────────────────────────────────────────────
/**
 * 辉火云企业套件事件 → NotificationEnvelope → 全局通知总线
 *
 * 流程：
 *   1. 应用 per-agent 偏好（enabled / kinds / minPriority / quietHours）
 *   2. 缓存 envelope 溯源信息（供入站回复时定位 辉火云记录）
 *   3. publish 到 bus，渠道插件决定投递细节
 *
 * 本方法不感知具体渠道。
 */
function handleOdooUpdates(api: OpenClawPluginApi, updates: SyncUpdate[], aid: string) {
  if (updates.length === 0) return;

  const prefs = prefsManager.load(aid);
  const odooUrl = odooClients.get(aid)?.getSessionInfo().url;

  let dispatched = 0;
  let filtered = 0;
  for (const u of updates) {
    const env = toEnvelope(u, aid, odooUrl);
    const decision = shouldDeliver(env, prefs);
    if (!decision.deliver) {
      filtered += 1;
      api.logger.debug?.(`[odoo] agent=${aid} 丢弃 ${env.id}: ${decision.reason}`);
      continue;
    }

    // 记录 envelope → 原记录 映射，以便回复时可以写回 chatter
    if (env.origin?.model && env.origin?.resId) {
      envelopeCache.set(env.id, {
        agentId: aid,
        model: env.origin.model,
        resId: env.origin.resId,
      });
    }

    notificationBus.publish(env).catch(err => {
      api.logger.error(`[odoo] bus publish 失败 ${env.id}: ${err instanceof Error ? err.message : String(err)}`);
    });
    dispatched += 1;
  }

  const subs = notificationBus.subscriberCount();
  const transports = notificationBus.listTransports().map(t => t.name).join(',') || '无';
  api.logger.info(
    `[odoo] agent=${aid} 发布 ${dispatched}/${updates.length} 条（过滤 ${filtered}，订阅者=${subs}，渠道=${transports}）`,
  );
}

// ── 处理入站回复（渠道 → 辉火云内部动态）──────────────────────────────────────
async function handleInboundReply(api: OpenClawPluginApi, reply: InboundReply): Promise<void> {
  const origin = envelopeCache.get(reply.envelopeId);
  if (!origin) {
    api.logger.warn?.(`[odoo] 入站回复找不到 envelope 溯源: ${reply.envelopeId}（来自 ${reply.channel}）`);
    return;
  }
  if (!origin.model || !origin.resId) {
    api.logger.warn?.(`[odoo] envelope ${reply.envelopeId} 无可写回目标（缺 model/resId）`);
    return;
  }

  const client = odooClients.get(origin.agentId);
  if (!client?.isAuthenticated()) {
    api.logger.warn?.(`[odoo] agent=${origin.agentId} 未连接，忽略回复 ${reply.envelopeId}`);
    return;
  }

  const bodyHtml = reply.html
    ? reply.html
    : `<p>${escapeHtml(reply.body)}</p>`;
  const subject = `来自 ${reply.channel}${reply.fromUser ? ` / ${reply.fromUser}` : ''} 的回复`;

  try {
    const id = await client.call('mail.message', 'create', [{
      model: origin.model,
      res_id: origin.resId,
      body: bodyHtml,
      subject,
      message_type: 'comment',
      subtype_xmlid: 'mail.mt_comment',
    }]);
    api.logger.info(`[odoo] 入站回复已写入 ${origin.model}#${origin.resId}（mail.message ${String(id)}）`);
  } catch (e) {
    api.logger.error(`[odoo] 写回辉火云内部动态失败: ${e instanceof Error ? e.message : String(e)}`);
  }
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
