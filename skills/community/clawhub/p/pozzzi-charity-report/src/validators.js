'use strict';

// -----------------------------------------------------------------------
// validators.js — 报告助手输入校验器
//
// 依赖：仅 Node.js 内置模块
// 合规依据：噗滋慈善 Spec v1.0 + PIPL 第23/28条 + 慈善法第75/77条
// -----------------------------------------------------------------------

/**
 * 合并两个校验结果对象（将 src 的 errors/warnings 追加到 dest）
 * @param {{ errors: string[], warnings: string[] }} dest
 * @param {{ errors: string[], warnings: string[] }} src
 */
function mergeResult(dest, src) {
  dest.errors.push(...src.errors);
  dest.warnings.push(...src.warnings);
}

/**
 * 解析日期字符串并返回 Date 对象；无效则返回 null
 * @param {string} str
 * @returns {Date|null}
 */
function parseDate(str) {
  if (typeof str !== 'string' || !str.trim()) return null;
  const d = new Date(str);
  return isNaN(d.getTime()) ? null : d;
}

// -----------------------------------------------------------------------
// 1. 通用输入校验
// -----------------------------------------------------------------------

/**
 * 校验所有报告类型共用的必填字段。
 *
 * PII 安全注释：contact_name / contact_phone 在此仅做非空校验，
 * 不进入 Prompt，由 validatePIISafety 负责标记和排除。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateCommonInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // org_name — 非空字符串
  if (!input.org_name || typeof input.org_name !== 'string' || !input.org_name.trim()) {
    errors.push('org_name 为必填字段，不能为空');
  }

  // org_registration_no — 非空字符串
  if (
    !input.org_registration_no ||
    typeof input.org_registration_no !== 'string' ||
    !input.org_registration_no.trim()
  ) {
    errors.push('org_registration_no 为必填字段，不能为空');
  }

  // org_type — enum
  const validOrgTypes = ['社会团体', '民办非企业单位', '基金会'];
  if (!input.org_type) {
    errors.push('org_type 为必填字段');
  } else if (!validOrgTypes.includes(input.org_type)) {
    errors.push(
      `org_type 值无效："${input.org_type}"，有效值为：${validOrgTypes.join('/')}`,
    );
  }

  // report_type — enum
  const validReportTypes = ['annual_work', 'project_final', 'finance_final'];
  if (!input.report_type) {
    errors.push('report_type 为必填字段');
  } else if (!validReportTypes.includes(input.report_type)) {
    errors.push(
      `report_type 值无效："${input.report_type}"，有效值为：${validReportTypes.join('/')}`,
    );
  }

  // report_year — 整数，[2000, 当前年份+1]
  const currentYear = new Date().getFullYear();
  if (input.report_year === undefined || input.report_year === null) {
    errors.push('report_year 为必填字段');
  } else {
    const year = Number(input.report_year);
    if (!Number.isInteger(year)) {
      errors.push('report_year 必须是整数');
    } else if (year < 2000) {
      errors.push(`report_year 不能早于 2000，当前值：${year}`);
    } else if (year > currentYear + 1) {
      errors.push(`report_year 不能超过 ${currentYear + 1}，当前值：${year}`);
    }
  }

  // contact_name — 必填（PII，仅存本地日志，不进模型）
  if (
    !input.contact_name ||
    typeof input.contact_name !== 'string' ||
    !input.contact_name.trim()
  ) {
    errors.push('contact_name 为必填字段，不能为空');
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 2. 年度工作报告专用校验
// -----------------------------------------------------------------------

/**
 * 年度工作报告专用字段校验。应在 validateCommonInput 通过后调用。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateAnnualWorkInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // fiscal_year_start / fiscal_year_end
  const startDate = parseDate(input.fiscal_year_start);
  const endDate = parseDate(input.fiscal_year_end);

  if (!startDate) {
    errors.push('fiscal_year_start 为必填字段，格式应为 YYYY-MM-DD');
  }
  if (!endDate) {
    errors.push('fiscal_year_end 为必填字段，格式应为 YYYY-MM-DD');
  }
  if (startDate && endDate && endDate <= startDate) {
    errors.push('fiscal_year_end 必须晚于 fiscal_year_start');
  }

  // org_mission — 50-200 字
  if (!input.org_mission || typeof input.org_mission !== 'string' || !input.org_mission.trim()) {
    errors.push('org_mission 为必填字段，不能为空');
  } else {
    const missionLen = input.org_mission.trim().length;
    if (missionLen < 50) {
      errors.push(`org_mission 不能少于 50 个字符，当前：${missionLen} 个字符`);
    } else if (missionLen > 200) {
      errors.push(`org_mission 不能超过 200 个字符，当前：${missionLen} 个字符`);
    }
  }

  // total_income — number >= 0
  if (input.total_income === undefined || input.total_income === null) {
    errors.push('total_income 为必填字段');
  } else if (typeof input.total_income !== 'number' || input.total_income < 0) {
    errors.push('total_income 必须是大于等于 0 的数值');
  }

  // total_expenditure — number >= 0
  if (input.total_expenditure === undefined || input.total_expenditure === null) {
    errors.push('total_expenditure 为必填字段');
  } else if (typeof input.total_expenditure !== 'number' || input.total_expenditure < 0) {
    errors.push('total_expenditure 必须是大于等于 0 的数值');
  }

  // income_breakdown — 非空数组
  if (!Array.isArray(input.income_breakdown) || input.income_breakdown.length === 0) {
    errors.push('income_breakdown 为必填字段，不能为空数组');
  } else {
    // 一致性校验：sum(income_breakdown[].amount) 与 total_income 差异 ≤ 100 元
    if (typeof input.total_income === 'number' && input.total_income >= 0) {
      const sumBreakdown = input.income_breakdown.reduce((acc, item) => {
        return acc + (typeof item.amount === 'number' ? item.amount : 0);
      }, 0);
      const diff = Math.abs(input.total_income - sumBreakdown);
      if (diff > 100) {
        errors.push(
          `income_breakdown 各项金额之和（${sumBreakdown} 元）与 total_income（${input.total_income} 元）差异为 ${diff.toFixed(2)} 元，超过允许误差 100 元，请核实`,
        );
      }
    }
  }

  // projects_list — 非空数组
  if (!Array.isArray(input.projects_list) || input.projects_list.length === 0) {
    errors.push('projects_list 为必填字段，不能为空数组');
  }

  // staff_fulltime — 整数 >= 0
  if (input.staff_fulltime === undefined || input.staff_fulltime === null) {
    errors.push('staff_fulltime 为必填字段');
  } else if (!Number.isInteger(input.staff_fulltime) || input.staff_fulltime < 0) {
    errors.push('staff_fulltime 必须是大于等于 0 的整数');
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 3. 项目结项报告专用校验
// -----------------------------------------------------------------------

/**
 * 项目结项报告专用字段校验。应在 validateCommonInput 通过后调用。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateProjectFinalInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // project_name — 非空字符串
  if (!input.project_name || typeof input.project_name !== 'string' || !input.project_name.trim()) {
    errors.push('project_name 为必填字段，不能为空');
  }

  // funder_name — 非空字符串
  if (!input.funder_name || typeof input.funder_name !== 'string' || !input.funder_name.trim()) {
    errors.push('funder_name 为必填字段，不能为空');
  }

  // funder_platform — enum
  const validPlatforms = ['tencent', 'yijia', 'nandu', 'generic'];
  if (!input.funder_platform) {
    errors.push('funder_platform 为必填字段');
  } else if (!validPlatforms.includes(input.funder_platform)) {
    errors.push(
      `funder_platform 值无效："${input.funder_platform}"，有效值为：${validPlatforms.join('/')}`,
    );
  }

  // project_start_date / project_end_date
  const projStart = parseDate(input.project_start_date);
  const projEnd = parseDate(input.project_end_date);

  if (!projStart) {
    errors.push('project_start_date 为必填字段，格式应为 YYYY-MM-DD');
  }
  if (!projEnd) {
    errors.push('project_end_date 为必填字段，格式应为 YYYY-MM-DD');
  }
  if (projStart && projEnd && projEnd <= projStart) {
    errors.push('project_end_date 必须晚于 project_start_date');
  }

  // total_budget — number >= 0
  if (input.total_budget === undefined || input.total_budget === null) {
    errors.push('total_budget 为必填字段');
  } else if (typeof input.total_budget !== 'number' || input.total_budget < 0) {
    errors.push('total_budget 必须是大于等于 0 的数值');
  }

  // actual_expenditure — number >= 0
  if (input.actual_expenditure === undefined || input.actual_expenditure === null) {
    errors.push('actual_expenditure 为必填字段');
  } else if (typeof input.actual_expenditure !== 'number' || input.actual_expenditure < 0) {
    errors.push('actual_expenditure 必须是大于等于 0 的数值');
  }

  // expenditure_breakdown — 非空数组，差异校验
  if (!Array.isArray(input.expenditure_breakdown) || input.expenditure_breakdown.length === 0) {
    errors.push('expenditure_breakdown 为必填字段，不能为空数组');
  } else {
    input.expenditure_breakdown.forEach((item, idx) => {
      if (
        typeof item.budgeted === 'number' &&
        item.budgeted > 0 &&
        typeof item.actual === 'number'
      ) {
        const varianceRatio = Math.abs(item.actual - item.budgeted) / item.budgeted;
        if (varianceRatio > 0.1 && !item.variance_reason) {
          errors.push(
            `expenditure_breakdown[${idx}]（${item.category || '未命名'}）实际支出与预算差异为 ${(varianceRatio * 100).toFixed(1)}%，超过 10%，必须填写 variance_reason`,
          );
        }
      }
    });
  }

  // target_indicators — 非空数组，完成率异常检测
  if (!Array.isArray(input.target_indicators) || input.target_indicators.length === 0) {
    errors.push('target_indicators 为必填字段，不能为空数组');
  } else {
    input.target_indicators.forEach((item, idx) => {
      if (typeof item.completion_rate === 'number' && item.completion_rate > 150) {
        warnings.push(
          `target_indicators[${idx}]（${item.indicator || '未命名'}）完成率为 ${item.completion_rate}%，超过 150%，请确认数据是否正确`,
        );
      }
    });
  }

  // activities_summary — 非空数组
  if (!Array.isArray(input.activities_summary) || input.activities_summary.length === 0) {
    errors.push('activities_summary 为必填字段，不能为空数组');
  }

  // challenges_and_response — 非空字符串
  if (
    !input.challenges_and_response ||
    typeof input.challenges_and_response !== 'string' ||
    !input.challenges_and_response.trim()
  ) {
    errors.push('challenges_and_response 为必填字段，不能为空');
  }

  // 腾讯公益特殊：tencent_project_id 必填且格式 TXGY-YYYY-XXX
  if (input.funder_platform === 'tencent') {
    if (!input.tencent_project_id) {
      errors.push('funder_platform 为 tencent 时，tencent_project_id 为必填字段');
    } else {
      const txPattern = /^TXGY-\d{4}-\d{3}$/;
      if (!txPattern.test(input.tencent_project_id)) {
        errors.push(
          `tencent_project_id 格式不正确："${input.tencent_project_id}"，期望格式：TXGY-YYYY-XXX（如 TXGY-2025-001）`,
        );
      }
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 4. 财务决算报告专用校验
// -----------------------------------------------------------------------

/**
 * 财务决算报告专用字段校验。应在 validateCommonInput 通过后调用。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateFinanceFinalInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // project_name — 非空字符串
  if (!input.project_name || typeof input.project_name !== 'string' || !input.project_name.trim()) {
    errors.push('project_name 为必填字段，不能为空');
  }

  // funder_name — 非空字符串
  if (!input.funder_name || typeof input.funder_name !== 'string' || !input.funder_name.trim()) {
    errors.push('funder_name 为必填字段，不能为空');
  }

  // total_grant / total_expenditure / unexpended_balance — number 类型校验
  const hasGrant =
    typeof input.total_grant === 'number' && isFinite(input.total_grant);
  const hasExpenditure =
    typeof input.total_expenditure === 'number' && isFinite(input.total_expenditure);
  const hasBalance =
    typeof input.unexpended_balance === 'number' && isFinite(input.unexpended_balance);

  if (!hasGrant) {
    errors.push('total_grant 为必填字段，必须是有效数值');
  }
  if (!hasExpenditure) {
    errors.push('total_expenditure 为必填字段，必须是有效数值');
  }
  if (!hasBalance) {
    errors.push('unexpended_balance 为必填字段，必须是有效数值');
  }

  // 严格等式：unexpended_balance === total_grant - total_expenditure
  // 使用浮点容差 0.01 元避免浮点精度问题，但语义上要求严格一致
  if (hasGrant && hasExpenditure && hasBalance) {
    const expectedBalance = input.total_grant - input.total_expenditure;
    if (Math.abs(input.unexpended_balance - expectedBalance) > 0.01) {
      errors.push(
        `unexpended_balance（${input.unexpended_balance} 元）与 total_grant - total_expenditure 计算结果（${expectedBalance.toFixed(2)} 元）不一致，请核实`,
      );
    }

    // 结余 > 1% 时：balance_handling 必填
    if (input.total_grant > 0) {
      const balanceRatio = input.unexpended_balance / input.total_grant;
      if (balanceRatio > 0.01) {
        const validHandling = ['return', 'carryover', 'other'];
        if (!input.balance_handling) {
          errors.push(
            `结余金额（${input.unexpended_balance} 元）超过资助总额的 1%，balance_handling 为必填字段`,
          );
        } else if (!validHandling.includes(input.balance_handling)) {
          errors.push(
            `balance_handling 值无效："${input.balance_handling}"，有效值为：${validHandling.join('/')}`,
          );
        }
      }
    }
  }

  // audit_required === true 时：audit_firm 必填
  if (input.audit_required === true) {
    if (!input.audit_firm || typeof input.audit_firm !== 'string' || !input.audit_firm.trim()) {
      errors.push('audit_required 为 true 时，audit_firm（审计机构名称）为必填字段');
    }
  }

  // expenditure_detail — 非空数组
  if (!Array.isArray(input.expenditure_detail) || input.expenditure_detail.length === 0) {
    errors.push('expenditure_detail 为必填字段，不能为空数组');
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 5. PII 安全校验
// -----------------------------------------------------------------------

/**
 * PII 安全校验。
 *
 * 合规依据：PIPL 第23/28条、未成年人保护法第72条
 * - 检测 story_case 中疑似中文真实姓名（2-4汉字，非化名标注）
 * - 标记 contact_name / contact_phone 为 PII 字段，供 prompt-builder 排除
 *
 * @param {object} input
 * @returns {{ piiFields: string[], warnings: string[] }}
 */
function validatePIISafety(input) {
  const piiFields = ['contact_name', 'contact_phone'];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { piiFields, warnings };
  }

  // 检测 story_case 中的疑似真实姓名（支持字符串和数组两种结构）
  let storyCaseText = '';
  if (input.story_case) {
    if (typeof input.story_case === 'string') {
      storyCaseText = input.story_case;
    } else if (Array.isArray(input.story_case)) {
      storyCaseText = input.story_case
        .map(c => [c.case_title, c.case_description].filter(Boolean).join(' '))
        .join(' ');
    }
  }

  if (storyCaseText) {
    const sanitized = storyCaseText
      .replace(/[\u4e00-\u9fa5]{1,4}[（(][^（()）]*化名[^（()）]*[）)]/g, '')
      .replace(/[（(]化名[）)]/g, '');

    // 保守动词列表：仅用高置信度的姓名引入动词，避免"一个来自""放学后参加"等误报
    const nameContextPattern = /[\u4e00-\u9fa5]{2,4}(?=是|叫|说|告诉|表示|介绍|反映|名叫|叫做)/g;
    const matches = sanitized.match(nameContextPattern);

    if (matches && matches.length > 0) {
      const uniqueMatches = [...new Set(matches)];
      warnings.push(
        `story_case 中检测到疑似真实姓名：${uniqueMatches.join('、')}。请确认已使用化名（如：小明（化名））替换真实姓名，以保护受益人隐私。`,
      );
    }
  }

  return { piiFields, warnings };
}

// -----------------------------------------------------------------------
// 6. 总入口
// -----------------------------------------------------------------------

/**
 * 总校验入口。根据 input.report_type 调用对应专项校验，汇总结果。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validate(input) {
  const result = { valid: true, errors: [], warnings: [] };

  // Step 1: 通用校验
  const commonResult = validateCommonInput(input);
  mergeResult(result, commonResult);

  // Step 2: 按 report_type 分发专项校验
  if (input && input.report_type) {
    switch (input.report_type) {
      case 'annual_work': {
        const r = validateAnnualWorkInput(input);
        mergeResult(result, r);
        break;
      }
      case 'project_final': {
        const r = validateProjectFinalInput(input);
        mergeResult(result, r);
        break;
      }
      case 'finance_final': {
        const r = validateFinanceFinalInput(input);
        mergeResult(result, r);
        break;
      }
      default:
        // report_type 无效已在 validateCommonInput 中报告
        break;
    }
  }

  // Step 3: PII 安全校验（仅追加 warnings，不影响 valid）
  const piiResult = validatePIISafety(input);
  result.warnings.push(...piiResult.warnings);

  // 汇总：有 error 则 valid = false
  result.valid = result.errors.length === 0;

  return result;
}

// -----------------------------------------------------------------------
// 导出
// -----------------------------------------------------------------------

module.exports = {
  validate,
  validateCommonInput,
  validateAnnualWorkInput,
  validateProjectFinalInput,
  validateFinanceFinalInput,
  validatePIISafety,
};
