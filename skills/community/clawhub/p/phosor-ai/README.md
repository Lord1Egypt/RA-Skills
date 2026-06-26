# Phosor AI — Agent Skill

Generate AI videos (text-to-video, image-to-video) with optional custom LoRA styles.

## Quick Start

```bash
export PHOSOR_API_KEY="your-key"

# Text-to-Video
python3 scripts/phosor_client.py submit "A cat walking on a beach" --width 854 --height 480

# Image-to-Video (two-step: upload then submit)
python3 scripts/phosor_client.py upload-image photo.jpg
python3 scripts/phosor_client.py submit "The scene comes alive" --image-url "images/img-xxx.jpg"

# With custom LoRA
python3 scripts/phosor_client.py upload-lora high_noise.safetensors low_noise.safetensors
python3 scripts/phosor_client.py submit "A person walking" --lora-id <lora_id>

# Check status / get result
python3 scripts/phosor_client.py status <request_id>
python3 scripts/phosor_client.py result <request_id>
```

## Requirements

- Python 3.7+ (stdlib only, no pip install needed)
- `PHOSOR_API_KEY` environment variable

## Commands

Run `python3 scripts/phosor_client.py --help` for all commands.

## Links

- [Phosor AI](https://phosor.ai)
- [API Documentation](https://phosor.ai/docs)
