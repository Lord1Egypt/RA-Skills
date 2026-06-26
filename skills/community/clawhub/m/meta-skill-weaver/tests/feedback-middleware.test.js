/**
 * FeedbackMiddleware 测试
 * @version 2.4.0
 */

const { FeedbackMiddleware, DEFAULT_CONFIG } = require('../src/middleware/feedback-middleware');
const fs = require('fs');
const path = require('path');

const TEST_STORAGE = path.join(__dirname, '.test-feedback');
let _counter = 0;

function createMiddleware(overrides = {}) {
  const uniquePath = path.join(TEST_STORAGE, `inst-${++_counter}`);
  return new FeedbackMiddleware({ storagePath: uniquePath, ...overrides });
}

beforeAll(() => {
  if (fs.existsSync(TEST_STORAGE)) {
    fs.rmSync(TEST_STORAGE, { recursive: true, force: true });
  }
});

afterAll(() => {
  if (fs.existsSync(TEST_STORAGE)) {
    fs.rmSync(TEST_STORAGE, { recursive: true, force: true });
  }
});

describe('FeedbackMiddleware', () => {
  describe('基本提交', () => {
    test('提交有效反馈', () => {
      const fb = createMiddleware();
      const result = fb.submit({ taskId: 't1', skillName: 'weather', rating: 5, comment: '很好用' });
      expect(result.id).toBeDefined();
      expect(result.taskId).toBe('t1');
      expect(result.rating).toBe(5);
      expect(result.category).toBe('praise');
    });

    test('评分范围验证', () => {
      const fb = createMiddleware();
      expect(() => fb.submit({ taskId: 't1', rating: 0 })).toThrow('between 1 and 5');
      expect(() => fb.submit({ taskId: 't1', rating: 6 })).toThrow('between 1 and 5');
      expect(() => fb.submit({ taskId: 't1', rating: 'abc' })).toThrow('between 1 and 5');
    });

    test('有效边界评分', () => {
      const fb = createMiddleware();
      expect(() => fb.submit({ taskId: 't1', rating: 1 })).not.toThrow();
      expect(() => fb.submit({ taskId: 't2', rating: 5 })).not.toThrow();
    });

    test('自动分类：高评分→praise', () => {
      const fb = createMiddleware();
      const r = fb.submit({ taskId: 't1', rating: 4 });
      expect(r.category).toBe('praise');
    });

    test('自动分类：低评分→issue', () => {
      const fb = createMiddleware();
      const r = fb.submit({ taskId: 't1', rating: 2, comment: '太慢了' });
      expect(r.category).toBe('issue');
    });

    test('自动分类：3星含bug→bug', () => {
      const fb = createMiddleware();
      const r = fb.submit({ taskId: 't1', rating: 3, comment: '有个bug' });
      expect(r.category).toBe('bug');
    });

    test('自动分类：3星含建议→suggestion', () => {
      const fb = createMiddleware();
      const r = fb.submit({ taskId: 't1', rating: 3, comment: '希望能改进速度' });
      expect(r.category).toBe('suggestion');
    });

    test('评论长度截断', () => {
      const fb = createMiddleware();
      const long = 'a'.repeat(3000);
      const r = fb.submit({ taskId: 't1', rating: 3, comment: long });
      expect(r.comment.length).toBeLessThanOrEqual(2000);
    });

    test('自定义分类覆盖自动分类', () => {
      const fb = createMiddleware();
      const r = fb.submit({ taskId: 't1', rating: 5, category: 'suggestion' });
      expect(r.category).toBe('suggestion');
    });

    test('tags 正确保存', () => {
      const fb = createMiddleware();
      const r = fb.submit({ taskId: 't1', rating: 4, tags: ['fast', 'reliable'] });
      expect(r.tags).toEqual(['fast', 'reliable']);
    });
  });

  describe('反馈上限', () => {
    test('单任务反馈数量上限', () => {
      const fb = createMiddleware({ maxFeedbackPerTask: 2 });
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't1', rating: 4 });
      expect(() => fb.submit({ taskId: 't1', rating: 3 })).toThrow('max feedback limit');
    });

    test('不同任务独立计数', () => {
      const fb = createMiddleware({ maxFeedbackPerTask: 1 });
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't2', rating: 4 }); // 不同任务，不应受限
      expect(fb.feedbacks.length).toBe(2);
    });

    test('总反馈上限', () => {
      const fb = createMiddleware({ maxTotalFeedback: 3 });
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't2', rating: 4 });
      fb.submit({ taskId: 't3', rating: 3 });
      fb.submit({ taskId: 't4', rating: 2 }); // 触发清理
      expect(fb.feedbacks.length).toBe(3);
    });
  });

  describe('统计查询', () => {
    test('空数据返回零值统计', () => {
      const fb = createMiddleware();
      const stats = fb.getStats();
      expect(stats.total).toBe(0);
      expect(stats.avgRating).toBe(0);
    });

    test('正确计算平均评分', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't2', rating: 3 });
      fb.submit({ taskId: 't3', rating: 4 });

      const stats = fb.getStats();
      expect(stats.total).toBe(3);
      expect(stats.avgRating).toBe(4);
    });

    test('评分分布正确', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't2', rating: 5 });
      fb.submit({ taskId: 't3', rating: 3 });

      const stats = fb.getStats();
      expect(stats.ratingDistribution[5]).toBe(2);
      expect(stats.ratingDistribution[3]).toBe(1);
      expect(stats.ratingDistribution[1]).toBe(0);
    });

    test('分类统计正确', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't2', rating: 5 });
      fb.submit({ taskId: 't3', rating: 1, comment: '崩溃了' });

      const stats = fb.getStats();
      expect(stats.categoryBreakdown['praise']).toBe(2);
      expect(stats.categoryBreakdown['bug']).toBe(1);
    });

    test('热门标签排序', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5, tags: ['fast', 'good'] });
      fb.submit({ taskId: 't2', rating: 4, tags: ['fast'] });
      fb.submit({ taskId: 't3', rating: 3, tags: ['slow', 'fast'] });

      const stats = fb.getStats();
      expect(stats.topTags[0].tag).toBe('fast');
      expect(stats.topTags[0].count).toBe(3);
    });

    test('按任务过滤统计', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 'report', rating: 5 });
      fb.submit({ taskId: 'report', rating: 4 });
      fb.submit({ taskId: 'export', rating: 2 });

      const reportStats = fb.getStats('report');
      expect(reportStats.total).toBe(2);
      expect(reportStats.avgRating).toBe(4.5);

      const exportStats = fb.getStats('export');
      expect(exportStats.total).toBe(1);
      expect(exportStats.avgRating).toBe(2);
    });
  });

  describe('技能排名', () => {
    test('按平均分排序', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', skillName: 'weather', rating: 5 });
      fb.submit({ taskId: 't2', skillName: 'xlsx', rating: 3 });
      fb.submit({ taskId: 't3', skillName: 'weather', rating: 4 });

      const rankings = fb.getSkillRankings();
      expect(rankings[0].skillName).toBe('weather');
      expect(rankings[0].avgRating).toBe(4.5);
      expect(rankings[1].skillName).toBe('xlsx');
    });
  });

  describe('搜索', () => {
    test('按技能名搜索', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', skillName: 'weather', rating: 5 });
      fb.submit({ taskId: 't2', skillName: 'xlsx', rating: 3 });

      const results = fb.search({ skillName: 'weather' });
      expect(results.length).toBe(1);
      expect(results[0].skillName).toBe('weather');
    });

    test('按分类搜索', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't2', rating: 1, comment: '崩溃' });

      const results = fb.search({ category: 'bug' });
      expect(results.length).toBe(1);
      expect(results[0].category).toBe('bug');
    });

    test('按评分范围搜索', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't2', rating: 3 });
      fb.submit({ taskId: 't3', rating: 1, comment: 'bad' });

      const results = fb.search({ minRating: 4 });
      expect(results.length).toBe(1);
      expect(results[0].rating).toBe(5);
    });

    test('按标签搜索', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5, tags: ['fast'] });
      fb.submit({ taskId: 't2', rating: 4, tags: ['slow'] });

      const results = fb.search({ tags: ['fast'] });
      expect(results.length).toBe(1);
    });

    test('组合过滤', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', skillName: 'weather', rating: 5 });
      fb.submit({ taskId: 't2', skillName: 'weather', rating: 2, comment: '慢' });
      fb.submit({ taskId: 't3', skillName: 'xlsx', rating: 5 });

      const results = fb.search({ skillName: 'weather', minRating: 4 });
      expect(results.length).toBe(1);
    });
  });

  describe('趋势分析', () => {
    test('按日聚合', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5 });
      fb.submit({ taskId: 't2', rating: 3 });

      const trend = fb.getTrend('daily');
      expect(trend.length).toBeGreaterThanOrEqual(1);
      expect(trend[0].period).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      expect(typeof trend[0].avgRating).toBe('number');
    });

    test('issueRate 计算', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 1, comment: 'error' });
      fb.submit({ taskId: 't2', rating: 5 });

      const trend = fb.getTrend('daily');
      expect(trend[0].issueRate).toBe(50); // 50%
    });
  });

  describe('execute 中间件接口', () => {
    test('标记反馈就绪', async () => {
      const fb = createMiddleware();
      const context = { taskId: 't1', skillName: 'test' };
      const next = jest.fn().mockResolvedValue({ ok: true });

      const result = await fb.execute(context, next);
      expect(result).toEqual({ ok: true });
      expect(context._feedbackReady).toBe(true);
      expect(context._feedbackSkill).toBe('test');
    });
  });

  describe('回调', () => {
    test('提交时触发回调', (done) => {
      const fb = createMiddleware({
        onFeedbackReceived: (feedback) => {
          expect(feedback.rating).toBe(5);
          expect(feedback.taskId).toBe('t1');
          done();
        },
      });
      fb.submit({ taskId: 't1', rating: 5 });
    });
  });

  describe('持久化', () => {
    test('保存和恢复', () => {
      const sharedPath = path.join(TEST_STORAGE, 'persist-test');
      const fb1 = new FeedbackMiddleware({ storagePath: sharedPath });
      fb1.submit({ taskId: 'persist', skillName: 'test', rating: 4, comment: 'good' });

      const fb2 = new FeedbackMiddleware({ storagePath: sharedPath });
      const found = fb2.search({ taskId: 'persist' });
      expect(found.length).toBe(1);
      expect(found[0].rating).toBe(4);
    });

    test('reset 清除数据', () => {
      const fb = createMiddleware();
      fb.submit({ taskId: 't1', rating: 5 });
      fb.reset();
      expect(fb.feedbacks.length).toBe(0);
    });
  });
});
