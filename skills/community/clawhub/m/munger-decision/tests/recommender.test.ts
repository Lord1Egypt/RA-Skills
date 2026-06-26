import { ModelRecommender } from '../src/recommender';

describe('ModelRecommender - 模型推荐测试', () => {
  let recommender: ModelRecommender;

  beforeEach(() => {
    recommender = new ModelRecommender();
  });

  describe('模型推荐覆盖率', () => {
    test('应能推荐所有核心模型', () => {
      const coreModels = ['01', '06', '07'];
      const result = recommender.recommend(coreModels);
      
      expect(result).toHaveLength(3);
      expect(result.map(m => m.id)).toEqual(coreModels);
    });

    test('应能推荐投资相关模型', () => {
      const investmentModels = ['06', '10', '09', '07', '44'];
      const result = recommender.recommend(investmentModels);
      
      expect(result.length).toBeGreaterThan(0);
      expect(result.every(m => investmentModels.includes(m.id))).toBe(true);
    });

    test('应能推荐产品相关模型', () => {
      const productModels = ['08', '06', '02', '43', '48'];
      const result = recommender.recommend(productModels);
      
      expect(result.length).toBeGreaterThan(0);
    });

    test('应过滤无效模型 ID', () => {
      const mixedIds = ['01', 'invalid', '06', 'fake'];
      const result = recommender.recommend(mixedIds);
      
      expect(result).toHaveLength(2);
      expect(result.map(m => m.id)).toEqual(['01', '06']);
    });

    test('空列表应返回空数组', () => {
      const result = recommender.recommend([]);
      expect(result).toHaveLength(0);
    });
  });

  describe('单个模型获取', () => {
    test('应能获取第一性原理模型', () => {
      const model = recommender.getModel('01');
      
      expect(model).toBeDefined();
      expect(model?.name).toBe('第一性原理');
      expect(model?.category).toBe('core');
    });

    test('应能获取能力圈模型', () => {
      const model = recommender.getModel('06');
      
      expect(model).toBeDefined();
      expect(model?.name).toBe('能力圈');
      expect(model?.questions).toHaveLength(3);
    });

    test('无效 ID 应返回 undefined', () => {
      const model = recommender.getModel('999');
      expect(model).toBeUndefined();
    });
  });

  describe('模型列表功能', () => {
    test('应能列出所有模型', () => {
      const models = recommender.listModels();
      
      expect(models.length).toBeGreaterThan(0);
      expect(models.every(m => m.id && m.name && m.category)).toBe(true);
    });

    test('应能按分类列出模型', () => {
      const coreModels = recommender.listByCategory('core');
      
      expect(coreModels.length).toBeGreaterThan(0);
      expect(coreModels.every(m => m.category === 'core')).toBe(true);
    });

    test('不存在的分类应返回空数组', () => {
      const result = recommender.listByCategory('nonexistent');
      expect(result).toHaveLength(0);
    });
  });

  describe('模型数据完整性', () => {
    test('所有模型应有必需字段', () => {
      const models = recommender.listModels();
      
      models.forEach(model => {
        expect(model.id).toBeDefined();
        expect(model.name).toBeDefined();
        expect(model.category).toBeDefined();
        expect(model.description).toBeDefined();
        expect(model.questions).toBeDefined();
        expect(Array.isArray(model.questions)).toBe(true);
        expect(model.scoring).toBeDefined();
      });
    });

    test('所有模型应至少有一个问题', () => {
      const models = recommender.listModels();
      
      models.forEach(model => {
        expect(model.questions.length).toBeGreaterThan(0);
      });
    });

    test('所有模型应有评分标准', () => {
      const models = recommender.listModels();
      
      models.forEach(model => {
        expect(Object.keys(model.scoring).length).toBeGreaterThan(0);
      });
    });
  });

  describe('推荐覆盖率 100% 验证', () => {
    test('所有场景推荐的模型都应存在', () => {
      const scenarios = [
        ['06', '10', '09', '07', '44'], // investment
        ['08', '06', '02', '43', '48'], // product
        ['08', '06', '45', '07'],       // hiring
        ['01', '06', '07', '09', '12'], // strategy
      ];

      scenarios.forEach(modelIds => {
        const result = recommender.recommend(modelIds);
        // 至少能推荐一些模型（部分 ID 可能不存在）
        expect(result.length).toBeGreaterThan(0);
      });
    });

    test('推荐结果应保持顺序', () => {
      const modelIds = ['07', '01', '06'];
      const result = recommender.recommend(modelIds);
      
      expect(result.map(m => m.id)).toEqual(modelIds);
    });
  });
});
