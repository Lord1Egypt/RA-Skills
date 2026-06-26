# LuxTTS 技能 - 本地高质量文本转语音

## 概述
LuxTTS 是一个高质量的本地文本转语音模型，支持语音克隆，速度达到实时150倍。本技能将 LuxTTS 集成到 OpenClaw 中，提供本地化的 TTS 服务。

## 特性
- 🚀 **极速生成**：150倍实时速度
- 🎯 **高质量语音**：48kHz 高清音频
- 🔒 **完全本地**：无需云端 API，保护隐私
- 🎨 **语音克隆**：支持自定义语音
- 💾 **智能路径管理**：自动检测安装位置

## 安装位置
- **主安装**：`D:\lux-tts\`（模型、大文件）
- **接口层**：`workspace/lux-tts/`（智能路径管理）
- **自动检测**：支持多个可能的位置

## 部署步骤

### 1. 运行部署脚本
```powershell
# 在 D:\lux-tts\scripts\ 目录下
.\deploy.ps1
```

### 2. 下载模型
```powershell
.\download-model.ps1
```

### 3. 测试安装
```python
# 在 OpenClaw 中测试
from lux_tts import test_installation
test_installation()
```

## 使用方法

### 基本使用
```python
from lux_tts_tool import tts_generate, tts_status

# 检查状态
status = tts_status()
print(status)

# 生成语音
result = tts_generate("你好，我是 LuxTTS")
if result["success"]:
    # result["audio_base64"] 包含 base64 编码的音频
    print(f"生成成功，时长: {result['duration']}秒")
```

### 在 OpenClaw 工具中调用
```python
# 在 OpenClaw 技能中
from lux_tts_tool import get_tts_tool

tts = get_tts_tool()
result = tts.generate("需要转换为语音的文本")
```

### 命令行测试
```bash
# 检查状态
python lux_tts_tool.py status

# 列出语音
python lux_tts_tool.py list

# 生成语音
python lux_tts_tool.py generate "你好世界" --output output.wav
```

## 配置

### 配置文件位置
`D:\lux-tts\config.yaml`

### 配置选项
```yaml
install_path: "D:\\lux-tts"      # 安装位置
device: "cuda"                   # 设备：cuda/cpu
model_repo: "YatharthS/LuxTTS"   # 模型仓库
reference_voice: "voices/test.wav" # 默认语音
audio_format: "wav"              # 音频格式
sample_rate: 48000               # 采样率
cache_enabled: true              # 启用缓存
cache_dir: "cache"               # 缓存目录
```

## 语音管理

### 添加自定义语音
1. 准备清晰的语音文件（WAV/MP3，≥3秒）
2. 复制到 `D:\lux-tts\voices\` 目录
3. 或在代码中调用：
```python
tts.add_voice("path/to/your/voice.wav", "my_voice.wav")
```

### 使用自定义语音
```python
result = tts_generate("文本", voice="D:\\lux-tts\\voices\\my_voice.wav")
```

## 故障排除

### 常见问题

#### 1. "未找到 LuxTTS 安装"
- 检查 `D:\lux-tts\` 目录是否存在
- 运行部署脚本：`deploy.ps1`
- 设置环境变量：`LUX_TTS_PATH=D:\lux-tts`

#### 2. "无法导入 zipvoice"
- 激活虚拟环境：`D:\lux-tts\venv\Scripts\activate`
- 重新安装：`pip install zipvoice-luxvoice`

#### 3. CUDA 不可用
- 检查 NVIDIA 驱动：`nvidia-smi`
- 回退到 CPU：修改 `config.yaml` 中的 `device: "cpu"`

#### 4. 音频质量不佳
- 确保参考音频 ≥3秒，清晰无噪音
- 调整参数：`rms=0.01`, `t_shift=0.9`, `num_steps=4`

### 日志查看
```python
import logging
logging.getLogger('lux_tts').setLevel(logging.DEBUG)
```

## 性能优化

### GPU 加速
- 确保 CUDA 可用：`nvidia-smi`
- 配置文件中设置 `device: "cuda"`

### 缓存启用
- 启用缓存减少重复生成
- 缓存目录：`D:\lux-tts\cache\`

### 批量处理
```python
# 批量生成可复用编码的提示
encoded = tts.client._model.encode_prompt(voice_file)
for text in texts:
    audio = tts.client._model.generate_speech(text, encoded)
```

## 与现有 TTS 集成

### 并行运行模式
```python
def hybrid_tts(text, use_local=True):
    """混合 TTS：本地优先，云端备用"""
    try:
        if use_local:
            return tts_generate(text)
    except Exception:
        pass
    
    # 回退到云端 TTS
    return cloud_tts_generate(text)
```

### 配置 OpenClaw
在 `TOOLS.md` 中添加：
```markdown
## TTS 选项
1. **本地 LuxTTS**：快速、免费、隐私好
2. **云端 TTS**：备用方案
```

## 更新和维护

### 更新模型
```powershell
# 重新下载模型
.\download-model.ps1
```

### 备份配置
```powershell
# 备份重要文件
Copy-Item "D:\lux-tts\config.yaml" "备份路径\"
Copy-Item "D:\lux-tts\voices\" "备份路径\voices\" -Recurse
```

### 清理缓存
```powershell
Remove-Item "D:\lux-tts\cache\*" -Recurse -Force
```

## 许可证
- LuxTTS 模型：Apache-2.0
- 本技能：MIT

## 参考
- [LuxTTS GitHub](https://github.com/ysharma3501/LuxTTS)
- [Hugging Face 模型](https://huggingface.co/YatharthS/LuxTTS)
- [OpenClaw 文档](https://docs.openclaw.ai)

---
*最后更新: 2026-03-16*