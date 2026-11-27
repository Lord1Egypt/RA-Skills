# Gumroad access policy

An access policy limits which endpoints Gumroad connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/gumroad#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Gumroad: its 54 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create gumroad --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v2/products/{id}/builds"},
    {"method": "GET", "path": "v2/products/{id}/builds/{id}"},
    {"method": "GET", "path": "v2/categories"},
    {"method": "GET", "path": "v2/products/{id}/custom_fields"},
    {"method": "GET", "path": "v2/earnings"},
    {"method": "GET", "path": "v2/emails"},
    {"method": "GET", "path": "v2/emails/{id}"},
    {"method": "GET", "path": "v2/help/articles"},
    {"method": "GET", "path": "v2/help/articles/{id}"},
    {"method": "GET", "path": "v2/marketing_actions/{id}"},
    {"method": "GET", "path": "v2/products/{id}/marketing/recommendations"},
    {"method": "GET", "path": "v2/media"},
    {"method": "GET", "path": "v2/offer_codes"},
    {"method": "GET", "path": "v2/offer_codes/{id}"},
    {"method": "GET", "path": "v2/products/{id}/offer_codes"},
    {"method": "GET", "path": "v2/products/{id}/offer_codes/{id}"},
    {"method": "GET", "path": "v2/pages"},
    {"method": "GET", "path": "v2/pages/{id}"},
    {"method": "GET", "path": "v2/partner/categories"},
    {"method": "GET", "path": "v2/partner/creators/top"},
    {"method": "GET", "path": "v2/partner/migrations/{id}"},
    {"method": "GET", "path": "v2/partner/products"},
    {"method": "GET", "path": "v2/payouts"},
    {"method": "GET", "path": "v2/payouts/upcoming"},
    {"method": "GET", "path": "v2/payouts/{id}"},
    {"method": "GET", "path": "v2/products"},
    {"method": "GET", "path": "v2/products/comps"},
    {"method": "GET", "path": "v2/products/{id}"},
    {"method": "GET", "path": "v2/products/{id}/custom_html"},
    {"method": "GET", "path": "v2/refund_policy"},
    {"method": "GET", "path": "v2/resource_subscriptions"},
    {"method": "GET", "path": "v2/products/{id}/reviews"},
    {"method": "GET", "path": "v2/sales"},
    {"method": "GET", "path": "v2/sales/summary"},
    {"method": "GET", "path": "v2/sales/{id}"},
    {"method": "GET", "path": "v2/products/{id}/skus"},
    {"method": "GET", "path": "v2/products/{id}/subscribers"},
    {"method": "GET", "path": "v2/subscribers/{id}"},
    {"method": "GET", "path": "v2/tax_forms"},
    {"method": "GET", "path": "v2/tax_forms/{id}/{id}/download"},
    {"method": "GET", "path": "v2/upsells"},
    {"method": "GET", "path": "v2/upsells/{id}"},
    {"method": "GET", "path": "v2/user"},
    {"method": "GET", "path": "v2/user/custom_html"},
    {"method": "GET", "path": "v2/user/profile_layout"},
    {"method": "GET", "path": "v2/user/theme"},
    {"method": "GET", "path": "v2/utm_links"},
    {"method": "GET", "path": "v2/utm_links/{id}"},
    {"method": "GET", "path": "v2/products/{id}/variant_categories"},
    {"method": "GET", "path": "v2/products/{id}/variant_categories/{id}"},
    {"method": "GET", "path": "v2/products/{id}/variant_categories/{id}/variants"},
    {"method": "GET", "path": "v2/products/{id}/variant_categories/{id}/variants/{id}"},
    {"method": "GET", "path": "v2/workflows"},
    {"method": "GET", "path": "v2/workflows/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Gumroad endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v2/products/{id}/builds | read | builds | List builds of a product. |
| POST | v2/products/{id}/builds/deploy | write | builds | Deploy a build of a product. |
| GET | v2/products/{id}/builds/{id} | read | builds | Retrieve a build of a product. |
| POST | v2/products/{id}/builds/{id}/demo | write | builds | Select a build as the demo. |
| DELETE | v2/products/{id}/builds/{id}/demo | write | builds | Unselect the demo build. |
| POST | v2/products/{id}/builds/{id}/promote | write | builds | Promote a build. |
| GET | v2/categories | read | categories | List categories. |
| POST | v2/products/{id}/covers | write | covers | Add a product cover. |
| DELETE | v2/products/{id}/covers/{id} | write | covers | Delete a product cover. |
| GET | v2/products/{id}/custom_fields | read | custom_fields | List custom fields. |
| POST | v2/products/{id}/custom_fields | write | custom_fields | Create a custom field. |
| PUT | v2/products/{id}/custom_fields/{id} | write | custom_fields | Update a custom field. |
| PATCH | v2/products/{id}/custom_fields/{id} | write | custom_fields | Update a custom field. |
| DELETE | v2/products/{id}/custom_fields/{id} | write | custom_fields | Delete a custom field. |
| GET | v2/earnings | read | earnings | Retrieve earnings. |
| GET | v2/emails | read | emails | List emails. |
| POST | v2/emails | write | emails | Create a email. |
| GET | v2/emails/{id} | read | emails | Retrieve a email. |
| DELETE | v2/emails/{id} | write | emails | Delete a email. |
| POST | v2/emails/{id}/preview | write | emails | Send a preview of an email. |
| POST | v2/emails/{id}/schedule | write | emails | Schedule an email. |
| POST | v2/emails/{id}/send | write | emails | Send an email to its audience. |
| POST | v2/emails/{id}/unschedule | write | emails | Unschedule an email. |
| POST | v2/direct_uploads | write | files | Create a direct upload. |
| POST | v2/files/abort | write | files | Abort a multipart file upload. |
| POST | v2/files/complete | write | files | Complete a multipart file upload. |
| POST | v2/files/presign | write | files | Get a presigned URL for a file upload. |
| GET | v2/help/articles | read | help | List help center articles. |
| GET | v2/help/articles/{id} | read | help | Retrieve a help center article by slug. |
| PUT | v2/licenses/decrement_uses_count | write | licenses | Decrement the use count of a license key. |
| PUT | v2/licenses/disable | write | licenses | Disable a license key. |
| PUT | v2/licenses/enable | write | licenses | Enable a license key. |
| PUT | v2/licenses/rotate | write | licenses | Rotate a license key. |
| POST | v2/licenses/verify | write | licenses | Verify a license key. Kept out of read: increments the license use count by default. |
| GET | v2/marketing_actions/{id} | read | marketing | Retrieve a marketing action. |
| POST | v2/marketing_actions/{id}/approve | write | marketing | Approve a marketing action. |
| POST | v2/marketing_actions/{id}/cancel | write | marketing | Cancel a marketing action. |
| POST | v2/marketing_actions/{id}/execute | write | marketing | Execute a marketing action. |
| GET | v2/products/{id}/marketing/recommendations | read | marketing | List marketing recommendations for a product. |
| POST | v2/products/{id}/marketing_actions | write | marketing | Create a marketing action for a product. |
| GET | v2/media | read | media | List media items. |
| POST | v2/media | write | media | Create a media item. |
| DELETE | v2/media/{id} | write | media | Delete a media item. |
| GET | v2/offer_codes | read | offer_codes | List offer codes. |
| GET | v2/offer_codes/{id} | read | offer_codes | Retrieve a offer code. |
| PUT | v2/offer_codes/{id} | write | offer_codes | Update a offer code. |
| PATCH | v2/offer_codes/{id} | write | offer_codes | Update a offer code. |
| GET | v2/products/{id}/offer_codes | read | offer_codes | List offer codes. |
| POST | v2/products/{id}/offer_codes | write | offer_codes | Create a offer code. |
| GET | v2/products/{id}/offer_codes/{id} | read | offer_codes | Retrieve a offer code. |
| PUT | v2/products/{id}/offer_codes/{id} | write | offer_codes | Update a offer code. |
| PATCH | v2/products/{id}/offer_codes/{id} | write | offer_codes | Update a offer code. |
| DELETE | v2/products/{id}/offer_codes/{id} | write | offer_codes | Delete a offer code. |
| GET | v2/pages | read | pages | List pages. |
| POST | v2/pages | write | pages | Create a page. |
| GET | v2/pages/{id} | read | pages | Retrieve a page. |
| PUT | v2/pages/{id} | write | pages | Update a page. |
| PATCH | v2/pages/{id} | write | pages | Update a page. |
| DELETE | v2/pages/{id} | write | pages | Delete a page. |
| GET | v2/partner/categories | read | partner | List partner categories. |
| GET | v2/partner/creators/top | read | partner | List top creators. |
| POST | v2/partner/migrations | write | partner | Create a partner migration. |
| GET | v2/partner/migrations/{id} | read | partner | Retrieve a partner migration. |
| GET | v2/partner/products | read | partner | List partner products. |
| POST | v2/partner/sellers | write | partner | Create a partner seller. |
| GET | v2/payouts | read | payouts | List payouts. |
| GET | v2/payouts/upcoming | read | payouts | List upcoming payouts. |
| GET | v2/payouts/{id} | read | payouts | Retrieve a payout. |
| GET | v2/products | read | products | List products. |
| POST | v2/products | write | products | Create a product. |
| GET | v2/products/comps | read | products | List comp products. |
| GET | v2/products/{id} | read | products | Retrieve a product. |
| PUT | v2/products/{id} | write | products | Update a product. |
| PATCH | v2/products/{id} | write | products | Update a product. |
| DELETE | v2/products/{id} | write | products | Delete a product. |
| PUT | v2/products/{id}/bundle_contents | write | products | Update the bundle contents of a product. |
| GET | v2/products/{id}/custom_html | read | products | Retrieve the custom HTML of a product. |
| POST | v2/products/{id}/custom_html/edit | write | products | Edit the custom HTML of a product. |
| PUT | v2/products/{id}/disable | write | products | Disable a product. |
| PUT | v2/products/{id}/enable | write | products | Enable a product. |
| POST | v2/products/{id}/preview_custom_html | write | products | Preview custom HTML for a product. |
| PUT | v2/products/{id}/sections | write | products | Update the profile sections of a product. |
| POST | v2/products/{id}/thumbnail | write | products | Upload a product thumbnail. |
| DELETE | v2/products/{id}/thumbnail | write | products | Delete a product thumbnail. |
| GET | v2/refund_policy | read | refund_policy | Retrieve the refund policy. |
| PUT | v2/refund_policy | write | refund_policy | Update the refund policy. |
| PATCH | v2/refund_policy | write | refund_policy | Update the refund policy. |
| GET | v2/resource_subscriptions | read | resource_subscriptions | List resource subscriptions (webhooks). |
| PUT | v2/resource_subscriptions | write | resource_subscriptions | Subscribe to a resource (webhook). |
| DELETE | v2/resource_subscriptions/{id} | write | resource_subscriptions | Unsubscribe from a resource (webhook). |
| POST | v2/resource_subscriptions/{id}/test_event | write | resource_subscriptions | Send a test event to a resource subscription. |
| GET | v2/products/{id}/reviews | read | reviews | List reviews of a product. |
| GET | v2/sales | read | sales | List sales. |
| POST | v2/sales/exports | write | sales | Request an export of sales. |
| GET | v2/sales/summary | read | sales | Retrieve a summary of sales. |
| GET | v2/sales/{id} | read | sales | Retrieve a sale. |
| PUT | v2/sales/{id}/mark_as_shipped | write | sales | Mark a sale as shipped. |
| PUT | v2/sales/{id}/refund | write | sales | Refund a sale. |
| POST | v2/sales/{id}/resend_receipt | write | sales | Resend the receipt of a sale. |
| PUT | v2/sales/{id}/revoke_access | write | sales | Revoke access for a sale. |
| PUT | v2/sales/{id}/undo_revoke_access | write | sales | Undo revoking access for a sale. |
| GET | v2/products/{id}/skus | read | skus | List SKUs of a product. |
| GET | v2/products/{id}/subscribers | read | subscribers | List subscribers of a product. |
| GET | v2/subscribers/{id} | read | subscribers | Retrieve a subscriber. |
| GET | v2/tax_forms | read | tax_forms | List tax forms. |
| GET | v2/tax_forms/{id}/{id}/download | read | tax_forms | Download a tax form. |
| GET | v2/upsells | read | upsells | List upsells. |
| POST | v2/upsells | write | upsells | Create a upsell. |
| GET | v2/upsells/{id} | read | upsells | Retrieve a upsell. |
| PUT | v2/upsells/{id} | write | upsells | Update a upsell. |
| PATCH | v2/upsells/{id} | write | upsells | Update a upsell. |
| DELETE | v2/upsells/{id} | write | upsells | Delete a upsell. |
| GET | v2/user | read | user | Retrieve the authenticated user. |
| PUT | v2/user | write | user | Update the authenticated user. |
| PATCH | v2/user | write | user | Update the authenticated user. |
| GET | v2/user/custom_html | read | user | Retrieve the profile custom HTML. |
| PUT | v2/user/custom_html | write | user | Update the profile custom HTML. |
| PATCH | v2/user/custom_html | write | user | Update the profile custom HTML. |
| POST | v2/user/custom_html/edit | write | user | Edit the profile custom HTML. |
| POST | v2/user/preview_custom_html | write | user | Preview custom HTML for the profile. |
| GET | v2/user/profile_layout | read | user | Retrieve the seller profile tabs and sections. |
| GET | v2/user/theme | read | user | Retrieve the seller store theme. |
| GET | v2/utm_links | read | utm_links | List UTM links. |
| POST | v2/utm_links | write | utm_links | Create a UTM link. |
| GET | v2/utm_links/{id} | read | utm_links | Retrieve a UTM link. |
| PUT | v2/utm_links/{id} | write | utm_links | Update a UTM link. |
| PATCH | v2/utm_links/{id} | write | utm_links | Update a UTM link. |
| DELETE | v2/utm_links/{id} | write | utm_links | Delete a UTM link. |
| PUT | v2/utm_links/{id}/disable | write | utm_links | Disable a UTM link. |
| PUT | v2/utm_links/{id}/enable | write | utm_links | Enable a UTM link. |
| GET | v2/products/{id}/variant_categories | read | variant_categories | List variant categories. |
| POST | v2/products/{id}/variant_categories | write | variant_categories | Create a variant category. |
| GET | v2/products/{id}/variant_categories/{id} | read | variant_categories | Retrieve a variant category. |
| PUT | v2/products/{id}/variant_categories/{id} | write | variant_categories | Update a variant category. |
| PATCH | v2/products/{id}/variant_categories/{id} | write | variant_categories | Update a variant category. |
| DELETE | v2/products/{id}/variant_categories/{id} | write | variant_categories | Delete a variant category. |
| GET | v2/products/{id}/variant_categories/{id}/variants | read | variants | List variants. |
| POST | v2/products/{id}/variant_categories/{id}/variants | write | variants | Create a variant. |
| GET | v2/products/{id}/variant_categories/{id}/variants/{id} | read | variants | Retrieve a variant. |
| PUT | v2/products/{id}/variant_categories/{id}/variants/{id} | write | variants | Update a variant. |
| PATCH | v2/products/{id}/variant_categories/{id}/variants/{id} | write | variants | Update a variant. |
| DELETE | v2/products/{id}/variant_categories/{id}/variants/{id} | write | variants | Delete a variant. |
| GET | v2/workflows | read | workflows | List workflows. |
| GET | v2/workflows/{id} | read | workflows | Retrieve a workflow. |
| POST | v2/workflows/{id}/emails | write | workflows | Create an email in a workflow. |
| PUT | v2/workflows/{id}/emails/{id} | write | workflows | Update an email in a workflow. |
| PATCH | v2/workflows/{id}/emails/{id} | write | workflows | Update an email in a workflow. |
