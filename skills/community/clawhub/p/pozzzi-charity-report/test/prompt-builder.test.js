'use strict';

const {
  buildPrompt,
  buildSystemPrompt,
  buildUserPrompt,
  loadTemplate,
  formatCurrency,
} = require('../src/prompt-builder');

// ---------------------------------------------------------------------------
// 测试数据
// ---------------------------------------------------------------------------

const BASE_INPUT = {
  org_name: '示例公益中心',
  org_registration_no: '5110000000001',
  org_type: '民办非企业单位',
  report_year: 2025,
  contact_name: '张三',
  contact_phone: '13800138000',
};

const ANNUAL_WORK_INPUT = {
  ...BASE_INPUT,
  report_type: 'annual_work',
  fiscal_year_start: '2025-01-01',
  fiscal_year_end: '2025-12-31',
  org_mission: '致力于改善贫困山区儿童的教育条件，通过助学金、图书室建设和支教项目覆盖更多受益群体。',
  total_income: 1580000,
  total_expenditure: 1200000,
  income_breakdown: [{ type: '公众募款', amount: 1580000 }],
  projects_list: [{ project_name: '山区图书室建设', status: '已结项' }],
  staff_fulltime: 5,
};

const PROJECT_FINAL_TENCENT_INPUT = {
  ...BASE_INPUT,
  report_type: 'project_final',
  funder_platform: 'tencent',
  tencent_project_id: 'TXGY-2025-001',
  project_name: '山区儿童助学项目',
  funder_name: '腾讯公益基金会',
  project_start_date: '2025-01-01',
  project_end_date: '2025-12-31',
  total_budget: 500000,
  actual_expenditure: 487600.5,
  expenditure_breakdown: [{ category: '助学金', budgeted: 500000, actual: 487600.5 }],
  target_indicators: [{ indicator: '受助学生数', completion_rate: 98 }],
  activities_summary: [{ activity: '发放助学金' }],
  challenges_and_response: '疫情影响部分活动推迟，通过线上方式完成。',
};

const FINANCE_FINAL_INPUT = {
  ...BASE_INPUT,
  report_type: 'finance_final',
  project_name: '助学项目2025',
  funder_name: '某基金会',
  total_grant: 300000,
  total_expenditure: 287600,
  unexpended_balance: 12400,
  balance_handling: 'return',
  audit_required: false,
  expenditure_detail: [{ category: '助学金', amount: 287600 }],
};

// ---------------------------------------------------------------------------
// 1. 模板加载
// ---------------------------------------------------------------------------
describe('模板加载', () => {
  test('annual_work 加载 annual-work-v1.md', () => {
    const result = loadTemplate('annual_work');
    expect(result.metadata).toBeTruthy();
    expect(result.content).toBeTruthy();
    expect(result.content).toContain('年度工作');
  });

  test('project_final + tencent 加载腾讯公益模板', () => {
    const result = loadTemplate('project_final', 'tencent');
    expect(result.metadata).toBeTruthy();
    expect(result.content).toContain('腾讯');
  });

  test('project_final + generic 加载通用模板', () => {
    const result = loadTemplate('project_final', 'generic');
    expect(result.metadata).toBeTruthy();
    expect(result.content.includes('腾讯公益')).toBe(false);
  });

  test('project_final + yijia 也加载通用模板', () => {
    const result = loadTemplate('project_final', 'yijia');
    expect(result.metadata.funder_platform).toBe('generic');
  });

  test('finance_final 加载财务决算模板', () => {
    const result = loadTemplate('finance_final');
    expect(result.metadata).toBeTruthy();
    expect(result.content).toMatch(/决算|财务/);
  });

  test('模板 metadata 包含 version 和 report_type', () => {
    const result = loadTemplate('annual_work');
    expect(result.metadata).toHaveProperty('version');
    expect(result.metadata.report_type).toBe('annual_work');
  });

  test('未知 reportType 抛出错误', () => {
    expect(() => loadTemplate('unknown_type')).toThrow(/未知报告类型/);
  });
});

// ---------------------------------------------------------------------------
// 2. F-07: contact 字段不在 prompt 中
// ---------------------------------------------------------------------------
describe('F-07: contact 不入 prompt', () => {
  const piiFields = ['contact_name', 'contact_phone'];

  test('buildUserPrompt 不含 contact_name 的值', () => {
    const template = loadTemplate('annual_work');
    const result = buildUserPrompt(ANNUAL_WORK_INPUT, template.content, piiFields, 'hunyuan');
    expect(result).not.toContain('张三');
  });

  test('buildUserPrompt 不含 contact_phone 的值', () => {
    const template = loadTemplate('annual_work');
    const result = buildUserPrompt(ANNUAL_WORK_INPUT, template.content, piiFields, 'hunyuan');
    expect(result).not.toContain('13800138000');
  });

  test('其他字段（org_name）正常出现', () => {
    const template = loadTemplate('annual_work');
    const result = buildUserPrompt(ANNUAL_WORK_INPUT, template.content, piiFields, 'hunyuan');
    expect(result).toContain('示例公益中心');
  });

  test('piiFields 为空时，contact 字段仍因硬编码防御被排除', () => {
    const template = loadTemplate('annual_work');
    const result = buildUserPrompt(ANNUAL_WORK_INPUT, template.content, [], 'hunyuan');
    expect(result).not.toContain('张三');
    expect(result).not.toContain('13800138000');
  });

  test('piiFields 中额外字段也被排除', () => {
    const template = loadTemplate('annual_work');
    const result = buildUserPrompt(ANNUAL_WORK_INPUT, template.content, [...piiFields, 'org_registration_no'], 'hunyuan');
    expect(result).not.toContain('5110000000001');
  });

  test('内部字段 _regenerate_section 不出现在 prompt 中', () => {
    const template = loadTemplate('annual_work');
    const inputWithInternal = { ...ANNUAL_WORK_INPUT, _regenerate_section: '年度工作概述' };
    const result = buildUserPrompt(inputWithInternal, template.content, piiFields, 'hunyuan');
    expect(result).not.toContain('_regenerate_section');
  });
});

// ---------------------------------------------------------------------------
// 3. F-15: 数值格式化
// ---------------------------------------------------------------------------
describe('F-15: 数值格式化', () => {
  test('1580000 → "1,580,000元"', () => {
    expect(formatCurrency(1580000)).toBe('1,580,000元');
  });

  test('0 → "0元"', () => {
    expect(formatCurrency(0)).toBe('0元');
  });

  test('287600.5 保留两位小数', () => {
    expect(formatCurrency(287600.5)).toBe('287,600.50元');
  });

  test('1000 → "1,000元"', () => {
    expect(formatCurrency(1000)).toBe('1,000元');
  });

  test('999 无逗号', () => {
    expect(formatCurrency(999)).toBe('999元');
  });

  test('12345.67 → "12,345.67元"', () => {
    expect(formatCurrency(12345.67)).toBe('12,345.67元');
  });

  test('100.00 视为整数', () => {
    expect(formatCurrency(100.00)).toBe('100元');
  });

  test('Infinity 返回占位符', () => {
    expect(formatCurrency(Infinity)).toBe('[请填写实际金额]');
  });

  test('-Infinity 返回占位符', () => {
    expect(formatCurrency(-Infinity)).toBe('[请填写实际金额]');
  });

  test('NaN 返回占位符', () => {
    expect(formatCurrency(NaN)).toBe('[请填写实际金额]');
  });
});

// ---------------------------------------------------------------------------
// 4. 模型差异 prompt
// ---------------------------------------------------------------------------
describe('模型差异 prompt', () => {
  test('hunyuan 含"政府公文用语"', () => {
    expect(buildSystemPrompt('annual_work', 'hunyuan')).toContain('政府公文用语');
  });

  test('deepseek 含"仅输出报告正文"', () => {
    expect(buildSystemPrompt('annual_work', 'deepseek')).toContain('仅输出报告正文');
  });

  test('deepseek user prompt 使用 XML 标签', () => {
    const template = loadTemplate('annual_work');
    const result = buildUserPrompt(ANNUAL_WORK_INPUT, template.content, ['contact_name', 'contact_phone'], 'deepseek');
    expect(result).toContain('<data>');
    expect(result).toContain('</data>');
    expect(result).toContain('<instruction>');
  });

  test('doubao 含"温暖、有人情味"', () => {
    expect(buildSystemPrompt('annual_work', 'doubao')).toContain('温暖、有人情味');
  });

  test('doubao 含 Markdown 格式指令', () => {
    expect(buildSystemPrompt('annual_work', 'doubao')).toContain('请用Markdown格式输出');
  });

  test('hunyuan user prompt 不使用 XML 标签', () => {
    const template = loadTemplate('annual_work');
    const result = buildUserPrompt(ANNUAL_WORK_INPUT, template.content, ['contact_name', 'contact_phone'], 'hunyuan');
    expect(result).not.toContain('<data>');
  });

  test('默认模型使用 hunyuan 策略', () => {
    expect(buildSystemPrompt('annual_work')).toContain('政府公文用语');
  });
});

// ---------------------------------------------------------------------------
// 5. buildPrompt 集成
// ---------------------------------------------------------------------------
describe('buildPrompt 集成', () => {
  test('返回正确的 messages 数组', () => {
    const messages = buildPrompt(ANNUAL_WORK_INPUT, 'hunyuan');
    expect(Array.isArray(messages)).toBe(true);
    expect(messages).toHaveLength(2);
    expect(messages[0].role).toBe('system');
    expect(messages[1].role).toBe('user');
  });

  test('user content 不含 contact_name/phone', () => {
    const messages = buildPrompt(ANNUAL_WORK_INPUT, 'hunyuan');
    expect(messages[1].content).not.toContain('张三');
    expect(messages[1].content).not.toContain('13800138000');
  });

  test('finance_final + deepseek 正常组装', () => {
    const messages = buildPrompt(FINANCE_FINAL_INPUT, 'deepseek');
    expect(messages[1].content).toContain('<data>');
    expect(messages[1].content).not.toContain('张三');
  });

  test('腾讯公益 + doubao 正常组装', () => {
    const messages = buildPrompt(PROJECT_FINAL_TENCENT_INPUT, 'doubao');
    expect(messages).toHaveLength(2);
    expect(messages[1].content).not.toContain('13800138000');
  });

  test('货币字段在 hunyuan prompt 中被格式化', () => {
    const template = loadTemplate('annual_work');
    const result = buildUserPrompt(ANNUAL_WORK_INPUT, template.content, ['contact_name', 'contact_phone'], 'hunyuan');
    expect(result).toContain('1,580,000元');
  });
});
