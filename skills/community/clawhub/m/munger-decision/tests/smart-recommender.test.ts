import { SmartRecommender } from '../src/smart-recommender';

describe('SmartRecommender - 智能推荐引擎测试', () => {
  let recommender: SmartRecommender;

  beforeEach(() => {
    recommender = new SmartRecommender();
  });

  describe('基础功能测试', () => {
    test('应返回评分结果', async () => {
      const scores = await recommender.analyzeAndScore('投资决策', 'investment');
      expect(scores).toBeDefined();
      expect(scores.length).toBeGreaterThan(0);
      expect(scores.length).toBeLessThanOrEqual(5);
    });

    test('评分应在 0-100 范围内', async () => {
      const scores = await recommender.analyzeAndScore('产品决策', 'product');
      scores.forEach(score => {
        expect(score.score).toBeGreaterThanOrEqual(0);
        expect(score.score).toBeLessThanOrEqual(100);
      });
    });

    test('应按评分降序排列', async () => {
      const scores = await recommender.analyzeAndScore('战略决策', 'strategy');
      for (let i = 0; i < scores.length - 1; i++) {
        expect(scores[i].score).toBeGreaterThanOrEqual(scores[i + 1].score);
      }
    });

    test('应包含推荐理由', async () => {
      const scores = await recommender.analyzeAndScore('招聘决策', 'hiring');
      scores.forEach(score => {
        expect(score.reason).toBeDefined();
        expect(score.reason.length).toBeGreaterThan(0);
      });
    });

    test('应包含完整的模型信息', async () => {
      const scores = await recommender.analyzeAndScore('投资决策', 'investment');
      scores.forEach(score => {
        expect(score.model).toBeDefined();
        expect(score.model.id).toBeDefined();
        expect(score.model.name).toBeDefined();
        expect(score.model.description).toBeDefined();
      });
    });
  });

  describe('特征提取测试', () => {
    test('应识别风险特征', async () => {
      const scores = await recommender.analyzeAndScore('这个投资风险大吗？', 'investment');
      const riskModels = scores.filter(s => s.reason.includes('风险'));
      expect(riskModels.length).toBeGreaterThan(0);
    });

    test('应识别从众特征', async () => {
      const scores = await recommender.analyzeAndScore('大家都在买，我要不要跟？', 'investment');
      expect(scores.length).toBeGreaterThan(0);
      expect(scores[0].score).toBeGreaterThan(50);
    });

    test('应识别价值特征', async () => {
      const scores = await recommender.analyzeAndScore('这个价格合理吗？估值如何？', 'investment');
      const valueModels = scores.filter(s => s.reason.includes('价值'));
      expect(valueModels.length).toBeGreaterThan(0);
    });

    test('应识别长期特征', async () => {
      const scores = await recommender.analyzeAndScore('长期持有是否值得？', 'investment');
      expect(scores.length).toBeGreaterThan(0);
      expect(scores[0].score).toBeGreaterThan(0);
    });

    test('应识别竞争特征', async () => {
      const scores = await recommender.analyzeAndScore('竞争对手的护城河如何？', 'product');
      const compModels = scores.filter(s => s.reason.includes('竞争'));
      expect(compModels.length).toBeGreaterThan(0);
    });
  });

  describe('场景适配测试', () => {
    test('投资场景应推荐相关模型', async () => {
      const scores = await recommender.analyzeAndScore('是否投资这只股票？', 'investment');
      expect(scores.length).toBeGreaterThan(0);
      expect(scores[0].score).toBeGreaterThan(0);
    });

    test('产品场景应推荐相关模型', async () => {
      const scores = await recommender.analyzeAndScore('是否开发这个功能？', 'product');
      expect(scores.length).toBeGreaterThan(0);
      expect(scores[0].score).toBeGreaterThan(0);
    });

    test('招聘场景应推荐相关模型', async () => {
      const scores = await recommender.analyzeAndScore('是否录用这个候选人？', 'hiring');
      expect(scores.length).toBeGreaterThan(0);
      expect(scores[0].score).toBeGreaterThan(0);
    });

    test('战略场景应推荐相关模型', async () => {
      const scores = await recommender.analyzeAndScore('公司战略是否需要调整？', 'strategy');
      expect(scores.length).toBeGreaterThan(0);
      expect(scores[0].score).toBeGreaterThan(0);
    });
  });

  describe('边界情况测试', () => {
    test('应处理空输入', async () => {
      const scores = await recommender.analyzeAndScore('', 'general');
      expect(scores).toBeDefined();
      expect(scores.length).toBeGreaterThan(0);
    });

    test('应处理特殊字符', async () => {
      const scores = await recommender.analyzeAndScore('是否投资 *特殊* 公司？！@#', 'investment');
      expect(scores).toBeDefined();
      expect(scores.length).toBeGreaterThan(0);
    });

    test('应处理超长输入', async () => {
      const longInput = '投资决策 '.repeat(100);
      const scores = await recommender.analyzeAndScore(longInput, 'investment');
      expect(scores).toBeDefined();
      expect(scores.length).toBeGreaterThan(0);
    });

    test('应处理未知场景', async () => {
      const scores = await recommender.analyzeAndScore('决策问题', 'unknown');
      expect(scores).toBeDefined();
      expect(scores.length).toBeGreaterThan(0);
    });

    test('应处理多特征混合输入', async () => {
      const scores = await recommender.analyzeAndScore(
        '大家都在买这只股票，风险大吗？长期持有值得吗？',
        'investment'
      );
      expect(scores).toBeDefined();
      expect(scores.length).toBeGreaterThan(0);
      expect(scores[0].score).toBeGreaterThan(50);
    });
  });

  describe('性能测试', () => {
    test('单次推荐应在 500ms 内完成', async () => {
      const start = Date.now();
      await recommender.analyzeAndScore('投资决策', 'investment');
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(500);
    });

    test('批量推荐应在 2s 内完成', async () => {
      const start = Date.now();
      const promises = [];
      for (let i = 0; i < 10; i++) {
        promises.push(recommender.analyzeAndScore('投资决策', 'investment'));
      }
      await Promise.all(promises);
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(2000);
    });
  });

  describe('一致性测试', () => {
    test('相同输入应返回相同结果', async () => {
      const input = '是否投资这只股票？';
      const scores1 = await recommender.analyzeAndScore(input, 'investment');
      const scores2 = await recommender.analyzeAndScore(input, 'investment');
      
      expect(scores1.length).toBe(scores2.length);
      for (let i = 0; i < scores1.length; i++) {
        expect(scores1[i].modelId).toBe(scores2[i].modelId);
        expect(scores1[i].score).toBe(scores2[i].score);
      }
    });

    test('不同输入应返回不同结果', async () => {
      const scores1 = await recommender.analyzeAndScore('投资决策', 'investment');
      const scores2 = await recommender.analyzeAndScore('产品决策', 'product');
      
      const ids1 = scores1.map(s => s.modelId).join(',');
      const ids2 = scores2.map(s => s.modelId).join(',');
      expect(ids1).not.toBe(ids2);
    });
  });
});
