---
name: parse-video
description: "视频去水印解析 Skill。支持 20+ 平台短视频去水印解析，包括抖音、快手、小红书、微博、西瓜视频、豆包、云雀、B站等。使用本技能时触发：解析视频、去水印、视频解析、解析链接、下载视频、去除水印、parse video、video parser、抖音解析、快手解析、小红书解析、bilibili 解析、douyin kuaishou redbook weibo xigua doubao yunque bilibili"
---

# parse-video Skill

## 简介

跨平台视频去水印解析工具，支持 20+ 主流短视频和社交媒体平台。首次使用自动下载对应平台的二进制文件。

### 支持平台

| 平台 | 域名 | 支持类型 |
|------|------|----------|
| 抖音 | v.douyin.com, www.iesdouyin.com | 视频/图集 |
| 快手 | v.kuaishou.com | 视频 |
| 小红书 | xhslink.com, www.xiaohongshu.com | 视频/图集/LivePhoto |
| 微博 | weibo.com, weibo.cn | 视频/图集 |
| 西瓜视频 | v.ixigua.com | 视频 |
| 哔哩哔哩 | bilibili.com, b23.tv | 视频 |
| 豆包 | www.doubao.com | 视频/图片 |
| 云雀 | xiaoyunque.jianying.com | 视频 |
| 更多... | ... | ... |

---

## 工作流程

### 方法一：一键解析（推荐）

使用 `scripts/parse.sh` 脚本，首次使用自动下载二进制：

```bash
# 解析任意视频分享链接
bash scripts/parse.sh "https://v.douyin.com/xxx"

# 解析豆包视频
bash scripts/parse.sh "https://www.doubao.com/video-sharing?share_id=xxx&video_id=xxx"

# 解析 B 站视频
bash scripts/parse.sh "https://b23.tv/xxx"
```

### 方法二：启动 HTTP 服务

```bash
# 启动服务（默认端口 8080）
bash scripts/serve.sh

# 指定端口
bash scripts/serve.sh 9090

# 服务启动后可访问 http://localhost:8080 查看 Web UI
```

### 方法三：直接使用 CLI（二进制位于 ~/.cache/parse-video/）

```bash
~/.cache/parse-video/parse-video-darwin-arm64 parse "https://v.douyin.com/xxx"
```

---

## 技术细节

- **二进制下载路径**: `~/.cache/parse-video/`
- **下载源**: Gitee 仓库 dist/ 目录
- **适用系统**: macOS (arm64/amd64), Windows (amd64), Linux
- **首次使用**: 自动检测平台并下载对应二进制（约 30MB）
