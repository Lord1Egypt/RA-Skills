------WebKitFormBoundary9i2sdz5srmd
Content-Disposition: form-data; name="file"; filename="test.js"
Content-Type: application/javascript

// 测试脚本 - 验证问候技能功能
const greeting = require('./greeting.js');

console.log('=== liufeng-greeting-skill 功能测试 ===\n');

// 测试数据
const testCases = [
  { input: '你好', expected: true, description: '中文问候' },
  { input: 'Hello!', expected: true, description: '英文问候' },
  { input: '嗨，在吗？', expected: true, description: '混合问候' },
  { input: '早上好', expected: true, description: '时间问候' },
  { input: '今天天气怎么样？', expected: false, description: '非问候消息' },
  { input: '', expected: false, description: '空消息' },
  { input: 'HELLO WORLD', expected: true, description: '大写英文' },
  { input: '你好，我想问个问题', expected: true, description: '问候+内容' }
];

// 运行测试
let passed = 0;
let failed = 0;

testCases.forEach((testCase, index) => {
  const result = greeting.isGreetingMessage(testCase.input);
  const success = result === testCase.expected;
  
  console.log(`测试 ${index + 1}: ${testCase.description}`);
  console.log(`  输入: "${testCase.input}"`);
  console.log(`  预期: ${testCase.expected}, 实际: ${result}`);
  console.log(`  结果: ${success ? '✅ 通过' : '❌ 失败'}\n`);
  
  if (success) {
    passed++;
  } else {
    failed++;
  }
  
  // 如果触发问候，显示示例回复
  if (result) {
    console.log(`  示例回复:`);
    console.log(`  ${greeting.generateGreetingResponse()}\n`);
  }
});

// 显示当前时间功能
console.log('=== 时间功能测试 ===');
console.log(`当前时间: ${greeting.getCurrentTime()}`);
console.log(`时区: Asia/Shanghai\n`);

// 测试结果汇总
console.log('=== 测试结果汇总 ===');
console.log(`总测试数: ${testCases.length}`);
console.log(`通过: ${passed}`);
console.log(`失败: ${failed}`);
console.log(`通过率: ${((passed / testCases.length) * 100).toFixed(1)}%`);

if (failed === 0) {
  console.log('\n🎉 所有测试通过！技能功能正常。');
} else {
  console.log('\n⚠️  有测试失败，请检查技能逻辑。');
}

// 测试handleGreeting函数
console.log('\n=== handleGreeting函数测试 ===');
const context = {
  message: '你好，柳峰',
  user: { name: '柳峰', id: 'liufeng' }
};

const response = greeting.handleGreeting(context);
if (response) {
  console.log('触发成功！');
  console.log('回复内容:', response.reply);
  console.log('元数据:', JSON.stringify(response.metadata, null, 2));
} else {
  console.log('未触发（这不应该发生，因为输入包含"你好"）');
}
------WebKitFormBoundary9i2sdz5srmd--
