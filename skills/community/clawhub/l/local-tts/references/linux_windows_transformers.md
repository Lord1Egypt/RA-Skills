# Linux/Windows qwen-tts Reference

## Overview

The Linux/Windows implementation uses the `qwen-tts` Python library with automatic optimizations:

-  **FlashAttention** - Faster attention computation, reduced memory usage
-  **bfloat16** - Better numerical stability than float16, faster than float32
-  **Auto device selection** - CUDA if available, CPU fallback
-  **Auto mixed precision** - Optimal speed/quality balance

## Installation

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | NVIDIA with 4GB VRAM | NVIDIA with 8GB+ VRAM |
| RAM | 8GB | 16GB+ |
| Disk | 5GB | 10GB |
| Python | 3.8 | 3.10 or 3.12 |

### Step-by-Step Installation

#### 1. Create Virtual Environment

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

#### 2. Install qwen-tts

```bash
pip install qwen-tts
```

This automatically installs compatible versions of:
- `torch`
- `transformers`
- `accelerate`

#### 3. Install FlashAttention (Recommended)

FlashAttention significantly improves speed and reduces memory usage:

```bash
pip install flash-attn --no-build-isolation
```

**Requirements:**
- CUDA 11.6+ or ROCm (AMD GPUs)
- For CUDA 12.x, use PyTorch with CUDA 12.x

**Troubleshooting:**
- If installation fails, the script will still work (just slower)
- On Windows, you may need Visual C++ Build Tools
- On older GPUs (pre-Ampere), FlashAttention v1 will be used

#### 4. Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH

#### 5. Verify Installation

```bash
# Check qwen-tts is installed
qwen-tts --help

# Run wrapper script test
python scripts/tts_linux.py "Hello world" --female
```

## Python API Usage

### Basic TTS with Optimizations

```python
from qwen_tts import Qwen3TTSModel, Qwen3TTSTokenizer
import torch
import soundfile as sf

# Configuration
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"

# Auto device selection
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Auto dtype selection (bfloat16 for Ampere+, float16 for older, float32 for CPU)
if device == "cuda":
    capability = torch.cuda.get_device_capability()
    if capability[0] >= 8:  # Ampere (SM 8.0+) - A100, RTX 30xx, RTX 40xx
        dtype = torch.bfloat16
        print("Using bfloat16 for optimal precision")
    else:  # Older GPUs
        dtype = torch.float16
        print("Using float16")
else:
    dtype = torch.float32
    print("Using float32 for CPU")

# Load model with optimizations
model = Qwen3TTSModel.from_pretrained(
    MODEL_ID,
    torch_dtype=dtype,
    device_map="auto" if device == "cuda" else None,
    attn_implementation="flash_attention_2",  # Enable FlashAttention
)

tokenizer = Qwen3TTSTokenizer.from_pretrained(MODEL_ID)

if device == "cpu":
    model = model.to(device)

# Generate
text = "Hello, this is optimized text-to-speech."
inputs = tokenizer(text, return_tensors="pt").to(device)

with torch.no_grad():
    if device == "cuda":
        # Use automatic mixed precision
        with torch.cuda.amp.autocast(dtype=dtype):
            audio = model.generate(**inputs, voice="Chelsie", language="en")
    else:
        audio = model.generate(**inputs, voice="Chelsie", language="en")

# Save
if isinstance(audio, torch.Tensor):
    audio = audio.cpu().numpy()
sf.write("output.wav", audio, 24000)
```

### CustomVoice with All Parameters

```python
from qwen_tts import Qwen3TTSModel, Qwen3TTSTokenizer
import torch
import soundfile as sf

model_id = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"

# Load with optimizations
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" and torch.cuda.get_device_capability()[0] >= 8 else torch.float16

model = Qwen3TTSModel.from_pretrained(
    model_id,
    torch_dtype=dtype,
    device_map="auto",
    attn_implementation="flash_attention_2",
)
tokenizer = Qwen3TTSTokenizer.from_pretrained(model_id)

text = "Welcome to our service"
inputs = tokenizer(text, return_tensors="pt").to(device)

# Generate with all parameters
with torch.no_grad(), torch.cuda.amp.autocast(dtype=dtype):
    audio = model.generate(
        **inputs,
        voice="Chelsie",        # Preset voice
        language="en-US",       # Language code
        speed=1.2,              # Speaking speed (0.5-2.0)
        pitch=1.0,              # Voice pitch (0.5-2.0)
        temperature=0.7,        # Sampling temperature
        top_p=0.9,              # Top-p sampling
    )

sf.write("output.wav", audio.cpu().numpy(), 24000)
```

### VoiceDesign with bfloat16

```python
from qwen_tts import Qwen3TTSModel, Qwen3TTSTokenizer
import torch
import soundfile as sf

model_id = "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign"

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" and torch.cuda.get_device_capability()[0] >= 8 else torch.float16

model = Qwen3TTSModel.from_pretrained(
    model_id,
    torch_dtype=dtype,
    device_map="auto",
    attn_implementation="flash_attention_2",
)
tokenizer = Qwen3TTSTokenizer.from_pretrained(model_id)

text = "I am your AI assistant"
inputs = tokenizer(text, return_tensors="pt").to(device)

# Generate with voice description
with torch.no_grad(), torch.cuda.amp.autocast(dtype=dtype):
    audio = model.generate(
        **inputs,
        instruct="A professional female voice, calm and authoritative",
        language="en-US"
    )

sf.write("output.wav", audio.cpu().numpy(), 24000)
```

### Voice Cloning

```python
from qwen_tts import Qwen3TTSModel, Qwen3TTSTokenizer
import torch
import soundfile as sf
import librosa

model_id = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" and torch.cuda.get_device_capability()[0] >= 8 else torch.float16

model = Qwen3TTSModel.from_pretrained(
    model_id,
    torch_dtype=dtype,
    device_map="auto",
    attn_implementation="flash_attention_2",
)
tokenizer = Qwen3TTSTokenizer.from_pretrained(model_id)

# Load reference audio
ref_audio, sr = librosa.load("reference.wav", sr=24000)

# Text to synthesize
text = "This is my cloned voice speaking"
inputs = tokenizer(text, return_tensors="pt").to(device)

# Generate with reference
with torch.no_grad(), torch.cuda.amp.autocast(dtype=dtype):
    audio = model.generate(
        **inputs,
        ref_audio=ref_audio,
        ref_text="Reference audio transcript",
        language="en-US"
    )

sf.write("cloned.wav", audio.cpu().numpy(), 24000)
```

## CLI Usage

### Web UI

```bash
# Launch with default optimizations
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-Base --ip 127.0.0.1 --port 8000
```

Access at http://127.0.0.1:8000

### Wrapper Script

```bash
# Basic usage with auto-optimizations
python scripts/tts_linux.py "Hello world" --female

# With custom parameters
python scripts/tts_linux.py "Hello world" \
    --voice Chelsie \
    --speed 1.2 \
    --pitch 1.0 \
    --lang_code en-US

# Voice design
python scripts/tts_linux.py "Hello world" \
    --model voicedesign \
    --instruct "A warm male voice with authority"

# Voice cloning
python scripts/tts_linux.py "Cloned voice text" \
    --ref_audio sample.wav \
    --ref_text "Sample transcript"

# Chinese TTS
python scripts/tts_linux.py "" \
    --voice Aiden \
    --lang_code zh-CN
```

## Optimization Guide

### FlashAttention Benefits

| Metric | Without FlashAttention | With FlashAttention | Improvement |
|--------|----------------------|---------------------|-------------|
| Memory Usage | 100% | ~60% | **40% reduction** |
| Speed | 1.0x | 1.3-2.0x | **30-100% faster** |
| Max Sequence Length | Limited | Extended | **Longer texts** |

### bfloat16 vs float16 vs float32

| Feature | float32 | float16 | bfloat16 |
|---------|---------|---------|----------|
| Memory | 4 bytes | 2 bytes | 2 bytes |
| Speed | Baseline | 2x faster | 2x faster |
| Precision | Best | Good (range issues) | Good (better range) |
| GPU Support | All | Most | Ampere+ (SM 8.0+) |

**Recommendation:**
- **Ampere+ GPUs (A100, RTX 30xx, RTX 40xx):** Use bfloat16
- **Older GPUs:** Use float16
- **CPU:** Use float32

### Device Selection Priority

```python
# Automatic (recommended)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Force CPU
device = "cpu"

# Force specific GPU
device = "cuda:0"
```

### Memory Optimization

If you encounter OOM errors:

1. **Use smaller models:**
   ```python
   model_id = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"  # Instead of 1.7B
   ```

2. **Enable gradient checkpointing (if training):**
   ```python
   model.gradient_checkpointing_enable()
   ```

3. **Use CPU offload:**
   ```python
   model = model.to("cpu")
   # Generate in chunks
   ```

4. **Clear cache between generations:**
   ```python
   torch.cuda.empty_cache()
   ```

## Model Identifiers

### Hugging Face Models

```
Qwen/Qwen3-TTS-12Hz-1.7B-Base
Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign
Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
Qwen/Qwen3-TTS-12Hz-0.6B-Base
Qwen/Qwen3-TTS-12Hz-0.6B-VoiceDesign
Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice
```

## Parameters Reference

### Generation Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `voice` | str | Preset voice name (CustomVoice) | None |
| `instruct` | str | Voice description (VoiceDesign) | None |
| `language` | str | Language code | "en-US" |
| `speed` | float | Speaking speed (0.5-2.0) | 1.0 |
| `pitch` | float | Voice pitch (0.5-2.0) | 1.0 |
| `temperature` | float | Sampling temperature | 0.7 |
| `top_p` | float | Top-p sampling | 0.9 |
| `repetition_penalty` | float | Repetition penalty | 1.0 |
| `ref_audio` | array | Reference audio for cloning | None |
| `ref_text` | str | Reference text for cloning | None |

### Model Loading Parameters

| Parameter | Description | Recommended Value |
|-----------|-------------|-------------------|
| `torch_dtype` | Model precision | `torch.bfloat16` or `torch.float16` |
| `device_map` | Device placement | `"auto"` for CUDA, `None` for manual |
| `attn_implementation` | Attention implementation | `"flash_attention_2"` if available |

### Supported Languages

| Code | Language |
|------|----------|
| "en", "en-US" | English (US) |
| "en-GB" | English (UK) |
| "zh", "zh-CN" | Chinese (Simplified) |
| "zh-TW" | Chinese (Traditional) |
| "ja" | Japanese |
| "ko" | Korean |
| "de" | German |
| "fr" | French |
| "ru" | Russian |
| "pt" | Portuguese |
| "es" | Spanish |
| "it" | Italian |
| "auto" | Auto-detect |

### Preset Voices (CustomVoice)

| Voice | Gender | Description |
|-------|--------|-------------|
| "Chelsie" | Female | Bright, slightly edgy young female |
| "Serena" | Female | English | Warm, gentle young female |
| "Ryan" | Male | Seasoned male voice with low, mellow timbre |
| "Aiden" | Male | Youthful Beijing male voice, clear natural timbre |

Use `model.get_supported_speakers()` to list all available voices.

## Troubleshooting

### FlashAttention Installation Fails

```bash
# Option 1: Skip FlashAttention (script will still work)
pip install qwen-tts

# Option 2: Install from source
pip install flash-attn --no-build-isolation --verbose
```

### CUDA Out of Memory

1. Use smaller models:
   ```python
   model_id = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
   ```

2. Use float16 instead of bfloat16 on older GPUs

3. Close other GPU applications

### Model Download Issues

```bash
# Set Hugging Face cache directory
export HF_HOME=/path/to/cache

# Or use huggingface-cli
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base
```

### Slow Generation

1. **Check CUDA is being used:**
   ```python
   import torch
   print(torch.cuda.is_available())  # Should be True
   ```

2. **Verify FlashAttention:**
   The script prints  if FlashAttention is active

3. **Check dtype:**
   bfloat16/float16 should be 2x faster than float32

### Windows-Specific Issues

1. **Visual C++ Redistributables**: Install if compilation errors occur
2. **PATH issues**: Ensure Python and ffmpeg are in PATH
3. **Long paths**: Enable long path support in Windows

```powershell
# Enable long paths (run as Administrator)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

## Performance Benchmarks

Expected performance on various GPUs (1.7B model, 20 tokens):

| GPU | FlashAttention | dtype | Time | VRAM |
|-----|---------------|-------|------|------|
| RTX 4090 | Yes | bfloat16 | ~0.5s | ~6GB |
| RTX 4090 | No | float16 | ~1.0s | ~8GB |
| RTX 3090 | Yes | bfloat16 | ~0.7s | ~6GB |
| A100 | Yes | bfloat16 | ~0.3s | ~6GB |
| CPU (16 cores) | N/A | float32 | ~10s+ | N/A |

*Times are approximate and vary based on text length and system load.*
