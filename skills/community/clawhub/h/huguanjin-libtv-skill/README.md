# libtv-skill

agent-im 会话技能 — 通过 [LibTV](https://www.liblib.tv) 的 AI 能力生成和编辑图片/视频，同时兼容 Gemini 文生图、Sora/Veo/Grok/豆包/Vidu 视频直连。

## 功能概览

| 模式 | 接口 | 说明 |
|------|------|------|
| LibTV 会话 | agent-im OpenAPI | 创建会话、发消息、上传文件、轮询结果、下载 |
| Gemini 文生图 | generateContent | 支持宽高比、清晰度控制 |
| Sora/Veo/Grok/豆包 | POST /v1/videos | 文生视频、图生视频 |
| Vidu | POST /v1/video/generations | 文生视频、图生视频、首尾帧 |

## 快速开始

1. 复制环境变量模板：

```bash
cp .env.example .env
```

2. 填入你的 API Key（至少配置 `LIBTV_ACCESS_KEY`）。

3. 运行脚本（仅需 Python 3 标准库，无额外依赖）：

```bash
# 创建会话并发送消息
python3 scripts/create_session.py "生一个动漫视频"

# 查询进度
python3 scripts/query_session.py SESSION_ID
```

详细配置说明见 [CONFIG.md](CONFIG.md)，冒烟测试见 [SMOKE_TESTS.md](SMOKE_TESTS.md)。

## 目录结构

```
libtv-skill/
├── SKILL.md           # 技能定义（Agent 读取）
├── _meta.json         # OpenClaw 发布元数据
├── CONFIG.md          # 配置指南
├── SMOKE_TESTS.md     # 冒烟测试清单
├── README.md          # 本文件
├── .env.example       # 环境变量模板
├── scripts/           # 可执行脚本
│   ├── _common.py     # LibTV OpenAPI 客户端
│   ├── _config.py     # 环境变量管理
│   ├── _logger.py     # 日志输出
│   ├── _validators.py # 输入校验
│   ├── create_session.py
│   ├── query_session.py
│   ├── change_project.py
│   ├── upload_file.py
│   ├── download_results.py
│   ├── gemini_generate_image.py
│   ├── sora_generate_video.py / sora_query_video.py
│   ├── veo_generate_video.py  / veo_query_video.py
│   ├── grok_generate_video.py / grok_query_video.py
│   ├── doubao_generate_video.py / doubao_query_video.py
│   └── vidu_generate_video.py / vidu_query_video.py
├── examples/          # 示例数据
└── references/        # 输出格式、工作流参考文档
```

## 许可证

Apache-2.0
