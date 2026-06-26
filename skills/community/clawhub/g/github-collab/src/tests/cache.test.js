/**
 * Cache 单元测试
 */

const { Cache } = require('../utils/cache');

describe('Cache - 缓存系统', () => {
  describe('基本功能', () => {
    test('应该创建缓存实例', () => {
      const cache = new Cache();
      expect(cache).toBeDefined();
      expect(cache.cache).toBeInstanceOf(Map);
    });

    test('应该使用默认配置', () => {
      const cache = new Cache();
      expect(cache.maxSize).toBe(1000);
      expect(cache.defaultTTL).toBe(300);
      expect(cache.enableLRU).toBe(true);
    });

    test('应该使用自定义配置', () => {
      const cache = new Cache({
        maxSize: 100,
        defaultTTL: 60,
        enableLRU: false
      });
      expect(cache.maxSize).toBe(100);
      expect(cache.defaultTTL).toBe(60);
      expect(cache.enableLRU).toBe(false);
    });

    test('应该设置缓存值', () => {
      const cache = new Cache();
      const result = cache.set('key', 'value');
      expect(result).toBe(true);
      expect(cache.cache.has('key')).toBe(true);
    });

    test('应该获取缓存值', () => {
      const cache = new Cache();
      cache.set('key', 'value');
      const result = cache.get('key');
      expect(result).toBe('value');
    });

    test('应该返回 undefined 当键不存在', () => {
      const cache = new Cache();
      const result = cache.get('nonexistent');
      expect(result).toBeUndefined();
    });

    test('应该删除缓存值', () => {
      const cache = new Cache();
      cache.set('key', 'value');
      const result = cache.delete('key');
      expect(result).toBe(true);
      expect(cache.cache.has('key')).toBe(false);
    });

    test('应该返回 false 当删除不存在的键', () => {
      const cache = new Cache();
      const result = cache.delete('nonexistent');
      expect(result).toBe(false);
    });

    test('应该清空所有缓存', () => {
      const cache = new Cache();
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.clear();
      expect(cache.cache.size).toBe(0);
    });
  });

  describe('TTL 功能', () => {
    test('应该使用默认 TTL', () => {
      const cache = new Cache({ defaultTTL: 1 });
      cache.set('key', 'value');

      // 等待过期
      return new Promise((resolve) => {
        setTimeout(() => {
          const result = cache.get('key');
          expect(result).toBeUndefined();
          resolve();
        }, 1100);
      });
    });

    test('应该使用自定义 TTL', () => {
      const cache = new Cache();
      cache.set('key', 'value', 1); // 1 秒

      return new Promise((resolve) => {
        setTimeout(() => {
          const result = cache.get('key');
          expect(result).toBeUndefined();
          resolve();
        }, 1100);
      });
    });

    test('应该永不过期当 TTL 为 0', () => {
      const cache = new Cache();
      cache.set('key', 'value', 0);

      return new Promise((resolve) => {
        setTimeout(() => {
          const result = cache.get('key');
          expect(result).toBe('value');
          resolve();
        }, 100);
      });
    });

    test('应该刷新 TTL', () => {
      const cache = new Cache({ defaultTTL: 500 }); // 500ms
      cache.set('key', 'value');

      return new Promise((resolve) => {
        setTimeout(() => {
          cache.refresh('key', 1000); // 刷新为 1000ms

          setTimeout(() => {
            const result = cache.get('key');
            expect(result).toBe('value');
            resolve();
          }, 100);
        }, 600);
      });
    });

    test('应该刷新为默认 TTL', () => {
      const cache = new Cache({ defaultTTL: 1000 }); // 1000ms
      cache.set('key', 'value', 0); // 永不过期

      return new Promise((resolve) => {
        setTimeout(() => {
          cache.refresh('key'); // 刷新为默认 TTL (1000ms)

          setTimeout(() => {
            const result = cache.get('key');
            expect(result).toBeUndefined(); // 应该过期
            resolve();
          }, 1100);
        }, 100);
      });
    });
  });

  describe('LRU 功能', () => {
    test('应该淘汰最少使用的项', () => {
      const cache = new Cache({ maxSize: 3, defaultTTL: 3600 });
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.set('key3', 'value3');

      // 访问 key1,使其成为最新使用的
      cache.get('key1');

      // 添加新项,应该淘汰 key2(最少使用)
      cache.set('key4', 'value4');

      expect(cache.cache.has('key1')).toBe(true);
      expect(cache.cache.has('key2')).toBe(false);
      expect(cache.cache.has('key3')).toBe(true);
      expect(cache.cache.has('key4')).toBe(true);
    });

    test('应该禁用 LRU 当配置为 false', () => {
      const cache = new Cache({ maxSize: 3, defaultTTL: 3600, enableLRU: false });
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.set('key3', 'value3');
      cache.set('key4', 'value4');

      // 当 LRU 禁用时,应该简单替换
      expect(cache.cache.size).toBe(4);
    });
  });

  describe('批量操作', () => {
    test('应该批量设置缓存', () => {
      const cache = new Cache();
      const entries = [
        { key: 'key1', value: 'value1' },
        { key: 'key2', value: 'value2' },
        { key: 'key3', value: 'value3' }
      ];

      cache.warm(entries);

      expect(cache.get('key1')).toBe('value1');
      expect(cache.get('key2')).toBe('value2');
      expect(cache.get('key3')).toBe('value3');
    });

    test('应该批量获取缓存', () => {
      const cache = new Cache();
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.set('key3', 'value3');

      const result = cache.getMany(['key1', 'key2', 'key3']);

      expect(result.key1).toBe('value1');
      expect(result.key2).toBe('value2');
      expect(result.key3).toBe('value3');
    });

    test('应该处理批量获取中不存在的键', () => {
      const cache = new Cache();
      cache.set('key1', 'value1');

      const result = cache.getMany(['key1', 'key2', 'key3']);

      expect(result.key1).toBe('value1');
      expect(result.key2).toBeUndefined();
      expect(result.key3).toBeUndefined();
    });

    test('应该批量删除缓存', () => {
      const cache = new Cache();
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.set('key3', 'value3');

      const result = cache.deleteMany(['key1', 'key2']);

      expect(result).toBe(2);
      expect(cache.get('key1')).toBeUndefined();
      expect(cache.get('key2')).toBeUndefined();
      expect(cache.get('key3')).toBe('value3');
    });
  });

  describe('缓存失效', () => {
    test('应该根据前缀失效缓存', () => {
      const cache = new Cache();
      cache.set('user:1', 'user1');
      cache.set('user:2', 'user2');
      cache.set('config:app', 'config');

      const result = cache.invalidateByPrefix('user:');

      expect(result).toBe(2);
      expect(cache.get('user:1')).toBeUndefined();
      expect(cache.get('user:2')).toBeUndefined();
      expect(cache.get('config:app')).toBe('config');
    });

    test('应该根据正则模式失效缓存', () => {
      const cache = new Cache();
      cache.set('user:1', 'user1');
      cache.set('user:2', 'user2');
      cache.set('config:app', 'config');

      const result = cache.invalidateByPattern(/^user:\d+$/);

      expect(result).toBe(2);
      expect(cache.get('user:1')).toBeUndefined();
      expect(cache.get('user:2')).toBeUndefined();
      expect(cache.get('config:app')).toBe('config');
    });

    test('应该清除过期缓存', () => {
      const cache = new Cache({ defaultTTL: 0 });
      cache.set('key1', 'value1', 1);
      cache.set('key2', 'value2', 1);
      cache.set('key3', 'value3', 0); // 永不过期

      return new Promise((resolve) => {
        setTimeout(() => {
          const result = cache.clearExpired();
          expect(result).toBe(2);
          expect(cache.get('key1')).toBeUndefined();
          expect(cache.get('key2')).toBeUndefined();
          expect(cache.get('key3')).toBe('value3');
          resolve();
        }, 1100);
      });
    });
  });

  describe('统计功能', () => {
    test('应该返回正确的统计信息', () => {
      const cache = new Cache({ maxSize: 100 });
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.get('key1');
      cache.get('key1');
      cache.get('nonexistent');

      const stats = cache.getStats();

      expect(stats.size).toBe(2);
      expect(stats.maxSize).toBe(100);
      expect(stats.hits).toBe(2);
      expect(stats.misses).toBe(1);
      expect(stats.hitRate).toMatch(/\d+\.\d+%/);
    });

    test('应该返回正确的缓存大小', () => {
      const cache = new Cache();
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');

      expect(cache.size()).toBe(2);
    });

    test('应该返回所有键', () => {
      const cache = new Cache();
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');

      const keys = cache.keys();
      expect(keys).toContain('key1');
      expect(keys).toContain('key2');
    });

    test('应该返回所有有效键', () => {
      const cache = new Cache({ defaultTTL: 0 });
      cache.set('key1', 'value1', 1);
      cache.set('key2', 'value2', 1);
      cache.set('key3', 'value3', 0);

      return new Promise((resolve) => {
        setTimeout(() => {
          const keys = cache.getValidKeys();
          expect(keys).toContain('key3');
          expect(keys).not.toContain('key1');
          expect(keys).not.toContain('key2');
          resolve();
        }, 1100);
      });
    });
  });

  describe('淘汰回调', () => {
    test('应该调用淘汰回调', () => {
      const evicted = [];
      const cache = new Cache({
        maxSize: 2,
        onEvict: (key, value) => {
          evicted.push({ key, value });
        }
      });

      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.set('key3', 'value3');

      expect(evicted.length).toBe(1);
      expect(evicted[0].key).toBe('key1');
      expect(evicted[0].value).toBe('value1');
    });

    test('应该在过期时调用淘汰回调', () => {
      const evicted = [];
      const cache = new Cache({
        onEvict: (key, value) => {
          evicted.push({ key, value });
        }
      });

      cache.set('key1', 'value1', 1);

      return new Promise((resolve) => {
        setTimeout(() => {
          cache.get('key1'); // 触发过期检查
          expect(evicted.length).toBe(1);
          expect(evicted[0].key).toBe('key1');
          resolve();
        }, 1100);
      });
    });
  });

  describe('边界情况', () => {
    test('应该处理空键', () => {
      const cache = new Cache();
      cache.set('', 'value');
      expect(cache.get('')).toBe('value');
    });

    test('应该处理 null 值', () => {
      const cache = new Cache();
      cache.set('key', null);
      expect(cache.get('key')).toBeNull();
    });

    test('应该处理 undefined 值', () => {
      const cache = new Cache();
      cache.set('key', undefined);
      expect(cache.get('key')).toBeUndefined();
    });

    test('应该处理复杂对象', () => {
      const cache = new Cache();
      const obj = { name: 'test', nested: { value: 123 }, array: [1, 2, 3] };
      cache.set('key', obj);
      const result = cache.get('key');
      expect(result).toEqual(obj);
    });

    test('应该处理大对象', () => {
      const cache = new Cache();
      const bigObj = { data: Array(10000).fill('x').join('') };
      cache.set('big', bigObj);
      const result = cache.get('big');
      expect(result).toEqual(bigObj);
    });
  });

  describe('性能', () => {
    test('应该快速设置和获取', () => {
      const cache = new Cache({ maxSize: 10000 });
      const start = Date.now();

      for (let i = 0; i < 1000; i++) {
        cache.set(`key${i}`, `value${i}`);
      }

      for (let i = 0; i < 1000; i++) {
        cache.get(`key${i}`);
      }

      const end = Date.now();
      expect(end - start).toBeLessThan(100);
    });

    test('应该高效处理过期', () => {
      const cache = new Cache({ defaultTTL: 0, maxSize: 10000 });

      for (let i = 0; i < 1000; i++) {
        cache.set(`key${i}`, `value${i}`, 1);
      }

      // 等待过期
      return new Promise((resolve) => {
        setTimeout(() => {
          const start = Date.now();
          cache.clearExpired();
          const end = Date.now();

          expect(end - start).toBeLessThan(100);
          expect(cache.size()).toBe(0);
          resolve();
        }, 100);
      });
    });
  });
});
