# Housecall Pro consumer API — recipes

Every recipe assumes `HCP_TOKEN` holds the 129-character retrieval token, as set
up in `SKILL.md`. Endpoints marked **unverified** were read out of the SPA's
JavaScript but never exercised against a real document.

## Field map — `GET /alpha/customer_estimates/$HCP_TOKEN` (verified)

The envelope nests under `{object, data}` wrappers.

| Path | What it is |
| --- | --- |
| `.estimate.data.estimate_number` | Human-facing estimate number |
| `.estimate.data.estimate_uuid` | `csr_…`, the estimate's id |
| `.estimate.data.organization_id` | Company UUID — feeds the company lookup |
| `.estimate.data.customer_approval_mode` | e.g. `single_option` |
| `.estimate.data.address.data.printable_address` | Service address |
| `.options.data[]` | One entry per priced option |
| `.options.data[].id` | `est_…` — **this is what you decline** |
| `.options.data[].status` | e.g. `Awaiting Approval`, `Declined` |
| `.options.data[].approval_date` | `null` until approved |
| `.options.data[].sub_total` / `.total_amount` | **integer cents** |
| `.options.data[].tax.data.rate` | Fraction (`0.0825`), NOT cents |
| `.options.data[].tax.data.amount` | **integer cents** |
| `.options.data[].line_items.data[]` | `name`, `description`, `quantity`, `kind`, `unit_price`, `amount` |
| `.customer_name`, `.customer_email` | Who it is for |
| `.message_from_pro` | Free-text note |
| `.company_name`, `.company_phone_number`, `.company_email`, `.company_website` | The contractor |
| `.payment_options.can_pay_online` | Whether online payment is offered |
| `.deposit_requirement` | e.g. `not required` |
| `.signatures_enabled` | Whether approval demands a signature |

`kind` on a line item is `labor` or `material` — not `service`.

## Totals, correctly scaled

```sh
jq -r '.options.data[]
  | "\(.name): subtotal $\(.sub_total/100) + tax $\(.tax.data.amount/100)"
  + " (\(.tax.data.rate*100)%) = $\(.total_amount/100)"' estimate.json
```

## Line items as TSV

```sh
jq -r '.options.data[].line_items.data[]
  | [.name, .kind, .quantity, (.unit_price/100), (.amount/100)] | @tsv' estimate.json
```

## Just the open options and their ids

```sh
jq -r '.options.data[]
  | select(.approval_date == null and .status != "Declined")
  | "\(.id)\t\(.name)\t$\(.total_amount/100)"' estimate.json
```

## The contractor behind it (verified)

```sh
ORG=$(jq -r '.estimate.data.organization_id' estimate.json)
curl -s "https://app.housecallpro.com/alpha/organizations/$ORG" | jq
```

Returns `id`, `company_name`, `phone_number`, `email`, `website`, `logo_url`,
`address`, `default_arrival_window`, `terms_url`, `founding_pro_uuid`. Needs no
auth header at all.

## Decline (verified shape, from the app's own code)

```sh
curl -s -X POST \
  -H "Authorization: Token $HCP_TOKEN" \
  --data-urlencode "estimate_option_uuids[]=est_XXXX" \
  https://app.housecallpro.com/api/estimates/estimate_options/customer_declines
```

Repeat `--data-urlencode "estimate_option_uuids[]=…"` per option.

## Approve — blocked

```
POST /api/estimates/estimate_options/customer_approvals
  Authorization: Token <token>
  estimate_option_uuids[]=est_…
  response_token=<reCAPTCHA v3 token>       <-- cannot be produced outside the page
  signature[signature], signature[signatory_name], signature[signatory_user_agent]
```

`estimates_customer_approvals` is the only reCAPTCHA action in the entire
consumer app. Approve in a browser.

## Invoices — `GET /api/invoices/consumer/v1/invoices/$HCP_TOKEN` (verified)

An invoice token is **32 hex characters**, not the estimate's 129. The document
is flat — no `{object, data}` wrappers.

| Path | What it is |
| --- | --- |
| `.invoice_number` | Human-facing invoice number |
| `.status` | Display string, e.g. `paid` |
| `.due_amount` | **integer cents** — the field that decides paid-ness |
| `.subtotal` / `.total` / `.amount` | **integer cents** |
| `.company_info.{name,phone_number,email,website,organization_uuid}` | The contractor |
| `.customer.{uuid,email,mobile_number,card_on_file}` | You |
| `.payment_options.can_pay_online` | Whether it can still be paid online |
| `.invoice_count` | How many invoices the job carries |

No line items, and no tax field — tax is `total - subtotal`.

```sh
jq -r '"#\(.invoice_number) [\(.status)] due $\(.due_amount/100) of $\(.total/100)"' invoice.json
```

These 404 for an invoice token despite appearing in the bundles — do not use
them: `/api/invoices/consumer/invoices/{t}`, `/api/v2/consumer/invoices/{t}`,
`/api/v2/consumer/sent_invoices/{t}`,
`/api/invoices/linking/consumer/sources/{t}`,
`/api/v2/consumer/invoices/{t}/invoice_or_estimate_pdf`.
`/alpha/jobs/{t}` answers 401 — it wants a different credential.

## Other endpoints (unverified)

Read out of the SPA bundles; shapes unconfirmed.

**Account-level portal (OTP login, spans all documents from one pro)** —
`/api/customer_portal/request_otp`, `/api/customer_portal/verify_otp`,
`/api/v2/customer_portal/magic_links`, `/api/v2/customer_portal/organizations`,
`/api/v2/consumer/user/{log_in,log_out,profile,service_agreements}`

**Jobs / media** — `/alpha/jobs/{id}`, `/api/customer_gallery/{id}`,
`/api/attachments/customer_gallery/{id}`, `/alpha/after_actions/{id}`

**Service agreements** — `/api/consumer/service_agreement/{id}`,
`/api/v2/consumer/service_agreement/{id}`

**Communications** — `/communications/consumer/organizations`,
`/communications/consumer/preferences/{id}`,
`/communications/consumer/consents/{opt_in,opt_out}`

## Safety

- The retrieval token is a bearer credential. Never commit it, never paste it
  into a shared transcript, never put it in a URL you log.
- Declining is not reversible from here.
- Never attempt to script approval.
