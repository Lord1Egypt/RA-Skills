import { SkillError } from './errors.mjs';
import { currentTaskEvidencePolicy } from './evidence-policy.mjs';

import {
  coerceNodeValue,
  formatDateForDisplay,
  isMinuteDate,
  isMonthOnlyDate
} from './answer-coercion.mjs';

const COMPONENT_TYPES = new Map([
  ['1', 'single_select'],
  ['2', 'multi_select'],
  ['3', 'text'],
  ['4', 'field_group'],
  ['6', 'repeatable_group'],
  ['8', 'date_range'],
  ['9', 'money'],
  ['10', 'date'],
  ['11', 'date'],
  ['12', 'number'],
  ['13', 'number'],
  ['17', 'region'],
  ['18', 'single_select'],
  ['20', 'number'],
  ['21', 'exchange_rate'],
  ['22', 'liquidated_damages'],
  ['23', 'single_select'],
  ['25', 'number_unit']
]);

const HTML_ENTITIES = new Map([
  ['amp', '&'], ['lt', '<'], ['gt', '>'], ['quot', '"'], ['apos', "'"],
  ['nbsp', ' '], ['ensp', ' '], ['emsp', ' '], ['middot', '·']
]);

const ASK_USER_QUESTION_LIMITS = Object.freeze({
  maxQuestions: 4,
  minOptions: 2,
  maxOptions: 4
});

const SUGGESTED_CHOICE_FIELD_TYPES = new Set([
  'text',
  'number',
  'money',
  'date',
  'date_range',
  'region',
  'exchange_rate',
  'liquidated_damages',
  'number_unit'
]);

const PERSON_NAME_PATTERN = /姓名|名字|联系人|真实姓名|法定代表人姓名|经办人姓名|(?:^|[^a-z])(realname|fullname|personname|contactname)(?:$|[^a-z])/i;
const PHONE_PATTERN = /电话|手机号|手机号码|联系电话|联系手机|联系方式|座机|(?:^|[^a-z])(phone|mobile|telephone|tel)(?:$|[^a-z])/i;
const IDENTITY_NUMBER_PATTERN = /身份证|公民身份号码|身份号码|证件号码|证件号|(?:^|[^a-z])(idcard|identitynumber|identityno)(?:$|[^a-z])/i;
const PROTECTED_REGION_PATTERN = /居住(?:地|地址)|实际(?:居住地|住址)|现(?:居住地|住址)|户籍(?:地|地址)|户口(?:所在地|地址)|住所(?:地|地址)|常住(?:地|地址)|经常居住地|身份证(?:上的)?登记地址|registeredaddress|residentialaddress|domicile/i;

// 这类题通常由后端按“所有可能类别”展开，但用户只选择了其中一类。
// 不能把“没有提到”当成否定；只有当前任务明确排除某类别时，才允许把依赖该类别的字段标记为不适用。
const CONDITIONAL_CATEGORY_PATTERNS = Object.freeze([
  { key: 'vehicle', field: /车辆|辆车|汽车|机动车|摩托车|电动车|车牌|购车|车辆数量|汽车数量/i, category: /车辆|辆车|汽车|机动车|摩托车|电动车|车牌|购车/i },
  { key: 'real_estate', field: /房产|房屋|住宅|不动产|门面|土地|房产数量/i, category: /房产|房屋|住宅|不动产|门面|土地/i },
  { key: 'deposit', field: /存款|银行存款|现金|账户余额|存款金额/i, category: /存款|银行存款|现金|账户余额/i },
  { key: 'securities', field: /股票|基金|证券|理财|债券/i, category: /股票|基金|证券|理财|债券/i },
  { key: 'equity', field: /股权|股份|公司出资|企业/i, category: /股权|股份|公司出资|企业/i },
  { key: 'insurance', field: /保险|保单|保险现金价值/i, category: /保险|保单/i }
]);

const EXPLICIT_NON_APPLICABLE_PATTERN = /(?:没有|无|不存在|未涉及|不涉及|不含|排除|没有任何|没有提到|并无|不属于)/;
const EXPLICIT_ONLY_CATEGORY_PATTERN = /(?:只有|仅有|只涉及|仅涉及|选择(?:了|的)?(?:是|为)?|争议(?:财产)?类型\s*(?:是|为|=|：|:)?|财产类型\s*(?:是|为|=|：|:)?)\s*([^。；;\n]+)/;

export function decodeHtml(value = '') {
  return String(value)
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([0-9a-f]+);/gi, (_, code) => String.fromCodePoint(Number.parseInt(code, 16)))
    .replace(/&([a-z]+);/gi, (match, name) => HTML_ENTITIES.get(name.toLowerCase()) ?? match);
}

export function plainText(value = '') {
  return decodeHtml(String(value))
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/[\t\r ]+/g, ' ')
    .replace(/\n\s+/g, '\n')
    .trim();
}

function nodeKey(node, fallback) {
  return String(
    node?.id
    || node?.nodeId
    || node?.questionKey
    || node?.code
    || node?.uuid
    || fallback
  );
}

function optionLabel(option) {
  return plainText(option?.title || option?.name || option?.label || option?.value || '');
}

function optionValue(option, fallback) {
  return String(option?.id ?? option?.code ?? option?.value ?? fallback);
}

function normalizeOptions(node) {
  const children = Array.isArray(node?.children)
    ? node.children
    : Array.isArray(node?.options)
      ? node.options
      : [];
  const selectedValues = new Set(
    (Array.isArray(node?.value) ? node.value : [node?.value])
      .filter(value => value !== undefined && value !== null && value !== '')
      .map(value => String(value))
  );
  return children.map((option, index) => {
    const followUps = Array.isArray(option?.add) ? option.add.filter(Boolean) : [];
    const value = optionValue(option, index + 1);
    return {
      value,
      label: optionLabel(option) || `选项${index + 1}`,
      description: plainText(option?.description || option?.remark || ''),
      selected: option?.selected === true || option?.checked === true || selectedValues.has(value),
      disabled: Boolean(option?.readyOnly || option?.readonly),
      hasFollowUp: followUps.length > 0,
      followUpCount: followUps.length
    };
  });
}

function fieldType(node) {
  return COMPONENT_TYPES.get(String(node?.component ?? node?.type ?? '')) || 'text';
}

function fieldRequired(node) {
  return Boolean(node?.required ?? node?.config?.required);
}

function fieldSearchText(label, key) {
  return `${plainText(label)} ${String(key || '')}`;
}

function isProtectedRegionField(label, key) {
  return PROTECTED_REGION_PATTERN.test(fieldSearchText(label, key));
}

function isPersonNameField(label, key) {
  return PERSON_NAME_PATTERN.test(fieldSearchText(label, key));
}

function isSensitiveField(label, key) {
  const text = fieldSearchText(label, key);
  // 居住地、户籍地等地区字段会影响政策、地方法规和计算标准，不能按敏感信息跳过。
  if (isProtectedRegionField(label, key)) return false;
  return PERSON_NAME_PATTERN.test(text)
    || PHONE_PATTERN.test(text)
    || IDENTITY_NUMBER_PATTERN.test(text);
}

function conditionalCategoryForField(label, key) {
  const text = fieldSearchText(label, key);
  return CONDITIONAL_CATEGORY_PATTERNS.find(item => item.field.test(text)) || null;
}

function hasExplicitCategoryExclusion(contextText, categoryPattern) {
  const text = plainText(contextText);
  if (!text || !categoryPattern) return false;
  // “没有汽车/不涉及车辆”是直接证据；只检查类别附近的窗口，避免把别的事实误判为排除。
  const categoryRegex = new RegExp(
    categoryPattern.source,
    categoryPattern.flags.includes('g') ? categoryPattern.flags : `${categoryPattern.flags}g`
  );
  const categoryMatches = [...text.matchAll(categoryRegex)];
  if (categoryMatches.some(match => {
    const start = Math.max(0, (match.index || 0) - 18);
    const end = Math.min(text.length, (match.index || 0) + String(match[0]).length + 18);
    return EXPLICIT_NON_APPLICABLE_PATTERN.test(text.slice(start, end));
  })) return true;

  // “只有存款/争议财产类型=存款”这类表述明确限定了类别集合。
  const onlyMatch = text.match(EXPLICIT_ONLY_CATEGORY_PATTERN);
  if (!onlyMatch) return false;
  const selected = onlyMatch[1] || '';
  const selectedCategories = CONDITIONAL_CATEGORY_PATTERNS
    .filter(item => item.category.test(selected))
    .map(item => item.key);
  const current = CONDITIONAL_CATEGORY_PATTERNS.find(item => item.category === categoryPattern);
  return selectedCategories.length > 0 && Boolean(current) && !selectedCategories.includes(current.key);
}

function fieldApplicability(node, label, key, contextText = '') {
  const config = node?.config || {};
  const explicitConfig = node?.notApplicable === true
    || config.notApplicable === true
    || config.applicable === false
    || config.isApplicable === false;
  const category = conditionalCategoryForField(label, key);
  const explicitContext = category && hasExplicitCategoryExclusion(contextText, category.category);
  if (!explicitConfig && !explicitContext) return null;
  return {
    status: 'not_applicable',
    reason: explicitConfig ? 'backend_explicit_non_applicable' : 'current_task_explicit_category_exclusion',
    category: category?.key || null,
    evidenceRequired: true
  };
}

function normalizeSimpleNode(node, key, options = {}) {
  const type = fieldType(node);
  const readonly = Boolean(node?.readyOnly || node?.readonly);
  const backendRequired = fieldRequired(node);
  const label = plainText(node?.title || node?.name || node?.label || key);
  const sensitive = isSensitiveField(label, key);
  const skipIfOptionalSensitive = !backendRequired && !readonly && sensitive;
  const applicability = fieldApplicability(node, label, key, options.suggestionContext || '');
  const notApplicable = Boolean(applicability);
  // 姓名等仅用于报告展示的可选字段没有可凭空生成的合法候选值。
  // 所有非必填敏感字段都不应阻塞流程；姓名继续保留 displayOnly 兼容标记。
  const displayOnly = skipIfOptionalSensitive && type === 'text' && isPersonNameField(label, key);
  const field = {
    key,
    label,
    type,
    required: backendRequired,
    backendRequired,
    responseRequired: !readonly && !skipIfOptionalSensitive && !notApplicable,
    displayOnly,
    sensitive,
    skipIfOptionalSensitive,
    notApplicable,
    applicability,
    skipReason: applicability?.reason || null,
    value: node?.value ?? '',
    options: ['single_select', 'multi_select'].includes(type) ? normalizeOptions(node) : [],
    unit: node?.config?.unit || node?.unit || '',
    help: plainText(node?.tips || node?.description || node?.remark || ''),
    readonly
  };
  const contract = valueContract(node, type);
  if (contract) field.valueContract = contract;
  if (type === 'date' && field.value) field.displayValue = formatDateForDisplay(node, field.value);
  return field;
}

// 告诉宿主这道题的取值形状和填写粒度。脚本会自动完成转换，
// 但宿主需要据此提问：年月题不要追问"日"，地区题要问到 areaLevel 指定的层级。
function valueContract(node, type) {
  const config = node?.config || {};
  if (type === 'date') {
    return {
      submit: 'unix_seconds',
      granularity: isMonthOnlyDate(node) ? 'year_month' : (isMinuteDate(node) ? 'minute' : 'day'),
      accepts: '1991-11-08、1991年11月、199111 等常见写法，脚本会转换成后端要求的取值'
    };
  }
  if (type === 'date_range') {
    return { submit: 'range_object', accepts: '["2024-01-01","2024-03-31"] 或 "2024-01-01 至 2024-03-31"' };
  }
  if (type === 'region') {
    const level = Number(config.areaLevel);
    const areaLevel = Number.isInteger(level) && level >= 1 && level <= 3 ? level : 2;
    return {
      submit: 'area_id',
      areaLevel,
      requiredDepth: ['省或直辖市', '省市', '省市区县'][areaLevel - 1],
      accepts: '地区名称或地区 id；名称必须覆盖到 requiredDepth 指定的层级'
    };
  }
  if (type === 'number_unit') {
    const units = String(config.nameUnit || '').split(',').map(item => item.trim()).filter(Boolean);
    return { submit: 'value_unit_object', units };
  }
  if (['exchange_rate', 'liquidated_damages'].includes(type)) {
    return { submit: 'option_content_object' };
  }
  return null;
}

function normalizeRepeatableNode(node, key, options = {}) {
  const readonly = Boolean(node?.readyOnly || node?.readonly);
  const children = Array.isArray(node.children) ? node.children : [];
  const rowCount = Math.max(
    1,
    ...children.map(child => Array.isArray(child.value) ? child.value.length : 0)
  );
  const fields = children.map((child, index) => ({
    ...normalizeSimpleNode(child, nodeKey(child, `${key}-field-${index + 1}`), options),
    // 重复记录中的姓名是当事人/记录的实际内容，不能按报告展示字段跳过。
    displayOnly: false,
    skipIfOptionalSensitive: false
  }));
  const rows = Array.from({ length: rowCount }, (_, rowIndex) => Object.fromEntries(
    fields.map((field, fieldIndex) => {
      const rawValue = children[fieldIndex]?.value;
      return [field.key, Array.isArray(rawValue) ? (rawValue[rowIndex] ?? '') : (rowIndex === 0 ? rawValue ?? '' : '')];
    })
  ));
  return {
    key,
    label: plainText(node?.title || node?.config?.matrixDynamicTitle || key),
    type: 'repeatable_group',
    required: fieldRequired(node),
    backendRequired: fieldRequired(node),
    responseRequired: !readonly,
    readonly,
    fields,
    rows,
    minItems: 1,
    maxItems: Number(node?.config?.matrixDynamicMax || 50),
    itemLabel: plainText(node?.config?.matrixDynamicTitle || node?.config?.nameUnit || '记录')
  };
}

function fieldJsonSchema(field) {
  if (field.type === 'single_select') {
    const choices = field.options.map(option => ({ const: option.value, title: option.label }));
    return {
      type: 'string',
      title: field.label,
      enum: field.options.map(option => option.value),
      enumNames: field.options.map(option => option.label),
      'x-enumNames': field.options.map(option => option.label),
      oneOf: choices
    };
  }
  if (field.type === 'multi_select') {
    const choices = field.options.map(option => ({ const: option.value, title: option.label }));
    return {
      type: 'array',
      title: field.label,
      items: {
        type: 'string',
        enum: field.options.map(option => option.value),
        enumNames: field.options.map(option => option.label),
        'x-enumNames': field.options.map(option => option.label),
        oneOf: choices
      },
      uniqueItems: true
    };
  }
  if (field.type === 'repeatable_group') {
    return {
      type: 'array',
      title: field.label,
      items: {
        type: 'object',
        properties: Object.fromEntries(field.fields.map(item => [item.key, fieldJsonSchema(item)])),
        required: field.fields.filter(item => item.responseRequired).map(item => item.key)
      }
    };
  }
  if (['money', 'number', 'number_unit', 'exchange_rate', 'liquidated_damages'].includes(field.type)) {
    return { type: 'number', title: field.label, description: field.help || undefined };
  }
  return { type: 'string', title: field.label, description: field.help || undefined };
}

function fieldText(field, index, total) {
  const prefix = total > 1 ? `${index + 1}. ` : '';
  const required = field.required ? '（必填）' : field.responseRequired ? '（请回答）' : '';
  const unit = field.unit ? `（单位：${field.unit}）` : '';
  const heading = `${prefix}${field.label}${required}${unit}`;
  if (['single_select', 'multi_select'].includes(field.type) && field.options.length) {
    const options = field.options.map((option, optionIndex) => `${optionIndex + 1}. ${option.label}`).join('\n');
    const instruction = field.type === 'multi_select'
      ? '请直接回复一个或多个选项编号（例如：1、3），也可以回复选项文字。'
      : '请直接回复选项编号，也可以回复选项文字。';
    return `${heading}\n${options}\n${instruction}`;
  }
  if (field.type === 'repeatable_group') {
    const labels = field.fields.map(item => item.label).join('、');
    return `${heading}\n请逐条提供：${labels}。`;
  }
  return `${heading}\n请直接输入${field.type === 'date' ? '日期' : '内容'}。`;
}

function questionText(label) {
  const text = plainText(label);
  return /[？?]$/.test(text) ? text : `${text}？`;
}

function shortHeader(label) {
  const text = plainText(label).replace(/[？?。！!：:；;，,、]/g, '').trim();
  return Array.from(text).slice(0, 12).join('') || '请选择';
}

function optionCandidate(value, label, description = '') {
  return {
    value: String(value),
    label: plainText(label),
    description: plainText(description),
    selected: false,
    disabled: false,
    hasFollowUp: false,
    followUpCount: 0,
    generated: true
  };
}

function uniqueCandidates(candidates = []) {
  const seen = new Set();
  return candidates.filter(candidate => {
    const key = `${candidate.value}\u0000${candidate.label}`;
    if (!candidate.label || seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, ASK_USER_QUESTION_LIMITS.maxOptions);
}

function amountCandidates(label) {
  if (/月工资|月收入|工资收入|收入标准/.test(label)) return [3000, 5000, 8000, 10000];
  if (/鉴定费|评估费|检验费/.test(label)) return [500, 1000, 2000, 3000];
  if (/医疗|住院|治疗|手术/.test(label)) return [1000, 5000, 10000, 50000];
  if (/交通|住宿|护理|营养|误工/.test(label)) return [500, 1000, 3000, 5000];
  return [500, 1000, 3000, 5000];
}

function numberCandidates(label) {
  if (/伤残.*等级|伤残等级/.test(label)) {
    return [
      optionCandidate(0, '无伤残等级'),
      optionCandidate(10, '十级伤残'),
      optionCandidate(9, '九级伤残'),
      optionCandidate(8, '八级伤残')
    ];
  }
  if (/年龄|周岁/.test(label)) return [18, 30, 45, 60];
  if (/天数|期限|住院|误工|护理|营养|休养/.test(label)) return [30, 60, 90, 120];
  if (/月数|几个月|多少个月/.test(label)) return [1, 3, 6, 12];
  if (/年数|几年|多少年/.test(label)) return [1, 2, 3, 5];
  if (/比例|百分比|责任份额/.test(label)) return [10, 30, 50, 100];
  if (/人数|数量|子女|孩子|几人/.test(label)) return [1, 2, 3, 4];
  return [1, 2, 3, 5];
}

function isoDateOffset(days) {
  const date = new Date();
  date.setHours(12, 0, 0, 0);
  date.setDate(date.getDate() - days);
  return date.toISOString().slice(0, 10);
}

function contextDates(contextText = '') {
  const values = [];
  const pattern = /(20\d{2})[年/-](\d{1,2})[月/-](\d{1,2})(?:日|号)?/g;
  for (const match of String(contextText).matchAll(pattern)) {
    values.push(`${match[1]}-${String(match[2]).padStart(2, '0')}-${String(match[3]).padStart(2, '0')}`);
  }
  return [...new Set(values)];
}

// 出生年月、参保年月这类字段的正确答案在几十年前，"今天/约一个月前"是无效候选，
// 只会诱导宿主提交一个能通过校验但完全错误的日期。这类题必须回到用户填写。
// 注意不要用裸的“生日”，否则“事故发生日期”里的“发生日期”会被误判。
const HISTORICAL_DATE_PATTERN = /出生|^生日|参加工作|参工|入职|参保|退休|建账|开户|结婚/;

function dateCandidates(contextText = '', field = {}) {
  const fromContext = contextDates(contextText).map(value => optionCandidate(value, value, '来自当前案情中的日期'));
  if (HISTORICAL_DATE_PATTERN.test(String(field.label || ''))) return fromContext;
  return [
    ...fromContext,
    optionCandidate(isoDateOffset(0), isoDateOffset(0), '今天'),
    optionCandidate(isoDateOffset(30), isoDateOffset(30), '约一个月前'),
    optionCandidate(isoDateOffset(90), isoDateOffset(90), '约三个月前'),
    optionCandidate(isoDateOffset(365), isoDateOffset(365), '约一年前')
  ];
}

function dateRangeCandidates() {
  const end = isoDateOffset(0);
  return [7, 30, 90, 365].map(days => {
    const start = isoDateOffset(days);
    return optionCandidate(`${start} 至 ${end}`, `${start} 至 ${end}`, `最近${days}天`);
  });
}

// 地区题的取值是地区表里的 id，"事故发生地""经常居住地"不是地区，
// 提交上去必然匹配失败，因此只保留当前案情里真实出现过的地名。
function regionCandidates(contextText = '') {
  const matches = String(contextText).match(/(?:北京|上海|天津|重庆)市(?:[\u4e00-\u9fa5]{1,12}(?:区|县|镇|街道))?|[\u4e00-\u9fa5]{2,8}(?:省|自治区|特别行政区)(?:[\u4e00-\u9fa5]{1,12}(?:市|自治州|地区|州|盟))?(?:[\u4e00-\u9fa5]{1,12}(?:区|县|市|旗|镇|街道))?/g) || [];
  return matches.map(value => optionCandidate(value, value, '来自当前案情中的地区'));
}

function textCandidates(label) {
  if (/是否|有无|能否|是否存在|是否已经/.test(label)) return ['是', '否'];
  if (/伤情|受伤|损伤|伤势/.test(label)) return ['软组织损伤', '骨折', '内脏损伤', '多处复合伤'];
  if (/职业|工作性质|就业/.test(label)) return ['企业职工', '个体经营', '灵活就业', '无固定职业'];
  if (/关系|亲属/.test(label)) return ['配偶', '父母', '子女', '兄弟姐妹'];
  if (/支付|付款|转账方式/.test(label)) return ['银行转账', '现金支付', '微信支付', '支付宝支付'];
  if (/治疗方式|诊疗方式/.test(label)) return ['门诊治疗', '住院治疗', '手术治疗', '康复治疗'];
  if (/证据|证明材料/.test(label)) return ['书面材料', '转账记录', '聊天记录', '证人证言'];
  if (/责任/.test(label)) return ['无责任', '次要责任', '同等责任', '主要责任'];
  return ['未发生', '已经发生', '正在进行', '已经完成'];
}

function suggestedCandidates(field, contextText = '') {
  const sourceType = field.originalType || field.type;
  const label = `${field.label || ''}${field.unit || ''}`;
  if (sourceType === 'money') {
    return amountCandidates(label).map(value => optionCandidate(value, `${value.toLocaleString('zh-CN')}元`));
  }
  if (['number', 'number_unit'].includes(sourceType)) {
    const values = numberCandidates(label);
    return values.map(value => typeof value === 'object'
      ? value
      : optionCandidate(value, `${value}${field.unit || (/年龄|周岁/.test(label) ? '岁' : /天数|期限|住院|误工|护理|营养|休养/.test(label) ? '天' : '')}`));
  }
  if (sourceType === 'date') return dateCandidates(contextText, field);
  if (sourceType === 'date_range') return dateRangeCandidates();
  if (sourceType === 'region') return regionCandidates(contextText);
  if (sourceType === 'exchange_rate') return [1, 6.5, 7, 7.5].map(value => optionCandidate(value, String(value)));
  if (sourceType === 'liquidated_damages') return [0, 10, 20, 30].map(value => optionCandidate(value, `${value}%`));
  return textCandidates(label).map(value => optionCandidate(value, value));
}

function suggestedChoiceEligible(field) {
  const sourceType = field?.originalType || field?.type;
  return !field?.readonly
    && !field?.sensitive
    && !field?.skipIfOptionalSensitive
    && SUGGESTED_CHOICE_FIELD_TYPES.has(sourceType);
}

function materializeSuggestedChoice(field, contextText = '') {
  if (!suggestedChoiceEligible(field)) return field;
  const originalType = field.originalType || field.type;
  const options = uniqueCandidates(suggestedCandidates({ ...field, originalType }, contextText));
  if (options.length < ASK_USER_QUESTION_LIMITS.minOptions) return field;
  return {
    ...field,
    originalType,
    type: 'single_select',
    options,
    suggestedChoice: {
      materialized: true,
      originalType,
      optionCount: options.length,
      source: 'skill_common_sense_rules',
      hostGenerationRequired: false,
      hostProvidesOtherInput: true,
      userMustConfirm: true
    }
  };
}

function nativeChoiceCompatible(field) {
  return ['single_select', 'multi_select'].includes(field?.type)
    && field.options.length >= ASK_USER_QUESTION_LIMITS.minOptions
    && field.options.length <= ASK_USER_QUESTION_LIMITS.maxOptions
    && field.options.every(option => option.label && !option.disabled);
}

function nativeQuestionForField(field) {
  return {
    question: questionText(field.label),
    header: shortHeader(field.label),
    options: field.options.map(option => ({
      label: option.label,
      description: option.description || ''
    })),
    multiSelect: field.type === 'multi_select'
  };
}

function autoSkipUnit(field, order) {
  return {
    order,
    fieldKey: field.key,
    type: field.type,
    mode: 'skip',
    reason: field.notApplicable
      ? 'explicit_non_applicable'
      : field.displayOnly
        ? 'optional_display_only'
        : 'optional_sensitive',
    label: field.label
  };
}

function chunk(values, size) {
  const chunks = [];
  for (let index = 0; index < values.length; index += size) {
    chunks.push(values.slice(index, index + size));
  }
  return chunks;
}

function buildRenderPlan(fields) {
  const nativeFields = fields.filter(nativeChoiceCompatible);
  const nativeQuestionBatches = chunk(nativeFields, ASK_USER_QUESTION_LIMITS.maxQuestions).map((batch, index) => ({
    batch: index + 1,
    tool: 'AskUserQuestion',
    fieldKeys: batch.map(field => field.key),
    input: { questions: batch.map(nativeQuestionForField) }
  }));
  const nativeFieldKeys = new Set(nativeFields.map(field => field.key));
  const units = fields.map((field, index) => (field.notApplicable || field.displayOnly || field.skipIfOptionalSensitive) && isEmptyAnswer(field.value)
    ? autoSkipUnit(field, index + 1)
    : nativeFieldKeys.has(field.key)
    ? {
        order: index + 1,
        fieldKey: field.key,
        type: field.type,
        mode: 'native_choice',
        tool: 'AskUserQuestion',
        input: { questions: [nativeQuestionForField(field)] }
      }
    : {
        order: index + 1,
        fieldKey: field.key,
        type: field.type,
        mode: 'input',
        label: field.label,
        prompt: fieldText(field, 0, 1)
      });

  return {
    mode: fields.length > 1 ? 'sequential_units' : (units[0]?.mode || 'input'),
    units,
    allFieldsRepresented: true,
    nativeQuestionBatches,
    nativeChoiceFieldKeys: [...nativeFieldKeys],
    nativeChoiceCoverageComplete: fields.length > 0 && nativeFields.length === fields.length,
    suggestedChoiceFieldKeys: fields.filter(field => field.suggestedChoice?.materialized).map(field => field.key),
    allFillChoicesMaterialized: fields
      .filter(field => SUGGESTED_CHOICE_FIELD_TYPES.has(field.originalType || field.type))
      .every(field => field.suggestedChoice?.materialized),
    nativeToolConstraints: {
      tool: 'AskUserQuestion',
      minQuestions: 1,
      maxQuestions: ASK_USER_QUESTION_LIMITS.maxQuestions,
      minOptions: ASK_USER_QUESTION_LIMITS.minOptions,
      maxOptions: ASK_USER_QUESTION_LIMITS.maxOptions,
      textInputsSupported: false
    }
  };
}

function withResponsePolicy(field) {
  const readonly = Boolean(field?.readonly);
  return {
    ...field,
    backendRequired: field?.backendRequired ?? Boolean(field?.required),
    responseRequired: field?.responseRequired ?? !readonly,
    sensitive: Boolean(field?.sensitive),
    skipIfOptionalSensitive: Boolean(field?.skipIfOptionalSensitive),
    readonly,
    fields: Array.isArray(field?.fields) ? field.fields.map(withResponsePolicy) : field?.fields
  };
}

// 案情里已经说清楚的题目，应该由宿主大模型做语义判断后直接作答，
// 而不是回头再问用户一遍。这与项目选型用的是同一套范式：脚本只声明
// 判定门槛和边界，语义理解交给模型。
//
// 之所以不在脚本里用关键词或正则去匹配：选项内容是开放的（身份、类型、
// 时长、金额、日期、是否……），案情表达更是千变万化（"老板"对"用人单位"、
// "钱是我借给他的"对"债权人"）。规则只能覆盖少数固定形态，覆盖不到的
// 静默漏掉，覆盖错的静默填错，两种都比交回用户更糟。
export const SEMANTIC_ANSWER_PROMPT = '先按 answerPolicy 做语义判断：把选项与当前案情逐一比对，含义一致即可，不要求字面相同（"拖欠5年"即"超过三年"，"老板"即"用人单位"）。达到 autoAnswer 门槛就直接用该选项 value 调用 question-reply，多选题提交全部成立项；依据不足或多项都可能成立才交给用户，不猜测，不选兜底项。';

function semanticAnswerPolicy() {
  return {
    matchingMode: 'host_model_semantic_answering',
    basis: 'current_task_case_text_and_confirmed_answers',
    matching: 'meaning_not_literal',
    autoAnswer: {
      minimumConfidence: 0.85,
      requireClearlyBestOption: true,
      multiSelectSubmitsAllSupportedOptions: true
    },
    uncertain: {
      action: 'ask_user_to_choose',
      neverGuess: true,
      neverDefaultToCatchAllOption: true
    }
  };
}

export function withInteractionRendering(interaction, options = {}) {
  if (!interaction) return null;
  const caseText = options.suggestionContext || interaction.caseContext?.text || '';
  const fields = Array.isArray(interaction.fields)
    ? interaction.fields
        .map(withResponsePolicy)
        .map(field => materializeSuggestedChoice(field, caseText))
    : [];
  const primary = fields.length === 1 ? fields[0] : null;
  const renderPlan = buildRenderPlan(fields);
  const properties = Object.fromEntries(fields.map(field => [field.key, fieldJsonSchema(field)]));
  const textFallback = fields.length
    ? fields.map((field, index) => fieldText(field, index, fields.length)).join('\n\n')
    : interaction.title || interaction.description || '';
  const choices = primary && ['single_select', 'multi_select'].includes(primary.type)
    ? primary.options.map((option, index) => ({
        number: index + 1,
        position: index + 1,
        total: primary.options.length,
        value: option.value,
        answer: option.label,
        label: option.label,
        description: option.description || '',
        selected: option.selected,
        disabled: option.disabled,
        hasFollowUp: option.hasFollowUp,
        followUpCount: option.followUpCount
      }))
    : [];
  const optionManifest = fields
    .filter(field => ['single_select', 'multi_select'].includes(field.type))
    .map(field => ({
      fieldKey: field.key,
      question: field.label,
      type: field.type,
      expectedOptionCount: field.options.length,
      requireExactRenderedCount: true,
      options: field.options.map((option, index) => ({
        number: index + 1,
        position: index + 1,
        value: option.value,
        answer: option.label,
        label: option.label,
        selected: option.selected,
        disabled: option.disabled
      }))
    }));
  return {
    ...interaction,
    fields,
    protocol: 'lvpin.interaction/v1',
    evidenceScope: currentTaskEvidencePolicy(interaction.sessionId || null),
    native: {
      preferredTool: 'AskUserQuestion',
      batches: renderPlan.nativeQuestionBatches,
      complete: renderPlan.nativeChoiceCoverageComplete,
      coveredFieldKeys: renderPlan.nativeChoiceFieldKeys
    },
    suggestedChoices: {
      materializedBySkill: true,
      hostGenerationRequired: false,
      fieldKeys: renderPlan.suggestedChoiceFieldKeys,
      oneFieldAtATime: true,
      minOptions: ASK_USER_QUESTION_LIMITS.minOptions,
      maxOptions: ASK_USER_QUESTION_LIMITS.maxOptions,
      hostProvidesOtherInput: true
    },
    renderPlan,
    renderHints: {
      preferNativeControls: true,
      nativeControlsRequired: true,
      mustInvokeNativeTool: true,
      capabilityDetection: true,
      preferredTools: ['request_user_input', 'AskUserQuestion', 'ask_user'],
      nativeKinds: choices.length ? ['choice', 'question'] : ['input', 'form'],
      requireCompleteRepresentation: true,
      requireAllOptionsRendered: true,
      requireRenderedOptionCountMatch: true,
      forbidOptionTruncation: true,
      forbidOptionOmission: true,
      incompleteRenderingAction: 'reject_and_rerender',
      capacityFallbackOrder: [
        'native_selector_with_all_options',
        'native_form_or_input_with_complete_numbered_option_list',
        'complete_text_fallback_only_without_compatible_native_tool'
      ],
      tryAlternativeNativeToolsBeforeFallback: true,
      forbidPlainTextWhenNativeAvailable: true,
      fallbackRequiresCapabilityCheck: true,
      fallbackAllowedOnlyWhen: 'no_compatible_native_tool',
      fallback: 'textFallback'
    },
    presentation: {
      mode: 'native_control_required',
      mustUseNativeComponent: true,
      allOptionsMustBeVisible: true,
      optionCountVerificationRequired: true,
      incompleteOptionSetIsInvalid: true,
      acceptAnswerOnlyAfterCompleteRendering: true,
      requireResponseForEveryUnresolvedField: true,
      optionalFieldsMustAlsoBePresented: true,
      doNotPrintInteractionJson: true,
      doNotRenderTextFallbackWhenNativeAvailable: true,
      suggestedChoicesAlreadyMaterialized: true,
      suggestedChoicesUseStandardSingleSelect: true,
      suggestedChoicesMustUseHostOtherInput: true,
      optionalDisplayOnlyFieldsMayBeSkipped: true,
      explicitlyNonApplicableFieldsMayBeSkipped: true,
      nonApplicableEvidenceMustBeExplicit: true,
      optionalSensitiveFieldsMayBeSkipped: true,
      optionalSensitiveFieldsRemainBlank: true,
      protectedRegionFieldsMustNotBeAutoSkipped: true,
      textFallbackCondition: 'no_compatible_native_tool'
    },
    historyResolution: {
      mode: 'current_task_evidence_first',
      scope: 'current_task_only',
      sources: [
        'current_task_user_messages',
        'current_task_user_materials',
        'current_session_saved_answers',
        'current_task_explicit_corrections'
      ],
      forbiddenSources: currentTaskEvidencePolicy(interaction.sessionId || null).forbiddenSources,
      globalMemoryAllowed: false,
      memoryToolAllowed: false,
      crossTaskMemoryAllowed: false,
      otherConversationHistoryAllowed: false,
      userProfileMemoryAllowed: false,
      currentUserQueryMustNotBeExpandedWithMemory: true,
      reuseSavedAnswersOnlyForExactSessionId: true,
      resolveBeforePresenting: true,
      submitResolvedValues: true,
      presentUnresolvedOnly: true,
      requireExplicitUnambiguousSupport: true,
      latestExplicitCorrectionWins: true,
      silenceDoesNotMeanNegative: true,
      noMatchAction: 'present_question_to_user',
      forbidGuessing: true,
      forbidDefaultSelection: true,
      forbidFallbackOptionSelection: true,
      backendPreselectionIsNotEvidence: true,
      uncertaintyOptionRequiresExplicitUserChoice: true,
      presentOptionalWhenUnresolved: true,
      autoSkipOptionalFields: false,
      optionalDisplayOnlyAutoSkip: true,
      optionalDisplayOnlyRule: 'empty_name_used_only_for_report_display_is_not_a_blocking_question',
      optionalSensitiveAutoSkip: true,
      optionalSensitiveRule: 'empty_non_required_name_phone_or_identity_number_is_not_a_blocking_question',
      explicitNonApplicableAutoSkip: true,
      nonApplicableRule: 'only_current_task_explicit_category_exclusion_or_backend_flag',
      protectedRegionRule: '居住地和户籍地等地区字段即使非必填也必须保留',
      backendRequiredAffectsValidationOnly: true,
      uncertaintyLabels: ['不清楚', '不知道', '不确定', '不详', '未知', '无法判断', '无法确认', '其他'],
      autoSubmitOnlyWhen: 'explicit_direct_unambiguous_case_evidence'
    },
    answerPolicy: {
      mode: 'evidence_or_user_input_only',
      evidenceScope: 'current_task_only',
      // 判断依据是语义而非字面：案情说"老板"、选项写"用人单位"，
      // 说"拖欠5年"、选项写"超过三年"，都算命中。
      ...semanticAnswerPolicy(),
      onExactCurrentTaskEvidenceMatch: 'submit_matching_answer',
      onNoCurrentTaskEvidenceMatch: 'render_complete_question_and_wait_for_user',
      onConflictOrAmbiguity: 'render_complete_question_and_wait_for_user',
      globalMemoryMustNeverBecomeAnswer: true,
      crossTaskFactsMustNeverBecomeAnswer: true,
      oldExamplesMustNeverBecomeAnswer: true,
      neverChooseUnknownAsDefault: true,
      neverChooseAnyOptionToAdvanceWorkflow: true,
      userMustChooseWhenEvidenceMissing: true,
      optionalUnmatchedAction: 'render_complete_question_and_wait_for_user',
      explicitNonApplicableAction: 'preserve_blank_and_advance',
      allowBlankOptionalAnswer: false,
      allowAutomaticOptionalSkip: false,
      allowAutomaticOptionalSensitiveSkip: true,
      optionalSensitiveSkipOnlyWhen: 'empty_and_backend_required_is_false',
      allowAutomaticNonApplicableSkip: true,
      nonApplicableSkipOnlyWhen: 'explicit_current_task_exclusion_or_backend_flag',
      protectedRegionFieldsCannotBeSkipped: true,
      neverAutoSelectAiGeneratedChoice: true,
      aiGeneratedChoiceRequiresExplicitUserConfirmation: true,
      aiGeneratedChoiceMustMapToFieldType: true
    },
    question: primary?.label || interaction.title || '',
    choices,
    options: choices,
    optionCount: choices.length,
    choicesComplete: optionManifest.every(manifest => manifest.expectedOptionCount === manifest.options.length),
    optionManifest,
    sensitiveFieldPolicy: {
      mode: 'skip_empty_non_required_sensitive_fields',
      fields: ['姓名', '电话', '手机号', '身份证号', '证件号码'],
      protectedRegionFields: ['居住地', '户籍地', '实际居住地', '住所地'],
      repeatedGroupFieldsAreNeverAutoSkipped: true,
      userProvidedValueMustBePreserved: true
    },
    multiple: primary?.type === 'multi_select',
    inputSchema: {
      $schema: 'https://json-schema.org/draft/2020-12/schema',
      type: 'object',
      title: interaction.title || '',
      properties,
      required: fields.filter(field => field.responseRequired).map(field => field.key)
    },
    textFallback
  };
}

export function materializeInteractionChoices(interaction, contextText = '') {
  if (!interaction) return null;
  return withInteractionRendering(interaction, { suggestionContext: contextText });
}

export function normalizeQuestionNodes(nodes = [], options = {}) {
  const source = Array.isArray(nodes) ? nodes : nodes ? [nodes] : [];
  const fields = [];

  source.forEach((node, index) => {
    const key = nodeKey(node, `field-${index + 1}`);
    const type = fieldType(node);
    if (type === 'field_group') {
      const children = Array.isArray(node.children) ? node.children : [];
      children.forEach((child, childIndex) => {
        fields.push(normalizeSimpleNode(child, `${key}.${nodeKey(child, childIndex + 1)}`, options));
      });
    } else if (type === 'repeatable_group') {
      fields.push(normalizeRepeatableNode(node, key, options));
    } else {
      fields.push(normalizeSimpleNode(node, key, options));
    }
  });

  return withInteractionRendering({
    type: options.form ? 'form' : fields.length === 1 ? 'question' : 'form',
    title: options.title || (options.form ? '请填写计算信息' : '请回答以下问题'),
    description: options.description || '',
    fields,
    submitLabel: options.submitLabel || '确认并继续'
  });
}

function chooseOption(node, value, multi = false) {
  const children = Array.isArray(node.children) ? node.children : [];
  const values = multi ? (Array.isArray(value) ? value : String(value).split(/[，,、\s]+/)) : [value];
  const selectedIds = values.map(item => {
    const raw = String(item).trim();
    const numeric = Number.parseInt(raw, 10);
    const byLabel = children.find(option => optionLabel(option) === raw);
    if (byLabel) return optionValue(byLabel, children.indexOf(byLabel) + 1);
    if (/^\d+$/.test(raw) && Number.isInteger(numeric) && numeric >= 1 && numeric <= children.length) {
      return optionValue(children[numeric - 1], numeric);
    }
    const byId = children.find((option, index) => optionValue(option, index + 1) === raw);
    if (byId) return optionValue(byId, children.indexOf(byId) + 1);
    throw new SkillError('OPTION_NOT_FOUND', `没有找到选项“${raw}”`, {
      details: { options: children.map(optionLabel) }
    });
  });

  node.children = children.map(option => ({
    ...option,
    value: selectedIds.includes(optionValue(option, children.indexOf(option) + 1))
  }));
  node.value = multi ? selectedIds : selectedIds[0];
  node.edit = true;
}

// 取值形状由节点的 component 和 config 决定，必须带上节点本身，
// 只看归一化后的 type 会把日期写成字符串、把数值单位写成裸数字。
function coerceSimpleValue(node, type, value) {
  return coerceNodeValue(node, type, value);
}

function applySimple(node, value) {
  const type = fieldType(node);
  if (type === 'single_select') chooseOption(node, value, false);
  else if (type === 'multi_select') chooseOption(node, value, true);
  else {
    node.value = coerceSimpleValue(node, type, value);
    node.edit = true;
  }
  if ('msg' in node) node.msg = '';
  if ('errors' in node) node.errors = '';
}

export function applyAnswersToNodes(nodes = [], answers = {}) {
  const next = structuredClone(Array.isArray(nodes) ? nodes : [nodes]);
  let applied = 0;

  next.forEach((node, index) => {
    const key = nodeKey(node, `field-${index + 1}`);
    const type = fieldType(node);
    if (type === 'field_group') {
      (node.children || []).forEach((child, childIndex) => {
        const childKey = `${key}.${nodeKey(child, childIndex + 1)}`;
        if (Object.hasOwn(answers, childKey)) {
          applySimple(child, answers[childKey]);
          applied += 1;
        }
      });
    } else if (type === 'repeatable_group') {
      const rows = answers[key];
      if (Array.isArray(rows)) {
        (node.children || []).forEach((child, childIndex) => {
          const childKey = nodeKey(child, `${key}-field-${childIndex + 1}`);
          child.value = rows.map(row => row?.[childKey] ?? '');
          child.edit = true;
        });
        applied += 1;
      }
    } else if (Object.hasOwn(answers, key)) {
      applySimple(node, answers[key]);
      applied += 1;
    }
  });

  if (applied === 0) {
    throw new SkillError('NO_MATCHING_ANSWERS', '提交内容没有匹配到当前问题字段', {
      details: { expectedKeys: normalizeQuestionNodes(next).fields.map(field => field.key) }
    });
  }
  return next;
}

export function missingRequiredFields(interaction) {
  const missing = [];
  for (const field of interaction?.fields || []) {
    if (field.notApplicable) continue;
    if (field.type === 'repeatable_group') {
      field.rows.forEach((row, index) => {
        field.fields.filter(item => item.required && !item.notApplicable).forEach(item => {
          if (row[item.key] === undefined || row[item.key] === null || row[item.key] === '') {
            missing.push(`${field.label}${index + 1}：${item.label}`);
          }
        });
      });
    } else if (field.required && (field.value === undefined || field.value === null || field.value === '' || (Array.isArray(field.value) && field.value.length === 0))) {
      missing.push(field.label);
    }
  }
  return missing;
}

export function unresolvedInteraction(interaction) {
  if (!interaction) return null;
  const unresolved = unansweredFields(interaction);
  if (!unresolved.length) return null;
  const unresolvedKeys = new Set(unresolved.map(field => field.key));
  const visibleFields = (interaction.fields || []).filter(field => {
    if (field.notApplicable && isEmptyAnswer(field.value)) return false;
    if (field.displayOnly && isEmptyAnswer(field.value)) return false;
    if (field.skipIfOptionalSensitive && isEmptyAnswer(field.value)) return false;
    if (field.type === 'repeatable_group') {
      return unresolved.some(item => item.key.startsWith(`${field.key}[`));
    }
    return unresolvedKeys.has(field.key);
  });
  return withInteractionRendering({ ...interaction, fields: visibleFields });
}

export function nextUnresolvedInteraction(interaction) {
  const remaining = unresolvedInteraction(interaction);
  if (!remaining) return null;
  const fields = Array.isArray(remaining.fields) ? remaining.fields : [];
  if (fields.length <= 1) return remaining;

  const [field] = fields;
  return withInteractionRendering({
    ...remaining,
    fields: [field],
    sequence: {
      mode: 'one_field_per_turn',
      totalRemaining: fields.length,
      nextFieldKey: field.key
    }
  }, { forceAiChoice: true });
}

function isEmptyAnswer(value) {
  return value === undefined
    || value === null
    || (typeof value === 'string' && value.trim() === '')
    || (Array.isArray(value) && value.length === 0);
}

export function unansweredFields(interaction) {
  const unanswered = [];
  for (const field of interaction?.fields || []) {
    if (field.readonly) continue;
    if (field.notApplicable && isEmptyAnswer(field.value)) continue;
    if (field.displayOnly && isEmptyAnswer(field.value)) continue;
    if (field.skipIfOptionalSensitive && isEmptyAnswer(field.value)) continue;
    if (field.type === 'repeatable_group') {
      field.rows.forEach((row, index) => {
        field.fields.filter(item => !item.readonly && !(item.notApplicable && isEmptyAnswer(row[item.key]))).forEach(item => {
          if (isEmptyAnswer(row[item.key])) {
            unanswered.push({
              key: `${field.key}[${index}].${item.key}`,
              label: `${field.label}${index + 1}：${item.label}`,
              backendRequired: item.required,
              responseRequired: true
            });
          }
        });
      });
    } else if (isEmptyAnswer(field.value)) {
      unanswered.push({
        key: field.key,
        label: field.label,
        backendRequired: field.required,
        responseRequired: true
      });
    }
  }
  return unanswered;
}

// 用于工作流判断当前返回的题目是否可以在无人填写时直接提交空敏感字段，
// 以便继续请求后端下一题。一般的非必填字段不满足此条件，居住地/户籍地也不满足。
export function onlyAutoSkippableFieldsRemain(interaction) {
  const fields = Array.isArray(interaction?.fields) ? interaction.fields : [];
  if (!fields.length || unansweredFields(interaction).length > 0) return false;
  const emptySkippable = fields.some(field =>
    isEmptyAnswer(field.value) && (field.notApplicable || field.displayOnly || field.skipIfOptionalSensitive)
  );
  if (!emptySkippable) return false;
  return fields.every(field =>
    field.readonly
    || !isEmptyAnswer(field.value)
    || field.notApplicable
    || field.displayOnly
    || field.skipIfOptionalSensitive
  );
}

function parseAttributes(source = '') {
  const attributes = {};
  const pattern = /([:@\w-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
  for (const match of source.matchAll(pattern)) {
    attributes[match[1]] = match[2] ?? match[3] ?? match[4] ?? true;
  }
  return attributes;
}

function nearestText(html, index, expression, maxDistance = 1200) {
  const start = Math.max(0, index - maxDistance);
  const segment = html.slice(start, index);
  let value = '';
  for (const match of segment.matchAll(expression)) value = plainText(match[1]);
  return value;
}

function htmlInputType(tag, attributes) {
  if (tag === 'textarea') return 'textarea';
  if (tag === 'select') return attributes.multiple ? 'multi_select' : 'single_select';
  const type = String(attributes.type || 'text').toLowerCase();
  if (type === 'date') return 'date';
  if (type === 'number') return 'number';
  if (type === 'radio') return 'single_select';
  if (type === 'checkbox') return 'multi_select';
  return 'text';
}

function inferSection(label, key = '') {
  const text = plainText(`${label} ${key}`);
  if (/原告|被告|答辩人|第三人|申请人|当事人|代理人|plaintiff|defendant|respondent|third.?person|applicant|agent|defender|claimant|party|guardian/i.test(text)) return '当事人信息';
  if (/证据|材料|evidence|proof|witness|exhibit/i.test(text)) return '证据材料';
  if (/诉讼请求|答辩事项|答辩意见|请求事项|litigation.?request|claim|request|defen[cs]e|objection|opinion|petition/i.test(text)) return '诉讼请求或答辩意见';
  if (/法院|管辖|保全|送达|court|jurisdiction|venue|service|preservation/i.test(text)) return '法院、管辖与送达';
  if (/事实|理由|经过|争议|fact|reason|background|dispute|process/i.test(text)) return '事实与理由';
  return '其他信息';
}

export function extractPleadingFormSchema(html) {
  const modelCollections = new Map();
  for (const match of String(html).matchAll(/v-for\s*=\s*["']\(\s*(\w+)\s*,\s*\w+\s*\)\s+in\s+(\w+)["']/g)) {
    modelCollections.set(match[1], match[2]);
  }

  const fields = [];
  const seen = new Set();
  const controlPattern = /<input\b([^>]*)>|<(textarea|select)\b([^>]*)>([\s\S]*?)<\/\2>/gi;
  for (const match of String(html).matchAll(controlPattern)) {
    const tag = match[1] !== undefined ? 'input' : match[2].toLowerCase();
    const attrsSource = match[1] ?? match[3] ?? '';
    const body = match[4] ?? '';
    const attributes = parseAttributes(attrsSource);
    const inputType = String(attributes.type || '').toLowerCase();
    if (['hidden', 'submit', 'button', 'reset', 'file'].includes(inputType)) continue;

    const model = attributes['v-model'];
    let key = attributes.name;
    if (!key && model) {
      const [owner, ...rest] = String(model).split('.');
      key = modelCollections.has(owner)
        ? `${modelCollections.get(owner)}[].${rest.join('.')}`
        : String(model);
    }
    if (!key || seen.has(key)) continue;
    seen.add(key);

    const id = attributes.id || attributes[':id'];
    let label = '';
    if (id && !String(id).includes('+')) {
      const escaped = String(id).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const labelMatch = String(html).match(new RegExp(`<label[^>]*for=["']${escaped}["'][^>]*>([\\s\\S]*?)<\\/label>`, 'i'));
      if (labelMatch) label = plainText(labelMatch[1]);
    }
    label ||= nearestText(String(html), match.index, /<label[^>]*>([\s\S]*?)<\/label>/gi, 500);
    label ||= nearestText(String(html), match.index, /<td[^>]*>([\s\S]*?)<\/td>/gi, 1000);
    label ||= plainText(attributes.placeholder || key);

    const options = tag === 'select'
      ? [...body.matchAll(/<option\b([^>]*)>([\s\S]*?)<\/option>/gi)]
          .map(option => {
            const optionAttrs = parseAttributes(option[1]);
            return { value: String(optionAttrs.value ?? plainText(option[2])), label: plainText(option[2]) };
          })
          .filter(option => option.value || option.label)
      : [];
    const sectionHeading = nearestText(
      String(html),
      match.index,
      /<td[^>]*(?:colspan=["']?2["']?|font-bold)[^>]*>([\s\S]*?)<\/td>/gi,
      9000
    );

    fields.push({
      key: String(key),
      label,
      type: htmlInputType(tag, attributes),
      required: attributes.required === true || attributes.required === 'required',
      options,
      section: inferSection(`${sectionHeading} ${label}`, key),
      repeatable: String(key).includes('[]')
    });
  }

  const templateName = String(html).match(/window\.__TEMPLATE_NAME__\s*=\s*["']([^"']+)["']/)?.[1]
    || String(html).match(/const\s+currentTemplate\s*=\s*["']([^"']+)["']/)?.[1]
    || null;

  const grouped = {};
  for (const field of fields) {
    (grouped[field.section] ||= []).push(field);
  }

  return {
    templateName,
    fieldCount: fields.length,
    sections: Object.entries(grouped).map(([title, sectionFields]) => ({
      title,
      fields: sectionFields
    })),
    fields
  };
}

export function parseMaybeJson(value) {
  let current = value;
  for (let i = 0; i < 2 && typeof current === 'string'; i += 1) {
    try {
      current = JSON.parse(current);
    } catch {
      break;
    }
  }
  return current;
}
