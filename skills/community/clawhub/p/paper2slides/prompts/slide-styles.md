# Slide Style Presets

10 curated visual styles. Select based on purpose and user preference. Preview all styles by opening `style-preview.html` in a browser.

## Light Themes

### 1. Swiss Modern ⭐ (default)

Clean, precise, Bauhaus-inspired. Red accent on white.

- **Display**: `Archivo` (800/900) · **Body**: `Nunito` (400/500) · **Mono**: `JetBrains Mono`
- **Colors**: `--bg: #ffffff` `--accent: #e63312` `--text: #1a1a1a`
- **Signature**: Red left accent bar, large faded section numbers, geometric circle on title slide
- **Best for**: 组会汇报、学术研讨、内部技术分享

### 2. Notebook Tabs

Editorial, organized, tactile. Cream paper with colorful tabs.

- **Display**: `Bodoni Moda` (700) · **Body**: `DM Sans` (400/500)
- **Colors**: `--bg-outer: #2d2d2d` `--bg-page: #f8f6f1` `--tabs: mint/lavender/pink/sky`
- **Signature**: Paper card with shadow, colorful right-edge tabs, binder holes
- **Best for**: 教学课件、读书笔记分享、论文阅读汇报

### 3. Pastel Geometry

Friendly, approachable, modern. Soft pastels.

- **Display/Body**: `Plus Jakarta Sans` (400-800)
- **Colors**: `--bg: #c8d9e6` `--card: #faf9f7` `--pills: pink/mint/purple`
- **Signature**: Rounded card, vertical pills on right edge
- **Best for**: 项目介绍、产品 Demo、轻松场合的学术汇报

### 4. Split Pastel

Playful, creative, modern. Dual-color vertical split.

- **Display/Body**: `Outfit` (400-800)
- **Colors**: `--left: #f5e6dc (peach)` `--right: #e4dff0 (lavender)`
- **Signature**: Two-tone background split, grid overlay, rounded badge pills
- **Best for**: 创意项目展示、实验室内部分享、Poster 风格

### 5. Vintage Editorial

Witty, confident, editorial. Cream with geometric shapes.

- **Display**: `Fraunces` (700/900) · **Body**: `Work Sans` (400/500)
- **Colors**: `--bg: #f5f3ee` `--text: #1a1a1a` `--accent: #e8d4c0`
- **Signature**: Abstract geometric shapes (circle outline + line + dot), bold bordered boxes
- **Best for**: 人文社科论文、综述性报告、设计/艺术相关

### 6. Paper & Ink

Literary, thoughtful, editorial. Warm cream with crimson.

- **Display**: `Cormorant Garamond` · **Body**: `Source Serif 4`
- **Colors**: `--bg: #faf9f7` `--text: #1a1a1a` `--accent: #c41e3a`
- **Signature**: Drop caps, pull quotes, elegant horizontal rules, all-serif typography
- **Best for**: 文献综述、理论性论文、需要阅读感的报告

## Dark Themes

### 7. Bold Signal

Confident, bold, high-impact. Orange card on dark gradient.

- **Display**: `Archivo Black` (900) · **Body**: `Space Grotesk` (400/500)
- **Colors**: `--bg: #1a1a1a gradient` `--card: #FF5722` `--text: #ffffff`
- **Signature**: Bold colored focal card, large section numbers, navigation breadcrumbs
- **Best for**: 学术会议演讲、Pitch/路演、高影响力汇报

### 8. Neon Cyber

Futuristic, techy, confident. Deep navy with neon accents.

- **Display**: `Clash Display` (Fontshare) · **Body**: `Satoshi` (Fontshare)
- **Colors**: `--bg: #0a0f1c` `--accent: #00ffcc` `--magenta: #ff00aa`
- **Signature**: Neon glow effects, grid background, particle systems
- **Best for**: AI/深度学习、技术大会、Hackathon

### 9. Dark Botanical

Elegant, sophisticated, artistic. Black with warm blurs.

- **Display**: `Cormorant` (400/600) · **Body**: `IBM Plex Sans` (300/400)
- **Colors**: `--bg: #0f0f0f` `--text: #e8e4df` `--accents: amber/rose-gold/pink`
- **Signature**: Blurred gradient orbs, thin vertical lines, italic signature typography
- **Best for**: 高端学术报告、邀请制研讨会、跨学科分享

### 10. Terminal Green

Developer-focused, hacker aesthetic. All monospace.

- **Font**: `JetBrains Mono` (monospace only)
- **Colors**: `--bg: #0d1117` `--green: #39d353`
- **Signature**: CRT scan lines, blinking cursor, code syntax styling
- **Best for**: 系统/架构论文、开源项目介绍、极客圈分享

## Common Design Elements

All styles should include these reusable CSS components:

- **`.tag`** — Small uppercase label
- **`.divider`** — Short accent-colored line under headings
- **`.section-num`** — Large faded number in background
- **`.feature-card`** — Bordered card for method modules
- **`.highlight-box`** — Accent-bordered callout for key insights
- **`.data-table`** — Clean comparison table
- **`.metric`** — Pill showing a big number + label
- **`.formula-box`** — Monospace box for equations/pseudocode
- **`.flow`** — Horizontal flow diagram with arrows
- **`.two-col` / `.three-col`** — Grid layouts

## Font DO NOTs

Never use: Inter, Roboto, Arial, system fonts. Avoid generic purple gradients on white (#6366f1). Vary choices across presentations.
