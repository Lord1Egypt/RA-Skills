---
name: forge-token-deployer
description: Deploy new tokens on Cross Forge and create liquidity pools via CrossToken CLI. Use this skill whenever a user wants to deploy, launch, or create a token on Cross Forge — including agent tokens (ai_agent category), game tokens, even if they just say "token launch", "create a token", "list on Forge", "agent token deploy", or anything about getting a token onto Forge. Handles the full flow from registration to pool creation in one step with vendor auth (no setup needed), or with client API keys from RampConsole.
---

# Forge Token Deployer

Deploy tokens by selecting authentication method and wallet type via CrossToken CLI.

## Options Matrix

| Options | Auth | Wallet | Behavior |
|---------|------|--------|----------|
| `--auth=client --wallet=user` | ClientKey | User wallet | Token deploy + unsigned tx returned |
| `--auth=client --wallet=tmp` | ClientKey | Temp wallet | Token deploy + pool creation |
| `--auth=vendor --wallet=user` | Vendor | User wallet | Token deploy + unsigned tx returned |
| `--auth=vendor --wallet=tmp` | Vendor | Temp wallet | Token deploy + pool creation **(default)** |

### Auth Methods

- **client**: Authenticate with ClientKey/Secret from RampConsole (https://cross-ramp-console.crosstoken.io). Requires `.env` setup.
- **vendor**: No sign-up or credentials needed. Works out of the box.

### Wallet Types

- **user**: User's real wallet becomes token owner. Pool creation requires signing unsigned tx on frontend.
- **tmp**: Creates a temporary wallet and completes pool creation automatically. Owner permissions are not reusable.

## Embedded Files

When the working directory does not contain both `deploy-token.js` and `package.json`, create them from the sources below before proceeding.

### package.json

```json
{
  "name": "forge-token-deployer",
  "version": "1.0.0",
  "description": "Token deployment CLI for Forge service",
  "type": "module",
  "dependencies": {
    "dotenv": "^17.3.1",
    "ethers": "^6.14.3"
  }
}
```

### deploy-token.js

```javascript
#!/usr/bin/env node
import "dotenv/config";
import { ethers } from "ethers";
import { readFileSync, existsSync } from "fs";
import { extname } from "path";

const DEPLOY_API = {
  client: "https://cross-console-api.crosstoken.io/api/client/mcp/builder",
  vendor: "https://cross-console-api.crosstoken.io/api/builder/mcp",
};

const RPC_URL = "https://mainnet.crosstoken.io:22001";
const ROUTER = "0x7aF414e4d373bb332f47769c8d28A446A0C1a1E8";
const TOKEN_B = "0xDdF8AaA3927b8Fd5684dc2edcc7287EcB0A2122d";
const TRADE_URL = "https://x.crosstoken.io/forge/token";
const VENDOR_ADDRESS = "0x254465624da909e0072fbf8c32bcfc26b9fe9da9";

const ROUTER_ABI = [{
  name: "createPairWithVirtualReserve",
  type: "function",
  stateMutability: "payable",
  inputs: [
    { name: "tokenA", type: "address" },
    { name: "tokenB", type: "address" },
    { name: "creatorFeeRecipient", type: "address" },
    { name: "deadline", type: "uint256" }
  ],
  outputs: [
    { name: "pair", type: "address" },
    { name: "liquidity", type: "uint256" }
  ]
}];

const VALID_CATEGORIES = ["game", "ai_agent"];

function getOption(name) {
  const arg = process.argv.find(a => a.startsWith(`--${name}=`));
  return arg ? arg.split("=")[1] : null;
}

async function callDeployAPI(auth, tokenName, tokenSymbol, tokenDescription, imageUrl, owner, category) {
  const payload = {
    owner,
    project_name: tokenName,
    token: { name: tokenName, symbol: tokenSymbol, image_url: imageUrl },
    token_description: tokenDescription,
    category,
  };

  const headers = { "Content-Type": "application/json" };

  if (auth === "client") {
    const clientKey = process.env.CLIENT_KEY;
    const clientSecret = process.env.CLIENT_SECRET;
    if (!clientKey || !clientSecret) {
      throw new Error("CLIENT_KEY and CLIENT_SECRET environment variables are not set. Please check your .env file.");
    }
    headers["Authorization"] = `API-Key ${clientKey}:${clientSecret}`;
  } else {
    payload.vendor = VENDOR_ADDRESS;
  }

  const response = await fetch(DEPLOY_API[auth], {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`HTTP ${response.status}: ${error}`);
  }

  const result = await response.json();
  if (result.code !== 200) {
    throw new Error(`API Error: ${result.message}`);
  }

  return result.data.token_address;
}

async function buildPoolTx(tokenAddress, feeRecipient, signer = null) {
  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const signerOrProvider = signer ? signer.connect(provider) : provider;
  const router = new ethers.Contract(ROUTER, ROUTER_ABI, signerOrProvider);
  const deadline = Math.floor(Date.now() / 1000) + 300;

  const txOptions = {
    type: 2,
    maxFeePerGas: ethers.parseUnits("100", "gwei"),
    maxPriorityFeePerGas: ethers.parseUnits("1", "gwei"),
  };

  const from = signer ? signer.address : feeRecipient;

  const gasEstimate = await router.createPairWithVirtualReserve.estimateGas(
    tokenAddress, TOKEN_B, feeRecipient, deadline, { from }
  );

  if (!signer) {
    const unsignedTx = await router.createPairWithVirtualReserve.populateTransaction(
      tokenAddress, TOKEN_B, feeRecipient, deadline
    );
    Object.assign(unsignedTx, txOptions);
    unsignedTx.from = from;
    unsignedTx.gasLimit = gasEstimate * 120n / 100n;
    return { unsignedTx };
  }

  const tx = await router.createPairWithVirtualReserve(
    tokenAddress, TOKEN_B, feeRecipient, deadline,
    { ...txOptions, gasLimit: gasEstimate * 120n / 100n }
  );
  const receipt = await tx.wait();
  return { tx, receipt };
}

async function main() {
  const args = process.argv.slice(2);

  if (args.includes("--help") || args.includes("-h")) {
    printUsage();
    process.exit(0);
  }

  const auth = getOption("auth") || "vendor";
  const wallet = getOption("wallet") || "tmp";

  if (!["client", "vendor"].includes(auth)) {
    console.error(`Error: --auth must be client or vendor. (received: ${auth})`);
    process.exit(1);
  }
  if (!["user", "tmp"].includes(wallet)) {
    console.error(`Error: --wallet must be user or tmp. (received: ${wallet})`);
    process.exit(1);
  }

  const positionalArgs = args.filter(a => !a.startsWith("--") && a.trim() !== "");

  if (positionalArgs.length < 6) {
    printUsage();
    process.exit(1);
  }

  let [tokenName, tokenSymbol, tokenDescription, imageUrl, walletAddress, category] = positionalArgs;

  if (existsSync(imageUrl)) {
    const ext = extname(imageUrl).toLowerCase();
    const mime = ext === ".jpg" || ext === ".jpeg" ? "image/jpeg" : "image/png";
    const buf = readFileSync(imageUrl);
    if (buf.length > 1024 * 1024) {
      console.error(`Error: Image file exceeds 1MB. (${(buf.length / 1024 / 1024).toFixed(2)}MB)`);
      process.exit(1);
    }
    imageUrl = `data:${mime};base64,${buf.toString("base64")}`;
    console.log(`Local image file converted to base64: ${positionalArgs[3]} (${(buf.length / 1024).toFixed(0)}KB)\n`);
  }

  if (!/^0x[0-9a-fA-F]{40}$/.test(walletAddress)) {
    console.error(`Error: Invalid ${wallet === "user" ? "user wallet" : "fee recipient"} address.`);
    process.exit(1);
  }

  if (!category || !VALID_CATEGORIES.includes(category)) {
    console.error(`Error: Category must be one of: ${VALID_CATEGORIES.join(", ")}`);
    process.exit(1);
  }

  try {
    const authLabel = auth === "client" ? "ClientKey" : "Vendor";
    const walletLabel = wallet === "user" ? "User Wallet" : "Temp Wallet";
    console.log(`\n[${authLabel} + ${walletLabel}] Starting token deployment\n`);

    let owner;
    let tmpWallet;

    if (wallet === "tmp") {
      tmpWallet = ethers.Wallet.createRandom();
      owner = tmpWallet.address;
      console.log(`Temp wallet created: ${owner}\n`);
    } else {
      owner = walletAddress;
    }

    console.log("Deploying token...\n");
    const tokenAddress = await callDeployAPI(auth, tokenName, tokenSymbol, tokenDescription, imageUrl, owner, category);

    console.log("Token deployed!");
    console.log(`  Token Name: ${tokenName} (${tokenSymbol})`);
    console.log(`  Token Address: ${tokenAddress}\n`);

    const tradeLink = `${TRADE_URL}/${tokenAddress}`;
    const jsonReplacer = (key, value) =>
      typeof value === "bigint" ? value.toString() : value;

    if (wallet === "user") {
      console.log("Generating unsigned TX for Forge pool creation...\n");
      const { unsignedTx } = await buildPoolTx(tokenAddress, owner);
      const output = { tokenAddress, tradeLink, unsignedTx };

      console.log("Unsigned Transaction for Forge pool creation:");
      console.log(JSON.stringify(output, jsonReplacer, 2));
      console.log(`\nSign the above unsignedTx with the user's wallet on the frontend.`);
      console.log(`The trade link will only be accessible after the pool TX succeeds.\n`);
    } else {
      await new Promise(resolve => setTimeout(resolve, 1000));

      console.log("Creating Forge pool...\n");
      const { tx, receipt } = await buildPoolTx(tokenAddress, walletAddress, tmpWallet);
      const success = receipt.status === 1;

      const output = {
        poolCreated: success,
        tokenAddress,
        tradeLink: success ? tradeLink : null,
        txHash: tx.hash,
        blockNumber: receipt.blockNumber,
      };

      if (success) {
        console.log("Forge pool created!\n");
        console.log(`  Token Name: ${tokenName} (${tokenSymbol})`);
        console.log(`  Token Address: ${tokenAddress}`);
        console.log(`  Trade Link: ${tradeLink}\n`);
      } else {
        console.log("Forge pool creation failed!\n");
        console.log(`  Token Address: ${tokenAddress}`);
        console.log(`  TX Hash: ${tx.hash}\n`);
      }

      console.log(JSON.stringify(output, jsonReplacer, 2));
    }
  } catch (error) {
    console.error("\nError:", error.message);
    process.exit(1);
  }
}

function printUsage() {
  console.log(`
Forge Token Deploy CLI

Options:
  --auth=client|vendor    Auth method (default: vendor)
    client  Authenticate with ClientKey/Secret from RampConsole
    vendor  Deploy without sign-up or credentials

  --wallet=user|tmp       Wallet type (default: tmp)
    user    User wallet becomes token owner, returns unsigned tx for pool creation
    tmp     Creates temp wallet, completes token deploy + pool creation (owner permissions not reusable)

Environment variables (when using --auth=client):
  CLIENT_KEY      Client key from RampConsole
  CLIENT_SECRET   Client secret from RampConsole

Usage:
  node deploy-token.js [options] <name> <symbol> <description> <imageUrl> <walletAddress> <category>

Examples:
  node deploy-token.js "MyToken" "MTK" "A fun token" "https://example.com/token.png" "0x1234..." "game"
  node deploy-token.js "MyToken" "MTK" "A fun token" "./token.png" "0x1234..." "game"
  node deploy-token.js --auth=client --wallet=user "MyToken" "MTK" "A fun token" "./token.png" "0x1234..." "game"

Arguments:
  name                Token name (e.g. "MyToken")
  symbol              Token symbol (e.g. "MTK")
  description         Token description (e.g. "A fun community token")
  imageUrl            Token image URL or local file path (PNG, JPG). Max 1MB.
  walletAddress       User wallet address (EVM)
                      --wallet=user: token owner + fee recipient
                      --wallet=tmp: fee recipient only (token owner is temp wallet)
  category            "game" or "ai_agent"

Notes:
  - Symbols are globally unique and case-insensitive
  - --wallet=tmp: temp wallet becomes token owner, owner permissions not reusable
`);
}

main();
```

## Workflow

When the user requests a token deployment:

1. **Setup files** (if not present in working directory):
   - Write `package.json` and `deploy-token.js` from the Embedded Files section above
   - Run `npm install`

2. **Option selection**:
   - **`ai_agent` category (agent token)**: Must use `--wallet=user` with the agent EOA wallet address. Do NOT use `--wallet=tmp` for agent tokens — the token `owner()` must be the agent EOA, and a temp wallet cannot satisfy this requirement.
   - **Other categories**: Defaults to `--auth=vendor --wallet=tmp`, which completes the entire process (token deploy + pool creation) in one step with no extra setup. Only change if the user explicitly requests it.

3. **Check prerequisites**:
   - If `--auth=client`, verify `.env` contains `CLIENT_KEY` and `CLIENT_SECRET`

4. **Collect parameters** (prompt the user for any missing values):

   | Field | Description | Example |
   |-------|-------------|---------|
   | Token Name | Name of the token | "MyToken" |
   | Symbol | Token symbol (uppercase recommended, must be unique) | "MTK" |
   | Token Description | Description of the token | "A fun community token" |
   | Image URL | Token image URL (PNG, JPG) or local file path. Max 1MB. | "https://example.com/token.png" or "./token.png" |
   | Wallet Address | EVM wallet address | "0x1234..." |
   | Category | `game` for game tokens, `ai_agent` for AI agent tokens | "game" |

   - **user wallet**: Wallet Address = token owner + fee recipient
   - **tmp wallet**: Wallet Address = fee recipient only (token owner is temporary wallet)

5. **Execute deployment**:

   ```bash
   # Default options (vendor + tmp)
   node deploy-token.js "<name>" "<symbol>" "<description>" "<imageUrl>" "<walletAddress>" "<category>"

   # With explicit options
   node deploy-token.js --auth=<method> --wallet=<type> "<name>" "<symbol>" "<description>" "<imageUrl>" "<walletAddress>" "<category>"
   ```

6. **Parse and present results**:

   **When `--wallet=user`** - return unsigned tx for frontend signing:
   ```json
   {
     "tokenAddress": "string",
     "tradeLink": "string",
     "unsignedTx": {
       "to": "string",
       "data": "string",
       "from": "string",
       "type": 2,
       "maxFeePerGas": "string",
       "maxPriorityFeePerGas": "string",
       "gasLimit": "string"
     }
   }
   ```

   **When `--wallet=tmp`** - pool creation completed:
   ```json
   {
     "poolCreated": true,
     "tokenAddress": "string",
     "tradeLink": "string",
     "txHash": "string",
     "blockNumber": 0
   }
   ```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `API Error: symbol already in use` | Symbol taken by another user | Choose a different symbol — symbols are globally unique and case-insensitive |
| `HTTP 401` | Invalid or missing CLIENT_KEY/CLIENT_SECRET | Check `.env` file; verify keys from RampConsole |
| `HTTP 400: invalid owner` | Wallet address format wrong | Ensure address is a valid 0x EVM address (42 chars) |
| Pool TX fails (`receipt.status === 0`) | RPC or contract issue | Token is deployed but pool failed; retry `buildPoolTx` manually or redeploy |
| `Error: Image file exceeds 1MB` | Image too large | Resize or compress the image before passing it |
| `INSUFFICIENT_OUTPUT_AMOUNT` | Pool creation slippage | Retry — transient price movement |

## Important Notes

- Symbols are globally unique and case-insensitive. A symbol already used by another user cannot be registered.
- **Agent token (`ai_agent` category)**: Always use `--wallet=user` with the agent EOA (`wallet_address` from `GET /accounts/me`). The token `owner()` must equal the agent EOA — using `--wallet=tmp` will cause registration to fail with a 403 error.
- `--wallet=tmp`: The temporary wallet becomes token owner. Owner permissions are **not reusable** after deployment. Do not use for agent tokens.
- `--wallet=user`: Pool creation is **not automatic**. The unsigned tx must be signed by the user's wallet on the frontend.
- Always confirm parameters with the user before executing the deploy command.
- **Image from local file**: If no external image URL is available, generate or obtain an image file first (e.g. image generation tool, user-provided file), then pass the local file path as the imageUrl argument.
