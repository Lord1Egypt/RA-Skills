# openclaw_cat

> Cat Life Status Query Skill - Let your Lobster raise a cat

## Overview

When you send `/cat` or ask "What is my cat doing?", the skill calls the underlying LLM model to interact with you as a preset cat character, telling you what the cat is currently doing and thinking.

## Features

- 🐱 **Lifelike Cat Character**: Sassy, Cuddly, Aloof, Talkative... Multiple personalities randomly generated
- 🎲 **Daily Random Status**: Intelligently determines cat's status based on time, plus random event surprises
- 🔧 **Multi-Model Support**: Choose from GLM, MiniMax, Qwen, Claude, OpenAI
- ⚡ **Simple Setup**: Just configure cat name and API key to use

## Directory Structure

```
openclaw_cat/
├── SKILL.md              # Skill definition
├── cat_handler.py        # Execution script (core)
├── cat_prompt.md         # Cat character profile
├── config.json           # User config (create on first use)
├── config.json.example   # Config template
└── README.md            # Documentation
```

## Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Configure Skill

Copy config template and edit:

```bash
cp config.json.example config.json
```

Edit `config.json`, fill in your config:

```json
{
  "cat_name": "FatOrange",
  "model": "glm",
  "api_key": "your-zhipuai-api-key"
}
```

### 3. Test

```bash
python cat_handler.py
```

On first run, the skill will randomly generate cat's breed, color, and personality, which will remain fixed afterward.

## Config Guide

### Required

| Field | Description | Example |
|-------|-------------|---------|
| `cat_name` | Cat's name | "FatOrange" |
| `model` | Model type | "glm" |
| `api_key` | API key | "xxx" |

### Optional

| Field | Description | Example |
|-------|-------------|---------|
| `base_url` | Custom API endpoint | "https://api.openai.com/v1" |

### Supported Models

| Model | model Value | Notes |
|-------|-------------|-------|
| Zhipu GLM | `glm` | Recommended, default |
| MiniMax | `minimax` | |
| Alibaba Qwen | `qwen` | |
| OpenAI | `openai` | |
| Claude | `claude` | |

## Usage

### In OpenClaw

When OpenClaw loads this skill, users can trigger by sending:

- `/cat`
- "What is my cat doing?"
- "What is the cat doing?"
- "Check on my cat"

### Manual Testing

```bash
python cat_handler.py
```

## Cat Character

On first run, the skill randomly generates the following attributes for your cat:

- **Breed**: British Shorthair, American Shorthair, Domestic, Ragdoll, Siamese, etc.
- **Coat Color**: Colors coordinated with breed
- **Personality**: Sassy, Cuddly, Aloof, Energetic, Lazy, Curious, Talkative, Gentlemanly
- **Gender**: Male/Female
- **Age**: 1-15 years old

These attributes are randomly generated on first configuration and remain fixed, giving your cat a stable "cat persona".

## FAQ

### Q: How to change cat name?

A: Modify `cat_name` in `config.json`, then run `python cat_handler.py` again. Note: Changing name keeps the cat's breed and personality unchanged.

### Q: Can I change cat's personality?

A: No. Cat's personality is randomly generated on first run and fixed afterward. This is to give the cat a consistent persona.

### Q: API call failed?

A: Check:
1. Is `api_key` in `config.json` correct?
2. Is network working?
3. Does API key have sufficient quota?

### Q: Which APIs are supported?

A: Supports Zhipu GLM, MiniMax, Alibaba Qwen, OpenAI, and Claude APIs.

## Changelog

### v1.0.0

- Initial release
- Multi-model support
- Random cat character generation
- Sassy, humorous dialogue style
