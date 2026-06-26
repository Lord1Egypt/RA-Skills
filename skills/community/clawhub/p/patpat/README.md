# 摸摸头 (PatPat) | AI Co-Regulation Skill for Kids

**PatPat (摸摸头)** is an AI-powered co-regulation skill for children aged 3-8 and their parents. It helps families through emotional storms, post-conflict repair, and everyday emotional practice with a parent-first, child-supportive flow.

「摸摸头 (PatPat)」是一款服务 3-8 岁儿童及家长的 AI 共同调节技能。它覆盖情绪爆发当下、事后修复、以及平时练习三个场景，目标是先托住家长，再托住孩子，帮助家庭形成可重复使用的情绪支持仪式。

---

## ✨ Key Features | 核心特性

- **Three entry modes (三大入口模式)**: `正在爆发` / `刚刚爆发完，想修复` / `平时练习`
- **Minimal-input triage (低负担分流)**: Ask only age band, visible state, and parent regulation when needed.
- **Parent-first coaching (家长优先托举)**: Fixed `Do now / Say now / Avoid now` scaffolding.
- **Repeatable family ritual (固定家庭仪式)**: Emotion creature → body cue → one shared action → next step.
- **Scenario-first guidance (场景优先)**: Common parenting moments map to emotional mechanisms without moralizing.
- **Risk boundaries (风险边界)**: Green / Yellow / Red routing with safer escalation rules.

---

## 🛠️ Repository Structure | 仓库结构

- `VISION.md`: Product vision, core philosophy, pain-point analysis, and experience design.
- `SKILL.md`: Core instruction set for agent behavior and routing.
- `logic/story-engine.md`: Mode-specific narrative rules, age bands, ritual structure, and output contract.
- `logic/emotion-creatures.md`: Emotion-creature-body mapping plus scenario guidance.
- `logic/parent-coach.md`: Canonical parent support guide and single source of truth for all normative parent-facing guidance.

---

## 🤖 Usage | 如何使用

1. Ingest `SKILL.md` into the agent system prompt.
2. Use the `logic/` files as the operational ruleset.
3. Route each request into one of the three entry modes before generating content.
4. Keep responses structured as: parent guidance → child content → shared action → next step.
5. If a frontend needs structured rendering, map the same sections into JSON.

---

## 🎯 Product Intent | 产品意图

PatPat is not here to replace parents or judge them.
It is a lightweight emotional scaffolding tool that helps families:
- get through hard moments with less shame
- repair connection after conflict
- practice emotional skills before the next storm

---

## 📄 License | 开源协议

MIT License. Copyright (c) 2026 gglinux.
