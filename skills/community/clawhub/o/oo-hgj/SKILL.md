---
name: oo-hgj
description: "HaiGuanJia (openapi.hgj.com). Use this skill for ANY HaiGuanJia request — reading, creating, updating, and deleting data. Whenever a task involves HaiGuanJia, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "HaiGuanJia"
  author: "OOMOL"
  version: "1.0.5"
  services: ["hgj"]
  icon: "https://static.oomol.com/logo/third-party/hgj.png"
---

# HaiGuanJia

Operate **HaiGuanJia** through your OOMOL-connected account. This skill calls the `hgj` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected HaiGuanJia. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hgj" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hgj" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `batch_get_truck_positions` — Get current positions for multiple trucks. Only query vehicles that the caller is authorized to track. HaiGuanJia may charge for this request.
- `bind_ningbo_schedule` — Bind a Ningbo bill to an explicit vessel schedule. [write]
- `bind_shanghai_schedule` — Bind a Shanghai bill to an explicit HaiGuanJia vessel schedule. [write]
- `cancel_em_manifest_close` — Cancel EM Close for a full 8000-code house bill. [destructive]
- `check_aci_bill_availability` — Check whether an ACI 8000-code and house-bill combination is available.
- `check_em_bill_availability` — Check whether an EM 8000-code and house-bill combination is available.
- `close_em_manifest` — Submit EM Close for a full 8000-code house bill. The official page has conflicting free/consumption wording, so Connector treats it as potentially chargeable and never retries automatically. [destructive]
- `delete_aci_manifest` — Delete an ACI house bill through the selected agency or customer channel. [destructive]
- `delete_afr_manifest` — Delete an AFR house bill with the required cancellation reason. [destructive]
- `delete_ams_manifest` — Delete an AMS house bill through the selected agency or customer SCAC channel. [destructive]
- `delete_em_manifest` — Delete an EM house bill through the selected agency or customer channel. [destructive]
- `delete_ics2_manifest` — Delete an ICS2 manifest through the shared endpoint while preserving the selected F14, F15, F16, or F17 product API ID. [destructive]
- `delete_isf10_manifest` — Delete an ISF-10 AMS bill through the selected agency or customer FILER CODE channel. [destructive]
- `delete_isf5_manifest` — Delete an ISF-5 AMS bill through the selected agency or customer FILER CODE channel. [destructive]
- `delete_qingdao_manifest` — Delete one or more Qingdao manifest declaration groups and return the declarations that HaiGuanJia could not delete. [destructive]
- `delete_shanghai_manifest` — Delete selected customs declarations from an existing Shanghai manifest. HaiGuanJia charges once per declaration, so Connector never retries this request automatically. [destructive]
- `get_ai_customs_intake_status` — Get the raw HaiGuanJia AI customs-intake status. Automatic wait semantics are unavailable because the official status enum is not documented.
- `get_export_customs_recognition_result` — Get the current export customs-recognition task state and structured or customs-XML result.
- `get_full_journey_tracking` — Get carrier full-journey data for a subscription previously created by the connected HaiGuanJia account. Use this as a fallback when a callback was not received.
- `get_import_customs_recognition_result` — Get the current import customs-recognition task state and structured or customs-XML result.
- `get_new_us_customs` — Get the complete new US customs result for a prior HaiGuanJia query, including BOL, air, importer-bond, and in-bond data when present.
- `get_ningbo_master_house_bills` — Resolve Ningbo master and house bill relationships without requiring the caller to identify whether the supplied bill is a master or house bill.
- `get_port_container` — Get current Ningbo, Shanghai, Shenzhen, or Qingdao container/cargo data. HaiGuanJia automatically subscribes missing data, so this operation may create a billed callback workflow and Connector never retries it automatically. [write]
- `get_port_schedule` — Get current Ningbo, Shanghai, Shenzhen, or Qingdao vessel schedule data. HaiGuanJia automatically subscribes missing or expired schedules, so Connector never retries this request automatically. [write]
- `get_qingdao_shipping_agent` — Get the Qingdao shipping agent for a bill, carrier, vessel, and voyage.
- `get_shanghai_manifest_deletion_status` — Get the receipt status for a Shanghai manifest deletion submitted through the connected HaiGuanJia account.
- `get_shanghai_manifest_status` — Get send receipts for a customs declaration submitted through the connected HaiGuanJia account.
- `get_shanghai_manifest_update_status` — Get the receipt status for a Shanghai manifest update submitted through the connected HaiGuanJia account.
- `get_shenzhen_nansha_schedule` — Query Shenzhen or Nansha vessel schedules using the selected product API ID and the shared official endpoint.
- `get_ship_position` — Get the latest HaiGuanJia position and identity data for a vessel.
- `list_shanghai_shipping_agents` — List candidate Shanghai shipping agent names for a bill, carrier, vessel, and voyage. HaiGuanJia documents the result as reference data only.
- `list_ship_track_points` — List HaiGuanJia track points for a previously subscribed vessel within a time range.
- `list_truck_track_points` — List a truck's historical track and parking events. Only query vehicles that the caller is authorized to track. HaiGuanJia documents this query as chargeable on every request.
- `reallocate_qingdao_manifest` — Reallocate a Qingdao manifest to another vessel and voyage. The official page has conflicting billing labels, so Connector treats it as potentially chargeable and never retries automatically. [destructive]
- `recognize_custom_document` — Recognize one or more documents with a promptCode maintained in HaiGuanJia's external Storybrooke console. This business-side billed request requires the connection's separate secondaryApiKey and is never retried automatically.
- `recognize_document` — Recognize one or more documents with a fixed HaiGuanJia product template. This business-side billed request requires the connection's separate secondaryApiKey and is never retried automatically.
- `resend_qingdao_manifest` — Resend the rejected original Qingdao manifest. Connector sends the operation once and never retries automatically. [write]
- `resend_shanghai_manifest` — Resend an original Shanghai manifest that HaiGuanJia has rejected. This endpoint only accepts the rejected original manifest and Connector never retries it automatically. [write]
- `send_aci_manifest` — Send an ACI manifest through agency filing or the customer's own 8000-code channel. Each house bill is chargeable and Connector never retries automatically. [write]
- `send_afr_manifest` — Send an AFR manifest. HaiGuanJia charges once per house bill, so Connector never retries automatically. [write]
- `send_ams_manifest` — Send an AMS manifest through HaiGuanJia agency service or the customer's own SCAC channel. Each house bill is chargeable and Connector never retries automatically. [write]
- `send_em_manifest` — Send an EM manifest through agency filing or the customer's own 8000-code channel. Each house bill is chargeable and Connector never retries automatically. [write]
- `send_ics2_manifest` — Send an ICS2 F14, F15, F16, or F17 manifest. HaiGuanJia bills the submission on the business side, so Connector never retries automatically. [write]
- `send_isf10_manifest` — Send an ISF-10 manifest through HaiGuanJia agency filing or the customer's own FILER CODE channel. Each AMS bill is chargeable and Connector never retries automatically. [write]
- `send_isf5_manifest` — Send an ISF-5 manifest through HaiGuanJia agency filing or the customer's own FILER CODE channel. Each AMS bill is chargeable and Connector never retries automatically. [write]
- `send_nansha_manifest` — Send a complete Nansha manifest. HaiGuanJia documents the request as chargeable, so Connector never retries automatically. [write]
- `send_qingdao_manifest` — Send a Qingdao manifest using HaiGuanJia coins. The request is chargeable and Connector never retries it automatically. [write]
- `send_shanghai_manifest` — Send a complete Shanghai port manifest through HaiGuanJia. HaiGuanJia charges once per customs declaration number, so Connector never retries this request automatically. [write]
- `send_shenzhen_manifest` — Send a complete Shenzhen manifest. HaiGuanJia documents the request as chargeable, so Connector never retries automatically. [write]
- `send_tianjin_manifest` — Send a complete Tianjin manifest including VGM and attachments. The workflow is chargeable, so Connector never retries automatically. [write]
- `send_tianjin_pickup_order` — Send a Tianjin pickup order. HaiGuanJia documents this sub-interface as free, but the required attachment URLs and all business data remain redacted from execution logs. [write]
- `send_vgm` — Send or resend multi-port VGM data. HaiGuanJia charges for every container on every call, including resends, so Connector never retries automatically. [write]
- `submit_ai_customs_intake` — Submit a new AI customs-intake request. Connector fixes isModify to false and HaiGuanJia fetches each attachment URL. [write]
- `submit_export_customs_recognition` — Submit a chargeable export customs-recognition task. HaiGuanJia fetches each fileUrl and Connector never retries automatically. [write]
- `submit_import_customs_recognition` — Submit a chargeable import customs-recognition task. HaiGuanJia fetches each fileUrl and Connector never retries automatically. [write]
- `subscribe_full_journey_tracking` — Subscribe a bill, booking/SO number, or container for HaiGuanJia carrier full-journey tracking. Subscription submission is free, but delivered callback data is billed per returned container, so Connector never retries this request automatically. [write]
- `subscribe_new_us_customs` — Submit a new US customs-data subscription. HaiGuanJia bills this workflow on the business side, so Connector never retries automatically. [write]
- `subscribe_port_container` — Subscribe Ningbo, Shanghai, Shenzhen, or Qingdao container/cargo data. Submission is free but callbacks are billed per returned bill or booking number, so Connector never retries automatically. [write]
- `subscribe_port_schedule` — Subscribe Ningbo, Shanghai, Shenzhen, or Qingdao vessel schedule data. Submission is free but callbacks are billed per returned vessel and voyage, subscriptions expire after 45 days, and Connector never retries automatically. [write]
- `subscribe_ship` — Subscribe a vessel in HaiGuanJia so its track information can be queried. [write]
- `subscribe_us_customs_data` — Subscribe US destination customs data for a bill and carrier. HaiGuanJia documents this request as chargeable, so Connector never retries automatically. [write]
- `subscribe_us_terminal_data` — Subscribe US terminal data for a container and port. HaiGuanJia documents this request as chargeable, so Connector never retries automatically. [write]
- `update_aci_manifest` — Overwrite an ACI manifest through the selected agency or customer channel. [destructive]
- `update_afr_manifest` — Overwrite an existing AFR house bill and its complete container data. [destructive]
- `update_ai_customs_intake` — Overwrite an existing AI customs-intake request. Connector fixes isModify to true and HaiGuanJia fetches each attachment URL. [destructive]
- `update_ams_manifest` — Overwrite an AMS manifest through the selected agency or customer SCAC channel. [destructive]
- `update_em_manifest` — Overwrite an EM manifest through the selected agency or customer channel. [destructive]
- `update_ics2_manifest` — Overwrite an ICS2 F14, F15, F16, or F17 manifest identified by billId. [destructive]
- `update_isf10_manifest` — Overwrite an ISF-10 manifest through the selected agency or customer FILER CODE channel. [destructive]
- `update_isf5_manifest` — Overwrite an ISF-5 manifest through the selected agency or customer FILER CODE channel. [destructive]
- `update_qingdao_manifest` — Overwrite a Qingdao manifest. HaiGuanJia charges for affected master and house bills, so Connector never retries automatically. [destructive]
- `update_shanghai_manifest` — Overwrite selected customs declarations in an existing Shanghai manifest. HaiGuanJia charges for each modified customs declaration, so Connector never retries this request automatically. [destructive]
- `validate_qingdao_voyage` — Validate a Qingdao vessel and voyage using the product API ID rather than the conflicting example ID.
- `validate_shanghai_voyage` — Validate a Shanghai vessel and voyage and return its port calls and current planned timing.
- `withdraw_qingdao_manifest` — Withdraw a rejected Qingdao manifest and request the documented refund. [destructive]
- `withdraw_shanghai_manifest` — Withdraw a rejected Shanghai manifest submission. A successful withdrawal refunds the documented balance or usage count. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change HaiGuanJia state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — HaiGuanJia is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/hgj
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- HaiGuanJia homepage: https://openapi.hgj.com/
- API documentation: https://openapi.hgj.com/
