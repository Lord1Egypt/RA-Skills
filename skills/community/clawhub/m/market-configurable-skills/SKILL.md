---
name: market-configurable-skills
display_name: GouGouBi Configurable Price Prediction Market Skill
description: >
  Call guide and best practices for the configurable crypto price prediction market contracts GouGouBiMarketConfigurable.sol and GouGouBiMarketConfigurableFactory.sol, including factory creation parameters, market configuration fields, core trading/settlement methods, and conventions for calling the contracts from scripts, frontends, or OpenClow workflows via ethers/web3. Use this skill when you need to create new prediction markets, buy YES/NO, swap positions, or redeem settlements.
author: frank
version: 0.1.0
language: en
tags:
  - prediction-market
  - evm
  - contract-call
---

# Configurable Crypto Price Prediction Market Skill

## 1. Protocol and contract overview

- **Market contract**: `contracts/contracts/GouGouBiMarketConfigurable.sol`
- **Factory contract**: `contracts/contracts/GouGouBiMarketConfigurableFactory.sol`
- **Model**: Polymarket-style CPMM YES/NO prediction market. Each round has its own YES/NO outcome tokens and uses a constant product market maker.
- **Key features**:
  - Uses Uniswap V3 pool prices as the oracle and computes time-windowed average prices.
  - Configurable to predict `token0/token1` or the reverse (`reverseOrder`).
  - Supports native coin or arbitrary ERC20 as the liquidity token.
  - Automatically starts a new round on schedule, and supports expiry handling and abnormal price handling (surfaced via events).

> This skill only describes the **contract APIs and calling patterns**. The actual deployment network and addresses should be provided by the product layer (for example via dApp config files or OpenClow workflow parameters).

---

## 2. Factory contract `GouGouBiMarketConfigurableFactory`

### 2.1 Core roles and state

- `owner`: factory admin, manages the creator whitelist.
- `marketImplementation`: implementation contract being cloned (`GouGouBiMarketConfigurable`).
- `isWhitelistedCreator[address]`: whether an address is allowed to call `createMarket`.
- `markets[]`: list of all created market addresses.
- `marketIndex[market]`: index of a market address (starting from 1, 0 means not created by this factory).
- `marketRecords[index]`: creation records (see below).

### 2.2 `MarketRecord` structure (read-only)

For each market created by the factory:

- `market`: market contract address
- `creator`: creator address
- `marketName`: market name
- `uniswapV3Pool`: Uniswap V3 pool address
- `liquidityToken`: liquidity token address, `address(0)` means native coin
- `feeRecipient`: fee recipient address
- `feeRate`: fee rate (denominator 10000)
- `createdAt`: creation timestamp
- The following fields align with `GouGouBiMarketConfigurable.MarketConfig` (see section 3):
  - `tokenDec`
  - `reverseOrder`
  - `settlementInterval`
  - `expiredSeconds`
  - `initialReserve`
  - `priceLookbackSeconds`
  - `imageUrl`
  - `rules`
  - `timezone`
  - `language`
  - `groupUrl`
  - `tags`
  - `predictionToken`
  - `anchorToken`
  - `currencyUnit`

### 2.3 Managing creator whitelist

```solidity
function setCreatorWhitelist(address account, bool allowed) external onlyOwner
function setCreatorWhitelistBatch(address[] calldata accounts, bool allowed) external onlyOwner
```

- Only the factory `owner` can call these.
- Must ensure `account != address(0)`.

### 2.4 Creating a market: `createMarket`

```solidity
function createMarket(GouGouBiMarketConfigurable.MarketConfig memory _config)
    external
    returns (address market)
```

Constraints:

- Only `owner` or an address with `isWhitelistedCreator[msg.sender] == true` can create:
  - `require(msg.sender == owner || isWhitelistedCreator[msg.sender], "NOT_WHITELISTED");`
- Internal flow:
  1. Use `Clones.clone(marketImplementation)` to create a minimal proxy.
  2. Call the new market’s `initialize(_config, msg.sender)` to set config and owner.
  3. Push the market address into `markets[]`, populate `marketRecords`, and update `marketIndex`.
  4. Emit `MarketCreated` event with key configuration info.

Read-only helpers:

```solidity
function getMarkets() external view returns (address[] memory)
function marketCount() external view returns (uint256)
function getMarketRecord(uint256 index) external view returns (MarketRecord memory)
function getMarketRecordsPaginated(uint256 offset, uint256 limit) external view returns (MarketRecord[] memory)
```

---

## 3. Market configuration `MarketConfig` (passed when creating)

The `_config` used by factory `createMarket` is identical to the `MarketConfig` struct inside the market contract:

```solidity
struct MarketConfig {
    string marketName;
    address uniswapV3Pool;
    address liquidityToken;    // address(0) means native coin
    uint8 tokenDec;            // if liquidityToken==0, automatically set to 18 in initialize
    bool reverseOrder;         // price direction: false=Token0/Token1, true=Token1/Token0
    uint256 settlementInterval; // settlement interval in seconds
    uint256 expiredSeconds;     // round expires and is void if not resolved by this time
    uint256 initialReserve;     // initial virtual reserve per round (will be multiplied by 10^decimals)
    uint32 priceLookbackSeconds;// lookback window for average price
    address feeRecipient;       // fee recipient address
    uint256 feeRate;            // fee numerator, denominator 10000
    string imageUrl;
    string rules;
    string timezone;
    string language;
    string groupUrl;
    string[] tags;
    address predictionToken;    // token whose price is being predicted
    address anchorToken;        // quote/anchor token, e.g. USDT, BNB
    string currencyUnit;        // display unit, e.g. "USD", "BNB", "DOGE"
}
```

Key constraints (validated in `initialize`):

- `marketName` must be non-empty: `bytes(_config.marketName).length > 0`
- `uniswapV3Pool != address(0)`
- `settlementInterval > 0`
- `expiredSeconds > 0`
- `0 < initialReserve <= 1_000_000_000`
- `feeRate <= FEE_DENOMINATOR (10000)`
- If `feeRate > 0`, then `feeRecipient != address(0)`; otherwise it will default to `_owner`.
- If `liquidityToken == address(0)`: `tokenDec` is automatically set to 18.
- If `liquidityToken != address(0)`: `tokenDec = IERC20(liquidityToken).decimals()`, requiring `tokenDec <= 18`.
- If `priceLookbackSeconds == 0`: it is automatically set to 300 seconds.

After initialization, the contract immediately calls `_startNewRound()` to open round 1.

---

## 4. Market rounds `RoundInfo` and price settlement

### 4.1 `RoundInfo` structure

```solidity
struct RoundInfo {
    uint8 winning;              // 0=not settled, 1=YES wins, 2=NO wins, 3=draw/exception
    uint256 poolAmount;         // total liquidity token amount in the pool for this round
    uint256 x;                  // CPMM x reserve (YES pool)
    uint256 y;                  // CPMM y reserve (NO pool)
    address yesToken;           // YES outcome token for this round
    address noToken;            // NO outcome token for this round
    uint256 startTime;          // round start time
    uint256 endTime;            // scheduled settlement time
    uint256 expiredTime;        // expiration time (if exceeded, treated as winning=3)
    uint256 startAveragePrice;  // average price at round start
    uint256 endAveragePrice;    // average price at round end / settlement
}
```

- Accessed via the read-only mapping `rounds[round]`.
- Current round index: `currentRound`.

### 4.2 Price fetching: `getAveragePriceFromUniswapV3`

```solidity
function getAveragePriceFromUniswapV3(uint32 startTime, uint32 endTime)
    public
    view
    returns (uint256 averagePrice)
```

- `startTime < endTime`, and `endTime <= block.timestamp`.
- Internally uses Uniswap V3 `observe` + `TickMath` to compute the average price over the interval, represented with `1e18` precision.
- If `reverseOrder == true`, takes the reciprocal of the price (still with `1e18` precision).

### 4.3 Settlement and round transitions

- `_checkAndExecuteSettlement()`: called before every trade/redeem/resolve to:
  - If `block.timestamp > expiredTime`: set `winning = 3`, `endAveragePrice = 0`, emit `AutoResolve` event, and start a new round.
  - If the current round has reached `endTime` and not yet expired: call `_calculateSettlementByPrice()`.
- `_calculateSettlementByPrice()`:
  - Uses `getAveragePriceFromUniswapV3(priceLookbackSeconds, 0)` to get the settlement-time average price.
  - Compares with `startAveragePrice`:
    - equal → `winning = 3` (draw/special situation)
    - settlement price > start price → `winning = 1` (YES wins)
    - settlement price < start price → `winning = 2` (NO wins)
  - Updates `endTime` and `endAveragePrice`, emits `AutoResolve`, then starts a new round.

External callers can trigger the check manually:

```solidity
function resolve() external nonReentrant {
    _checkAndExecuteSettlement();
}
```

---

## 5. Core user interaction methods

### 5.1 Buying YES / NO

#### 5.1.1 `buyYes`

```solidity
function buyYes(uint256 tokenIn, uint256 minYesOut) external payable nonReentrant
```

Semantics:

- For the current `currentRound`:
  - If the market uses the native coin (`liquidityToken == address(0)`):
    - Ignore `tokenIn`, use `msg.value` as the input amount, requiring `msg.value > 0`.
  - If using an ERC20:
    - Require `tokenIn > 0 && msg.value == 0`.
    - Must first call `IERC20(liquidityToken).approve(market, tokenIn)`; the contract uses `safeTransferFrom` internally.
- Contract logic:
  - Add `tokenIn` to `rounds[currentRound].poolAmount`.
  - Mint equal virtual YES/NO positions (`mintedYes = mintedNo = tokenIn`), then use the constant product formula to compute slippage and obtain additional swapped amount.
  - Final YES amount is `totalYesOut = mintedYes + swappedYes`, which must be `>= minYesOut` or the transaction reverts (slippage protection).
  - Use `OutcomeToken(yesToken).mint(msg.sender, totalYesOut)` to issue YES tokens.

#### 5.1.2 `buyNo`

```solidity
function buyNo(uint256 tokenIn, uint256 minNoOut) external payable nonReentrant
```

- Symmetric to `buyYes` but operates on the NO pool, yielding `totalNoOut`, which must be `>= minNoOut`.

### 5.2 Position swaps: `swapYesForNo` / `swapNoForYes`

```solidity
function swapYesForNo(uint256 amountIn, uint256 minAmountOut) external nonReentrant
function swapNoForYes(uint256 amountIn, uint256 minAmountOut) external nonReentrant
```

Common logic:

- Only allowed while `winning == 0` (round not yet settled).
- Caller must already hold the corresponding YES or NO token balance.
- Computes `amountOut` based on the current reserves `x`, `y` and `amountIn`, then checks slippage:
  - `swapYesForNo`: `amountOut = (y * amountIn) / (x + amountIn)`
  - `swapNoForYes`: `amountOut = (x * amountIn) / (y + amountIn)`
- Burns the input tokens via `burn`, mints output tokens via `mint`, and updates `x`, `y`.

### 5.3 Settlement redemption: `redeem`

```solidity
function redeem(uint256 round) external nonReentrant
```

Constraints and flow:

- First calls `_checkAndExecuteSettlement()`, which may change the current round state.
- Requires:
  - `round > 0 && round <= currentRound`
  - `rounds[round].winning != 0` (round already settled: YES wins, NO wins, or draw)
  - `rounds[round].poolAmount > 0`
  - Caller holds at least one of YES/NO tokens for that round.
- Distribution logic:
  - If `winning == 1` (YES wins):
    - Distribute pool amount in proportion to YES token supply shares.
  - If `winning == 2` (NO wins):
    - Distribute in proportion to NO token supply shares.
  - If `winning == 3` (draw/exception):
    - Sum the caller’s YES and NO balances and distribute according to their share of total YES+NO supply.
  - Every payout deducts `tokenOut` from the pool and applies fees by `feeRate`:
    - `fee = tokenOut * feeRate / FEE_DENOMINATOR`
    - User receives `userAmount = tokenOut - fee`
    - Fee is transferred to `config.feeRecipient`
  - Supports both native coin and ERC20 transfers.

### 5.4 Price queries and pool info

```solidity
function priceYes() external view returns (uint256 num, uint256 den)
function priceNo() external view returns (uint256 num, uint256 den)
function getPoolInfo() external view returns (
    uint256 _x, uint256 _y, uint256 _poolAmount,
    uint256 _priceYes, uint256 _priceNo,
    uint256 _currentRound, uint8 _winning
)
function getRoundInfo(uint256 round) external view returns (
    uint8 _winning, uint256 _poolAmount, uint256 _x, uint256 _y,
    address _yesToken, address _noToken,
    uint256 _startTime, uint256 _endTime, uint256 _expiredTime,
    uint256 _startAveragePrice, uint256 _endAveragePrice
)
```

- `priceYes`/`priceNo` return prices as fractions (`num/den`) for UI display or estimation.
- `getPoolInfo` returns current round pool and price information in one call.
- `getRoundInfo` returns detailed data for any round, including YES/NO token addresses and timing info.

---

## 6. Usage examples in scripts / frontends (ethers.js)

> These examples only demonstrate call patterns. The actual `FACTORY_ADDRESS` and market addresses depend on deployment and should be passed via your project config.

```ts
import { ethers } from "ethers";
import MarketAbi from "../artifacts/contracts/GouGouBiMarketConfigurable.sol/GouGouBiMarketConfigurable.json";
import FactoryAbi from "../artifacts/contracts/GouGouBiMarketConfigurableFactory.sol/GouGouBiMarketConfigurableFactory.json";

// Provided by the product side
const FACTORY_ADDRESS = "<REPLACE_WITH_FACTORY_ADDRESS>";

export function getFactory(providerOrSigner: ethers.Signer | ethers.providers.Provider) {
  return new ethers.Contract(FACTORY_ADDRESS, FactoryAbi.abi, providerOrSigner);
}

export function getMarket(
  marketAddress: string,
  providerOrSigner: ethers.Signer | ethers.providers.Provider
) {
  return new ethers.Contract(marketAddress, MarketAbi.abi, providerOrSigner);
}

// Create a new market (requires factory owner or whitelisted address)
export async function createMarket(
  signer: ethers.Signer,
  config: {
    marketName: string;
    uniswapV3Pool: string;
    liquidityToken: string;   // for native-coin markets, pass ethers.constants.AddressZero
    reverseOrder: boolean;
    settlementInterval: number;
    expiredSeconds: number;
    initialReserve: ethers.BigNumberish;
    priceLookbackSeconds?: number;
    feeRecipient?: string;
    feeRate: number;
    imageUrl?: string;
    rules?: string;
    timezone?: string;
    language?: string;
    groupUrl?: string;
    tags?: string[];
    predictionToken: string;
    anchorToken: string;
    currencyUnit: string;
  }
) {
  const factory = getFactory(signer);
  const _config = {
    ...config,
    // Let the contract infer defaults such as tokenDec / priceLookbackSeconds / feeRecipient
    tokenDec: 0,
    priceLookbackSeconds: config.priceLookbackSeconds ?? 0,
    feeRecipient: config.feeRecipient ?? ethers.constants.AddressZero,
    tags: config.tags ?? [],
  };
  const tx = await factory.createMarket(_config);
  const receipt = await tx.wait();
  // You can parse the new market address from the MarketCreated event
  return receipt;
}

// Buy YES in the current round (ERC20 market example)
export async function buyYes(
  signer: ethers.Signer,
  marketAddress: string,
  amountIn: ethers.BigNumberish,
  minYesOut: ethers.BigNumberish
) {
  const market = getMarket(marketAddress, signer);
  const tx = await market.buyYes(amountIn, minYesOut);
  return tx.wait();
}

// Buy NO in the current round (native-coin market example)
export async function buyNoNative(
  signer: ethers.Signer,
  marketAddress: string,
  amountWei: ethers.BigNumberish,
  minNoOut: ethers.BigNumberish
) {
  const market = getMarket(marketAddress, signer);
  const tx = await market.buyNo(0, minNoOut, { value: amountWei });
  return tx.wait();
}

// Redeem settlement for a specific round
export async function redeem(
  signer: ethers.Signer,
  marketAddress: string,
  round: number
) {
  const market = getMarket(marketAddress, signer);
  const tx = await market.redeem(round);
  return tx.wait();
}
```

Recommended integration practices in frontends or automation scripts:

- **Read operations** (`getPoolInfo`, `getRoundInfo`, `priceYes`, `priceNo`, etc.) should use a read-only `provider`.
- **Write operations** (`createMarket`, `buyYes`, `buyNo`, `swapYesForNo`, `swapNoForYes`, `redeem`, `resolve`) must use a `signer` with signing capability.
- For ERC20 markets, call `approve` on the market contract before `buyYes` / `buyNo`; for native-coin markets, attach funds via `value`.
- Frontends should set `minYesOut` / `minNoOut` with reasonable slippage protection (e.g. 95%–99% of expected output).

---

## 7. Relationship with other skills

- This `market-configurable-skills` focuses on the **concrete implementation and calling patterns of the GouGouBi configurable price prediction market**, including factory creation, market configuration fields, and trading/settlement logic.
- If your product also uses the giveaway protocol or other contracts, you can read the corresponding skills (such as `giveaway-skills` / `giveaway-protocol`) together. There is no direct contract-level dependency; they only cooperate at the product level.

---

## 8. ABI information and minimal examples

> For the full ABI, it is recommended to use the compiled artifacts directly (for example, the `abi` fields in `artifacts/contracts/GouGouBiMarketConfigurable.sol/GouGouBiMarketConfigurable.json` and `...Factory.sol/GouGouBiMarketConfigurableFactory.json`). This section only provides **minimal fragments for common events and functions**, for quick debugging or for constructing temporary contract instances when build artifacts are not accessible.

### 8.1 Factory contract `GouGouBiMarketConfigurableFactory` ABI fragments

```json
[
  {
    "type": "event",
    "name": "CreatorWhitelistUpdated",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "account", "type": "address" },
      { "indexed": false, "name": "allowed", "type": "bool" }
    ]
  },
  {
    "type": "event",
    "name": "MarketCreated",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "market", "type": "address" },
      { "indexed": false, "name": "marketName", "type": "string" },
      { "indexed": true, "name": "uniswapV3Pool", "type": "address" },
      { "indexed": true, "name": "creator", "type": "address" },
      { "indexed": false, "name": "liquidityToken", "type": "address" },
      { "indexed": false, "name": "createdAt", "type": "uint256" },
      { "indexed": false, "name": "feeRecipient", "type": "address" },
      { "indexed": false, "name": "feeRate", "type": "uint256" },
      { "indexed": false, "name": "tokenDec", "type": "uint8" },
      { "indexed": false, "name": "reverseOrder", "type": "bool" },
      { "indexed": false, "name": "settlementInterval", "type": "uint256" },
      { "indexed": false, "name": "expiredSeconds", "type": "uint256" },
      { "indexed": false, "name": "initialReserve", "type": "uint256" },
      { "indexed": false, "name": "priceLookbackSeconds", "type": "uint32" },
      { "indexed": false, "name": "imageUrl", "type": "string" },
      { "indexed": false, "name": "rules", "type": "string" },
      { "indexed": false, "name": "timezone", "type": "string" },
      { "indexed": false, "name": "language", "type": "string" },
      { "indexed": false, "name": "groupUrl", "type": "string" },
      { "indexed": false, "name": "tags", "type": "string[]" },
      { "indexed": false, "name": "predictionToken", "type": "address" },
      { "indexed": false, "name": "anchorToken", "type": "address" },
      { "indexed": false, "name": "currencyUnit", "type": "string" }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "owner",
    "inputs": [],
    "outputs": [{ "type": "address" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "marketImplementation",
    "inputs": [],
    "outputs": [{ "type": "address" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "isWhitelistedCreator",
    "inputs": [{ "name": "account", "type": "address" }],
    "outputs": [{ "type": "bool" }]
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "setCreatorWhitelist",
    "inputs": [
      { "name": "account", "type": "address" },
      { "name": "allowed", "type": "bool" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "setCreatorWhitelistBatch",
    "inputs": [
      { "name": "accounts", "type": "address[]" },
      { "name": "allowed", "type": "bool" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "createMarket",
    "inputs": [
      {
        "name": "_config",
        "type": "tuple",
        "components": [
          { "name": "marketName", "type": "string" },
          { "name": "uniswapV3Pool", "type": "address" },
          { "name": "liquidityToken", "type": "address" },
          { "name": "tokenDec", "type": "uint8" },
          { "name": "reverseOrder", "type": "bool" },
          { "name": "settlementInterval", "type": "uint256" },
          { "name": "expiredSeconds", "type": "uint256" },
          { "name": "initialReserve", "type": "uint256" },
          { "name": "priceLookbackSeconds", "type": "uint32" },
          { "name": "feeRecipient", "type": "address" },
          { "name": "feeRate", "type": "uint256" },
          { "name": "imageUrl", "type": "string" },
          { "name": "rules", "type": "string" },
          { "name": "timezone", "type": "string" },
          { "name": "language", "type": "string" },
          { "name": "groupUrl", "type": "string" },
          { "name": "tags", "type": "string[]" },
          { "name": "predictionToken", "type": "address" },
          { "name": "anchorToken", "type": "address" },
          { "name": "currencyUnit", "type": "string" }
        ]
      }
    ],
    "outputs": [{ "type": "address" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getMarkets",
    "inputs": [],
    "outputs": [{ "type": "address[]" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "marketCount",
    "inputs": [],
    "outputs": [{ "type": "uint256" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getMarketRecord",
    "inputs": [{ "name": "index", "type": "uint256" }],
    "outputs": [
      {
        "type": "tuple",
        "components": [
          { "name": "market", "type": "address" },
          { "name": "creator", "type": "address" },
          { "name": "marketName", "type": "string" },
          { "name": "uniswapV3Pool", "type": "address" },
          { "name": "liquidityToken", "type": "address" },
          { "name": "feeRecipient", "type": "address" },
          { "name": "feeRate", "type": "uint256" },
          { "name": "createdAt", "type": "uint256" },
          { "name": "tokenDec", "type": "uint8" },
          { "name": "reverseOrder", "type": "bool" },
          { "name": "settlementInterval", "type": "uint256" },
          { "name": "expiredSeconds", "type": "uint256" },
          { "name": "initialReserve", "type": "uint256" },
          { "name": "priceLookbackSeconds", "type": "uint32" },
          { "name": "imageUrl", "type": "string" },
          { "name": "rules", "type": "string" },
          { "name": "timezone", "type": "string" },
          { "name": "language", "type": "string" },
          { "name": "groupUrl", "type": "string" },
          { "name": "tags", "type": "string[]" },
          { "name": "predictionToken", "type": "address" },
          { "name": "anchorToken", "type": "address" },
          { "name": "currencyUnit", "type": "string" }
        ]
      }
    ]
  }
]
```

### 8.2 Market contract `GouGouBiMarketConfigurable` ABI fragments

```json
[
  {
    "type": "event",
    "name": "StartRound",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "x", "type": "uint256" },
      { "indexed": false, "name": "y", "type": "uint256" },
      { "indexed": false, "name": "startTime", "type": "uint256" },
      { "indexed": false, "name": "endTime", "type": "uint256" },
      { "indexed": false, "name": "expiredTime", "type": "uint256" },
      { "indexed": false, "name": "startAveragePrice", "type": "uint256" },
      { "indexed": false, "name": "endAveragePrice", "type": "uint256" },
      { "indexed": false, "name": "yesToken", "type": "address" },
      { "indexed": false, "name": "noToken", "type": "address" }
    ]
  },
  {
    "type": "event",
    "name": "AutoResolve",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "winning", "type": "uint8" },
      { "indexed": false, "name": "poolAmount", "type": "uint256" },
      { "indexed": false, "name": "x", "type": "uint256" },
      { "indexed": false, "name": "y", "type": "uint256" },
      { "indexed": false, "name": "startTime", "type": "uint256" },
      { "indexed": false, "name": "endTime", "type": "uint256" },
      { "indexed": false, "name": "endAveragePrice", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "BuyYes",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "tokenIn", "type": "uint256" },
      { "indexed": false, "name": "yesOut", "type": "uint256" },
      { "indexed": false, "name": "newX", "type": "uint256" },
      { "indexed": false, "name": "newY", "type": "uint256" },
      { "indexed": false, "name": "poolAmount", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "BuyNo",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "tokenIn", "type": "uint256" },
      { "indexed": false, "name": "noOut", "type": "uint256" },
      { "indexed": false, "name": "newX", "type": "uint256" },
      { "indexed": false, "name": "newY", "type": "uint256" },
      { "indexed": false, "name": "poolAmount", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "Redeem",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "winning", "type": "uint8" },
      { "indexed": false, "name": "tokensYes", "type": "uint256" },
      { "indexed": false, "name": "tokensNo", "type": "uint256" },
      { "indexed": false, "name": "tokensReceived", "type": "uint256" },
      { "indexed": false, "name": "poolAmount", "type": "uint256" },
      { "indexed": false, "name": "timestamp", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "SwapYesForNo",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "yesIn", "type": "uint256" },
      { "indexed": false, "name": "noOut", "type": "uint256" },
      { "indexed": false, "name": "newX", "type": "uint256" },
      { "indexed": false, "name": "newY", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "SwapNoForYes",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "noIn", "type": "uint256" },
      { "indexed": false, "name": "yesOut", "type": "uint256" },
      { "indexed": false, "name": "newX", "type": "uint256" },
      { "indexed": false, "name": "newY", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "FeeCollected",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "feeAmount", "type": "uint256" },
      { "indexed": false, "name": "feeRecipient", "type": "address" }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "config",
    "inputs": [],
    "outputs": [
      {
        "type": "tuple",
        "components": [
          { "name": "marketName", "type": "string" },
          { "name": "uniswapV3Pool", "type": "address" },
          { "name": "liquidityToken", "type": "address" },
          { "name": "tokenDec", "type": "uint8" },
          { "name": "reverseOrder", "type": "bool" },
          { "name": "settlementInterval", "type": "uint256" },
          { "name": "expiredSeconds", "type": "uint256" },
          { "name": "initialReserve", "type": "uint256" },
          { "name": "priceLookbackSeconds", "type": "uint32" },
          { "name": "feeRecipient", "type": "address" },
          { "name": "feeRate", "type": "uint256" },
          { "name": "imageUrl", "type": "string" },
          { "name": "rules", "type": "string" },
          { "name": "timezone", "type": "string" },
          { "name": "language", "type": "string" },
          { "name": "groupUrl", "type": "string" },
          { "name": "tags", "type": "string[]" },
          { "name": "predictionToken", "type": "address" },
          { "name": "anchorToken", "type": "address" },
          { "name": "currencyUnit", "type": "string" }
        ]
      }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "currentRound",
    "inputs": [],
    "outputs": [{ "type": "uint256" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getRoundInfo",
    "inputs": [{ "name": "round", "type": "uint256" }],
    "outputs": [
      {
        "type": "tuple",
        "components": [
          { "name": "winning", "type": "uint8" },
          { "name": "poolAmount", "type": "uint256" },
          { "name": "x", "type": "uint256" },
          { "name": "y", "type": "uint256" },
          { "name": "yesToken", "type": "address" },
          { "name": "noToken", "type": "address" },
          { "name": "startTime", "type": "uint256" },
          { "name": "endTime", "type": "uint256" },
          { "name": "expiredTime", "type": "uint256" },
          { "name": "startAveragePrice", "type": "uint256" },
          { "name": "endAveragePrice", "type": "uint256" }
        ]
      }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getPoolInfo",
    "inputs": [],
    "outputs": [
      { "name": "_x", "type": "uint256" },
      { "name": "_y", "type": "uint256" },
      { "name": "_poolAmount", "type": "uint256" },
      { "name": "_priceYes", "type": "uint256" },
      { "name": "_priceNo", "type": "uint256" },
      { "name": "_currentRound", "type": "uint256" },
      { "name": "_winning", "type": "uint8" }
    ]
  },
  {
    "type": "function",
    "stateMutability": "payable",
    "name": "buyYes",
    "inputs": [
      { "name": "tokenIn", "type": "uint256" },
      { "name": "minYesOut", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "payable",
    "name": "buyNo",
    "inputs": [
      { "name": "tokenIn", "type": "uint256" },
      { "name": "minNoOut", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "swapYesForNo",
    "inputs": [
      { "name": "amountIn", "type": "uint256" },
      { "name": "minAmountOut", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "swapNoForYes",
    "inputs": [
      { "name": "amountIn", "type": "uint256" },
      { "name": "minAmountOut", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "redeem",
    "inputs": [{ "name": "round", "type": "uint256" }],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "resolve",
    "inputs": [],
    "outputs": []
  }
]
```

The ABI fragments above can be combined with the TypeScript examples in section 6, for example:

```ts
import { ethers } from "ethers";
import { factoryFragment, marketFragment } from "./fragments"; // export the JSON fragments above as constants

const factory = new ethers.Contract(FACTORY_ADDRESS, factoryFragment, signerOrProvider);
const market = new ethers.Contract(marketAddress, marketFragment, signerOrProvider);
```

---
name: market-configurable-skills
display_name: GouGouBi 可配置价格预测市场 Skill
description: >
  基于 contracts/contracts/GouGouBiMarketConfigurable.sol 与 GouGouBiMarketConfigurableFactory.sol 的加密价格预测市场合约调用说明与最佳实践，包含工厂创建参数、市场配置字段、核心交易/结算方法以及在脚本、前端或 OpenClow 工作流中通过 ethers/web3 调用该合约的规范。当需要创建新预测市场、进行 YES/NO 买入、头寸互换或结算赎回时使用本 skill。
author: frank
version: 0.1.0
language: zh-CN
tags:
  - prediction-market
  - evm
  - contract-call
---

# 可配置加密价格预测市场 Skill

## 1. 协议与合约概览

- **市场合约**：`contracts/contracts/GouGouBiMarketConfigurable.sol`
- **工厂合约**：`contracts/contracts/GouGouBiMarketConfigurableFactory.sol`
- **模式**：Polymarket 风格 CPMM YES/NO 预测市场，每一轮（Round）都有独立的 YES/NO 结果代币，通过常数乘积做市。
- **特点**：
  - 使用 Uniswap V3 池的价格作为预言机，按时间区间计算平均价格。
  - 可配置是否预测 `token0/token1` 还是反向（`reverseOrder`）。
  - 支持原生币或任意 ERC20 作为流动性代币。
  - 自动按周期开启新一轮市场，支持结算过期、价格异常处理（通过事件体现）。

> 本 skill 只描述 **合约 API 与调用模式**，具体部署网络与地址由业务方在上层配置（例如在 dApp 配置文件或 OpenClow workflow 的参数中传入）。

---

## 2. 工厂合约 GouGouBiMarketConfigurableFactory

### 2.1 核心角色与状态

- `owner`：工厂管理员，可管理创建白名单。
- `marketImplementation`：被克隆的逻辑合约实现（`GouGouBiMarketConfigurable`）。
- `isWhitelistedCreator[address]`：是否允许该地址调用 `createMarket`。
- `markets[]`：所有已创建市场地址列表。
- `marketIndex[market]`：市场地址对应的索引（从 1 开始，0 表示不是本工厂创建）。
- `marketRecords[index]`：创建记录（见下）。

### 2.2 MarketRecord 结构（只读）

对应工厂中每个已创建市场：

- `market`：市场合约地址
- `creator`：创建者地址
- `marketName`：市场名称
- `uniswapV3Pool`：Uniswap V3 池地址
- `liquidityToken`：流动性代币地址，`address(0)` 表示原生币
- `feeRecipient`：手续费接收地址
- `feeRate`：手续费率（分母 10000）
- `createdAt`：创建时间戳
- 以下字段与 `GouGouBiMarketConfigurable.MarketConfig` 对齐（见第 3 节）：
  - `tokenDec`
  - `reverseOrder`
  - `settlementInterval`
  - `expiredSeconds`
  - `initialReserve`
  - `priceLookbackSeconds`
  - `imageUrl`
  - `rules`
  - `timezone`
  - `language`
  - `groupUrl`
  - `tags`
  - `predictionToken`
  - `anchorToken`
  - `currencyUnit`

### 2.3 管理白名单

```solidity
function setCreatorWhitelist(address account, bool allowed) external onlyOwner
function setCreatorWhitelistBatch(address[] calldata accounts, bool allowed) external onlyOwner
```

- 只有工厂 `owner` 可调用。
- 需保证 `account != address(0)`。

### 2.4 创建市场 createMarket

```solidity
function createMarket(GouGouBiMarketConfigurable.MarketConfig memory _config)
    external
    returns (address market)
```

约束：

- 仅 `owner` 或 `isWhitelistedCreator[msg.sender] == true` 的地址可创建：
  - `require(msg.sender == owner || isWhitelistedCreator[msg.sender], "NOT_WHITELISTED");`
- 内部流程：
  1. 使用 `Clones.clone(marketImplementation)` 创建最小代理。
  2. 调用新市场的 `initialize(_config, msg.sender)`，设置配置与 owner。
  3. 将市场地址加入 `markets[]`，填充 `marketRecords`，更新 `marketIndex`。
  4. 触发 `MarketCreated` 事件，记录关键配置信息。

读接口：

```solidity
function getMarkets() external view returns (address[] memory)
function marketCount() external view returns (uint256)
function getMarketRecord(uint256 index) external view returns (MarketRecord memory)
function getMarketRecordsPaginated(uint256 offset, uint256 limit) external view returns (MarketRecord[] memory)
```

---

## 3. 市场配置 MarketConfig（创建时传入）

工厂 `createMarket` 的 `_config` 与市场合约中的 `MarketConfig` 完全一致：

```solidity
struct MarketConfig {
    string marketName;
    address uniswapV3Pool;
    address liquidityToken;    // address(0) 表示原生币
    uint8 tokenDec;            // 若 liquidityToken==0，则在 initialize 中自动设为 18
    bool reverseOrder;         // 价格方向：false=Token0/Token1, true=Token1/Token0
    uint256 settlementInterval; // 结算周期秒数
    uint256 expiredSeconds;     // 超时未裁决则作废
    uint256 initialReserve;     // 每轮初始虚拟储备（会乘以 10^decimals）
    uint32 priceLookbackSeconds;// 取价回溯时间，用于平均价
    address feeRecipient;       // 手续费接收地址
    uint256 feeRate;            // 手续费分子，分母 10000
    string imageUrl;
    string rules;
    string timezone;
    string language;
    string groupUrl;
    string[] tags;
    address predictionToken;    // 被预测价格的代币
    address anchorToken;        // 计价/锚定代币，如 USDT、BNB
    string currencyUnit;        // 展示用单位，如 "USD"、"BNB"、"DOGE"
}
```

关键约束（在 `initialize` 中校验）：

- `marketName` 非空：`bytes(_config.marketName).length > 0`
- `uniswapV3Pool != address(0)`
- `settlementInterval > 0`
- `expiredSeconds > 0`
- `0 < initialReserve <= 1_000_000_000`
- `feeRate <= FEE_DENOMINATOR (10000)`
- 若 `feeRate > 0`，`feeRecipient != address(0)`，否则会默认设置为 `_owner`。
- 若 `liquidityToken == address(0)`：`tokenDec` 自动设为 18。
- 若 `liquidityToken != address(0)`：`tokenDec = IERC20(liquidityToken).decimals()`，要求 `tokenDec <= 18`。
- 若 `priceLookbackSeconds == 0`：自动设为 300 秒。

初始化完成后，合约立即调用 `_startNewRound()` 开启第 1 轮。

---

## 4. 市场轮次 RoundInfo 与价格结算

### 4.1 RoundInfo 结构

```solidity
struct RoundInfo {
    uint8 winning;              // 0=未结算, 1=YES 赢, 2=NO 赢, 3=平局/异常
    uint256 poolAmount;         // 池中当前累计的流动性代币数量
    uint256 x;                  // CPMM x 储备（YES 池）
    uint256 y;                  // CPMM y 储备（NO 池）
    address yesToken;           // 本轮 YES OutcomeToken
    address noToken;            // 本轮 NO OutcomeToken
    uint256 startTime;          // 本轮开始时间
    uint256 endTime;            // 预定结算时间
    uint256 expiredTime;        // 过期时间（超时自动视为 winning=3）
    uint256 startAveragePrice;  // 轮次开始时平均价格
    uint256 endAveragePrice;    // 轮次结束/结算时平均价格
}
```

- 通过 `rounds[round]` 只读映射访问。
- 当前轮次索引：`currentRound`。

### 4.2 价格获取：getAveragePriceFromUniswapV3

```solidity
function getAveragePriceFromUniswapV3(uint32 startTime, uint32 endTime)
    public
    view
    returns (uint256 averagePrice)
```

- `startTime > endTime`，且 `endTime <= block.timestamp`。
- 内部使用 Uniswap V3 `observe` + `TickMath` 计算对应区间的平均价格，并用 `1e18` 精度表示。
- 若 `reverseOrder == true`，会对价格取倒数（同样保持 1e18 精度）。

### 4.3 结算与轮次切换

- `_checkAndExecuteSettlement()`：在每次交易/赎回/resolve 前调用，用于：
  - 若 `block.timestamp > expiredTime`：将本轮 `winning = 3`，`endAveragePrice = 0`，触发 `AutoResolve` 事件，并开启新一轮。
  - 若当前轮已到达 `endTime` 且未过期：调用 `_calculateSettlementByPrice()`。
- `_calculateSettlementByPrice()`：
  - 通过 `getAveragePriceFromUniswapV3(priceLookbackSeconds, 0)` 获取结算时平均价。
  - 与 `startAveragePrice` 比较：
    - 相等 → `winning = 3`（平局/特殊情况）
    - 结算价 > 起始价 → `winning = 1`（YES 赢）
    - 结算价 < 起始价 → `winning = 2`（NO 赢）
  - 更新 `endTime`、`endAveragePrice`，触发 `AutoResolve`，然后开启新一轮。

外部可主动触发检查：

```solidity
function resolve() external nonReentrant {
    _checkAndExecuteSettlement();
}
```

---

## 5. 用户交互核心方法

### 5.1 买入 YES / NO

#### 5.1.1 buyYes

```solidity
function buyYes(uint256 tokenIn, uint256 minYesOut) external payable nonReentrant
```

语义：

- 对当前轮 `currentRound`：
  - 若市场为原生币（`liquidityToken == address(0)`）：
    - 忽略 `tokenIn` 参数，使用 `msg.value` 作为投入金额，要求 `msg.value > 0`。
  - 若为 ERC20：
    - 要求 `tokenIn > 0 && msg.value == 0`。
    - 需提前 `IERC20(liquidityToken).approve(market, tokenIn)`，合约内部使用 `safeTransferFrom`。
- 合约逻辑：
  - 将 `tokenIn` 记入 `rounds[currentRound].poolAmount`。
  - 铸造等量 YES/NO 虚拟头寸（`mintedYes = mintedNo = tokenIn`），通过常数乘积公式计算价格滑点，得到额外的 swapped 数量。
  - 最终得到的 YES 数量 `totalYesOut = mintedYes + swappedYes`，必须 `>= minYesOut`，否则交易回滚（滑点保护）。
  - 使用 `OutcomeToken(yesToken).mint(msg.sender, totalYesOut)` 发放 YES 代币。

#### 5.1.2 buyNo

```solidity
function buyNo(uint256 tokenIn, uint256 minNoOut) external payable nonReentrant
```

- 与 `buyYes` 对称，只是对 NO 池进行操作，最终得到 `totalNoOut`，需要满足 `>= minNoOut`。

### 5.2 头寸互换：swapYesForNo / swapNoForYes

```solidity
function swapYesForNo(uint256 amountIn, uint256 minAmountOut) external nonReentrant
function swapNoForYes(uint256 amountIn, uint256 minAmountOut) external nonReentrant
```

通用逻辑要点：

- 仅当本轮 `winning == 0`（未结算）时允许互换。
- 需先持有对应的 YES 或 NO 代币余额。
- 根据当前池子 `x`、`y` 以及输入数量 `amountIn` 计算 `amountOut`，并进行滑点检查：
  - `swapYesForNo`：`amountOut = (y * amountIn) / (x + amountIn)`
  - `swapNoForYes`：`amountOut = (x * amountIn) / (y + amountIn)`
- 使用 `burn` 销毁输入代币，`mint` 发放输出代币，并更新 `x`、`y`。

### 5.3 赎回结算：redeem

```solidity
function redeem(uint256 round) external nonReentrant
```

约束与流程：

- 先调用 `_checkAndExecuteSettlement()`，可能会改变当前轮状态。
- 要求：
  - `round > 0 && round <= currentRound`
  - `rounds[round].winning != 0`（本轮已结算：YES 赢、NO 赢或平局）
  - `rounds[round].poolAmount > 0`
  - 调用者在该轮 YES/NO 中至少持有一种代币。
- 分配逻辑：
  - 若 `winning == 1`（YES 赢）：
    - 按 YES 代币在总 YES 供应中的占比分配池中金额。
  - 若 `winning == 2`（NO 赢）：
    - 按 NO 代币在总 NO 供应中的占比分配。
  - 若 `winning == 3`（平局/异常）：
    - 先将调用者持有的 YES/NO 数量相加，按其在总供应量中的占比分配池中金额。
  - 所有分配都会从池中扣除 `tokenOut`，并按 `feeRate` 抽取手续费：
    - `fee = tokenOut * feeRate / FEE_DENOMINATOR`
    - 用户实收 `userAmount = tokenOut - fee`
    - 手续费转给 `config.feeRecipient`
  - 支持原生币或 ERC20 方式转账。

### 5.4 价格查询与池信息

```solidity
function priceYes() external view returns (uint256 num, uint256 den)
function priceNo() external view returns (uint256 num, uint256 den)
function getPoolInfo() external view returns (
    uint256 _x, uint256 _y, uint256 _poolAmount,
    uint256 _priceYes, uint256 _priceNo,
    uint256 _currentRound, uint8 _winning
)
function getRoundInfo(uint256 round) external view returns (
    uint8 _winning, uint256 _poolAmount, uint256 _x, uint256 _y,
    address _yesToken, address _noToken,
    uint256 _startTime, uint256 _endTime, uint256 _expiredTime,
    uint256 _startAveragePrice, uint256 _endAveragePrice
)
```

- `priceYes/priceNo` 返回分数形式的价格（`num/den`），用于前端展示或估算。
- `getPoolInfo` 一次性获取当前轮的池子与价格信息。
- `getRoundInfo` 可查询任意轮的详细数据，包括 YES/NO 代币地址与时间信息。

---

## 6. 在脚本 / 前端中调用示例（ethers.js）

> 示例仅展示调用模式，实际 `FACTORY_ADDRESS` 与市场地址由部署环境决定，请在项目配置中传入。

```ts
import { ethers } from "ethers";
import MarketAbi from "../artifacts/contracts/GouGouBiMarketConfigurable.sol/GouGouBiMarketConfigurable.json";
import FactoryAbi from "../artifacts/contracts/GouGouBiMarketConfigurableFactory.sol/GouGouBiMarketConfigurableFactory.json";

// 由业务方配置
const FACTORY_ADDRESS = "<REPLACE_WITH_FACTORY_ADDRESS>";

export function getFactory(providerOrSigner: ethers.Signer | ethers.providers.Provider) {
  return new ethers.Contract(FACTORY_ADDRESS, FactoryAbi.abi, providerOrSigner);
}

export function getMarket(
  marketAddress: string,
  providerOrSigner: ethers.Signer | ethers.providers.Provider
) {
  return new ethers.Contract(marketAddress, MarketAbi.abi, providerOrSigner);
}

// 创建新市场（需要工厂 owner 或白名单地址）
export async function createMarket(
  signer: ethers.Signer,
  config: {
    marketName: string;
    uniswapV3Pool: string;
    liquidityToken: string;   // 原生币市场可传 ethers.constants.AddressZero
    reverseOrder: boolean;
    settlementInterval: number;
    expiredSeconds: number;
    initialReserve: ethers.BigNumberish;
    priceLookbackSeconds?: number;
    feeRecipient?: string;
    feeRate: number;
    imageUrl?: string;
    rules?: string;
    timezone?: string;
    language?: string;
    groupUrl?: string;
    tags?: string[];
    predictionToken: string;
    anchorToken: string;
    currencyUnit: string;
  }
) {
  const factory = getFactory(signer);
  const _config = {
    ...config,
    // 让合约自动推断 tokenDec / priceLookbackSeconds / feeRecipient 等默认值
    tokenDec: 0,
    priceLookbackSeconds: config.priceLookbackSeconds ?? 0,
    feeRecipient: config.feeRecipient ?? ethers.constants.AddressZero,
    tags: config.tags ?? [],
  };
  const tx = await factory.createMarket(_config);
  const receipt = await tx.wait();
  // 可以从 MarketCreated 事件中解析新市场地址
  return receipt;
}

// 在当前轮买入 YES（ERC20 市场为例）
export async function buyYes(
  signer: ethers.Signer,
  marketAddress: string,
  amountIn: ethers.BigNumberish,
  minYesOut: ethers.BigNumberish
) {
  const market = getMarket(marketAddress, signer);
  const tx = await market.buyYes(amountIn, minYesOut);
  return tx.wait();
}

// 在当前轮买入 NO（原生币市场为例）
export async function buyNoNative(
  signer: ethers.Signer,
  marketAddress: string,
  amountWei: ethers.BigNumberish,
  minNoOut: ethers.BigNumberish
) {
  const market = getMarket(marketAddress, signer);
  const tx = await market.buyNo(0, minNoOut, { value: amountWei });
  return tx.wait();
}

// 赎回某一轮的结算结果
export async function redeem(
  signer: ethers.Signer,
  marketAddress: string,
  round: number
) {
  const market = getMarket(marketAddress, signer);
  const tx = await market.redeem(round);
  return tx.wait();
}
```

在前端或自动化脚本中集成时建议：

- **读操作**（`getPoolInfo`、`getRoundInfo`、`priceYes`、`priceNo` 等）使用只读 `provider`。
- **写操作**（`createMarket`、`buyYes`、`buyNo`、`swapYesForNo`、`swapNoForYes`、`redeem`、`resolve`）必须使用具有签名能力的 `signer`。
- ERC20 市场在 `buyYes` / `buyNo` 前要先对市场合约执行一次 `approve`，原生币市场则通过 `value` 附带资金。
- 前端应对 `minYesOut` / `minNoOut` 做合理设置以防滑点过大（例如按预期输出的 95%~99% 设定）。

---

## 7. 与其他 skill 的关系

- 本 `market-configurable-skills` 专注于 **GouGouBi 可配置价格预测市场的具体实现与调用方式**，包括工厂创建、市场配置字段、交易与结算逻辑。
- 若在同一产品中同时使用红包协议或其他合约，可结合对应 skill（如 `giveaway-skills` / `giveaway-protocol`）一起阅读，但它们之间没有直接合约依赖关系，仅在产品层面协同使用。

---

## 8. ABI 信息与精简示例

> 完整 ABI 推荐直接使用编译产物（例如 `artifacts/contracts/GouGouBiMarketConfigurable.sol/GouGouBiMarketConfigurable.json` 和 `...Factory.sol/GouGouBiMarketConfigurableFactory.json` 中的 `abi` 字段）。本节只提供**常用事件与函数的精简片段**，用于快速调试或在无法访问编译产物时临时构造合约实例。

### 8.1 工厂合约 GouGouBiMarketConfigurableFactory ABI 片段

```json
[
  {
    "type": "event",
    "name": "CreatorWhitelistUpdated",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "account", "type": "address" },
      { "indexed": false, "name": "allowed", "type": "bool" }
    ]
  },
  {
    "type": "event",
    "name": "MarketCreated",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "market", "type": "address" },
      { "indexed": false, "name": "marketName", "type": "string" },
      { "indexed": true, "name": "uniswapV3Pool", "type": "address" },
      { "indexed": true, "name": "creator", "type": "address" },
      { "indexed": false, "name": "liquidityToken", "type": "address" },
      { "indexed": false, "name": "createdAt", "type": "uint256" },
      { "indexed": false, "name": "feeRecipient", "type": "address" },
      { "indexed": false, "name": "feeRate", "type": "uint256" },
      { "indexed": false, "name": "tokenDec", "type": "uint8" },
      { "indexed": false, "name": "reverseOrder", "type": "bool" },
      { "indexed": false, "name": "settlementInterval", "type": "uint256" },
      { "indexed": false, "name": "expiredSeconds", "type": "uint256" },
      { "indexed": false, "name": "initialReserve", "type": "uint256" },
      { "indexed": false, "name": "priceLookbackSeconds", "type": "uint32" },
      { "indexed": false, "name": "imageUrl", "type": "string" },
      { "indexed": false, "name": "rules", "type": "string" },
      { "indexed": false, "name": "timezone", "type": "string" },
      { "indexed": false, "name": "language", "type": "string" },
      { "indexed": false, "name": "groupUrl", "type": "string" },
      { "indexed": false, "name": "tags", "type": "string[]" },
      { "indexed": false, "name": "predictionToken", "type": "address" },
      { "indexed": false, "name": "anchorToken", "type": "address" },
      { "indexed": false, "name": "currencyUnit", "type": "string" }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "owner",
    "inputs": [],
    "outputs": [{ "type": "address" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "marketImplementation",
    "inputs": [],
    "outputs": [{ "type": "address" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "isWhitelistedCreator",
    "inputs": [{ "name": "account", "type": "address" }],
    "outputs": [{ "type": "bool" }]
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "setCreatorWhitelist",
    "inputs": [
      { "name": "account", "type": "address" },
      { "name": "allowed", "type": "bool" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "setCreatorWhitelistBatch",
    "inputs": [
      { "name": "accounts", "type": "address[]" },
      { "name": "allowed", "type": "bool" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "createMarket",
    "inputs": [
      {
        "name": "_config",
        "type": "tuple",
        "components": [
          { "name": "marketName", "type": "string" },
          { "name": "uniswapV3Pool", "type": "address" },
          { "name": "liquidityToken", "type": "address" },
          { "name": "tokenDec", "type": "uint8" },
          { "name": "reverseOrder", "type": "bool" },
          { "name": "settlementInterval", "type": "uint256" },
          { "name": "expiredSeconds", "type": "uint256" },
          { "name": "initialReserve", "type": "uint256" },
          { "name": "priceLookbackSeconds", "type": "uint32" },
          { "name": "feeRecipient", "type": "address" },
          { "name": "feeRate", "type": "uint256" },
          { "name": "imageUrl", "type": "string" },
          { "name": "rules", "type": "string" },
          { "name": "timezone", "type": "string" },
          { "name": "language", "type": "string" },
          { "name": "groupUrl", "type": "string" },
          { "name": "tags", "type": "string[]" },
          { "name": "predictionToken", "type": "address" },
          { "name": "anchorToken", "type": "address" },
          { "name": "currencyUnit", "type": "string" }
        ]
      }
    ],
    "outputs": [{ "type": "address" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getMarkets",
    "inputs": [],
    "outputs": [{ "type": "address[]" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "marketCount",
    "inputs": [],
    "outputs": [{ "type": "uint256" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getMarketRecord",
    "inputs": [{ "name": "index", "type": "uint256" }],
    "outputs": [
      {
        "type": "tuple",
        "components": [
          { "name": "market", "type": "address" },
          { "name": "creator", "type": "address" },
          { "name": "marketName", "type": "string" },
          { "name": "uniswapV3Pool", "type": "address" },
          { "name": "liquidityToken", "type": "address" },
          { "name": "feeRecipient", "type": "address" },
          { "name": "feeRate", "type": "uint256" },
          { "name": "createdAt", "type": "uint256" },
          { "name": "tokenDec", "type": "uint8" },
          { "name": "reverseOrder", "type": "bool" },
          { "name": "settlementInterval", "type": "uint256" },
          { "name": "expiredSeconds", "type": "uint256" },
          { "name": "initialReserve", "type": "uint256" },
          { "name": "priceLookbackSeconds", "type": "uint32" },
          { "name": "imageUrl", "type": "string" },
          { "name": "rules", "type": "string" },
          { "name": "timezone", "type": "string" },
          { "name": "language", "type": "string" },
          { "name": "groupUrl", "type": "string" },
          { "name": "tags", "type": "string[]" },
          { "name": "predictionToken", "type": "address" },
          { "name": "anchorToken", "type": "address" },
          { "name": "currencyUnit", "type": "string" }
        ]
      }
    ]
  }
]
```

### 8.2 市场合约 GouGouBiMarketConfigurable ABI 片段

```json
[
  {
    "type": "event",
    "name": "StartRound",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "x", "type": "uint256" },
      { "indexed": false, "name": "y", "type": "uint256" },
      { "indexed": false, "name": "startTime", "type": "uint256" },
      { "indexed": false, "name": "endTime", "type": "uint256" },
      { "indexed": false, "name": "expiredTime", "type": "uint256" },
      { "indexed": false, "name": "startAveragePrice", "type": "uint256" },
      { "indexed": false, "name": "endAveragePrice", "type": "uint256" },
      { "indexed": false, "name": "yesToken", "type": "address" },
      { "indexed": false, "name": "noToken", "type": "address" }
    ]
  },
  {
    "type": "event",
    "name": "AutoResolve",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "winning", "type": "uint8" },
      { "indexed": false, "name": "poolAmount", "type": "uint256" },
      { "indexed": false, "name": "x", "type": "uint256" },
      { "indexed": false, "name": "y", "type": "uint256" },
      { "indexed": false, "name": "startTime", "type": "uint256" },
      { "indexed": false, "name": "endTime", "type": "uint256" },
      { "indexed": false, "name": "endAveragePrice", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "BuyYes",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "tokenIn", "type": "uint256" },
      { "indexed": false, "name": "yesOut", "type": "uint256" },
      { "indexed": false, "name": "newX", "type": "uint256" },
      { "indexed": false, "name": "newY", "type": "uint256" },
      { "indexed": false, "name": "poolAmount", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "BuyNo",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "tokenIn", "type": "uint256" },
      { "indexed": false, "name": "noOut", "type": "uint256" },
      { "indexed": false, "name": "newX", "type": "uint256" },
      { "indexed": false, "name": "newY", "type": "uint256" },
      { "indexed": false, "name": "poolAmount", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "Redeem",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "winning", "type": "uint8" },
      { "indexed": false, "name": "tokensYes", "type": "uint256" },
      { "indexed": false, "name": "tokensNo", "type": "uint256" },
      { "indexed": false, "name": "tokensReceived", "type": "uint256" },
      { "indexed": false, "name": "poolAmount", "type": "uint256" },
      { "indexed": false, "name": "timestamp", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "SwapYesForNo",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "yesIn", "type": "uint256" },
      { "indexed": false, "name": "noOut", "type": "uint256" },
      { "indexed": false, "name": "newX", "type": "uint256" },
      { "indexed": false, "name": "newY", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "SwapNoForYes",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "noIn", "type": "uint256" },
      { "indexed": false, "name": "yesOut", "type": "uint256" },
      { "indexed": false, "name": "newX", "type": "uint256" },
      { "indexed": false, "name": "newY", "type": "uint256" }
    ]
  },
  {
    "type": "event",
    "name": "FeeCollected",
    "anonymous": false,
    "inputs": [
      { "indexed": true, "name": "user", "type": "address" },
      { "indexed": true, "name": "round", "type": "uint256" },
      { "indexed": false, "name": "feeAmount", "type": "uint256" },
      { "indexed": false, "name": "feeRecipient", "type": "address" }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "config",
    "inputs": [],
    "outputs": [
      {
        "type": "tuple",
        "components": [
          { "name": "marketName", "type": "string" },
          { "name": "uniswapV3Pool", "type": "address" },
          { "name": "liquidityToken", "type": "address" },
          { "name": "tokenDec", "type": "uint8" },
          { "name": "reverseOrder", "type": "bool" },
          { "name": "settlementInterval", "type": "uint256" },
          { "name": "expiredSeconds", "type": "uint256" },
          { "name": "initialReserve", "type": "uint256" },
          { "name": "priceLookbackSeconds", "type": "uint32" },
          { "name": "feeRecipient", "type": "address" },
          { "name": "feeRate", "type": "uint256" },
          { "name": "imageUrl", "type": "string" },
          { "name": "rules", "type": "string" },
          { "name": "timezone", "type": "string" },
          { "name": "language", "type": "string" },
          { "name": "groupUrl", "type": "string" },
          { "name": "tags", "type": "string[]" },
          { "name": "predictionToken", "type": "address" },
          { "name": "anchorToken", "type": "address" },
          { "name": "currencyUnit", "type": "string" }
        ]
      }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "currentRound",
    "inputs": [],
    "outputs": [{ "type": "uint256" }]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getRoundInfo",
    "inputs": [{ "name": "round", "type": "uint256" }],
    "outputs": [
      {
        "type": "tuple",
        "components": [
          { "name": "winning", "type": "uint8" },
          { "name": "poolAmount", "type": "uint256" },
          { "name": "x", "type": "uint256" },
          { "name": "y", "type": "uint256" },
          { "name": "yesToken", "type": "address" },
          { "name": "noToken", "type": "address" },
          { "name": "startTime", "type": "uint256" },
          { "name": "endTime", "type": "uint256" },
          { "name": "expiredTime", "type": "uint256" },
          { "name": "startAveragePrice", "type": "uint256" },
          { "name": "endAveragePrice", "type": "uint256" }
        ]
      }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "getPoolInfo",
    "inputs": [],
    "outputs": [
      { "name": "_x", "type": "uint256" },
      { "name": "_y", "type": "uint256" },
      { "name": "_poolAmount", "type": "uint256" },
      { "name": "_priceYes", "type": "uint256" },
      { "name": "_priceNo", "type": "uint256" },
      { "name": "_currentRound", "type": "uint256" },
      { "name": "_winning", "type": "uint8" }
    ]
  },
  {
    "type": "function",
    "stateMutability": "payable",
    "name": "buyYes",
    "inputs": [
      { "name": "tokenIn", "type": "uint256" },
      { "name": "minYesOut", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "payable",
    "name": "buyNo",
    "inputs": [
      { "name": "tokenIn", "type": "uint256" },
      { "name": "minNoOut", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "swapYesForNo",
    "inputs": [
      { "name": "amountIn", "type": "uint256" },
      { "name": "minAmountOut", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "swapNoForYes",
    "inputs": [
      { "name": "amountIn", "type": "uint256" },
      { "name": "minAmountOut", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "redeem",
    "inputs": [{ "name": "round", "type": "uint256" }],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "resolve",
    "inputs": [],
    "outputs": []
  }
]
```

上述 ABI 片段可以与第 6 节中的 TypeScript 示例直接组合使用，例如：

```ts
import { ethers } from "ethers";
import { factoryFragment, marketFragment } from "./fragments"; // 将上面的 JSON 片段拆分成常量

const factory = new ethers.Contract(FACTORY_ADDRESS, factoryFragment, signerOrProvider);
const market = new ethers.Contract(marketAddress, marketFragment, signerOrProvider);
```


