# OpenClaw Buddy

Generate a unique virtual pet buddy for any user — like Tamagotchi meets gacha!

## Trigger

Activate when the user says: "buddy", "我的buddy", "抽buddy", "生成buddy", "/buddy", or asks about their virtual pet / 虚拟宠物.

## How It Works

Each user gets a **deterministic** buddy based on their unique ID. Same ID always produces the same buddy. The buddy has:

- **Species** (18 types): duck, goose, blob, cat, dragon, octopus, owl, penguin, turtle, snail, ghost, axolotl, capybara, cactus, robot, rabbit, mushroom, chonk
- **Rarity**: common (60%) → uncommon (25%) → rare (10%) → epic (4%) → legendary (1%)
- **Eyes & Hat**: cosmetic accessories (hats only for uncommon+)
- **Stats**: DEBUGGING, PATIENCE, CHAOS, WISDOM, SNARK (higher rarity = higher floor)
- **Shiny**: 1% chance of a shiny variant ✨

## Steps

### 1. Determine User ID

Use the user's unique identifier as the seed. Priority:

1. **Feishu**: Use sender's `open_id` (e.g., `ou_54e680914a71dc8636180ce79cebdca8`) from the message context
2. **Discord/Telegram/etc.**: Use the sender's platform user ID
3. **Manual**: If the user provides a custom string, use that
4. **Fallback**: Use `"anon"`

### 2. Generate Buddy

Run the script with the user ID:

```bash
node ~/.openclaw/workspace/skills/openclaw-buddy/scripts/buddy.js "<user_id>"
```

The script outputs:
- **stdout**: Formatted text card (ready to send as message)
- **stderr**: JSON data (for programmatic use)

### 3. Send the Result

Send the **stdout** output directly to the user. The card includes:
- Species name + rarity stars
- ASCII art sprite
- Eyes & hat info
- Stats with visual bars
- A personality description

### Example Output

```
🐱 猫咪 | 史诗 ★★★★

   /\_/\
  ( ✦   ✦)
  (  ω  )
  (")_(")

🎭 眼睛: ✦ 眼  |  🎩 帽子: 皇冠

📊 属性面板
  调试力 ████████████████░░░░  80
  耐心值 ██████░░░░░░░░░░░░░░  30
  混乱度 ██████████████░░░░░░  65
  智慧值 ██████████░░░░░░░░░░  50
  毒舌值 ████████████████████  95

💬 "一只毒舌但可爱的猫咪"
```

## Notes

- The generation is **deterministic** — same ID always gets the same buddy
- Uses FNV-1a hash + Mulberry32 PRNG, same algorithm family as Claude Buddy but with a different salt (`openclaw-buddy-2026`)
- Buddy results are different from Claude Code's `/buddy` (different salt = different outcomes)
- If a user wants to check someone else's buddy, they can provide that person's ID
- ASCII art looks best in monospace font / code blocks; on platforms without good monospace support, the sprite may look slightly off
