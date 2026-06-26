# Filter Catalog

## Non-actionable defaults

### Newsletters

Signals:
- `List-Unsubscribe`
- newsletter / digest phrasing
- unsubscribe and view-in-browser links

Typical action:
- add `Newsletter`
- remove `INBOX`

Language coverage should include English, Portuguese, and Spanish terms when defining keyword-based newsletter filters.

### Promotions

Signals:
- discount language
- coupons
- sales campaigns
- retail / growth marketing layout

Typical action:
- add `CATEGORY_PROMOTIONS`
- remove `INBOX`

### Notifications

Signals:
- system status or account activity updates
- service notices
- automated alerts that do not require user action
- Portuguese and Spanish SaaS/system variants such as `notificação`, `atualização`, `recordatorio`, `actualización`

Typical action:
- add `CATEGORY_UPDATES`
- remove `INBOX`

### Ordinary receipts

Signals:
- payment confirmed
- invoice available
- thank-you receipt language
- no due / expired / failed-payment urgency

Typical action:
- add `Receipt`
- remove `INBOX`

## Actionable defaults

### Billing issues

Signals:
- overdue
- payment due
- failed payment
- expired subscription
- renewal required

Typical action:
- add `Receipt`
- add `STARRED`
- keep in Inbox
- optional notify

### Replies

Signals:
- `Re:` subject
- `In-Reply-To`
- `References`
- conversational follow-up tone

Typical action:
- add `IMPORTANT`
- keep in Inbox

### Opportunities

Signals:
- partnership
- sponsorship
- consulting / speaking request
- proposal / pilot / commercial inquiry

Exclude generic social-network activity, product onboarding, and automated invitation acceptance messages unless there is clear commercial intent.
Do not use plain `invitation` by itself as an opportunity signal.

Typical action:
- add `Opportunity`
- add `STARRED`
- keep in Inbox
- optional notify

### Action Required

Signals:
- explicit request for confirmation or completion
- asks for a form, document, approval, or response
- typically from a person

Typical action:
- add `Action Required`
- add `IMPORTANT`
- keep in Inbox
- optional notify

## Local-only examples

The following categories are intentionally better kept in local overlays instead of shared defaults:
- press releases / PR blasts
- press trips / media invitations
- company-specific lead routing
- custom editorial or operational labels
