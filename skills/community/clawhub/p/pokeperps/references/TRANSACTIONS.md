# PokePerps On-Chain Transaction Reference

Detailed guide to constructing and submitting Solana transactions for PokePerps.

**Program ID**: `8hH5CWo14R5QhaFUuXpxJytchS6NgrhRLHASyVeriEvN`

---

## PDA Derivation

All accounts are Program Derived Addresses (PDAs).

| Account | Seeds |
|---|---|
| Exchange | `["exchange"]` |
| Vault | `["vault"]` |
| Insurance Fund | `["insurance"]` |
| Oracle | `["oracle"]` |
| Market | `["market", product_id_as_u32_le]` |
| User Account | `["user_account", owner_pubkey_32_bytes]` |
| Position | `["position", owner_pubkey_32_bytes, product_id_as_u32_le]` |

```javascript
const PROGRAM_ID = new PublicKey("8hH5CWo14R5QhaFUuXpxJytchS6NgrhRLHASyVeriEvN");

function derivePDA(seeds) {
  return PublicKey.findProgramAddressSync(seeds, PROGRAM_ID)[0];
}

// Examples
const exchange = derivePDA([Buffer.from("exchange")]);
const vault = derivePDA([Buffer.from("vault")]);
const userAccount = derivePDA([Buffer.from("user_account"), walletPubkey.toBuffer()]);

// For product-specific PDAs, encode product_id as u32 little-endian
function u32LE(n) {
  const buf = Buffer.alloc(4);
  buf.writeUInt32LE(n);
  return buf;
}
const market = derivePDA([Buffer.from("market"), u32LE(productId)]);
const position = derivePDA([Buffer.from("position"), walletPubkey.toBuffer(), u32LE(productId)]);
```

---

## Instruction Discriminators

8-byte Anchor-compatible discriminators:

```
createUserAccount:          [146, 68, 100, 69, 63, 46, 182, 199]
closeUserAccount:           [236, 181, 3, 71, 194, 18, 151, 191]
createMarketPermissionless: [72, 192, 190, 142, 105, 151, 2, 80]
deposit:                    [242, 35, 198, 137, 82, 225, 242, 182]
withdraw:                   [183, 18, 70, 156, 148, 109, 161, 34]
openPosition:               [135, 128, 47, 77, 15, 152, 240, 49]
closePosition:              [123, 134, 81, 0, 49, 68, 98, 98]
addMargin:                  [211, 238, 238, 90, 223, 228, 228, 76]
liquidate:                  [223, 179, 226, 125, 48, 46, 39, 74]
```

---

## Account Orders Per Instruction

Accounts must be in exactly this order:

### createUserAccount

| # | Name | Writable | Signer |
|---|------|----------|--------|
| 0 | userAccount (PDA) | yes | no |
| 1 | owner | yes | yes |
| 2 | systemProgram | no | no |

### deposit

| # | Name | Writable | Signer |
|---|------|----------|--------|
| 0 | userAccount (PDA) | yes | no |
| 1 | exchangeState (PDA) | yes | no |
| 2 | vault (PDA) | yes | no |
| 3 | userTokenAccount | yes | no |
| 4 | owner | yes | yes |
| 5 | tokenProgram | no | no |

### withdraw

| # | Name | Writable | Signer |
|---|------|----------|--------|
| 0 | userAccount (PDA) | yes | no |
| 1 | exchangeState (PDA) | yes | no |
| 2 | vault (PDA) | yes | no |
| 3 | userTokenAccount | yes | no |
| 4 | owner | yes | yes |
| 5 | tokenProgram | no | no |

### openPosition

| # | Name | Writable | Signer |
|---|------|----------|--------|
| 0 | userAccount (PDA) | yes | no |
| 1 | position (PDA) | yes | no |
| 2 | market (PDA) | yes | no |
| 3 | exchangeState (PDA) | yes | no |
| 4 | oracleState (PDA) | no | no |
| 5 | owner | yes | yes |
| 6 | systemProgram | no | no |
| 7 | instructionsSysvar | no | no |

### closePosition

| # | Name | Writable | Signer |
|---|------|----------|--------|
| 0 | userAccount (PDA) | yes | no |
| 1 | position (PDA) | yes | no |
| 2 | market (PDA) | yes | no |
| 3 | exchangeState (PDA) | yes | no |
| 4 | vault (PDA) | yes | no |
| 5 | insuranceFund (PDA) | yes | no |
| 6 | oracleState (PDA) | no | no |
| 7 | owner | yes | yes |
| 8 | tokenProgram | no | no |
| 9 | instructionsSysvar | no | no |

### addMargin

| # | Name | Writable | Signer |
|---|------|----------|--------|
| 0 | userAccount (PDA) | yes | no |
| 1 | position (PDA) | yes | no |
| 2 | owner | yes | yes |

---

## Instruction Data Encoding

All instructions start with their 8-byte discriminator, followed by args in little-endian:

### deposit / withdraw

```
[discriminator: 8 bytes] [amount: u64]
```

Amount in USDC base units (6 decimals): $100 = `100_000_000`

### openPosition

```
[discriminator: 8 bytes] [productId: u32] [side: u8] [size: u64] [leverage: u32] [price: u64] [timestamp: i64]
```

- `side`: 0 = long, 1 = short
- `size`: USDC base units (6 decimals)
- `price`: scaled by 10^8 (so $45.67 = `4_567_000_000`)
- `timestamp`: unix seconds (from `signedPrice` response)

Total: 41 bytes (8 + 4 + 1 + 8 + 4 + 8 + 8)

### closePosition

```
[discriminator: 8 bytes] [productId: u32] [price: u64] [timestamp: i64]
```

Total: 28 bytes (8 + 4 + 8 + 8)

### addMargin

```
[discriminator: 8 bytes] [productId: u32] [amount: u64]
```

Total: 20 bytes (8 + 4 + 8)

---

## Ed25519 Signed Price Transaction

For `openPosition` and `closePosition`, the transaction **MUST** include an Ed25519SigVerify precompile instruction at index 0. The on-chain program verifies that the oracle price was signed by the authorized oracle keypair.

### Ed25519SigVerify Instruction Data Layout (112 + N bytes)

```
Offset  Size  Field
------  ----  -----
0       1     num_sigs = 1
1       1     padding = 0
2       2     signature_offset = 48 (u16 LE)
4       2     signature_instruction_index = 0xFFFF (u16 LE)
6       2     public_key_offset = 16 (u16 LE)
8       2     public_key_instruction_index = 0xFFFF (u16 LE)
10      2     message_data_offset = 112 (u16 LE)
12      2     message_data_size = 20 (u16 LE)
14      2     message_instruction_index = 0xFFFF (u16 LE)
16      32    public_key (from signedPrice.publicKey, base64-decoded)
48      64    signature (from signedPrice.signature, base64-decoded)
112     20    message (from signedPrice.message, base64-decoded)
```

The signed message is 20 bytes: `[product_id: u32] [price: u64] [timestamp: i64]`

### Building the Ed25519 Instruction

```javascript
const ED25519_PROGRAM = new PublicKey("Ed25519SigVerify111111111111111111111111111");

function buildEd25519Ix(pubkey, signature, message) {
  const msgLen = message.length;
  const data = new Uint8Array(112 + msgLen);
  const view = new DataView(data.buffer);

  let off = 0;
  data[off++] = 1;    // num_sigs
  data[off++] = 0;    // padding

  // Ed25519SignatureOffsets (14 bytes)
  view.setUint16(off, 48, true); off += 2;       // signature_offset
  view.setUint16(off, 0xFFFF, true); off += 2;   // sig_ix_index
  view.setUint16(off, 16, true); off += 2;       // pubkey_offset
  view.setUint16(off, 0xFFFF, true); off += 2;   // pubkey_ix_index
  view.setUint16(off, 112, true); off += 2;      // msg_offset
  view.setUint16(off, msgLen, true); off += 2;    // msg_size
  view.setUint16(off, 0xFFFF, true); off += 2;   // msg_ix_index

  data.set(pubkey, 16);      // 32-byte public key
  data.set(signature, 48);   // 64-byte signature
  data.set(message, 112);    // 20-byte message

  return new TransactionInstruction({
    programId: ED25519_PROGRAM,
    keys: [],
    data: Buffer.from(data),
  });
}
```

### Transaction Structure

The transaction **must use VersionedTransaction (V0)** and contain exactly 2 instructions:

1. **Instruction 0**: Ed25519SigVerify precompile (verifies oracle signature)
2. **Instruction 1**: The actual `openPosition` or `closePosition` instruction

```javascript
const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
const msg = new TransactionMessage({
  payerKey: wallet.publicKey,
  recentBlockhash: blockhash,
  instructions: [ed25519Ix, tradeIx],  // Ed25519 MUST be first
}).compileToV0Message();
const tx = new VersionedTransaction(msg);
tx.sign([wallet]);
const sig = await connection.sendTransaction(tx);
await connection.confirmTransaction({ signature: sig, blockhash, lastValidBlockHeight });
```

---

## Security: PDA Verification

Always independently derive PDAs client-side and verify they match what the backend returns. This prevents a compromised backend from substituting malicious accounts.

```javascript
// Derive locally
const expectedUserAccount = PublicKey.findProgramAddressSync(
  [Buffer.from("user_account"), walletPubkey.toBuffer()],
  PROGRAM_ID
)[0];

// Compare with backend response
if (params.accounts.userAccount !== expectedUserAccount.toString()) {
  throw new Error("PDA mismatch — potential attack!");
}
```

Do this for every PDA in every transaction (userAccount, position, market, exchange, vault, etc.).

---

## Complete Trading Flow

### Step 1: Discover Tradable Cards
```
GET /api/trading/tradable
```

### Step 2: Research Cards
```
GET /api/cards/{product_id}/bundle?include_listings=true&include_sales=true&include_history=true
```

### Step 3: Check Account
```
GET /api/trading/account/{your_wallet_address}
```
If `exists` is `false`, create an account first.

### Step 4: Create Account (one-time)
```
POST /api/trading/tx/create-account
{ "owner": "YourWalletPublicKey" }
```
Build and sign the returned transaction.

### Step 5: Deposit USDC
Your USDC token account:
```javascript
const userTokenAccount = getAssociatedTokenAddressSync(
  new PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"),
  walletPubkey
);
```

```
POST /api/trading/tx/deposit
{ "owner": "...", "userTokenAccount": "...", "amount": 100.0 }
```

### Step 6: Open Position
```
POST /api/trading/tx/open-position
{ "owner": "...", "productId": 123456, "side": "long", "size": 50.0, "leverage": 5 }
```
Build VersionedTransaction with Ed25519 + openPosition instructions.

### Step 7: Monitor
```
GET /api/trading/portfolio/{wallet}
```

### Step 8: Close Position
```
POST /api/trading/tx/close-position
{ "owner": "...", "productId": 123456 }
```
Same Ed25519 + closePosition flow.

### Step 9: Withdraw
```
POST /api/trading/tx/withdraw
{ "owner": "...", "userTokenAccount": "...", "amount": 50.0 }
```
