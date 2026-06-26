# li_nvvideocodec Skill 目录结构

作者: 北京老李 (beijingLL)

## 📁 完整目录

```
li_nvvideocodec/
│
├── README.md                    # 📖 主文档（通用说明）
├── SKILL.md                     # 📋 Skill描述（所有agent通用）
├── skill.json                   # 🔧 结构化配置（hermes/openclaw）
├── agent_interface.py           # 🤖 Agent统一API接口
├── requirements.txt             # 📦 Python依赖
│
├── hermes_config.json           # 📝 hermes专用配置
├── openclaw_config.yaml         # 📝 openclaw专用配置
├── AGENT_USAGE.md               # 📚 Agent集成详细指南
├── STRUCTURE.md                 # 📋 本文件
│
└── scripts/
    └── compress_videos.py       # 🎬 主压缩脚本
```

## 📄 文件说明

### 核心文件（必需）

| 文件 | 用途 | 谁需要 |
|------|------|--------|
| `README.md` | 主文档，使用说明 | 所有用户 |
| `SKILL.md` | Skill元数据 | 所有agent |
| `agent_interface.py` | 统一API入口 | hermes, openclaw, qwen-code |
| `scripts/compress_videos.py` | 实际压缩逻辑 | 所有 |

### 配置文件（可选）

| 文件 | 用途 | 谁需要 |
|------|------|--------|
| `skill.json` | 结构化配置 | hermes, openclaw |
| `hermes_config.json` | hermes专用 | hermes |
| `openclaw_config.yaml` | openclaw专用 | openclaw |

### 文档文件（参考）

| 文件 | 用途 |
|------|------|
| `AGENT_USAGE.md` | Agent集成详细指南 |
| `STRUCTURE.md` | 目录结构说明 |
| `requirements.txt` | Python依赖列表 |

## 🤖 不同Agent的使用方式

### hermes

```bash
# 方式1：使用skill.json配置
hermes skill load li_nvvideocodec/skill.json

# 方式2：使用专用配置
hermes skill load li_nvvideocodec/hermes_config.json

# 方式3：直接调用
hermes run li_nvvideocodec/agent_interface.py --action check
```

### openclaw

```bash
# 方式1：使用yaml配置
openclaw skill load li_nvvideocodec/openclaw_config.yaml

# 方式2：使用json配置
openclaw skill load li_nvvideocodec/skill.json

# 方式3：直接调用
openclaw exec li_nvvideocodec/agent_interface.py analyze -i "目录"
```

### qwen-code

```bash
# 直接使用，当用户提到"压缩视频"时自动推荐
python li_nvvideocodec/scripts/compress_videos.py -i "目录" -p B

# 或使用agent接口
python li_nvvideocodec/agent_interface.py --action compress -i "目录" -p B
```

## 🔄 Agent调用流程

```
用户请求
   ↓
Agent识别意图（"压缩视频"）
   ↓
Agent读取 SKILL.md 或 skill.json
   ↓
Agent调用 agent_interface.py
   ↓
   ├─ --action check      → 检查环境
   ├─ --action analyze    → 分析视频
   └─ --action compress   → 压缩视频
   ↓
返回结果给用户
```

## 📊 数据流

```
agent_interface.py
   ↓
读取 skill.json / hermes_config.json / openclaw_config.yaml
   ↓
调用 scripts/compress_videos.py
   ↓
执行FFmpeg命令
   ↓
返回JSON或文本结果
```

## ✅ 兼容性保证

所有配置文件都包含：
- `compatible_agents` 字段
- 统一的action定义
- 标准的参数格式

确保三个agent都可以正确解析和使用。
