# li-feishu-audio 技能

飞书语音交互技能 - 完整的语音消息自动识别、AI 处理、语音回复解决方案。

**作者**: 北京老李 (BeijingLL)  
**版本**: 0.1.1  
**发布日期**: 2026-03-17  
**更新**: 文档增强 - README.md 和 README_EN.md 全面更新

---

## 📖 简介

本技能提供完整的飞书语音交互能力：

```
用户语音 → faster-whisper 识别 → AI 处理 → Edge TTS 合成 → OPUS 转换 → 飞书发送
```

**核心功能**：
- ✅ 语音消息自动识别（faster-whisper 1.2.1）
- ✅ AI 智能回复（支持各大语言模型）
- ✅ 语音合成回复（Edge TTS 7.2.7）
- ✅ 自动格式转换（MP3 → OPUS）
- ✅ 飞书渠道集成
- ✅ 临时文件自动清理
- ✅ 支持自定义目录
- ✅ 不要求 root 权限

---

## 🚀 快速开始

### 安装

```bash
# 从 clawhub 安装
skillhub install li-feishu-audio
```

### 配置环境变量

**必填环境变量**：

| 变量 | 用途 | 获取方式 |
|------|------|---------|
| `FEISHU_APP_ID` | 飞书应用 ID | [飞书开放平台](https://open.feishu.cn/) |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | [飞书开放平台](https://open.feishu.cn/) |

**可选环境变量**：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `FAST_WHISPER_MODEL_DIR` | `$HOME/.fast-whisper-models` | 语音模型存储目录 |
| `VENV_DIR` | `技能目录/.venv` | Python 虚拟环境目录 |
| `TEMP_DIR` | `/tmp` | 临时文件目录 |
| `LOG_DIR` | `技能目录/logs` | 日志目录 |
| `OPENCLAW_CONFIG` | `$HOME/.openclaw/openclaw.json` | OpenClaw 配置文件 |
| `HF_ENDPOINT` | `https://hf-mirror.com` | HuggingFace 镜像（中国加速） |

**配置方法**：

```bash
# 1. 复制配置模板
cd skills/li-feishu-audio/scripts
cp .env.example .env

# 2. 编辑配置文件
vi .env

# 3. 填入实际值
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"

# 4. 加载环境变量
source .env
```

### 运行安装

```bash
./scripts/install.sh
```

安装脚本会：
1. ✅ 检查系统依赖（Python, uv, ffmpeg, jq）
2. ✅ 创建 Python 虚拟环境
3. ✅ 安装 Python 包（faster-whisper, edge-tts）
4. ✅ 下载语音模型
5. ✅ 验证配置

### 测试

```bash
# 重启 OpenClaw 网关
openclaw gateway restart

# 发送语音消息到飞书
# 等待自动识别和语音回复
```

---

## 📁 目录结构

```
li-feishu-audio/
├── SKILL.md              # 技能技术说明
├── README.md             # 中文使用说明（本文件）
├── README_EN.md          # 英文使用说明
├── SECURITY.md           # 安全说明与审计指南
├── .gitignore            # Git 忽略文件
└── scripts/
    ├── .env.example      # 环境变量模板
    ├── install.sh        # 自动安装脚本
    ├── fast-whisper-fast.sh  # 语音识别
    ├── tts-voice.sh      # TTS 生成
    ├── feishu-tts.sh     # 飞书发送
    └── cleanup-tts.sh    # 清理脚本
```

---

## 📋 系统要求

| 组件 | 要求 | 自动安装 |
|------|------|---------|
| 操作系统 | Linux (Ubuntu/Debian) | ❌ |
| Python | 3.11+ | ❌ |
| uv | 任意版本 | ❌ |
| ffmpeg | 任意版本 | ✅ |
| jq | 任意版本 | ✅ |

**权限要求**：不需要 root 权限

---

## 🔧 脚本说明

### install.sh

自动安装脚本：

```bash
./scripts/install.sh
```

**执行步骤**：
1. 检查系统依赖
2. 创建 Python 虚拟环境
3. 安装 Python 包
4. 下载语音模型
5. 创建配置模板
6. 验证飞书凭证

### fast-whisper-fast.sh

语音识别脚本：

```bash
./scripts/fast-whisper-fast.sh <音频文件.ogg>
```

**输出**：
```
[0.00s -> 2.32s] 识别的文本内容
```

### tts-voice.sh

TTS 语音生成脚本：

```bash
./scripts/tts-voice.sh "文本内容" [输出文件.mp3]
```

### feishu-tts.sh

飞书语音发送脚本（自动转换 OPUS）：

```bash
./scripts/feishu-tts.sh <音频文件.mp3> <用户 open_id>
```

### cleanup-tts.sh

临时文件清理脚本：

```bash
./scripts/cleanup-tts.sh [保留数量]

# 定时任务（可选）
0 2 * * * ./scripts/cleanup-tts.sh 10
```

---

## ⚙️ 配置说明

### 飞书凭证

**方法 1: 环境变量**（推荐）

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

**方法 2: openclaw.json**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  }
}
```

**⚠️ 安全提示**：不要将凭证提交到版本控制系统！

### 自定义目录（可选）

在 `.env` 文件中配置：

```bash
# 模型目录（默认：$HOME/.fast-whisper-models）
export FAST_WHISPER_MODEL_DIR="/opt/fast-whisper-models"

# 虚拟环境目录（默认：技能目录/.venv）
export VENV_DIR="/path/to/venv"

# 临时文件目录（默认：/tmp）
export TEMP_DIR="/tmp"

# 日志目录（默认：技能目录/logs）
export LOG_DIR="/path/to/logs"
```

---

## 🔒 安全说明

**详细安全信息请阅读**: [SECURITY.md](SECURITY.md)

### 凭证管理

- ✅ 使用环境变量存储敏感凭证
- ✅ 不要将 `.env` 提交到版本控制
- ✅ 将 `.env` 加入 `.gitignore`
- ✅ 定期更换凭证（建议每 3-6 个月）

### 权限说明

- ✅ 不要求 root 权限
- ✅ 所有目录使用用户家目录（`$HOME/`）
- ✅ 虚拟环境在技能目录下

### 网络访问

| 服务 | URL | 用途 |
|------|-----|------|
| 飞书 API | `https://open.feishu.cn/` | 发送语音消息 |
| HuggingFace 镜像 | `https://hf-mirror.com/` | 下载语音模型 |
| 微软 Edge TTS | `https://speech.platform.bing.com/` | 语音合成 |

---

## 🛠️ 故障排查

### 语音识别失败

**检查**:
1. 模型是否下载：`ls $FAST_WHISPER_MODEL_DIR/`
2. 虚拟环境：`技能目录/.venv/bin/python --version`
3. 网络：`export HF_ENDPOINT=https://hf-mirror.com`

### TTS 生成失败

**检查**:
1. edge-tts 安装：`uv pip list -p 技能目录/.venv | grep edge`
2. 网络连接：Edge TTS 需要访问微软服务

### 飞书发送失败

**检查**:
1. 凭证配置：`echo $FEISHU_APP_ID`
2. 音频格式：必须是 OPUS
3. 用户 ID 类型：使用 open_id

---

## 📊 性能指标

| 操作 | 耗时 |
|------|------|
| 语音识别 (tiny) | ~8-10 秒 |
| TTS 生成 | ~3-5 秒 |
| OPUS 转换 | <1 秒 |
| 飞书上传 | ~2-3 秒 |
| **总计** | **~15 秒** |

---

## 📝 版本历史

### 重新发布版本

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| **0.1.0** | **2026-03-17** | **安全增强**（默认路径使用 $HOME/，声明环境变量，添加 SECURITY.md） |
| **0.1.1** | **2026-03-17** | **文档增强**（README.md 和 README_EN.md 全面更新） |

### 历史版本（已删除）

~~0.0.1 - 0.0.10: 初始开发版本~~

---

## 📞 支持

- **安全文档**: [SECURITY.md](SECURITY.md)
- **技能文档**: [SKILL.md](SKILL.md)
- **OpenClaw 文档**: https://docs.openclaw.ai
- **飞书开放平台**: https://open.feishu.cn/document

---

## 📋 作者

**北京老李 (BeijingLL)**

---

**最后更新**: 2026-03-17  
**版本**: 0.0.9
