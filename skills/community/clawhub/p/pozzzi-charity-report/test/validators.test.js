'use strict';

// -----------------------------------------------------------------------
// validators.test.js — 报告助手输入校验器测试
//
// 测试覆盖 Spec v1.0 验收标准：
//   F-04 数值一致性校验
//   F-05 必填字段
//   F-06 PII 检测
//   F-07 contact 不入 prompt（piiFields 标记）
//   F-11 完成率异常
//   F-12 差异标注
// -----------------------------------------------------------------------

const {
  validate,
  validateCommonInput,
  validateAnnualWorkInput,
  validateProjectFinalInput,
  validateFinanceFinalInput,
  validatePIISafety,
} = require('../src/validators');

// -----------------------------------------------------------------------
// 测试数据工厂函数
// -----------------------------------------------------------------------

/** 最小合法通用输入 */
function baseCommonInput(overrides = {}) {
  return {
    org_name: '广州市绿芽社会工作服务中心',
    org_registration_no: '44010220XXXX',
    org_type: '民办非企业单位',
    report_type: 'annual_work',
    report_year: 2025,
    contact_name: '李老师',
    ...overrides,
  };
}

/** 最小合法年度工作报告输入 */
function baseAnnualWorkInput(overrides = {}) {
  return {
    ...baseCommonInput({ report_type: 'annual_work' }),
    fiscal_year_start: '2025-01-01',
    fiscal_year_end: '2025-12-31',
    // 使命文本需在 50-200 字之间（以下为 58 字）
    org_mission: '为流动儿童提供课外辅导和心理支持，促进教育公平，帮助他们更好地融入城市生活，建设一个包容平等的社会环境。',
    total_income: 1000000,
    total_expenditure: 900000,
    income_breakdown: [
      { source: '腾讯公益', amount: 600000, type: 'grant' },
      { source: '个人捐赠', amount: 400000, type: 'donation' },
    ],
    projects_list: [
      { name: '阳光课堂2025', status: 'completed' },
    ],
    staff_fulltime: 6,
    ...overrides,
  };
}

/** 最小合法项目结项报告输入 */
function baseProjectFinalInput(overrides = {}) {
  return {
    ...baseCommonInput({ report_type: 'project_final' }),
    project_name: '阳光课堂2024-2025',
    funder_name: '腾讯公益慈善基金会',
    funder_platform: 'tencent',
    tencent_project_id: 'TXGY-2025-001',
    project_start_date: '2024-09-01',
    project_end_date: '2025-08-31',
    total_budget: 300000,
    actual_expenditure: 287600,
    expenditure_breakdown: [
      { category: '人力成本', budgeted: 120000, actual: 115000 },
    ],
    target_indicators: [
      { indicator: '累计服务儿童人次', planned: '2000人次', actual: '2400人次', completion_rate: 120 },
    ],
    activities_summary: [
      { name: '暑期读写营', date: '2025-07-01至07-14', description: '为留守儿童提供暑期阅读和写作训练，提升语文能力。' },
    ],
    challenges_and_response: '疫情影响场地，改为线上活动，参与率下降约 15%。',
    ...overrides,
  };
}

/** 最小合法财务决算报告输入
 *
 * 注意：默认使用小额结余（总额的 0.1%，不触发 balance_handling 必填）
 * 需要测试结余>1%场景时在 overrides 中覆盖相关字段
 */
function baseFinanceFinalInput(overrides = {}) {
  return {
    ...baseCommonInput({ report_type: 'finance_final' }),
    project_name: '阳光课堂2024-2025',
    funder_name: '腾讯公益慈善基金会',
    audit_required: false,
    total_grant: 300000,
    total_expenditure: 299700, // 结余 300 元（0.1%），不触发 balance_handling 必填
    unexpended_balance: 300,
    expenditure_detail: [
      { category: '人力成本', amount: 150000 },
    ],
    ...overrides,
  };
}

// -----------------------------------------------------------------------
// validateCommonInput
// -----------------------------------------------------------------------

describe('validateCommonInput', () => {
  test('合法输入返回 valid=true', () => {
    const result = validateCommonInput(baseCommonInput());
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  // F-05: 缺失 org_name → error
  test('F-05 缺失 org_name 返回 error', () => {
    const result = validateCommonInput(baseCommonInput({ org_name: '' }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('org_name'))).toBe(true);
  });

  test('F-05 org_name 为纯空格返回 error', () => {
    const result = validateCommonInput(baseCommonInput({ org_name: '   ' }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('org_name'))).toBe(true);
  });

  // F-05: 缺失 report_type → error
  test('F-05 缺失 report_type 返回 error', () => {
    const input = baseCommonInput();
    delete input.report_type;
    const result = validateCommonInput(input);
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('report_type'))).toBe(true);
  });

  test('无效 report_type 返回 error', () => {
    const result = validateCommonInput(baseCommonInput({ report_type: 'invalid_type' }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('report_type'))).toBe(true);
  });

  test('缺失 org_registration_no 返回 error', () => {
    const result = validateCommonInput(baseCommonInput({ org_registration_no: '' }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('org_registration_no'))).toBe(true);
  });

  test('无效 org_type 返回 error', () => {
    const result = validateCommonInput(baseCommonInput({ org_type: '非法组织类型' }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('org_type'))).toBe(true);
  });

  test('report_year 小于 2000 返回 error', () => {
    const result = validateCommonInput(baseCommonInput({ report_year: 1999 }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('report_year'))).toBe(true);
  });

  test('report_year 超过当前年份+1 返回 error', () => {
    const futureYear = new Date().getFullYear() + 2;
    const result = validateCommonInput(baseCommonInput({ report_year: futureYear }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('report_year'))).toBe(true);
  });

  test('report_year 等于当前年份+1 允许通过', () => {
    const nextYear = new Date().getFullYear() + 1;
    const result = validateCommonInput(baseCommonInput({ report_year: nextYear }));
    expect(result.valid).toBe(true);
  });

  test('缺失 contact_name 返回 error', () => {
    const result = validateCommonInput(baseCommonInput({ contact_name: '' }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('contact_name'))).toBe(true);
  });

  test('输入为 null 返回 valid=false', () => {
    const result = validateCommonInput(null);
    expect(result.valid).toBe(false);
  });
});

// -----------------------------------------------------------------------
// validateAnnualWorkInput
// -----------------------------------------------------------------------

describe('validateAnnualWorkInput', () => {
  test('合法年度工作报告输入返回 valid=true', () => {
    const result = validateAnnualWorkInput(baseAnnualWorkInput());
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('fiscal_year_end <= fiscal_year_start 返回 error', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({
        fiscal_year_start: '2025-12-31',
        fiscal_year_end: '2025-01-01',
      }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('fiscal_year_end'))).toBe(true);
  });

  test('org_mission 少于 50 字返回 error', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({ org_mission: '短使命文本' }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('org_mission'))).toBe(true);
  });

  test('org_mission 超过 200 字返回 error', () => {
    const longText = '为'.repeat(201);
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({ org_mission: longText }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('org_mission'))).toBe(true);
  });

  test('total_income 为负数返回 error', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({ total_income: -1 }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('total_income'))).toBe(true);
  });

  // F-04: income_breakdown 总和与 total_income 差异 > 100 元 → error
  test('F-04 income_breakdown 总和与 total_income 差异 > 100 元返回 error', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({
        total_income: 1000000,
        income_breakdown: [
          { source: '腾讯公益', amount: 600000, type: 'grant' },
          { source: '个人捐赠', amount: 399800, type: 'donation' }, // 差 200 元
        ],
      }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('income_breakdown'))).toBe(true);
  });

  test('F-04 income_breakdown 总和与 total_income 差异恰好 100 元允许通过', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({
        total_income: 1000000,
        income_breakdown: [
          { source: '腾讯公益', amount: 600000, type: 'grant' },
          { source: '个人捐赠', amount: 399900, type: 'donation' }, // 差 100 元，在容差内
        ],
      }),
    );
    expect(result.valid).toBe(true);
  });

  test('F-04 income_breakdown 总和与 total_income 完全一致允许通过', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({
        total_income: 1000000,
        income_breakdown: [
          { source: '腾讯公益', amount: 600000, type: 'grant' },
          { source: '个人捐赠', amount: 400000, type: 'donation' },
        ],
      }),
    );
    expect(result.valid).toBe(true);
  });

  test('projects_list 为空数组返回 error', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({ projects_list: [] }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('projects_list'))).toBe(true);
  });

  test('staff_fulltime 为负数返回 error', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({ staff_fulltime: -1 }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('staff_fulltime'))).toBe(true);
  });

  test('staff_fulltime 为 0 允许通过', () => {
    const result = validateAnnualWorkInput(
      baseAnnualWorkInput({ staff_fulltime: 0 }),
    );
    expect(result.valid).toBe(true);
  });
});

// -----------------------------------------------------------------------
// validateProjectFinalInput
// -----------------------------------------------------------------------

describe('validateProjectFinalInput', () => {
  test('合法项目结项报告输入返回 valid=true', () => {
    const result = validateProjectFinalInput(baseProjectFinalInput());
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  // F-05: project_final 缺失 project_name → error
  test('F-05 缺失 project_name 返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({ project_name: '' }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('project_name'))).toBe(true);
  });

  test('缺失 funder_name 返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({ funder_name: '' }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('funder_name'))).toBe(true);
  });

  test('无效 funder_platform 返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({ funder_platform: 'unknown' }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('funder_platform'))).toBe(true);
  });

  test('project_end_date <= project_start_date 返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({
        project_start_date: '2025-08-31',
        project_end_date: '2024-09-01',
      }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('project_end_date'))).toBe(true);
  });

  // F-12: expenditure_breakdown 中 actual/budgeted 差异 15% 且无 variance_reason → error
  test('F-12 支出差异 15% 且无 variance_reason 返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({
        expenditure_breakdown: [
          { category: '人力成本', budgeted: 120000, actual: 138000 }, // 差 15%，无 variance_reason
        ],
      }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('variance_reason'))).toBe(true);
  });

  // F-12: 差异 15% 但有 variance_reason → 允许通过
  test('F-12 支出差异 15% 但有 variance_reason 允许通过', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({
        expenditure_breakdown: [
          {
            category: '人力成本',
            budgeted: 120000,
            actual: 138000,
            variance_reason: '因扩大服务规模增加兼职人员',
          },
        ],
      }),
    );
    expect(result.valid).toBe(true);
  });

  // F-12: 差异 5% 且无 variance_reason → 无 error（在阈值内）
  test('F-12 支出差异 5% 且无 variance_reason 不返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({
        expenditure_breakdown: [
          { category: '人力成本', budgeted: 120000, actual: 126000 }, // 差 5%，无 variance_reason
        ],
      }),
    );
    expect(result.valid).toBe(true);
    expect(result.errors.some(e => e.includes('variance_reason'))).toBe(false);
  });

  test('F-12 支出差异恰好 10% 且无 variance_reason 不返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({
        expenditure_breakdown: [
          { category: '人力成本', budgeted: 120000, actual: 132000 }, // 差恰好 10%，不超过
        ],
      }),
    );
    expect(result.valid).toBe(true);
    expect(result.errors.some(e => e.includes('variance_reason'))).toBe(false);
  });

  // F-11: completion_rate = 160 → warning（不阻断）
  test('F-11 completion_rate=160 返回 warning 但 valid=true', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({
        target_indicators: [
          {
            indicator: '服务人次',
            planned: '1000人次',
            actual: '1600人次',
            completion_rate: 160,
          },
        ],
      }),
    );
    expect(result.valid).toBe(true); // warning 不阻断
    expect(result.warnings.some(w => w.includes('160'))).toBe(true);
  });

  test('F-11 completion_rate=150 不触发 warning', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({
        target_indicators: [
          {
            indicator: '服务人次',
            planned: '1000人次',
            actual: '1500人次',
            completion_rate: 150,
          },
        ],
      }),
    );
    expect(result.warnings.some(w => w.includes('completion_rate') || w.includes('%'))).toBe(false);
  });

  // 腾讯公益：tencent_project_id 必填且格式正确
  test('funder_platform=tencent 时 tencent_project_id 缺失返回 error', () => {
    const input = baseProjectFinalInput({ funder_platform: 'tencent' });
    delete input.tencent_project_id;
    const result = validateProjectFinalInput(input);
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('tencent_project_id'))).toBe(true);
  });

  test('tencent_project_id 格式错误返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({ tencent_project_id: 'TX-2025-001' }), // 格式不符
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('tencent_project_id'))).toBe(true);
  });

  test('tencent_project_id 格式 TXGY-YYYY-XXX 通过校验', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({ tencent_project_id: 'TXGY-2025-001' }),
    );
    expect(result.valid).toBe(true);
  });

  test('funder_platform=generic 时不校验 tencent_project_id', () => {
    const input = baseProjectFinalInput({ funder_platform: 'generic' });
    delete input.tencent_project_id;
    const result = validateProjectFinalInput(input);
    expect(result.valid).toBe(true);
  });

  test('activities_summary 为空数组返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({ activities_summary: [] }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('activities_summary'))).toBe(true);
  });

  test('缺失 challenges_and_response 返回 error', () => {
    const result = validateProjectFinalInput(
      baseProjectFinalInput({ challenges_and_response: '' }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('challenges_and_response'))).toBe(true);
  });
});

// -----------------------------------------------------------------------
// validateFinanceFinalInput
// -----------------------------------------------------------------------

describe('validateFinanceFinalInput', () => {
  test('合法财务决算报告输入返回 valid=true', () => {
    const result = validateFinanceFinalInput(baseFinanceFinalInput());
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  // F-04: unexpended_balance !== total_grant - total_expenditure → error
  test('F-04 unexpended_balance 与计算值不一致返回 error', () => {
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({
        total_grant: 300000,
        total_expenditure: 287600,
        unexpended_balance: 99999, // 应为 12400
      }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('unexpended_balance'))).toBe(true);
  });

  test('F-04 unexpended_balance 与计算值精确一致允许通过', () => {
    // 结余 12400 元（4.1%），需同时提供 balance_handling 才能通过
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({
        total_grant: 300000,
        total_expenditure: 287600,
        unexpended_balance: 12400,
        balance_handling: 'return',
      }),
    );
    expect(result.valid).toBe(true);
  });

  test('结余超过总额 1% 时 balance_handling 缺失返回 error', () => {
    // 12400/300000 ≈ 4.1%，超过 1%
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({
        total_grant: 300000,
        total_expenditure: 287600,
        unexpended_balance: 12400,
        balance_handling: undefined,
      }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('balance_handling'))).toBe(true);
  });

  test('结余超过 1% 且提供合法 balance_handling 允许通过', () => {
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({
        total_grant: 300000,
        total_expenditure: 287600,
        unexpended_balance: 12400,
        balance_handling: 'return',
      }),
    );
    expect(result.valid).toBe(true);
  });

  test('结余不超过 1% 时 balance_handling 可不填', () => {
    // 结余 300 元 / 300000 = 0.1%，不超过 1%
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({
        total_grant: 300000,
        total_expenditure: 299700,
        unexpended_balance: 300,
        balance_handling: undefined,
      }),
    );
    expect(result.valid).toBe(true);
  });

  test('audit_required=true 时 audit_firm 缺失返回 error', () => {
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({ audit_required: true, audit_firm: '' }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('audit_firm'))).toBe(true);
  });

  test('audit_required=true 且提供 audit_firm 允许通过', () => {
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({
        audit_required: true,
        audit_firm: '广州XX会计师事务所',
        // 结余 12400 需要 balance_handling
        balance_handling: 'return',
      }),
    );
    expect(result.valid).toBe(true);
  });

  test('audit_required=false 时 audit_firm 可不填', () => {
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({ audit_required: false }),
    );
    expect(result.valid).toBe(true);
  });

  test('expenditure_detail 为空数组返回 error', () => {
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({ expenditure_detail: [] }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('expenditure_detail'))).toBe(true);
  });

  test('缺失 project_name 返回 error', () => {
    const result = validateFinanceFinalInput(
      baseFinanceFinalInput({ project_name: '' }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('project_name'))).toBe(true);
  });
});

// -----------------------------------------------------------------------
// validatePIISafety
// -----------------------------------------------------------------------

describe('validatePIISafety', () => {
  // F-07: piiFields 必须包含 contact_name 和 contact_phone
  test('F-07 piiFields 始终包含 contact_name 和 contact_phone', () => {
    const result = validatePIISafety({});
    expect(result.piiFields).toContain('contact_name');
    expect(result.piiFields).toContain('contact_phone');
  });

  test('F-07 piiFields 在任意输入下均包含 contact_name 和 contact_phone', () => {
    const result = validatePIISafety(baseAnnualWorkInput());
    expect(result.piiFields).toContain('contact_name');
    expect(result.piiFields).toContain('contact_phone');
  });

  // F-06: story_case 含"张三是一个..." → warning
  test('F-06 story_case 含疑似真实姓名返回 warning', () => {
    const result = validatePIISafety({
      story_case: '张三是一个来自河南的流动儿童，家庭困难。',
    });
    expect(result.warnings.length).toBeGreaterThan(0);
    expect(result.warnings[0]).toMatch(/疑似真实姓名/);
  });

  // F-06: story_case 含"小明（化名）..." → 无 warning（化名标注已排除）
  test('F-06 story_case 含化名标注（全角括号）不触发 warning', () => {
    const result = validatePIISafety({
      story_case: '小明（化名）是一个来自河南的流动儿童，每天放学后参加课堂辅导。',
    });
    expect(result.warnings).toHaveLength(0);
  });

  test('F-06 story_case 含化名标注（半角括号）不触发 warning', () => {
    const result = validatePIISafety({
      story_case: '小红(化名)是本次活动中进步最大的学员。',
    });
    expect(result.warnings).toHaveLength(0);
  });

  test('story_case 为空时不触发 warning', () => {
    const result = validatePIISafety({ story_case: '' });
    expect(result.warnings).toHaveLength(0);
  });

  test('无 story_case 字段时不触发 warning', () => {
    const result = validatePIISafety({ org_name: '测试组织' });
    expect(result.warnings).toHaveLength(0);
  });

  test('null 输入安全处理，返回 piiFields 不抛出异常', () => {
    expect(() => validatePIISafety(null)).not.toThrow();
    const result = validatePIISafety(null);
    expect(result.piiFields).toContain('contact_name');
  });

  test('F-06 story_case 为数组时 case_title 中的姓名触发 warning', () => {
    const result = validatePIISafety({
      story_case: [{ case_title: '张三是受益学生', case_description: '来自贫困家庭' }],
    });
    expect(result.warnings.some(w => w.includes('疑似真实姓名'))).toBe(true);
  });

  test('F-06 story_case 数组含化名标注不触发 warning', () => {
    const result = validatePIISafety({
      story_case: [{ case_title: '小明（化名）是受益学生', case_description: '' }],
    });
    expect(result.warnings).toHaveLength(0);
  });

  test('F-06 story_case 数组多条记录只要有一条含姓名即触发', () => {
    const result = validatePIISafety({
      story_case: [
        { case_title: '小红（化名）的故事', case_description: '表现很好' },
        { case_title: '李四是志愿者', case_description: '帮助很多人' },
      ],
    });
    expect(result.warnings.some(w => w.includes('疑似真实姓名'))).toBe(true);
  });
});

// -----------------------------------------------------------------------
// validate（总入口）
// -----------------------------------------------------------------------

describe('validate（总入口）', () => {
  test('合法年度工作报告返回 valid=true', () => {
    const result = validate(baseAnnualWorkInput());
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('合法项目结项报告返回 valid=true', () => {
    const result = validate(baseProjectFinalInput());
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('合法财务决算报告（含结余>1%）返回 valid=true', () => {
    const result = validate(baseFinanceFinalInput({ balance_handling: 'return' }));
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  test('F-05 缺失 org_name 通过总入口返回 error', () => {
    const result = validate(baseAnnualWorkInput({ org_name: '' }));
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('org_name'))).toBe(true);
  });

  test('F-04 annual_work income_breakdown 差异 > 100 通过总入口返回 error', () => {
    const result = validate(
      baseAnnualWorkInput({
        total_income: 1000000,
        income_breakdown: [
          { source: '腾讯公益', amount: 999798, type: 'grant' }, // 差 202 元
        ],
      }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('income_breakdown'))).toBe(true);
  });

  test('F-04 finance_final unexpended_balance 不等于 total_grant - total_expenditure 通过总入口返回 error', () => {
    const result = validate(
      baseFinanceFinalInput({
        total_grant: 300000,
        total_expenditure: 287600,
        unexpended_balance: 10000, // 应为 12400
        balance_handling: 'return',
      }),
    );
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('unexpended_balance'))).toBe(true);
  });

  test('F-06 PII warning 通过总入口汇总到 result.warnings', () => {
    const result = validate(
      baseProjectFinalInput({
        story_case: '王芳是一个来自山区的受助学生。',
      }),
    );
    // PII warning 不影响 valid（假设其他字段合法）
    expect(result.warnings.some(w => w.includes('疑似真实姓名'))).toBe(true);
  });

  test('F-11 completion_rate warning 通过总入口汇总到 result.warnings', () => {
    const result = validate(
      baseProjectFinalInput({
        target_indicators: [
          {
            indicator: '服务人次',
            planned: '1000人次',
            actual: '1600人次',
            completion_rate: 160,
          },
        ],
      }),
    );
    expect(result.valid).toBe(true);
    expect(result.warnings.some(w => w.includes('160'))).toBe(true);
  });

  test('无效 report_type 时跳过专项校验，仅返回 common error', () => {
    const result = validate({
      ...baseCommonInput({ report_type: 'bad_type' }),
    });
    expect(result.valid).toBe(false);
    expect(result.errors.some(e => e.includes('report_type'))).toBe(true);
  });

  test('null 输入不抛出异常', () => {
    expect(() => validate(null)).not.toThrow();
    const result = validate(null);
    expect(result.valid).toBe(false);
  });
});
