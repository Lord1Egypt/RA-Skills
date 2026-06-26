# 安全说明

本文档说明 li-feishu-audio 技能的安全配置和注意事项。

## 🔐 所需凭证

### 必填环境变量

| 变量 | 用途 | 获取方式 |
|------|------|---------|
| `FEISHU_APP_ID` | 飞书应用 ID | [飞书开放平台](https://open.feishu.cn/) |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | [飞书开放平台](https://open.feishu.cn/) |

### 可选环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `FAST_WHISPER_MODEL_DIR` | `$HOME/.fast-whisper-models` | 语音模型存储目录 |
| `VENV_DIR` | `技能目录/.venv` | Python 虚拟环境目录 |
| `TEMP_DIR` | `/tmp` | 临时文件目录 |
| `LOG_DIR` | `技能目录/logs` | 日志目录 |
| `OPENCLAW_CONFIG` | `$HOME/.openclaw/openclaw.json` | OpenClaw 配置文件 |
| `HF_ENDPOINT` | `https://hf-mirror.com` | HuggingFace 镜像（中国加速） |

## 🔒 安全配置

### 1. 凭证管理

**推荐方式**：使用 `.env` 文件

```bash
# 复制模板
cd skills/li-feishu-audio/scripts
cp .env.example .env

# 编辑填入实际值
vi .env

# 加载环境变量
source .env
```

**安全提示**：
- ⚠️ 不要将 `.env` 提交到 Git
- ⚠️ 不要分享凭证
- ⚠️ 定期更换凭证

### 2. 目录权限

**默认配置（不需要 root 权限）**：

| 目录 | 权限 | 说明 |
|------|------|------|
| 技能目录 | 用户读写 | 技能安装位置 |
| 模型目录 | 用户读写 | `$HOME/.fast-whisper-models` |
| 虚拟环境 | 用户读写 | `技能目录/.venv` |
| 临时文件 | 用户读写 | `/tmp` |

**不需要修改系统目录！**

### 3. 网络访问

**技能会访问的外部服务**：

| 服务 | URL | 用途 |
|------|-----|------|
| 飞书 API | `https://open.feishu.cn/` | 发送语音消息 |
| HuggingFace 镜像 | `https://hf-mirror.com/` | 下载语音模型 |
| 微软 Edge TTS | `https://speech.platform.bing.com/` | 语音合成 |

### 4. 系统调用

**技能使用的系统命令**：

| 命令 | 用途 |
|------|------|
| `ffmpeg` | 音频格式转换（MP3 → OPUS） |
| `jq` | JSON 处理 |
| `curl` | 飞书 API 调用 |
| `uv` | Python 包管理 |

## ⚠️ 风险提示

### 已知风险

1. **凭证泄露风险**
   - 风险：`.env` 文件包含敏感凭证
   - 缓解：已配置 `.gitignore`，不要手动分享

2. **临时文件**
   - 风险：`/tmp` 目录存储临时音频文件
   - 缓解：自动清理脚本（可配置 cron）

3. **网络请求**
   - 风险：向飞书 API 发送请求
   - 缓解：仅使用官方 API，凭证加密传输

### 缓解措施

1. **使用最小权限**
   - 不使用 root 运行
   - 所有目录使用用户家目录

2. **定期清理**
   ```bash
   # 手动清理
   ./scripts/cleanup-tts.sh
   
   # 或配置 cron（可选）
   0 2 * * * /path/to/scripts/cleanup-tts.sh
   ```

3. **凭证轮换**
   - 建议每 3-6 个月更换飞书凭证
   - 在飞书开放平台重新生成 App Secret

## 🔍 审计指南

### 安装前检查

```bash
# 1. 检查脚本内容
cat scripts/install.sh
cat scripts/*.sh

# 2. 检查网络连接
curl -I https://open.feishu.cn/
curl -I https://hf-mirror.com/

# 3. 检查系统依赖
which python3 uv ffmpeg jq
```

### 运行时监控

```bash
# 查看日志（如果配置）
tail -f $LOG_DIR/*.log

# 监控临时文件
ls -la /tmp/openclaw/

# 检查网络连接
netstat -an | grep feishu
```

## 📋 合规说明

### 数据收集

**本技能不收集任何用户数据**：
- ❌ 不收集语音内容
- ❌ 不收集聊天记录
- ❌ 不收集个人信息

**仅存储**：
- ✅ 临时音频文件（自动清理）
- ✅ 模型文件（本地使用）

### 第三方服务

| 服务 | 数据 | 用途 |
|------|------|------|
| 飞书 | 语音消息 | 发送回复 |
| HuggingFace | 模型文件 | 语音识别 |
| 微软 Edge TTS | 文本 | 语音合成 |

## 🆘 问题反馈

如发现安全问题，请联系：
- 作者：北京老李 (BeijingLL)
- 发布平台：clawhub

---

**最后更新**: 2026-03-17  
**版本**: 0.0.8
