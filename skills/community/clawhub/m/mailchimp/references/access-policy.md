# Mailchimp access policy

An access policy limits which endpoints Mailchimp connections may call through Maton. Mailchimp doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/mailchimp#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Mailchimp: its 154 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create mailchimp --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "3.0/account-exports"},
    {"method": "GET", "path": "3.0/account-exports/{id}"},
    {"method": "GET", "path": "3.0/activity-feed/chimp-chatter"},
    {"method": "GET", "path": "3.0/audiences"},
    {"method": "GET", "path": "3.0/audiences/{id}"},
    {"method": "GET", "path": "3.0/audiences/{id}/contacts"},
    {"method": "GET", "path": "3.0/audiences/{id}/contacts/{id}"},
    {"method": "GET", "path": "3.0/authorized-apps"},
    {"method": "GET", "path": "3.0/authorized-apps/{id}"},
    {"method": "GET", "path": "3.0/automations"},
    {"method": "GET", "path": "3.0/automations/{id}"},
    {"method": "GET", "path": "3.0/automations/{id}/emails"},
    {"method": "GET", "path": "3.0/automations/{id}/emails/{id}"},
    {"method": "GET", "path": "3.0/automations/{id}/emails/{id}/queue"},
    {"method": "GET", "path": "3.0/automations/{id}/emails/{id}/queue/{id}"},
    {"method": "GET", "path": "3.0/automations/{id}/removed-subscribers"},
    {"method": "GET", "path": "3.0/automations/{id}/removed-subscribers/{id}"},
    {"method": "GET", "path": "3.0/batch-webhooks"},
    {"method": "GET", "path": "3.0/batch-webhooks/{id}"},
    {"method": "GET", "path": "3.0/batches"},
    {"method": "GET", "path": "3.0/batches/{id}"},
    {"method": "GET", "path": "3.0/campaign-folders"},
    {"method": "GET", "path": "3.0/campaign-folders/{id}"},
    {"method": "GET", "path": "3.0/campaigns"},
    {"method": "GET", "path": "3.0/campaigns/{id}"},
    {"method": "GET", "path": "3.0/campaigns/{id}/content"},
    {"method": "GET", "path": "3.0/campaigns/{id}/feedback"},
    {"method": "GET", "path": "3.0/campaigns/{id}/feedback/{id}"},
    {"method": "GET", "path": "3.0/campaigns/{id}/send-checklist"},
    {"method": "GET", "path": "3.0/connected-sites"},
    {"method": "GET", "path": "3.0/connected-sites/{id}"},
    {"method": "GET", "path": "3.0/conversations"},
    {"method": "GET", "path": "3.0/conversations/{id}"},
    {"method": "GET", "path": "3.0/conversations/{id}/messages"},
    {"method": "GET", "path": "3.0/conversations/{id}/messages/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/orders"},
    {"method": "GET", "path": "3.0/ecommerce/stores"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/carts"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/carts/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/carts/{id}/lines"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/carts/{id}/lines/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/customers"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/customers/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/orders"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/orders/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/orders/{id}/lines"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/orders/{id}/lines/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/products"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/products/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/products/{id}/images"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/products/{id}/images/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/products/{id}/variants"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/products/{id}/variants/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/promo-rules"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/promo-rules/{id}"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/promo-rules/{id}/promo-codes"},
    {"method": "GET", "path": "3.0/ecommerce/stores/{id}/promo-rules/{id}/promo-codes/{id}"},
    {"method": "GET", "path": "3.0/facebook-ads"},
    {"method": "GET", "path": "3.0/facebook-ads/{id}"},
    {"method": "GET", "path": "3.0/file-manager/files"},
    {"method": "GET", "path": "3.0/file-manager/files/{id}"},
    {"method": "GET", "path": "3.0/file-manager/folders"},
    {"method": "GET", "path": "3.0/file-manager/folders/{id}"},
    {"method": "GET", "path": "3.0/file-manager/folders/{id}/files"},
    {"method": "GET", "path": "3.0/landing-pages"},
    {"method": "GET", "path": "3.0/landing-pages/{id}"},
    {"method": "GET", "path": "3.0/landing-pages/{id}/content"},
    {"method": "GET", "path": "3.0/lists"},
    {"method": "GET", "path": "3.0/lists/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/abuse-reports"},
    {"method": "GET", "path": "3.0/lists/{id}/abuse-reports/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/activity"},
    {"method": "GET", "path": "3.0/lists/{id}/clients"},
    {"method": "GET", "path": "3.0/lists/{id}/growth-history"},
    {"method": "GET", "path": "3.0/lists/{id}/growth-history/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/interest-categories"},
    {"method": "GET", "path": "3.0/lists/{id}/interest-categories/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/interest-categories/{id}/interests"},
    {"method": "GET", "path": "3.0/lists/{id}/interest-categories/{id}/interests/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/locations"},
    {"method": "GET", "path": "3.0/lists/{id}/members"},
    {"method": "GET", "path": "3.0/lists/{id}/members/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/members/{id}/activity"},
    {"method": "GET", "path": "3.0/lists/{id}/members/{id}/activity-feed"},
    {"method": "GET", "path": "3.0/lists/{id}/members/{id}/events"},
    {"method": "GET", "path": "3.0/lists/{id}/members/{id}/goals"},
    {"method": "GET", "path": "3.0/lists/{id}/members/{id}/notes"},
    {"method": "GET", "path": "3.0/lists/{id}/members/{id}/notes/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/members/{id}/tags"},
    {"method": "GET", "path": "3.0/lists/{id}/merge-fields"},
    {"method": "GET", "path": "3.0/lists/{id}/merge-fields/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/segments"},
    {"method": "GET", "path": "3.0/lists/{id}/segments/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/segments/{id}/members"},
    {"method": "GET", "path": "3.0/lists/{id}/signup-forms"},
    {"method": "GET", "path": "3.0/lists/{id}/surveys"},
    {"method": "GET", "path": "3.0/lists/{id}/surveys/{id}"},
    {"method": "GET", "path": "3.0/lists/{id}/tag-search"},
    {"method": "GET", "path": "3.0/lists/{id}/webhooks"},
    {"method": "GET", "path": "3.0/lists/{id}/webhooks/{id}"},
    {"method": "GET", "path": "3.0/ping"},
    {"method": "GET", "path": "3.0/reporting/facebook-ads"},
    {"method": "GET", "path": "3.0/reporting/facebook-ads/{id}"},
    {"method": "GET", "path": "3.0/reporting/facebook-ads/{id}/ecommerce-product-activity"},
    {"method": "GET", "path": "3.0/reporting/landing-pages"},
    {"method": "GET", "path": "3.0/reporting/landing-pages/{id}"},
    {"method": "GET", "path": "3.0/reporting/surveys"},
    {"method": "GET", "path": "3.0/reporting/surveys/{id}"},
    {"method": "GET", "path": "3.0/reporting/surveys/{id}/questions"},
    {"method": "GET", "path": "3.0/reporting/surveys/{id}/questions/{id}"},
    {"method": "GET", "path": "3.0/reporting/surveys/{id}/questions/{id}/answers"},
    {"method": "GET", "path": "3.0/reporting/surveys/{id}/responses"},
    {"method": "GET", "path": "3.0/reporting/surveys/{id}/responses/{id}"},
    {"method": "GET", "path": "3.0/reports"},
    {"method": "GET", "path": "3.0/reports/{id}"},
    {"method": "GET", "path": "3.0/reports/{id}/abuse-reports"},
    {"method": "GET", "path": "3.0/reports/{id}/abuse-reports/{id}"},
    {"method": "GET", "path": "3.0/reports/{id}/advice"},
    {"method": "GET", "path": "3.0/reports/{id}/click-details"},
    {"method": "GET", "path": "3.0/reports/{id}/click-details/{id}"},
    {"method": "GET", "path": "3.0/reports/{id}/click-details/{id}/members"},
    {"method": "GET", "path": "3.0/reports/{id}/click-details/{id}/members/{id}"},
    {"method": "GET", "path": "3.0/reports/{id}/domain-performance"},
    {"method": "GET", "path": "3.0/reports/{id}/ecommerce-product-activity"},
    {"method": "GET", "path": "3.0/reports/{id}/eepurl"},
    {"method": "GET", "path": "3.0/reports/{id}/email-activity"},
    {"method": "GET", "path": "3.0/reports/{id}/email-activity/{id}"},
    {"method": "GET", "path": "3.0/reports/{id}/locations"},
    {"method": "GET", "path": "3.0/reports/{id}/open-details"},
    {"method": "GET", "path": "3.0/reports/{id}/open-details/{id}"},
    {"method": "GET", "path": "3.0/reports/{id}/sent-to"},
    {"method": "GET", "path": "3.0/reports/{id}/sent-to/{id}"},
    {"method": "GET", "path": "3.0/reports/{id}/sub-reports"},
    {"method": "GET", "path": "3.0/reports/{id}/unsubscribed"},
    {"method": "GET", "path": "3.0/reports/{id}/unsubscribed/{id}"},
    {"method": "GET", "path": "3.0"},
    {"method": "GET", "path": "3.0/search-campaigns"},
    {"method": "GET", "path": "3.0/search-members"},
    {"method": "GET", "path": "3.0/segments"},
    {"method": "GET", "path": "3.0/segments/{id}"},
    {"method": "GET", "path": "3.0/segments/{id}/count"},
    {"method": "GET", "path": "3.0/segments/{id}/snapshots/{id}"},
    {"method": "GET", "path": "3.0/segments/{id}/snapshots/{id}/members"},
    {"method": "GET", "path": "3.0/sms-campaigns"},
    {"method": "GET", "path": "3.0/sms-campaigns/{id}"},
    {"method": "GET", "path": "3.0/sms-campaigns/{id}/content"},
    {"method": "GET", "path": "3.0/template-folders"},
    {"method": "GET", "path": "3.0/template-folders/{id}"},
    {"method": "GET", "path": "3.0/templates"},
    {"method": "GET", "path": "3.0/templates/{id}"},
    {"method": "GET", "path": "3.0/templates/{id}/default-content"},
    {"method": "GET", "path": "3.0/verified-domains"},
    {"method": "GET", "path": "3.0/verified-domains/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Mailchimp endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | 3.0/account-exports | read | account-exports | Get a list of account exports for a given account. |
| POST | 3.0/account-exports | write | account-exports | Create a new account export in your Mailchimp account. |
| GET | 3.0/account-exports/{id} | read | account-exports | Get information about a specific account export. |
| GET | 3.0/activity-feed/chimp-chatter | read | activity-feed | Return the Chimp Chatter for this account ordered by most recent. |
| GET | 3.0/audiences | read | audiences | Get information about all audiences in the account. |
| GET | 3.0/audiences/{id} | read | audiences | Get information about a specific audience. |
| GET | 3.0/audiences/{id}/contacts | read | audiences | Get a list of omni-channel contacts for a given audience. |
| POST | 3.0/audiences/{id}/contacts | write | audiences | Create a new omni-channel contact for an audience. |
| GET | 3.0/audiences/{id}/contacts/{id} | read | audiences | Retrieve a specific omni-channel contact in an audience. |
| PATCH | 3.0/audiences/{id}/contacts/{id} | write | audiences | Update an existing omni-channel contact. |
| POST | 3.0/audiences/{id}/contacts/{id}/actions/archive | write | audiences | Archives a Contact. |
| POST | 3.0/audiences/{id}/contacts/{id}/actions/forget | write | audiences | Forgets a Contact. |
| GET | 3.0/authorized-apps | read | authorized-apps | Get a list of an account's registered, connected applications. |
| GET | 3.0/authorized-apps/{id} | read | authorized-apps | Get information about a specific authorized application. |
| GET | 3.0/automations | read | automations | Get a summary of an account's classic automations. |
| POST | 3.0/automations | write | automations | Create a new classic automation in your Mailchimp account. |
| GET | 3.0/automations/{id} | read | automations | Get a summary of an individual classic automation workflow's settings and content. |
| POST | 3.0/automations/{id}/actions/archive | write | automations | Archiving will permanently end your automation and keep the report data. |
| POST | 3.0/automations/{id}/actions/pause-all-emails | write | automations | Pause all emails in a specific classic automation workflow. |
| POST | 3.0/automations/{id}/actions/start-all-emails | write | automations | Start all emails in a classic automation workflow. |
| GET | 3.0/automations/{id}/emails | read | automations | Get a summary of the emails in a classic automation workflow. |
| GET | 3.0/automations/{id}/emails/{id} | read | automations | Get information about an individual classic automation workflow email. |
| PATCH | 3.0/automations/{id}/emails/{id} | write | automations | Update settings for a classic automation workflow email. |
| DELETE | 3.0/automations/{id}/emails/{id} | write | automations | Removes an individual classic automation workflow email. |
| POST | 3.0/automations/{id}/emails/{id}/actions/pause | write | automations | Pause an automated email. |
| POST | 3.0/automations/{id}/emails/{id}/actions/start | write | automations | Start an automated email. |
| GET | 3.0/automations/{id}/emails/{id}/queue | read | automations | Get information about a classic automation email queue. |
| POST | 3.0/automations/{id}/emails/{id}/queue | write | automations | Manually add a subscriber to a workflow, bypassing the default trigger settings. |
| GET | 3.0/automations/{id}/emails/{id}/queue/{id} | read | automations | Get information about a specific subscriber in a classic automation email queue. |
| GET | 3.0/automations/{id}/removed-subscribers | read | automations | Get information about subscribers who were removed from a classic automation workflow. |
| POST | 3.0/automations/{id}/removed-subscribers | write | automations | Remove a subscriber from a specific classic automation workflow. |
| GET | 3.0/automations/{id}/removed-subscribers/{id} | read | automations | Get information about a specific subscriber who was removed from a classic automation workflow. |
| GET | 3.0/batch-webhooks | read | batch-webhooks | Get all webhooks that have been configured for batches. |
| POST | 3.0/batch-webhooks | write | batch-webhooks | Configure a webhook that will fire whenever any batch request completes processing. |
| GET | 3.0/batch-webhooks/{id} | read | batch-webhooks | Get information about a specific batch webhook. |
| PATCH | 3.0/batch-webhooks/{id} | write | batch-webhooks | Update a webhook that will fire whenever any batch request completes processing. |
| DELETE | 3.0/batch-webhooks/{id} | write | batch-webhooks | Remove a batch webhook. |
| GET | 3.0/batches | read | batches | Get a summary of batch requests that have been made. |
| POST | 3.0/batches | write | batches | Begin processing a batch operations request. |
| GET | 3.0/batches/{id} | read | batches | Get the status of a batch request. |
| DELETE | 3.0/batches/{id} | write | batches | Stops a batch request from running. |
| GET | 3.0/campaign-folders | read | campaign-folders | Get all folders used to organize campaigns. |
| POST | 3.0/campaign-folders | write | campaign-folders | Create a new campaign folder. |
| GET | 3.0/campaign-folders/{id} | read | campaign-folders | Get information about a specific folder used to organize campaigns. |
| PATCH | 3.0/campaign-folders/{id} | write | campaign-folders | Update a specific folder used to organize campaigns. |
| DELETE | 3.0/campaign-folders/{id} | write | campaign-folders | Delete a specific campaign folder, and mark all the campaigns in the folder as 'unfiled'. |
| GET | 3.0/campaigns | read | campaigns | Get all campaigns in an account. |
| POST | 3.0/campaigns | write | campaigns | Create a new Mailchimp campaign. |
| GET | 3.0/campaigns/{id} | read | campaigns | Get information about a specific campaign. |
| PATCH | 3.0/campaigns/{id} | write | campaigns | Update some or all of the settings for a specific campaign. |
| DELETE | 3.0/campaigns/{id} | write | campaigns | Remove a campaign from your Mailchimp account. |
| POST | 3.0/campaigns/{id}/actions/cancel-send | write | campaigns | Cancel a Regular or Plain-Text Campaign after you send, before all of your recipients receive it. |
| POST | 3.0/campaigns/{id}/actions/create-resend | write | campaigns | Remove the guesswork for resending a campaign to certain segments. |
| POST | 3.0/campaigns/{id}/actions/pause | write | campaigns | Pause an RSS-Driven campaign. |
| POST | 3.0/campaigns/{id}/actions/replicate | write | campaigns | Replicate a campaign in saved or send status. |
| POST | 3.0/campaigns/{id}/actions/resume | write | campaigns | Resume an RSS-Driven campaign. |
| POST | 3.0/campaigns/{id}/actions/schedule | write | campaigns | Schedule a campaign for delivery. |
| POST | 3.0/campaigns/{id}/actions/send | write | campaigns | Send a Mailchimp campaign. |
| POST | 3.0/campaigns/{id}/actions/test | write | campaigns | Send a test email. |
| POST | 3.0/campaigns/{id}/actions/unschedule | write | campaigns | Unschedule a scheduled campaign that hasn't started sending. |
| GET | 3.0/campaigns/{id}/content | read | campaigns | Get the the HTML and plain-text content for a campaign. |
| PUT | 3.0/campaigns/{id}/content | write | campaigns | Set the content for a campaign. |
| GET | 3.0/campaigns/{id}/feedback | read | campaigns | Get team feedback while you're working together on a Mailchimp campaign. |
| POST | 3.0/campaigns/{id}/feedback | write | campaigns | Add feedback on a specific campaign. |
| GET | 3.0/campaigns/{id}/feedback/{id} | read | campaigns | Get a specific feedback message from a campaign. |
| PATCH | 3.0/campaigns/{id}/feedback/{id} | write | campaigns | Update a specific feedback message for a campaign. |
| DELETE | 3.0/campaigns/{id}/feedback/{id} | write | campaigns | Remove a specific feedback message for a campaign. |
| GET | 3.0/campaigns/{id}/send-checklist | read | campaigns | Review the send checklist for a campaign, and resolve any issues before sending. |
| GET | 3.0/connected-sites | read | connected-sites | Get all connected sites in an account. |
| POST | 3.0/connected-sites | write | connected-sites | Create a new Mailchimp connected site. |
| GET | 3.0/connected-sites/{id} | read | connected-sites | Get information about a specific connected site. |
| DELETE | 3.0/connected-sites/{id} | write | connected-sites | Remove a connected site from your Mailchimp account. |
| POST | 3.0/connected-sites/{id}/actions/disable-pixel | write | connected-sites | Disable the Mailchimp tracking pixel for a connected site. |
| POST | 3.0/connected-sites/{id}/actions/enable-pixel | write | connected-sites | Enable the Mailchimp tracking pixel for a connected site. |
| POST | 3.0/connected-sites/{id}/actions/verify-script-installation | write | connected-sites | Verify that the connected sites script has been installed, either via the script URL or fragment. |
| GET | 3.0/conversations | read | conversations | Get a list of conversations for the account. |
| GET | 3.0/conversations/{id} | read | conversations | Get details about an individual conversation. |
| GET | 3.0/conversations/{id}/messages | read | conversations | Get messages from a specific conversation. |
| GET | 3.0/conversations/{id}/messages/{id} | read | conversations | Get an individual message in a conversation. |
| POST | 3.0/customer-journeys/journeys/{id}/steps/{id}/actions/trigger | write | customer-journeys | A step trigger in an Automation flow. |
| GET | 3.0/ecommerce/orders | read | ecommerce | Get information about an account's orders. |
| GET | 3.0/ecommerce/stores | read | ecommerce | Get information about all stores in the account. |
| POST | 3.0/ecommerce/stores | write | ecommerce | Add a new store to your Mailchimp account. |
| GET | 3.0/ecommerce/stores/{id} | read | ecommerce | Get information about a specific store. |
| PATCH | 3.0/ecommerce/stores/{id} | write | ecommerce | Update a store. |
| DELETE | 3.0/ecommerce/stores/{id} | write | ecommerce | Delete a store. |
| GET | 3.0/ecommerce/stores/{id}/carts | read | ecommerce | Get information about a store's carts. |
| POST | 3.0/ecommerce/stores/{id}/carts | write | ecommerce | Add a new cart to a store. |
| GET | 3.0/ecommerce/stores/{id}/carts/{id} | read | ecommerce | Get information about a specific cart. |
| PATCH | 3.0/ecommerce/stores/{id}/carts/{id} | write | ecommerce | Update a specific cart. |
| DELETE | 3.0/ecommerce/stores/{id}/carts/{id} | write | ecommerce | Delete a cart. |
| GET | 3.0/ecommerce/stores/{id}/carts/{id}/lines | read | ecommerce | Get information about a cart's line items. |
| POST | 3.0/ecommerce/stores/{id}/carts/{id}/lines | write | ecommerce | Add a new line item to an existing cart. |
| GET | 3.0/ecommerce/stores/{id}/carts/{id}/lines/{id} | read | ecommerce | Get information about a specific cart line item. |
| PATCH | 3.0/ecommerce/stores/{id}/carts/{id}/lines/{id} | write | ecommerce | Update a specific cart line item. |
| DELETE | 3.0/ecommerce/stores/{id}/carts/{id}/lines/{id} | write | ecommerce | Delete a specific cart line item. |
| GET | 3.0/ecommerce/stores/{id}/customers | read | ecommerce | Get information about a store's customers. |
| POST | 3.0/ecommerce/stores/{id}/customers | write | ecommerce | Add a new customer to a store. |
| GET | 3.0/ecommerce/stores/{id}/customers/{id} | read | ecommerce | Get information about a specific customer. |
| PUT | 3.0/ecommerce/stores/{id}/customers/{id} | write | ecommerce | Add or update a customer. |
| PATCH | 3.0/ecommerce/stores/{id}/customers/{id} | write | ecommerce | Update a customer. |
| DELETE | 3.0/ecommerce/stores/{id}/customers/{id} | write | ecommerce | Delete a customer from a store. |
| GET | 3.0/ecommerce/stores/{id}/orders | read | ecommerce | Get information about a store's orders. |
| POST | 3.0/ecommerce/stores/{id}/orders | write | ecommerce | Add a new order to a store. |
| GET | 3.0/ecommerce/stores/{id}/orders/{id} | read | ecommerce | Get information about a specific order. |
| PUT | 3.0/ecommerce/stores/{id}/orders/{id} | write | ecommerce | Add or update an order. |
| PATCH | 3.0/ecommerce/stores/{id}/orders/{id} | write | ecommerce | Update a specific order. |
| DELETE | 3.0/ecommerce/stores/{id}/orders/{id} | write | ecommerce | Delete an order. |
| GET | 3.0/ecommerce/stores/{id}/orders/{id}/lines | read | ecommerce | Get information about an order's line items. |
| POST | 3.0/ecommerce/stores/{id}/orders/{id}/lines | write | ecommerce | Add a new line item to an existing order. |
| GET | 3.0/ecommerce/stores/{id}/orders/{id}/lines/{id} | read | ecommerce | Get information about a specific order line item. |
| PATCH | 3.0/ecommerce/stores/{id}/orders/{id}/lines/{id} | write | ecommerce | Update a specific order line item. |
| DELETE | 3.0/ecommerce/stores/{id}/orders/{id}/lines/{id} | write | ecommerce | Delete a specific order line item. |
| GET | 3.0/ecommerce/stores/{id}/products | read | ecommerce | Get information about a store's products. |
| POST | 3.0/ecommerce/stores/{id}/products | write | ecommerce | Add a new product to a store. |
| GET | 3.0/ecommerce/stores/{id}/products/{id} | read | ecommerce | Get information about a specific product. |
| PUT | 3.0/ecommerce/stores/{id}/products/{id} | write | ecommerce | Update a specific product. |
| PATCH | 3.0/ecommerce/stores/{id}/products/{id} | write | ecommerce | Update a specific product. |
| DELETE | 3.0/ecommerce/stores/{id}/products/{id} | write | ecommerce | Delete a product. |
| GET | 3.0/ecommerce/stores/{id}/products/{id}/images | read | ecommerce | Get information about a product's images. |
| POST | 3.0/ecommerce/stores/{id}/products/{id}/images | write | ecommerce | Add a new image to the product. |
| GET | 3.0/ecommerce/stores/{id}/products/{id}/images/{id} | read | ecommerce | Get information about a specific product image. |
| PATCH | 3.0/ecommerce/stores/{id}/products/{id}/images/{id} | write | ecommerce | Update a product image. |
| DELETE | 3.0/ecommerce/stores/{id}/products/{id}/images/{id} | write | ecommerce | Delete a product image. |
| GET | 3.0/ecommerce/stores/{id}/products/{id}/variants | read | ecommerce | Get information about a product's variants. |
| POST | 3.0/ecommerce/stores/{id}/products/{id}/variants | write | ecommerce | Add a new variant to the product. |
| GET | 3.0/ecommerce/stores/{id}/products/{id}/variants/{id} | read | ecommerce | Get information about a specific product variant. |
| PUT | 3.0/ecommerce/stores/{id}/products/{id}/variants/{id} | write | ecommerce | Add or update a product variant. |
| PATCH | 3.0/ecommerce/stores/{id}/products/{id}/variants/{id} | write | ecommerce | Update a product variant. |
| DELETE | 3.0/ecommerce/stores/{id}/products/{id}/variants/{id} | write | ecommerce | Delete a product variant. |
| GET | 3.0/ecommerce/stores/{id}/promo-rules | read | ecommerce | Get information about a store's promo rules. |
| POST | 3.0/ecommerce/stores/{id}/promo-rules | write | ecommerce | Add a new promo rule to a store. |
| GET | 3.0/ecommerce/stores/{id}/promo-rules/{id} | read | ecommerce | Get information about a specific promo rule. |
| PATCH | 3.0/ecommerce/stores/{id}/promo-rules/{id} | write | ecommerce | Update a promo rule. |
| DELETE | 3.0/ecommerce/stores/{id}/promo-rules/{id} | write | ecommerce | Delete a promo rule from a store. |
| GET | 3.0/ecommerce/stores/{id}/promo-rules/{id}/promo-codes | read | ecommerce | Get information about a store's promo codes. |
| POST | 3.0/ecommerce/stores/{id}/promo-rules/{id}/promo-codes | write | ecommerce | Add a new promo code to a store. |
| GET | 3.0/ecommerce/stores/{id}/promo-rules/{id}/promo-codes/{id} | read | ecommerce | Get information about a specific promo code. |
| PATCH | 3.0/ecommerce/stores/{id}/promo-rules/{id}/promo-codes/{id} | write | ecommerce | Update a promo code. |
| DELETE | 3.0/ecommerce/stores/{id}/promo-rules/{id}/promo-codes/{id} | write | ecommerce | Delete a promo code from a store. |
| GET | 3.0/facebook-ads | read | facebook-ads | Get list of Facebook ads. |
| GET | 3.0/facebook-ads/{id} | read | facebook-ads | Get details of a Facebook ad. |
| GET | 3.0/file-manager/files | read | file-manager | Get a list of available images and files stored in the File Manager for the account. |
| POST | 3.0/file-manager/files | write | file-manager | Upload a new image or file to the File Manager. |
| GET | 3.0/file-manager/files/{id} | read | file-manager | Get information about a specific file in the File Manager. |
| PATCH | 3.0/file-manager/files/{id} | write | file-manager | Update a file in the File Manager. |
| DELETE | 3.0/file-manager/files/{id} | write | file-manager | Remove a specific file from the File Manager. |
| GET | 3.0/file-manager/folders | read | file-manager | Get a list of all folders in the File Manager. |
| POST | 3.0/file-manager/folders | write | file-manager | Create a new folder in the File Manager. |
| GET | 3.0/file-manager/folders/{id} | read | file-manager | Get information about a specific folder in the File Manager. |
| PATCH | 3.0/file-manager/folders/{id} | write | file-manager | Update a specific File Manager folder. |
| DELETE | 3.0/file-manager/folders/{id} | write | file-manager | Delete a specific folder in the File Manager. |
| GET | 3.0/file-manager/folders/{id}/files | read | file-manager | Get a list of available images and files stored in this folder. |
| GET | 3.0/landing-pages | read | landing-pages | Get all landing pages. |
| POST | 3.0/landing-pages | write | landing-pages | Create an unpublished and contentless Mailchimp landing page. |
| GET | 3.0/landing-pages/{id} | read | landing-pages | Get information about a specific page. |
| PATCH | 3.0/landing-pages/{id} | write | landing-pages | Update a landing page. |
| DELETE | 3.0/landing-pages/{id} | write | landing-pages | Delete a landing page. |
| POST | 3.0/landing-pages/{id}/actions/publish | write | landing-pages | Publish a landing page that is in draft, unpublished, or has been previously published and edited. |
| POST | 3.0/landing-pages/{id}/actions/unpublish | write | landing-pages | Unpublish a landing page that is in draft or has been published. |
| GET | 3.0/landing-pages/{id}/content | read | landing-pages | Get the the HTML for your landing page. |
| GET | 3.0/lists | read | lists | Get information about all lists in the account. |
| POST | 3.0/lists | write | lists | Create a new list in your Mailchimp account. |
| GET | 3.0/lists/{id} | read | lists | Get information about a specific list in your Mailchimp account. |
| POST | 3.0/lists/{id} | write | lists | Batch subscribe or unsubscribe list members. |
| PATCH | 3.0/lists/{id} | write | lists | Update the settings for a specific list. |
| DELETE | 3.0/lists/{id} | write | lists | Delete a list from your Mailchimp account. |
| GET | 3.0/lists/{id}/abuse-reports | read | lists | Get all abuse reports for a specific list. |
| GET | 3.0/lists/{id}/abuse-reports/{id} | read | lists | Get details about a specific abuse report. |
| GET | 3.0/lists/{id}/activity | read | lists | Get up to the previous 180 days of daily detailed aggregated activity stats for a list, not including Automation activity. |
| GET | 3.0/lists/{id}/clients | read | lists | Get a list of the top email clients based on user-agent strings. |
| GET | 3.0/lists/{id}/growth-history | read | lists | Get a month-by-month summary of a specific list's growth activity. |
| GET | 3.0/lists/{id}/growth-history/{id} | read | lists | Get a summary of a specific list's growth activity for a specific month and year. |
| GET | 3.0/lists/{id}/interest-categories | read | lists | Get information about a list's interest categories. |
| POST | 3.0/lists/{id}/interest-categories | write | lists | Create a new interest category. |
| GET | 3.0/lists/{id}/interest-categories/{id} | read | lists | Get information about a specific interest category. |
| PATCH | 3.0/lists/{id}/interest-categories/{id} | write | lists | Update a specific interest category. |
| DELETE | 3.0/lists/{id}/interest-categories/{id} | write | lists | Delete a specific interest category. |
| GET | 3.0/lists/{id}/interest-categories/{id}/interests | read | lists | Get a list of this category's interests. |
| POST | 3.0/lists/{id}/interest-categories/{id}/interests | write | lists | Create a new interest or 'group name' for a specific category. |
| GET | 3.0/lists/{id}/interest-categories/{id}/interests/{id} | read | lists | Get interests or 'group names' for a specific category. |
| PATCH | 3.0/lists/{id}/interest-categories/{id}/interests/{id} | write | lists | Update interests or 'group names' for a specific category. |
| DELETE | 3.0/lists/{id}/interest-categories/{id}/interests/{id} | write | lists | Delete interests or group names in a specific category. |
| GET | 3.0/lists/{id}/locations | read | lists | Get the locations (countries) that the list's subscribers have been tagged to based on geocoding their IP address. |
| GET | 3.0/lists/{id}/members | read | lists | Get information about members in a specific Mailchimp list. |
| POST | 3.0/lists/{id}/members | write | lists | Add a new member to the list. |
| GET | 3.0/lists/{id}/members/{id} | read | lists | Get information about a specific list member, including a currently subscribed, unsubscribed, or bounced member. |
| PUT | 3.0/lists/{id}/members/{id} | write | lists | Add or update a list member. |
| PATCH | 3.0/lists/{id}/members/{id} | write | lists | Update information for a specific list member. |
| DELETE | 3.0/lists/{id}/members/{id} | write | lists | Archive a list member. |
| POST | 3.0/lists/{id}/members/{id}/actions/delete-permanent | write | lists | Delete all personally identifiable information related to a list member, and remove them from a list. |
| GET | 3.0/lists/{id}/members/{id}/activity | read | lists | Get the last 50 events of a member's activity on a specific list, including opens, clicks, and unsubscribes. |
| GET | 3.0/lists/{id}/members/{id}/activity-feed | read | lists | Get a member's activity on a specific list, including opens, clicks, and unsubscribes. |
| GET | 3.0/lists/{id}/members/{id}/events | read | lists | Get events for a contact. |
| POST | 3.0/lists/{id}/members/{id}/events | write | lists | Add an event for a list member. |
| GET | 3.0/lists/{id}/members/{id}/goals | read | lists | Get the last 50 Goal events for a member on a specific list. |
| GET | 3.0/lists/{id}/members/{id}/notes | read | lists | Get recent notes for a specific list member. |
| POST | 3.0/lists/{id}/members/{id}/notes | write | lists | Add a new note for a specific subscriber. |
| GET | 3.0/lists/{id}/members/{id}/notes/{id} | read | lists | Get a specific note for a specific list member. |
| PATCH | 3.0/lists/{id}/members/{id}/notes/{id} | write | lists | Update a specific note for a specific list member. |
| DELETE | 3.0/lists/{id}/members/{id}/notes/{id} | write | lists | Delete a specific note for a specific list member. |
| GET | 3.0/lists/{id}/members/{id}/tags | read | lists | Get the tags on a list member. |
| POST | 3.0/lists/{id}/members/{id}/tags | write | lists | Add or remove tags from a list member. |
| GET | 3.0/lists/{id}/merge-fields | read | lists | Get a list of all merge fields for an audience. |
| POST | 3.0/lists/{id}/merge-fields | write | lists | Add a new merge field for a specific audience. |
| GET | 3.0/lists/{id}/merge-fields/{id} | read | lists | Get information about a specific merge field. |
| PATCH | 3.0/lists/{id}/merge-fields/{id} | write | lists | Update a specific merge field. |
| DELETE | 3.0/lists/{id}/merge-fields/{id} | write | lists | Delete a specific merge field. |
| GET | 3.0/lists/{id}/segments | read | lists | Get information about all available segments for a specific list. |
| POST | 3.0/lists/{id}/segments | write | lists | Create a new segment in a specific list. |
| GET | 3.0/lists/{id}/segments/{id} | read | lists | Get information about a specific segment. |
| POST | 3.0/lists/{id}/segments/{id} | write | lists | Batch add/remove list members to static segment. |
| PATCH | 3.0/lists/{id}/segments/{id} | write | lists | Update a specific segment in a list. |
| DELETE | 3.0/lists/{id}/segments/{id} | write | lists | Delete a specific segment in a list. |
| GET | 3.0/lists/{id}/segments/{id}/members | read | lists | Get information about members in a saved segment. |
| POST | 3.0/lists/{id}/segments/{id}/members | write | lists | Add a member to a static segment. |
| DELETE | 3.0/lists/{id}/segments/{id}/members/{id} | write | lists | Remove a member from the specified static segment. |
| GET | 3.0/lists/{id}/signup-forms | read | lists | Get signup forms for a specific list. |
| POST | 3.0/lists/{id}/signup-forms | write | lists | Customize a list's default signup form. |
| GET | 3.0/lists/{id}/surveys | read | lists | Get information about all available surveys for a specific list. |
| POST | 3.0/lists/{id}/surveys | write | lists | Create a draft survey for an audience. |
| GET | 3.0/lists/{id}/surveys/{id} | read | lists | Get details about a specific survey. |
| PATCH | 3.0/lists/{id}/surveys/{id} | write | lists | Update a survey. |
| DELETE | 3.0/lists/{id}/surveys/{id} | write | lists | Delete a survey. |
| POST | 3.0/lists/{id}/surveys/{id}/actions/create-email | write | lists | Utilize the List ID and Survey ID to generate a Campaign that links to your survey. |
| POST | 3.0/lists/{id}/surveys/{id}/actions/publish | write | lists | Publish a survey that is in draft, unpublished, or has been previously published and edited. |
| POST | 3.0/lists/{id}/surveys/{id}/actions/replicate | write | lists | Replicate a survey. |
| POST | 3.0/lists/{id}/surveys/{id}/actions/unpublish | write | lists | Unpublish a survey that has been published. |
| GET | 3.0/lists/{id}/tag-search | read | lists | Search for tags on a list by name. |
| GET | 3.0/lists/{id}/webhooks | read | lists | Get information about all webhooks for a specific list. |
| POST | 3.0/lists/{id}/webhooks | write | lists | Create a new webhook for a specific list. |
| GET | 3.0/lists/{id}/webhooks/{id} | read | lists | Get information about a specific webhook. |
| PATCH | 3.0/lists/{id}/webhooks/{id} | write | lists | Update the settings for an existing webhook. |
| DELETE | 3.0/lists/{id}/webhooks/{id} | write | lists | Delete a specific webhook in a list. |
| GET | 3.0/ping | read | ping | A health check for the API that won't return any account-specific information. |
| GET | 3.0/reporting/facebook-ads | read | reporting | Get reports of Facebook ads. |
| GET | 3.0/reporting/facebook-ads/{id} | read | reporting | Get report of a Facebook ad. |
| GET | 3.0/reporting/facebook-ads/{id}/ecommerce-product-activity | read | reporting | Get breakdown of product activity for an outreach. |
| GET | 3.0/reporting/landing-pages | read | reporting | Get reports of landing pages. |
| GET | 3.0/reporting/landing-pages/{id} | read | reporting | Get report of a landing page. |
| GET | 3.0/reporting/surveys | read | reporting | Get reports for surveys. |
| GET | 3.0/reporting/surveys/{id} | read | reporting | Get report for a survey. |
| GET | 3.0/reporting/surveys/{id}/questions | read | reporting | Get reports for survey questions. |
| GET | 3.0/reporting/surveys/{id}/questions/{id} | read | reporting | Get report for a survey question. |
| GET | 3.0/reporting/surveys/{id}/questions/{id}/answers | read | reporting | Get answers for a survey question. |
| GET | 3.0/reporting/surveys/{id}/responses | read | reporting | Get responses to a survey. |
| GET | 3.0/reporting/surveys/{id}/responses/{id} | read | reporting | Get a single survey response. |
| GET | 3.0/reports | read | reports | Get campaign reports. |
| GET | 3.0/reports/{id} | read | reports | Get report details for a specific sent campaign. |
| GET | 3.0/reports/{id}/abuse-reports | read | reports | Get a list of abuse complaints for a specific campaign. |
| GET | 3.0/reports/{id}/abuse-reports/{id} | read | reports | Get information about a specific abuse report for a campaign. |
| GET | 3.0/reports/{id}/advice | read | reports | Get feedback based on a campaign's statistics. |
| GET | 3.0/reports/{id}/click-details | read | reports | Get information about clicks on specific links in your Mailchimp campaigns. |
| GET | 3.0/reports/{id}/click-details/{id} | read | reports | Get click details for a specific link in a campaign. |
| GET | 3.0/reports/{id}/click-details/{id}/members | read | reports | Get information about list members who clicked on a specific link in a campaign. |
| GET | 3.0/reports/{id}/click-details/{id}/members/{id} | read | reports | Get information about a specific subscriber who clicked a link in a specific campaign. |
| GET | 3.0/reports/{id}/domain-performance | read | reports | Get statistics for the top-performing email domains in a campaign. |
| GET | 3.0/reports/{id}/ecommerce-product-activity | read | reports | Get breakdown of product activity for a campaign. |
| GET | 3.0/reports/{id}/eepurl | read | reports | Get a summary of social activity for the campaign, tracked by EepURL. |
| GET | 3.0/reports/{id}/email-activity | read | reports | Get a list of member's subscriber activity in a specific campaign. |
| GET | 3.0/reports/{id}/email-activity/{id} | read | reports | Get a specific list member's activity in a campaign including opens, clicks, and bounces. |
| GET | 3.0/reports/{id}/locations | read | reports | Get top open locations for a specific campaign. |
| GET | 3.0/reports/{id}/open-details | read | reports | Get detailed information about any campaign emails that were opened by a list member. |
| GET | 3.0/reports/{id}/open-details/{id} | read | reports | Get information about a specific subscriber who opened a campaign. |
| GET | 3.0/reports/{id}/sent-to | read | reports | Get information about campaign recipients. |
| GET | 3.0/reports/{id}/sent-to/{id} | read | reports | Get information about a specific campaign recipient. |
| GET | 3.0/reports/{id}/sub-reports | read | reports | Get a list of reports with child campaigns for a specific parent campaign. |
| GET | 3.0/reports/{id}/unsubscribed | read | reports | Get information about members who have unsubscribed from a specific campaign. |
| GET | 3.0/reports/{id}/unsubscribed/{id} | read | reports | Get information about a specific list member who unsubscribed from a campaign. |
| GET | 3.0 | read | root | Get links to all other resources available in the API. |
| GET | 3.0/search-campaigns | read | search-campaigns | Search all campaigns for the specified query terms. |
| GET | 3.0/search-members | read | search-members | Search for list members. |
| GET | 3.0/segments | read | segments | Get the segments of a list. |
| POST | 3.0/segments | write | segments | Create an advanced segment from a segment definition. |
| GET | 3.0/segments/{id} | read | segments | Get the metadata of a segment. |
| PATCH | 3.0/segments/{id} | write | segments | Update the name, the definition, or both of an advanced segment. |
| DELETE | 3.0/segments/{id} | write | segments | Delete an advanced segment. |
| GET | 3.0/segments/{id}/count | read | segments | Get the current number of members in a segment. |
| POST | 3.0/segments/{id}/snapshots | write | segments | Start a snapshot of the members of a segment. |
| GET | 3.0/segments/{id}/snapshots/{id} | read | segments | Get the status of a segment snapshot. |
| GET | 3.0/segments/{id}/snapshots/{id}/members | read | segments | Get the contact IDs of the members in a segment snapshot, one page at a time. |
| GET | 3.0/sms-campaigns | read | sms-campaigns | Get all SMS campaigns in an account. |
| POST | 3.0/sms-campaigns | write | sms-campaigns | Create a new SMS campaign. |
| GET | 3.0/sms-campaigns/{id} | read | sms-campaigns | Get information about a specific SMS campaign. |
| PATCH | 3.0/sms-campaigns/{id} | write | sms-campaigns | Update some or all of the settings for a specific SMS campaign. |
| DELETE | 3.0/sms-campaigns/{id} | write | sms-campaigns | Remove an SMS campaign from your Mailchimp account. |
| POST | 3.0/sms-campaigns/{id}/actions/cancel-send | write | sms-campaigns | Cancel a scheduled or sending SMS campaign. |
| POST | 3.0/sms-campaigns/{id}/actions/schedule | write | sms-campaigns | Schedule an SMS campaign to send at a specific time. |
| POST | 3.0/sms-campaigns/{id}/actions/send | write | sms-campaigns | Send an SMS campaign. |
| GET | 3.0/sms-campaigns/{id}/content | read | sms-campaigns | Get the content for an SMS campaign. |
| PUT | 3.0/sms-campaigns/{id}/content | write | sms-campaigns | Set the content for an SMS campaign. |
| GET | 3.0/template-folders | read | template-folders | Get all folders used to organize templates. |
| POST | 3.0/template-folders | write | template-folders | Create a new template folder. |
| GET | 3.0/template-folders/{id} | read | template-folders | Get information about a specific folder used to organize templates. |
| PATCH | 3.0/template-folders/{id} | write | template-folders | Update a specific folder used to organize templates. |
| DELETE | 3.0/template-folders/{id} | write | template-folders | Delete a specific template folder, and mark all the templates in the folder as 'unfiled'. |
| GET | 3.0/templates | read | templates | Get a list of an account's available templates. |
| POST | 3.0/templates | write | templates | Create a new template for the account. |
| GET | 3.0/templates/{id} | read | templates | Get information about a specific template. |
| PATCH | 3.0/templates/{id} | write | templates | Update the name, HTML, or `folder_id` of an existing template. |
| DELETE | 3.0/templates/{id} | write | templates | Delete a specific template. |
| GET | 3.0/templates/{id}/default-content | read | templates | Get the sections that you can edit in a template, including each section's default content. |
| GET | 3.0/verified-domains | read | verified-domains | Get all of the sending domains on the account. |
| POST | 3.0/verified-domains | write | verified-domains | Add a domain to the account. |
| GET | 3.0/verified-domains/{id} | read | verified-domains | Get the details for a single domain on the account. |
| DELETE | 3.0/verified-domains/{id} | write | verified-domains | Delete a verified domain from the account. |
| POST | 3.0/verified-domains/{id}/actions/verify | write | verified-domains | Verify a domain for sending. |
