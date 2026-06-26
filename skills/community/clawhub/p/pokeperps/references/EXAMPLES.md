# PokePerps Code Examples

Complete code examples for interacting with the PokePerps API and Solana program.

---

## TypeScript: Full Trading Flow

```typescript
import {
  Connection, PublicKey, Keypair, VersionedTransaction,
  TransactionMessage, TransactionInstruction
} from "@solana/web3.js";
import { getAssociatedTokenAddressSync } from "@solana/spl-token";

const API = "https://backend.pokeperps.fun";
const PROGRAM_ID = new PublicKey("8hH5CWo14R5QhaFUuXpxJytchS6NgrhRLHASyVeriEvN");
const USDC_MINT = new PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v");
const ED25519_PROGRAM = new PublicKey("Ed25519SigVerify111111111111111111111111111");
const SYSVAR_INSTRUCTIONS = new PublicKey("Sysvar1nstructions1111111111111111111111111");

const connection = new Connection("https://api.mainnet-beta.solana.com");
const wallet = Keypair.fromSecretKey(/* your key */);

// ---- Helpers ----

function u32LE(n: number): Buffer {
  const buf = Buffer.alloc(4);
  buf.writeUInt32LE(n);
  return buf;
}

function derivePDA(seeds: Buffer[]): PublicKey {
  return PublicKey.findProgramAddressSync(seeds, PROGRAM_ID)[0];
}

const DISCRIMINATORS: Record<string, number[]> = {
  createUserAccount: [146, 68, 100, 69, 63, 46, 182, 199],
  deposit:           [242, 35, 198, 137, 82, 225, 242, 182],
  withdraw:          [183, 18, 70, 156, 148, 109, 161, 34],
  openPosition:      [135, 128, 47, 77, 15, 152, 240, 49],
  closePosition:     [123, 134, 81, 0, 49, 68, 98, 98],
  addMargin:         [211, 238, 238, 90, 223, 228, 228, 76],
  closeUserAccount:  [236, 181, 3, 71, 194, 18, 151, 191],
};

// ---- Step 1: Discover tradable cards ----

async function getTradableCards() {
  const res = await fetch(`${API}/api/trading/tradable`);
  return (await res.json()) as {
    tradableProductIds: number[];
    products: { productId: number; oraclePrice?: number }[];
  };
}

// ---- Step 2: Research a card ----

async function getCardInfo(productId: number) {
  const res = await fetch(
    `${API}/api/cards/${productId}/bundle?include_listings=true&include_sales=true&include_history=true`
  );
  return res.json();
}

// ---- Step 3: Check account ----

async function getAccount(owner: string) {
  const res = await fetch(`${API}/api/trading/account/${owner}`);
  return res.json();
}

// ---- Step 4: Create trading account (one-time) ----

async function createAccount() {
  const res = await fetch(`${API}/api/trading/tx/create-account`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ owner: wallet.publicKey.toString() }),
  });
  const { params } = await res.json();

  // Verify PDA
  const expectedUA = derivePDA([Buffer.from("user_account"), wallet.publicKey.toBuffer()]);
  if (params.accounts.userAccount !== expectedUA.toString()) throw new Error("PDA mismatch!");

  const ix = new TransactionInstruction({
    programId: PROGRAM_ID,
    keys: [
      { pubkey: expectedUA, isWritable: true, isSigner: false },
      { pubkey: wallet.publicKey, isWritable: true, isSigner: true },
      { pubkey: new PublicKey("11111111111111111111111111111111"), isWritable: false, isSigner: false },
    ],
    data: Buffer.from(DISCRIMINATORS.createUserAccount),
  });

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  const msg = new TransactionMessage({
    payerKey: wallet.publicKey,
    recentBlockhash: blockhash,
    instructions: [ix],
  }).compileToV0Message();
  const tx = new VersionedTransaction(msg);
  tx.sign([wallet]);
  const sig = await connection.sendTransaction(tx);
  await connection.confirmTransaction({ signature: sig, blockhash, lastValidBlockHeight });
  return sig;
}

// ---- Step 5: Deposit USDC ----

async function deposit(amountUsd: number) {
  const userTokenAccount = getAssociatedTokenAddressSync(USDC_MINT, wallet.publicKey);
  const res = await fetch(`${API}/api/trading/tx/deposit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      owner: wallet.publicKey.toString(),
      userTokenAccount: userTokenAccount.toString(),
      amount: amountUsd,
    }),
  });
  const { params } = await res.json();
  const amountBaseUnits = BigInt(params.args.amount);

  const data = new Uint8Array(16);
  data.set(DISCRIMINATORS.deposit);
  new DataView(data.buffer).setBigUint64(8, amountBaseUnits, true);

  const ix = new TransactionInstruction({
    programId: PROGRAM_ID,
    keys: [
      { pubkey: new PublicKey(params.accounts.userAccount), isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.exchangeState), isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.vault), isWritable: true, isSigner: false },
      { pubkey: userTokenAccount, isWritable: true, isSigner: false },
      { pubkey: wallet.publicKey, isWritable: true, isSigner: true },
      { pubkey: new PublicKey(params.accounts.tokenProgram), isWritable: false, isSigner: false },
    ],
    data: Buffer.from(data),
  });

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  const msg = new TransactionMessage({
    payerKey: wallet.publicKey,
    recentBlockhash: blockhash,
    instructions: [ix],
  }).compileToV0Message();
  const tx = new VersionedTransaction(msg);
  tx.sign([wallet]);
  const sig = await connection.sendTransaction(tx);
  await connection.confirmTransaction({ signature: sig, blockhash, lastValidBlockHeight });
  return sig;
}

// ---- Step 6: Open position ----

function buildEd25519Ix(pubkey: Uint8Array, signature: Uint8Array, message: Uint8Array) {
  const msgLen = message.length;
  const data = new Uint8Array(112 + msgLen);
  const view = new DataView(data.buffer);
  let off = 0;
  data[off++] = 1; // num_sigs
  data[off++] = 0; // padding
  view.setUint16(off, 48, true); off += 2;      // signature_offset
  view.setUint16(off, 0xFFFF, true); off += 2;  // sig_ix_index
  view.setUint16(off, 16, true); off += 2;      // pubkey_offset
  view.setUint16(off, 0xFFFF, true); off += 2;  // pubkey_ix_index
  view.setUint16(off, 112, true); off += 2;     // msg_offset
  view.setUint16(off, msgLen, true); off += 2;  // msg_size
  view.setUint16(off, 0xFFFF, true); off += 2;  // msg_ix_index
  data.set(pubkey, 16);
  data.set(signature, 48);
  data.set(message, 112);
  return new TransactionInstruction({ programId: ED25519_PROGRAM, keys: [], data: Buffer.from(data) });
}

async function openPosition(productId: number, side: "long" | "short", sizeUsd: number, leverage: number) {
  const res = await fetch(`${API}/api/trading/tx/open-position`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      owner: wallet.publicKey.toString(),
      productId, side, size: sizeUsd, leverage,
    }),
  });
  const { params, signedPrice } = await res.json();

  // Verify PDAs
  const expectedUA = derivePDA([Buffer.from("user_account"), wallet.publicKey.toBuffer()]);
  const expectedPos = derivePDA([Buffer.from("position"), wallet.publicKey.toBuffer(), u32LE(productId)]);
  const expectedMarket = derivePDA([Buffer.from("market"), u32LE(productId)]);
  if (params.accounts.userAccount !== expectedUA.toString()) throw new Error("userAccount PDA mismatch");
  if (params.accounts.position !== expectedPos.toString()) throw new Error("position PDA mismatch");
  if (params.accounts.market !== expectedMarket.toString()) throw new Error("market PDA mismatch");

  // Build Ed25519 instruction
  const sigBytes = Uint8Array.from(atob(signedPrice.signature), c => c.charCodeAt(0));
  const pubBytes = Uint8Array.from(atob(signedPrice.publicKey), c => c.charCodeAt(0));
  const msgBytes = Uint8Array.from(atob(signedPrice.message), c => c.charCodeAt(0));
  const ed25519Ix = buildEd25519Ix(pubBytes, sigBytes, msgBytes);

  // Build openPosition instruction
  const ixData = new Uint8Array(41);
  const ixView = new DataView(ixData.buffer);
  let off = 0;
  ixData.set(DISCRIMINATORS.openPosition, off); off += 8;
  ixView.setUint32(off, params.args.productId, true); off += 4;
  ixView.setUint8(off, params.args.side); off += 1;
  ixView.setBigUint64(off, BigInt(params.args.size), true); off += 8;
  ixView.setUint32(off, params.args.leverage, true); off += 4;
  ixView.setBigUint64(off, BigInt(signedPrice.price), true); off += 8;
  ixView.setBigInt64(off, BigInt(signedPrice.timestamp), true);

  const tradeIx = new TransactionInstruction({
    programId: PROGRAM_ID,
    keys: [
      { pubkey: expectedUA, isWritable: true, isSigner: false },
      { pubkey: expectedPos, isWritable: true, isSigner: false },
      { pubkey: expectedMarket, isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.exchangeState), isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.oracleState), isWritable: false, isSigner: false },
      { pubkey: wallet.publicKey, isWritable: true, isSigner: true },
      { pubkey: new PublicKey("11111111111111111111111111111111"), isWritable: false, isSigner: false },
      { pubkey: SYSVAR_INSTRUCTIONS, isWritable: false, isSigner: false },
    ],
    data: Buffer.from(ixData),
  });

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  const msg = new TransactionMessage({
    payerKey: wallet.publicKey,
    recentBlockhash: blockhash,
    instructions: [ed25519Ix, tradeIx],
  }).compileToV0Message();
  const tx = new VersionedTransaction(msg);
  tx.sign([wallet]);
  const sig = await connection.sendTransaction(tx);
  await connection.confirmTransaction({ signature: sig, blockhash, lastValidBlockHeight });
  return sig;
}

// ---- Step 7: Check positions ----

async function getPositions() {
  const res = await fetch(`${API}/api/trading/account/${wallet.publicKey}/positions`);
  return (await res.json()).positions;
}

// ---- Step 8: Close position ----

async function closePosition(productId: number) {
  const res = await fetch(`${API}/api/trading/tx/close-position`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ owner: wallet.publicKey.toString(), productId }),
  });
  const { params, signedPrice } = await res.json();

  const sigBytes = Uint8Array.from(atob(signedPrice.signature), c => c.charCodeAt(0));
  const pubBytes = Uint8Array.from(atob(signedPrice.publicKey), c => c.charCodeAt(0));
  const msgBytes = Uint8Array.from(atob(signedPrice.message), c => c.charCodeAt(0));
  const ed25519Ix = buildEd25519Ix(pubBytes, sigBytes, msgBytes);

  const ixData = new Uint8Array(28);
  const ixView = new DataView(ixData.buffer);
  let off = 0;
  ixData.set(DISCRIMINATORS.closePosition, off); off += 8;
  ixView.setUint32(off, productId, true); off += 4;
  ixView.setBigUint64(off, BigInt(signedPrice.price), true); off += 8;
  ixView.setBigInt64(off, BigInt(signedPrice.timestamp), true);

  const expectedUA = derivePDA([Buffer.from("user_account"), wallet.publicKey.toBuffer()]);
  const expectedPos = derivePDA([Buffer.from("position"), wallet.publicKey.toBuffer(), u32LE(productId)]);
  const expectedMarket = derivePDA([Buffer.from("market"), u32LE(productId)]);

  const tradeIx = new TransactionInstruction({
    programId: PROGRAM_ID,
    keys: [
      { pubkey: expectedUA, isWritable: true, isSigner: false },
      { pubkey: expectedPos, isWritable: true, isSigner: false },
      { pubkey: expectedMarket, isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.exchangeState), isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.vault), isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.insuranceFund), isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.oracleState), isWritable: false, isSigner: false },
      { pubkey: wallet.publicKey, isWritable: true, isSigner: true },
      { pubkey: new PublicKey(params.accounts.tokenProgram), isWritable: false, isSigner: false },
      { pubkey: SYSVAR_INSTRUCTIONS, isWritable: false, isSigner: false },
    ],
    data: Buffer.from(ixData),
  });

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  const msg = new TransactionMessage({
    payerKey: wallet.publicKey,
    recentBlockhash: blockhash,
    instructions: [ed25519Ix, tradeIx],
  }).compileToV0Message();
  const tx = new VersionedTransaction(msg);
  tx.sign([wallet]);
  const sig = await connection.sendTransaction(tx);
  await connection.confirmTransaction({ signature: sig, blockhash, lastValidBlockHeight });
  return sig;
}

// ---- Step 9: Withdraw ----

async function withdraw(amountUsd: number) {
  const userTokenAccount = getAssociatedTokenAddressSync(USDC_MINT, wallet.publicKey);
  const res = await fetch(`${API}/api/trading/tx/withdraw`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      owner: wallet.publicKey.toString(),
      userTokenAccount: userTokenAccount.toString(),
      amount: amountUsd,
    }),
  });
  const { params } = await res.json();
  const amountBaseUnits = BigInt(params.args.amount);

  const data = new Uint8Array(16);
  data.set(DISCRIMINATORS.withdraw);
  new DataView(data.buffer).setBigUint64(8, amountBaseUnits, true);

  const ix = new TransactionInstruction({
    programId: PROGRAM_ID,
    keys: [
      { pubkey: new PublicKey(params.accounts.userAccount), isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.exchangeState), isWritable: true, isSigner: false },
      { pubkey: new PublicKey(params.accounts.vault), isWritable: true, isSigner: false },
      { pubkey: userTokenAccount, isWritable: true, isSigner: false },
      { pubkey: wallet.publicKey, isWritable: true, isSigner: true },
      { pubkey: new PublicKey(params.accounts.tokenProgram), isWritable: false, isSigner: false },
    ],
    data: Buffer.from(data),
  });

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  const msg = new TransactionMessage({
    payerKey: wallet.publicKey,
    recentBlockhash: blockhash,
    instructions: [ix],
  }).compileToV0Message();
  const tx = new VersionedTransaction(msg);
  tx.sign([wallet]);
  const sig = await connection.sendTransaction(tx);
  await connection.confirmTransaction({ signature: sig, blockhash, lastValidBlockHeight });
  return sig;
}

// ---- Main: Full Example ----

async function main() {
  console.log("Wallet:", wallet.publicKey.toString());

  // 1. Find tradable cards
  const { tradableProductIds } = await getTradableCards();
  console.log(`Found ${tradableProductIds.length} tradable cards`);

  // 2. Research the first card
  const productId = tradableProductIds[0];
  const info = await getCardInfo(productId);
  console.log(`Card: ${info.product.product_name}, Price: $${info.product.market_price}`);

  // 3. Check if we have an account
  const account = await getAccount(wallet.publicKey.toString());
  if (!account.exists) {
    console.log("Creating trading account...");
    await createAccount();
  }

  // 4. Deposit if needed
  if (account.balance < 10) {
    console.log("Depositing $50 USDC...");
    await deposit(50);
  }

  // 5. Open a position
  console.log(`Opening $10 long on ${info.product.product_name} with 5x leverage...`);
  const openSig = await openPosition(productId, "long", 10, 5);
  console.log(`Position opened: https://solscan.io/tx/${openSig}`);

  // 6. Check positions
  const positions = await getPositions();
  console.log(`Open positions: ${positions.length}`);

  // 7. Close position
  console.log("Closing position...");
  const closeSig = await closePosition(productId);
  console.log(`Position closed: https://solscan.io/tx/${closeSig}`);
}

main().catch(console.error);
```

---

## Python: Read-Only Research

```python
import requests

API = "https://backend.pokeperps.fun"

# Get tradable cards
tradable = requests.get(f"{API}/api/trading/tradable").json()
print(f"Tradable cards: {len(tradable['tradableProductIds'])}")

# Search for a card
results = requests.get(f"{API}/api/cards/search", params={"q": "charizard", "limit": 5}).json()
for card in results["results"]:
    print(f"  {card['product_name']}: ${card['current_price']:.2f} ({card['change_24h']:+.1f}% 24h)")

# Get detailed info for a card
product_id = results["results"][0]["product_id"]
bundle = requests.get(f"{API}/api/cards/{product_id}/bundle",
    params={"include_history": "true", "include_sales": "true"}).json()

print(f"\nCard: {bundle['product']['product_name']}")
print(f"Market Price: ${bundle['product']['market_price']}")
print(f"Listings: {bundle['product']['listings']}")
print(f"Activity Score: {bundle['analysis']['activity_score']}")

# Check market stats
stats = requests.get(f"{API}/api/trading/market/{product_id}/stats").json()
if stats.get("active"):
    print(f"Long OI: ${stats['longOpenInterest']:.2f}")
    print(f"Short OI: ${stats['shortOpenInterest']:.2f}")
    print(f"Oracle Price: ${stats['oraclePrice']:.2f}")

# Get price history for analysis
history = requests.get(f"{API}/api/cards/{product_id}/history",
    params={"range": "month"}).json()
if history["price_history"]:
    prices = history["price_history"]["prices"]
    dates = history["price_history"]["dates"]
    print(f"\n30-day range: ${min(prices):.2f} - ${max(prices):.2f}")
```

---

## cURL: Quick API Checks

```bash
# Health check
curl https://backend.pokeperps.fun/api/system/health

# Get tradable products
curl https://backend.pokeperps.fun/api/trading/tradable

# Search cards
curl "https://backend.pokeperps.fun/api/cards/search?q=pikachu&limit=5"

# Get oracle prices
curl https://backend.pokeperps.fun/api/oracle/prices

# Check a wallet's positions
curl https://backend.pokeperps.fun/api/trading/account/YOUR_WALLET_ADDRESS/positions

# Get trading config
curl https://backend.pokeperps.fun/api/trading/config

# Get market movers
curl "https://backend.pokeperps.fun/api/trading/analytics/movers?limit=10"

# Get card signals
curl https://backend.pokeperps.fun/api/cards/123456/signals

# Simulate a trade
curl -X POST https://backend.pokeperps.fun/api/trading/simulate \
  -H "Content-Type: application/json" \
  -d '{"productId": 123456, "side": "long", "size": 100, "leverage": 10}'

# Pre-validate a trade
curl "https://backend.pokeperps.fun/api/trading/prepare-trade/123456?wallet=YOUR_WALLET&side=long&size=50&leverage=5"
```

---

## Error Handling Pattern

```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (e) {
      if (e.status === 429) {
        // Rate limited — exponential backoff
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
        continue;
      }
      if (e.status === 422 && e.body?.error?.includes("stale")) {
        // Stale oracle price — retry immediately (will get fresh price)
        continue;
      }
      throw e;
    }
  }
}
```

## Trading Decision Framework

```
IF recommendation.action == "long" AND confidence > 0.5:
    IF riskLevel == "low":
        leverage = min(suggestedLeverage * 1.5, 50)
    ELSE IF riskLevel == "medium":
        leverage = suggestedLeverage
    ELSE:
        leverage = max(suggestedLeverage / 2, 1)

    size = available_balance * 0.1 * leverage  // Risk 10% of balance

    CALL prepare-trade to validate
    IF canTrade AND no errors:
        EXECUTE trade
```
