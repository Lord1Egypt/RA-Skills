# 🀄 Mahjong AI — 川麻 AI 出牌助手

> **拍照发牌，秒出建议，防放炮听最宽。**

AI-powered Sichuan Mahjong (川麻/血战到底) assistant. Send a photo of your hand, get optimal discard recommendations instantly.

**[OpenClaw](https://openclaw.ai) Skill** — The first mahjong AI on [ClawHub](https://clawhub.ai)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📸 **Tile Recognition** | AI vision identifies tiles from photos (筒/条/万) |
| 🧮 **Shanten Calculation** | How many steps to tenpai (向听数) |
| 🎯 **Tenpai Analysis** | What tiles you're waiting for + remaining count |
| 💡 **Discard Recommendation** | Which tile to discard, ranked by effectiveness |
| 🛡️ **Safety Scoring** | 🟢 Safe / 🟡 Caution / 🔴 Danger (防放炮) |
| 🏆 **Special Hands** | Qingyise, Qidui, Longqidui, Duiduihu detection |
| 🎲 **Dingque Advice** | Which suit to declare missing at game start |
| 🔄 **Swap-3 Strategy** | Best 3 tiles to swap after dingque |
| 🔍 **Opponent Prediction** | Predict opponent's strategy from their discards |

## 🎮 Sichuan Mahjong Rules (川麻)

- **Tiles**: Only 筒 (dots), 条 (bamboo), 万 (characters) — 108 tiles total
- **Hand**: 13 tiles per player
- **No Chi (吃)**: Only Pon (碰), Kan (杠), Win (胡)
- **Blood War (血战到底)**: Game continues after someone wins
- **Special Hands**: 清一色 (flush), 七对 (7 pairs), 龙七对, 对对胡

## 📦 Installation

### As an OpenClaw Skill
```bash
# Via ClawHub (coming March 21, 2026)
clawhub install mahjong-ai

# Via Git
git clone https://github.com/sceneun1ty/mahjong-ai.git
cp -r mahjong-ai ~/.openclaw/workspace/skills/
```

### Standalone Usage
```bash
# Analyze a hand (14 tiles = discard advice)
python3 scripts/mahjong_analyze.py \
  --hand "1m,2m,3m,5m,5m,3p,4p,7p,8p,9p,2s,3s,4s,6s" \
  --discard "1p,2p,5p,5p,9s,9s"

# Dingque advice (which suit to drop)
python3 scripts/mahjong_analyze.py \
  --hand "1m,3m,5m,2p,3p,4p,5p,7p,8p,1s,2s,9s,9s" \
  --mode dingque

# Swap-3 strategy
python3 scripts/mahjong_analyze.py \
  --hand "1m,3m,5m,2p,3p,4p,5p,7p,8p,1s,2s,9s,9s" \
  --mode swap3

# Predict opponent's strategy
python3 scripts/mahjong_analyze.py \
  --discard "1m,3m,5m,7m,9m,2m,8m,1p,3s" \
  --mode predict --player "上家"
```

## 🎯 Example Output

```
🀄 手牌（14张）：[万] 1万 2万 3万 5万 5万 [筒] 3筒 4筒 7筒 8筒 9筒 [条] 2条 3条 4条 6条

🗑️ 场上已出（6张）

🎯 出牌建议：
=========================================================
⭐ 打 6条  🟡40  → 听 2筒(3) 5筒(2) (5张)
   打 5万  🟡55  → 听 5筒(3) (3张)
   打 1万  🟢60  → 1向听

💡 建议打 6条 — 听5张最多
```

## 📂 Project Structure

```
mahjong-ai/
├── SKILL.md                    # OpenClaw skill definition
├── DEVLOG.md                   # Development log (Chinese)
├── scripts/
│   └── mahjong_analyze.py      # Core analysis engine (~460 lines)
├── references/
│   ├── mahjong_theory.md       # Sichuan mahjong theory & strategy
│   └── tile_visual_guide.md    # Visual tile identification guide
└── README.md
```

## 🔧 Tile Encoding

| Suit | Code | Example | Chinese |
|------|------|---------|---------|
| 万 (Characters) | `m` | `1m` = 一万 | 万子 |
| 筒 (Dots) | `p` | `5p` = 五筒 | 筒子 |
| 条 (Bamboo) | `s` | `9s` = 九条 | 条子 |

## 📊 Test Results

- ✅ 10 random hands: shanten calculation 100% correct
- ✅ 5 special scenarios: all detected (qingyise, qidui, duiduihu)
- ✅ Real game replay: correctly identified 清一色+杠 win
- ✅ Analysis speed: <1 second

## 🛣️ Roadmap

- [x] Core analysis engine
- [x] Dingque advice
- [x] Swap-3 strategy  
- [x] Opponent prediction
- [ ] Guobiao (国标) mahjong rules
- [ ] Guangdong mahjong rules
- [ ] Hong Kong mahjong rules
- [ ] ClawHub official release (March 21)

## 🤝 How It Works with OpenClaw

1. 📸 Take a photo of your hand → send to your OpenClaw assistant
2. 👁️ AI vision recognizes each tile
3. 🧠 Algorithm analyzes optimal play
4. ⚡ Get recommendation in <1 second

Works with any OpenClaw-connected messaging platform (WhatsApp, Telegram, Discord, etc.)

## 📄 License

MIT

## 👤 Author

**Kevin Liu** ([@sceneun1ty](https://github.com/sceneun1ty))

Built with 🦞 [OpenClaw](https://openclaw.ai) + Claude Opus 4

---

_🀄 The first Sichuan Mahjong AI on ClawHub. 拍照发牌，秒出建议。_
