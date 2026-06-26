---
name: holdem-poker
description: "Text-based Texas Hold'em poker game with auto AI players for OpenClaw"
allowed-tools: Bash, Read, Write, Exec
metadata: {"clawdbot":{"requires":{"bins":["node"]}}}
---

# Texas Hold'em Poker Skill

A text-based Texas Hold'em poker game where you control the small blind player, and AI controls other players automatically. Designed for OpenClaw chat interactions.

## Features

- Full Texas Hold'em rules implementation
- Automatic AI players for other positions  
- Card suits displayed with emoji symbols
- Support for multiple game rounds
- Proper betting rounds: pre-flop, flop, turn, river
- Chat-friendly output format

## How to Use

### Start a New Game

```bash
node {baseDir}/scripts/final-game.js
```

### Play Commands

During the game, use these commands:

#### Text Commands
1. **fold** - Fold your hand and exit the current round
2. **check** - Check (pass without betting)
3. **call** - Call the current bet
4. **bet [amount]** - Place a bet (e.g., "bet 5")
5. **allin** - Go all-in with your remaining chips
6. **next** - Start the next round after a game ends
7. **help** - Show available commands
8. **quit** - Exit the game

#### Number Commands (Quick Access)
1. **1** = fold
2. **2** = check  
3. **3** = call
4. **4 N** = bet N (e.g., "4 5" = bet 5)
5. **5** = allin

**Example Usage:**
- `1` (fold) = `fold`
- `2` (check) = `check`
- `3` (call) = `call`
- `4 5` (bet 5) = `bet 5`
- `5` (allin) = `allin`

### QQ Chat Integration

For OpenClaw chat integration, the game is designed to work in a turn-based fashion:

```
User: start
Bot: 🃏 Round 1 - PRE-FLOP
      You: J♦️ 8♣️ | $99
      AI Players: ?? | $98, $100
      Community: A❤️ 2❤️ 3❤️
      Pot: $5 | Current Bet: $2
      Action?

User: call
Bot: You called $1
      AI players act automatically...
```

**AI Player Handling:**
- AI hole cards are saved but hidden as "??" until showdown
- AI decisions are automatic and immediate after your action
- At showdown, all cards are revealed simultaneously
- This creates a fair, turn-based experience perfect for chat interfaces

**Security & Fair Play:**
- AI hole cards are stored securely and never revealed prematurely
- Game state is validated at each step to ensure fair play
- Complete game history is logged for review
- No player can see another's hole cards before showdown

### Game Flow

1. **Pre-flop**: Small blind and big blind forced bets, 2 hole cards dealt
2. **Flop**: 3 community cards revealed, first betting round
3. **Turn**: 4th community card revealed, second betting round
4. **River**: 5th community card revealed, final betting round
5. **Showdown**: Winners determined by best 5-card hand

### Card Notation

- **Suits**: ❤️ (Hearts), ♦️ (Diamonds), ♣️ (Clubs), ♠️ (Spades)
- **Values**: A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2

## Chat Integration Example

```
User: start
Bot: 🃏 Texas Hold'em - Round 1
You (Small Blind): J♦️ 8♣️ | Chips: $99
Community: A❤️ 2❤️ 3❤️
Pot: $5 | Current Bet: $2
Action? [fold/check/call/bet/allin]

User: check
Bot: You checked. AI players act automatically...
```

## Hand Rankings (Strongest to Weakest)

1. Royal Flush - A K Q J 10 same suit
2. Straight Flush - Five consecutive same suit
3. Four of a Kind - Four same values
4. Full House - Three of a kind + pair
5. Flush - Five same suit
6. Straight - Five consecutive different suits
7. Three of a Kind - Three same values
8. Two Pair - Two different pairs
9. One Pair - One pair
10. High Card - Highest card

## API Usage

```javascript
import { PokerGame } from './scripts/simple-game.mjs';

const game = new PokerGame();
const state = game.startNewRound();
console.log(state);

// Player actions
const result = game.playerAction('call');
console.log(result);

// AI acts automatically
const newState = await game.playAIActions();
```

## Configuration

Edit `references/config.json` to change:
- Starting chip amount
- Blind amounts  
- Number of AI players
- Auto-play delay speed

## Files

- `scripts/simple-game.mjs` - Main game logic
- `scripts/game.mjs` - Full interactive CLI version
- `references/config.json` - Game configuration

## 💰 资金追踪与常见问题

### 资金问题记录

#### 🔴 问题：资金总额不匹配

**根本原因：** AI玩家弃牌时，已投入的筹码被错误退还，而不是保留在底池中
**修复方案：** 
- 修改`scripts/final-game.js`中的AI弃牌逻辑
- AI弃牌时，已投入的筹码正确保留在底池
- 确保`player.isActive = false`不会退还已投入筹码

**修复代码：**
```javascript
// 弃牌：保留已投入的筹码在底池
player.isActive = false;
// 已投入的筹码 already in pot, don't return
```

#### ✅ 资金验证公式
**总资金 = 玩家1筹码 + 玩家2筹码 + 玩家3筹码 + 底池**

**验证时机：**
- 每局开始前
- 每次下注后
- 摊牌结算后

**预期结果：** 总资金始终保持初始值（默认$300）

### 🎯 预防措施

#### 资金追踪检查点
1. **盲注阶段：** 验证盲注正确扣除
2. **下注阶段：** 验证每次下注正确转移到底池
3. **弃牌处理：** 验证弃牌玩家已投入筹码保留在底池
4. **摊牌结算：** 验证赢家获得底池，总资金不变

#### 自动化测试
建议添加资金验证测试：
```javascript
function validateTotalChips() {
  const total = players.reduce((sum, p) => sum + p.chips, 0) + pot;
  return total === INITIAL_TOTAL_CHIPS;
}
```

### 🐛 常见Bug及修复

#### 1. 筹码负数问题
**原因：** 下注金额超过玩家筹码
**修复：** 添加筹码不足检查，自动转为全下

#### 2. 底池计算错误
**原因：** 玩家弃牌时筹码退还
**修复：** 弃牌只标记`isActive = false`，不修改筹码

#### 3. AI决策逻辑错误
**原因：** 手牌强度计算不准确
**修复：** 优化`evaluateHandStrength`函数



