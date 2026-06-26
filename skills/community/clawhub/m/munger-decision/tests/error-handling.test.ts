import { MungerDecisionAssistant } from '../src/index';
import { ScenarioDetector } from '../src/detector';
import { ModelRecommender } from '../src/recommender';

describe('错误处理测试', () => {
  let assistant: MungerDecisionAssistant;

  beforeEach(() => {
    assistant = new MungerDecisionAssistant();
  });

  describe('输入验证', () => {
    test('应拒绝空字符串', async () => {
      const result = await assistant.startAnalysis('user123', '');
      expect(result).toContain('❌');
      expect(result).toContain('请提供决策问题');
    });

    test('应拒绝纯空白字符', async () => {
      const result = await assistant.startAnalysis('user123', '   \n\t  ');
      expect(result).toContain('❌');
    });

    test('应处理 null 会话 ID', async () => {
      const result = await assistant.handleAnswer('', '答案');
      expect(result).toContain('❌');
      expect(result).toContain('会话不存在');
    });

    test('应处理不存在的会话', async () => {
      const result = await assistant.handleAnswer('nonexistent-session', '答案');
      expect(result).toContain('❌');
      expect(result).toContain('会话不存在');
    });

    test('应处理特殊字符输入', async () => {
      const result = await assistant.startAnalysis('user123', '!@#$%^&*()');
      expect(result).toBeDefined();
      expect(result.length).toBeGreaterThan(0);
    });

    test('应处理超长输入', async () => {
      const longInput = 'a'.repeat(10000);
      const result = await assistant.startAnalysis('user123', longInput);
      expect(result).toBeDefined();
    });

    test('应处理 Unicode 字符', async () => {
      const result = await assistant.startAnalysis('user123', '投资决策 🚀 📈 💰');
      expect(result).toBeDefined();
      expect(result).toContain('场景识别');
    });

    test('应处理 HTML 标签', async () => {
      const result = await assistant.startAnalysis('user123', '<script>alert("test")</script>投资决策');
      expect(result).toBeDefined();
    });
  });

  describe('场景识别错误处理', () => {
    test('应处理无法识别的场景', async () => {
      const detector = new ScenarioDetector();
      const result = await detector.detect('今天天气怎么样？');
      expect(result.scenarioId).toBe('general');
      expect(result.suggestedModels.length).toBeGreaterThan(0);
    });

    test('应处理空输入', async () => {
      const detector = new ScenarioDetector();
      const result = await detector.detect('');
      expect(result.scenarioId).toBe('general');
    });

    test('应处理纯数字输入', async () => {
      const detector = new ScenarioDetector();
      const result = await detector.detect('123456');
      expect(result.scenarioId).toBe('general');
    });

    test('应处理纯符号输入', async () => {
      const detector = new ScenarioDetector();
      const result = await detector.detect('!@#$%^&*()');
      expect(result.scenarioId).toBe('general');
    });
  });

  describe('模型推荐错误处理', () => {
    test('应处理空模型 ID 列表', () => {
      const recommender = new ModelRecommender();
      const models = recommender.recommend([]);
      expect(models).toEqual([]);
    });

    test('应过滤不存在的模型 ID', () => {
      const recommender = new ModelRecommender();
      const models = recommender.recommend(['06', '999', '07', '888']);
      expect(models.length).toBe(2);
      expect(models[0].id).toBe('06');
      expect(models[1].id).toBe('07');
    });

    test('应处理重复的模型 ID', () => {
      const recommender = new ModelRecommender();
      const models = recommender.recommend(['06', '06', '06']);
      expect(models.length).toBe(3);
      expect(models[0].id).toBe('06');
    });

    test('应处理大小写混合的模型 ID', () => {
      const recommender = new ModelRecommender();
      const models = recommender.recommend(['06', '06', '06']);
      expect(models.length).toBe(3);
    });

    test('应处理带空格的模型 ID', () => {
      const recommender = new ModelRecommender();
      const models = recommender.recommend([' 06 ', '  07  ']);
      expect(models.length).toBe(2);
    });

    test('应处理 undefined 模型查询', () => {
      const recommender = new ModelRecommender();
      const model = recommender.getModel('999');
      expect(model).toBeUndefined();
    });
  });

  describe('会话管理错误处理', () => {
    test('应处理重复开始分析', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      const result = await assistant.startAnalysis('user123', '产品决策');
      expect(result).toContain('场景识别');
      expect(result).toContain('产品决策');
    });

    test('应处理并发会话', async () => {
      const promises = [];
      for (let i = 0; i < 10; i++) {
        promises.push(assistant.startAnalysis(`user${i}`, '投资决策'));
      }
      const results = await Promise.all(promises);
      results.forEach(result => {
        expect(result).toContain('场景识别');
      });
    });

    test('应处理快速连续的回答', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      
      const promises = [];
      for (let i = 0; i < 5; i++) {
        promises.push(assistant.handleAnswer('user123', `答案${i}`));
      }
      
      const results = await Promise.all(promises);
      results.forEach(result => {
        expect(result).toBeDefined();
      });
    });
  });

  describe('边界情况处理', () => {
    test('应处理极短输入', async () => {
      const result = await assistant.startAnalysis('user123', 'a');
      expect(result).toBeDefined();
    });

    test('应处理单个字符', async () => {
      const result = await assistant.startAnalysis('user123', '投');
      expect(result).toBeDefined();
    });

    test('应处理纯空格答案', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      const result = await assistant.handleAnswer('user123', '   ');
      expect(result).toBeDefined();
    });

    test('应处理空答案', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      const result = await assistant.handleAnswer('user123', '');
      expect(result).toBeDefined();
    });

    test('应处理超长答案', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      const longAnswer = 'a'.repeat(10000);
      const result = await assistant.handleAnswer('user123', longAnswer);
      expect(result).toBeDefined();
    });
  });

  describe('异常恢复测试', () => {
    test('应从无效场景恢复', async () => {
      const result1 = await assistant.startAnalysis('user123', '无法识别的输入');
      expect(result1).toBeDefined();
      
      const result2 = await assistant.startAnalysis('user123', '投资决策');
      expect(result2).toContain('场景识别');
    });

    test('应从会话错误恢复', async () => {
      const result1 = await assistant.handleAnswer('nonexistent', '答案');
      expect(result1).toContain('❌');
      
      const result2 = await assistant.startAnalysis('user123', '投资决策');
      expect(result2).toContain('场景识别');
    });

    test('应支持会话重启', async () => {
      await assistant.startAnalysis('user123', '投资决策');
      await assistant.handleAnswer('user123', '答案1');
      
      // 重新开始
      const result = await assistant.startAnalysis('user123', '产品决策');
      expect(result).toContain('场景识别');
      expect(result).toContain('产品决策');
    });
  });

  describe('性能降级测试', () => {
    test('应处理大量并发请求', async () => {
      const promises = [];
      for (let i = 0; i < 100; i++) {
        promises.push(assistant.startAnalysis(`user${i}`, '投资决策'));
      }
      
      const start = Date.now();
      const results = await Promise.all(promises);
      const duration = Date.now() - start;
      
      expect(results.length).toBe(100);
      expect(duration).toBeLessThan(5000); // 5 秒内完成
    });

    test('应处理快速连续请求', async () => {
      const start = Date.now();
      
      for (let i = 0; i < 50; i++) {
        await assistant.startAnalysis(`user${i}`, '投资决策');
      }
      
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(3000); // 3 秒内完成
    });
  });

  describe('数据完整性测试', () => {
    test('错误不应破坏后续操作', async () => {
      // 触发错误
      await assistant.handleAnswer('nonexistent', '答案');
      
      // 正常操作应该成功
      const result = await assistant.startAnalysis('user123', '投资决策');
      expect(result).toContain('场景识别');
    });

    test('无效输入不应影响缓存', async () => {
      const recommender = new ModelRecommender();
      
      // 无效查询
      recommender.getModel('999');
      
      // 有效查询应该成功
      const model = recommender.getModel('06');
      expect(model).toBeDefined();
      expect(model?.name).toBe('能力圈');
    });

    test('并发错误不应相互影响', async () => {
      const promises = [
        assistant.handleAnswer('nonexistent1', '答案'),
        assistant.startAnalysis('user1', '投资决策'),
        assistant.handleAnswer('nonexistent2', '答案'),
        assistant.startAnalysis('user2', '产品决策'),
      ];
      
      const results = await Promise.all(promises);
      
      expect(results[0]).toContain('❌');
      expect(results[1]).toContain('场景识别');
      expect(results[2]).toContain('❌');
      expect(results[3]).toContain('场景识别');
    });
  });
});
