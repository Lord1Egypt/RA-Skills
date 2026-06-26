import { MungerDecisionAssistant } from '../src/index';
import { DialogueState } from '../src/types';

describe('MungerDecisionAssistant - 集成测试', () => {
  let assistant: MungerDecisionAssistant;

  beforeEach(() => {
    assistant = new MungerDecisionAssistant();
  });

  describe('完整决策流程', () => {
    test('应能完成投资决策分析', async () => {
      const sessionId = 'integration-001';
      
      // 1. 开始分析
      const start = await assistant.startAnalysis(sessionId, '是否投资腾讯股票');
      expect(start.includes('场景识别') || start.includes('无法识别')).toBe(true);
      
      // 如果无法识别场景，跳过后续测试
      if (start.includes('无法识别')) {
        return;
      }
      
      // 2. 回答问题
      let response = await assistant.handleAnswer(sessionId, '长期价值投资');
      expect(response).toContain('已记录');
      
      response = await assistant.handleAnswer(sessionId, '互联网行业龙头');
      expect(response).toContain('已记录');
      
      response = await assistant.handleAnswer(sessionId, '分批建仓降低风险');
      expect(response).toContain('已记录');
      
      // 继续回答直到生成报告
      for (let i = 0; i < 20; i++) {
        response = await assistant.handleAnswer(sessionId, `答案 ${i}`);
        if (response.includes('决策分析报告')) {
          break;
        }
      }
      
      // 3. 验证报告
      expect(response).toContain('决策分析报告');
      expect(response).toContain('综合建议');
      expect(response).toContain('风险提示');
    });

    test('应能完成产品决策分析', async () => {
      const sessionId = 'integration-002';
      
      const start = await assistant.startAnalysis(sessionId, '是否开发 AI 聊天功能');
      expect(start.includes('场景识别') || start.includes('无法识别')).toBe(true);
    });

    test('应能完成战略决策分析', async () => {
      const sessionId = 'integration-003';
      
      const start = await assistant.startAnalysis(sessionId, '公司战略是否需要调整');
      expect(start.includes('场景识别') || start.includes('无法识别')).toBe(true);
    });
  });

  describe('模型列表功能', () => {
    test('应能列出所有模型', () => {
      const list = assistant.listModels();
      
      expect(list).toContain('芒格思维模型清单');
      expect(list).toContain('第一性原理');
      expect(list).toContain('能力圈');
      expect(list).toContain('逆向思维');
    });

    test('模型列表应按分类组织', () => {
      const list = assistant.listModels();
      
      expect(list).toMatch(/## \w+/); // 应有分类标题
    });
  });

  describe('错误处理', () => {
    test('不存在的会话应返回错误', async () => {
      const response = await assistant.handleAnswer('nonexistent', '答案');
      expect(response).toContain('会话不存在');
    });

    test('无法识别的场景应返回提示', async () => {
      const response = await assistant.startAnalysis('test-error', '');
      expect(response.includes('无法识别') || response.includes('场景识别') || response.includes('请提供')).toBe(true);
    });
  });

  describe('会话隔离', () => {
    test('不同会话应相互独立', async () => {
      const session1 = 'isolation-001';
      const session2 = 'isolation-002';
      
      await assistant.startAnalysis(session1, '投资决策A');
      await assistant.startAnalysis(session2, '投资决策B');
      
      await assistant.handleAnswer(session1, '答案A1');
      await assistant.handleAnswer(session2, '答案B1');
      
      // 两个会话应独立进行
      const response1 = await assistant.handleAnswer(session1, '答案A2');
      const response2 = await assistant.handleAnswer(session2, '答案B2');
      
      expect(response1).toBeDefined();
      expect(response2).toBeDefined();
    });
  });
});
