# Mutation safety

## Approval boundary

Reading or planning does not authorize mutation. Before a write, identify the active environment/account, target resource, exact proposed change, cost, reversibility, and expected effect. Obtain explicit approval for that concrete action.

Approval for one domain, DNS record, quote, API operation, or environment does not cover another.

## Preflight

1. Run `gddy --version` and inspect the relevant command or API operation.
2. Confirm `gddy env get` and `gddy auth status` without exposing credentials.
3. Read the current resource and retain rollback data.
4. Use `--dry-run` for any supported mutation.
5. Show the plan and obtain approval.
6. Execute once, capture the operation/request ID, then verify with a fresh read.

## Domain registration

Use `gddy guide domain-purchase`. Quote first and show domain, price, currency, period, renewal price, auto-renew/privacy/nameservers, contacts, legal agreements, and expiry. The purchase must use the reviewed cached quote on the same machine. Never add `--agree --confirm` until the user approves that exact quote.

If the call becomes ambiguous, check account domains and the returned operation. Do not request a new quote or start another purchase merely because the client timed out.

## DNS

- DNS writes work only when GoDaddy hosts the authoritative zone.
- `add` appends; retry can duplicate.
- `set` reconciles per record and is not atomic. A mid-run failure can leave partial progress.
- `delete` removes every record matching type+name.
- `NS` and `SOA` are GoDaddy-managed and read-only through the DNS commands.
- A CNAME cannot coexist with another record type at the same name. Do not use `--replace-conflicting-types` without showing every record it will remove.

Before `set` or `delete`, save the current matching records. After execution, list them again. For changes affecting web, mail, verification, or delegation, explain DNS propagation and verify authoritative data separately when useful.

## Generic API mutations

An operation exposed by `gddy api call` may affect money, identity, legal consent, certificates, hosting, shopper accounts, auctions, transfers, or production availability. The presence of `--dry-run` is not approval and does not guarantee the remote service can simulate every effect. Inspect the operation schema/scopes and apply the same domain-specific safety standard before calling it.
