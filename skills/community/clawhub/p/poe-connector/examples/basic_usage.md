# Poe Connector — Usage Examples

## Setup

```bash
# Install dependency
pip install openai

# Set your API key (get one at https://poe.com/api/keys)
export POE_API_KEY="your-key-here"
```

---

## Text Chat

### Simple question

```bash
python3 src/poe_chat.py --model Claude-Sonnet-4 --message "What is the capital of France?"
```

### With a system prompt

```bash
python3 src/poe_chat.py --model GPT-5.2 \
  --system "You are a helpful cooking assistant who gives concise recipes." \
  --message "How do I make pasta carbonara?"
```

### Streaming output

```bash
python3 src/poe_chat.py --model Gemini-3-Pro \
  --message "Write a short story about a robot learning to paint" \
  --stream
```

### Multi-turn conversation

```bash
python3 src/poe_chat.py --model Claude-Sonnet-4 \
  --messages '[
    {"role": "user", "content": "My name is Alice."},
    {"role": "assistant", "content": "Nice to meet you, Alice!"},
    {"role": "user", "content": "What is my name?"}
  ]'
```

### With custom parameters (extended thinking)

```bash
python3 src/poe_chat.py --model Claude-Sonnet-4 \
  --message "Solve this complex math problem step by step: ..." \
  --extra '{"thinking_budget": 20000}'
```

### With temperature control

```bash
python3 src/poe_chat.py --model GPT-5.2 \
  --message "Write a creative poem about the moon" \
  --temperature 1.5
```

---

## File Analysis

### Describe an image

```bash
python3 src/poe_chat.py --model Claude-Sonnet-4 \
  --message "What do you see in this image?" \
  --files photo.jpg
```

### Summarize a PDF

```bash
python3 src/poe_chat.py --model GPT-5.2 \
  --message "Summarize the key points of this document" \
  --files report.pdf
```

### Compare multiple images

```bash
python3 src/poe_chat.py --model Claude-Sonnet-4 \
  --message "Compare these two images and describe the differences" \
  --files before.png after.png
```

---

## Image Generation

### Basic image

```bash
python3 src/poe_media.py --type image \
  --prompt "A serene Japanese garden in autumn with a red bridge"
```

### With specific model and aspect ratio

```bash
python3 src/poe_media.py --type image \
  --model Imagen-4 \
  --prompt "Cyberpunk cityscape at night, neon lights" \
  --aspect 16:9 --quality high
```

### Save to specific path

```bash
python3 src/poe_media.py --type image \
  --model GPT-Image-1 \
  --prompt "A minimalist logo for a coffee shop called 'Bean There'" \
  --output logo.png
```

---

## Video Generation

```bash
python3 src/poe_media.py --type video \
  --model Veo-3 \
  --prompt "A timelapse of a flower blooming in a sunlit meadow"
```

---

## Audio / TTS

```bash
python3 src/poe_media.py --type audio \
  --model ElevenLabs \
  --prompt "Welcome to Poe Connector. This is a demonstration of text-to-speech capabilities."
```

---

## Model Discovery

### List all models

```bash
python3 src/poe_models.py --list
```

### Search for Claude models

```bash
python3 src/poe_models.py --search "claude"
```

### Search for image generation models

```bash
python3 src/poe_models.py --search "image"
```

### Get info on a specific model

```bash
python3 src/poe_models.py --info "Claude-Sonnet-4"
```

### Output as JSON (for programmatic use)

```bash
python3 src/poe_models.py --list --json
```
