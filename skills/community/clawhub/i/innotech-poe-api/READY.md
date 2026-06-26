# 🎯 Poe API Orchestration Skill - Ready!

**Status**: ✅ Complete  
**Version**: 2.0.0  
**Date**: 2026-03-03

---

## ✅ What's Been Created

### **Core Files**

1. **SKILL.md** - Main skill documentation
   - When to use this skill
   - Quick start guide
   - Task types overview
   - Key principles

2. **MODEL_SELECTION_GUIDE.md** - Comprehensive model guide
   - 28 models analyzed across 5 categories
   - When to use each model
   - Decision trees
   - Best practices
   - Common mistakes to avoid

3. **scripts/poe_client.py** - Client implementation
   - Simple API
   - Task-based model selection
   - Convenience methods
   - Error handling

4. **README.md** - User guide
   - Overview
   - Quick start
   - Examples
   - API reference

5. **skill.json** - Metadata
6. **.env.example** - Configuration template (NO SECRETS!)
7. **requirements.txt** - Dependencies

### **Examples**

1. **examples/basic_usage.py** - Common usage patterns
2. **examples/model_selection.py** - Model selection logic

---

## 📊 Model Categories Covered

### **Text/Reasoning** (5 models)
- claude-opus-4.6 (deepest reasoning)
- claude-sonnet-4.6 (best all-around) ⭐
- claude-haiku-4.5 (fastest)
- gemini-3.1-pro (1M context)
- gpt-5.3-codex (code-focused)

### **Web Search** (5 models)
- perplexity-search (simple)
- perplexity-sonar-pro (complex)
- perplexity-sonar-rsn-pro (reasoning)
- o3-deep-research (extensive)
- o4-mini-deep-research (budget)

### **Image Generation** (6 models)
- imagen-4-ultra (best quality)
- nano-banana-2 (latest + fast) ⭐
- nano-banana-pro (text in images)
- nano-banana (general)
- gpt-image-1.5 (editing)
- seedream-4.0 (Asian style)

### **Video Generation** (8 models)
- veo-3.1 (best + audio) ⭐
- sora-2-pro (cinematic)
- kling-o3 (versatile)
- sora-2 (standard)
- wan-2.6 (storytelling)
- kling-v3-pro (professional)
- seedance-1.0-pro (fast)
- kling-v3 (budget)

### **Audio Generation** (4 models)
- elevenlabs-v3 (realistic speech) ⭐
- gemini-2.5-flash-tts (fast)
- hailuo-speech-02 (controlled)
- hailuo-music-v1.5 (music)

---

## 🎯 Key Features

### **1. Intelligent Model Selection**
- Automatic based on task type
- Considers complexity
- Balances quality vs speed

### **2. Simple API**
```python
from poe_client import PoeClient

client = PoeClient()

# Auto-select
result = client.query_for_task("programming", "Write code")

# Convenience methods
code = client.programming("Write function")
design = client.ui_design("Create UI")
search = client.web_search("AI news")
img = client.generate_image("Sunset")
```

### **3. No Hard-coded Limits**
- Token limits from Poe API
- No secrets in files
- Environment variables only

### **4. Comprehensive Documentation**
- Decision trees
- Model capabilities
- Best practices
- Common mistakes

---

## 🚀 How to Use (For OpenClaw)

### **Step 1: Read the Guide**
```
Read: MODEL_SELECTION_GUIDE.md
```

This teaches:
- Which model for which task
- When to use each model
- How to balance quality/cost

### **Step 2: Import and Initialize**
```python
from skills.poe_api.scripts.poe_client import PoeClient

client = PoeClient()
```

### **Step 3: Use Task-Based Methods**
```python
# Programming
result = client.programming("Write a REST API")

# Design
result = client.ui_design("Create design system")

# Analysis
result = client.data_analysis("Analyze trends")

# Search
result = client.web_search("Latest AI news")

# Creative
result = client.generate_image("Modern dashboard")
result = client.generate_video("City sunset")
result = client.generate_audio("Welcome message")
```

---

## 📋 Default Recommendations

| Task Type | Default Model | Why |
|-----------|---------------|-----|
| **Programming** | claude-sonnet-4.6 | Best all-around |
| **UI/UX Design** | gemini-3.1-pro | 1M context |
| **Analysis** | claude-sonnet-4.6 | Excellent reasoning |
| **Search** | perplexity-sonar-pro | Citations + depth |
| **Images** | nano-banana-2 | Latest + fast |
| **Videos** | veo-3.1 | Quality + audio |
| **Audio** | elevenlabs-v3 | Most realistic |

**When in doubt**: Use `claude-sonnet-4.6`

---

## 🔐 Security

✅ **NO SECRETS IN ANY FILE**

- `.env.example` has placeholders only
- No API keys in documentation
- No real tokens in examples
- Use environment variables

---

## 📁 File Structure

```
skills/poe-api/
├── SKILL.md                      # Main skill doc
├── MODEL_SELECTION_GUIDE.md      # Detailed model guide (READ THIS!)
├── README.md                     # User guide
├── skill.json                    # Metadata
├── .env.example                  # Config template
├── requirements.txt              # Dependencies
├── scripts/
│   └── poe_client.py            # Client implementation
└── examples/
    ├── basic_usage.py           # Usage examples
    └── model_selection.py       # Selection logic
```

---

## ✅ Ready for Use

The skill is now complete and ready for OpenClaw to use!

**Next Steps**:
1. Read `MODEL_SELECTION_GUIDE.md` to understand model selection
2. Import `PoeClient` in your OpenClaw bot
3. Use task-based methods for automatic model selection
4. When in doubt, use `claude-sonnet-4.6`

---

**No tokens wasted on testing!** 🎯

The skill provides all the information OpenClaw needs to intelligently choose models without any test queries.
