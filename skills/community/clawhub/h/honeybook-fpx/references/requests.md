# HoneyBook requests for fpx + curl

Ready-to-run commands for the four live read endpoints `honeybook-mcp`
actually calls (from `src/tools/*.ts` + `src/client.ts`). All are
`GET api.honeybook.com/api/v2/*`, carrying the same headers built in
`HoneyBookClient.request` — see `../SKILL.md` for how to capture
`$AUTH_TOKEN`/`$USER_ID`/`$API_VERSION` first. `$TRUSTED_DEVICE` is
optional and `hb-api-fingerprint` is not required at all.

```sh
hb_get() {   # $1 = path (e.g. /api/v2/users/$USER_ID/workspace_files)
  curl -s "https://api.honeybook.com$1" \
    -H 'accept: application/json, text/plain, */*' \
    -H "hb-api-auth-token: $AUTH_TOKEN" \
    -H "hb-api-user-id: $USER_ID" \
    ${TRUSTED_DEVICE:+-H "hb-trusted-device: $TRUSTED_DEVICE"} \
    -H "hb-api-client-version: $API_VERSION" \
    -H "hb-api-duplicate-calls-prevention-uuid: $(uuidgen)" \
    -H 'hb-admin-login: false'
}
```

`sign_contract`/`pay_invoice` are **not** included below — the MCP itself
doesn't call a signing/payment API; it returns a deep link
(`$PORTAL_ORIGIN/app/workspace_file/<file_id>/agreement` or `/invoice`) for
the user to open in their browser. There's no request shape to transcribe.

---

## 1. List a vendor's shared files

`list_workspace_files` (`src/tools/workspace_files.ts`):

```sh
hb_get "/api/v2/users/$USER_ID/workspace_files" > /tmp/hb-files.json
```

Response envelope (`HBListEnvelope<T>`, `src/types.ts`):
`{ data: [...], cur_page, last_page, last_id?, total_count? }`.
If `last_page` is `false`, more results exist on later pages. The MCP
requests `?page=2`, `?page=3`, … (the parameter `/api/v2/client/events`
takes) until `last_page` is true, and reports `complete: false` if a page
brings nothing new; do the same here if you need every file.

```sh
# Filter to a file_type client-side (agreement | invoice | brochure | proposal)
jq '[.data[] | select(.file_type == "agreement")]' /tmp/hb-files.json

# Compact listing: id, type, title, accepted/paid flags
jq -r '.data[] | [.["_id"], .file_type, .file_title, (.is_file_accepted|tostring), (.has_pending_payment|tostring)] | @tsv' /tmp/hb-files.json
```

## 2. Get one file's detail

`get_workspace_file` (`src/tools/workspace_files.ts`):

```sh
hb_get "/api/v2/workspace_files/$FILE_ID" > /tmp/hb-file.json
```

The raw response is large on proposal-class files (a real one hit ~1.3 MB,
mostly vendor-internal fields the MCP prunes off `company`:
`vendor_emails`, `workflow_automation_infos`, `brochure_templates`,
`questionnaires`, `lead_sources`, `proposals`, `agreements`, `invoices`,
`vendor_packages`, `contact_forms`, `stripe_persons`,
`user_pipeline_stages`, `project_types`, `company_assets`). Project what you
need instead of dumping the whole body:

```sh
# Summary-equivalent: identity, status, vendor, event, pricing totals, payments
jq '{
  id: .["_id"], title: .file_title, type: .file_type,
  status: .status_name, accepted: .is_file_accepted,
  vendor: .company.company_name,
  event: (.event | {date: .event_date, type, couple_names}),
  total_price: .vendor_proposal.total_price,
  payments: (.payments_container.payments // [] | map({due_date, amount, is_paid}))
}' /tmp/hb-file.json

# Full contract text + signatures (the "agreement" section)
jq '.agreement' /tmp/hb-file.json

# Full line items (the "pricing" section)
jq '.vendor_proposal' /tmp/hb-file.json
```

## 3. Get a workspace (vendor project)

`get_workspace` (`src/tools/workspaces.ts`) — `workspace_id` is
`.workspace._id` on any workspace_file from endpoint 1 or 2:

```sh
hb_get "/api/v2/workspaces/$WORKSPACE_ID" \
  | jq '{id: .["_id"], has_sent_files, has_signed_files, has_paid_payments}'
```

## 4. List saved payment methods

`list_payment_methods` (`src/tools/payment_methods.ts`):

```sh
hb_get "/api/v2/users/$USER_ID/payment_methods" | jq '.'
```

Empty array (`[]`) if the client has no payment method saved with this
vendor — not an error.

---

## Error shapes to check on every response

```sh
# Wrong API version — re-derive it from the error body itself (no /api/gon round-trip needed)
jq -r 'select(type=="object") | .error_data.server_api_version // empty' /tmp/hb-resp.json

# HTTP status: 401 = session expired (re-capture), 429 = rate limited (wait 2s, retry once).
# A 404 whose body names HBUnauthorizedError is ALSO an expired session, not a
# missing resource — a revoked token does not reliably come back as 401.
```

A non-2xx HTTP status with a body matching `HBWrongAPIVersionError` means
retry the *same* request with `hb-api-client-version` set to
`.error_data.server_api_version` from the body (or a fresh `/api/gon` fetch,
per `../SKILL.md`).
