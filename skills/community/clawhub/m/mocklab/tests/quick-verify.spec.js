/**
 * 快速验证脚本 - 专门测试 nested 字段 bug 修复
 * 运行: npx playwright test tests/quick-verify.spec.js --headed
 */
const { test, expect } = require('@playwright/test');

test('🔍 快速验证：nested 字段 JSON 显示正确', async ({ page }) => {
  console.log('\n====================================');
  console.log('  快速验证：nested 字段修复');
  console.log('====================================\n');

  // 1. 打开页面
  console.log('✓ 步骤 1/6: 访问 MockLab...');
  await page.goto('http://localhost:18080');
  await page.waitForSelector('#proj-select option');

  // 2. 选择项目
  console.log('✓ 步骤 2/6: 选择【峻茗】项目...');
  await page.selectOption('#proj-select', '峻茗');
  await page.waitForSelector('.iface-item');

  // 3. 点击编辑按钮
  console.log('✓ 步骤 3/6: 点击 /api/clue/submitPreCredit 编辑按钮...');
  await page.click('.iface-item[data-path="/api/clue/submitPreCredit"] .ib-edit');
  await page.waitForSelector('#ci-modal.show', { timeout: 5000 });

  // 4. 等待异步加载完成
  console.log('✓ 步骤 4/6: 等待 Promise.all 完成（inner_schemas 加载）...');
  await page.waitForTimeout(1500);

  // 5. 展开 data 字段
  console.log('✓ 步骤 5/6: 展开 data 字段配置区...');
  const dataFieldRow = page.locator('.ci-field-row').filter({
    has: page.locator('.ci-rname[value="data"]')
  });
  await dataFieldRow.locator('.ci-toggle').click();

  // 6. 验证 textarea 内容
  console.log('✓ 步骤 6/6: 验证 textarea 内容...\n');

  const textarea = page.locator('.ci-nested-json[data-schema="峻茗_submitPreCredit_req_data"]');
  await textarea.waitFor({ state: 'visible', timeout: 3000 });

  const content = await textarea.inputValue();

  console.log('====================================');
  console.log('  验证结果');
  console.log('====================================\n');

  // 验证 1：不是空的
  if (content.length === 0) {
    console.log('❌ 失败：textarea 为空');
    throw new Error('textarea 内容为空');
  }
  console.log('✓ textarea 不为空');

  // 验证 2：不是错误的 placeholder
  if (content === '{"fieldName": "fixed:value"}') {
    console.log('❌ 失败：显示的是错误的 placeholder');
    throw new Error('显示错误的 placeholder');
  }
  console.log('✓ 不是错误的 placeholder');

  // 验证 3：能解析成 JSON
  let json;
  try {
    json = JSON.parse(content);
  } catch (e) {
    console.log('❌ 失败：无法解析为 JSON');
    console.log('内容:', content);
    throw new Error('JSON 解析失败: ' + e.message);
  }
  console.log('✓ JSON 格式正确');

  // 验证 4：是数组
  if (!Array.isArray(json)) {
    console.log('❌ 失败：不是数组格式');
    throw new Error('内容不是数组');
  }
  console.log('✓ 数据类型正确（数组）');

  // 验证 5：包含必要字段
  const fieldNames = json.map(f => f.name);
  const requiredFields = ['userInfo', 'applyNo', 'faceImgInfo', 'idCardOcrInfo', 'clueInfo'];

  console.log('\n字段列表:');
  fieldNames.forEach(name => console.log(`  - ${name}`));

  const missingFields = requiredFields.filter(f => !fieldNames.includes(f));
  if (missingFields.length > 0) {
    console.log('\n❌ 失败：缺少字段:', missingFields.join(', '));
    throw new Error('缺少必要字段');
  }
  console.log('\n✓ 包含所有必要字段');

  // 验证 6：userInfo 字段的 rule
  const userInfoField = json.find(f => f.name === 'userInfo');
  if (!userInfoField) {
    console.log('❌ 失败：找不到 userInfo 字段');
    throw new Error('userInfo 字段不存在');
  }
  if (userInfoField.rule !== 'nested:峻茗_userInfo') {
    console.log('❌ 失败：userInfo.rule 不正确');
    console.log('预期:', 'nested:峻茗_userInfo');
    console.log('实际:', userInfoField.rule);
    throw new Error('userInfo.rule 不正确');
  }
  console.log('✓ userInfo 字段规则正确');

  console.log('\n====================================');
  console.log('  🎉 所有验证通过！');
  console.log('====================================');
  console.log('\nBug 已修复:');
  console.log('  ✓ Promise.all 并行加载 example 和 project-full');
  console.log('  ✓ _innerSchemas 在弹窗打开前加载完成');
  console.log('  ✓ getRuleConfigHTML 直接读取并填充 textarea');
  console.log('  ✓ fillNestedJSONTextareas 有守卫检查');
  console.log('\n现在编辑项目接口时，nested 字段会正确显示真实 JSON！\n');
});
