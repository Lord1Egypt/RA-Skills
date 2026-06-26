# Risk Policy

## Hard rules
- one position per symbol by default
- no pyramiding unless explicitly enabled
- enforce symbol allowlist
- enforce max daily loss
- enforce max total exposure
- enforce max notional per trade
- enforce max concurrent positions
- require stop-loss when configured
- require reward:risk threshold

## Circuit breakers
Pause new execution when:
- repeated API errors occur
- rate-limit violations stack up
- account state cannot be reconciled
- exchange health looks degraded
- daily loss limit is hit
