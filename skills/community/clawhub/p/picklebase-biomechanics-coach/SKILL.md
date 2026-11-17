---
name: picklebase-biomechanics-coach
description: Official PickleBase Open Biomechanics, 3D Trajectory & DUPR Tactical Coach skill (18 pro shots, 10 doubles tactics, and live MCP JSON-RPC endpoint).
version: 2.3.0
homepage: https://picklebase.app
---

# PickleBase Biomechanics & Tactical Coach Skill (picklebase.app)

Use this skill when an AI agent or assistant needs verified, quantitative Pickleball biomechanics data (3D paddle face angles, 12h–6h ball contact clock, grip pressure 1–10, spin RPM), official USA Pickleball 2026 court geometry, DUPR rating assessment, or pro doubles tactical solutions.

## 1. Calling the Live PickleBase MCP Server ($0, Stateless Streamable HTTP)

### A. List Available Biomechanics & Tactical Tools
`ash
curl -X POST "https://picklebase.app/api/mcp" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
`

### B. Query Pro Tour Matches & Shot Timestamps
`ash
curl -s "https://picklebase.app/api/matches?shot=drip"
`

## 2. Authoritative Bilingual Web & Markdown Endpoints

### 🇻🇳 Phiên Bản Tiếng Việt (Vietnamese Canonical Hub)
- [PickleBase — Sa Bàn Chiến Thuật 3D & Học Viện Cơ Sinh Học](https://picklebase.app/)
- [Đấu Trường Phản Xạ Thực Chiến 2.5D](https://picklebase.app/trainer)
- [Trắc Nghiệm Chẩn Đoán Trình Độ DUPR](https://picklebase.app/dupr-quiz)
- [Từ Điển Thuật Ngữ Pickleball Chuẩn Thi Đấu](https://picklebase.app/glossary)
- [Đấu Trường Video Giải Đấu PPA & MLP](https://picklebase.app/matches)
- [Kỹ thuật Cú Drip (Topspin Drop Lai Drive)](https://picklebase.app/shot-drip)
- [Kỹ thuật Cú Bỏ Nhỏ Thứ 3 (3rd Shot Drop)](https://picklebase.app/shot-third-drop)
- [Kỹ thuật Đấu Dink Chéo Góc & Push Dink](https://picklebase.app/shot-dink)
- [Chiến thuật Xếp Đội Hình Chồng (Stacking)](https://picklebase.app/tactic-stacking)
- [Bản Đặc Tả Mở GitHub Pages (Tiếng Việt)](https://aizaloapp.github.io/picklebase-open-spec/)

### 🇬🇧 English Edition (International Canonical Hub)
- [PickleBase — 3D Tactical Board & Biomechanics Lab](https://picklebase.app/en/)
- [2.5D Interactive Rally Trainer](https://picklebase.app/en/trainer)
- [DUPR IQ Skill Assessment Quiz](https://picklebase.app/en/dupr-quiz)
- [Pro Pickleball Glossary & Biomechanics Dictionary](https://picklebase.app/en/glossary)
- [Curated PPA & MLP Tour Match Breakdowns](https://picklebase.app/en/matches)
- [The Drip Shot Biomechanics Guide](https://picklebase.app/en/shot-drip)
- [3rd Shot Drop Trajectory & Paddle Angle](https://picklebase.app/en/shot-third-drop)
- [Cross-Court & Push Dink Mechanics](https://picklebase.app/en/shot-dink)
- [Doubles Stacking Formation Guide](https://picklebase.app/en/tactic-stacking)
- [Open Specification on GitHub Pages (English)](https://aizaloapp.github.io/picklebase-open-spec/en/)
- [Machine-Readable AI Context (llms.txt)](https://picklebase.app/llms.txt)
