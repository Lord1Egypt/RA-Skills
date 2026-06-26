/**
 * 创建全新的飞书多维表格
 * 用法: node scripts/create_bitable_app.js --name "表格名称"
 */
const path = require('path');
const { apiPost } = require(path.join(__dirname, 'request'));
const { CONFIG } = require(path.join(__dirname, 'config'));
const readline = require('readline');

async function createBitableApp(name) {
  console.log(`🔄 正在创建多维表格: ${name}...`);
  
  const result = await apiPost('/bitable/v1/apps', {
    name: name
  });
  
  if (result.code === 0) {
    const app = result.data.app;
    console.log(`✅ 创建成功！`);
    console.log(`   App Token: ${app.app_token}`);
    console.log(`   表格名称: ${app.name}`);
    console.log(`   Default Table ID: ${app.default_table_id}`);
    console.log(`   URL: ${app.url}`);
    console.log(`\n💡 下一步操作:`);
    console.log(`   1. 设置配置: node scripts/set_config.js --app-token "${app.app_token}" --table-id "${app.default_table_id}"`);
    console.log(`   2. 初始化字段: node scripts/init_table.js --open-id "[USER_OPEN_ID]"`);
  } else {
    console.log(`❌ 创建失败: ${result.msg}`);
  }
  return result;
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const name = process.argv.find(arg => arg.startsWith('--name='))?.split('=')[1];

if (!name) {
  rl.question('请输入表格名称: ', async (answer) => {
    await createBitableApp(answer.trim());
    rl.close();
  });
} else {
  createBitableApp(name).then(() => process.exit(0));
}
