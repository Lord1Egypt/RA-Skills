# Video Understanding (Local Video Comprehension)

A skill for understanding video content using local AI models, supporting both audio transcription and image understanding.

## Model Installation

### Image Understanding - qwen3-vl:8b

**Windows:**
1. Download Ollama from https://ollama.com/download
2. Install and verify: `ollama --version`

**macOS/Linux:**
```bash
brew install ollama  # or download from ollama.com
```

**Pull the model:**
```bash
ollama pull qwen3-vl:8b
```

### Audio Recognition - FunASR

**Create conda environment:**
```bash
conda create -n asr-local python=3.11
conda activate asr-local
pip install funasr
```

**Note:** The FunASR model will be downloaded automatically on first use.

## Environment Requirements

- ffmpeg (in PATH)
- conda + Python 3.11
- Ollama (running)
- ~6GB VRAM for qwen3-vl:8b

## Troubleshooting

**Ollama not running:**
```bash
ollama serve
```

**FunASR model not found:**
- Models are auto-downloaded on first use
- Ensure internet connection for initial download

**Chinese audio not recognized:**
- FunASR Paraformer model is optimized for Chinese
- For English, consider Whisper via Ollama instead
