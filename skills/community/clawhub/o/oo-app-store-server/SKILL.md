---
name: oo-app-store-server
description: "App Store Server API (developer.apple.com). Use this skill for ANY App Store Server API request — reading, creating, updating, and deleting data. Whenever a task involves App Store Server API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "App Store Server API"
  author: "OOMOL"
  version: "1.0.5"
  services: ["app_store_server"]
  icon: "https://static.oomol.com/logo/third-party/app_store_server.svg"
---

# App Store Server API

Operate **App Store Server API** through your OOMOL-connected account. This skill calls the `app_store_server` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected App Store Server API. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "app_store_server" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "app_store_server" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `configure_default_retention_message` — Set the default retention message the App Store shows for one subscription product in one locale, replacing any default configured before. Only text-based messages, with or without an image, can be defaults, and both the message and its image must be APPROVED. Products without a default in a locale show no retention message there, and the default is also the fallback when your real-time endpoint fails. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [destructive]
- `configure_retention_realtime_url` — Register the URL of your Get Retention Message endpoint for the environment of this connection, replacing any URL registered before. Once set, the App Store calls it whenever a subscriber opens the cancellation flow and shows the message you pick. A production URL is accepted only after your endpoint passed the sandbox performance test (Apple answers 403 otherwise). Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [destructive]
- `delete_default_retention_message` — Remove the default retention message of one subscription product in one locale, so the App Store shows no retention message there. Succeeds even when no default was configured. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [destructive]
- `delete_retention_image` — Delete an uploaded retention image. Apple refuses with 403 while a message still references the image, so delete the message first; a missing image answers 404. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [destructive]
- `delete_retention_message` — Delete an uploaded retention message. A missing message answers 404. Stop returning the identifier from your Get Retention Message endpoint first, and delete any image it used afterwards with delete_retention_image. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [destructive]
- `delete_retention_realtime_url` — Unregister the Get Retention Message endpoint URL for the environment of this connection. Afterwards the App Store shows only default messages in that environment until a URL is registered again. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [destructive]
- `extend_renewal_date_for_all_active_subscribers` — Extend the renewal date of every active subscription to one product, optionally limited to some storefronts. The App Store processes the request asynchronously; poll get_subscription_renewal_date_extension_status for the outcome. The extension cannot be reversed. [destructive]
- `extend_subscription_renewal_date` — Extend the renewal date of one customer's active auto-renewable subscription, to compensate for a service outage or a cancelled event. The extension cannot be reversed, and Apple emails the customer about the new renewal date. [destructive]
- `finish_transaction` — Tell the App Store that your server finished delivering the content for a transaction. Call it only after the customer has the content; it cannot be undone. Apple still returns a finished transaction from get_transaction_history, so do not treat its disappearance as confirmation. [destructive]
- `get_all_subscription_statuses` — Read the status of every auto-renewable subscription a customer has for your app, grouped by subscription group, with the latest transaction and renewal information of each decoded from the signed payloads Apple returns.
- `get_app_transaction_info` — Read the app download transaction for a customer, decoded from the signed payload Apple returns. It records when and on which platform the customer first acquired the app.
- `get_default_retention_message` — Read which message is configured as the default retention message for one subscription product in one locale. Returns a null messageIdentifier when no default is configured there. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body.
- `get_notification_history` — List the App Store Server Notifications the App Store tried to deliver to your server in a time span, with each notification payload decoded. History covers the past 180 days in production and the past 30 days in sandbox, and returns up to 20 records per page.
- `get_refund_history` — List the in-app purchase transactions the App Store refunded for a customer in your app, newest first, decoded from the signed payloads Apple returns. Returns up to 20 transactions per page.
- `get_retention_image_list` — List every image uploaded for retention messaging in this app and environment, with its size slot and approval state. Only images and messages in the APPROVED state are shown to customers; the sandbox approves uploads immediately. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body.
- `get_retention_message_list` — List every message uploaded for retention messaging in this app and environment, with its approval state. A message that carries an image also needs that image to be APPROVED; check it with get_retention_image_list. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body.
- `get_retention_performance_test_results` — Read the outcome of a sandbox performance test started with initiate_retention_performance_test: PENDING while it runs, then PASS or FAIL together with the measured response times, success rate and failure counts. Available only on a connection whose environment is sandbox; Apple serves the performance test endpoints on the sandbox host alone. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body.
- `get_retention_realtime_url` — Read the URL of the Get Retention Message endpoint registered for the environment of this connection. Returns a null realtimeUrl when none is registered. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body.
- `get_subscription_renewal_date_extension_status` — Check how far the App Store has got with a renewal date extension that was requested for all active subscribers of a product.
- `get_test_notification_status` — Read the delivery result of a test notification, with the notification payload decoded from the signed payload Apple returns. Apple answers 404 until it has finished the first delivery attempt.
- `get_transaction_history` — List a customer's in-app purchase transactions for your app, oldest first by default, decoded from the signed payloads Apple returns. Pass sort DESCENDING to get the most recent transactions first. Returns up to 20 transactions per page.
- `get_transaction_info` — Read one in-app purchase transaction by identifier, decoded from the signed payload Apple returns.
- `initiate_retention_performance_test` — Start Apple's performance test of the Get Retention Message endpoint registered in the sandbox, using an active sandbox subscription as the sample purchase. Passing the test is required before configure_retention_realtime_url accepts a production URL. Returns the request identifier and the test parameters; the test runs for the returned totalDuration. Available only on a connection whose environment is sandbox; Apple serves the performance test endpoints on the sandbox host alone. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [write]
- `look_up_order_id` — Look up the in-app purchase transactions behind an order ID from a customer's App Store receipt, to check that the order is genuine and belongs to your app. Apple serves this endpoint only in the production environment, so it fails on a sandbox connection.
- `request_test_notification` — Ask the App Store to send a TEST notification to the App Store Server Notifications URL configured for your app, and get back the token that identifies the attempt. Fails when no notification URL is configured for the selected environment. [write]
- `send_consumption_information` — Send consumption information for an in-app purchase after a CONSUMPTION_REQUEST notification, so the App Store can decide on the customer's refund request. Apple expects an answer within 12 hours of the notification. Use this for App Store in-app purchases that do not go through the Advanced Commerce API. [write]
- `send_consumption_information_v1` — Send the version 1 consumption information for an in-app purchase after a CONSUMPTION_REQUEST notification. Apple documents this shape for purchases made through the Advanced Commerce API; use send_consumption_information for ordinary App Store in-app purchases. [write]
- `set_app_account_token` — Set or replace the app account token on a transaction, to associate a purchase made outside your app with a customer on your own service. Overwrites any token already set. [destructive]
- `upload_retention_image` — Upload a PNG image for retention messages, either a FULL_SIZE image shown above the message body or a BULLET_POINT icon. The image starts in the PENDING state and Apple reviews it before it can be displayed; check the state with get_retention_image_list. Each app can hold up to 2000 images and an identifier can be uploaded only once. Only images and messages in the APPROVED state are shown to customers; the sandbox approves uploads immediately. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [write]
- `upload_retention_message` — Upload the text of a retention message: a header, a body, optionally a full-size image and bullet points with icons. The message starts in the PENDING state and Apple reviews it; check the state with get_retention_message_list. Leave out image and bulletPoints for messages you will use as switch-plan or promotional-offer messages. Each app can hold up to 2000 messages and an identifier can be uploaded only once. Only images and messages in the APPROVED state are shown to customers; the sandbox approves uploads immediately. Apple grants Retention Messaging API access per developer account; without it these endpoints answer 404 with no error body. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change App Store Server API state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — App Store Server API is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/app_store_server
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- App Store Server API homepage: https://developer.apple.com/documentation/appstoreserverapi
- API documentation: https://developer.apple.com/documentation/appstoreserverapi
