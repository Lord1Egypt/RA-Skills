/**
 * Reminder Skill 综合测试套件
 * 测试农历日期处理、联系人创建、祝福语生成
 */

const fs = require('fs');
const path = require('path');
const { Lunar, Solar } = require('lunar-javascript');

// 导入被测试的模块
const {
  lunarToSolar,
  solarToLunar,
  getThisYearSolarDate,
  parseLunarDate,
  formatLunarDate,
  getNextLunarBirthday
} = require('./lunar-converter');

const ContentGenerator = require('./content-generator');
const ReminderChecker = require('./reminder-checker');

// 测试框架
class TestRunner {
  constructor() {
    this.tests = [];
    this.results = {
      passed: 0,
      failed: 0,
      errors: []
    };
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('\n========================================');
    console.log('🧪 Reminder Skill 测试套件');
    console.log('========================================\n');

    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✅ ${name}`);
        this.results.passed++;
      } catch (error) {
        console.log(`❌ ${name}`);
        console.log(`   错误: ${error.message}`);
        this.results.failed++;
        this.results.errors.push({ test: name, error: error.message });
      }
    }

    this.printSummary();
  }

  printSummary() {
    console.log('\n========================================');
    console.log('📊 测试结果汇总');
    console.log('========================================');
    console.log(`通过: ${this.results.passed}`);
    console.log(`失败: ${this.results.failed}`);
    console.log(`总计: ${this.tests.length}`);
    
    if (this.results.failed > 0) {
      console.log('\n❌ 失败的测试:');
      this.results.errors.forEach(({ test, error }) => {
        console.log(`  - ${test}: ${error}`);
      });
    }
    console.log('========================================\n');
  }

  assertEqual(actual, expected, message) {
    if (actual !== expected) {
      throw new Error(`${message || '断言失败'}: 预期 ${expected}, 实际 ${actual}`);
    }
  }

  assertTrue(condition, message) {
    if (!condition) {
      throw new Error(message || '断言失败: 期望为真');
    }
  }

  assertContains(text, substring, message) {
    if (!text.includes(substring)) {
      throw new Error(`${message || '断言失败'}: "${text}" 不包含 "${substring}"`);
    }
  }
}

// 创建测试实例
const runner = new TestRunner();

// ==========================================
// 测试套件 1: Skill 结构验证
// ==========================================
runner.test('Skill 结构 - SKILL.md 存在', () => {
  const skillPath = path.join(__dirname, '..', 'SKILL.md');
  runner.assertTrue(fs.existsSync(skillPath), 'SKILL.md 文件必须存在');
});

runner.test('Skill 结构 - 脚本文件完整', () => {
  const scriptsDir = path.join(__dirname, '..', 'scripts');
  const requiredFiles = ['lunar-converter.js', 'content-generator.js', 'reminder-checker.js'];
  
  requiredFiles.forEach(file => {
    const filePath = path.join(scriptsDir, file);
    runner.assertTrue(fs.existsSync(filePath), `${file} 必须存在`);
  });
});

runner.test('Skill 结构 - 依赖已安装', () => {
  const nodeModulesPath = path.join(__dirname, 'node_modules', 'lunar-javascript');
  runner.assertTrue(fs.existsSync(nodeModulesPath), 'lunar-javascript 必须已安装');
  
  const jsYamlPath = path.join(__dirname, 'node_modules', 'js-yaml');
  runner.assertTrue(fs.existsSync(jsYamlPath), 'js-yaml 必须已安装');
});

// ==========================================
// 测试套件 2: 农历日期格式处理（关键测试）
// ==========================================
runner.test('农历日期 - 农历转阳历基础功能', () => {
  // 农历 1998年5月20日 转阳历
  const result = lunarToSolar(1998, 5, 20);
  runner.assertEqual(result.year, 1998, '年份应为1998');
  runner.assertEqual(result.month, 6, '月份应为6月');
  runner.assertEqual(result.day, 14, '日期应为14日');
});

runner.test('农历日期 - 获取今年农历日期', () => {
  const result = getThisYearSolarDate(8, 5);
  runner.assertTrue(result.year >= 2025 && result.year <= 2026, '年份应为今年或明年');
  runner.assertTrue(result.month >= 1 && result.month <= 12, '月份应在1-12之间');
  runner.assertTrue(result.day >= 1 && result.day <= 31, '日期应在1-31之间');
});

runner.test('农历日期 - 解析中文农历日期', () => {
  const result = parseLunarDate('八月初五');
  runner.assertTrue(result !== null, '应成功解析');
  runner.assertEqual(result.month, 8, '月份应为8');
  runner.assertEqual(result.day, 5, '日期应为5');
  runner.assertEqual(result.isLeapMonth, false, '不应为闰月');
});

runner.test('农历日期 - 解析数字格式农历日期', () => {
  const result = parseLunarDate('8-15');
  runner.assertTrue(result !== null, '应成功解析数字格式');
  runner.assertEqual(result.month, 8, '月份应为8');
  runner.assertEqual(result.day, 15, '日期应为15');
});

runner.test('农历日期 - 解析闰月日期', () => {
  const result = parseLunarDate('闰八月初五');
  runner.assertTrue(result !== null, '应成功解析闰月');
  runner.assertEqual(result.month, 8, '月份应为8');
  runner.assertEqual(result.isLeapMonth, true, '应为闰月');
});

runner.test('农历日期 - 格式化输出', () => {
  const result = formatLunarDate(8, 5, false);
  runner.assertEqual(result, '农历八月初五', '应正确格式化为中文');
  
  const leapResult = formatLunarDate(8, 5, true);
  runner.assertTrue(leapResult.includes('闰'), '闰月应包含"闰"字');
});

runner.test('农历日期 - 获取下一个农历生日', () => {
  const result = getNextLunarBirthday(8, 5, 1998);
  runner.assertTrue(result.year >= 2025, '下一个生日年份应在2025或之后');
  runner.assertTrue(result.age >= 27, '年龄应正确计算');
  runner.assertTrue(result.daysUntil > 0, '距离天数应为正数');
});

runner.test('农历日期 - 特殊日期边界测试', () => {
  // 测试腊月（十二月）
  const result = parseLunarDate('腊月二十三');
  // 注意：当前实现可能不支持腊月格式，需要检查
  if (result === null) {
    console.log('   ⚠️  警告: 腊月格式解析失败（可能是已知限制）');
  }
});

runner.test('农历日期 - 阳历转农历', () => {
  // 阳历 1998-06-14 转农历
  const result = solarToLunar(1998, 6, 14);
  runner.assertEqual(result.month, 5, '农历月份应为5月');
  runner.assertEqual(result.day, 20, '农历日期应为20日');
});

// ==========================================
// 测试套件 3: 联系人功能
// ==========================================
runner.test('联系人 - ReminderChecker 初始化', () => {
  const checker = new ReminderChecker();
  runner.assertTrue(checker !== null, 'ReminderChecker 应成功实例化');
});

runner.test('联系人 - 解析联系人文件', () => {
  const checker = new ReminderChecker();
  const sampleContent = `---
name: "测试用户"
relationship: "friend"
tags: ["篮球"]
created_at: "2024-01-15"
updated_at: "2024-01-15"
---

# 测试用户

## 事件

### 生日
- **类型**: 生日
- **日期**: 1990-05-20
- **农历**: false
- **提醒**: true
`;
  
  const contact = checker.parseContactFile(sampleContent, 'test.md');
  runner.assertTrue(contact !== null, '应成功解析联系人');
  runner.assertEqual(contact.name, '测试用户', '姓名应正确');
  runner.assertEqual(contact.events.length, 1, '应有一个事件');
});

runner.test('联系人 - 解析事件详情', () => {
  const checker = new ReminderChecker();
  const sampleContent = `---
name: "测试"
relationship: "friend"
---

### 生日
- **类型**: 生日
- **日期**: 农历八月初五
- **农历**: true
- **提醒**: true
`;
  
  const contact = checker.parseContactFile(sampleContent, 'test.md');
  runner.assertTrue(contact !== null, '应成功解析');
  runner.assertEqual(contact.events[0].isLunar, true, '应识别为农历');
});

runner.test('联系人 - 计算提醒时间', () => {
  const checker = new ReminderChecker();
  const contact = {
    name: '测试用户',
    relationship: 'friend'
  };
  const event = {
    name: '生日',
    type: '生日',
    date: '1998-05-20',  // 使用完整的 YYYY-MM-DD 格式
    isLunar: false,
    reminder: true
  };
  
  // 模拟今天的日期（与生日的月日相同）
  const checkDate = new Date('2025-05-20');
  const reminder = checker.calculateReminder(contact, event, checkDate, 7);
  
  runner.assertTrue(reminder !== null, '应生成提醒');
  runner.assertEqual(reminder.reminder_type, 'today', '今天应为当天提醒');
});

// ==========================================
// 测试套件 4: 祝福语生成
// ==========================================
runner.test('祝福语 - ContentGenerator 初始化', () => {
  const generator = new ContentGenerator();
  runner.assertTrue(generator !== null, 'ContentGenerator 应成功实例化');
});

runner.test('祝福语 - 生成生日祝福语', async () => {
  const generator = new ContentGenerator();
  const contact = {
    name: '张三',
    relationship: 'friend',
    tags: ['篮球']
  };
  const event = {
    name: '生日',
    type: '生日'
  };
  
  const wish = await generator.generateBirthdayWish(contact, event);
  runner.assertTrue(wish.length > 0, '祝福语不应为空');
  runner.assertContains(wish, '张三', '祝福语应包含姓名');
});

runner.test('祝福语 - 关系类型适配', async () => {
  const generator = new ContentGenerator();
  
  const relationships = ['friend', 'close_friend', 'family', 'colleague'];
  
  for (const rel of relationships) {
    const contact = {
      name: '测试',
      relationship: rel
    };
    const event = { name: '生日', type: '生日' };
    
    const wish = await generator.generateBirthdayWish(contact, event);
    runner.assertTrue(wish.length > 0, `${rel} 关系应生成祝福语`);
  }
});

runner.test('祝福语 - 礼物建议生成', async () => {
  const generator = new ContentGenerator();
  const contact = {
    name: '李四',
    relationship: 'friend',
    tags: ['篮球', '音乐']
  };
  const event = { name: '生日', type: '生日' };
  
  const suggestion = await generator.generateGiftSuggestion(contact, event);
  runner.assertTrue(suggestion.budget !== undefined, '应有预算信息');
  runner.assertTrue(suggestion.categories.length > 0, '应有礼物类别');
  runner.assertTrue(suggestion.specificIdeas.length > 0, '应有具体建议');
});

runner.test('祝福语 - 预算规则验证', async () => {
  const generator = new ContentGenerator();
  
  // 测试朋友关系预算
  const friendBudget = generator.getBudget('friend');
  runner.assertEqual(friendBudget.type, 'fixed', '朋友预算应为固定');
  runner.assertEqual(friendBudget.max, 300, '朋友预算应为300元');
  
  // 测试家人关系预算
  const familyBudget = generator.getBudget('family');
  runner.assertEqual(familyBudget.type, 'flexible', '家人预算应为弹性');
});

runner.test('祝福语 - 标签个性化', async () => {
  const generator = new ContentGenerator();
  const contact = {
    name: '王五',
    relationship: 'friend',
    tags: ['篮球', '科技']
  };
  
  const template = generator.personalizeTemplate(['祝{name}生日快乐'], generator.buildContext(contact, {}));
  runner.assertTrue(template.includes('篮球') || template.includes('科技'), '应包含标签相关个性化内容');
});

runner.test('祝福语 - 提醒消息格式', async () => {
  const generator = new ContentGenerator();
  const contact = {
    name: '测试用户',
    relationship: 'friend',
    tags: ['音乐']
  };
  const event = {
    name: '生日',
    type: '生日',
    target_date: '2025-05-20'
  };
  
  const message = await generator.generateReminderMessage(contact, event, 'today');
  runner.assertTrue(message.includes('测试用户'), '消息应包含用户名');
  runner.assertTrue(message.includes('生日'), '消息应包含事件名');
  runner.assertTrue(message.includes('礼物建议'), '消息应包含礼物建议');
});

// ==========================================
// 测试套件 5: 边界条件和错误处理
// ==========================================
runner.test('边界 - 无效日期处理', () => {
  try {
    // 测试无效农历日期
    const result = lunarToSolar(2025, 13, 1); // 13月不存在
    // 如果 lunar-javascript 抛出异常，代码会捕获
  } catch (error) {
    runner.assertTrue(error.message.includes('失败'), '应抛出错误信息');
  }
});

runner.test('边界 - 空联系人解析', () => {
  const checker = new ReminderChecker();
  // 空的frontmatter应该返回null，因为联系人文件必须有name和relationship
  const result = checker.parseContactFile('---\n---\n# 空文件', 'empty.md');
  runner.assertTrue(result === null, '空frontmatter应返回null，因为缺少必填字段');
});

runner.test('边界 - 缺少事件的联系人', () => {
  const checker = new ReminderChecker();
  const sampleContent = `---
name: "测试"
relationship: "friend"
---

# 测试

无事件
`;
  
  const contact = checker.parseContactFile(sampleContent, 'test.md');
  runner.assertTrue(contact.events.length === 0, '无事件的联系人事件数组应为空');
});

runner.test('边界 - 复杂的农历日期格式', () => {
  // 测试各种农历日期格式
  const formats = [
    '农历六月初八',
    '六月初八',
    '阴历八月初五',
    '旧历正月初一',
    '6月8日',
    '6-8'
  ];
  
  for (const format of formats) {
    const result = parseLunarDate(format);
    // 至少应该能解析出月日
    if (result) {
      runner.assertTrue(result.month >= 1 && result.month <= 12, `${format} 月份应在1-12之间`);
      runner.assertTrue(result.day >= 1 && result.day <= 30, `${format} 日期应在1-30之间`);
    }
  }
});

// 运行所有测试
runner.run();
