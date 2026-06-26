---
name: giveaway-skills
display_name: BSC Giveaway Contract Call Skill
description: >
  Call guide and best practices for the BSC on-chain giveaway contract based on contracts/contracts/Giveaway.sol, including contract address, core method signatures, parameter meanings, and conventions for calling the contract from scripts, frontends, or OpenClow workflows via ethers/web3. Use this skill when you need to create giveaways, claim giveaways, manage whitelists, or withdraw expired giveaways on BSC.
author: frank
version: 0.1.0
language: en
tags:
  - bsc
  - evm
  - giveaway
  - contract-call
---

# BSC Giveaway Contract Call Skill

## 1. Deployment information

- **Network**: BSC (Binance Smart Chain mainnet, chainId = 56)
- **Contract file**: `contracts/contracts/Giveaway.sol`
- **Contract address**: `0xc9Db158004fEFe15633eF2Ac3C3eA209e58Db5B9`
- **Main dependencies**: `IERC20`, `Ownable`, `ReentrancyGuard`, internal `TransferHelper` library

Assumptions when calling:
- You are already connected to a BSC mainnet RPC (for example `https://bsc-dataseed.binance.org`)
- Account balance and gas settings are handled by the caller

## 2. Core enums and structs (pass as uint in calls)

**DistributionType**
- `0` = AVERAGE: equal share, each claim gets `amount / count`
- `1` = RANDOM: random share, a single claim is roughly in the range \(0 \sim 2 \times\) the average

**ClaimRestriction**
- `0` = PUBLIC: public, no additional restriction
- `1` = TOKEN_HOLDER: only addresses holding `restrictionToken` with balance ≥ `minTokenBalance`
- `2` = WHITELIST: only whitelisted addresses can claim

**GiveawayInfo**
- `token`: token address for the giveaway, `address(0)` means BNB
- `sender`: creator address
- `amount`: current remaining total giveaway amount in the contract (after creation fee is deducted)
- `count`: current remaining claimable slots
- `distributionType`: distribution type (0/1)
- `restriction`: claim restriction type (0/1/2)
- `restrictionToken`: restriction token address (only meaningful for TOKEN_HOLDER)
- `minTokenBalance`: minimum token balance required
- `lastDate`: expiration timestamp (seconds)

## 3. Write function cheatsheet

### 3.1 Create giveaway `createGiveaway`

Signature:

```solidity
function createGiveaway(
    address token,
    uint256 amount,
    uint256 count,
    DistributionType distributionType,
    ClaimRestriction restriction,
    address restrictionToken,
    uint256 minTokenBalance,
    string memory content,
    uint256 lastDate
) public payable
```

Key constraints:
- `bytes(content).length < 128`
- `amount > 0`
- `amount / count > 0`
- `distributionType` ∈ {0,1}
- `restriction` ∈ {0,1,2}
- If `restriction == TOKEN_HOLDER (1)`:
  - `restrictionToken != address(0)`
  - `minTokenBalance > 0`

Fees and transfers:
- Fee: `feeAmount = (amount / 1000) * FEERATE`, sent directly to `FEEADDRESS`
- Actual amount entering the contract: `sendAmount = amount - feeAmount`
- If `token == address(0)` (BNB giveaway):
  - Transaction `msg.value >= amount`
  - `feeAmount` and `sendAmount` are both paid in BNB
- If `token != address(0)` (ERC20 giveaway):
  - Transaction `msg.value == 0`
  - You must first `approve` on-chain:
    - `approve(contract, amount)` (user → contract)
  - The contract internally uses `safeTransferFrom` to send `feeAmount` to `FEEADDRESS` and `sendAmount` to the contract itself

### 3.2 Claim giveaway `claimGiveaway`

```solidity
function claimGiveaway(uint256 id) public nonReentrant
```

Internal checks:
- `giveawayInfos[id].amount != 0`: giveaway exists and has remaining amount
- Caller has not claimed yet: `giveawayInfo_exist[id][msg.sender] == 0`
- Not expired: `giveawayInfos[id].lastDate > block.timestamp`
- TOKEN_HOLDER: check `IERC20(restrictionToken).balanceOf(msg.sender) >= minTokenBalance`
- WHITELIST: `giveawayWhitelist[id][msg.sender] == true`

Distribution logic:
- AVERAGE:
  - If `count == 1`: send all remaining amount to the current claimer
  - Otherwise, single claim amount is `sendAmount = amount / count`
- RANDOM:
  - If `count == 1`: also send all remaining amount
  - Otherwise:
    - `randomNumber = uint8(keccak256(...)) % 100`
    - `sendAmount = (amount / count * 2) * randomNumber / 100`

### 3.3 Withdraw expired giveaway `withdrawExpiredGiveaway`

```solidity
function withdrawExpiredGiveaway(uint256 id) public nonReentrant
```

Constraints:
- `giveawayInfos[id].amount != 0`
- `giveawayInfos[id].sender == msg.sender`
- `giveawayInfos[id].lastDate < block.timestamp`

Withdrawal fee:
- `feeAmount = (amount / 1000) * EXPIREDRATE`
- `sendAmount = amount - feeAmount`
- Transfer logic also distinguishes BNB vs ERC20

### 3.4 Whitelist management

```solidity
function addToWhitelist(uint256 giveawayId, address[] memory addresses) public
function removeFromWhitelist(uint256 giveawayId, address[] memory addresses) public
```

Constraints:
- Only the giveaway creator: `giveawayInfos[giveawayId].sender == msg.sender`
- And the giveaway must be of WHITELIST type: `restriction == ClaimRestriction.WHITELIST`

## 4. Read function cheatsheet

```solidity
function getGiveawayInfo(uint256 id) external view returns (GiveawayInfo memory)
function isInWhitelist(uint256 giveawayId, address user) external view returns (bool)
function canClaim(uint256 id, address user) external view returns (bool)
```

Key points of `canClaim`:
- Returns `false` if amount is 0, already claimed, or `block.timestamp >= lastDate`
- TOKEN_HOLDER: checks token balance
- WHITELIST: checks whitelist
- Otherwise returns `true` (PUBLIC)

## 5. Script / frontend usage example (ethers.js)

Assume you already have a `provider` / `signer` and have loaded the compiled ABI:

```ts
import { ethers } from "ethers";
import GiveawayAbi from "../artifacts/contracts/Giveaway.sol/Giveaway.json";

const GIVEAWAY_ADDRESS = "0xc9Db158004fEFe15633eF2Ac3C3eA209e58Db5B9";

// Create contract instance (read or write)
export function getGiveawayContract(providerOrSigner: ethers.Signer | ethers.providers.Provider) {
  return new ethers.Contract(GIVEAWAY_ADDRESS, GiveawayAbi.abi, providerOrSigner);
}

// Example: create a BNB giveaway
export async function createBnbGiveaway(
  signer: ethers.Signer,
  params: {
    amountWei: ethers.BigNumberish;
    count: number;
    distributionType: 0 | 1;
    restriction: 0 | 1 | 2;
    restrictionToken: string;
    minTokenBalance: ethers.BigNumberish;
    content: string;
    lastDate: number;
  }
) {
  const contract = getGiveawayContract(signer);
  const tx = await contract.createGiveaway(
    ethers.constants.AddressZero,
    params.amountWei,
    params.count,
    params.distributionType,
    params.restriction,
    params.restrictionToken,
    params.minTokenBalance,
    params.content,
    params.lastDate,
    { value: params.amountWei }
  );
  return tx.wait();
}

// Example: claim a giveaway
export async function claimGiveaway(signer: ethers.Signer, id: number) {
  const contract = getGiveawayContract(signer);
  const tx = await contract.claimGiveaway(id);
  return tx.wait();
}
```

When integrating in a frontend or script:
- **Read functions** (`getGiveawayInfo`, `canClaim`, `isInWhitelist`) can use a `provider` instance;
- **Write functions** (`createGiveaway`, `claimGiveaway`, `withdrawExpiredGiveaway`, whitelist add/remove) must use a `signer` with signing capability;
- For BNB giveaways you must pass BNB equal to `amount` via `value`; for ERC20 giveaways you must `approve` beforehand.

## 7. ABI information and minimal examples

- **Full ABI source**: the JSON generated after compiling `contracts/contracts/Giveaway.sol` in this repo (for example `artifacts/.../Giveaway.json`); in scripts/frontends you should generally import the `abi` field from that file.
- **Purpose of this section**: provide a **minimal ABI fragment** for quick debugging or building a minimal frontend/script when you cannot directly access the compiled artifacts. It is **not** guaranteed to stay perfectly in sync with future contract upgrades.

### 7.1 Key event fragments

```json
[
  {
    "type": "event",
    "name": "GiveawayCreated",
    "anonymous": false,
    "inputs": [
      { "indexed": false, "name": "id", "type": "uint256" },
      { "indexed": false, "name": "token", "type": "address" },
      { "indexed": false, "name": "sender", "type": "address" },
      { "indexed": false, "name": "amount", "type": "uint256" },
      { "indexed": false, "name": "count", "type": "uint256" },
      { "indexed": false, "name": "distributionType", "type": "uint8" },
      { "indexed": false, "name": "restriction", "type": "uint8" },
      { "indexed": false, "name": "restrictionToken", "type": "address" },
      { "indexed": false, "name": "minTokenBalance", "type": "uint256" },
      { "indexed": false, "name": "content", "type": "string" },
      { "indexed": false, "name": "lastDate", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "GiveawayClaimed",
    "anonymous": false,
    "inputs": [
      { "indexed": false, "name": "id", "type": "uint256" },
      { "indexed": false, "name": "sender", "type": "address" },
      { "indexed": false, "name": "count", "type": "uint256" },
      { "indexed": false, "name": "amount", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "GiveawayWithdrawn",
    "anonymous": false,
    "inputs": [
      { "indexed": false, "name": "id", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "WhitelistAdded",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "giveawayId", "type": "uint256" },
      { "indexed": false, "name": "addresses", "type": "address[]" }
    ]
  },
  {
    "type": "event",
    "name": "WhitelistRemoved",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "giveawayId", "type": "uint256" },
      { "indexed": false, "name": "addresses", "type": "address[]" }
    ]
  }
]
```

### 7.2 Common function fragments

> Only the most common read/write function signatures are listed below, to make it easy to construct `ethers.Contract` / `web3.eth.Contract`. For the full ABI, always refer to the build artifacts.

```json
[
  {
    "type": "function",
    "stateMutability": "payable",
    "name": "createGiveaway",
    "inputs": [
      { "name": "token", "type": "address" },
      { "name": "amount", "type": "uint256" },
      { "name": "count", "type": "uint256" },
      { "name": "distributionType", "type": "uint8" },
      { "name": "restriction", "type": "uint8" },
      { "name": "restrictionToken", "type": "address" },
      { "name": "minTokenBalance", "type": "uint256" },
      { "name": "content", "type": "string" },
      { "name": "lastDate", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "claimGiveaway",
    "inputs": [
      { "name": "id", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "withdrawExpiredGiveaway",
    "inputs": [
      { "name": "id", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "addToWhitelist",
    "inputs": [
      { "name": "giveawayId", "type": "uint256" },
      { "name": "addresses", "type": "address[]" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "removeFromWhitelist",
    "inputs": [
      { "name": "giveawayId", "type": "uint256" },
      { "name": "addresses", "type": "address[]" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getGiveawayInfo",
    "inputs": [
      { "name": "id", "type": "uint256" }
    ],
    "outputs": [
      {
        "components": [
          { "name": "token", "type": "address" },
          { "name": "sender", "type": "address" },
          { "name": "amount", "type": "uint256" },
          { "name": "count", "type": "uint256" },
          { "name": "distributionType", "type": "uint8" },
          { "name": "restriction", "type": "uint8" },
          { "name": "restrictionToken", "type": "address" },
          { "name": "minTokenBalance", "type": "uint256" },
          { "name": "lastDate", "type": "uint256" }
        ],
        "type": "tuple"
      }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "canClaim",
    "inputs": [
      { "name": "id", "type": "uint256" },
      { "name": "user", "type": "address" }
    ],
    "outputs": [
      { "type": "bool" }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "isInWhitelist",
    "inputs": [
      { "name": "giveawayId", "type": "uint256" },
      { "name": "user", "type": "address" }
    ],
    "outputs": [
      { "type": "bool" }
    ]
  }
]
```

The fragments above can be combined with the TypeScript example earlier, for example:

```ts
const abi = [...eventsFragment, ...functionsFragment];
const contract = new ethers.Contract(GIVEAWAY_ADDRESS, abi, signerOrProvider);
```

## 6. Relationship with existing `giveaway-protocol` skill

- `giveaway-protocol` focuses more on the **protocol-level** description (enum semantics, logical constraints, general call conventions);
- `giveaway-skills` is specifically about **this concrete contract deployed on BSC mainnet** (fixed contract address + specific network info + call examples).

When you need “the contract address and direct on-chain interaction”, you should prefer this skill.  
If you need more complete error descriptions or protocol details, you can also refer to `giveaway-protocol`’s `reference.md`.
