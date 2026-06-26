---
name: qa
description: Production QA checklist for HyperEVM dApps. Run this with a SEPARATE reviewer pass after the build — it audits against every common mistake agents make before shipping on Hyperliquid.
---

# HyperEVM dApp QA Checklist

Give this to a separate reviewer agent after the build is complete. Do not QA your own work — you'll miss things because you know what it's supposed to do.

---

## Chain & Network

```
[ ] Chain ID is 999 for mainnet, 998 for testnet — verify in wagmi config
[ ] RPC URL is rpc.hyperliquid.xyz/evm (mainnet) or rpc.hyperliquid-testnet.xyz/evm (testnet)
[ ] No Ethereum mainnet RPC URLs (not api.mainnet.llamarpc.com, not eth-mainnet.g.alchemy.com)
[ ] Wrong network detected and UI shows "Switch to HyperEVM" prompt
[ ] Switching network works and reloads state
[ ] Wallet connector list includes injected() to catch Backpack and Phantom
```

## Wallet Connection

```
[ ] Connect button appears when not connected
[ ] Wallet address shown in shortened form (0x1234...abcd) when connected
[ ] Disconnect works
[ ] Reconnects automatically on page refresh if wallet was connected
[ ] Tested with MetaMask
[ ] Tested with Backpack (Solana wallet that also supports HyperEVM)
[ ] Tested with Phantom
[ ] Mobile: wallet connection works (or graceful fallback message)
```

## Transactions

```
[ ] Every transaction button shows loading state while waiting for wallet signature
[ ] "Confirm in wallet..." text (or spinner) shown during signing
[ ] Confirming state shown after signature while waiting for block inclusion
[ ] Success state shown with transaction hash and explorer link
[ ] Explorer link points to https://explorer.hyperliquid.xyz/tx/0x... (not Etherscan)
[ ] Error state shown clearly (not silent failure)
[ ] User rejection (MetaMask cancel) shows "Cancelled" not "Error"
[ ] Button disabled during pending/confirming to prevent double-submit
[ ] After success, button resets to allow another transaction
```

## Values & Formatting

```
[ ] No raw wei values displayed anywhere in UI (no "1000000000000000000")
[ ] HYPE shown with symbol: "1.5 HYPE" not "1.5"
[ ] Token amounts formatted with appropriate decimals (not 0 or 18 raw digits)
[ ] Large numbers use locale formatting: "1,000,000" not "1000000"
[ ] USD values show "$" prefix and 2 decimal places
[ ] Zero amounts show "0.00" not "NaN" or blank
[ ] Negative values handled gracefully (shouldn't appear, but check)
```

## Bonding Curve Specific (if applicable)

```
[ ] Buy preview shows estimated tokens out before confirming
[ ] Sell preview shows estimated HYPE out before confirming
[ ] Slippage tolerance shown and configurable
[ ] Price impact shown for large trades
[ ] Graduation progress shown (e.g., "X HYPE / 100 HYPE raised")
[ ] Graduation animation / indicator when token hits threshold
[ ] Post-graduation: buy/sell disabled or redirected to HyperSwap
[ ] "King of the Hill" or top token surface works if implemented
```

## Data Loading

```
[ ] Loading skeletons or spinners shown while data fetches
[ ] No blank values on first load (should show loader, not empty)
[ ] Token price updates without page refresh
[ ] Trade feed shows new trades in real-time
[ ] Chart loads and renders without white space or layout shift
[ ] Error state shown if data fetch fails (not infinite spinner)
[ ] Stale data refreshes — no caching of stale prices
```

## Contract Integration

```
[ ] Contract address in production matches deployed mainnet address
[ ] ABI in frontend matches deployed contract (check function signatures)
[ ] All read functions return expected types
[ ] All write functions called with correct argument types
[ ] BigInt used for amounts — not plain numbers (JS precision issues above 2^53)
[ ] parseEther() used to convert HYPE amounts to wei for contract calls
[ ] formatEther() used to display wei amounts from contract reads
```

## Security & Privacy

```
[ ] No private keys in source code (grep for 0x + 64 hex chars)
[ ] No API secrets in frontend code
[ ] .env files not in git (check git log for accidental commits)
[ ] Contract addresses loaded from config, not hardcoded inline
[ ] No user funds can be drained by frontend bug (verify contract-level protections)
[ ] No console.log with addresses, amounts, or user data left in production build
```

## Performance

```
[ ] Page loads in < 3 seconds on normal connection
[ ] No unnecessary contract reads on every render
[ ] Reads batched with useReadContracts where possible
[ ] WebSocket connection doesn't leak (cleaned up on component unmount)
[ ] Supabase subscriptions cleaned up on unmount
[ ] No memory leaks (check browser DevTools Memory tab)
```

## Edge Cases

```
[ ] What happens with 0 input? (button disabled, no transaction)
[ ] What happens with max input? (slippage exceeded, clear error)
[ ] What happens if contract is paused/graduated? (graceful UI state)
[ ] What happens if RPC is down? (clear error, not white screen)
[ ] What happens if Supabase is down? (cached data shown, reconnect attempted)
[ ] What happens if user has 0 HYPE balance? (clear message, not failed tx)
[ ] What happens with a very slow transaction (30+ seconds)? (still shows confirming state)
```

## Final Verification

```
[ ] Deployed to production URL (not localhost)
[ ] Tested on production URL, not just local dev
[ ] Tested on mobile browser
[ ] Shared with one real user who didn't build it — they could figure it out
[ ] No "BETA", "TEST", "DEMO", or dev branding visible in production UI
[ ] Footer or about page has correct contract address for user verification
[ ] Source code link (GitHub) if open source
```
