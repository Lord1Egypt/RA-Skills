---
name: housecallpro
description: >-
  Read a Housecall Pro estimate or invoice your contractor sent you — line
  items, totals, tax, what is still owed, the company behind it — from a shell
  with plain curl, instead of running the housecallpro-mcp server. Use when you want the data without the MCP, in a
  script, or on a machine where the MCP isn't installed. Covers declining an
  option, and why approving cannot be scripted.
---

# Housecall Pro customer portal via curl (no MCP)

This reads the **customer** side of Housecall Pro: the estimate or invoice a
contractor emails or texts you. It is not the Housecall Pro public API — that
one serves the business running on Housecall Pro and needs an API key from
their account.

**No browser bridge is needed.** `app.housecallpro.com` is not bot-walled; a
plain `curl` gets a `200`. Do not reach for `fpx` here.

## The one thing to know first

There is no account and no standing link: Housecall Pro sends a separate,
disposable link per document, so you work from whichever link you were sent.

Your link is a **bearer credential**. Anyone holding it can read the estimate
and decline it. Keep it in a variable or a file you control, never in a command
you paste into a shared transcript, and never commit it.

## Setup

Two forms of link exist, and **estimates and invoices use different token
shapes**: an estimate token is 129 characters (two 64-char hex halves joined by
`_`), an invoice token is a bare 32-char hex string. The short link redirects to
whichever applies:

```sh
# What your contractor sent (short form)
SHORT='https://pro.housecallpro.com/mobile_estimate/XXXXXXXXXX'   # or /mobile_invoice/…

# Resolve it to the retrieval token (an estimate's is 129 chars, an invoice's 32)
HCP_TOKEN=$(curl -sI "$SHORT" | tr -d '\r' | awk 'tolower($1)=="location:"{print $2}' | sed 's#.*/##')

# If you already have a client.housecallpro.com/estimates/… or /invoices/… link, just:
# HCP_TOKEN='<the last path segment>'

echo "${#HCP_TOKEN}"   # 129 for an estimate, 32 for an invoice
```

## Read the estimate

```sh
curl -s -H 'Accept: application/json' \
  "https://app.housecallpro.com/alpha/customer_estimates/$HCP_TOKEN" > estimate.json
```

No `Authorization` header — reads carry the token in the path.

**Money is integer cents.** `total_amount: 34639` means `$346.39`. Divide by 100
before reporting anything. `tax.rate` is the exception: it is a fraction
(`0.0825` = 8.25%) and must not be scaled.

A one-line summary:

```sh
jq -r '
  "\(.company_name) — estimate #\(.estimate.data.estimate_number)",
  "For: \(.customer_name) at \(.estimate.data.address.data.printable_address)",
  (.options.data[] |
    "  \(.name) [\(.status)] $\(.total_amount/100)"),
  (.options.data[].line_items.data[] |
    "    \(.quantity) x \(.name) @ $\(.unit_price/100) = $\(.amount/100)")
' estimate.json
```

More recipes, including the company lookup and the full field map, are in
[`references/recipes.md`](references/recipes.md).

## Is it still awaiting me?

```sh
jq -r '.options.data[] | select(.approval_date == null and .status != "Declined")
       | "OPEN: \(.name) $\(.total_amount/100)"' estimate.json
```

## Declining an option

Declining works from a shell. It is the only mutation that does — and it tells
the contractor you are not proceeding, so read the estimate first.

```sh
OPTION_ID=$(jq -r '.options.data[0].id' estimate.json)   # est_…

curl -s -X POST \
  -H "Authorization: Token $HCP_TOKEN" \
  --data-urlencode "estimate_option_uuids[]=$OPTION_ID" \
  https://app.housecallpro.com/api/estimates/estimate_options/customer_declines
```

Note the asymmetry: **writes put the token in the `Authorization` header**,
reads put it in the path.

**A 2xx is not proof.** Re-read and check the option actually moved:

```sh
curl -s "https://app.housecallpro.com/alpha/customer_estimates/$HCP_TOKEN" \
  | jq -r '.options.data[] | "\(.id) \(.status) approval_date=\(.approval_date)"'
```

## Approving cannot be scripted

`POST /api/estimates/estimate_options/customer_approvals` requires a
`response_token` — a **reCAPTCHA v3 token** minted in-page for the action
`estimates_customer_approvals`. No shell client can produce one, and neither can
the fetchproxy bridge (it issues `fetch` calls; it does not run page JS).

Open the link in a browser and press Approve there. Do not try to work around
this: approving is a binding commitment to a quoted price.

## Failure modes

| Symptom | Meaning |
| --- | --- |
| `401` / `403` | The link expired or was revoked. Ask your contractor to resend it. |
| `404` (HTML) | The document was deleted or re-issued; the old link is dead. |
| `$HCP_TOKEN` is empty or not 129 chars | The short link expired before it could redirect. |
| A `200` that isn't JSON | Same as above — the link is no longer valid. |

## Invoices

```sh
curl -s -H 'Accept: application/json' \
  "https://app.housecallpro.com/api/invoices/consumer/v1/invoices/$HCP_TOKEN" > invoice.json
```

**The `v1` segment is required.** `/api/invoices/consumer/invoices/<token>` —
the same path without it — returns 404, as do the `/api/v2/consumer/invoices/…`
and `/api/v2/consumer/sent_invoices/…` paths that also appear in the app's
JavaScript. Only this one answers.

```sh
jq -r '"\(.company_info.name) — invoice #\(.invoice_number) [\(.status)]",
       "  subtotal $\(.subtotal/100)",
       "  tax      $\((.total - .subtotal)/100)",
       "  total    $\(.total/100)",
       "  due      $\(.due_amount/100)"' invoice.json
```

Two things to know: the invoice document has **no line items** (a paid invoice
renders as a summary in the portal, and the API returns exactly that), and **no
tax field** — the tax figure is `total - subtotal`. Money is integer cents here
too. Use `due_amount` rather than `status` to decide whether it is settled.

## In context groups

On mcp-host, housecallpro-mcp joins the **home** group. It ships no canonical
read and no subject: there is no customer account to list from, so nothing
here can answer "what's new / due / on at home" across your documents — every
estimate or invoice is reached only through the link the contractor sent. Its
tools carry `lookup` hints (estimate, invoice, the contractor's details, the
saved links), `change` on declining an option, and `other` on approve (which
always refuses). A compound ask such as "is the pool on, and what does the
plumber's quote say?" reaches it only with a link in hand — the group's
round-up skips it. It needs no browser: reads are plain HTTPS.
