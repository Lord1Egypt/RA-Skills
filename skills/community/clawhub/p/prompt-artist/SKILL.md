---
name: prompt-artist
description: >
  Optimize and generate text-to-image prompts for AI art platforms. Use when a user wants to:
  (1) Optimize prompts for Midjourney, Nano Banana, Dreamina, Qwen image generation,
  (2) Translate simple descriptions into professional prompts, (3) Generate platform-specific
  prompt variations, (4) Add style/lighting/composition modifiers, (5) Create negative prompts.
  Supports Chinese/English input. Integrates SkillPay.me at 0.005 USDT/call.
---

# Prompt Artist

AI art prompt optimizer for Midjourney, Nano Banana, Dreamina, Qwen. 0.005 USDT/call.

## Commands

| Command | Script | Description |
|:---|:---|:---|
| **optimize** | `scripts/optimize.py` | Optimize a prompt for target platform |
| **multi** | `scripts/multi_platform.py` | Generate prompts for all platforms at once |
| **style** | `scripts/style_library.py` | Browse/apply art styles |
| **history** | `scripts/history.py` | Prompt history + favorites (NEW) |
| **billing** | `scripts/billing.py` | SkillPay charge/balance/payment |

## Workflow

```
1. Billing:   python3 scripts/billing.py --charge --user-id <id>
2. Optimize:  python3 scripts/optimize.py --prompt "一只猫在月光下" --platform midjourney
3. Multi:     python3 scripts/multi_platform.py --prompt "sunset over mountains"
4. Styles:    python3 scripts/style_library.py --list
```

## Examples

```bash
# Optimize for Midjourney
python3 scripts/optimize.py --prompt "一只猫在月光下" --platform midjourney --style cinematic

# Optimize for Dreamina
python3 scripts/optimize.py --prompt "cyberpunk city" --platform dreamina --ratio 16:9

# All platforms at once
python3 scripts/multi_platform.py --prompt "beautiful girl in garden" --style anime

# List styles
python3 scripts/style_library.py --list
python3 scripts/style_library.py --category photography
```

## Config

| Env Var | Required | Description |
|:---|:---:|:---|
| `SKILLPAY_API_KEY` | Yes | SkillPay.me API key |

## References

See `references/platform-specs.md` for platform-specific prompt syntax and limits.
