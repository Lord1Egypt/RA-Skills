---
name: mgtv
description: 搜索芒果 TV 视频资源并在系统浏览器中播放
version: 1.0.2
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "📺"
---

# MGTV - 芒果 TV 视频搜索与播放

## 功能说明

此 skill 用于搜索芒果 TV 视频资源，并在系统默认浏览器中打开播放页面。

## 何时使用

当用户请求：
- 搜索芒果 TV 的视频（综艺、电视剧、电影、动漫等）
- 播放芒果 TV 的节目
- 打开芒果 TV 网站
- 查找特定的芒果 TV 内容
- 打开芒果 TV 视频链接

## 使用示例

### 搜索视频

```
用户："我想看《乘风破浪的姐姐》"
→ 在浏览器中打开芒果 TV 搜索页面

用户："播放芒果 TV 的《歌手 2024》"
→ 搜索并打开相关视频

用户："帮我找一下《大侦探》最新一期"
→ 打开搜索结果页面
```

### 直接打开链接

```
用户："打开这个芒果 TV 视频：https://www.mgtv.com/b/xxx/xxx.html"
→ 直接在浏览器中播放视频

用户："打开芒果 TV 首页"
→ 打开 mgtv.com
```

## 使用方法

### 命令行

```bash
# 搜索视频
node scripts/search-mgtv.js --query "节目名称"

# 直接打开 URL
node scripts/search-mgtv.js --direct-url "https://www.mgtv.com/b/xxx/xxx.html"
```

### 参数说明

- `--query`: 搜索关键词（必填，用于搜索）
- `--direct-url`: 直接打开的视频 URL（用于已知链接时）

## 脚本说明

### scripts/search-mgtv.js

主要脚本，功能：
1. 解析命令行参数
2. 构建芒果 TV 搜索 URL 或使用提供的 URL
3. 调用系统命令在浏览器中打开

支持的操作系统：
- macOS: 使用 `open` 命令
- Windows: 使用 `start` 命令
- Linux: 使用 `xdg-open` 命令

## 注意事项

1. **网络连接**：需要能够访问芒果 TV 网站
2. **浏览器**：系统需要有默认浏览器
3. **VIP 内容**：部分视频需要芒果 TV 会员账号
4. **搜索精确度**：使用完整节目名称效果更好

## 故障排除

### 浏览器无法打开
- 确认系统有相应的命令（macOS: open, Windows: start, Linux: xdg-open）

### 搜索无结果
- 使用更精确的节目名称
- 检查网络连接

### 视频无法播放
- 清除浏览器缓存
- 检查是否需要登录 VIP 账号

## 测试

```bash
# 运行测试套件
node scripts/test.js

# 单个测试
node scripts/search-mgtv.js --query "歌手"
```

## 文件结构

```
mgtv/
├── SKILL.md           # Skill 定义（本文件）
├── README.md          # 详细文档
├── USAGE.md           # 使用指南
├── package.json       # 项目配置
├── .gitignore         # Git 忽略文件
├── .clawhubignore     # Clawhub 忽略文件
└── scripts/
    ├── search-mgtv.js # 主脚本
    └── test.js        # 测试脚本
```

## 许可证

MIT License

---

**免责声明**：本 Skill 仅供学习交流使用，请支持正版视频内容。
