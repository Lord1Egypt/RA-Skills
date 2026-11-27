# Keap access policy

An access policy limits which endpoints Keap connections may call through Maton. Keap doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/keap#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Keap: its 165 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create keap --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "crm/rest/v2/affiliates"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/commissionPrograms"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/commissionPrograms/{id}"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/commissionPrograms/{id}/resources"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/model"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/model/customFields/groups"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/model/customFields/groups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/model/customFields/tabs"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/model/customFields/tabs/{id}"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/redirects"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/redirects/{id}"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/summaries"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/{id}"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/{id}/commissionTotal"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/{id}/payments"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/{id}/referrals"},
    {"method": "GET", "path": "crm/rest/v2/affiliates/{id}:commissions"},
    {"method": "GET", "path": "crm/rest/v2/automations"},
    {"method": "GET", "path": "crm/rest/v2/automations/ids"},
    {"method": "GET", "path": "crm/rest/v2/automations/{id}"},
    {"method": "GET", "path": "crm/rest/v2/automationCategory"},
    {"method": "GET", "path": "crm/rest/v2/businessProfile"},
    {"method": "GET", "path": "crm/rest/v2/campaigns"},
    {"method": "GET", "path": "crm/rest/v2/campaigns/{id}"},
    {"method": "GET", "path": "crm/rest/v2/campaigns/{id}/goals"},
    {"method": "GET", "path": "crm/rest/v2/campaigns/{id}/sequences"},
    {"method": "GET", "path": "crm/rest/v2/discounts/productCategories"},
    {"method": "GET", "path": "crm/rest/v2/discounts/productCategories/{id}"},
    {"method": "GET", "path": "crm/rest/v2/companies"},
    {"method": "GET", "path": "crm/rest/v2/companies/model"},
    {"method": "GET", "path": "crm/rest/v2/companies/model/customFields/groups"},
    {"method": "GET", "path": "crm/rest/v2/companies/model/customFields/groups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/companies/model/customFields/tabs"},
    {"method": "GET", "path": "crm/rest/v2/companies/model/customFields/tabs/{id}"},
    {"method": "GET", "path": "crm/rest/v2/companies/{id}"},
    {"method": "GET", "path": "crm/rest/v2/companies/{id}/tags"},
    {"method": "GET", "path": "crm/rest/v2/contacts"},
    {"method": "GET", "path": "crm/rest/v2/contacts/-/tags"},
    {"method": "GET", "path": "crm/rest/v2/contacts/links/types"},
    {"method": "GET", "path": "crm/rest/v2/contacts/model"},
    {"method": "GET", "path": "crm/rest/v2/contacts/model/customFields/groups"},
    {"method": "GET", "path": "crm/rest/v2/contacts/model/customFields/groups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/contacts/model/customFields/tabs"},
    {"method": "GET", "path": "crm/rest/v2/contacts/model/customFields/tabs/{id}"},
    {"method": "GET", "path": "crm/rest/v2/contacts/{id}"},
    {"method": "GET", "path": "crm/rest/v2/contacts/{id}/links"},
    {"method": "GET", "path": "crm/rest/v2/contacts/{id}/tags"},
    {"method": "GET", "path": "crm/rest/v2/emails"},
    {"method": "GET", "path": "crm/rest/v2/emails/templates"},
    {"method": "GET", "path": "crm/rest/v2/emails/templates/{id}"},
    {"method": "GET", "path": "crm/rest/v2/emails/{id}"},
    {"method": "GET", "path": "crm/rest/v2/emailAddresses"},
    {"method": "GET", "path": "crm/rest/v2/emailAddresses/{id}/status"},
    {"method": "GET", "path": "crm/rest/v2/files"},
    {"method": "GET", "path": "crm/rest/v2/files/{id}"},
    {"method": "GET", "path": "crm/rest/v2/files/{id}:data"},
    {"method": "GET", "path": "crm/rest/v2/discounts/freeTrials"},
    {"method": "GET", "path": "crm/rest/v2/discounts/freeTrials/{id}"},
    {"method": "GET", "path": "crm/rest/v2/integrations/wordpress/options"},
    {"method": "GET", "path": "crm/rest/v2/leadSourceCategories"},
    {"method": "GET", "path": "crm/rest/v2/leadSourceCategories/{id}"},
    {"method": "GET", "path": "crm/rest/v2/leadSources/{id}/expenses"},
    {"method": "GET", "path": "crm/rest/v2/leadSources/{id}/expenses/{id}"},
    {"method": "GET", "path": "crm/rest/v2/leadSources/{id}/recurringExpenses"},
    {"method": "GET", "path": "crm/rest/v2/leadSources/{id}/recurringExpenses/{id}"},
    {"method": "GET", "path": "crm/rest/v2/leadSources/{id}/recurringExpenses/{id}/expenses"},
    {"method": "GET", "path": "crm/rest/v2/leadSources"},
    {"method": "GET", "path": "crm/rest/v2/leadSources/{id}"},
    {"method": "GET", "path": "crm/rest/v2/contacts/{id}/leadScore"},
    {"method": "GET", "path": "crm/rest/v2/locales/countries"},
    {"method": "GET", "path": "crm/rest/v2/locales/countries/{id}"},
    {"method": "GET", "path": "crm/rest/v2/locales/countries/{id}/provinces"},
    {"method": "GET", "path": "crm/rest/v2/locales/countries/{id}/provinces/{id}"},
    {"method": "GET", "path": "crm/rest/v2/merchants"},
    {"method": "GET", "path": "crm/rest/v2/contacts/{id}/notes"},
    {"method": "GET", "path": "crm/rest/v2/contacts/{id}/notes/{id}"},
    {"method": "GET", "path": "crm/rest/v2/notes"},
    {"method": "GET", "path": "crm/rest/v2/notes/model"},
    {"method": "GET", "path": "crm/rest/v2/notes/model/customFields/groups"},
    {"method": "GET", "path": "crm/rest/v2/notes/model/customFields/groups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/notes/model/customFields/tabs"},
    {"method": "GET", "path": "crm/rest/v2/notes/model/customFields/tabs/{id}"},
    {"method": "GET", "path": "crm/rest/v2/notes/templates"},
    {"method": "GET", "path": "crm/rest/v2/opportunities"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/model"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/model/customFields/groups"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/model/customFields/groups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/model/customFields/tabs"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/model/customFields/tabs/{id}"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/stageMoves"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/stageMoves/{id}"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/stages"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/stages/{id}"},
    {"method": "GET", "path": "crm/rest/v2/opportunities/{id}"},
    {"method": "GET", "path": "crm/rest/v2/discounts/orderTotals"},
    {"method": "GET", "path": "crm/rest/v2/discounts/orderTotals/{id}"},
    {"method": "GET", "path": "crm/rest/v2/orders"},
    {"method": "GET", "path": "crm/rest/v2/orders/model"},
    {"method": "GET", "path": "crm/rest/v2/orders/model/customFields/groups"},
    {"method": "GET", "path": "crm/rest/v2/orders/model/customFields/groups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/orders/model/customFields/tabs"},
    {"method": "GET", "path": "crm/rest/v2/orders/model/customFields/tabs/{id}"},
    {"method": "GET", "path": "crm/rest/v2/orders/{id}"},
    {"method": "GET", "path": "crm/rest/v2/orders/{id}/items/{id}"},
    {"method": "GET", "path": "crm/rest/v2/orders/{id}/payments"},
    {"method": "GET", "path": "crm/rest/v2/contacts/{id}/paymentMethods"},
    {"method": "GET", "path": "crm/rest/v2/paymentMethods"},
    {"method": "GET", "path": "crm/rest/v2/productCategories"},
    {"method": "GET", "path": "crm/rest/v2/productCategories/assignedProducts"},
    {"method": "GET", "path": "crm/rest/v2/productCategories/{id}"},
    {"method": "GET", "path": "crm/rest/v2/discounts/products"},
    {"method": "GET", "path": "crm/rest/v2/discounts/products/{id}"},
    {"method": "GET", "path": "crm/rest/v2/productInterestBundles"},
    {"method": "GET", "path": "crm/rest/v2/productInterestBundles/{id}"},
    {"method": "GET", "path": "crm/rest/v2/products"},
    {"method": "GET", "path": "crm/rest/v2/products/{id}"},
    {"method": "GET", "path": "crm/rest/v2/products/{id}/images/legacyImageData"},
    {"method": "GET", "path": "crm/rest/v2/products/{id}/options"},
    {"method": "GET", "path": "crm/rest/v2/products/{id}/options/{id}"},
    {"method": "GET", "path": "crm/rest/v2/referrals"},
    {"method": "GET", "path": "crm/rest/v2/reporting/reports"},
    {"method": "GET", "path": "crm/rest/v2/reporting/reports/{id}"},
    {"method": "GET", "path": "crm/rest/v2/reporting/reports/{id}/model"},
    {"method": "POST", "path": "crm/rest/v2/reporting/reports/{id}:run"},
    {"method": "GET", "path": "crm/rest/v2/sales/payments"},
    {"method": "GET", "path": "crm/rest/v2/sales/transactions"},
    {"method": "GET", "path": "crm/rest/v2/settings/applications:getConfiguration"},
    {"method": "GET", "path": "crm/rest/v2/settings/applications:isEnabled"},
    {"method": "GET", "path": "crm/rest/v2/settings/contactOptionTypes"},
    {"method": "GET", "path": "crm/rest/v2/shipping"},
    {"method": "GET", "path": "crm/rest/v2/discounts/shipping"},
    {"method": "GET", "path": "crm/rest/v2/discounts/shipping/{id}"},
    {"method": "GET", "path": "crm/rest/v2/products/{id}/subscriptions"},
    {"method": "GET", "path": "crm/rest/v2/products/{id}/subscriptions/{id}"},
    {"method": "GET", "path": "crm/rest/v2/subscriptions"},
    {"method": "GET", "path": "crm/rest/v2/subscriptions/model"},
    {"method": "GET", "path": "crm/rest/v2/subscriptions/model/customFields/groups"},
    {"method": "GET", "path": "crm/rest/v2/subscriptions/model/customFields/groups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/subscriptions/model/customFields/tabs"},
    {"method": "GET", "path": "crm/rest/v2/subscriptions/model/customFields/tabs/{id}"},
    {"method": "GET", "path": "crm/rest/v2/subscriptions/{id}"},
    {"method": "GET", "path": "crm/rest/v2/tags"},
    {"method": "GET", "path": "crm/rest/v2/tags/-/contacts"},
    {"method": "GET", "path": "crm/rest/v2/tags/categories"},
    {"method": "GET", "path": "crm/rest/v2/tags/categories/{id}"},
    {"method": "GET", "path": "crm/rest/v2/tags/{id}"},
    {"method": "GET", "path": "crm/rest/v2/tags/{id}/companies"},
    {"method": "GET", "path": "crm/rest/v2/tags/{id}/contacts"},
    {"method": "GET", "path": "crm/rest/v2/tags/{id}/contacts/count"},
    {"method": "GET", "path": "crm/rest/v2/tasks"},
    {"method": "GET", "path": "crm/rest/v2/tasks/model"},
    {"method": "GET", "path": "crm/rest/v2/tasks/model/customFields/groups"},
    {"method": "GET", "path": "crm/rest/v2/tasks/model/customFields/groups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/tasks/model/customFields/tabs"},
    {"method": "GET", "path": "crm/rest/v2/tasks/model/customFields/tabs/{id}"},
    {"method": "GET", "path": "crm/rest/v2/tasks/{id}"},
    {"method": "GET", "path": "crm/rest/v2/taskAppointments"},
    {"method": "GET", "path": "crm/rest/v2/userGroups"},
    {"method": "GET", "path": "crm/rest/v2/userGroups/{id}"},
    {"method": "GET", "path": "crm/rest/v2/oauth/connect/userinfo"},
    {"method": "GET", "path": "crm/rest/v2/users"},
    {"method": "GET", "path": "crm/rest/v2/users/{id}"},
    {"method": "GET", "path": "crm/rest/v2/users/{id}/signature"},
    {"method": "GET", "path": "crm/rest/v2/webforms"},
    {"method": "GET", "path": "crm/rest/v2/webforms/{id}:data"}
  ],
  "deny": []
}
```

## Endpoints

The Keap endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | crm/rest/v2/affiliates | read | affiliate | Retrieves a list of Affiliates. |
| POST | crm/rest/v2/affiliates | write | affiliate | Creates a single Affiliate. |
| GET | crm/rest/v2/affiliates/commissionPrograms | read | affiliate | Retrieves a list of Affiliate Commission Programs. |
| POST | crm/rest/v2/affiliates/commissionPrograms | write | affiliate | Creates an Affiliate Commission Program. |
| POST | crm/rest/v2/affiliates/commissionPrograms/defaultCommissionPrograms/{id} | write | affiliate | Creates a Default Commission Program. |
| PATCH | crm/rest/v2/affiliates/commissionPrograms/defaultCommissionPrograms/{id} | write | affiliate | Updates a Default Commission Program. |
| POST | crm/rest/v2/affiliates/commissionPrograms/productCommissionPrograms/{id} | write | affiliate | Assigns a Product Commission Program to a Product. |
| PATCH | crm/rest/v2/affiliates/commissionPrograms/productCommissionPrograms/{id} | write | affiliate | Updates a Product Commission Program. |
| POST | crm/rest/v2/affiliates/commissionPrograms/resources | write | affiliate | Creates a resource for a commission program. |
| PATCH | crm/rest/v2/affiliates/commissionPrograms/resources/{id} | write | affiliate | Updates a resource for a commission program. |
| DELETE | crm/rest/v2/affiliates/commissionPrograms/resources/{id} | write | affiliate | Removes a resource from a commission program. |
| POST | crm/rest/v2/affiliates/commissionPrograms/subscriptionCommissionPrograms/{id} | write | affiliate | Assigns a Subscription Commission Program to a Subscription. |
| PATCH | crm/rest/v2/affiliates/commissionPrograms/subscriptionCommissionPrograms/{id} | write | affiliate | Updates a Subscription Commission Program. |
| GET | crm/rest/v2/affiliates/commissionPrograms/{id} | read | affiliate | Retrieves a single Commission Program. |
| PATCH | crm/rest/v2/affiliates/commissionPrograms/{id} | write | affiliate | Updates the properties of an Affiliate Commission Program. |
| DELETE | crm/rest/v2/affiliates/commissionPrograms/{id} | write | affiliate | Deletes a Commission Program. |
| GET | crm/rest/v2/affiliates/commissionPrograms/{id}/resources | read | affiliate | Retrieves resources for a commission program. |
| POST | crm/rest/v2/affiliates/commissionPrograms/{id}:removeProductCommission | write | affiliate | Removes a Product from a Commission Program. |
| POST | crm/rest/v2/affiliates/commissionPrograms/{id}:removeSubscriptionCommission | write | affiliate | Removes a Subscription from a Commission Program. |
| GET | crm/rest/v2/affiliates/model | read | affiliate | Get the custom fields and optional properties for the Affiliate object. |
| POST | crm/rest/v2/affiliates/model/customFields | write | affiliate | Creates a single Affiliate Custom Field. |
| GET | crm/rest/v2/affiliates/model/customFields/groups | read | affiliate | Retrieves a list of custom field groups for the Affiliate record type. |
| POST | crm/rest/v2/affiliates/model/customFields/groups | write | affiliate | Creates a new custom field group for the Affiliate record type. |
| GET | crm/rest/v2/affiliates/model/customFields/groups/{id} | read | affiliate | Retrieves a single custom field group by id for the Affiliate record type. |
| PATCH | crm/rest/v2/affiliates/model/customFields/groups/{id} | write | affiliate | Updates an existing custom field group. |
| DELETE | crm/rest/v2/affiliates/model/customFields/groups/{id} | write | affiliate | Deletes a custom field group. |
| GET | crm/rest/v2/affiliates/model/customFields/tabs | read | affiliate | Retrieves a list of custom field tabs for the Affiliate record type. |
| POST | crm/rest/v2/affiliates/model/customFields/tabs | write | affiliate | Creates a new custom field tab for the Affiliate record type. |
| GET | crm/rest/v2/affiliates/model/customFields/tabs/{id} | read | affiliate | Retrieves a single custom field tab by id for the Affiliate record type. |
| PATCH | crm/rest/v2/affiliates/model/customFields/tabs/{id} | write | affiliate | Updates an existing custom field tab. |
| DELETE | crm/rest/v2/affiliates/model/customFields/tabs/{id} | write | affiliate | Deletes a custom field tab. |
| PATCH | crm/rest/v2/affiliates/model/customFields/{id} | write | affiliate | Updates a custom field of the specified type and options to the Affiliate object. |
| DELETE | crm/rest/v2/affiliates/model/customFields/{id} | write | affiliate | Deletes a Custom Field from Affiliate. |
| GET | crm/rest/v2/affiliates/redirects | read | affiliate | Retrieves a list of Affiliate Links. |
| POST | crm/rest/v2/affiliates/redirects | write | affiliate | Creates a single Affiliate Link. |
| GET | crm/rest/v2/affiliates/redirects/{id} | read | affiliate | Retrieves information about a single Affiliate Link. |
| PATCH | crm/rest/v2/affiliates/redirects/{id} | write | affiliate | Updates an Affiliate Link. |
| DELETE | crm/rest/v2/affiliates/redirects/{id} | write | affiliate | Deletes an Affiliate Link. |
| GET | crm/rest/v2/affiliates/summaries | read | affiliate | Retrieves a list of Affiliate Summaries. |
| GET | crm/rest/v2/affiliates/{id} | read | affiliate | Retrieves a single Affiliate. |
| PATCH | crm/rest/v2/affiliates/{id} | write | affiliate | Updates a single Affiliate. |
| DELETE | crm/rest/v2/affiliates/{id} | write | affiliate | Deletes the specified Affiliate. |
| GET | crm/rest/v2/affiliates/{id}/commissionTotal | read | affiliate | Get the Affiliate Commission Earned and View LedgerURl for portal. |
| GET | crm/rest/v2/affiliates/{id}/payments | read | affiliate | Retrieves a list of affiliate payments. |
| GET | crm/rest/v2/affiliates/{id}/referrals | read | affiliate | Retrieves all referrals belonging to the given affiliate. |
| POST | crm/rest/v2/affiliates/{id}:assignToProgram | write | affiliate | Assigns an Affiliate to Commission Program. |
| GET | crm/rest/v2/affiliates/{id}:commissions | read | affiliate | Retrieve a list of Affiliate's Commissions. |
| POST | crm/rest/v2/affiliates/{id}:removeFromProgram | write | affiliate | Removes an Affiliate from a Commission Program. |
| GET | crm/rest/v2/automations | read | automation | Retrieves a list of automations. |
| DELETE | crm/rest/v2/automations | write | automation | Deletes a single automation. |
| POST | crm/rest/v2/automations/batch-unpublish | write | automation | Bulk unpublish one or more automations. |
| POST | crm/rest/v2/automations/categories/batchAssign | write | automation | Bulk updates the categories of one or more automations. |
| POST | crm/rest/v2/automations/goals/achieve | write | automation | Achieves a goal in an automation for a contact. |
| GET | crm/rest/v2/automations/ids | read | automation | Retrieves a list of automations IDs. |
| GET | crm/rest/v2/automations/{id} | read | automation | Retrieves a single automation. |
| POST | crm/rest/v2/automations/{id}/sequences/{id}:addContacts | write | automation | Adds a list of contacts to an automation sequence. |
| PUT | crm/rest/v2/automations/{id}/unpublish | write | automation | Unpublishes a single automation. |
| GET | crm/rest/v2/automationCategory | read | automationcategory | Retrieves a list of automation categories. |
| POST | crm/rest/v2/automationCategory | write | automationcategory | Creates a single automation category. |
| DELETE | crm/rest/v2/automationCategory | write | automationcategory | Deletes one or more automation categories based on the request parameters. |
| PATCH | crm/rest/v2/automationCategory/{id} | write | automationcategory | Updates part of a single automation category. |
| GET | crm/rest/v2/businessProfile | read | business-profile | Retrieves Business Profile information. |
| PATCH | crm/rest/v2/businessProfile | write | business-profile | Updates Business Profile information. |
| GET | crm/rest/v2/campaigns | read | campaign | Retrieves a list of campaigns for the authenticated user. |
| GET | crm/rest/v2/campaigns/{id} | read | campaign | Retrieves a single campaign. |
| GET | crm/rest/v2/campaigns/{id}/goals | read | campaign | Retrieves a list of Goals (published) for a Campaign. |
| GET | crm/rest/v2/campaigns/{id}/sequences | read | campaign | Retrieves a list of Sequences (published) for a Campaign. |
| POST | crm/rest/v2/campaigns/{id}/sequences/{id}:addContacts | write | campaign | Adds a list of contacts to a campaign sequence. |
| POST | crm/rest/v2/campaigns/{id}/sequences/{id}:removeContacts | write | campaign | Removes a list of contacts from a campaign sequence. |
| GET | crm/rest/v2/discounts/productCategories | read | category-discounts | Retrieves a list of Category Discounts. |
| POST | crm/rest/v2/discounts/productCategories | write | category-discounts | Creates a Category Discount. |
| GET | crm/rest/v2/discounts/productCategories/{id} | read | category-discounts | Retrieves a single Category Discount. |
| PATCH | crm/rest/v2/discounts/productCategories/{id} | write | category-discounts | Updates a Category Discount. |
| DELETE | crm/rest/v2/discounts/productCategories/{id} | write | category-discounts | Deletes a specified Category Discount. |
| POST | crm/rest/v2/discounts/productCategories/{id}/criteria | write | category-discounts | Creates a Category Discount Criteria. |
| DELETE | crm/rest/v2/discounts/productCategories/{id}/criteria/{id} | write | category-discounts | Deletes a specified Category Discount Criteria. |
| GET | crm/rest/v2/companies | read | company | Retrieves a list of all Companies. |
| POST | crm/rest/v2/companies | write | company | Creates a new Company.`country_code` is required if `region` is specified. |
| GET | crm/rest/v2/companies/model | read | company | Get the custom fields for the Company object. |
| POST | crm/rest/v2/companies/model/customFields | write | company | Creates a custom field of the specified type and options to the Company object. |
| GET | crm/rest/v2/companies/model/customFields/groups | read | company | Retrieves a list of custom field groups for the Company record type. |
| POST | crm/rest/v2/companies/model/customFields/groups | write | company | Creates a new custom field group for the Company record type. |
| GET | crm/rest/v2/companies/model/customFields/groups/{id} | read | company | Retrieves a single custom field group by id for the Company record type. |
| PATCH | crm/rest/v2/companies/model/customFields/groups/{id} | write | company | Updates an existing custom field group. |
| DELETE | crm/rest/v2/companies/model/customFields/groups/{id} | write | company | Deletes a custom field group. |
| GET | crm/rest/v2/companies/model/customFields/tabs | read | company | Retrieves a list of custom field tabs for the Company record type. |
| POST | crm/rest/v2/companies/model/customFields/tabs | write | company | Creates a new custom field tab for the Company record type. |
| GET | crm/rest/v2/companies/model/customFields/tabs/{id} | read | company | Retrieves a single custom field tab by id for the Company record type. |
| PATCH | crm/rest/v2/companies/model/customFields/tabs/{id} | write | company | Updates an existing custom field tab. |
| DELETE | crm/rest/v2/companies/model/customFields/tabs/{id} | write | company | Deletes a custom field tab. |
| PATCH | crm/rest/v2/companies/model/customFields/{id} | write | company | Updates a custom field of the specified type and options to the Company object. |
| DELETE | crm/rest/v2/companies/model/customFields/{id} | write | company | Deletes a custom field from the company model. |
| GET | crm/rest/v2/companies/{id} | read | company | Retrieves a single Company. |
| PATCH | crm/rest/v2/companies/{id} | write | company | Updates a Company with the values provided in the request. |
| DELETE | crm/rest/v2/companies/{id} | write | company | Deletes the specified Company. |
| GET | crm/rest/v2/companies/{id}/tags | read | company | Retrieves a list of tags applied to the specified Company. |
| POST | crm/rest/v2/companies/{id}/tags/{id} | write | company | Applies a Tag to a Company. |
| DELETE | crm/rest/v2/companies/{id}/tags/{id} | write | company | Remove a Tag from a Company. |
| GET | crm/rest/v2/contacts | read | contact | Retrieves a list of Contacts. |
| POST | crm/rest/v2/contacts | write | contact | Creates a new Contact. |
| GET | crm/rest/v2/contacts/-/tags | read | contact | Bulk-retrieves tag-contact associations across multiple contacts in a single request. |
| GET | crm/rest/v2/contacts/links/types | read | contact | Retrieves a list of Contact Link types. |
| POST | crm/rest/v2/contacts/links/types | write | contact | Creates a new type of Contact Link. |
| PATCH | crm/rest/v2/contacts/links/types/{id} | write | contact | Updates the specified Contact Link type. |
| DELETE | crm/rest/v2/contacts/links/types/{id} | write | contact | Deletes the specified Contact Link type. |
| GET | crm/rest/v2/contacts/model | read | contact | Get the custom fields and optional properties for the Contact object. |
| POST | crm/rest/v2/contacts/model/customFields | write | contact | Creates a custom field of the specified type and options to the Contact object. |
| GET | crm/rest/v2/contacts/model/customFields/groups | read | contact | Retrieves a list of custom field groups for the Contact record type. |
| POST | crm/rest/v2/contacts/model/customFields/groups | write | contact | Creates a new custom field group for the Contact record type. |
| GET | crm/rest/v2/contacts/model/customFields/groups/{id} | read | contact | Retrieves a single custom field group by id for the Contact record type. |
| PATCH | crm/rest/v2/contacts/model/customFields/groups/{id} | write | contact | Updates an existing custom field group. |
| DELETE | crm/rest/v2/contacts/model/customFields/groups/{id} | write | contact | Deletes a custom field group. |
| GET | crm/rest/v2/contacts/model/customFields/tabs | read | contact | Retrieves a list of custom field tabs for the Contact record type. |
| POST | crm/rest/v2/contacts/model/customFields/tabs | write | contact | Creates a new custom field tab for the Contact record type. |
| GET | crm/rest/v2/contacts/model/customFields/tabs/{id} | read | contact | Retrieves a single custom field tab by id for the Contact record type. |
| PATCH | crm/rest/v2/contacts/model/customFields/tabs/{id} | write | contact | Updates an existing custom field tab. |
| DELETE | crm/rest/v2/contacts/model/customFields/tabs/{id} | write | contact | Deletes a custom field tab. |
| DELETE | crm/rest/v2/contacts/model/customFields/{id} | write | contact | Deletes a custom field from the Contacts model. |
| GET | crm/rest/v2/contacts/{id} | read | contact | Retrieves a single Contact. |
| PATCH | crm/rest/v2/contacts/{id} | write | contact | Updates a Contact. |
| DELETE | crm/rest/v2/contacts/{id} | write | contact | Deletes the specified Contact. |
| GET | crm/rest/v2/contacts/{id}/links | read | contact | Retrieves a list of Linked Contacts for a given Contact. |
| GET | crm/rest/v2/contacts/{id}/tags | read | contact | Retrieves a list of tags applied to the specified Contact. |
| POST | crm/rest/v2/contacts:link | write | contact | Links two Contacts together using the provided Link type. |
| POST | crm/rest/v2/contacts:merge | write | contact | Merges two Contacts together. |
| POST | crm/rest/v2/contacts:unlink | write | contact | Deletes Link between two Contacts. |
| GET | crm/rest/v2/emails | read | email | Retrieves a list of emails that have been sent. |
| POST | crm/rest/v2/emails | write | email | Creates a Record of an Email sent to a Contact. |
| GET | crm/rest/v2/emails/templates | read | email | Retrieves a paginated list of email templates. |
| GET | crm/rest/v2/emails/templates/{id} | read | email | Retrieve an email template. |
| POST | crm/rest/v2/emails/templates:send | write | email | Send an email based on a template. |
| GET | crm/rest/v2/emails/{id} | read | email | Retrieves a single Email that has been sent. |
| DELETE | crm/rest/v2/emails/{id} | write | email | Deletes a specific Email Record. |
| POST | crm/rest/v2/emails:batchAdd | write | email | Creates a set of Records of Emails sent to Contacts, maximum 1000 per transaction. |
| POST | crm/rest/v2/emails:batchRemove | write | email | Removes a set of Email Records. |
| POST | crm/rest/v2/emails:send | write | email | Sends an Email to a list of Contacts. |
| GET | crm/rest/v2/emailAddresses | read | email-address | Retrieve a list of the Status of Email Addresses. |
| GET | crm/rest/v2/emailAddresses/{id}/status | read | email-address | Retrieves the opt-in status for a given Email Address. |
| PATCH | crm/rest/v2/emailAddresses/{id}/status | write | email-address | Updates an Email Address opt-in status. |
| GET | crm/rest/v2/files | read | files | Retrieves a list of files. |
| POST | crm/rest/v2/files | write | files | Uploads a file using multipart/form-data. |
| GET | crm/rest/v2/files/{id} | read | files | Retrieves a file. |
| POST | crm/rest/v2/files/{id} | write | files | Updates a file using multipart/form-data. |
| DELETE | crm/rest/v2/files/{id} | write | files | Deletes a specified file. |
| GET | crm/rest/v2/files/{id}:data | read | files | Retrieves a file's data. |
| GET | crm/rest/v2/discounts/freeTrials | read | free-trial-discounts | Retrieves a list of Subscription Free Trial Discounts. |
| POST | crm/rest/v2/discounts/freeTrials | write | free-trial-discounts | Creates a Subscription Free Trial Discount. |
| GET | crm/rest/v2/discounts/freeTrials/{id} | read | free-trial-discounts | Retrieves a Subscription Free Trial Discount. |
| PATCH | crm/rest/v2/discounts/freeTrials/{id} | write | free-trial-discounts | Updates a Subscription Free Trial Discount. |
| DELETE | crm/rest/v2/discounts/freeTrials/{id} | write | free-trial-discounts | Deletes a specified Subscription Free Trial Discount. |
| POST | crm/rest/v2/discounts/freeTrials/{id}/criteria | write | free-trial-discounts | Creates a Subscription Free Trial Discount Criteria. |
| DELETE | crm/rest/v2/discounts/freeTrials/{id}/criteria/{id} | write | free-trial-discounts | Deletes a specified Subscription Free Trial Discount Criteria. |
| GET | crm/rest/v2/integrations/wordpress/options | read | integrations | Retrieves the list of WordPress Opt-In Options available. |
| POST | crm/rest/v2/integrations/wordpress/options | write | integrations | Adds a value to the list of WordPress Opt-In Options Available. |
| DELETE | crm/rest/v2/integrations/wordpress/options/{id} | write | integrations | Deletes a value from the list of WordPress Opt-In Options Available. |
| POST | crm/rest/v2/integrations/wordpress/options/{id}:achieve | write | integrations | Achieves a WordPress Opt-In Option Goal. |
| GET | crm/rest/v2/leadSourceCategories | read | lead-source-categories | Retrieves a list of Lead Source Categories. |
| POST | crm/rest/v2/leadSourceCategories | write | lead-source-categories | Creates a new Lead Source Category. |
| GET | crm/rest/v2/leadSourceCategories/{id} | read | lead-source-categories | Retrieves a single Lead Source Category for a given ID. |
| PATCH | crm/rest/v2/leadSourceCategories/{id} | write | lead-source-categories | Updates a Lead Source Category. |
| DELETE | crm/rest/v2/leadSourceCategories/{id} | write | lead-source-categories | Deletes the specified Lead Source Category. |
| GET | crm/rest/v2/leadSources/{id}/expenses | read | lead-source-expenses | Retrieves a list of lead source expenses. |
| POST | crm/rest/v2/leadSources/{id}/expenses | write | lead-source-expenses | Creates a new Lead Source Expense. |
| GET | crm/rest/v2/leadSources/{id}/expenses/{id} | read | lead-source-expenses | Retrieves a single Lead Source Expense for a given ID. |
| PATCH | crm/rest/v2/leadSources/{id}/expenses/{id} | write | lead-source-expenses | Updates a new Lead Source Expense. |
| DELETE | crm/rest/v2/leadSources/{id}/expenses/{id} | write | lead-source-expenses | Deletes a lead source expense by ID. |
| GET | crm/rest/v2/leadSources/{id}/recurringExpenses | read | lead-source-recurring-expenses | Retrieves a list of recurring expenses with lead_source_id and optional 'filter' query param. |
| POST | crm/rest/v2/leadSources/{id}/recurringExpenses | write | lead-source-recurring-expenses | Creates a new Lead Source Recurring Expense. |
| GET | crm/rest/v2/leadSources/{id}/recurringExpenses/{id} | read | lead-source-recurring-expenses | Retrieves a Lead Source Recurring Expense using leadSourceId and leadSourceRecurringExpenseId. |
| PATCH | crm/rest/v2/leadSources/{id}/recurringExpenses/{id} | write | lead-source-recurring-expenses | Updates a Lead Source Recurring Expense. |
| DELETE | crm/rest/v2/leadSources/{id}/recurringExpenses/{id} | write | lead-source-recurring-expenses | Deletes a new Lead Source Recurring Expense that belongs to a Lead Source. |
| GET | crm/rest/v2/leadSources/{id}/recurringExpenses/{id}/expenses | read | lead-source-recurring-expenses | Retrieves a list of expenses incurred from a recurring expense. |
| GET | crm/rest/v2/leadSources | read | lead-sources | Retrieves a list of Lead Sources. |
| POST | crm/rest/v2/leadSources | write | lead-sources | Creates a new Lead Source. |
| GET | crm/rest/v2/leadSources/{id} | read | lead-sources | Retrieves a Lead Source by ID. |
| PATCH | crm/rest/v2/leadSources/{id} | write | lead-sources | Updates a Lead Source with only the values provided in the request. |
| DELETE | crm/rest/v2/leadSources/{id} | write | lead-sources | Deletes a Lead Source by ID. |
| GET | crm/rest/v2/contacts/{id}/leadScore | read | leadscore | Retrieves information about the Lead Score of a Contact. |
| GET | crm/rest/v2/locales/countries | read | locale | Retrieves a list of countries. |
| GET | crm/rest/v2/locales/countries/{id} | read | locale | Gets a country by its code or name. |
| GET | crm/rest/v2/locales/countries/{id}/provinces | read | locale | Retrieves a list of provinces for a given country. |
| GET | crm/rest/v2/locales/countries/{id}/provinces/{id} | read | locale | Get a province by its code or name. |
| GET | crm/rest/v2/merchants | read | merchants | Retrieves a list of Merchant accounts. |
| GET | crm/rest/v2/contacts/{id}/notes | read | note | Retrieves a list of Notes for a given contact. |
| POST | crm/rest/v2/contacts/{id}/notes | write | note | Creates a new Note. |
| GET | crm/rest/v2/contacts/{id}/notes/{id} | read | note | Retrieves the specified Note. |
| PATCH | crm/rest/v2/contacts/{id}/notes/{id} | write | note | Updates a Note for a Contact. |
| DELETE | crm/rest/v2/contacts/{id}/notes/{id} | write | note | Deletes the specified Note. |
| GET | crm/rest/v2/notes | read | note | Retrieves a list of all notes. |
| GET | crm/rest/v2/notes/model | read | note | Gets the custom fields for the Note object. |
| POST | crm/rest/v2/notes/model/customFields | write | note | Creates a custom field of the specified type and options to the Note object. |
| GET | crm/rest/v2/notes/model/customFields/groups | read | note | Retrieves a list of custom field groups for the Note record type. |
| POST | crm/rest/v2/notes/model/customFields/groups | write | note | Creates a new custom field group for the Note record type. |
| GET | crm/rest/v2/notes/model/customFields/groups/{id} | read | note | Retrieves a single custom field group by id for the Note record type. |
| PATCH | crm/rest/v2/notes/model/customFields/groups/{id} | write | note | Updates an existing custom field group. |
| DELETE | crm/rest/v2/notes/model/customFields/groups/{id} | write | note | Deletes a custom field group. |
| GET | crm/rest/v2/notes/model/customFields/tabs | read | note | Retrieves a list of custom field tabs for the Note record type. |
| POST | crm/rest/v2/notes/model/customFields/tabs | write | note | Creates a new custom field tab for the Note record type. |
| GET | crm/rest/v2/notes/model/customFields/tabs/{id} | read | note | Retrieves a single custom field tab by id for the Note record type. |
| PATCH | crm/rest/v2/notes/model/customFields/tabs/{id} | write | note | Updates an existing custom field tab. |
| DELETE | crm/rest/v2/notes/model/customFields/tabs/{id} | write | note | Deletes a custom field tab. |
| PATCH | crm/rest/v2/notes/model/customFields/{id} | write | note | Updates a custom field of the specified type and options to the Note object. |
| DELETE | crm/rest/v2/notes/model/customFields/{id} | write | note | Deletes a Custom Field from the Note object. |
| GET | crm/rest/v2/notes/templates | read | note | Retrieves a list of Note Templates. |
| GET | crm/rest/v2/opportunities | read | opportunity | Retrieves a list of all Opportunities. |
| POST | crm/rest/v2/opportunities | write | opportunity | Creates a new opportunity as the authenticated user. |
| GET | crm/rest/v2/opportunities/model | read | opportunity | Get the custom fields for the Opportunity object. |
| POST | crm/rest/v2/opportunities/model/customFields | write | opportunity | Creates a custom field of the specified type and options to the Opportunity object. |
| GET | crm/rest/v2/opportunities/model/customFields/groups | read | opportunity | Retrieves a list of custom field groups for the Opportunity record type. |
| POST | crm/rest/v2/opportunities/model/customFields/groups | write | opportunity | Creates a new custom field group for the Opportunity record type. |
| GET | crm/rest/v2/opportunities/model/customFields/groups/{id} | read | opportunity | Retrieves a single custom field group by id for the Opportunity record type. |
| PATCH | crm/rest/v2/opportunities/model/customFields/groups/{id} | write | opportunity | Updates an existing custom field group. |
| DELETE | crm/rest/v2/opportunities/model/customFields/groups/{id} | write | opportunity | Deletes a custom field group. |
| GET | crm/rest/v2/opportunities/model/customFields/tabs | read | opportunity | Retrieves a list of custom field tabs for the Opportunity record type. |
| POST | crm/rest/v2/opportunities/model/customFields/tabs | write | opportunity | Creates a new custom field tab for the Opportunity record type. |
| GET | crm/rest/v2/opportunities/model/customFields/tabs/{id} | read | opportunity | Retrieves a single custom field tab by id for the Opportunity record type. |
| PATCH | crm/rest/v2/opportunities/model/customFields/tabs/{id} | write | opportunity | Updates an existing custom field tab. |
| DELETE | crm/rest/v2/opportunities/model/customFields/tabs/{id} | write | opportunity | Deletes a custom field tab. |
| PATCH | crm/rest/v2/opportunities/model/customFields/{id} | write | opportunity | Updates a custom field of the specified type and options to the Opportunity object. |
| DELETE | crm/rest/v2/opportunities/model/customFields/{id} | write | opportunity | Deletes a Custom Field from Opportunity. |
| GET | crm/rest/v2/opportunities/stageMoves | read | opportunity | Returns a paginated list of historical stage-move records. |
| GET | crm/rest/v2/opportunities/stageMoves/{id} | read | opportunity | Retrieves a single historical record of an opportunity being moved from one pipeline stage to another. |
| GET | crm/rest/v2/opportunities/stages | read | opportunity | Retrieves a list of Opportunity Stages. |
| POST | crm/rest/v2/opportunities/stages | write | opportunity | Creates a new Opportunity Stage. |
| GET | crm/rest/v2/opportunities/stages/{id} | read | opportunity | Retrieves the specified Opportunity Stage. |
| PATCH | crm/rest/v2/opportunities/stages/{id} | write | opportunity | Updates specified values of a given Opportunity Stage. |
| DELETE | crm/rest/v2/opportunities/stages/{id} | write | opportunity | Deletes the specified Opportunity Stage. |
| GET | crm/rest/v2/opportunities/{id} | read | opportunity | Retrieves the specified Opportunity. |
| PATCH | crm/rest/v2/opportunities/{id} | write | opportunity | Updates specified values of a given opportunity. |
| DELETE | crm/rest/v2/opportunities/{id} | write | opportunity | Deletes the specified Opportunity. |
| GET | crm/rest/v2/discounts/orderTotals | read | order-total-discounts | Retrieves a list of Order Total Discounts. |
| POST | crm/rest/v2/discounts/orderTotals | write | order-total-discounts | Creates an Order Total Discount. |
| GET | crm/rest/v2/discounts/orderTotals/{id} | read | order-total-discounts | Retrieves an Order Total Discount. |
| PATCH | crm/rest/v2/discounts/orderTotals/{id} | write | order-total-discounts | Updates an Order Total Discount. |
| DELETE | crm/rest/v2/discounts/orderTotals/{id} | write | order-total-discounts | Deletes a specified Order Total Discount. |
| POST | crm/rest/v2/discounts/orderTotals/{id}/criteria | write | order-total-discounts | Creates an Order Total Discount Criteria. |
| DELETE | crm/rest/v2/discounts/orderTotals/{id}/criteria/{id} | write | order-total-discounts | Deletes a specified Order Total Discount Criteria. |
| GET | crm/rest/v2/orders | read | orders | Retrieves a list of orders. |
| POST | crm/rest/v2/orders | write | orders | Creates a one time Order with Order items. |
| GET | crm/rest/v2/orders/model | read | orders | Gets the custom fields for the Order object. |
| POST | crm/rest/v2/orders/model/customFields | write | orders | Creates a custom field of the specified type and options to the Order object. |
| GET | crm/rest/v2/orders/model/customFields/groups | read | orders | Retrieves a list of custom field groups for the Order record type. |
| POST | crm/rest/v2/orders/model/customFields/groups | write | orders | Creates a new custom field group for the Order record type. |
| GET | crm/rest/v2/orders/model/customFields/groups/{id} | read | orders | Retrieves a single custom field group by id for the Order record type. |
| PATCH | crm/rest/v2/orders/model/customFields/groups/{id} | write | orders | Updates an existing custom field group. |
| DELETE | crm/rest/v2/orders/model/customFields/groups/{id} | write | orders | Deletes a custom field group. |
| GET | crm/rest/v2/orders/model/customFields/tabs | read | orders | Retrieves a list of custom field tabs for the Order record type. |
| POST | crm/rest/v2/orders/model/customFields/tabs | write | orders | Creates a new custom field tab for the Order record type. |
| GET | crm/rest/v2/orders/model/customFields/tabs/{id} | read | orders | Retrieves a single custom field tab by id for the Order record type. |
| PATCH | crm/rest/v2/orders/model/customFields/tabs/{id} | write | orders | Updates an existing custom field tab. |
| DELETE | crm/rest/v2/orders/model/customFields/tabs/{id} | write | orders | Deletes a custom field tab. |
| PATCH | crm/rest/v2/orders/model/customFields/{id} | write | orders | Updates a custom field of the specified type and options to the Order object. |
| DELETE | crm/rest/v2/orders/model/customFields/{id} | write | orders | Deletes a Custom Field from the Order object. |
| GET | crm/rest/v2/orders/{id} | read | orders | Retrieves a single Order for a given order id. |
| PATCH | crm/rest/v2/orders/{id} | write | orders | Updates an Order. |
| DELETE | crm/rest/v2/orders/{id} | write | orders | Deletes an Order. |
| POST | crm/rest/v2/orders/{id}/items | write | orders | Creates an order item on an existing order. |
| GET | crm/rest/v2/orders/{id}/items/{id} | read | orders | Retrieves a single order item from an existing order. |
| PATCH | crm/rest/v2/orders/{id}/items/{id} | write | orders | Updates an Order Item. |
| DELETE | crm/rest/v2/orders/{id}/items/{id} | write | orders | Deletes an order item on an existing order. |
| POST | crm/rest/v2/orders/{id}/items/{id}:applyCommission | write | orders | Applies commission to an order item on an existing order. |
| GET | crm/rest/v2/orders/{id}/payments | read | orders | Retrieves a list of payments made against a given order, including historical or external payments of cash or credit card. |
| POST | crm/rest/v2/orders/{id}/payments | write | orders | Creates a payment record. |
| PATCH | crm/rest/v2/orders/{id}/payments/{id} | write | orders | Updates a payment record with external source information and status. |
| POST | crm/rest/v2/orders/{id}:applyTax | write | orders | Calculate taxes for a single Order for a given order id. |
| POST | crm/rest/v2/orders/{id}:attachFile | write | orders | Attaches an uploaded File to an Order Invoice. |
| POST | crm/rest/v2/orders/{id}:detachFile | write | orders | Detaches a File from an Order Invoice. |
| POST | crm/rest/v2/paymentMethodConfigs | write | payment-method-configs | Creates configuration details for rendering payment method components. |
| GET | crm/rest/v2/contacts/{id}/paymentMethods | read | payment-methods | Retrieves a list of Contact Payment Methods. |
| DELETE | crm/rest/v2/contacts/{id}/paymentMethods/{id} | write | payment-methods | Deletes the specified payment method. |
| POST | crm/rest/v2/contacts/{id}/paymentMethods/{id}:deactivate | write | payment-methods | Deactivate the specified payment method. |
| GET | crm/rest/v2/paymentMethods | read | payment-methods | Retrieves a list of Payment Methods. |
| GET | crm/rest/v2/productCategories | read | product-categories | Retrieves a list of Product Categories. |
| POST | crm/rest/v2/productCategories | write | product-categories | Creates a new Product Category. |
| GET | crm/rest/v2/productCategories/assignedProducts | read | product-categories | Retrieves a list of Products assigned to Product Categories. |
| GET | crm/rest/v2/productCategories/{id} | read | product-categories | Gets a single Product Category. |
| PATCH | crm/rest/v2/productCategories/{id} | write | product-categories | Updates a single Product Category. |
| DELETE | crm/rest/v2/productCategories/{id} | write | product-categories | Deletes the specified Product Category, its sub-categories, and removes products from it. |
| POST | crm/rest/v2/productCategories/{id}/images | write | product-categories | Creates the product category image file and uploads it to the specified product category. |
| DELETE | crm/rest/v2/productCategories/{id}/images | write | product-categories | Deletes the image from the specified product category. |
| POST | crm/rest/v2/productCategories/{id}:assignProducts | write | product-categories | Updates the list of products assigned to a Product Category. |
| GET | crm/rest/v2/discounts/products | read | product-discounts | Retrieves a list of Product Discounts. |
| POST | crm/rest/v2/discounts/products | write | product-discounts | Creates a Product Discount. |
| GET | crm/rest/v2/discounts/products/{id} | read | product-discounts | Retrieves a Product Discount. |
| PATCH | crm/rest/v2/discounts/products/{id} | write | product-discounts | Updates a Product Discount. |
| DELETE | crm/rest/v2/discounts/products/{id} | write | product-discounts | Deletes a specified Product Discount. |
| POST | crm/rest/v2/discounts/products/{id}/criteria | write | product-discounts | Creates a Product Discount Criteria. |
| DELETE | crm/rest/v2/discounts/products/{id}/criteria/{id} | write | product-discounts | Deletes a specified Product Discount Criteria. |
| GET | crm/rest/v2/productInterestBundles | read | product-interest-bundles | Retrieves a list of Product Interest Bundles. |
| POST | crm/rest/v2/productInterestBundles | write | product-interest-bundles | Creates a new Product Interest Bundle. |
| GET | crm/rest/v2/productInterestBundles/{id} | read | product-interest-bundles | Gets a single Product Interest Bundle. |
| PATCH | crm/rest/v2/productInterestBundles/{id} | write | product-interest-bundles | Updates an existing Product Interest Bundle. |
| DELETE | crm/rest/v2/productInterestBundles/{id} | write | product-interest-bundles | Deletes an existing Product Interest Bundle. |
| POST | crm/rest/v2/productInterestBundles/{id}/interests | write | product-interest-bundles | Creates a new Product Interest in an existing Bundle. |
| PATCH | crm/rest/v2/productInterestBundles/{id}/interests/{id} | write | product-interest-bundles | Updates an existing Product Interest in an existing Bundle. |
| DELETE | crm/rest/v2/productInterestBundles/{id}/interests/{id} | write | product-interest-bundles | Deletes an existing Product Interest from an existing Bundle. |
| GET | crm/rest/v2/products | read | products | Retrieves a list of Products. |
| POST | crm/rest/v2/products | write | products | Creates a new product. |
| GET | crm/rest/v2/products/{id} | read | products | Gets a single Product. |
| PATCH | crm/rest/v2/products/{id} | write | products | Updates a product. |
| DELETE | crm/rest/v2/products/{id} | write | products | Deletes a single product. |
| POST | crm/rest/v2/products/{id}/images | write | products | Creates the Product Image file and uploads it to the specified Product. |
| DELETE | crm/rest/v2/products/{id}/images | write | products | Deletes the Product Image from the specified Product. |
| GET | crm/rest/v2/products/{id}/images/legacyImageData | read | products | Retrieves the product's legacy image. |
| GET | crm/rest/v2/products/{id}/options | read | products | Retrieves all options of a Product. |
| POST | crm/rest/v2/products/{id}/options | write | products | Creates a new product option. |
| GET | crm/rest/v2/products/{id}/options/{id} | read | products | Retrieves a Product Option. |
| PATCH | crm/rest/v2/products/{id}/options/{id} | write | products | Updates a product option. |
| DELETE | crm/rest/v2/products/{id}/options/{id} | write | products | Deletes a single product option. |
| POST | crm/rest/v2/products/{id}/options/{id}/listItems | write | products | Adds product option values to a product option of type LIST. |
| PATCH | crm/rest/v2/products/{id}/options/{id}/listItems/{id} | write | products | Updates a single product option value. |
| DELETE | crm/rest/v2/products/{id}/options/{id}/listItems/{id} | write | products | Deletes a single option value in a Product Option of type LIST. |
| POST | crm/rest/v2/products/{id}:adjustInventory | write | products | Increase or decrease the quantity of the Product. |
| GET | crm/rest/v2/referrals | read | referral | Retrieves a list of all referrals with optional filtering and sorting. |
| POST | crm/rest/v2/referrals | write | referral | Creates a new referral partner referral on the provided contact. |
| GET | crm/rest/v2/reporting/reports | read | reporting | Retrieves a list of Reports as defined in the application (identified as Saved Search). |
| GET | crm/rest/v2/reporting/reports/{id} | read | reporting | Retrieves information about a Report as defined in the application (identified as Saved Search). |
| GET | crm/rest/v2/reporting/reports/{id}/model | read | reporting | Retrieves the list of fields available for a Report (Saved Search). |
| POST | crm/rest/v2/reporting/reports/{id}:run | read | reporting | Runs a report as defined in the application (identified as Saved Search). |
| POST | crm/rest/v2/sales/merchants/{id}:setDefault | write | sales | Sets the specified Merchant Account as the default Merchant Account. |
| GET | crm/rest/v2/sales/payments | read | sales | Retrieves a list of payments. |
| GET | crm/rest/v2/sales/transactions | read | sales | Retrieves a list of sales transactions. |
| GET | crm/rest/v2/settings/applications:getConfiguration | read | settings | Get configuration values for the application instance. |
| GET | crm/rest/v2/settings/applications:isEnabled | read | settings | Check if the application is enabled or not. |
| GET | crm/rest/v2/settings/contactOptionTypes | read | settings | Gets a list of Contact Option types. |
| GET | crm/rest/v2/shipping | read | shipping | Retrieves a list of Shipping methods. |
| GET | crm/rest/v2/discounts/shipping | read | shipping-discounts | Retrieves a list of Shipping Discounts. |
| POST | crm/rest/v2/discounts/shipping | write | shipping-discounts | Creates a Shipping Discount. |
| GET | crm/rest/v2/discounts/shipping/{id} | read | shipping-discounts | Retrieves a Shipping Discount. |
| PATCH | crm/rest/v2/discounts/shipping/{id} | write | shipping-discounts | Updates a Shipping Discount. |
| DELETE | crm/rest/v2/discounts/shipping/{id} | write | shipping-discounts | Deletes a specified Shipping Discount. |
| POST | crm/rest/v2/discounts/shipping/{id}/criteria | write | shipping-discounts | Creates a Shipping Discount Criteria. |
| DELETE | crm/rest/v2/discounts/shipping/{id}/criteria/{id} | write | shipping-discounts | Deletes a specified Shipping Discount Criteria. |
| GET | crm/rest/v2/products/{id}/subscriptions | read | subscription-plans | Retrieves a list of Subscription Plans. |
| POST | crm/rest/v2/products/{id}/subscriptions | write | subscription-plans | Creates a Subscription Plan. |
| GET | crm/rest/v2/products/{id}/subscriptions/{id} | read | subscription-plans | Retrieves a Subscription Plan. |
| PATCH | crm/rest/v2/products/{id}/subscriptions/{id} | write | subscription-plans | Updates a Subscription Plan. |
| DELETE | crm/rest/v2/products/{id}/subscriptions/{id} | write | subscription-plans | Deletes a Subscription Plan. |
| GET | crm/rest/v2/subscriptions | read | subscriptions | Retrieves a list of subscriptions using the specified search criteria. |
| POST | crm/rest/v2/subscriptions | write | subscriptions | Creates a subscription with the specified product and product subscription id. |
| GET | crm/rest/v2/subscriptions/model | read | subscriptions | Get the custom fields for the Subscription object. |
| POST | crm/rest/v2/subscriptions/model/customFields | write | subscriptions | Creates a custom field of the specified type and options to the Subscription object. |
| GET | crm/rest/v2/subscriptions/model/customFields/groups | read | subscriptions | Retrieves a list of custom field groups for the Subscription record type. |
| POST | crm/rest/v2/subscriptions/model/customFields/groups | write | subscriptions | Creates a new custom field group for the Subscription record type. |
| GET | crm/rest/v2/subscriptions/model/customFields/groups/{id} | read | subscriptions | Retrieves a single custom field group by id for the Subscription record type. |
| PATCH | crm/rest/v2/subscriptions/model/customFields/groups/{id} | write | subscriptions | Updates an existing custom field group. |
| DELETE | crm/rest/v2/subscriptions/model/customFields/groups/{id} | write | subscriptions | Deletes a custom field group. |
| GET | crm/rest/v2/subscriptions/model/customFields/tabs | read | subscriptions | Retrieves a list of custom field tabs for the Subscription record type. |
| POST | crm/rest/v2/subscriptions/model/customFields/tabs | write | subscriptions | Creates a new custom field tab for the Subscription record type. |
| GET | crm/rest/v2/subscriptions/model/customFields/tabs/{id} | read | subscriptions | Retrieves a single custom field tab by id for the Subscription record type. |
| PATCH | crm/rest/v2/subscriptions/model/customFields/tabs/{id} | write | subscriptions | Updates an existing custom field tab. |
| DELETE | crm/rest/v2/subscriptions/model/customFields/tabs/{id} | write | subscriptions | Deletes a custom field tab. |
| PATCH | crm/rest/v2/subscriptions/model/customFields/{id} | write | subscriptions | Updates a custom field of the specified type and options to the Subscription object. |
| DELETE | crm/rest/v2/subscriptions/model/customFields/{id} | write | subscriptions | Deletes a custom field from the Subscription object. |
| GET | crm/rest/v2/subscriptions/{id} | read | subscriptions | Retrieves a single subscription. |
| PATCH | crm/rest/v2/subscriptions/{id} | write | subscriptions | Updates a Subscription. |
| POST | crm/rest/v2/subscriptions/{id}:deactivate | write | subscriptions | Cancels the specified subscription. |
| POST | crm/rest/v2/subscriptions/{id}:invoice | write | subscriptions | Generates invoices from all cycles of a subscription that are due. |
| GET | crm/rest/v2/tags | read | tags | Retrieves a list of Tags defined in the application. |
| POST | crm/rest/v2/tags | write | tags | Creates a new Tag. |
| GET | crm/rest/v2/tags/-/contacts | read | tags | Bulk-retrieves tag-contact associations across multiple tags in a single request. |
| GET | crm/rest/v2/tags/categories | read | tags | Retrieves a list of defined Tag Categories. |
| POST | crm/rest/v2/tags/categories | write | tags | Creates a new Tag Category. |
| GET | crm/rest/v2/tags/categories/{id} | read | tags | Returns information about the specified Tag Category. |
| PATCH | crm/rest/v2/tags/categories/{id} | write | tags | Updates a Tag Category with only the values provided in the request. |
| DELETE | crm/rest/v2/tags/categories/{id} | write | tags | Deletes the specified Tag Category. |
| GET | crm/rest/v2/tags/{id} | read | tags | Retrieves information about the specified Tag. |
| PATCH | crm/rest/v2/tags/{id} | write | tags | Updates a Tag with only the values provided in the request. |
| DELETE | crm/rest/v2/tags/{id} | write | tags | Deletes a Tag. |
| GET | crm/rest/v2/tags/{id}/companies | read | tags | Retrieves a list of Companies that have the given Tag applied. |
| GET | crm/rest/v2/tags/{id}/contacts | read | tags | Retrieves a list of Contacts with the specified Tag. |
| GET | crm/rest/v2/tags/{id}/contacts/count | read | tags | Returns the total number of contacts associated with the given tag. |
| POST | crm/rest/v2/tags/{id}/contacts:applyTags | write | tags | Applies a Tag to a list of Contacts. |
| POST | crm/rest/v2/tags/{id}/contacts:removeTags | write | tags | Removes a Tag from a list of Contacts. |
| GET | crm/rest/v2/tasks | read | task | Retrieves a list of tasks based on the provided filter. |
| POST | crm/rest/v2/tasks | write | task | Creates a new task as the authenticated user. |
| GET | crm/rest/v2/tasks/model | read | task | Get the custom fields for the Task object. |
| POST | crm/rest/v2/tasks/model/customFields | write | task | Creates a custom field of the specified type and options to the Task object. |
| GET | crm/rest/v2/tasks/model/customFields/groups | read | task | Retrieves a list of custom field groups for the Task record type. |
| POST | crm/rest/v2/tasks/model/customFields/groups | write | task | Creates a new custom field group for the Task record type. |
| GET | crm/rest/v2/tasks/model/customFields/groups/{id} | read | task | Retrieves a single custom field group by id for the Task record type. |
| PATCH | crm/rest/v2/tasks/model/customFields/groups/{id} | write | task | Updates an existing custom field group. |
| DELETE | crm/rest/v2/tasks/model/customFields/groups/{id} | write | task | Deletes a custom field group. |
| GET | crm/rest/v2/tasks/model/customFields/tabs | read | task | Retrieves a list of custom field tabs for the Task record type. |
| POST | crm/rest/v2/tasks/model/customFields/tabs | write | task | Creates a new custom field tab for the Task record type. |
| GET | crm/rest/v2/tasks/model/customFields/tabs/{id} | read | task | Retrieves a single custom field tab by id for the Task record type. |
| PATCH | crm/rest/v2/tasks/model/customFields/tabs/{id} | write | task | Updates an existing custom field tab. |
| DELETE | crm/rest/v2/tasks/model/customFields/tabs/{id} | write | task | Deletes a custom field tab. |
| PATCH | crm/rest/v2/tasks/model/customFields/{id} | write | task | Updates a custom field of the specified type and options to the Task object. |
| DELETE | crm/rest/v2/tasks/model/customFields/{id} | write | task | Deletes a Custom Field from the Task object. |
| GET | crm/rest/v2/tasks/{id} | read | task | Retrieves a single task. |
| PATCH | crm/rest/v2/tasks/{id} | write | task | Updates a task with only the values provided in the request. |
| DELETE | crm/rest/v2/tasks/{id} | write | task | Deletes a single task. |
| GET | crm/rest/v2/taskAppointments | read | task-appointments | Retrieves a paginated list of Task Appointments. |
| GET | crm/rest/v2/userGroups | read | user-groups | Retrieves a list of all user groups in the application. |
| GET | crm/rest/v2/userGroups/{id} | read | user-groups | Retrieves a single user group by its ID. |
| GET | crm/rest/v2/oauth/connect/userinfo | read | users | Retrieves information for the current authenticated end-user, as outlined by the OpenID Connect specification. |
| GET | crm/rest/v2/users | read | users | Retrieves a list of users. |
| GET | crm/rest/v2/users/{id} | read | users | Retrieves a specific User. |
| PATCH | crm/rest/v2/users/{id} | write | users | Updates information on a specific User. |
| GET | crm/rest/v2/users/{id}/signature | read | users | Retrieves a HTML snippet that contains the user's email signature. |
| GET | crm/rest/v2/webforms | read | webforms | Retrieves a list of webforms. |
| GET | crm/rest/v2/webforms/{id}:data | read | webforms | Returns the HTML. |
