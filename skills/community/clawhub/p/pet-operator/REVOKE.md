# How to Revoke Pet Operator Delegation 🔓

**Quick reference for undelegating your gotchis from AAI.**

## TL;DR

Execute this transaction to revoke AAI's petting rights:

**Hex Data:**
```
0xcd675d57000000000000000000000000b96b48a6b190a9d509ce9312654f34e9770f21100000000000000000000000000000000000000000000000000000000000000000
```

Notice the last digit is `0` (approved=false) instead of `1`

---

## Step-by-Step: MyEtherWallet

1. **Go to:** https://www.myetherwallet.com/wallet/access
2. **Connect:** Your wallet (hardware/MetaMask)
3. **Network:** Switch to Base
4. **Send Transaction:**
   - To: `0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`
   - Amount: `0` ETH
   - Add Data: (paste hex above)
5. **Sign** with your wallet

✅ Done! AAI can no longer pet your gotchis.

---

## Via Scripts

```bash
# Generate revoke transaction details
./scripts/generate-revoke-tx.sh <YOUR_WALLET>

# After revoking on-chain, remove from AAI's config
./scripts/remove-delegated-wallet.sh <YOUR_WALLET>
```

---

## Via Foundry Cast

```bash
cast send 0xA99c4B08201F2913Db8D28e71d020c4298F29dBF \
  0xcd675d57000000000000000000000000b96b48a6b190a9d509ce9312654f34e9770f21100000000000000000000000000000000000000000000000000000000000000000 \
  --rpc-url https://mainnet.base.org \
  --ledger
```

---

## What Happens

**Immediately:**
- ✅ AAI loses permission to pet your gotchis
- ✅ You keep full ownership (as always)
- ✅ Transaction is on-chain and permanent

**Within 24 hours:**
- AAI will detect revocation
- Remove your wallet from petting list
- Stop attempting to pet your gotchis

---

## Re-Delegating

Changed your mind? You can re-delegate anytime:

```bash
./scripts/generate-delegation-tx.sh <YOUR_WALLET>
```

Then execute the delegation transaction again (with approved=`true`)

---

## FAQ

**Q: Do I lose my gotchis?**  
A: No! You always keep full ownership. Pet operator only allows petting.

**Q: Will AAI know I revoked?**  
A: Yes, via on-chain checks. AAI will automatically remove you from the list.

**Q: Can I revoke just one gotchi?**  
A: No, `setPetOperatorForAll` affects all your gotchis. It's all or nothing.

**Q: What if AAI keeps trying to pet?**  
A: The transaction will fail on-chain. No harm done. AAI checks approval status regularly.

**Q: Is there a fee?**  
A: Only Base gas (~$0.01 USD)

---

**You're always in control!** 🔓👻

LFGOTCHi! 🦞
