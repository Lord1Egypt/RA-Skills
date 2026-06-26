'use strict';

// -----------------------------------------------------------------------
// validators.js — 文书助手输入校验器
//
// 依赖：仅 Node.js 内置模块
// 合规依据：噗滋慈善文书助手 Spec v1.0 + PIPL 第23/28条 + 慈善法第75/77条
// 架构复用：与 application-assistant/src/validators.js 框架保持一致
//
// 枚举值来源：文书助手 Spec v1.0 输入定义章节（以 Spec 为准）
//   document_type:    contract / minutes / letter / plan_summary
//   document_subtype: 见各 document_type 分支下的合法子类型
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
// 子类型映射表（document_type → 合法 document_subtype 列表）
// 来源：Spec v1.0 §功能范围 / §工作流 §文书类型识别
// -----------------------------------------------------------------------
const VALID_SUBTYPES = {
  contract: ['volunteer_agreement', 'cooperation_agreement', 'rental_agreement'],
  minutes: ['board_minutes', 'team_minutes'],
  letter: ['govt_letter', 'thanks_letter_funder', 'thanks_letter_donor'],
  plan_summary: ['work_plan', 'work_summary'],
};

// -----------------------------------------------------------------------
// 1. 通用输入校验
// -----------------------------------------------------------------------

/**
 * 校验所有文书类型共用的必填字段。
 *
 * PII 安全注释（Spec §合规要求）：
 *   contact_name / contact_phone 在此仅做非空校验，
 *   不得出现在模型 API Prompt、生成文书正文、任何网络请求中。
 *   由 validatePIISafety 负责标记和排除。
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

  // document_type — enum: contract / minutes / letter / plan_summary
  const validDocumentTypes = Object.keys(VALID_SUBTYPES);
  if (!input.document_type) {
    errors.push('document_type 为必填字段');
  } else if (!validDocumentTypes.includes(input.document_type)) {
    errors.push(
      `document_type 值无效："${input.document_type}"，有效值为：${validDocumentTypes.join('/')}`,
    );
  }

  // document_subtype — 根据 document_type 校验合法子类型
  if (!input.document_subtype) {
    errors.push('document_subtype 为必填字段');
  } else if (input.document_type && validDocumentTypes.includes(input.document_type)) {
    const validSubs = VALID_SUBTYPES[input.document_type];
    if (!validSubs.includes(input.document_subtype)) {
      errors.push(
        `document_subtype 值无效："${input.document_subtype}"，` +
          `在 document_type="${input.document_type}" 下有效值为：${validSubs.join('/')}`,
      );
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

  // draft_date — 可选，格式 YYYY-MM-DD（若填写则校验格式）
  if (input.draft_date !== undefined && input.draft_date !== null) {
    if (typeof input.draft_date !== 'string') {
      errors.push('draft_date 格式不正确，应为 YYYY-MM-DD 字符串');
    } else {
      const datePattern = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
      if (!datePattern.test(input.draft_date.trim())) {
        errors.push(
          `draft_date 格式不正确："${input.draft_date}"，期望格式：YYYY-MM-DD（如 2026-04-01）`,
        );
      }
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 2. 合同/协议专用校验
// -----------------------------------------------------------------------

/**
 * 校验合同/协议专用字段。
 * 应在 document_type === 'contract' 时调用。
 *
 * 适用 document_subtype：
 *   volunteer_agreement（志愿者服务协议）
 *   cooperation_agreement（项目合作协议）
 *   rental_agreement（场地/设备租赁协议）
 *
 * 合规说明（Spec §合规要求）：
 *   - agreement_purpose 不得包含模型自行补充的金额；金额字段由用户自填
 *   - party_b_name 涉及自然人时输出操作建议（warning，不阻断）
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateContractInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // party_b_type — enum: individual / org
  const validPartyBTypes = ['individual', 'org'];
  if (!input.party_b_type) {
    errors.push('party_b_type 为必填字段');
  } else if (!validPartyBTypes.includes(input.party_b_type)) {
    errors.push(
      `party_b_type 值无效："${input.party_b_type}"，有效值为：${validPartyBTypes.join('/')}`,
    );
  }

  // agreement_purpose — 必填，50-300 字
  if (
    !input.agreement_purpose ||
    typeof input.agreement_purpose !== 'string' ||
    !input.agreement_purpose.trim()
  ) {
    errors.push('agreement_purpose 为必填字段，不能为空');
  } else {
    const len = input.agreement_purpose.trim().length;
    if (len < 50) {
      errors.push(`agreement_purpose 不能少于 50 个字符，当前：${len} 个字符`);
    } else if (len > 300) {
      errors.push(`agreement_purpose 不能超过 300 个字符，当前：${len} 个字符`);
    }
  }

  // service_period_start — 可选，格式 YYYY-MM-DD
  if (input.service_period_start !== undefined && input.service_period_start !== null) {
    const datePattern = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
    if (
      typeof input.service_period_start !== 'string' ||
      !datePattern.test(input.service_period_start.trim())
    ) {
      errors.push(
        `service_period_start 格式不正确："${input.service_period_start}"，期望格式：YYYY-MM-DD`,
      );
    }
  }

  // service_period_end — 可选，格式 YYYY-MM-DD；且不得早于 start
  if (input.service_period_end !== undefined && input.service_period_end !== null) {
    const datePattern = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
    if (
      typeof input.service_period_end !== 'string' ||
      !datePattern.test(input.service_period_end.trim())
    ) {
      errors.push(
        `service_period_end 格式不正确："${input.service_period_end}"，期望格式：YYYY-MM-DD`,
      );
    } else if (
      input.service_period_start &&
      typeof input.service_period_start === 'string'
    ) {
      if (input.service_period_end.trim() <= input.service_period_start.trim()) {
        errors.push(
          `service_period_end（${input.service_period_end}）不得早于或等于 service_period_start（${input.service_period_start}）`,
        );
      }
    }
  }

  // key_obligations_a — 可选，若填写则 50-200 字
  if (input.key_obligations_a !== undefined && input.key_obligations_a !== null) {
    if (typeof input.key_obligations_a !== 'string' || !input.key_obligations_a.trim()) {
      errors.push('key_obligations_a 若填写，不能为空字符串');
    } else {
      const len = input.key_obligations_a.trim().length;
      if (len < 50) {
        errors.push(`key_obligations_a 若填写，不能少于 50 个字符，当前：${len} 个字符`);
      } else if (len > 200) {
        errors.push(`key_obligations_a 若填写，不能超过 200 个字符，当前：${len} 个字符`);
      }
    }
  }

  // key_obligations_b — 可选，若填写则 50-200 字
  if (input.key_obligations_b !== undefined && input.key_obligations_b !== null) {
    if (typeof input.key_obligations_b !== 'string' || !input.key_obligations_b.trim()) {
      errors.push('key_obligations_b 若填写，不能为空字符串');
    } else {
      const len = input.key_obligations_b.trim().length;
      if (len < 50) {
        errors.push(`key_obligations_b 若填写，不能少于 50 个字符，当前：${len} 个字符`);
      } else if (len > 200) {
        errors.push(`key_obligations_b 若填写，不能超过 200 个字符，当前：${len} 个字符`);
      }
    }
  }

  // dispute_resolution — 可选，enum
  const validDisputeTypes = ['negotiation', 'mediation', 'arbitration', 'litigation'];
  if (input.dispute_resolution !== undefined && input.dispute_resolution !== null) {
    if (!validDisputeTypes.includes(input.dispute_resolution)) {
      errors.push(
        `dispute_resolution 值无效："${input.dispute_resolution}"，有效值为：${validDisputeTypes.join('/')}`,
      );
    }
  }

  // party_b_name 自然人提示（warning，不阻断）
  if (input.party_b_type === 'individual' && input.party_b_name && input.party_b_name.trim()) {
    warnings.push(
      '协议另一方为自然人时，正式签署版本需在签署栏填写真实姓名和身份证号，' +
        '但草稿阶段建议使用"乙方姓名占位符"，签署前再替换。',
    );
  }

  // compensation_desc 为空时提示（warning，不阻断）
  if (!input.compensation_desc || !input.compensation_desc.trim()) {
    warnings.push(
      '未填写 compensation_desc（报酬/补贴说明）。若为无偿服务，建议明确填写"无偿"；AI 不会补充任何金额。',
    );
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 3. 会议纪要专用校验
// -----------------------------------------------------------------------

/**
 * 校验会议纪要专用字段。
 * 应在 document_type === 'minutes' 时调用。
 *
 * 适用 document_subtype：
 *   board_minutes（理事会/监事会会议纪要）
 *   team_minutes（项目/团队内部会议纪要）
 *
 * PII 合规（Spec §合规要求）：
 *   attendees_desc / discussion_summary[].key_points 中疑似真实姓名
 *   → 黄色警告（不阻断），由 validatePIISafety 负责检测
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateMeetingMinutesInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // meeting_date — 必填，格式 YYYY-MM-DD
  if (!input.meeting_date || typeof input.meeting_date !== 'string') {
    errors.push('meeting_date 为必填字段，格式应为 YYYY-MM-DD');
  } else {
    const datePattern = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
    if (!datePattern.test(input.meeting_date.trim())) {
      errors.push(
        `meeting_date 格式不正确："${input.meeting_date}"，期望格式：YYYY-MM-DD（如 2026-03-28）`,
      );
    } else {
      // 未来日期合理性校验（Spec §输入校验：未来 >7天 → 提示确认）
      const inputDate = new Date(input.meeting_date.trim());
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const sevenDaysLater = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);
      if (inputDate > sevenDaysLater) {
        warnings.push(
          `meeting_date（${input.meeting_date}）超过今日 7 天，请确认会议日期是否正确。`,
        );
      }
    }
  }

  // attendees_desc — 必填，非空字符串
  if (
    !input.attendees_desc ||
    typeof input.attendees_desc !== 'string' ||
    !input.attendees_desc.trim()
  ) {
    errors.push('attendees_desc 为必填字段，不能为空');
  }

  // agenda_items — 非空字符串数组
  if (!Array.isArray(input.agenda_items) || input.agenda_items.length === 0) {
    errors.push('agenda_items 为必填字段，不能为空数组');
  } else {
    input.agenda_items.forEach((item, idx) => {
      if (!item || typeof item !== 'string' || !item.trim()) {
        errors.push(`agenda_items[${idx}] 不能为空字符串`);
      }
    });
  }

  // discussion_summary — 非空对象数组
  if (!Array.isArray(input.discussion_summary) || input.discussion_summary.length === 0) {
    errors.push('discussion_summary 为必填字段，不能为空数组');
  } else {
    input.discussion_summary.forEach((item, idx) => {
      if (
        !item.agenda_item ||
        typeof item.agenda_item !== 'string' ||
        !item.agenda_item.trim()
      ) {
        errors.push(`discussion_summary[${idx}].agenda_item 为必填字段，不能为空`);
      }
      if (
        !item.key_points ||
        typeof item.key_points !== 'string' ||
        !item.key_points.trim()
      ) {
        errors.push(`discussion_summary[${idx}].key_points 为必填字段，不能为空`);
      }
      // resolution — 可选，但若填写不能是空字符串
      if (item.resolution !== undefined && item.resolution !== null) {
        if (typeof item.resolution !== 'string' || !item.resolution.trim()) {
          errors.push(`discussion_summary[${idx}].resolution 若填写，不能为空字符串`);
        }
      }
    });
  }

  // action_items — 可选，若填写则校验子字段
  if (Array.isArray(input.action_items) && input.action_items.length > 0) {
    input.action_items.forEach((item, idx) => {
      if (!item.task || typeof item.task !== 'string' || !item.task.trim()) {
        errors.push(`action_items[${idx}].task 为必填字段，不能为空`);
      }
      if (!item.responsible || typeof item.responsible !== 'string' || !item.responsible.trim()) {
        errors.push(`action_items[${idx}].responsible 为必填字段，不能为空`);
      }
      // deadline — 可选，格式 YYYY-MM-DD
      if (item.deadline !== undefined && item.deadline !== null) {
        const datePattern = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
        if (
          typeof item.deadline !== 'string' ||
          !datePattern.test(item.deadline.trim())
        ) {
          errors.push(
            `action_items[${idx}].deadline 格式不正确："${item.deadline}"，期望格式：YYYY-MM-DD`,
          );
        }
      }
    });
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 4. 公函/感谢信专用校验
// -----------------------------------------------------------------------

/**
 * 校验公函/感谢信专用字段。
 * 应在 document_type === 'letter' 时调用。
 *
 * 适用 document_subtype：
 *   govt_letter（致政府部门的公函）
 *   thanks_letter_funder（致资助方/合作伙伴的感谢信）
 *   thanks_letter_donor（致捐赠企业/个人的感谢信）
 *
 * 合规说明（Spec §输入校验）：
 *   - govt_letter 固定使用 formal 语气，tone=warm 不允许（error，阻断）
 *   - govt_letter 时 recipient_org 应包含政府部门标识词（warning，不阻断）
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateOfficialLetterInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // recipient_org — 必填，非空字符串
  if (
    !input.recipient_org ||
    typeof input.recipient_org !== 'string' ||
    !input.recipient_org.trim()
  ) {
    errors.push('recipient_org 为必填字段，不能为空');
  }

  // letter_purpose — 必填，50-200 字
  if (
    !input.letter_purpose ||
    typeof input.letter_purpose !== 'string' ||
    !input.letter_purpose.trim()
  ) {
    errors.push('letter_purpose 为必填字段，不能为空');
  } else {
    const len = input.letter_purpose.trim().length;
    if (len < 50) {
      errors.push(`letter_purpose 不能少于 50 个字符，当前：${len} 个字符`);
    } else if (len > 200) {
      errors.push(`letter_purpose 不能超过 200 个字符，当前：${len} 个字符`);
    }
  }

  // key_content — 必填，100-500 字
  if (
    !input.key_content ||
    typeof input.key_content !== 'string' ||
    !input.key_content.trim()
  ) {
    errors.push('key_content 为必填字段，不能为空');
  } else {
    const len = input.key_content.trim().length;
    if (len < 100) {
      errors.push(`key_content 不能少于 100 个字符，当前：${len} 个字符`);
    } else if (len > 500) {
      errors.push(`key_content 不能超过 500 个字符，当前：${len} 个字符`);
    }
  }

  // tone — 可选，enum
  const validTones = ['formal', 'warm', 'mixed'];
  if (input.tone !== undefined && input.tone !== null) {
    if (!validTones.includes(input.tone)) {
      errors.push(
        `tone 值无效："${input.tone}"，有效值为：${validTones.join('/')}`,
      );
    }
    // govt_letter 固定使用 formal（Spec §公函语气注意事项）
    if (input.document_subtype === 'govt_letter' && input.tone !== 'formal') {
      errors.push(
        'document_subtype=govt_letter 时，tone 必须为 formal（政府公函格式有明确公文规范要求）',
      );
    }
  }

  // govt_letter 专项：recipient_org 应含政府部门标识词（warning，不阻断）
  if (input.document_subtype === 'govt_letter' && input.recipient_org) {
    const deptKeywords = ['局', '委', '办', '部', '厅', '署', '院', '所', '处', '科'];
    const hasDeptKeyword = deptKeywords.some((kw) => input.recipient_org.includes(kw));
    if (!hasDeptKeyword) {
      warnings.push(
        `收件方"${input.recipient_org}"未包含政府部门标识词（局/委/办/部等），` +
          '请确认收件方是否为政府部门？政府公函格式与普通函件不同。',
      );
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 5. 感谢信专用校验（thanks_letter_funder / thanks_letter_donor）
// -----------------------------------------------------------------------

/**
 * 校验感谢信额外专用字段。
 * 应在 document_subtype 为 thanks_letter_funder 或 thanks_letter_donor 时，
 * 在 validateOfficialLetterInput 之后调用。
 *
 * PII 合规：
 *   recipient_title 中不应出现个人真实姓名，只允许职务称谓（warning，不阻断）
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateThankYouLetterInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // funding_amount_ref — 可选，若填写则触发金额确认提示（warning，不阻断）
  if (input.funding_amount_ref && typeof input.funding_amount_ref === 'string' && input.funding_amount_ref.trim()) {
    const amountPattern = /\d/;
    if (amountPattern.test(input.funding_amount_ref)) {
      warnings.push(
        `funding_amount_ref 中包含金额数字（"${input.funding_amount_ref}"）。` +
          '以上金额来源于您的填写，AI 不会修改，请确认金额准确性。',
      );
    }
  }

  // attachment_list — 可选，若填写则为非空字符串数组
  if (input.attachment_list !== undefined && input.attachment_list !== null) {
    if (!Array.isArray(input.attachment_list)) {
      errors.push('attachment_list 若填写，必须是数组');
    } else {
      input.attachment_list.forEach((item, idx) => {
        if (!item || typeof item !== 'string' || !item.trim()) {
          errors.push(`attachment_list[${idx}] 不能为空字符串`);
        }
      });
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 6. 工作计划/总结专用校验
// -----------------------------------------------------------------------

/**
 * 校验工作计划/总结专用字段。
 * 应在 document_type === 'plan_summary' 时调用。
 *
 * 适用 document_subtype：
 *   work_plan（工作计划）
 *   work_summary（工作总结）
 *
 * 合规说明：
 *   - work_summary + annual → 触发报告助手引导提示（warning，不阻断）
 *   - work_items[].target 含数字时触发数字来源确认（warning，不阻断）
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateWorkPlanInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // period_type — enum: annual / quarterly / monthly
  const validPeriodTypes = ['annual', 'quarterly', 'monthly'];
  if (!input.period_type) {
    errors.push('period_type 为必填字段');
  } else if (!validPeriodTypes.includes(input.period_type)) {
    errors.push(
      `period_type 值无效："${input.period_type}"，有效值为：${validPeriodTypes.join('/')}`,
    );
  }

  // period_year — 必填，合理整数（1900-2100）
  if (input.period_year === undefined || input.period_year === null) {
    errors.push('period_year 为必填字段');
  } else {
    const year = Number(input.period_year);
    if (!Number.isInteger(year) || year < 1900 || year > 2100) {
      errors.push(`period_year 必须是合理年份（1900-2100），当前：${input.period_year}`);
    }
  }

  // period_quarter — 条件必填（period_type=quarterly 时必填，1-4）
  if (input.period_type === 'quarterly') {
    if (input.period_quarter === undefined || input.period_quarter === null) {
      errors.push('period_type=quarterly 时，period_quarter 为必填字段');
    } else {
      const q = Number(input.period_quarter);
      if (!Number.isInteger(q) || q < 1 || q > 4) {
        errors.push(`period_quarter 必须是 1-4 的整数，当前：${input.period_quarter}`);
      }
    }
  }

  // period_month — 条件必填（period_type=monthly 时必填，1-12）
  if (input.period_type === 'monthly') {
    if (input.period_month === undefined || input.period_month === null) {
      errors.push('period_type=monthly 时，period_month 为必填字段');
    } else {
      const m = Number(input.period_month);
      if (!Number.isInteger(m) || m < 1 || m > 12) {
        errors.push(`period_month 必须是 1-12 的整数，当前：${input.period_month}`);
      }
    }
  }

  // work_items — 非空对象数组
  if (!Array.isArray(input.work_items) || input.work_items.length === 0) {
    errors.push('work_items 为必填字段，不能为空数组');
  } else {
    input.work_items.forEach((item, idx) => {
      if (!item.area || typeof item.area !== 'string' || !item.area.trim()) {
        errors.push(`work_items[${idx}].area 为必填字段，不能为空`);
      }
      if (!item.content || typeof item.content !== 'string' || !item.content.trim()) {
        errors.push(`work_items[${idx}].content 为必填字段，不能为空`);
      }
      // status — work_summary 时必填
      if (input.document_subtype === 'work_summary') {
        const validStatuses = ['completed', 'in_progress', 'delayed', 'cancelled'];
        if (!item.status) {
          errors.push(`work_items[${idx}].status 在 document_subtype=work_summary 时为必填字段`);
        } else if (!validStatuses.includes(item.status)) {
          errors.push(
            `work_items[${idx}].status 值无效："${item.status}"，有效值为：${validStatuses.join('/')}`,
          );
        }
      }
      // target 含数字 → warning（数字来源确认）
      if (item.target && typeof item.target === 'string' && /\d/.test(item.target)) {
        warnings.push(
          `work_items[${idx}].target 中包含数字："${item.target}"。` +
            '以上成果数字来源于您的填写，AI 不会修改，请确认数字准确。',
        );
      }
    });
  }

  // next_steps — work_summary 时必填
  if (input.document_subtype === 'work_summary') {
    if (
      !input.next_steps ||
      typeof input.next_steps !== 'string' ||
      !input.next_steps.trim()
    ) {
      errors.push('document_subtype=work_summary 时，next_steps 为必填字段，不能为空');
    }
  }

  // org_mission_brief — 可选，若填写则 50-100 字
  if (input.org_mission_brief !== undefined && input.org_mission_brief !== null) {
    if (typeof input.org_mission_brief !== 'string' || !input.org_mission_brief.trim()) {
      errors.push('org_mission_brief 若填写，不能为空字符串');
    } else {
      const len = input.org_mission_brief.trim().length;
      if (len < 50) {
        errors.push(`org_mission_brief 若填写，不能少于 50 个字符，当前：${len} 个字符`);
      } else if (len > 100) {
        errors.push(`org_mission_brief 若填写，不能超过 100 个字符，当前：${len} 个字符`);
      }
    }
  }

  // work_summary + annual → 报告助手引导提示（warning，不阻断）
  if (input.document_subtype === 'work_summary' && input.period_type === 'annual') {
    warnings.push(
      '如果您需要向民政部门提交的正式年检报告，请使用报告助手；' +
        '如果是内部管理用途的年度工作总结，继续在这里完成即可。',
    );
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 7. PII 安全校验
// -----------------------------------------------------------------------

/**
 * PII 安全校验（文书助手版）。
 *
 * 合规依据：PIPL 第23/28条、未成年人保护法第72条、文书助手 Spec v1.0 §合规要求
 *
 * 标记字段：
 *   - contact_name / contact_phone → piiFields（禁止进入 Prompt）
 *
 * 检测逻辑：
 *   - attendees_desc / discussion_summary[].key_points 中疑似中文真实姓名
 *     （2-4字连续中文 + 上下文动词）→ 黄色 warning（不阻断）
 *   - contract 类型中的 party_b_name 若为自然人（2-4字中文）→ 提示 warning
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

  // 合同中自然人姓名标记为 PII（不入模型，用占位符替代）
  if (input.document_type === 'contract' && input.party_b_type === 'individual'
      && input.party_b_name && input.party_b_name.trim()) {
    piiFields.push('party_b_name');
    warnings.push(
      'party_b_name（个人姓名）已标记为敏感信息，不会发送至 AI 模型。' +
      '合同签署栏将显示占位符，请在打印版本中手动填写。',
    );
  }

  // 保守动词列表：高置信度的姓名引入动词（与 application-assistant 一致）
  const nameContextPattern = /[\u4e00-\u9fa5]{2,4}(?=是|叫|说|告诉|表示|介绍|反映|名叫|叫做)/g;

  // 检测 attendees_desc 中疑似中文真实姓名
  if (
    input.attendees_desc &&
    typeof input.attendees_desc === 'string' &&
    input.attendees_desc.trim()
  ) {
    const matches = input.attendees_desc.match(nameContextPattern);
    if (matches && matches.length > 0) {
      const uniqueMatches = [...new Set(matches)];
      warnings.push(
        `attendees_desc 中检测到疑似真实姓名：${uniqueMatches.join('、')}。` +
          '建议使用职位/角色描述代替真实姓名（如"理事长"、"项目主任"），以保护个人信息。',
      );
    }
  }

  // 检测 discussion_summary[].key_points 中疑似中文真实姓名
  if (Array.isArray(input.discussion_summary) && input.discussion_summary.length > 0) {
    input.discussion_summary.forEach((item, idx) => {
      if (!item.key_points || typeof item.key_points !== 'string') return;
      const matches = item.key_points.match(nameContextPattern);
      if (matches && matches.length > 0) {
        const uniqueMatches = [...new Set(matches)];
        warnings.push(
          `discussion_summary[${idx}].key_points 中检测到疑似真实姓名：${uniqueMatches.join('、')}。` +
            '建议使用职位/角色描述代替真实姓名，以保护个人信息。',
        );
      }
    });
  }

  // 检测合同 party_b_name 中疑似中文真实姓名（2-4字中文，提示核确认）
  if (
    input.document_type === 'contract' &&
    input.party_b_name &&
    typeof input.party_b_name === 'string' &&
    input.party_b_name.trim()
  ) {
    const chineseNamePattern = /^[\u4e00-\u9fa5]{2,4}$/;
    if (chineseNamePattern.test(input.party_b_name.trim())) {
      warnings.push(
        `party_b_name"${input.party_b_name}"疑似个人姓名。` +
          '合同中个人姓名是正常的，但请确认是否应使用机构名称而非个人姓名。',
      );
    }
  }

  return { piiFields, warnings };
}

// -----------------------------------------------------------------------
// 8. 总入口
// -----------------------------------------------------------------------

/**
 * 总校验入口。按顺序执行：
 * 1. 通用必填字段校验（validateCommonInput）
 * 2. 按 document_type 分发专项校验
 * 3. PII 安全校验（仅追加 warnings，不影响 valid）
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[], piiFields: string[] }}
 */
function validate(input) {
  const result = { valid: true, errors: [], warnings: [], piiFields: [] };

  // Step 1: 通用校验
  const commonResult = validateCommonInput(input);
  mergeResult(result, commonResult);

  // Step 2: 按 document_type 分发专项校验
  if (input && input.document_type) {
    switch (input.document_type) {
      case 'contract': {
        const r = validateContractInput(input);
        mergeResult(result, r);
        break;
      }
      case 'minutes': {
        const r = validateMeetingMinutesInput(input);
        mergeResult(result, r);
        break;
      }
      case 'letter': {
        const r = validateOfficialLetterInput(input);
        mergeResult(result, r);
        // 感谢信额外字段校验
        if (
          input.document_subtype === 'thanks_letter_funder' ||
          input.document_subtype === 'thanks_letter_donor'
        ) {
          const tr = validateThankYouLetterInput(input);
          mergeResult(result, tr);
        }
        break;
      }
      case 'plan_summary': {
        const r = validateWorkPlanInput(input);
        mergeResult(result, r);
        break;
      }
      default:
        // document_type 无效已在 validateCommonInput 中报告
        break;
    }
  }

  // Step 3: PII 安全校验（仅追加 warnings/piiFields，不影响 valid）
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
  validateContractInput,
  validateMeetingMinutesInput,
  validateOfficialLetterInput,
  validateThankYouLetterInput,
  validateWorkPlanInput,
  validatePIISafety,
  // 内部常量导出（供测试使用）
  VALID_SUBTYPES,
};
