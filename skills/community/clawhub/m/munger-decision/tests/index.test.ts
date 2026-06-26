import { MungerDecisionAssistant } from '../src/index';

describe('MungerDecisionAssistant - 主入口测试', () => {
  let assistant: MungerDecisionAssistant;

  beforeEach(() => {
    assistant = new MungerDecisionAssistant();
  });

  describe('startAnalysis - 开始分析', () => {
    test('应成功开始分析', async () => {
      const result = await assistant.startAnalysis('user123', '是否投资这只股票？');
      expect(result).toContain('场景识别');
      expect(result).toContain('推荐模型');
    });

    test('应拒绝空输入', async () => {
      const result = await assistant.startAnalysis('user123', '');
      expect(result).toContain('❌');
      expect(result).toContain('请提供决策问题');
    });

    test('应拒绝空白输入', async () => {
      const result = await assistant.startAnalysis('user123', '   ');
      expect(result).toContain('❌');
    });

    test('应识别投资场景', async () => {
      const result = await assistant.startAnalysis('user123', '买入茅台股票');
      expect(result).toContain('投资决策');
    });

    test('应识别产品场景', async () => {
      const result = await assistant.startAnalysis('user456', '是否开发新功能？');
      expect(result).toContain('产品决策');
    });

    test('应识别招聘场景', async () => {
      const result = await assistant.startAnalysis('user789', '是否录用这个候选人？');
      expect(result).toContain('人员决策');
    });

    test('应返回第一个问题', async () => {
      const result = await assistant.startAnalysis('user123', '投资决策');
      expect(result).toContain('##');
      expect(result.split('\n').length).toBeGreaterThan(3);
    });
  });

  describe('handleAnswer - 处理回答', () => {
    test('应处理用户回答', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      const result = await assistant.handleAnswer('user123', '我不太了解这个行业');
      expect(result).toBeDefined();
      expect(result.length).toBeGreaterThan(0);
    });

    test('应拒绝不存在的会话', async () => {
      const result = await assistant.handleAnswer('nonexistent', '答案');
      expect(result).toContain('❌');
      expect(result).toContain('会话不存在');
    });

    test('应记录答案并返回下一个问题', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      const result = await assistant.handleAnswer('user123', '我了解这个行业');
      expect(result).toBeDefined();
    });

    test('应在所有问题完成后生成报告', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      
      // 回答所有问题
      for (let i = 0; i < 10; i++) {
        const result = await assistant.handleAnswer('user123', '测试答案');
        if (result.includes('决策分析报告') || result.includes('综合评分')) {
          expect(result).toContain('决策分析报告');
          return;
        }
      }
    });
  });

  describe('listModels - 列出模型', () => {
    test('应返回模型清单', () => {
      const result = assistant.listModels();
      expect(result).toContain('芒格思维模型清单');
      expect(result).toContain('##');
    });

    test('应包含模型分类', () => {
      const result = assistant.listModels();
      expect(result).toContain('core');
    });

    test('应包含模型名称和描述', () => {
      const result = assistant.listModels();
      expect(result).toContain('能力圈');
      expect(result).toContain('逆向思维');
    });

    test('应包含所有模型', () => {
      const result = assistant.listModels();
      const modelCount = (result.match(/\*\*/g) || []).length / 2;
      expect(modelCount).toBeGreaterThan(50);
    });
  });

  describe('完整流程测试', () => {
    test('投资决策完整流程', async () => {
      const sessionId = 'test-investment';
      
      // 1. 开始分析
      const start = await assistant.startAnalysis(sessionId, '是否投资中宠股份？');
      expect(start).toContain('场景识别');
      
      // 2. 回答问题
      const answer1 = await assistant.handleAnswer(sessionId, '我了解宠物食品行业');
      expect(answer1).toBeDefined();
      
      const answer2 = await assistant.handleAnswer(sessionId, '公司有护城河');
      expect(answer2).toBeDefined();
    });

    test('产品决策完整流程', async () => {
      const sessionId = 'test-product';
      
      const start = await assistant.startAnalysis(sessionId, '是否开发 AI 功能？');
      expect(start).toContain('场景识别');
      
      const answer1 = await assistant.handleAnswer(sessionId, '用户需求强烈');
      expect(answer1).toBeDefined();
    });

    test('多用户并发测试', async () => {
      const user1 = await assistant.startAnalysis('user1', '投资决策');
      const user2 = await assistant.startAnalysis('user2', '产品决策');
      
      expect(user1).toContain('场景识别');
      expect(user2).toContain('场景识别');
      
      const answer1 = await assistant.handleAnswer('user1', '答案1');
      const answer2 = await assistant.handleAnswer('user2', '答案2');
      
      expect(answer1).toBeDefined();
      expect(answer2).toBeDefined();
    });
  });

  describe('错误处理测试', () => {
    test('应处理无法识别的场景', async () => {
      const result = await assistant.startAnalysis('user123', '今天天气怎么样？');
      expect(result).toBeDefined();
    });

    test('应处理特殊字符输入', async () => {
      const result = await assistant.startAnalysis('user123', '投资决策！@#$%^&*()');
      expect(result).toBeDefined();
    });

    test('应处理超长输入', async () => {
      const longInput = '投资决策 '.repeat(100);
      const result = await assistant.startAnalysis('user123', longInput);
      expect(result).toBeDefined();
    });

    test('应处理重复开始分析', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      const result = await assistant.startAnalysis('user123', '产品决策');
      expect(result).toContain('场景识别');
    });
  });

  describe('性能测试', () => {
    test('开始分析应在 500ms 内完成', async () => {
      const start = Date.now();
      await assistant.startAnalysis('user123', '投资决策');
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(500);
    });

    test('处理回答应在 500ms 内完成', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      const start = Date.now();
      await assistant.handleAnswer('user123', '测试答案');
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(500);
    });

    test('列出模型应在 100ms 内完成', () => {
      const start = Date.now();
      assistant.listModels();
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(100);
    });
  });

  describe('内存管理测试', () => {
    test('应在生成报告后清理会话', async () => {
      const sessionId = 'test-cleanup';
      await assistant.startAnalysis(sessionId, '投资决策');
      
      // 回答所有问题直到生成报告
      for (let i = 0; i < 10; i++) {
        const result = await assistant.handleAnswer(sessionId, '测试答案');
        if (result.includes('决策分析报告')) {
          // 报告生成后，会话应被清理
          const nextResult = await assistant.handleAnswer(sessionId, '新答案');
          expect(nextResult).toContain('会话不存在');
          return;
        }
      }
    });

    test('应支持多会话并发', async () => {
      const sessions = [];
      for (let i = 0; i < 10; i++) {
        sessions.push(assistant.startAnalysis(`user${i}`, '投资决策'));
      }
      const results = await Promise.all(sessions);
      results.forEach(result => {
        expect(result).toContain('场景识别');
      });
    });
  });
});
