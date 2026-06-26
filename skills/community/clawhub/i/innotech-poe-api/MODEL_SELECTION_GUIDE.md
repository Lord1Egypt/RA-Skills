# 🎯 Poe API Model Selection Guide for OpenClaw

**Purpose**: Teach OpenClaw how to choose the correct AI model for any task  
**Last Updated**: 2026-03-03  
**Models Available**: 342 total, key models documented here

---

## 📋 Quick Decision Tree

```
What type of task?
│
├─ PROGRAMMING / CODING
│  ├─ General coding → claude-sonnet-4.6 ⭐
│  ├─ Very complex → claude-opus-4.6
│  ├─ Need fast → claude-haiku-4.5
│  ├─ Huge context (>200K) → gemini-3.1-pro
│  └─ Code-focused → gpt-5.3-codex
│
├─ UI/UX DESIGN
│  ├─ Design systems → gemini-3.1-pro ⭐ (1M context!)
│  ├─ UI components → claude-sonnet-4.6
│  └─ Quick design → claude-haiku-4.5
│
├─ REQUIREMENT ANALYSIS
│  ├─ Requirements gathering → claude-sonnet-4.6 ⭐
│  ├─ Complex systems → claude-opus-4.6
│  └─ Huge documents → gemini-3.1-pro
│
├─ DATA ANALYSIS
│  ├─ Data interpretation → claude-sonnet-4.6 ⭐
│  ├─ Large datasets → gemini-3.1-pro
│  └─ Statistical analysis → claude-opus-4.6
│
├─ WEB SEARCH
│  ├─ Simple search → perplexity-search
│  ├─ Complex queries → perplexity-sonar-pro
│  ├─ Reasoning + search → perplexity-sonar-rsn-pro
│  ├─ Deep research → o3-deep-research
│  └─ Budget research → o4-mini-deep-research
│
├─ IMAGE GENERATION
│  ├─ Best quality → imagen-4-ultra
│  ├─ Fast + good → nano-banana-2 ⭐
│  ├─ Text in images → nano-banana-pro
│  ├─ General purpose → nano-banana
│  ├─ Professional editing → gpt-image-1.5
│  └─ Asian aesthetics → seedream-4.0
│
├─ VIDEO GENERATION
│  ├─ Best + audio → veo-3.1 ⭐
│  ├─ Cinematic → sora-2-pro
│  ├─ Versatile → kling-o3
│  ├─ Standard → sora-2
│  ├─ Storytelling → wan-2.6
│  └─ Fast → seedance-1.0-pro
│
└─ AUDIO GENERATION
   ├─ Realistic speech → elevenlabs-v3 ⭐
   ├─ Fast TTS → gemini-2.5-flash-tts
   ├─ Controlled speech → hailuo-speech-02
   └─ Music → hailuo-music-v1.5
```

---

## 🤖 TEXT/REASONING MODELS

### **Claude-Opus-4.6** ⭐⭐⭐⭐⭐
**ID**: `claude-opus-4.6`  
**Context**: 983,040 tokens (nearly 1M!)  
**Max Output**: 128,000 tokens  
**Owner**: Anthropic

#### **Best For**
- ✅ Most complex problems requiring deepest reasoning
- ✅ Complex coding and system design
- ✅ Long-running autonomous tasks
- ✅ Planning and debugging
- ✅ Critical/safety systems

#### **When to Use**
- Task is very complex
- Need deepest reasoning
- Budget is not a concern
- Research-grade analysis

#### **Strengths**
- State-of-the-art reasoning
- 1M token context window
- Excellent at autonomous tasks
- Strong safety and reliability

#### **Avoid When**
- Need fast results (use Haiku instead)
- Simple tasks (use Haiku instead)
- Budget-conscious (use Sonnet or Haiku)

---

### **Claude-Sonnet-4.6** ⭐⭐⭐⭐⭐ (RECOMMENDED DEFAULT)
**ID**: `claude-sonnet-4.6`  
**Context**: 983,040 tokens  
**Max Output**: 128,000 tokens  
**Owner**: Anthropic

#### **Best For**
- ✅ **DEFAULT CHOICE for most tasks** ⭐
- ✅ Programming and coding
- ✅ Requirement analysis
- ✅ Data analysis
- ✅ General reasoning
- ✅ High-quality conversations
- ✅ End-to-end project management
- ✅ Document writing

#### **When to Use**
- **When in doubt, use this model!**
- Most programming tasks
- Most analysis tasks
- Need balanced quality and speed

#### **Strengths**
- Excellent all-around performance
- 1M token context window
- Great at coding and development
- Polished document generation
- Good balance of speed and quality

#### **Avoid When**
- Need fastest possible (use Haiku)
- Most complex problems (use Opus)
- Need >200K context AND multimodal (use Gemini-3.1-Pro)

---

### **Claude-Haiku-4.5** ⭐⭐⭐⭐
**ID**: `claude-haiku-4.5`  
**Context**: 192,000 tokens  
**Max Output**: 64,000 tokens  
**Owner**: Anthropic

#### **Best For**
- ✅ Fastest and most efficient Claude
- ✅ Real-time applications
- ✅ High-volume tasks
- ✅ Quick iterations
- ✅ Simple tasks

#### **When to Use**
- Need fast results
- Budget-conscious
- Simple coding tasks
- Quick analysis
- High-volume applications

#### **Strengths**
- Near-frontier intelligence at low cost
- Very fast
- Efficient
- >73% on SWE-bench verified
- Extended thinking support

#### **Avoid When**
- Very complex problems (use Sonnet/Opus)
- Need >192K context (use Sonnet/Opus/Gemini)

---

### **Gemini-3.1-Pro** ⭐⭐⭐⭐⭐
**ID**: `gemini-3.1-pro`  
**Context**: 1,048,576 tokens (**1M!**)  
**Max Output**: 65,536 tokens  
**Owner**: Google

#### **Best For**
- ✅ **HUGE context (1M tokens!)** ⭐
- ✅ UI/UX design systems
- ✅ Analyzing massive documents (>200K tokens)
- ✅ Large codebase analysis
- ✅ Complex problem-solving
- ✅ Multimodal tasks (text, image, video, audio input)

#### **When to Use**
- **MUST use when context >200K tokens**
- Design systems and UX research
- Need to analyze entire codebases
- Need multimodal input
- When 1M context is needed

#### **Strengths**
- Massive 1M context window
- Multimodal input support (text, image, video, audio)
- Top benchmark results
- Great for design thinking

#### **Avoid When**
- Need >65K output (use Claude models)
- Only text tasks <200K (Claude is often better)

---

### **GPT-5.3-Codex** ⭐⭐⭐⭐
**ID**: `gpt-5.3-codex`  
**Context**: 400,000 tokens  
**Max Output**: 128,000 tokens  
**Owner**: OpenAI

#### **Best For**
- ✅ Software development
- ✅ Code completion
- ✅ Algorithm explanation
- ✅ Debugging
- ✅ Full-stack coding

#### **When to Use**
- Code-focused tasks
- Need to understand complex codebases
- Algorithm design
- Debugging assistance
- Full-stack development

#### **Strengths**
- Designed for developers
- Excellent at code understanding
- Accurate completions
- Supports modern languages
- 400K context

#### **Avoid When**
- Need general reasoning (use Claude-Sonnet)
- Need >400K context (use Gemini-3.1-Pro)
- Non-coding tasks

---

## 🔍 WEB SEARCH MODELS

### **Perplexity-Search** ⭐⭐⭐
**ID**: `perplexity-search`  
**Owner**: Empirio Labs AI

#### **Best For**
- ✅ Simple web searches
- ✅ Real-time information
- ✅ Quick lookups

#### **When to Use**
- Simple web searches
- Need real-time information
- Don't need LLM-style response

#### **Note**: Returns search results, not LLM response

---

### **Perplexity-Sonar-Pro** ⭐⭐⭐⭐
**ID**: `perplexity-sonar-pro`  
**Context**: 200,000 tokens  
**Owner**: Empirio Labs AI

#### **Best For**
- ✅ Complex queries
- ✅ In-depth research
- ✅ Double the citations

#### **When to Use**
- Need detailed answers with citations
- Complex research queries

---

### **Perplexity-Sonar-Rsn-Pro** ⭐⭐⭐⭐⭐
**ID**: `perplexity-sonar-rsn-pro`  
**Context**: 128,000 tokens  
**Owner**: Empirio Labs AI

#### **Best For**
- ✅ Reasoning + search
- ✅ Superior quality and precision
- ✅ High-quality answer generation

#### **When to Use**
- Need reasoning with search
- Complex queries requiring logic
- Best quality answers

---

### **o3-deep-research** ⭐⭐⭐⭐⭐
**ID**: `o3-deep-research`  
**Context**: 200,000 tokens  
**Max Output**: 100,000 tokens  
**Owner**: OpenAI

#### **Best For**
- ✅ Extensive web research
- ✅ Complex, nuanced questions
- ✅ Finance, consulting, science
- ✅ Deep analysis

#### **When to Use**
- Need deep research
- Complex multi-domain questions
- Professional research needs

---

### **o4-mini-deep-research** ⭐⭐⭐⭐
**ID**: `o4-mini-deep-research`  
**Context**: 200,000 tokens  
**Max Output**: 100,000 tokens  
**Owner**: OpenAI

#### **Best For**
- ✅ Budget-friendly deep research
- ✅ Similar to o3 but cheaper

#### **When to Use**
- Need deep research but budget-conscious

---

## 🖼️ IMAGE GENERATION MODELS

### **Imagen-4-Ultra** ⭐⭐⭐⭐⭐
**ID**: `imagen-4-ultra`  
**Owner**: Google

#### **Best For**
- ✅ Highest quality images
- ✅ Exceptional prompt adherence
- ✅ Great detail and lighting

#### **When to Use**
- Need highest quality
- Complex prompts
- Professional graphics

---

### **Nano-Banana-2** ⭐⭐⭐⭐⭐
**ID**: `nano-banana-2`  
**Context**: 65,536 tokens  
**Owner**: Google

#### **Best For**
- ✅ Latest image model
- ✅ Pro-level intelligence
- ✅ Lightning-fast generation
- ✅ Precise text rendering
- ✅ 4K production-ready

#### **When to Use**
- Need fast + high quality
- Text in images
- 4K resolution

---

### **Nano-Banana-Pro** ⭐⭐⭐⭐
**ID**: `nano-banana-pro`  
**Context**: 65,536 tokens  
**Owner**: Google

#### **Best For**
- ✅ Text in images (multi-language)
- ✅ Precise editing/restyling
- ✅ Detailed visuals

#### **When to Use**
- Image editing
- Text rendering
- Need exceptional fidelity

---

### **Nano-Banana** ⭐⭐⭐⭐
**ID**: `nano-banana`  
**Context**: 65,536 tokens  
**Owner**: Google

#### **Best For**
- ✅ General purpose
- ✅ Photo-realistic edits
- ✅ Very fast

#### **When to Use**
- General image generation
- Multi-turn editing
- Need fast generation

---

### **GPT-Image-1.5** ⭐⭐⭐⭐
**ID**: `gpt-image-1.5`  
**Context**: 128,000 tokens  
**Owner**: OpenAI

#### **Best For**
- ✅ Professional image editing
- ✅ Facial preservation
- ✅ World knowledge in images

#### **When to Use**
- Complex editing tasks
- Need facial preservation
- Professional work

---

### **Seedream-4.0** ⭐⭐⭐⭐
**ID**: `seedream-4.0`  
**Owner**: Bytedance

#### **Best For**
- ✅ High fidelity
- ✅ Great text-rendering
- ✅ Asian aesthetics

#### **When to Use**
- Asian style images
- High fidelity
- Text rendering

---

## 🎬 VIDEO GENERATION MODELS

### **Veo-3.1** ⭐⭐⭐⭐⭐
**ID**: `veo-3.1`  
**Owner**: Google

#### **Best For**
- ✅ Best quality + native audio
- ✅ Richer audio (conversations, SFX)
- ✅ Character consistency
- ✅ Cinematic styles

#### **When to Use**
- Need highest quality video
- Native audio important
- Multiple scenes
- Professional/cinematic

#### **Features**
- Duration: 4s, 6s, 8s
- Resolution: 720p, 1080p
- Native audio generation
- Image-to-video support

---

### **Sora-2-Pro** ⭐⭐⭐⭐⭐
**ID**: `sora-2-pro`  
**Owner**: OpenAI

#### **Best For**
- ✅ State-of-the-art video + audio
- ✅ Enhanced physical accuracy
- ✅ Highest fidelity cinematic
- ✅ Synchronized dialogue

#### **When to Use**
- OpenAI ecosystem preference
- Need synchronized dialogue
- Highest fidelity cinematic
- Complex multi-shot

#### **Features**
- Duration: 4s, 8s, 12s
- Multiple resolutions
- Text-to-video and image-to-video

---

### **Kling-O3** ⭐⭐⭐⭐⭐
**ID**: `kling-o3`  
**Owner**: Empirio Labs AI

#### **Best For**
- ✅ Most versatile (4 workflows)
- ✅ Native sound generation
- ✅ Multi-scene transitions

#### **When to Use**
- Need multiple workflows
- Video editing
- Multi-scene videos

#### **Workflows**
1. Text-to-Video
2. Image-to-Video
3. Reference-to-Video
4. Video Editing

---

### **Wan-2.6** ⭐⭐⭐⭐⭐
**ID**: `wan-2.6`  
**Owner**: Empirio Labs AI

#### **Best For**
- ✅ Cinematic storytelling
- ✅ Multi-shot narratives
- ✅ Character consistency
- ✅ Audio-visual sync

#### **When to Use**
- Cinematic, multi-shot storytelling
- Need character consistency
- Production-ready results

#### **Multi-Shot Prompting**
```
[Shot 1] [0-5s] Wide shot of city.
[Shot 2] [5-10s] Close-up of character.
```

---

### **Sora-2** ⭐⭐⭐⭐
**ID**: `sora-2`  
**Owner**: OpenAI

#### **Best For**
- ✅ Standard video generation
- ✅ OpenAI ecosystem
- ✅ Cinematic scenes

---

### **Kling-v3-Pro** ⭐⭐⭐⭐
**ID**: `kling-v3-pro`

#### **Best For**
- ✅ Professional quality
- ✅ Text-to-video and image-to-video

---

### **Seedance-1.0-Pro** ⭐⭐⭐⭐
**ID**: `seedance-1.0-pro`

#### **Best For**
- ✅ Fast generation
- ✅ Good prompt following

---

## 🎵 AUDIO GENERATION MODELS

### **ElevenLabs-v3** ⭐⭐⭐⭐⭐
**ID**: `elevenlabs-v3`  
**Context**: 128,000 tokens  
**Owner**: ElevenLabs

#### **Best For**
- ✅ Most realistic speech
- ✅ Emotional tone control
- ✅ Sound effects
- ✅ Audiobooks, games, podcasts

#### **When to Use**
- Need most realistic TTS
- Control over emotion
- Audiobook production
- Game/dialogue audio

#### **Control Tags**
- Voice: `[whispers]`, `[angry]`, `[sarcastic]`
- SFX: `[gunshot]`, `[applause]`, `[explosion]`

#### **Features**
- 35+ voices
- Multiple speakers
- Emotion control
- Sound effects

---

### **Gemini-2.5-Flash-TTS** ⭐⭐⭐⭐
**ID**: `gemini-2.5-flash-tts`  
**Owner**: Empirio Labs AI

#### **Best For**
- ✅ Low-latency TTS
- ✅ Fast generation
- ✅ Multi-speaker

#### **When to Use**
- Need fast TTS
- Conversational systems

#### **Features**
- 30+ voices
- 20+ languages
- Style control

---

### **Hailuo-Speech-02** ⭐⭐⭐⭐
**ID**: `hailuo-speech-02`

#### **Best For**
- ✅ Fine control over speech
- ✅ Speed/pitch/volume adjustments

#### **Parameters**
- Speed: 0.5-2.0
- Volume: 0-10
- Pitch: -12 to 12
- Emotion: happy, sad, angry, etc.

---

### **Hailuo-Music-v1.5** ⭐⭐⭐⭐
**ID**: `hailuo-music-v1.5`

#### **Best For**
- ✅ Music generation
- ✅ High-quality compositions

#### **Prompt Format**
```
[intro]
[verse] Lyrics here
[chorus] Chorus lyrics
[outro] Ending
```

---

## 📊 MODEL SELECTION BY TASK TYPE

### **Programming/Coding**

| Complexity | Primary | Fallback | Budget |
|------------|---------|----------|--------|
| **Simple** | claude-haiku-4.5 | claude-sonnet-4.6 | claude-haiku-4.5 |
| **Medium** | claude-sonnet-4.6 | claude-opus-4.6 | claude-haiku-4.5 |
| **Complex** | claude-opus-4.6 | - | claude-sonnet-4.6 |
| **Huge Context** | gemini-3.1-pro | claude-sonnet-4.6 | - |

### **UI/UX Design**

| Task | Primary | Reason |
|------|---------|--------|
| **Design Systems** | gemini-3.1-pro | 1M context for full systems |
| **UI Components** | claude-sonnet-4.6 | Excellent reasoning |
| **Quick Design** | claude-haiku-4.5 | Fast iterations |

### **Requirement Analysis**

| Task | Primary | Reason |
|------|---------|--------|
| **Gathering** | claude-sonnet-4.6 | Comprehensive, structured |
| **Complex** | claude-opus-4.6 | Deepest analysis |
| **Huge Docs** | gemini-3.1-pro | 1M context |

### **Data Analysis**

| Task | Primary | Reason |
|------|---------|--------|
| **Interpretation** | claude-sonnet-4.6 | Excellent reasoning |
| **Large Datasets** | gemini-3.1-pro | 1M context |
| **Statistical** | claude-opus-4.6 | Deep reasoning |

### **Web Search**

| Task | Primary | Reason |
|------|---------|--------|
| **Simple** | perplexity-search | Fast, real-time |
| **Complex** | perplexity-sonar-pro | Citations, depth |
| **Research** | o3-deep-research | Extensive |

### **Image Generation**

| Task | Primary | Reason |
|------|---------|--------|
| **Best Quality** | imagen-4-ultra | Highest quality |
| **Fast + Good** | nano-banana-2 | Latest, 4K |
| **Text in Image** | nano-banana-pro | Text rendering |
| **General** | nano-banana | All-around |

### **Video Generation**

| Task | Primary | Reason |
|------|---------|--------|
| **Best + Audio** | veo-3.1 | Native audio |
| **Cinematic** | sora-2-pro | Highest fidelity |
| **Versatile** | kling-o3 | 4 workflows |
| **Storytelling** | wan-2.6 | Multi-scene |

### **Audio Generation**

| Task | Primary | Reason |
|------|---------|--------|
| **Speech** | elevenlabs-v3 | Most realistic |
| **Fast TTS** | gemini-2.5-flash-tts | Low latency |
| **Music** | hailuo-music-v1.5 | Song generation |

---

## 🎯 DECISION FRAMEWORK

### **Step 1: Identify Task Type**

1. **Is this programming?**
   - YES → Use Claude family
   - Check complexity:
     - Simple → `claude-haiku-4.5`
     - Medium → `claude-sonnet-4.6` ⭐
     - Complex → `claude-opus-4.6`

2. **Is this UI/UX design?**
   - YES → `gemini-3.1-pro` (1M context for design systems)

3. **Is this analysis?**
   - YES → Check context size:
     - <200K → `claude-sonnet-4.6`
     - >200K → `gemini-3.1-pro`

4. **Is this web search?**
   - Simple → `perplexity-search`
   - Complex → `perplexity-sonar-pro`
   - Research → `o3-deep-research`

5. **Is this creative (image/video/audio)?**
   - Image → `imagen-4-ultra` or `nano-banana-2`
   - Video → `veo-3.1` or `sora-2-pro`
   - Audio → `elevenlabs-v3`

### **Step 2: Check Context Size**

```
if context_size > 1000000:
    → gemini-3.1-pro (1M context)
elif context_size > 200000:
    → gemini-3.1-pro OR claude-opus-4.6 OR claude-sonnet-4.6
else:
    → Any model works
```

### **Step 3: Balance Quality vs Speed**

```
if quality == "highest":
    → Use Pro/Ultra models
elif speed == "fastest":
    → Use Haiku/Flash models
else:
    → Use Sonnet/Standard models (balanced)
```

### **Step 4: Consider Budget**

```
if budget == "unlimited":
    → Use best model for task
elif budget == "limited":
    → Use standard models
else:  # very limited
    → Use budget models (Haiku, mini)
```

---

## ✅ BEST PRACTICES

### **1. Default to claude-sonnet-4.6**

When uncertain, use `claude-sonnet-4.6`:
- Best all-around model
- Works well for most tasks
- Good balance of quality and speed
- 983K context

### **2. Use Task-Based Selection**

Instead of manually choosing, use:

```python
client.query_for_task(
    task_type="programming",
    complexity="medium"
)
```

### **3. Consider Context Size**

- **< 200K**: Any Claude/GPT model
- **200K - 1M**: Gemini-3.1-Pro
- **> 1M**: Split into chunks or use Gemini-3.1-Pro

### **4. Implement Fallbacks**

Always have backup models:

```python
models = [
    "claude-sonnet-4.6",  # Primary
    "claude-opus-4.6",    # Fallback 1
    "gpt-5.3-codex"       # Fallback 2
]
```

### **5. Balance Cost**

- Simple tasks → Haiku
- Medium tasks → Sonnet
- Complex tasks → Opus

---

## 🚨 COMMON MISTAKES

### ❌ **Mistake 1: Always Using the Most Expensive Model**

**Wrong**:
```python
# Using Opus for simple task
client.query("claude-opus-4.6", "Sort this list: [3, 1, 2]")
```

**Correct**:
```python
# Using appropriate model
client.query("claude-haiku-4.5", "Sort this list: [3, 1, 2]")
```

### ❌ **Mistake 2: Ignoring Context Size**

**Wrong**:
```python
# Claude-Sonnet has 983K context, but task needs 1M
client.query("claude-sonnet-4.6", huge_document)  # Will fail!
```

**Correct**:
```python
# Use Gemini for 1M context
client.query("gemini-3.1-pro", huge_document)  # Works!
```

### ❌ **Mistake 3: Wrong Model for Task Type**

**Wrong**:
```python
# Using Claude for web search
client.query("claude-sonnet-4.6", "Search for latest AI news")
```

**Correct**:
```python
# Use search model
client.query("perplexity-search", "Latest AI news")
```

---

## 📝 SUMMARY

### **Default Recommendations**

| Task Type | Primary Model | Reason |
|-----------|---------------|--------|
| **Programming** | claude-sonnet-4.6 | Best all-around |
| **UI/UX** | gemini-3.1-pro | 1M context |
| **Analysis** | claude-sonnet-4.6 | Excellent reasoning |
| **Search** | perplexity-sonar-pro | Citations + depth |
| **Images** | nano-banana-2 | Latest + fast |
| **Videos** | veo-3.1 | Quality + audio |
| **Audio** | elevenlabs-v3 | Most realistic |

### **When in Doubt**

→ Use **`claude-sonnet-4.6`**

### **Key Rules**

1. ✅ Default to `claude-sonnet-4.6`
2. ✅ Use `gemini-3.1-pro` for huge context (>200K)
3. ✅ Use search models for web search
4. ✅ Use specialized models for creative tasks
5. ✅ Implement fallbacks

---

**Remember**: This guide teaches you how to choose the right model. Read it carefully and apply these principles! 🎯
