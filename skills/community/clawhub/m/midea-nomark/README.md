# parse-video Skill

> 跨平台视频去水印解析工具，支持 20+ 平台

## 功能特性

- 🎬 **20+ 平台支持**：抖音、快手、小红书、微博、B站、西瓜视频、豆包、云雀等
- 🌐 **跨平台兼容**：macOS (Intel/Apple Silicon)、Windows、Linux
- 💧 **无水印下载**：自动去除视频水印，解析纯净视频链接
- ⚡ **快速响应**：本地二进制，无需等待远程服务器
- 🔒 **安全可靠**：不开源可执行文件，仅本地运行

## 支持的平台

| 平台 | 链接格式 | 类型 |
|------|----------|------|
| 抖音 | v.douyin.com | 视频/图集 |
| 快手 | v.kuaishou.com | 视频 |
| 小红书 | xhslink.com | 视频/图集 |
| 微博 | weibo.com | 视频/图集 |
| B站 | b23.tv | 视频 |
| 豆包 | www.doubao.com | 视频/图片 |
| 云雀 | xiaoyunque.jianying.com | 视频 |
| ... | ... | ... |

## 安装

解压后将 `parse-video` 文件夹复制到 `~/.workbuddy/skills/` 目录

## 使用

在 AI 助手中直接发送视频链接即可自动解析：
```
帮我去水印下载这个视频 https://v.douyin.com/xxx
```

或使用命令行：
```bash
bash scripts/parse.sh "https://v.douyin.com/xxx"
bash scripts/serve.sh 8080  # 启动 HTTP 服务
```

## 文件结构

```
parse-video/
├── SKILL.md              # 技能说明
├── README.md             # 使用说明
├── _skillhub_meta.json   # 元数据
├── scripts/
│   ├── parse.sh          # 解析脚本
│   └── serve.sh          # 服务脚本
└── assets/
    ├── parse-video-darwin-arm64    # macOS ARM64
    ├── parse-video-darwin-amd64    # macOS x64
    └── parse-video-win64.exe       # Windows x64
```

## 注意事项

- 解析结果为临时链接，建议及时下载
- 仅供个人学习研究使用
- 部分平台可能因接口调整而失效
