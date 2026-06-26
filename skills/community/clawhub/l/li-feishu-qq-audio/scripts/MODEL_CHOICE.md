# 模型选择指南

## 快速开始

### 安装时选择模型

使用增强版安装脚本，支持交互式模型选择：

```bash
cd ~/.openclaw/workspace/skills/li-feishu-audio
./scripts/install-with-model-choice.sh
```

安装时会提示：
```
请选择 faster-whisper 模型大小：
  1) tiny   (约 75MB,  最快，准确率较低)  ← 推荐默认
  2) base   (约 142MB, 快速，准确率中等)
  3) small  (约 466MB, 中等速度，准确率高)
  4) medium (约 1.5GB, 较慢，准确率最高)

请选择模型 [1-4, 默认:1]:
```

### 切换已有模型

编辑 `scripts/.env` 文件：

```bash
vi scripts/.env
```

修改 `WHISPER_MODEL` 配置：

```bash
# 从 tiny 切换到 base
WHISPER_MODEL=base
```

然后重新运行安装脚本（会自动检测新模型并下载）：

```bash
./scripts/install-with-model-choice.sh
```

## 模型对比

| 模型 | 大小 | 速度 | 准确率 | 适用场景 |
|------|------|------|--------|----------|
| **tiny** | 75MB | ⚡⚡⚡ | ⭐⭐ | 清晰语音、快速响应 |
| **base** | 142MB | ⚡⚡ | ⭐⭐⭐ | 日常使用（推荐） |
| **small** | 466MB | ⚡ | ⭐⭐⭐⭐ | 嘈杂环境、多方言 |
| **medium** | 1.5GB | 🐌 | ⭐⭐⭐⭐⭐ | 专业场景、高精度要求 |

## 性能参考

在普通 CPU（Intel i5）上的测试：

| 模型 | 识别速度 | 内存占用 |
|------|----------|----------|
| tiny | ~0.3x 实时 | ~500MB |
| base | ~0.5x 实时 | ~800MB |
| small | ~1.0x 实时 | ~1.5GB |
| medium | ~2.0x 实时 | ~3GB |

*注：0.3x 实时 = 1 分钟音频需 18 秒识别完成*

## 配置说明

### 环境变量

在 `scripts/.env` 中配置：

```bash
# 模型名称（tiny/base/small/medium）
WHISPER_MODEL=tiny

# 模型缓存目录（可选）
FAST_WHISPER_MODEL_DIR=/root/.fast-whisper-models

# 虚拟环境目录（可选）
VENV_DIR=/root/.openclaw/workspace/skills/li-feishu-audio/.venv
```

### 脚本中使用

`fast-whisper-fast.sh` 会自动读取配置：

```bash
# 加载环境变量
source scripts/.env

# 运行识别（自动使用配置的模型）
./scripts/fast-whisper-fast.sh audio.wav
```

## 多模型共存

可以安装多个模型，根据需要切换：

```bash
# 首次安装 tiny 模型
WHISPER_MODEL=tiny ./scripts/install-with-model-choice.sh

# 下载 base 模型（不删除 tiny）
WHISPER_MODEL=base ./scripts/install-with-model-choice.sh

# 切换回 tiny
WHISPER_MODEL=tiny ./scripts/fast-whisper-fast.sh audio.wav
```

模型文件会存储在 `FAST_WHISPER_MODEL_DIR` 目录下，按模型名称分隔。

## 手动下载模型

如果自动下载失败，可以手动下载：

```bash
# 使用 hf-mirror 下载
export HF_ENDPOINT=https://hf-mirror.com

cd /root/.fast-whisper-models

# 下载 base 模型
git lfs install
git clone https://hf-mirror.com/Systran/faster-whisper-base.git
```

## 故障排查

### 模型下载失败

```bash
# 检查网络
curl -I https://hf-mirror.com

# 使用代理
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# 重新运行安装
./scripts/install-with-model-choice.sh --force
```

### 识别准确率低

1. 尝试更大的模型（tiny → base → small）
2. 确保音频质量良好（无噪音、音量适中）
3. 检查音频格式（推荐 16kHz, 16bit, 单声道）

### 内存不足

```bash
# 检查内存
free -h

# 使用更小的模型
WHISPER_MODEL=tiny
```

## 最佳实践

1. **首次安装**：使用 `tiny` 模型测试功能
2. **日常使用**：升级到 `base` 模型（平衡速度和准确率）
3. **专业场景**：考虑 `small` 或 `medium`（需要更强硬件）
4. **定期清理**：运行 `./scripts/cleanup-tts.sh --weekly` 清理临时文件
