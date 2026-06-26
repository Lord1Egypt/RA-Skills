/**
 * 财税获客销售漏斗 5 阶段定义。
 * sales_followup_plan 工具按阶段输出未来 14 天动作清单。
 */

export type StageId = 'cold' | 'introduced' | 'proposal' | 'negotiation' | 'won_or_lost';

export interface Stage {
  id: StageId;
  display: string;
  /** 该阶段销售的核心目标。 */
  goals: string[];
  /** 标准跟进动作。每条 = { day_offset, action, channel }。 */
  actions: Array<{
    day_offset: number;
    action: string;
    channel: 'phone' | 'wechat' | 'email' | 'visit' | 'wecom';
  }>;
  /** 客户在此阶段的常见异议。 */
  common_objections: string[];
  /** 推进到下一阶段的判定信号。 */
  promote_signals: string[];
  /** 默认 mail.activity 类型（喂给 huihuoyun-odoo 的 odoo_create_activity）。 */
  default_activity_type: 'todo' | 'call' | 'meeting' | 'email';
}

export const STAGES: Record<StageId, Stage> = {
  cold: {
    id: 'cold',
    display: '陌拜 / 初次触达',
    goals: ['打通联系通道', '换到决策人微信/直拨电话', '判断有无近期需求窗口'],
    actions: [
      { day_offset: 0, action: '首次电话/微信 —— 用行业 hook 开场，30 秒内说清来意', channel: 'phone' },
      { day_offset: 2, action: '发送 1 篇行业相关短文（汇算清缴提醒 / 高新认定 / 稽查案例）', channel: 'wechat' },
      { day_offset: 5, action: '电话二次触达 —— 问"上次的内容有没有看，咱这边大致情况是？"', channel: 'phone' },
      { day_offset: 9, action: '邀约 30 分钟面谈 / 视频会，主题"财税体检"', channel: 'wechat' },
    ],
    common_objections: ['我们已经有代账了', '现在不忙', '老板说不需要'],
    promote_signals: ['同意约面谈', '主动问报价', '让转给老板/CFO'],
    default_activity_type: 'call',
  },
  introduced: {
    id: 'introduced',
    display: '初谈 / 需求挖掘',
    goals: ['挖出 2-3 个具体痛点', '确认决策链路与时间表', '获取近 1 年财务数据样本'],
    actions: [
      { day_offset: 0, action: '面谈 —— 用 SPIN 提问拉出痛点', channel: 'visit' },
      { day_offset: 1, action: '当天发感谢信 + 会议纪要（含 3 个待确认问题）', channel: 'email' },
      { day_offset: 4, action: '电话确认问题答案 —— 客户已答即推进，未答即温柔催', channel: 'phone' },
      { day_offset: 7, action: '初步方向方案（PPT 5 页） —— 不报价，只展示思路', channel: 'email' },
      { day_offset: 11, action: '电话讨论方向，约第二次正式提案会', channel: 'phone' },
    ],
    common_objections: ['再考虑一下', '老板还在比价', '内部还在讨论'],
    promote_signals: ['提供财务数据', '约第二次会议', '发起对比"你们和某某有什么不同"'],
    default_activity_type: 'meeting',
  },
  proposal: {
    id: 'proposal',
    display: '方案 / 报价',
    goals: ['给出量身定制方案 + 报价区间', '锁定决策时间线', '识别并应对真实异议'],
    actions: [
      { day_offset: 0, action: '正式提案会 —— 方案 + 报价区间 + 案例 3 个', channel: 'visit' },
      { day_offset: 1, action: '当天发完整方案 PDF + 报价书', channel: 'email' },
      { day_offset: 3, action: '电话确认收到，问"哪几个点需要更细的解释"', channel: 'phone' },
      { day_offset: 7, action: '主动给一个限时小让步（比如赠 1 季合规体检），制造决策动机', channel: 'wechat' },
      { day_offset: 12, action: '正式约签约面谈或寄合同', channel: 'phone' },
    ],
    common_objections: ['价格偏高', '需要走采购流程', '能不能再优惠'],
    promote_signals: ['老板亲自见面', '要求出合同稿', '确定签约时间'],
    default_activity_type: 'meeting',
  },
  negotiation: {
    id: 'negotiation',
    display: '议价 / 合同',
    goals: ['锁定最终价格与服务边界', '签约', '完成首笔预付款'],
    actions: [
      { day_offset: 0, action: '商务谈判 —— 守住底价但用"延展服务"换价格', channel: 'visit' },
      { day_offset: 1, action: '修订合同稿（针对客户异议条款）', channel: 'email' },
      { day_offset: 3, action: '电话敲定细节 —— 价格、付款节奏、服务起算日', channel: 'phone' },
      { day_offset: 6, action: '寄/送合同正本 + 用印', channel: 'visit' },
      { day_offset: 10, action: '催首笔预付款 —— 用"服务起算日"作为 anchor', channel: 'phone' },
    ],
    common_objections: ['付款节奏要分多期', '服务范围要再加一项', '要先试用一个月'],
    promote_signals: ['合同盖章', '确认起算日', '财务对接预付款'],
    default_activity_type: 'todo',
  },
  won_or_lost: {
    id: 'won_or_lost',
    display: '成交 / 失败 复盘',
    goals: [
      '成交：交接给服务团队 + 触达客户老板做满意度承诺',
      '失败：复盘失分点 + 进入"半年回访池"',
    ],
    actions: [
      { day_offset: 0, action: '成交：服务交付 kickoff 会；失败：复盘 1 页纸', channel: 'visit' },
      { day_offset: 2, action: '成交：发欢迎邮件 + 服务时间表；失败：发"保持联系"短信', channel: 'email' },
      { day_offset: 7, action: '成交：第一次月度对账；失败：纳入 90 天回访池', channel: 'wechat' },
    ],
    common_objections: [],
    promote_signals: [],
    default_activity_type: 'todo',
  },
};

export function listStages(): Stage[] {
  return ['cold', 'introduced', 'proposal', 'negotiation', 'won_or_lost'].map((id) => STAGES[id as StageId]);
}
