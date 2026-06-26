/**
 * MetricsMiddleware 测试 - 自优化触发机制 + 自适应重试策略
 * @version 2.4.0
 */

const { MetricsMiddleware, DEFAULT_CONFIG } = require('../src/middleware/metrics-middleware');
const fs = require('fs');
const path = require('path');

const TEST_STORAGE = path.join(__dirname, '.test-metrics');
let _counter = 0;

// Helper: 创建干净的中间件实例（每个实例独立存储目录）
function createMiddleware(overrides = {}) {
  const uniquePath = path.join(TEST_STORAGE, `inst-${++_counter}`);
  return new MetricsMiddleware({
    storagePath: uniquePath,
    ...overrides,
  });
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

describe('MetricsMiddleware', () => {
  describe('基本指标记录', () => {
    test('记录成功任务', () => {
      const m = createMiddleware();
      m.recordSuccess('t1', 'weather', 100);
      expect(m.metrics.totalTasks).toBe(1);
      expect(m.metrics.completedTasks).toBe(1);
      expect(m.metrics.failedTasks).toBe(0);
    });

    test('记录失败任务', () => {
      const m = createMiddleware();
      m.recordFailure('t2', 'weather', new Error('timeout'), 5000);
      expect(m.metrics.totalTasks).toBe(1);
      expect(m.metrics.failedTasks).toBe(1);
    });

    test('记录暂停和取消', () => {
      const m = createMiddleware();
      m.recordPause('t3');
      m.recordCancel('t4');
      expect(m.metrics.pausedTasks).toBe(1);
      expect(m.metrics.cancelledTasks).toBe(1);
    });

    test('技能调用统计正确累加', () => {
      const m = createMiddleware();
      m.recordSuccess('t1', 'weather', 100);
      m.recordSuccess('t2', 'weather', 200);
      m.recordFailure('t3', 'weather', new Error('fail'), 3000);
      m.recordSuccess('t4', 'xlsx', 50);

      const weather = m.metrics.skillCalls['weather'];
      expect(weather.total).toBe(3);
      expect(weather.success).toBe(2);
      expect(weather.failed).toBe(1);

      const xlsx = m.metrics.skillCalls['xlsx'];
      expect(xlsx.total).toBe(1);
      expect(xlsx.success).toBe(1);
    });
  });

  describe('失败率分析', () => {
    test('低失败率不触发优化', () => {
      const m = createMiddleware({ failureRateThreshold: 0.25 });
      // 10 成功，1 失败 → 10% 失败率
      for (let i = 0; i < 10; i++) m.recordSuccess(`t${i}`, 'test', 100);
      m.recordFailure('t10', 'test', new Error('fail'), 2000);

      const analysis = m.analyzeAndOptimize('test');
      expect(analysis.triggered).toBe(false);
      expect(analysis.suggestions.length).toBe(0);
    });

    test('高失败率触发优化建议', () => {
      const m = createMiddleware({ failureRateThreshold: 0.25 });
      // 3 成功，7 失败 → 70% 失败率
      for (let i = 0; i < 3; i++) m.recordSuccess(`t${i}`, 'test', 100);
      for (let i = 0; i < 7; i++) m.recordFailure(`t${i + 3}`, 'test', new Error('fail'), 2000);

      const analysis = m.analyzeAndOptimize('test');
      expect(analysis.triggered).toBe(true);
      expect(analysis.suggestions.some(s => s.type === 'HIGH_FAILURE_RATE')).toBe(true);
      expect(analysis.suggestions.some(s => s.type === 'SKILL_FAILURE_RATE')).toBe(true);
    });

    test('连续失败触发优化', () => {
      const m = createMiddleware({ consecutiveFailureThreshold: 3 });
      m.recordSuccess('t0', 'api', 100);
      // 连续 3 次失败
      for (let i = 0; i < 3; i++) {
        m.recordFailure(`t${i + 1}`, 'api', new Error('timeout'), 5000);
      }

      const analysis = m.analyzeAndOptimize('api');
      expect(analysis.triggered).toBe(true);
      expect(analysis.suggestions.some(s => s.type === 'CONSECUTIVE_FAILURES')).toBe(true);
    });

    test('分析结果包含时间戳', () => {
      const m = createMiddleware();
      m.recordFailure('t1', 'test', new Error('x'), 100);
      const analysis = m.analyzeAndOptimize('test');
      expect(analysis.timestamp).toBeDefined();
      expect(new Date(analysis.timestamp).getTime()).toBeGreaterThan(0);
    });
  });

  describe('自适应重试策略', () => {
    test('高失败率增加重试次数', () => {
      const m = createMiddleware();
      // 模拟 60% 失败率
      for (let i = 0; i < 4; i++) m.recordSuccess(`t${i}`, 'slow-api', 100);
      for (let i = 0; i < 6; i++) m.recordFailure(`t${i + 4}`, 'slow-api', new Error('fail'), 3000);

      const config = m.getAdaptiveRetryConfig('slow-api');
      expect(config.maxRetries).toBeGreaterThan(DEFAULT_CONFIG.retry.maxRetries);
      expect(config.shouldRetry).toBe(true);
    });

    test('低失败率减少重试次数', () => {
      const m = createMiddleware();
      // 15 次成功，1 次失败 → ~6%
      for (let i = 0; i < 15; i++) m.recordSuccess(`t${i}`, 'stable-api', 100);
      m.recordFailure('t15', 'stable-api', new Error('rare'), 500);

      const config = m.getAdaptiveRetryConfig('stable-api');
      expect(config.maxRetries).toBeLessThanOrEqual(DEFAULT_CONFIG.retry.maxRetries);
    });

    test('连续失败增加退避倍数', () => {
      const m = createMiddleware();
      for (let i = 0; i < 5; i++) {
        m.recordFailure(`t${i}`, 'flaky', new Error('fail'), 3000);
      }

      const config = m.getAdaptiveRetryConfig('flaky');
      expect(config.backoffMultiplier).toBeGreaterThan(DEFAULT_CONFIG.retry.backoffMultiplier);
      expect(config.baseDelay).toBeGreaterThan(DEFAULT_CONFIG.retry.baseDelay);
    });

    test('新技能使用默认配置', () => {
      const m = createMiddleware();
      const config = m.getAdaptiveRetryConfig('new-skill');
      expect(config.maxRetries).toBe(DEFAULT_CONFIG.retry.maxRetries);
      expect(config.backoffMultiplier).toBe(DEFAULT_CONFIG.retry.backoffMultiplier);
      expect(config.shouldRetry).toBe(true);
    });

    test('退避延迟计算包含随机抖动', () => {
      const m = createMiddleware();
      const delays = [];
      for (let i = 0; i < 10; i++) {
        delays.push(m._calculateBackoff('test', 2));
      }
      // 由于有随机抖动，10 次计算不太可能完全相同
      const unique = new Set(delays.map(d => Math.round(d)));
      expect(unique.size).toBeGreaterThan(1);
    });
  });

  describe('execute 中间件接口', () => {
    test('成功传递到 next', async () => {
      const m = createMiddleware();
      const next = jest.fn().mockResolvedValue({ data: 'ok' });
      const result = await m.execute({ taskId: 't1', skillName: 'test' }, next);
      expect(result).toEqual({ data: 'ok' });
      expect(m.metrics.completedTasks).toBe(1);
    });

    test('失败时记录指标并附带分析', async () => {
      const m = createMiddleware({ failureRateThreshold: 0.0 });
      const error = new Error('skill error');
      const next = jest.fn().mockRejectedValue(error);

      await expect(m.execute({ taskId: 't1', skillName: 'fail-test' }, next))
        .rejects.toThrow('skill error');

      // 失败被记录
      expect(m.metrics.failedTasks).toBe(1);
    });

    test('失败时附带 retryConfig', async () => {
      const m = createMiddleware();
      const next = jest.fn().mockRejectedValue(new Error('fail'));

      try {
        await m.execute({ taskId: 't1', skillName: 'retry-test', retryCount: 0 }, next);
      } catch (e) {
        expect(e.retryConfig).toBeDefined();
        expect(e.retryConfig.shouldRetry).toBe(true);
      }
    });
  });

  describe('持久化', () => {
    test('save 和加载', () => {
      const sharedPath = path.join(TEST_STORAGE, 'persist-test');
      const m1 = new MetricsMiddleware({ storagePath: sharedPath });
      m1.recordSuccess('t1', 'persist', 100);
      m1.recordFailure('t2', 'persist', new Error('x'), 2000);
      m1.save();

      const m2 = new MetricsMiddleware({ storagePath: sharedPath });
      expect(m2.metrics.totalTasks).toBe(2);
      expect(m2.metrics.completedTasks).toBe(1);
      expect(m2.metrics.failedTasks).toBe(1);
    });

    test('reset 清除所有数据', () => {
      const m = createMiddleware();
      m.recordSuccess('t1', 'test', 100);
      m.recordFailure('t2', 'test', new Error('x'), 1000);
      m.reset();
      expect(m.metrics.totalTasks).toBe(0);
      expect(Object.keys(m.metrics.skillCalls)).toHaveLength(0);
    });
  });

  describe('查询接口', () => {
    test('getReport 返回完整报告', () => {
      const m = createMiddleware();
      m.recordSuccess('t1', 'weather', 100);
      m.recordSuccess('t2', 'xlsx', 200);
      m.recordFailure('t3', 'weather', new Error('fail'), 3000);

      const report = m.getReport();
      expect(report.summary).toBeDefined();
      expect(report.summary.totalTasks).toBe(3);
      expect(report.skills['weather']).toBeDefined();
      expect(report.skills['xlsx']).toBeDefined();
      expect(report.timestamp).toBeDefined();
    });

    test('getTrend 返回时间序列', () => {
      const m = createMiddleware();
      for (let i = 0; i < 15; i++) {
        m.recordSuccess(`t${i}`, 'trend', 100 + i * 10);
      }

      const trend = m.getTrend(5);
      expect(trend.length).toBe(5);
      expect(trend[0].timestamp).toBeDefined();
      expect(typeof trend[0].failureRate).toBe('number');
    });

    test('建议历史不超过上限', () => {
      const m = createMiddleware({ maxSuggestionHistory: 3, failureRateThreshold: 0 });
      for (let i = 0; i < 5; i++) {
        m.recordFailure(`t${i}`, 'flood', new Error('x'), 100);
        m.analyzeAndOptimize('flood');
      }
      expect(m.metrics.suggestions.length).toBeLessThanOrEqual(3);
    });
  });

  describe('onOptimizationTriggered 回调', () => {
    test('触发时调用回调', (done) => {
      const m = createMiddleware({
        failureRateThreshold: 0,
        onOptimizationTriggered: (analysis) => {
          expect(analysis.triggered).toBe(true);
          expect(analysis.suggestions.length).toBeGreaterThan(0);
          done();
        },
      });
      m.recordFailure('t1', 'cb-test', new Error('fail'), 100);
      m.analyzeAndOptimize('cb-test');
    });

    test('不触发时不调用回调', () => {
      let called = false;
      const m = createMiddleware({
        failureRateThreshold: 0.5,
        onOptimizationTriggered: () => { called = true; },
      });
      m.recordSuccess('t1', 'ok', 100);
      m.analyzeAndOptimize('ok');
      expect(called).toBe(false);
    });
  });
});
