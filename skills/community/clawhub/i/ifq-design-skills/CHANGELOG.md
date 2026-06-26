# Changelog

All notable changes to IFQ Design Skills are tracked here. Versions match the
`SKILL.md` frontmatter and `clawhub.json` manifest.

## 2.4.3 - 2026-04-29

### Templates (12 total — up from 8)
- Added `T-portfolio` (portfolio-essay.html): essay-style personal portfolio with
  5 switchable direction variants (Editorial Serif, Terminal Hacker, Magazine Grid,
  Paper Journal, Minimalist Card) and Currently/Writing/Building structure.
- Added `T-onboarding` (onboarding-flow.html): 5-screen horizontal flow prototype
  with CSS scroll-snap, iPhone device frames, progress indicator, user mindset
  annotations, and data-track attributes for analytics.
- Added `T-diagnosis` (brand-diagnosis.html): brand diagnosis report with 6-dimension
  SVG radar chart, score cards, three direction moodboard cards, and Keep/Fix/Quick Wins
  tri-section. Pure CSS/SVG, no library.
- Added `T-social-multi` (social-multi.html): multi-platform social gallery showing
  X (1200x675), RedNote (1242x1656), IG Square (1080x1080), and WeChat (900x383)
  formats with shared brand tokens.
- Added `GALLERY.html`: standalone template gallery with CSS-only preview cards for
  all 12 templates.
- Updated modeRoutes: M-02 → T-portfolio, M-06 → T-onboarding, M-09 → T-social-multi,
  M-11 → T-diagnosis (old templates kept as fallbacks).

### Agent Ergonomics
- Added Quick Decision Tree to SKILL.md for sub-3-second mode routing.
- Added Anti-Slop Preflight as a hard gate in SKILL.md (7-point checklist from
  references/anti-ai-slop.md).
- Created `scripts/anti-slop-preflight.mjs`: zero-dependency HTML scanner for
  7 AI-slop violations (gradient text, glassmorphism, hero-metric, display font, etc.).
- Added `npm run anti-slop` to package.json and clawhub.json quick_commands.

### ClawHub Marketplace Optimization
- Expanded discovery tags from 10 to 22 (added prototype, mockup, app-design,
  presentation, pitch-deck, branding, logo, typography, print-design, no-code-design,
  ai-design, social-media, changelog).
- Enhanced summary to be more specific about one-turn value proposition.
- Expanded starter_prompts from 5 to 8 (added onboarding, social kit, portfolio).
- Expanded demo_artifacts from 3 to 5 (added infographic, brand protocol).
- Added Windows to supported platforms (macos, linux, windows).

### Eval Suite
- Updated M-02, M-06, M-09, M-11 eval scenarios to reference new template IDs.
- Added 2 new edge-case scenarios: m02-portfolio-five-directions and
  m06-onboarding-multi-screen.

### OpenClaw / ClawHub Spec Compliance
- Added `skillKey` to `metadata.openclaw` for proper hyphenated-name config
  resolution in OpenClaw gateway.
- Added `security_scan` posture block to `clawhub.json` with scanner expectations
  (VirusTotal, ClawScan, static analysis), deny-list rule counts, and bundle
  integrity description.
- Added `changelog` field to `clawhub.json` referencing CHANGELOG.md.
- Added `compatibility` array to `clawhub.json` listing all 8 supported runtimes.
- Expanded discovery tags from 22 to 29 (added portfolio, business-card,
  whitepaper, onboarding, brand-diagnosis, social-kit, motion-design).
- Added `anti-slop` quick command to SKILL.md frontmatter `quick_commands`.
- Expanded SKILL.md `metadata.openclaw.triggers` with 4 new triggers:
  portfolio, onboarding, brand-diagnosis, changelog.
- Enhanced `metadata.security` with deny_list_rules and secret_patterns counts.

### Security Documentation
- Strengthened SECURITY.md with explicit reference to
  `scripts/script-safety-rules.json` (18 deny-list rules across 3 groups).
- Added "Automated Security Gates" section documenting all 6 preflight check
  categories: script safety, secret leakage, package safety, ClawHub cleanliness,
  font loading protocol, and template runtime isolation.
- Added operator hardening guidance for post-download skill inspection.

### Smoke Test
- Added GALLERY.html existence check to verify template gallery is present.
- Added evals.schema.json existence check to verify eval schema is present.
- Total automated checks: 30 → 32.

## 2.4.2 - 2026-04-29

- Added an AI Leverage Loop to the root skill contract so agents optimize for
  early artifacts, visible assumptions, and proof packets instead of setup churn.
- Expanded ClawHub marketplace metadata with activation loop, evidence packet,
  and top-skill signals for human review and agent-readable listing quality.
- Strengthened the template quality contract with first-run evidence and failure
  policy fields.
- Added a ClawHub first-run eval scenario and validation checks that require
  route, template, assumptions, verification, and caveat evidence.
- Updated README and AGENTS onboarding to make first-run expectations and
  ClawHub Top 10 positioning explicit without expanding runtime permissions.

## 2.4.1 - 2026-04-29

- Added a first-run success path to `SKILL.md`, README files, and
  `clawhub.json` so ClawHub installs lead to a verified HTML artifact instead
  of setup churn.
- Added machine-readable marketplace, first-run, and demo artifact metadata to
  the ClawHub manifest.
- Added `evals/evals.schema.json` and tightened eval validation so scenarios
  stay aligned with route references, primary templates, and required preview
  evidence.
- Strengthened smoke checks for SKILL.md disclosure budget, single-line
  metadata, route/template consistency, and ClawHub listing readiness.
- Fixed template mode declarations for routes that reuse hero/comparison
  templates as primary entry points.

## 2.4.0 - 2026-04-28

- Added OpenClaw loader-gating metadata to `SKILL.md` frontmatter, including
  `metadata.openclaw.os`, `requires.bins`, empty env/config gates, and homepage.
- Strengthened ClawHub/OpenClaw smoke checks for manifest/frontmatter parity,
  plugin declarations, workspace-scoped permissions, no-binary bundle posture,
  and package/runtime safety.
- Renamed the root license file from `LICENSE` to `LICENSE.md` because the
  ClawHub web publisher can misclassify extensionless text files as non-text.
- Fixed ClawHub bundle ignore handling for deep `**/personal-asset-index.json`
  paths and added archive verification for private asset indexes.
- Documented the expanded publish preflight so maintainers can verify safety
  before ClawHub upload.

## 2.3.9 - 2026-04-28

- Added a human + agent execution contract centered on making AI higher
  leverage.
- Added machine-readable `modeRoutes` for all 12 modes in the template index.
- Added a zero-dependency eval suite covering all 12 modes plus `preview` and
  `verify:lite` helper scripts for OpenClaw / ClawHub validation.
- Clarified the ClawHub-safe bundle boundary: HTML/SVG/static source in the
  bundle, heavy MP4/GIF/PDF/PPTX automation in the full GitHub repo.
- Added MIT license, notice, contribution, and security documentation.
- Strengthened workflow guidance so agents proceed with reversible assumptions
  instead of blocking on low-risk clarification.
