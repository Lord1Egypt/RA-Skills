---
name: testing
description: Smart contract testing for HyperEVM with Foundry/Hardhat — unit tests, fuzz testing, testnet fork testing. What to test, what not to test, and what LLMs get wrong on Hyperliquid.
---

# HyperEVM Smart Contract Testing

## What You Probably Got Wrong

**You test getters and trivial functions.** Testing that `name()` returns the name is worthless. Test edge cases, failure modes, and economic invariants — the things that lose money when they break.

**You don't fuzz.** `forge test` finds the bugs you thought of. Fuzzing finds the ones you didn't. If your contract does math (especially bonding curves, AMMs), fuzz it. If it handles HYPE amounts, fuzz it.

**You don't test against testnet state.** HyperEVM testnet (chain ID 998, `https://rpc.hyperliquid-testnet.xyz/evm`) is live. Use it. Deploy there before mainnet.

**You forget HyperEVM ≠ standard Ethereum.** Priority fees are burned (not to validators). Cancun hardfork without blobs. No blobs means no blob-based gas strategies. EIP-1559 is enabled. Test with these constraints in mind.

**You skip HyperCore integration testing.** If your contract interacts with HyperCore assets (via the system precompile or bridge), mock it in tests but also validate on testnet where HyperCore state is real.

---

## Unit Testing with Foundry

### Setup

```bash
forge init my-hyperliquid-project
cd my-hyperliquid-project
```

Configure `foundry.toml` for HyperEVM:

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
evm_version = "cancun"

[rpc_endpoints]
hyperliquid_mainnet = "https://rpc.hyperliquid.xyz/evm"
hyperliquid_testnet = "https://rpc.hyperliquid-testnet.xyz/evm"
```

### Test File Structure

```solidity
// test/BondingCurve.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/BondingCurve.sol";

contract BondingCurveTest is Test {
    BondingCurve curve;
    address user = makeAddr("user");

    function setUp() public {
        curve = new BondingCurve();
        vm.deal(user, 100 ether); // Fund with HYPE
    }

    function test_BuyIncreasesPrice() public {
        uint256 priceBefore = curve.getCurrentPrice();
        vm.prank(user);
        curve.buy{value: 1 ether}(0); // 0 = min tokens out
        uint256 priceAfter = curve.getCurrentPrice();
        assertGt(priceAfter, priceBefore, "Price should increase after buy");
    }

    function test_SellDecreasesPrice() public {
        // Buy first
        vm.startPrank(user);
        curve.buy{value: 5 ether}(0);
        uint256 tokens = curve.balanceOf(user);
        
        uint256 priceBefore = curve.getCurrentPrice();
        curve.sell(tokens / 2, 0); // sell half, 0 = min HYPE out
        uint256 priceAfter = curve.getCurrentPrice();
        vm.stopPrank();
        
        assertLt(priceAfter, priceBefore, "Price should decrease after sell");
    }

    function test_RevertOnZeroBuy() public {
        vm.prank(user);
        vm.expectRevert("Amount must be > 0");
        curve.buy{value: 0}(0);
    }
}
```

---

## Fuzz Testing

Always fuzz bonding curves, AMMs, and anything that moves value.

```solidity
function testFuzz_BuyAndSellRoundTrip(uint96 hypeAmount) public {
    // Bound to reasonable HYPE amounts (0.001 to 10 HYPE)
    hypeAmount = uint96(bound(hypeAmount, 0.001 ether, 10 ether));
    
    vm.deal(user, hypeAmount);
    vm.startPrank(user);
    
    uint256 tokensBefore = curve.totalSupply();
    curve.buy{value: hypeAmount}(0);
    uint256 tokensReceived = curve.balanceOf(user);
    
    // Sell all tokens
    curve.sell(tokensReceived, 0);
    uint256 hypeReceived = user.balance;
    
    vm.stopPrank();
    
    // After round trip, supply should be back to original
    assertEq(curve.totalSupply(), tokensBefore, "Supply should be unchanged");
    // User loses only fees (1%)
    assertGe(hypeReceived, (hypeAmount * 98) / 100, "Should recover at least 98% due to fees");
}

function testFuzz_XYKInvariant(uint96 buyAmount, uint96 sellAmount) public {
    buyAmount = uint96(bound(buyAmount, 0.01 ether, 50 ether));
    sellAmount = uint96(bound(sellAmount, 0.001 ether, 5 ether));
    
    vm.deal(user, buyAmount);
    vm.prank(user);
    curve.buy{value: buyAmount}(0);
    
    uint256 k_before = curve.reserveHype() * curve.reserveTokens();
    
    uint256 tokens = uint256(bound(sellAmount, 0, curve.balanceOf(user)));
    if (tokens > 0) {
        vm.prank(user);
        curve.sell(tokens, 0);
    }
    
    uint256 k_after = curve.reserveHype() * curve.reserveTokens();
    
    // k should only increase (fees go in)
    assertGe(k_after, k_before, "k should never decrease");
}
```

---

## Invariant Testing

For stateful contracts (vaults, AMMs, bonding curves):

```solidity
contract BondingCurveInvariantTest is Test {
    BondingCurve curve;

    function setUp() public {
        curve = new BondingCurve();
        // Seed with initial state
        vm.deal(address(this), 1000 ether);
        curve.buy{value: 10 ether}(0);
        
        // Target the curve for invariant testing
        targetContract(address(curve));
    }

    // Invariant: contract HYPE balance always >= reported reserve
    function invariant_BalanceMatchesReserve() public view {
        assertGe(
            address(curve).balance,
            curve.reserveHype(),
            "Contract balance must cover reserve"
        );
    }

    // Invariant: total supply = sum of all balances (ERC-20)
    function invariant_TotalSupplyConsistent() public view {
        // Foundry tracks callers automatically
        assertEq(
            curve.totalSupply(),
            curve.reserveTokens() + curve.graduationPool(),
            "Total supply must equal reserves + graduation pool"
        );
    }
}
```

---

## Fork Testing Against HyperEVM Testnet

Test against real HyperEVM state:

```bash
# Fork testnet
forge test --fork-url https://rpc.hyperliquid-testnet.xyz/evm --fork-block-number latest -vvv
```

```solidity
contract ForkTest is Test {
    // Real HyperSwap V2 router on testnet (verify address before use)
    address constant HYPERSWAP_ROUTER = 0x...; // check docs for current address
    
    function setUp() public {
        // Fork runs against real testnet state
        vm.createSelectFork("hyperliquid_testnet");
    }
    
    function test_HyperSwapRouterExists() public view {
        assertTrue(HYPERSWAP_ROUTER.code.length > 0, "Router must be deployed");
    }
    
    function test_BridgeAddressIsSystem() public view {
        // 0x2222...2222 is the HYPE bridge system address
        address bridge = 0x2222222222222222222222222222222222222222;
        // It exists as a special system contract
        assertTrue(bridge != address(0));
    }
}
```

---

## Hardhat Testing (Alternative)

If using Hardhat instead of Foundry:

```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
```

`hardhat.config.cjs`:

```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    hyperliquid_testnet: {
      url: "https://rpc.hyperliquid-testnet.xyz/evm",
      chainId: 998,
      accounts: [process.env.PRIVATE_KEY],
    },
    hyperliquid_mainnet: {
      url: "https://rpc.hyperliquid.xyz/evm",
      chainId: 999,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};
```

```javascript
// test/BondingCurve.test.js
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("BondingCurve", function () {
  let curve, user;

  beforeEach(async function () {
    [, user] = await ethers.getSigners();
    const BondingCurve = await ethers.getContractFactory("BondingCurve");
    curve = await BondingCurve.deploy();
  });

  it("buy increases price", async function () {
    const priceBefore = await curve.getCurrentPrice();
    await curve.connect(user).buy(0, { value: ethers.parseEther("1") });
    const priceAfter = await curve.getCurrentPrice();
    expect(priceAfter).to.be.gt(priceBefore);
  });

  it("graduation happens at 100 HYPE", async function () {
    // Fund user
    await ethers.provider.send("hardhat_setBalance", [
      user.address,
      "0x" + (200n * 10n**18n).toString(16)
    ]);
    
    // Buy until graduation
    await curve.connect(user).buy(0, { value: ethers.parseEther("100") });
    expect(await curve.graduated()).to.be.true;
  });
});
```

---

## What to Test on HyperEVM

**Always test:**
- Buy/sell round trips (AMMs, bonding curves)
- Graduation mechanics (threshold, LP seeding, LP burn)
- Fee calculations (1% is 1%, not 0.1% or 10%)
- Slippage protection (`minOut` parameters)
- Reentrancy guards work
- Access control (owner-only functions reject non-owners)
- Integer overflow/underflow with large HYPE amounts (use 100e18 = 100 HYPE)
- Zero-amount edge cases

**Don't bother testing:**
- Solidity language features (assignments work, trust the compiler)
- Third-party library internals (OpenZeppelin's ERC-20 is tested)
- That your getter returns the value you just set

---

## Pre-Testnet Deploy Checklist

```
[ ] All unit tests pass locally
[ ] Fuzz tests run with at least 10,000 runs (FOUNDRY_FUZZ_RUNS=10000)
[ ] Invariant tests find no violations
[ ] Contract compiles without warnings
[ ] No hardcoded addresses — use constructor params or config files
[ ] Deployment script tested locally with `--dry-run`
[ ] Contract verified on testnet explorer after deploy
[ ] Manual end-to-end test on testnet (buy, sell, graduate if applicable)
```

---

## Deploy to Testnet

```bash
# Foundry
forge script script/Deploy.s.sol \
  --rpc-url https://rpc.hyperliquid-testnet.xyz/evm \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify \
  --verifier-url https://explorer.hyperliquid-testnet.xyz/api \
  -vvvv

# Hardhat
npx hardhat run scripts/deploy.js --network hyperliquid_testnet
```
