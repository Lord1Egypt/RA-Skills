/**
 * Odoo JSON-RPC API 客户端 — v1.1
 *
 * 支持 Odoo 19 Enterprise 的 JSON-RPC 接口。
 * 覆盖模块：Session、Project、CRM、Sale、Purchase、
 *           Helpdesk、Accounting、HR、Stock、Mail/Activity
 */

import type { OdooConfig, OdooSession, OdooRecord, OdooError } from '../types/index.js';
import { today, tomorrow } from '../utils/date-utils.js';

/**
 * v1.21.0: RPC fetch timeout 上限（3 秒）。
 *
 * 背景：用户实测首字延迟 P50=16.4s/P95=54.9s，gateway.err.log 唯一报 timeout
 * 的是 odoo `before_prompt_build` hook（每次 LLM prompt 构建前尝试 RPC 认证恢复，
 * fetch 无 timeout 控制 → odoo 后端慢就阻塞 → OpenClaw gateway 默认 15s timeout
 * 强行掐断）。3s 快速失败让上游 hook 拿到错误立即 fallback 到"未连接"提示，
 * 而非死等 15s。常态 Odoo RPC <500ms，3s 留 6x 余量足够。
 */
const RPC_TIMEOUT_MS = 3000;

type DomainItem = string | [string, string, unknown];
type Domain = DomainItem[];

function isOdooError(result: unknown): result is { error: OdooError } {
  return typeof result === 'object' && result !== null && 'error' in result;
}

export class OdooClient {
  private url: string;
  private db: string;
  private username: string;
  private password: string;
  private uid: number | null = null;
  private session_id: string | null = null;
  private user_context: Record<string, unknown> = {};

  constructor(config: OdooConfig) {
    this.url = config.url.replace(/\/$/, '');
    this.db = config.db;
    this.username = config.username;
    this.password = config.password;
  }

  // ==================== 会话管理 ====================

  async authenticate(): Promise<OdooSession> {
    const result = await this.rpc('/web/session/authenticate', {
      db: this.db,
      login: this.username,
      password: this.password,
    });

    if (isOdooError(result)) {
      throw new Error(`认证失败: ${JSON.stringify(result.error)}`);
    }

    const session = result as OdooSession;
    if (!session.uid) throw new Error('认证失败：用户名或密码错误');

    this.uid = session.uid;
    this.session_id = (session as unknown as Record<string, unknown>).session_id as string | null ?? null;
    this.user_context = session.user_context || {};
    return session;
  }

  async checkSession(): Promise<boolean> {
    try {
      const result = await this.rpc('/web/session/get_session_info', {});
      const r = result as Record<string, unknown>;
      return 'uid' in r && r['uid'] !== false && r['uid'] !== null;
    } catch {
      return false;
    }
  }

  async ensureAuthenticated(): Promise<void> {
    if (!this.isAuthenticated() || !(await this.checkSession())) {
      await this.authenticate();
    }
  }

  async destroy(): Promise<void> {
    try { await this.rpc('/web/session/destroy', {}); } finally {
      this.uid = null; this.session_id = null; this.user_context = {};
    }
  }

  isAuthenticated(): boolean { return this.uid !== null; }
  getUid(): number | null { return this.uid; }

  /**
   * 查询 Odoo 实例可用的数据库列表（无需认证）
   * Odoo 19 端点: POST /web/database/list
   */
  static async listDatabases(url: string): Promise<string[]> {
    const endpoint = `${url.replace(/\/$/, '')}/web/database/list`;
    const payload = { jsonrpc: '2.0', method: 'call', id: Date.now(), params: {} };
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(RPC_TIMEOUT_MS),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    const data = await response.json() as { result?: string[]; error?: unknown };
    if (data.error) throw new Error(`获取数据库列表失败: ${JSON.stringify(data.error)}`);
    return data.result ?? [];
  }
  getSessionInfo(): { uid: number | null; username: string; url: string } {
    return { uid: this.uid, username: this.username, url: this.url };
  }

  // ==================== 通用 ORM ====================

  async searchRead(
    model: string, domain: Domain, fields: string[] = ['id', 'name'],
    options: { limit?: number; offset?: number; order?: string } = {},
  ): Promise<{ length: number; records: OdooRecord[] }> {
    const { limit = 100, offset = 0, order = '' } = options;
    const result = await this.rpc('/web/dataset/call_kw', {
      model, method: 'search_read', args: [domain],
      kwargs: { fields, domain, limit, offset, order },
    });
    if (isOdooError(result)) throw new Error(`查询 ${model} 失败: ${JSON.stringify(result.error)}`);
    const records = Array.isArray(result) ? result as OdooRecord[] : [];
    return { length: records.length, records };
  }

  async read(model: string, ids: number[], fields: string[] = ['id', 'name']): Promise<OdooRecord[]> {
    const result = await this.rpc('/web/dataset/call_kw', { model, method: 'read', args: [ids], kwargs: { fields } });
    if (isOdooError(result)) throw new Error(`读取 ${model} 失败: ${JSON.stringify(result.error)}`);
    return result as OdooRecord[];
  }

  async create(model: string, values: Record<string, unknown>): Promise<number> {
    const result = await this.rpc('/web/dataset/call_kw', { model, method: 'create', args: [values], kwargs: {} });
    if (isOdooError(result)) throw new Error(`创建 ${model} 失败: ${JSON.stringify(result.error)}`);
    return result as number;
  }

  async write(model: string, ids: number[], values: Record<string, unknown>): Promise<boolean> {
    const result = await this.rpc('/web/dataset/call_kw', { model, method: 'write', args: [ids, values], kwargs: {} });
    if (isOdooError(result)) throw new Error(`更新 ${model} 失败: ${JSON.stringify(result.error)}`);
    return result === true;
  }

  async unlink(model: string, ids: number[]): Promise<boolean> {
    const result = await this.rpc('/web/dataset/call_kw', { model, method: 'unlink', args: [ids], kwargs: {} });
    if (isOdooError(result)) throw new Error(`删除 ${model} 失败: ${JSON.stringify(result.error)}`);
    return result === true;
  }

  async searchCount(model: string, domain: Domain): Promise<number> {
    const result = await this.rpc('/web/dataset/call_kw', { model, method: 'search_count', args: [domain], kwargs: {} });
    if (isOdooError(result)) throw new Error(`计数 ${model} 失败: ${JSON.stringify(result.error)}`);
    return result as number;
  }

  async call(model: string, method: string, args: unknown[] = [], kwargs: Record<string, unknown> = {}): Promise<unknown> {
    const result = await this.rpc('/web/dataset/call_kw', { model, method, args, kwargs });
    if (isOdooError(result)) throw new Error(`调用 ${model}.${method} 失败: ${JSON.stringify(result.error)}`);
    return result;
  }

  // ==================== Project / Task ====================

  async createTask(values: {
    name: string; description?: string; project_id?: number;
    date_deadline?: string; user_ids?: number[]; priority?: '0' | '1' | '2' | '3';
  }): Promise<number> {
    return this.create('project.task', {
      name: values.name,
      description: values.description || '',
      project_id: values.project_id || false,
      date_deadline: values.date_deadline || false,
      user_ids: values.user_ids ? [[6, false, values.user_ids]] : [[6, false, [this.uid ?? 1]]],
      priority: values.priority || '0',
      active: true,
    });
  }

  /**
   * 获取我的任务（待办）
   *
   * Odoo 待办应用（To-Do）基于 project.task 模型，
   * 过滤条件：project_id=False（无项目=私人任务）
   * 项目任务在「项目」应用中管理，不在待办里。
   *
   * Odoo project.task 状态机制：
   * - state 字段：01_in_progress / 04_waiting_normal / 1_done / 1_canceled 等
   * - is_closed = state in ['1_done', '1_canceled']
   *
   * stage_state 选项：
   *   'in_progress' — 进行中（未关闭，默认）
   *   'done'        — 已完成
   *   'all'         — 全部
   *
   * include_project — 是否包含项目任务（默认 false，待办应用模式）
   */
  async getMyTasks(options: {
    limit?: number;
    project_id?: number;
    today_only?: boolean;
    stage_state?: 'in_progress' | 'done' | 'all';
    state_filter?: string;
    stage_id?: number;
    include_project?: boolean;
  } = {}): Promise<OdooRecord[]> {
    // 待办应用过滤：project_id=False（私人任务），排除子任务
    // 项目任务（project_id 有值）属于「项目」应用，不在待办里
    const domain: Domain = [['user_ids', 'in', [this.uid ?? 0]], ['active', '=', true], ['project_id', '=', false], ['parent_id', '=', false]];
    if (options.project_id) {
      // 如果指定了 project_id，则切换到项目任务模式
      domain.length = 0;
      domain.push(['user_ids', 'in', [this.uid ?? 0]], ['active', '=', true], ['project_id', '=', options.project_id]);
    }
    if (options.today_only) domain.push(['date_deadline', '<=', today()]);

    const stageState = options.stage_state ?? 'in_progress';
    if (stageState === 'in_progress') {
      domain.push(['state', 'not in', ['1_done', '1_canceled']]);
    } else if (stageState === 'done') {
      domain.push(['state', 'in', ['1_done', '1_canceled']]);
    }

    if (options.state_filter) {
      domain.length = domain.filter(d => !Array.isArray(d) || d[0] !== 'state').length;
      domain.push(['state', '=', options.state_filter]);
    }

    if (options.stage_id) domain.push(['stage_id', '=', options.stage_id]);

    const result = await this.searchRead('project.task', domain,
      ['id', 'name', 'description', 'date_deadline', 'stage_id', 'project_id', 'priority', 'user_ids', 'milestone_id', 'state'],
      { limit: options.limit ?? 50 });
    return result.records;
  }

  /** 获取项目任务阶段列表（用于查找 stage_id） */
  async getTaskStages(projectId?: number): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (projectId) domain.push(['project_ids', '=', projectId]);
    const result = await this.searchRead('project.task.type', domain,
      ['id', 'name', 'fold', 'sequence'], { order: 'sequence asc' });
    return result.records;
  }

  async getProjectOverview(projectId?: number): Promise<OdooRecord[]> {
    const domain: Domain = [['active', '=', true]];
    if (projectId) domain.push(['id', '=', projectId]);
    const result = await this.searchRead('project.project', domain,
      ['id', 'name', 'partner_id', 'user_id', 'date_start', 'date', 'task_count', 'open_task_count', 'closed_task_count'],
      { limit: 50 });
    return result.records;
  }

  async getMilestones(projectId?: number): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (projectId) domain.push(['project_id', '=', projectId]);
    const result = await this.searchRead('project.milestone', domain,
      ['id', 'name', 'project_id', 'deadline', 'is_reached', 'reached_date', 'task_count', 'done_task_count', 'is_deadline_exceeded'],
      { limit: 50 });
    return result.records;
  }

  async logTimesheet(values: {
    name: string; unit_amount: number; project_id?: number; task_id?: number; date?: string;
  }): Promise<number> {
    return this.create('account.analytic.line', {
      name: values.name,
      unit_amount: values.unit_amount,
      date: values.date || today(),
      user_id: this.uid ?? 1,
      project_id: values.project_id || false,
      task_id: values.task_id || false,
    });
  }

  // ==================== CRM ====================

  async getCrmPipeline(options: {
    limit?: number; stage_id?: number; user_id?: number;
    type?: 'lead' | 'opportunity'; won_status?: string;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['active', '=', true]];
    if (options.stage_id) domain.push(['stage_id', '=', options.stage_id]);
    if (options.user_id) domain.push(['user_id', '=', options.user_id]);
    else domain.push(['user_id', '=', this.uid ?? 0]);
    if (options.type) domain.push(['type', '=', options.type]);
    const result = await this.searchRead('crm.lead', domain,
      ['id', 'name', 'partner_id', 'stage_id', 'probability', 'expected_revenue', 'user_id', 'team_id', 'date_deadline', 'type', 'won_status', 'activity_ids', 'tag_ids'],
      { limit: options.limit ?? 50, order: 'stage_id asc, probability desc' });
    return result.records;
  }

  async createCrmLead(values: {
    name: string; type?: 'lead' | 'opportunity'; partner_id?: number;
    expected_revenue?: number; probability?: number; user_id?: number;
    stage_id?: number; date_deadline?: string; description?: string;
  }): Promise<number> {
    return this.create('crm.lead', {
      name: values.name,
      type: values.type || 'opportunity',
      partner_id: values.partner_id || false,
      expected_revenue: values.expected_revenue || 0,
      probability: values.probability || 10,
      user_id: values.user_id || this.uid || 1,
      stage_id: values.stage_id || false,
      date_deadline: values.date_deadline || false,
      description: values.description || '',
    });
  }

  async setCrmWon(leadIds: number[]): Promise<boolean> {
    await this.call('crm.lead', 'action_set_won', [leadIds]);
    return true;
  }

  async setCrmLost(leadIds: number[], lostReasonId?: number): Promise<boolean> {
    const kwargs: Record<string, unknown> = {};
    if (lostReasonId) kwargs['additional_values'] = { lost_reason_id: lostReasonId };
    await this.call('crm.lead', 'action_set_lost', [leadIds], kwargs);
    return true;
  }

  async getCrmStages(): Promise<OdooRecord[]> {
    const result = await this.searchRead('crm.stage', [],
      ['id', 'name', 'sequence', 'is_won', 'fold'], { order: 'sequence asc' });
    return result.records;
  }

  // ==================== Sales ====================

  async getSaleOrders(options: {
    limit?: number; state?: string; partner_id?: number; user_id?: number;
    /** v1.22: 按订单编号精确查（如 "S00016"） */
    name?: string;
    /** v1.22: 按记录 ID 精确取 */
    record_id?: number;
    /** v1.22: 同时拉订单明细行（sale.order.line），写合同/对账常用 */
    include_lines?: boolean;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.name) domain.push(['name', '=', options.name]);
    if (options.record_id) domain.push(['id', '=', options.record_id]);
    if (options.state) domain.push(['state', '=', options.state]);
    else if (!options.name && !options.record_id) domain.push(['state', 'not in', ['cancel']]);
    if (options.partner_id) domain.push(['partner_id', '=', options.partner_id]);
    if (options.user_id) domain.push(['user_id', '=', options.user_id]);
    const result = await this.searchRead('sale.order', domain,
      ['id', 'name', 'partner_id', 'state', 'date_order', 'amount_total', 'amount_untaxed', 'amount_tax',
        'invoice_status', 'user_id', 'team_id', 'validity_date', 'currency_id', 'note', 'payment_term_id'],
      { limit: options.limit ?? 20, order: 'date_order desc' });

    if (!options.include_lines || result.records.length === 0) return result.records;

    // v1.22: 一次拉所有 lines，避免 N+1
    const orderIds = result.records.map(o => o['id'] as number);
    const lines = await this.searchRead('sale.order.line',
      [['order_id', 'in', orderIds]],
      ['id', 'order_id', 'product_id', 'name', 'product_uom_qty', 'qty_delivered', 'qty_invoiced',
        'product_uom', 'price_unit', 'discount', 'price_subtotal', 'price_total', 'price_tax'],
      { order: 'order_id asc, sequence asc' });
    const linesByOrder = new Map<number, OdooRecord[]>();
    for (const ln of lines.records) {
      const oid = (Array.isArray(ln['order_id']) ? ln['order_id'][0] : ln['order_id']) as number;
      const arr = linesByOrder.get(oid) ?? [];
      arr.push(ln);
      linesByOrder.set(oid, arr);
    }
    return result.records.map(o => ({ ...o, order_line: linesByOrder.get(o['id'] as number) ?? [] }));
  }

  async confirmSaleOrder(orderId: number): Promise<unknown> {
    return this.call('sale.order', 'action_confirm', [[orderId]]);
  }

  // ==================== Purchase ====================

  async getPurchaseOrders(options: {
    limit?: number; state?: string;
    /** v1.22: 按订单编号精确查（如 "PO0001"） */
    name?: string;
    /** v1.22: 按记录 ID 精确取 */
    record_id?: number;
    /** v1.22: 同时拉采购明细行（purchase.order.line） */
    include_lines?: boolean;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.name) domain.push(['name', '=', options.name]);
    if (options.record_id) domain.push(['id', '=', options.record_id]);
    if (options.state) domain.push(['state', '=', options.state]);
    else if (!options.name && !options.record_id) domain.push(['state', 'not in', ['cancel']]);
    const result = await this.searchRead('purchase.order', domain,
      ['id', 'name', 'partner_id', 'state', 'date_order', 'date_planned', 'amount_total', 'amount_untaxed', 'amount_tax',
        'invoice_status', 'user_id', 'currency_id', 'notes', 'payment_term_id'],
      { limit: options.limit ?? 20, order: 'date_order desc' });

    if (!options.include_lines || result.records.length === 0) return result.records;

    const orderIds = result.records.map(o => o['id'] as number);
    const lines = await this.searchRead('purchase.order.line',
      [['order_id', 'in', orderIds]],
      ['id', 'order_id', 'product_id', 'name', 'product_qty', 'qty_received', 'qty_invoiced',
        'product_uom', 'price_unit', 'price_subtotal', 'price_total', 'price_tax', 'date_planned'],
      { order: 'order_id asc, sequence asc' });
    const linesByOrder = new Map<number, OdooRecord[]>();
    for (const ln of lines.records) {
      const oid = (Array.isArray(ln['order_id']) ? ln['order_id'][0] : ln['order_id']) as number;
      const arr = linesByOrder.get(oid) ?? [];
      arr.push(ln);
      linesByOrder.set(oid, arr);
    }
    return result.records.map(o => ({ ...o, order_line: linesByOrder.get(o['id'] as number) ?? [] }));
  }

  // ==================== Helpdesk ====================

  async getHelpdeskTickets(options: {
    limit?: number; stage_id?: number; user_id?: number; priority?: string;
    partner_id?: number; team_id?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['active', '=', true]];
    if (options.user_id !== undefined) domain.push(['user_id', '=', options.user_id]);
    if (options.stage_id) domain.push(['stage_id', '=', options.stage_id]);
    if (options.priority) domain.push(['priority', '=', options.priority]);
    if (options.partner_id) domain.push(['partner_id', '=', options.partner_id]);
    if (options.team_id) domain.push(['team_id', '=', options.team_id]);
    const result = await this.searchRead('helpdesk.ticket', domain,
      ['id', 'name', 'ticket_ref', 'team_id', 'stage_id', 'user_id', 'partner_id', 'priority', 'kanban_state', 'sla_deadline', 'sla_fail', 'create_date', 'close_date'],
      { limit: options.limit ?? 30, order: 'priority desc, create_date desc' });
    return result.records;
  }

  async createHelpdeskTicket(values: {
    name: string; team_id?: number; partner_id?: number;
    description?: string; priority?: '0' | '1' | '2' | '3'; user_id?: number;
  }): Promise<number> {
    return this.create('helpdesk.ticket', {
      name: values.name,
      team_id: values.team_id || false,
      partner_id: values.partner_id || false,
      description: values.description || '',
      priority: values.priority || '0',
      user_id: values.user_id || false,
    });
  }

  async getHelpdeskStages(teamId?: number): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (teamId) domain.push(['team_ids', 'in', [teamId]]);
    const result = await this.searchRead('helpdesk.stage', domain,
      ['id', 'name', 'sequence', 'fold'], { order: 'sequence asc' });
    return result.records;
  }

  // ==================== Accounting ====================

  async getInvoices(options: {
    limit?: number; move_type?: string; state?: string;
    partner_id?: number; payment_state?: string;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['move_type', 'in', options.move_type
      ? [options.move_type]
      : ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']]];
    if (options.state) domain.push(['state', '=', options.state]);
    if (options.partner_id) domain.push(['partner_id', '=', options.partner_id]);
    if (options.payment_state) domain.push(['payment_state', '=', options.payment_state]);
    const result = await this.searchRead('account.move', domain,
      ['id', 'name', 'move_type', 'partner_id', 'state', 'invoice_date', 'invoice_date_due', 'amount_total', 'payment_state', 'invoice_status'],
      { limit: options.limit ?? 20, order: 'invoice_date desc' });
    return result.records;
  }

  async getOverdueInvoices(): Promise<OdooRecord[]> {
    const result = await this.searchRead('account.move', [
      ['move_type', '=', 'out_invoice'],
      ['state', '=', 'posted'],
      ['payment_state', 'not in', ['paid', 'reversed']],
      ['invoice_date_due', '<', today()],
    ],
      ['id', 'name', 'partner_id', 'invoice_date_due', 'amount_total', 'payment_state'],
      { limit: 30, order: 'invoice_date_due asc' });
    return result.records;
  }

  // ==================== 联系人 / 客户 ====================

  async getPartners(options: {
    limit?: number; is_company?: boolean; customer_rank?: boolean;
    supplier_rank?: boolean; keyword?: string;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['active', '=', true]];
    if (options.is_company !== undefined) domain.push(['is_company', '=', options.is_company]);
    if (options.customer_rank) domain.push(['customer_rank', '>', 0]);
    if (options.supplier_rank) domain.push(['supplier_rank', '>', 0]);
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    const result = await this.searchRead('res.partner', domain,
      ['id', 'name', 'email', 'phone', 'mobile', 'is_company', 'city', 'country_id', 'customer_rank', 'supplier_rank', 'parent_id'],
      { limit: options.limit ?? 30, order: 'name asc' });
    return result.records;
  }

  async createPartner(values: {
    name: string; email?: string; phone?: string; mobile?: string;
    is_company?: boolean; city?: string; street?: string;
    customer_rank?: number; supplier_rank?: number; parent_id?: number;
  }): Promise<number> {
    return this.create('res.partner', {
      name: values.name,
      email: values.email || false,
      phone: values.phone || false,
      mobile: values.mobile || false,
      is_company: values.is_company ?? false,
      city: values.city || false,
      street: values.street || false,
      customer_rank: values.customer_rank ?? 1,
      supplier_rank: values.supplier_rank ?? 0,
      parent_id: values.parent_id || false,
    });
  }

  // ==================== 库存 ====================

  async getStockLevels(options: {
    limit?: number; product_id?: number; location_id?: number; keyword?: string;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['quantity', '>', 0]];
    if (options.product_id) domain.push(['product_id', '=', options.product_id]);
    if (options.location_id) domain.push(['location_id', '=', options.location_id]);
    if (options.keyword) domain.push(['product_id.name', 'ilike', options.keyword]);
    const result = await this.searchRead('stock.quant', domain,
      ['id', 'product_id', 'location_id', 'lot_id', 'quantity', 'reserved_quantity', 'available_quantity'],
      { limit: options.limit ?? 50, order: 'product_id asc' });
    return result.records;
  }

  async getStockPickings(options: {
    limit?: number; state?: string; picking_type?: string;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.state) domain.push(['state', '=', options.state]);
    else domain.push(['state', 'not in', ['done', 'cancel']]);
    if (options.picking_type) domain.push(['picking_type_code', '=', options.picking_type]);
    const result = await this.searchRead('stock.picking', domain,
      ['id', 'name', 'partner_id', 'picking_type_id', 'state', 'scheduled_date', 'date_done', 'origin'],
      { limit: options.limit ?? 20, order: 'scheduled_date asc' });
    return result.records;
  }

  // ==================== HR ====================

  async getEmployees(options: { limit?: number; department_id?: number; active?: boolean; keyword?: string } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['active', '=', options.active !== false]];
    if (options.department_id) domain.push(['department_id', '=', options.department_id]);
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    const result = await this.searchRead('hr.employee', domain,
      ['id', 'name', 'department_id', 'job_id', 'work_email', 'mobile_phone', 'parent_id', 'user_id'],
      { limit: options.limit ?? 50, order: 'name asc' });
    return result.records;
  }

  async getLeaves(options: { limit?: number; state?: string; employee_id?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.state) domain.push(['state', '=', options.state]);
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    else domain.push(['employee_id.user_id', '=', this.uid ?? 0]);
    const result = await this.searchRead('hr.leave', domain,
      ['id', 'name', 'employee_id', 'holiday_status_id', 'date_from', 'date_to', 'number_of_days', 'state'],
      { limit: options.limit ?? 20, order: 'date_from desc' });
    return result.records;
  }

  async getAttendances(options: { limit?: number; employee_id?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    else domain.push(['employee_id.user_id', '=', this.uid ?? 0]);
    const result = await this.searchRead('hr.attendance', domain,
      ['id', 'employee_id', 'check_in', 'check_out', 'worked_hours'],
      { limit: options.limit ?? 20, order: 'check_in desc' });
    return result.records;
  }

  // ==================== 审批 ====================

  async getApprovals(options: { limit?: number; state?: string; my_requests?: boolean } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.state) domain.push(['request_status', '=', options.state]);
    if (options.my_requests) domain.push(['request_owner_id.user_id', '=', this.uid ?? 0]);
    const result = await this.searchRead('approval.request', domain,
      ['id', 'name', 'category_id', 'request_owner_id', 'request_status', 'date', 'date_confirmed', 'amount', 'reason'],
      { limit: options.limit ?? 20, order: 'date desc' });
    return result.records;
  }

  // ==================== Mail / Activity ====================

  async getTodayActivities(options: { limit?: number } = {}): Promise<OdooRecord[]> {
    const result = await this.searchRead('mail.activity',
      [['user_id', '=', this.uid ?? 0], ['date_deadline', '<=', today()]],
      ['id', 'summary', 'date_deadline', 'activity_type_id', 'res_model', 'res_id', 'note', 'state'],
      { limit: options.limit ?? 50 });
    return result.records;
  }

  async createActivity(values: {
    res_model: string; res_id: number; activity_type_id: number;
    summary?: string; note?: string; date_deadline: string; user_id?: number;
  }): Promise<number> {
    return this.create('mail.activity', {
      res_model: values.res_model, res_id: values.res_id,
      activity_type_id: values.activity_type_id,
      summary: values.summary || '', note: values.note || '',
      date_deadline: values.date_deadline,
      user_id: values.user_id ?? this.uid ?? 1,
    });
  }

  async getActivityTypes(): Promise<OdooRecord[]> {
    const result = await this.searchRead('mail.activity.type', [],
      ['id', 'name', 'icon', 'category', 'delay_count', 'delay_unit'], { order: 'name asc' });
    return result.records;
  }

  /**
   * 完成活动（闭环）—— 调 mail.activity.action_feedback：
   * 活动标记为 done、写入反馈到源记录 chatter、从活动列表里移除。
   * 这是 Odoo 活动闭环的正式 API，不要直接 unlink。
   */
  async completeActivity(id: number, feedback?: string): Promise<unknown> {
    return this.call('mail.activity', 'action_feedback', [[id]], {
      feedback: feedback || '',
    });
  }

  /** 改期：把活动的 date_deadline 挪到新日期（YYYY-MM-DD） */
  async rescheduleActivity(id: number, newDeadline: string): Promise<boolean> {
    return this.write('mail.activity', [id], { date_deadline: newDeadline });
  }

  async createCalendarEvent(values: {
    name: string; start: string; stop: string;
    description?: string; partner_ids?: number[]; alarm_ids?: number[];
  }): Promise<number> {
    return this.create('calendar.event', {
      name: values.name, start: values.start, stop: values.stop,
      description: values.description || '',
      partner_ids: values.partner_ids ? [[6, false, values.partner_ids]] : [[6, false, [this.uid ?? 1]]],
      alarm_ids: values.alarm_ids ? [[6, false, values.alarm_ids]] : false,
    });
  }

  /**
   * 获取今日会议/日程 —— 覆盖 [今天 00:00, 明天 00:00) 区间里与我相关的事件。
   * 包含：我是组织者、或我是参与者（partner_ids 含 my partner_id）。
   */
  async getCalendarToday(options: { limit?: number } = {}): Promise<OdooRecord[]> {
    const t = today();
    const next = tomorrow();
    const uid = this.uid ?? 0;
    // 我的 partner_id 需要先查一次（cached on session user_context 里没有，所以 read res.users）
    let myPartnerId: number | false = false;
    try {
      const users = await this.read('res.users', [uid], ['partner_id']);
      const pid = users[0]?.['partner_id'];
      if (Array.isArray(pid) && typeof pid[0] === 'number') myPartnerId = pid[0];
    } catch { /* ignore */ }

    const domain: Domain = [
      ['start', '>=', `${t} 00:00:00`],
      ['start', '<', `${next} 00:00:00`],
    ];
    if (myPartnerId) {
      domain.unshift('|', ['user_id', '=', uid], ['partner_ids', 'in', [myPartnerId]]);
    } else {
      domain.unshift(['user_id', '=', uid]);
    }

    const result = await this.searchRead('calendar.event', domain,
      ['id', 'name', 'start', 'stop', 'duration', 'location', 'partner_ids', 'description', 'user_id', 'allday'],
      { limit: options.limit ?? 30, order: 'start asc' });
    return result.records;
  }

  /** 更新日历事件（时间、地点、标题、描述、参与者） */
  async updateCalendarEvent(id: number, values: {
    name?: string; start?: string; stop?: string; location?: string;
    description?: string; partner_ids?: number[];
  }): Promise<boolean> {
    const payload: Record<string, unknown> = {};
    if (values.name !== undefined) payload['name'] = values.name;
    if (values.start !== undefined) payload['start'] = values.start;
    if (values.stop !== undefined) payload['stop'] = values.stop;
    if (values.location !== undefined) payload['location'] = values.location;
    if (values.description !== undefined) payload['description'] = values.description;
    if (values.partner_ids !== undefined) payload['partner_ids'] = [[6, false, values.partner_ids]];
    if (Object.keys(payload).length === 0) return true;
    return this.write('calendar.event', [id], payload);
  }

  /** 取消日历事件：active=false（软删除，保留历史），而不是 unlink */
  async cancelCalendarEvent(id: number): Promise<boolean> {
    return this.write('calendar.event', [id], { active: false });
  }

  // ==================== 关注者（followers）====================
  //
  // Odoo 的 mail.thread 混入提供：
  //   - message_subscribe(partner_ids, subtype_ids?) — 添加关注者
  //   - message_unsubscribe(partner_ids)              — 移除关注者
  //   - message_follower_ids                           — 列表
  // 任何继承 mail.thread 的模型（project.task、crm.lead、helpdesk.ticket、
  // sale.order、res.partner 等）都能用。

  async followRecord(model: string, resId: number, partnerIds?: number[]): Promise<unknown> {
    // 默认关注者 = 当前用户的 partner_id
    let targets = partnerIds;
    if (!targets || targets.length === 0) {
      const uid = this.uid ?? 0;
      const users = await this.read('res.users', [uid], ['partner_id']);
      const pid = users[0]?.['partner_id'];
      if (Array.isArray(pid) && typeof pid[0] === 'number') targets = [pid[0]];
      else throw new Error('无法获取当前用户的 partner_id');
    }
    return this.call(model, 'message_subscribe', [[resId]], { partner_ids: targets });
  }

  async unfollowRecord(model: string, resId: number, partnerIds?: number[]): Promise<unknown> {
    let targets = partnerIds;
    if (!targets || targets.length === 0) {
      const uid = this.uid ?? 0;
      const users = await this.read('res.users', [uid], ['partner_id']);
      const pid = users[0]?.['partner_id'];
      if (Array.isArray(pid) && typeof pid[0] === 'number') targets = [pid[0]];
      else throw new Error('无法获取当前用户的 partner_id');
    }
    return this.call(model, 'message_unsubscribe', [[resId]], { partner_ids: targets });
  }

  // ==================== 邮件（mail.mail + mail.template）====================
  //
  // 两条路径：
  //   1) 随手发一封：用 message_post 发在某条记录的 chatter，Odoo 会自动
  //      邮件化给 followers（如果 subtype 是 comment）。这是 Odoo 原生的"发邮件"方式。
  //   2) 显式发邮件给任意地址：mail.mail create → send。适合真正"给外部发邮件"场景。
  // 模板：mail.template.send_mail(res_id, force_send=True) 是 Odoo 原生的模板发送入口。

  /**
   * 直接发送邮件（不依赖 chatter）。
   * recipients 为 email 字符串数组（逗号分隔会被 Odoo 自行拆分，但我们显式传逗号拼接）。
   * bodyHtml 建议是 HTML，纯文本会按 <br/> 保留换行。
   */
  async sendEmail(values: {
    subject: string; bodyHtml: string;
    recipients: string[]; cc?: string[]; bcc?: string[];
    res_model?: string; res_id?: number;
    attachment_ids?: number[];
  }): Promise<number> {
    const payload: Record<string, unknown> = {
      subject: values.subject,
      body_html: values.bodyHtml,
      email_to: values.recipients.join(','),
      email_from: false, // Odoo 会用当前用户的邮箱/公司邮箱
    };
    if (values.cc && values.cc.length > 0) payload['email_cc'] = values.cc.join(',');
    if (values.bcc && values.bcc.length > 0) (payload as Record<string, unknown>)['email_bcc'] = values.bcc.join(',');
    if (values.res_model) payload['model'] = values.res_model;
    if (values.res_id) payload['res_id'] = values.res_id;
    if (values.attachment_ids && values.attachment_ids.length > 0) {
      payload['attachment_ids'] = [[6, false, values.attachment_ids]];
    }
    const id = await this.create('mail.mail', payload);
    // 立即发送（否则会等到 cron）
    await this.call('mail.mail', 'send', [[id]]);
    return id;
  }

  async getEmailTemplates(options: { model?: string; keyword?: string; limit?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.model) domain.push(['model', '=', options.model]);
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    const result = await this.searchRead('mail.template', domain,
      ['id', 'name', 'model', 'subject', 'email_from', 'email_to', 'use_default_to', 'lang'],
      { limit: options.limit ?? 50, order: 'name asc' });
    return result.records;
  }

  /**
   * 用模板发邮件。template_id 通过 getEmailTemplates 查。
   * res_id 是模板关联模型的记录 id（模板的 model 字段决定）。
   * force_send=true 立即入队发送。
   */
  async sendEmailFromTemplate(templateId: number, resId: number, options: {
    force_send?: boolean; email_values?: Record<string, unknown>;
  } = {}): Promise<unknown> {
    return this.call('mail.template', 'send_mail', [templateId, resId], {
      force_send: options.force_send ?? true,
      email_values: options.email_values ?? false,
    });
  }

  // ==================== 附件（ir.attachment）/ 文档（documents.document）====================
  //
  // ir.attachment 是 Odoo 通用附件表；传 datas（base64 编码）即可。
  // 挂到记录：res_model + res_id 就会在该记录的 chatter/附件面板出现。
  // documents.document 是 Enterprise 文档管理应用，可选 folder_id 归档。

  async attachFile(values: {
    res_model: string; res_id: number;
    name: string; datas_base64: string; mimetype?: string;
  }): Promise<number> {
    return this.create('ir.attachment', {
      name: values.name,
      datas: values.datas_base64,
      res_model: values.res_model,
      res_id: values.res_id,
      type: 'binary',
      mimetype: values.mimetype || 'application/octet-stream',
    });
  }

  async listAttachments(model: string, resId: number, options: { limit?: number } = {}): Promise<OdooRecord[]> {
    const result = await this.searchRead('ir.attachment',
      [['res_model', '=', model], ['res_id', '=', resId]],
      ['id', 'name', 'mimetype', 'file_size', 'create_date', 'create_uid', 'url', 'type'],
      { limit: options.limit ?? 50, order: 'create_date desc' });
    return result.records;
  }

  async uploadDocument(values: {
    name: string; datas_base64: string; mimetype?: string;
    folder_id?: number; tag_ids?: number[];
  }): Promise<number> {
    const payload: Record<string, unknown> = {
      name: values.name,
      datas: values.datas_base64,
      type: 'binary',
      mimetype: values.mimetype || 'application/octet-stream',
    };
    if (values.folder_id) payload['folder_id'] = values.folder_id;
    if (values.tag_ids && values.tag_ids.length > 0) payload['tag_ids'] = [[6, false, values.tag_ids]];
    return this.create('documents.document', payload);
  }

  async getUnreadMessages(options: { limit?: number } = {}): Promise<OdooRecord[]> {
    const result = await this.searchRead('mail.message',
      [['message_type', '!=', 'notification'], ['to_read', '=', true]],
      ['id', 'body', 'date', 'author_id', 'model', 'res_id', 'subject'],
      { limit: options.limit ?? 20 });
    return result.records;
  }

  async getInboxNotifications(options: { limit?: number } = {}): Promise<OdooRecord[]> {
    const result = await this.searchRead('mail.notification',
      [['is_read', '=', false], ['notification_type', '=', 'inbox']],
      ['id', 'mail_message_id', 'notification_status', 'is_read', 'read_date'],
      { limit: options.limit ?? 20 });
    return result.records;
  }

  // ==================== Knowledge（知识库 / knowledge.article）====================
  //
  // Odoo 19 Enterprise 的 `knowledge.article` 模型要点：
  //  - body 字段是 HTML
  //  - category 由 internal_permission 计算得出：
  //      internal_permission='write' → workspace，='none' → private（无 parent 时）
  //      子文章不需要 internal_permission，权限沿 parent 继承
  //  - DB 约束：顶层文章必须给 internal_permission；子文章必须给 parent_id
  //  - 通过 action_toggle_favorite / action_send_to_trash / move_to 等 action 操作
  //  - is_user_favorite 是 compute + search，不能直接 write

  async searchKnowledgeArticles(options: {
    keyword?: string;
    category?: 'workspace' | 'private' | 'shared';
    only_favorite?: boolean;
    only_roots?: boolean;         // 只列顶层文章
    parent_id?: number;           // 列某文章的直接子节点
    limit?: number;
    include_trashed?: boolean;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (!options.include_trashed) domain.push(['to_delete', '=', false]);
    domain.push(['active', '=', true]);
    if (options.category) domain.push(['category', '=', options.category]);
    if (options.only_favorite) domain.push(['is_user_favorite', '=', true]);
    if (options.only_roots) domain.push(['parent_id', '=', false]);
    if (options.parent_id !== undefined) domain.push(['parent_id', '=', options.parent_id]);
    if (options.keyword) {
      domain.push('|', ['name', 'ilike', options.keyword], ['body', 'ilike', options.keyword]);
    }
    const result = await this.searchRead('knowledge.article', domain,
      ['id', 'name', 'icon', 'parent_id', 'root_article_id', 'category',
       'is_user_favorite', 'favorite_count', 'last_edition_date', 'last_edition_uid',
       'has_article_children', 'sequence'],
      { limit: options.limit ?? 30, order: 'sequence asc, last_edition_date desc, id desc' });
    return result.records;
  }

  /** 读取单篇文章完整内容（含 body） */
  async readKnowledgeArticle(id: number): Promise<OdooRecord | null> {
    const records = await this.read('knowledge.article', [id],
      ['id', 'name', 'icon', 'body', 'parent_id', 'root_article_id', 'category',
       'internal_permission', 'inherited_permission',
       'is_user_favorite', 'favorite_count', 'is_locked', 'to_delete',
       'last_edition_date', 'last_edition_uid', 'sequence', 'has_article_children']);
    return records[0] ?? null;
  }

  /**
   * 创建知识库文章
   *
   * - 顶层：必须传 category='workspace'|'private'；自动映射到 internal_permission
   *     workspace → 'write'  （默认所有内部用户可编辑）
   *     private   → 'none'   （仅所有者）
   *     shared    → 'none'（通常通过加 member 实现）
   * - 子文章：传 parent_id，其余权限继承
   */
  async createKnowledgeArticle(values: {
    name?: string;
    body?: string;                // HTML
    icon?: string;                // emoji
    parent_id?: number;
    category?: 'workspace' | 'private' | 'shared';
  }): Promise<number> {
    const payload: Record<string, unknown> = {
      name: values.name || '未命名',
      body: values.body ?? false,
      icon: values.icon || false,
    };
    if (values.parent_id) {
      payload['parent_id'] = values.parent_id;
    } else {
      const cat = values.category ?? 'private';
      payload['internal_permission'] = cat === 'workspace' ? 'write' : 'none';
      if (cat === 'workspace') payload['is_article_visible_by_everyone'] = true;
    }
    return this.create('knowledge.article', payload);
  }

  async updateKnowledgeArticle(id: number, values: {
    name?: string; body?: string; icon?: string;
  }): Promise<boolean> {
    const payload: Record<string, unknown> = {};
    if (values.name !== undefined) payload['name'] = values.name;
    if (values.body !== undefined) payload['body'] = values.body;
    if (values.icon !== undefined) payload['icon'] = values.icon || false;
    if (Object.keys(payload).length === 0) return true;
    return this.write('knowledge.article', [id], payload);
  }

  /**
   * 在现有文章的 body 末尾追加一段 HTML —— 读-改-写（Odoo body 字段无原子 append）。
   * 调用者负责把 markdown 之类的输入转成合法 HTML。
   */
  async appendKnowledgeArticle(id: number, htmlSuffix: string): Promise<boolean> {
    const rec = await this.readKnowledgeArticle(id);
    if (!rec) throw new Error(`文章 ${id} 不存在`);
    const body = (rec['body'] as string | false) || '';
    const next = `${body}${htmlSuffix}`;
    return this.write('knowledge.article', [id], { body: next });
  }

  /** 移动到新 parent 或在兄弟节点中排序 */
  async moveKnowledgeArticle(id: number, options: {
    parent_id?: number | false;
    before_article_id?: number;
    category?: 'workspace' | 'private' | 'shared';
  }): Promise<unknown> {
    return this.call('knowledge.article', 'move_to', [[id]], {
      parent_id: options.parent_id ?? false,
      before_article_id: options.before_article_id ?? false,
      category: options.category ?? false,
    });
  }

  async toggleKnowledgeFavorite(id: number): Promise<unknown> {
    return this.call('knowledge.article', 'action_toggle_favorite', [[id]]);
  }

  async trashKnowledgeArticle(id: number): Promise<unknown> {
    return this.call('knowledge.article', 'action_send_to_trash', [[id]]);
  }

  async restoreKnowledgeArticle(id: number): Promise<unknown> {
    return this.call('knowledge.article', 'action_unarchive', [[id]]);
  }

  // ==================== v1.8 — Chatter / Project / Ticket / Approval ====================
  //
  // Chatter = Odoo 的内置沟通轨迹。任何 mail.thread 混入的模型（几乎所有业务模型）
  // 都有 message_post() 方法：
  //   - subtype 'mail.mt_comment'   → 评论，会 email 给 followers
  //   - subtype 'mail.mt_note'      → 内部记录，只留痕不发邮件
  // body 是 HTML；message_type 常用 'comment' / 'notification'。

  /**
   * 在任意记录 chatter 发消息（评论，会通知 followers）。
   * partner_ids 传进来会被当作额外收件人加入。
   */
  async postMessage(model: string, resId: number, values: {
    bodyHtml: string;
    subject?: string;
    partner_ids?: number[];
    attachment_ids?: number[];
    as_log?: boolean;                // true = 内部记录（mt_note），false = 评论（mt_comment）
  }): Promise<number> {
    const kwargs: Record<string, unknown> = {
      body: values.bodyHtml,
      message_type: values.as_log ? 'notification' : 'comment',
      subtype_xmlid: values.as_log ? 'mail.mt_note' : 'mail.mt_comment',
    };
    if (values.subject) kwargs['subject'] = values.subject;
    if (values.partner_ids && values.partner_ids.length > 0) {
      kwargs['partner_ids'] = values.partner_ids;
    }
    if (values.attachment_ids && values.attachment_ids.length > 0) {
      kwargs['attachment_ids'] = values.attachment_ids;
    }
    const result = await this.call(model, 'message_post', [[resId]], kwargs);
    if (typeof result === 'number') return result;
    // Odoo 19 返回的是 mail.message 记录（dict），取 id
    if (typeof result === 'object' && result !== null && 'id' in (result as Record<string, unknown>)) {
      const r = result as Record<string, unknown>;
      return typeof r['id'] === 'number' ? r['id'] : 0;
    }
    return 0;
  }

  /** 读取某条记录的 chatter 消息历史（最新在前） */
  async getMessageHistory(model: string, resId: number, options: {
    limit?: number;
    include_notifications?: boolean;   // 默认 false，过滤掉系统通知（auto-followers 之类）
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['model', '=', model], ['res_id', '=', resId]];
    if (!options.include_notifications) {
      domain.push(['message_type', 'in', ['comment', 'email']]);
    }
    const result = await this.searchRead('mail.message', domain,
      ['id', 'date', 'author_id', 'email_from', 'subject', 'body', 'message_type', 'subtype_id'],
      { limit: options.limit ?? 20, order: 'date desc' });
    return result.records;
  }

  // ------- Project / Milestone ------------------------------------------------

  async createProject(values: {
    name: string;
    partner_id?: number;
    user_id?: number;                   // 项目负责人
    date_start?: string;
    date?: string;                      // 结束日期
    description?: string;
    privacy_visibility?: 'followers' | 'employees' | 'portal';
  }): Promise<number> {
    return this.create('project.project', {
      name: values.name,
      partner_id: values.partner_id || false,
      user_id: values.user_id || this.uid || false,
      date_start: values.date_start || false,
      date: values.date || false,
      description: values.description || '',
      privacy_visibility: values.privacy_visibility || 'employees',
      active: true,
    });
  }

  async createMilestone(values: {
    name: string;
    project_id: number;
    deadline?: string;
  }): Promise<number> {
    return this.create('project.milestone', {
      name: values.name,
      project_id: values.project_id,
      deadline: values.deadline || false,
    });
  }

  // ------- Helpdesk ticket 更新/关闭 ----------------------------------------

  /**
   * 查找某客服团队里 fold=true 的阶段（= 关闭阶段）。
   * 不传 teamId 就找任何 fold=true 的阶段，返回最小 sequence 的那条。
   */
  async findHelpdeskClosedStage(teamId?: number): Promise<OdooRecord | null> {
    const domain: Domain = [['fold', '=', true]];
    if (teamId) domain.push(['team_ids', 'in', [teamId]]);
    const result = await this.searchRead('helpdesk.stage', domain,
      ['id', 'name', 'sequence'], { limit: 1, order: 'sequence asc' });
    return result.records[0] ?? null;
  }

  // ------- 审批 approval.request -------------------------------------------
  //
  // 审批流状态机：
  //   new → pending（action_confirm）→ approved（action_approve）
  //                                  → refused  （action_refuse）
  //                                  → cancel   （action_withdraw）
  // 我们只暴露 approve / refuse 两个最常见的审批人动作；
  // 发起人侧的 action_confirm 可以后续再加。

  async approveApprovalRequest(id: number): Promise<unknown> {
    return this.call('approval.request', 'action_approve', [[id]]);
  }

  async refuseApprovalRequest(id: number): Promise<unknown> {
    return this.call('approval.request', 'action_refuse', [[id]]);
  }

  // ==================== HR 扩展（v1.11） ====================
  //
  // v1.11 新增：请假闭环 / 报销闭环 / 招聘 / 考核 / 工资 / 排班
  //
  // 注意权限边界：
  //   - hr_payroll.* 需要 hr_payroll.group_hr_payroll_user
  //   - hr_recruitment.stage 写操作需要 hr_recruitment.group_hr_recruitment_user
  //   - hr.expense 的 action_approve 之上需要 hr_expense.group_hr_expense_team_approver
  //   - hr.leave 的 action_validate（二次审批）需要 hr_holidays.group_hr_holidays_manager
  //
  // 这里只做 RPC 调用，权限错误由 Odoo 自己抛 → 上层 catch 后返回给用户

  // ---------- 请假类型 / 申请 / 审批 / 额度分配 ----------

  async getLeaveTypes(options: { keyword?: string; limit?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['active', '=', true]];
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    const result = await this.searchRead('hr.leave.type', domain,
      ['id', 'name', 'requires_allocation', 'leave_validation_type', 'request_unit', 'company_id', 'color'],
      { limit: options.limit ?? 30, order: 'name asc' });
    return result.records;
  }

  async createLeave(values: {
    employee_id?: number;            // 不填默认当前 user 的 employee
    holiday_status_id: number;
    request_date_from: string;       // YYYY-MM-DD
    request_date_to: string;         // YYYY-MM-DD
    name?: string;                   // 请假事由
  }): Promise<number> {
    const payload: Record<string, unknown> = {
      holiday_status_id: values.holiday_status_id,
      request_date_from: values.request_date_from,
      request_date_to: values.request_date_to,
    };
    if (values.employee_id) payload['employee_id'] = values.employee_id;
    if (values.name) payload['name'] = values.name;
    return this.create('hr.leave', payload);
  }

  async approveLeave(id: number): Promise<unknown> {
    // action_approve 自动在 confirm→validate1→validate 状态机里递进
    return this.call('hr.leave', 'action_approve', [[id]]);
  }

  async refuseLeave(id: number): Promise<unknown> {
    return this.call('hr.leave', 'action_refuse', [[id]]);
  }

  async cancelLeave(id: number, reason?: string): Promise<unknown> {
    // hr.leave.action_cancel 在 v17+ 支持 reason 参数；v15/v16 直接 action_cancel
    if (reason) {
      try { return await this.call('hr.leave', 'action_cancel', [[id]], { reason }); }
      catch { /* fallback */ }
    }
    return this.call('hr.leave', 'action_cancel', [[id]]);
  }

  async createLeaveAllocation(values: {
    employee_id: number;
    holiday_status_id: number;
    number_of_days: number;
    name?: string;
    date_from?: string;              // YYYY-MM-DD，默认今天
    auto_approve?: boolean;          // true 时创建后立即调 action_approve
  }): Promise<{ id: number; approved: boolean }> {
    const payload: Record<string, unknown> = {
      employee_id: values.employee_id,
      holiday_status_id: values.holiday_status_id,
      number_of_days: values.number_of_days,
      allocation_type: 'regular',
    };
    if (values.name) payload['name'] = values.name;
    if (values.date_from) payload['date_from'] = values.date_from;
    const id = await this.create('hr.leave.allocation', payload);
    let approved = false;
    if (values.auto_approve) {
      try { await this.call('hr.leave.allocation', 'action_approve', [[id]]); approved = true; }
      catch { /* 权限不足 / 状态不对 → 保留 draft，让用户手动审批 */ }
    }
    return { id, approved };
  }

  // ---------- 报销 ----------

  async getExpenses(options: {
    employee_id?: number;
    state?: string;                  // draft / submitted / approved / posted / paid / refused
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.state) domain.push(['state', '=', options.state]);
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    else domain.push(['employee_id.user_id', '=', this.uid ?? 0]);
    const result = await this.searchRead('hr.expense', domain,
      ['id', 'name', 'employee_id', 'product_id', 'date', 'total_amount', 'currency_id', 'state', 'payment_state'],
      { limit: options.limit ?? 30, order: 'date desc' });
    return result.records;
  }

  async createExpense(values: {
    name: string;
    product_id?: number;             // 默认 0 时让 Odoo 取默认产品
    employee_id?: number;
    quantity?: number;
    unit_amount?: number;            // 当 product 是按数量计费时
    total_amount?: number;           // 总金额（首选；产品行无单价时直接传）
    date?: string;                   // YYYY-MM-DD，默认今天
    description?: string;
  }): Promise<number> {
    const payload: Record<string, unknown> = {
      name: values.name,
      quantity: values.quantity ?? 1,
    };
    if (values.product_id) payload['product_id'] = values.product_id;
    if (values.employee_id) payload['employee_id'] = values.employee_id;
    if (values.unit_amount !== undefined) payload['unit_amount'] = values.unit_amount;
    if (values.total_amount !== undefined) payload['total_amount'] = values.total_amount;
    if (values.date) payload['date'] = values.date;
    if (values.description) payload['description'] = values.description;
    return this.create('hr.expense', payload);
  }

  async submitExpense(ids: number[]): Promise<unknown> {
    // hr.expense.action_submit 在不同版本叫法不一：v17 是 action_submit_sheet，v18+ 是 action_submit
    try { return await this.call('hr.expense', 'action_submit', [ids]); }
    catch {
      return this.call('hr.expense', 'action_submit_sheet', [ids]);
    }
  }

  async approveExpense(ids: number[]): Promise<unknown> {
    try { return await this.call('hr.expense', 'action_approve', [ids]); }
    catch {
      // 老版本走 sheet
      return this.call('hr.expense', 'action_approve_expense_sheets', [ids]);
    }
  }

  async refuseExpense(ids: number[], reason?: string): Promise<unknown> {
    if (reason) {
      try { return await this.call('hr.expense', 'action_refuse', [ids], { reason }); }
      catch { /* fallback */ }
    }
    try { return await this.call('hr.expense', 'action_refuse', [ids]); }
    catch {
      return this.call('hr.expense', 'action_refuse_expense_sheets', [ids]);
    }
  }

  // ---------- 招聘 ----------

  async getApplicants(options: {
    job_id?: number;
    stage_id?: number;
    keyword?: string;
    only_active?: boolean;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.only_active !== false) domain.push(['active', '=', true]);
    if (options.job_id) domain.push(['job_id', '=', options.job_id]);
    if (options.stage_id) domain.push(['stage_id', '=', options.stage_id]);
    if (options.keyword) domain.push('|', ['partner_name', 'ilike', options.keyword], ['email_from', 'ilike', options.keyword]);
    const result = await this.searchRead('hr.applicant', domain,
      ['id', 'partner_name', 'email_from', 'job_id', 'stage_id', 'kanban_state', 'priority',
       'user_id', 'date_open', 'date_last_stage_update', 'salary_expected', 'salary_proposed', 'availability'],
      { limit: options.limit ?? 30, order: 'priority desc, date_last_stage_update desc' });
    return result.records;
  }

  async getRecruitmentStages(jobId?: number): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (jobId) domain.push('|', ['job_ids', 'in', [jobId]], ['job_ids', '=', false]);
    const result = await this.searchRead('hr.recruitment.stage', domain,
      ['id', 'name', 'sequence', 'hired_stage', 'fold'],
      { limit: 50, order: 'sequence asc' });
    return result.records;
  }

  async moveApplicantStage(id: number, opts: {
    stage_id?: number;
    kanban_state?: 'normal' | 'done' | 'blocked';
    refuse_reason_id?: number;
  }): Promise<boolean> {
    const values: Record<string, unknown> = {};
    if (opts.stage_id) values['stage_id'] = opts.stage_id;
    if (opts.kanban_state) values['kanban_state'] = opts.kanban_state;
    if (opts.refuse_reason_id) values['refuse_reason_id'] = opts.refuse_reason_id;
    if (Object.keys(values).length === 0) return true;
    return this.write('hr.applicant', [id], values);
  }

  async getApplicantRefuseReasons(): Promise<OdooRecord[]> {
    const result = await this.searchRead('hr.applicant.refuse.reason', [],
      ['id', 'name'], { limit: 30, order: 'name asc' });
    return result.records;
  }

  // ---------- 考核 ----------

  async getAppraisals(options: {
    employee_id?: number;
    state?: '1_new' | '2_pending' | '3_done';
    only_mine?: boolean;             // 我作为 reviewer
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.state) domain.push(['state', '=', options.state]);
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    if (options.only_mine) domain.push(['manager_ids.user_id', '=', this.uid ?? 0]);
    const result = await this.searchRead('hr.appraisal', domain,
      ['id', 'employee_id', 'department_id', 'job_id', 'manager_ids',
       'date_close', 'state', 'next_appraisal_date', 'waiting_feedback'],
      { limit: options.limit ?? 20, order: 'date_close desc' });
    return result.records;
  }

  async appraisalAction(id: number, action: 'confirm' | 'done' | 'back'): Promise<unknown> {
    const methodMap = { confirm: 'action_confirm', done: 'action_done', back: 'action_back' };
    return this.call('hr.appraisal', methodMap[action], [[id]]);
  }

  // ---------- 工资 ----------

  async getPayslips(options: {
    employee_id?: number;
    state?: 'draft' | 'verify' | 'done' | 'paid' | 'cancel';
    payslip_run_id?: number;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.state) domain.push(['state', '=', options.state]);
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    else domain.push(['employee_id.user_id', '=', this.uid ?? 0]);
    if (options.payslip_run_id) domain.push(['payslip_run_id', '=', options.payslip_run_id]);
    const result = await this.searchRead('hr.payslip', domain,
      ['id', 'name', 'employee_id', 'date_from', 'date_to', 'state',
       'basic_wage', 'gross_wage', 'net_wage', 'currency_id', 'payslip_run_id', 'paid'],
      { limit: options.limit ?? 20, order: 'date_from desc' });
    return result.records;
  }

  // ---------- 排班 ----------

  async getPlanningShifts(options: {
    employee_id?: number;
    department_id?: number;
    date_from?: string;              // YYYY-MM-DD，默认今天
    date_to?: string;                // YYYY-MM-DD，默认 7 天后
    only_published?: boolean;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const dFrom = options.date_from ?? today();
    const dTo = options.date_to ?? (() => {
      const d = new Date(); d.setDate(d.getDate() + 7);
      return d.toISOString().substring(0, 10);
    })();
    const domain: Domain = [
      ['start_datetime', '>=', `${dFrom} 00:00:00`],
      ['start_datetime', '<=', `${dTo} 23:59:59`],
    ];
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    if (options.department_id) domain.push(['department_id', '=', options.department_id]);
    if (options.only_published) domain.push(['state', '=', 'published']);
    const result = await this.searchRead('planning.slot', domain,
      ['id', 'employee_id', 'role_id', 'department_id', 'start_datetime', 'end_datetime',
       'allocated_hours', 'state', 'name'],
      { limit: options.limit ?? 50, order: 'start_datetime asc' });
    return result.records;
  }

  // ==================== HR 行动力补完（v1.12） ====================
  //
  // v1.12 把 v1.11 中只读的几个 HR 域升级到完整 action 闭环：
  //   - hr.payslip 工资单生命周期：validate → paid → cancel
  //   - hr.appraisal 考核：confirm → done → back
  //   - hr.recruitment.stage / hr.applicant.refuse.reason：master data 查询
  //   - hr.applicant.action_create_meeting：创建面试日历事件
  //   - planning.slot publish/unpublish：排班发布/取消发布
  // 以及新增三个 HR 域：
  //   - hr.employee.skill / hr.skill[.type|.level]：员工技能管理
  //   - hr.employee.location（hr_homeworking 模块）：远程办公地点
  //   - fleet.vehicle：员工车辆

  // ---------- 工资单生命周期 ----------

  async validatePayslip(ids: number[]): Promise<unknown> {
    // draft → done。需要 hr_payroll.group_hr_payroll_user
    return this.call('hr.payslip', 'action_payslip_done', [ids]);
  }

  async markPayslipPaid(ids: number[]): Promise<unknown> {
    // done → paid。需要 hr_payroll.group_hr_payroll_user
    return this.call('hr.payslip', 'action_payslip_paid', [ids]);
  }

  async cancelPayslip(ids: number[]): Promise<unknown> {
    // any → cancel。需要 hr_payroll.group_hr_payroll_user
    return this.call('hr.payslip', 'action_payslip_cancel', [ids]);
  }

  // ---------- 招聘助手 ----------

  async createApplicantMeeting(applicantId: number, values: {
    name: string;
    start: string;                   // YYYY-MM-DD HH:MM:SS
    duration?: number;               // 小时，默认 1
    description?: string;
  }): Promise<number> {
    // 通过创建 calendar.event 来"约面试"，把 default_applicant_id 填到上下文
    // 比直接调 action_create_meeting（返回 act_window dict）更适合工具化调用
    const app = (await this.read('hr.applicant', [applicantId],
      ['id', 'partner_name', 'partner_id', 'email_from', 'user_id', 'department_id']))[0];
    if (!app) throw new Error(`未找到应聘者 #${applicantId}`);

    // 自动建一个联系人（如果没有）
    let partnerId = Array.isArray(app['partner_id']) ? app['partner_id'][0] as number : null;
    if (!partnerId && app['partner_name']) {
      partnerId = await this.create('res.partner', {
        name: app['partner_name'],
        is_company: false,
        email: app['email_from'] ?? false,
      });
      // 回写到 applicant
      await this.write('hr.applicant', [applicantId], { partner_id: partnerId });
    }

    const partnerIds: number[] = [];
    if (partnerId) partnerIds.push(partnerId);
    const recruiter = Array.isArray(app['user_id']) ? app['user_id'][0] as number : null;
    if (recruiter) {
      const recruiterUser = (await this.read('res.users', [recruiter], ['partner_id']))[0];
      const rPartner = Array.isArray(recruiterUser?.['partner_id']) ? recruiterUser['partner_id'][0] as number : null;
      if (rPartner && !partnerIds.includes(rPartner)) partnerIds.push(rPartner);
    }

    const duration = values.duration ?? 1;
    const startDate = new Date(values.start.replace(' ', 'T') + 'Z');
    const endDate = new Date(startDate.getTime() + duration * 60 * 60 * 1000);
    const stop = endDate.toISOString().substring(0, 19).replace('T', ' ');

    const eventValues: Record<string, unknown> = {
      name: values.name,
      start: values.start,
      stop,
      duration,
      partner_ids: [[6, 0, partnerIds]],
      applicant_id: applicantId,
    };
    if (values.description) eventValues['description'] = values.description;
    return this.create('calendar.event', eventValues);
  }

  // ---------- 排班发布 / 取消发布 ----------

  async publishPlanningShift(ids: number[], notify: boolean = true): Promise<unknown> {
    // 简单地写 state='published'；如需通知员工，逐条调 action_send
    if (notify) {
      // action_send 会按 employee_id 发邮件 + 自动写 state='published'
      const results: unknown[] = [];
      for (const id of ids) {
        try { results.push(await this.call('planning.slot', 'action_send', [[id]])); }
        catch (e) { results.push({ error: String(e), id }); }
      }
      return results;
    }
    return this.write('planning.slot', ids, { state: 'published' });
  }

  async unpublishPlanningShift(ids: number[]): Promise<unknown> {
    // 需要 planning.group_planning_manager
    return this.call('planning.slot', 'action_unpublish', [ids]);
  }

  // ---------- 技能管理 ----------

  async getEmployeeSkills(options: {
    employee_id?: number;
    skill_type_id?: number;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    else domain.push(['employee_id.user_id', '=', this.uid ?? 0]);
    if (options.skill_type_id) domain.push(['skill_type_id', '=', options.skill_type_id]);
    const result = await this.searchRead('hr.employee.skill', domain,
      ['id', 'employee_id', 'skill_id', 'skill_type_id', 'skill_level_id', 'level_progress'],
      { limit: options.limit ?? 50, order: 'skill_type_id, skill_id' });
    return result.records;
  }

  async addEmployeeSkill(values: {
    employee_id: number;
    skill_type_id: number;
    skill_id: number;
    skill_level_id: number;
  }): Promise<number> {
    return this.create('hr.employee.skill', {
      employee_id: values.employee_id,
      skill_type_id: values.skill_type_id,
      skill_id: values.skill_id,
      skill_level_id: values.skill_level_id,
    });
  }

  async getSkillsCatalog(options: {
    keyword?: string;
    skill_type_id?: number;
    limit?: number;
  } = {}): Promise<{
    skill_types: OdooRecord[];
    skills: OdooRecord[];
    skill_levels: OdooRecord[];
  }> {
    const skillDomain: Domain = [];
    if (options.skill_type_id) skillDomain.push(['skill_type_id', '=', options.skill_type_id]);
    if (options.keyword) skillDomain.push(['name', 'ilike', options.keyword]);
    const [skillTypes, skills, levels] = await Promise.all([
      this.searchRead('hr.skill.type', [], ['id', 'name'], { limit: 30, order: 'name asc' }),
      this.searchRead('hr.skill', skillDomain, ['id', 'name', 'skill_type_id'],
        { limit: options.limit ?? 50, order: 'skill_type_id, name asc' }),
      this.searchRead('hr.skill.level', [], ['id', 'name', 'level_progress', 'skill_type_id'],
        { limit: 60, order: 'skill_type_id, level_progress asc' }),
    ]);
    return {
      skill_types: skillTypes.records,
      skills: skills.records,
      skill_levels: levels.records,
    };
  }

  // ---------- 远程办公（hr_homeworking） ----------

  async setHomeworking(values: {
    employee_id?: number;            // 不填默认为当前用户的员工
    date: string;                    // YYYY-MM-DD
    work_location_id: number;        // hr.work.location id（办公室/家/其他）
  }): Promise<number> {
    // hr.employee.location 有 unique(employee_id, date) 约束
    // 已存在则更新，没有则创建
    const empId = values.employee_id ?? await this._getCurrentEmployeeId();
    const existing = await this.searchRead('hr.employee.location',
      [['employee_id', '=', empId], ['date', '=', values.date]],
      ['id'], { limit: 1 });
    if (existing.records.length > 0) {
      const id = existing.records[0]?.['id'] as number;
      await this.write('hr.employee.location', [id], { work_location_id: values.work_location_id });
      return id;
    }
    return this.create('hr.employee.location', {
      employee_id: empId,
      date: values.date,
      work_location_id: values.work_location_id,
    });
  }

  private async _getCurrentEmployeeId(): Promise<number> {
    const users = await this.read('res.users', [this.uid ?? 0], ['employee_id']);
    const empField = users[0]?.['employee_id'];
    if (Array.isArray(empField) && typeof empField[0] === 'number') return empField[0];
    throw new Error('当前用户没有关联员工记录（res.users.employee_id 为空）');
  }

  // ---------- 车队 ----------

  async getFleetVehicles(options: {
    driver_user_id?: number;         // 按司机的 res.users id 筛
    employee_id?: number;
    keyword?: string;
    only_active?: boolean;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.only_active !== false) domain.push(['active', '=', true]);
    if (options.driver_user_id) {
      // driver_id 是 Many2one('res.partner')，所以要过 res.users.partner_id 联表
      domain.push(['driver_id.user_ids', 'in', [options.driver_user_id]]);
    }
    if (options.keyword) domain.push('|', ['name', 'ilike', options.keyword], ['license_plate', 'ilike', options.keyword]);
    const result = await this.searchRead('fleet.vehicle', domain,
      ['id', 'name', 'license_plate', 'model_id', 'driver_id', 'acquisition_date',
       'odometer', 'odometer_unit', 'state_id', 'company_id'],
      { limit: options.limit ?? 30, order: 'name asc' });
    return result.records;
  }

  // ==================== HR 全生命周期治理（v1.13） ====================
  //
  // v1.13 把 HR 推到「全生命周期 + 数据洞察 + 组织治理」：
  //   - 员工 CRUD：create / update / archive / unarchive（入职 → 改资料 → 离职/返聘）
  //   - HR 仪表盘：一次聚合在编/今日生日/待审请假/待审报销/招聘漏斗/今日请假人
  //   - 部门 / 岗位 / 工作地点：列表 + 创建
  //   - 合同 / 版本：hr.version 列表与历史
  //   - 工时洞察：本月按项目聚合 / 经理查下属工时
  //   - 组织架构：上下级树
  //
  // 数据洞察大量用 read_group（Odoo 原生 group-by + 聚合，比 search_read
  // 自己 reduce 高效得多）。

  // ---------- 通用：read_group helper ----------

  async readGroup(model: string, domain: Domain,
                  fields: string[], groupby: string[],
                  options: { limit?: number; orderby?: string; lazy?: boolean } = {}): Promise<OdooRecord[]> {
    const result = await this.call(model, 'read_group', [domain, fields, groupby], {
      limit: options.limit ?? 100,
      orderby: options.orderby ?? '',
      lazy: options.lazy ?? true,
    });
    return Array.isArray(result) ? result as OdooRecord[] : [];
  }

  // ---------- 员工 CRUD ----------

  async createEmployee(values: {
    name: string;
    work_email?: string;
    work_phone?: string;
    mobile_phone?: string;
    job_title?: string;
    department_id?: number;
    job_id?: number;
    parent_id?: number;            // 上级 hr.employee.id
    coach_id?: number;
    user_id?: number;              // 关联的 res.users.id
    work_location_id?: number;
    company_id?: number;
  }): Promise<number> {
    // hr.employee 的 resource_id 是 required，但 Odoo 在 create 时会按 name 自动建一条 resource.resource
    return this.create('hr.employee', values as Record<string, unknown>);
  }

  async updateEmployee(id: number, values: {
    name?: string;
    work_email?: string;
    work_phone?: string;
    mobile_phone?: string;
    job_title?: string;
    department_id?: number;
    job_id?: number;
    parent_id?: number;
    coach_id?: number;
    user_id?: number;
    work_location_id?: number;
  }): Promise<boolean> {
    return this.write('hr.employee', [id], values as Record<string, unknown>);
  }

  async archiveEmployee(id: number): Promise<boolean> {
    // active 字段 related to resource_id.active；写 active=false 会同时归档 resource
    return this.write('hr.employee', [id], { active: false });
  }

  async unarchiveEmployee(id: number): Promise<boolean> {
    return this.write('hr.employee', [id], { active: true });
  }

  // ---------- HR 仪表盘 ----------

  async getHrDashboard(): Promise<{
    today: string;
    headcount: { total: number; by_department: Record<string, unknown>[] };
    today_birthdays: Record<string, unknown>[];
    today_on_leave: Record<string, unknown>[];
    pending_leaves: number;
    pending_expenses: number;
    recruitment_pipeline: Record<string, unknown>[];
    open_positions: number;
  }> {
    const todayStr = today();
    const [
      totalActive,
      byDept,
      birthdays,
      onLeave,
      pendingLeaves,
      pendingExpenses,
      pipeline,
      openPositions,
    ] = await Promise.all([
      this.searchCount('hr.employee', [['active', '=', true]]),
      // 部门人数分布（read_group）
      this.readGroup('hr.employee',
        [['active', '=', true], ['department_id', '!=', false]],
        ['department_id'], ['department_id'], { limit: 30 }),
      // 今日生日（按 birthday 字段的 month-day 匹配；只有 hr.group_hr_user 才能读 birthday）
      // 退化方案：按 search_read，前端 reduce
      this.searchRead('hr.employee',
        [['active', '=', true]],
        ['id', 'name', 'birthday', 'department_id'],
        { limit: 200 }).then(r => r.records.filter(e => {
          const bd = e['birthday'];
          if (typeof bd !== 'string' || bd.length < 10) return false;
          return bd.substring(5, 10) === todayStr.substring(5, 10);
        })).catch(() => []),  // 没权限读 birthday 时静默返空
      // 今日请假中（state=validate, date_from <= today <= date_to）
      this.searchRead('hr.leave',
        [['state', '=', 'validate'],
         ['date_from', '<=', `${todayStr} 23:59:59`],
         ['date_to', '>=', `${todayStr} 00:00:00`]],
        ['id', 'employee_id', 'holiday_status_id', 'date_from', 'date_to'],
        { limit: 50 }),
      // 待审请假（confirm + validate1）
      this.searchCount('hr.leave', ['|', ['state', '=', 'confirm'], ['state', '=', 'validate1']]),
      // 待审报销（submitted）
      this.searchCount('hr.expense', [['state', '=', 'submitted']]),
      // 招聘漏斗：按 stage 分组
      this.readGroup('hr.applicant',
        [['active', '=', true]],
        ['stage_id'], ['stage_id'], { limit: 20 }).catch(() => []),
      // 招聘中的岗位数
      this.searchCount('hr.job', [['active', '=', true]]),
    ]);
    return {
      today: todayStr,
      headcount: {
        total: totalActive,
        by_department: byDept.map((g: OdooRecord) => ({
          department: g['department_id'],
          count: g['department_id_count'] ?? g['__count'] ?? 0,
        })),
      },
      today_birthdays: (birthdays as OdooRecord[]).map(e => ({
        id: e['id'], name: e['name'], department: e['department_id'],
      })),
      today_on_leave: onLeave.records.map(l => ({
        id: l['id'], employee: l['employee_id'], type: l['holiday_status_id'],
        from: l['date_from'], to: l['date_to'],
      })),
      pending_leaves: pendingLeaves,
      pending_expenses: pendingExpenses,
      recruitment_pipeline: pipeline.map((g: OdooRecord) => ({
        stage: g['stage_id'],
        count: g['stage_id_count'] ?? g['__count'] ?? 0,
      })),
      open_positions: openPositions,
    };
  }

  // ---------- 部门 / 岗位 / 工作地点 ----------

  async getDepartments(options: { keyword?: string; parent_id?: number; limit?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['active', '=', true]];
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    if (options.parent_id !== undefined) domain.push(['parent_id', '=', options.parent_id || false]);
    const result = await this.searchRead('hr.department', domain,
      ['id', 'name', 'complete_name', 'parent_id', 'manager_id', 'company_id', 'member_ids'],
      { limit: options.limit ?? 100, order: 'complete_name asc' });
    return result.records;
  }

  async createDepartment(values: {
    name: string;
    parent_id?: number;
    manager_id?: number;
    company_id?: number;
  }): Promise<number> {
    return this.create('hr.department', values as Record<string, unknown>);
  }

  async getJobs(options: { department_id?: number; only_active?: boolean; limit?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.only_active !== false) domain.push(['active', '=', true]);
    if (options.department_id) domain.push(['department_id', '=', options.department_id]);
    const result = await this.searchRead('hr.job', domain,
      ['id', 'name', 'department_id', 'expected_employees', 'company_id', 'sequence'],
      { limit: options.limit ?? 100, order: 'sequence asc, name asc' });
    return result.records;
  }

  async createJob(values: {
    name: string;
    department_id?: number;
    company_id?: number;
    sequence?: number;
  }): Promise<number> {
    return this.create('hr.job', values as Record<string, unknown>);
  }

  async getWorkLocations(options: { keyword?: string; location_type?: string; limit?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['active', '=', true]];
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    if (options.location_type) domain.push(['location_type', '=', options.location_type]);
    const result = await this.searchRead('hr.work.location', domain,
      ['id', 'name', 'location_type', 'address_id', 'company_id'],
      { limit: options.limit ?? 50, order: 'name asc' });
    return result.records;
  }

  // ---------- 合同 / 版本（hr.version） ----------

  async getEmployeeVersions(employeeId: number, options: { limit?: number } = {}): Promise<OdooRecord[]> {
    // 注意：date_start/date_end/wage 等字段需要 hr.group_hr_user / hr_manager 才能读
    // 没权限时退化只取基本字段
    const fields = ['id', 'name', 'employee_id', 'date_version', 'department_id', 'job_id',
                    'contract_type_id', 'wage', 'company_id', 'active'];
    try {
      const result = await this.searchRead('hr.version',
        [['employee_id', '=', employeeId]],
        fields,
        { limit: options.limit ?? 30, order: 'date_version desc' });
      return result.records;
    } catch {
      // 退化只取基础字段
      const result = await this.searchRead('hr.version',
        [['employee_id', '=', employeeId]],
        ['id', 'name', 'employee_id', 'department_id', 'job_id', 'company_id', 'active'],
        { limit: options.limit ?? 30 });
      return result.records;
    }
  }

  // ---------- 工时洞察 ----------

  async getTimesheetSummary(options: {
    employee_id?: number;            // 不填默认当前用户
    date_from?: string;              // YYYY-MM-DD，默认本月初
    date_to?: string;                // YYYY-MM-DD，默认今天
    group_by?: 'project' | 'task' | 'employee';   // 默认 project
  } = {}): Promise<{
    period: { from: string; to: string };
    total_hours: number;
    groups: Record<string, unknown>[];
  }> {
    const todayStr = today();
    const dFrom = options.date_from ?? todayStr.substring(0, 7) + '-01';
    const dTo = options.date_to ?? todayStr;
    const domain: Domain = [
      ['date', '>=', dFrom],
      ['date', '<=', dTo],
      ['project_id', '!=', false],
    ];
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    else domain.push(['employee_id.user_id', '=', this.uid ?? 0]);
    const groupField = options.group_by === 'task' ? 'task_id'
                       : options.group_by === 'employee' ? 'employee_id'
                       : 'project_id';
    const groups = await this.readGroup('account.analytic.line',
      domain, ['unit_amount:sum'], [groupField], { limit: 200 });
    const totalHours = groups.reduce((sum: number, g: OdooRecord) => sum + Number(g['unit_amount'] ?? 0), 0);
    return {
      period: { from: dFrom, to: dTo },
      total_hours: totalHours,
      groups: groups.map((g: OdooRecord) => ({
        [groupField]: g[groupField],
        hours: g['unit_amount'] ?? 0,
        count: g[`${groupField}_count`] ?? g['__count'] ?? 0,
      })),
    };
  }

  async getTeamTimesheets(options: {
    manager_id?: number;             // 默认当前用户对应的 employee.id
    date_from?: string;
    date_to?: string;
    limit?: number;
  } = {}): Promise<Record<string, unknown>[]> {
    const todayStr = today();
    const dFrom = options.date_from ?? todayStr.substring(0, 7) + '-01';
    const dTo = options.date_to ?? todayStr;
    // 找经理对应的 employee
    let managerEmpId = options.manager_id;
    if (!managerEmpId) {
      try {
        const me = await this.read('res.users', [this.uid ?? 0], ['employee_id']);
        if (Array.isArray(me[0]?.['employee_id'])) managerEmpId = me[0]?.['employee_id'][0] as number;
      } catch { /* noop */ }
    }
    if (!managerEmpId) {
      throw new Error('未能确定当前经理 employee_id（res.users.employee_id 为空？）');
    }
    // 查所有 parent_id = managerEmpId 的下属
    const subordinates = await this.searchRead('hr.employee',
      [['parent_id', '=', managerEmpId], ['active', '=', true]],
      ['id', 'name'], { limit: 100 });
    const subIds = subordinates.records.map(e => e['id'] as number);
    if (subIds.length === 0) return [];
    // 查这批人在时间范围内的工时聚合
    const groups = await this.readGroup('account.analytic.line',
      [
        ['employee_id', 'in', subIds],
        ['date', '>=', dFrom],
        ['date', '<=', dTo],
        ['project_id', '!=', false],
      ],
      ['unit_amount:sum'], ['employee_id'], { limit: options.limit ?? 100 });
    // 组装：员工→工时
    const empMap = new Map(subordinates.records.map(e => [e['id'] as number, e['name']]));
    return groups.map((g: OdooRecord) => {
      const empArr = g['employee_id'];
      const empId = Array.isArray(empArr) ? empArr[0] as number : 0;
      return {
        employee: g['employee_id'],
        employee_name: empMap.get(empId),
        hours: g['unit_amount'] ?? 0,
        days_in_period: g['employee_id_count'] ?? g['__count'] ?? 0,
      };
    });
  }

  // ---------- 组织架构（上下级树） ----------

  async getEmployeeOrgChart(employeeId: number): Promise<{
    employee: OdooRecord | null;
    manager: OdooRecord | null;
    coach: OdooRecord | null;
    direct_reports: OdooRecord[];
    skip_level_reports_count: number;
  }> {
    const fields = ['id', 'name', 'job_title', 'department_id', 'parent_id',
                    'coach_id', 'work_email', 'mobile_phone'];
    const me = (await this.read('hr.employee', [employeeId], fields))[0];
    if (!me) return { employee: null, manager: null, coach: null, direct_reports: [], skip_level_reports_count: 0 };
    const managerId = Array.isArray(me['parent_id']) ? me['parent_id'][0] as number : null;
    const coachId = Array.isArray(me['coach_id']) ? me['coach_id'][0] as number : null;
    const [manager, coach, directReports] = await Promise.all([
      managerId ? this.read('hr.employee', [managerId], fields).then(r => r[0] ?? null) : Promise.resolve(null),
      coachId ? this.read('hr.employee', [coachId], fields).then(r => r[0] ?? null) : Promise.resolve(null),
      this.searchRead('hr.employee',
        [['parent_id', '=', employeeId], ['active', '=', true]],
        fields, { limit: 100, order: 'name asc' }),
    ]);
    const directReportIds = directReports.records.map(r => r['id'] as number);
    let skipLevelCount = 0;
    if (directReportIds.length > 0) {
      skipLevelCount = await this.searchCount('hr.employee',
        [['parent_id', 'in', directReportIds], ['active', '=', true]]);
    }
    return {
      employee: me,
      manager: manager ?? null,
      coach: coach ?? null,
      direct_reports: directReports.records,
      skip_level_reports_count: skipLevelCount,
    };
  }

  // ==================== Analytics & Orchestration（v1.14） ====================
  //
  // v1.14 核心：把 v1.13 的 dashboard 模式（read_group + Promise.all）
  // 推广到所有主域，并加 onboarding/offboarding 编排工具。
  //
  // - HR Analytics 进阶：attendance / leave 趋势 / turnover
  // - HR 编排：onboarding 一链式 / offboarding 转移下属
  // - 工时审批闭环：action_validate_timesheet（来自 timesheet_grid 企业模块）
  // - 跨域仪表盘：sales / crm pipeline health / invoice aging / helpdesk
  // - 项目分析：project_dashboard / my_workload
  // - 薪酬批次：payslip_run + generate_payslips

  // ---------- HR Analytics 进阶 ----------

  async getAttendanceAnalytics(options: {
    employee_id?: number;            // 默认全员（HR 视角）
    department_id?: number;
    date_from?: string;              // YYYY-MM-DD，默认本月初
    date_to?: string;                // YYYY-MM-DD，默认今天
  } = {}): Promise<{
    period: { from: string; to: string };
    total_records: number;
    total_hours: number;
    by_employee: Record<string, unknown>[];
  }> {
    const todayStr = today();
    const dFrom = options.date_from ?? todayStr.substring(0, 7) + '-01';
    const dTo = options.date_to ?? todayStr;
    const domain: Domain = [
      ['check_in', '>=', `${dFrom} 00:00:00`],
      ['check_in', '<=', `${dTo} 23:59:59`],
    ];
    if (options.employee_id) domain.push(['employee_id', '=', options.employee_id]);
    if (options.department_id) domain.push(['employee_id.department_id', '=', options.department_id]);
    const [groups, totalCount] = await Promise.all([
      this.readGroup('hr.attendance', domain, ['worked_hours:sum'], ['employee_id'], { limit: 200 }),
      this.searchCount('hr.attendance', domain),
    ]);
    const totalHours = groups.reduce((s: number, g: Record<string, unknown>) => s + Number(g['worked_hours'] ?? 0), 0);
    return {
      period: { from: dFrom, to: dTo },
      total_records: totalCount,
      total_hours: totalHours,
      by_employee: groups.map((g: Record<string, unknown>) => ({
        employee: g['employee_id'],
        hours: g['worked_hours'] ?? 0,
        days: g['employee_id_count'] ?? g['__count'] ?? 0,
      })),
    };
  }

  async getLeaveAnalytics(options: {
    department_id?: number;
    date_from?: string;
    date_to?: string;
  } = {}): Promise<{
    period: { from: string; to: string };
    by_type: Record<string, unknown>[];
    by_state: Record<string, unknown>[];
    total_days_taken: number;        // 已批准的总天数
  }> {
    const todayStr = today();
    const dFrom = options.date_from ?? todayStr.substring(0, 7) + '-01';
    const dTo = options.date_to ?? todayStr;
    const domain: Domain = [
      ['date_from', '>=', `${dFrom} 00:00:00`],
      ['date_from', '<=', `${dTo} 23:59:59`],
    ];
    if (options.department_id) domain.push(['department_id', '=', options.department_id]);
    const [byType, byState, validated] = await Promise.all([
      this.readGroup('hr.leave', domain, ['number_of_days:sum'], ['holiday_status_id'], { limit: 50 }),
      this.readGroup('hr.leave', domain, [], ['state'], { limit: 10 }),
      this.readGroup('hr.leave',
        [...domain, ['state', '=', 'validate']],
        ['number_of_days:sum'], [], { limit: 1 }),
    ]);
    const total = Array.isArray(validated) && validated[0]
      ? Number((validated[0] as Record<string, unknown>)['number_of_days'] ?? 0) : 0;
    return {
      period: { from: dFrom, to: dTo },
      by_type: byType.map((g: Record<string, unknown>) => ({
        type: g['holiday_status_id'],
        days: g['number_of_days'] ?? 0,
        count: g['holiday_status_id_count'] ?? g['__count'] ?? 0,
      })),
      by_state: byState.map((g: Record<string, unknown>) => ({
        state: g['state'],
        count: g['state_count'] ?? g['__count'] ?? 0,
      })),
      total_days_taken: total,
    };
  }

  async getTurnoverMetrics(options: {
    days?: number;                   // 滑动窗口长度，默认 90
  } = {}): Promise<{
    window: { from: string; to: string; days: number };
    headcount_now: number;
    hires_in_window: number;
    departures_in_window: number;
    turnover_rate: number;           // (hires + departures) / 2 / headcount * (365/days)
    annualized_attrition_rate: number;  // departures / headcount * (365/days)
  }> {
    const days = options.days ?? 90;
    const dTo = today();
    const dFromDate = new Date();
    dFromDate.setDate(dFromDate.getDate() - days);
    const dFrom = dFromDate.toISOString().substring(0, 10);
    // 在编人数（active=true）
    // 入职 = 这个窗口内 create_date 落在窗口的 hr.employee
    // 离职 = active=false 且 write_date 在窗口内（近似，因为没有正式离职日字段）
    const [headcount, hires, departures] = await Promise.all([
      this.searchCount('hr.employee', [['active', '=', true]]),
      this.searchCount('hr.employee', [
        ['create_date', '>=', `${dFrom} 00:00:00`],
        ['create_date', '<=', `${dTo} 23:59:59`],
      ]),
      this.searchCount('hr.employee', [
        ['active', '=', false],
        ['write_date', '>=', `${dFrom} 00:00:00`],
        ['write_date', '<=', `${dTo} 23:59:59`],
      ]),
    ]);
    const turnover = headcount > 0
      ? ((hires + departures) / 2 / headcount) * (365 / days)
      : 0;
    const attrition = headcount > 0
      ? (departures / headcount) * (365 / days)
      : 0;
    return {
      window: { from: dFrom, to: dTo, days },
      headcount_now: headcount,
      hires_in_window: hires,
      departures_in_window: departures,
      turnover_rate: Math.round(turnover * 1000) / 1000,
      annualized_attrition_rate: Math.round(attrition * 1000) / 1000,
    };
  }

  // ---------- 入离职编排 ----------

  async employeeOnboarding(values: {
    name: string;
    work_email?: string;
    work_phone?: string;
    mobile_phone?: string;
    job_title?: string;
    department_id?: number;
    job_id?: number;
    parent_id?: number;
    user_id?: number;
    work_location_id?: number;
    company_id?: number;
    create_user?: boolean;           // true 时自动建 res.users（如果还没绑定）
    user_login?: string;             // 配合 create_user
    welcome_message?: string;        // 在 chatter 留一条入职欢迎
  }): Promise<{
    employee_id: number;
    user_id: number | null;
    actions: string[];
  }> {
    const actions: string[] = [];

    // 1) 创建 employee
    const empPayload: Record<string, unknown> = {
      name: values.name,
    };
    for (const k of ['work_email','work_phone','mobile_phone','job_title','department_id','job_id','parent_id','user_id','work_location_id','company_id'] as const) {
      const v = values[k];
      if (v !== undefined) empPayload[k] = v;
    }
    const empId = await this.create('hr.employee', empPayload);
    actions.push(`创建员工 #${empId}`);

    // 2) 创建关联 res.users（可选）
    let userId: number | null = (values.user_id as number | undefined) ?? null;
    if (values.create_user && !userId && values.user_login) {
      try {
        userId = await this.create('res.users', {
          login: values.user_login,
          name: values.name,
          email: values.work_email ?? values.user_login,
        });
        await this.write('hr.employee', [empId], { user_id: userId });
        actions.push(`创建系统账号 res.users #${userId}`);
      } catch (e) {
        actions.push(`系统账号创建失败：${String(e)}`);
      }
    }

    // 3) 写入欢迎 chatter
    if (values.welcome_message) {
      try {
        await this.call('hr.employee', 'message_post', [[empId]], {
          body: values.welcome_message,
          message_type: 'comment',
          subtype_xmlid: 'mail.mt_comment',
        });
        actions.push('已发送入职欢迎消息');
      } catch (e) {
        actions.push(`欢迎消息发送失败：${String(e)}`);
      }
    }

    return { employee_id: empId, user_id: userId, actions };
  }

  async employeeOffboarding(values: {
    employee_id: number;
    new_manager_id?: number;         // 把下属转给 new_manager_id
    leaving_message?: string;        // chatter 留言
    refuse_pending_leaves?: boolean; // 自动拒掉未批的请假
  }): Promise<{
    employee_id: number;
    actions: string[];
  }> {
    const actions: string[] = [];

    // 1) 转移直接下属
    if (values.new_manager_id) {
      const reports = await this.searchRead('hr.employee',
        [['parent_id', '=', values.employee_id], ['active', '=', true]],
        ['id', 'name'], { limit: 200 });
      const reportIds = reports.records.map(r => r['id'] as number);
      if (reportIds.length > 0) {
        await this.write('hr.employee', reportIds, { parent_id: values.new_manager_id });
        actions.push(`已把 ${reportIds.length} 名下属转给经理 #${values.new_manager_id}`);
      } else {
        actions.push('没有需要转移的下属');
      }
    }

    // 2) 拒绝未批的请假（可选）
    if (values.refuse_pending_leaves) {
      const pending = await this.searchRead('hr.leave',
        [['employee_id', '=', values.employee_id],
         '|', ['state', '=', 'confirm'], ['state', '=', 'validate1']],
        ['id'], { limit: 100 });
      for (const l of pending.records) {
        try { await this.refuseLeave(l['id'] as number); }
        catch { /* 个别失败不阻塞 */ }
      }
      if (pending.records.length > 0) {
        actions.push(`已拒绝 ${pending.records.length} 条未批请假`);
      }
    }

    // 3) chatter 留言
    if (values.leaving_message) {
      try {
        await this.call('hr.employee', 'message_post', [[values.employee_id]], {
          body: values.leaving_message,
          message_type: 'comment',
          subtype_xmlid: 'mail.mt_comment',
        });
        actions.push('已发送离职说明 chatter');
      } catch { /* noop */ }
    }

    // 4) archive 员工（最后一步，避免前几步因 active=false 失败）
    await this.write('hr.employee', [values.employee_id], { active: false });
    actions.push(`员工 #${values.employee_id} 已归档`);

    return { employee_id: values.employee_id, actions };
  }

  // ---------- 工时审批闭环（来自 timesheet_grid 企业模块） ----------

  async validateTimesheets(ids: number[]): Promise<unknown> {
    // 需要 timesheet_grid 已安装 + hr_timesheet.group_hr_timesheet_approver
    return this.call('account.analytic.line', 'action_validate_timesheet', [ids]);
  }

  async invalidateTimesheets(ids: number[]): Promise<unknown> {
    return this.call('account.analytic.line', 'action_invalidate_timesheet', [ids]);
  }

  // ---------- 销售仪表盘 ----------

  async getSalesDashboard(options: {
    date_from?: string;
    date_to?: string;
  } = {}): Promise<{
    period: { from: string; to: string };
    total_amount: number;
    order_count: number;
    by_state: Record<string, unknown>[];
    top_customers: Record<string, unknown>[];
    pending_invoice_count: number;   // 已确认但还没开票
    pending_delivery_count: number;  // 已确认但还没发货
  }> {
    const todayStr = today();
    const dFrom = options.date_from ?? todayStr.substring(0, 7) + '-01';
    const dTo = options.date_to ?? todayStr;
    const domain: Domain = [
      ['date_order', '>=', `${dFrom} 00:00:00`],
      ['date_order', '<=', `${dTo} 23:59:59`],
    ];
    const [byState, totals, topCust, pendingInv, pendingDel] = await Promise.all([
      this.readGroup('sale.order', domain, [], ['state'], { limit: 10 }),
      this.readGroup('sale.order',
        [...domain, '|', ['state', '=', 'sale'], ['state', '=', 'done']],
        ['amount_total:sum'], [], { limit: 1 }),
      this.readGroup('sale.order',
        [...domain, '|', ['state', '=', 'sale'], ['state', '=', 'done']],
        ['amount_total:sum'], ['partner_id'], { limit: 10, orderby: 'amount_total desc' }),
      this.searchCount('sale.order',
        ['|', ['state', '=', 'sale'], ['state', '=', 'done'], ['invoice_status', '=', 'to invoice']]),
      this.searchCount('sale.order',
        ['|', ['state', '=', 'sale'], ['state', '=', 'done'], ['delivery_status', 'in', ['pending', 'started']]]).catch(() => 0),
    ]);
    const total = Array.isArray(totals) && totals[0]
      ? Number((totals[0] as Record<string, unknown>)['amount_total'] ?? 0) : 0;
    const orderCount = byState.reduce((s: number, g: Record<string, unknown>) =>
      s + Number(g['state_count'] ?? g['__count'] ?? 0), 0);
    return {
      period: { from: dFrom, to: dTo },
      total_amount: total,
      order_count: orderCount,
      by_state: byState.map((g: Record<string, unknown>) => ({
        state: g['state'],
        count: g['state_count'] ?? g['__count'] ?? 0,
      })),
      top_customers: topCust.map((g: Record<string, unknown>) => ({
        partner: g['partner_id'],
        amount: g['amount_total'] ?? 0,
        order_count: g['partner_id_count'] ?? g['__count'] ?? 0,
      })),
      pending_invoice_count: pendingInv,
      pending_delivery_count: pendingDel,
    };
  }

  // ---------- CRM 漏斗健康 ----------

  async getCrmPipelineHealth(options: {
    user_id?: number;                // 不填默认所有人
    days_overdue?: number;           // date_deadline < today - X 视为逾期，默认 0（今天就算）
  } = {}): Promise<{
    by_stage: Record<string, unknown>[];   // 阶段分布 + 总金额
    by_user: Record<string, unknown>[];    // 销售员分布
    overdue_count: number;
    overdue_value: number;
    avg_probability: number;
    total_pipeline_value: number;
  }> {
    const todayStr = today();
    const overdueDate = options.days_overdue
      ? new Date(Date.now() - options.days_overdue * 86400000).toISOString().substring(0, 10)
      : todayStr;
    const domain: Domain = [['type', '=', 'opportunity'], ['active', '=', true]];
    if (options.user_id) domain.push(['user_id', '=', options.user_id]);

    const [byStage, byUser, overdueCount, overdueAgg, totalAgg] = await Promise.all([
      this.readGroup('crm.lead', domain, ['expected_revenue:sum'], ['stage_id'], { limit: 30 }),
      this.readGroup('crm.lead', domain, ['expected_revenue:sum'], ['user_id'], { limit: 30 }),
      this.searchCount('crm.lead', [...domain, ['date_deadline', '<', overdueDate]]),
      this.readGroup('crm.lead',
        [...domain, ['date_deadline', '<', overdueDate]],
        ['expected_revenue:sum'], [], { limit: 1 }),
      this.readGroup('crm.lead', domain,
        ['expected_revenue:sum', 'probability:avg'], [], { limit: 1 }),
    ]);
    const overdueVal = Array.isArray(overdueAgg) && overdueAgg[0]
      ? Number((overdueAgg[0] as Record<string, unknown>)['expected_revenue'] ?? 0) : 0;
    const totalVal = Array.isArray(totalAgg) && totalAgg[0]
      ? Number((totalAgg[0] as Record<string, unknown>)['expected_revenue'] ?? 0) : 0;
    const avgProb = Array.isArray(totalAgg) && totalAgg[0]
      ? Number((totalAgg[0] as Record<string, unknown>)['probability'] ?? 0) : 0;
    return {
      by_stage: byStage.map((g: Record<string, unknown>) => ({
        stage: g['stage_id'],
        revenue: g['expected_revenue'] ?? 0,
        count: g['stage_id_count'] ?? g['__count'] ?? 0,
      })),
      by_user: byUser.map((g: Record<string, unknown>) => ({
        user: g['user_id'],
        revenue: g['expected_revenue'] ?? 0,
        count: g['user_id_count'] ?? g['__count'] ?? 0,
      })),
      overdue_count: overdueCount,
      overdue_value: overdueVal,
      avg_probability: Math.round(avgProb * 100) / 100,
      total_pipeline_value: totalVal,
    };
  }

  // ---------- 发票账龄分析 ----------

  async getInvoiceAging(options: {
    partner_id?: number;             // 只看某客户
    company_id?: number;
  } = {}): Promise<{
    today: string;
    bucket_0_30: { count: number; amount: number };
    bucket_31_60: { count: number; amount: number };
    bucket_61_90: { count: number; amount: number };
    bucket_90_plus: { count: number; amount: number };
    not_due: { count: number; amount: number };
    total_outstanding: number;
  }> {
    const todayStr = today();
    const baseDomain: Domain = [
      ['move_type', '=', 'out_invoice'],
      ['state', '=', 'posted'],
      ['payment_state', 'in', ['not_paid', 'partial']],
    ];
    if (options.partner_id) baseDomain.push(['partner_id', '=', options.partner_id]);
    if (options.company_id) baseDomain.push(['company_id', '=', options.company_id]);

    function dateOffset(days: number): string {
      const d = new Date();
      d.setDate(d.getDate() - days);
      return d.toISOString().substring(0, 10);
    }
    const day30 = dateOffset(30), day60 = dateOffset(60), day90 = dateOffset(90);

    const [b0_30, b31_60, b61_90, b90p, notDue] = await Promise.all([
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '<=', todayStr], ['invoice_date_due', '>', day30]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '<=', day30], ['invoice_date_due', '>', day60]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '<=', day60], ['invoice_date_due', '>', day90]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '<=', day90]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '>', todayStr]],
        ['amount_residual:sum'], [], { limit: 1 }),
    ]);

    function unpack(g: Record<string, unknown>[]): { count: number; amount: number } {
      const row = g[0] as Record<string, unknown> | undefined;
      return {
        count: Number(row?.['__count'] ?? 0),
        amount: Number(row?.['amount_residual'] ?? 0),
      };
    }
    const b0 = unpack(b0_30), b1 = unpack(b31_60), b2 = unpack(b61_90), b3 = unpack(b90p), bn = unpack(notDue);
    return {
      today: todayStr,
      bucket_0_30: b0,
      bucket_31_60: b1,
      bucket_61_90: b2,
      bucket_90_plus: b3,
      not_due: bn,
      total_outstanding: b0.amount + b1.amount + b2.amount + b3.amount + bn.amount,
    };
  }

  // ---------- Helpdesk 仪表盘 ----------

  async getHelpdeskDashboard(options: {
    team_id?: number;
    user_id?: number;
  } = {}): Promise<{
    open_count: number;
    by_stage: Record<string, unknown>[];
    by_priority: Record<string, unknown>[];
    by_assignee: Record<string, unknown>[];
    overdue_count: number;
    high_priority_open: number;
  }> {
    const baseDomain: Domain = [['close_date', '=', false]];   // 未关闭
    if (options.team_id) baseDomain.push(['team_id', '=', options.team_id]);
    if (options.user_id) baseDomain.push(['user_id', '=', options.user_id]);

    const todayStr = today();
    const [openCount, byStage, byPrio, byUser, overdueCnt, highPrio] = await Promise.all([
      this.searchCount('helpdesk.ticket', baseDomain),
      this.readGroup('helpdesk.ticket', baseDomain, [], ['stage_id'], { limit: 30 }),
      this.readGroup('helpdesk.ticket', baseDomain, [], ['priority'], { limit: 5 }),
      this.readGroup('helpdesk.ticket', baseDomain, [], ['user_id'], { limit: 30 }),
      this.searchCount('helpdesk.ticket',
        [...baseDomain, ['sla_deadline', '<', `${todayStr} 23:59:59`], ['sla_deadline', '!=', false]]).catch(() => 0),
      this.searchCount('helpdesk.ticket', [...baseDomain, ['priority', '=', '3']]),
    ]);
    return {
      open_count: openCount,
      by_stage: byStage.map((g: Record<string, unknown>) => ({
        stage: g['stage_id'], count: g['stage_id_count'] ?? g['__count'] ?? 0,
      })),
      by_priority: byPrio.map((g: Record<string, unknown>) => ({
        priority: g['priority'], count: g['priority_count'] ?? g['__count'] ?? 0,
      })),
      by_assignee: byUser.map((g: Record<string, unknown>) => ({
        user: g['user_id'], count: g['user_id_count'] ?? g['__count'] ?? 0,
      })),
      overdue_count: overdueCnt,
      high_priority_open: highPrio,
    };
  }

  // ---------- 项目仪表盘 ----------

  async getProjectDashboard(options: { project_id?: number } = {}): Promise<{
    projects: Record<string, unknown>[];
    total_tasks_open: number;
    total_tasks_done: number;
    overdue_tasks: number;
  }> {
    const projDomain: Domain = [['active', '=', true]];
    if (options.project_id) projDomain.push(['id', '=', options.project_id]);
    const projects = await this.searchRead('project.project', projDomain,
      ['id', 'name', 'task_count', 'company_id'],
      { limit: 50, order: 'name asc' });
    const projIds = projects.records.map(p => p['id'] as number);
    const taskBaseDomain: Domain = projIds.length > 0 ? [['project_id', 'in', projIds]] : [];
    const todayStr = today();
    const [openCount, doneCount, overdueCount] = await Promise.all([
      this.searchCount('project.task',
        [...taskBaseDomain, ['active', '=', true],
         '|', ['state', 'in', ['01_in_progress', '02_changes_requested', '03_approved']],
              ['state', '=', false]]).catch(() =>
        this.searchCount('project.task', [...taskBaseDomain, ['stage_id.fold', '=', false]])),
      this.searchCount('project.task',
        [...taskBaseDomain, ['state', '=', '1_done']]).catch(() =>
        this.searchCount('project.task', [...taskBaseDomain, ['stage_id.fold', '=', true]])),
      this.searchCount('project.task',
        [...taskBaseDomain, ['date_deadline', '<', todayStr], ['date_deadline', '!=', false]]),
    ]);
    return {
      projects: projects.records.map(p => ({
        id: p['id'], name: p['name'],
        task_count: p['task_count'], company: p['company_id'],
      })),
      total_tasks_open: openCount,
      total_tasks_done: doneCount,
      overdue_tasks: overdueCount,
    };
  }

  // ---------- 我的工作负荷 ----------

  async getMyWorkload(): Promise<{
    user_id: number;
    open_tasks: number;
    overdue_tasks: number;
    pending_activities: number;
    open_tickets: number;
    pending_approvals: number;
    today_calendar_events: number;
  }> {
    const uid = this.uid ?? 0;
    const todayStr = today();
    const [tasks, overdueTasks, activities, tickets, approvals, events] = await Promise.all([
      this.searchCount('project.task',
        [['user_ids', 'in', [uid]], ['active', '=', true]]),
      this.searchCount('project.task',
        [['user_ids', 'in', [uid]], ['active', '=', true],
         ['date_deadline', '<', todayStr], ['date_deadline', '!=', false]]),
      this.searchCount('mail.activity', [['user_id', '=', uid]]),
      this.searchCount('helpdesk.ticket',
        [['user_id', '=', uid], ['close_date', '=', false]]).catch(() => 0),
      this.searchCount('approval.request',
        [['approver_ids.user_id', '=', uid], ['request_status', '=', 'pending']]).catch(() => 0),
      this.searchCount('calendar.event',
        [['partner_ids.user_ids', 'in', [uid]],
         ['start', '>=', `${todayStr} 00:00:00`],
         ['start', '<=', `${todayStr} 23:59:59`]]).catch(() => 0),
    ]);
    return {
      user_id: uid,
      open_tasks: tasks,
      overdue_tasks: overdueTasks,
      pending_activities: activities,
      open_tickets: tickets,
      pending_approvals: approvals,
      today_calendar_events: events,
    };
  }

  // ---------- 薪酬批次 ----------

  async createPayslipRun(values: {
    name: string;
    date_start: string;              // YYYY-MM-DD
    date_end: string;                // YYYY-MM-DD
    company_id?: number;
    employee_ids?: number[];         // 不填则手动添加
    auto_generate?: boolean;         // 创建后自动 generate_payslips
  }): Promise<{ run_id: number; payslip_count: number; actions: string[] }> {
    const actions: string[] = [];
    const payload: Record<string, unknown> = {
      name: values.name,
      date_start: values.date_start,
      date_end: values.date_end,
    };
    if (values.company_id) payload['company_id'] = values.company_id;
    const runId = await this.create('hr.payslip.run', payload);
    actions.push(`创建工资单批次 #${runId}`);

    let payslipCount = 0;
    if (values.auto_generate && values.employee_ids && values.employee_ids.length > 0) {
      try {
        await this.call('hr.payslip.run', 'generate_payslips', [[runId]], {
          employee_ids: values.employee_ids,
        });
        payslipCount = await this.searchCount('hr.payslip', [['payslip_run_id', '=', runId]]);
        actions.push(`已生成 ${payslipCount} 条 payslip`);
      } catch (e) {
        actions.push(`generate_payslips 失败：${String(e)}`);
      }
    }

    return { run_id: runId, payslip_count: payslipCount, actions };
  }

  // ==================== 个人视图 + 跨域桥 + 库存 + 预测（v1.15） ====================
  //
  // v1.15 围绕三个主题：
  // 1) 个人高频问题合并：odoo_my_overdues / odoo_my_today / odoo_my_unread
  // 2) 跨模块桥接：helpdesk→task / lead→project / 发逾期催款
  // 3) 库存深化：低库存预警 / 按仓库聚合 / picking 验收 / 仓库 dashboard
  // 4) 多公司可见性 + 加权销售预测

  // ---------- 个人视图 3 工具 ----------

  async getMyOverdues(): Promise<{
    today: string;
    overdue_tasks: Record<string, unknown>[];
    overdue_activities: Record<string, unknown>[];
    overdue_tickets: Record<string, unknown>[];
    overdue_invoices: Record<string, unknown>[];
    total_count: number;
  }> {
    const uid = this.uid ?? 0;
    const todayStr = today();
    const [tasks, activities, tickets, invoices] = await Promise.all([
      this.searchRead('project.task',
        [['user_ids', 'in', [uid]], ['active', '=', true],
         ['date_deadline', '<', todayStr], ['date_deadline', '!=', false]],
        ['id', 'name', 'project_id', 'date_deadline', 'priority'],
        { limit: 50, order: 'date_deadline asc' }),
      this.searchRead('mail.activity',
        [['user_id', '=', uid], ['date_deadline', '<', todayStr]],
        ['id', 'summary', 'date_deadline', 'res_model', 'res_id', 'activity_type_id'],
        { limit: 50, order: 'date_deadline asc' }),
      this.searchRead('helpdesk.ticket',
        [['user_id', '=', uid], ['close_date', '=', false],
         ['sla_deadline', '<', `${todayStr} 23:59:59`], ['sla_deadline', '!=', false]],
        ['id', 'name', 'partner_id', 'sla_deadline', 'priority'],
        { limit: 50, order: 'sla_deadline asc' }).catch(() => ({ records: [], length: 0 })),
      this.searchRead('account.move',
        [['move_type', '=', 'out_invoice'], ['state', '=', 'posted'],
         ['payment_state', 'in', ['not_paid', 'partial']],
         ['invoice_date_due', '<', todayStr],
         ['invoice_user_id', '=', uid]],
        ['id', 'name', 'partner_id', 'invoice_date_due', 'amount_residual', 'currency_id'],
        { limit: 50, order: 'invoice_date_due asc' }).catch(() => ({ records: [], length: 0 })),
    ]);
    const total = tasks.records.length + activities.records.length
                + tickets.records.length + invoices.records.length;
    return {
      today: todayStr,
      overdue_tasks: tasks.records.map(t => ({
        id: t['id'], name: t['name'], project: t['project_id'],
        deadline: t['date_deadline'], priority: t['priority'],
      })),
      overdue_activities: activities.records.map(a => ({
        id: a['id'], summary: a['summary'], deadline: a['date_deadline'],
        related: { model: a['res_model'], id: a['res_id'] },
        type: a['activity_type_id'],
      })),
      overdue_tickets: tickets.records.map(t => ({
        id: t['id'], name: t['name'], partner: t['partner_id'],
        sla_deadline: t['sla_deadline'], priority: t['priority'],
      })),
      overdue_invoices: invoices.records.map(i => ({
        id: i['id'], name: i['name'], partner: i['partner_id'],
        due_date: i['invoice_date_due'], amount: i['amount_residual'],
        currency: i['currency_id'],
      })),
      total_count: total,
    };
  }

  async getMyToday(): Promise<{
    today: string;
    today_tasks: Record<string, unknown>[];
    today_activities: Record<string, unknown>[];
    today_calendar_events: Record<string, unknown>[];
    today_due_invoices: Record<string, unknown>[];
    total_count: number;
  }> {
    const uid = this.uid ?? 0;
    const todayStr = today();
    const [tasks, activities, events, invoices] = await Promise.all([
      this.searchRead('project.task',
        [['user_ids', 'in', [uid]], ['active', '=', true],
         ['date_deadline', '=', todayStr]],
        ['id', 'name', 'project_id', 'date_deadline', 'priority'],
        { limit: 50, order: 'priority desc' }),
      this.searchRead('mail.activity',
        [['user_id', '=', uid], ['date_deadline', '=', todayStr]],
        ['id', 'summary', 'date_deadline', 'res_model', 'res_id', 'activity_type_id'],
        { limit: 50 }),
      this.searchRead('calendar.event',
        [['partner_ids.user_ids', 'in', [uid]],
         ['start', '>=', `${todayStr} 00:00:00`],
         ['start', '<=', `${todayStr} 23:59:59`]],
        ['id', 'name', 'start', 'stop', 'duration', 'location'],
        { limit: 50, order: 'start asc' }).catch(() => ({ records: [], length: 0 })),
      this.searchRead('account.move',
        [['move_type', '=', 'out_invoice'], ['state', '=', 'posted'],
         ['payment_state', 'in', ['not_paid', 'partial']],
         ['invoice_date_due', '=', todayStr],
         ['invoice_user_id', '=', uid]],
        ['id', 'name', 'partner_id', 'amount_residual', 'currency_id'],
        { limit: 50 }).catch(() => ({ records: [], length: 0 })),
    ]);
    const total = tasks.records.length + activities.records.length
                + events.records.length + invoices.records.length;
    return {
      today: todayStr,
      today_tasks: tasks.records.map(t => ({
        id: t['id'], name: t['name'], project: t['project_id'], priority: t['priority'],
      })),
      today_activities: activities.records.map(a => ({
        id: a['id'], summary: a['summary'],
        related: { model: a['res_model'], id: a['res_id'] },
        type: a['activity_type_id'],
      })),
      today_calendar_events: events.records.map(e => ({
        id: e['id'], name: e['name'], start: e['start'], stop: e['stop'],
        duration: e['duration'], location: e['location'],
      })),
      today_due_invoices: invoices.records.map(i => ({
        id: i['id'], name: i['name'], partner: i['partner_id'],
        amount: i['amount_residual'], currency: i['currency_id'],
      })),
      total_count: total,
    };
  }

  async getMyUnread(): Promise<{
    unread_count: number;
    unread_messages: Record<string, unknown>[];
  }> {
    const uid = this.uid ?? 0;
    // 找当前 user 的 partner_id
    const me = await this.read('res.users', [uid], ['partner_id']);
    const partnerArr = me[0]?.['partner_id'];
    if (!Array.isArray(partnerArr)) {
      return { unread_count: 0, unread_messages: [] };
    }
    const partnerId = partnerArr[0] as number;

    // mail.notification 按 res_partner_id + is_read=false 找未读
    const notifs = await this.searchRead('mail.notification',
      [['res_partner_id', '=', partnerId], ['is_read', '=', false],
       ['notification_type', '=', 'inbox']],
      ['id', 'mail_message_id', 'notification_type'],
      { limit: 100, order: 'id desc' });
    const messageIds = notifs.records
      .map(n => Array.isArray(n['mail_message_id']) ? n['mail_message_id'][0] as number : null)
      .filter((x): x is number => x !== null);
    if (messageIds.length === 0) {
      return { unread_count: 0, unread_messages: [] };
    }
    const messages = await this.read('mail.message', messageIds,
      ['id', 'subject', 'body', 'author_id', 'date', 'model', 'res_id', 'message_type']);
    return {
      unread_count: messages.length,
      unread_messages: messages.map(m => ({
        id: m['id'], subject: m['subject'],
        body_preview: typeof m['body'] === 'string'
          ? (m['body'] as string).replace(/<[^>]+>/g, '').substring(0, 200)
          : '',
        author: m['author_id'], date: m['date'],
        related: { model: m['model'], id: m['res_id'] },
        type: m['message_type'],
      })),
    };
  }

  // ---------- CRM 智能助手 2 工具 ----------

  async getCrmStaleLeads(options: {
    user_id?: number;
    days_no_activity?: number;       // 默认 14 天
    limit?: number;
  } = {}): Promise<{
    threshold_days: number;
    threshold_date: string;
    stale_leads: Record<string, unknown>[];
  }> {
    const days = options.days_no_activity ?? 14;
    const threshold = new Date(Date.now() - days * 86400000).toISOString().substring(0, 10);
    const domain: Domain = [
      ['type', '=', 'opportunity'],
      ['active', '=', true],
      // 没赢没输（非 won/lost stage 上）— probability < 100 且 active
      ['probability', '<', 100],
      // 最近 N 天没动：date_last_stage_update < threshold
      ['date_last_stage_update', '<', `${threshold} 00:00:00`],
    ];
    if (options.user_id) domain.push(['user_id', '=', options.user_id]);
    const result = await this.searchRead('crm.lead', domain,
      ['id', 'name', 'partner_id', 'user_id', 'stage_id',
       'expected_revenue', 'probability', 'date_last_stage_update',
       'date_deadline', 'priority'],
      { limit: options.limit ?? 30, order: 'date_last_stage_update asc' });
    return {
      threshold_days: days,
      threshold_date: threshold,
      stale_leads: result.records.map(l => ({
        id: l['id'], name: l['name'], partner: l['partner_id'],
        user: l['user_id'], stage: l['stage_id'],
        revenue: l['expected_revenue'], probability: l['probability'],
        last_stage_update: l['date_last_stage_update'],
        deadline: l['date_deadline'], priority: l['priority'],
      })),
    };
  }

  async getCrmNextAction(leadId: number): Promise<{
    lead: OdooRecord | null;
    days_in_stage: number | null;
    has_pending_activity: boolean;
    recommendation: string;
    suggested_actions: string[];
  }> {
    const leads = await this.read('crm.lead', [leadId],
      ['id', 'name', 'stage_id', 'partner_id', 'user_id', 'date_deadline',
       'date_last_stage_update', 'expected_revenue', 'probability',
       'activity_ids', 'next_activity_id', 'activity_state']);
    const lead = leads[0] ?? null;
    if (!lead) {
      return {
        lead: null, days_in_stage: null, has_pending_activity: false,
        recommendation: '商机不存在或不可访问',
        suggested_actions: [],
      };
    }
    const lastStageStr = lead['date_last_stage_update'] as string | undefined;
    let daysInStage: number | null = null;
    if (typeof lastStageStr === 'string' && lastStageStr.length >= 10) {
      const lastStage = new Date(lastStageStr.replace(' ', 'T') + 'Z');
      daysInStage = Math.floor((Date.now() - lastStage.getTime()) / 86400000);
    }
    const hasPending = Array.isArray(lead['activity_ids']) && (lead['activity_ids'] as unknown[]).length > 0;
    const probability = Number(lead['probability'] ?? 0);

    // 简单规则推荐
    const suggestions: string[] = [];
    let recommendation = '商机推进正常';
    if (daysInStage !== null && daysInStage > 14 && !hasPending) {
      recommendation = `已 ${daysInStage} 天没动且无待办活动，建议立即跟进`;
      suggestions.push('调 odoo_create_activity 创建一个跟进电话/邮件活动');
      suggestions.push('或调 odoo_crm_update 更新 stage_id 推进商机');
      suggestions.push('或调 odoo_send_message 给商机发一条进度说明 chatter');
    } else if (daysInStage !== null && daysInStage > 7 && probability >= 50) {
      recommendation = `${daysInStage} 天没动但概率 ${probability}% 较高，建议主动联系决策人`;
      suggestions.push('调 odoo_send_message 写一条客户进度说明');
      suggestions.push('调 odoo_create_activity 安排一次客户拜访');
    } else if (probability < 30 && daysInStage !== null && daysInStage > 30) {
      recommendation = `概率 ${probability}% 低 + 30+ 天无变动，考虑 odoo_crm_lost 标记输单`;
      suggestions.push('如确认无希望：调 odoo_crm_lost 关闭');
      suggestions.push('如还有机会：先调 odoo_crm_update 改 probability 和 stage');
    } else if (hasPending) {
      recommendation = `已有待办活动，无需额外动作`;
      suggestions.push('调 odoo_list_activities 查看具体待办');
    } else {
      suggestions.push('调 odoo_create_activity 安排下一步跟进');
      suggestions.push('调 odoo_crm_update 更新 stage_id / probability');
    }

    return {
      lead, days_in_stage: daysInStage, has_pending_activity: hasPending,
      recommendation, suggested_actions: suggestions,
    };
  }

  // ---------- 跨模块桥 3 工具 ----------

  async helpdeskToTask(values: {
    ticket_id: number;
    project_id: number;
    task_name?: string;              // 不填默认用 ticket.name
    user_ids?: number[];             // 任务经办人，不填默认 ticket.user_id
    keep_chatter_link?: boolean;     // 在 ticket chatter 里写"已转任务 #X"
  }): Promise<{ task_id: number; ticket_id: number; actions: string[] }> {
    const actions: string[] = [];
    const ticket = (await this.read('helpdesk.ticket', [values.ticket_id],
      ['id', 'name', 'description', 'partner_id', 'user_id']))[0];
    if (!ticket) throw new Error(`未找到工单 #${values.ticket_id}`);

    const taskValues: Record<string, unknown> = {
      name: values.task_name ?? `[来自工单 #${values.ticket_id}] ${ticket['name']}`,
      project_id: values.project_id,
      description: ticket['description'] ?? '',
    };
    if (values.user_ids && values.user_ids.length > 0) {
      taskValues['user_ids'] = [[6, 0, values.user_ids]];
    } else {
      const ticketUser = Array.isArray(ticket['user_id']) ? ticket['user_id'][0] as number : null;
      if (ticketUser) taskValues['user_ids'] = [[6, 0, [ticketUser]]];
    }
    if (Array.isArray(ticket['partner_id']) && ticket['partner_id'][0]) {
      taskValues['partner_id'] = ticket['partner_id'][0];
    }
    const taskId = await this.create('project.task', taskValues);
    actions.push(`已创建任务 #${taskId}`);

    if (values.keep_chatter_link !== false) {
      try {
        await this.call('helpdesk.ticket', 'message_post', [[values.ticket_id]], {
          body: `已转为项目任务 <a href="#" data-oe-model="project.task" data-oe-id="${taskId}">#${taskId}</a>`,
          message_type: 'comment',
          subtype_xmlid: 'mail.mt_comment',
        });
        actions.push('已在工单 chatter 留下任务链接');
      } catch (e) {
        actions.push(`chatter 写入失败：${String(e)}`);
      }
    }
    return { task_id: taskId, ticket_id: values.ticket_id, actions };
  }

  async leadToProject(values: {
    lead_id: number;
    project_name?: string;           // 默认用 lead.name
    partner_id?: number;             // 默认用 lead.partner_id
    user_id?: number;                // 项目经理
    mark_won?: boolean;              // 顺手把商机标记 won（默认 false 让用户先确认）
  }): Promise<{ project_id: number; lead_id: number; actions: string[] }> {
    const actions: string[] = [];
    const lead = (await this.read('crm.lead', [values.lead_id],
      ['id', 'name', 'partner_id', 'user_id', 'description']))[0];
    if (!lead) throw new Error(`未找到商机 #${values.lead_id}`);

    const projValues: Record<string, unknown> = {
      name: values.project_name ?? lead['name'] ?? `项目 from 商机 #${values.lead_id}`,
      description: lead['description'] ?? '',
    };
    const partnerId = values.partner_id
      ?? (Array.isArray(lead['partner_id']) ? lead['partner_id'][0] as number : null);
    if (partnerId) projValues['partner_id'] = partnerId;
    const managerId = values.user_id
      ?? (Array.isArray(lead['user_id']) ? lead['user_id'][0] as number : null);
    if (managerId) projValues['user_id'] = managerId;

    const projId = await this.create('project.project', projValues);
    actions.push(`已创建项目 #${projId}`);

    if (values.mark_won) {
      try {
        await this.call('crm.lead', 'action_set_won_rainbowman', [[values.lead_id]]);
        actions.push(`商机 #${values.lead_id} 标记为赢单`);
      } catch (e) {
        // fallback: 直接 write probability=100 + active=false
        try {
          await this.write('crm.lead', [values.lead_id], { probability: 100 });
          actions.push(`商机 #${values.lead_id} probability 设为 100（赢单兜底）`);
        } catch (e2) {
          actions.push(`赢单标记失败：${String(e2)}`);
        }
      }
    }

    // 在商机 chatter 留链接
    try {
      await this.call('crm.lead', 'message_post', [[values.lead_id]], {
        body: `已转化为项目 <a href="#" data-oe-model="project.project" data-oe-id="${projId}">#${projId}</a>`,
        message_type: 'comment',
        subtype_xmlid: 'mail.mt_comment',
      });
      actions.push('已在商机 chatter 留下项目链接');
    } catch { /* noop */ }

    return { project_id: projId, lead_id: values.lead_id, actions };
  }

  async sendInvoiceReminder(values: {
    invoice_id: number;
    custom_message?: string;
  }): Promise<{ invoice_id: number; partner: unknown; actions: string[] }> {
    const actions: string[] = [];
    const invoice = (await this.read('account.move', [values.invoice_id],
      ['id', 'name', 'partner_id', 'invoice_date_due', 'amount_residual', 'currency_id']))[0];
    if (!invoice) throw new Error(`未找到发票 #${values.invoice_id}`);
    const partner = invoice['partner_id'];

    const todayStr = today();
    const dueDate = invoice['invoice_date_due'] as string | undefined;
    let daysOverdue = 0;
    if (dueDate) {
      daysOverdue = Math.max(0, Math.floor((Date.now() - new Date(dueDate + 'T00:00:00Z').getTime()) / 86400000));
    }
    const amount = invoice['amount_residual'];
    const currencyArr = invoice['currency_id'];
    const currencyName = Array.isArray(currencyArr) ? currencyArr[1] : '';

    const body = values.custom_message ?? `您好，发票 ${invoice['name']} 已逾期 ${daysOverdue} 天，未付金额 ${amount} ${currencyName}，麻烦尽快安排付款。今天日期 ${todayStr}。`;

    try {
      await this.call('account.move', 'message_post', [[values.invoice_id]], {
        body,
        message_type: 'comment',
        subtype_xmlid: 'mail.mt_comment',
        partner_ids: Array.isArray(partner) ? [partner[0]] : [],
      });
      actions.push(`已通过 chatter 发送催款给 ${Array.isArray(partner) ? partner[1] : '客户'}`);
    } catch (e) {
      actions.push(`催款发送失败：${String(e)}`);
    }
    return { invoice_id: values.invoice_id, partner, actions };
  }

  // ---------- 库存深化 4 工具 ----------

  async getStockLowAlerts(options: {
    warehouse_id?: number;
    limit?: number;
  } = {}): Promise<{
    alert_count: number;
    alerts: Record<string, unknown>[];
  }> {
    // stock.warehouse.orderpoint 上有 qty_to_order > 0 的就是触发预警的
    const domain: Domain = [['qty_to_order', '>', 0]];
    if (options.warehouse_id) domain.push(['warehouse_id', '=', options.warehouse_id]);
    const result = await this.searchRead('stock.warehouse.orderpoint', domain,
      ['id', 'product_id', 'warehouse_id', 'location_id',
       'product_min_qty', 'product_max_qty', 'qty_to_order', 'company_id'],
      { limit: options.limit ?? 50, order: 'qty_to_order desc' });
    return {
      alert_count: result.records.length,
      alerts: result.records.map(r => ({
        id: r['id'], product: r['product_id'], warehouse: r['warehouse_id'],
        location: r['location_id'], min_qty: r['product_min_qty'],
        max_qty: r['product_max_qty'], to_order: r['qty_to_order'],
        company: r['company_id'],
      })),
    };
  }

  async getStockByLocation(options: {
    location_id?: number;
    product_id?: number;
    company_id?: number;
  } = {}): Promise<{
    by_location: Record<string, unknown>[];
    total_quantity: number;
  }> {
    const domain: Domain = [];
    if (options.location_id) domain.push(['location_id', '=', options.location_id]);
    if (options.product_id) domain.push(['product_id', '=', options.product_id]);
    if (options.company_id) domain.push(['company_id', '=', options.company_id]);
    const groups = await this.readGroup('stock.quant', domain,
      ['quantity:sum', 'reserved_quantity:sum'],
      ['location_id'], { limit: 200, orderby: 'quantity desc' });
    const total = groups.reduce((s: number, g: Record<string, unknown>) => s + Number(g['quantity'] ?? 0), 0);
    return {
      by_location: groups.map((g: Record<string, unknown>) => ({
        location: g['location_id'],
        on_hand: g['quantity'] ?? 0,
        reserved: g['reserved_quantity'] ?? 0,
        available: Number(g['quantity'] ?? 0) - Number(g['reserved_quantity'] ?? 0),
        product_count: g['location_id_count'] ?? g['__count'] ?? 0,
      })),
      total_quantity: total,
    };
  }

  async validatePicking(pickingId: number): Promise<unknown> {
    // stock.picking.button_validate 是 single-record action
    return this.call('stock.picking', 'button_validate', [[pickingId]]);
  }

  async getWarehouseDashboard(options: { warehouse_id?: number } = {}): Promise<{
    warehouses: Record<string, unknown>[];
    pending_in: number;               // 待入库 (incoming)
    pending_out: number;              // 待出库 (outgoing)
    pending_internal: number;         // 待内部调拨
    backorders: number;               // 部分完成的回单
  }> {
    const whDomain: Domain = [['active', '=', true]];
    if (options.warehouse_id) whDomain.push(['id', '=', options.warehouse_id]);
    const warehouses = await this.searchRead('stock.warehouse', whDomain,
      ['id', 'name', 'code', 'company_id'],
      { limit: 50, order: 'name asc' });

    const baseDomain: Domain = [['state', 'in', ['confirmed', 'assigned', 'waiting']]];
    if (options.warehouse_id) {
      baseDomain.push(['picking_type_id.warehouse_id', '=', options.warehouse_id]);
    }
    const [pIn, pOut, pInt, backorders] = await Promise.all([
      this.searchCount('stock.picking',
        [...baseDomain, ['picking_type_code', '=', 'incoming']]),
      this.searchCount('stock.picking',
        [...baseDomain, ['picking_type_code', '=', 'outgoing']]),
      this.searchCount('stock.picking',
        [...baseDomain, ['picking_type_code', '=', 'internal']]),
      this.searchCount('stock.picking',
        [...baseDomain, ['backorder_id', '!=', false]]),
    ]);
    return {
      warehouses: warehouses.records.map(w => ({
        id: w['id'], name: w['name'], code: w['code'], company: w['company_id'],
      })),
      pending_in: pIn,
      pending_out: pOut,
      pending_internal: pInt,
      backorders,
    };
  }

  // ---------- 多公司 1 工具 ----------

  async getCompanies(): Promise<{
    current_company_id: number | null;
    allowed_company_ids: number[];
    companies: Record<string, unknown>[];
  }> {
    // 拿当前 user 的 company_id 和 company_ids
    const me = await this.read('res.users', [this.uid ?? 0],
      ['id', 'name', 'company_id', 'company_ids']);
    const companyArr = me[0]?.['company_id'];
    const currentId = Array.isArray(companyArr) ? companyArr[0] as number : null;
    const allowedIds = Array.isArray(me[0]?.['company_ids'])
      ? (me[0]?.['company_ids'] as number[])
      : (currentId ? [currentId] : []);
    if (allowedIds.length === 0) {
      return { current_company_id: currentId, allowed_company_ids: [], companies: [] };
    }
    const companies = await this.read('res.company', allowedIds,
      ['id', 'name', 'partner_id', 'email', 'phone', 'currency_id', 'country_id', 'parent_id']);
    return {
      current_company_id: currentId,
      allowed_company_ids: allowedIds,
      companies: companies.map(c => ({
        id: c['id'], name: c['name'], partner: c['partner_id'],
        email: c['email'], phone: c['phone'],
        currency: c['currency_id'], country: c['country_id'],
        parent: c['parent_id'],
      })),
    };
  }

  // ---------- 加权销售预测 1 工具 ----------

  async getSalesForecast(options: {
    user_id?: number;
    horizon_days?: number;            // 预测窗口（默认 90 天）
  } = {}): Promise<{
    horizon: { from: string; to: string; days: number };
    weighted_pipeline: number;        // sum(expected_revenue × probability/100)
    raw_pipeline: number;             // sum(expected_revenue)
    by_stage: Record<string, unknown>[];
    by_user: Record<string, unknown>[];
    confirmed_so_amount: number;      // 已确认 sale.order 金额（同窗口）
  }> {
    const horizon = options.horizon_days ?? 90;
    const dFrom = today();
    const dToDate = new Date();
    dToDate.setDate(dToDate.getDate() + horizon);
    const dTo = dToDate.toISOString().substring(0, 10);

    const domain: Domain = [
      ['type', '=', 'opportunity'],
      ['active', '=', true],
      ['probability', '<', 100],
      ['probability', '>', 0],
    ];
    if (options.user_id) domain.push(['user_id', '=', options.user_id]);

    const [opportunities, byStage, byUser, soAgg] = await Promise.all([
      this.searchRead('crm.lead', domain, ['expected_revenue', 'probability'], { limit: 1000 }),
      this.readGroup('crm.lead', domain,
        ['expected_revenue:sum', 'probability:avg'], ['stage_id'], { limit: 30 }),
      this.readGroup('crm.lead', domain,
        ['expected_revenue:sum'], ['user_id'], { limit: 30, orderby: 'expected_revenue desc' }),
      this.readGroup('sale.order',
        [['date_order', '>=', `${dFrom} 00:00:00`],
         '|', ['state', '=', 'sale'], ['state', '=', 'done']],
        ['amount_total:sum'], [], { limit: 1 }),
    ]);

    const weighted = opportunities.records.reduce((sum, o) =>
      sum + Number(o['expected_revenue'] ?? 0) * Number(o['probability'] ?? 0) / 100, 0);
    const raw = opportunities.records.reduce((sum, o) =>
      sum + Number(o['expected_revenue'] ?? 0), 0);
    const soTotal = Array.isArray(soAgg) && soAgg[0]
      ? Number((soAgg[0] as Record<string, unknown>)['amount_total'] ?? 0) : 0;

    return {
      horizon: { from: dFrom, to: dTo, days: horizon },
      weighted_pipeline: Math.round(weighted * 100) / 100,
      raw_pipeline: raw,
      by_stage: byStage.map((g: Record<string, unknown>) => ({
        stage: g['stage_id'],
        revenue: g['expected_revenue'] ?? 0,
        avg_probability: g['probability'] ?? 0,
        count: g['stage_id_count'] ?? g['__count'] ?? 0,
      })),
      by_user: byUser.map((g: Record<string, unknown>) => ({
        user: g['user_id'],
        revenue: g['expected_revenue'] ?? 0,
        count: g['user_id_count'] ?? g['__count'] ?? 0,
      })),
      confirmed_so_amount: soTotal,
    };
  }

  // ==================== 业务深化 + 智能洞察 + 报表（v1.16） ====================
  //
  // v1.16 五个主题：
  //   - 采购深化：v1.0 的 purchase_orders 只有 list，补 create / confirm /
  //     dashboard / vendor_bill_aging
  //   - 生产 MRP：从 0 起步，加 mo_list / mo_confirm / bom_query
  //   - 会计深化：journal_entries / payment_register（走 wizard）/
  //     chart_of_accounts
  //   - 智能洞察：anomaly_detect / kpi_summary
  //   - 报表 / 数据导出：pdf_report URL 构造 / export_csv 自渲染

  // ---------- 采购深化 4 工具 ----------

  async createPurchaseOrder(values: {
    partner_id: number;
    order_lines: Array<{
      product_id: number;
      product_qty: number;
      price_unit?: number;
      name?: string;                   // 描述，不填默认产品名
    }>;
    date_planned?: string;             // YYYY-MM-DD HH:MM:SS
    notes?: string;
    company_id?: number;
  }): Promise<number> {
    const order_line: unknown[] = values.order_lines.map(l => {
      const lineVals: Record<string, unknown> = {
        product_id: l.product_id,
        product_qty: l.product_qty,
      };
      if (l.price_unit !== undefined) lineVals['price_unit'] = l.price_unit;
      if (l.name) lineVals['name'] = l.name;
      return [0, 0, lineVals];
    });
    const payload: Record<string, unknown> = {
      partner_id: values.partner_id,
      order_line,
    };
    if (values.date_planned) payload['date_planned'] = values.date_planned;
    if (values.notes) payload['notes'] = values.notes;
    if (values.company_id) payload['company_id'] = values.company_id;
    return this.create('purchase.order', payload);
  }

  async confirmPurchaseOrder(ids: number[]): Promise<unknown> {
    // button_confirm 在 v18+ 支持多 record，老版本可能要 for-loop
    try { return await this.call('purchase.order', 'button_confirm', [ids]); }
    catch {
      const results: unknown[] = [];
      for (const id of ids) {
        try { results.push(await this.call('purchase.order', 'button_confirm', [[id]])); }
        catch (e) { results.push({ error: String(e), id }); }
      }
      return results;
    }
  }

  async getPurchaseDashboard(options: {
    date_from?: string;
    date_to?: string;
  } = {}): Promise<{
    period: { from: string; to: string };
    total_amount: number;
    order_count: number;
    by_state: Record<string, unknown>[];
    top_vendors: Record<string, unknown>[];
    pending_receipt_count: number;
    pending_bill_count: number;
  }> {
    const todayStr = today();
    const dFrom = options.date_from ?? todayStr.substring(0, 7) + '-01';
    const dTo = options.date_to ?? todayStr;
    const baseDomain: Domain = [
      ['date_order', '>=', `${dFrom} 00:00:00`],
      ['date_order', '<=', `${dTo} 23:59:59`],
    ];
    const [byState, totals, topVendors, pendingReceipt, pendingBill] = await Promise.all([
      this.readGroup('purchase.order', baseDomain, [], ['state'], { limit: 10 }),
      this.readGroup('purchase.order',
        [...baseDomain, '|', ['state', '=', 'purchase'], ['state', '=', 'done']],
        ['amount_total:sum'], [], { limit: 1 }),
      this.readGroup('purchase.order',
        [...baseDomain, '|', ['state', '=', 'purchase'], ['state', '=', 'done']],
        ['amount_total:sum'], ['partner_id'],
        { limit: 10, orderby: 'amount_total desc' }),
      this.searchCount('purchase.order',
        ['|', ['state', '=', 'purchase'], ['state', '=', 'done'],
         ['receipt_status', 'in', ['pending', 'started']]]).catch(() => 0),
      this.searchCount('purchase.order',
        ['|', ['state', '=', 'purchase'], ['state', '=', 'done'],
         ['invoice_status', 'in', ['to invoice', 'no']]]),
    ]);
    const total = Array.isArray(totals) && totals[0]
      ? Number((totals[0] as Record<string, unknown>)['amount_total'] ?? 0) : 0;
    const orderCount = byState.reduce((s: number, g: Record<string, unknown>) =>
      s + Number(g['state_count'] ?? g['__count'] ?? 0), 0);
    return {
      period: { from: dFrom, to: dTo },
      total_amount: total,
      order_count: orderCount,
      by_state: byState.map((g: Record<string, unknown>) => ({
        state: g['state'], count: g['state_count'] ?? g['__count'] ?? 0,
      })),
      top_vendors: topVendors.map((g: Record<string, unknown>) => ({
        partner: g['partner_id'],
        amount: g['amount_total'] ?? 0,
        order_count: g['partner_id_count'] ?? g['__count'] ?? 0,
      })),
      pending_receipt_count: pendingReceipt,
      pending_bill_count: pendingBill,
    };
  }

  async getVendorBillAging(options: {
    partner_id?: number;
    company_id?: number;
  } = {}): Promise<{
    today: string;
    bucket_0_30: { count: number; amount: number };
    bucket_31_60: { count: number; amount: number };
    bucket_61_90: { count: number; amount: number };
    bucket_90_plus: { count: number; amount: number };
    not_due: { count: number; amount: number };
    total_outstanding: number;
  }> {
    // 复用 getInvoiceAging 的桶模型，但 move_type='in_invoice'（供应商账单）
    const todayStr = today();
    const baseDomain: Domain = [
      ['move_type', '=', 'in_invoice'],
      ['state', '=', 'posted'],
      ['payment_state', 'in', ['not_paid', 'partial']],
    ];
    if (options.partner_id) baseDomain.push(['partner_id', '=', options.partner_id]);
    if (options.company_id) baseDomain.push(['company_id', '=', options.company_id]);
    function dateOffset(days: number): string {
      const d = new Date();
      d.setDate(d.getDate() - days);
      return d.toISOString().substring(0, 10);
    }
    const day30 = dateOffset(30), day60 = dateOffset(60), day90 = dateOffset(90);
    const [b0, b1, b2, b3, bn] = await Promise.all([
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '<=', todayStr], ['invoice_date_due', '>', day30]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '<=', day30], ['invoice_date_due', '>', day60]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '<=', day60], ['invoice_date_due', '>', day90]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '<=', day90]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [...baseDomain, ['invoice_date_due', '>', todayStr]],
        ['amount_residual:sum'], [], { limit: 1 }),
    ]);
    function unpack(g: Record<string, unknown>[]): { count: number; amount: number } {
      const row = g[0];
      return {
        count: Number(row?.['__count'] ?? 0),
        amount: Number(row?.['amount_residual'] ?? 0),
      };
    }
    const u0 = unpack(b0), u1 = unpack(b1), u2 = unpack(b2), u3 = unpack(b3), uN = unpack(bn);
    return {
      today: todayStr,
      bucket_0_30: u0, bucket_31_60: u1, bucket_61_90: u2,
      bucket_90_plus: u3, not_due: uN,
      total_outstanding: u0.amount + u1.amount + u2.amount + u3.amount + uN.amount,
    };
  }

  // ---------- 生产 MRP 3 工具 ----------

  async getMrpProductions(options: {
    state?: 'draft'|'confirmed'|'progress'|'to_close'|'done'|'cancel';
    product_id?: number;
    keyword?: string;                  // 按 name (单号) 模糊搜
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.state) domain.push(['state', '=', options.state]);
    if (options.product_id) domain.push(['product_id', '=', options.product_id]);
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    const result = await this.searchRead('mrp.production', domain,
      ['id', 'name', 'product_id', 'product_qty', 'state', 'date_start',
       'date_finished', 'bom_id', 'company_id', 'priority'],
      { limit: options.limit ?? 30, order: 'date_start desc' });
    return result.records;
  }

  async confirmMrpProduction(ids: number[]): Promise<unknown> {
    // mrp.production.action_confirm（draft → confirmed）
    return this.call('mrp.production', 'action_confirm', [ids]);
  }

  async getBomQuery(options: {
    product_id?: number;
    product_tmpl_id?: number;
    bom_id?: number;
    limit?: number;
  } = {}): Promise<{
    boms: Record<string, unknown>[];
  }> {
    const domain: Domain = [];
    if (options.bom_id) domain.push(['id', '=', options.bom_id]);
    if (options.product_id) domain.push(['product_id', '=', options.product_id]);
    if (options.product_tmpl_id) domain.push(['product_tmpl_id', '=', options.product_tmpl_id]);
    const boms = await this.searchRead('mrp.bom', domain,
      ['id', 'product_tmpl_id', 'product_id', 'type', 'product_qty',
       'product_uom_id', 'bom_line_ids', 'company_id', 'code'],
      { limit: options.limit ?? 30 });
    if (boms.records.length === 0) return { boms: [] };
    // 把每个 BOM 的 line 一起读出来
    const allLineIds = boms.records.flatMap(b =>
      Array.isArray(b['bom_line_ids']) ? (b['bom_line_ids'] as number[]) : []);
    const lines = allLineIds.length > 0
      ? await this.read('mrp.bom.line', allLineIds,
          ['id', 'bom_id', 'product_id', 'product_qty', 'product_uom_id'])
      : [];
    const linesByBomId = new Map<number, OdooRecord[]>();
    for (const l of lines) {
      const bomArr = l['bom_id'];
      const bomId = Array.isArray(bomArr) ? bomArr[0] as number : 0;
      const arr = linesByBomId.get(bomId) ?? [];
      arr.push(l);
      linesByBomId.set(bomId, arr);
    }
    return {
      boms: boms.records.map(b => ({
        id: b['id'], product: b['product_id'], product_tmpl: b['product_tmpl_id'],
        type: b['type'], qty: b['product_qty'], uom: b['product_uom_id'],
        code: b['code'], company: b['company_id'],
        lines: (linesByBomId.get(b['id'] as number) ?? []).map(l => ({
          id: l['id'], product: l['product_id'],
          qty: l['product_qty'], uom: l['product_uom_id'],
        })),
      })),
    };
  }

  // ---------- 会计深化 3 工具 ----------

  async getJournalEntries(options: {
    journal_id?: number;
    state?: 'draft' | 'posted' | 'cancel';
    date_from?: string;
    date_to?: string;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const todayStr = today();
    const dFrom = options.date_from ?? todayStr.substring(0, 7) + '-01';
    const dTo = options.date_to ?? todayStr;
    const domain: Domain = [
      ['date', '>=', dFrom],
      ['date', '<=', dTo],
      ['move_type', '=', 'entry'],   // 只看普通凭证（排除发票/账单）
    ];
    if (options.journal_id) domain.push(['journal_id', '=', options.journal_id]);
    if (options.state) domain.push(['state', '=', options.state]);
    const result = await this.searchRead('account.move', domain,
      ['id', 'name', 'date', 'journal_id', 'state', 'amount_total_signed', 'ref'],
      { limit: options.limit ?? 30, order: 'date desc, id desc' });
    return result.records;
  }

  async registerPayment(values: {
    invoice_ids: number[];               // 一组 account.move id
    amount?: number;                     // 不填默认全额
    payment_date?: string;               // YYYY-MM-DD，默认今天
    journal_id?: number;                 // 不填默认配置的现金/银行账户
    communication?: string;              // 备注
  }): Promise<{
    payment_count: number;
    actions: string[];
  }> {
    const actions: string[] = [];
    // account.payment.register 是 transient model wizard
    const wizardVals: Record<string, unknown> = {
      payment_date: values.payment_date ?? today(),
    };
    if (values.amount !== undefined) wizardVals['amount'] = values.amount;
    if (values.journal_id) wizardVals['journal_id'] = values.journal_id;
    if (values.communication) wizardVals['communication'] = values.communication;

    // 在 context 注入 active_model + active_ids
    const wizardId = await this.call('account.payment.register', 'create', [wizardVals], {
      context: {
        active_model: 'account.move',
        active_ids: values.invoice_ids,
      },
    }) as number;
    actions.push(`创建 register 向导 #${wizardId}`);

    // 触发 action_create_payments
    await this.call('account.payment.register', 'action_create_payments', [[wizardId]]);
    // 数一下到底创建了几个 payment（按 invoice_ids 反查）
    const paymentCount = await this.searchCount('account.payment',
      [['ref', 'like', '%']]);   // 这里粗略数最近的，不严格
    actions.push(`已对 ${values.invoice_ids.length} 张发票登记付款`);
    return { payment_count: values.invoice_ids.length, actions };
  }

  async getChartOfAccounts(options: {
    keyword?: string;
    account_type?: string;
    company_id?: number;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.keyword) {
      domain.push('|', ['code', 'ilike', options.keyword], ['name', 'ilike', options.keyword]);
    }
    if (options.account_type) domain.push(['account_type', '=', options.account_type]);
    if (options.company_id) domain.push(['company_ids', 'in', [options.company_id]]);
    const result = await this.searchRead('account.account', domain,
      ['id', 'code', 'name', 'account_type', 'currency_id', 'reconcile', 'company_ids'],
      { limit: options.limit ?? 100, order: 'code asc' });
    return result.records;
  }

  // ---------- 智能洞察 2 工具 ----------

  async detectAnomalies(): Promise<{
    detected_at: string;
    anomalies: Array<{
      type: string;
      severity: 'low' | 'medium' | 'high';
      count: number;
      description: string;
      sample_ids?: number[];
    }>;
  }> {
    const todayStr = today();
    const day30Ago = (() => {
      const d = new Date(); d.setDate(d.getDate() - 30);
      return d.toISOString().substring(0, 10);
    })();
    const day7Ago = (() => {
      const d = new Date(); d.setDate(d.getDate() - 7);
      return d.toISOString().substring(0, 10);
    })();

    const [
      negativeStock, largeOrders, oldUnpaid, pendingApprovals,
      staleLeads, draftPayslips,
    ] = await Promise.all([
      // 1) 库存负数
      this.searchRead('stock.quant',
        [['quantity', '<', 0]],
        ['id', 'product_id', 'location_id', 'quantity'],
        { limit: 20 }),
      // 2) 大额销售订单（最近 7 天 amount_total > 100k）
      this.searchRead('sale.order',
        [['date_order', '>=', `${day7Ago} 00:00:00`],
         ['amount_total', '>', 100000],
         '|', ['state', '=', 'sale'], ['state', '=', 'done']],
        ['id', 'name', 'partner_id', 'amount_total'],
        { limit: 20, order: 'amount_total desc' }),
      // 3) 老的未付发票（>= 90 天逾期）
      this.searchRead('account.move',
        [['move_type', '=', 'out_invoice'], ['state', '=', 'posted'],
         ['payment_state', 'in', ['not_paid', 'partial']],
         ['invoice_date_due', '<', day30Ago]],
        ['id', 'name', 'partner_id', 'amount_residual', 'invoice_date_due'],
        { limit: 20 }).catch(() => ({ records: [], length: 0 })),
      // 4) 堆积的待审批（pending 超过 7 天）
      this.searchRead('approval.request',
        [['request_status', '=', 'pending'],
         ['date', '<', `${day7Ago} 00:00:00`]],
        ['id', 'name', 'category_id', 'request_owner_id', 'date'],
        { limit: 20 }).catch(() => ({ records: [], length: 0 })),
      // 5) 长期停滞商机（30 天没动）
      this.searchCount('crm.lead',
        [['type', '=', 'opportunity'], ['active', '=', true],
         ['probability', '<', 100], ['probability', '>', 0],
         ['date_last_stage_update', '<', `${day30Ago} 00:00:00`]]).catch(() => 0),
      // 6) draft 状态的工资单（异常滞留）
      this.searchCount('hr.payslip',
        [['state', '=', 'draft'],
         ['create_date', '<', `${day7Ago} 00:00:00`]]).catch(() => 0),
    ]);

    const anomalies: Array<{
      type: string;
      severity: 'low' | 'medium' | 'high';
      count: number;
      description: string;
      sample_ids?: number[];
    }> = [];

    if (negativeStock.records.length > 0) {
      anomalies.push({
        type: 'negative_stock',
        severity: 'high',
        count: negativeStock.records.length,
        description: `${negativeStock.records.length} 条 stock.quant 数量为负，可能存在库存账实不符`,
        sample_ids: negativeStock.records.slice(0, 5).map(r => r['id'] as number),
      });
    }
    if (largeOrders.records.length > 0) {
      anomalies.push({
        type: 'large_orders',
        severity: 'medium',
        count: largeOrders.records.length,
        description: `近 7 天 ${largeOrders.records.length} 笔大额订单（>10w），需额外关注审核与执行`,
        sample_ids: largeOrders.records.slice(0, 5).map(r => r['id'] as number),
      });
    }
    if (oldUnpaid.records.length > 0) {
      anomalies.push({
        type: 'old_unpaid_invoices',
        severity: 'high',
        count: oldUnpaid.records.length,
        description: `${oldUnpaid.records.length} 张发票逾期 30+ 天未付，建议催款`,
        sample_ids: oldUnpaid.records.slice(0, 5).map(r => r['id'] as number),
      });
    }
    if (pendingApprovals.records.length > 0) {
      anomalies.push({
        type: 'stale_approvals',
        severity: 'medium',
        count: pendingApprovals.records.length,
        description: `${pendingApprovals.records.length} 条审批已 pending 超 7 天，可能阻塞业务`,
        sample_ids: pendingApprovals.records.slice(0, 5).map(r => r['id'] as number),
      });
    }
    if (staleLeads > 0) {
      anomalies.push({
        type: 'stale_crm_leads',
        severity: 'low',
        count: staleLeads,
        description: `${staleLeads} 个商机超 30 天未动，调 odoo_crm_stale_leads 查详情`,
      });
    }
    if (draftPayslips > 0) {
      anomalies.push({
        type: 'draft_payslips_stuck',
        severity: 'medium',
        count: draftPayslips,
        description: `${draftPayslips} 张工资单 draft 状态超 7 天，应验证或取消`,
      });
    }

    return {
      detected_at: todayStr,
      anomalies,
    };
  }

  async getKpiSummary(): Promise<{
    today: string;
    sales_mtd: number;                 // 本月销售额
    receivables_outstanding: number;   // 应收余额
    open_helpdesk_count: number;
    overdue_helpdesk_sla: number;
    open_mrp_count: number;
    stock_alert_count: number;
    pending_payslips: number;
  }> {
    const todayStr = today();
    const monthStart = todayStr.substring(0, 7) + '-01';
    const [
      salesAgg, recvAgg, openHelpdesk, overdueSla,
      openMrp, stockAlerts, pendingPayslips,
    ] = await Promise.all([
      this.readGroup('sale.order',
        [['date_order', '>=', `${monthStart} 00:00:00`],
         '|', ['state', '=', 'sale'], ['state', '=', 'done']],
        ['amount_total:sum'], [], { limit: 1 }),
      this.readGroup('account.move',
        [['move_type', '=', 'out_invoice'], ['state', '=', 'posted'],
         ['payment_state', 'in', ['not_paid', 'partial']]],
        ['amount_residual:sum'], [], { limit: 1 }),
      this.searchCount('helpdesk.ticket', [['close_date', '=', false]]).catch(() => 0),
      this.searchCount('helpdesk.ticket',
        [['close_date', '=', false],
         ['sla_deadline', '<', `${todayStr} 23:59:59`],
         ['sla_deadline', '!=', false]]).catch(() => 0),
      this.searchCount('mrp.production',
        [['state', 'in', ['confirmed', 'progress', 'to_close']]]).catch(() => 0),
      this.searchCount('stock.warehouse.orderpoint', [['qty_to_order', '>', 0]]).catch(() => 0),
      this.searchCount('hr.payslip', [['state', 'in', ['draft', 'verify']]]).catch(() => 0),
    ]);
    const salesAmount = Array.isArray(salesAgg) && salesAgg[0]
      ? Number((salesAgg[0] as Record<string, unknown>)['amount_total'] ?? 0) : 0;
    const recvAmount = Array.isArray(recvAgg) && recvAgg[0]
      ? Number((recvAgg[0] as Record<string, unknown>)['amount_residual'] ?? 0) : 0;
    return {
      today: todayStr,
      sales_mtd: salesAmount,
      receivables_outstanding: recvAmount,
      open_helpdesk_count: openHelpdesk,
      overdue_helpdesk_sla: overdueSla,
      open_mrp_count: openMrp,
      stock_alert_count: stockAlerts,
      pending_payslips: pendingPayslips,
    };
  }

  // ---------- 报表 / 数据导出 2 工具 ----------

  /** 构造 PDF 下载 URL（不直接拉 base64，避免 RPC payload 爆炸） */
  getPdfReportUrl(reportRef: string, recordIds: number[]): string {
    // 标准 Odoo URL 模式：/report/pdf/<report_ref>/<id1>,<id2>,...
    const idsStr = recordIds.join(',');
    return `${this.url}/report/pdf/${encodeURIComponent(reportRef)}/${idsStr}`;
  }

  async exportCsv(options: {
    model: string;
    fields: string[];
    domain?: Domain;
    limit?: number;
    order?: string;
  }): Promise<{
    model: string;
    fields: string[];
    row_count: number;
    csv: string;
  }> {
    const result = await this.searchRead(options.model,
      options.domain ?? [], options.fields,
      { limit: options.limit ?? 1000, order: options.order ?? '' });

    function csvEscape(v: unknown): string {
      if (v === null || v === undefined || v === false) return '';
      // Many2one returned as [id, "name"]
      if (Array.isArray(v) && v.length === 2) v = v[1];
      const s = String(v);
      if (/[",\n\r]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
      return s;
    }
    const header = options.fields.map(csvEscape).join(',');
    const rows = result.records.map(r =>
      options.fields.map(f => csvEscape(r[f])).join(','));
    const csv = [header, ...rows].join('\n');
    return {
      model: options.model,
      fields: options.fields,
      row_count: result.records.length,
      csv,
    };
  }

  // ==================== 自动化 + 数据治理 + 批量 + 集成（v1.17） ====================
  //
  // v1.17 转向"深度+自动化+集成"，不再追业务广度：
  //   - 流程自动化：base.automation / ir.cron 列表与创建
  //   - 数据治理：联系人/产品重复检测、字段完整性扫描、合并向导
  //   - 批量操作：邮件/归档/重新指派
  //   - 集成 / 治理：多语言翻译写入、自定义字段查询、用户与权限组管理

  // ---------- 自动化 3 ----------

  async getAutomations(options: { model_id?: number; only_active?: boolean; limit?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.only_active !== false) domain.push(['active', '=', true]);
    if (options.model_id) domain.push(['model_id', '=', options.model_id]);
    const result = await this.searchRead('base.automation', domain,
      ['id', 'name', 'model_id', 'model_name', 'trigger', 'active',
       'filter_domain', 'filter_pre_domain', 'trg_date_id'],
      { limit: options.limit ?? 50, order: 'model_name, name' });
    return result.records;
  }

  async getCronJobs(options: { only_active?: boolean; limit?: number } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.only_active !== false) domain.push(['active', '=', true]);
    const result = await this.searchRead('ir.cron', domain,
      ['id', 'cron_name', 'user_id', 'active',
       'interval_number', 'interval_type', 'nextcall', 'ir_actions_server_id'],
      { limit: options.limit ?? 100, order: 'nextcall asc' });
    return result.records;
  }

  async createAutomation(values: {
    name: string;
    model_id: number;                  // ir.model id
    trigger: 'on_create' | 'on_write' | 'on_create_or_write' | 'on_unlink' | 'on_change' | 'on_time' | 'on_time_created' | 'on_time_updated';
    server_action_ids?: number[];      // ir.actions.server ids
    filter_domain?: string;            // odoo domain string
    active?: boolean;
  }): Promise<number> {
    const payload: Record<string, unknown> = {
      name: values.name,
      model_id: values.model_id,
      trigger: values.trigger,
      active: values.active ?? true,
    };
    if (values.server_action_ids && values.server_action_ids.length > 0) {
      payload['action_server_ids'] = [[6, 0, values.server_action_ids]];
    }
    if (values.filter_domain) payload['filter_domain'] = values.filter_domain;
    return this.create('base.automation', payload);
  }

  // ---------- 数据治理 4 ----------

  async detectDuplicatePartners(options: {
    by?: 'email' | 'phone' | 'name';   // 默认 email
    limit?: number;
  } = {}): Promise<{
    detected_at: string;
    by: string;
    duplicate_groups: Array<{ key: string; partner_ids: number[]; count: number }>;
  }> {
    const by = options.by ?? 'email';
    const fieldMap: Record<string, string> = {
      email: 'email', phone: 'phone', name: 'name',
    };
    const groupField = fieldMap[by] ?? 'email';
    // 用 read_group 找出现 > 1 次的值
    const groups = await this.readGroup('res.partner',
      [[groupField, '!=', false]],
      [], [groupField], { limit: options.limit ?? 1000 });
    const dups = groups.filter((g: Record<string, unknown>) => {
      const cnt = Number(g[`${groupField}_count`] ?? g['__count'] ?? 0);
      return cnt > 1;
    });
    // 对每个 dup group 拉具体 partner_ids
    const groups_out: Array<{ key: string; partner_ids: number[]; count: number }> = [];
    for (const g of dups.slice(0, 50)) {
      const key = String((g as Record<string, unknown>)[groupField] ?? '');
      if (!key) continue;
      const cnt = Number((g as Record<string, unknown>)[`${groupField}_count`]
                        ?? (g as Record<string, unknown>)['__count'] ?? 0);
      const partners = await this.searchRead('res.partner',
        [[groupField, '=', key]],
        ['id'], { limit: 10 });
      groups_out.push({
        key,
        partner_ids: partners.records.map(r => r['id'] as number),
        count: cnt,
      });
    }
    return {
      detected_at: today(),
      by,
      duplicate_groups: groups_out,
    };
  }

  async detectDuplicateProducts(options: {
    by?: 'default_code' | 'barcode' | 'name';
    limit?: number;
  } = {}): Promise<{
    detected_at: string;
    by: string;
    duplicate_groups: Array<{ key: string; product_ids: number[]; count: number }>;
  }> {
    const by = options.by ?? 'default_code';
    const groupField = by;
    const groups = await this.readGroup('product.product',
      [[groupField, '!=', false]],
      [], [groupField], { limit: options.limit ?? 1000 });
    const dups = groups.filter((g: Record<string, unknown>) => {
      const cnt = Number(g[`${groupField}_count`] ?? g['__count'] ?? 0);
      return cnt > 1;
    });
    const groups_out: Array<{ key: string; product_ids: number[]; count: number }> = [];
    for (const g of dups.slice(0, 50)) {
      const key = String((g as Record<string, unknown>)[groupField] ?? '');
      if (!key) continue;
      const cnt = Number((g as Record<string, unknown>)[`${groupField}_count`]
                        ?? (g as Record<string, unknown>)['__count'] ?? 0);
      const products = await this.searchRead('product.product',
        [[groupField, '=', key]],
        ['id'], { limit: 10 });
      groups_out.push({
        key,
        product_ids: products.records.map(r => r['id'] as number),
        count: cnt,
      });
    }
    return {
      detected_at: today(),
      by,
      duplicate_groups: groups_out,
    };
  }

  async dataQualityCompleteness(): Promise<{
    detected_at: string;
    issues: Array<{
      model: string;
      field: string;
      missing_count: number;
      severity: 'low' | 'medium' | 'high';
      sample_ids: number[];
    }>;
  }> {
    // 6 类高频"应填未填"扫描
    const [
      empNoEmail, empNoPhone, empNoMgr, partnerNoEmail, partnerCustNoCountry, prodNoCode,
    ] = await Promise.all([
      this.searchRead('hr.employee',
        [['active', '=', true], ['work_email', '=', false]],
        ['id'], { limit: 10 }).catch(() => ({ records: [], length: 0 })),
      this.searchRead('hr.employee',
        [['active', '=', true], ['work_phone', '=', false], ['mobile_phone', '=', false]],
        ['id'], { limit: 10 }).catch(() => ({ records: [], length: 0 })),
      this.searchRead('hr.employee',
        [['active', '=', true], ['parent_id', '=', false]],
        ['id'], { limit: 10 }).catch(() => ({ records: [], length: 0 })),
      this.searchRead('res.partner',
        [['active', '=', true], ['email', '=', false], ['is_company', '=', true]],
        ['id'], { limit: 10 }),
      this.searchRead('res.partner',
        [['active', '=', true], ['country_id', '=', false], ['customer_rank', '>', 0]],
        ['id'], { limit: 10 }).catch(() => ({ records: [], length: 0 })),
      this.searchRead('product.product',
        [['active', '=', true], ['default_code', '=', false]],
        ['id'], { limit: 10 }).catch(() => ({ records: [], length: 0 })),
    ]);

    const issues: Array<{
      model: string;
      field: string;
      missing_count: number;
      severity: 'low' | 'medium' | 'high';
      sample_ids: number[];
    }> = [];

    function addIssue(model: string, field: string, records: { records: OdooRecord[]; length?: number }, severity: 'low' | 'medium' | 'high') {
      if (records.records.length === 0) return;
      issues.push({
        model, field,
        missing_count: records.records.length,
        severity,
        sample_ids: records.records.slice(0, 5).map(r => r['id'] as number),
      });
    }
    addIssue('hr.employee', 'work_email', empNoEmail, 'medium');
    addIssue('hr.employee', 'work_phone+mobile_phone', empNoPhone, 'low');
    addIssue('hr.employee', 'parent_id', empNoMgr, 'low');
    addIssue('res.partner', 'email (公司)', partnerNoEmail, 'medium');
    addIssue('res.partner', 'country_id (客户)', partnerCustNoCountry, 'low');
    addIssue('product.product', 'default_code', prodNoCode, 'medium');

    return { detected_at: today(), issues };
  }

  async mergePartners(values: {
    partner_ids: number[];               // 2-3 个 partner id
    dst_partner_id?: number;             // 主记录，不填默认 partner_ids[0]
  }): Promise<{ kept_partner_id: number; merged_partner_ids: number[]; actions: string[] }> {
    const actions: string[] = [];
    if (values.partner_ids.length < 2) {
      throw new Error('合并至少需要 2 个 partner');
    }
    if (values.partner_ids.length > 3) {
      throw new Error('Odoo 安全限制：单次最多合并 3 个 partner');
    }
    const dstId = values.dst_partner_id ?? values.partner_ids[0]!;
    // 创建合并向导记录然后调 _merge
    // base.partner.merge.automatic.wizard._merge 是私有方法但可 RPC 调
    // 创建向导
    const wizardId = await this.create('base.partner.merge.automatic.wizard', {});
    actions.push(`创建合并向导 #${wizardId}`);
    // 调 _merge
    await this.call('base.partner.merge.automatic.wizard', '_merge', [
      [wizardId], values.partner_ids, dstId,
    ]);
    actions.push(`已合并到 partner #${dstId}（保留），归并 ${values.partner_ids.filter(i => i !== dstId).join(', ')}`);
    return {
      kept_partner_id: dstId,
      merged_partner_ids: values.partner_ids.filter(i => i !== dstId),
      actions,
    };
  }

  // ---------- 批量操作 3 ----------

  async batchEmail(values: {
    model: string;
    domain: Domain;
    template_id: number;                 // mail.template id
    limit?: number;
  }): Promise<{ sent_count: number; record_ids: number[]; actions: string[] }> {
    const actions: string[] = [];
    const records = await this.searchRead(values.model, values.domain, ['id'],
      { limit: values.limit ?? 100 });
    const ids = records.records.map(r => r['id'] as number);
    if (ids.length === 0) {
      return { sent_count: 0, record_ids: [], actions: ['没有匹配的记录'] };
    }
    actions.push(`匹配 ${ids.length} 条记录`);
    // 用 mail.template.send_mail 逐条发
    let sent = 0;
    for (const id of ids) {
      try {
        await this.call('mail.template', 'send_mail', [[values.template_id], id], {
          force_send: false,            // 进队列，不阻塞
        });
        sent++;
      } catch { /* 个别失败不阻塞 */ }
    }
    actions.push(`成功入队 ${sent} 封`);
    return { sent_count: sent, record_ids: ids, actions };
  }

  async batchArchive(values: {
    model: string;
    record_ids: number[];
    activate?: boolean;                  // false=archive, true=unarchive
  }): Promise<{ count: number; model: string; activate: boolean }> {
    const newActive = values.activate ?? false;
    await this.write(values.model, values.record_ids, { active: newActive });
    return { count: values.record_ids.length, model: values.model, activate: newActive };
  }

  async batchAssign(values: {
    model: string;
    record_ids: number[];
    user_id: number;                     // 新经办人 res.users id
    field?: string;                      // 默认 user_id；项目任务用 user_ids
  }): Promise<{ count: number; model: string; field: string; user_id: number }> {
    const field = values.field ?? 'user_id';
    const writeVals: Record<string, unknown> = {};
    if (field === 'user_ids') {
      writeVals[field] = [[6, 0, [values.user_id]]];   // M2m replace
    } else {
      writeVals[field] = values.user_id;
    }
    await this.write(values.model, values.record_ids, writeVals);
    return { count: values.record_ids.length, model: values.model, field, user_id: values.user_id };
  }

  // ---------- 集成 / 治理 4 ----------

  async translateRecord(values: {
    model: string;
    record_id: number;
    field: string;
    translations: Record<string, string>;   // { 'zh_CN': '中文', 'en_US': 'English' }
  }): Promise<{ model: string; record_id: number; field: string; updated_languages: string[] }> {
    // Odoo 19 多语言写入：用 update_field_translations
    // 等价：调 model.update_field_translations(field, {lang: value, ...})
    await this.call(values.model, 'update_field_translations', [
      [values.record_id], values.field, values.translations,
    ]);
    return {
      model: values.model,
      record_id: values.record_id,
      field: values.field,
      updated_languages: Object.keys(values.translations),
    };
  }

  async getCustomFields(options: {
    model?: string;                      // 不填看全部 x_* 字段
    keyword?: string;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    // ir.model.fields where state='manual' 表示自定义字段
    const domain: Domain = [['state', '=', 'manual']];
    if (options.model) {
      // 通过 ir.model.model = options.model 联表
      domain.push(['model', '=', options.model]);
    }
    if (options.keyword) {
      domain.push('|', ['name', 'ilike', options.keyword], ['field_description', 'ilike', options.keyword]);
    }
    const result = await this.searchRead('ir.model.fields', domain,
      ['id', 'name', 'model', 'field_description', 'ttype', 'required',
       'relation', 'help'],
      { limit: options.limit ?? 100, order: 'model, name' });
    return result.records;
  }

  async createUser(values: {
    name: string;
    login: string;                       // 通常是 email
    email?: string;
    employee_id?: number;                // 关联到 hr.employee
    group_ids?: number[];                // 直接指定权限组 res.groups ids
    password?: string;                   // 不填则需走"邀请邮件"流程
    company_id?: number;
  }): Promise<{ user_id: number; partner_id: number; actions: string[] }> {
    const actions: string[] = [];
    const payload: Record<string, unknown> = {
      name: values.name,
      login: values.login,
      email: values.email ?? values.login,
    };
    if (values.password) payload['password'] = values.password;
    if (values.company_id) payload['company_id'] = values.company_id;
    if (values.group_ids && values.group_ids.length > 0) {
      payload['groups_id'] = [[6, 0, values.group_ids]];
    }
    const userId = await this.create('res.users', payload);
    actions.push(`创建系统用户 #${userId}`);

    // 关联 employee
    if (values.employee_id) {
      try {
        await this.write('hr.employee', [values.employee_id], { user_id: userId });
        actions.push(`已关联到员工 #${values.employee_id}`);
      } catch (e) {
        actions.push(`员工关联失败：${String(e)}`);
      }
    }

    const userRecord = (await this.read('res.users', [userId], ['partner_id']))[0];
    const partnerArr = userRecord?.['partner_id'];
    const partnerId = Array.isArray(partnerArr) ? partnerArr[0] as number : 0;

    return { user_id: userId, partner_id: partnerId, actions };
  }

  async getUserGroups(userId?: number): Promise<{
    user_id: number;
    user_name: string;
    groups: Array<{ id: number; name: string; category: unknown }>;
  }> {
    const uid = userId ?? this.uid ?? 0;
    const me = (await this.read('res.users', [uid],
      ['id', 'name', 'groups_id']))[0];
    if (!me) {
      return { user_id: uid, user_name: '', groups: [] };
    }
    const groupIds = Array.isArray(me['groups_id']) ? me['groups_id'] as number[] : [];
    if (groupIds.length === 0) {
      return { user_id: uid, user_name: String(me['name'] ?? ''), groups: [] };
    }
    const groups = await this.read('res.groups', groupIds,
      ['id', 'name', 'category_id', 'full_name']);
    return {
      user_id: uid,
      user_name: String(me['name'] ?? ''),
      groups: groups.map(g => ({
        id: g['id'] as number,
        name: String(g['full_name'] ?? g['name'] ?? ''),
        category: g['category_id'],
      })),
    };
  }

  // ==================== Studio 元编程 + 审计 + 多公司 + 报表 + 集成（v1.18） ====================
  //
  // v1.18 五个主题：
  //   - Studio 元编程：ir.model / ir.model.fields 创建与查询
  //   - 审计与变更追踪：mail.tracking.value / res.users.log / 字段历史
  //   - 多公司联动：切公司 + 跨公司聚合
  //   - 报表深化：通用 pivot 数据
  //   - 外部集成：webhook / portal 分享 / 邮件日志

  // ---------- Studio 元编程 4 ----------

  async getModels(options: {
    keyword?: string;                    // 模型名 / 描述模糊搜
    only_custom?: boolean;               // 只看自定义（state='manual'）
    transient?: boolean;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.keyword) {
      domain.push('|', ['model', 'ilike', options.keyword], ['name', 'ilike', options.keyword]);
    }
    if (options.only_custom) domain.push(['state', '=', 'manual']);
    if (options.transient !== undefined) domain.push(['transient', '=', options.transient]);
    const result = await this.searchRead('ir.model', domain,
      ['id', 'name', 'model', 'state', 'info', 'transient', 'abstract', 'order'],
      { limit: options.limit ?? 100, order: 'model asc' });
    return result.records;
  }

  async getModelFields(model: string, options: {
    keyword?: string;
    only_custom?: boolean;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [['model', '=', model]];
    if (options.keyword) {
      domain.push('|', ['name', 'ilike', options.keyword], ['field_description', 'ilike', options.keyword]);
    }
    if (options.only_custom) domain.push(['state', '=', 'manual']);
    const result = await this.searchRead('ir.model.fields', domain,
      ['id', 'name', 'field_description', 'ttype', 'required', 'readonly',
       'relation', 'selection', 'state', 'translate', 'help'],
      { limit: options.limit ?? 200, order: 'name asc' });
    return result.records;
  }

  async createModel(values: {
    name: string;                        // 显示名
    model: string;                       // 技术名，必须 x_ 开头
    transient?: boolean;
    abstract?: boolean;
  }): Promise<number> {
    if (!values.model.startsWith('x_')) {
      throw new Error('自定义模型 model 必须以 x_ 开头（Odoo 强制约束）');
    }
    return this.create('ir.model', {
      name: values.name,
      model: values.model,
      state: 'manual',
      transient: values.transient ?? false,
      abstract: values.abstract ?? false,
    });
  }

  async createModelField(values: {
    model: string;                       // 目标 model 技术名
    name: string;                        // 字段名，必须 x_ 开头
    field_description: string;
    ttype: 'char' | 'text' | 'integer' | 'float' | 'monetary' | 'boolean' | 'date'
         | 'datetime' | 'binary' | 'selection' | 'many2one' | 'one2many' | 'many2many' | 'html';
    required?: boolean;
    relation?: string;                   // many2one / one2many / many2many 必填
    selection?: Array<[string, string]>; // selection 必填，[[key, label], ...]
    help?: string;
    translate?: boolean;
  }): Promise<number> {
    if (!values.name.startsWith('x_')) {
      throw new Error('自定义字段 name 必须以 x_ 开头（Odoo 强制约束）');
    }
    // model 字段需要 model_id（通过 model 技术名查 ir.model.id）
    const modelRec = await this.searchRead('ir.model',
      [['model', '=', values.model]], ['id'], { limit: 1 });
    if (modelRec.records.length === 0) {
      throw new Error(`模型 ${values.model} 不存在`);
    }
    const modelId = modelRec.records[0]?.['id'] as number;
    const payload: Record<string, unknown> = {
      model: values.model,
      model_id: modelId,
      name: values.name,
      field_description: values.field_description,
      ttype: values.ttype,
      state: 'manual',
      required: values.required ?? false,
    };
    if (values.relation) payload['relation'] = values.relation;
    if (values.selection) {
      payload['selection'] = JSON.stringify(values.selection);
    }
    if (values.help) payload['help'] = values.help;
    if (values.translate) payload['translate'] = values.translate;
    return this.create('ir.model.fields', payload);
  }

  // ---------- 审计与变更追踪 3 ----------

  async getAuditLog(options: {
    model: string;
    record_id: number;
    limit?: number;
  }): Promise<{
    model: string;
    record_id: number;
    changes: Array<{
      date: unknown;
      author: unknown;
      field: unknown;
      old_value: unknown;
      new_value: unknown;
    }>;
  }> {
    // 拉这条记录的 mail.message 列表，再取每条 message 的 tracking_value_ids
    const messages = await this.searchRead('mail.message',
      [['model', '=', options.model], ['res_id', '=', options.record_id]],
      ['id', 'date', 'author_id', 'tracking_value_ids', 'subject', 'body'],
      { limit: options.limit ?? 100, order: 'date desc' });
    const allTrackingIds = messages.records.flatMap(m =>
      Array.isArray(m['tracking_value_ids']) ? m['tracking_value_ids'] as number[] : []);
    const trackingsById = new Map<number, OdooRecord>();
    if (allTrackingIds.length > 0) {
      const trackings = await this.read('mail.tracking.value', allTrackingIds,
        ['id', 'field_id', 'old_value_char', 'new_value_char',
         'mail_message_id']);
      for (const t of trackings) {
        trackingsById.set(t['id'] as number, t);
      }
    }
    const changes: Array<{
      date: unknown; author: unknown; field: unknown;
      old_value: unknown; new_value: unknown;
    }> = [];
    for (const m of messages.records) {
      const trackingIds = Array.isArray(m['tracking_value_ids']) ? m['tracking_value_ids'] as number[] : [];
      for (const tid of trackingIds) {
        const t = trackingsById.get(tid);
        if (!t) continue;
        changes.push({
          date: m['date'],
          author: m['author_id'],
          field: t['field_id'],
          old_value: t['old_value_char'],
          new_value: t['new_value_char'],
        });
      }
    }
    return { model: options.model, record_id: options.record_id, changes };
  }

  async getLoginHistory(options: {
    user_id?: number;                    // 不填默认当前
    days?: number;                       // 默认 30
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const days = options.days ?? 30;
    const dateFrom = (() => {
      const d = new Date(); d.setDate(d.getDate() - days);
      return d.toISOString().substring(0, 19).replace('T', ' ');
    })();
    const userId = options.user_id ?? this.uid ?? 0;
    const result = await this.searchRead('res.users.log',
      [['user_id', '=', userId], ['create_date', '>=', dateFrom]],
      ['id', 'user_id', 'create_date'],
      { limit: options.limit ?? 100, order: 'create_date desc' });
    return result.records;
  }

  async getFieldHistory(options: {
    model: string;
    record_id: number;
    field_name: string;
    limit?: number;
  }): Promise<{
    model: string;
    record_id: number;
    field_name: string;
    history: Array<{ date: unknown; author: unknown; from: unknown; to: unknown }>;
  }> {
    // 找该字段对应的 ir.model.fields.id
    const fieldRec = await this.searchRead('ir.model.fields',
      [['model', '=', options.model], ['name', '=', options.field_name]],
      ['id'], { limit: 1 });
    if (fieldRec.records.length === 0) {
      throw new Error(`字段 ${options.model}.${options.field_name} 不存在`);
    }
    const fieldId = fieldRec.records[0]?.['id'] as number;
    // mail.tracking.value 没有 res_model + res_id 字段（追踪挂在 mail.message 上）
    // 必须先找 mail.message，再过滤 tracking
    const messages = await this.searchRead('mail.message',
      [['model', '=', options.model], ['res_id', '=', options.record_id],
       ['tracking_value_ids', '!=', false]],
      ['id', 'date', 'author_id', 'tracking_value_ids'],
      { limit: 200, order: 'date desc' });
    const allTrackingIds = messages.records.flatMap(m =>
      Array.isArray(m['tracking_value_ids']) ? m['tracking_value_ids'] as number[] : []);
    if (allTrackingIds.length === 0) {
      return { model: options.model, record_id: options.record_id,
               field_name: options.field_name, history: [] };
    }
    const trackings = await this.searchRead('mail.tracking.value',
      [['id', 'in', allTrackingIds], ['field_id', '=', fieldId]],
      ['id', 'old_value_char', 'new_value_char', 'mail_message_id'],
      { limit: options.limit ?? 50 });
    // 把 tracking 关联回 message 时间
    const msgById = new Map<number, OdooRecord>();
    for (const m of messages.records) msgById.set(m['id'] as number, m);
    const history = trackings.records.map(t => {
      const msgArr = t['mail_message_id'];
      const msgId = Array.isArray(msgArr) ? msgArr[0] as number : 0;
      const msg = msgById.get(msgId);
      return {
        date: msg?.['date'],
        author: msg?.['author_id'],
        from: t['old_value_char'],
        to: t['new_value_char'],
      };
    }).sort((a, b) => String(b.date).localeCompare(String(a.date)));
    return {
      model: options.model, record_id: options.record_id,
      field_name: options.field_name, history,
    };
  }

  // ---------- 多公司联动 2 ----------

  async switchCompany(companyId: number): Promise<{
    user_id: number;
    new_company_id: number;
    new_company_name: string;
    actions: string[];
  }> {
    const actions: string[] = [];
    const uid = this.uid ?? 0;
    // 检查 user 是否在该 company 的 allowed list
    const me = (await this.read('res.users', [uid], ['company_ids']))[0];
    const allowed = Array.isArray(me?.['company_ids']) ? me['company_ids'] as number[] : [];
    if (!allowed.includes(companyId)) {
      throw new Error(`user #${uid} 没有切到公司 #${companyId} 的权限`);
    }
    // 写 res.users.company_id
    await this.write('res.users', [uid], { company_id: companyId });
    actions.push(`已切换 res.users.company_id → #${companyId}`);
    // 读公司名
    const company = (await this.read('res.company', [companyId], ['name']))[0];
    return {
      user_id: uid,
      new_company_id: companyId,
      new_company_name: String(company?.['name'] ?? ''),
      actions,
    };
  }

  async getConsolidatedDashboard(options: {
    company_ids?: number[];              // 不填用 user 的 company_ids
    date_from?: string;
    date_to?: string;
  } = {}): Promise<{
    period: { from: string; to: string };
    by_company: Array<{
      company: unknown;
      sales: number;
      receivables: number;
      open_helpdesk: number;
      headcount: number;
    }>;
    grand_total: {
      sales: number;
      receivables: number;
      open_helpdesk: number;
      headcount: number;
    };
  }> {
    const todayStr = today();
    const dFrom = options.date_from ?? todayStr.substring(0, 7) + '-01';
    const dTo = options.date_to ?? todayStr;
    let companyIds = options.company_ids;
    if (!companyIds || companyIds.length === 0) {
      const me = (await this.read('res.users', [this.uid ?? 0], ['company_ids']))[0];
      companyIds = Array.isArray(me?.['company_ids']) ? me['company_ids'] as number[] : [];
    }
    if (companyIds.length === 0) {
      return {
        period: { from: dFrom, to: dTo },
        by_company: [],
        grand_total: { sales: 0, receivables: 0, open_helpdesk: 0, headcount: 0 },
      };
    }
    const companies = await this.read('res.company', companyIds, ['id', 'name']);
    const byCompany = await Promise.all(companies.map(async c => {
      const cid = c['id'] as number;
      const [salesAgg, recvAgg, helpdeskCnt, hcCnt] = await Promise.all([
        this.readGroup('sale.order',
          [['company_id', '=', cid],
           ['date_order', '>=', `${dFrom} 00:00:00`],
           '|', ['state', '=', 'sale'], ['state', '=', 'done']],
          ['amount_total:sum'], [], { limit: 1 }),
        this.readGroup('account.move',
          [['company_id', '=', cid],
           ['move_type', '=', 'out_invoice'], ['state', '=', 'posted'],
           ['payment_state', 'in', ['not_paid', 'partial']]],
          ['amount_residual:sum'], [], { limit: 1 }),
        this.searchCount('helpdesk.ticket',
          [['company_id', '=', cid], ['close_date', '=', false]]).catch(() => 0),
        this.searchCount('hr.employee',
          [['company_id', '=', cid], ['active', '=', true]]),
      ]);
      const sales = Array.isArray(salesAgg) && salesAgg[0]
        ? Number((salesAgg[0] as Record<string, unknown>)['amount_total'] ?? 0) : 0;
      const recv = Array.isArray(recvAgg) && recvAgg[0]
        ? Number((recvAgg[0] as Record<string, unknown>)['amount_residual'] ?? 0) : 0;
      return { company: [cid, c['name']], sales, receivables: recv,
               open_helpdesk: helpdeskCnt, headcount: hcCnt };
    }));
    const grand = byCompany.reduce((acc, r) => ({
      sales: acc.sales + r.sales,
      receivables: acc.receivables + r.receivables,
      open_helpdesk: acc.open_helpdesk + r.open_helpdesk,
      headcount: acc.headcount + r.headcount,
    }), { sales: 0, receivables: 0, open_helpdesk: 0, headcount: 0 });
    return { period: { from: dFrom, to: dTo }, by_company: byCompany, grand_total: grand };
  }

  // ---------- 报表深化 2 ----------

  async getPivotData(options: {
    model: string;
    measures: string[];                  // 如 ['amount_total:sum', 'qty:sum']
    groupby: string[];                   // 1-2 维分组
    domain?: Domain;
    limit?: number;
    orderby?: string;
  }): Promise<{
    model: string;
    measures: string[];
    groupby: string[];
    rows: Record<string, unknown>[];
    total: Record<string, number>;
  }> {
    const groups = await this.readGroup(
      options.model, options.domain ?? [],
      options.measures, options.groupby,
      { limit: options.limit ?? 200, orderby: options.orderby });
    // 算总计
    const total: Record<string, number> = {};
    for (const m of options.measures) {
      const fname = m.split(':')[0]!;
      total[fname] = groups.reduce((s: number, g: Record<string, unknown>) =>
        s + Number(g[fname] ?? 0), 0);
    }
    return {
      model: options.model,
      measures: options.measures,
      groupby: options.groupby,
      rows: groups,
      total,
    };
  }

  async getEmailLog(options: {
    state?: 'outgoing' | 'sent' | 'received' | 'exception' | 'cancel';
    days?: number;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const days = options.days ?? 7;
    const dateFrom = (() => {
      const d = new Date(); d.setDate(d.getDate() - days);
      return d.toISOString().substring(0, 19).replace('T', ' ');
    })();
    const domain: Domain = [['create_date', '>=', dateFrom]];
    if (options.state) domain.push(['state', '=', options.state]);
    const result = await this.searchRead('mail.mail', domain,
      ['id', 'subject', 'email_from', 'email_to', 'state', 'create_date',
       'date', 'failure_type', 'failure_reason'],
      { limit: options.limit ?? 50, order: 'create_date desc' });
    return result.records;
  }

  // ---------- 外部集成 3 ----------

  async createWebhookAction(values: {
    name: string;
    model_id: number;                    // ir.model id
    webhook_url: string;
    webhook_field_ids?: number[];        // ir.model.fields ids
    automation: {                        // 自动包装一个 base.automation 触发
      trigger: 'on_create' | 'on_write' | 'on_create_or_write';
      filter_domain?: string;
    };
  }): Promise<{ server_action_id: number; automation_id: number; actions: string[] }> {
    const actions: string[] = [];
    // 第 1 步：创建 ir.actions.server with state='webhook'
    const serverActionPayload: Record<string, unknown> = {
      name: values.name,
      model_id: values.model_id,
      state: 'webhook',
      webhook_url: values.webhook_url,
    };
    if (values.webhook_field_ids && values.webhook_field_ids.length > 0) {
      serverActionPayload['webhook_field_ids'] = [[6, 0, values.webhook_field_ids]];
    }
    const serverActionId = await this.create('ir.actions.server', serverActionPayload);
    actions.push(`创建 webhook server action #${serverActionId}`);

    // 第 2 步：创建 base.automation 触发 server action
    const automationPayload: Record<string, unknown> = {
      name: `${values.name}（webhook 触发器）`,
      model_id: values.model_id,
      trigger: values.automation.trigger,
      action_server_ids: [[6, 0, [serverActionId]]],
      active: true,
    };
    if (values.automation.filter_domain) {
      automationPayload['filter_domain'] = values.automation.filter_domain;
    }
    const automationId = await this.create('base.automation', automationPayload);
    actions.push(`创建 automation #${automationId} 关联到 server action`);
    return { server_action_id: serverActionId, automation_id: automationId, actions };
  }

  async getRecordShareUrl(options: {
    model: string;
    record_id: number;
  }): Promise<{
    model: string;
    record_id: number;
    portal_url: string | null;
    backend_url: string;
  }> {
    // 优先尝试 record.get_portal_url（mail.thread.portal_mixin 的方法）
    let portalUrl: string | null = null;
    try {
      const result = await this.call(options.model, 'get_portal_url', [[options.record_id]]) as string | string[];
      portalUrl = typeof result === 'string' ? result
                  : Array.isArray(result) ? String(result[0] ?? '') : null;
      if (portalUrl && !portalUrl.startsWith('http')) {
        portalUrl = `${this.url}${portalUrl}`;
      }
    } catch {
      // 不支持 portal mixin 就 null
    }
    const backendUrl = `${this.url}/odoo/action-base.action_open_view?model=${encodeURIComponent(options.model)}&id=${options.record_id}`;
    return {
      model: options.model,
      record_id: options.record_id,
      portal_url: portalUrl,
      backend_url: backendUrl,
    };
  }

  async getMailQueue(): Promise<{
    pending_outgoing: number;
    failed: number;
    sent_today: number;
    samples_outgoing: OdooRecord[];
    samples_failed: OdooRecord[];
  }> {
    const todayStr = today();
    const [pending, failed, sentToday, samplesOut, samplesFailed] = await Promise.all([
      this.searchCount('mail.mail', [['state', '=', 'outgoing']]),
      this.searchCount('mail.mail', [['state', '=', 'exception']]),
      this.searchCount('mail.mail',
        [['state', '=', 'sent'], ['date', '>=', `${todayStr} 00:00:00`]]),
      this.searchRead('mail.mail', [['state', '=', 'outgoing']],
        ['id', 'subject', 'email_to', 'create_date'],
        { limit: 5, order: 'create_date desc' }),
      this.searchRead('mail.mail', [['state', '=', 'exception']],
        ['id', 'subject', 'email_to', 'failure_reason', 'create_date'],
        { limit: 5, order: 'create_date desc' }),
    ]);
    return {
      pending_outgoing: pending,
      failed,
      sent_today: sentToday,
      samples_outgoing: samplesOut.records,
      samples_failed: samplesFailed.records,
    };
  }

  // ==================== 审批发起 + 克隆 + 关注 + 资源 + 报表订阅（v1.20） ====================
  //
  // v1.20 六个主题：
  //   - 审批工作流深化：列分类 + 发起 + 提交 + 我待审
  //   - 数据克隆：浅复制 / 深复制 / CSV 导入
  //   - Mail 关注：列关注者 / 订阅 / 取消订阅
  //   - 资源 / 工作时间表：resource.resource + resource.calendar
  //   - 报表订阅：cron 定期发 PDF
  //   - 多语言：读现有翻译

  // ---------- 审批工作流深化 4 ----------

  async getApprovalCategories(options: {
    keyword?: string;
    only_active?: boolean;
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.only_active !== false) domain.push(['active', '=', true]);
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    const result = await this.searchRead('approval.category', domain,
      ['id', 'name', 'approval_minimum', 'approval_type',
       'company_id', 'automated_sequence'],
      { limit: options.limit ?? 50, order: 'name asc' });
    return result.records;
  }

  async createApprovalRequest(values: {
    category_id: number;
    name?: string;                     // 不填用 category 默认
    reason?: string;
    date_start?: string;               // YYYY-MM-DD HH:MM:SS
    date_end?: string;
    quantity?: number;
    amount?: number;
    location?: string;
    partner_id?: number;
    auto_confirm?: boolean;            // 创建后立即 action_confirm 提交
  }): Promise<{ request_id: number; confirmed: boolean; actions: string[] }> {
    const actions: string[] = [];
    const payload: Record<string, unknown> = {
      category_id: values.category_id,
    };
    for (const k of ['name','reason','date_start','date_end','quantity','amount','location','partner_id'] as const) {
      const v = values[k];
      if (v !== undefined) payload[k] = v;
    }
    const reqId = await this.create('approval.request', payload);
    actions.push(`创建审批请求 #${reqId}`);

    let confirmed = false;
    if (values.auto_confirm) {
      try {
        await this.call('approval.request', 'action_confirm', [[reqId]]);
        confirmed = true;
        actions.push('已提交（new → pending）');
      } catch (e) {
        actions.push(`自动提交失败：${String(e)}`);
      }
    }
    return { request_id: reqId, confirmed, actions };
  }

  async confirmApprovalRequest(ids: number[]): Promise<unknown> {
    return this.call('approval.request', 'action_confirm', [ids]);
  }

  async getMyPendingApprovals(options: { limit?: number } = {}): Promise<OdooRecord[]> {
    const uid = this.uid ?? 0;
    // 我作为 approver 且 request 是 pending
    const result = await this.searchRead('approval.request',
      [['request_status', '=', 'pending'],
       ['approver_ids.user_id', '=', uid]],
      ['id', 'name', 'category_id', 'request_owner_id', 'request_status',
       'date', 'amount', 'reason'],
      { limit: options.limit ?? 30, order: 'date asc' });
    return result.records;
  }

  // ---------- 数据克隆 / 导入 3 ----------

  async cloneRecord(values: {
    model: string;
    record_id: number;
    overrides?: Record<string, unknown>;   // copy(default=...) 的 default 参数
  }): Promise<{ original_id: number; clone_id: number; model: string }> {
    // BaseModel.copy(default) 是 Odoo 内置，所有 model 都有
    const result = await this.call(values.model, 'copy',
      [[values.record_id]],
      values.overrides ? { default: values.overrides } : {});
    // copy 返回 ids 数组（v18+）或单个 id（更老版本兼容）
    const cloneId = Array.isArray(result) ? Number(result[0]) : Number(result);
    return {
      original_id: values.record_id,
      clone_id: cloneId,
      model: values.model,
    };
  }

  async cloneRecordWithLines(values: {
    model: string;
    record_id: number;
    line_field: string;                    // 如 sale.order 用 order_line, mrp.bom 用 bom_line_ids
    line_model: string;                    // 子表 model，如 sale.order.line
    line_fields: string[];                 // 要复制的子表字段
    overrides?: Record<string, unknown>;
  }): Promise<{
    original_id: number;
    clone_id: number;
    model: string;
    lines_copied: number;
  }> {
    // 第 1 步：先拿源记录的 line ids
    const original = (await this.read(values.model, [values.record_id], [values.line_field]))[0];
    const lineIds = Array.isArray(original?.[values.line_field])
      ? original[values.line_field] as number[] : [];

    // 第 2 步：copy 主记录（不含子，因为我们要重写）
    const overrides = { ...(values.overrides ?? {}), [values.line_field]: [[5]] };  // [5] = clear all
    const cloneResult = await this.call(values.model, 'copy',
      [[values.record_id]], { default: overrides });
    const cloneId = Array.isArray(cloneResult) ? Number(cloneResult[0]) : Number(cloneResult);

    // 第 3 步：读所有原子表 + 重写到新主记录
    if (lineIds.length === 0) {
      return { original_id: values.record_id, clone_id: cloneId, model: values.model, lines_copied: 0 };
    }
    const lines = await this.read(values.line_model, lineIds, values.line_fields);
    // 找到子表里指向主表的 M2o 字段（约定 = model 的最后一段，去 _line / _ids 后缀）
    // 简单做法：让调用方传 parent_field，但兜底从 line 的字段反推
    // 这里采用约定：忽略 m2o 反向，让 [0,0,vals] 自动挂到新主记录
    // 但 [0,0,vals] 必须写到 model 的 line_field 字段上
    // 所以：write 主记录，line_field = [[0, 0, lineVals], ...]
    const lineCommands = lines.map(l => {
      // 去掉 id 字段，拿剩下的纯值
      const vals: Record<string, unknown> = {};
      for (const f of values.line_fields) {
        if (f === 'id') continue;
        let v = l[f];
        // M2o 类字段返回 [id, name]，写入要拍扁成 id
        if (Array.isArray(v) && v.length === 2 && typeof v[0] === 'number') {
          v = v[0];
        }
        vals[f] = v;
      }
      return [0, 0, vals];
    });
    await this.write(values.model, [cloneId], { [values.line_field]: lineCommands });

    return {
      original_id: values.record_id,
      clone_id: cloneId,
      model: values.model,
      lines_copied: lines.length,
    };
  }

  async importCsv(values: {
    model: string;
    headers: string[];                     // 字段技术名
    rows: string[][];                      // 每行字符串
  }): Promise<{
    model: string;
    imported_ids: number[];
    failed_rows: Array<{ row_index: number; error: string }>;
  }> {
    const imported_ids: number[] = [];
    const failed_rows: Array<{ row_index: number; error: string }> = [];
    // 一行一行 create（不使用 Odoo 内置 load() 因为它要求 base64 编码 + CSV 模板）
    for (let i = 0; i < values.rows.length; i++) {
      const row = values.rows[i]!;
      const vals: Record<string, unknown> = {};
      values.headers.forEach((h, idx) => {
        const v = row[idx];
        if (v === undefined || v === '') return;
        // 尝试自动数字转换（M2o id / Integer / Float）
        if (/^\d+$/.test(v)) vals[h] = Number(v);
        else if (/^\d+\.\d+$/.test(v)) vals[h] = Number(v);
        else if (v.toLowerCase() === 'true') vals[h] = true;
        else if (v.toLowerCase() === 'false') vals[h] = false;
        else vals[h] = v;
      });
      try {
        const id = await this.create(values.model, vals);
        imported_ids.push(id);
      } catch (e) {
        failed_rows.push({ row_index: i, error: String(e) });
      }
    }
    return { model: values.model, imported_ids, failed_rows };
  }

  // ---------- Mail 关注（3） ----------

  async getFollowers(options: {
    model: string;
    record_id: number;
    limit?: number;
  }): Promise<OdooRecord[]> {
    const result = await this.searchRead('mail.followers',
      [['res_model', '=', options.model], ['res_id', '=', options.record_id]],
      ['id', 'partner_id', 'res_model', 'res_id', 'subtype_ids'],
      { limit: options.limit ?? 100 });
    return result.records;
  }

  async subscribeRecord(values: {
    model: string;
    record_id: number;
    partner_ids?: number[];                // 不填默认订阅当前用户的 partner
  }): Promise<{ model: string; record_id: number; partner_ids: number[] }> {
    let partnerIds = values.partner_ids;
    if (!partnerIds || partnerIds.length === 0) {
      const me = (await this.read('res.users', [this.uid ?? 0], ['partner_id']))[0];
      const partnerArr = me?.['partner_id'];
      const myPartner = Array.isArray(partnerArr) ? partnerArr[0] as number : null;
      partnerIds = myPartner ? [myPartner] : [];
    }
    if (partnerIds.length === 0) {
      throw new Error('未指定 partner_ids，且当前用户没有 partner_id');
    }
    await this.call(values.model, 'message_subscribe',
      [[values.record_id]], { partner_ids: partnerIds });
    return { model: values.model, record_id: values.record_id, partner_ids: partnerIds };
  }

  async unsubscribeRecord(values: {
    model: string;
    record_id: number;
    partner_ids?: number[];                // 不填默认 = 取消我自己的订阅
  }): Promise<{ model: string; record_id: number; partner_ids: number[] }> {
    let partnerIds = values.partner_ids;
    if (!partnerIds || partnerIds.length === 0) {
      const me = (await this.read('res.users', [this.uid ?? 0], ['partner_id']))[0];
      const partnerArr = me?.['partner_id'];
      const myPartner = Array.isArray(partnerArr) ? partnerArr[0] as number : null;
      partnerIds = myPartner ? [myPartner] : [];
    }
    await this.call(values.model, 'message_unsubscribe',
      [[values.record_id]], { partner_ids: partnerIds });
    return { model: values.model, record_id: values.record_id, partner_ids: partnerIds };
  }

  // ---------- 资源 / 工作时间表 2 ----------

  async getResources(options: {
    keyword?: string;
    resource_type?: 'user' | 'material';
    limit?: number;
  } = {}): Promise<OdooRecord[]> {
    const domain: Domain = [];
    if (options.keyword) domain.push(['name', 'ilike', options.keyword]);
    if (options.resource_type) domain.push(['resource_type', '=', options.resource_type]);
    const result = await this.searchRead('resource.resource', domain,
      ['id', 'name', 'resource_type', 'user_id', 'company_id',
       'calendar_id', 'tz', 'time_efficiency'],
      { limit: options.limit ?? 50, order: 'name asc' });
    return result.records;
  }

  async getResourceCalendar(calendarId: number): Promise<{
    calendar: OdooRecord | null;
    attendances: OdooRecord[];
  }> {
    const calendars = await this.read('resource.calendar', [calendarId],
      ['id', 'name', 'tz', 'two_weeks_calendar', 'attendance_ids', 'company_id']);
    const calendar = calendars[0] ?? null;
    if (!calendar) return { calendar: null, attendances: [] };
    const attendanceIds = Array.isArray(calendar['attendance_ids'])
      ? calendar['attendance_ids'] as number[] : [];
    const attendances = attendanceIds.length > 0
      ? await this.read('resource.calendar.attendance', attendanceIds,
          ['id', 'name', 'dayofweek', 'hour_from', 'hour_to', 'day_period',
           'date_from', 'date_to'])
      : [];
    return { calendar, attendances };
  }

  // ---------- 报表订阅 1 ----------

  async scheduleReportEmail(values: {
    name: string;                          // cron 名
    report_ref: string;                    // ir.actions.report xml id
    record_domain?: string;                // 用 Python eval 的 domain，如 [('state','=','sale')]
    model: string;                         // 报表对应的 model
    interval_number: number;               // 间隔数
    interval_type: 'minutes' | 'hours' | 'days' | 'weeks' | 'months';
    next_call?: string;                    // YYYY-MM-DD HH:MM:SS
    user_id?: number;                      // scheduler 身份
  }): Promise<{ cron_id: number; server_action_id: number; actions: string[] }> {
    const actions: string[] = [];
    // 第 1 步：创建 ir.actions.server 用于真正执行
    // state='code'：写一段 Python 调 _render_qweb_pdf + 发邮件
    const code = `
# 自动生成：定期渲染并发送 ${values.report_ref} 报表
domain = ${values.record_domain ?? '[]'}
records = env['${values.model}'].search(domain)
if records:
    report = env.ref('${values.report_ref}')
    pdf_content, _ = report._render_qweb_pdf(report, records.ids)
    # 简化：写入主 user 收件箱（更复杂的可改为发邮件）
    env['mail.message'].create({
        'subject': '定期报表：${values.name}',
        'body': '${values.name} 报表已就绪（共 %d 条记录）' % len(records),
        'message_type': 'notification',
        'model': 'res.users',
        'res_id': env.uid,
    })
`.trim();

    // 找一个 model_id（必须给 server action）
    const modelRec = await this.searchRead('ir.model',
      [['model', '=', values.model]], ['id'], { limit: 1 });
    if (modelRec.records.length === 0) throw new Error(`model ${values.model} 不存在`);
    const modelId = modelRec.records[0]?.['id'] as number;

    const serverActionId = await this.create('ir.actions.server', {
      name: `定期报表：${values.name}`,
      model_id: modelId,
      state: 'code',
      code,
    });
    actions.push(`创建 server action #${serverActionId}（state=code）`);

    // 第 2 步：创建 ir.cron 调用这个 server action
    const cronPayload: Record<string, unknown> = {
      cron_name: `report-${values.name}`,
      ir_actions_server_id: serverActionId,
      interval_number: values.interval_number,
      interval_type: values.interval_type,
      active: true,
    };
    if (values.next_call) cronPayload['nextcall'] = values.next_call;
    if (values.user_id) cronPayload['user_id'] = values.user_id;
    const cronId = await this.create('ir.cron', cronPayload);
    actions.push(`创建 cron #${cronId}（每 ${values.interval_number} ${values.interval_type}）`);

    return { cron_id: cronId, server_action_id: serverActionId, actions };
  }

  // ---------- 多语言 1 ----------

  async getRecordTranslations(values: {
    model: string;
    record_id: number;
    field: string;
  }): Promise<{
    model: string;
    record_id: number;
    field: string;
    translations: Record<string, string>;  // { 'zh_CN': '...', 'en_US': '...' }
  }> {
    // Odoo 19 用 model.get_field_translations(field) 返 [{lang, value, source}, ...]
    try {
      const result = await this.call(values.model, 'get_field_translations',
        [[values.record_id], values.field]) as unknown[];
      // result[0] 是 list of {lang, value, source}, result[1] 是 dict 元数据
      const list = Array.isArray(result) && Array.isArray(result[0])
        ? result[0] as Array<Record<string, unknown>> : [];
      const translations: Record<string, string> = {};
      for (const r of list) {
        const lang = r['lang'];
        const value = r['value'];
        if (typeof lang === 'string') translations[lang] = String(value ?? '');
      }
      return { model: values.model, record_id: values.record_id, field: values.field, translations };
    } catch {
      // 老版本退化：直接读 ir.translation
      const trans = await this.searchRead('ir.translation',
        [['name', '=', `${values.model},${values.field}`],
         ['res_id', '=', values.record_id]],
        ['lang', 'value'], { limit: 50 });
      const translations: Record<string, string> = {};
      for (const t of trans.records) {
        translations[String(t['lang'])] = String(t['value'] ?? '');
      }
      return { model: values.model, record_id: values.record_id, field: values.field, translations };
    }
  }

  // ==================== 实施经理每日概况 ====================

  async getDailyBriefing(): Promise<{
    todayTasks: OdooRecord[];
    overdueActivities: OdooRecord[];
    openTickets: OdooRecord[];
    overdueInvoices: OdooRecord[];
    crmFollowUps: OdooRecord[];
    unreadMessages: OdooRecord[];
  }> {
    const uid = this.uid ?? 0;
    const [todayTasks, overdueActivities, openTickets, overdueInvoices, crmFollowUps, unreadMessages] = await Promise.all([
      // 今日截止任务
      this.searchRead('project.task',
        [['user_ids', 'in', [uid]], ['active', '=', true], ['date_deadline', '<=', today()]],
        ['id', 'name', 'project_id', 'date_deadline', 'priority', 'stage_id'], { limit: 20 }),
      // 逾期活动
      this.searchRead('mail.activity',
        [['user_id', '=', uid], ['date_deadline', '<=', today()]],
        ['id', 'summary', 'date_deadline', 'activity_type_id', 'res_model', 'res_id', 'state'], { limit: 20 }),
      // 我的待处理工单
      this.searchRead('helpdesk.ticket',
        [['user_id', '=', uid], ['active', '=', true]],
        ['id', 'name', 'ticket_ref', 'priority', 'stage_id', 'sla_deadline', 'sla_fail'], { limit: 10 }).catch(() => ({ records: [] })),
      // 逾期应收发票
      this.getOverdueInvoices().then(r => ({ records: r })).catch(() => ({ records: [] })),
      // 需要跟进的商机（today activities）
      this.searchRead('crm.lead',
        [['user_id', '=', uid], ['active', '=', true], ['activity_date_deadline', '<=', today()]],
        ['id', 'name', 'partner_id', 'stage_id', 'probability', 'expected_revenue', 'activity_summary'], { limit: 10 }).catch(() => ({ records: [] })),
      // 未读消息
      this.searchRead('mail.message',
        [['message_type', '!=', 'notification'], ['to_read', '=', true]],
        ['id', 'subject', 'author_id', 'date', 'model', 'res_id'], { limit: 10 }),
    ]);

    return {
      todayTasks: todayTasks.records,
      overdueActivities: overdueActivities.records,
      openTickets: openTickets.records,
      overdueInvoices: overdueInvoices.records,
      crmFollowUps: crmFollowUps.records,
      unreadMessages: unreadMessages.records,
    };
  }

  // ==================== 私有传输层 ====================

  private async rpc(endpoint: string, params: Record<string, unknown>): Promise<unknown> {
    const url = `${this.url}${endpoint}`;
    const payload = { jsonrpc: '2.0', method: 'call', id: Date.now(), params };
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (this.session_id) headers['Cookie'] = `session_id=${this.session_id}`;

    // v1.21.0: 加 AbortSignal.timeout(3000) 防 odoo 后端慢导致 fetch 永久挂
    // → 上游 OpenClaw before_prompt_build hook 卡 15s 被 gateway 强行掐断 →
    // 用户实测首字延迟 P50=16.4s/P95=54.9s 的根因（gateway.err.log 唯一报
    // timeout 的就是 odoo before_prompt_build handler）。3s 快速失败让上游
    // hook 拿到错误就 fallback 到"未连接"提示，不再死等。
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(RPC_TIMEOUT_MS),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);

    const data = await response.json() as { result?: unknown; error?: OdooError };
    if (data.error) return { error: data.error };
    return data.result;
  }
}
