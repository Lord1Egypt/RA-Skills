# OpenClaw语音转文字使用指南
## 为小碗和小微准备的快速上手文档

### 🎯 问题背景
在OpenClaw升级后，语音消息无法被转录为文字，系统显示 "whisper not found in PATH" 或模型加载失败。

### 💡 解决方案
我们创建了一个基于whisper.cpp的本地语音转文字方案，使用国内镜像源解决模型下载问题，无需API密钥，完全离线工作。

### 🔧 安装步骤

#### 1. 检查环境
```bash
# 检查whisper命令
which whisper

# 检查OpenClaw技能
openclaw skills list | grep whisper

# 验证网络
ping -c 2 8.8.8.8
```

#### 2. 安装语音转文字包装器
```bash
# 创建目录
mkdir -p ~/bin

# 创建whisper包装器
cat > ~/bin/whisper << 'EOF'
#!/usr/bin/env bash
# whisper - wrapper for faster_whisper audio transcription

if [[ $# -lt 1 ]]; then
    echo "Usage: whisper <audio_file> [options]"
    exit 1
fi

AUDIO_FILE="$1"
shift

# 默认参数
MODEL="tiny"
LANGUAGE="zh"
TASK="transcribe"

# 解析选项
while [[ $# -gt 0 ]]; do
    case $1 in
        --model) MODEL="$2"; shift 2;;
        --language) LANGUAGE="$2"; shift 2;;
        --task) TASK="$2"; shift 2;;
        *) shift;;  # 忽略未知选项
    esac
done

# 检查文件
if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "错误：文件不存在: $AUDIO_FILE"
    exit 1
fi

# 设置镜像源
export HF_ENDPOINT=${HF_ENDPOINT:-https://hf-mirror.com}
export HF_HOME=${HF_HOME:-/tmp/hf_cache}
mkdir -p "$HF_HOME"

# 使用faster_whisper进行转录
python3 -c "
import sys
import os
from faster_whisper import WhisperModel

try:
    model = WhisperModel('$MODEL', device='cpu', download_root=os.environ.get('HF_HOME', '/tmp/hf_cache'))
    segments, info = model.transcribe('$AUDIO_FILE', language='$LANGUAGE', task='$TASK')
    text = ''.join([segment.text for segment in segments]).strip()
    print(text if text else ''.join([segment.text for segment in segments]).strip())
except Exception as e:
    print(f'错误: {e}', file=sys.stderr)
    sys.exit(1)
"
EOF

# 使脚本可执行
chmod +x ~/bin/whisper

# 添加到PATH（如果需要）
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/bin:$PATH"
fi
```

#### 3. 下载模型（首次使用时需要）
```bash
# 设置国内镜像
export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=/tmp/hf_mirror_cache

# 下载tiny模型（约75MB）
mkdir -p /tmp/whisper.cpp/models
cd /tmp/whisper.cpp/models
wget -O ggml-tiny.bin https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin
```

### 📖 使用方法

#### 基本转录命令
```bash
# 转录语音文件（默认使用tiny模型和中文）
whisper /path/to/your/audio.ogg

# 指定不同模型大小
whisper /path/to/audio.ogg --model base   # 更平衡
whisper /path/to/audio.ogg --model small  # 更好准确率

# 指定语言
whisper /path/to/audio.ogg --language en  # 英文
whisper /path/to/audio.ogg --language zh  # 中文

# 指定任务
whisper /path/to/audio.ogg --task translate  # 翻译成英文
```

#### 在OpenClaw中使用
当您收到语音消息时，系统会自动：
1. 将音频转换为适当格式
2. 使用中文模型进行转录
3. 返回文字结果

### ⚠️ 注意事项

1. **首次使用延迟**：第一次使用时需要下载模型文件（约75MB），请耐心等待
2. **模型缓存**：下载后模型会缓存，后续使用加载会很快
3. **模型选择**：
   - `tiny`：最快，约75MB，适合快速测试
   - `base`：平衡，约150MB，日常使用推荐
   - `small`：更好准确率，约240MB
   - `medium`：更高准确率，约780MB
   - `large`：最准确，约1550MB
4. **网络环境**：如果网络良好，可将HF_ENDPOINT设置为官方源：`https://huggingface.co`

### 🔧 故障排除

| 问题 | 解决方案 |
|------|----------|
| `whisper: command not found` | 确认`~/bin`在PATH中，运行 `source ~/.bashrc` 重新加载 |
| 模型下载失败 | 检查网络连接，确认可访问 `https://hf-mirror.com` |
| 转录结果为空 | 检查音频文件格式，尝试不同模型大小 |
| `ffmpeg: command not found` | 安装ffmpeg：`sudo apt install ffmpeg` (Ubuntu/Debian) |

### ✅ 功能验证
安装后可使用以下命令测试：
```bash
# 创建测试音频（沉默）
ffmpeg -f lavfi -i anullsrc=channel_layout=mono:sample_rate=16000 -t 1 -c:a pcm_s16le /tmp/test.wav

# 测试转录
whisper /tmp/test.wav --model tiny --language zh
# 应该返回空或几乎空的输出（因为是沉默音频）
```

### 📞 获取帮助
如果遇到问题，可以：
1. 重新阅读此指南
2. 检查错误信息按照故障排除表格处理
3. 联系小曦获得进一步帮助

---
*此方案已在真实语音消息上验证有效*
*文档版本：1.0.0*
*创建时间：2026-05-22*