import { MungerDecisionAssistant } from '../src/index';
import { ScenarioDetector } from '../src/detector';
import { ModelRecommender } from '../src/recommender';
import { SmartRecommender } from '../src/smart-recommender';

describe('性能测试', () => {
  describe('响应时间测试', () => {
    test('开始分析应在 500ms 内完成', async () => {
      const assistant = new MungerDecisionAssistant();
      
      const start = Date.now();
      await assistant.startAnalysis('user123', '是否投资这只股票？');
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(500);
    });

    test('处理回答应在 500ms 内完成', async () => {
      const assistant = new MungerDecisionAssistant();
      await assistant.startAnalysis('user123', '投资决策');
      
      const start = Date.now();
      await assistant.handleAnswer('user123', '我了解这个行业');
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(500);
    });

    test('场景识别应在 200ms 内完成', async () => {
      const detector = new ScenarioDetector();
      
      const start = Date.now();
      await detector.detect('是否投资这只股票？');
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(200);
    });

    test('模型推荐应在 100ms 内完成', () => {
      const recommender = new ModelRecommender();
      
      const start = Date.now();
      recommender.recommend(['06', '07', '10', '31', '32']);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(100);
    });

    test('智能推荐应在 500ms 内完成', async () => {
      const recommender = new SmartRecommender();
      
      const start = Date.now();
      await recommender.analyzeAndScore('是否投资这只股票？', 'investment');
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(500);
    });

    test('列出模型应在 50ms 内完成', () => {
      const assistant = new MungerDecisionAssistant();
      
      const start = Date.now();
      assistant.listModels();
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(50);
    });
  });

  describe('批量操作性能', () => {
    test('10 次开始分析应在 3s 内完成', async () => {
      const assistant = new MungerDecisionAssistant();
      
      const start = Date.now();
      const promises = [];
      for (let i = 0; i < 10; i++) {
        promises.push(assistant.startAnalysis(`user${i}`, '投资决策'));
      }
      await Promise.all(promises);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(3000);
    });

    test('100 次场景识别应在 5s 内完成', async () => {
      const detector = new ScenarioDetector();
      
      const start = Date.now();
      const promises = [];
      for (let i = 0; i < 100; i++) {
        promises.push(detector.detect('投资决策'));
      }
      await Promise.all(promises);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(5000);
    });

    test('1000 次模型查询应在 500ms 内完成', () => {
      const recommender = new ModelRecommender();
      
      const start = Date.now();
      for (let i = 0; i < 1000; i++) {
        recommender.getModel('06');
      }
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(500);
    });

    test('100 次批量推荐应在 1s 内完成', () => {
      const recommender = new ModelRecommender();
      const modelIds = ['06', '07', '10', '31', '32'];
      
      const start = Date.now();
      for (let i = 0; i < 100; i++) {
        recommender.recommend(modelIds);
      }
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(1000);
    });

    test('50 次智能推荐应在 10s 内完成', async () => {
      const recommender = new SmartRecommender();
      
      const start = Date.now();
      const promises = [];
      for (let i = 0; i < 50; i++) {
        promises.push(recommender.analyzeAndScore('投资决策', 'investment'));
      }
      await Promise.all(promises);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(10000);
    });
  });

  describe('并发性能测试', () => {
    test('50 个并发会话应在 5s 内完成', async () => {
      const assistant = new MungerDecisionAssistant();
      
      const start = Date.now();
      const promises = [];
      for (let i = 0; i < 50; i++) {
        promises.push(assistant.startAnalysis(`user${i}`, '投资决策'));
      }
      await Promise.all(promises);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(5000);
    });

    test('100 个并发场景识别应在 10s 内完成', async () => {
      const detector = new ScenarioDetector();
      
      const start = Date.now();
      const promises = [];
      for (let i = 0; i < 100; i++) {
        promises.push(detector.detect(`投资决策 ${i}`));
      }
      await Promise.all(promises);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(10000);
    });

    test('并发查询不应相互阻塞', async () => {
      const assistant = new MungerDecisionAssistant();
      
      const start = Date.now();
      const promises = [
        assistant.startAnalysis('user1', '投资决策'),
        assistant.startAnalysis('user2', '产品决策'),
        assistant.startAnalysis('user3', '招聘决策'),
        assistant.startAnalysis('user4', '战略决策'),
        assistant.startAnalysis('user5', '投资决策'),
      ];
      await Promise.all(promises);
      const duration = Date.now() - start;
      
      // 5 个并发请求应该接近单次请求的时间
      expect(duration).toBeLessThan(1000);
    });
  });

  describe('内存性能测试', () => {
    test('创建 100 个实例应保持高性能', () => {
      const start = Date.now();
      
      for (let i = 0; i < 100; i++) {
        new MungerDecisionAssistant();
      }
      
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(500);
    });

    test('100 个会话不应导致性能下降', async () => {
      const assistant = new MungerDecisionAssistant();
      
      // 创建 100 个会话
      for (let i = 0; i < 100; i++) {
        await assistant.startAnalysis(`user${i}`, '投资决策');
      }
      
      // 测试最后一个会话的性能
      const start = Date.now();
      await assistant.handleAnswer('user99', '测试答案');
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(500);
    });

    test('缓存应减少重复加载时间', () => {
      const start1 = Date.now();
      new ModelRecommender();
      const duration1 = Date.now() - start1;
      
      const start2 = Date.now();
      new ModelRecommender();
      const duration2 = Date.now() - start2;
      
      // 第二次应该更快（使用缓存）
      expect(duration2).toBeLessThanOrEqual(duration1);
    });
  });

  describe('数据量性能测试', () => {
    test('处理长文本输入应保持高性能', async () => {
      const assistant = new MungerDecisionAssistant();
      const longInput = '投资决策 '.repeat(100);
      
      const start = Date.now();
      await assistant.startAnalysis('user123', longInput);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(1000);
    });

    test('处理大量关键词应保持高性能', async () => {
      const detector = new ScenarioDetector();
      const input = '投资 股票 基金 风险 收益 估值 价格 长期 短期 竞争 护城河 '.repeat(10);
      
      const start = Date.now();
      await detector.detect(input);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(500);
    });

    test('推荐大量模型应保持高性能', () => {
      const recommender = new ModelRecommender();
      const allModels = recommender.listModels();
      const allIds = allModels.map(m => m.id);
      
      const start = Date.now();
      recommender.recommend(allIds);
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(100);
    });
  });

  describe('平均响应时间统计', () => {
    test('开始分析平均响应时间应 < 300ms', async () => {
      const assistant = new MungerDecisionAssistant();
      const durations: number[] = [];
      
      for (let i = 0; i < 20; i++) {
        const start = Date.now();
        await assistant.startAnalysis(`user${i}`, '投资决策');
        durations.push(Date.now() - start);
      }
      
      const avg = durations.reduce((a, b) => a + b, 0) / durations.length;
      expect(avg).toBeLessThan(300);
    });

    test('场景识别平均响应时间应 < 100ms', async () => {
      const detector = new ScenarioDetector();
      const durations: number[] = [];
      
      for (let i = 0; i < 50; i++) {
        const start = Date.now();
        await detector.detect('投资决策');
        durations.push(Date.now() - start);
      }
      
      const avg = durations.reduce((a, b) => a + b, 0) / durations.length;
      expect(avg).toBeLessThan(100);
    });

    test('模型查询平均响应时间应 < 10ms', () => {
      const recommender = new ModelRecommender();
      const durations: number[] = [];
      
      for (let i = 0; i < 100; i++) {
        const start = Date.now();
        recommender.getModel('06');
        durations.push(Date.now() - start);
      }
      
      const avg = durations.reduce((a, b) => a + b, 0) / durations.length;
      expect(avg).toBeLessThan(10);
    });
  });

  describe('性能稳定性测试', () => {
    test('连续操作性能应保持稳定', async () => {
      const assistant = new MungerDecisionAssistant();
      const durations: number[] = [];
      
      for (let i = 0; i < 50; i++) {
        const start = Date.now();
        await assistant.startAnalysis(`user${i}`, '投资决策');
        durations.push(Date.now() - start);
      }
      
      // 前 10 次和后 10 次的平均时间差异应 < 100ms
      const firstAvg = durations.slice(0, 10).reduce((a, b) => a + b, 0) / 10;
      const lastAvg = durations.slice(-10).reduce((a, b) => a + b, 0) / 10;
      
      expect(Math.abs(firstAvg - lastAvg)).toBeLessThan(100);
    });

    test('性能不应随时间退化', async () => {
      const detector = new ScenarioDetector();
      
      const start1 = Date.now();
      for (let i = 0; i < 50; i++) {
        await detector.detect('投资决策');
      }
      const duration1 = Date.now() - start1;
      
      const start2 = Date.now();
      for (let i = 0; i < 50; i++) {
        await detector.detect('投资决策');
      }
      const duration2 = Date.now() - start2;
      
      // 第二批不应明显慢于第一批（允许 2 倍容差，避免边界值误报）
      expect(duration2).toBeLessThan(duration1 * 2);
    });
  });
});
