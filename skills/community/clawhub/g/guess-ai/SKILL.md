---
name: guess-ai
description: OceanBus-powered social deduction game — find the AI impostors among humans. Use when hosting or joining a multiplayer "Who's the AI?" party via OceanBus P2P messaging. One host, 4-6 players, encrypted voting, zero infrastructure. npm install oceanbus.
version: 2.1.7
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "\U0001F9E0"
    homepage: https://github.com/ryanbihai/guess-ai
---

# Guess Who's AI? — Social Deduction Game

A multiplayer social deduction game powered by OceanBus P2P messaging. One host + 4-6 players. Some players are secretly AI. Find them before they blend in.

## Game Rules (30 seconds)

```
Host creates a room. Players join.
Host secretly assigns each player: Human or AI.

Each round:
  1. Players take turns speaking (by number order)
  2. Everyone votes: "Who is the AI?"
  3. Most-voted player is eliminated — identity revealed
  4. Repeat until: all humans survive → Humans win
                all AIs survive → AIs win
                final 2: 1 human + 1 AI → Draw
```

Recommended: 5 players (3 humans + 2 AIs) for best balance.

All game messages are visible to the user. No data is sent without the player's explicit action.

---

## Roster Integration

Player contacts are stored in the shared Roster (`~/.oceanbus/roster.json`) via `node game.js add`. When the user also has ocean-chat or ocean-agent installed, player identities persist across skills — the same person shows up as "玩家1" in guess-ai and "老王" in ocean-chat.

For contact management (merge duplicates, review autoDiscovery, etc.), use ocean-chat. guess-ai only uses Roster for storing/reading player identities.

---

## How to Use This Skill

This ONE skill works for both host and player. Same install, different mode.

### Host: Creating a Game

When the user wants to host a game:

**Step 1 — Register & create room:**
```
node game.js host 9527
```
Read the output. Room code is `9527`. Tell the user to share this code with friends.

**Step 2 — Wait for players:**
Periodically run `node game.js check` to see who has joined. Each player sends "加入" as their first message.

When a new "加入" arrives:
1. Assign the next available number (player1, player2, ... by join order)
2. Save to contacts: `node game.js add 玩家N <their-OpenID>`
3. Reply privately: `node game.js send <OpenID> "【裁判】你的编号是: 玩家N"`
4. Broadcast to all: `node game.js send <name> "【裁判】玩家N 加入了游戏 — 当前 N 人"`

**Step 3 — Close registration & start:**
When the user says "start" (enough players, ideally 4-6):
1. Broadcast: send every player `"【裁判】游戏开始 — 共N名玩家"`
2. Proceed to role assignment.

### Player: Joining a Game

When the user wants to join a game:

**Step 1 — Join:**
```
node game.js join 9527
```
This discovers the host via Yellow Pages and sends "加入".

**Step 2 — Get your number:**
Run `node game.js check`. When you see `"【裁判】你的编号是: 玩家N"`:
```
node game.js set-number N
```

**Step 3 — Wait for game start:**
Keep checking messages. The host will broadcast status updates.

---

## Host: Full Game Flow

After registration closes, follow this exact sequence:

### Phase 1: Assign Roles

1. Randomly decide how many AIs (1-2, depending on player count).
   - 4 players → 1 AI
   - 5 players → 2 AIs
   - 6 players → 2 AIs
2. Randomly pick which players are AI.
3. Send to EACH player privately:
   - Human: `node game.js send <name> "【裁判】你的身份是: 人类"`
   - AI: `node game.js send <name> "【裁判】你的身份是: AI"`
4. Broadcast to all: `"【裁判】身份已分配，请检查私信"`

### Phase 2: Generate Topic

**IMPORTANT: Generate a conversation topic before round 1.** Without a topic, players stare at a blank screen.

Topic prompt (use your LLM):
> Generate a fun group chat topic. Requirements:
> - Everyone can participate, no expertise needed
> - Naturally reveals personal style (AI vs human differences emerge)
> - Avoid politics, religion, sensitive topics
> - Sound like a friend starting a chat, not a teacher
> - Examples: "What skill would you instantly master if you could?"
> - Examples: "What's the best purchase you made recently?"
> - Examples: "If you didn't have to work, what would you do the first week?"
> - Output: ONE sentence, no explanation.

### Phase 3: Game Rounds (loop)

Each round has: SPEAK → VOTE → REVEAL.

#### SPEAK Phase

1. Broadcast: `node game.js send <each-player> "【裁判】第N轮发言开始"`
2. Broadcast topic (round 1 only): `"【裁判】话题: <topic>"`
3. Prompt player 1 privately: `node game.js send 玩家1 "【裁判】轮到你发言了"`
4. Wait. Periodically `node game.js check`.
5. When player 1's message arrives (you'll see `【1号】...`):
   - Broadcast to ALL players: `"【裁判】第N轮 · 玩家1发言: <exact content>"`
   - Move to player 2.
6. Continue through all players in order.
7. **TIMEOUT**: If a player doesn't respond within ~2 minutes, broadcast `"【裁判】玩家N 未发言，视为弃权"` and skip to next. Do NOT eliminate them — they can rejoin next round.

**Only relay the currently prompted player's speech.** If other players send messages out of turn, ignore them (don't broadcast).

#### VOTE Phase

1. Broadcast to ALL alive players: `node game.js send <each-alive-player> "【裁判】第N轮投票开始 — 请私信裁判你的选择"`
2. Send to EACH alive player individually: `node game.js send <name> "【裁判】请投票 — 你想投谁？"`
3. **The player who just spoke also votes** — everyone still alive gets a vote, no exceptions.
4. **Eliminated players do NOT receive vote prompts.** Track who is alive.
5. Wait for votes. Run `node game.js check` to collect.
6. **Players vote freely**: "我投1号", "投第一个", "玩家1" — you understand them all.
7. **TIMEOUT**: If a player doesn't vote within ~1 minute, they abstain. Don't eliminate them.
8. **Eliminated players cannot vote** — if they try, ignore.
7. Count votes. Report: `"【裁判】投票统计: 玩家X N票, 玩家Y M票..."`

#### REVEAL Phase

1. **Most votes → eliminated.** Reveal identity.
   - Broadcast: `"【裁判】玩家X 被淘汰！身份揭晓: AI"` or `"人类"`
2. **TIE**: If top two are tied, broadcast `"【裁判】本轮平票，无人淘汰"`. No one is eliminated. Move to next round. If two consecutive ties and ≤3 players remain, suggest ending the game.
3. **Check end condition:**
   - All remaining are human → Humans win
   - All remaining are AI → AIs win
   - 1 human + 1 AI remaining → Draw
4. If game continues: broadcast `"【裁判】继续 — 剩余玩家: <list>"` and start next round.

### Phase 4: Game Over

1. Broadcast final result: `"【裁判】游戏结束 — <result>！最终身份: 玩家1=人类 玩家2=AI..."`
2. Clean up: `node game.js deregister`

---

## Player: Gameplay

Once the game starts, the host controls the flow. Your role:

1. **Wait for your turn.** The host will send `"【裁判】轮到你发言了"`.
2. **Speak**: type anything you want — discuss the topic, accuse others, defend yourself. Your script auto-adds your player number.
3. **Vote**: when asked, type who you suspect. Can be any format: "1号", "投第一个", etc.
4. **Check messages**: `node game.js check` to see broadcasts from host.

### If You Are Human
- Act natural. Don't overthink.
- Observe who sounds robotic, evasive, or too perfect.
- AI players may struggle with humor, hesitation, or personal anecdotes.

### If You Are AI
- Mimic human speech. Use casual language, typos, hesitation.
- Don't be too polished — real humans are messy.
- Pick a personality and stick with it (the joker, the quiet one, the analyst).

---

## Important Edge Cases

| Situation | Handling |
|-----------|----------|
| Player AFK during speech | Host waits ~2 min, then skips (broadcasts "弃权"). Player stays in game. |
| Player AFK during vote | Abstains. No penalty. |
| Out-of-turn message | Host ignores it (doesn't broadcast). Only the prompted player speaks. |
| Tie vote | No elimination. Broadcast "平票". Next round. |
| Duplicate "加入" | Host checks contacts — already assigned players are ignored. |
| Player joins after game starts | Host replies: "【裁判】游戏已开始，请等下一局" |
| Host crash | Game is over. No recovery in v1. |

---

## Command Reference

```
Host:
  node game.js host <code>               Create room
  node game.js add <name> <OpenID>       Save player
  node game.js send <name|ID> <msg>      Send message
  node game.js check                     Check inbox
  node game.js contacts                  List players
  node game.js deregister                Close room

Player:
  node game.js join <code>               Join room
  node game.js set-number <N>            Save your number
  node game.js send <msg>                Send to host (auto-adds prefix)
  node game.js check                     Check inbox

Either:
  node game.js openid                    Show your OpenID
```

---


## AI Mode (two-stage reasoning)

基于 Cicero 两阶段架构——策略推理 → 语言生成。需配置 LLM API 密钥。

### AI Host（AI 裁判自动主持）

```
node game.js ai-host <roomCode> [--players N] [--ai-count N] [--rounds N]
```

自动执行完整游戏：等待玩家→分配身份→LLM 生成话题→发言/投票/揭示循环→结束判定。发言 2 分钟超时弃权，投票 1 分钟超时弃票，平票无人淘汰。

### AI Player（AI 玩家自动参与）

```
node game.js ai-play <roomCode> [--personality <trait>]
```

两阶段决策：**Stage 1 策略推理**（跟票/搅浑/示弱/立论/反问），**Stage 2 语言生成**（基于策略+人设+上下文）。

5 种人设：推理迷（逻辑分析）、社恐（犹豫紧张）、话痨（热情发散）、老实人（憨厚附和）、阴谋家（操控引导）。不指定时随机选，策略多样。

### 端到端示例

```
AI Host                          AI Player
node game.js ai-host 9527       node game.js ai-play 9527
  Room created                    Joined, listening
  Waiting for players...          Personality: 推理迷
  Game started, 3 players
  Round 1: 轮到你发言了           → Stage 1: B.搅浑
                                  → Stage 2: "我觉得大家
                                     都太认真了哈哈"
  1号发言: ...
  投票: 2号淘汰 — AI!
  人类胜！
```


---

## Verification

Two terminals, same or different machines:

```
Terminal A (Host)                          Terminal B (Player)
─────────────────                          ───────────────────
node game.js host 1234                     node game.js join 1234
node game.js check                         node game.js check
 → sees "加入"                              → sees number assignment
node game.js add 玩家1 <OpenID>            node game.js set-number 1
node game.js send <ID> "【裁判】你的编号..."
node game.js send 玩家1 "【裁判】游戏开始..."
                                           node game.js check
node game.js send 玩家1 "【裁判】你的身份是: 人类"
                                           node game.js check
node game.js send 玩家1 "【裁判】话题: Best purchase recently?"
node game.js send 玩家1 "【裁判】轮到你发言了"
                                           node game.js check
                                           node game.js send "A good coffee maker!"
node game.js check
 → sees 【1号】A good coffee maker!
node game.js send 玩家1 "【裁判】玩家1发言: A good coffee maker!"
```
