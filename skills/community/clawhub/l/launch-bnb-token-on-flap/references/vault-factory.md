# Vault Factory Setup

This reference is only needed for **tax token + vault** launches (`VaultPortal.newTokenV6WithVault`).

## Step 1 — Choose a vault factory

Determine the vault factory address to use. For official factories the `vaultData` encoding is known (see table below) and Step 2 can be skipped. For any other factory, proceed to Step 2 to read the schema on-chain.

### Official vault factories (BNB mainnet)

| Name | Factory address | vaultData summary |
|---|---|---|
| SplitVault | `0xfab75Dc774cB9B38b91749B8833360B46a52345F` | ABI-encode `Recipient[]` — up to 10 `{address, bps}` entries summing to 10 000 |
| Gift Vault (FlapXVault) | `0x025549F52B03cF36f9e1a337c02d3AA7Af66ab32` | ABI-encode `{string xHandle}` — lowercase X (Twitter) handle of the fee manager |

Any vault factory address is accepted — unregistered or unverified factories can be used, but the resulting vault will be marked unverified in the UI.

## Step 2 — Read the factory's vaultData schema

Call `vaultDataSchema()` on the factory contract to determine what fields are required and how `vaultData` must be encoded.

`vaultDataSchema()` returns a `VaultDataSchema` struct (from `IVaultSchemasV1.sol`):

```solidity
struct VaultDataSchema {
    string description;       // describes what the vault does and what data it expects
    FieldDescriptor[] fields; // ordered list of fields — one entry per value to encode
    bool isArray;             // true → vaultData is abi.encode(tuple[]), false → abi.encode(tuple)
}

struct FieldDescriptor {
    string name;         // machine-readable field name
    string fieldType;    // ABI type string: "string", "address", "uint16", "uint256", "bool", "bytes", "bytes32", "time"
    string description;  // human-readable label/tooltip
    uint8  decimals;     // if > 0, multiply numeric value by 10^decimals before encoding
}
```

```typescript
import { createPublicClient, http } from "viem";
import { bsc } from "viem/chains";

const FIELD_DESCRIPTOR = {
  type: "tuple",
  components: [
    { name: "name",        type: "string" },
    { name: "fieldType",   type: "string" },
    { name: "description", type: "string" },
    { name: "decimals",    type: "uint8"  },
  ],
} as const;

const VAULT_DATA_SCHEMA_ABI = [{
  name: "vaultDataSchema",
  type: "function",
  stateMutability: "view",
  inputs: [],
  outputs: [{
    type: "tuple",
    components: [
      { name: "description", type: "string" },
      { name: "fields",      type: "tuple[]", components: FIELD_DESCRIPTOR.components },
      { name: "isArray",     type: "bool" },
    ],
  }],
}] as const;

const client = createPublicClient({ chain: bsc, transport: http(RPC_URL) });

const schema = await client.readContract({
  address: vaultFactoryAddress,
  abi: VAULT_DATA_SCHEMA_ABI,
  functionName: "vaultDataSchema",
});

// schema.description — describes the vault's purpose and expected data
// schema.fields      — one entry per value needed for encoding
// schema.isArray     — determines encoding shape (see Step 3)
console.log("description:", schema.description);
for (const f of schema.fields) {
  console.log(`  field: ${f.name} (${f.fieldType}) — ${f.description}`);
}
```

Resolve a value for each entry in `schema.fields`, applying `decimals` scaling to any numeric field, then proceed to Step 3.

## Step 3 — Encode vaultData

### SplitVault example

```typescript
import { encodeAbiParameters } from "viem";

// recipients must be unique, non-zero, bps must sum to 10 000
const vaultData = encodeAbiParameters(
  [{ type: "tuple[]", components: [{ name: "recipient", type: "address" }, { name: "bps", type: "uint16" }] }],
  [[
    { recipient: "0xAlice...", bps: 5000 },
    { recipient: "0xBob...",   bps: 5000 },
  ]]
);
```

### Gift Vault (FlapXVault) example

```typescript
const vaultData = encodeAbiParameters(
  [{ type: "tuple", components: [{ name: "xHandle", type: "string" }] }],
  [{ xHandle: "elonmusk" }]  // lowercase, no "@"
);
```

Store the hex-encoded `vaultData` bytes — they go directly into the `NewTokenV6WithVaultParams.vaultData` field.
