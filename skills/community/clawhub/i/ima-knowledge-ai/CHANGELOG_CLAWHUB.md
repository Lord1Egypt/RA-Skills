# Changelog — AI Content Brief, Script & Outline Generator

All notable changes to this skill will be documented in this file.

---

## [1.0.7] - 2026-03-25

### Changed
- Renamed display name to "AI Content Brief, Script & Outline Generator — Research Assistant for Video & Image" for SDO optimization
- Rewrote description to naturally include target search terms (brief, script, outline, generator, research assistant)
- Added keywords: brief, script, outline, research
- SDO impact: lexical boost from 0 → +1.1 for all 5 target search queries

---

## [1.0.6] - 2026-03-19

### Changed
- Renamed display name to "Knowledge Base for AI Video, Image & Audio Generation" for better ClawHub search discoverability
- SDO optimization: name now contains key search terms (video, image, audio, generation) for lexical boost

---

## [1.0.4] - 2026-03-11

### Changed
- Optimized Midjourney usage guide
- Improved SKILL.md header metadata

---

## [1.0.3] - 2026-03-05

### Changed
- Optimized skill description
- Model selection guide: Improved Midjourney and Nano Banana 2 logic

---

## [1.0.2] — 2026-03-04

### 📚 Modular Knowledge Base Expansion

**Major update: Added 68 KB of new knowledge with modular on-demand loading architecture.**

#### Added

**New Modular Knowledge Directories** (contributor: 李鹤, senior designer):

1. **`references/color-theory/`** (32 KB, 8 files)
   - Color psychology for 11 major colors
   - 5 color combination principles
   - Cultural differences (China/US/Japan/India/Middle East + 4 detailed regions)
   - Religious color systems (5 major religions)
   - Industry-specific color preferences (10 industries)
   - IMA Studio color decision strategy

2. **`references/design-pitfalls/`** (21 KB, 5 files)
   - 29 common design mistakes across 4 scenarios
   - Logo design pitfalls (10 rules)
   - Poster/Banner pitfalls (8 rules)
   - Product/E-commerce pitfalls (6 rules)
   - Web/UI pitfalls (5 rules)

3. **`references/color-trends-2026/`** (16 KB, 6 files)
   - 2026 annual representative colors (Pantone Cloud Dancer, WGSN Transformative Teal, China Horse Red)
   - Spring-Summer trends (Mar-Aug: Cobalt Blue, Violet, Bright Pink)
   - Fall-Winter trends (Sep-Feb: Dark Luxury theme)
   - Regional differences (China/US/Southeast Asia)
   - Industry-specific applications

**Modular Architecture**:
- Each directory has an index `README.md` with quick navigation
- Agent loads only relevant modules (60-90% token savings)
- Relative path linking between modules
- Time-based and scenario-based loading strategies

#### Changed

- **SKILL.md**: Updated to reference 12 knowledge modules (was 8)
  - Added sections 10-12 for new modular directories
  - Expanded Quick Reference table (+7 entries, now 28 total)
  - Updated version: 1.0.1 → 1.0.2
  
- **Total knowledge base**: 116 KB → 184 KB (+68 KB, +59%)
- **Total files**: 13 → 42 (+29 files)

#### Fixed

- **Security & Compliance**:
  - Removed brand name "ImaClaw" → generic "评价/建议"
  - Replaced operational instructions with descriptive guidance (ClawHub security scan compliance)
  - Removed ffmpeg code snippets → "use video editing tools"
  - Removed ima_prefs.json file reference → "consider user preferences"
  - Changed specific tool names → generic descriptions
  
- **Documentation**:
  - All references remain strictly advisory (no operational steps)
  - Maintained focus on planning and parameter choices

#### Technical Details

**Contributor Credit**: 李鹤 (Senior Designer)
- 2.5 hours professional knowledge contribution (2026-03-03)
- 90 KB professional design knowledge
- Color theory + cultural sensitivity + design pitfalls

**Commit History**:
- `9837d4f` - Initial 3 documents (64 KB)
- `198986c` - Modularized color-theory + design-pitfalls
- `a56c97b` - Modularized color-trends-2026
- `7301a66` - Updated SKILL.md accessibility
- `242c67b` - Removed ImaClaw brand name
- `2960cc1` - Security compliance fixes

---

## [1.0.1] — 2026-03-03

### 🔧 ClawHub Release Fixes

**Cleanup and improvements for public release.**

#### Removed
- **Development Scripts**: Removed `scripts/parse_arena_leaderboard.py` (development-only tool, not needed for production)

#### Changed
- **Best Practices Links**: Updated `references/best-practices/README.md` to use relative markdown links
  - Scene index table now uses `[jewelry.md](jewelry.md)` format instead of inline code
  - Keyword sections now link to respective scene files
  - Improves navigation in ClawHub skill browser

#### Fixed
- Version consistency across all files (1.0.0 → 1.0.1)

---

## [1.0.0] — 2026-03-03

### 🎉 Initial ClawHub Release

This is the first public release of **ima-knowledge-ai** — a comprehensive knowledge base for strategic guidance on IMA Studio multi-media content creation.

### 📚 Knowledge Base (9 Topics, ~80 KB optimized)

#### Core Strategic Guidance

1. **workflow-design.md** (7.2 KB)
   - Task decomposition strategies
   - Dependency identification methods
   - Multi-step workflow templates
   - Common creation patterns

2. **model-selection.md** (8 KB) ⭐ **NEW**
   - Task type consolidation (7 types: 2 image, 4 video, 1 music)
   - Arena.AI leaderboard rankings (Text-to-Image, Text-to-Video)
   - Model recommendations with real performance data
   - Content policy warnings (OpenAI real-person restrictions)
   - Midjourney special notes (strong aesthetics, weak text rendering)

3. **parameter-guide.md** (8 KB) ⭐ **REWRITTEN**
   - Task type awareness (modification tasks vs new generation)
   - Prompt optimization rules (when to optimize, when not to)
   - Aspect ratio selection strategy
   - Midjourney special implementation (--ar parameter)

#### Visual Consistency & Production

4. **visual-consistency.md** (12 KB)
   - Why AI lacks consistency by default
   - Reference-driven generation workflow
   - Image-to-Image / Video-to-Video modes
   - Multi-shot coherence strategies

5. **video-modes.md** (8 KB) ⭐ **OPTIMIZED**
   - `image_to_video` vs `reference_image_to_video` (critical distinction!)
   - Traditional two-step vs modern one-step workflow
   - Fallback strategies when primary method fails

6. **long-video-production.md** (8 KB) ⭐ **OPTIMIZED**
   - Why models are limited to 10-15 seconds
   - Shot-by-shot generation strategy
   - Video editing and stitching techniques
   - Simplified workflow patterns

7. **character-design.md** (8 KB) ⭐ **OPTIMIZED**
   - Character Design workflow (Reference-driven)
   - Turnaround sheets, expression library, outfit variants
   - Action poses and consistency strategies

8. **vi-design.md** (8 KB) ⭐ **OPTIMIZED**
   - VI (Visual Identity) system overview
   - Foundation system (Logo / Color / Typography)
   - Application system (Office / Store / Packaging / Digital)
   - Reference-driven workflow (Foundation → Applications)

#### Best Practices (Modular Structure) ⭐⭐⭐ **NEW**

9. **best-practices/** (15 KB, 5 files)
   - **On-demand loading structure** for context efficiency
   - **Index + 4 scenario files** (jewelry, skincare, perfume, cinematic-art)
   - Contributed by 李鹤 (colleague)
   - **Token savings: 60-85%** per task (load only relevant scenario)
   
   Files:
   - `README.md` (2 KB) — Index with keyword matching
   - `jewelry.md` (3 KB) — Jewelry & accessories commercial ads
   - `skincare.md` (3 KB) — Skincare & cosmetics commercial ads
   - `perfume.md` (3 KB) — Perfume & fragrance commercial ads
   - `cinematic-art.md` (4 KB) — Cinematic vintage art photography

---

## 🎯 Core Methodology

### Reference-Driven Generation

**The universal principle** taught across all advanced topics:

> Generate a **Master Reference** first → Use it to generate all **Variants**

This methodology applies to:
- **Video Production** → Master character/scene → All shots
- **Character Design** → Base design → Turnaround sheets, expressions, outfits
- **VI Design** → Logo foundation → All application materials
- **Commercial Ads** → Master visual style → Product variations

**Why it works**:
- AI models generate **random variations** by default
- Reference images provide **visual anchors** for consistency
- `reference_strength` parameter controls consistency level (0.7-0.95)

---

## 📊 Knowledge Base Optimization

### Before Optimization (Initial Version)
- **Total Size**: 184 KB (8 files)
- **Longest file**: 34 KB (long-video-production.md)
- **Structure**: Single monolithic documents

### After Optimization (v1.0.0)
- **Total Size**: ~80 KB (9 topics, -53% reduction)
- **Longest file**: 12 KB (visual-consistency.md)
- **Structure**: Modular best-practices (on-demand loading)
- **Token efficiency**: 60-85% savings per task

### Optimization Highlights
- ✅ 4 files slimmed: 172 KB → 80 KB (-53%)
- ✅ parameter-guide.md rewritten: 502 lines → 208 lines (-59%)
- ✅ model-selection.md rewritten: Arena.AI leaderboard data integrated
- ✅ best-practices split: Single 13.3KB file → 5 modular files (2-4KB each)

**Philosophy**: Agent documentation = Decision handbook, not textbook

---

## 🌟 Key Features

### What This Skill Does

✅ **Strategic Guidance** — Helps you make better decisions  
✅ **Model Selection** — Recommends optimal models for tasks  
✅ **Parameter Optimization** — Teaches cost/quality/speed trade-offs  
✅ **Visual Consistency** — Reference-driven workflow methodology  
✅ **Production Workflows** — Real-world case studies with step-by-step guides  
✅ **Cost Transparency** — Clear credit costs for all recommendations  

### What This Skill Does NOT Do

❌ **API Calls** — This is pure knowledge, not execution  
❌ **File Operations** — No image/video generation or uploads  
❌ **Direct Content Creation** — Use `ima-image-ai`, `ima-video-ai`, `ima-voice-ai` for that  

---

## 🔗 Related Skills

**ima-knowledge-ai** works alongside IMA Studio execution skills:

- **[ima-image-ai](https://git.joyme.sg/imagent/skills/ima-image-ai)** — Image generation (text-to-image, image-to-image)
- **[ima-video-ai](https://git.joyme.sg/imagent/skills/ima-video-ai)** — Video generation (text-to-video, image-to-video)
- **[ima-voice-ai](https://git.joyme.sg/imagent/skills/ima-voice-ai)** — Music generation (text-to-music)
- **[ima-all-ai](https://git.joyme.sg/imagent/skills/ima-all-ai)** — Unified multi-media generation
- **[ima-resource-upload](https://git.joyme.sg/imagent/skills/ima-resource-skill)** — File upload to IMA OSS

---

## 🎓 Target Audience

### Who Should Use This Skill?

- ✅ **AI Agents** using ima-*-ai skills
- ✅ **Content Creators** planning multi-step workflows
- ✅ **Designers** working on character/IP development
- ✅ **Brand Managers** creating VI/identity systems
- ✅ **Video Producers** making long-form content
- ✅ **Developers** integrating IMA Studio APIs
- ✅ **Anyone** needing strategic guidance for AI content creation

---

## 🛠️ Technical Details

### Knowledge Base Structure

```
references/
├── workflow-design.md           # 7.2 KB  — Task decomposition
├── model-selection.md           # 9.7 KB  — Model recommendations
├── parameter-guide.md           # 12 KB   — Parameter optimization
├── visual-consistency.md        # 12 KB   — Reference-driven workflow
├── video-modes.md               # 31 KB   — Video generation modes
├── long-video-production.md     # 34 KB   — Long-form video guide
├── character-design.md          # 22 KB   — Character/IP design
└── vi-design.md                 # 31 KB   — VI/brand identity
```

### API Version Compatibility

- **Based on**: IMA Studio Production API (2026-02-27)
- **Models Covered**: 20+ models across image/video/music
- **Last Verified**: 2026-03-02

---

## 🚀 Installation

### Via ClawHub CLI

```bash
clawhub install ima-knowledge-ai
```

### Manual Installation

```bash
cd ~/.openclaw/skills
git clone https://git.joyme.sg/imagent/skills/ima-knowledge-ai.git
```

---

## 📖 Usage Pattern

```
User Request
  ↓
[ima-knowledge-ai] Query relevant knowledge
  ↓
Make informed decision (model, parameters, workflow)
  ↓
[ima-*-ai] Execute API call with optimized settings
  ↓
Success! 🎉
```

---

## 💡 Example Scenarios

### Scenario 1: Image Series

**User**: "生成一套产品图,5张不同角度"

**Knowledge consulted**:
- `visual-consistency.md` → Reference-driven workflow
- `parameter-guide.md` → Optimal resolution settings

**Result**: Generate 1 master reference → Use it for 4 additional angles

---

### Scenario 2: Long Video

**User**: "做个1分钟的宣传片"

**Knowledge consulted**:
- `long-video-production.md` → Multi-shot workflow
- `video-modes.md` → Shot generation modes
- `visual-consistency.md` → Maintain visual coherence

**Result**: Script → 6 shots (10s each) → Video editing → 1min output

---

### Scenario 3: Character Design

**User**: "游戏角色设计,需要多角度视图"

**Knowledge consulted**:
- `character-design.md` → Turnaround sheet workflow
- `visual-consistency.md` → Reference-driven generation

**Result**: Master design → 3-4 view turnaround sheet → Expression library

---

## 🎯 Future Roadmap

### Planned Topics (v2.0+)

- **Prompt Engineering** — Advanced prompt writing techniques
- **Cost Optimization** — Budget control and batch generation strategies
- **Failure Handling** — Error recovery and retry strategies
- **Case Studies Library** — More real-world production examples
- **Performance Optimization** — Speed vs. quality trade-offs

---

## 📞 Support & Feedback

- **Issues**: [GitLab Issues](https://git.joyme.sg/imagent/skills/ima-knowledge-ai/-/issues)
- **Discussions**: [ClawHub Comments](https://clawhub.com)
- **API Support**: [IMA Studio](https://imastudio.com)

---

## 📜 License

MIT License — See [LICENSE](LICENSE) for full details.

---

## 🙏 Credits

**Developed by**: IMA Skills Team  
**Contributors**: OpenClaw Community  
**Special Thanks**: All early testers and feedback providers

---

**Last Updated**: 2026-03-03  
**Version**: 1.0.1  
**Status**: ✅ Ready for ClawHub Release

---

**"Knowledge is power — but only when applied!"** 🍵
