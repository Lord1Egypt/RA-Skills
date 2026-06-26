# Gotchi Channeling - Security & Access Control

## 🔐 Access Control Rules

### Who Can Channel?

Based on contract behavior and Aavegotchi documentation:

**✅ YOU CAN channel if:**
1. **You OWN the parcel** - Contract checks parcel ownership
2. **OR you have "Access Rights"** - Parcel owner can grant access
3. **The gotchi exists** - Valid gotchi ID on Base chain

**❌ YOU CANNOT channel if:**
1. You don't own the parcel (and don't have access rights)
2. The parcel doesn't have an Aaltar equipped
3. The gotchi is still on cooldown (24h not passed)
4. The contract is paused

---

## ⚠️ Important Security Notes

### 1. Parcel Owner Gets the Rewards

**The Alchemica goes to the PARCEL OWNER, not the gotchi owner!**

From Aavegotchi wiki:
> "Owners of REALM parcels can employ their Aavegotchis **(and those of others)** to farm their REALM parcels"

**This means:**
- ✅ **Your parcel + Your gotchi** = You get all rewards
- ⚠️ **Your parcel + Someone else's gotchi** = You get rewards (they get nothing)
- ❌ **Someone else's parcel + Your gotchi** = They get rewards (you get nothing!)

### 2. Access Rights System

Parcel owners can grant "Access Rights" to other wallets:
- ✅ Allow specific addresses to channel on your parcel
- ✅ Useful for guilds/teams/lending
- ⚠️ Be careful who you grant access to!

### 3. Gotchi Vault Example

From GotchiVault docs:
> "Once in the Vault, anyone borrowing a Vault gotchi can channel on your parcel. You will receive 10% of all alchemica channeled"

**This shows:**
- Borrowed gotchis can channel on your parcel
- You (parcel owner) get the rewards
- Borrower gets a small cut (in Vault's case)

---

## 🎯 Safe Usage Patterns

### ✅ SAFE: Own Both Parcel & Gotchi

```json
{
  "parcelId": "867",
  "gotchiId": "9638",
  "description": "My parcel + My gotchi = I get all rewards"
}
```

**Result:** You get 100% of Alchemica ✅

### ⚠️ CAREFUL: Someone Else's Gotchi on Your Parcel

```json
{
  "parcelId": "867",         // You own this
  "gotchiId": "99999",       // Someone else owns this
  "description": "Their gotchi helps me farm"
}
```

**Result:** 
- You get the Alchemica
- They get kinship increase on their gotchi
- Fair if you have an agreement!

### ❌ DANGEROUS: Your Gotchi on Someone Else's Parcel

```json
{
  "parcelId": "99999",       // Someone else owns this
  "gotchiId": "9638",        // You own this
  "description": "DON'T DO THIS!"
}
```

**Result:**
- They get the Alchemica ❌
- You get nothing except kinship
- Your gotchi goes on 24h cooldown
- **You just gave them free rewards!**

---

## 🛡️ Skill Protection

### Built-in Safety Checks

The skill checks:
1. ✅ **Parcel ownership** - Verifies you own the parcel
2. ✅ **Cooldown status** - Won't channel if not ready
3. ✅ **Transaction simulation** - Bankr validates before sending
4. ✅ **Error handling** - Shows clear error if access denied

### Recommended Configuration

**ONLY configure parcels YOU OWN:**

```json
{
  "channeling": [
    {
      "parcelId": "867",     // ✅ Verify you own this!
      "gotchiId": "9638",    // ✅ Your gotchi or trusted gotchi
      "description": "Confirm ownership before adding"
    }
  ]
}
```

### Verification Steps

**Before adding a parcel to config:**

```bash
# Check parcel ownership
cast call 0x4B0040c3646D3c44B8a28Ad7055cfCF536c05372 \
  "ownerOf(uint256)" 867 \
  --rpc-url https://mainnet.base.org

# Should return YOUR wallet address!
# 0xb96b48a6b190a9d509ce9312654f34e9770f2110
```

**Before adding a gotchi:**

```bash
# Verify it's your gotchi (or you have permission)
cast call 0xA99c4B08201F2913Db8D28e71d020c4298F29dBF \
  "ownerOf(uint256)" 9638 \
  --rpc-url https://mainnet.base.org

# Should return YOUR wallet address!
```

---

## 🎓 Understanding the Flow

### Normal Channeling Flow

```
1. You call channelAlchemica(parcelId, gotchiId, ...)
2. Contract checks: Do you own/have access to parcelId?
   ✅ YES → Continue
   ❌ NO → Revert: "Access Right - Only Owner"
3. Contract checks: Is Aaltar equipped?
   ✅ YES → Continue
   ❌ NO → Revert: "Must equip Altar"
4. Contract checks: Has 24h passed?
   ✅ YES → Continue
   ❌ NO → Revert: "Gotchi can't channel yet"
5. Mint Alchemica to PARCEL OWNER
6. Portion goes to gotchi's pocket
7. Rest is spillover on parcel
```

### Rewards Distribution

```
Total Alchemica Channeled: 250 tokens

Distribution:
- To Parcel Owner: ~125 tokens (50%)
- To Gotchi Pocket: ~75 tokens (30%)
- Spillover on Parcel: ~50 tokens (20%)

(Percentages vary by Aaltar level)
```

**Important:** Even if you channel someone else's gotchi, the rewards go to YOUR wallet (parcel owner)!

---

## 📋 Security Checklist

Before using this skill:

- [ ] ✅ I own all parcels in my config.json
- [ ] ✅ I verified ownership on BaseScan
- [ ] ✅ I understand rewards go to PARCEL owner
- [ ] ✅ I have Aaltars equipped on my parcels
- [ ] ✅ I own the gotchis (or have permission to use them)
- [ ] ✅ I won't channel on parcels I don't own
- [ ] ✅ I secured my Bankr API key
- [ ] ✅ I understand the cooldown system

---

## ⚠️ What Could Go Wrong?

### Scenario 1: Wrong Parcel ID

```bash
# You type wrong parcel ID
./scripts/channel.sh 9638 99999

# Result: ERROR
# "Access Right - Only Owner"
# ✅ Skill protects you - transaction fails
```

### Scenario 2: Someone Else Channels Your Gotchi

```bash
# Someone channels YOUR gotchi on THEIR parcel

# Result:
# - They get Alchemica ❌
# - Your gotchi goes on cooldown ❌
# - You get nothing ❌

# Protection: Only give access to trusted people!
```

### Scenario 3: Access Rights Exploit

If parcel owner grants you access:
- ✅ You CAN channel on their parcel
- ✅ You CAN use your gotchi
- ⚠️ They get the rewards, not you
- ⚠️ Make sure you have an agreement!

---

## 💡 Best Practices

### 1. Own Your Infrastructure
- ✅ Own the parcel
- ✅ Own the gotchi
- ✅ Own the Aaltar
- ✅ Get 100% of rewards

### 2. Verify Ownership
```bash
# Before configuring, verify:
./scripts/verify-ownership.sh 867 9638

# Script checks:
# - You own parcel #867
# - You own gotchi #9638
# - Aaltar is equipped
```

### 3. Monitor Transactions
```bash
# Check recent channels
grep "CHANNELING SUCCESSFUL" /tmp/channeling.log

# Verify rewards went to YOUR wallet
```

### 4. Secure Your Keys
- ✅ Use Bankr (no private keys exposed)
- ✅ Never share Bankr API key
- ✅ Use env vars, not hardcoded keys
- ✅ Rotate keys periodically

---

## 🎯 Summary

**The skill is SAFE when:**
- ✅ You own the parcels you configure
- ✅ You own (or have permission for) the gotchis
- ✅ You verify ownership before adding to config
- ✅ You use Bankr for secure transactions

**The skill PROTECTS you from:**
- ✅ Channeling on parcels you don't own (fails with error)
- ✅ Private key exposure (uses Bankr)
- ✅ Wasting gas on cooldown (checks first)

**The skill CANNOT protect you from:**
- ❌ Configuring wrong parcel IDs (user error)
- ❌ Trusting someone who steals your rewards
- ❌ Social engineering attacks

**Bottom line:** 
**Only configure parcels YOU OWN in config.json!** ✅

---

**Made with 💜 by AAI 👻**

*Channel safely, channel wisely!*

LFGOTCHi! 🔮💜✨
