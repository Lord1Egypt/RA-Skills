# Troubleshooting

## Missing token

### Symptom

The script exits before making a live API call and tells you `META_ACCESS_TOKEN` is missing.

### Fix

Set `META_ACCESS_TOKEN` in the environment or inject it through OpenClaw skill config. Use `accounts` to validate.

```bash
python3 scripts/meta_ads.py accounts
```

## Wrong account

### Symptom

You can read some data but not the account or object the user asked about.

### Fix

- confirm the ad account ID,
- use `accounts` to list accessible accounts,
- set or override `META_AD_ACCOUNT_ID`,
- remember that account edges usually need `act_123...`

## Permission denied

### Symptom

OAuth errors, code 10, code 200, or write calls fail while read calls succeed.

### Causes

- missing `ads_management`
- missing `ads_read`
- missing `business_management` for a business-scoped workflow
- system user not assigned to the ad account
- app still in the wrong access mode

### Fix

1. inspect token permissions in Meta’s debugger,
2. confirm the user or system user is assigned to the ad account,
3. confirm the app has the right access level for the target account.

## Object not found

### Symptom

Graph returns code `803` or an equivalent “cannot load object” message.

### Causes

- wrong ID
- object belongs to another account
- token has no access
- object was deleted or archived beyond the queried scope

### Fix

Read the parent object or list edge first and work from known IDs.

## Invalid parameter

### Symptom

Graph returns code `100` or a message about invalid fields or params.

### Causes

- wrong enum value
- stale field copied from an old example
- missing required nested object
- wrong objective and optimisation combination
- malformed JSON string on a nested param

### Fix

- move the payload into a JSON file,
- use `--dry-run`,
- compare field names to current docs,
- keep top-level nested params as JSON objects and let the script stringify them.

## Rate limiting

### Symptom

Code `613`, `80004`, HTTP `429`, or repeated throttling messages.

### Fix

- reduce field count,
- shrink the date window,
- avoid `--fetch-all` unless necessary,
- use `batch` for many small reads,
- use `--async` for heavy Insights jobs,
- wait before retrying.

The script already applies exponential backoff for common transient and throttling failures.

## Async Insights timeout

### Symptom

A long report stays running or the script times out.

### Fix

- reduce breakdowns,
- reduce fields,
- shorten the date range,
- lower the reporting level from `ad` to `adset` or `campaign`,
- increase `--poll-timeout`,
- write results to a file with `--output`.

## Upload errors

### Symptom

Image or video upload fails.

### Fix

- make sure the file exists,
- for image upload, keep a real filename extension such as `.jpg` or `.png`,
- check the file size and format are supported by Meta,
- confirm the account has access to the asset destination.

## Status did not change delivery

### Symptom

You set an ad `ACTIVE`, but delivery still looks inactive.

### Cause

A parent ad set or campaign may still be paused, limited, rejected, or misconfigured.

### Fix

Read upward through the hierarchy:

1. ad
2. ad set
3. campaign
4. account context

Also confirm billing, schedule, and creative approval state.

## Tracking or conversion fields are empty

### Symptom

Insights show spend and clicks but conversions are empty or inconsistent.

### Causes

- wrong attribution window
- event not configured in pixel or app
- querying the wrong action type
- using flat conversion fields instead of `actions` and `action_values`

### Fix

- request `actions` and `action_values`,
- confirm the promoted object and pixel or app setup,
- check the requested attribution window,
- shorten the date range if conversion lag is high.

## Script path or Python missing in OpenClaw

### Symptom

The skill loads but command execution fails.

### Fix

- ensure `python3` exists on the host or sandbox,
- if using an OpenClaw sandbox, install Python inside the container too,
- start a new session after changing skill config or the sandbox image.
