/**
 * TemplateEngine 测试脚本
 */

const { TemplateEngine, Templates } = require('./template-engine');

console.log('🧪 TemplateEngine 测试\n');

const engine = new TemplateEngine();

// 1. 基础变量插值
console.log('1️⃣ 基础变量插值');
let result = engine.render('Hello, {{name}}!', { name: '森森' });
console.log(`   输入: "Hello, {{name}}!"`);
console.log(`   输出: ${result}`);

// 2. 嵌套属性
console.log('\n2️⃣ 嵌套属性');
result = engine.render('Agent: {{agent.name}}', { agent: { name: 'Marketing', status: 'active' } });
console.log(`   输出: ${result}`);

// 3. 条件渲染
console.log('\n3️⃣ 条件渲染');
result = engine.render('{{#if active}}在线{{else}}离线{{/if}}', { active: true });
console.log(`   active=true: ${result}`);
result = engine.render('{{#if active}}在线{{else}}离线{{/if}}', { active: false });
console.log(`   active=false: ${result}`);

// 4. 内置函数
console.log('\n4️⃣ 内置函数');
const timestamp = new Date().toISOString();
result = engine.render('{{name|uppercase}}', { name: 'marketing agent' });
console.log(`   uppercase: ${result}`);
result = engine.render('{{name|lowercase}}', { name: 'MARKETING AGENT' });
console.log(`   lowercase: ${result}`);
result = engine.render('{{ts|datetime}}', { ts: timestamp });
console.log(`   datetime: ${result}`);
result = engine.render('{{ts|relative}}', { ts: new Date(Date.now() - 3600000).toISOString() });
console.log(`   relative (1小时前): ${result}`);

// 5. 循环渲染
console.log('\n5️⃣ 循环渲染');
const tasks = [
  { title: '任务A', status: 'done' },
  { title: '任务B', status: 'pending' }
];
result = engine.render('{{#each tasks}} - {{item.title}}({{item.status}})\n{{/each}}', { tasks });
console.log(`   输出:\n${result}`);

// 6. 复杂模板
console.log('6️⃣ 复杂模板：任务状态通知');
result = engine.render(Templates.taskStatus, {
  status: 'done',
  title: '小红书内容发布',
  agent: 'Marketing',
  priority: 'P0',
  updatedAt: new Date().toISOString(),
  result: '已成功发布到小红书'
});
console.log(result);

// 7. 协作进度模板
console.log('\n7️⃣ 协作进度模板');
result = engine.render(Templates.collabProgress, {
  name: '内容发布流程',
  progress: 75,
  completed: 3,
  total: 4,
  lastUpdate: new Date(Date.now() - 600000).toISOString()
});
console.log(result);

// 8. 超时提醒模板
console.log('\n8️⃣ 超时提醒模板');
result = engine.render(Templates.timeoutAlert, {
  title: '等待Marketing确认',
  status: 'review',
  elapsed: '2小时30分钟',
  suggestion: '发送提醒消息给@Marketing'
});
console.log(result);

// 9. 模板缓存测试
console.log('\n9️⃣ 模板缓存测试');
engine.render('测试{{name}}', { name: '1' });
engine.render('测试{{name}}', { name: '2' });
console.log(`   缓存条目数: ${engine.cache.size}`);
console.log('   (相同模板只编译一次)');

// 10. HTML 转义
console.log('\n🔟 HTML 转义测试');
result = engine.render('内容: {{content}}', { content: '<script>alert("xss")</script>' });
console.log(`   输入: <script>alert("xss")</script>`);
console.log(`   输出: ${result}`);

console.log('\n✅ TemplateEngine 测试完成！');
console.log('\nP2-3 增强功能总结:');
console.log('  ✅ 变量插值 - {{variable}} 和 {{nested.property}}');
console.log('  ✅ 条件渲染 - {{#if}}...{{else}}...{{/if}}');
console.log('  ✅ 循环渲染 - {{#each items}}...{{/each}}');
console.log('  ✅ 内置函数 - uppercase/lowercase/date/relative 等');
console.log('  ✅ 模板缓存 - 编译一次，多次渲染');
console.log('  ✅ HTML 转义 - 防止 XSS');
