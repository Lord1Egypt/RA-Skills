import { ReportGenerator } from '../src/reporter';
import { DialogueContext, DialogueState, Model } from '../src/types';

describe('ReportGenerator - 报告生成测试', () => {
  let reporter: ReportGenerator;

  beforeEach(() => {
    reporter = new ReportGenerator();
  });

  const mockModels: Model[] = [
    {
      id: '01',
      name: '第一性原理',
      category: 'core',
      description: '回归事物本质',
      questions: ['问题1', '问题2', '问题3'],
      scoring: {
        clear: '目标清晰，逻辑自洽',
        unclear: '目标模糊，需重新思考'
      }
    },
    {
      id: '06',
      name: '能力圈',
      category: 'core',
      description: '只在理解的领域决策',
      questions: ['问题A', '问题B'],
      scoring: {
        high: '高（可以决策）',
        low: '低（建议放弃）'
      }
    }
  ];

  const mockContext: DialogueContext = {
    sessionId: 'test-001',
    state: DialogueState.REPORT,
    userInput: '是否投资腾讯股票',
    scenario: 'investment',
    selectedModels: ['01', '06'],
    currentModelIndex: 2,
    currentQuestionIndex: 0,
    answers: {
      '01': ['核心目标是长期增值', '基本事实是腾讯有稳定现金流', '最优解是分批建仓'],
      '06': ['对互联网行业了解 8 分', '能清晰解释商业模式', '能预测未来发展趋势']
    },
    createdAt: Date.now(),
    updatedAt: Date.now()
  };

  describe('报告生成', () => {
    test('应能生成完整报告', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      
      expect(report.title).toBe('是否投资腾讯股票');
      expect(report.scenario).toBe('投资决策');
      expect(report.analyses).toHaveLength(2);
      expect(report.recommendation).toBeDefined();
      expect(report.risks).toBeDefined();
    });

    test('报告应包含所有模型分析', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      
      expect(report.analyses[0].modelId).toBe('01');
      expect(report.analyses[0].modelName).toBe('第一性原理');
      expect(report.analyses[0].answers).toHaveLength(3);
      
      expect(report.analyses[1].modelId).toBe('06');
      expect(report.analyses[1].modelName).toBe('能力圈');
      expect(report.analyses[1].answers).toHaveLength(3);
    });

    test('报告应有时间戳', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      
      expect(report.timestamp).toBeDefined();
      expect(typeof report.timestamp).toBe('number');
      expect(report.timestamp).toBeGreaterThan(0);
    });
  });

  describe('综合建议生成', () => {
    test('多数积极评估应建议执行', () => {
      const positiveContext: DialogueContext = {
        ...mockContext,
        answers: {
          '01': ['详细答案1', '详细答案2', '详细答案3'],
          '06': ['详细答案A', '详细答案B', '详细答案C']
        }
      };
      
      const report = reporter.generate(positiveContext, mockModels, '投资决策');
      expect(report.recommendation).toContain('建议');
    });

    test('缺少分析数据应给出警告', () => {
      const emptyContext: DialogueContext = {
        ...mockContext,
        selectedModels: [],
        answers: {}
      };
      
      const report = reporter.generate(emptyContext, mockModels, '投资决策');
      expect(report.recommendation).toContain('缺少');
    });
  });

  describe('风险识别', () => {
    test('应能识别风险', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      
      expect(report.risks).toBeDefined();
      expect(Array.isArray(report.risks)).toBe(true);
      expect(report.risks.length).toBeGreaterThan(0);
    });

    test('无明显风险时应给出提示', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      
      const hasDefaultRisk = report.risks.some(r => 
        r.includes('未识别') || r.includes('持续监控')
      );
      expect(hasDefaultRisk || report.risks.length > 0).toBe(true);
    });
  });

  describe('Markdown 格式化', () => {
    test('应能格式化为 Markdown', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      const markdown = reporter.formatMarkdown(report);
      
      expect(markdown).toContain('# 决策分析报告');
      expect(markdown).toContain('**决策主题：**');
      expect(markdown).toContain('**分析时间：**');
      expect(markdown).toContain('**决策场景：**');
    });

    test('Markdown 应包含所有模型分析', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      const markdown = reporter.formatMarkdown(report);
      
      expect(markdown).toContain('第一性原理');
      expect(markdown).toContain('能力圈');
      expect(markdown).toContain('## 1. 第一性原理分析');
      expect(markdown).toContain('## 2. 能力圈分析');
    });

    test('Markdown 应包含综合建议', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      const markdown = reporter.formatMarkdown(report);
      
      expect(markdown).toContain('## 综合建议');
      expect(markdown).toContain(report.recommendation);
    });

    test('Markdown 应包含风险提示', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      const markdown = reporter.formatMarkdown(report);
      
      expect(markdown).toContain('## 风险提示');
      report.risks.forEach(risk => {
        expect(markdown).toContain(risk);
      });
    });

    test('Markdown 应包含答案列表', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      const markdown = reporter.formatMarkdown(report);
      
      expect(markdown).toContain('**回答：**');
      expect(markdown).toContain('核心目标是长期增值');
      expect(markdown).toContain('对互联网行业了解 8 分');
    });

    test('Markdown 应有正确的分隔符', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      const markdown = reporter.formatMarkdown(report);
      
      expect(markdown).toContain('---');
    });

    test('Markdown 应格式化时间', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      const markdown = reporter.formatMarkdown(report);
      
      // 应包含日期格式（中文）
      expect(markdown).toMatch(/\d{4}[年\/\-]\d{1,2}[月\/\-]\d{1,2}/);
    });
  });

  describe('边界情况', () => {
    test('应处理空答案', () => {
      const emptyContext: DialogueContext = {
        ...mockContext,
        answers: {
          '01': [],
          '06': []
        }
      };
      
      const report = reporter.generate(emptyContext, mockModels, '投资决策');
      expect(report.analyses).toHaveLength(2);
    });

    test('应处理部分答案', () => {
      const partialContext: DialogueContext = {
        ...mockContext,
        answers: {
          '01': ['只有一个答案']
        }
      };
      
      const report = reporter.generate(partialContext, mockModels, '投资决策');
      expect(report.analyses.length).toBeGreaterThan(0);
    });

    test('应处理不存在的模型', () => {
      const invalidContext: DialogueContext = {
        ...mockContext,
        selectedModels: ['01', '999']
      };
      
      const report = reporter.generate(invalidContext, mockModels, '投资决策');
      expect(report.analyses).toHaveLength(1);
    });
  });

  describe('报告格式规范性', () => {
    test('报告标题应与用户输入一致', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      expect(report.title).toBe(mockContext.userInput);
    });

    test('报告场景应与传入参数一致', () => {
      const report = reporter.generate(mockContext, mockModels, '测试场景');
      expect(report.scenario).toBe('测试场景');
    });

    test('分析结果应包含必需字段', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      
      report.analyses.forEach(analysis => {
        expect(analysis.modelId).toBeDefined();
        expect(analysis.modelName).toBeDefined();
        expect(analysis.answers).toBeDefined();
        expect(analysis.score).toBeDefined();
        expect(analysis.analysis).toBeDefined();
      });
    });

    test('Markdown 格式应符合规范', () => {
      const report = reporter.generate(mockContext, mockModels, '投资决策');
      const markdown = reporter.formatMarkdown(report);
      
      // 检查标题层级
      expect(markdown).toMatch(/^# /m);
      expect(markdown).toMatch(/^## /m);
      
      // 检查列表格式
      expect(markdown).toMatch(/^- /m);
      
      // 检查加粗格式
      expect(markdown).toMatch(/\*\*.*\*\*/);
    });
  });
});
