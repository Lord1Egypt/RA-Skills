# Kit access policy

An access policy limits which endpoints Kit connections may call through Maton. Kit doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/kit#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Kit: its 42 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create kit --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v4/account"},
    {"method": "GET", "path": "v4/account/colors"},
    {"method": "GET", "path": "v4/account/creator_profile"},
    {"method": "GET", "path": "v4/account/email_stats"},
    {"method": "GET", "path": "v4/account/growth_stats"},
    {"method": "GET", "path": "v4/apps"},
    {"method": "GET", "path": "v4/apps/{id}"},
    {"method": "GET", "path": "v4/broadcasts"},
    {"method": "GET", "path": "v4/broadcasts/stats"},
    {"method": "GET", "path": "v4/broadcasts/{id}"},
    {"method": "GET", "path": "v4/broadcasts/{id}/clicks"},
    {"method": "GET", "path": "v4/broadcasts/{id}/stats"},
    {"method": "GET", "path": "v4/custom_fields"},
    {"method": "GET", "path": "v4/email_templates"},
    {"method": "GET", "path": "v4/forms"},
    {"method": "GET", "path": "v4/forms/{id}/subscribers"},
    {"method": "GET", "path": "v4/kit_fields"},
    {"method": "GET", "path": "v5/ping"},
    {"method": "GET", "path": "v4/posts"},
    {"method": "GET", "path": "v4/posts/{id}"},
    {"method": "GET", "path": "v4/purchases"},
    {"method": "GET", "path": "v4/purchases/{id}"},
    {"method": "GET", "path": "v4/segments"},
    {"method": "GET", "path": "v4/sequences/{id}/emails"},
    {"method": "GET", "path": "v4/sequences/{id}/emails/{id}"},
    {"method": "GET", "path": "v4/sequences"},
    {"method": "GET", "path": "v4/sequences/{id}"},
    {"method": "GET", "path": "v4/sequences/{id}/subscribers"},
    {"method": "GET", "path": "v4/snippets"},
    {"method": "GET", "path": "v4/snippets/{id}"},
    {"method": "GET", "path": "v4/subscribers"},
    {"method": "POST", "path": "v4/subscribers/filter"},
    {"method": "GET", "path": "v4/subscribers/{id}"},
    {"method": "GET", "path": "v4/subscribers/{id}/stats"},
    {"method": "GET", "path": "v4/subscribers/{id}/tags"},
    {"method": "GET", "path": "v4/tags"},
    {"method": "GET", "path": "v4/tags/{id}/subscribers"},
    {"method": "GET", "path": "v4/webhook_endpoints"},
    {"method": "GET", "path": "v4/webhook_endpoints/{id}"},
    {"method": "GET", "path": "v4/webhook_endpoints/{id}/deliveries"},
    {"method": "GET", "path": "v4/webhook_endpoints/{id}/deliveries/{id}"},
    {"method": "GET", "path": "v4/webhooks"}
  ],
  "deny": []
}
```

## Endpoints

The Kit endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v4/account | read | accounts | Returns the authenticated account and user: account `id`, `name`, `plan_type`, primary email address, timezone, and the account's sending addresses with their verification and DMARC status. |
| GET | v4/account/colors | read | accounts | Returns the account's saved brand color palette as an array of hex codes (up to 10). |
| PUT | v4/account/colors | write | accounts | Replaces the account's brand color palette with the provided array of up to 10 hex codes and returns the updated list. |
| GET | v4/account/creator_profile | read | accounts | Returns the account's Creator Profile — the public-facing identity shown on their Kit profile page and in the Creator Network: display `name`, `byline`, `bio`, `image_url`, and the public... |
| GET | v4/account/email_stats | read | accounts | Returns account-level email performance for the last 90 days: `sent`, `opened`, and `clicked` counts plus open, click, unsubscribe, and bounce rates, with the exact reporting window in... |
| GET | v4/account/growth_stats | read | accounts | Get growth stats for a specific time period. |
| GET | v4/apps | read | apps | Returns the apps in the Kit App Store that the account can see: every app listed in the store, plus any app the account created, in any status, marked `owned`. |
| GET | v4/apps/{id} | read | apps | Fetches one app by `id` with everything List apps leaves out: the listing `description` as plain text, the app's `capabilities` inside Kit, the developer's `links`, screenshots in `media_links`,... |
| GET | v4/broadcasts | read | broadcasts | Returns a cursor-paginated list of broadcasts in the account with their content, targeting (`subscriber_filter`), email template, and web-publishing settings. |
| POST | v4/broadcasts | write | broadcasts | Draft or schedule to send a broadcast to all or a subset of your subscribers.To save a draft, set `send_at` to `null`.To publish to the web, set `public` to `true`.To schedule the broadcast for... |
| GET | v4/broadcasts/stats | read | broadcasts | Returns delivery and engagement stats — recipients, opens, clicks, unsubscribes, and their corresponding rates — for a page of broadcasts in a single request, avoiding a call per broadcast. |
| GET | v4/broadcasts/{id} | read | broadcasts | Returns a single broadcast's full record: subject, `content` (HTML), preview text, targeting (`subscriber_filter`), email template, sending schedule (`send_at`), and web-publishing details... |
| PUT | v4/broadcasts/{id} | write | broadcasts | Update an existing broadcast. |
| DELETE | v4/broadcasts/{id} | write | broadcasts | Permanently deletes a draft or scheduled broadcast and returns `204 No Content` on success. |
| GET | v4/broadcasts/{id}/clicks | read | broadcasts | Returns click performance for each link in a broadcast: the link `url`, its `unique_clicks`, and its click-to-delivery and click-to-open rates. |
| GET | v4/broadcasts/{id}/stats | read | broadcasts | Returns delivery and engagement stats for a single broadcast: recipients, opens, clicks, unsubscribes, their corresponding rates, plus the sending `status` and `progress`. |
| POST | v4/bulk/custom_fields | write | custom-fields | See "Bulk & async processing" for more information. |
| POST | v4/bulk/custom_fields/subscribers | write | custom-fields | Creates or updates custom field values for many subscribers in one request. |
| GET | v4/custom_fields | read | custom-fields | A custom field allows you to collect subscriber information beyond the standard fields of first name and email address. |
| POST | v4/custom_fields | write | custom-fields | Create a custom field for your account. |
| PUT | v4/custom_fields/{id} | write | custom-fields | Updates a custom field label (see Create a custom field for more information on labels). |
| DELETE | v4/custom_fields/{id} | write | custom-fields | This will remove all data in this field from your subscribers. |
| GET | v4/email_templates | read | email-templates | Returns a cursor-paginated list of the account's email templates with each template's `id`, `name`, `is_default` flag, and `category` (for example `HTML` or `Starting point`). |
| POST | v4/bulk/forms/subscribers | write | forms | Adding subscribers to double opt-in forms will trigger sending an Incentive Email. |
| GET | v4/forms | read | forms | Returns a cursor-paginated list of forms and landing pages in the account. |
| GET | v4/forms/{id}/subscribers | read | forms | Returns a cursor-paginated list of subscribers who joined through (or were added to) the form. |
| POST | v4/forms/{id}/subscribers | write | forms | The subscriber being added to the form must already exist. |
| POST | v4/forms/{id}/subscribers/{id} | write | forms | The subscriber being added to the form must already exist. |
| GET | v4/kit_fields | read | kit-fields | Returns the Kit Fields: what Subscriber Signals knows about each subscriber, such as job title, social profiles and follower counts, and demographics. |
| GET | v5/ping | read | ping | Check your credentials. |
| GET | v4/posts | read | posts | Returns a cursor-paginated list of the account's posts — content published to the creator's Kit site and/or sent by email — with each post's `status` (e.g. |
| GET | v4/posts/{id} | read | posts | Returns a single post's full record, including its `content` HTML, `status` (e.g. |
| GET | v4/purchases | read | purchases | Returns a cursor-paginated list of purchases recorded in the account, typically imported from e-commerce platforms. |
| POST | v4/purchases | write | purchases | Records a purchase against a subscriber, identified by `email_address` — use this to sync order data from your e-commerce platform into Kit so it appears on the subscriber's profile and can drive... |
| GET | v4/purchases/{id} | read | purchases | Returns a single purchase's details: `transaction_id`, `status`, `source`, the buyer's `email_address` and `subscriber_id`, monetary breakdown (`subtotal`, `discount`, `tax`, `total`, `currency`),... |
| GET | v4/segments | read | segments | Returns a cursor-paginated list of all segments in the account with their `id`, `name`, and creation date. |
| GET | v4/sequences/{id}/emails | read | sequence-emails | Returns every email inside a sequence, ordered by `position` (the order subscribers receive them). |
| POST | v4/sequences/{id}/emails | write | sequence-emails | Adds a single email to a sequence. |
| GET | v4/sequences/{id}/emails/{id} | read | sequence-emails | Fetches a single sequence email by `id`. |
| PUT | v4/sequences/{id}/emails/{id} | write | sequence-emails | Updates any field on a sequence email — `subject`, `preview_text`, `content`, `delay_value`, `delay_unit`, `send_days`, `position`, `email_template_id`, or `published`. |
| DELETE | v4/sequences/{id}/emails/{id} | write | sequence-emails | Permanently removes one email from a sequence. |
| GET | v4/sequences | read | sequences | Returns every sequence on the account. |
| POST | v4/sequences | write | sequences | Creates an empty sequence — the container that holds sequence emails. |
| GET | v4/sequences/{id} | read | sequences | Fetches a single sequence by `id`. |
| PUT | v4/sequences/{id} | write | sequences | Updates any sequence settings — `name`, `email_address`, schedule (`send_days`, `send_hour`, `time_zone`), `email_template_id`, `exclude_subscriber_sources`, or the `active` / `repeat` / `hold` flags. |
| DELETE | v4/sequences/{id} | write | sequences | Soft-deletes a sequence. |
| GET | v4/sequences/{id}/subscribers | read | sequences | Returns a cursor-paginated list of subscribers in the sequence, each with an `added_at` timestamp for when they entered it. |
| POST | v4/sequences/{id}/subscribers | write | sequences | The subscriber being added to the sequence must already exist. |
| POST | v4/sequences/{id}/subscribers/{id} | write | sequences | The subscriber being added to the sequence must already exist. |
| GET | v4/snippets | read | snippets | Returns every snippet on the account. |
| POST | v4/snippets | write | snippets | Snippets are reusable pieces of email content you can drop into a broadcast or sequence email using Liquid: `{{ snippet.key }}`. |
| GET | v4/snippets/{id} | read | snippets | Fetches a single snippet by `id`. |
| PUT | v4/snippets/{id} | write | snippets | Rename a snippet, replace its body, or archive/restore it. |
| POST | v4/bulk/subscribers | write | subscribers | See "Bulk & async processing" for more information. |
| GET | v4/subscribers | read | subscribers | Returns a cursor-paginated list of subscribers in the account. |
| POST | v4/subscribers | write | subscribers | Behaves as an upsert. |
| POST | v4/subscribers/filter | read | subscribers | Searches your subscriber list with compound conditions: email engagement (opens, clicks, sends, deliveries — with count thresholds and date ranges), sign-up date, subscriber state, and tags. |
| GET | v4/subscribers/{id} | read | subscribers | Returns a single subscriber's record: first name, email address, `state` (e.g. |
| PUT | v4/subscribers/{id} | write | subscribers | If you include a custom field key that does not exist on your account, the request returns an error. |
| POST | v4/subscribers/{id}/location | write | subscribers | Pins an explicit location to a subscriber, overriding any location Kit has inferred from open events. |
| PATCH | v4/subscribers/{id}/location | write | subscribers | Updates a subscriber's pinned location. |
| DELETE | v4/subscribers/{id}/location | write | subscribers | Removes the subscriber's pinned location and returns `204 No Content` on success. |
| GET | v4/subscribers/{id}/stats | read | subscribers | Retrieve email stats for a specific subscriber: totals for sent, opened, clicked, and bounced emails, open and click rates, and recency signals (`last_sent`, `last_opened`, `last_clicked`, and... |
| GET | v4/subscribers/{id}/tags | read | subscribers | Returns a cursor-paginated list of the tags currently applied to a subscriber, including when each was applied (`tagged_at`). |
| POST | v4/subscribers/{id}/unsubscribe | write | subscribers | Unsubscribes the subscriber from all future emails, moving them to the `cancelled` state. |
| POST | v4/bulk/tags | write | tags | See "Bulk & async processing" for more information. |
| DELETE | v4/bulk/tags | write | tags | See "Bulk & async processing" for more information. |
| POST | v4/bulk/tags/subscribers | write | tags | The subscribers being tagged must already exist. |
| DELETE | v4/bulk/tags/subscribers | write | tags | See "Bulk & async processing" for more information. |
| GET | v4/tags | read | tags | Returns a cursor-paginated list of all tags in the account with their `id`, `name`, and creation date. |
| POST | v4/tags | write | tags | Creates a tag with the given `name`. |
| PUT | v4/tags/{id} | write | tags | Renames a tag. |
| GET | v4/tags/{id}/subscribers | read | tags | Returns a cursor-paginated list of subscribers who have this tag. |
| POST | v4/tags/{id}/subscribers | write | tags | The subscriber being tagged must already exist. |
| DELETE | v4/tags/{id}/subscribers | write | tags | Removes the tag from a subscriber identified by the `email_address` query parameter, returning `204 No Content`. |
| POST | v4/tags/{id}/subscribers/{id} | write | tags | The subscriber being tagged must already exist. |
| DELETE | v4/tags/{id}/subscribers/{id} | write | tags | Removes the tag from the subscriber and returns `204 No Content`. |
| GET | v4/webhook_endpoints | read | webhooks | Returns a paginated list of the account's webhook endpoints. |
| POST | v4/webhook_endpoints | write | webhooks | Registers a URL to receive deliveries for the event types listed in `events`. |
| GET | v4/webhook_endpoints/{id} | read | webhooks | Returns a single webhook endpoint. |
| PATCH | v4/webhook_endpoints/{id} | write | webhooks | Updates any of `name`, `url`, `description`, `status`, and `events`. |
| DELETE | v4/webhook_endpoints/{id} | write | webhooks | Deletes the webhook endpoint and stops all future deliveries of its subscribed events. |
| GET | v4/webhook_endpoints/{id}/deliveries | read | webhooks | Returns a paginated list of deliveries for a webhook endpoint. |
| GET | v4/webhook_endpoints/{id}/deliveries/{id} | read | webhooks | Returns a single delivery record including its full attempt history — timestamps, HTTP status codes, and response bodies. |
| POST | v4/webhook_endpoints/{id}/revoke_previous_secret | write | webhooks | Closes a rotation's overlap window early: the previous secret stops verifying immediately, leaving only the current secret valid. |
| POST | v4/webhook_endpoints/{id}/rotate_secret | write | webhooks | Generates a new signing secret for the endpoint and returns it. |
| GET | v4/webhooks | read | webhooks-(legacy) | Legacy: This is the previous generation of Kit webhooks. |
| POST | v4/webhooks | write | webhooks-(legacy) | Legacy: This creates a previous-generation webhook. |
| DELETE | v4/webhooks/{id} | write | webhooks-(legacy) | Legacy: This deletes a previous-generation webhook. |
