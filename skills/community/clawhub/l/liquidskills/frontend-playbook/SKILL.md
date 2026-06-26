---
name: frontend-playbook
description: Complete build-to-production pipeline for HyperEVM dApps — local dev, testnet deploy, mainnet deploy, Vercel config, and go-live checklist.
---

# HyperEVM Frontend Playbook

## The Stack

```
Frontend:   React 18 + Vite
Wallets:    wagmi v2 + viem
Charts:     TradingView lightweight-charts (for price charts)
Realtime:   Supabase Realtime (for live feeds from indexed events)
Data:       Hyperliquid /info API + WebSocket
Deploy:     Vercel (frontend) + HyperEVM (contracts)
```

---

## Phase 0: Local Setup

```bash
npm create vite@latest my-hl-app -- --template react
cd my-hl-app
npm install wagmi viem @tanstack/react-query
npm install @supabase/supabase-js  # if using Supabase
npm install lightweight-charts     # if building price charts
```

Create `.env.local`:
```
VITE_CHAIN_ID=998
VITE_RPC_URL=https://rpc.hyperliquid-testnet.xyz/evm
VITE_CONTRACT_ADDRESS=0x...
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
```

`.gitignore` must include:
```
.env
.env.local
.env.*.local
```

---

## Phase 1: Contract Deployment

### Testnet First (Always)

```bash
# Hardhat
npx hardhat run scripts/deploy.js --network hyperliquid_testnet

# Foundry
forge script script/Deploy.s.sol \
  --rpc-url https://rpc.hyperliquid-testnet.xyz/evm \
  --private-key $PRIVATE_KEY \
  --broadcast \
  -vvvv
```

**After deploy:**
1. Copy contract address → `VITE_CONTRACT_ADDRESS` in `.env.local`
2. Copy ABI → `src/abi/ContractName.json`
3. Verify on testnet explorer: `https://explorer.hyperliquid-testnet.xyz`
4. Run through all contract functions manually in the UI
5. Run automated tests against testnet deployment

### Mainnet Deploy

Only after testnet is solid:

```bash
# Hardhat
npx hardhat run scripts/deploy.js --network hyperliquid_mainnet

# Foundry
forge script script/Deploy.s.sol \
  --rpc-url https://rpc.hyperliquid.xyz/evm \
  --private-key $PRIVATE_KEY \
  --broadcast \
  -vvvv
```

Update production env vars with mainnet contract address.

---

## Phase 2: Vercel Deployment

### Project Setup

```bash
npm install -g vercel
vercel login
vercel  # follow prompts
```

Or connect GitHub repo directly in Vercel dashboard.

### Environment Variables (Vercel Dashboard)

Set these in Vercel → Project → Settings → Environment Variables:

```
VITE_CHAIN_ID=999
VITE_RPC_URL=https://rpc.hyperliquid.xyz/evm
VITE_CONTRACT_ADDRESS=0x<mainnet-address>
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
```

Set separate values for Preview (testnet) vs Production (mainnet) environments.

### vercel.json

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/" }],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" }
      ]
    }
  ]
}
```

The rewrite rule is required for client-side routing (React Router, etc.).

---

## Phase 3: Local Development Flow

```bash
# Start local dev
npm run dev

# Always test against testnet in dev
VITE_CHAIN_ID=998 VITE_RPC_URL=https://rpc.hyperliquid-testnet.xyz/evm npm run dev
```

### Fork Mode (Hardhat)

For testing contract interactions locally with mainnet/testnet state:

```javascript
// hardhat.config.cjs
module.exports = {
  networks: {
    hardhat: {
      forking: {
        url: "https://rpc.hyperliquid-testnet.xyz/evm",
        blockNumber: "latest",
      },
    },
  },
};
```

```bash
npx hardhat node --fork https://rpc.hyperliquid-testnet.xyz/evm
# Then point your frontend at http://localhost:8545
```

---

## Phase 4: Supabase Realtime Setup

For live trade feeds, token launches, and event feeds:

```javascript
// services/supabase.js
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);

// Subscribe to live trades
export function subscribeToTrades(tokenAddress, onTrade) {
  return supabase
    .channel(`trades:${tokenAddress}`)
    .on('postgres_changes', {
      event: 'INSERT',
      schema: 'public',
      table: 'trades',
      filter: `token=eq.${tokenAddress}`,
    }, (payload) => onTrade(payload.new))
    .subscribe();
}
```

```jsx
// components/TradeFeed.jsx
import { useEffect, useState } from 'react';
import { subscribeToTrades } from '../services/supabase';

function TradeFeed({ tokenAddress }) {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    const channel = subscribeToTrades(tokenAddress, (trade) => {
      setTrades(prev => [trade, ...prev].slice(0, 50)); // keep last 50
    });
    return () => channel.unsubscribe();
  }, [tokenAddress]);

  return (
    <div>
      {trades.map(trade => (
        <div key={trade.tx_hash} className={trade.is_buy ? 'buy' : 'sell'}>
          {trade.is_buy ? '🟢 Buy' : '🔴 Sell'} {' '}
          {formatToken(BigInt(trade.token_amount))} for {' '}
          {formatHYPE(BigInt(trade.hype_amount))} HYPE
        </div>
      ))}
    </div>
  );
}
```

---

## Phase 5: Price Charts

```jsx
// components/PriceChart.jsx
import { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

function PriceChart({ candles }) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = createChart(chartRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#0d0d0d' },
        textColor: '#d1d4dc',
      },
      width: chartRef.current.clientWidth,
      height: 300,
      grid: {
        vertLines: { color: '#1c1c1c' },
        horzLines: { color: '#1c1c1c' },
      },
    });

    const series = chartInstance.current.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
    });

    // candles format: [{ time, open, high, low, close }]
    // time must be Unix timestamp in seconds
    series.setData(candles);

    return () => chartInstance.current?.remove();
  }, []);

  useEffect(() => {
    // Update with new candles
  }, [candles]);

  return <div ref={chartRef} />;
}
```

---

## Go-Live Checklist

```
Contracts
[ ] Deployed to HyperEVM mainnet (chain ID 999)
[ ] Verified on https://explorer.hyperliquid.xyz
[ ] Contract address correct in production env vars
[ ] ABI matches deployed contract (not a stale copy)

Frontend
[ ] All .env.local values replaced with production values in Vercel
[ ] VITE_CHAIN_ID=999 in production
[ ] No testnet RPC URLs in production code
[ ] No console.log with sensitive data
[ ] Error boundaries implemented (app doesn't white-screen on JS error)

Wallet
[ ] Tested with MetaMask
[ ] Tested with Backpack
[ ] Tested with Phantom
[ ] Wrong network prompt works and switches to chain ID 999
[ ] Mobile wallet tested (WalletConnect if supported)

Transactions
[ ] Buy flow tested end-to-end on mainnet
[ ] Sell flow tested end-to-end on mainnet
[ ] Error states shown correctly
[ ] Explorer links open correct mainnet explorer

Data
[ ] Supabase indexer running and current
[ ] Live trade feed working
[ ] Price chart loading
[ ] Token stats (price, supply, reserve) loading correctly

Performance
[ ] Lighthouse score > 80
[ ] No unnecessary re-renders (use React DevTools Profiler)
[ ] Images optimized
[ ] Contract reads batched where possible

Security
[ ] No private keys anywhere in codebase
[ ] .env files not in git history
[ ] contract addresses from config, not hardcoded
[ ] CSP headers set (vercel.json)
```
