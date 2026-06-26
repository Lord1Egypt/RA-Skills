# Finding the Vanity Salt

`Portal` uses CREATE2 for deterministic token deployment. The token address must carry a specific 4-character suffix:

| Token type | Required suffix |
|---|---|
| Tax token (`TOKEN_TAXED_V3`) | `7777` |
| Standard token (`TOKEN_V2_PERMIT`) | `8888` |

## Contract addresses (BNB mainnet)

| Name | Address |
|---|---|
| Portal | `0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0` |
| Standard Token Impl | `0x8b4329947e34b6d56d71a3385cac122bade7d78d` |
| Tax Token V3 Impl | `0x024f18294970B5c76c0691b87f138A0317156422` |

> **Important**: When calculating the salt, **always use the Portal address** as the deployer in CREATE2 calculations, even if you're launching the token through vaultPortal. This is because vaultPortal delegates the actual token deployment to Portal, which acts as the deployer contract.

## Algorithm

Repeatedly hash a random seed until the predicted CREATE2 address ends with the required suffix. The token is deployed as a minimal proxy clone of the token implementation.

```typescript
import {
  generatePrivateKey,
  getContractAddress,
  keccak256,
  toBytes,
  toHex,
} from "viem";
import type { Address, Hex } from "viem";

function findVanityTokenSalt(
  suffix: string,           // "7777" or "8888"
  tokenImpl: Address,       // token implementation address
  portal: Address           // Always use Portal contract address as the deployer for CREATE2 calculations 
): { salt: Hex; address: Address; iterations: number } {
  if (suffix.length !== 4) throw new Error("Suffix must be 4 characters");

  // Minimal proxy bytecode (EIP-1167) pointing to tokenImpl
  const bytecode = (
    "0x3d602d80600a3d3981f3363d3d373d3d3d363d73" +
    tokenImpl.slice(2).toLowerCase() +
    "5af43d82803e903d91602b57fd5bf3"
  ) as Hex;

  const predict = (salt: Hex): Address =>
    getContractAddress({ from: portal, salt: toBytes(salt), bytecode, opcode: "CREATE2" });

  // you can start with any random seed — here we use a random new private key as the initial seed  
  let salt = keccak256(toHex(generatePrivateKey()));
  let iterations = 0;

  while (!predict(salt).toLowerCase().endsWith(suffix)) {
    salt = keccak256(salt);
    iterations++;
  }

  const address = predict(salt);
  return { salt, address, iterations };
}

// Example usage — tax token on BNB mainnet:
const PORTAL   = "0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0" as Address;
const TAX_IMPL = "0x024f18294970B5c76c0691b87f138A0317156422" as Address;
const STD_IMPL = "0x8b4329947e34b6d56d71a3385cac122bade7d78d" as Address;

const result = findVanityTokenSalt("7777", TAX_IMPL, PORTAL);
console.log("Salt:         ", result.salt);
console.log("Token address:", result.address);
console.log("Iterations:   ", result.iterations);
```

Typical run finds a match in a few thousand iterations (< 1 second).

Save both `result.salt` and `result.address` — the salt goes into the launch params and the address is shown to the user after the transaction succeeds.
