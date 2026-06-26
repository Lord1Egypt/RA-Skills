# Poe API Orchestration Skill

**Intelligent AI model selection for OpenClaw**

---

## Overview

This skill enables OpenClaw to intelligently query 300+ AI models via the Poe API, automatically selecting the best model for each task type.

## Features

- ✅ **Intelligent Model Selection** - Automatically choose the right AI model
- ✅ **Task-Based Routing** - Programming, design, analysis, search, creative
- ✅ **Simple API** - Easy to use for other OpenClaw bots
- ✅ **Cost Optimized** - Balance quality, speed, and cost
- ✅ **300+ Models** - Access to Claude, GPT, Gemini, and more

---

## Quick Start

### 1. Read the Model Selection Guide

**IMPORTANT**: Before using this skill, read:

```
MODEL_SELECTION_GUIDE.md
```

This guide teaches you which model to use for each task.

### 2. Set API Key

```bash
export POE_API_KEY="your_api_key_here"
```

**⚠️ NEVER hardcode API keys in any file!**

### 3. Use the Client

```python
from skills.poe_api.scripts.poe_client import PoeClient

# Initialize
client = PoeClient()

# Auto-select model
result = client.query_for_task(
    task_type="programming",
    message="Write a Python function"
)

# Specific model
result = client.query("claude-sonnet-4.6", "Your prompt")

# Convenience methods
code = client.programming("Write a function")  # Programming
design = client.ui_design("Design a dashboard")  # UI/UX
analysis = client.data_analysis("Analyze this data")  # Analysis
search = client.web_search("Latest AI news")  # Search
img = client.generate_image("A sunset")  # Image
vid = client.generate_video("City skyline")  # Video
audio = client.generate_audio("Welcome")  # Audio
```

---

## Task Types

### **Programming / Coding**
- **Simple**: `claude-haiku-4.5` (fastest)
- **Medium**: `claude-sonnet-4.6` (balanced) ⭐
- **Complex**: `claude-opus-4.6` (deepest reasoning)
- **Huge Context**: `gemini-3.1-pro` (1M tokens)
- **Code-Focused**: `gpt-5.3-codex`

### **UI/UX Design**
- **Default**: `gemini-3.1-pro` (1M context for design systems) ⭐
- **Fast**: `claude-haiku-4.5`
- **Components**: `claude-sonnet-4.6`

### **Data Analysis**
- **Default**: `claude-sonnet-4.6` ⭐
- **Huge Data**: `gemini-3.1-pro`
- **Complex**: `claude-opus-4.6`

### **Requirement Analysis**
- **Default**: `claude-sonnet-4.6` ⭐
- **Complex**: `claude-opus-4.6`
- **Huge Docs**: `gemini-3.1-pro`

### **Web Search**
- **Simple**: `perplexity-search`
- **Complex**: `perplexity-sonar-pro` ⭐
- **Reasoning**: `perplexity-sonar-rsn-pro`
- **Deep**: `o3-deep-research`
- **Budget**: `o4-mini-deep-research`

### **Image Generation**
- **Best Quality**: `imagen-4-ultra`
- **Fast + Good**: `nano-banana-2` ⭐
- **Text in Images**: `nano-banana-pro`
- **General**: `nano-banana`
- **Editing**: `gpt-image-1.5`

### **Video Generation**
- **Best + Audio**: `veo-3.1` ⭐
- **Cinematic**: `sora-2-pro`
- **Versatile**: `kling-o3`
- **Standard**: `sora-2`
- **Storytelling**: `wan-2.6`

### **Audio Generation**
- **Realistic Speech**: `elevenlabs-v3` ⭐
- **Fast TTS**: `gemini-2.5-flash-tts`
- **Controlled**: `hailuo-speech-02`
- **Music**: `hailuo-music-v1.5`

---

## Usage Examples

### **Programming**

```python
# Simple task
result = client.programming("Sort this list: [3, 1, 2]", complexity="simple")

# Medium task (default)
result = client.programming("Write a REST API", complexity="medium")

# Complex task
result = client.programming("Design microservices architecture", complexity="complex")
```

### **UI/UX Design**

```python
# Design system
result = client.ui_design("Create a design system for fintech app")

# User flow
result = client.ui_design("Design checkout flow for e-commerce")
```

### **Data Analysis**

```python
# Analyze data
result = client.data_analysis(f"Analyze trends in: {data}")

# Generate insights
result = client.data_analysis("What patterns do you see?")
```

### **Web Search**

```python
# Simple search
result = client.web_search("Latest AI news", search_type="simple")

# Complex search
result = client.web_search("Compare quantum computers", search_type="complex")

# Deep research
result = client.web_search("AI impact on jobs", search_type="deep")
```

### **Creative Tasks**

```python
# Image
result = client.generate_image("Modern dashboard UI", quality="fast")

# Video
result = client.generate_video("City sunset", style="cinematic")

# Audio
result = client.generate_audio("Welcome to our app", audio_type="speech")
```

---

## Model Selection Guide

### **When to Use Which Model**

**Read `MODEL_SELECTION_GUIDE.md` for detailed guidance!**

### **Quick Rules**

1. **Default**: Use `claude-sonnet-4.6`
2. **Huge Context (>200K)**: Use `gemini-3.1-pro`
3. **Fast/Cheap**: Use `claude-haiku-4.5`
4. **Complex**: Use `claude-opus-4.6`
5. **Search**: Use Perplexity models
6. **Creative**: Use specialized models

---

## API Reference

### **PoeClient**

```python
class PoeClient:
    def __init__(self, config: Optional[PoeConfig] = None)
    
    # Core methods
    def query(model: str, message: str, context: Optional[str] = None) -> Dict
    def query_for_task(task_type: str, message: str, complexity: str = "medium") -> Dict
    
    # Convenience methods
    def programming(task: str, complexity: str = "medium") -> str
    def ui_design(task: str) -> str
    def data_analysis(task: str) -> str
    def web_search(query: str, search_type: str = "complex") -> str
    def generate_image(prompt: str, quality: str = "fast") -> str
    def generate_video(prompt: str, style: str = "best") -> str
    def generate_audio(text: str, audio_type: str = "speech") -> str
```

### **Quick Functions**

```python
# Quick one-liners
from poe_client import code, design, analyze, search, image, video, audio

result = code("Write a function")  # Programming
result = design("Create UI")  # UI/UX
result = analyze("Analyze data")  # Analysis
result = search("AI news")  # Web search
result = image("Sunset")  # Image
result = video("City")  # Video
result = audio("Welcome")  # Audio
```

---

## Important Notes

### **Token Limits**
- Managed automatically by Poe API
- No need to specify `max_tokens`
- Different models have different limits

### **Cost Management**
- Use `max_calls_per_task` to limit calls
- Use cheaper models for simple tasks
- Reserve expensive models for complex work

### **Error Handling**
- Always check `result["success"]`
- Implement retry logic
- Use fallback models

---

## Files

- **SKILL.md** - Skill documentation (read this first!)
- **MODEL_SELECTION_GUIDE.md** - Detailed model selection guide (READ THIS!)
- **scripts/poe_client.py** - Client implementation
- **examples/** - Usage examples

---

## Requirements

```
openai>=1.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Security

**⚠️ NEVER hardcode API keys in any file!**

Always use environment variables:
```bash
export POE_API_KEY="your_key_here"
```

See `.env.example` for template.

---

## License

MIT

---

## Support

For questions, read:
1. `SKILL.md` - Skill documentation
2. `MODEL_SELECTION_GUIDE.md` - Model selection guide
3. Check examples in `examples/` directory

---

**Remember**: Read `MODEL_SELECTION_GUIDE.md` to learn which model to use for each task! 🎯
