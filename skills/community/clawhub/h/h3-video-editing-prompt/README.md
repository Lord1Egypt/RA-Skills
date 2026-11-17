# H3 Video Editing Prompt

> A Codex skill for writing **MiniMax H3 Ref2VA editing prompts** that turn a marked source video into the edited target while preserving its performance and timing.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-7C3AED)](SKILL.md)
[![MiniMax H3](https://img.shields.io/badge/MiniMax-H3-FF6B35)](SKILL.md)
[![EN / 中文](https://img.shields.io/badge/Lang-EN%20%2F%20中文-10B981)](SKILL.cn.md)

This skill is **prompt-only**. It rewrites the brief that you hand to H3 — it does not run the model itself, and no wording alone can guarantee a perfect mask, an untouched time window, or frame-accurate lip sync.

---

## ✨ What it does

Given a source video and reference material (and optional audio), this skill writes the six-field `Ref2VA` prompt H3 needs to:

- 🎭 **Replace a masked person** with a reference identity while preserving pose, timing, gaze, expression, and contact
- 👤 **Swap faces** across one or many shots while keeping `<Subject 1>` as the same persistent character
- 👗 **Rebuild costume, hair, or accessories** inside the overlay from a reference picture
- 🧍 **Swap an object** (hand-held prop, foreground element) without changing the source's geometry, contact, or occlusion
- 🪟 **Replace background** or scene elements while keeping the source camera, parallax, and depth order
- 🧹 **Clean up overlays** such as inverted / false-colour / green / blue mats when the internal geometry is still readable
- 🎯 **Persist identity across shot cuts** so a partial, cropped, or edge-of-frame target still carries the same `<Subject 2>` after each `[Shot N]`
- 👄 **Preserve lip sync** through four explicit branches that handle visible mouths, erased mouths, with-audio, and frames-only runtimes

---

## 📦 When to use it

Trigger this skill when the user request looks like:

- *"Masked person replacement"*, *"蒙版换人"*, *"伪彩遮罩"*, *"反相遮罩"*
- *"Ref2VA"*, *"H3 video editing"*, *"reference video editing"*
- *"Cross-shot replacement"*, *"跨镜头替换"*, *"保留同一个人"*
- *"Face replacement that keeps the performance"*, *"换脸并保留表演"*
- *"Lip-sync preservation"*, *"对口型"*, *"口型同步"*, *"lip sync"*

Do **not** trigger this skill for: text-to-video, image-to-video, storyboarding, or video continuation without an overlay.

---

## 🚀 Quick start

Inside Codex, point the assistant at your source video, reference picture, and (if available) audio. The skill will:

1. **Inspect** the assets — duration, fps, mask coverage, audio presence, shot cuts, occluders, off-frame body parts
2. **Assign ownership** — appearance from the reference, pose/motion/gaze/expression from the source frames, optics from the source scene
3. **Pick a lip-sync branch** (see below)
4. **Write the six fields** in the exact official order
5. **Run the quality gate** before delivery

To install this skill into your own Codex environment:

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo wangminrui2022/h3-video-editing-prompt \
  --path . \
  --name h3-video-editing-prompt
```

Or use the Codex in-app skill installer and paste this repo URL:

```
https://github.com/wangminrui2022/h3-video-editing-prompt
```

---

## 🧱 Output contract

The skill emits a single English `text` block with exactly six fields, in this order:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

| Field | Purpose |
|---|---|
| `subject_definitions` | Declares `<Video 1>`, `<Subject 1>`, `<Subject 2>`, and (optionally) `<Picture 1>` / `<Audio 1>` |
| `summary` | One-paragraph task summary, beginning after the task prefix with `The target video is an edited version of <Video 1>.` |
| `retention_analysis` | Per-subject retention policy: `partially_preserved`, `fully_replaced`, `not_carried_over`, etc. |
| `detailed_description` | The shot-by-shot visual brief. **Every measured cut gets its own `[Shot N] At MM:SS.mmm` paragraph.** |
| `overall_soundscape` | Ambient diegetic sound, or `N/A` when the runtime is frames-only |
| `non_diegetic_music` | Score, or `N/A` |

**Target length:** ~7000 characters. **Hard limit:** 10000 characters. Always count before delivery.

Only official reference labels are allowed: `<Video N>`, `<Subject N>`, `<Picture N>`, `<Audio N>`. Never emit `<Theme N>`, `<Topic N>`, `Topic definition`, `Task`, or `Retain analysis`.

---

## 👄 Lip-sync — four branches, pick exactly one

| Branch | When to use it |
|---|---|
| **A.** Source mouth visible **and** original audio reaches H3 | Combine source-frame mouth shapes with audio as a timing check. Do not hand-write phoneme schedules. |
| **B.** Source mouth visible **but** the runtime is frames-only | Preserve the visible mouth trajectory from `<Video 1>`. Reattach the untouched original track after generation. |
| **C.** Mouth erased by an opaque mask, audio does reach H3 | State explicitly that only approximate timing comes from audio. Plan a downstream audio-driven lip-sync or face-reenactment pass. |
| **D.** No usable audio | If the mouth is also erased, write a neutral closed mouth unless the user supplies reliable dialogue + alignment data. Never estimate timing by hand. |

---

## 🧪 Quality gate (checked before delivery)

- [ ] Picture target is classified as person/face-capable character **or** ordinary object; objects have no emotion or lip-sync clauses
- [ ] Audio presence, role, duration, offset, and speaker were verified, not assumed
- [ ] `audio reuse` is used for the final copied signal; `audio reference` is used only for timbre/style
- [ ] The generator's audio-input capability was verified separately from audio-file presence
- [ ] New wording or a different audio timeline is **not** combined with a demand for the source's exact lip shapes
- [ ] Exactly one lip-sync branch is used
- [ ] No hand-written phoneme / syllable / word / character timing appears
- [ ] Six official fields appear in the correct order; only official reference labels are used
- [ ] Masked appearance is rebuilt; masked source appearance is not also retained
- [ ] False-colour or inverted overlays are treated as geometry-readable when internal structure remains visible; their colours and textures are **not** retained
- [ ] `<Subject 1>` is a persistent target across shots, not an anonymous region
- [ ] Every measured cut has its own `[Shot N]` paragraph; post-cut partial appearances retain `<Subject 2>`
- [ ] Frame-edge crops stay crops; off-frame body parts are not pulled into view
- [ ] Lighting, geometry, contact, occlusion, other people, and off-frame parts remain source-owned
- [ ] Any inactive mask interval is enforced by segmentation, not by prompt wording
- [ ] Character count was measured (target ~7000, hard max 10000)

---

## 🗂 File layout

```
h3-video-editing-prompt/
├── README.md                              # This file
├── LICENSE                                # MIT (c) 2026 顶尖王牌程序员
├── SKILL.md                               # Authoritative English spec (read this first)
├── SKILL.cn.md                            # 中文速查 (Chinese cheat sheet)
├── agents/
│   └── openai.yaml                        # Codex / ChatGPT connector metadata
└── references/
    ├── editing-recipes.md                 # Copy-ready skeletons & failure handling
    └── universal-replacement-template.md  # Slot grammar for non-person targets
```

| File | Use it when |
|---|---|
| `SKILL.md` | Authoritative workflow, lip-sync branches, ownership rules, quality gate |
| `SKILL.cn.md` | Fast Chinese reminder of the same rules |
| `references/editing-recipes.md` | You need a ready-to-fill six-field skeleton or are debugging a finished clip |
| `references/universal-replacement-template.md` | The replacement target is not a person (object, costume, background, text, material, light, removal) |

---

## 🧰 Background

Codex doesn't run H3 itself. The value of this skill is the **ownership map**: deciding where each piece of the final frame comes from — the reference picture, the source video, the source scene, or the audio — and writing that map in H3's official `Ref2VA` dialect so the model can act on it.

The skill is deliberately conservative. It will refuse to promise frame-accurate lip sync when the runtime cannot deliver it, and it will route you to a dedicated audio-driven lip-sync or face-reenactment stage when the finished clip is already out of sync.

---

## 🌐 Related skills in this Codex

| Skill | When to reach for it instead |
|---|---|
| [`h3-prompt-writing`](https://github.com/wangminrui2022/h3-prompt-writing) | T2VA, I2VA, FL2VA, L2VA — non-editing H3 prompts |
| [`fight-video-create-skill`](https://github.com/wangminrui2022/fight-video-create-skill) | Combat / action video prompt design |
| [`seedance-combat-director`](https://github.com/wangminrui2022/seedance-combat-director) | Seedance 2.5 generic action prompts |
| [`krea2-megastructure-prompts`](https://github.com/wangminrui2022/krea2-megastructure-prompts) | Mega-scale still-image prompts |
| [`handdrawn-live-video-generator`](https://github.com/wangminrui2022/handdrawn-live-video-generator) | Hand-drawn × live-action hybrid clips |
| [`paper-collage-explainer-generator`](https://github.com/wangminrui2022/paper-collage-explainer-generator) | Paper-collage explainer shorts |
| [`papercraft-stop-motion-explainer`](https://github.com/wangminrui2022/papercraft-stop-motion-explainer) | Papercraft stop-motion explainers |
| [`music-video-subtitle-generator`](https://github.com/wangminrui2022/music-video-subtitle-generator) | Lyric-driven AI music videos |
| [`brand-promo-video-generator`](https://github.com/wangminrui2022/brand-promo-video-generator) | Brand / product promo shorts |
| [`co-op-game-intro-generator`](https://github.com/wangminrui2022/co-op-game-intro-generator) | Two-player co-op menu intros |
| [`3d-animation-short-generator`](https://github.com/wangminrui2022/3d-animation-short-generator) | Stylized 3D animated shorts |
| [`minimalist-product-ad-generator`](https://github.com/wangminrui2022/minimalist-product-ad-generator) | Minimalist e-commerce product films |
| [`cloud-palace-minimax-h3`](https://github.com/wangminrui2022/cloud-palace-minimax-h3) | Cloud-palace / 仙宫 epic imagery |
| [`link-resolver-engine`](https://github.com/wangminrui2022/link-resolver-engine) | Douyin / Bilibili video downloader |
| [`yue2-music`](https://github.com/wangminrui2022/yue2-music) | YuE2 song generation & covers |

---

## 📄 License

[MIT](LICENSE) — Copyright (c) 2026 顶尖王牌程序员.
