---
name: jovay-dapp
description: Full-stack dApp generation skill for Jovay blockchain — from requirements gathering to contract deployment and frontend debugging
version: 0.0.1alpha
author: Jovay Team
metadata:
  {
    "openclaw": {
        "emoji": "🚀",
        "requires": { "bins": ["jovay", "git", "node", "npx"] },
        "install": [{
          "id": "npm",
          "kind": "npm",
          "package": "@jovaylabs/jovay-cli",
          "bins": ["jovay"],
          "label": "Install jovay-cli (npm)"
        }]
    }
  }
---

# Jovay DApp Generation Skill

## Description

This skill generates complete full-stack dApps on the **Jovay** Layer 2 EVM blockchain. It guides the AI through an end-to-end workflow: gathering requirements from the user, initializing the project, generating Solidity smart contracts, compiling and testing, generating a Vue 3 frontend, deploying contracts to testnet, and running the frontend locally for debugging.

## Prerequisites

- Node.js v20+
- Git installed
- `jovay-cli` installed (`npm install -g @jovaylabs/jovay-cli`)
- Jovay CLI initialized (`jovay init`) with wallet configured
- Testnet ETH available (`jovay wallet airdrop`)

## Overview Workflow

```
1. Requirements Gathering  →  Ask user about dApp type, features, contract logic
2. Project Initialization  →  jovay dapp init --name <project>
3. Install Dependencies    →  npm install, OpenZeppelin, etc.
4. Generate Contracts       →  Write Solidity contracts in contracts/
5. Compile & Test          →  jovay dapp build / npx hardhat test
6. Generate Frontend       →  Write Vue 3 frontend in frontend/
7. Deploy Contracts        →  jovay dapp deploy (testnet)
8. Local Frontend Debug    →  cd frontend && npm run dev
```

---

## Phase 1: Requirements Gathering

When the user says they want to generate a dApp, you MUST ask clarifying questions before proceeding. Continue asking until you have enough information to generate the complete dApp.

### Required Information

Ask the user about the following (adapt based on context):

1. **dApp Type & Purpose**: What does the dApp do? (e.g., NFT marketplace, token swap, voting system, crowdfunding, DAO governance, DeFi protocol, game, social platform)
2. **Smart Contract Features**: What contract functionality is needed?
   - Token type: ERC20 (fungible token), ERC721 (NFT), ERC1155 (multi-token), or custom
   - Access control: Ownable, Role-based (AccessControl), or open
   - Special features: Pausable, upgradeable, burnable, mintable, etc.
   - Custom business logic: specific functions, state variables, events
3. **Frontend Features**: What pages/views are needed?
   - Wallet connection (MetaMask)
   - Which contract functions should be exposed in the UI
   - Any specific UI requirements (dashboard, gallery, forms, etc.)
4. **Network**: Confirm testnet deployment (default: Jovay Sepolia testnet)

### Gathering Strategy

- Start with a broad question about what the user wants to build
- Follow up with specific technical questions based on their answer
- If the user gives a vague description, propose a concrete architecture and ask for confirmation
- Once you have enough detail, summarize the plan and ask for approval before proceeding

### Example Interaction

```
User: "I want to build an NFT dApp"

AI should ask:
- What kind of NFTs? (art, collectibles, membership, gaming items)
- Should there be a minting limit (max supply)?
- Should users be able to mint, or only the owner?
- Do you need a whitelist/allowlist mechanism?
- Should NFTs be burnable or transferable?
- What metadata standard? (on-chain or off-chain URI)
- Frontend needs: gallery view, mint page, profile page?
- Any royalty mechanism (ERC2981)?
```

---

## Phase 2: Project Initialization

### 2.1 Verify Jovay CLI Setup

Before creating the project, verify the CLI is initialized:

```bash
jovay network get
```

If not initialized:

```bash
jovay init --enc
```

Check testnet balance:

```bash
jovay wallet balance
```

If balance is zero, request airdrop:

```bash
jovay wallet airdrop
```

### 2.2 Initialize Project

```bash
jovay dapp init --name <project_name>
```

This clones the `EasyJovayDappTemplate` from GitHub and creates the project structure:

```
<project_name>/
├── contracts/              # Solidity smart contracts
├── frontend/               # Vue 3 + Vite frontend
│   ├── src/
│   │   ├── components/     # Reusable Vue components
│   │   ├── views/          # Page components
│   │   ├── stores/         # Pinia state management
│   │   ├── config/         # Configuration files
│   │   └── contracts/      # Contract ABI files for frontend
├── tools/                  # Build and deploy shell scripts
├── scripts/                # Hardhat deployment scripts (JS)
├── hardhat.config.cjs      # Hardhat configuration
├── package.json            # Root package.json with Hardhat deps
└── .jovay/
    └── .env                # JSON: { PROJECT_NAME, TEMPLATE_NAME }
```

### 2.3 Install Dependencies

```bash
cd <project_name>

# Install base deps (Hardhat, ethers, etc.)
npm install

# Install OpenZeppelin contracts (almost always needed)
npm install @openzeppelin/contracts

# If the template has an install script:
# chmod +x tools/install_deps.sh && ./tools/install_deps.sh
```

---

## Phase 3: Generate Smart Contracts

Write Solidity files into the `contracts/` directory. Remove any sample contracts that came with the template if they are not needed.

### Hardhat Configuration

The template includes a `hardhat.config.cjs` that reads environment variables for Jovay testnet. Ensure it includes:

```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    jovay_testnet: {
      url: process.env.JOVAY_TESTNET_RPC_URL || "https://testnet-rpc.jovay.xyz",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
    },
  },
};
```

### Contract Patterns

Below are common contract patterns. Adapt and combine based on user requirements.

#### ERC20 Token

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, ERC20Burnable, Ownable {
    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply,
        address initialOwner
    ) ERC20(name, symbol) Ownable(initialOwner) {
        _mint(initialOwner, initialSupply * 10 ** decimals());
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
```

#### ERC721 NFT

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;
    uint256 public maxSupply;
    uint256 public mintPrice;

    constructor(
        string memory name,
        string memory symbol,
        uint256 _maxSupply,
        uint256 _mintPrice,
        address initialOwner
    ) ERC721(name, symbol) Ownable(initialOwner) {
        maxSupply = _maxSupply;
        mintPrice = _mintPrice;
    }

    function safeMint(address to, string memory uri) public payable {
        require(_nextTokenId < maxSupply, "Max supply reached");
        if (msg.sender != owner()) {
            require(msg.value >= mintPrice, "Insufficient payment");
        }
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // Required overrides
    function _update(address to, uint256 tokenId, address auth)
        internal override(ERC721, ERC721Enumerable) returns (address) {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal override(ERC721, ERC721Enumerable) {
        super._increaseBalance(account, value);
    }

    function tokenURI(uint256 tokenId)
        public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public view override(ERC721, ERC721Enumerable, ERC721URIStorage) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}
```

#### ERC1155 Multi-Token

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyMultiToken is ERC1155, Ownable {
    mapping(uint256 => string) private _tokenURIs;

    constructor(address initialOwner)
        ERC1155("") Ownable(initialOwner) {}

    function mint(address to, uint256 id, uint256 amount, bytes memory data) public onlyOwner {
        _mint(to, id, amount, data);
    }

    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data) public onlyOwner {
        _mintBatch(to, ids, amounts, data);
    }

    function setURI(uint256 tokenId, string memory newUri) public onlyOwner {
        _tokenURIs[tokenId] = newUri;
    }

    function uri(uint256 tokenId) public view override returns (string memory) {
        string memory tokenUri = _tokenURIs[tokenId];
        return bytes(tokenUri).length > 0 ? tokenUri : super.uri(tokenId);
    }
}
```

#### Custom Contract (Voting / DAO Example)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract SimpleVoting is Ownable {
    struct Proposal {
        string description;
        uint256 voteCount;
        uint256 deadline;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => mapping(address => bool)) public hasVoted;
    uint256 public proposalCount;

    event ProposalCreated(uint256 indexed proposalId, string description, uint256 deadline);
    event Voted(uint256 indexed proposalId, address indexed voter);

    constructor(address initialOwner) Ownable(initialOwner) {}

    function createProposal(string memory description, uint256 duration) public onlyOwner returns (uint256) {
        uint256 proposalId = proposalCount++;
        proposals[proposalId] = Proposal({
            description: description,
            voteCount: 0,
            deadline: block.timestamp + duration,
            executed: false
        });
        emit ProposalCreated(proposalId, description, block.timestamp + duration);
        return proposalId;
    }

    function vote(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp < proposal.deadline, "Voting ended");
        require(!hasVoted[proposalId][msg.sender], "Already voted");
        hasVoted[proposalId][msg.sender] = true;
        proposal.voteCount++;
        emit Voted(proposalId, msg.sender);
    }

    function getProposal(uint256 proposalId) public view returns (string memory, uint256, uint256, bool) {
        Proposal storage p = proposals[proposalId];
        return (p.description, p.voteCount, p.deadline, p.executed);
    }
}
```

### Design Principles

When generating contracts:

1. **Use OpenZeppelin** wherever possible for standard functionality
2. **Solidity ^0.8.20** as the pragma version (matches Hardhat config)
3. **Emit events** for all state changes
4. **Add access control** (Ownable at minimum)
5. **Include NatDoc comments** for public functions
6. **Follow checks-effects-interactions** pattern
7. **Avoid known vulnerabilities**: reentrancy, integer overflow (handled by Solidity 0.8+), etc.

---

## Phase 4: Compile & Test

### 4.1 Compile Contracts

Option A — Using `jovay dapp build`:

```bash
jovay dapp build
# Or with encrypted wallet:
jovay dapp build --enc-key <YOUR_ENC_KEY>
```

Option B — Using Hardhat directly (recommended for more control):

```bash
npx hardhat compile
```

After compilation, ABIs are generated in `artifacts/contracts/`.

### 4.2 Write Tests

Create test files in the `test/` directory using Hardhat's testing framework:

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MyNFT", function () {
  let myNFT;
  let owner;
  let addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const MyNFT = await ethers.getContractFactory("MyNFT");
    myNFT = await MyNFT.deploy("TestNFT", "TNFT", 100, ethers.parseEther("0.01"), owner.address);
    await myNFT.waitForDeployment();
  });

  it("Should mint an NFT", async function () {
    await myNFT.safeMint(owner.address, "https://example.com/token/0");
    expect(await myNFT.ownerOf(0)).to.equal(owner.address);
    expect(await myNFT.tokenURI(0)).to.equal("https://example.com/token/0");
  });

  it("Should enforce max supply", async function () {
    // Test max supply logic
  });

  it("Should enforce mint price for non-owner", async function () {
    await expect(
      myNFT.connect(addr1).safeMint(addr1.address, "uri", { value: 0 })
    ).to.be.revertedWith("Insufficient payment");
  });
});
```

Run tests:

```bash
npx hardhat test
```

### 4.3 Verify Compilation Artifacts

After successful compilation, the ABIs are at:

```
artifacts/contracts/<ContractName>.sol/<ContractName>.json
```

Copy the ABI to the frontend for use:

```bash
# Extract ABI and copy to frontend
cp artifacts/contracts/<ContractName>.sol/<ContractName>.json frontend/src/contracts/
```

---

## Phase 5: Generate Frontend

The template provides a Vue 3 + Vite + Pinia + ethers.js frontend scaffold. You need to customize it for the specific dApp.

### Frontend Stack

- **Vue 3** (Composition API with `<script setup>`)
- **Vite** (build tool)
- **Pinia** (state management)
- **ethers.js v6** (blockchain interaction)
- **Vue Router** (routing)

### 5.1 Frontend Project Structure

```
frontend/
├── src/
│   ├── App.vue                 # Root component
│   ├── main.js                 # App entry point
│   ├── router/
│   │   └── index.js            # Vue Router configuration
│   ├── views/                  # Page-level components
│   │   ├── HomeView.vue
│   │   └── ...
│   ├── components/             # Reusable components
│   │   ├── WalletConnect.vue
│   │   └── ...
│   ├── stores/                 # Pinia stores
│   │   ├── wallet.js           # Wallet connection state
│   │   └── contract.js         # Contract interaction state
│   ├── contracts/              # ABI JSON files
│   │   └── <ContractName>.json
│   └── config/
│       └── index.js            # Chain config, contract addresses
├── package.json
├── vite.config.js
└── index.html
```

### 5.2 Core Frontend Patterns

#### Chain Configuration (`frontend/src/config/index.js`)

```javascript
export const CHAIN_CONFIG = {
  chainId: "0xC352", // Jovay Sepolia testnet chain ID (50002)
  chainName: "Jovay Sepolia Testnet",
  rpcUrls: ["https://testnet-rpc.jovay.xyz"],
  nativeCurrency: {
    name: "ETH",
    symbol: "ETH",
    decimals: 18,
  },
  blockExplorerUrls: ["https://testnet-explorer.jovay.xyz"],
};

export const CONTRACT_ADDRESSES = {
  // Fill in after deployment
  MyContract: "0x...",
};
```

#### Wallet Store (`frontend/src/stores/wallet.js`)

```javascript
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { BrowserProvider } from "ethers";
import { CHAIN_CONFIG } from "@/config";

export const useWalletStore = defineStore("wallet", () => {
  const provider = ref(null);
  const signer = ref(null);
  const address = ref("");
  const chainId = ref("");
  const isConnected = computed(() => !!address.value);

  async function connect() {
    if (!window.ethereum) {
      alert("Please install MetaMask!");
      return;
    }
    const browserProvider = new BrowserProvider(window.ethereum);
    const accounts = await browserProvider.send("eth_requestAccounts", []);
    provider.value = browserProvider;
    signer.value = await browserProvider.getSigner();
    address.value = accounts[0];
    const network = await browserProvider.getNetwork();
    chainId.value = "0x" + network.chainId.toString(16);

    if (chainId.value.toLowerCase() !== CHAIN_CONFIG.chainId.toLowerCase()) {
      await switchChain();
    }

    window.ethereum.on("accountsChanged", handleAccountsChanged);
    window.ethereum.on("chainChanged", () => window.location.reload());
  }

  async function switchChain() {
    try {
      await window.ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: CHAIN_CONFIG.chainId }],
      });
    } catch (switchError) {
      if (switchError.code === 4902) {
        await window.ethereum.request({
          method: "wallet_addEthereumChain",
          params: [CHAIN_CONFIG],
        });
      }
    }
  }

  function handleAccountsChanged(accounts) {
    if (accounts.length === 0) {
      disconnect();
    } else {
      address.value = accounts[0];
    }
  }

  function disconnect() {
    provider.value = null;
    signer.value = null;
    address.value = "";
    chainId.value = "";
  }

  function shortenAddress(addr) {
    if (!addr) return "";
    return addr.slice(0, 6) + "..." + addr.slice(-4);
  }

  return {
    provider, signer, address, chainId, isConnected,
    connect, disconnect, switchChain, shortenAddress,
  };
});
```

#### Contract Store (`frontend/src/stores/contract.js`)

```javascript
import { defineStore } from "pinia";
import { ref } from "vue";
import { Contract } from "ethers";
import { useWalletStore } from "./wallet";
import { CONTRACT_ADDRESSES } from "@/config";
import ContractABI from "@/contracts/<ContractName>.json";

export const useContractStore = defineStore("contract", () => {
  const contract = ref(null);
  const loading = ref(false);
  const error = ref("");

  function getContract() {
    const wallet = useWalletStore();
    if (!wallet.signer) throw new Error("Wallet not connected");
    if (!contract.value) {
      contract.value = new Contract(
        CONTRACT_ADDRESSES.MyContract,
        ContractABI.abi,
        wallet.signer
      );
    }
    return contract.value;
  }

  async function callReadMethod(method, ...args) {
    loading.value = true;
    error.value = "";
    try {
      const c = getContract();
      return await c[method](...args);
    } catch (e) {
      error.value = e.message;
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function callWriteMethod(method, ...args) {
    loading.value = true;
    error.value = "";
    try {
      const c = getContract();
      const tx = await c[method](...args);
      const receipt = await tx.wait();
      return receipt;
    } catch (e) {
      error.value = e.message;
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return { contract, loading, error, getContract, callReadMethod, callWriteMethod };
});
```

#### Wallet Connect Component (`frontend/src/components/WalletConnect.vue`)

```vue
<script setup>
import { useWalletStore } from "@/stores/wallet";

const wallet = useWalletStore();
</script>

<template>
  <button v-if="!wallet.isConnected" @click="wallet.connect" class="connect-btn">
    Connect Wallet
  </button>
  <div v-else class="wallet-info">
    <span class="address">{{ wallet.shortenAddress(wallet.address) }}</span>
    <button @click="wallet.disconnect" class="disconnect-btn">Disconnect</button>
  </div>
</template>

<style scoped>
.connect-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.connect-btn:hover { opacity: 0.9; }
.wallet-info { display: flex; align-items: center; gap: 12px; }
.address {
  background: #f0f0f0;
  padding: 8px 16px;
  border-radius: 8px;
  font-family: monospace;
  font-size: 14px;
}
.disconnect-btn {
  background: #ff4757;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
}
</style>
```

### 5.3 UI Design Guidelines

When generating frontend pages:

1. **Modern, clean design** with consistent spacing and colors
2. **Responsive layout** that works on desktop and mobile
3. **Loading states** for all blockchain interactions (transactions take time)
4. **Error handling** with user-friendly messages
5. **Transaction feedback**: show pending state, success with tx hash link to explorer, or error
6. **Form validation** before sending transactions
7. **Use CSS variables** for theming consistency

### 5.4 Install Frontend Dependencies

```bash
cd frontend
npm install
# ethers should already be included; if not:
npm install ethers
```

---

## Phase 6: Deploy Contracts to Testnet

### 6.1 Write Deployment Script

Create or update `scripts/deploy.js`:

```javascript
const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await deployer.provider.getBalance(deployer.address)).toString());

  // Deploy each contract
  const MyContract = await ethers.getContractFactory("MyContract");
  const myContract = await MyContract.deploy(/* constructor args */);
  await myContract.waitForDeployment();
  console.log("MyContract deployed to:", myContract.target);

  // If deploying multiple contracts:
  // const Token = await ethers.getContractFactory("Token");
  // const token = await Token.deploy(/* args */);
  // await token.waitForDeployment();
  // console.log("Token deployed to:", token.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

### 6.2 Deploy

Option A — Using `jovay dapp deploy`:

```bash
jovay dapp deploy
# Or with encrypted wallet:
jovay dapp deploy --enc-key <YOUR_ENC_KEY>
```

Option B — Using Hardhat directly:

```bash
JOVAY_TESTNET_RPC_URL="<rpc_url>" DEPLOYER_PRIVATE_KEY="<private_key>" \
  npx hardhat run scripts/deploy.js --network jovay_testnet
```

### 6.3 Post-Deployment

After deployment:

1. **Record the contract addresses** from the deployment output
2. **Update frontend config** with deployed addresses:
   ```javascript
   // frontend/src/config/index.js
   export const CONTRACT_ADDRESSES = {
     MyContract: "0x<deployed_address>",
   };
   ```
3. **Copy ABI to frontend**:
   ```bash
   cp artifacts/contracts/MyContract.sol/MyContract.json frontend/src/contracts/
   ```
4. **Verify on explorer** (optional):
   ```bash
   jovay transaction info --tx <deployment_tx_hash>
   ```

---

## Phase 7: Local Frontend Debugging

### 7.1 Start Development Server

```bash
cd frontend
npm run dev
```

This starts the Vite dev server (typically at `http://localhost:5173`).

### 7.2 Testing Checklist

1. **Wallet Connection**: Connect MetaMask, verify correct network (Jovay Sepolia)
2. **Chain Switching**: If wrong chain, prompt to switch automatically
3. **Read Operations**: Verify view functions return expected data
4. **Write Operations**: Test state-changing transactions, check tx confirmation
5. **Error Handling**: Test with insufficient balance, wrong parameters
6. **UI/UX**: Check responsiveness, loading states, success/error notifications

### 7.3 Common MetaMask Setup for Jovay Testnet

Users need to add Jovay Sepolia testnet to MetaMask:

| Field | Value |
|-------|-------|
| Network Name | Jovay Sepolia Testnet |
| RPC URL | https://testnet-rpc.jovay.xyz |
| Chain ID | 50002 |
| Currency Symbol | ETH |
| Block Explorer | https://testnet-explorer.jovay.xyz |

The frontend's `switchChain()` function handles this automatically via `wallet_addEthereumChain`.

---

## Complete Example: NFT Minting DApp

This example demonstrates the full workflow for a simple NFT minting dApp.

<example>
<user_query>I want to build an NFT minting dApp on Jovay</user_query>
<assistant_response>

### Step 1: Gather requirements

Ask the user:
- NFT name and symbol?
- Max supply?
- Mint price (free or paid)?
- Who can mint (public or owner-only)?
- Any metadata URI pattern?

### Step 2: Initialize

```bash
jovay dapp init --name my-nft-dapp
cd my-nft-dapp
npm install
npm install @openzeppelin/contracts
```

### Step 3: Write contract

Create `contracts/MyNFT.sol` with ERC721 + URIStorage + Enumerable + Ownable.

### Step 4: Write deploy script

Update `scripts/deploy.js` to deploy MyNFT with constructor arguments.

### Step 5: Compile & test

```bash
npx hardhat compile
npx hardhat test
```

### Step 6: Deploy to testnet

```bash
jovay dapp deploy
```

Record the deployed contract address.

### Step 7: Generate frontend

- Update `frontend/src/config/index.js` with contract address
- Copy ABI to `frontend/src/contracts/`
- Create mint page with form: token URI input, mint button
- Add gallery page showing owned NFTs
- Implement wallet connection

### Step 8: Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, connect MetaMask, test minting.

</assistant_response>
</example>

<example>
<user_query>Help me create a token airdrop dApp</user_query>
<assistant_response>

### Step 1: Gather requirements

Ask the user:
- Token name and symbol?
- Total supply?
- Airdrop amount per address?
- Any claiming restrictions (whitelist, time limit)?
- One-time claim or multiple?

### Step 2: Initialize and write contracts

Two contracts needed:
1. `MyToken.sol` — ERC20 with minting
2. `Airdrop.sol` — Holds tokens and manages claims

### Step 3: Frontend

- Claim page: connect wallet, check eligibility, claim button
- Admin page: fund airdrop contract, set whitelist
- Status page: show total distributed, remaining

### Step 4: Deploy both contracts, fund airdrop

Deploy token → deploy airdrop → transfer tokens to airdrop contract.

</assistant_response>
</example>

<example>
<user_query>Build a simple voting dApp</user_query>
<assistant_response>

### Step 1: Gather requirements

Ask the user:
- What types of proposals?
- Who can create proposals (admin or anyone)?
- Who can vote (any address or token holders)?
- Voting period?
- Any quorum requirement?

### Step 2: Write Voting contract

Create `contracts/Voting.sol` with proposal creation, voting, and result tallying.

### Step 3: Frontend

- Create proposal form (admin)
- List active proposals with vote buttons
- Show results for ended proposals
- Dashboard with voting statistics

### Step 4: Deploy and test

Deploy contract, create test proposals through CLI or frontend.

</assistant_response>
</example>

---

## Important Notes

1. **Always deploy to testnet** unless the user explicitly requests mainnet. Use `jovay network switch --network testnet` to ensure testnet.
2. **Testnet ETH**: Ensure the wallet has sufficient testnet ETH. Use `jovay wallet airdrop` (limited to once per 24h, gives 0.001 ETH).
3. **Amount units**: All amounts in Wei for ETH (1 ETH = 10^18 Wei).
4. **Frontend is local only**: The frontend is for local development/testing. Do NOT deploy the frontend to any hosting service unless the user explicitly asks.
5. **ABI sync**: After any contract recompilation, re-copy the ABI JSON to `frontend/src/contracts/`.
6. **Gas estimation**: Jovay L2 has low gas fees, but always test transactions before production.
7. **Security**: Never hardcode private keys in frontend code. Use MetaMask for all signing operations.
8. **Contract verification**: After deployment, verify the contract address exists on the Jovay testnet explorer.
9. **Encrypted wallet**: If the user set up an encrypted wallet with `jovay init --enc`, they need `--enc-key` for build and deploy commands.
10. **Hardhat network**: The Hardhat config uses `jovay_testnet` as the network name. The `jovay dapp build/deploy` commands handle the environment variables automatically.
