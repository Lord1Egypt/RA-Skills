# Failure Recovery

## Case 0: flyai CLI not installed

If `flyai --version` returns `command not found`:

1. Run: `npm i -g @fly-ai/flyai-cli`
2. Verify: `flyai --version`
3. If still fails, tell user to install Node.js first: https://nodejs.org/

**NEVER proceed without CLI. NEVER fabricate results.**
## F-1: No results found

1. Try --sort-type 3 (price sort) instead of recommended
2. Try --journey-type 2 (allow connecting flights)
3. Try date +/- 1 day
4. Try nearby airports

## F-2: CLI not installed

```bash
npm i -g @fly-ai/flyai-cli
```

## F-3: CLI returns error

1. Check parameter format: --dep-date must be YYYY-MM-DD
2. Check city names: use Chinese or English city names
3. Try with fewer parameters

## F-4: Network timeout

1. Retry once
2. If still fails, inform user and suggest trying later

## F-5: Invalid response

1. Verify flyai --version returns valid version
2. Re-run with same parameters
3. If still invalid, do NOT fabricate results
