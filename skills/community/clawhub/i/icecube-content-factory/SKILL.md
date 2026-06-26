---
name: icecube-content-factory
description: "🧊 IceCube Content Factory — Turn any topic into viral-worthy content. Auto-generate hooks, threads, and posts with engagement psychology built-in. When users mention 'content creation', 'viral posts', 'social media content', 'write threads', 'content hooks', 'engagement optimization'."
metadata:
  openclaw:
    requires: {}
---

# 🧊 IceCube Content Factory

**Content that captures attention. Automatically.**

Most content gets ignored. IceCube Content Factory uses engagement psychology to create content that stops the scroll.

## What This Skill Does

### 1. Hook Generation
Generate 10 different hook styles for any topic:
- Pattern interrupt hooks
- Curiosity gap hooks
- Pain point hooks
- Story hooks
- Controversy hooks
- Social proof hooks
- FOMO hooks
- Counterintuitive hooks
- How-to hooks
- List hooks

### 2. Thread/Post Structures
- Twitter/X threads (optimal structure)
- LinkedIn posts (professional tone)
- Xiaohongshu notes (visual + emotional)
- Reddit posts (authentic + value)
- Blog intros (SEO + engagement)

### 3. Engagement Optimization
- Optimal posting times by platform
- Hashtag strategies
- CTA placement
- Emoji usage patterns
- Formatting for readability

### 4. Content Remixing
- Turn one idea into 10 posts
- Repurpose long-form into short-form
- Transform text into visual concepts
- Create content series from single topic

## Hook Templates

### 1. Pattern Interrupt
```
"Everyone thinks [common belief].
Here's why they're wrong:"
```

### 2. Curiosity Gap
```
"I discovered something that changed everything.
Most people will never know this:"
```

### 3. Pain Point
```
"Struggling with [pain point]?
I spent 6 months figuring this out so you don't have to:"
```

### 4. Story
```
"6 months ago, I was [bad situation].
Today, [good outcome].
Here's exactly what changed:"
```

### 5. Controversy
```
"Unpopular opinion: [controversial take]
Let me explain:"
```

### 6. Social Proof
```
"[X people] have used this to [result].
Here's the breakdown:"
```

### 7. FOMO
```
"This [opportunity] is disappearing.
Those who act now will [benefit]:"
```

### 8. Counterintuitive
```
"The best way to [goal] is NOT [expected method].
It's actually [surprising method]:"
```

### 9. How-to
```
"How to [achieve outcome] in [timeframe]:
A step-by-step guide:"
```

### 10. List
```
"[Number] [things] that will [outcome]:
[Teaser 1]
[Teaser 2]
[Teaser 3]
Thread 🧵"
```

## Usage Examples

### Example 1: Twitter Thread
```
Input: "AI agent memory"
Output:
Hook: "Most AI agents forget everything after 30 minutes.
Here's how I built one that remembers forever:"

Structure:
1/8 [Hook]

2/8 The problem: Zep uses 600K tokens per conversation

3/8 The solution: File-based memory

4/8 How it works: Four-layer architecture

5/8 The results: 15KB vs 600KB

6/8 Implementation details

7/8 Lessons learned

8/8 If you're building AI agents, this matters.
RT if helpful 🔁
```

### Example 2: Xiaohongshu Note
```
Input: "AI agent memory"
Output:
Title: "AI agent 记忆力提升 4000%｜从 600KB 降到 15KB"

Hook: "大部分人不知道 AI agent 为什么总是忘记..."

Structure:
- Problem (痛点)
- Solution (解决方案)
- Results (效果)
- How-to (教程)
- CTA (互动)

Emojis: 🧊 💾 ⚡ 📉

Hashtags: #AI工具 #效率提升 #黑科技
```

### Example 3: LinkedIn Post
```
Input: "AI agent memory"
Output:
Hook: "After 6 months of experimentation, I finally solved the AI memory problem."

Body:
- Professional framing
- Data-driven results
- Business implications
- Call to action

Tone: Thought leadership, not clickbait
```

## Content Psychology Principles

### 1. Open Loops
- Start with incomplete information
- Promise resolution at the end
- Keep readers engaged throughout

### 2. Pattern Interrupts
- Break expected patterns
- Surprise the brain
- Force attention

### 3. Value Density
- Every sentence must add value
- Cut fluff ruthlessly
- Respect reader time

### 4. Emotional Triggers
- Curiosity
- Fear of missing out
- Desire for gain
- Pain avoidance
- Social validation

### 5. Authority Signals
- Data and metrics
- Personal experience
- Expert quotes
- Case studies

## Workflow

### Step 1: Topic Input
```yaml
topic: "AI agent memory"
audience: "developers"
platform: "twitter"
tone: "technical but accessible"
goal: "educate and drive interest"
```

### Step 2: Hook Generation
Generate 5 hooks using different templates.

### Step 3: Structure Selection
Choose optimal structure for platform.

### Step 4: Content Drafting
Draft complete content with hooks + body + CTA.

### Step 5: Optimization
- Check readability score
- Verify engagement elements
- Add platform-specific elements

### Step 6: Output
Generate final content ready to post.

## Advanced Features

### A/B Test Hooks
Generate multiple hooks, test engagement:
```yaml
hooks:
  - hook_a: "Most AI agents forget everything..."
    style: "pattern_interrupt"
  - hook_b: "I spent 6 months solving memory..."
    style: "story"
  - hook_c: "600KB vs 15KB: The memory breakthrough..."
    style: "counterintuitive"
```

### Content Series
Turn one topic into a week of content:
```
Day 1: Hook-focused intro
Day 2: Deep dive #1
Day 3: Case study
Day 4: Deep dive #2
Day 5: Implementation guide
Day 6: Common mistakes
Day 7: Summary + CTA
```

### Platform Optimization
```yaml
twitter:
  max_chars: 280
  optimal_threads: 8-12 tweets
  hashtag_limit: 2-3

linkedin:
  max_chars: 3000
  optimal_length: 1300-2000
  no_hashtags_in_body

xiaohongshu:
  title_chars: 20
  body_style: emotional + visual
  emoji_density: high

reddit:
  max_title: 300
  style: authentic + value-dense
  no_obvious_promotion
```

## Integration with IceCube Suite

**icecube-memory:** Store successful hooks and patterns
**icecube-heartbeat:** Track content performance during maintenance
**icecube-evolution:** Learn from high-engagement content

## Output Format

**memory/content/YYYY-MM-DD.md:**
```markdown
# Content Factory — YYYY-MM-DD

## Topic: AI Agent Memory
Platform: Twitter
Generated: HH:MM

### Hooks Generated
1. Pattern Interrupt: "Most AI agents forget..."
2. Story: "I spent 6 months..."
3. Counterintuitive: "600KB vs 15KB..."

### Selected Hook
"Most AI agents forget everything after 30 minutes.
Here's how I built one that remembers forever:"

### Full Content
[8-tweet thread]

### Engagement Prediction
- High: Hook type performs well in tech niche
- Risk: Might attract developer audience only

### Posted
- [ ] Twitter
- [ ] LinkedIn
- [ ] Xiaohongshu

### Actual Performance
(Updated after posting)
- Impressions: 
- Engagement:
- Click-through:
```

## Anti-Patterns

❌ **Don't:**
- Use clickbait without substance
- Over-promise and under-deliver
- Ignore platform norms
- Copy-paste without adaptation

✅ **Do:**
- Deliver value in every piece
- Match hook to actual content
- Adapt tone per platform
- Learn from high performers

## License

MIT — Use freely.

---

*Content that stops the scroll. Not just more noise.*