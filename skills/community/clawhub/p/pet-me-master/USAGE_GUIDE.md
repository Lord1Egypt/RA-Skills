# pet-me-master Usage Guide

**The flawless way to use this skill** 👻💜

## Quick Commands

### Check Status
```bash
bash scripts/check-status.sh
```
Shows which gotchis are ready to pet and countdown timers.

### Pet All Ready Gotchis
```bash
bash scripts/pet-all.sh
```
Automatically checks status and pets only the gotchis that are ready.

### Pet Specific Gotchi
```bash
bash scripts/pet.sh <gotchi_id>
```

## Workflows

### Daily Ritual (Recommended)
```bash
# 1. Check status
bash scripts/check-status.sh

# 2. Pet all ready gotchis
bash scripts/pet-all.sh
```

### Conversational (via AAI)
Just say:
- "check petting status" → uses scripts/check-status.sh
- "pet gotchis" → uses scripts/pet-all.sh
- "pet all when ready" → waits for all, then pets

## What Each Script Does

### ✅ check-status.sh
- Shows all gotchis with ready/waiting status
- Displays countdown timers
- Shows last pet time
- **Always accurate** (uses Node.js ethers)

### ✅ pet-all.sh
- Checks which gotchis are ready
- Pets only the ready ones via Bankr
- Skips gotchis on cooldown
- Returns job ID for tracking

### ✅ pet-status.sh
- Internal script (check-status.sh wraps this)
- Most reliable status check
- Uses ethers.js to read contract data

### ⚙️ check-cooldown.sh
- Low-level script (returns raw data)
- Not recommended for direct use

## Gotchi Cooldown Rules

- **Cooldown:** 12 hours after each pet
- **Kinship gain:** +1 per pet
- **Best practice:** Pet twice daily (every 12h)

## Troubleshooting

**"Wrong status showing"**
→ Always use `scripts/check-status.sh` (most reliable)

**"Pet failed"**
→ Check Bankr API key in ~/.openclaw/.env
→ Verify BANKR_API_KEY is set

**"Gotchi still on cooldown"**
→ Trust the check-status.sh output
→ Website (app.aavegotchi.com) may be more up-to-date

## AAI Integration

When I (AAI) check your gotchis, I now use:
1. `scripts/check-status.sh` for accurate status
2. `scripts/pet-all.sh` for petting

No more manual cast calls with broken parsing! ✅

---

**Last updated:** 2026-02-22
**Version:** 2.0.1 (Flawless Edition)
