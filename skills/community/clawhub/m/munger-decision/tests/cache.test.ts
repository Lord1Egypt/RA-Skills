import { ModelRecommender } from '../src/recommender';

describe('缓存机制测试', () => {
  describe('模型数据缓存', () => {
    test('应缓存模型数据', () => {
      const recommender1 = new ModelRecommender();
      const recommender2 = new ModelRecommender();
      
      const models1 = recommender1.listModels();
      const models2 = recommender2.listModels();
      
      // 验证数据一致性
      expect(models1.length).toBe(models2.length);
      expect(models1[0].id).toBe(models2[0].id);
    });

    test('应包含所有 83 个模型', () => {
      const recommender = new ModelRecommender();
      const models = recommender.listModels();
      expect(models.length).toBe(83);
    });

    test('缓存应提高查询性能', () => {
      const recommender = new ModelRecommender();
      
      // 第一次查询
      const start1 = Date.now();
      recommender.getModel('06');
      const duration1 = Date.now() - start1;
      
      // 第二次查询（应该更快）
      const start2 = Date.now();
      recommender.getModel('06');
      const duration2 = Date.now() - start2;
      
      // 两次查询都应该很快（< 10ms）
      expect(duration1).toBeLessThan(10);
      expect(duration2).toBeLessThan(10);
    });

    test('多次实例化应共享缓存', () => {
      const start = Date.now();
      
      // 创建多个实例
      for (let i = 0; i < 100; i++) {
        new ModelRecommender();
      }
      
      const duration = Date.now() - start;
      
      // 如果有缓存，100 次实例化应该很快（< 100ms）
      expect(duration).toBeLessThan(100);
    });

    test('缓存应支持大小写不敏感查询', () => {
      const recommender = new ModelRecommender();
      
      const model1 = recommender.getModel('06');
      const model2 = recommender.getModel('06');
      const model3 = recommender.getModel('06');
      
      expect(model1).toBeDefined();
      expect(model2).toBeDefined();
      expect(model3).toBeDefined();
      expect(model1?.id).toBe(model2?.id);
      expect(model2?.id).toBe(model3?.id);
    });

    test('缓存应处理不存在的模型 ID', () => {
      const recommender = new ModelRecommender();
      
      const model = recommender.getModel('999');
      expect(model).toBeUndefined();
    });

    test('批量查询应使用缓存', () => {
      const recommender = new ModelRecommender();
      
      const start = Date.now();
      const modelIds = ['01', '02', '03', '06', '07', '10'];
      const models = recommender.recommend(modelIds);
      const duration = Date.now() - start;
      
      expect(models.length).toBe(6);
      expect(duration).toBeLessThan(10);
    });
  });

  describe('缓存一致性测试', () => {
    test('不同实例应返回相同的模型数据', () => {
      const recommender1 = new ModelRecommender();
      const recommender2 = new ModelRecommender();
      
      const model1 = recommender1.getModel('06');
      const model2 = recommender2.getModel('06');
      
      expect(model1?.id).toBe(model2?.id);
      expect(model1?.name).toBe(model2?.name);
      expect(model1?.description).toBe(model2?.description);
    });

    test('缓存应保持数据完整性', () => {
      const recommender = new ModelRecommender();
      const model = recommender.getModel('06');
      
      expect(model).toBeDefined();
      expect(model?.id).toBeDefined();
      expect(model?.name).toBeDefined();
      expect(model?.description).toBeDefined();
      expect(model?.category).toBeDefined();
      expect(model?.questions).toBeDefined();
      expect(model?.scoring).toBeDefined();
    });

    test('缓存应支持并发访问', async () => {
      const recommender = new ModelRecommender();
      
      const promises = [];
      for (let i = 0; i < 50; i++) {
        promises.push(Promise.resolve(recommender.getModel('06')));
      }
      
      const results = await Promise.all(promises);
      
      // 所有结果应该一致
      results.forEach(model => {
        expect(model?.id).toBe('06');
        expect(model?.name).toBe('能力圈');
      });
    });
  });

  describe('缓存性能测试', () => {
    test('大量查询应保持高性能', () => {
      const recommender = new ModelRecommender();
      
      const start = Date.now();
      for (let i = 0; i < 1000; i++) {
        recommender.getModel('06');
      }
      const duration = Date.now() - start;
      
      // 1000 次查询应该在 100ms 内完成
      expect(duration).toBeLessThan(100);
    });

    test('批量推荐应保持高性能', () => {
      const recommender = new ModelRecommender();
      const modelIds = ['01', '02', '03', '06', '07', '10', '31', '32', '33'];
      
      const start = Date.now();
      for (let i = 0; i < 100; i++) {
        recommender.recommend(modelIds);
      }
      const duration = Date.now() - start;
      
      // 100 次批量推荐应该在 50ms 内完成
      expect(duration).toBeLessThan(50);
    });

    test('列出所有模型应保持高性能', () => {
      const recommender = new ModelRecommender();
      
      const start = Date.now();
      for (let i = 0; i < 100; i++) {
        recommender.listModels();
      }
      const duration = Date.now() - start;
      
      // 100 次列出所有模型应该在 50ms 内完成
      expect(duration).toBeLessThan(50);
    });
  });
});
