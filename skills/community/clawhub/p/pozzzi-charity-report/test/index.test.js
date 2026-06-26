'use strict';

// ---------------------------------------------------------------------------
// test/index.test.js — 报告助手 Skill 集成测试
//
// 测试策略：
//   - 所有外部依赖通过 jest.mock + 依赖注入隔离
//   - prompt-builder 用 jest.mock 替换（另一 agent 并行开发中）
//   - modelClient / storage 通过 options 依赖注入（mockModelClient / mockStorage）
//   - disclaimer-injector 用真实实现（纯函数，无 I/O）
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Mock prompt-builder（另一 agent 并行开发，不可直接 require 真实模块）
// ---------------------------------------------------------------------------
jest.mock('../src/prompt-builder', () => ({
  buildPrompt: jest.fn(() => [
    { role: 'system', content: '你是报告撰写专家，请根据以下信息生成年度工作报告。' },
    { role: 'user',   content: '请生成报告内容。' },
  ]),
  formatCurrency: jest.fn(n => `${n.toLocaleString('zh-CN')}元`),
}));

const { handleReport, regenerateSection, getMaxTokens } = require('../src/index');
const promptBuilder = require('../src/prompt-builder');

// ---------------------------------------------------------------------------
// 测试固件
// ---------------------------------------------------------------------------

/** 合法的最小 annual_work 输入 */
const VALID_ANNUAL_INPUT = {
  report_type:         'annual_work',
  org_name:            '示例公益基金会',
  org_registration_no: '5110000X1234567890',
  org_type:            '基金会',
  report_year:         2025,
  contact_name:        '张三',
  fiscal_year_start:   '2025-01-01',
  fiscal_year_end:     '2025-12-31',
  org_mission:         '致力于支持中西部地区农村留守儿童的教育事业，通过捐助学习用品、改善学习环境来推动教育公平与机会均等。',
  total_income:        500000,
  total_expenditure:   450000,
  income_breakdown:    [{ source: '捐款', amount: 500000 }],
  projects_list:       [{ name: '助学项目', description: '为山区儿童捐书' }],
  staff_fulltime:      5,
};

/** 合法的最小 project_final 输入（腾讯公益） */
const VALID_PROJECT_TENCENT_INPUT = {
  report_type:             'project_final',
  org_name:                '示例公益基金会',
  org_registration_no:     '5110000X1234567890',
  org_type:                '基金会',
  report_year:             2025,
  contact_name:            '李四',
  project_name:            '山村助学2025',
  funder_name:             '腾讯公益',
  funder_platform:         'tencent',
  tencent_project_id:      'TXGY-2025-001',
  project_start_date:      '2025-01-01',
  project_end_date:        '2025-12-31',
  total_budget:            200000,
  actual_expenditure:      190000,
  expenditure_breakdown:   [{ category: '物资', budgeted: 200000, actual: 190000, variance_reason: '节省物流费' }],
  target_indicators:       [{ indicator: '受益学生人数', target: 200, actual: 210, completion_rate: 105 }],
  activities_summary:      [{ name: '发书活动', date: '2025-06-01', description: '发放图书200册' }],
  challenges_and_response: '物流延迟，通过提前采购解决。',
};

/** 合法的最小 finance_final 输入 */
const VALID_FINANCE_INPUT = {
  report_type:         'finance_final',
  org_name:            '示例公益基金会',
  org_registration_no: '5110000X1234567890',
  org_type:            '基金会',
  report_year:         2025,
  contact_name:        '王五',
  project_name:        '山村助学2025',
  funder_name:         '腾讯公益',
  total_grant:         200000,
  total_expenditure:   190000,
  unexpended_balance:  10000,
  balance_handling:    'return',
  audit_required:      false,
  expenditure_detail:  [{ category: '物资', amount: 190000 }],
};

// ---------------------------------------------------------------------------
// Mock model client（依赖注入）
// ---------------------------------------------------------------------------

/** 标准 mock 模型响应（annual_work 场景） */
const MOCK_REPORT_CONTENT =
  '# 2025年度工作报告\n\n' +
  '## 一、组织基本信息\n\n本机构为示例公益基金会，致力于教育公益。\n\n' +
  '## 二、年度工作概述\n\n本年度共开展项目5个，受益群众3000人。\n\n' +
  '## 三、财务概况\n\n年度总收入500,000元，总支出450,000元。\n\n' +
  '## 四、挑战与应对\n\n面临资金短缺，通过募款解决。\n\n' +
  '## 五、展望\n\n明年计划扩大项目规模。';

function makeMockModelClient(overrides = {}) {
  return {
    chat: jest.fn().mockResolvedValue({
      content:  MOCK_REPORT_CONTENT,
      model:    'hunyuan-lite',
      provider: 'hunyuan',
      usage:    { promptTokens: 100, completionTokens: 500, totalTokens: 600 },
      degraded: false,
      ...overrides,
    }),
  };
}

/** Mock storage（依赖注入，使用内存实现） */
function makeMockStorage() {
  return {
    appendAuditLog: jest.fn().mockResolvedValue(undefined),
    appendHistory:  jest.fn().mockResolvedValue(undefined),
  };
}

// ---------------------------------------------------------------------------
// getMaxTokens — 独立单元测试
// ---------------------------------------------------------------------------

describe('getMaxTokens', () => {
  test('annual_work 返回 4000', () => {
    expect(getMaxTokens('annual_work')).toBe(4000);
  });

  test('project_final 返回 3000', () => {
    expect(getMaxTokens('project_final')).toBe(3000);
  });

  test('finance_final 返回 2000', () => {
    expect(getMaxTokens('finance_final')).toBe(2000);
  });

  test('未知类型返回 3000（默认值）', () => {
    expect(getMaxTokens('unknown_type')).toBe(3000);
  });
});

// ---------------------------------------------------------------------------
// handleReport — 核心流程测试
// ---------------------------------------------------------------------------

describe('handleReport', () => {
  let mockModelClient;
  let mockStorage;

  beforeEach(() => {
    jest.clearAllMocks();
    mockModelClient = makeMockModelClient();
    mockStorage     = makeMockStorage();
  });

  // -------------------------------------------------------------------------
  // F-01/F-02: 章节完整性
  // -------------------------------------------------------------------------
  describe('F-01/F-02: 章节完整性', () => {
    test('模型返回包含多章节的报告时，handleReport 成功返回 report', async () => {
      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(result.success).toBe(true);
      expect(typeof result.report).toBe('string');
      expect(result.report.length).toBeGreaterThan(0);
    });

    test('模型返回缺失章节的报告时，仍然成功（章节完整性由模型保证，Skill 不阻断）', async () => {
      // 返回只有一个章节的精简报告
      const sparseClient = makeMockModelClient({
        content: '## 一、组织基本信息\n\n只有这一章节。',
      });

      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: sparseClient,
        storage:     mockStorage,
      });

      expect(result.success).toBe(true);
      expect(result.report).toContain('一、组织基本信息');
    });
  });

  // -------------------------------------------------------------------------
  // F-03: 腾讯公益模板
  // -------------------------------------------------------------------------
  describe('F-03: 腾讯公益模板', () => {
    test('funder_platform=tencent 时 promptBuilder.buildPrompt 被调用并收到正确参数', async () => {
      await handleReport(VALID_PROJECT_TENCENT_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(promptBuilder.buildPrompt).toHaveBeenCalledTimes(1);
      // 第一个参数的 funder_platform 应为 'tencent'
      const calledInput = promptBuilder.buildPrompt.mock.calls[0][0];
      expect(calledInput.funder_platform).toBe('tencent');
    });

    test('modelType 参数正确透传给 buildPrompt', async () => {
      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
        modelType:   'deepseek',
      });

      expect(promptBuilder.buildPrompt).toHaveBeenCalledWith(
        expect.any(Object),
        'deepseek',
      );
    });
  });

  // -------------------------------------------------------------------------
  // F-08: AI 标识声明
  // -------------------------------------------------------------------------
  describe('F-08: AI 辅助生成声明', () => {
    test('返回的 report 包含 "AI 辅助生成声明"', async () => {
      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(result.report).toContain('AI 辅助生成声明');
    });

    test('report 头部和尾部各含一次声明（disclaimer-injector 双重注入）', async () => {
      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      // 头部：AI 辅助生成声明（blockquote 格式）
      const headerIndex = result.report.indexOf('AI 辅助生成声明');
      expect(headerIndex).toBeGreaterThanOrEqual(0);

      // 尾部：免责提示（---\n> ⚠️ 免责提示）
      const footerIndex = result.report.indexOf('⚠️ 免责提示');
      expect(footerIndex).toBeGreaterThan(headerIndex);
    });
  });

  // -------------------------------------------------------------------------
  // F-09: 免责提示
  // -------------------------------------------------------------------------
  describe('F-09: 免责提示', () => {
    test('report 包含 "仅供参考"', async () => {
      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(result.report).toContain('仅供参考');
    });

    test('report 包含 "请结合实际情况核实数据"', async () => {
      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(result.report).toContain('核实数据');
    });
  });

  // -------------------------------------------------------------------------
  // F-10: 日志写入
  // -------------------------------------------------------------------------
  describe('F-10: 日志写入', () => {
    test('handleReport 成功后 storage.appendAuditLog 被调用一次', async () => {
      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(mockStorage.appendAuditLog).toHaveBeenCalledTimes(1);
    });

    test('审计日志 entry 包含必要字段', async () => {
      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      const logEntry = mockStorage.appendAuditLog.mock.calls[0][0];
      expect(logEntry.org_name).toBe(VALID_ANNUAL_INPUT.org_name);
      expect(logEntry.report_type).toBe('annual_work');
      expect(logEntry.model_used).toBe('hunyuan-lite');
      expect(logEntry.success).toBe(true);
      expect(typeof logEntry.duration_ms).toBe('number');
    });

    test('审计日志 entry 不含 prompt 正文', async () => {
      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      const logEntry = mockStorage.appendAuditLog.mock.calls[0][0];
      // 不应含 prompt、messages、content 等敏感字段
      expect(logEntry).not.toHaveProperty('prompt');
      expect(logEntry).not.toHaveProperty('messages');
      expect(logEntry).not.toHaveProperty('content');
      expect(logEntry).not.toHaveProperty('report');
    });

    test('handleReport 成功后 storage.appendHistory 被调用一次', async () => {
      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(mockStorage.appendHistory).toHaveBeenCalledTimes(1);
    });

    test('history entry 包含 org_name / report_type / model_used / success / duration_ms', async () => {
      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      const [skillId, histEntry] = mockStorage.appendHistory.mock.calls[0];
      expect(skillId).toBe('report-assistant');
      expect(histEntry.org_name).toBe(VALID_ANNUAL_INPUT.org_name);
      expect(histEntry.report_type).toBe('annual_work');
      expect(histEntry.model_used).toBe('hunyuan-lite');
      expect(histEntry.success).toBe(true);
      expect(typeof histEntry.duration_ms).toBe('number');
    });
  });

  // -------------------------------------------------------------------------
  // F-14: 模型降级
  // -------------------------------------------------------------------------
  describe('F-14: 模型降级', () => {
    test('modelClient.chat 返回 degraded=true 时 metadata.degraded=true', async () => {
      const degradedClient = makeMockModelClient({ degraded: true, provider: 'deepseek' });

      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: degradedClient,
        storage:     mockStorage,
      });

      expect(result.success).toBe(true);
      expect(result.metadata.degraded).toBe(true);
    });
  });

  // -------------------------------------------------------------------------
  // metadata 字段完整性
  // -------------------------------------------------------------------------
  describe('metadata', () => {
    test('成功时 metadata 包含 model / provider / degraded / duration_ms / version', async () => {
      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(result.metadata).toMatchObject({
        model:    'hunyuan-lite',
        provider: 'hunyuan',
        degraded: false,
        version:  '1.0.0',
      });
      expect(typeof result.metadata.duration_ms).toBe('number');
      expect(result.metadata.duration_ms).toBeGreaterThanOrEqual(0);
    });
  });

  // -------------------------------------------------------------------------
  // 错误处理
  // -------------------------------------------------------------------------
  describe('错误处理', () => {
    test('输入校验失败（valid=false）→ 返回 { success: false, errors }', async () => {
      const invalidInput = { report_type: 'annual_work' }; // 缺失大量必填字段

      const result = await handleReport(invalidInput, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(result.success).toBe(false);
      expect(Array.isArray(result.errors)).toBe(true);
      expect(result.errors.length).toBeGreaterThan(0);
      // 校验失败时不应调用模型
      expect(mockModelClient.chat).not.toHaveBeenCalled();
    });

    test('validators 返回 warnings 时记录但不阻断', async () => {
      // 完成率 > 150% 会产生 warning
      const inputWithWarning = {
        ...VALID_PROJECT_TENCENT_INPUT,
        target_indicators: [
          { indicator: '受益人数', target: 100, actual: 200, completion_rate: 200 },
        ],
      };

      const result = await handleReport(inputWithWarning, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(result.success).toBe(true);
      expect(Array.isArray(result.warnings)).toBe(true);
      expect(result.warnings.some(w => w.includes('完成率') || w.includes('200%'))).toBe(true);
    });

    test('modelClient.chat 抛出 PII detected → 返回 { success: false, errors: ["PII detected..."] }', async () => {
      const piiError = new Error('model-gateway: PII detected in input, request blocked');
      const piiClient = { chat: jest.fn().mockRejectedValue(piiError) };

      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: piiClient,
        storage:     mockStorage,
      });

      expect(result.success).toBe(false);
      expect(result.errors[0]).toContain('PII detected');
    });

    test('modelClient.chat 抛出网络错误 → 返回 { success: false, errors: ["..."] }', async () => {
      const networkError = new Error('connect ETIMEDOUT api.hunyuan.cloud.tencent.com:443');
      const failClient   = { chat: jest.fn().mockRejectedValue(networkError) };

      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: failClient,
        storage:     mockStorage,
      });

      expect(result.success).toBe(false);
      expect(Array.isArray(result.errors)).toBe(true);
      expect(result.errors[0]).toContain('ETIMEDOUT');
    });

    test('模型调用失败时仍会写入失败的审计日志', async () => {
      const failClient = { chat: jest.fn().mockRejectedValue(new Error('网络超时')) };

      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: failClient,
        storage:     mockStorage,
      });

      expect(mockStorage.appendAuditLog).toHaveBeenCalledTimes(1);
      const logEntry = mockStorage.appendAuditLog.mock.calls[0][0];
      expect(logEntry.success).toBe(false);
    });

    test('storage.appendAuditLog 抛出错误时不影响主流程（容错）', async () => {
      const brokenStorage = {
        appendAuditLog: jest.fn().mockRejectedValue(new Error('磁盘已满')),
        appendHistory:  jest.fn().mockResolvedValue(undefined),
      };

      // 主流程应正常返回，不因日志写入失败而抛出
      const result = await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     brokenStorage,
      });

      expect(result.success).toBe(true);
    });

    test('finance_final 报告类型正常处理', async () => {
      const result = await handleReport(VALID_FINANCE_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      expect(result.success).toBe(true);
      // maxTokens 应为 2000
      const chatOptions = mockModelClient.chat.mock.calls[0][1];
      expect(chatOptions.maxTokens).toBe(2000);
    });

    test('annual_work maxTokens 传递 4000', async () => {
      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      const chatOptions = mockModelClient.chat.mock.calls[0][1];
      expect(chatOptions.maxTokens).toBe(4000);
    });

    test('temperature 固定为 0.3', async () => {
      await handleReport(VALID_ANNUAL_INPUT, {
        modelClient: mockModelClient,
        storage:     mockStorage,
      });

      const chatOptions = mockModelClient.chat.mock.calls[0][1];
      expect(chatOptions.temperature).toBe(0.3);
    });
  });
});

// ---------------------------------------------------------------------------
// regenerateSection — 单章节重生成
// ---------------------------------------------------------------------------

describe('regenerateSection', () => {
  let mockModelClient;
  let mockStorage;

  // 包含 disclaimer 的完整报告（handleReport 输出格式）
  let previousReport;

  beforeEach(() => {
    jest.clearAllMocks();
    mockModelClient = makeMockModelClient({
      content:  '## 二、年度工作概述\n\n（重生成版本）本年度完成项目7个，受益群众5000人。',
      model:    'hunyuan-lite',
      provider: 'hunyuan',
      degraded: false,
    });
    mockStorage = makeMockStorage();

    // 模拟 handleReport 产出的完整报告（带 disclaimer）
    const { injectDisclaimer } = require('../../../packages/shared/disclaimer-injector');
    const { content } = injectDisclaimer(MOCK_REPORT_CONTENT, {
      format:    'markdown',
      skillName: '报告助手',
      modelName: 'hunyuan',
    });
    previousReport = content;
  });

  // -------------------------------------------------------------------------
  // F-13: 单章节重生成
  // -------------------------------------------------------------------------
  describe('F-13: 单章节重生成', () => {
    test('只重新调用一次模型', async () => {
      await regenerateSection(
        VALID_ANNUAL_INPUT,
        '年度工作概述',
        previousReport,
        { modelClient: mockModelClient, storage: mockStorage },
      );

      expect(mockModelClient.chat).toHaveBeenCalledTimes(1);
    });

    test('返回的报告中指定章节内容已更新', async () => {
      const result = await regenerateSection(
        VALID_ANNUAL_INPUT,
        '年度工作概述',
        previousReport,
        { modelClient: mockModelClient, storage: mockStorage },
      );

      expect(result.success).toBe(true);
      expect(result.report).toContain('重生成版本');
    });

    test('返回的报告包含 disclaimer（重新注入）', async () => {
      const result = await regenerateSection(
        VALID_ANNUAL_INPUT,
        '年度工作概述',
        previousReport,
        { modelClient: mockModelClient, storage: mockStorage },
      );

      expect(result.report).toContain('AI 辅助生成声明');
      expect(result.report).toContain('仅供参考');
    });

    test('其他章节内容在原报告中仍然存在（不被清除）', async () => {
      const result = await regenerateSection(
        VALID_ANNUAL_INPUT,
        '年度工作概述',
        previousReport,
        { modelClient: mockModelClient, storage: mockStorage },
      );

      // 其他章节：一、三、四、五 应仍存在
      expect(result.report).toContain('一、组织基本信息');
      expect(result.report).toContain('三、财务概况');
    });

    test('sectionName 为空时返回 { success: false, errors }', async () => {
      const result = await regenerateSection(
        VALID_ANNUAL_INPUT,
        '',
        previousReport,
        { modelClient: mockModelClient, storage: mockStorage },
      );

      expect(result.success).toBe(false);
      expect(result.errors[0]).toContain('sectionName');
    });

    test('previousReport 为空时返回 { success: false, errors }', async () => {
      const result = await regenerateSection(
        VALID_ANNUAL_INPUT,
        '年度工作概述',
        null,
        { modelClient: mockModelClient, storage: mockStorage },
      );

      expect(result.success).toBe(false);
      expect(result.errors[0]).toContain('previousReport');
    });
  });

  // -------------------------------------------------------------------------
  // F-14: 降级透传
  // -------------------------------------------------------------------------
  describe('F-14: 模型降级透传', () => {
    test('模型降级时 metadata.degraded=true', async () => {
      const degradedClient = makeMockModelClient({
        content:  '## 二、年度工作概述\n\n降级版本内容。',
        degraded: true,
        provider: 'deepseek',
      });

      const result = await regenerateSection(
        VALID_ANNUAL_INPUT,
        '年度工作概述',
        previousReport,
        { modelClient: degradedClient, storage: mockStorage },
      );

      expect(result.success).toBe(true);
      expect(result.metadata.degraded).toBe(true);
    });
  });

  // -------------------------------------------------------------------------
  // 错误处理
  // -------------------------------------------------------------------------
  describe('错误处理', () => {
    test('modelClient.chat 抛出错误时返回 { success: false, errors }', async () => {
      const failClient = { chat: jest.fn().mockRejectedValue(new Error('API 不可用')) };

      const result = await regenerateSection(
        VALID_ANNUAL_INPUT,
        '年度工作概述',
        previousReport,
        { modelClient: failClient, storage: mockStorage },
      );

      expect(result.success).toBe(false);
      expect(result.errors[0]).toContain('API 不可用');
    });

    test('章节在原报告中不存在时，新内容追加到末尾，带 warning', async () => {
      const result = await regenerateSection(
        VALID_ANNUAL_INPUT,
        '不存在的章节名称',
        previousReport,
        { modelClient: mockModelClient, storage: mockStorage },
      );

      // 应成功，且有 warning 提示
      expect(result.success).toBe(true);
      expect(result.warnings.length).toBeGreaterThan(0);
      expect(result.report).toContain('重生成版本');
    });
  });
});
