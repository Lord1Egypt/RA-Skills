# Pocketbook Schema

Use this reference when writing or editing ledger payloads, or when changing the scripts.

## Data Root

Default data root: `~/.openclaw/pocketbook/default`

Files:

- `ledger.jsonl`: append-only event log and source of truth
- `personal_finance.md`: derived readable view
- `profile.json`: user defaults and aliases

## Event Model

Persist one JSON object per line in `ledger.jsonl`.

Required common fields:

- `event_id`: unique event identifier such as `evt_...`
- `event_type`: `create`, `update`, or `revert`
- `entry_id`: stable identifier for the logical ledger entry
- `recorded_at`: ISO 8601 timestamp with offset
- `timezone`: usually `Asia/Shanghai`
- `source_text`: original user utterance that caused the event

### Create Event

Create payload fields:

- `entry_type`: `expense`, `income`, `refund`, or `transfer`
- `amount`: decimal string such as `"28.00"`
- `currency`: default `CNY`
- `occurred_at`: ISO 8601 timestamp with offset
- `category`: string, may be `unknown`
- `payment_method`: string, may be `unknown`
- `account`: string, may be `unknown`
- `merchant`: optional string, may be `unknown`
- `note`: optional string
- `status`: `confirmed` or `incomplete`
- `needs_review`: boolean
- `inferred_fields`: list of field names inferred by the agent
- `confidence`: optional object keyed by field name with numeric confidence values
- `fingerprint`: duplicate-detection fingerprint
- `idempotency_key`: optional dedupe key from caller

### Update Event

Update payload fields:

- `entry_id`
- `changes`: object of mutable fields to overwrite
- `reason`: optional short explanation

Mutable fields:

- `amount`
- `occurred_at`
- `category`
- `payment_method`
- `account`
- `merchant`
- `note`
- `status`
- `needs_review`
- `inferred_fields`
- `confidence`
- `currency`
- `entry_type`

### Revert Event

Revert payload fields:

- `entry_id`
- `reason`: optional short explanation

## Profile Model

`profile.json` is optional, but when present it should be applied before falling back to `unknown`.

Suggested structure:

```json
{
  "defaults": {
    "currency": "CNY",
    "timezone": "Asia/Shanghai",
    "payment_method": "wechat",
    "account": "cmb"
  },
  "aliases": {
    "payment_method": {
      "微信": "wechat",
      "wx": "wechat"
    },
    "account": {
      "招行": "cmb",
      "招商银行": "cmb"
    },
    "category": {
      "餐饮": "food"
    }
  }
}
```

Supported default fields:

- `currency`
- `timezone`
- `payment_method`
- `account`

Supported alias fields:

- `entry_type`
- `category`
- `payment_method`
- `account`
- `merchant`
- `currency`
- `timezone`

## Completion Rules

Treat an entry as pending when any of these are true:

- `status` is `incomplete`
- `needs_review` is `true`
- `category`, `payment_method`, or `account` is `unknown`

## Query Semantics

- expense total: sum of active `expense` entries
- income total: sum of active `income` entries
- refund total: sum of active `refund` entries
- transfer total: sum of active `transfer` entries
- net outflow: `expense - refund`

`transfer` does not count as spending by default.

## Duplicate Heuristic

The append script reports possible duplicates when an existing active entry matches:

- same `entry_type`
- same `amount`
- same local calendar date
- plus at least one contextual match such as same category, same merchant, or a close timestamp

This is a warning, not a hard rejection.
