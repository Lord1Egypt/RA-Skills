# Daraja Endpoint Reference

Use this reference when a task needs endpoint names, API versions, or flow coverage. Treat it as a quick index, not a replacement for checking the live Safaricom Daraja portal before production work.

## Official Source Snapshot

Checked on 2026-05-25 against:

- Safaricom Daraja developer portal: https://developer.safaricom.co.ke/
- Safaricom developer API catalogue GraphQL query \`getApis\` via https://developer.safaricom.co.ke/api/graphql
- Portal documentation records through \`populateApi\` for STK Push, STK Query, Transaction Status, Reversal, and Account Balance

The portal is branded Daraja 3.0. The public pages are client-rendered, so prefer the live catalogue response over scraped static HTML when checking endpoint versions.

## Core Sandbox Endpoints

| Flow | Method | Sandbox endpoint |
| --- | --- | --- |
| Daraja authorization session | GET | Check the current Daraja portal for the session endpoint before implementation. |
| STK Push / Lipa na M-Pesa Online | POST | \`https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest\` |
| STK Push query | POST | \`https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query\` |
| C2B register URL | POST | \`https://sandbox.safaricom.co.ke/mpesa/c2b/v2/registerurl\` |
| B2C payment request | POST | \`https://sandbox.safaricom.co.ke/mpesa/b2c/v3/paymentrequest\` |
| Transaction status | POST | \`https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query\` |
| Account balance | POST | \`https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query\` |
| Reversal | POST | \`https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request\` |

## Guidance

- Use sandbox endpoints by default. Switch to production hostnames only when the user explicitly asks for production guidance, and ask before any live call.
- Re-check the official catalogue before writing production instructions. Endpoint versions can differ from older examples and SDK snippets.
- The May 2026 catalogue listed C2B register URL as \`v2\` and B2C payment request as \`v3\`; avoid hard-coding older \`v1\` B2C/C2B URLs unless maintaining legacy code.
- If the catalogue and a detailed documentation page disagree, report the disagreement and avoid claiming a migration is required without confirmation from Safaricom.
