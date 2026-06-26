---
name: Playwright Download Fix
description: 自动处理 Playwright 下载文件名问题，监听下载事件并用正确的原始文件名保存文件。解决 Playwright 下载的文件名是 UUID 而不是原始文件名的问题。
---

# Playwright Download Fix

Playwright 下载的文件名是 UUID 而不是原始文件名？这个 skill 帮你自动修复这个问题。

## 问题

当使用 Playwright 下载文件时，经常会遇到：
- 浏览器中显示的文件名是 `f63a84ec-abd1-48fa-a748-11ebeca07935`（UUID）
- 但在真实 Chrome 中下载的文件名是正确的，比如 `MVIMG_20250706_131754.jpg`

## 原因

1. Playwright 默认下载到临时目录，使用 UUID 作为临时文件名
2. 网站检测到自动化工具，返回了临时文件名
3. 需要拦截 `download` 事件并使用 `suggestedFilename()` 获取原始文件名

## 解决方案

这个 skill 提供了一个 `DownloadHelper` 模块，自动监听下载事件并用正确的文件名保存文件。

---

## 🚀 快速启动

### 方式 1: 使用 pw-start 命令（推荐）

确保快捷命令已添加到 shell 配置文件：

\`\`\`bash
# 添加到 ~/.zshrc（首次使用）
echo "alias pw-start='cd ~/.openclaw-autoclaw/workspace && node pw-start.js'" >> ~/.zshrc
source ~/.zshrc

# 使用
pw-start                      # 打开默认页面（智联招聘）
pw-start https://example.com  # 打开指定 URL
\`\`\`

**每次运行都会自动加载 DownloadHelper skill 并显示配置信息：**

```
========================================
📋 配置信息
========================================
🌐 User-Agent: 真实 Chrome (macOS)
📂 下载目录: /Users/allen/downloads
🔍 调试模式: 开启
========================================
```

### 方式 2: 直接运行独立脚本

\`\`\`bash
cd ~/.openclaw-autoclaw/skills/playwright-download-fix
node standalone-script.js
\`\`\`

### 方式 3: 在现有项目中集成模块

\`\`\`bash
# 复制模块到项目
cp ~/.openclaw-autoclaw/skills/playwright-download-fix/download-helper.js .
\`\`\`

然后在脚本中使用：

\`\`\`javascript
const { chromium } = require('playwright');
const DownloadHelper = require('./download-helper');

async function myScript() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    acceptDownloads: true,
  });

  const page = await context.newPage();

  // 初始化下载助手
  const helper = new DownloadHelper(page, {
    downloadDir: '~/downloads',
    debug: true
  });
  const downloadDir = await helper.setup();
  console.log(\`📂 下载目录: \${downloadDir}\`);

  // 你的自动化代码...
  await page.goto('https://example.com');
  await page.click('#download-button');

  // 获取下载的文件列表
  console.log('下载的文件:', helper.getDownloadedFiles());

  await browser.close();
}

myScript();
\`\`\`

---

## 📋 启动环境与要求

### 系统要求

- **操作系统**: macOS / Linux / Windows
- **Node.js**: >= 14.x
- **Playwright**: 已安装

### 依赖安装

\`\`\`bash
# 安装 Playwright（如果未安装）
npm install playwright

# 安装浏览器
npx playwright install chromium
\`\`\`

### 启动条件

1. **下载目录权限**: 确保对下载目录（默认 `~/downloads`）有写权限
2. **浏览器缓存**: 首次运行会下载 Chromium（约 170MB）
3. **内存要求**: 至少 4GB 可用内存
4. **网络连接**: 部分网站需要网络访问

### 启动配置

**默认配置**（可在 `pw-start.js` 中修改）：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| User-Agent | Chrome 122.0.0.0 (macOS) | 模拟真实浏览器 |
| Locale | zh-CN | 中文环境 |
| Timezone | Asia/Shanghai | 中国时区 |
| 下载目录 | ~/downloads | 文件保存位置 |
| 调试模式 | 开启 | 显示下载信息 |

### 反自动化检测

为了更接近真实浏览器，默认启用以下配置：

\`\`\`javascript
const context = await browser.newContext({
  userAgent: realChromeUA,
  locale: 'zh-CN',
  timezoneId: 'Asia/Shanghai',
  bypassCSP: true,
  javaScriptEnabled: true,
  acceptDownloads: true,
});
\`\`\`

---

## DownloadHelper API

### 构造函数

\`\`\`javascript
new DownloadHelper(page, options)
\`\`\`

**参数：**
- \`page\` (Page) - Playwright page 实例
- \`options\` (Object) - 配置选项
  - \`downloadDir\` (string) - 下载目录路径，支持 \`~\` 符号，默认 \`~/downloads\`
  - \`debug\` (boolean) - 是否显示调试信息，默认 \`false\`

### 方法

#### setup()

初始化下载监听器，创建下载目录（如果不存在）。

\`\`\`javascript
const downloadDir = await helper.setup();
\`\`\`

**返回：** 下载目录的绝对路径

#### getDownloadedFiles()

获取本次会话中下载的所有文件路径列表。

\`\`\`javascript
const files = helper.getDownloadedFiles();
console.log('下载的文件:', files);
\`\`\`

**返回：** 文件路径数组

#### clearHistory()

清空下载历史记录。

\`\`\`javascript
helper.clearHistory();
\`\`\`

#### dispose()

移除下载监听器。

\`\`\`javascript
helper.dispose();
\`\`\`

---

## 完整示例

### 示例 1: 下载单个文件

\`\`\`javascript
const { chromium } = require('playwright');
const DownloadHelper = require('./download-helper');

async function downloadSingle() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    acceptDownloads: true,
  });

  const page = await context.newPage();

  const helper = new DownloadHelper(page, {
    downloadDir: '~/downloads',
    debug: true
  });
  await helper.setup();

  await page.goto('https://example.com');
  await page.click('#download-button');
  await page.waitForTimeout(3000);

  const files = helper.getDownloadedFiles();
  console.log('下载的文件:', files);

  await browser.close();
}

downloadSingle();
\`\`\`

### 示例 2: 批量下载

\`\`\`javascript
const { chromium } = require('playwright');
const DownloadHelper = require('./download-helper');

async function downloadMultiple(urls) {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();

  const helper = new DownloadHelper(page, {
    downloadDir: '~/downloads',
    debug: true
  });
  await helper.setup();

  for (const url of urls) {
    await page.goto(url);
    await page.click('.download-link');
    await page.waitForTimeout(2000);
  }

  console.log(\`共下载 \${helper.getDownloadedFiles().length} 个文件\`);

  await browser.close();
}

downloadMultiple(['url1', 'url2', 'url3']);
\`\`\`

### 示例 3: 智联招聘下载简历

\`\`\`javascript
const { chromium } = require('playwright');
const DownloadHelper = require('./download-helper');

async function downloadResumes() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    acceptDownloads: true,
  });

  const page = await context.newPage();

  const helper = new DownloadHelper(page, {
    downloadDir: '~/downloads',
    debug: true
  });
  await helper.setup();

  // 导航到搜索页面
  await page.goto('https://rd6.zhaopin.com/app/search');

  // 手动登录...

  // 搜索候选人并下载简历
  // ...

  await browser.close();
}

downloadResumes();
\`\`\`

---

## 工作原理

1. **监听下载事件**：通过 \`page.on('download', ...)\` 监听所有下载
2. **获取原始文件名**：使用 \`download.suggestedFilename()\` 获取服务器返回的真实文件名
3. **保存到指定目录**：用正确的文件名保存到用户指定的目录
4. **追踪下载历史**：记录所有下载的文件路径，方便后续处理

---

## 故障排除

### 问题 1: 下载的文件名仍然是 UUID

**可能原因：**
- 网站检测到了自动化工具
- User-Agent 不够真实
- 缺少必要的请求头

**解决方案：**
1. 使用更真实的 User-Agent
2. 添加更多请求头
3. 考虑使用 \`puppeteer-extra-plugin-stealth\`
4. 连接到真实的 Chrome 实例（CDP）

\`\`\`javascript
// 连接真实 Chrome
const browser = await chromium.connectOverCDP('http://localhost:9222');
\`\`\`

### 问题 2: 文件下载失败

**可能原因：**
- 未设置 \`acceptDownloads: true\`
- 下载目录无写权限
- 网络问题

**解决方案：**
\`\`\`javascript
// 1. 确保设置 acceptDownloads
const context = await browser.newContext({
  acceptDownloads: true,  // 必须设置
});

// 2. 检查目录权限
fs.accessSync(downloadDir, fs.constants.W_OK);

// 3. 查看 debug 输出
const helper = new DownloadHelper(page, { debug: true });
\`\`\`

### 问题 3: 文件保存位置不对

**可能原因：**
- \`downloadDir\` 配置错误
- 相对路径解析问题

**解决方案：**
\`\`\`javascript
// 使用绝对路径
const helper = new DownloadHelper(page, {
  downloadDir: '/Users/yourname/Downloads',  // 绝对路径
});

// 或使用 ~ 符号
const helper = new DownloadHelper(page, {
  downloadDir: '~/downloads',  // 会自动解析为用户主目录
});
\`\`\`

### 问题 4: pw-start 命令未找到

**解决方案：**
\`\`\`bash
# 添加快捷命令
echo "alias pw-start='cd ~/.openclaw-autoclaw/workspace && node pw-start.js'" >> ~/.zshrc

# 重新加载配置
source ~/.zshrc

# 或重启终端
\`\`\`

---

## 配置文件说明

### pw-start.js

主启动脚本，位于 \`~/.openclaw-autoclaw/workspace/pw-start.js\`

**可配置项：**
\`\`\`javascript
const CONFIG = {
  userAgent: '...',           // 自定义 User-Agent
  locale: 'zh-CN',            // 语言
  timezoneId: 'Asia/Shanghai', // 时区
  downloadDir: '~/downloads', // 下载目录
  debug: true,                // 调试模式
  defaultUrl: '...'           // 默认 URL
};
\`\`\`

### standalone-script.js

独立运行脚本，位于 \`~/.openclaw-autoclaw/skills/playwright-download-fix/standalone-script.js\`

**特点：**
- 默认打开智联招聘搜索页
- 完整的下载事件监听

### download-helper.js

核心模块，可复制到任何项目使用。

---

## 使用场景

### 场景 1: 智联招聘下载简历

\`\`\`bash
pw-start
# 浏览器自动打开智联招聘
# 手动登录后下载简历
# 文件自动保存到 ~/downloads
\`\`\`

### 场景 2: 任何需要下载的网站

\`\`\`bash
pw-start https://example.com
# 在浏览器中操作
# 下载的文件会自动用正确的文件名保存
\`\`\`

### 场景 3: 开发测试

\`\`\`bash
pw-start http://localhost:3000
# 测试本地开发环境的下载功能
\`\`\`

### 场景 4: 批量下载任务

在自动化脚本中集成 \`DownloadHelper\`，实现批量下载。

---

## 常见问题

### Q: 如何查看下载的文件？

\`\`\`bash
ls ~/downloads
\`\`\`

### Q: 支持其他浏览器吗？

当前仅支持 Chromium，但可以通过修改 \`pw-start.js\` 使用 Firefox 或 WebKit：

\`\`\`javascript
const { firefox } = require('playwright');
const browser = await firefox.launch();
\`\`\`

---

## 相关文件

- \`download-helper.js\` - 核心下载处理模块
- \`standalone-script.js\` - 独立运行脚本
- \`pw-start.js\` - 快速启动脚本（位于 workspace）
- \`example.js\` - 使用示例
- \`README.md\` - 快速指南

---

## 许可

MIT
