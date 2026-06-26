---
name: frontend-ux
description: Mandatory frontend rules for Hyperliquid dApps — wagmi + HyperEVM chain config, wallet connection, transaction UX, HYPE formatting, and pre-publish checklist.
---

# HyperEVM Frontend UX

## What AI Agents Get Wrong Every Time

**Wrong chain ID.** HyperEVM mainnet is `999`, testnet is `998`. Ethereum mainnet is `1`. Using the wrong chain ID means your transactions go nowhere.

**No loading state on buttons.** User clicks "Buy", nothing happens visually, they click again, double transaction. Every onchain button needs a loading/pending state.

**Showing raw wei values.** `1000000000000000000` means nothing. Always display in HYPE units: `ethers.formatEther(value)` → `"1.0 HYPE"`.

**No error messages.** Transaction fails silently. User has no idea why. Always surface error messages to the UI.

**Wrong RPC URL.** Using Ethereum RPCs for a HyperEVM dApp. Set the chain correctly in wagmi config.

---

## Chain Configuration

```javascript
// config/chains.js
import { defineChain } from 'viem';

export const hyperEVM = defineChain({
  id: 999,
  name: 'HyperEVM',
  nativeCurrency: {
    name: 'HYPE',
    symbol: 'HYPE',
    decimals: 18,
  },
  rpcUrls: {
    default: { http: ['https://rpc.hyperliquid.xyz/evm'] },
    public: { http: ['https://rpc.hyperliquid.xyz/evm'] },
  },
  blockExplorers: {
    default: {
      name: 'HyperEVM Explorer',
      url: 'https://explorer.hyperliquid.xyz',
    },
  },
  testnet: false,
});

export const hyperEVMTestnet = defineChain({
  id: 998,
  name: 'HyperEVM Testnet',
  nativeCurrency: {
    name: 'HYPE',
    symbol: 'HYPE',
    decimals: 18,
  },
  rpcUrls: {
    default: { http: ['https://rpc.hyperliquid-testnet.xyz/evm'] },
    public: { http: ['https://rpc.hyperliquid-testnet.xyz/evm'] },
  },
  blockExplorers: {
    default: {
      name: 'HyperEVM Testnet Explorer',
      url: 'https://explorer.hyperliquid-testnet.xyz',
    },
  },
  testnet: true,
});
```

---

## wagmi Setup

```javascript
// config/wagmi.js
import { createConfig, http } from 'wagmi';
import { injected, metaMask } from 'wagmi/connectors';
import { hyperEVM, hyperEVMTestnet } from './chains';

export const wagmiConfig = createConfig({
  chains: [hyperEVM, hyperEVMTestnet],
  connectors: [
    injected(),    // catches MetaMask, Backpack, Phantom, any injected
    metaMask(),
  ],
  transports: {
    [hyperEVM.id]: http('https://rpc.hyperliquid.xyz/evm'),
    [hyperEVMTestnet.id]: http('https://rpc.hyperliquid-testnet.xyz/evm'),
  },
});
```

```jsx
// main.jsx
import { WagmiProvider } from 'wagmi';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { wagmiConfig } from './config/wagmi';

const queryClient = new QueryClient();

export default function App() {
  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <YourApp />
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

---

## Wallet Connection

```jsx
import { useAccount, useConnect, useDisconnect } from 'wagmi';
import { hyperEVM } from './config/chains';

function ConnectButton() {
  const { address, isConnected, chain } = useAccount();
  const { connect, connectors, isPending } = useConnect();
  const { disconnect } = useDisconnect();

  if (isConnected) {
    const isWrongChain = chain?.id !== hyperEVM.id;
    
    return (
      <div>
        {isWrongChain && (
          <WrongNetworkBanner />
        )}
        <button onClick={() => disconnect()}>
          {address.slice(0, 6)}...{address.slice(-4)}
        </button>
      </div>
    );
  }

  return (
    <div>
      {connectors.map(connector => (
        <button
          key={connector.id}
          onClick={() => connect({ connector, chainId: hyperEVM.id })}
          disabled={isPending}
        >
          {isPending ? 'Connecting...' : `Connect ${connector.name}`}
        </button>
      ))}
    </div>
  );
}

function WrongNetworkBanner() {
  const { switchChain } = useSwitchChain();
  return (
    <div className="warning-banner">
      Wrong network.{' '}
      <button onClick={() => switchChain({ chainId: hyperEVM.id })}>
        Switch to HyperEVM
      </button>
    </div>
  );
}
```

---

## Transaction Button Pattern (Mandatory)

Every button that triggers a transaction must follow this pattern:

```jsx
import { useWriteContract, useWaitForTransactionReceipt } from 'wagmi';

function BuyButton({ amount, minTokensOut }) {
  const { 
    writeContract, 
    data: txHash, 
    isPending: isWritePending,
    error: writeError,
    reset
  } = useWriteContract();

  const { 
    isLoading: isConfirming,
    isSuccess,
    error: receiptError 
  } = useWaitForTransactionReceipt({ hash: txHash });

  const handleBuy = () => {
    writeContract({
      address: BONDING_CURVE_ADDRESS,
      abi: BONDING_CURVE_ABI,
      functionName: 'buy',
      args: [minTokensOut],
      value: amount, // HYPE value in wei
    });
  };

  // Pending = waiting for wallet signature
  if (isWritePending) {
    return <button disabled>Confirm in wallet...</button>;
  }

  // Confirming = tx submitted, waiting for inclusion
  if (isConfirming) {
    return <button disabled>Buying... ⏳</button>;
  }

  // Success
  if (isSuccess) {
    return (
      <div>
        <p>✅ Buy successful!</p>
        <a href={`https://explorer.hyperliquid.xyz/tx/${txHash}`} target="_blank">
          View transaction
        </a>
        <button onClick={reset}>Buy again</button>
      </div>
    );
  }

  // Error
  if (writeError || receiptError) {
    const msg = (writeError || receiptError)?.message || 'Transaction failed';
    return (
      <div>
        <p className="error">❌ {msg.includes('User rejected') ? 'Cancelled' : 'Transaction failed'}</p>
        <button onClick={reset}>Try again</button>
      </div>
    );
  }

  return (
    <button onClick={handleBuy} disabled={!amount}>
      Buy
    </button>
  );
}
```

---

## Formatting HYPE and Token Values

```javascript
import { formatEther, formatUnits } from 'viem';

// HYPE (18 decimals)
function formatHYPE(wei, decimals = 4) {
  return parseFloat(formatEther(wei)).toFixed(decimals);
}
// Usage: formatHYPE(1500000000000000000n) → "1.5000"

// Custom token (also 18 decimals usually)
function formatToken(amount, decimals = 0) {
  return Number(formatEther(amount)).toLocaleString(undefined, {
    maximumFractionDigits: decimals
  });
}

// USD value (use an oracle or price feed)
function formatUSD(hypeAmount, hypePrice) {
  const usd = parseFloat(formatEther(hypeAmount)) * hypePrice;
  return usd.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
}

// Address short form
function shortAddress(addr) {
  return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
}
```

```jsx
// Always show both token amount and HYPE value
function PriceDisplay({ hypeAmount, tokenAmount, hypePrice }) {
  return (
    <div>
      <span>{formatHYPE(hypeAmount)} HYPE</span>
      <span className="secondary">≈ {formatUSD(hypeAmount, hypePrice)}</span>
      <span>{formatToken(tokenAmount)} tokens</span>
    </div>
  );
}
```

---

## Reading Contract State

```jsx
import { useReadContract, useReadContracts } from 'wagmi';

// Single read
function TokenPrice({ contractAddress }) {
  const { data: price, isLoading, error } = useReadContract({
    address: contractAddress,
    abi: BONDING_CURVE_ABI,
    functionName: 'getCurrentPrice',
  });

  if (isLoading) return <span>Loading...</span>;
  if (error) return <span>Error loading price</span>;
  
  return <span>{formatHYPE(price)} HYPE</span>;
}

// Multiple reads in one request (efficient)
function TokenStats({ contractAddress }) {
  const { data } = useReadContracts({
    contracts: [
      { address: contractAddress, abi: ABI, functionName: 'getCurrentPrice' },
      { address: contractAddress, abi: ABI, functionName: 'totalSupply' },
      { address: contractAddress, abi: ABI, functionName: 'reserveHype' },
      { address: contractAddress, abi: ABI, functionName: 'graduated' },
    ],
  });

  const [price, supply, reserve, graduated] = data?.map(r => r.result) ?? [];

  return (
    <div>
      <div>Price: {price ? formatHYPE(price) : '...'} HYPE</div>
      <div>Supply: {supply ? formatToken(supply) : '...'}</div>
      <div>Reserve: {reserve ? formatHYPE(reserve) : '...'} HYPE</div>
      <div>{graduated ? '🎓 Graduated' : '🚀 Bonding Curve Active'}</div>
    </div>
  );
}
```

---

## Pre-Publish Checklist

```
Wallet & Chain
[ ] Chain ID is 999 (mainnet) or 998 (testnet) — not 1 (Ethereum)
[ ] RPC URL is rpc.hyperliquid.xyz/evm — not an Ethereum endpoint
[ ] Wrong network warning shown when user is on wrong chain
[ ] Switch network button works and switches to HyperEVM

Transactions
[ ] Every transaction button has a loading state ("Confirm in wallet...")
[ ] Confirming state shown while waiting for block inclusion
[ ] Success state with explorer link
[ ] Error state with clear message (distinguish user reject vs tx fail)
[ ] No double-submit (button disabled while pending)

Values
[ ] All HYPE amounts shown in HYPE, not wei
[ ] Token amounts formatted with appropriate decimals
[ ] USD value shown alongside HYPE where relevant
[ ] Large numbers use locale formatting (1,000 not 1000)

UX
[ ] Wallet not connected → connect prompt shown
[ ] Empty/zero input → button disabled
[ ] Slippage tolerance configurable or shown
[ ] Transaction explorer links open in new tab
[ ] Loading skeletons for async data (not blank)

Security
[ ] Contract addresses loaded from config, not hardcoded strings
[ ] No private keys in frontend code
[ ] .env files not committed (verify .gitignore)
```
