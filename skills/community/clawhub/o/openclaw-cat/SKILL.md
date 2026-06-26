---
name: openclaw_cat
description: "Cat Life Status Query Skill. Triggers when you send /cat command or ask about your cat. The skill calls the underlying LLM model to interact with you as a sassy and funny cat, telling you what the cat is doing and thinking. For OpenClaw deployment environments."
license: MIT
---

# 🦞 openclaw_cat - Let Your Lobster Raise a Cat

> Mr. Lobster, you should go check on your cat.

## What is This Skill?

Imagine you are a lobster 🦞 living at the bottom of the ocean, and one day you decide to adopt a cat 🐱. This cat has a sassy, humorous personality and lives life on its own terms.

When you ask "What is my cat doing?", the skill calls the LLM to respond as the cat, telling you:
- What the cat is doing right now
- What the cat is thinking
- How the cat feels

## Example

```
You: /cat

🦞Lobster's Cat: Hmph, foolish human—no wait, foolish lobster! This majesty is currently lying comfortably on your lobster shell bed, enjoying the sunlight. Only because you prepare little fish treats for me every day will I allow you to witness my supreme beauty! 🐱
```

## Initial Setup

### 1. Copy Config Template

```bash
cp config.json.example config.json
```

### 2. Edit Config

```json
{
  "cat_name": "Your cat's name",
  "model": "glm",
  "model_name": "glm-4-flash",
  "api_key": "Your API key",
  "base_url": ""
}
```

### 3. Config Guide

| Field | Required | Description |
|-------|:--------:|-------------|
| `cat_name` | ✅ | Name for your adopted cat |
| `model` | ✅ | Model type: `glm` / `minimax` / `qwen` / `openai` / `claude` |
| `model_name` | ❌ | Model name, see default values below |
| `api_key` | ✅ | API key for the model |
| `base_url` | ❌ | Custom API endpoint |

### Supported Models

| Model | model default | model_name default |
|-------|------------|-----------------|
| Zhipu GLM | `glm` | `glm-4-flash` |
| MiniMax | `minimax` | `MiniMax-Text-01` |
| Alibaba Qwen | `qwen` | `qwen-turbo` |
| OpenAI | `openai` | `gpt-4o-mini` |
| Claude | `claude` | `claude-sonnet-4-20250514` |

## Usage

### In OpenClaw

Send any of these commands to trigger:

- `/cat`
- "What is my cat doing?"
- "What is the cat doing?"
- "Check on my cat"

### Manual Testing

```bash
python cat_handler.py
```

## Cat Character Profile

On first run, the skill randomly generates for your cat:

- **Breed**: British Shorthair, American Shorthair, Ragdoll, Siamese, Chinese Domestic Cat...
- **Coat Color**: Colors matching the breed
- **Personality**: Sassy, Cuddly, Aloof, Energetic, Lazy, Curious, Talkative, Gentlemanly
- **Gender**: Male/Female
- **Age**: 1-15 years old

These attributes are randomly generated on first run and remain fixed, giving the cat a consistent "cat persona".

## Cat Speaking Style

- Self-refer as "This Majesty", "This Prince/Lady"
- Sassy expressions: "Hmph", "It's not because I want to..."
- Humorous narcissism: Believes being the best cat in the world
- Teases the lobster: Right, you're a lobster, not a human

## File Structure

```
openclaw_cat/
├── SKILL.md              # Skill definition
├── cat_handler.py        # Execution script
├── cat_prompt.md         # Cat character profile
├── config.json           # User config
├── config.json.example   # Config template
└── README.md            # Documentation
```

## Dependencies

```bash
pip install requests
```

## Notes

- API keys need to be obtained from the respective platforms
- Ensure sufficient API quota
- After initial setup, cat attributes are saved in `.cat_cache.json`
