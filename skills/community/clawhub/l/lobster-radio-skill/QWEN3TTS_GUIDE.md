# Qwen3-TTS 安装和使用指南

Qwen3-TTS是阿里开源的高质量TTS模型，但**不在Ollama公共仓库中**。本文档说明如何正确下载和使用Qwen3-TTS。

## 模型信息

### 模型规格

| 模型名称 | 参数量 | 显存需求 | 特点 |
|---------|--------|---------|------|
| Qwen3-TTS-12Hz-0.6B-Base | 6亿 | 4-8GB | 性能与效率平衡，实时场景首选 |
| Qwen3-TTS-1.7B | 17亿 | 8-16GB | 性能最优、控制能力最强 |

### 核心能力

- ✅ **秒级声音克隆**：仅需3秒语音样本
- ✅ **语音设计**：通过文字描述创造新音色
- ✅ **多语言支持**：10种主流语言
- ✅ **多方言支持**：四川话、北京话等
- ✅ **跨语言音色一致性**：切换语言音色不变
- ✅ **实时流式输出**：端到端延迟97ms
- ✅ **100%本地运行**：无云端依赖

## 安装步骤

### 方法一：从HuggingFace下载（推荐）

#### 1. 安装依赖

```bash
pip install torch transformers accelerate huggingface_hub
```

#### 2. 下载模型

**方式A：使用Python脚本下载**

```python
from huggingface_hub import snapshot_download

# 下载0.6B模型（推荐，显存需求低）
snapshot_download(
    repo_id="Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    local_dir="./models/Qwen3-TTS-12Hz-0.6B-Base",
    local_dir_use_symlinks=False
)

# 或下载1.7B模型（性能更好）
snapshot_download(
    repo_id="Qwen/Qwen3-TTS-1.7B",
    local_dir="./models/Qwen3-TTS-1.7B",
    local_dir_use_symlinks=False
)
```

**方式B：使用huggingface-cli下载**

```bash
# 安装huggingface_hub
pip install huggingface_hub

# 下载模型
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base
```

#### 3. 验证下载

```bash
# 检查模型文件
ls -lh ./models/Qwen3-TTS-12Hz-0.6B-Base

# 应该看到以下文件：
# config.json
# pytorch_model.bin
# tokenizer.json
# tokenizer_config.json
# special_tokens_map.json
```

### 方法二：从ModelScope下载（国内用户推荐）

#### 1. 安装ModelScope

```bash
pip install modelscope
```

#### 2. 下载模型

```python
from modelscope import snapshot_download

model_dir = snapshot_download(
    'qwen/Qwen3-TTS-12Hz-0.6B-Base',
    cache_dir='./models'
)

print(f"模型已下载到: {model_dir}")
```

### 方法三：使用Git LFS下载

```bash
# 安装Git LFS
git lfs install

# 克隆模型仓库
git clone https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice

# 或从ModelScope克隆
git clone https://modelscope.cn/qwen/Qwen3-TTS-12Hz-0.6B-Base
```

## 使用方法

### 基础使用

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 加载模型
model_name = "./models/Qwen3-TTS-12Hz-0.6B-Base"  # 或 "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

# 生成语音
text = "今天的人工智能领域发展迅速，让我们一起探索最新的技术趋势。"
voice_prompt = "请用温柔女声，语速适中，声音甜美朗读以下内容："

prompt = f"{voice_prompt}\n{text}"

with torch.no_grad():
    output = model.generate(
        **tokenizer(prompt, return_tensors="pt").to("cuda"),
        max_new_tokens=2048,
        do_sample=True,
        temperature=0.7
    )

# 提取音频
output_text = tokenizer.decode(output[0], skip_special_tokens=False)

if "<audio>" in output_text and "</audio>" in output_text:
    import base64
    audio_start = output_text.find("<audio>") + 7
    audio_end = output_text.find("</audio>")
    audio_base64 = output_text[audio_start:audio_end]
    audio_data = base64.b64decode(audio_base64)
    
    # 保存音频文件
    with open("output.wav", "wb") as f:
        f.write(audio_data)
    
    print("音频已保存到 output.wav")
```

### 高级使用：声音克隆

```python
# 使用3秒语音样本克隆声音
reference_audio = "./reference_voice.wav"  # 3秒清晰语音样本

prompt = f"请模仿以下声音朗读：{reference_audio}\n{text}"

with torch.no_grad():
    output = model.generate(
        **tokenizer(prompt, return_tensors="pt").to("cuda"),
        max_new_tokens=2048
    )

# 提取音频...
```

### 高级使用：语音设计

```python
# 通过文字描述创造新音色
voice_description = "17岁元气少女，声音清甜带奶音，语速稍快"
prompt = f"请用{voice_description}朗读以下内容：\n{text}"

with torch.no_grad():
    output = model.generate(
        **tokenizer(prompt, return_tensors="pt").to("cuda"),
        max_new_tokens=2048
    )

# 提取音频...
```

## 系统要求

### 最低配置（Qwen3-TTS-12Hz-0.6B-Base）

- **CPU**: 任意现代CPU（可运行，但速度慢）
- **内存**: 8GB RAM
- **存储**: 5GB可用空间
- **GPU**: 可选（推荐）

### 推荐配置（Qwen3-TTS-12Hz-0.6B-Base）

- **GPU**: NVIDIA显卡（支持CUDA）
- **显存**: 4GB以上
- **内存**: 16GB RAM
- **存储**: 10GB可用空间

### 推荐配置（Qwen3-TTS-1.7B）

- **GPU**: NVIDIA显卡（RTX 3080及以上）
- **显存**: 8GB以上（推荐16GB）
- **内存**: 32GB RAM
- **存储**: 20GB可用空间

## 性能优化

### 1. 使用GPU加速

```python
# 检查CUDA是否可用
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(0)}")

# 使用GPU
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.float16,  # 使用FP16减少显存
    device_map="auto"
)
```

### 2. 使用CPU（无GPU情况）

```python
# 使用CPU
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.float32,
    device_map="cpu"
)
```

### 3. 量化模型（减少显存）

```python
# 使用8-bit量化
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    load_in_8bit=True,
    device_map="auto"
)

# 或使用4-bit量化
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    load_in_4bit=True,
    device_map="auto"
)
```

## 常见问题

### Q1: 模型下载速度慢？

**解决方案**：使用ModelScope镜像（国内用户）

```bash
# 设置HuggingFace镜像
export HF_ENDPOINT=https://hf-mirror.com

# 或使用ModelScope
pip install modelscope
```

### Q2: 显存不足？

**解决方案**：
1. 使用0.6B模型而非1.7B
2. 使用量化（8-bit或4-bit）
3. 减少batch size
4. 使用CPU模式

### Q3: 生成速度慢？

**解决方案**：
1. 使用GPU加速
2. 使用FP16精度
3. 启用CUDA优化
4. 使用更小的模型

### Q4: 音频质量不好？

**解决方案**：
1. 使用1.7B模型
2. 调整temperature参数
3. 提供更详细的音色描述
4. 使用高质量的参考音频

## 更新龙虾电台Skill

现在我们已经知道如何使用Qwen3-TTS，让我更新龙虾电台Skill的代码：

### 1. 更新依赖

```bash
# requirements.txt
torch>=2.0.0
transformers>=4.40.0
accelerate>=0.20.0
huggingface_hub>=0.16.0
modelscope>=1.10.0
```

### 2. 使用Qwen3TTSProvider

```python
# 在generate_radio.py中使用
from providers.qwen3_tts import Qwen3TTSProvider

# 初始化Provider
tts_provider = Qwen3TTSProvider(
    model_name="Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    device="auto",
    use_gpu=True
)

# 检查模型是否可用
if not await tts_provider.check_availability():
    print("模型未下载，正在下载...")
    await tts_provider.download_model()

# 生成音频
audio_data = await tts_provider.synthesize(
    text=content,
    voice_id="xiaoxiao",
    emotion=Emotion.NEUTRAL
)
```

## 参考链接

- **GitHub**: https://github.com/QwenLM/Qwen3-TTS
- **HuggingFace**: https://huggingface.co/collections/Qwen/qwen3-tts
- **ModelScope**: https://modelscope.cn/collections/Qwen/Qwen3-TTS
- **官方博客**: https://qwen.ai/blog?id=qwen3tts-0115
- **在线体验**: 
  - ModelScope: https://modelscope.cn/studios/Qwen/Qwen3-TTS
  - HuggingFace: https://huggingface.co/spaces/Qwen/Qwen3-TTS

---

**注意**: Qwen3-TTS模型较大，首次下载需要一定时间。建议在网络良好的环境下进行下载。
