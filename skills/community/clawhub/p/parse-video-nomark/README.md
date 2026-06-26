# parse-video

> 跨平台视频去水印解析工具，支持 20+ 平台（抖音、快手、小红书、微博、B站、豆包、云雀等）

## 功能特性

- 🎬 **20+ 平台支持**：抖音、快手、小红书、微博、B站、西瓜视频、豆包、云雀等
- 🌐 **跨平台兼容**：macOS (Intel/Apple Silicon)、Windows、Linux
- 💧 **无水印下载**：自动去除视频水印，解析纯净视频链接
- ⚡ **首次自动下载**：首次使用自动检测平台并下载对应二进制
- 🔒 **安全可靠**：不开源可执行文件，仅本地运行

## 安装

1. 解压后将 `parse-video` 文件夹复制到 `~/.workbuddy/skills/` 目录
2. 在 WorkBuddy/OpenCat 中重新加载即可

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

## 二进制下载

二进制文件托管在 Gitee Release dist/ 目录：
- `parse-video-darwin-arm64` — macOS ARM64
- `parse-video-darwin-amd64` — macOS Intel
- `parse-video-win64.exe` — Windows x64

首次使用脚本会自动下载对应平台的二进制到 `~/.cache/parse-video/`。

## 文件结构

```
parse-video/
├── SKILL.md              # 技能说明
├── README.md             # 使用说明
├── _skillhub_meta.json   # 元数据
├── scripts/
│   ├── parse.sh          # 解析脚本（自动下载二进制）
│   └── serve.sh          # 服务脚本（自动下载二进制）
└── dist/                  # 二进制文件（由 Gitee 托管）
    ├── parse-video-darwin-arm64
    ├── parse-video-darwin-amd64
    └── parse-video-win64.exe
```

## 注意事项

- 解析结果为临时链接，建议及时下载
- 仅供个人学习研究使用
- 部分平台可能因接口调整而失效
