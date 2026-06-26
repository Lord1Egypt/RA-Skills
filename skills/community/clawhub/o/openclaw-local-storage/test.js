const OpenClawLocalStorage = require('./src/index');

async function test() {
  const storage = new OpenClawLocalStorage();

  // 测试初始化
  console.log('=== 测试初始化 ===');
  let result = await storage.processCommand('存储一条用户信息：{"name": "张三", "age": 25, "email": "zhangsan@example.com"}');
  console.log(result);

  // 测试添加数据
  console.log('\n=== 测试添加数据 ===');
  result = await storage.processCommand('添加一条用户信息：name为李四，age为30，email为lisi@example.com');
  console.log(result);

  // 测试查询所有数据
  console.log('\n=== 测试查询所有数据 ===');
  result = await storage.processCommand('查询所有用户信息');
  console.log(result);

  // 测试条件查询
  console.log('\n=== 测试条件查询 ===');
  result = await storage.processCommand('查询name为张三的用户信息');
  console.log(result);

  // 测试修改数据
  console.log('\n=== 测试修改数据 ===');
  result = await storage.processCommand('修改name为张三的用户信息，age改为26');
  console.log(result);

  // 测试删除数据
  console.log('\n=== 测试删除数据 ===');
  result = await storage.processCommand('删除name为李四的用户信息');
  console.log(result);

  // 测试查询所有数据（验证删除结果）
  console.log('\n=== 测试查询所有数据（验证删除结果） ===');
  result = await storage.processCommand('查询所有用户信息');
  console.log(result);
}

test().catch(console.error);