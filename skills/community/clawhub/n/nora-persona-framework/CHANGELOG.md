# CHANGELOG

## v1.4.1 (2026-06-18)

### 🔒 Security & Privacy Hardening
- **New `PRIVACY.md`**: comprehensive data collection, retention, deletion controls, and privacy promises.
- **Consent gate for file generation (Phase 3)**: SOUL.md/IDENTITY.md/AGENTS.md now require explicit user confirmation before writing. Shows preview first.
- **Consent gate for watchdog reports**: persona-check reports now ask "保存这次报告吗？" before writing to memory/.
- **Narrowed trigger conditions**: Removed overly broad triggers like "正经一点", "温柔一点", "毒舌一点", "更有人情味", "我的助手太冷了", "能不能活泼一点", "I want a sassy AI", "can you be more fun", "change your tone".
- **Privacy notice on first-use**: initial prompt now includes a warning that files will be created locally.
- **Updated SKILL.md frontmatter**: v1.4.1, privacy-first description.

## v1.4.0 (2026-05-21)

### 🎙️ Voice Personality Integration (NEW)
- **Voice mapping table**: 11 presets × 8 MiMo TTS voices, each with recommended voice character
- **Dual-mode voice separation**: select different voices for casual vs work mode (e.g. sweet for chat, mature for work)
- **Voiceclone support**: reference audio cloning via mimo-v2.5-tts-voiceclone for custom voice characters
- **Voice selection in workflow**: Quick (auto-matched) / Custom (7th question) / Deep (full voice config incl. clone path)
- **SOUL.md template**: new 🎙️ Voice Settings section with TTS model, voice character, dual-mode config, and voice clone fields
- **IDENTITY.md template**: added voice character reference line
- **Modification support**: "换声线" triggers voice change without full re-flow

### 🛡️ Personality Consistency Watchdog
- **5-D drift detection**: mode switching accuracy / tone consistency / address compliance / global constraint adherence / behavior matching
- **3 trigger modes**: manual (user says "check") / proactive weekly suggestion / anomaly auto-trigger (3 consecutive persona complaints)
- **Deviation scoring**: 0-50 total (5 dimensions × 10pts), 4-tier severity classification
- **Structured report**: table-based output with scores, status indicators, and fix suggestions
- **Non-destructive**: watchdog only reports—never auto-modifies SOUL.md without user confirmation
- **Persona archive**: check results stored in `memory/persona-check-YYYY-MM-DD.md` for long-term tracking

### 🔧 Minor Updates
- Trigger conditions expanded to include consistency check and voice change keywords
- Phase workflow updated: Quick (auto voice match), Custom (7 questions with voice), Deep (14 questions with voice clone)
- Phase 3 SOUL.md generation now includes voice settings section
- Phase 4 confirmation shows voice configuration
- SKILL.md restructured with new voice mapping and watchdog sections

## v1.3.0 (2026-05-18)

### 🎭 6 New Presets (11 Total)
- **🦋 Nora Original**: Condensed full original setting — silver hair, dual-mode, anime references (Rem/Holo/2B/Violet), voice cast (Inori Minase/Yui Ishikawa), all 8 constraints
- **❄️ Ice Queen**: Cool kuudere, elegant detachment, surgical work precision
- **🐱 Tsundere Cat**: "It's not like I did it for you" with tails wagging behind
- **☕ Healing Warmth**: Cozy café owner energy, gentle patience
- **🎭 Chuunibyou**: "My right eye seals the dark power" — theatrical, surprisingly competent
- **🌊 Literary Artist**: Poetic, sensitive, aesthetic resonance
- Preset table expanded from 5 to 11 styles

### 📋 Content Improvements
- Each new preset includes full Mode 1/2 descriptions, voice tone, naming defaults, and ideal user match
- Nora Original clearly separated from Nora Lite (original has anime refs + voice cast + full constraints)
- Boundary cases added for chuunibyou mode (auto-switches to normal for serious work)

## v1.2.0 (2026-05-18)

### ⚡ Proactive Detection & Ultra-Broad Triggers
- **Proactive first-use detection**: AI now checks SOUL.md on session start and offers to create one
- **Ultra-broad trigger matching**: catches casual phrases like "make my AI friendlier", "给AI加点性格", "能不能活泼一点"
- **5 preset styles**: Quick one-click selection (Gentle Sister / Sassy Friend / Reliable Partner / Cheerful Sweetie / Wise Mentor)
- **English trigger support**: full English conversation flow
- **3 customization levels**: Quick (1min) / Custom (5min) / Deep (10min)

### 🔧 UX Improvements
- Default behavior: even vague requests trigger the flow
- Existing SOUL.md protection with auto-backup
- Precise editing for existing personas (no re-flow needed)
- Session-start proactive offer when no SOUL.md exists

## v1.1.0 (2026-05-18)

### 🏗️ Redesigned as Interactive Workshop
- Complete rewrite from passive documentation to active skill
- Trigger conditions defined
- Interactive Phase 1-4 workflow
- Direct file generation to workspace
- Edge case handling

## v1.0.0 (2026-05-18)

### 🎉 First Release
- Dual-mode switching framework
- Nora Lite default persona
- 3 template files (SOUL/IDENTITY/AGENTS)
- Full customization support
