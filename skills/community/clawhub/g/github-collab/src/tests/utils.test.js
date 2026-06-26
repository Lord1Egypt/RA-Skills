/**
 * Utils 单元测试
 */

const utils = require('../utils/helpers');

describe('Utils - 格式化函数', () => {
  describe('formatStatus', () => {
    test('应该正确格式化各种状态', () => {
      expect(utils.formatStatus('pending')).toBe('⏳ 待分配');
      expect(utils.formatStatus('in_progress')).toBe('🔄 进行中');
      expect(utils.formatStatus('completed')).toBe('✅ 已完成');
      expect(utils.formatStatus('cancelled')).toBe('❌ 已取消');
      expect(utils.formatStatus('unknown')).toBe('🔵 unknown');
    });
  });

  describe('formatPriority', () => {
    test('应该正确格式化各种优先级', () => {
      expect(utils.formatPriority(1)).toBe('🔴 高');
      expect(utils.formatPriority(2)).toBe('🟡 中');
      expect(utils.formatPriority(3)).toBe('🟢 低');
      expect(utils.formatPriority(99)).toBe('⚪ 99');
    });
  });

  describe('formatTime', () => {
    test('应该格式化有效日期', () => {
      const date = new Date('2024-01-15T10:30:00');
      const result = utils.formatTime(date);
      expect(result).toBeTruthy();
      expect(typeof result).toBe('string');
    });

    test('应该处理 null/undefined', () => {
      expect(utils.formatTime(null)).toBe('-');
      expect(utils.formatTime(undefined)).toBe('-');
      expect(utils.formatTime()).toBe('-');
    });
  });

  describe('formatTimeDiff', () => {
    test('应该格式化不同时间差', () => {
      // 刚刚
      const now = new Date();
      expect(utils.formatTimeDiff(now)).toBe('刚刚');

      // 几分钟前
      const minutesAgo = new Date(Date.now() - 5 * 60000);
      expect(utils.formatTimeDiff(minutesAgo)).toBe('5 分钟前');

      // 几小时前
      const hoursAgo = new Date(Date.now() - 3 * 60 * 60000);
      expect(utils.formatTimeDiff(hoursAgo)).toBe('3 小时前');

      // 几天前
      const daysAgo = new Date(Date.now() - 2 * 24 * 60 * 60000);
      expect(utils.formatTimeDiff(daysAgo)).toBe('2 天前');

      // null
      expect(utils.formatTimeDiff(null)).toBe('-');
    });
  });

  describe('createProgressBar', () => {
    test('应该创建正确的进度条', () => {
      expect(utils.createProgressBar(0, 10)).toBe('░░░░░░░░░░');
      expect(utils.createProgressBar(50, 10)).toBe('█████░░░░░');
      expect(utils.createProgressBar(100, 10)).toBe('██████████');
      expect(utils.createProgressBar(25, 20)).toBe('█████░░░░░░░░░░░░░░░');
    });

    test('应该处理边界值', () => {
      expect(utils.createProgressBar(-10, 10)).toBe('░░░░░░░░░░');
      expect(utils.createProgressBar(150, 10)).toBe('██████████');
    });
  });

  describe('createTable', () => {
    test('应该创建正确的表格', () => {
      const headers = ['Name', 'Age'];
      const rows = [
        ['Alice', '30'],
        ['Bob', '25']
      ];
      const result = utils.createTable(headers, rows);
      expect(result).toContain('Name');
      expect(result).toContain('Alice');
      expect(result).toContain('─');
    });

    test('应该处理空数据', () => {
      const result = utils.createTable(['Col'], []);
      expect(result).toContain('Col');
    });
  });
});

describe('Utils - 数据处理函数', () => {
  describe('paginate', () => {
    test('应该正确分页', () => {
      const items = Array.from({ length: 25 }, (_, i) => i);
      const result = utils.paginate(items, 1, 10);

      expect(result.items.length).toBe(10);
      expect(result.total).toBe(25);
      expect(result.page).toBe(1);
      expect(result.pageSize).toBe(10);
      expect(result.totalPages).toBe(3);
    });

    test('应该处理最后一页', () => {
      const items = Array.from({ length: 25 }, (_, i) => i);
      const result = utils.paginate(items, 3, 10);
      expect(result.items.length).toBe(5);
    });

    test('应该处理超出范围的页码', () => {
      const items = [1, 2, 3];
      const result = utils.paginate(items, 100, 10);
      expect(result.items.length).toBe(0);
    });
  });

  describe('sortByKey', () => {
    test('应该按升序排序', () => {
      const items = [{ name: 'C' }, { name: 'A' }, { name: 'B' }];
      const result = utils.sortByKey(items, 'name', 'asc');
      expect(result[0].name).toBe('A');
      expect(result[1].name).toBe('B');
      expect(result[2].name).toBe('C');
    });

    test('应该按降序排序', () => {
      const items = [{ name: 'C' }, { name: 'A' }, { name: 'B' }];
      const result = utils.sortByKey(items, 'name', 'desc');
      expect(result[0].name).toBe('C');
      expect(result[1].name).toBe('B');
      expect(result[2].name).toBe('A');
    });

    test('不应该修改原数组', () => {
      const items = [{ name: 'C' }, { name: 'A' }];
      const original = JSON.stringify(items);
      utils.sortByKey(items, 'name');
      expect(JSON.stringify(items)).toBe(original);
    });
  });

  describe('filterBy', () => {
    test('应该正确过滤数据', () => {
      const items = [
        { status: 'active', name: 'A' },
        { status: 'inactive', name: 'B' },
        { status: 'active', name: 'C' }
      ];
      const result = utils.filterBy(items, 'status', 'active');
      expect(result.length).toBe(2);
      expect(result.every((r) => r.status === 'active')).toBe(true);
    });

    test('应该返回空数组当没有匹配项', () => {
      const items = [{ status: 'active' }];
      const result = utils.filterBy(items, 'status', 'inactive');
      expect(result.length).toBe(0);
    });
  });

  describe('findFirst', () => {
    test('应该找到第一个匹配项', () => {
      const items = [{ id: 1 }, { id: 2 }, { id: 3 }];
      const result = utils.findFirst(items, (item) => item.id > 1);
      expect(result.id).toBe(2);
    });

    test('应该返回 undefined 当没有匹配项', () => {
      const items = [{ id: 1 }];
      const result = utils.findFirst(items, (item) => item.id > 100);
      expect(result).toBeUndefined();
    });
  });

  describe('groupBy', () => {
    test('应该正确分组', () => {
      const items = [
        { category: 'A', name: 'A1' },
        { category: 'B', name: 'B1' },
        { category: 'A', name: 'A2' }
      ];
      const result = utils.groupBy(items, 'category');
      expect(result.A.length).toBe(2);
      expect(result.B.length).toBe(1);
    });
  });

  describe('countBy', () => {
    test('应该正确计数', () => {
      const items = [{ status: 'active' }, { status: 'inactive' }, { status: 'active' }];
      const result = utils.countBy(items, 'status');
      expect(result.active).toBe(2);
      expect(result.inactive).toBe(1);
    });
  });

  describe('sumBy', () => {
    test('应该正确求和', () => {
      const items = [{ value: 1 }, { value: 2 }, { value: 3 }];
      expect(utils.sumBy(items, 'value')).toBe(6);
    });

    test('应该处理空数组', () => {
      expect(utils.sumBy([], 'value')).toBe(0);
    });

    test('应该处理缺失值', () => {
      const items = [{ value: 1 }, {}, { value: 3 }];
      expect(utils.sumBy(items, 'value')).toBe(4);
    });
  });

  describe('averageBy', () => {
    test('应该正确计算平均值', () => {
      const items = [{ value: 2 }, { value: 4 }, { value: 6 }];
      expect(utils.averageBy(items, 'value')).toBe(4);
    });

    test('应该处理空数组', () => {
      expect(utils.averageBy([], 'value')).toBe(0);
    });
  });

  describe('maxBy', () => {
    test('应该找到最大值', () => {
      const items = [{ value: 1 }, { value: 3 }, { value: 2 }];
      expect(utils.maxBy(items, 'value').value).toBe(3);
    });

    test('应该处理空数组', () => {
      expect(utils.maxBy([], 'value')).toBeNull();
    });
  });

  describe('minBy', () => {
    test('应该找到最小值', () => {
      const items = [{ value: 1 }, { value: 3 }, { value: 2 }];
      expect(utils.minBy(items, 'value').value).toBe(1);
    });

    test('应该处理空数组', () => {
      expect(utils.minBy([], 'value')).toBeNull();
    });
  });

  describe('uniqueBy', () => {
    test('应该去重', () => {
      const items = [
        { id: 1, name: 'A' },
        { id: 2, name: 'B' },
        { id: 1, name: 'C' }
      ];
      const result = utils.uniqueBy(items, 'id');
      expect(result.length).toBe(2);
    });
  });

  describe('limit', () => {
    test('应该限制数量', () => {
      const items = [1, 2, 3, 4, 5];
      expect(utils.limit(items, 3).length).toBe(3);
    });

    test('应该返回全部当限制大于数组长度', () => {
      const items = [1, 2, 3];
      expect(utils.limit(items, 10).length).toBe(3);
    });
  });
});

describe('Utils - 异步工具函数', () => {
  describe('sleep', () => {
    test('应该延迟指定时间', async () => {
      const start = Date.now();
      await utils.sleep(100);
      const end = Date.now();
      expect(end - start).toBeGreaterThanOrEqual(100);
    });
  });

  describe('retry', () => {
    test('应该成功当函数最终成功', async () => {
      let attempts = 0;
      const fn = () => {
        attempts++;
        if (attempts < 3) throw new Error('fail');
        return 'success';
      };
      const result = await utils.retry(fn, 5, 10);
      expect(result).toBe('success');
      expect(attempts).toBe(3);
    });

    test('应该抛出错误当所有尝试都失败', async () => {
      const fn = () => {
        throw new Error('always fail');
      };
      await expect(utils.retry(fn, 2, 10)).rejects.toThrow('always fail');
    });
  });

  describe('debounce', () => {
    test('应该防抖', async () => {
      let callCount = 0;
      const fn = () => callCount++;
      const debounced = utils.debounce(fn, 50);

      debounced();
      debounced();
      debounced();

      await utils.sleep(100);
      expect(callCount).toBe(1);
    });
  });

  describe('throttle', () => {
    test('应该节流', async () => {
      let callCount = 0;
      const fn = () => callCount++;
      const throttled = utils.throttle(fn, 50);

      throttled();
      throttled();
      throttled();

      await utils.sleep(60);
      throttled();

      await utils.sleep(60);
      expect(callCount).toBeGreaterThanOrEqual(2);
    });
  });
});

describe('Utils - 工具函数', () => {
  describe('generateId', () => {
    test('应该生成唯一 ID', () => {
      const ids = new Set();
      for (let i = 0; i < 100; i++) {
        ids.add(utils.generateId());
      }
      expect(ids.size).toBe(100);
    });

    test('应该返回字符串', () => {
      expect(typeof utils.generateId()).toBe('string');
    });
  });

  describe('isValidEmail', () => {
    test('应该验证有效邮箱', () => {
      expect(utils.isValidEmail('test@example.com')).toBe(true);
      expect(utils.isValidEmail('user.name@domain.co.uk')).toBe(true);
    });

    test('应该验证无效邮箱', () => {
      expect(utils.isValidEmail('invalid')).toBe(false);
      expect(utils.isValidEmail('@example.com')).toBe(false);
      expect(utils.isValidEmail('test@')).toBe(false);
    });
  });

  describe('isValidUrl', () => {
    test('应该验证有效 URL', () => {
      expect(utils.isValidUrl('https://example.com')).toBe(true);
      expect(utils.isValidUrl('http://localhost:3000')).toBe(true);
    });

    test('应该验证无效 URL', () => {
      expect(utils.isValidUrl('not-a-url')).toBe(false);
      expect(utils.isValidUrl('ftp://invalid')).toBe(false);
    });
  });

  describe('truncate', () => {
    test('应该截断长字符串', () => {
      const str = 'This is a very long string that needs to be truncated';
      const result = utils.truncate(str, 20);
      expect(result).toBe('This is a very lo...');
      expect(result.length).toBeLessThanOrEqual(23);
    });

    test('应该返回原字符串当不需要截断', () => {
      const str = 'Short';
      expect(utils.truncate(str, 10)).toBe('Short');
    });
  });

  describe('escapeHtml', () => {
    test('应该转义 HTML 特殊字符', () => {
      const input = '<script>alert("XSS")</script>';
      const result = utils.escapeHtml(input);
      expect(result).not.toContain('<');
      expect(result).not.toContain('>');
      expect(result).toContain('&lt;');
      expect(result).toContain('&gt;');
    });

    test('应该转义引号', () => {
      const input = 'He said "Hello"';
      const result = utils.escapeHtml(input);
      expect(result).toContain('&quot;');
    });
  });

  describe('deepClone', () => {
    test('应该深拷贝对象', () => {
      const original = { a: 1, b: { c: 2 } };
      const clone = utils.deepClone(original);
      clone.b.c = 3;
      expect(original.b.c).toBe(2);
    });

    test('应该深拷贝数组', () => {
      const original = [1, [2, 3]];
      const clone = utils.deepClone(original);
      clone[1][0] = 99;
      expect(original[1][0]).toBe(2);
    });
  });

  describe('mergeObjects', () => {
    test('应该合并多个对象', () => {
      const result = utils.mergeObjects({ a: 1 }, { b: 2 }, { c: 3 });
      expect(result).toEqual({ a: 1, b: 2, c: 3 });
    });

    test('后面的对象应该覆盖前面的', () => {
      const result = utils.mergeObjects({ a: 1 }, { a: 2 });
      expect(result.a).toBe(2);
    });
  });
});

describe('Utils - 对象工具函数', () => {
  describe('getKeys', () => {
    test('应该返回对象的所有键', () => {
      const obj = { a: 1, b: 2, c: 3 };
      const keys = utils.getKeys(obj);
      expect(keys).toEqual(expect.arrayContaining(['a', 'b', 'c']));
    });
  });

  describe('getValues', () => {
    test('应该返回对象的所有值', () => {
      const obj = { a: 1, b: 2, c: 3 };
      const values = utils.getValues(obj);
      expect(values).toEqual(expect.arrayContaining([1, 2, 3]));
    });
  });

  describe('getEntries', () => {
    test('应该返回对象的所有条目', () => {
      const obj = { a: 1, b: 2 };
      const entries = utils.getEntries(obj);
      expect(entries).toEqual([
        ['a', 1],
        ['b', 2]
      ]);
    });
  });
});

describe('Utils - 类型检查函数', () => {
  describe('isEmpty', () => {
    test('应该正确识别空值', () => {
      expect(utils.isEmpty(null)).toBe(true);
      expect(utils.isEmpty(undefined)).toBe(true);
      expect(utils.isEmpty('')).toBe(true);
      expect(utils.isEmpty([])).toBe(true);
      expect(utils.isEmpty({})).toBe(true);
    });

    test('应该正确识别非空值', () => {
      expect(utils.isEmpty(0)).toBe(false);
      expect(utils.isEmpty(false)).toBe(false);
      expect(utils.isEmpty('text')).toBe(false);
      expect(utils.isEmpty([1])).toBe(false);
      expect(utils.isEmpty({ a: 1 })).toBe(false);
    });
  });

  describe('isNumber', () => {
    test('应该正确识别数字', () => {
      expect(utils.isNumber(123)).toBe(true);
      expect(utils.isNumber('123')).toBe(true);
      expect(utils.isNumber(3.14)).toBe(true);
    });

    test('应该正确识别非数字', () => {
      expect(utils.isNumber('abc')).toBe(false);
      expect(utils.isNumber(NaN)).toBe(false);
    });
  });

  describe('isInteger', () => {
    test('应该正确识别整数', () => {
      expect(utils.isInteger(123)).toBe(true);
      expect(utils.isInteger(0)).toBe(true);
      expect(utils.isInteger(-1)).toBe(true);
    });

    test('应该正确识别非整数', () => {
      expect(utils.isInteger(3.14)).toBe(false);
      expect(utils.isInteger('123')).toBe(false);
    });
  });

  describe('isString', () => {
    test('应该正确识别字符串', () => {
      expect(utils.isString('hello')).toBe(true);
      expect(utils.isString('')).toBe(true);
    });

    test('应该正确识别非字符串', () => {
      expect(utils.isString(123)).toBe(false);
      expect(utils.isString(null)).toBe(false);
    });
  });

  describe('isArray', () => {
    test('应该正确识别数组', () => {
      expect(utils.isArray([])).toBe(true);
      expect(utils.isArray([1, 2, 3])).toBe(true);
    });

    test('应该正确识别非数组', () => {
      expect(utils.isArray({})).toBe(false);
      expect(utils.isArray('string')).toBe(false);
    });
  });

  describe('isObject', () => {
    test('应该正确识别对象', () => {
      expect(utils.isObject({})).toBe(true);
      expect(utils.isObject({ a: 1 })).toBe(true);
    });

    test('应该正确识别非对象', () => {
      expect(utils.isObject([])).toBe(false);
      expect(utils.isObject(null)).toBe(false);
      expect(utils.isObject('string')).toBe(false);
    });
  });

  describe('isFunction', () => {
    test('应该正确识别函数', () => {
      expect(utils.isFunction(() => {})).toBe(true);
      expect(utils.isFunction(function () {})).toBe(true);
    });

    test('应该正确识别非函数', () => {
      expect(utils.isFunction({})).toBe(false);
      expect(utils.isFunction(123)).toBe(false);
    });
  });

  describe('isDate', () => {
    test('应该正确识别日期', () => {
      expect(utils.isDate(new Date())).toBe(true);
    });

    test('应该正确识别无效日期', () => {
      expect(utils.isDate(new Date('invalid'))).toBe(false);
      expect(utils.isDate({})).toBe(false);
    });
  });

  describe('isBoolean', () => {
    test('应该正确识别布尔值', () => {
      expect(utils.isBoolean(true)).toBe(true);
      expect(utils.isBoolean(false)).toBe(true);
    });

    test('应该正确识别非布尔值', () => {
      expect(utils.isBoolean(1)).toBe(false);
      expect(utils.isBoolean('true')).toBe(false);
    });
  });

  describe('isNull', () => {
    test('应该正确识别 null', () => {
      expect(utils.isNull(null)).toBe(true);
      expect(utils.isNull(undefined)).toBe(false);
      expect(utils.isNull(0)).toBe(false);
    });
  });

  describe('isUndefined', () => {
    test('应该正确识别 undefined', () => {
      expect(utils.isUndefined(undefined)).toBe(true);
      expect(utils.isUndefined(null)).toBe(false);
      expect(utils.isUndefined(void 0)).toBe(true);
    });
  });

  describe('isNil', () => {
    test('应该正确识别 null 和 undefined', () => {
      expect(utils.isNil(null)).toBe(true);
      expect(utils.isNil(undefined)).toBe(true);
      expect(utils.isNil(0)).toBe(false);
    });
  });

  describe('isTruthy', () => {
    test('应该正确识别真值', () => {
      expect(utils.isTruthy(1)).toBe(true);
      expect(utils.isTruthy('text')).toBe(true);
      expect(utils.isTruthy({})).toBe(true);
    });

    test('应该正确识别假值', () => {
      expect(utils.isTruthy(0)).toBe(false);
      expect(utils.isTruthy('')).toBe(false);
      expect(utils.isTruthy(null)).toBe(false);
    });
  });

  describe('isFalsy', () => {
    test('应该正确识别假值', () => {
      expect(utils.isFalsy(0)).toBe(true);
      expect(utils.isFalsy('')).toBe(true);
      expect(utils.isFalsy(null)).toBe(true);
      expect(utils.isFalsy(undefined)).toBe(true);
      expect(utils.isFalsy(false)).toBe(true);
      expect(utils.isFalsy(NaN)).toBe(true);
    });

    test('应该正确识别真值', () => {
      expect(utils.isFalsy(1)).toBe(false);
      expect(utils.isFalsy('text')).toBe(false);
    });
  });
});
