# Emergency Controls

MoneySharks supports always-available emergency controls, regardless of mode or circuit state.

## Trigger phrases (say any of these to activate)

- `halt moneysharks`
- `stop trading`
- `kill switch`
- `switch to paper mode`
- `cancel all orders`
- `flatten all positions`
- `disable cron`

## Halt sequence

When the agent receives any halt command:

1. **Set `state.json → halt=true`** immediately — blocks all future autonomous cycles
2. **Set `state.json → circuit_breaker=true`** — additional safety layer
3. **Disable cron execution** — pause all scheduled scan jobs
4. **Cancel resting orders** (if `execution.cancel_on_halt=true` in config)
   - Call `aster_readonly_client.cancel_all_orders(symbol)` for each allowed symbol
5. **Flatten positions** (only if user explicitly requests or `execution.flatten_on_emergency_stop=true`)
   - Call `aster_readonly_client.close_position_market()` for each open position
6. **Journal the halt event** with timestamp and reason
7. **Confirm to user**: "MoneySharks halted. All cycles stopped. [N] orders cancelled. Positions: [status]. Say 'resume moneysharks' to restart in paper mode."

## Resume from halt

After the user confirms it's safe to resume:

1. Confirm mode to restart in (default: `paper` for safety)
2. Set `state.json → halt=false`
3. Set `state.json → circuit_breaker=false`
4. Set `state.json → consecutive_errors=0`
5. If returning to `autonomous_live`: require re-confirmation of consent
6. Re-enable cron (if requested)
7. Run reconcile cycle before first execution

## Paper mode switch

"switch to paper mode":
1. Set `config.json → mode=paper`
2. Set `config.json → autonomous_live_consent=false`
3. No positions are touched (paper switch doesn't auto-close live positions)
4. Confirm: "Switched to paper mode. Existing positions are NOT auto-closed — manage them manually."

## Manual order management

To cancel a specific order or close a specific position without full halt:
- "cancel orders for BTCUSDT" → `cancel_all_orders("BTCUSDT")`
- "close BTCUSDT position" → `close_position_market("BTCUSDT", side, quantity)`

## Circuit breaker auto-trip conditions

The circuit breaker trips automatically when:
- `consecutive_errors >= 5` (API errors, script failures)
- An API error indicates account suspension or margin call
- Exchange health check fails (server errors)
- State reconciliation fails repeatedly

## State file reference

```json
{
  "halt": false,
  "circuit_breaker": false,
  "consecutive_errors": 0,
  "daily_loss": 0.0,
  "last_run": "2026-01-01T00:00:00Z"
}
```

Set `halt=true` in state.json to stop the agent immediately, even between cron runs.
