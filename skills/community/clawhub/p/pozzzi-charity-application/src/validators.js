'use strict';

// -----------------------------------------------------------------------
// validators.js — 申报助手输入校验器
//
// 依赖：仅 Node.js 内置模块
// 合规依据：噗滋慈善申报助手 Spec v1.0 + PIPL 第23/28条 + 慈善法第75/77条
// 架构复用：与 report-assistant/src/validators.js 框架保持一致
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

// -----------------------------------------------------------------------
// 1. 通用输入校验
// -----------------------------------------------------------------------

/**
 * 校验所有申报类型共用的必填字段。
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

  // org_type — enum
  const validOrgTypes = ['社会团体', '民办非企业单位', '基金会'];
  if (!input.org_type) {
    errors.push('org_type 为必填字段');
  } else if (!validOrgTypes.includes(input.org_type)) {
    errors.push(
      `org_type 值无效："${input.org_type}"，有效值为：${validOrgTypes.join('/')}`,
    );
  }

  // application_type — enum
  const validApplicationTypes = ['generic', 'tencent99', 'govt_purchase'];
  if (!input.application_type) {
    errors.push('application_type 为必填字段');
  } else if (!validApplicationTypes.includes(input.application_type)) {
    errors.push(
      `application_type 值无效："${input.application_type}"，有效值为：${validApplicationTypes.join('/')}`,
    );
  }

  // project_name — 非空字符串
  if (!input.project_name || typeof input.project_name !== 'string' || !input.project_name.trim()) {
    errors.push('project_name 为必填字段，不能为空');
  }

  // project_domain — enum
  const validProjectDomains = [
    'education', 'health', 'elderly', 'disability', 'poverty',
    'environment', 'women_children', 'community', 'arts_culture', 'other',
  ];
  if (!input.project_domain) {
    errors.push('project_domain 为必填字段');
  } else if (!validProjectDomains.includes(input.project_domain)) {
    errors.push(
      `project_domain 值无效："${input.project_domain}"，有效值为：${validProjectDomains.join('/')}`,
    );
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
// 2. 项目设计输入校验
// -----------------------------------------------------------------------

/**
 * 校验项目设计相关字段（所有申报类型共用）。
 * 应在 validateCommonInput 通过后调用。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateProjectDesignInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // project_goal — 50-200 字
  if (!input.project_goal || typeof input.project_goal !== 'string' || !input.project_goal.trim()) {
    errors.push('project_goal 为必填字段，不能为空');
  } else {
    const goalLen = input.project_goal.trim().length;
    if (goalLen < 50) {
      errors.push(`project_goal 不能少于 50 个字符，当前：${goalLen} 个字符`);
    } else if (goalLen > 200) {
      errors.push(`project_goal 不能超过 200 个字符，当前：${goalLen} 个字符`);
    }
  }

  // project_objectives — 非空数组，每项有 description + indicator
  if (!Array.isArray(input.project_objectives) || input.project_objectives.length === 0) {
    errors.push('project_objectives 为必填字段，不能为空数组');
  } else {
    input.project_objectives.forEach((obj, idx) => {
      if (!obj.description || typeof obj.description !== 'string' || !obj.description.trim()) {
        errors.push(`project_objectives[${idx}].description 为必填字段，不能为空`);
      }
      if (!obj.indicator || typeof obj.indicator !== 'string' || !obj.indicator.trim()) {
        errors.push(`project_objectives[${idx}].indicator 为必填字段，不能为空`);
      }
    });
  }

  // activities_design — 非空数组
  if (!Array.isArray(input.activities_design) || input.activities_design.length === 0) {
    errors.push('activities_design 为必填字段，不能为空数组');
  } else {
    input.activities_design.forEach((act, idx) => {
      if (!act.name || typeof act.name !== 'string' || !act.name.trim()) {
        errors.push(`activities_design[${idx}].name 为必填字段，不能为空`);
      }
      if (!act.description || typeof act.description !== 'string' || !act.description.trim()) {
        errors.push(`activities_design[${idx}].description 为必填字段，不能为空`);
      }
      if (!act.frequency || typeof act.frequency !== 'string' || !act.frequency.trim()) {
        errors.push(`activities_design[${idx}].frequency 为必填字段，不能为空`);
      }
    });
  }

  // timeline — 非空数组，end_month > start_month
  if (!Array.isArray(input.timeline) || input.timeline.length === 0) {
    errors.push('timeline 为必填字段，不能为空数组');
  } else {
    input.timeline.forEach((phase, idx) => {
      if (!phase.phase || typeof phase.phase !== 'string' || !phase.phase.trim()) {
        errors.push(`timeline[${idx}].phase 为必填字段，不能为空`);
      }
      const startMonth = Number(phase.start_month);
      const endMonth = Number(phase.end_month);
      if (!Number.isInteger(startMonth) || startMonth < 1) {
        errors.push(`timeline[${idx}].start_month 必须是正整数`);
      }
      if (!Number.isInteger(endMonth) || endMonth < 1) {
        errors.push(`timeline[${idx}].end_month 必须是正整数`);
      }
      if (Number.isInteger(startMonth) && Number.isInteger(endMonth) && endMonth <= startMonth) {
        errors.push(
          `timeline[${idx}]（${phase.phase || '未命名阶段'}）end_month（${endMonth}）必须大于 start_month（${startMonth}）`,
        );
      }
      if (!phase.key_tasks || typeof phase.key_tasks !== 'string' || !phase.key_tasks.trim()) {
        errors.push(`timeline[${idx}].key_tasks 为必填字段，不能为空`);
      }
    });

    // 最后一个阶段的 end_month 不应超过 project_duration_months
    if (
      typeof input.project_duration_months === 'number' &&
      input.project_duration_months > 0
    ) {
      const lastPhase = input.timeline[input.timeline.length - 1];
      const lastEndMonth = Number(lastPhase.end_month);
      if (Number.isInteger(lastEndMonth) && lastEndMonth > input.project_duration_months) {
        errors.push(
          `timeline 最后阶段的 end_month（${lastEndMonth}）超过了 project_duration_months（${input.project_duration_months}），请检查时间表`,
        );
      }
    }
  }

  // project_duration_months — 正整数
  if (
    input.project_duration_months === undefined ||
    input.project_duration_months === null
  ) {
    errors.push('project_duration_months 为必填字段');
  } else {
    const dur = Number(input.project_duration_months);
    if (!Number.isInteger(dur) || dur <= 0) {
      errors.push('project_duration_months 必须是正整数');
    }
  }

  // project_start_date — 格式 YYYY-MM
  if (!input.project_start_date || typeof input.project_start_date !== 'string') {
    errors.push('project_start_date 为必填字段，格式应为 YYYY-MM');
  } else {
    const ymPattern = /^\d{4}-(0[1-9]|1[0-2])$/;
    if (!ymPattern.test(input.project_start_date.trim())) {
      errors.push(
        `project_start_date 格式不正确："${input.project_start_date}"，期望格式：YYYY-MM（如 2026-07）`,
      );
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 3. 预算输入校验
// -----------------------------------------------------------------------

/**
 * 校验预算相关字段（所有申报类型共用）。
 * 应在 validateCommonInput 通过后调用。
 *
 * 合规依据（合规红线第8条）：
 * - total_budget 和 budget_breakdown[].amount 必须由用户填写
 * - Skill 不生成、推算或补充任何预算金额
 * - sum(breakdown.amount) 与 total_budget 差异 > 100 元 → error（阻断）
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateBudgetInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // total_budget — 正数
  const hasTotalBudget =
    typeof input.total_budget === 'number' &&
    isFinite(input.total_budget) &&
    input.total_budget > 0;

  if (input.total_budget === undefined || input.total_budget === null) {
    errors.push('total_budget 为必填字段');
  } else if (!hasTotalBudget) {
    errors.push('total_budget 必须是大于 0 的数值');
  }

  // budget_breakdown — 非空数组，每项有 category/amount/description
  if (!Array.isArray(input.budget_breakdown) || input.budget_breakdown.length === 0) {
    errors.push('budget_breakdown 为必填字段，不能为空数组');
  } else {
    input.budget_breakdown.forEach((item, idx) => {
      if (!item.category || typeof item.category !== 'string' || !item.category.trim()) {
        errors.push(`budget_breakdown[${idx}].category 为必填字段，不能为空`);
      }
      if (typeof item.amount !== 'number' || !isFinite(item.amount) || item.amount <= 0) {
        errors.push(`budget_breakdown[${idx}].amount 必须是大于 0 的数值`);
      }
      if (!item.description || typeof item.description !== 'string' || !item.description.trim()) {
        errors.push(`budget_breakdown[${idx}].description 为必填字段，不能为空`);
      }
    });

    // 预算一致性校验：sum(breakdown.amount) 与 total_budget 差异 ≤ 100 元
    if (hasTotalBudget) {
      const sumBreakdown = input.budget_breakdown.reduce((acc, item) => {
        return acc + (typeof item.amount === 'number' && isFinite(item.amount) ? item.amount : 0);
      }, 0);
      const diff = Math.abs(input.total_budget - sumBreakdown);
      if (diff > 100) {
        errors.push(
          `budget_breakdown 各项金额之和（${sumBreakdown} 元）与 total_budget（${input.total_budget} 元）差异为 ${diff.toFixed(2)} 元，超过允许误差 100 元，请核实后继续`,
        );
      }

      // percentage 自动计算校验（用户填了才校验）
      input.budget_breakdown.forEach((item, idx) => {
        if (item.percentage !== undefined && item.percentage !== null) {
          const expectedPct = (item.amount / input.total_budget) * 100;
          const pctDiff = Math.abs(item.percentage - expectedPct);
          if (pctDiff > 0.5) {
            warnings.push(
              `budget_breakdown[${idx}]（${item.category || '未命名'}）percentage（${item.percentage}%）与计算值（${expectedPct.toFixed(2)}%）差异超过 0.5%，建议核实`,
            );
          }
        }
      });
    }
  }

  // has_matching_fund — boolean 类型
  if (input.has_matching_fund === undefined || input.has_matching_fund === null) {
    errors.push('has_matching_fund 为必填字段');
  } else if (typeof input.has_matching_fund !== 'boolean') {
    errors.push('has_matching_fund 必须是布尔值（true/false）');
  } else if (input.has_matching_fund === true) {
    // has_matching_fund=true 时，matching_fund_amount + matching_fund_source 必填
    if (
      input.matching_fund_amount === undefined ||
      input.matching_fund_amount === null
    ) {
      errors.push('has_matching_fund 为 true 时，matching_fund_amount 为必填字段');
    } else if (
      typeof input.matching_fund_amount !== 'number' ||
      !isFinite(input.matching_fund_amount) ||
      input.matching_fund_amount <= 0
    ) {
      errors.push('matching_fund_amount 必须是大于 0 的数值');
    }

    if (
      !input.matching_fund_source ||
      typeof input.matching_fund_source !== 'string' ||
      !input.matching_fund_source.trim()
    ) {
      errors.push('has_matching_fund 为 true 时，matching_fund_source 为必填字段，不能为空');
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 4. 腾讯公益99公益日专项校验
// -----------------------------------------------------------------------

/**
 * 腾讯公益99公益日专用字段校验。
 * 应在 application_type === 'tencent99' 时调用。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateTencent99Input(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // tencent_fundraising_goal — 正数
  if (
    input.tencent_fundraising_goal === undefined ||
    input.tencent_fundraising_goal === null
  ) {
    errors.push('tencent_fundraising_goal 为必填字段');
  } else if (
    typeof input.tencent_fundraising_goal !== 'number' ||
    !isFinite(input.tencent_fundraising_goal) ||
    input.tencent_fundraising_goal <= 0
  ) {
    errors.push('tencent_fundraising_goal 必须是大于 0 的数值');
  } else {
    // 筹款目标不应超过 total_budget 的 2 倍（警告，不阻断）
    if (
      typeof input.total_budget === 'number' &&
      input.total_budget > 0 &&
      input.tencent_fundraising_goal > input.total_budget * 2
    ) {
      warnings.push(
        `tencent_fundraising_goal（${input.tencent_fundraising_goal} 元）超过 total_budget（${input.total_budget} 元）的 2 倍，请确认筹款目标是否合理`,
      );
    }
  }

  // tencent_project_category — 非空字符串
  if (
    !input.tencent_project_category ||
    typeof input.tencent_project_category !== 'string' ||
    !input.tencent_project_category.trim()
  ) {
    errors.push('tencent_project_category 为必填字段，不能为空');
  }

  // donation_use_description — 非空，100-200 字
  if (
    !input.donation_use_description ||
    typeof input.donation_use_description !== 'string' ||
    !input.donation_use_description.trim()
  ) {
    errors.push('donation_use_description 为必填字段，不能为空');
  } else {
    const descLen = input.donation_use_description.trim().length;
    if (descLen < 100) {
      errors.push(`donation_use_description 不能少于 100 个字符，当前：${descLen} 个字符`);
    } else if (descLen > 200) {
      errors.push(`donation_use_description 不能超过 200 个字符，当前：${descLen} 个字符`);
    }
  }

  // has_previous_99_project — boolean
  if (
    input.has_previous_99_project === undefined ||
    input.has_previous_99_project === null
  ) {
    errors.push('has_previous_99_project 为必填字段');
  } else if (typeof input.has_previous_99_project !== 'boolean') {
    errors.push('has_previous_99_project 必须是布尔值（true/false）');
  } else if (input.has_previous_99_project === true) {
    // has_previous_99_project=true 时 previous_99_outcome 必填
    if (
      !input.previous_99_outcome ||
      typeof input.previous_99_outcome !== 'string' ||
      !input.previous_99_outcome.trim()
    ) {
      errors.push('has_previous_99_project 为 true 时，previous_99_outcome 为必填字段，不能为空');
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 5. 政府购买服务专项校验
// -----------------------------------------------------------------------

/**
 * 政府购买服务专用字段校验。
 * 应在 application_type === 'govt_purchase' 时调用。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateGovtPurchaseInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // govt_dept_name — 非空字符串
  if (
    !input.govt_dept_name ||
    typeof input.govt_dept_name !== 'string' ||
    !input.govt_dept_name.trim()
  ) {
    errors.push('govt_dept_name 为必填字段，不能为空');
  }

  // tender_project_name — 非空字符串
  if (
    !input.tender_project_name ||
    typeof input.tender_project_name !== 'string' ||
    !input.tender_project_name.trim()
  ) {
    errors.push('tender_project_name 为必填字段，不能为空');
  }

  // service_area — 非空字符串
  if (
    !input.service_area ||
    typeof input.service_area !== 'string' ||
    !input.service_area.trim()
  ) {
    errors.push('service_area 为必填字段，不能为空');
  }

  // performance_indicators — 非空数组，每项有 indicator/target/measurement
  if (!Array.isArray(input.performance_indicators) || input.performance_indicators.length === 0) {
    errors.push('performance_indicators 为必填字段，不能为空数组');
  } else {
    input.performance_indicators.forEach((item, idx) => {
      if (!item.indicator || typeof item.indicator !== 'string' || !item.indicator.trim()) {
        errors.push(`performance_indicators[${idx}].indicator 为必填字段，不能为空`);
      }
      if (!item.target || typeof item.target !== 'string' || !item.target.trim()) {
        errors.push(`performance_indicators[${idx}].target 为必填字段，不能为空`);
      }
      if (!item.measurement || typeof item.measurement !== 'string' || !item.measurement.trim()) {
        errors.push(`performance_indicators[${idx}].measurement 为必填字段，不能为空`);
      }
    });
  }

  // price_quote — 正数
  if (input.price_quote === undefined || input.price_quote === null) {
    errors.push('price_quote 为必填字段');
  } else if (
    typeof input.price_quote !== 'number' ||
    !isFinite(input.price_quote) ||
    input.price_quote <= 0
  ) {
    errors.push('price_quote 必须是大于 0 的数值');
  }

  // price_breakdown — 非空（字符串或非空数组均可）
  if (
    input.price_breakdown === undefined ||
    input.price_breakdown === null
  ) {
    errors.push('price_breakdown 为必填字段，不能为空');
  } else if (typeof input.price_breakdown === 'string') {
    if (!input.price_breakdown.trim()) {
      errors.push('price_breakdown 为必填字段，不能为空字符串');
    }
  } else if (Array.isArray(input.price_breakdown)) {
    if (input.price_breakdown.length === 0) {
      errors.push('price_breakdown 为必填字段，不能为空数组');
    }
  } else {
    errors.push('price_breakdown 格式不正确，应为字符串或数组');
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 6. PII 安全校验
// -----------------------------------------------------------------------

/**
 * PII 安全校验（申报助手版）。
 *
 * 合规依据：PIPL 第23/28条、未成年人保护法第72条、申报助手 Spec v1.0
 * - 标记 contact_name / contact_phone 为 piiFields，供 prompt-builder 排除
 * - 检测 team_composition[].background 中疑似中文真实姓名（2-4汉字+上下文动词）
 * - 检测 problem_statement 中统计数据模式 → warning 提示填写 needs_data_source
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

  // 检测 team_composition[].background 中疑似中文真实姓名
  if (Array.isArray(input.team_composition) && input.team_composition.length > 0) {
    const allBackgrounds = input.team_composition
      .map((m, idx) => ({ idx, text: m.background || '' }))
      .filter(item => typeof item.text === 'string' && item.text.trim());

    // 姓名检测：动词上下文 + 分隔符后2-4汉字（如"项目主任：王小明，…"）
    const nameContextPattern = /[\u4e00-\u9fa5]{2,4}(?=是|叫|说|告诉|表示|介绍|反映|名叫|叫做)/g;
    const nameAfterDelimiter = /[：:、，]\s*([\u4e00-\u9fa5]{2,4})(?=[，,。\s]|$)/g;

    allBackgrounds.forEach(({ idx, text }) => {
      const matches1 = text.match(nameContextPattern) || [];
      const matches2 = [];
      let dm;
      while ((dm = nameAfterDelimiter.exec(text)) !== null) {
        matches2.push(dm[1]);
      }
      nameAfterDelimiter.lastIndex = 0;
      const matches = [...matches1, ...matches2];
      if (matches && matches.length > 0) {
        const uniqueMatches = [...new Set(matches)];
        warnings.push(
          `team_composition[${idx}].background 中检测到疑似真实姓名：${uniqueMatches.join('、')}。请使用职位/专业背景描述代替真实姓名（如"社会工作专业硕士"），以保护团队成员隐私。`,
        );
      }
    });
  }

  // 检测 problem_statement 中的统计数据模式 → warning 提示填写 needs_data_source
  if (
    input.problem_statement &&
    typeof input.problem_statement === 'string' &&
    input.problem_statement.trim()
  ) {
    // 检测模式：XX万人 / XX% / XX人 / XX亿 等统计数字
    const statsPattern = /\d+(\.\d+)?\s*(万|亿|千)?\s*(人次?|%|个|所|家|名|户|例)/;
    const hasStats = statsPattern.test(input.problem_statement);

    if (hasStats && (!input.needs_data_source || !input.needs_data_source.trim())) {
      warnings.push(
        '您的需求描述（problem_statement）中包含统计数字，建议在 needs_data_source 字段中注明数据来源。AI 不会在申报书中补充或修改您未提供的统计数据。',
      );
    }
  }

  return { piiFields, warnings };
}

// -----------------------------------------------------------------------
// 7. 总入口
// -----------------------------------------------------------------------

/**
 * 总校验入口。按顺序执行：
 * 1. 通用必填字段校验（validateCommonInput）
 * 2. 项目设计字段校验（validateProjectDesignInput）
 * 3. 按 application_type 分发专项校验
 * 4. 预算校验（validateBudgetInput）
 * 5. PII 安全校验（validatePIISafety，仅追加 warnings，不影响 valid）
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[], piiFields: string[] }}
 */
function validate(input) {
  const result = { valid: true, errors: [], warnings: [], piiFields: [] };

  // Step 1: 通用校验
  const commonResult = validateCommonInput(input);
  mergeResult(result, commonResult);

  // Step 2: 项目设计校验
  const designResult = validateProjectDesignInput(input);
  mergeResult(result, designResult);

  // Step 3: 按 application_type 分发专项校验
  if (input && input.application_type) {
    switch (input.application_type) {
      case 'tencent99': {
        const r = validateTencent99Input(input);
        mergeResult(result, r);
        break;
      }
      case 'govt_purchase': {
        const r = validateGovtPurchaseInput(input);
        mergeResult(result, r);
        break;
      }
      case 'generic':
        // generic 无额外专项字段校验
        break;
      default:
        // application_type 无效已在 validateCommonInput 中报告
        break;
    }
  }

  // Step 4: 预算校验
  const budgetResult = validateBudgetInput(input);
  mergeResult(result, budgetResult);

  // Step 5: PII 安全校验（仅追加 warnings，piiFields，不影响 valid）
  const piiResult = validatePIISafety(input);
  result.warnings.push(...piiResult.warnings);
  result.piiFields = piiResult.piiFields;

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
  validateProjectDesignInput,
  validateBudgetInput,
  validateTencent99Input,
  validateGovtPurchaseInput,
  validatePIISafety,
};
