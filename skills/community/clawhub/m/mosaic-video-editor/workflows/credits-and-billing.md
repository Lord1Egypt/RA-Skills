# Credits & Billing

## Read credit state (balance + auto top-up)

```
GET /credits
```

This endpoint returns balance, active plan metadata, billing cycle dates, and current `auto_topup` settings in one response.

[Docs](https://docs.mosaic.so/api/credits/get-credits)

## Update auto top-up settings

Use:

```bash
POST /credits/settings
```

Example body:

```json
{
  "auto_topup": {
    "enabled": true,
    "threshold": 1000,
    "quantity": 5000
  }
}
```

When credit balance drops below `threshold`, `quantity` credits are purchased automatically at your plan's rate.

Notes:
- Requires an eligible paid plan (Creator/Professional family); free plans receive `403`.
- To read current top-up values, use `GET /credits` (not `GET /credits/settings`).

[Docs](https://docs.mosaic.so/api/credits/post-credits-settings)

## View current plan

```
GET /plan
```

[Docs](https://docs.mosaic.so/api/plan/get-plan)

## List available plans (for upgrade UX)

```
GET /plan/list
```

Typical plan IDs: `creator`, `creator_annual`, `professional`, `professional_annual`, `pro`.

[Docs](https://docs.mosaic.so/api/plan/get-plan-list)

## Upgrade plan

```json
POST /plan/upgrade
{ "plan_id": "professional" }
```

Possible responses:
- Immediate change (`requires_checkout: false`)
- Checkout required (`requires_checkout: true`, with `checkout_url`)

[Docs](https://docs.mosaic.so/api/plan/post-plan-upgrade)

## Required flow for credit-blocked runs

When a run or node is marked as needing credits (`needs_credits: true` or `needsCredits: true`), do this in order:

1. **Check plan first:** `GET /plan`
2. **If user is on free/no paid plan:**
   - Tell the user a paid plan is required to continue the run.
   - Call `GET /plan/list`.
   - Present available plans (`id`, `billing`, `price_usd`, `credits_per_month`, `top_up_rate_per_100_credits_usd`).
   - Ask which `plan_id` to upgrade to.
   - Call `POST /plan/upgrade` with that `plan_id`.
3. **If upgrade requires checkout (`requires_checkout: true`):**
   - Share the `checkout_url` with the user.
   - Wait for confirmation that checkout is complete.
   - Re-check with `GET /plan` before proceeding.
4. **After upgrade succeeds:** ask whether to enable auto top-ups.
5. **If yes:** collect `threshold` and `quantity` and call `POST /credits/settings`.
6. **Then resume blocked work:** `POST /agent_run/{run_id}/resume`.
