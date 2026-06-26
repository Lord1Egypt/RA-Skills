# SkillPay Configuration Guide

## Overview

SkillPay is the micropayment system for OpenClaw skills. This guide explains how to configure it for the Hypii Hyperliquid Trader skill.

## Current Status

🔧 **Development Mode** - Skill is functional but billing is simulated

## Configuration Steps

### Step 1: Set Environment Variable (Optional for Dev)

```bash
# For development (no real billing)
export SKILLPAY_API_KEY=""

# For production (when you get API key)
export SKILLPAY_API_KEY="your_actual_api_key_here"
```

### Step 2: Get SkillPay API Key

#### Option A: OpenClaw Discord (Recommended)
1. Join Discord: https://discord.gg/clawd
2. Go to #skill-developers channel
3. Request API key with:
   - Skill name: `hypii-hyperliquid-trader`
   - Developer: [Your name]
   - Pricing: 0.01-0.1 USDT per call
   - Description: AI trading agent for Hyperliquid

#### Option B: GitHub Issue
Create issue at: https://github.com/openclaw/openclaw/issues
```
Title: Request SkillPay API Key
Body:
- Skill: hypii-hyperliquid-trader
- Purpose: Hyperliquid trading automation
- Pricing: Freemium (5 free/day, then 0.01-0.1 USDT)
```

### Step 3: Update Configuration

Once you have API key:

```bash
# Add to your shell profile (.zshrc, .bashrc, etc.)
export SKILLPAY_API_KEY="sk_live_xxxxxxxx"

# Or set for current session only
export SKILLPAY_API_KEY="sk_live_xxxxxxxx"
```

### Step 4: Verify Configuration

```bash
cd skills/hypii-hyperliquid-trader
node -e "
import('./lib/skillpay.js').then(({SkillPayBilling}) => {
  const billing = new SkillPayBilling(process.env.SKILLPAY_API_KEY);
  console.log('Billing Status:', billing.getStatus());
});
"
```

## Pricing Structure

| Feature | Price | Billing Code |
|---------|-------|--------------|
| Free Tier | $0 | `free` |
| Basic Query | 0.01 USDT | `base_call` |
| Strategy | 0.05 USDT | `strategy_execution` |
| Auto Trade | 0.1 USDT | `auto_trade` |

## Development Mode

When `SKILLPAY_API_KEY` is not set:
- ✅ All features work normally
- ✅ Billing is logged but not charged
- ⚠️ Console shows `[DEV MODE]` messages
- 💡 Use for testing before going live

## Production Mode

When `SKILLPAY_API_KEY` is set:
- ✅ Real USDC billing
- ✅ Automatic payment processing
- ✅ Transaction tracking
- 💰 Revenue goes to your wallet

## Troubleshooting

### Issue: "SkillPay API key not configured"
**Solution**: Running in dev mode is normal. Get API key from OpenClaw team.

### Issue: "Payment failed"
**Solution**: Check user's USDC balance on Base chain

### Issue: "Rate limit exceeded"
**Solution**: Contact SkillPay support to increase limits

## Support

- OpenClaw Discord: https://discord.gg/clawd
- ClawHub: https://clawhub.ai
- Email: support@openclaw.ai

## Next Steps

1. ✅ Skill development complete
2. 🔄 Get SkillPay API key
3. 🔄 Test with real billing
4. 🔄 Publish to ClawHub
5. 🔄 Promote to users
