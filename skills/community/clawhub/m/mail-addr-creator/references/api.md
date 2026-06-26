# API Reference

## Endpoint

- Frontend: `https://webmail.suilong.online`
- Backend: `https://mail-api.suilong.online`
- Create address: `POST https://mail-api.suilong.online/admin/new_address`

## Request Headers

- `Content-Type: application/json`
- `x-admin-auth: <admin auth>` required
- `Authorization: Bearer <token>` optional when the system requires it
- `x-fingerprint` optional
- `x-lang` optional
- `x-user-token` optional

## Request Body

```json
{
  "enablePrefix": true,
  "name": "t2",
  "domain": "suilong.online"
}
```

## Success Response

```json
{
  "jwt": "xxx",
  "address": "t2@suilong.online",
  "password": null
}
```

## Normalized Output

Single result fields:

- `status`
- `address`
- `jwt`
- `password`
- `error`

Batch result fields:

- `summary.requested`
- `summary.created`
- `summary.already_exists`
- `summary.failed`
- `results[].name`
- `results[].status`
- `results[].address`
- `results[].jwt`
- `results[].password`
- `results[].error`

## Export Options

- `--output-format json` keeps the default structured JSON output
- `--output-format csv` writes a flat CSV stream
- `--output-file <path>` writes the rendered output to a file as well as stdout

CSV format:

- `row_type=summary` contains batch counts
- `row_type=result` contains one row per mailbox result

## Error Mapping

- Duplicate or existing-address responses map to `already_exists`
- Missing or rejected credentials map to `auth_error`
- Request validation failures, server errors, and network failures map to `error`

The script also performs local validation before calling the API:

- trim whitespace
- reject invalid names
- validate domains
- default `enablePrefix=true`
- de-duplicate batch names
- skip empty lines
