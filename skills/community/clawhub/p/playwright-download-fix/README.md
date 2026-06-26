# Playwright Download Fix

自动处理 Playwright 下载文件名问题的 Skill。

## 快速使用

### 方式 1: 在现有项目中使用

复制模块到你的项目：

\`\`\`bash
cp ~/.openclaw-autoclaw/skills/playwright-download-fix/download-helper.js .
\`\`\`

然后在你的脚本中：

\`\`\`javascript
const DownloadHelper = require('./download-helper');

// 初始化
const helper = new DownloadHelper(page, {
  downloadDir: '~/downloads',
  debug: true
});
await helper.setup();

// 下载的文件列表
const files = helper.getDownloadedFiles();
\`\`\`

### 方式 2: 独立运行（手动操作）

\`\`\`bash
cd ~/.openclaw-autoclaw/skills/playwright-download-fix
node standalone-script.js
\`\`\`

浏览器会自动打开，你手动操作下载，文件会自动用正确的文件名保存。

## 特性

✅ 自动监听下载事件
✅ 使用正确的原始文件名保存
✅ 支持自定义下载目录
✅ 调试信息输出
✅ 反自动化检测配置
✅ 追踪下载历史

## 文件

- `SKILL.md` - 详细文档
- `download-helper.js` - 核心模块
- `standalone-script.js` - 独立运行脚本
- `README.md` - 本文件

## 许可

MIT
