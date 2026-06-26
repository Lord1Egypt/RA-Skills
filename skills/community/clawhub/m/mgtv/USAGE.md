# MGTV Skill 使用指南

## 快速开始

### 1. 安装 Skill

**方法 A：使用 ClawHub（推荐）**

```bash
cd /Users/bilong/opencode/skills/mgtv
clawhub publish . --slug mgtv --name "MGTV" --version 1.0.0
```

然后在 OpenClaw 中安装：
```
clawhub install mgtv
```

**方法 B：手动安装**

skill 已经位于 `/Users/bilong/opencode/skills/mgtv`

确保你的 OpenClaw 配置中包含这个 skills 目录。

### 2. 安装依赖

```bash
cd /Users/bilong/opencode/skills/mgtv
npm install
```

### 3. 测试

```bash
node scripts/test.js
```

## 在 OpenClaw 中使用

### 自然语言触发

安装后，在 OpenClaw 中直接使用自然语言：

```
用户：我想看《乘风破浪的姐姐》
助手：正在为您搜索芒果 TV 的《乘风破浪的姐姐》...
     已找到相关视频，正在打开浏览器...
     ✓ 已在浏览器中打开播放页面

用户：播放《歌手 2024》最新一期
助手：搜索《歌手 2024》...
     正在打开芒果 TV 搜索结果页面...

用户：帮我找一下何炅的综艺节目
助手：搜索何炅的综艺节目...
     已打开芒果 TV，请查看搜索结果

用户：打开这个芒果 TV 视频：https://www.mgtv.com/b/xxx/xxx.html
助手：正在打开视频...
     ✓ 已在浏览器中播放
```

### 触发条件

MGTV skill 会在以下情况自动激活：

1. **包含芒果 TV 相关关键词**：
   - "芒果 TV"
   - "mgtv"
   - "湖南卫视"

2. **请求观看视频**：
   - "我想看..."
   - "播放..."
   - "帮我找..."
   - "打开...视频"

3. **提供芒果 TV URL**：
   - 包含 `mgtv.com` 的链接

### 技能行为

1. **搜索模式**：当用户提供节目名称时
   - 构建搜索 URL：`https://www.mgtv.com/?q={query}`
   - 在浏览器中打开搜索页面
   - 用户可以手动选择想看的视频

2. **直接播放模式**：当用户提供完整 URL 时
   - 直接在浏览器中打开视频播放页面
   - 开始播放视频

## 命令行使用

### 基本用法

```bash
# 搜索视频
node scripts/search-mgtv.js --query "节目名称"

# 直接打开 URL
node scripts/search-mgtv.js --direct-url "https://www.mgtv.com/b/xxx/xxx.html"
```

### 示例

```bash
# 搜索综艺节目
node scripts/search-mgtv.js --query "大侦探"

# 搜索电视剧
node scripts/search-mgtv.js --query "庆余年"

# 搜索电影
node scripts/search-mgtv.js --query "流浪地球"

# 打开特定视频
node scripts/search-mgtv.js --direct-url "https://www.mgtv.com/b/328606/5533377.html"

# 打开芒果 TV 首页
node scripts/search-mgtv.js --direct-url "https://www.mgtv.com"
```

### 运行测试

```bash
# 运行完整测试套件
node scripts/test.js

# 单个测试
node scripts/search-mgtv.js --query "歌手"
```

## 配置选项

### 环境变量（可选）

可以在 `.env` 文件中配置：

```bash
# 浏览器命令（默认根据操作系统自动选择）
BROWSER_COMMAND=open  # macOS
BROWSER_COMMAND=start # Windows
BROWSER_COMMAND=xdg-open # Linux
```

## 故障排除

### 问题 1：浏览器无法打开

**症状**：显示"打开浏览器失败"

**解决方案**：
- macOS: 确认系统有 `open` 命令（通常都有）
- Windows: 使用命令提示符或 PowerShell
- Linux: 安装 `xdg-open`

```bash
# Linux 安装 xdg-open
sudo apt-get install xdg-utils  # Debian/Ubuntu
sudo yum install xdg-utils      # CentOS/RHEL
```

### 问题 2：搜索结果为空

**症状**：搜索页面没有相关内容

**解决方案**：
- 尝试更精确的关键词
- 使用节目的完整名称
- 检查网络连接
- 确认芒果 TV 网站可访问

### 问题 3：视频无法播放

**症状**：页面打开但视频不播放

**可能原因**：
- 需要芒果 TV 会员（VIP 内容）
- 地区限制
- 浏览器插件冲突

**解决方案**：
- 登录芒果 TV 账号
- 清除浏览器缓存
- 尝试无痕模式
- 禁用广告拦截插件

## 开发自定义功能

### 添加新的搜索参数

编辑 `scripts/search-mgtv.js`：

```javascript
// 添加自定义搜索逻辑
function customSearch(query) {
  // 你的实现
}
```

### 集成 Playwright（高级）

如果需要自动化操作（如自动点击第一个搜索结果）：

```bash
npm install playwright
```

然后在脚本中使用 Playwright：

```javascript
const { chromium } = require('playwright');

async function autoClickFirstResult(query) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`https://www.mgtv.com/?q=${encodeURIComponent(query)}`);
  // 点击第一个搜索结果
  await page.click('.result-item:first-child');
}
```

## 最佳实践

1. **明确节目名称**：使用完整的节目名称，避免简称
2. **添加年份**：对于有多个季的节目，加上年份更准确
3. **直接 URL**：如果知道具体视频 URL，直接使用更高效
4. **网络稳定**：确保网络连接稳定，避免加载失败

## 扩展建议

未来可以添加的功能：

- [ ] 自动点击第一个搜索结果
- [ ] 支持播放列表管理
- [ ] 获取视频播放地址（m3u8）
- [ ] 支持视频下载（需 VIP）
- [ ] 播放历史记录
- [ ] 收藏夹同步
- [ ] 弹幕功能
- [ ] 倍速播放控制

## 技术支持

如有问题或建议：
1. 查看本文档
2. 运行测试脚本诊断问题
3. 提交 Issue 到 ClawHub

---

**注意**：本 Skill 仅供学习交流使用，请支持正版视频内容。部分内容可能需要芒果 TV 会员账号。
