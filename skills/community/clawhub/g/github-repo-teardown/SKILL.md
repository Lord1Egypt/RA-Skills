---
name: github-repo-teardown
metadata:
  author: Junjie Liu / Philosophie AI
  homepage: https://www.linkedin.com/in/junjieliu/
  version: 1.0.0
description: >
  Deep-dive teardown of any GitHub open-source project into a beautifully designed HTML report
  that both product people and engineers can understand. Covers architecture, design decisions,
  comparable repos, and actionable application scenarios. Use this skill whenever the user shares
  a GitHub repo URL and asks to analyze, explain, teardown, or understand a project. Also trigger
  when the user says things like "break down this repo", "how does this project work", "analyze
  this codebase", "walk me through this repo", "what can I learn from this project", "explain
  this open-source project", "拆解一下", "帮我看看这个项目", or "讲解这个 repo". Even if the user
  just drops a GitHub link with a brief "what is this?" — use this skill. Produces a polished
  HTML teardown document covering product logic, technical architecture, and practical takeaways.
---

# GitHub Repo Teardown

## Purpose

Transform any GitHub open-source project into a **product + engineering teardown** — a single
HTML document that explains not just *what* the code does, but *why* it's designed that way
and *what you can learn from it*. The core premise: every technical choice reflects a product
judgment, and every product design requires an architecture to support it.

## When to Trigger

- User shares a GitHub repo URL and asks to analyze / explain / teardown
- User says "break down this repo", "how is this designed", "analyze this project"
- User mentions "teardown", "code walkthrough", "explain this codebase"
- User wants to learn from an open-source project's design
- User drops a GitHub link with even minimal context ("what is this?")

## Configuration

### Language

Output defaults to **English**. If the user's message is in another language (e.g., Chinese,
Japanese, Spanish), match that language for the narrative while keeping technical terms,
code references, and file paths in their original form.

If the user explicitly requests a language (e.g., "write it in Chinese", "用中文写"),
follow that instruction regardless of the default.

## Research Phase

Before writing anything, gather comprehensive information. Follow these steps in order,
spending 5-15 tool calls depending on repo complexity. **Do not skip steps — thin research
produces thin teardowns.**

### Step 1: Repo Overview

- `web_fetch` the GitHub repo main page to get: README content, directory structure,
  stars/forks/language breakdown, license, last commit date
- Pay attention to any Architecture / Design / How It Works sections in the README
- Check for `ARCHITECTURE.md`, `DESIGN.md`, `CONTRIBUTING.md`, or `AGENTS.md`

### Step 2: Deep-Dive Sources (pick 2-4 most useful)

- `web_search` "{repo-name} architecture" or "{repo-name} how it works internally"
- Try fetching DeepWiki: `https://deepwiki.com/{owner}/{repo}` — often has good architecture
  analysis. If unavailable, skip without concern — it's a nice-to-have, not a dependency.
- Look for the project's official blog post, launch announcement, or HN/Reddit discussion
- If the repo has a `/docs` directory or documentation site, fetch key pages

### Step 3: Source Code Reconnaissance

- From README and any architecture docs, identify 3-5 **key source files** — entry points,
  core modules, config files, data models
- `web_fetch` these files directly via raw GitHub URLs:
  `https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}`
- You don't need to read every line — focus on understanding the **relationships between
  files**, the **main abstractions**, and any **clever patterns**
- Check `package.json`, `Cargo.toml`, `pyproject.toml`, or equivalent for dependency insights

### Step 4: Community & Traction Signals

- Scan the Issues tab (sort by most commented or most reacted) to understand:
  - What problems users actually hit
  - What features are most requested
  - Where the project's limitations show
- Check Discussions or recent release notes if available
- Note contributor count and commit frequency — signals project health

### Step 5: Comparable Repos Discovery (CRITICAL — do not skip)

This step directly feeds CH.6 and is one of the highest-value parts of the teardown.

- `web_search` for 2-4 comparable or alternative projects:
  - "{repo-name} vs" or "{repo-name} alternatives"
  - Search by the problem domain: "{problem-the-repo-solves} open source"
- For each comparable repo found, `web_fetch` its GitHub page to get: stars, language,
  approach/architecture, key differentiator
- Look for projects that solve the **same problem differently**, not just forks or clones
- Note: "comparable" includes both direct competitors AND projects with similar architectural
  patterns applied to different domains

### Step 6: Synthesize Before Writing

Before opening any file, mentally organize:
- **One-line definition** of what this project is (test: would a smart non-technical person get it?)
- **The main analogy** you'll use throughout the document
- **3 key design decisions** that make this project interesting
- **The "aha" insight** — what's the non-obvious thing about this project?

## Output Framework

Produce a single HTML file saved to `/mnt/user-data/outputs/` and displayed via `present_files`.

### Document Structure (10 chapters — trim as needed)

```
┌─────────────────────────────────────────────────┐
│  HEADER                                          │
│  - Project name + one-line definition (must fit  │
│    in a single sentence)                         │
│  - Health indicators: Stars / Language / Version  │
│  - Audience tag: who should read this            │
└─────────────────────────────────────────────────┘

CH.1  What Problem Does It Solve?
      - Before vs After (pain → solution)
      - A real-world analogy (non-technical readers should get it)
      - 🔑 Product Insight (why this problem is worth solving)

CH.2  Core Mechanism
      - Explain the core working principle using ONE main analogy
        that runs through the entire document
      - Side-by-side: what the user sees vs what the system does
      - ⚙️ Technical Notes (file names, function names for deep-divers)

CH.3  Architecture & Key Decisions
      - Architecture flow diagram (annotated with the analogy)
      - "Why A not B" decision cards (3-5 key design choices)
      - 🎯 Product-level takeaway for each decision

CH.4  A Single Operation's Full Journey
      - Pick ONE typical user action and trace it through the system
      - Timeline-style: each step shows what happens + what tech is used
      - Technical notes: file paths, function names

CH.5  Product Design Highlights (3-5)
      - Each highlight: Title + Paragraph + Product Insight
      - Tag which ones are "reusable patterns"

CH.6  Comparable Repos & Positioning
      - 2-4 comparable/alternative projects with actual GitHub links
      - For each: what it is, stars, approach, key difference
      - Positioning matrix or comparison table
      - "When to use THIS repo vs THAT repo" decision guide
      - (If insufficient data found in research, say so honestly
        and provide what you have)

CH.7  Risks & Trade-offs
      - 2-3 key limitations or trade-offs
      - "What did it sacrifice to gain its current advantage?"
      - Honest > comprehensive

CH.8  Technical Quick Reference
      - Source tree with annotations
      - Tech stack table
      - Key dependencies explained
      - (Reference section for deep-divers)

CH.9  Where Can This Be Applied? (Application Brainstorm)
      - Three tiers of application (see detailed spec below)
      - Card-based layout, each scenario as an independent block
      - Distinguish "use directly" vs "borrow the pattern"
      - 6-8 cards total (quality over quantity)

CH.10 Portable Takeaways
      - 3-5 transferable insights from this project
      - Numbered, 1-2 sentences each
      - Not a summary — distill into reusable mental models
```

### CH.6 Comparable Repos — Detailed Spec

This chapter is one of the most valuable parts of the teardown. Users want to understand
not just what THIS project does, but how it fits in the landscape.

**Required elements:**
- Each comparable repo gets: Name (linked), Stars count, Language, One-line description,
  Architectural approach, Key differentiator from the subject repo
- A clear "when to use which" decision framework
- Honest assessment — don't artificially favor the subject repo

**Comparison formats (pick the most appropriate):**
- **Table**: Best for 3+ repos with clear feature dimensions
- **Decision tree**: Best when the choice depends on context ("If you need X, use A; if Y, use B")
- **Positioning map**: Best when repos differ on 2 clear axes

**If research yielded thin results:**
- State clearly: "Limited comparable projects found in this specific niche"
- Still provide whatever alternatives exist, even if they're partial overlaps
- Suggest search terms the reader can use to find more

### CH.9 Application Scenarios — Detailed Spec

The most practically valuable chapter. Goal: give readers **specific, actionable** directions,
not vague possibilities.

#### Three Tiers

**Tier A: Use Directly — "What can I do with it tomorrow?"**
- What real problem can this repo solve as-is?
- 2-3 specific scenarios: Who uses it / For what / Expected outcome
- Format: "A [role] can use this to [specific action], eliminating [specific pain point]"

**Tier B: Combine — "What creates a chemical reaction?"**
- What tools/platforms/products does this pair well with for 1+1>2 effects?
- 2-3 combination proposals, each explaining what NEW capability emerges
- Focus on **non-obvious combinations** — obvious ones are already in the README

**Tier C: Borrow the Pattern — "What new products could this inspire?"**
- Extract the core design pattern (not the code) and apply it elsewhere
- Use the format: "If you apply [this pattern] to [another domain], you get..."
- 2-3 cross-domain applications, each specific enough to be a product spec
- This is the most creative tier — encourage bold leaps, but each must land
  on a concrete product form

#### Card Design

Each scenario is an **independent card** with:
- Type tag: 🔧 Use Directly / 🧪 Combine / 💡 Borrow Pattern
- Scenario title
- One-line summary: who + what for
- 2-3 sentences on how to execute

Total: 6-8 cards. Every card must contain genuine insight.

### Chapter Usage Rules

- **Must write**: CH.1, CH.2, CH.3, CH.4, CH.9, CH.10 (core skeleton)
- **Strongly recommended**: CH.5, CH.6, CH.8 (applicable to most repos)
- **Write if warranted**: CH.7 (when there are clear trade-offs)
- Overall principle: **every paragraph must add information — no padding**
- If a chapter would be thin, skip it entirely rather than write filler

## Writing Style Guide

### The Throughline Analogy

- Choose **1 main analogy** per project (e.g., browser-use = "a remote-controlled restaurant order")
- Introduce it in CH.1, extend it through CH.2-CH.4
- The analogy must serve understanding, not decoration
- Avoid: switching to a new unrelated analogy every chapter

### Dual-Layer Narrative

- **Surface layer**: Product logic, business value, user perspective
  (a PM can read just this layer and understand 80%)
- **Deep layer**: File paths, function names, protocol details
  (engineers dig into this layer for implementation specifics)
- Visually separate them: technical details use `code font`, gray backgrounds,
  or "Technical Note" callout boxes

### Insight Callouts

Use colored callout boxes to mark insights:
- 🔵 Blue: Product insight / Design principle
- 🟠 Orange: Technical design lesson
- 🟢 Green: Reusable pattern
- 🟣 Purple: Growth / Business strategy

### Voice & Tone

- Like a senior product advisor giving you a **private briefing**
- Not a textbook, not a blog post — it's "help you understand fast and form judgment"
- Opinions are welcome but labeled: distinguish analysis from fact
- Concise and direct — every sentence earns its place

### Language Conventions

- Narrative in the configured output language (default: English)
- Technical terms stay in English regardless (Daemon, IPC, CDP, Schema, etc.)
- Code snippets and file paths always in original form
- Project-specific terminology in original language with brief explanation on first use

## Visual Design Guide

### Overall Aesthetic

- Light background (#faf9f6 warm white), high readability
- Serif font for headings (Newsreader) — gravitas
- Sans-serif for body (Inter) — modern readability
- Monospace for technical content (JetBrains Mono)
- Max width 820px, centered layout
- Generous whitespace, clear visual hierarchy

### Google Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
```

### Key Components

- **Analogy cards**: White rounded cards, 💡 emoji marker
- **Comparison panels**: Two-column layout (Before vs After, Traditional vs New)
- **Flow diagrams**: Horizontal emoji flow with arrow connectors
- **Decision cards**: 2×2 grid, Q&A format
- **Insight callouts**: Left color bar + tinted background
- **Timeline**: Circle dots + vertical line + content cards
- **Tech reference**: Monospace file tree + tables
- **Scenario cards**: Independent rounded cards, type tag top-left (🔧/🧪/💡)
- **Comparable repo cards**: GitHub-style cards with stars badge, language dot, link

### Responsive Design

- Cards stack vertically on narrow screens
- Side-by-side comparisons collapse to stacked on mobile
- Font sizes adjust for readability

## Quality Checklist

Before delivering, verify:

- [ ] One-line definition is truly one sentence?
- [ ] Main analogy runs through the entire document (not switching per chapter)?
- [ ] Every chapter adds new information (not rephrasing earlier content)?
- [ ] A PM can understand 80% reading only the surface layer?
- [ ] An engineer can find specific files and functions in the deep layer?
- [ ] CH.6 includes actual GitHub links to comparable repos?
- [ ] CH.6 has a clear "when to use which" decision guide?
- [ ] CH.9 scenarios are specific enough (who / what / how all stated)?
- [ ] CH.9 "Borrow Pattern" tier has genuine cross-domain leaps (not "same domain, new name")?
- [ ] CH.10 takeaways are transferable mental models (not a project summary)?
- [ ] Insights are specific to THIS project (not "AI is changing the world" platitudes)?
- [ ] HTML saved to `/mnt/user-data/outputs/` and displayed via `present_files`?

## What This Skill is NOT

- ❌ Not a code review (doesn't read every line)
- ❌ Not a README translation (doesn't repeat existing docs)
- ❌ Not an academic paper (doesn't aim for completeness)
- ❌ Not an SEO article (no filler content)
- ✅ It's a **product teardown** that helps you rapidly understand a project's design wisdom
  and walk away with actionable insights

---

## Credits

Built by **Junjie Liu** at [Philosophie AI](https://philosophie.ai) — where AI proves its
value through real, practical use.

- GitHub: [github.com/jjliu6](https://github.com/jjliu6)
- LinkedIn: [linkedin.com/in/junjieliu](https://linkedin.com/in/junjieliu)
- Products: [philosophie.ai](https://philosophie.ai)

If this skill helped you understand a project better, consider starring it on ClawHub.
