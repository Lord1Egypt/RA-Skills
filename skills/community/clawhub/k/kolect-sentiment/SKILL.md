
---
name: kolect-sentiment-feed
description: Use this skill when the user wants to read, explain, or interact with the Kolect Sentiment Feed contract on Base, including querying sentiment, checking freshness, checking pending requests, and requesting new on-chain sentiment updates for supported symbols and time windows.
---

# Kolect Sentiment Feed

## Purpose

Use this skill for the **Kolect Sentiment Feed** contract, an on-chain sentiment oracle on **Base**.

It stores normalized sentiment for supported `(symbol, timeWindow)` pairs through a request–response flow:

1. User requests an update on-chain
2. Off-chain publisher fetches sentiment from Kolect API
3. Publisher fulfills the request on-chain with normalized BPS data

Use this skill when the user wants to:
- read the latest sentiment
- check freshness
- check pending request state
- request a new update
- understand how the oracle works
- integrate the feed into AI agents, trading, dashboards, or DeFi logic

---

## Contract

- Project: Kolect
- Module: Kolect Sentiment Feed
- Version: v1.0.0
- Network: Base
- Address: `0x6783ab3c181976e8c960c43d711aaf4da79a4e4b`
- Explorer: `https://base.blockscout.com/address/0x6783ab3c181976e8c960c43d711aaf4da79a4e4b`
- Website: `https://kolect.info`
- Twitter/X: `https://x.com/kolect_info`

---

## Interaction Types

### Read-only calls
Usually used to inspect current state:
- `getLatest(symbol, timeWindow)`
- `isFresh(symbol, timeWindow)`
- `hasPendingRequest(symbol, timeWindow)`

These are normally read calls and do **not** require the contract request fee.

### Write call
Used to initiate a new oracle update:
- `requestUpdate(symbol, timeWindow)`

This is **not** a free read. It is a state-changing transaction:
- requires gas
- may require request fee payment

Never present `requestUpdate` as a free data read.

---

## Data Model

Each feed is identified by:
- `symbol`
- `timeWindow`

Examples:
- `(BTC, 1d)`
- `(ETH, 1h)`

Each feed stores:
- `negativeBps`
- `neutralBps`
- `positiveBps`
- `dataTimestamp` — off-chain data time
- `updatedAt` — on-chain fulfillment time

### Invariant

`negativeBps + neutralBps + positiveBps = 10000`

Interpretation:
- `10000` = 100.00%
- `2500` = 25.00%
- `5000` = 50.00%

Always preserve and validate this rule.

---

## Core Workflow

### 1. Request update
Function:
`requestUpdate(string symbol, string timeWindow)`

Should only succeed if:
- symbol is supported
- time window is supported
- feed is not already fresh
- no pending request exists
- required fee is paid

### 2. Off-chain processing
Publisher:
- listens to `UpdateRequested`
- fetches sentiment from Kolect API
- normalizes result into BPS

### 3. Fulfillment
Function:
`fulfillRequest(requestId, negativeBps, neutralBps, positiveBps, dataTimestamp)`

Result:
- data stored on-chain
- request marked fulfilled
- event emitted

### 4. Failure
Function:
`failRequest(requestId, errorCode)`

Used when data retrieval or fulfillment fails.

---

## Functions

### User
- `requestUpdate(string symbol, string timeWindow)`

### View
- `getLatest(symbol, timeWindow)`
- `isFresh(symbol, timeWindow)`
- `hasPendingRequest(symbol, timeWindow)`

### Publisher
- `fulfillRequest(...)`
- `failRequest(...)`

### Owner
- `setSupportedSymbol(...)`
- `setSupportedTimeWindow(...)`
- `setUpdateInterval(...)`
- `setRequestFee(...)`
- `withdrawFees(...)`

Do not imply ordinary users can call owner-only functions.

---

## Events

Important indexing events:
- `UpdateRequested`
- `RequestFulfilled`
- `RequestFailed`

Use these when discussing dashboards, Dune, subgraphs, analytics, or automation.

---

## Decision Logic

### If the user wants the latest sentiment
1. Identify `symbol` and `timeWindow`
2. Use `getLatest(symbol, timeWindow)`
3. Present:
   - negative / neutral / positive
   - both BPS and %
   - `dataTimestamp`
   - `updatedAt`

### If the user asks whether an update is needed
1. Check `isFresh(symbol, timeWindow)`
2. If fresh, explain no update may be needed
3. If stale, explain `requestUpdate` may be appropriate

### If the user wants to request an update
1. Identify `symbol` and `timeWindow`
2. Check:
   - supported symbol
   - supported time window
   - not fresh
   - no pending request
   - fee requirement
3. Then prepare or describe `requestUpdate(symbol, timeWindow)`

### If the user asks why a request may fail
Likely reasons:
- unsupported symbol
- unsupported time window
- feed already fresh
- request already pending
- fee missing
- publisher fulfillment failure

---

## Output Format

When reporting sentiment, use:

- Symbol: BTC
- Time window: 1d
- Negative: 2300 BPS (23.00%)
- Neutral: 4100 BPS (41.00%)
- Positive: 3600 BPS (36.00%)
- Data timestamp: [off-chain time]
- Updated on-chain at: [on-chain time]
- Fresh: [true/false if known]
- Pending request: [true/false if known]

Do not report only raw integers unless explicitly requested.

---

## Validation Rules

Whenever sentiment data is given, validate:
1. `negativeBps + neutralBps + positiveBps == 10000`
2. each value is non-negative
3. `dataTimestamp` = off-chain data time
4. `updatedAt` = on-chain update time

If the sum is not `10000`, flag it as invalid.

---

## Python Examples

### Read latest sentiment

```python
from web3 import Web3

RPC_URL = "https://mainnet.base.org"
CONTRACT_ADDRESS = Web3.to_checksum_address("0x6783ab3c181976e8c960c43d711aaf4da79a4e4b")

ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "string", "name": "timeWindow", "type": "string"}
        ],
        "name": "getLatest",
        "outputs": [
            {"internalType": "uint256", "name": "negativeBps", "type": "uint256"},
            {"internalType": "uint256", "name": "neutralBps", "type": "uint256"},
            {"internalType": "uint256", "name": "positiveBps", "type": "uint256"},
            {"internalType": "uint256", "name": "dataTimestamp", "type": "uint256"},
            {"internalType": "uint256", "name": "updatedAt", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

symbol = "BTC"
time_window = "1d"

negative_bps, neutral_bps, positive_bps, data_timestamp, updated_at = (
    contract.functions.getLatest(symbol, time_window).call()
)

print("Negative:", negative_bps, f"({negative_bps / 100:.2f}%)")
print("Neutral:", neutral_bps, f"({neutral_bps / 100:.2f}%)")
print("Positive:", positive_bps, f"({positive_bps / 100:.2f}%)")
print("Data timestamp:", data_timestamp)
print("Updated at:", updated_at)
````

### Check freshness and pending request

```python
from web3 import Web3

RPC_URL = "https://mainnet.base.org"
CONTRACT_ADDRESS = Web3.to_checksum_address("0x6783ab3c181976e8c960c43d711aaf4da79a4e4b")

ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "string", "name": "timeWindow", "type": "string"}
        ],
        "name": "isFresh",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "string", "name": "timeWindow", "type": "string"}
        ],
        "name": "hasPendingRequest",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

symbol = "ETH"
time_window = "1h"

fresh = contract.functions.isFresh(symbol, time_window).call()
pending = contract.functions.hasPendingRequest(symbol, time_window).call()

print("Fresh:", fresh)
print("Pending:", pending)
```

### Request an update

```python
from web3 import Web3

RPC_URL = "https://mainnet.base.org"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"
ACCOUNT = "YOUR_WALLET_ADDRESS"
CONTRACT_ADDRESS = Web3.to_checksum_address("0x6783ab3c181976e8c960c43d711aaf4da79a4e4b")

ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "string", "name": "timeWindow", "type": "string"}
        ],
        "name": "requestUpdate",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

symbol = "BTC"
time_window = "1d"
request_fee_wei = 0  # replace with actual fee if needed

tx = contract.functions.requestUpdate(symbol, time_window).build_transaction({
    "from": ACCOUNT,
    "nonce": w3.eth.get_transaction_count(ACCOUNT),
    "value": request_fee_wei,
    "gas": 300000,
    "gasPrice": w3.eth.gas_price,
    "chainId": 8453
})

signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print(tx_hash.hex())
```

---

## JavaScript Examples

### Read latest sentiment

```javascript
import { ethers } from "ethers";

const RPC_URL = "https://mainnet.base.org";
const CONTRACT_ADDRESS = "0x6783ab3c181976e8c960c43d711aaf4da79a4e4b";

const ABI = [
  "function getLatest(string symbol, string timeWindow) view returns (uint256 negativeBps, uint256 neutralBps, uint256 positiveBps, uint256 dataTimestamp, uint256 updatedAt)"
];

const provider = new ethers.JsonRpcProvider(RPC_URL);
const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, provider);

const result = await contract.getLatest("BTC", "1d");

console.log(Number(result.negativeBps), Number(result.neutralBps), Number(result.positiveBps));
console.log(Number(result.dataTimestamp), Number(result.updatedAt));
```

### Check freshness and pending request

```javascript
import { ethers } from "ethers";

const RPC_URL = "https://mainnet.base.org";
const CONTRACT_ADDRESS = "0x6783ab3c181976e8c960c43d711aaf4da79a4e4b";

const ABI = [
  "function isFresh(string symbol, string timeWindow) view returns (bool)",
  "function hasPendingRequest(string symbol, string timeWindow) view returns (bool)"
];

const provider = new ethers.JsonRpcProvider(RPC_URL);
const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, provider);

const fresh = await contract.isFresh("ETH", "1h");
const pending = await contract.hasPendingRequest("ETH", "1h");

console.log("Fresh:", fresh);
console.log("Pending:", pending);
```

### Request an update

```javascript
import { ethers } from "ethers";

const RPC_URL = "https://mainnet.base.org";
const PRIVATE_KEY = "YOUR_PRIVATE_KEY";
const CONTRACT_ADDRESS = "0x6783ab3c181976e8c960c43d711aaf4da79a4e4b";

const ABI = [
  "function requestUpdate(string symbol, string timeWindow) payable"
];

const provider = new ethers.JsonRpcProvider(RPC_URL);
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, wallet);

const tx = await contract.requestUpdate("BTC", "1d", {
  value: 0n // replace with actual request fee if needed
});

console.log(tx.hash);
await tx.wait();
```

---

## Recommended Agent Behavior

An AI agent should use the feed in this order:

1. `getLatest(symbol, timeWindow)`
2. validate BPS values
3. `isFresh(symbol, timeWindow)`
4. `hasPendingRequest(symbol, timeWindow)`
5. only if stale and no pending request exists:

   * prepare or send `requestUpdate(symbol, timeWindow)`

Recommended phrasing:

> The Kolect Sentiment Feed lets the agent consume verifiable on-chain sentiment state. The agent should first read current state, then verify freshness, and only request a new update when needed.

---

## Action Policy

* If the user asks for explanation only, explain the contract and do not push a write transaction.
* If the user asks for current sentiment, prefer read calls first.
* If the user asks to refresh, explain freshness and pending checks before suggesting `requestUpdate`.
* Never suggest owner-only functions unless the user is explicitly admin/operator.
* Never imply all interactions are free. Read calls are usually free from the contract side; write calls need gas and may need request fee.

---

## Safe Assumptions

The model may assume:

* this contract is on Base
* the address above is the intended deployment
* sentiment is normalized in BPS

The model must not assume without checking:

* supported symbols
* supported time windows
* current request fee
* current update interval
* whether a feed is fresh right now
* whether a request is pending right now

These are dynamic contract states.

---

## Anti-Patterns

Do not:

* confuse BPS with percentages
* say the contract computes sentiment internally
* describe the feed as auto-updating on a timer
* assume request fee is zero
* merge `dataTimestamp` and `updatedAt`
* assume all symbols and time windows are supported by default
* tell the user to call `requestUpdate` before checking freshness and pending state

---

## Minimal Cheat Sheet

**Chain:** Base
**Contract:** `0x6783ab3c181976e8c960c43d711aaf4da79a4e4b`

**Main user action**

* `requestUpdate(symbol, timeWindow)`

**Main read functions**

* `getLatest(symbol, timeWindow)`
* `isFresh(symbol, timeWindow)`
* `hasPendingRequest(symbol, timeWindow)`

**Publisher functions**

* `fulfillRequest(...)`
* `failRequest(...)`

**Key events**

* `UpdateRequested`
* `RequestFulfilled`
* `RequestFailed`

**Core invariant**

* `negativeBps + neutralBps + positiveBps = 10000`

