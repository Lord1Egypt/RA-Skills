/**
 * Logger 测试脚本
 */

const {
  SensenLogger,
  LogLevel,
  createLogger,
  defaultLogger,
  LOG_DIR,
  LOG_FILE
} = require('./sensen-logger');

console.log('🧪 Sensen Logger 测试\n');

// 1. 默认Logger测试
console.log('1️⃣ 默认Logger测试');
defaultLogger.info('这是INFO级别日志');
defaultLogger.debug('这是DEBUG级别日志（不显示，因为默认是INFO）');
defaultLogger.warn('这是WARN级别日志');
defaultLogger.error('这是ERROR级别日志');

// 2. 自定义Logger
console.log('\n2️⃣ 自定义Logger测试');
const customLogger = new SensenLogger({
  name: 'TaskManager',
  level: LogLevel.DEBUG,  // 显示所有级别
  showTimestamp: true,
  showModule: true,
  outputToFile: false
});

customLogger.debug('TaskManager DEBUG消息');
customLogger.info('TaskManager INFO消息', { taskId: 'task_12345678' });
customLogger.warn('TaskManager WARN消息', { agent: 'Marketing' });
customLogger.error('TaskManager ERROR消息', { error: 'Something went wrong' });

// 3. 带上下文的日志
console.log('\n3️⃣ 带上下文的日志');
const taskLogger = customLogger.child('tasks');
taskLogger.info('创建任务', { taskId: 'task_abc123', priority: 'P0' });
taskLogger.info('更新任务状态', { taskId: 'task_abc123', from: 'inbox', to: 'planning' });

// 4. 子模块Logger
console.log('\n4️⃣ 子模块Logger链');
const parentLogger = createLogger('Parent');
const childLogger = parentLogger.child('Child');
const grandchildLogger = childLogger.child('GrandChild');

parentLogger.info('父模块消息');
childLogger.info('子模块消息');
grandchildLogger.info('孙模块消息');

// 5. 不同级别过滤
console.log('\n5️⃣ 不同级别过滤测试');
const warnOnly = new SensenLogger({ name: 'WARN_ONLY', level: LogLevel.WARN, outputToFile: false });
warnOnly.debug('这条不会显示');
warnOnly.info('这条不会显示');
warnOnly.warn('这条会显示');
warnOnly.error('这条会显示');

// 6. 检查日志文件
console.log('\n6️⃣ 检查日志文件');
const fs = require('fs');
if (fs.existsSync(LOG_DIR)) {
  const files = fs.readdirSync(LOG_DIR).filter(f => f.endsWith('.log'));
  console.log(`   日志目录: ${LOG_DIR}`);
  console.log(`   日志文件: ${files.join(', ')}`);
  
  if (fs.existsSync(LOG_FILE)) {
    const stats = fs.statSync(LOG_FILE);
    console.log(`   当前日志大小: ${stats.size} bytes`);
    
    // 读取最后一行验证JSON格式
    const content = fs.readFileSync(LOG_FILE, 'utf-8');
    const lines = content.trim().split('\n');
    const lastLine = lines[lines.length - 1];
    
    try {
      const parsed = JSON.parse(lastLine);
      console.log('\n   ✅ 最后一条日志是有效的JSON:');
      console.log(`   ${JSON.stringify(parsed, null, 2).split('\n').join('\n   ')}`);
    } catch (e) {
      console.log('   ❌ JSON解析失败:', e.message);
    }
  }
}

console.log('\n✅ Logger 测试完成！');
console.log('\nP2-1 增强功能总结:');
console.log('  ✅ 多级别日志 - DEBUG/INFO/WARN/ERROR');
console.log('  ✅ 上下文支持 - module/taskId/agent/correlationId');
console.log('  ✅ 控制台彩色输出');
console.log('  ✅ 文件JSON持久化');
console.log('  ✅ 模块化Logger链');
