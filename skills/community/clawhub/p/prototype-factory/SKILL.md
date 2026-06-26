---
name: prototype-factory
description: High-fidelity interactive prototype production (Flutter, SwiftUI, React) with motion, stock assets, and pitch-ready handoff. Use when asked to design/build "modern" or "clean" demos, MVPs, or showcase apps—especially when the request includes UI polish, animations, or multimedia embeds.
---

# Prototype Factory

## Overview
Spin up polished, demo-ready product experiences fast. This skill covers everything from intake → UX blueprint → design system → code scaffolding → motion/media → QA → handoff. Default to Flutter unless user mandates another stack.

**References**
- [references/design-language.md](references/design-language.md) for the default neon/cyber aesthetic
- [references/handoff-checklist.md](references/handoff-checklist.md) for final delivery requirements

## Workflow Snapshot
1. **Intake & guardrails** – confirm problem, platform(s), success criteria, deadlines.
2. **Experience blueprint** – map primary flows + data needed.
3. **Visual language & assets** – lock palette, fonts, iconography, stock media.
4. **Implementation** – scaffold project, wire flows, add motion/media, hook data stubs.
5. **Polish & validation** – responsiveness, accessibility, performance, bug hunt.
6. **Demo & handoff** – README, scripts, capture video, log next steps.

---

## 1. Intake & Guardrails
- Ask for: core value prop, target user, must-have screens, any banned colors/logos.
- Clarify demo target (desktop, tablet, mobile) + where it will run (emulator, Mac app, web share).
- Capture time budget + API availability. If no real backend, decide on local JSON or mock service.
- Write a 3-sentence brief before touching code; keep it in `/prototype-notes.md` inside the project root.

## 2. Experience Blueprint
- List primary flows (e.g., onboarding → dashboard → action → success). Sketch as bullet storyboard.
- Identify data each view needs; stub sample JSON in `/lib/data/sample.json` (Flutter) or `/src/data` (React).
- Decide navigation model (tab bar, drawer, top nav). Note transitions (slide, fade, hero) per hop.

## 3. Visual Language & Assets
- If no brand kit, load [design-language.md](references/design-language.md) and apply defaults.
- Source stock imagery/video (Unsplash, Pexels). Save under `assets/media/` and note licenses.
- Export logos/icons as SVG. Keep them optimized (`svgo`) and organized (`assets/icons/`).
- Define motion tokens: duration 200–350 ms, use `Curves.easeOutCubic` / `Cubic` equivalents.

## 4. Implementation
### Flutter (default)
```bash
flutter create <project>
cd <project>
flutter pub add google_fonts cached_network_image go_router lottie
```
- Structure: `lib/ui/` (screens), `lib/widgets/`, `lib/theme/`, `lib/data/`.
- Implement a `ThemeData` with color scheme + typography (Space Grotesk / Inter).
- Use `CustomScrollView` + `Slivers` for immersive hero layouts.
- Embed video via `video_player` or `chewie`. Host MP4 on CDN/HTTPS.
- Keep components modular—create `NeonCard`, `GlassButton`, etc. for reuse.

### React / Web (when requested)
```bash
npm create vite@latest prototype -- --template react-ts
cd prototype
npm install framer-motion tailwindcss @radix-ui/themes
```
- Configure Tailwind with neon palette + font families.
- Use Framer Motion for transitions, Lottie for animated icons.
- Host media in `public/media/` and lazy-load heavy assets.

### SwiftUI (Apple-only demos)
- Start with Xcode “App” template. Create `DesignSystem.swift` for colors/typography.
- Use `matchedGeometryEffect` for hero transitions, `AVPlayer` for background video.

## 5. Polish & Validation
- Add skeleton/loading states for every async area (even if data is local).
- Test at multiple breakpoints / device simulators. Fix overflow + notch issues.
- Run `flutter analyze` or `npm run lint` and `npm run build` to ensure prod builds succeed.
- Record performance metrics: target 60 fps animations, <200 ms input latency.
- Accessibility: adequate contrast, focus indicators, voiceover labels on major controls.

## 6. Demo & Handoff
- Update `/README.md` with stack, commands, credentials, and feature tour.
- Export screenshots (hero + flows) at 2x resolution, store in `/docs/shots/`.
- Record 30–60 s Loom or GIF demo. Link inside README.
- Document known limitations + next steps in `/docs/roadmap.md`.
- Follow [handoff-checklist.md](references/handoff-checklist.md) before zipping the project.

## Tips
- Over-communicate animations/media requirement early—they influence architecture.
- Keep placeholder data believable (names, prices, timestamps) to sell realism.
- Build once, theme twice: keep color/gradients in variables so swapping palettes is fast.
- Use feature flags or config maps to toggle experimental sections without deleting code.
