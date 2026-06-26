# MLX Local AI

一键部署本地 AI 服务，支持 Apple Silicon (M1/M2/M3/M4)。

## 功能

- 🤖 **本地 LLM 服务**：Qwen3.5-4B-OptiQ-4bit
- 📊 **Embedding 服务**：bge-base-zh-v1.5
- 🔄 **OpenClaw Gateway**：统一 API 网关
- 🎯 **一键安装/启动/停止**

## 快速开始

```bash
# 1. 安装
./install.sh

# 2. 启动服务
~/start_ai.sh start

# 3. 检查状态
~/start_ai.sh status

# 4. 测试 API
~/start_ai.sh test
```

## 文件结构

```
mlx-local-ai/
├── SKILL.md           # 技能说明
├── README.md          # 本文件
├── install.sh         # 安装脚本
├── uninstall.sh       # 卸载脚本
├── config/            # 配置文件
│   ├── openclaw.json  # OpenClaw 配置
│   └── env.example    # 环境变量示例
└── scripts/           # 工具脚本
    ├── check_deps.py  # 依赖检查
    └── test_api.py    # API 测试
```

## 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Chat API | 8080 | OpenAI 兼容 API |
| Embedding API | 8081 | 向量嵌入 API |

## 用于 ClawHub

此技能可发布到 ClawHub 供其他用户安装使用。

### 发布命令

```bash
clawhub publish mlx-local-ai
```

### 安装命令

```bash
clawhub install mlx-local-ai --dir ~/.openclaw/skills
```

## 许可证

MIT License
