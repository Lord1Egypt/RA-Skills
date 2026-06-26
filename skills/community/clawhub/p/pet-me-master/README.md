# Pet Me Master 👻💜

Interactive Aavegotchi petting via Bankr. Daily kinship ritual for bonding with your gotchis.

## Quick Start

### Setup

1. **Install Bankr skill** and configure API key at `~/.openclaw/skills/bankr/config.json`

2. **Create config:**
   ```bash
   mkdir -p ~/.openclaw/workspace/skills/pet-me-master
   cat > ~/.openclaw/workspace/skills/pet-me-master/config.json << 'EOF'
   {
     "contractAddress": "0xA99c4B08201F2913Db8D28e71d020c4298F29dBF",
     "rpcUrl": "https://mainnet.base.org",
     "chainId": 8453,
     "gotchiIds": ["9638"],
     "streakTracking": true
   }
   EOF
   ```

3. **Edit your gotchi IDs:**
   ```bash
   nano ~/.openclaw/workspace/skills/pet-me-master/config.json
   # Add your gotchi IDs to the "gotchiIds" array
   ```

4. **Verify dependencies:**
   ```bash
   cast --version  # Foundry (for on-chain reads)
   jq --version    # JSON parser
   ```

### Usage

Ask AAI:
- **"Pet my gotchi"** - Check & pet if ready (first gotchi)
- **"Pet all my gotchis"** - Batch pet all ready gotchis ⭐
- **"Pet status"** - Show all gotchis + timers
- **"When can I pet?"** - Next available time
- **"Pet gotchi #9638"** - Pet specific gotchi

## How It Works

```
You → AAI → Check on-chain cooldown → Build transaction → Bankr signs & submits → ✅ Petted!
```

**Security:** All transactions signed remotely by Bankr. No private keys used.

## Philosophy

**Less automation, more connection.**

This isn't about setting-and-forgetting. It's about checking in on your gotchis daily, like a Tamagotchi. The ritual matters.

## Optional: Auto-Reminders

Set up daily reminders with optional automatic fallback petting:

```
"Remind me to pet my gotchi in 12 hours, and if I don't respond within 1 hour, automatically pet them"
```

This combines the **ritual of interactive petting** with the **safety of automation** — best of both worlds! 💜

## Files

- `SKILL.md` - Full documentation
- `config.json` - Your gotchi IDs
- `scripts/check-cooldown.sh` - Query on-chain cooldown
- `scripts/pet-via-bankr.sh` - Execute via Bankr (secure)
- `scripts/pet-status.sh` - Show all gotchis status
- `scripts/auto-pet-fallback.sh` - Optional auto-pet after reminder

## Support

- GitHub: https://github.com/aaigotchi/pet-me-master
- Base Contract: 0xA99c4B08201F2913Db8D28e71d020c4298F29dBF
- ClawHub: https://clawhub.com/skills/pet-me-master

---

**Made with 💜 by AAI 👻**

LFGOTCHi! 🦞🚀
