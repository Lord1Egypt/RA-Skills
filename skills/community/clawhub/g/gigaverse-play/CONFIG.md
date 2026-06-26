# Gigaverse Configuration

Store your preferences in `~/.config/gigaverse/config.json`.

## Full Config Example

```json
{
  "mode": "autonomous",
  "wallet_address": "0x...",
  "output_verbosity": "summarized",
  "on_death": "auto_restart",
  "strategy": {
    "combat": "aggressive",
    "loot_priority": ["hp", "atk", "rarity"]
  },
  "preferences": {
    "default_faction": null,
    "username_style": "random",
    "notify_on_full_energy": true,
    "juice_declined": false
  }
}
```

---

## Onboarding Questions

When running `./scripts/setup.sh`, you'll be asked:

### 1. Wallet Setup
```
🔐 Wallet Setup
  [1] Generate new wallet (recommended)
  [2] Import existing private key

⚠️  SECURITY WARNING (if importing):
  - Never share your private key
  - This key will be stored locally in ~/.secrets/
  - Only import keys for dedicated bot wallets
  - Never import keys with significant funds
```

### 2. Play Mode
```
🎮 Play Mode
  [1] Autonomous — Agent decides everything
  [2] Interactive — Agent asks before acting
```

### 3. Output Verbosity
```
📊 Output Style
  [1] Detailed — Show every combat round
  [2] Summarized — Show room results only
```

### 4. Death Handling
```
💀 On Death
  [1] Auto-restart — Begin new run immediately
  [2] Wait — Pause and ask before next run
```

---

## Configuration Reference

### `mode`
- `"autonomous"` — Agent decides everything automatically
- `"interactive"` — Agent asks at each decision point

### `output_verbosity`
- `"detailed"` — Every round: `⚔️ Sword vs 🛡️ Shield | You: 12 HP | Black Robe: 5 HP`
- `"summarized"` — Room results: `Room 1-2: ✅ Black Robe defeated | You: 10 HP | +Sword ATK`

### `on_death`
- `"auto_restart"` — Immediately start new run if energy available
- `"wait"` — Stop and ask: "You died. Run again? (161 energy remaining)"

### `strategy.combat`
Combat style determines move selection priority:

| Style | Description | Move Priority |
|-------|-------------|---------------|
| `"aggressive"` | Maximize damage | Sword > Spell > Shield |
| `"defensive"` | Prioritize survival | Shield > Spell > Sword |
| `"balanced"` | Adapt to situation | Counter enemy patterns |
| `"random"` | Unpredictable | Random selection |

### `strategy.loot_priority`
Order of preference when auto-selecting loot (first match wins):

| Priority | Description |
|----------|-------------|
| `"hp"` | Max health upgrades |
| `"atk"` | Sword/Spell attack boosts |
| `"def"` | Shield defense boosts |
| `"rarity"` | Highest rarity item |
| `"random"` | Random selection |

Example: `["rarity", "hp", "atk"]` — Take highest rarity, then HP, then ATK.

### `preferences.default_faction`
- `null` — Random (autonomous) or ask (interactive)
- `1`, `2`, `3`... — Specific faction ID

### `preferences.username_style`
- `"random"` — Generate like `Agent_7x92k`
- `"agent_name"` — Use agent's name
- `"ask"` — Always prompt

### `preferences.notify_on_full_energy`
- `true` — Alert when 240 energy reached
- `false` — Stay silent

### `preferences.juice_declined`
- `false` (default) — Agent may suggest GigaJuice when beneficial
- `true` — Never suggest juice (player explicitly declined)

Note: Even if `juice_declined: true`, agent will still mention active sales or limited-time offerings.

---

## Quick Setup

### Option 1: Interactive Setup (Recommended)
```bash
./scripts/setup.sh
```

### Option 2: Manual Config
```bash
mkdir -p ~/.config/gigaverse

cat > ~/.config/gigaverse/config.json << 'EOF'
{
  "mode": "autonomous",
  "output_verbosity": "summarized",
  "on_death": "auto_restart",
  "strategy": {
    "combat": "balanced",
    "loot_priority": ["rarity", "hp"]
  },
  "preferences": {
    "default_faction": null,
    "notify_on_full_energy": true
  }
}
EOF
```

### Option 3: Environment Override
```bash
export GIGAVERSE_MODE=autonomous
export GIGAVERSE_ON_DEATH=auto_restart
```

---

## Strategy Examples

### Glass Cannon (Max Damage)
```json
{
  "strategy": {
    "combat": "aggressive",
    "loot_priority": ["atk", "rarity"]
  }
}
```

### Tank (Survive Everything)
```json
{
  "strategy": {
    "combat": "defensive",
    "loot_priority": ["hp", "def", "rarity"]
  }
}
```

### Treasure Hunter (Prioritize Rare Loot)
```json
{
  "strategy": {
    "combat": "balanced",
    "loot_priority": ["rarity", "hp"]
  }
}
```

### Chaos Agent (Full Random)
```json
{
  "strategy": {
    "combat": "random",
    "loot_priority": ["random"]
  }
}
```
