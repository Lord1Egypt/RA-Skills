# Pinterest Browser Publisher

**版本：** 1.0.1  
**作者：** jp-girl-agent  
**描述：** 基于浏览器自动化的 Pinterest 发布工具，无需 API 密钥

---

## 📦 快速安装

```bash
npx clawhub@latest install pinterest-browser-publisher
```

---

## 🚀 功能特点

- ✅ **无需 API** - 使用浏览器自动化，无需申请 Pinterest API
- ✅ **Cookie 持久化** - 登录一次，长期复用
- ✅ **自动发布** - 上传图片、填写标题描述、选择 Board
- ✅ **批量发布** - 支持多张图片连续发布
- ✅ **日本区支持** - 专为 jp.pinterest.com 优化
- ✅ **反检测** - 模拟人类操作，降低封号风险

---

## 📖 使用指南

### 1. 首次登录保存 Cookie

```bash
cd skills/pinterest-browser-publisher
node scripts/force-login.js
```

浏览器打开后：
1. 登录你的 Pinterest 账号
2. 等待首页加载完成
3. 浏览器自动关闭，Cookie 已保存

### 2. 发布 Pin 图

```bash
# 自动发布配置的 Pin
node scripts/publish-fix.js

# 批量发布所有 Pin
node scripts/auto-publish-all.js

# 单张自定义发布
node scripts/publish-jp-direct.js --images "./pin.png" --title "标题" --description "描述"
```

---

## 📁 脚本说明

| 脚本 | 用途 | 参数 |
|------|------|------|
| `force-login.js` | 登录并保存 Cookie | 无 |
| `publish-fix.js` | 自动发布配置的 Pin | 内置配置 |
| `auto-publish-all.js` | 批量发布所有 | 内置配置 |
| `publish-jp-direct.js` | 直接发布单张 | `--images`, `--title`, `--description` |

---

## ⚙️ 自定义发布

编辑 `scripts/publish-fix.js` 中的 pins 数组：

```javascript
const pins = [
  {
    image: '/path/to/image.png',
    title: 'ピンタイトル',
    description: '説明テキスト #ハッシュタグ'
  },
  // 添加更多...
];
```

---

## 🔧 配置

Cookie 存储位置：`~/.config/pinterest/cookies.json`

可编辑配置：`~/.config/pinterest/config.json`

```json
{
  "headless": false,
  "slowMo": 100,
  "postDelay": 30000,
  "randomizeTiming": true
}
```

---

## ⚠️ 注意事项

1. **Cookie 有效期** - 约 30 天，过期需重新登录
2. **发布频率** - 建议每小时不超过 10 张，每天不超过 50 张
3. **图片要求** - PNG/JPG，最小宽度 1000px，推荐 2:3 或 4:5 比例
4. **网络要求** - 需要能访问 jp.pinterest.com
5. **浏览器依赖** - 需要安装 Playwright Chromium

---

## 🛠️ 依赖安装

```bash
# 安装 Playwright
npm install -g playwright
playwright install chromium

# 进入技能目录
cd skills/pinterest-browser-publisher
npm install
```

---

## 📊 发布示例

### 家居类 Pin

```javascript
{
  image: './pins/home01.png',
  title: '✨轻奢×中古ミックス✨大人の部屋作りアイデア',
  description: '高級感とヴィンテージの絶妙なバランス🏠 #轻奢风 #中古风 #家居灵感'
}
```

### 穿搭类 Pin

```javascript
{
  image: './pins/outfit01.png',
  title: '👗优衣库神搭配👗5 着で 7 デイズコーデ',
  description: '着回し力抜群のアイテムで、一週間コーデが完成！#优衣库 #穿搭 #日系'
}
```

### 植物类 Pin

```javascript
{
  image: './pins/plant01.png',
  title: '🌿室内绿植推荐🌿初心者でも育てやすい 10 選',
  description: '日陰でも育つ、手間いらずの観葉植物まとめました🪴 #植物 #绿植 #室内'
}
```

---

## 🎯 最佳实践

### 标题优化
- ✅ 使用 emoji 吸引注意（✨🌿💎）
- ✅ 包含核心关键词
- ✅ 控制在 50 字符以内

### 描述优化
- ✅ 前 50 字包含核心信息
- ✅ 使用 bullet points 列出要点
- ✅ 添加 5-10 个相关标签

### 发布时间
- 🇯🇵 日本用户活跃时间：
  - 早上 7:00-8:00（通勤）
  - 中午 12:00-13:00（午休）
  - 晚上 20:00-22:00（睡前）

### Board 管理
- 创建 5-10 个主题 Board
- 每个 Board 有清晰的命名
- 定期整理和更新

---

## 🐛 常见问题

### Q: Cookie 失效怎么办？
A: 重新运行 `node scripts/force-login.js` 登录

### Q: 上传失败怎么办？
A: 检查图片路径是否正确，格式是否为 PNG/JPG

### Q: 标题描述没填上？
A: Pinterest UI 可能更新，检查选择器是否需要调整

### Q: 发布后看不到？
A: 可能需要几分钟审核，稍后刷新主页查看

---

## 📝 更新日志

### v1.0.1 (2026-03-26)
- ✅ 修复标题和描述填写选择器
- ✅ 优化发布流程
- ✅ 添加批量发布支持

### v1.0.0 (2026-03-26)
- ✅ 初始版本
- ✅ 支持 jp.pinterest.com
- ✅ Cookie 持久化
- ✅ 自动发布流程
- ✅ 批量发布支持

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- Playwright 团队
- Pinterest 平台
- OpenClaw 社区

---

**发布地址：** https://clawhub.ai/skills/pinterest-browser-publisher

**问题反馈：** https://github.com/openclaw/openclaw/issues
