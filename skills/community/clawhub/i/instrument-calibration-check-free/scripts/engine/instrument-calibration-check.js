#!/usr/bin/env node
/**
 * instrument-calibration-check.js —— 计量器具检定校准到期核对（确定性、纯 Node 标准库）。
 *
 * 真实痛点：强制检定/校准的计量器具（卡尺、千分尺、天平、压力表、温度计、电子秤、流量计…）
 * 都有**检定/校准周期**，到期未检定仍在用是**体系审核与监管的直接不合格项**，而且会让产品数据不可信。
 * 计量管理员/质量部每月必须核：台账与证书是否齐、下次到期日是否在覆盖期内、
 * 停用/报废器具是否仍在用、校准结果是否满足最大允许误差。
 *
 * 材料形态（一段文本、用小标题分段）：主表「计量器具台账」为必需；
 * `#证书明细#` 段按需提供（用于台账与证书一致性核对）；其余分段标记属于完整档口径，本包不使用。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，**不发起任何网络请求**
 * （没有 fetch / http / https / net / dns / tls），不读环境变量（没有 process.env），不写盘。
 * ⚠️ 本文件是 **免费档子集**：只实现下面这六项免费检查；**完整档（付费）的实现不在这个包里**，
 *    `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 *    本版本只核对主表「计量器具台账」段，`#证书明细#` 段用于台账与证书一致性核对。
 *
 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不判定检定/校准结果本身是否合格、不判定器具是否属于强制检定目录、
 *          不读 .xlsx/.pdf 原件、不联网核验证书与机构资质真伪；材料不足**一律不给结论**。
 *
 * ⚠️ 本文件是**从买断版引擎摘出的免费子集**：完整档的实现不在这个文件里，
 *    改这份文件时请同步改买断版引擎，再重新摘一次，否则两个包会分叉。
 */
'use strict';

/* ============================ 契约常量 ============================ */

const CHECKS_GIVEN = [
  '到期覆盖核对（核对基准日 ≤ 下次检定日期；超期即报，给出原文与超期天数）',
  '台账与证书一致性（证书编号/检定日期/有效期在台账与证书两边对不上即报，并给两处原文）',
  '校准周期勾稽（上次检定日期 + 校准周期(月) = 下次检定日期，逐行复算）',
  '同一器具编号重复登记（同一器具编号在台账里出现两次以上）',
  '合计行/统计行逐列复核（合计行的数量类列须等于明细行逐列累加）',
  '空白/占位符/日期格式/状态值非法（器具编号/名称/型号规格/准确度等级/上次检定日期/校准周期/下次检定日期/证书编号/使用部门/状态，日期格式与状态值须合法）',
];

const CHECKS_WITHHELD = [
  '最大允许误差（MPE）超差（实测误差绝对值 > 允许误差 ⇒ 报出超差量与超差倍数）',
  '停用/报废器具仍在使用记录里出现（跨表交叉核对）',
  '检定机构资质与证书有效期覆盖（机构授权有效期须晚于该器具的检定日期）',
  '期间核查/日常点检记录断档（按日期序列逐日比对，间隔超过核查周期即报）',
  '分部门×分器具类别的汇总清单（按超期天数排序，给出可整改动作）',
];

const OUT_OF_SCOPE = [
  '判定检定/校准结果本身是否合格、是否判废、能否继续使用 —— 那是检定机构与计量确认的职责，本工具只核台账、证书与记录之间的算术与日期覆盖',
  '判定某台器具是否属于强制检定目录、适用哪个检定规程 —— 那是计量行政管理的认定权，本工具不做',
  '读取 .xlsx / .pdf 原件、联网核验证书编号与机构资质真伪、替代计量确认记录或体系审核结论',
  '判定期间核查的方法是否科学（只核记录日期序列是否断档，不判断核查数据本身）',
];

/** 段标记：`#名称#` 单独成行；主表（计量器具台账）写了也不影响，不写就是默认段 */
const SECTION_MARKS = {
  ledger: '#计量器具台账#',
  certificate: '#证书明细#',
  agency: '#机构资质#',
  usage: '#使用记录#',
  spot: '#期间核查#',
};

// 可参与合计行逐列复核的「数量类列」——合计行能对上的就是这几列，
// 靠**角色**判定，不能靠表头里有没有「合计」两个字（那等于什么列都认不出来）。
const QTY_ROLES = ['qty', 'cycleMonths', 'overdueDays', 'amount'];
const SUM_ROLES = QTY_ROLES;

// 正则统一用 new RegExp 拼出来，避免源码里出现看不出是正则的字面量。
const RE_TABLE_SEP = new RegExp('\\t');
const RE_PLACEHOLDER = /^(n\/?a|无|不适用|待填|待补|待定|待核|未知|不详)$/i;
const RE_DASH = /^[-—–]+$/;
const RE_ALLOWED_STATUS = /^(在用|使用中|正常|未使用|闲置|停用|禁用|封存|报废|已报废|送检中|检定中|校准中|待检定|待校准|已停用|已报废|维修中)$/;
const RE_TOTAL_ROW = /合计|小计|总计|统计|汇总|共\s*\d/;

const REQUIRED_ROLES = ['itemNo', 'itemName', 'spec', 'accuracy', 'lastDate', 'cycleMonths', 'nextDate', 'certNumber', 'dept', 'status'];

const REQUIRED_FIELDS = [
  ['itemNo', '器具编号'],
  ['itemName', '器具名称'],
  ['spec', '型号规格'],
  ['accuracy', '准确度等级'],
  ['lastDate', '上次检定日期'],
  ['cycleMonths', '校准周期(月)'],
  ['nextDate', '下次检定日期'],
  ['certNumber', '证书编号'],
  ['dept', '使用部门'],
  ['status', '状态'],
];

const AMOUNT_ROLES = [['amount', '检定费用']];

// ⚠️ 表头 → 角色：靠关键词**顺序**匹配，更具体的必须排在更宽泛的前面。
//    顺序一错，宽泛词会抢走更具体的列（本仓库踩过六次，见 tools/header_map_check.py）。
//    第二条铁律：别名不能是另一列别名的**超串**（'检定日期' 是 '下次检定日期' 的子串），
//    否则 indexOf 先命中的是短词，列会被整段抢走。
const ROLE_KEYS = [
  ['itemNo', ['器具编号', '计量编号', '设备编号', '仪器编号', '台账编号', '资产编号', '编号']],
  ['certNumber', ['证书编号', '检定证书编号', '校准证书编号', '证书号', '证书']],
  ['itemName', ['器具名称', '计量器具名称', '仪器名称', '设备名称', '名称']],
  ['spec', ['型号规格', '规格型号', '型号', '规格']],
  ['accuracy', ['准确度等级', '精度等级', '准确度', '精度', '等级']],
  ['lastDate', ['上次检定日期', '上次校准日期', '上次检定', '上次校准', '检定日期', '校准日期']],
  ['spotCycleDays', ['核查周期(天)', '点检周期(天)', '核查周期（天）', '点检周期（天）', '核查周期', '点检周期', '核查频次']],
  ['cycleMonths', ['校准周期(月)', '校准周期（月）', '检定周期(月)', '检定周期（月）', '校准周期', '检定周期', '周期(月)', '周期']],
  ['nextDate', ['下次检定日期', '下次校准日期', '下次检定', '下次校准', '下次到期日', '计划检定日期']],
  ['dept', ['使用部门', '使用单位', '所属部门', '责任部门', '部门', '科室']],
  ['status', ['器具状态', '使用状态', '状态']],
  ['note', ['备注', '说明', '附注']],
  ['mpe', ['最大允许误差', '允许误差限', '允许误差', '允差', '允许偏差', '最大允许偏差', '误差限']],
  ['measuredError', ['实测误差值', '测量误差', '示值误差', '实测偏差', '误差值', '实测误差', '偏差']],
  ['agency', ['检定机构名称', '校准机构名称', '检定机构', '校准机构', '检定单位', '校准单位', '服务机构']],
  ['agencyValidTo', ['机构授权有效期至', '机构授权有效期', '授权有效期至', '资质有效期至', '授权有效期', '资质有效期', '授权截止日期']],
  ['spotDates', ['期间核查记录', '日常点检记录', '点检记录', '核查记录', '点检日期序列', '核查日期序列']],
  ['qty', ['数量(台)', '数量（台）', '台数', '数量', '件数']],
  ['overdueDays', ['超期天数', '逾期天数', '超期日数']],
  ['amount', ['检定费用', '校准费用', '费用金额', '金额']],
  ['validTo', ['证书有效期至', '证书有效期', '证书有效期止', '有效期至', '有效期', '有效期止']],
  ['auditDate', ['核查日期', '点检日期', '核查时间', '点检时间']],
  ['auditResult', ['核查结果', '点检结果', '核查结论', '点检结论', '结果']],
  ['auditNote', ['核查备注', '点检备注']],
  ['usageDate', ['使用日期', '领用日期', '借用日期', '使用时间']],
  ['usageItem', ['使用人', '领用人', '操作人', '使用人员']],
  ['usagePurpose', ['用途', '使用用途', '使用事项']],
  ['wareName', ['器具类别', '器具分类', '仪器类别', '设备类别', '类别']],
];

const LABELS = {
  itemNo: '器具编号',
  itemName: '器具名称',
  spec: '型号规格',
  accuracy: '准确度等级',
  lastDate: '上次检定日期',
  cycleMonths: '校准周期(月)',
  nextDate: '下次检定日期',
  certNumber: '证书编号',
  dept: '使用部门',
  status: '状态',
  wareName: '器具类别',
  qty: '数量(台)',
  mpe: '最大允许误差',
  measuredError: '实测误差',
  amount: '检定费用',
  agency: '检定机构',
  agencyValidTo: '机构授权有效期至',
  spotDates: '期间核查记录',
  spotCycleDays: '核查周期(天)',
  certValidTo: '证书有效期至',
  note: '备注',
  auditDate: '核查日期',
  auditResult: '核查结果',
  auditNote: '核查备注',
  usageDate: '使用日期',
  usageItem: '使用人',
  usagePurpose: '用途',
  overdueDays: '超期天数',
  validTo: '有效期至',
};

/** 每段表允许被识别成「自身列」的角色（防止把别段的列名误认成自己的列而静默串味） */
const SECTION_OWN_ROLES = {
  ledger: ['itemNo', 'itemName', 'spec', 'accuracy', 'lastDate', 'cycleMonths', 'nextDate', 'certNumber', 'certValidTo', 'validTo', 'dept', 'status', 'wareName', 'qty', 'mpe', 'measuredError', 'amount', 'agency', 'agencyValidTo', 'spotDates', 'spotCycleDays', 'certValidTo', 'note', 'overdueDays'],
  certificate: ['itemNo', 'itemName', 'certNumber', 'auditDate', 'validTo', 'agency', 'note'],
  agency: ['agency', 'agencyValidTo', 'note'],
  usage: ['itemNo', 'itemName', 'usageDate', 'usageItem', 'usagePurpose', 'note', 'status'],
  spot: ['itemNo', 'itemName', 'auditDate', 'auditResult', 'auditNote'],
};

/** 段内角色别名：证书明细表里的「检定日期」是**该证书的出证日期**，
 *  不能被台账的「上次检定日期」角色抢走（roleOf 是按关键词顺序匹配的，'检定日期' 会先命中 lastDate）。
 *  别名一律写成**已知角色名**，这样代码里不出现表头中文串，改名时只改一处。 */
const SECTION_ROLE_ALIAS = {
  certificate: { lastDate: 'auditDate' },
};

const SECTION_TITLES = {
  ledger: '计量器具台账',
  certificate: '证书明细表',
  agency: '检定机构资质表',
  usage: '器具使用记录表',
  spot: '期间核查/日常点检记录表',
};

// 列的完整声明顺序（汇总/校验都按它走）——
// 同样守「更具体的在前」：'有效期' 与 '有效期至' 不能排到 '机构授权有效期' 前面。
const COLUMN_ROLE_ORDER = [
  'itemNo', 'itemName', 'spec', 'accuracy', 'lastDate', 'cycleMonths', 'nextDate', 'certNumber',
  'dept', 'status', 'wareName', 'qty', 'mpe', 'measuredError', 'amount', 'agency',
  'agencyValidTo', 'spotDates', 'spotCycleDays', 'certValidTo', 'note',
  'auditDate', 'auditResult', 'auditNote', 'usageDate', 'usageItem', 'usagePurpose',
  'overdueDays', 'validTo',
];

// 样例：一张**干净**的计量器具台账 + 证书明细 + 机构资质 + 使用记录 + 期间核查记录。
// 核对基准日 2026-07-01：六台器具全部在有效期内、台账与证书一致、周期复算相等、
// 没有停用/报废器具出现在使用记录里、机构授权覆盖检定日期、期间核查无断档。
const SAMPLE_TEXT = [
  '器具编号\t器具名称\t型号规格\t准确度等级\t上次检定日期\t校准周期(月)\t下次检定日期\t证书编号\t证书有效期至\t使用部门\t状态\t最大允许误差\t实测误差\t检定机构\t机构授权有效期至\t期间核查记录\t核查周期(天)\t检定费用',
  'YX-2025-001\t数显卡尺\t0-150mm\t0.02mm\t2026-06-10\t12\t2027-06-10\tZJ-2026-CAL-00123\t2027-06-10\t机加工车间\t在用\t±0.02\t0.008\t省计量科学研究院\t2027-12-31\t2026-06-10;2026-06-10;2026-09-10;2026-12-10;2027-03-10;2027-06-10\t95\t120.00',
  'YX-2025-002\t外径千分尺\t0-25mm\t0.01mm\t2026-04-20\t12\t2027-04-20\tZJ-2026-CAL-00231\t2027-04-20\t机加工车间\t报废\t±0.01\t0.003\t省计量科学研究院\t2027-12-31\t2026-04-20\t95\t150.00',
  'YX-2025-003\t电子天平\t200g/0.1mg\tⅠ级\t2026-05-10\t12\t2027-05-10\tZJ-2026-CAL-00344\t2027-05-10\t理化检验室\t在用\t±0.5\t0.12\t省计量科学研究院\t2027-12-31\t2026-05-10\t95\t300.00',
  'YX-2025-004\t精密压力表\t0-1.6MPa\t0.4级\t2026-03-10\t12\t2027-03-10\tZJ-2026-CAL-00412\t2027-03-10\t理化检验室\t在用\t±0.4\t0.15\t市计量检定所\t2028-06-30\t2026-03-10;2026-06-10\t95\t200.00',
  'YX-2025-005\t双金属温度计\t0-200℃\t1.5级\t2026-06-01\t12\t2027-06-01\tZJ-2026-CAL-00518\t2027-06-01\t生产保障部\t在用\t±1.5\t0.6\t市计量检定所\t2028-06-30\t2026-06-01\t95\t80.00',
  'YX-2025-006\t电子台秤\t0-150kg\tⅢ级\t2025-08-15\t24\t2027-08-15\tZJ-2025-CAL-00607\t2027-08-15\t仓储物流部\t停用\t±50\t12\t市计量检定所\t2028-06-30\t2025-08-15;2025-11-18;2026-02-21;2026-05-27\t95\t180.00',
  '合计\t6 台计量器具\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t1030.00',
  '',
  '#证书明细#',
  '器具编号\t器具名称\t证书编号\t检定日期\t有效期至\t检定机构\t备注',
  'YX-2025-001\t数显卡尺\tZJ-2026-CAL-00123\t2026-06-10\t2027-06-10\t省计量科学研究院\t定期检定',
  'YX-2025-002\t外径千分尺\tZJ-2026-CAL-00231\t2026-04-20\t2027-04-20\t省计量科学研究院\t已判废',
  'YX-2025-003\t电子天平\tZJ-2026-CAL-00344\t2026-05-10\t2027-05-10\t省计量科学研究院\t',
  'YX-2025-004\t精密压力表\tZJ-2026-CAL-00412\t2026-03-10\t2027-03-10\t市计量检定所\t',
  'YX-2025-005\t双金属温度计\tZJ-2026-CAL-00518\t2026-06-01\t2027-06-01\t市计量检定所\t',
  'YX-2025-006\t电子台秤\tZJ-2025-CAL-00607\t2025-08-15\t2027-08-15\t市计量检定所\t停用待报废',
  '',
  '#机构资质#',
  '检定机构\t机构授权有效期至\t备注',
  '省计量科学研究院\t2027-12-31\t法定计量检定机构授权证书',
  '市计量检定所\t2028-06-30\t法定计量检定机构授权证书',
  '',
  '#使用记录#',
  '器具编号\t器具名称\t使用日期\t使用人\t用途\t备注',
  'YX-2025-001\t数显卡尺\t2026-06-19\t张伟\t零件首检\t',
  'YX-2025-003\t电子天平\t2026-06-25\t李娜\t样品称量\t',
  'YX-2025-004\t精密压力表\t2026-06-28\t王强\t管路压力巡检\t',
  'YX-2025-005\t双金属温度计\t2026-06-30\t赵敏\t烘箱温度监控\t',
  '',
  '#期间核查#',
  '器具编号\t器具名称\t核查日期\t核查结果\t核查备注',
  'YX-2025-001\t数显卡尺\t2026-06-10\t合格\t',
  'YX-2025-001\t数显卡尺\t2026-09-10\t合格\t',
  'YX-2025-001\t数显卡尺\t2026-12-10\t合格\t',
  'YX-2025-001\t数显卡尺\t2027-03-10\t合格\t',
  'YX-2025-003\t电子天平\t2026-05-10\t合格\t',
  'YX-2025-004\t精密压力表\t2026-03-10\t合格\t',
  'YX-2025-004\t精密压力表\t2026-06-10\t合格\t',
  'YX-2025-005\t双金属温度计\t2026-06-01\t合格\t',
  'YX-2025-006\t电子台秤\t2025-08-15\t合格\t停用前最后一次核查',
  'YX-2025-006\t电子台秤\t2025-11-18\t合格\t',
  'YX-2025-006\t电子台秤\t2026-02-21\t合格\t',
  'YX-2025-006\t电子台秤\t2026-05-27\t合格\t',
].filter((s) => s !== '').join('\n');

const TOL = 0.01;

// 停用/报废类状态（这些器具继续出现在「使用记录」里就是体系审核的直接不合格项）
const PROHIBITED_STATUS = ['停用', '已停用', '禁用', '报废', '已报废', '封存'];

// 允许的状态值集合（不在里面就是非法状态值）
const ALLOWED_STATUS = ['在用', '使用中', '正常', '未使用', '闲置', '停用', '已停用', '禁用', '封存', '报废', '已报废', '送检中', '检定中', '校准中', '待检定', '待校准', '维修中'];

// 器具类别的关键词（顺序 = 具体 → 宽泛，'卡尺' 必须排在 '尺' 前面）
const CATEGORY_KEYS = [
  ['卡尺', ['游标卡尺', '数显卡尺', '深度卡尺', '卡尺']],
  ['千分尺', ['千分尺', '测微计']],
  ['天平', ['电子天平', '分析天平', '天平']],
  ['压力表', ['压力表', '压力计', '压力变送器']],
  ['温度计', ['温度计', '热电偶', '铂电阻', '温湿度计']],
  ['电子秤', ['电子台秤', '电子秤', '台秤', '地磅', '衡器']],
  ['流量计', ['流量计', '流量表']],
  ['分光光度计', ['分光光度计', '光谱仪']],
  ['酸度计', ['酸度计', 'pH计', 'ph计']],
  ['湿度计', ['湿度计']],
  ['量筒', ['量筒', '量杯', '容量瓶']],
  ['秒表', ['秒表', '计时器']],
  ['万用表', ['万用表', '数字多用表']],
  ['标准器', ['标准器', '标准块', '量块', '标准物质']],
  ['色差计', ['色差计', '色度计']],
  ['砝码', ['砝码']],
  ['冰箱', ['超低温冰箱', '冷藏箱', '冰箱']],
  ['培养箱', ['培养箱', '干燥箱', '烘箱']],
];

/* ============================ 工具函数 ============================ */

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把这张表补全再跑：从 Excel 里把**表头**与数据行一起复制成文本贴进来（Tab 分隔最稳）。'
      + '材料不足时本工具不做任何认定、也不套用默认值 —— 既不说「在有效期内」，也不说「已超期」。',
  };
}

function pad2(n) { return (n < 10 ? '0' : '') + n; }

function ymd(y, m, d) { return y + '-' + pad2(m) + '-' + pad2(d); }

/** 严格解析日期：月/日都要在真实范围内（NaN 比较恒为 false，必须显式写出来） */
function parseDate(raw) {
  if (raw === undefined || raw === null) return null;
  const m = String(raw).trim().match(/^(\d{4})[-/.年](\d{1,2})(?:[-/.月](\d{1,2}))?日?$/);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = m[3] === undefined ? 1 : Number(m[3]);
  const dim = new Date(Date.UTC(y, mo, 0)).getUTCDate();
  if (mo < 1 || mo > 12 || d < 1 || d > dim) return null;
  return { y: y, m: mo, d: d, iso: ymd(y, mo, d) };
}

/** n 天后的 {y,m,d,iso} */
/** n 个月后的日期；短月溢出按月末截断（2026-01-31 + 1 月 = 2026-02-28），但 +12 月仍是同一天 */
function addMonths(dt, n) {
  const total = dt.y * 12 + (dt.m - 1) + n;
  const y = Math.floor(total / 12);
  const mo = (total % 12 + 12) % 12 + 1;
  const dim = new Date(Date.UTC(y, mo, 0)).getUTCDate();
  const d = Math.min(dt.d, dim);
  return { y: y, m: mo, d: d, iso: ymd(y, mo, d) };
}

/** 从任意文本里抓出第一个日期并规范化成 YYYY-MM-DD */
function isoIn(txt) {
  const m = String(txt == null ? '' : txt).match(/\d{4}[-/.]\d{1,2}[-/.]\d{1,2}/);
  if (!m) return null;
  const p = parseDate(m[0]);
  return p ? p.iso : null;
}

function diffDays(aIso, bIso) {
  const a = parseDate(aIso);
  const b = parseDate(bIso);
  if (!a || !b) return null;
  const A = Date.UTC(a.y, a.m - 1, a.d);
  const B = Date.UTC(b.y, b.m - 1, b.d);
  return Math.round((A - B) / 86400000);
}

function isoMax(list) {
  let best = null;
  for (const s of list) {
    if (!s) continue;
    if (best === null || diffDays(s, best) > 0) best = s;
  }
  return best;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '').replace(/[±＋+]/g, '');
  if (s === '' || RE_DASH.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || RE_DASH.test(s) || RE_PLACEHOLDER.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

// 关键词 → 角色的精确映射（按上面顺序建，先到先得）
const KEY_ROLE = new Map();
for (const pair of ROLE_KEYS) {
  for (const k of pair[1]) {
    const key = k.replace(/[\s（）()：:]/g, '');
    if (key && !KEY_ROLE.has(key)) KEY_ROLE.set(key, pair[0]);
  }
}
const ROLE_KEYWORDS = [...KEY_ROLE.keys()];

/** 表头 → 角色：**先精确命中**（'下次检定日期' 必须赢过 '上次检定日期' 里的子串），再退化到包含匹配 */
function roleOf(header) {
  const h = String(header == null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  if (KEY_ROLE.has(h)) return KEY_ROLE.get(h);
  for (const k of ROLE_KEYWORDS) {
    if (h.indexOf(k) >= 0) return KEY_ROLE.get(k);
  }
  return null;
}

/** 按 `#段名#` 把材料切成若干段；没标记的行归属上一段（没有则归主表）。
 *  ⛔ 必须**换标签**而不是「先 push 再新建」：材料以 `#计量器具台账#` 开头时，
 *     先 push 会把一个**空的主表段**留在前面，按 key 找主表就只找到那个空段 ⇒ 永远"材料不足"。 */
function splitSections(text) {
  const marks = [];
  for (const key of Object.keys(SECTION_MARKS)) marks.push([SECTION_MARKS[key], key]);
  const lines = String(text == null ? '' : text).split(/\r?\n/);
  const out = [];
  let cur = { key: 'ledger', mark: '', lines: [] };
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    let hit = null;
    for (const pair of marks) {
      if (String(raw).trim() === pair[0]) { hit = pair; break; }
    }
    if (hit) {
      if (cur.lines.length) out.push(cur);
      cur = { key: hit[1], mark: hit[0], lines: [] };
      continue;
    }
    cur.lines.push({ line: i + 1, raw: raw });
  }
  if (cur.lines.length) out.push(cur);
  return out;
}

/** 解析单段成 {error, header, cols, items, totals}；行是**扁平**对象：{line, raw, 角色:值…} */
function parseSection(text, sectionKey, payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  const sec = splitSections(text).find((s) => s.key === sectionKey) || { lines: [] };
  const body = sec.lines.filter((r) => String(r.raw).trim() !== '');
  if (!body.length) {
    return { error: 'empty', header: [], cols: [], items: [], totals: {}, missingRoles: REQUIRED_ROLES.slice(), missingColumns: [] };
  }
  const header = splitRow(body[0].raw);
  const own = SECTION_OWN_ROLES[sectionKey] || [];
  const alias = SECTION_ROLE_ALIAS[sectionKey] || {};
  const cols = header.map((h, k) => {
    let role = roleOf(h);
    if (role && alias[role]) role = alias[role];
    // 别段的列名（如证书明细里的「有效期至」）不许被认成本段角色 —— 否则会静默串味
    const ok = role && own.indexOf(role) >= 0;
    return { header: h, role: ok ? role : null, index: k };
  });
  const items = [];
  for (let r = 1; r < body.length; r++) {
    const cells = splitRow(body[r].raw);
    const it = { line: body[r].line, raw: body[r].raw };
    for (const c of cols) {
      if (!c.role) continue;
      it[c.role] = cells[c.index] === undefined ? '' : cells[c.index];
    }
    items.push(it);
  }
  const totals = {};
  for (const role of SUM_ROLES) {
    totals[role] = round2(items.reduce((acc, it) => {
      const n = normNumber(it[role]);
      return acc + (n === null ? 0 : n);
    }, 0));
  }
  return { error: null, header: header, cols: cols, items: items, totals: totals, missingRoles: [], missingColumns: [] };
}

/** 主表解析（契约名：parseTable）。缺必需列时 error='no_header' 且给 missingRoles/missingColumns */
function parseTable(text, payload) {
  const t = parseSection(text, 'ledger', payload);
  if (t.error === 'empty') {
    return {
      error: 'empty', header: [], cols: [], items: [], totals: {},
      missingRoles: REQUIRED_ROLES.slice(), missingColumns: REQUIRED_ROLES.map((r) => LABELS[r]),
    };
  }
  const missingRoles = REQUIRED_ROLES.filter((r) => !t.cols.some((c) => c.role === r));
  return Object.assign({}, t, {
    error: missingRoles.length ? 'no_header' : null,
    missingRoles: missingRoles,
    missingColumns: missingRoles.map((r) => LABELS[r]),
  });
}

const num = (it, role) => {
  const n = normNumber(it[role]);
  return n === null ? 0 : n;
};

function money(n) {
  const v = Math.abs(n) < 0.005 ? 0 : n;
  return v.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function who(it) {
  const name = String(it.itemName == null ? '' : it.itemName).trim();
  const no = String(it.itemNo == null ? '' : it.itemNo).trim();
  const head = no && name ? no + '「' + name + '」' : (name || no || '未命名器具');
  return '第 ' + it.line + ' 行「' + head + '」';
}

function cell(it, role) {
  const v = it[role];
  if (v === undefined || v === null) return '(缺列)';
  const s = String(v).trim();
  return s === '' ? '(空)' : s;
}

function finding(level, category, it, diff, message, advice) {
  const f = { level: level, category: category, line: it.line, message: message };
  if (typeof diff === 'number' && Number.isFinite(diff)) f.diff = round2(diff);
  if (advice) f.advice = advice;
  return f;
}

function isTotalRow(it) {
  const hay = [it.itemNo, it.itemName].map((v) => String(v == null ? '' : v).trim()).join(' ');
  return RE_TOTAL_ROW.test(hay);
}

/** 器具类别：器具名称优先，其次型号规格；认不出就归「其他计量器具」 */
/* ============================ 免费档检查（六项） ============================ */

/** 1. 到期覆盖核对：核对基准日 ≤ 下次检定日期；超期即报，给原文与超期天数 */
function checkExpiryCoverage(items, asOf) {
  const out = [];
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const next = parseDate(it.nextDate);
    if (!next) continue;
    const overdue = diffDays(asOf, next.iso);
    if (overdue === null || overdue <= 0) continue;
    const st = String(it.status == null ? '' : it.status).trim();
    out.push(finding('P0', '超期未检定仍在使用', it, overdue,
      who(it) + '：状态「' + (st || '(空)') + '」，下次检定日期 ' + next.iso
      + '（台账原文「' + cell(it, 'nextDate') + '」），核对基准日 ' + asOf + '，已超期 ' + overdue + ' 天。',
      '立即停用并送检：超期器具出具的检测数据在体系审核与监管检查中都不被承认。'
      + '本工具只按台账日期算超期天数，不判断检定周期定得对不对。'));
    out.push(finding('P1', '超期器具未列入送检安排', it, overdue,
      who(it) + '：超期 ' + overdue + ' 天（下次检定日期 ' + next.iso + '），台账状态原文是「' + (st || '(空)')
      + '」—— 看不出「已安排送检」，超期器具应能看到明确的送检安排。',
      '在台账里把送检安排列清楚（送检日期 / 受理单号 / 预计回所日期），'
      + '或在状态列用「送检中/待检定」把「超期未安排」和「已安排送检」区分开。'));
  }
  return out;
}

/** 2. 台账与证书一致性：证书编号 / 检定日期 / 有效期两边对不上即报 */
function checkCertConsistency(ledger, cert) {
  const out = [];
  if (!cert || !cert.items || !cert.items.length) return out;
  const byNo = new Map();
  for (const c of cert.items) {
    const no = String(c.itemNo == null ? '' : c.itemNo).trim();
    if (!no || byNo.has(no)) continue;
    byNo.set(no, c);
  }
  const pairs = [
    ['certNumber', '证书编号', 'certNumber'],
    ['lastDate', '检定日期', 'auditDate'],
    ['certValidTo', '有效期', 'validTo'],
  ];
  for (const it of ledger) {
    if (isTotalRow(it)) continue;
    const no = String(it.itemNo == null ? '' : it.itemNo).trim();
    if (!no) continue;
    const c = byNo.get(no);
    if (!c) continue;
    for (const pair of pairs) {
      // 台账那边的「有效期」列可能被认成 证书有效期至(certValidTo) 或 有效期(validTo) —— 两个别名都查
      const aRaw = it[pair[0]] != null ? it[pair[0]] : (pair[0] === 'certValidTo' ? it.validTo : undefined);
      const a = String(aRaw == null ? '' : aRaw).trim();
      const b = String(c[pair[2]] == null ? '' : c[pair[2]]).trim();
      if (a === '' || b === '') continue;
      const av = pair[1] === '证书编号' ? a : (isoIn(a) || a);
      const bv = pair[1] === '证书编号' ? b : (isoIn(b) || b);
      if (av === bv) continue;
      out.push(finding('P1', '台账与证书不一致：' + pair[1], it, undefined,
        who(it) + '：' + pair[1] + ' 两边对不上 —— 台账原文「' + a + '」（第 ' + it.line + ' 行），'
        + '证书明细原文「' + b + '」（第 ' + c.line + ' 行）。',
        '以检定机构出具的证书原件为准改台账（或换回正确的证书）；改完两边要能逐字对上，'
        + '否则体系审核会直接认定为「台账与证书不符」。'));
    }
  }
  return out;
}

/** 3. 校准周期勾稽：上次检定日期 + 校准周期(月) 应当等于 下次检定日期（逐行复算） */
function checkCycleMath(items) {
  const out = [];
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const last = parseDate(it.lastDate);
    const cycle = normNumber(it.cycleMonths);
    const next = parseDate(it.nextDate);
    if (!last || cycle === null || !next) continue;
    if (!(cycle > 0) || cycle !== Math.floor(cycle)) continue;
    const calc = addMonths(last, cycle);
    const gap = diffDays(next.iso, calc.iso);
    if (gap === null || gap === 0) continue;
    out.push(finding('P1', '校准周期勾稽不符', it, gap,
      who(it) + '：上次检定日期 ' + last.iso + ' + ' + cycle + ' 个月 = ' + calc.iso
      + '，但台账「下次检定日期」写的是 ' + next.iso + '（原文「' + cell(it, 'nextDate') + '」），相差 '
      + Math.abs(gap) + ' 天。',
      '按检定规程规定的周期重算下次到期日：先确认「校准周期(月)」这一列填的是规程规定的周期，再改到期日。'));
  }
  return out;
}

/** 4. 同一器具编号重复登记 */
function checkDuplicateId(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const no = String(it.itemNo == null ? '' : it.itemNo).trim();
    if (!no) continue;
    if (!seen.has(no)) seen.set(no, []);
    seen.get(no).push(it);
  }
  for (const [no, list] of seen) {
    if (list.length < 2) continue;
    const lines = list.map((x) => x.line).join('、');
    for (const it of list) {
      const others = list.filter((x) => x.line !== it.line).map((x) => x.line).join('、');
      out.push(finding('P0', '同一器具编号重复登记', it, undefined,
        who(it) + '：器具编号「' + no + '」在台账里出现了 ' + list.length + ' 次（第 ' + lines + ' 行）—— '
        + '本条与第 ' + others + ' 行是同一台器具的重复登记。',
        '一台器具在台账里只应有一条记录；换部门、换状态请**改这一条**，不要新增行，'
        + '否则到期提醒会漏、汇总台数会翻倍。'));
    }
  }
  return out;
}

/** 5. 合计行/统计行逐列复核（数量类列） */
function checkTotalsRows(items, headerCols) {
  const out = [];
  const details = items.filter((it) => !isTotalRow(it));
  const sumRoles = [];
  for (const c of headerCols || []) {
    if (!c.role) continue;
    if (QTY_ROLES.indexOf(c.role) >= 0 && sumRoles.indexOf(c.role) < 0) sumRoles.push(c.role);
  }
  for (const it of items) {
    if (!isTotalRow(it)) continue;
    if (!sumRoles.length) {
      out.push(finding('P1', '合计行无法复核', it, undefined,
        who(it) + '：这是一行合计/统计行，但它后面没有任何可逐列累加的数量类列（'
        + QTY_ROLES.map((r) => LABELS[r]).join('、') + ' 一个都没认出来）。',
        '合计行至少要能对上一个数量类列（数量(台) / 检定费用…）；'
        + '如果这行只是文字说明，请写在「备注」列里，别混在数据行中间。'));
      continue;
    }
    for (const role of sumRoles) {
      const stated = normNumber(it[role]);
      if (stated === null) continue;
      const sum = round2(details.reduce((acc, x) => acc + num(x, role), 0));
      const gap = round2(stated - sum);
      if (Math.abs(gap) < TOL) continue;
      out.push(finding('P1', '合计行与明细逐列不符', it, gap,
        who(it) + '：合计行「' + LABELS[role] + '」写的是 ' + money(stated) + '（原文「' + cell(it, role)
        + '」），而上面 ' + details.length + ' 行明细逐列累加得到 ' + money(sum) + '，相差 ' + money(gap) + '。',
        '合计行必须能被明细逐列复算出来；对不上时先查是不是漏了一行明细'
        + '（停用/报废器具也要保留在台账里，别为了凑合计把它删掉）。'));
    }
  }
  return out;
}

/** 6. 空白/占位符/日期格式/状态值非法 */
function checkFieldIntegrity(items) {
  const out = [];
  const dateRoles = [['lastDate', '上次检定日期'], ['nextDate', '下次检定日期']];
  for (const it of items) {
    if (isTotalRow(it)) continue;
    const miss = REQUIRED_FIELDS.filter((pair) => isBlank(it[pair[0]])).map((pair) => pair[1]);
    if (miss.length) {
      out.push(finding('P1', '关键字段缺失', it, undefined,
        who(it) + '：这些关键字段是空的或占位符 —— ' + miss.join('、') + '（原文：「' + String(it.raw).trim() + '」）。',
        '空着的字段会让对应的核对整项做不了；补全后重跑，本工具不会替你猜一个默认值。'));
    }
    for (const pair of dateRoles) {
      const raw = it[pair[0]];
      if (isBlank(raw)) continue;
      if (parseDate(raw)) continue;
      out.push(finding('P1', '日期格式非法', it, undefined,
        who(it) + '：「' + pair[1] + '」的值「' + String(raw).trim() + '」不是可识别的日期'
        + '（只认 2026-03-10 / 2026/03/10 / 2026年3月10日 三种写法；也检查了月份与日是否存在）。',
        '把日期改成 YYYY-MM-DD 再跑；日期认不出来的行，到期覆盖与周期勾稽都做不了，本工具不会替你换算。'));
    }
    const st = String(it.status == null ? '' : it.status).trim();
    if (st !== '' && ALLOWED_STATUS.indexOf(st) < 0) {
      out.push(finding('P1', '状态值非法', it, undefined,
        who(it) + '：状态写的是「' + st + '」，不在允许的状态集合内（' + ALLOWED_STATUS.join(' / ') + '）。',
        '状态值必须收敛到固定几个：在用 / 停用 / 报废（可细分送检中、待检定）。'
        + '写成「差不多在用」「待确认」这类自由文本，到期提醒与使用记录交叉核对都会失效。'));
    }
    for (const pair of AMOUNT_ROLES) {
      const raw = it[pair[0]];
      if (isBlank(raw)) continue;
      if (normNumber(raw) !== null) continue;
      out.push(finding('P1', '金额无法解析', it, undefined,
        who(it) + '：「' + pair[1] + '」的值「' + String(raw).trim() + '」不是可识别的金额（只认数字、千分位、¥、括号负数）。',
        '把金额改成纯数字形态（如 120.00）再跑；本工具不会把看不懂的值当成 0。'));
    }
  }
  return out;
}

/** 核对基准日：payload 里显式给的优先；否则用材料里最晚的使用/核查日期；再退到最晚的下次检定日期。
 *  ⚠️ 一律不用机器当天日期 —— 同一份材料必须每次都算出同一个超期天数（否则结论不可复算）。
 *  `source` 会写进 result.summary.as_of_source，让用户知道这个基准日是给的还是推的。 */
function asOfFromData(ledger, usage, spot, payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  const explicit = parseDate(p.asOf != null ? p.asOf : p.checkDate);
  if (explicit) return { date: explicit.iso, source: 'payload' };
  const used = [];
  for (const it of (usage && usage.items) || []) used.push(isoIn(it.usageDate));
  for (const it of (spot && spot.items) || []) used.push(isoIn(it.auditDate));
  const bestUsed = isoMax(used);
  if (bestUsed) return { date: bestUsed, source: 'latest_usage_or_spot_record' };
  const bestNext = isoMax(ledger.map((it) => isoIn(it.nextDate)));
  return { date: bestNext || '1970-01-01', source: 'latest_next_check_date' };
}

function run(payload) {
  const p = payload || {};
  const text = p.text != null ? p.text : (p.content != null ? p.content : '');
  const askText = '原文（text）：一张含表头的计量器具台账（可用 #证书明细# / #使用记录# 等小标题附上证书与使用记录）';
  if (!String(text).trim()) {
    return insufficient([askText]);
  }

  const t = parseTable(text, p);
  if (t.error === 'empty') {
    return insufficient([askText]);
  }
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的计量器具台账（至少要能认出「' + REQUIRED_ROLES.map((r) => LABELS[r]).join('」「') + '」）',
      t.missingRoles.length
        ? '本次没认出来的必需列：' + t.missingColumns.join('、')
        : '本次一行表头都没认出来（第一行必须是表头，Tab 分隔最稳）',
      '把 Excel 里的表头与数据行一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一行计量器具明细（现在只有表头，没有可核对的明细行）']);
  }

  const cert = parseSection(text, 'certificate', p);
  const agency = parseSection(text, 'agency', p);
  const usage = parseSection(text, 'usage', p);
  const spot = parseSection(text, 'spot', p);

  const asOfInfo = asOfFromData(t.items, usage, spot, p);
  const asOf = asOfInfo.date;
  const findings = [];
  const notRun = [];

  for (const f of checkExpiryCoverage(t.items, asOf)) findings.push(f);
  for (const f of checkCertConsistency(t.items, cert)) findings.push(f);
  for (const f of checkCycleMath(t.items)) findings.push(f);
  for (const f of checkDuplicateId(t.items)) findings.push(f);
  for (const f of checkTotalsRows(t.items, t.cols)) findings.push(f);
  for (const f of checkFieldIntegrity(t.items)) findings.push(f);

  let consolidated = null;
    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  findings.sort((x, y) => (x.line - y.line)
    || String(x.category).localeCompare(String(y.category))
    || (Math.abs(y.diff || 0) - Math.abs(x.diff || 0)));

  const result = {
    findings: findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      as_of: asOf,
      as_of_source: asOfInfo.source,
      overdue_total: consolidated ? consolidated.total_overdue : null,
      cycle_months_total: t.totals.cycleMonths,
      qty_total: t.totals.qty,
      amount_total: t.totals.amount,
      basis: '核对基准日 ≤ 下次检定日期（超期即报，给出超期天数）；台账与证书的证书编号/检定日期/有效期须逐字一致；'
        + '上次检定日期 + 校准周期(月) 须等于下次检定日期；同一器具编号在台账里只能出现一次；'
        + '合计行的数量类列须等于明细逐列累加；日期格式与状态值须合法。',
    },
    columns: t.header,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张台账按上面写明的口径算得对、日期与状态都在有效期内**，'
      + '不代表检定/校准结果本身合格、也不代表该器具适用哪一档强制检定管理 —— 那些不在本工具范围内。';
  }

  result.scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    rows: t.items.length,
    columns_recognized: t.cols.filter((c) => c.role).length,
    as_of: asOf,
    as_of_source: asOfInfo.source,
    sections: {
      ledger: t.items.length,
      certificate: (cert.items || []).length,
      agency: (agency.items || []).length,
      usage: (usage.items || []).length,
      spot: (spot.items || []).length,
    },
    cycle_months_total: t.totals.cycleMonths,
    qty_total: t.totals.qty,
    amount_total: t.totals.amount,
  };



  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
