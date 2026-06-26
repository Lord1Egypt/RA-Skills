# Troubleshooting - Maps

## Result Is in the Wrong Place

Symptoms:
- The returned point is in the wrong city or country.

Actions:
1. Check coordinate order and serialization.
2. Add explicit city, region, postal code, or country bias.
3. Re-run with a bounded query instead of free text alone.

## Address Match Is Too Fuzzy

Symptoms:
- Provider returns locality-level or approximate matches only.

Actions:
1. Ask for missing apartment, postal code, or district context.
2. Switch to a provider with stronger rooftop geocoding if needed.
3. Mark the result as approximate instead of pretending it is exact.

## Travel Time Looks Unrealistic

Symptoms:
- ETA or distance is much lower than expected.

Actions:
1. Confirm the route used a real routing engine, not Haversine.
2. Verify travel mode and traffic assumptions.
3. Re-check whether ferries, tolls, or highways were implicitly included.

## Apple Maps Link Opens in Browser Instead of the App

Symptoms:
- The link opens in a browser tab on macOS instead of Maps.app.

Actions:
1. Keep the link for sharing.
2. If local execution matters, use a macOS-specific `open -a Maps` workflow.
3. Treat the browser-open result as a launch-path issue, not a data issue.

## Paid Provider Returns Quota Errors

Symptoms:
- Provider reports limit, denied, or rate errors.

Actions:
1. Stop repeating the same request.
2. Switch to cached results or an acceptable fallback provider.
3. Document whether the blocker is daily quota, bad auth, or burst rate.
