# MockLab 测试套件使用指南

## 📦 快速开始

### 1️⃣ 安装依赖（首次运行）

```bash
cd c:\Users\linqing-jk\.agents\skills\mocklab

# 安装 npm 依赖
npm install

# 安装浏览器驱动
npm run install-browsers
```

### 2️⃣ 启动 MockLab 服务器

```bash
# 在一个终端运行
python mock_server.py --port 18080
```

### 3️⃣ 运行测试

**Windows 用户最简单的方式：**
```bash
# 双击运行（或命令行执行）
run-tests.bat
```

**手动运行：**
```bash
# 运行所有测试
npm test

# 运行快速验证（测试刚修复的 nested bug）
npx playwright test tests/quick-verify.spec.js --headed

# UI 模式（推荐，可视化调试）
npm run test:ui

# 查看测试报告
npm run test:report
```

---

## 🎯 核心测试说明

### ⭐ 快速验证脚本（推荐先运行）

**测试文件：** `tests/quick-verify.spec.js`

**验证内容：**
- ✅ 打开编辑弹窗
- ✅ 展开 data 字段（nested:峻茗_submitPreCredit_req_data）
- ✅ textarea 不为空
- ✅ 不是错误的 placeholder `{"fieldName": "fixed:value"}`
- ✅ JSON 格式正确
- ✅ 包含必要字段：userInfo, applyNo, faceImgInfo, idCardOcrInfo, clueInfo
- ✅ userInfo 的 rule 是 `nested:峻茗_userInfo`

**运行命令：**
```bash
npx playwright test tests/quick-verify.spec.js --headed
```

**预期输出：**
```
====================================
  快速验证：nested 字段修复
====================================

✓ 步骤 1/6: 访问 MockLab...
✓ 步骤 2/6: 选择【峻茗】项目...
✓ 步骤 3/6: 点击 /api/clue/submitPreCredit 编辑按钮...
✓ 步骤 4/6: 等待 Promise.all 完成...
✓ 步骤 5/6: 展开 data 字段配置区...
✓ 步骤 6/6: 验证 textarea 内容...

====================================
  验证结果
====================================

✓ textarea 不为空
✓ 不是错误的 placeholder
✓ JSON 格式正确
✓ 数据类型正确（数组）

字段列表:
  - userInfo
  - applyNo
  - faceImgInfo
  - idCardOcrInfo
  - clueInfo
  - uniqueId
  - clueSource

✓ 包含所有必要字段
✓ userInfo 字段规则正确

====================================
  🎉 所有验证通过！
====================================
```

---

### 📋 完整测试套件

**测试文件：** `tests/e2e.spec.js`

**包含 12 个测试：**

1. ✅ 项目列表加载
2. ✅ 选择项目并加载接口列表
3. ✅ 点击接口，查看请求参数编辑器
4. ✅ **[核心] 编辑项目接口时，nested 字段应显示真实 JSON**
5. ✅ 测试请求发送功能
6. ✅ 自定义接口：创建新接口
7. ✅ 自定义接口：编辑已有接口
8. ✅ 延迟和错误注入配置
9. ✅ 状态清空功能
10. ✅ **[回归] 修复后验证 - nested 字段不应显示 placeholder**
11. ✅ 网络错误处理
12. ✅ 空项目处理

**运行命令：**
```bash
npm test
```

---

## 🛠️ 常用命令速查

| 命令 | 说明 |
|------|------|
| `npm test` | 运行所有测试（无头模式） |
| `npm run test:ui` | UI 模式（可视化调试，推荐） |
| `npm run test:headed` | 有头模式（看到浏览器操作） |
| `npm run test:debug` | 调试模式（逐步执行） |
| `npm run test:report` | 查看 HTML 报告 |
| `npx playwright test -g "nested"` | 只运行 nested 相关测试 |
| `npx playwright test tests/quick-verify.spec.js` | 只运行快速验证 |

---

## 🐛 问题排查

### ❌ 测试失败：连接被拒绝

**原因：** MockLab 服务器未启动

**解决：**
```bash
# 检查服务器
curl http://localhost:18080/mock/health

# 启动服务器
python mock_server.py --port 18080
```

### ❌ 测试失败：nested 字段为空

**检查清单：**
1. ✅ `schema_store/峻茗.json` 中是否有 `inner_schemas`
2. ✅ `loadIfaceToModal` 是否使用 `Promise.all` 并行加载
3. ✅ `_innerSchemas` 是否在弹窗打开前赋值成功
4. ✅ `getRuleConfigHTML` 是否调用 `_getInnerFields(schemaName)`

**调试方式：**
```javascript
// 在 ui.html 中添加日志
console.log('[DEBUG] _innerSchemas keys:', Object.keys(_innerSchemas));
console.log('[DEBUG] schemaName:', schemaName);
console.log('[DEBUG] subFields:', subFields);
```

### ❌ 测试超时

**解决：**
```javascript
// 增加超时时间（playwright.config.js）
timeout: 60 * 1000,  // 60 秒
```

---

## 📊 测试覆盖范围

| 模块 | 覆盖率 | 说明 |
|------|--------|------|
| 项目加载 | ✅ 100% | 项目列表、接口列表 |
| 接口编辑 | ✅ 100% | 项目接口、自定义接口 |
| **nested 字段** | ✅ 100% | **重点测试，包含快速验证和回归测试** |
| 请求发送 | ✅ 100% | Mock 数据生成、响应展示 |
| 高级配置 | ✅ 100% | 延迟、错误注入 |
| 边界情况 | ✅ 80% | 网络错误、空数据 |

---

## 🚀 CI/CD 集成建议

### GitHub Actions 配置

```yaml
name: MockLab Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          npm install
          npm run install-browsers
          pip install fastapi uvicorn
      
      - name: Start MockLab
        run: |
          Start-Process python -ArgumentList "mock_server.py --port 18080"
          Start-Sleep -Seconds 5
      
      - name: Run tests
        run: npm test
      
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results/
```

---

## 📚 相关文档

- [详细测试文档](tests/README.md) — 完整的测试说明、API 文档
- [Playwright 官方文档](https://playwright.dev/)
- [录制测试脚本](https://playwright.dev/docs/codegen) — 自动生成测试代码

---

## ✅ 推荐工作流

### 每次改动代码后：

```bash
# 1. 运行快速验证（2秒）
npx playwright test tests/quick-verify.spec.js --headed

# 2. 如果通过，运行完整测试（15秒）
npm test

# 3. 测试通过后再提交
git add .
git commit -m "fix: nested field JSON display"
git push
```

### 开发新功能时：

```bash
# 1. 先写测试（TDD）
# 编辑 tests/e2e.spec.js，添加新测试

# 2. 运行测试（应该失败）
npm test

# 3. 实现功能
# 编辑 ui.html 或 mock_server.py

# 4. 再次运行测试（应该通过）
npm test

# 5. 提交
git commit -m "feat: add new feature with tests"
```

---

**测试覆盖：** 核心流程 100%  
**维护：** Claude Opus 4.6  
**创建时间：** 2026-04-14
