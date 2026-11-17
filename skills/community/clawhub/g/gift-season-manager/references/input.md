# Offline helper contract

Python 3.11+ standard library, no network, writes, credentials or external actions. Resolve paths from the installed skill directory.

```sh
python3 scripts/budget.py assets/example.json
```

Run the command from this skill directory, or resolve both paths absolutely. For real use point to a private input JSON file. Reads only the explicitly supplied file and prints derived JSON; errors go to stderr with exit code 2. No output file is created and the source is unchanged. The included [example](../assets/example.json) is fictional.

Schema 1: currency (uppercase three-letter code), budget and costs. Only one currency per report; this v1 supports nonnegative amounts with at most two decimals, not every currency's minor-unit convention. Money is a decimal string or integer, never float/boolean/nonfinite. Use opaque cost IDs, not recipient names.

Each cost: id, same currency, paid (gross cash paid), refund_received, committed_total (gross TOTAL including paid, or null), estimate (uncommitted only, or null), cancelled boolean. Duplicate IDs fail. A paid item requires committed_total >= paid. Refund received cannot exceed paid; a promised refund stays 0 until received. Once committed, estimate must be null. Cancellation means outstanding contractual obligation has been confirmed released; do not mark cancelled just because a request was sent. Cancellation doesn't imply cash returned. A partially reduced but active obligation must be reconciled explicitly.

Net paid = gross paid minus received refunds. Forecast = net paid + active unpaid commitments + estimates for active uncommitted items. Active unknown estimates make complete false. Headroom is against KNOWN costs, not permission or proof of affordability. No exchange rates or negative line-item adjustments. Refund reconciliation is original bookkeeping logic, not a provider integration.

Expected example: gross/net paid 80; unpaid commitment 70; estimates 90; forecast 240; known headroom 60. After cancelling cost-1 but with refund pending, its remaining commitment is released but the paid 80 stays in forecast. With received refund 80, net paid becomes 0. Output contains only totals and unknown opaque cost IDs; arbitrary recipient/order fields are never exported.
