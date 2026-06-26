# Poe API Orchestration Skill

**Purpose**: Enable OpenClaw to intelligently query multiple AI models via Poe API  
**Version**: 1.0.0  
**Last Updated**: 2026-03-03

---

## What This Skill Does

This skill provides:

1. **Intelligent Model Selection** - Automatically choose the right AI model for each task
2. **Poe API Integration** - Simple interface to query 300+ AI models
3. **Task-Based Routing** - Route requests to the best model based on task type
4. **Cost Optimization** - Use appropriate models to balance quality and cost

---

## When OpenClaw Should Use This Skill

Use this skill when you need to:

- ✅ Query AI models for text generation, reasoning, or analysis
- ✅ Generate images, videos, or audio
- ✅ Perform web searches with AI assistance
- ✅ Access specialized models for specific tasks
- ✅ Need to choose between multiple AI models

**Do NOT use this skill for**:
- Simple string operations (use built-in functions)
- Local file operations
- System commands

---

## Quick Start

### 1. Read the Model Selection Guide

**CRITICAL**: Before using this skill, read:

```
MODEL_SELECTION_GUIDE.md
```

This guide teaches you:
- Which model to use for each task type
- When to use Claude, GPT, Gemini, or other models
- How to balance quality, speed, and cost

### 2. Use the Client

```python
from skills.poe_api.scripts.poe_client import PoeClient

# Initialize
client = PoeClient()

# Simple query (auto-selects best model)
result = client.query_for_task(
    task_type="programming",
    message="Write a Python function to sort a list"
)

# Specific model
result = client.query("claude-sonnet-4.6", "Your prompt")

# Web search
result = client.web_search("Latest AI developments")

# Generate image
result = client.generate_image("A sunset over mountains")

# Generate video
result = client.generate_video("A cat playing piano")
```

---

## Task Types and Model Selection

### **Text/Reasoning Tasks**

| Task Type | Primary Model | When to Use |
|-----------|---------------|-------------|
| **Programming** | claude-sonnet-4.6 | General coding, algorithms |
| **Complex Problems** | claude-opus-4.6 | Deep reasoning, architecture |
| **Fast/Cheap** | claude-haiku-4.5 | Quick tasks, simple code |
| **Huge Context** | gemini-3.1-pro | >200K tokens, design systems |
| **Code-Focused** | gpt-5.3-codex | Debugging, code completion |
| **UI/UX Design** | gemini-3.1-pro | Design systems, UX research |
| **Requirements** | claude-sonnet-4.6 | Gathering, analysis |
| **Data Analysis** | claude-sonnet-4.6 | Data interpretation |

### **Web Search Tasks**

| Task Type | Model | When to Use |
|-----------|-------|-------------|
| **Simple Search** | perplexity-search | Quick lookups |
| **Complex Queries** | perplexity-sonar-pro | In-depth research |
| **Reasoning + Search** | perplexity-sonar-rsn-pro | Analysis with sources |
| **Deep Research** | o3-deep-research | Extensive research |
| **Budget Research** | o4-mini-deep-research | Cost-conscious |

### **Image Generation**

| Task Type | Model | When to Use |
|-----------|-------|-------------|
| **Best Quality** | imagen-4-ultra | Professional graphics |
| **Fast + Good** | nano-banana-2 | Quick iterations |
| **Text in Images** | nano-banana-pro | Banners, signs |
| **General Purpose** | nano-banana | Standard generation |
| **Professional Editing** | gpt-image-1.5 | Complex edits |
| **Asian Aesthetics** | seedream-4.0 | Specific style |

### **Video Generation**

| Task Type | Model | When to Use |
|-----------|-------|-------------|
| **Best + Audio** | veo-3.1 | Cinematic with sound |
| **Cinematic** | sora-2-pro | High-fidelity |
| **Versatile** | kling-o3 | Multiple workflows |
| **Standard** | sora-2 | Good quality |
| **Storytelling** | wan-2.6 | Multi-scene |
| **Fast** | seedance-1.0-pro | Quick generation |

### **Audio Generation**

| Task Type | Model | When to Use |
|-----------|-------|-------------|
| **Realistic Speech** | elevenlabs-v3 | Audiobooks, podcasts |
| **Fast TTS** | gemini-2.5-flash-tts | Quick conversion |
| **Controlled Speech** | hailuo-speech-02 | Fine-grained control |
| **Music** | hailuo-music-v1.5 | Song generation |

---

## Key Principles

### 1. **Read MODEL_SELECTION_GUIDE.md First**

This guide contains:
- Detailed decision trees
- Model capabilities and strengths
- When to use each model
- Cost/quality tradeoffs

### 2. **Default to claude-sonnet-4.6**

When in doubt, use `claude-sonnet-4.6`:
- Best all-around performance
- 983K token context
- Excellent at most tasks
- Good balance of speed and quality

### 3. **Use Task-Based Methods**

Instead of manually selecting models, use:

```python
# Automatic model selection
client.query_for_task(task_type="programming", message="...")
client.query_for_task(task_type="ui_design", message="...")
client.query_for_task(task_type="data_analysis", message="...")
```

### 4. **Consider Context Size**

- **< 200K tokens**: Claude-Sonnet, Claude-Opus, GPT models
- **> 200K tokens**: Gemini-3.1-Pro (1M context)

### 5. **Balance Quality vs Speed**

- **Highest Quality**: claude-opus-4.6, imagen-4-ultra, veo-3.1
- **Balanced**: claude-sonnet-4.6, nano-banana-2
- **Fast/Cheap**: claude-haiku-4.5, perplexity-search

---

## Model Capabilities

### **Text Models**

#### **Claude Family (Anthropic)**
- **claude-opus-4.6**: 983K context, deepest reasoning
- **claude-sonnet-4.6**: 983K context, best all-around
- **claude-haiku-4.5**: 192K context, fastest

**Strengths**:
- Excellent reasoning and coding
- Great at following complex instructions
- Strong safety and reliability
- Very large context windows

#### **GPT Family (OpenAI)**
- **gpt-5.3-codex**: 400K context, code-focused
- **gpt-5.2**: 400K context, general purpose

**Strengths**:
- Great at code completion
- Good instruction following
- Large context

#### **Gemini Family (Google)**
- **gemini-3.1-pro**: **1M context**, multimodal

**Strengths**:
- Massive 1M token context
- Multimodal input (text, image, video, audio)
- Great for design systems

### **Search Models (Perplexity)**
- **perplexity-search**: Simple web search
- **perplexity-sonar-pro**: Complex queries with citations
- **perplexity-sonar-rsn-pro**: Reasoning + search

**Strengths**:
- Real-time web access
- Citations included
- Great for research

### **Image Models**
- **imagen-4-ultra**: Best quality
- **nano-banana-2**: Latest, fast, 4K
- **gpt-image-1.5**: Professional editing

### **Video Models**
- **veo-3.1**: Best quality + native audio
- **sora-2-pro**: Cinematic (OpenAI)
- **kling-o3**: Most versatile (4 workflows)

### **Audio Models**
- **elevenlabs-v3**: Most realistic speech
- **hailuo-music-v1.5**: Music generation

---

## Common Use Cases

### **Programming Tasks**

```python
# General coding
result = client.query_for_task(
    task_type="programming",
    message="Write a REST API in Python"
)

# Code review
result = client.query_for_task(
    task_type="programming",
    message=f"Review this code: {code}"
)

# Debugging
result = client.query_for_task(
    task_type="programming",
    message=f"Debug this error: {error}"
)
```

### **UI/UX Design**

```python
# Design system
result = client.query_for_task(
    task_type="ui_design",
    message="Create a design system for a fintech app"
)

# User research
result = client.query_for_task(
    task_type="ui_design",
    message="Analyze user flow for checkout process"
)
```

### **Data Analysis**

```python
# Analyze data
result = client.query_for_task(
    task_type="data_analysis",
    message=f"Analyze this dataset: {data}"
)

# Generate insights
result = client.query_for_task(
    task_type="data_analysis",
    message="What trends do you see in this data?"
)
```

### **Web Search**

```python
# Quick search
result = client.web_search("Latest AI developments 2026")

# Deep research
result = client.deep_search(
    "Impact of AI on job markets",
    model="o3-deep-research"
)
```

### **Content Creation**

```python
# Generate image
result = client.generate_image(
    "Modern dashboard UI with dark theme"
)

# Generate video
result = client.generate_video(
    "A drone shot of city skyline at sunset"
)

# Generate audio
result = client.generate_audio(
    "[whispers] Welcome to our podcast",
    voice_model="elevenlabs-v3"
)
```

---

## Decision Framework

### **Step 1: Identify Task Type**

Ask yourself:
- Is this programming? → `programming`
- Is this design? → `ui_design`
- Is this analysis? → `data_analysis`
- Is this search? → `web_search`
- Is this creative? → `image/video/audio`

### **Step 2: Check Context Size**

- **< 200K tokens**: Any Claude/GPT model
- **> 200K tokens**: Must use `gemini-3.1-pro`

### **Step 3: Balance Quality vs Speed**

- **Need best quality?** → Use Pro/Ultra models
- **Need fast?** → Use Haiku/Flash models
- **Need balanced?** → Use Sonnet/Standard models

### **Step 4: Use Task-Based Methods**

```python
# Let the skill choose the model
result = client.query_for_task(
    task_type="programming",
    message="Your task",
    complexity="medium"  # low, medium, high
)
```

---

## Important Notes

### **Token Limits**
- **Managed by Poe API** - No need to specify
- Different models have different limits
- Poe will automatically handle limits

### **Cost Management**
- Use `max_calls_per_task` to limit API calls
- Use cheaper models for simple tasks
- Reserve expensive models for complex work

### **Error Handling**
- Always check `result["success"]`
- Implement retry logic
- Use fallback models if primary fails

---

## Examples

See `examples/` directory for:
- Basic usage examples
- Advanced workflows
- Error handling patterns
- Multi-step tasks

---

## Troubleshooting

### **Model Not Available**
```
Error: Model not found
```
**Solution**: Model names are case-sensitive. Use lowercase:
- ✅ `claude-sonnet-4.6`
- ❌ `Claude-Sonnet-4.6`

### **Rate Limited**
```
Error: Rate limit exceeded
```
**Solution**: Wait and retry, or use fallback model

### **Context Too Large**
```
Error: Context exceeds limit
```
**Solution**: Use `gemini-3.1-pro` (1M context)

---

## Next Steps

1. ✅ Read `MODEL_SELECTION_GUIDE.md` for detailed model information
2. ✅ Check `examples/` for usage patterns
3. ✅ Use `query_for_task()` for automatic model selection
4. ✅ When in doubt, use `claude-sonnet-4.6`

---

**Remember**: The key to using this skill effectively is understanding which model to use for which task. Read `MODEL_SELECTION_GUIDE.md` carefully! 🎯
