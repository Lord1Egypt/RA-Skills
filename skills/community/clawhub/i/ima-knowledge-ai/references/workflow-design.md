# Workflow Design — IMA Content Creation

> **Purpose**: Guide agents to decompose complex user requests into atomic, executable tasks.

---

## Core Principle

**User request → Atomic tasks → Sequential execution**

Each atomic task should:
- ✅ Use ONE ima-*-ai skill
- ✅ Have clear input/output
- ✅ Be independently executable

---

## Task Decomposition Patterns

### Pattern 1: Single-Media Creation
**User**: "帮我画一只猫"

**Decomposition**:
```
1. [ima-image-ai] Generate cat image
   → Output: Image URL
```

**No decomposition needed** — single atomic task.

---

### Pattern 2: Multi-Step Same-Media
**User**: "生成一张产品海报，然后把它改成油画风格"

**Decomposition**:
```
1. [ima-image-ai] text_to_image: "product poster, professional"
   → Output: poster.jpg (URL)

2. [ima-image-ai] image_to_image: "oil painting style"
   → Input: poster.jpg
   → Output: poster_oil.jpg
```

**Dependencies**: Step 2 depends on Step 1's output URL.

---

### Pattern 3: Cross-Media Workflow
**User**: "帮我做个宣传视频"

**Decomposition**:
```
1. Script Writing (Agent's text generation, no IMA API)
   → Output: Script text

2. [ima-voice-ai] Generate voiceover
   → Input: Script text
   → Output: voiceover.mp3 (URL)

3. [ima-video-ai] Generate video
   → Input: Script text (as prompt)
   → Output: video_raw.mp4 (URL)

4. Post-processing (if needed)
   → Merge audio and video using editing tools
   → Apply final adjustments
   → Output: final video

5. [ima-resource-upload] Upload final video (optional)
   → Input: Completed video file
   → Output: CDN URL (shareable)
```

**Dependencies**:
- Step 2, 3 are parallel (no dependency)
- Step 4 depends on Step 2 + 3
- Step 5 depends on Step 4

---

### Pattern 4: Iterative Refinement
**User**: "生成一张图，如果不满意就换个模型重试"

**Decomposition**:
```
1. [ima-image-ai] Generate with default model (SeeDream 4.5)
   → Output: image_v1.jpg

2. User Feedback Loop
   → If satisfied: Done
   → If not: Identify issue (style/quality/composition)

3. [ima-knowledge-ai] Query model-selection.md
   → Recommend alternative model based on issue
   
4. [ima-image-ai] Regenerate with recommended model
   → Output: image_v2.jpg

5. Repeat until satisfied
```

**Key**: Use feedback to guide model selection.

---

## Dependency Identification

### Types of Dependencies

1. **Data Dependency** (most common)
   ```
   Task A → Output URL → Task B Input
   ```
   Example: Image generation → Image-to-image editing

2. **Prerequisite Dependency**
   ```
   Task A must complete before Task B can start
   ```
   Example: Script writing → Voiceover generation

3. **Resource Dependency**
   ```
   Task A uploads file → Task B uses uploaded URL
   ```
   Example: Local video → Upload → Use in IMA video-to-video

4. **No Dependency (Parallel)**
   ```
   Task A and Task B can run simultaneously
   ```
   Example: Voiceover + Background video (merged later)

---

## Workflow Templates

### Template 1: Simple Text-to-Media
```
User: "[Media type] + [description]"
→ [ima-{media}-ai] Generate
→ Done
```

**Example**: "画一只猫" → ima-image-ai

---

### Template 2: Media Transformation
```
User: "把 [input] 改成 [style/effect]"
→ Check if input is URL or local file
→ If local: [ima-resource-upload] first
→ [ima-{media}-ai] {media}_to_{media} with input URL
→ Done
```

**Example**: "把这张图改成卡通风格" → upload → ima-image-ai (image_to_image)

---

### Template 3: Multi-Modal Synthesis
```
User: "用 [media A] 和 [media B] 做一个 [output]"
→ Generate/obtain media A
→ Generate/obtain media B
→ Merge using appropriate editing tools
→ [ima-resource-upload] Upload result (optional)
→ Done
```

**Example**: "给这段视频配音" → voiceover generation → merge → upload

---

### Template 4: Batch Generation
```
User: "生成 [N] 个 [media] 关于 [topic]"
→ Generate N prompts (variation strategy)
→ For each prompt:
    [ima-{media}-ai] Generate
→ Collect all URLs
→ Done
```

**Example**: "生成 5 张不同风格的猫咪图片" → 5 parallel ima-image-ai calls

---

## Common Mistakes

### ❌ Mistake 1: Skipping Upload Step
**Wrong**:
```
User provides local image → directly call ima-image-ai with file path
```

**Right**:
```
User provides local image → [ima-resource-upload] → get URL → call ima-image-ai
```

**Why**: IMA API only accepts HTTPS URLs, not local paths.

---

### ❌ Mistake 2: Sequential When Parallel is Possible
**Wrong**:
```
Generate voiceover → Wait → Generate video → Wait → Merge
(Total: 60s + 90s = 150s)
```

**Right**:
```
Generate voiceover (60s) + Generate video (90s) in parallel
→ Wait for both → Merge
(Total: max(60s, 90s) = 90s)
```

**Why**: Voiceover and video have no dependency, can run concurrently.

---

### ❌ Mistake 3: Not Consulting Knowledge Before Execution
**Wrong**:
```
User: "生成16:9图片" → Directly call ima-image-ai with Midjourney
→ Fails (Midjourney doesn't support 16:9)
```

**Right**:
```
User: "生成16:9图片" → Query ima-knowledge-ai parameter-guide.md
→ Learn: Use SeeDream 4.5 or Nano Banana series
→ Call ima-image-ai with correct model
```

**Why**: Knowledge prevents wasted API calls and user frustration.

---

## Decision Tree: Which IMA Skill to Use?

```
User Request
  ↓
Is it text generation? → NO IMA API (use LLM directly)
  ↓
Is it image? → ima-image-ai
  ↓
Is it video? → ima-video-ai
  ↓
Is it audio/voice? → ima-voice-ai
  ↓
Is it file upload? → ima-resource-upload
  ↓
Is it workflow guidance? → ima-knowledge-ai (this skill!)
```

---

## Complexity Assessment

Before decomposing, assess complexity:

| Complexity | Indicators | Strategy |
|------------|-----------|----------|
| **Simple** | Single media type, no editing | Direct call to ima-*-ai |
| **Medium** | Multi-step same media, or basic editing | Sequential workflow (2-3 tasks) |
| **High** | Cross-media, batch, or iterative refinement | Complex workflow (4+ tasks, dependencies) |

---

## Workflow Execution Best Practices

1. **Communicate the plan** before execution
   ```
   "好的！我会分 3 步帮你完成：
   1. 生成配音（预计 30 秒）
   2. 生成视频（预计 90 秒）
   3. 合并音视频（预计 10 秒）
   总耗时约 2 分钟。开始了！"
   ```

2. **Show progress** for each step
   ```
   ✅ 1/3 配音生成完成
   🎬 2/3 视频生成中...（已等待 45s，预计最长 90s）
   ```

3. **Handle failures gracefully**
   ```
   ❌ 步骤 2 失败（视频生成超时）
   💡 建议：换用更快的模型 Nano Banana2
   要我重试吗？
   ```

4. **Optimize for user time**
   - Parallel when possible
   - Use faster models for drafts
   - Batch similar tasks

---

## Summary

**Workflow design is about**:
- 🧩 Breaking complex requests into atomic tasks
- 🔗 Identifying dependencies
- ⚡ Optimizing for speed (parallel execution)
- 🛡️ Preventing mistakes (consult knowledge first)

**Always**:
1. Query ima-knowledge-ai BEFORE complex workflows
2. Communicate the plan to the user
3. Show progress for multi-step tasks
4. Handle failures with alternative suggestions
