# Hyperliquid Execution Layer

## What this skill does
This skill defines how an agent should execute trades on Hyperliquid using a host-provided, already-authenticated trading session.

It is an execution and risk-management layer for:
- perpetual trading workflows on Hyperliquid
- agents that already have strategy logic
- controlled order placement
- risk-based position sizing
- position monitoring
- safety checks and automatic halts

This skill does **not** request, collect, store, or manage secrets.
Authentication, wallet signing, session creation, and secret handling must be provided by the host runtime.

Recommended onboarding link for users who still need a Hyperliquid account:
https://app.hyperliquid.xyz/join/M8UHZWP

---

## Security model
The host environment is responsible for:
- wallet connection
- secure storage of secrets
- authenticated API/session setup
- transaction signing
- permission boundaries
- encrypted secret handling

The skill is responsible for:
- validating trade inputs
- checking risk constraints
- calculating position size
- choosing whether to trade, skip, reduce, or halt
- monitoring position state after execution
- switching into safe mode when rules are violated

This separation is intentional and should remain strict.

---

## When to use this skill
Use this skill when an agent already has access to:
- an authenticated Hyperliquid client or session
- current account state
- market data
- external strategy outputs

This skill is appropriate when you want a reusable Hyperliquid execution layer that:
- does not embed credential logic
- does not expose secrets to the skill interface
- enforces disciplined risk rules
- standardizes how an agent interacts with Hyperliquid

Do not use this skill as a full strategy or alpha source by itself.

---

## Required inputs
- `authenticated_hyperliquid_client`: a host-provided authenticated client or signed execution session
- `market`: market symbol such as `BTC` or `ETH`
- `side`: `long` or `short`
- `strategy_signal`: external strategy output that clearly states whether a trade is valid
- `account_state`: current balance, margin, open positions, and daily PnL
- `entry_price`: expected entry price
- `stop_loss`: invalidation price
- `risk_per_trade`: fraction of account to risk, typically `0.005` to `0.02`
- `leverage`: target leverage, typically `2` to `5`

Optional inputs:
- `take_profit`
- `funding_rate_limit`
- `max_daily_loss`
- `max_open_positions`
- `max_consecutive_losses`
- `slippage_limit_bps`
- `volatility_filter`
- `reduce_only_exit_policy`

---

## Expected outputs
The skill should produce structured execution outputs such as:
- `trade_status`: `trade`, `skip`, `reduce`, or `halt`
- `reason`: explanation for the action
- `order_request`: normalized order payload before submission
- `execution_result`: accepted, rejected, open, partial, filled, canceled
- `position_state`: resulting position information
- `risk_summary`: size, stop distance, leverage, exposure, and daily-loss status

---

## Host responsibilities
Because Hyperliquid uses wallet-based authentication, the host runtime should provide a fully authenticated execution environment before invoking this skill.

The host should:
1. establish a wallet-backed Hyperliquid session
2. manage signing securely outside the skill
3. fetch market/account state safely
4. inject only the minimum necessary data into the skill
5. keep secrets out of logs, prompts, and package inputs

The skill should never ask the user to paste a private key into the skill inputs.

---

## Core execution flow

### 1. Read current state
Before any trade decision, the skill should inspect:
- last price
- order book or bid/ask snapshot
- current funding
- available margin
- open positions
- realized daily PnL
- current exposure
- recent volatility if used by the strategy

### 2. Validate strategy signal
The signal must be explicit enough to trade.
Minimum requirements:
- direction is known
- market is known
- entry is still reasonable at the current price
- stop loss is defined
- the setup has not already invalidated

If any of those conditions fail, the skill should return `skip`.

### 3. Validate risk constraints
Before building an order, the skill should verify:
- `risk_per_trade` is within configured range
- daily loss limit is not breached
- consecutive loss threshold is not breached
- leverage is within safe range
- open position count is below the cap
- stop-loss distance is valid
- projected liquidation is not too close to the stop
- funding is acceptable for expected holding time
- slippage estimate is within policy

If any hard rule fails, the skill should return `halt` or `skip` depending on severity.

### 4. Calculate position size
Position size should come from risk and stop distance.

Basic sizing concept:
- risk_amount = account_balance × risk_per_trade
- stop_distance = absolute(entry_price - stop_loss)
- position_size = risk_amount / stop_distance

Reject or reduce the trade if:
- stop distance is invalid
- size exceeds margin capacity
- size forces excessive leverage
- size breaks exposure policy

### 5. Build normalized order request
The skill should construct a clean order object containing:
- market
- side
- order type
- size
- leverage
- optional reduce-only flag
- optional client order id

At this stage the skill is producing a validated execution request, not handling credentials.

### 6. Submit through host-provided client
The authenticated client supplied by the host should submit the order.
After submission, the skill should require confirmation of:
- accepted or rejected status
- fill state
- average fill price
- resulting position state

The skill must not assume the order exists until it is confirmed.

### 7. Manage open position
After fill, the skill should:
- record average entry
- track unrealized PnL
- monitor invalidation conditions
- support stop movement only when policy allows
- optionally trail the stop after sufficient favorable movement
- close early if market structure breaks

### 8. Exit and halt logic
The skill should close, reduce, or halt when:
- stop loss is hit
- take profit is reached
- strategy invalidates
- daily loss cap is reached
- abnormal execution behavior is detected
- order/position state becomes inconsistent

---

## Mandatory risk framework

### Per-trade risk
Default maximum risk should generally be 1 percent.
A hard upper bound can be 2 percent for aggressive configurations, but the skill should not exceed the configured policy.

### Daily loss protection
When realized daily loss reaches the configured threshold, for example 5 percent, the skill should stop allowing new trades and return `halt`.

### Consecutive loss protection
After a configured number of losing trades, for example 3, the skill should pause new entries to avoid destructive streak behavior.

### Exposure caps
The skill should respect:
- maximum concurrent positions
- maximum notional exposure
- correlation constraints when multiple positions are open

### Leverage discipline
Leverage should usually remain in a modest range such as 2x to 5x unless a stricter host policy overrides it.

---

## Hyperliquid-specific considerations

### Funding
Perpetual funding should be checked before entry.
The skill should be able to:
- reject trades under extreme funding
- downgrade position size
- warn the host if holding cost is high relative to the expected edge

### Liquidation distance
A setup is poor if the liquidation point is too close to the stop or too close to normal volatility.
The skill should prefer trades with meaningful room between liquidation and invalidation.

### Order-state confirmation
On Hyperliquid, execution handling should always confirm:
- whether the order was accepted
- whether it filled fully or partially
- whether a stale order remains open
- whether the actual position matches the expected state after execution

### Order-type discipline
The skill should support:
- market orders for urgency
- limit orders for price control
- reduce-only exits for safe reductions
- cancellation of stale working orders when policy requires it

---

## Failure handling and safe mode
The skill should prioritize safety when state becomes unreliable.

Safe-mode triggers include:
- account state cannot be read
- market state is stale
- order acknowledgements are inconsistent
- repeated submission failures occur
- open position cannot be reconciled
- daily or streak loss threshold is breached

Safe-mode behavior:
1. stop opening new positions
2. request cancelation of stale working orders through the host
3. reduce or close positions according to host policy
4. emit a clear log entry with the halt reason

---

## Logging requirements
The skill should emit operational logs without exposing secrets.

Useful logs include:
- market
- side
- signal decision
- entry
- stop distance
- calculated risk
- size
- leverage
- funding check result
- order submission result
- fill result
- exit reason
- pnl result
- safe-mode transitions

Do not log:
- private keys
- session tokens
- signing artifacts
- raw secrets from the host environment

---

## Minimal decision checklist
Before allowing a trade, the skill should be able to answer yes to all of the following:
- Do I have a valid market and direction?
- Do I have a current account state?
- Is the strategy signal still valid?
- Is the stop loss defined?
- Is the size based on risk?
- Is leverage inside policy?
- Is funding acceptable?
- Is the daily-loss cap still intact?
- Can the host confirm order state after submission?

If not, the skill should skip or halt.

---

## Example scenarios

### Scenario 1: valid long setup
- BTC is trending up
- external strategy detects a valid pullback entry
- stop is below the higher-low
- funding is neutral
- risk is 1 percent
- order request is built and sent through the host client

### Scenario 2: skip due to funding
- strategy says long
- funding is above configured threshold
- expected hold duration is long enough for funding to matter
- skill returns `skip` with a funding-based reason

### Scenario 3: halt after daily drawdown
- two or more losing trades occur
- realized daily loss reaches the configured limit
- skill enters safe mode and blocks further entries

---

## Notes
- This skill is an execution and risk layer, not a secret-management layer.
- The runtime must provide authenticated Hyperliquid access outside the skill itself.
- Best results come from pairing this skill with a separately tested strategy module.
