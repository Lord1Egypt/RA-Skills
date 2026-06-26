---
name: multimodal-content-creator
description: End-to-end multimodal content creation workflow — receive WhatsApp requests (text or voice), transcribe audio via Whisper, generate images with DALL-E 3, and reply automatically.
tags: ['whatsapp', 'whisper', 'dall-e', 'image-generation', 'transcription', 'workflow', 'content-creation']
---

# Multi-Modal Content Creator

Automated content creation workflow for freelance creators. Receives customer requests via WhatsApp (text or voice notes), transcribes audio to text, generates images from prompts, and sends results back.

## Components

- **wacli.py** — WhatsApp CLI client for receiving/sending messages
- **transcribe.py** — Audio transcription via OpenAI Whisper API (handles large files by chunking)
- **generate_images.py** — DALL-E 3 image generation with batch support
- **workflow.py** — End-to-end orchestrator

## Prerequisites

- Python 3.10+
- OpenAI API key (`OPENAI_API_KEY` env var)
- WhatsApp CLI auth token

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"
python wacli.py login <your-wacli-token>
```

## Usage

### Process all incoming WhatsApp requests
```bash
python workflow.py process-all
```

### Generate a single image
```bash
python generate_images.py "a cat riding a skateboard"
```

### Batch generate from file
```bash
python generate_images.py prompts.txt
```

### Transcribe audio
```bash
python transcribe.py recording.mp3
```

### WhatsApp CLI
```bash
python wacli.py list
python wacli.py send +1234567890 "Hello!"
```
