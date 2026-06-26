# MGTV Skill - 芒果 TV 视频搜索与播放

📺 在 OpenClaw 中搜索芒果 TV 视频资源并自动在浏览器中播放

## 功能特性

- 🔍 **智能搜索**：调用芒果 TV 官方 API 搜索视频资源
- 🎯 **精准匹配**：自动匹配最相关的视频结果
- 🌐 **自动播放**：在系统默认浏览器中打开播放页面
- 📺 **多类型支持**：支持综艺、电视剧、电影、动漫等多种类型
- 🎬 **筛选功能**：支持按类型、年份、热度筛选

## 安装方法

### 方法 1：使用 ClawHub CLI（推荐）

```bash
# 在当前目录下
clawhub install mgtv
```

### 方法 2：手动安装

```bash
# 将 skill 复制到 OpenClaw skills 目录
cp -r mgtv ~/.openclaw/skills/

# 或者复制到当前工作目录的 skills 文件夹
cp -r mgtv ./skills/
```

### 安装依赖

```bash
# 安装必要的 Node.js 包
npm install playwright
```

## 使用方法

### 基本使用

在 OpenClaw 中直接使用自然语言：

```
用户："我想看《乘风破浪的姐姐》"
用户："播放芒果 TV 的《歌手 2024》"
用户："帮我找一下《大侦探》最新一期"
```

### 命令行使用

直接使用脚本：

```bash
# 基本搜索
node scripts/search-mgtv.js --query "乘风破浪的姐姐"

# 指定类型（variety|drama|movie|anime）
node scripts/search-mgtv.js --query "歌手" --type variety

# 指定年份
node scripts/search-mgtv.js --query "大侦探" --year 2024

# 按热度排序
node scripts/search-mgtv.js --query "明星大侦探" --sort hot
```

### 参数说明

| 参数 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `--query` | 搜索关键词（必填） | 任意文本 | - |
| `--type` | 视频类型 | all, variety, drama, movie, anime | all |
| `--year` | 年份筛选 | 年份数字（如 2024） | 不限 |
| `--sort` | 排序方式 | default, hot, newest | default |

## 示例

### 示例 1：搜索综艺节目

```bash
node scripts/search-mgtv.js --query "你好星期六" --type variety --sort hot
```

### 示例 2：搜索特定年份的电视剧

```bash
node scripts/search-mgtv.js --query "繁花" --type drama --year 2024
```

### 示例 3：搜索最新动漫

```bash
node scripts/search-mgtv.js --query "斗罗大陆" --type anime --sort newest
```

## 技术实现

### API 接口

- **搜索 API**: `https://pianku.api.mgtv.com/rider/list/pcweb/v3`
- **视频详情**: `https://pcweb.api.mgtv.com/player/video?video_id={video_id}`
- **播放页面**: `https://www.mgtv.com/b/{clipId}/{partId}.html`

### 脚本结构

```
mgtv/
├── SKILL.md           # Skill 定义文件
├── README.md          # 本文档
└── scripts/
    └── search-mgtv.js # 搜索与播放脚本
```

## 注意事项

1. **网络连接**：需要能够访问芒果 TV 网站
2. **浏览器**：需要系统有默认浏览器
3. **VIP 内容**：部分视频需要芒果 TV 会员账号
4. **地区限制**：某些内容可能有地区限制

## 故障排除

### 问题 1：搜索无结果

**解决方案**：
- 尝试更精确的节目名称
- 检查网络连接
- 确认芒果 TV API 可访问

### 问题 2：无法打开浏览器

**解决方案**：
- macOS: 确认 `open` 命令可用（系统自带）
- Windows: 使用 `start` 命令
- Linux: 安装 `xdg-open`

### 问题 3：播放页面无法加载

**解决方案**：
- 清除浏览器缓存
- 尝试无痕模式
- 检查是否需要登录

## 开发计划

- [ ] 支持直接获取视频播放地址（m3u8 解析）
- [ ] 支持下载视频（需 VIP）
- [ ] 支持播放历史记录
- [ ] 支持收藏夹管理
- [ ] 支持更多筛选条件
- [ ] 添加播放列表功能

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过 ClawHub 联系作者。

---

**免责声明**：本 Skill 仅供学习交流使用，请支持正版视频内容。
