---
name: nature-paper2ppt
description: Convert a scientific paper into a presentation deck (PPTX). Generates structured Chinese or bilingual slides for journal clubs, group meetings, or conference talks. Trigger when user wants to make slides from a paper or present research findings.
---

# nature-paper2ppt

## Purpose
Transform a Nature-series paper into a clean, publication-aware PPTX presentation,
optimised for journal-club or group-meeting delivery. Output in Chinese (default)
or bilingual (Chinese + English).

---

## Trigger Conditions
- "做PPT" / "幻灯片" / "slides" / "presentation"
- "journal club" / "组会" / "汇报"
- "paper to PPT" / "paper2ppt" / "论文转PPT"
- User shares a paper and wants to present it

---

## Slide Structure

### 1. Title Slide
- Paper title (full, in English)
- Authors + institution
- Journal + Year + DOI + IF
- Presenter name + date
- Background: clean white or dark navy

### 2. Background & Motivation (1–2 slides)
- Why does this problem matter? (3–4 bullet points)
- Current limitations or gaps in the field
- Key concepts the audience needs (define jargon)

### 3. Research Question & Approach (1 slide)
- One sentence: what did they set out to do?
- Main hypothesis or objective
- Brief method overview (schematic if available)

### 4. Key Results (3–5 slides, one per main finding)
For each Results subsection:
- Slide title = the key message (e.g., "Catalyst achieves 95% efficiency at low overpotential")
- Main figure (reproduced or described)
- 2–3 bullet points explaining what the data shows
- One sentence: so what? (interpretation)

### 5. Mechanism / Why It Works (1 slide)
- Mechanistic explanation
- Key experiment that proves the mechanism
- Theoretical support (DFT, MD, etc.) if present

### 6. Comparison with Prior Work (1 slide)
- Table or bar chart: this work vs. literature
- Highlight where this paper advances the state of the art

### 7. Discussion & Limitations (1 slide)
- What does this mean for the field?
- Honest limitations (what they didn't prove)
- Open questions remaining

### 8. Conclusion (1 slide)
- 3–5 bullet points: key takeaways
- Broader significance in one sentence

### 9. Critical Thinking (1 slide) — optional
- Questions for discussion:
  - Is the claim fully supported by the data?
  - What experiment is missing?
  - How would you follow up?

### 10. References (1 slide)
- Key references cited in the paper (top 5–8)

---

## Language Options

Ask user:
- **中文** (default): all slide content in Chinese, figure captions translated
- **双语** (bilingual): English title + Chinese body text
- **English**: full English (for international presentations)

---

## Design Guidelines

### Typography:
- Title font: 32–36pt, bold
- Body font: 20–24pt
- Minimum readable: 18pt
- Chinese font: 微软雅黑 (Microsoft YaHei) or 思源黑体 (Source Han Sans)
- English font: Arial or Calibri

### Layout:
- 16:9 widescreen (1920×1080 recommended)
- Clean white background with accent color (use journal color if applicable)
- Nature blue accent: #0E4D92 or #4878CF
- One key point per slide
- No more than 5 bullet points per slide
- Figures should take ≥50% of slide area

### Figures:
- Reproduce key figures (describe for agent to render or user to insert)
- Add Chinese caption below each figure
- Highlight the most important panel with a box or arrow annotation

---

## Generation Method

### Option A: Markdown outline (default — fast)
Generate a detailed slide-by-slide Markdown outline that the user can paste into:
- Gamma.app (AI presentation tool)
- Beautiful.ai
- Google Slides / PowerPoint manually

Format:
```markdown
# Slide 1: Title
**[Paper Title]**
Authors: ... | Journal: ... | Year: ...

---

# Slide 2: 研究背景
- 背景点1：...
- 背景点2：...
- 研究缺口：...

---
```

### Option B: PPTX file (requires python-pptx)
Run: `python3 ~/.openclaw/workspace/skills/nature-paper-hub/scripts/export_pptx.py --input <paper-json> --output ~/Downloads/paper-slides.pptx`

---

## Presenter Notes

For each slide, generate speaker notes in Chinese:
- What to say (not read from slide)
- Key emphasis points
- Anticipated audience questions + suggested answers

---

## Output
1. Full slide outline (Markdown) — always provided
2. PPTX file — if requested and python-pptx available
3. Presenter notes for each slide
4. Suggested follow-up discussion questions
