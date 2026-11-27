# Klaviyo access policy

An access policy limits which endpoints Klaviyo connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/klaviyo#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Klaviyo: its 265 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create klaviyo --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/accounts"},
    {"method": "GET", "path": "api/accounts/{id}"},
    {"method": "GET", "path": "api/billing-usage"},
    {"method": "GET", "path": "api/billing-usage/{id}"},
    {"method": "GET", "path": "api/brand-buttons"},
    {"method": "GET", "path": "api/brand-buttons/{id}"},
    {"method": "GET", "path": "api/brand-colors"},
    {"method": "GET", "path": "api/brand-colors/{id}"},
    {"method": "GET", "path": "api/brand-email-defaults"},
    {"method": "GET", "path": "api/brand-email-defaults/{id}"},
    {"method": "GET", "path": "api/brand-logos"},
    {"method": "GET", "path": "api/brand-logos/{id}"},
    {"method": "GET", "path": "api/brand-social-groups"},
    {"method": "GET", "path": "api/brand-social-groups/{id}"},
    {"method": "GET", "path": "api/brand-voice/{id}"},
    {"method": "GET", "path": "api/campaign-audiences/{id}"},
    {"method": "GET", "path": "api/campaign-audiences/{id}/campaign"},
    {"method": "GET", "path": "api/campaign-audiences/{id}/campaign-messages"},
    {"method": "GET", "path": "api/campaign-audiences/{id}/relationships/campaign"},
    {"method": "GET", "path": "api/campaign-audiences/{id}/relationships/campaign-messages"},
    {"method": "GET", "path": "api/campaign-messages"},
    {"method": "GET", "path": "api/campaign-messages/{id}"},
    {"method": "GET", "path": "api/campaign-messages/{id}/campaign"},
    {"method": "GET", "path": "api/campaign-messages/{id}/campaign-audience"},
    {"method": "GET", "path": "api/campaign-messages/{id}/campaign-variations"},
    {"method": "GET", "path": "api/campaign-messages/{id}/image"},
    {"method": "GET", "path": "api/campaign-messages/{id}/relationships/campaign"},
    {"method": "GET", "path": "api/campaign-messages/{id}/relationships/campaign-audience"},
    {"method": "GET", "path": "api/campaign-messages/{id}/relationships/campaign-variations"},
    {"method": "GET", "path": "api/campaign-messages/{id}/relationships/image"},
    {"method": "GET", "path": "api/campaign-messages/{id}/relationships/tags"},
    {"method": "GET", "path": "api/campaign-messages/{id}/relationships/template"},
    {"method": "GET", "path": "api/campaign-messages/{id}/tags"},
    {"method": "GET", "path": "api/campaign-messages/{id}/template"},
    {"method": "GET", "path": "api/campaign-recipient-estimation-jobs/{id}"},
    {"method": "GET", "path": "api/campaign-recipient-estimations/{id}"},
    {"method": "GET", "path": "api/campaign-send-jobs/{id}"},
    {"method": "GET", "path": "api/campaign-variations/{id}"},
    {"method": "GET", "path": "api/campaign-variations/{id}/campaign-message"},
    {"method": "GET", "path": "api/campaign-variations/{id}/image"},
    {"method": "GET", "path": "api/campaign-variations/{id}/relationships/campaign-message"},
    {"method": "GET", "path": "api/campaign-variations/{id}/relationships/image"},
    {"method": "GET", "path": "api/campaign-variations/{id}/relationships/translation"},
    {"method": "GET", "path": "api/campaign-variations/{id}/translation"},
    {"method": "GET", "path": "api/campaigns"},
    {"method": "GET", "path": "api/campaigns/{id}"},
    {"method": "GET", "path": "api/campaigns/{id}/campaign-audiences"},
    {"method": "GET", "path": "api/campaigns/{id}/campaign-messages"},
    {"method": "GET", "path": "api/campaigns/{id}/relationships/campaign-audiences"},
    {"method": "GET", "path": "api/campaigns/{id}/relationships/campaign-messages"},
    {"method": "GET", "path": "api/campaigns/{id}/relationships/tags"},
    {"method": "GET", "path": "api/campaigns/{id}/tags"},
    {"method": "GET", "path": "api/catalog-categories"},
    {"method": "GET", "path": "api/catalog-categories/{id}"},
    {"method": "GET", "path": "api/catalog-categories/{id}/items"},
    {"method": "GET", "path": "api/catalog-categories/{id}/relationships/items"},
    {"method": "GET", "path": "api/catalog-category-bulk-create-jobs"},
    {"method": "GET", "path": "api/catalog-category-bulk-create-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-category-bulk-delete-jobs"},
    {"method": "GET", "path": "api/catalog-category-bulk-delete-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-category-bulk-update-jobs"},
    {"method": "GET", "path": "api/catalog-category-bulk-update-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-item-bulk-create-jobs"},
    {"method": "GET", "path": "api/catalog-item-bulk-create-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-item-bulk-delete-jobs"},
    {"method": "GET", "path": "api/catalog-item-bulk-delete-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-item-bulk-update-jobs"},
    {"method": "GET", "path": "api/catalog-item-bulk-update-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-items"},
    {"method": "GET", "path": "api/catalog-items/{id}"},
    {"method": "GET", "path": "api/catalog-items/{id}/categories"},
    {"method": "GET", "path": "api/catalog-items/{id}/relationships/categories"},
    {"method": "GET", "path": "api/catalog-items/{id}/relationships/variants"},
    {"method": "GET", "path": "api/catalog-items/{id}/variants"},
    {"method": "GET", "path": "api/catalog-variant-bulk-create-jobs"},
    {"method": "GET", "path": "api/catalog-variant-bulk-create-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-variant-bulk-delete-jobs"},
    {"method": "GET", "path": "api/catalog-variant-bulk-delete-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-variant-bulk-update-jobs"},
    {"method": "GET", "path": "api/catalog-variant-bulk-update-jobs/{id}"},
    {"method": "GET", "path": "api/catalog-variants"},
    {"method": "GET", "path": "api/catalog-variants/{id}"},
    {"method": "GET", "path": "client/geofences"},
    {"method": "GET", "path": "client/ip-allowlists/{id}"},
    {"method": "GET", "path": "client/review-values-reports"},
    {"method": "GET", "path": "client/reviews"},
    {"method": "GET", "path": "api/coupon-code-bulk-create-jobs"},
    {"method": "GET", "path": "api/coupon-code-bulk-create-jobs/{id}"},
    {"method": "GET", "path": "api/coupon-codes"},
    {"method": "GET", "path": "api/coupon-codes/{id}"},
    {"method": "GET", "path": "api/coupon-codes/{id}/coupon"},
    {"method": "GET", "path": "api/coupon-codes/{id}/relationships/coupon"},
    {"method": "GET", "path": "api/coupons"},
    {"method": "GET", "path": "api/coupons/{id}"},
    {"method": "GET", "path": "api/coupons/{id}/coupon-codes"},
    {"method": "GET", "path": "api/coupons/{id}/relationships/coupon-codes"},
    {"method": "GET", "path": "api/data-sources"},
    {"method": "GET", "path": "api/data-sources/{id}"},
    {"method": "GET", "path": "api/object-records/{id}"},
    {"method": "GET", "path": "api/object-schemas/{id}"},
    {"method": "GET", "path": "api/object-schemas/{id}/relationships/object-schemas"},
    {"method": "GET", "path": "api/object-schemas/{id}/relationships/profile-object-schemas"},
    {"method": "GET", "path": "api/object-schemas/{id}/relationships/source-mapping"},
    {"method": "GET", "path": "api/object-schemas/{id}/source-mapping"},
    {"method": "GET", "path": "api/object-types"},
    {"method": "GET", "path": "api/object-types/{id}"},
    {"method": "GET", "path": "api/object-types/{id}/current-schema"},
    {"method": "GET", "path": "api/object-types/{id}/draft-schema"},
    {"method": "GET", "path": "api/object-types/{id}/object-ingestion-logs"},
    {"method": "GET", "path": "api/object-types/{id}/object-records"},
    {"method": "GET", "path": "api/object-types/{id}/relationships/current-schema"},
    {"method": "GET", "path": "api/object-types/{id}/relationships/draft-schema"},
    {"method": "GET", "path": "api/object-types/{id}/relationships/object-ingestion-logs"},
    {"method": "GET", "path": "api/object-types/{id}/relationships/object-records"},
    {"method": "GET", "path": "api/object-types/{id}/relationships/object-types"},
    {"method": "GET", "path": "api/object-types/{id}/relationships/profile-object-types"},
    {"method": "GET", "path": "api/object-types/{id}/relationships/schema-versions"},
    {"method": "GET", "path": "api/object-types/{id}/schema-versions"},
    {"method": "GET", "path": "api/source-mappings/{id}"},
    {"method": "GET", "path": "api/events"},
    {"method": "GET", "path": "api/events/{id}"},
    {"method": "GET", "path": "api/events/{id}/metric"},
    {"method": "GET", "path": "api/events/{id}/profile"},
    {"method": "GET", "path": "api/events/{id}/relationships/metric"},
    {"method": "GET", "path": "api/events/{id}/relationships/profile"},
    {"method": "GET", "path": "api/flow-actions/{id}"},
    {"method": "GET", "path": "api/flow-actions/{id}/flow"},
    {"method": "GET", "path": "api/flow-actions/{id}/flow-messages"},
    {"method": "GET", "path": "api/flow-actions/{id}/relationships/flow"},
    {"method": "GET", "path": "api/flow-actions/{id}/relationships/flow-messages"},
    {"method": "GET", "path": "api/flow-messages/{id}"},
    {"method": "GET", "path": "api/flow-messages/{id}/flow-action"},
    {"method": "GET", "path": "api/flow-messages/{id}/relationships/flow-action"},
    {"method": "GET", "path": "api/flow-messages/{id}/relationships/template"},
    {"method": "GET", "path": "api/flow-messages/{id}/template"},
    {"method": "GET", "path": "api/flows"},
    {"method": "GET", "path": "api/flows/{id}"},
    {"method": "GET", "path": "api/flows/{id}/flow-actions"},
    {"method": "GET", "path": "api/flows/{id}/relationships/flow-actions"},
    {"method": "GET", "path": "api/flows/{id}/relationships/tags"},
    {"method": "GET", "path": "api/flows/{id}/tags"},
    {"method": "GET", "path": "api/form-versions/{id}"},
    {"method": "GET", "path": "api/form-versions/{id}/form"},
    {"method": "GET", "path": "api/form-versions/{id}/relationships/form"},
    {"method": "GET", "path": "api/forms"},
    {"method": "GET", "path": "api/forms/{id}"},
    {"method": "GET", "path": "api/forms/{id}/form-versions"},
    {"method": "GET", "path": "api/forms/{id}/relationships/form-versions"},
    {"method": "GET", "path": "api/images"},
    {"method": "GET", "path": "api/images/{id}"},
    {"method": "GET", "path": "api/lists"},
    {"method": "GET", "path": "api/lists/{id}"},
    {"method": "GET", "path": "api/lists/{id}/flow-triggers"},
    {"method": "GET", "path": "api/lists/{id}/profiles"},
    {"method": "GET", "path": "api/lists/{id}/relationships/flow-triggers"},
    {"method": "GET", "path": "api/lists/{id}/relationships/profiles"},
    {"method": "GET", "path": "api/lists/{id}/relationships/tags"},
    {"method": "GET", "path": "api/lists/{id}/tags"},
    {"method": "GET", "path": "api/custom-metrics"},
    {"method": "GET", "path": "api/custom-metrics/{id}"},
    {"method": "GET", "path": "api/custom-metrics/{id}/metrics"},
    {"method": "GET", "path": "api/custom-metrics/{id}/relationships/metrics"},
    {"method": "GET", "path": "api/mapped-metrics"},
    {"method": "GET", "path": "api/mapped-metrics/{id}"},
    {"method": "GET", "path": "api/mapped-metrics/{id}/custom-metric"},
    {"method": "GET", "path": "api/mapped-metrics/{id}/metric"},
    {"method": "GET", "path": "api/mapped-metrics/{id}/relationships/custom-metric"},
    {"method": "GET", "path": "api/mapped-metrics/{id}/relationships/metric"},
    {"method": "POST", "path": "api/metric-aggregates"},
    {"method": "GET", "path": "api/metric-properties/{id}"},
    {"method": "GET", "path": "api/metric-properties/{id}/metric"},
    {"method": "GET", "path": "api/metric-properties/{id}/relationships/metric"},
    {"method": "GET", "path": "api/metrics"},
    {"method": "GET", "path": "api/metrics/{id}"},
    {"method": "GET", "path": "api/metrics/{id}/flow-triggers"},
    {"method": "GET", "path": "api/metrics/{id}/metric-properties"},
    {"method": "GET", "path": "api/metrics/{id}/relationships/flow-triggers"},
    {"method": "GET", "path": "api/metrics/{id}/relationships/metric-properties"},
    {"method": "GET", "path": "api/profile-bulk-import-jobs"},
    {"method": "GET", "path": "api/profile-bulk-import-jobs/{id}"},
    {"method": "GET", "path": "api/profile-bulk-import-jobs/{id}/import-errors"},
    {"method": "GET", "path": "api/profile-bulk-import-jobs/{id}/lists"},
    {"method": "GET", "path": "api/profile-bulk-import-jobs/{id}/profiles"},
    {"method": "GET", "path": "api/profile-bulk-import-jobs/{id}/relationships/lists"},
    {"method": "GET", "path": "api/profile-bulk-import-jobs/{id}/relationships/profiles"},
    {"method": "GET", "path": "api/profile-suppression-bulk-create-jobs"},
    {"method": "GET", "path": "api/profile-suppression-bulk-create-jobs/{id}"},
    {"method": "GET", "path": "api/profile-suppression-bulk-delete-jobs"},
    {"method": "GET", "path": "api/profile-suppression-bulk-delete-jobs/{id}"},
    {"method": "GET", "path": "api/profiles"},
    {"method": "GET", "path": "api/profiles/{id}"},
    {"method": "GET", "path": "api/profiles/{id}/conversation"},
    {"method": "GET", "path": "api/profiles/{id}/conversations"},
    {"method": "GET", "path": "api/profiles/{id}/lists"},
    {"method": "GET", "path": "api/profiles/{id}/push-tokens"},
    {"method": "GET", "path": "api/profiles/{id}/relationships/conversation"},
    {"method": "GET", "path": "api/profiles/{id}/relationships/conversations"},
    {"method": "GET", "path": "api/profiles/{id}/relationships/lists"},
    {"method": "GET", "path": "api/profiles/{id}/relationships/push-tokens"},
    {"method": "GET", "path": "api/profiles/{id}/relationships/segments"},
    {"method": "GET", "path": "api/profiles/{id}/segments"},
    {"method": "GET", "path": "api/push-tokens"},
    {"method": "GET", "path": "api/push-tokens/{id}"},
    {"method": "GET", "path": "api/push-tokens/{id}/profile"},
    {"method": "GET", "path": "api/push-tokens/{id}/relationships/profile"},
    {"method": "POST", "path": "api/campaign-values-reports"},
    {"method": "POST", "path": "api/flow-series-reports"},
    {"method": "POST", "path": "api/flow-values-reports"},
    {"method": "POST", "path": "api/form-series-reports"},
    {"method": "POST", "path": "api/form-values-reports"},
    {"method": "POST", "path": "api/segment-series-reports"},
    {"method": "POST", "path": "api/segment-values-reports"},
    {"method": "GET", "path": "api/reviews"},
    {"method": "GET", "path": "api/reviews/{id}"},
    {"method": "GET", "path": "api/segments"},
    {"method": "GET", "path": "api/segments/{id}"},
    {"method": "GET", "path": "api/segments/{id}/flow-triggers"},
    {"method": "GET", "path": "api/segments/{id}/profiles"},
    {"method": "GET", "path": "api/segments/{id}/relationships/flow-triggers"},
    {"method": "GET", "path": "api/segments/{id}/relationships/profiles"},
    {"method": "GET", "path": "api/segments/{id}/relationships/tags"},
    {"method": "GET", "path": "api/segments/{id}/tags"},
    {"method": "GET", "path": "api/tag-groups"},
    {"method": "GET", "path": "api/tag-groups/{id}"},
    {"method": "GET", "path": "api/tag-groups/{id}/relationships/tags"},
    {"method": "GET", "path": "api/tag-groups/{id}/tags"},
    {"method": "GET", "path": "api/tags"},
    {"method": "GET", "path": "api/tags/{id}"},
    {"method": "GET", "path": "api/tags/{id}/relationships/campaigns"},
    {"method": "GET", "path": "api/tags/{id}/relationships/flows"},
    {"method": "GET", "path": "api/tags/{id}/relationships/lists"},
    {"method": "GET", "path": "api/tags/{id}/relationships/segments"},
    {"method": "GET", "path": "api/tags/{id}/relationships/tag-group"},
    {"method": "GET", "path": "api/tags/{id}/tag-group"},
    {"method": "GET", "path": "api/template-conversion-jobs"},
    {"method": "GET", "path": "api/template-conversion-jobs/{id}"},
    {"method": "POST", "path": "api/template-render"},
    {"method": "GET", "path": "api/template-universal-content"},
    {"method": "GET", "path": "api/template-universal-content/{id}"},
    {"method": "GET", "path": "api/templates"},
    {"method": "GET", "path": "api/templates/{id}"},
    {"method": "GET", "path": "api/text-messaging-configurations/{id}"},
    {"method": "GET", "path": "api/text-messaging-sender-registrations/{id}"},
    {"method": "GET", "path": "api/text-messaging-senders"},
    {"method": "GET", "path": "api/text-messaging-senders/{id}"},
    {"method": "GET", "path": "api/text-messaging-senders/{id}/relationships/text-messaging-sender-registration"},
    {"method": "GET", "path": "api/text-messaging-senders/{id}/text-messaging-sender-registration"},
    {"method": "GET", "path": "api/tracking-settings"},
    {"method": "GET", "path": "api/tracking-settings/{id}"},
    {"method": "GET", "path": "api/translations"},
    {"method": "GET", "path": "api/translations/{id}"},
    {"method": "GET", "path": "api/translations/{id}/campaign-variation"},
    {"method": "GET", "path": "api/translations/{id}/flow-message"},
    {"method": "GET", "path": "api/translations/{id}/relationships/campaign-variation"},
    {"method": "GET", "path": "api/translations/{id}/relationships/flow-message"},
    {"method": "GET", "path": "api/translations/{id}/relationships/template"},
    {"method": "GET", "path": "api/translations/{id}/relationships/template-universal-content"},
    {"method": "GET", "path": "api/translations/{id}/template"},
    {"method": "GET", "path": "api/translations/{id}/template-universal-content"},
    {"method": "GET", "path": "api/web-feeds"},
    {"method": "GET", "path": "api/web-feeds/{id}"},
    {"method": "GET", "path": "api/webhook-topics"},
    {"method": "GET", "path": "api/webhook-topics/{id}"},
    {"method": "GET", "path": "api/webhooks"},
    {"method": "GET", "path": "api/webhooks/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Klaviyo endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/accounts | read | accounts | Retrieve the account(s) associated with a given private API key. |
| GET | api/accounts/{id} | read | accounts | Retrieve a single account object by its account ID. |
| GET | api/billing-usage | read | billing | List current-period usage and plan caps for the account. |
| GET | api/billing-usage/{id} | read | billing | Get current-period usage and plan cap for a single usage type. |
| GET | api/brand-buttons | read | brands | Get all brand buttons for the authenticated account. |
| POST | api/brand-buttons | write | brands | Create a new brand button. |
| GET | api/brand-buttons/{id} | read | brands | Get the brand button with the given ID. |
| PATCH | api/brand-buttons/{id} | write | brands | Update the brand button with the given ID. |
| DELETE | api/brand-buttons/{id} | write | brands | Delete the brand button with the given ID. |
| GET | api/brand-colors | read | brands | Get all brand color groups for the authenticated account. |
| POST | api/brand-colors | write | brands | Create a new brand color group. |
| GET | api/brand-colors/{id} | read | brands | Get the brand color group with the given ID. |
| PATCH | api/brand-colors/{id} | write | brands | Update the brand color group with the given ID. |
| DELETE | api/brand-colors/{id} | write | brands | Delete the brand color group with the given ID. |
| GET | api/brand-email-defaults | read | brands | List the brand email defaults for the authenticated account. |
| GET | api/brand-email-defaults/{id} | read | brands | Get the brand email defaults for the authenticated account. |
| PATCH | api/brand-email-defaults/{id} | write | brands | Partial update of the brand email defaults for the authenticated account. |
| GET | api/brand-logos | read | brands | Get all brand logos for the authenticated account. |
| POST | api/brand-logos | write | brands | Create a new brand logo. |
| GET | api/brand-logos/{id} | read | brands | Get the brand logo with the given ID. |
| PATCH | api/brand-logos/{id} | write | brands | Update the brand logo with the given ID. |
| DELETE | api/brand-logos/{id} | write | brands | Delete the brand logo with the given ID. |
| GET | api/brand-social-groups | read | brands | Get all brand social groups for the authenticated account. |
| POST | api/brand-social-groups | write | brands | Create a new brand social group. |
| GET | api/brand-social-groups/{id} | read | brands | Get the brand social group with the given ID. |
| PATCH | api/brand-social-groups/{id} | write | brands | Update the brand social group with the given ID. |
| DELETE | api/brand-social-groups/{id} | write | brands | Delete the brand social group with the given ID. |
| GET | api/brand-voice/{id} | read | brands | Get the brand voice for the authenticated company. |
| PATCH | api/brand-voice/{id} | write | brands | Update the brand voice for the authenticated company. |
| POST | api/campaign-audience-clone | write | campaigns | Clone an existing campaign audience to a target campaign. |
| POST | api/campaign-audiences | write | campaigns | Create a campaign audience. |
| GET | api/campaign-audiences/{id} | read | campaigns | Get the campaign audience with the given ID. |
| PATCH | api/campaign-audiences/{id} | write | campaigns | Update the campaign audience with the given ID. |
| DELETE | api/campaign-audiences/{id} | write | campaigns | Delete the campaign audience with the given ID. |
| GET | api/campaign-audiences/{id}/campaign | read | campaigns | Get the campaign for the given campaign audience ID. |
| GET | api/campaign-audiences/{id}/campaign-messages | read | campaigns | Get all campaign messages for the given campaign audience ID. |
| GET | api/campaign-audiences/{id}/relationships/campaign | read | campaigns | Get the campaign relationship for the given campaign audience ID. |
| GET | api/campaign-audiences/{id}/relationships/campaign-messages | read | campaigns | Get all campaign messages relationships for the given campaign audience ID. |
| POST | api/campaign-clone | write | campaigns | Clones an existing campaign, returning a new campaign based on the original with a new ID and name. |
| POST | api/campaign-message-assign-template | write | campaigns | Creates a non-reusable version of the template and assigns it to the message. |
| POST | api/campaign-message-clone | write | campaigns | Clone an existing campaign message to a target audience. |
| POST | api/campaign-message-schedule | write | campaigns | Schedule a single campaign message. |
| PATCH | api/campaign-message-schedule/{id} | write | campaigns | Cancel or revert a scheduled campaign message. |
| GET | api/campaign-messages | read | campaigns | Returns campaign messages based on filters. |
| POST | api/campaign-messages | write | campaigns | Create a campaign message. |
| GET | api/campaign-messages/{id} | read | campaigns | Get a campaign message by ID. |
| PATCH | api/campaign-messages/{id} | write | campaigns | Update a campaign message. |
| DELETE | api/campaign-messages/{id} | write | campaigns | Delete a campaign message. |
| GET | api/campaign-messages/{id}/campaign | read | campaigns | Return the related omnicampaign. |
| GET | api/campaign-messages/{id}/campaign-audience | read | campaigns | Get the campaign audience for the given campaign message ID. |
| GET | api/campaign-messages/{id}/campaign-variations | read | campaigns | Get all campaign variations for the given campaign message ID. |
| GET | api/campaign-messages/{id}/image | read | campaigns | Return the related image for a given campaign message. |
| GET | api/campaign-messages/{id}/relationships/campaign | read | campaigns | Returns the ID of the related omnicampaign. |
| GET | api/campaign-messages/{id}/relationships/campaign-audience | read | campaigns | Get the campaign audience relationship for the given campaign message ID. |
| GET | api/campaign-messages/{id}/relationships/campaign-variations | read | campaigns | Get all campaign variation relationships for the given campaign message ID. |
| GET | api/campaign-messages/{id}/relationships/image | read | campaigns | Returns the ID of the related image. |
| PATCH | api/campaign-messages/{id}/relationships/image | write | campaigns | Update a campaign message image. |
| GET | api/campaign-messages/{id}/relationships/tags | read | campaigns | Get all tag relationships for the given campaign message ID. |
| GET | api/campaign-messages/{id}/relationships/template | read | campaigns | Returns the ID of the related template. |
| GET | api/campaign-messages/{id}/tags | read | campaigns | Get all tags for the given campaign message ID. |
| GET | api/campaign-messages/{id}/template | read | campaigns | Return the related template. |
| POST | api/campaign-recipient-estimation-jobs | write | campaigns | Trigger an asynchronous job to update the estimated number of recipients for the given campaign ID. |
| GET | api/campaign-recipient-estimation-jobs/{id} | read | campaigns | Retrieve the status of a recipient estimation job triggered with the `Create Campaign Recipient Estimation Job` endpoint. |
| GET | api/campaign-recipient-estimations/{id} | read | campaigns | Get the estimated recipient count for a campaign with the provided campaign ID. |
| POST | api/campaign-send-jobs | write | campaigns | Trigger a campaign to send asynchronously. |
| GET | api/campaign-send-jobs/{id} | read | campaigns | Get a campaign send job. |
| PATCH | api/campaign-send-jobs/{id} | write | campaigns | Permanently cancel the campaign, setting the status to CANCELED or revert the campaign, setting the status back to DRAFT. |
| POST | api/campaign-variations | write | campaigns | Create a campaign variation. |
| GET | api/campaign-variations/{id} | read | campaigns | Get the campaign variation with the given ID. |
| PATCH | api/campaign-variations/{id} | write | campaigns | Update the campaign variation with the given ID. |
| DELETE | api/campaign-variations/{id} | write | campaigns | Delete the campaign variation with the given ID. |
| GET | api/campaign-variations/{id}/campaign-message | read | campaigns | Get the campaign message for the given campaign variation ID. |
| GET | api/campaign-variations/{id}/image | read | campaigns | Get the image for the given campaign variation ID. |
| GET | api/campaign-variations/{id}/relationships/campaign-message | read | campaigns | Get the campaign message relationship for the given campaign variation ID. |
| GET | api/campaign-variations/{id}/relationships/image | read | campaigns | Get the image relationship for the given campaign variation ID. |
| GET | api/campaign-variations/{id}/relationships/translation | read | campaigns | Get the translation relationship for the given campaign variation ID. |
| GET | api/campaign-variations/{id}/translation | read | campaigns | Get the translation for the given campaign variation ID. |
| GET | api/campaigns | read | campaigns | Get all campaigns, with optional filtering. |
| POST | api/campaigns | write | campaigns | Create a campaign with inline audiences, messages, and variations. |
| GET | api/campaigns/{id} | read | campaigns | Get a campaign by ID. |
| PATCH | api/campaigns/{id} | write | campaigns | Update a campaign with the given campaign ID. |
| DELETE | api/campaigns/{id} | write | campaigns | Delete a campaign with the given campaign ID. |
| GET | api/campaigns/{id}/campaign-audiences | read | campaigns | Get all campaign audiences for the given campaign ID. |
| GET | api/campaigns/{id}/campaign-messages | read | campaigns | Get all messages for the given campaign. |
| GET | api/campaigns/{id}/relationships/campaign-audiences | read | campaigns | Get all campaign audience relationships for the given campaign ID. |
| GET | api/campaigns/{id}/relationships/campaign-messages | read | campaigns | Get all campaign message relationships for the given campaign ID. |
| GET | api/campaigns/{id}/relationships/tags | read | campaigns | Get all tag relationships for the given campaign ID. |
| GET | api/campaigns/{id}/tags | read | campaigns | Get the tags on the given campaign ID. |
| POST | api/back-in-stock-subscriptions | write | catalogs | Subscribe a profile to receive back in stock notifications. |
| GET | api/catalog-categories | read | catalogs | Get all catalog categories in an account. |
| POST | api/catalog-categories | write | catalogs | Create a new catalog category. |
| GET | api/catalog-categories/{id} | read | catalogs | Get a catalog category with the given category ID. |
| PATCH | api/catalog-categories/{id} | write | catalogs | Update a catalog category with the given category ID. |
| DELETE | api/catalog-categories/{id} | write | catalogs | Delete a catalog category using the given category ID. |
| GET | api/catalog-categories/{id}/items | read | catalogs | Get all items in a category with the given category ID. |
| GET | api/catalog-categories/{id}/relationships/items | read | catalogs | Get all items in the given category ID. |
| POST | api/catalog-categories/{id}/relationships/items | write | catalogs | Create a new item relationship for the given category ID. |
| PATCH | api/catalog-categories/{id}/relationships/items | write | catalogs | Update item relationships for the given category ID. |
| DELETE | api/catalog-categories/{id}/relationships/items | write | catalogs | Delete item relationships for the given category ID. |
| GET | api/catalog-category-bulk-create-jobs | read | catalogs | Get all catalog category bulk create jobs. |
| POST | api/catalog-category-bulk-create-jobs | write | catalogs | Create a catalog category bulk create job to create a batch of catalog categories. |
| GET | api/catalog-category-bulk-create-jobs/{id} | read | catalogs | Get a catalog category bulk create job with the given job ID. |
| GET | api/catalog-category-bulk-delete-jobs | read | catalogs | Get all catalog category bulk delete jobs. |
| POST | api/catalog-category-bulk-delete-jobs | write | catalogs | Create a catalog category bulk delete job to delete a batch of catalog categories. |
| GET | api/catalog-category-bulk-delete-jobs/{id} | read | catalogs | Get a catalog category bulk delete job with the given job ID. |
| GET | api/catalog-category-bulk-update-jobs | read | catalogs | Get all catalog category bulk update jobs. |
| POST | api/catalog-category-bulk-update-jobs | write | catalogs | Create a catalog category bulk update job to update a batch of catalog categories. |
| GET | api/catalog-category-bulk-update-jobs/{id} | read | catalogs | Get a catalog category bulk update job with the given job ID. |
| GET | api/catalog-item-bulk-create-jobs | read | catalogs | Get all catalog item bulk create jobs. |
| POST | api/catalog-item-bulk-create-jobs | write | catalogs | Create a catalog item bulk create job to create a batch of catalog items. |
| GET | api/catalog-item-bulk-create-jobs/{id} | read | catalogs | Get a catalog item bulk create job with the given job ID. |
| GET | api/catalog-item-bulk-delete-jobs | read | catalogs | Get all catalog item bulk delete jobs. |
| POST | api/catalog-item-bulk-delete-jobs | write | catalogs | Create a catalog item bulk delete job to delete a batch of catalog items. |
| GET | api/catalog-item-bulk-delete-jobs/{id} | read | catalogs | Get a catalog item bulk delete job with the given job ID. |
| GET | api/catalog-item-bulk-update-jobs | read | catalogs | Get all catalog item bulk update jobs. |
| POST | api/catalog-item-bulk-update-jobs | write | catalogs | Create a catalog item bulk update job to update a batch of catalog items. |
| GET | api/catalog-item-bulk-update-jobs/{id} | read | catalogs | Get a catalog item bulk update job with the given job ID. |
| GET | api/catalog-items | read | catalogs | Get all catalog items in an account. |
| POST | api/catalog-items | write | catalogs | Create a new catalog item. |
| GET | api/catalog-items/{id} | read | catalogs | Get a specific catalog item with the given item ID. |
| PATCH | api/catalog-items/{id} | write | catalogs | Update a catalog item with the given item ID. |
| DELETE | api/catalog-items/{id} | write | catalogs | Delete a catalog item with the given item ID. |
| GET | api/catalog-items/{id}/categories | read | catalogs | Get all catalog categories that an item with the given item ID is in. |
| GET | api/catalog-items/{id}/relationships/categories | read | catalogs | Get all catalog categories that a particular item is in. |
| POST | api/catalog-items/{id}/relationships/categories | write | catalogs | Create a new catalog category relationship for the given item ID. |
| PATCH | api/catalog-items/{id}/relationships/categories | write | catalogs | Update catalog category relationships for the given item ID. |
| DELETE | api/catalog-items/{id}/relationships/categories | write | catalogs | Delete catalog category relationships for the given item ID. |
| GET | api/catalog-items/{id}/relationships/variants | read | catalogs | Get all variants related to the given item ID. |
| GET | api/catalog-items/{id}/variants | read | catalogs | Get all variants related to the given item ID. |
| GET | api/catalog-variant-bulk-create-jobs | read | catalogs | Get all catalog variant bulk create jobs. |
| POST | api/catalog-variant-bulk-create-jobs | write | catalogs | Create a catalog variant bulk create job to create a batch of catalog variants. |
| GET | api/catalog-variant-bulk-create-jobs/{id} | read | catalogs | Get a catalog variant bulk create job with the given job ID. |
| GET | api/catalog-variant-bulk-delete-jobs | read | catalogs | Get all catalog variant bulk delete jobs. |
| POST | api/catalog-variant-bulk-delete-jobs | write | catalogs | Create a catalog variant bulk delete job to delete a batch of catalog variants. |
| GET | api/catalog-variant-bulk-delete-jobs/{id} | read | catalogs | Get a catalog variant bulk delete job with the given job ID. |
| GET | api/catalog-variant-bulk-update-jobs | read | catalogs | Get all catalog variant bulk update jobs. |
| POST | api/catalog-variant-bulk-update-jobs | write | catalogs | Create a catalog variant bulk update job to update a batch of catalog variants. |
| GET | api/catalog-variant-bulk-update-jobs/{id} | read | catalogs | Get a catalog variate bulk update job with the given job ID. |
| GET | api/catalog-variants | read | catalogs | Get all variants in an account. |
| POST | api/catalog-variants | write | catalogs | Create a new variant for a related catalog item. |
| GET | api/catalog-variants/{id} | read | catalogs | Get a catalog item variant with the given variant ID. |
| PATCH | api/catalog-variants/{id} | write | catalogs | Update a catalog item variant with the given variant ID. |
| DELETE | api/catalog-variants/{id} | write | catalogs | Delete a catalog item variant with the given variant ID. |
| POST | client/back-in-stock-subscriptions | write | client | Subscribe a profile to receive back in stock notifications. |
| POST | client/event-bulk-create | write | client | Create new events to track a profile's activity. |
| POST | client/events | write | client | Create a new event to track a profile's activity. |
| GET | client/geofences | read | client | Get all geofences in an account. |
| GET | client/ip-allowlists/{id} | read | client | Return the current integration-egress IP allow list. |
| POST | client/profiles | write | client | Create or update properties about a profile without tracking an associated event. |
| POST | client/push-token-unregister | write | client | Unregister a push token. |
| POST | client/push-tokens | write | client | Create or update a push token. |
| GET | client/review-values-reports | read | client | Get all reviews values reports in an account. |
| GET | client/reviews | read | client | Get all reviews. |
| POST | client/reviews | write | client | Create a review with the given ID. |
| POST | client/subscriptions | write | client | Creates a subscription and consent record for email and/or SMS channels based on the provided `email` and `phone_number` attributes, respectively. |
| POST | api/conversation-messages | write | conversations | Send an outbound message to a conversation. |
| GET | api/coupon-code-bulk-create-jobs | read | coupons | Get all coupon code bulk create jobs. |
| POST | api/coupon-code-bulk-create-jobs | write | coupons | Create a coupon-code-bulk-create-job to bulk create a list of coupon codes. |
| GET | api/coupon-code-bulk-create-jobs/{id} | read | coupons | Get a coupon code bulk create job with the given job ID. |
| GET | api/coupon-codes | read | coupons | Gets a list of coupon codes associated with a coupon/coupons or a profile/profiles. |
| POST | api/coupon-codes | write | coupons | Synchronously creates a coupon code for the given coupon. |
| GET | api/coupon-codes/{id} | read | coupons | Returns a Coupon Code specified by the given identifier. |
| PATCH | api/coupon-codes/{id} | write | coupons | Updates a coupon code specified by the given identifier synchronously. |
| DELETE | api/coupon-codes/{id} | write | coupons | Deletes a coupon code specified by the given identifier synchronously. |
| GET | api/coupon-codes/{id}/coupon | read | coupons | Get the coupon associated with a given coupon code ID. |
| GET | api/coupon-codes/{id}/relationships/coupon | read | coupons | Gets the coupon relationship associated with the given coupon code id. |
| GET | api/coupons | read | coupons | Get all coupons in an account. |
| POST | api/coupons | write | coupons | Creates a new coupon. |
| GET | api/coupons/{id} | read | coupons | Get a specific coupon with the given coupon ID. |
| PATCH | api/coupons/{id} | write | coupons | Update Coupon. |
| DELETE | api/coupons/{id} | write | coupons | Delete the coupon with the given coupon ID. |
| GET | api/coupons/{id}/coupon-codes | read | coupons | Gets a list of coupon codes associated with the given coupon id. |
| GET | api/coupons/{id}/relationships/coupon-codes | read | coupons | Gets a list of coupon code relationships associated with the given coupon id. |
| POST | api/data-source-record-bulk-create-jobs | write | custom-objects | Create a bulk data source record import job to create a batch of records. |
| POST | api/data-source-record-create-jobs | write | custom-objects | Create a data source record import job to create a single record. |
| GET | api/data-sources | read | custom-objects | Get all data sources in an account. |
| POST | api/data-sources | write | custom-objects | Create a new data source in an account. |
| GET | api/data-sources/{id} | read | custom-objects | Retrieve a data source in an account. |
| DELETE | api/data-sources/{id} | write | custom-objects | Delete a data source in an account. |
| POST | api/object-record-bulk-delete-jobs | write | custom-objects | Delete a batch of object records. |
| GET | api/object-records/{id} | read | custom-objects | Get the object record with the given compound ID. |
| POST | api/object-schemas | write | custom-objects | Create an object schema. |
| GET | api/object-schemas/{id} | read | custom-objects | Get the object schema with the given ID. |
| PATCH | api/object-schemas/{id} | write | custom-objects | Update the object schema with the given ID. |
| GET | api/object-schemas/{id}/relationships/object-schemas | read | custom-objects | Get related object schemas for an object schema. |
| POST | api/object-schemas/{id}/relationships/object-schemas | write | custom-objects | Create a relationship between object schemas. |
| PATCH | api/object-schemas/{id}/relationships/object-schemas | write | custom-objects | Update a relationship between object schemas. |
| DELETE | api/object-schemas/{id}/relationships/object-schemas | write | custom-objects | Delete a relationship between object schemas. |
| GET | api/object-schemas/{id}/relationships/profile-object-schemas | read | custom-objects | Get related profile object schemas for an object schema. |
| POST | api/object-schemas/{id}/relationships/profile-object-schemas | write | custom-objects | Create a relationship between an object schema and a profile. |
| PATCH | api/object-schemas/{id}/relationships/profile-object-schemas | write | custom-objects | Update a relationship between an object schema and a profile. |
| DELETE | api/object-schemas/{id}/relationships/profile-object-schemas | write | custom-objects | Delete a relationship between an object schema and a profile. |
| GET | api/object-schemas/{id}/relationships/source-mapping | read | custom-objects | Get source mapping for an object schema. |
| GET | api/object-schemas/{id}/source-mapping | read | custom-objects | Get source mapping for an object schema. |
| GET | api/object-types | read | custom-objects | Get all object types in an account. |
| POST | api/object-types | write | custom-objects | Create an object type. |
| GET | api/object-types/{id} | read | custom-objects | Get the object type with the given ID. |
| DELETE | api/object-types/{id} | write | custom-objects | Delete the object type with the given ID. |
| GET | api/object-types/{id}/current-schema | read | custom-objects | Get current schema for an object type. |
| GET | api/object-types/{id}/draft-schema | read | custom-objects | Get draft schema for an object type. |
| GET | api/object-types/{id}/object-ingestion-logs | read | custom-objects | Get the ingestion logs for a given object type. |
| GET | api/object-types/{id}/object-records | read | custom-objects | Get all object records for a given object type. |
| GET | api/object-types/{id}/relationships/current-schema | read | custom-objects | Get current schema for an object type. |
| GET | api/object-types/{id}/relationships/draft-schema | read | custom-objects | Get draft schema for an object type. |
| GET | api/object-types/{id}/relationships/object-ingestion-logs | read | custom-objects | Get the ingestion logs for a given object type. |
| GET | api/object-types/{id}/relationships/object-records | read | custom-objects | Get all object records for a given object type. |
| GET | api/object-types/{id}/relationships/object-types | read | custom-objects | Get related object types for an object type. |
| GET | api/object-types/{id}/relationships/profile-object-types | read | custom-objects | Get related profile object types for an object type. |
| GET | api/object-types/{id}/relationships/schema-versions | read | custom-objects | Get all schema versions for an object type. |
| GET | api/object-types/{id}/schema-versions | read | custom-objects | Get all schema versions for an object type. |
| GET | api/source-mappings/{id} | read | custom-objects | Get the source mapping with the given ID. |
| PATCH | api/source-mappings/{id} | write | custom-objects | Update the source mapping with the given ID. |
| POST | api/data-privacy-deletion-jobs | write | data-privacy | Request a deletion for the profiles corresponding to one of the following identifiers: `email`, `phone_number`, or `id`. |
| POST | api/event-bulk-create-jobs | write | events | Create a batch of events for one or more profiles. |
| GET | api/events | read | events | Get all events in an account. |
| POST | api/events | write | events | Create a new event to track a profile's activity. |
| GET | api/events/{id} | read | events | Get an event with the given event ID. |
| GET | api/events/{id}/metric | read | events | Get the metric for an event with the given event ID. |
| GET | api/events/{id}/profile | read | events | Get the profile associated with an event with the given event ID. |
| GET | api/events/{id}/relationships/metric | read | events | Get a list of related Metrics for an Event. |
| GET | api/events/{id}/relationships/profile | read | events | Get profile relationships for an event with the given event ID. |
| POST | api/flow-actions | write | flows | Insert a new action into an existing flow. |
| GET | api/flow-actions/{id} | read | flows | Get a flow action from a flow with the given flow action ID. |
| PATCH | api/flow-actions/{id} | write | flows | Update a flow action. |
| DELETE | api/flow-actions/{id} | write | flows | Delete a flow action. |
| GET | api/flow-actions/{id}/flow | read | flows | Get the flow associated with the given action ID. |
| GET | api/flow-actions/{id}/flow-messages | read | flows | Get all flow messages associated with the given flow action ID. |
| GET | api/flow-actions/{id}/relationships/flow | read | flows | Get the flow associated with the given action ID. |
| GET | api/flow-actions/{id}/relationships/flow-messages | read | flows | Get all relationships for flow messages associated with the given flow action ID. |
| GET | api/flow-messages/{id} | read | flows | Get a flow message from a flow with the given flow message ID. |
| GET | api/flow-messages/{id}/flow-action | read | flows | Get the flow action for a flow message with the given message ID. |
| GET | api/flow-messages/{id}/relationships/flow-action | read | flows | Get the relationship for a flow message's flow action, given the flow ID. |
| GET | api/flow-messages/{id}/relationships/template | read | flows | Returns the ID of the related template. |
| GET | api/flow-messages/{id}/template | read | flows | Return the related template. |
| GET | api/flows | read | flows | Get all flows in an account. |
| POST | api/flows | write | flows | Create a new flow using an encoded flow definition. |
| GET | api/flows/{id} | read | flows | Get a flow with the given flow ID. |
| PATCH | api/flows/{id} | write | flows | Update the status of a flow with the given flow ID, and all actions in that flow. |
| DELETE | api/flows/{id} | write | flows | Delete a flow with the given flow ID. |
| GET | api/flows/{id}/flow-actions | read | flows | Get all flow actions associated with the given flow ID. |
| GET | api/flows/{id}/relationships/flow-actions | read | flows | Get all relationships for flow actions associated with the given flow ID. |
| GET | api/flows/{id}/relationships/tags | read | flows | Return the tag IDs of all tags associated with the given flow. |
| GET | api/flows/{id}/tags | read | flows | Return all tags associated with the given flow ID. |
| POST | api/form-publish-jobs | write | forms | Publish the draft version of a form. |
| POST | api/form-unpublish-jobs | write | forms | Unpublish the live version of a form. |
| GET | api/form-versions/{id} | read | forms | Get the form version with the given ID. |
| GET | api/form-versions/{id}/form | read | forms | Get the form associated with the given form version. |
| GET | api/form-versions/{id}/relationships/form | read | forms | Get the ID of the form associated with the given form version. |
| GET | api/forms | read | forms | Get all forms in an account. |
| POST | api/forms | write | forms | Create a new form. |
| GET | api/forms/{id} | read | forms | Get the form with the given ID. |
| PATCH | api/forms/{id} | write | forms | Update a form. |
| DELETE | api/forms/{id} | write | forms | Delete a given form. |
| GET | api/forms/{id}/form-versions | read | forms | Get the form versions for the given form. |
| GET | api/forms/{id}/relationships/form-versions | read | forms | Get the IDs of the form versions for the given form. |
| POST | api/image-upload | write | images | Upload an image from a file. |
| GET | api/images | read | images | Get all images in an account. |
| POST | api/images | write | images | Import an image from a url or data uri. |
| GET | api/images/{id} | read | images | Get the image with the given image ID. |
| PATCH | api/images/{id} | write | images | Update the image with the given image ID. |
| GET | api/lists | read | lists | Get all lists in an account. |
| POST | api/lists | write | lists | Create a new list. |
| GET | api/lists/{id} | read | lists | Get a list with the given list ID. |
| PATCH | api/lists/{id} | write | lists | Update the name of a list with the given list ID. |
| DELETE | api/lists/{id} | write | lists | Delete a list with the given list ID. |
| GET | api/lists/{id}/flow-triggers | read | lists | Get all flows where the given list ID is being used as the trigger. |
| GET | api/lists/{id}/profiles | read | lists | Get all profiles within a list with the given list ID. |
| GET | api/lists/{id}/relationships/flow-triggers | read | lists | Get the IDs of all flows where the given list is being used as the trigger. |
| GET | api/lists/{id}/relationships/profiles | read | lists | Get profile membership relationships for a list with the given list ID. |
| POST | api/lists/{id}/relationships/profiles | write | lists | Add a profile to a list with the given list ID. |
| DELETE | api/lists/{id}/relationships/profiles | write | lists | Remove a profile from a list with the given list ID. |
| GET | api/lists/{id}/relationships/tags | read | lists | Return all tags associated with the given list ID. |
| GET | api/lists/{id}/tags | read | lists | Return all tags associated with the given list ID. |
| GET | api/custom-metrics | read | metrics | Get all custom metrics in an account. |
| POST | api/custom-metrics | write | metrics | Create a new custom metric. |
| GET | api/custom-metrics/{id} | read | metrics | Get a custom metric with the given custom metric ID. |
| PATCH | api/custom-metrics/{id} | write | metrics | Update a custom metric with the given custom metric ID. |
| DELETE | api/custom-metrics/{id} | write | metrics | Delete a custom metric with the given custom metric ID. |
| GET | api/custom-metrics/{id}/metrics | read | metrics | Get all metrics for the given custom metric ID. |
| GET | api/custom-metrics/{id}/relationships/metrics | read | metrics | Get all metrics for the given custom metric ID. |
| GET | api/mapped-metrics | read | metrics | Get all mapped metrics in an account. |
| GET | api/mapped-metrics/{id} | read | metrics | Get the mapped metric with the given ID. |
| PATCH | api/mapped-metrics/{id} | write | metrics | Update the mapped metric with the given ID. |
| GET | api/mapped-metrics/{id}/custom-metric | read | metrics | Get the custom metric for the given mapped metric ID (if applicable). |
| GET | api/mapped-metrics/{id}/metric | read | metrics | Get the metric for the given mapped metric ID (if applicable). |
| GET | api/mapped-metrics/{id}/relationships/custom-metric | read | metrics | Get the ID of the custom metric for the given mapped metric. |
| GET | api/mapped-metrics/{id}/relationships/metric | read | metrics | Get the ID of the metric for the given mapped metric. |
| POST | api/metric-aggregates | read | metrics | Query and aggregate event data associated with a metric, including native Klaviyo metrics, integration-specific metrics, and custom events (not to be confused with custom metrics, which are not... |
| GET | api/metric-properties/{id} | read | metrics | Get a metric property with the given metric property ID. |
| GET | api/metric-properties/{id}/metric | read | metrics | Get the metric for the given metric property ID. |
| GET | api/metric-properties/{id}/relationships/metric | read | metrics | Get the ID of the metric for the given metric property. |
| GET | api/metrics | read | metrics | Get all metrics in an account. |
| GET | api/metrics/{id} | read | metrics | Get a metric with the given metric ID. |
| GET | api/metrics/{id}/flow-triggers | read | metrics | Get all flows where the given metric is being used as the trigger. |
| GET | api/metrics/{id}/metric-properties | read | metrics | Get the metric properties for the given metric ID. |
| GET | api/metrics/{id}/relationships/flow-triggers | read | metrics | Get the IDs of all flows where the given metric is being used as the trigger. |
| GET | api/metrics/{id}/relationships/metric-properties | read | metrics | Get the IDs of metric properties for the given metric. |
| GET | api/profile-bulk-import-jobs | read | profiles | Get all bulk profile import jobs. |
| POST | api/profile-bulk-import-jobs | write | profiles | Create a bulk profile import job to create or update a batch of profiles. |
| GET | api/profile-bulk-import-jobs/{id} | read | profiles | Get a bulk profile import job with the given job ID. |
| GET | api/profile-bulk-import-jobs/{id}/import-errors | read | profiles | Get import errors for the bulk profile import job with the given ID. |
| GET | api/profile-bulk-import-jobs/{id}/lists | read | profiles | Get list for the bulk profile import job with the given ID. |
| GET | api/profile-bulk-import-jobs/{id}/profiles | read | profiles | Get profiles for the bulk profile import job with the given ID. |
| GET | api/profile-bulk-import-jobs/{id}/relationships/lists | read | profiles | Get list relationship for the bulk profile import job with the given ID. |
| GET | api/profile-bulk-import-jobs/{id}/relationships/profiles | read | profiles | Get profile relationships for the bulk profile import job with the given ID. |
| POST | api/profile-import | write | profiles | Given a set of profile attributes and optionally an ID, create or update a profile. |
| POST | api/profile-merge | write | profiles | Merge a given related profile into a profile with the given profile ID. |
| POST | api/profile-subscription-bulk-create-jobs | write | profiles | Subscribe one or more profiles to email marketing, SMS marketing, WhatsApp, or push. |
| POST | api/profile-subscription-bulk-delete-jobs | write | profiles | > 🚧 > > Profiles not in the specified list will be globally unsubscribed. |
| GET | api/profile-suppression-bulk-create-jobs | read | profiles | Get the status of all bulk profile suppression jobs. |
| POST | api/profile-suppression-bulk-create-jobs | write | profiles | Manually suppress profiles by email address or specify a segment/list ID to suppress all current members of a segment/list. |
| GET | api/profile-suppression-bulk-create-jobs/{id} | read | profiles | Get the bulk suppress profiles job with the given job ID. |
| GET | api/profile-suppression-bulk-delete-jobs | read | profiles | Get all bulk unsuppress profiles jobs. |
| POST | api/profile-suppression-bulk-delete-jobs | write | profiles | Manually unsuppress profiles by email address or specify a segment/list ID to unsuppress all current members of a segment/list. |
| GET | api/profile-suppression-bulk-delete-jobs/{id} | read | profiles | Get the bulk unsuppress profiles job with the given job ID. |
| GET | api/profiles | read | profiles | Get all profiles in an account. |
| POST | api/profiles | write | profiles | Create a new profile. |
| GET | api/profiles/{id} | read | profiles | Get the profile with the given profile ID. |
| PATCH | api/profiles/{id} | write | profiles | Update the profile with the given profile ID. |
| GET | api/profiles/{id}/conversation | read | profiles | Get the conversation for a profile with the given profile ID. |
| GET | api/profiles/{id}/conversations | read | profiles | Get all conversations for a profile with the given profile ID. |
| GET | api/profiles/{id}/lists | read | profiles | Get list memberships for a profile with the given profile ID. |
| GET | api/profiles/{id}/push-tokens | read | profiles | Return all push tokens that belong to the given profile. |
| GET | api/profiles/{id}/relationships/conversation | read | profiles | Get the conversation relationship for a profile with the given profile ID. |
| GET | api/profiles/{id}/relationships/conversations | read | profiles | Get the IDs of all conversations for a profile across all channels. |
| GET | api/profiles/{id}/relationships/lists | read | profiles | Get list memberships for a profile with the given profile ID. |
| GET | api/profiles/{id}/relationships/push-tokens | read | profiles | Return the IDs of all push tokens associated with the given profile. |
| GET | api/profiles/{id}/relationships/segments | read | profiles | Get segment membership relationships for a profile with the given profile ID. |
| GET | api/profiles/{id}/segments | read | profiles | Get segment memberships for a profile with the given profile ID. |
| GET | api/push-tokens | read | profiles | Return push tokens associated with company. |
| POST | api/push-tokens | write | profiles | Create or update a push token. |
| GET | api/push-tokens/{id} | read | profiles | Return a specific push token based on its ID. |
| DELETE | api/push-tokens/{id} | write | profiles | Delete a specific push token based on its ID. |
| GET | api/push-tokens/{id}/profile | read | profiles | Return the profile associated with the given push token. |
| GET | api/push-tokens/{id}/relationships/profile | read | profiles | Return the ID of the profile associated with the given push token. |
| POST | api/campaign-values-reports | read | reporting | Returns the requested campaign analytics values data. |
| POST | api/flow-series-reports | read | reporting | Returns the requested flow analytics series data. |
| POST | api/flow-values-reports | read | reporting | Returns the requested flow analytics values data. |
| POST | api/form-series-reports | read | reporting | Returns the requested form analytics series data. |
| POST | api/form-values-reports | read | reporting | Returns the requested form analytics values data. |
| POST | api/segment-series-reports | read | reporting | Returns the requested segment analytics series data. |
| POST | api/segment-values-reports | read | reporting | Returns the requested segment analytics values data. |
| GET | api/reviews | read | reviews | Get all reviews. |
| GET | api/reviews/{id} | read | reviews | Get the review with the given ID. |
| PATCH | api/reviews/{id} | write | reviews | Update a review. |
| GET | api/segments | read | segments | Get all segments in an account. |
| POST | api/segments | write | segments | Create a segment. |
| GET | api/segments/{id} | read | segments | Get a segment with the given segment ID. |
| PATCH | api/segments/{id} | write | segments | Update a segment with the given segment ID. |
| DELETE | api/segments/{id} | write | segments | Delete a segment with the given segment ID. |
| GET | api/segments/{id}/flow-triggers | read | segments | Get all flows where the given segment ID is being used as the trigger. |
| GET | api/segments/{id}/profiles | read | segments | Get all profiles within a segment with the given segment ID. |
| GET | api/segments/{id}/relationships/flow-triggers | read | segments | Get the IDs of all flows where the given segment is being used as the trigger. |
| GET | api/segments/{id}/relationships/profiles | read | segments | Get all profile membership relationships for the given segment ID. |
| GET | api/segments/{id}/relationships/tags | read | segments | If `related_resource` is `tags`, returns the tag IDs of all tags associated with the given segment ID. |
| GET | api/segments/{id}/tags | read | segments | Return all tags associated with the given segment ID. |
| GET | api/tag-groups | read | tags | List all tag groups in an account. |
| POST | api/tag-groups | write | tags | Create a tag group. |
| GET | api/tag-groups/{id} | read | tags | Retrieve the tag group with the given tag group ID. |
| PATCH | api/tag-groups/{id} | write | tags | Update the tag group with the given tag group ID. |
| DELETE | api/tag-groups/{id} | write | tags | Delete the tag group with the given tag group ID. |
| GET | api/tag-groups/{id}/relationships/tags | read | tags | Returns the tag IDs of all tags inside the given tag group. |
| GET | api/tag-groups/{id}/tags | read | tags | Return the tags for a given tag group ID. |
| GET | api/tags | read | tags | List all tags in an account. |
| POST | api/tags | write | tags | Create a tag. |
| GET | api/tags/{id} | read | tags | Retrieve the tag with the given tag ID. |
| PATCH | api/tags/{id} | write | tags | Update the tag with the given tag ID. |
| DELETE | api/tags/{id} | write | tags | Delete the tag with the given tag ID. |
| GET | api/tags/{id}/relationships/campaigns | read | tags | Returns the IDs of all campaigns associated with the given tag. |
| POST | api/tags/{id}/relationships/campaigns | write | tags | Associate a tag with one or more campaigns. |
| DELETE | api/tags/{id}/relationships/campaigns | write | tags | Remove a tag's association with one or more campaigns. |
| GET | api/tags/{id}/relationships/flows | read | tags | Returns the IDs of all flows associated with the given tag. |
| POST | api/tags/{id}/relationships/flows | write | tags | Associate a tag with one or more flows. |
| DELETE | api/tags/{id}/relationships/flows | write | tags | Remove a tag's association with one or more flows. |
| GET | api/tags/{id}/relationships/lists | read | tags | Returns the IDs of all lists associated with the given tag. |
| POST | api/tags/{id}/relationships/lists | write | tags | Associate a tag with one or more lists. |
| DELETE | api/tags/{id}/relationships/lists | write | tags | Remove a tag's association with one or more lists. |
| GET | api/tags/{id}/relationships/segments | read | tags | Returns the IDs of all segments associated with the given tag. |
| POST | api/tags/{id}/relationships/segments | write | tags | Associate a tag with one or more segments. |
| DELETE | api/tags/{id}/relationships/segments | write | tags | Remove a tag's association with one or more segments. |
| GET | api/tags/{id}/relationships/tag-group | read | tags | Returns the id of the tag group related to the given tag. |
| GET | api/tags/{id}/tag-group | read | tags | Returns the tag group resource for a given tag ID. |
| POST | api/template-clone | write | templates | Create a clone of a template with the given template ID. |
| GET | api/template-conversion-jobs | read | templates | Get the template conversion jobs created in the last 7 days, newest first. |
| POST | api/template-conversion-jobs | write | templates | Convert an HTML template into a new drag-and-drop template. |
| GET | api/template-conversion-jobs/{id} | read | templates | Get a template conversion job with the given job ID. |
| POST | api/template-preview-send-jobs | write | templates | Send a test email of a template to one or more recipients. |
| POST | api/template-render | read | templates | Render a template with the given template ID and context attribute. |
| GET | api/template-universal-content | read | templates | Get all universal content in an account. |
| POST | api/template-universal-content | write | templates | Create universal content. |
| POST | api/template-universal-content-clone | write | templates | Create a clone of the universal content with the given ID. |
| GET | api/template-universal-content/{id} | read | templates | Get the universal content with the given ID. |
| PATCH | api/template-universal-content/{id} | write | templates | Update universal content. |
| DELETE | api/template-universal-content/{id} | write | templates | Delete the universal content with the given ID. |
| GET | api/templates | read | templates | Get all templates in an account. |
| POST | api/templates | write | templates | Create a new HTML or drag-and-drop template. |
| GET | api/templates/{id} | read | templates | Get a template with the given template ID. |
| PATCH | api/templates/{id} | write | templates | Update a template with the given template ID. |
| DELETE | api/templates/{id} | write | templates | Delete a template with the given template ID. |
| POST | api/text-messaging-configurations | write | text-messaging | Create the SMS account for the calling company. |
| GET | api/text-messaging-configurations/{id} | read | text-messaging | Retrieve the SMS account for the calling company. |
| POST | api/text-messaging-sender-registrations | write | text-messaging | Submit a new registration for an existing sender (resubmission). |
| GET | api/text-messaging-sender-registrations/{id} | read | text-messaging | Retrieve a sender registration by ID. |
| GET | api/text-messaging-senders | read | text-messaging | List the calling company's text-messaging senders. |
| POST | api/text-messaging-senders | write | text-messaging | Create a sender and submit its initial registration. |
| GET | api/text-messaging-senders/{id} | read | text-messaging | Retrieve a single text-messaging sender by ID. |
| GET | api/text-messaging-senders/{id}/relationships/text-messaging-sender-registration | read | text-messaging | Return the most-recent registration for the given sender. |
| GET | api/text-messaging-senders/{id}/text-messaging-sender-registration | read | text-messaging | Return the most-recent registration for the given sender. |
| GET | api/tracking-settings | read | tracking-settings | Get all UTM tracking settings in an account. |
| GET | api/tracking-settings/{id} | read | tracking-settings | Get the UTM tracking setting with the given account ID. |
| PATCH | api/tracking-settings/{id} | write | tracking-settings | Update the UTM tracking setting with the given account ID. |
| GET | api/translations | read | translations | Get all translations in an account. |
| POST | api/translations | write | translations | Create a translation. |
| GET | api/translations/{id} | read | translations | Get the translation with the given ID. |
| PATCH | api/translations/{id} | write | translations | Update the translation with the given ID. |
| DELETE | api/translations/{id} | write | translations | Delete the translation with the given ID. |
| GET | api/translations/{id}/campaign-variation | read | translations | Get the campaign variation for the given translation ID. |
| GET | api/translations/{id}/flow-message | read | translations | Get the flow message for the given translation ID. |
| GET | api/translations/{id}/relationships/campaign-variation | read | translations | Get the campaign variation for the given translation ID. |
| GET | api/translations/{id}/relationships/flow-message | read | translations | Get the flow message for the given translation ID. |
| GET | api/translations/{id}/relationships/template | read | translations | Get the template for the given translation ID. |
| GET | api/translations/{id}/relationships/template-universal-content | read | translations | Get the template universal content for the given translation ID. |
| GET | api/translations/{id}/template | read | translations | Get the template for the given translation ID. |
| GET | api/translations/{id}/template-universal-content | read | translations | Get the template universal content for the given translation ID. |
| GET | api/web-feeds | read | web-feeds | Get all web feeds for an account. |
| POST | api/web-feeds | write | web-feeds | Create a web feed. |
| GET | api/web-feeds/{id} | read | web-feeds | Get the web feed with the given ID. |
| PATCH | api/web-feeds/{id} | write | web-feeds | Update the web feed with the given ID. |
| DELETE | api/web-feeds/{id} | write | web-feeds | Delete the web feed with the given ID. |
| GET | api/webhook-topics | read | webhooks | Get all webhook topics in a Klaviyo account. |
| GET | api/webhook-topics/{id} | read | webhooks | Get the webhook topic with the given ID. |
| GET | api/webhooks | read | webhooks | Get all webhooks in an account. |
| POST | api/webhooks | write | webhooks | Create a new Webhook. |
| GET | api/webhooks/{id} | read | webhooks | Get the webhook with the given ID. |
| PATCH | api/webhooks/{id} | write | webhooks | Update the webhook with the given ID. |
| DELETE | api/webhooks/{id} | write | webhooks | Delete a webhook with the given ID. |
