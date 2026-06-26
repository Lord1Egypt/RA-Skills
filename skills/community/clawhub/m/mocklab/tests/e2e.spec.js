/**
 * MockLab E2E 测试
 * 运行: npm test 或 npx playwright test
 */
const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:18080';
const TEST_PROJECT = '峻茗';

test.describe('MockLab 核心功能测试', () => {

  test.beforeEach(async ({ page }) => {
    // 每个测试前访问首页
    await page.goto(BASE_URL);
    // 等待页面初始化完成
    await page.waitForSelector('#proj-select option');
  });

  test('01 - 项目列表加载', async ({ page }) => {
    // 检查项目下拉框是否有选项
    const options = await page.locator('#proj-select option').count();
    expect(options).toBeGreaterThan(1); // 至少有 "-- 选择项目 --" + 1 个项目

    // 检查是否有峻茗项目
    const hasProject = await page.locator(`#proj-select option[value="${TEST_PROJECT}"]`).count();
    expect(hasProject).toBe(1);

    console.log('✓ 项目列表加载成功');
  });

  test('02 - 选择项目并加载接口列表', async ({ page }) => {
    // 选择项目
    await page.selectOption('#proj-select', TEST_PROJECT);

    // 等待接口列表加载
    await page.waitForSelector('.iface-item', { timeout: 5000 });

    // 检查接口数量
    const ifaceCount = await page.locator('.iface-item').count();
    expect(ifaceCount).toBeGreaterThan(0);

    // 检查是否有特定接口
    const hasSubmitPreCredit = await page.locator('.iface-item[data-path="/api/clue/submitPreCredit"]').count();
    expect(hasSubmitPreCredit).toBe(1);

    console.log(`✓ 接口列表加载成功，共 ${ifaceCount} 个接口`);
  });

  test('03 - 点击接口，查看请求参数编辑器', async ({ page }) => {
    // 选择项目
    await page.selectOption('#proj-select', TEST_PROJECT);
    await page.waitForSelector('.iface-item');

    // 点击接口
    await page.click('.iface-item[data-path="/api/clue/submitPreCredit"]');

    // 等待编辑器加载
    await page.waitForSelector('#editor-hdr', { state: 'visible', timeout: 3000 });

    // 检查标题
    const pathText = await page.locator('#iface-path').textContent();
    expect(pathText).toBe('/api/clue/submitPreCredit');

    // 检查字段编辑器
    const fields = await page.locator('.fg').count();
    expect(fields).toBeGreaterThan(0);

    console.log('✓ 接口编辑器加载成功');
  });

  test('04 - [核心] 编辑项目接口时，nested 字段应显示真实 JSON', async ({ page }) => {
    // 选择项目
    await page.selectOption('#proj-select', TEST_PROJECT);
    await page.waitForSelector('.iface-item');

    // 点击编辑按钮（不是接口本身，而是编辑图标）
    await page.click('.iface-item[data-path="/api/clue/submitPreCredit"] .ib-edit');

    // 等待弹窗打开
    await page.waitForSelector('#ci-modal.show', { timeout: 5000 });

    // 等待 Promise.all 完成（inner_schemas 异步加载）
    await page.waitForTimeout(1000);

    // 检查弹窗标题
    const modalTitle = await page.locator('#ci-modal-title').textContent();
    expect(modalTitle).toBe('编辑接口');

    // 找到 data 字段对应的行（rule 是 nested:峻茗_submitPreCredit_req_data）
    const dataFieldRow = await page.locator('.ci-field-row').filter({ has: page.locator('.ci-rname[value="data"]') });
    expect(await dataFieldRow.count()).toBe(1);

    // 点击 ⚙ 按钮展开配置区
    const toggleBtn = dataFieldRow.locator('.ci-toggle');
    await toggleBtn.click();

    // 等待 JSON textarea 显示
    await page.waitForSelector('.ci-nested-json[data-schema="峻茗_submitPreCredit_req_data"]', { state: 'visible', timeout: 2000 });

    // 读取 textarea 内容
    const textareaContent = await page.locator('.ci-nested-json[data-schema="峻茗_submitPreCredit_req_data"]').inputValue();

    // 验证内容
    expect(textareaContent).toContain('"userInfo"');
    expect(textareaContent).toContain('"applyNo"');
    expect(textareaContent).toContain('"faceImgInfo"');
    expect(textareaContent).toContain('"idCardOcrInfo"');
    expect(textareaContent).toContain('"clueInfo"');
    expect(textareaContent).toContain('"nested:峻茗_userInfo"');

    // 验证不是错误的 placeholder
    expect(textareaContent).not.toContain('{"fieldName": "fixed:value"}');

    // 解析 JSON 确保格式正确
    const parsedJSON = JSON.parse(textareaContent);
    expect(Array.isArray(parsedJSON)).toBe(true);
    expect(parsedJSON.length).toBeGreaterThan(5);

    console.log('✓ nested 字段 JSON 内容正确');
    console.log(`  字段数量: ${parsedJSON.length}`);
  });

  test('05 - 测试请求发送功能', async ({ page }) => {
    // 选择项目
    await page.selectOption('#proj-select', TEST_PROJECT);
    await page.waitForSelector('.iface-item');

    // 点击接口
    await page.click('.iface-item[data-path="/api/clue/submitPreCredit"]');
    await page.waitForSelector('#send-btn:not([disabled])');

    // 点击发送请求
    await page.click('#send-btn');

    // 等待响应
    await page.waitForSelector('#status-badge.s-ok, #status-badge.s-err', { timeout: 5000 });

    // 检查响应状态
    const statusBadge = await page.locator('#status-badge').textContent();
    expect(statusBadge).toMatch(/200|201/);

    // 检查响应内容
    const respBody = await page.locator('#resp-body pre').textContent();
    expect(respBody).toContain('"code"');
    expect(respBody).toContain('"message"');

    console.log(`✓ 请求发送成功: ${statusBadge}`);
  });

  test('06 - 自定义接口：创建新接口', async ({ page }) => {
    // 点击 + 新建按钮
    await page.click('button:has-text("+ 新建")');

    // 等待弹窗打开
    await page.waitForSelector('#ci-modal.show');

    // 填写接口信息
    await page.fill('#ci-path', '/test/auto-created');
    await page.fill('#ci-name', 'E2E 测试接口');

    // 添加请求字段
    const reqFieldName = await page.locator('#ci-req-fields .ci-rname').first();
    await reqFieldName.fill('test_id');

    const reqFieldRule = await page.locator('#ci-req-fields .ci-rrule').first();
    await reqFieldRule.selectOption('sequence:');

    // 展开配置并填写参数
    await page.click('#ci-req-fields .ci-toggle');
    await page.fill('#ci-req-fields .ci-param', 'test_seq');

    // 添加响应字段
    const respFieldName = await page.locator('#ci-resp-fields .ci-rname').first();
    await respFieldName.fill('status');

    const respFieldRule = await page.locator('#ci-resp-fields .ci-rrule').first();
    await respFieldRule.selectOption('fixed:');

    await page.click('#ci-resp-fields .ci-toggle');
    await page.fill('#ci-resp-fields .ci-param', 'success');

    // 保存
    await page.click('button:has-text("保存")');

    // 等待 toast 提示
    await page.waitForSelector('.toast-success', { timeout: 3000 });

    // 检查接口列表中是否出现
    await page.waitForSelector('.iface-item[data-path="/test/auto-created"]', { timeout: 2000 });

    console.log('✓ 自定义接口创建成功');
  });

  test('07 - 自定义接口：编辑已有接口', async ({ page }) => {
    // 先创建一个接口（复用上个测试的逻辑）
    await page.click('button:has-text("+ 新建")');
    await page.waitForSelector('#ci-modal.show');
    await page.fill('#ci-path', '/test/edit-test');
    await page.fill('#ci-name', '待编辑接口');
    await page.locator('#ci-resp-fields .ci-rname').first().fill('code');
    await page.locator('#ci-resp-fields .ci-rrule').first().selectOption('fixed:');
    await page.click('#ci-resp-fields .ci-toggle');
    await page.fill('#ci-resp-fields .ci-param', '0');
    await page.click('button:has-text("保存")');
    await page.waitForSelector('.toast-success');
    await page.waitForTimeout(500);

    // 点击编辑按钮
    await page.click('.iface-item[data-path="/test/edit-test"] .ib-edit');
    await page.waitForSelector('#ci-modal.show');

    // 修改名称
    await page.fill('#ci-name', '已编辑接口');

    // 修改响应字段
    await page.fill('#ci-resp-fields .ci-param', '1');

    // 保存
    await page.click('button:has-text("保存")');
    await page.waitForSelector('.toast-success');

    // 验证修改生效（重新打开编辑弹窗）
    await page.waitForTimeout(500);
    await page.click('.iface-item[data-path="/test/edit-test"] .ib-edit');
    await page.waitForSelector('#ci-modal.show');

    const newName = await page.locator('#ci-name').inputValue();
    expect(newName).toBe('已编辑接口');

    console.log('✓ 自定义接口编辑成功');
  });

  test('08 - 延迟和错误注入配置', async ({ page }) => {
    // 选择项目
    await page.selectOption('#proj-select', TEST_PROJECT);
    await page.waitForSelector('.iface-item');

    // 点击接口
    await page.click('.iface-item[data-path="/api/clue/submitPreCredit"]');
    await page.waitForSelector('#settings-bar.visible');

    // 配置延迟
    await page.check('#in-delay-on');
    await page.fill('#in-delay-min', '100');
    await page.fill('#in-delay-max', '300');

    // 配置错误注入
    await page.check('#in-err-on');
    await page.selectOption('#in-err-type', '500');
    await page.fill('#in-err-prob', '1.0');
    await page.fill('#in-err-code', 'TEST_ERROR');
    await page.fill('#in-err-msg', '测试错误');

    // 保存配置
    await page.click('#settings-bar button:has-text("保存")');

    // 等待保存成功提示
    await page.waitForSelector('#updated-msg.show', { timeout: 3000 });

    console.log('✓ 延迟和错误注入配置成功');
  });

  test('09 - 状态清空功能', async ({ page }) => {
    // 点击清空状态按钮
    await page.click('button:has-text("清空状态")');

    // 等待 toast 提示
    await page.waitForSelector('.toast-success:has-text("状态已清空")', { timeout: 3000 });

    console.log('✓ 状态清空成功');
  });

  test('10 - [回归] 修复后验证 - nested 字段不应显示 placeholder', async ({ page }) => {
    // 这是专门针对你刚修复的 bug 的回归测试
    await page.selectOption('#proj-select', TEST_PROJECT);
    await page.waitForSelector('.iface-item');

    // 点击编辑
    await page.click('.iface-item[data-path="/api/clue/submitPreCredit"] .ib-edit');
    await page.waitForSelector('#ci-modal.show');
    await page.waitForTimeout(1000); // 等待异步加载

    // 展开 data 字段配置
    const dataFieldRow = await page.locator('.ci-field-row').filter({ has: page.locator('.ci-rname[value="data"]') });
    await dataFieldRow.locator('.ci-toggle').click();

    // 读取 textarea
    const textareaContent = await page.locator('.ci-nested-json[data-schema="峻茗_submitPreCredit_req_data"]').inputValue();

    // 【核心验证】不应该是错误的 placeholder
    expect(textareaContent).not.toBe('{"fieldName": "fixed:value"}');
    expect(textareaContent).not.toBe('');

    // 应该包含真实字段
    const json = JSON.parse(textareaContent);
    const fieldNames = json.map(f => f.name);
    expect(fieldNames).toContain('userInfo');
    expect(fieldNames).toContain('applyNo');

    console.log('✓ [回归测试通过] nested 字段显示正确的 JSON');
  });
});

test.describe('边界情况测试', () => {

  test('网络错误处理 - schema 加载失败', async ({ page }) => {
    // 拦截 project-full 请求，模拟失败
    await page.route('**/mock/project-full/**', route => route.abort());

    await page.goto(BASE_URL);
    await page.selectOption('#proj-select', TEST_PROJECT);
    await page.waitForSelector('.iface-item');

    // 尝试打开编辑弹窗
    await page.click('.iface-item[data-path="/api/clue/submitPreCredit"] .ib-edit');

    // 应该显示错误提示
    await page.waitForSelector('.toast-error', { timeout: 3000 });

    console.log('✓ 网络错误处理正确');
  });

  test('空项目处理', async ({ page }) => {
    // 如果项目列表为空，应该友好提示
    await page.goto(BASE_URL);

    const hasProjects = await page.locator('#proj-select option[value!=""]').count();
    if (hasProjects === 0) {
      const placeholder = await page.locator('#iface-list .eh').textContent();
      expect(placeholder).toContain('选择项目');
    }

    console.log('✓ 空项目处理正确');
  });
});
