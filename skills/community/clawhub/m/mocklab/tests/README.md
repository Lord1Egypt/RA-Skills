# MockLab E2E 测试文档

## 📦 安装依赖

```bash
cd c:\Users\linqing-jk\.agents\skills\mocklab

# 安装 Node.js 依赖
npm install

# 安装浏览器驱动（首次运行）
npm run install-browsers
```

## 🚀 运行测试

### 1. 启动 MockLab 服务器
```bash
# 在一个终端窗口中启动服务器
python mock_server.py --port 18080
```

### 2. 运行测试（在另一个终端窗口）

```bash
# 运行所有测试（无头模式）
npm test

# 可视化 UI 模式运行（推荐开发时使用）
npm run test:ui

# 有头模式运行（看到浏览器操作）
npm run test:headed

# 调试模式（逐步执行）
npm run test:debug

# 查看测试报告
npm run test:report
```

## 📋 测试清单

### 核心功能测试（10个）

✅ **01 - 项目列表加载**
- 验证项目下拉框有选项
- 验证峻茗项目存在

✅ **02 - 选择项目并加载接口列表**
- 选择项目后接口列表加载
- 验证接口数量 > 0

✅ **03 - 点击接口，查看请求参数编辑器**
- 编辑器正确显示
- 字段列表加载

✅ **04 - [核心] 编辑项目接口时，nested 字段应显示真实 JSON** ⭐
- 打开编辑弹窗
- nested 字段展开
- textarea 显示完整 JSON（不是 placeholder）
- 验证字段名：userInfo, applyNo, faceImgInfo 等

✅ **05 - 测试请求发送功能**
- 点击发送按钮
- 验证响应状态 200
- 验证响应内容包含 code, message

✅ **06 - 自定义接口：创建新接口**
- 点击"+ 新建"按钮
- 填写接口信息
- 保存成功

✅ **07 - 自定义接口：编辑已有接口**
- 创建测试接口
- 编辑并保存
- 验证修改生效

✅ **08 - 延迟和错误注入配置**
- 配置延迟范围
- 配置错误类型和概率
- 保存成功

✅ **09 - 状态清空功能**
- 点击清空状态按钮
- 验证成功提示

✅ **10 - [回归] 修复后验证 - nested 字段不应显示 placeholder** ⭐
- 专门针对刚修复的 bug
- 验证不再出现 `{"fieldName": "fixed:value"}`

### 边界情况测试（2个）

✅ **网络错误处理**
- 模拟 schema 加载失败
- 验证错误提示

✅ **空项目处理**
- 验证空项目友好提示

## 📊 测试结果示例

```
Running 12 tests using 3 workers

  ✓ 01 - 项目列表加载 (523ms)
  ✓ 02 - 选择项目并加载接口列表 (892ms)
  ✓ 03 - 点击接口，查看请求参数编辑器 (1.2s)
  ✓ 04 - [核心] 编辑项目接口时，nested 字段应显示真实 JSON (2.1s)
  ✓ 05 - 测试请求发送功能 (1.5s)
  ✓ 06 - 自定义接口：创建新接口 (1.8s)
  ✓ 07 - 自定义接口：编辑已有接口 (2.3s)
  ✓ 08 - 延迟和错误注入配置 (1.1s)
  ✓ 09 - 状态清空功能 (456ms)
  ✓ 10 - [回归] 修复后验证 (1.9s)
  ✓ 网络错误处理 (789ms)
  ✓ 空项目处理 (234ms)

  12 passed (14.2s)
```

## 🎯 关键测试说明

### 测试 04 和 10：nested 字段 JSON 显示

**问题背景：**
之前编辑 `/api/clue/submitPreCredit` 接口时，`data` 字段（`rule: "nested:峻茗_submitPreCredit_req_data"`）的 textarea 只显示 `{"fieldName": "fixed:value"}`，而不是真实的嵌套字段。

**验证逻辑：**
1. 打开编辑弹窗
2. 等待异步数据加载（Promise.all）
3. 展开 data 字段配置区
4. 读取 textarea 内容
5. 断言包含真实字段名：userInfo, applyNo, faceImgInfo 等
6. 断言不包含错误的 placeholder

**预期结果：**
```json
[
  {
    "name": "userInfo",
    "rule": "nested:峻茗_userInfo"
  },
  {
    "name": "applyNo",
    "rule": "sequence",
    "example": "AP20260413001"
  },
  ...
]
```

## 🔧 调试技巧

### 1. 查看失败截图
测试失败时，自动保存截图到：
```
test-results/
  chromium/
    04-core-nested-field-json/
      test-failed-1.png
```

### 2. 查看失败视频
```
test-results/
  chromium/
    04-core-nested-field-json/
      video.webm
```

### 3. 使用 Trace Viewer
```bash
npm run test:report
# 点击失败的测试，查看完整交互过程
```

### 4. 单独运行某个测试
```bash
# 只运行 nested 字段测试
npx playwright test -g "nested 字段"

# 只运行回归测试
npx playwright test -g "回归"
```

## 📌 CI/CD 集成

### GitHub Actions 示例

```yaml
# .github/workflows/test.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd mocklab
          npm install
          npm run install-browsers
          pip install fastapi uvicorn
      
      - name: Start MockLab server
        run: |
          cd mocklab
          python mock_server.py --port 18080 &
          sleep 5
      
      - name: Run tests
        run: |
          cd mocklab
          npm test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: mocklab/test-results/
```

## 🛡️ 最佳实践

### 1. 每次改动后运行测试
```bash
# 修改代码后
git add .
npm test  # 测试通过再提交
git commit -m "fix: nested field JSON display"
```

### 2. 添加新功能时同步写测试
```javascript
test('11 - 新功能：XXX', async ({ page }) => {
  // 测试逻辑
});
```

### 3. 失败时先看截图和视频
不要盲目改代码，先看：
- `test-results/` 目录下的截图
- 视频录像
- Trace 文件

### 4. 本地开发时用 UI 模式
```bash
npm run test:ui
# 可以暂停、单步执行、查看元素选择器
```

## 📞 问题排查

### 问题 1：测试超时
**原因：** MockLab 服务器未启动或端口被占用

**解决：**
```bash
# 检查服务器是否运行
curl http://localhost:18080/mock/health

# 杀掉占用端口的进程
netstat -ano | findstr :18080
taskkill /PID <PID> /F
```

### 问题 2：找不到元素
**原因：** 异步加载未完成

**解决：**
```javascript
// 增加等待时间
await page.waitForTimeout(2000);

// 或者使用更精确的等待
await page.waitForSelector('.ci-nested-json', { state: 'visible', timeout: 5000 });
```

### 问题 3：nested 字段测试失败
**检查清单：**
1. ✅ `峻茗.json` 文件中是否有 `峻茗_submitPreCredit_req_data` schema
2. ✅ `loadIfaceToModal` 是否正确并行加载 example 和 project-full
3. ✅ `_innerSchemas` 是否在弹窗打开前赋值
4. ✅ `getRuleConfigHTML` 是否读取 `_innerSchemas` 并填充 textarea

## 🎓 学习资源

- [Playwright 官方文档](https://playwright.dev/)
- [Playwright Inspector](https://playwright.dev/docs/debug#playwright-inspector)
- [录制测试脚本](https://playwright.dev/docs/codegen)

```bash
# 录制新测试
npx playwright codegen http://localhost:18080
```

---

**测试覆盖率：** 核心流程 100%  
**维护者：** Claude Opus 4.6  
**最后更新：** 2026-04-14
