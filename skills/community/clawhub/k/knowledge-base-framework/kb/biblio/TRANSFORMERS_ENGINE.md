# TransformersEngine

Hugging Face Transformers Integration for kb-framework LLM module.

## Overview

The `TransformersEngine` provides local inference using Hugging Face Transformers models.
Unlike `OllamaEngine` which requires a separate server, TransformersEngine loads models
directly into memory and runs inference locally.

## Features

- **Local Inference**: Run models locally without external dependencies
- **Quantization Support**: 8-bit and 4-bit quantization via `bitsandbytes`
- **Auto-Device Detection**: Automatically uses CUDA, MPS (Apple Silicon), or CPU
- **Memory Management**: Automatic model loading/unloading with cache clearing
- **Streaming**: Token-by-token generation for real-time output
- **Batch Processing**: Process multiple prompts efficiently

## Requirements

```bash
# Core dependencies
pip install torch transformers

# Optional: For quantization
pip install bitsandbytes

# Optional: For better memory management
pip install accelerate
```

## Configuration

```python
from kb.biblio.config import LLMConfig

config = LLMConfig(
    model_source="huggingface",
    hf_model_name="microsoft/Phi-3-mini-4k-instruct",
    hf_device="auto",  # auto, cpu, cuda, mps
    hf_quantization=None,  # None, "8bit", "4bit"
    hf_temperature=0.7,
    hf_max_tokens=2048,
)
```

## Usage

```python
from kb.biblio.engine.factory import EngineFactory

# Create engine
factory = EngineFactory()
engine = factory.create_engine("huggingface")

# Load model
engine.load_model()

# Generate response
response = engine.generate("What is the capital of France?")
print(response.content)

# Unload to free memory
engine.unload_model()
```

## Model Recommendations

| Model | Size | VRAM (FP16) | VRAM (8-bit) | VRAM (4-bit) |
|-------|------|-------------|--------------|--------------|
| microsoft/Phi-3-mini-4k-instruct | 3.8B | ~8 GB | ~5 GB | ~3 GB |
| meta-llama/Llama-3.2-3B-Instruct | 3B | ~6 GB | ~4 GB | ~2.5 GB |
| TinyLlama/TinyLlama-1.1B-Chat-v1.0 | 1.1B | ~2.5 GB | ~1.5 GB | ~1 GB |

## Quantization

Quantization reduces memory usage at the cost of some accuracy:

```python
# 8-bit quantization (recommended)
config = LLMConfig(
    model_source="huggingface",
    hf_model_name="microsoft/Phi-3-mini-4k-instruct",
    hf_quantization="8bit",
)

# 4-bit quantization (lowest memory)
config = LLMConfig(
    model_source="huggingface",
    hf_model_name="microsoft/Phi-3-mini-4k-instruct",
    hf_quantization="4bit",
)
```

## Troubleshooting

### CUDA Out of Memory

```python
# Clear cache and retry
engine.unload_model()
import torch
torch.cuda.empty_cache()
```

### Model Not Loading

```python
# Check availability
if engine.is_available():
    engine.load_model()
else:
    print("Dependencies missing. Install: pip install torch transformers")
```

### Slow Inference on CPU

- Use smaller models (TinyLlama, Phi-3-mini)
- Enable 8-bit or 4-bit quantization
- Consider using OllamaEngine with remote GPU

## Architecture

```
┌─────────────────────────────────────┐
│        TransformersEngine            │
├─────────────────────────────────────┤
│  - Model loading/caching            │
│  - Quantization handling            │
│  - Device management                │
│  - Token streaming                  │
└─────────────────────────────────────┘
│
▼
┌─────────────────────────────────────┐
│    transformers.AutoModelForCausalLM │
├─────────────────────────────────────┤
│  - torch.nn.Module                  │
│  - HuggingFace implementation       │
└─────────────────────────────────────┘
```

## API Reference

### TransformersEngine

```python
class TransformersEngine(BaseEngine):
    def __init__(self, config: LLMConfig)
    def is_available() -> bool
    def load_model() -> None
    def unload_model() -> None
    def generate(prompt: str, **kwargs) -> LLMResponse
    def generate_async(prompt: str, **kwargs) -> LLMResponse
    def generate_stream(prompt: str, **kwargs) -> Iterator[str]
    def generate_stream_async(prompt: str, **kwargs) -> AsyncIterator[str]
```

## See Also

- `ollama_engine.py` - For remote API-based inference
- `base.py` - Base engine interface
- `factory.py` - Engine creation factory