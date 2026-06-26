---
name: page_js_operation
description: 通过 CDP 和 Page JS Extension 操作网页元素，节省 95% Token（仅用于 UI 自动化测试）
tools:
  - cdp
---

# Page JS CDP 网页操作 Skill

## ⚠️ 重要说明

**本 Skill 仅用于浏览器自动化测试场景，不适用于处理敏感数据页面。**

### 🎯 使用场景建议

**✅ 推荐用于：**
- 自动化测试环境
- CI/CD 流程中的 UI 测试
- 开发阶段的页面功能验证
- 公开信息的网页操作演示

**❌ 不推荐用于：**
- 日常访问网站
- 处理个人敏感信息的页面
- 生产环境的自动化操作（除非充分测试）

### 依赖项

本 Skill **必须** 配合以下组件使用：

1. **Page JS Extension** - Chrome 扩展（需手动安装）
   - GitHub: https://github.com/TangJing/openclaw_access_web_page_js
   - **请自行下载源码审查后安装**
   - 安装方式：`chrome://extensions/` → 开发者模式 → 加载已解压的扩展程序

2. **CDP 环境** - Chrome DevTools Protocol 访问权限
   - 本地运行：`http://127.0.0.1:9222`
   - 或 Puppeteer/Playwright 等自动化框架

---

## 工作流程

1. **检查扩展** → 确认 `ElementCollector` 已注入（仅首次）
2. **获取元素索引** → 调用 `exportData()` 获取元素 key 列表（非敏感数据）
3. **AI 分析** → 根据 key 识别目标元素（按钮、输入框等）
4. **执行操作** → 通过 CDP 执行 click/input 等操作

---

## ⚠️ 安全限制

### 禁止操作的页面类型

**不要在以下页面使用本 Skill：**

- 🔒 银行/金融网站
- 🔒 登录/注册页面（涉及密码）
- 🔒 支付页面
- 🔒 医疗健康网站
- 🔒 政府/证件相关网站
- 🔒 任何包含个人敏感信息的页面

### 禁止操作的数据类型

**不要读取或修改以下元素：**

- 密码输入框（`type="password"`）
- 信用卡号输入框
- 身份证号输入框
- 其他敏感个人信息字段

### 推荐操作场景

**本 Skill 适用于：**

- ✅ 公开信息的网页操作
- ✅ 自动化测试环境
- ✅ 非敏感的表单填写（如搜索框）
- ✅ 按钮点击操作
- ✅ 下拉选择操作

---

## 操作模板

### 检查扩展是否可用（首次启动）

```javascript
typeof ElementCollector !== 'undefined'
// 返回 true 表示扩展已安装
```

### 获取页面元素索引（非敏感数据）

```javascript
ElementCollector.exportData()
// 返回：{ elements: [...keys], keywords: [...], elementCount: N }
// 注意：仅返回元素的 key 列表，不包含实际 DOM 内容
```

### 点击按钮

```javascript
const results = ElementCollector.searchElementsByKey('{按钮关键字}');
const element = Object.values(results)[0];
if (element) element.click();
```

### 填充普通输入框（非敏感）

```javascript
const inputs = ElementCollector.searchElementsByKey('{搜索框/普通输入框}');
const input = Object.values(inputs)[0];
if (input) {
  input.value = '{值}';
  input.dispatchEvent(new Event('input', { bubbles: true }));
}
```

### 选择下拉选项

```javascript
const selects = ElementCollector.searchElementsByKey('{选择器关键字}');
const select = Object.values(selects)[0];
if (select) {
  select.value = '{选项 value}';
  select.dispatchEvent(new Event('change', { bubbles: true }));
}
```

---

## CDP 命令参考

| 操作 | CDP Runtime.evaluate 表达式 |
|------|---------------------------|
| 检查扩展 | `typeof ElementCollector !== 'undefined'` |
| 获取索引 | `ElementCollector.exportData()` |
| 点击 | `ElementCollector.searchElementsByKey('btn')[0].click()` |
| 填充 | `ElementCollector.searchElementsByKey('input')[0].value = 'text'` |
| 选择 | `ElementCollector.searchElementsByKey('select')[0].value = 'option'` |

---

## 常见关键字

| 操作 | 推荐关键字 |
|------|-----------|
| 搜索 | `'搜索'`, `'search'` |
| 提交 | `'提交'`, `'submit'` |
| 取消 | `'取消'`, `'cancel'` |
| 确认 | `'确定'`, `'confirm'` |
| 删除 | `'删除'`, `'delete'` |
| 编辑 | `'编辑'`, `'edit'` |
| 保存 | `'保存'`, `'save'` |

---

## ⚠️ 隐私与数据流说明

### 数据流向

```
浏览器 DOM → ElementCollector (内存索引) → CDP → 本地 AI Agent
                     ↑
              (仅 key 列表，无敏感内容)
```

### 隐私说明

1. **扩展层面**：
   - ✅ Page JS Extension 完全运行在浏览器本地
   - ✅ 不主动向外部服务器发送数据
   - ✅ 数据存储在内存中，页面关闭即清除

2. **Agent 层面**：
   - ⚠️ **AI Agent 可能将元素数据发送给 LLM 服务**
   - ⚠️ 元素 key 可能包含页面文本内容（如按钮文字、输入框标签）
   - ⚠️ 请确保你的 AI Agent 配置符合隐私要求

3. **用户责任**：
   - ⚠️ 用户需自行审查扩展源码
   - ⚠️ 用户需确保 AI Agent 不会将敏感数据发送到不可信的服务
   - ⚠️ 用户需避免在敏感页面使用本 Skill

### 数据范围

| 数据类型 | 是否收集 | 是否可操作 | 说明 |
|----------|----------|-----------|------|
| 元素 id | ✅ 是 | - | 用于索引 |
| 元素 class | ✅ 是 | - | 用于索引 |
| 元素 title | ✅ 是 | - | 用于索引 |
| 元素 innerText | ✅ 是 | - | 用于索引（最多 100 字符） |
| 普通输入框 | ✅ 是 | ✅ 可读写 | 可搜索、填充、读取 |
| 密码字段 | ❌ **不收集** | ⚠️ **仅可写入** | 不索引，无法通过关键字搜索，但可通过原生 DOM 操作设置值 |
| 隐藏字段 | ❌ **不收集** | ⚠️ **仅可写入** | 不索引，无法通过关键字搜索，但可通过原生 DOM 操作设置值 |
| 文件上传 | ❌ **不收集** | ⚠️ **仅可写入** | 不索引，无法通过关键字搜索，但可通过原生 DOM 操作设置值 |
| Cookie/Storage | ❌ 否 | ❌ 无法访问 | 扩展无此权限 |

**技术实现：**

```javascript
// collectAllElements() 中自动跳过敏感字段
const sensitiveTypes = ['password', 'hidden', 'file'];
if (element.tagName === 'INPUT' && sensitiveTypes.includes(element.type)) {
  return;  // 不收集到索引中，无法通过 searchElementsByKey 搜索
}
```

**注意：** 敏感字段虽不被索引，但仍可通过原生 DOM API 直接操作（如 `document.querySelector('input[type="password"]').value = 'xxx'`）。本插件不主动读取这些字段的值。

---

## 安装步骤

### 步骤 1：安装 Page JS Extension

```bash
# 1. 下载源码
git clone https://github.com/TangJing/openclaw_access_web_page_js.git
cd openclaw_access_web_page_js

# 2. 审查源码（推荐）
# 重点检查：
# - 是否有网络请求代码
# - 是否有数据外传逻辑
# - manifest.json 权限声明

# 3. 安装扩展
# 打开 chrome://extensions/
# 开启"开发者模式"
# 点击"加载已解压的扩展程序"，选择项目目录
```

### 步骤 2：安装 OpenClaw Skill

```bash
# 1. 创建 Skill 目录
mkdir -p ~/.openclaw/workspace/skills/page-js-operation

# 2. 将本 SKILL.md 保存到该目录
# 路径：~/.openclaw/workspace/skills/page-js-operation/SKILL.md

# 3. 刷新 Skills
openclaw agent --message "refresh skills"
```

---

## 使用示例

### 安全场景：搜索操作

```bash
# 在搜索引擎页面
openclaw agent --message "use page_js_operation to fill search box with 'keyword'"
openclaw agent --message "use page_js_operation to click search button"
```

### 安全场景：导航操作

```bash
# 在内容页面
openclaw agent --message "use page_js_operation to click next page button"
openclaw agent --message "use page_js_operation to select category from dropdown"
```

### ❌ 禁止场景：登录操作

```bash
# 不要在登录页面使用
# openclaw agent --message "fill username and password and click login"
# 原因：涉及密码字段
```

---

## 安全最佳实践

1. **使用专用浏览器配置文件**
   - 为自动化测试创建独立的 Chrome 用户配置
   - 不要在测试配置中保存任何真实账号密码

2. **限制访问域名**
   - 在扩展设置中限制可访问的域名
   - 仅允许访问测试环境或公开网站

3. **用户确认机制**
   - 在执行敏感操作前要求用户确认
   - 如：涉及表单提交、删除等操作

4. **定期审查**
   - 定期审查扩展代码是否有更新
   - 检查 Skill 执行日志

---

## 技术说明

### ElementCollector 工作原理

```javascript
// 收集阶段
elementMap = Map<key, Element>  // key → DOM 引用
keywordMap = Map<keyword, Set<keys>>  // 关键字 → key 集合

// key 格式：id|class|title|innerText
// 示例："login-btn|btn primary||登录"
```

### 为什么节省 Token

- **传统方式**：发送完整 HTML（5000-20000 tokens）
- **本插件**：仅发送元素 key 列表（100-500 tokens）
- **节省率**：约 95%+

---

## 免责声明

**使用本 Skill 即表示您同意：**

1. 您已自行审查并信任 Page JS Extension 源码
2. 您了解 AI Agent 可能将元素数据发送给 LLM 服务
3. 您不会在涉及敏感信息的页面使用本 Skill
4. 您自行承担使用本 Skill 的全部风险
5. 本 Skill 作者不对任何数据泄露或损失负责

---

## 相关链接

- [GitHub 仓库](https://github.com/TangJing/openclaw_access_web_page_js)
- [Chrome 扩展开发文档](https://developer.chrome.com/docs/extensions/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
