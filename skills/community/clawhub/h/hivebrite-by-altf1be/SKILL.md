---
name: hivebrite-by-altf1be
description: "Hivebrite Admin API CLI — users, companies, events, groups, donations, memberships, emailings, mentoring, news, projects, media center, forums, and more. OAuth2 auth (password grant or refresh token) or bearer token."
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-hivebrite-by-altf1be
metadata:
  {"openclaw": {"emoji": "🐝", "requires": {"env": ["HIVEBRITE_BASE_URL", "HIVEBRITE_ACCESS_TOKEN"]}, "optional": {"env": ["HIVEBRITE_CLIENT_ID", "HIVEBRITE_CLIENT_SECRET", "HIVEBRITE_ADMIN_EMAIL", "HIVEBRITE_ADMIN_PASSWORD", "HIVEBRITE_REFRESH_TOKEN", "HIVEBRITE_MAX_RESULTS"]}, "primaryEnv": "HIVEBRITE_ACCESS_TOKEN"}}
---

# Hivebrite by @altf1be

Full Hivebrite Admin API CLI covering users, companies, events, groups, donations, memberships, emailings, mentoring, news, projects, media center, forums, admins, approvals, roles, receipts, categories, comments, posts, audit logs, engagement scoring, payment accounts, network settings, and more.

## Setup

1. Obtain API credentials from your Hivebrite admin panel (Settings > Integrations or API).
2. Set environment variables (or create `.env` in `{baseDir}`):

```
# Required — your Hivebrite instance URL
HIVEBRITE_BASE_URL=https://yourcommunity.hivebrite.com

# Auth Option 1: Bearer token (simplest)
HIVEBRITE_ACCESS_TOKEN=your-access-token

# Auth Option 2: OAuth2 password grant (set all four):
# HIVEBRITE_CLIENT_ID=your-client-id
# HIVEBRITE_CLIENT_SECRET=your-client-secret
# HIVEBRITE_ADMIN_EMAIL=admin@example.com
# HIVEBRITE_ADMIN_PASSWORD=your-password

# Auth Option 3: OAuth2 refresh token grant (set all three):
# HIVEBRITE_CLIENT_ID=your-client-id
# HIVEBRITE_CLIENT_SECRET=your-client-secret
# HIVEBRITE_REFRESH_TOKEN=your-refresh-token

# Optional
# HIVEBRITE_MAX_RESULTS=25
```

3. Install dependencies: `cd {baseDir} && npm install`

## API Info

- **Base URL:** `{HIVEBRITE_BASE_URL}/api/admin/v2/` (some endpoints use v1 or v3)
- **Auth:** OAuth2 (`grant_type=password` or `grant_type=refresh_token`) or Bearer token
- **Pagination:** RFC-5988 Link headers. Params: `page` (default 1), `per_page` (default 25, max 100)
- **Rate limits:** 300 requests/minute. Max 15 errors (5xx) per minute before throttling.

## Commands

### Me

```bash
node {baseDir}/scripts/hivebrite.mjs me
```

### Settings

```bash
node {baseDir}/scripts/hivebrite.mjs settings customizable-attributes
node {baseDir}/scripts/hivebrite.mjs settings fields-of-study
node {baseDir}/scripts/hivebrite.mjs settings industries
node {baseDir}/scripts/hivebrite.mjs settings job-functions
node {baseDir}/scripts/hivebrite.mjs settings currencies
```

### Network

```bash
node {baseDir}/scripts/hivebrite.mjs network info
node {baseDir}/scripts/hivebrite.mjs network sub-networks
node {baseDir}/scripts/hivebrite.mjs network citizenships
```

### Users

```bash
# List / search users
node {baseDir}/scripts/hivebrite.mjs users list
node {baseDir}/scripts/hivebrite.mjs users list --query "john"

# CRUD
node {baseDir}/scripts/hivebrite.mjs users read --id 123
node {baseDir}/scripts/hivebrite.mjs users create --email "jane@example.com" --firstname Jane --lastname Doe
node {baseDir}/scripts/hivebrite.mjs users update --id 123 --phone "+1234567890"
node {baseDir}/scripts/hivebrite.mjs users delete --id 123 --confirm

# Sub-resources
node {baseDir}/scripts/hivebrite.mjs users experiences --user-id 123
node {baseDir}/scripts/hivebrite.mjs users educations --user-id 123
node {baseDir}/scripts/hivebrite.mjs users notification-settings --user-id 123
node {baseDir}/scripts/hivebrite.mjs users postal-addresses --user-id 123
node {baseDir}/scripts/hivebrite.mjs users group-membership --user-id 123

# Special actions
node {baseDir}/scripts/hivebrite.mjs users find-by-field --field email --value "jane@example.com"
node {baseDir}/scripts/hivebrite.mjs users notify --id 123 --subject "Hello" --message "Welcome!"
node {baseDir}/scripts/hivebrite.mjs users activate --id 123
```

### Experiences (standalone)

```bash
node {baseDir}/scripts/hivebrite.mjs experiences list
node {baseDir}/scripts/hivebrite.mjs experiences read --id 456
node {baseDir}/scripts/hivebrite.mjs experiences create --user-id 123 --title "Engineer" --organization "Acme"
node {baseDir}/scripts/hivebrite.mjs experiences update --id 456 --title "Senior Engineer"
node {baseDir}/scripts/hivebrite.mjs experiences delete --id 456 --confirm
node {baseDir}/scripts/hivebrite.mjs experiences customizable-attributes
```

### Educations (standalone)

```bash
node {baseDir}/scripts/hivebrite.mjs educations list
node {baseDir}/scripts/hivebrite.mjs educations read --id 789
node {baseDir}/scripts/hivebrite.mjs educations create --user-id 123 --degree "MSc" --school "MIT"
node {baseDir}/scripts/hivebrite.mjs educations update --id 789 --field "Computer Science"
node {baseDir}/scripts/hivebrite.mjs educations delete --id 789 --confirm
node {baseDir}/scripts/hivebrite.mjs educations customizable-attributes
```

### Emailings

```bash
# Categories
node {baseDir}/scripts/hivebrite.mjs emailings categories list
node {baseDir}/scripts/hivebrite.mjs emailings categories read --id 10
node {baseDir}/scripts/hivebrite.mjs emailings categories create --name "Newsletter"
node {baseDir}/scripts/hivebrite.mjs emailings categories update --id 10 --name "Monthly Newsletter"
node {baseDir}/scripts/hivebrite.mjs emailings categories delete --id 10 --confirm

# Campaigns
node {baseDir}/scripts/hivebrite.mjs emailings campaigns list
node {baseDir}/scripts/hivebrite.mjs emailings campaigns read --id 20
node {baseDir}/scripts/hivebrite.mjs emailings campaigns create --subject "Spring Update" --name "Spring 2026"
node {baseDir}/scripts/hivebrite.mjs emailings campaigns update --id 20 --subject "Updated Subject"
node {baseDir}/scripts/hivebrite.mjs emailings campaigns delete --id 20 --confirm
node {baseDir}/scripts/hivebrite.mjs emailings campaigns send --id 20
```

### Groups

```bash
# Groups CRUD
node {baseDir}/scripts/hivebrite.mjs groups list
node {baseDir}/scripts/hivebrite.mjs groups read --id 30
node {baseDir}/scripts/hivebrite.mjs groups create --name "Alumni Paris"
node {baseDir}/scripts/hivebrite.mjs groups update --id 30 --description "Paris chapter"
node {baseDir}/scripts/hivebrite.mjs groups delete --id 30 --confirm

# Group users
node {baseDir}/scripts/hivebrite.mjs groups users list --group-id 30
node {baseDir}/scripts/hivebrite.mjs groups users add --group-id 30 --user-id 123
node {baseDir}/scripts/hivebrite.mjs groups users remove --group-id 30 --user-id 123 --confirm

# Topic categories
node {baseDir}/scripts/hivebrite.mjs groups topic-categories --group-id 30
```

### Companies

```bash
node {baseDir}/scripts/hivebrite.mjs companies list
node {baseDir}/scripts/hivebrite.mjs companies list --query "Acme"
node {baseDir}/scripts/hivebrite.mjs companies read --id 40
node {baseDir}/scripts/hivebrite.mjs companies create --name "Acme Corp" --industry "Technology"
node {baseDir}/scripts/hivebrite.mjs companies update --id 40 --website "https://acme.com"
node {baseDir}/scripts/hivebrite.mjs companies delete --id 40 --confirm
```

### News

```bash
# Categories
node {baseDir}/scripts/hivebrite.mjs news categories list
node {baseDir}/scripts/hivebrite.mjs news categories read --id 50
node {baseDir}/scripts/hivebrite.mjs news categories create --name "Announcements"
node {baseDir}/scripts/hivebrite.mjs news categories update --id 50 --name "Official News"
node {baseDir}/scripts/hivebrite.mjs news categories delete --id 50 --confirm

# Posts
node {baseDir}/scripts/hivebrite.mjs news posts list
node {baseDir}/scripts/hivebrite.mjs news posts read --id 60
node {baseDir}/scripts/hivebrite.mjs news posts create --title "Welcome!" --body "<p>Hello world</p>"
node {baseDir}/scripts/hivebrite.mjs news posts update --id 60 --title "Updated Title"
node {baseDir}/scripts/hivebrite.mjs news posts delete --id 60 --confirm
node {baseDir}/scripts/hivebrite.mjs news posts duplicate --id 60
```

### Roles

```bash
node {baseDir}/scripts/hivebrite.mjs roles list
node {baseDir}/scripts/hivebrite.mjs roles read --id 70
```

### Business Opportunities

```bash
node {baseDir}/scripts/hivebrite.mjs business-opportunities list
node {baseDir}/scripts/hivebrite.mjs business-opportunities read --id 80
node {baseDir}/scripts/hivebrite.mjs business-opportunities create --title "Senior Dev" --type "job" --company "Acme"
node {baseDir}/scripts/hivebrite.mjs business-opportunities update --id 80 --status "closed"
node {baseDir}/scripts/hivebrite.mjs business-opportunities delete --id 80 --confirm
```

### Receipts

```bash
node {baseDir}/scripts/hivebrite.mjs receipts list
node {baseDir}/scripts/hivebrite.mjs receipts read --id 90
node {baseDir}/scripts/hivebrite.mjs receipts update --id 90 --status "paid"
```

### Pages (customizable)

```bash
node {baseDir}/scripts/hivebrite.mjs pages list
node {baseDir}/scripts/hivebrite.mjs pages read --id 100
node {baseDir}/scripts/hivebrite.mjs pages create --title "About Us"
node {baseDir}/scripts/hivebrite.mjs pages update --id 100 --title "About Our Community"
node {baseDir}/scripts/hivebrite.mjs pages delete --id 100 --confirm
```

### Approvals

```bash
node {baseDir}/scripts/hivebrite.mjs approvals list
node {baseDir}/scripts/hivebrite.mjs approvals read --id 110
node {baseDir}/scripts/hivebrite.mjs approvals approve --id 110
node {baseDir}/scripts/hivebrite.mjs approvals reject --id 110
node {baseDir}/scripts/hivebrite.mjs approvals link-to-user --id 110 --user-id 123
node {baseDir}/scripts/hivebrite.mjs approvals delete --id 110 --confirm
```

### Versions (deleted items)

```bash
node {baseDir}/scripts/hivebrite.mjs versions list
node {baseDir}/scripts/hivebrite.mjs versions list --item-type "User"
```

### Comments (v3 API)

```bash
node {baseDir}/scripts/hivebrite.mjs comments list
node {baseDir}/scripts/hivebrite.mjs comments list --commentable-type "News" --commentable-id 60
node {baseDir}/scripts/hivebrite.mjs comments read --id 120
node {baseDir}/scripts/hivebrite.mjs comments create --body "Great post!" --commentable-type "News" --commentable-id 60
node {baseDir}/scripts/hivebrite.mjs comments update --id 120 --body "Updated comment"
node {baseDir}/scripts/hivebrite.mjs comments delete --id 120 --confirm
```

### Posts (v3 API)

```bash
node {baseDir}/scripts/hivebrite.mjs posts list
node {baseDir}/scripts/hivebrite.mjs posts read --id 130
node {baseDir}/scripts/hivebrite.mjs posts create --body "Hello community!" --group-id 30
node {baseDir}/scripts/hivebrite.mjs posts update --id 130 --body "Updated post"
node {baseDir}/scripts/hivebrite.mjs posts delete --id 130 --confirm
```

### Events

```bash
# Events CRUD
node {baseDir}/scripts/hivebrite.mjs events list
node {baseDir}/scripts/hivebrite.mjs events read --id 140
node {baseDir}/scripts/hivebrite.mjs events create --name "Annual Gala" --starts-at "2026-06-15T18:00:00Z" --location "Brussels"
node {baseDir}/scripts/hivebrite.mjs events update --id 140 --capacity 200
node {baseDir}/scripts/hivebrite.mjs events delete --id 140 --confirm
node {baseDir}/scripts/hivebrite.mjs events cancel --id 140
node {baseDir}/scripts/hivebrite.mjs events duplicate --id 140
node {baseDir}/scripts/hivebrite.mjs events customizable-attributes

# Tickets
node {baseDir}/scripts/hivebrite.mjs events tickets list --event-id 140
node {baseDir}/scripts/hivebrite.mjs events tickets read --event-id 140 --id 1
node {baseDir}/scripts/hivebrite.mjs events tickets create --event-id 140 --name "VIP" --price 50 --currency EUR
node {baseDir}/scripts/hivebrite.mjs events tickets update --event-id 140 --id 1 --price 75
node {baseDir}/scripts/hivebrite.mjs events tickets delete --event-id 140 --id 1 --confirm

# Bookings
node {baseDir}/scripts/hivebrite.mjs events bookings list --event-id 140
node {baseDir}/scripts/hivebrite.mjs events bookings read --event-id 140 --id 2
node {baseDir}/scripts/hivebrite.mjs events bookings create --event-id 140 --user-id 123 --ticket-id 1
node {baseDir}/scripts/hivebrite.mjs events bookings update --event-id 140 --id 2 --status "confirmed"
node {baseDir}/scripts/hivebrite.mjs events bookings delete --event-id 140 --id 2 --confirm

# Attendees
node {baseDir}/scripts/hivebrite.mjs events attendees list --event-id 140
node {baseDir}/scripts/hivebrite.mjs events attendees read --event-id 140 --id 3
node {baseDir}/scripts/hivebrite.mjs events attendees create --event-id 140 --user-id 123
node {baseDir}/scripts/hivebrite.mjs events attendees update --event-id 140 --id 3 --checked-in true
node {baseDir}/scripts/hivebrite.mjs events attendees delete --event-id 140 --id 3 --confirm

# RSVPs
node {baseDir}/scripts/hivebrite.mjs events rsvps list --event-id 140
node {baseDir}/scripts/hivebrite.mjs events rsvps read --event-id 140 --id 4
node {baseDir}/scripts/hivebrite.mjs events rsvps create --event-id 140 --user-id 123 --status "attending"
node {baseDir}/scripts/hivebrite.mjs events rsvps update --event-id 140 --id 4 --status "declined"
node {baseDir}/scripts/hivebrite.mjs events rsvps delete --event-id 140 --id 4 --confirm
```

### Projects (Ventures)

```bash
node {baseDir}/scripts/hivebrite.mjs projects list
node {baseDir}/scripts/hivebrite.mjs projects read --id 150
node {baseDir}/scripts/hivebrite.mjs projects create --name "Innovation Lab"
node {baseDir}/scripts/hivebrite.mjs projects update --id 150 --status "active"
node {baseDir}/scripts/hivebrite.mjs projects delete --id 150 --confirm

# Team members
node {baseDir}/scripts/hivebrite.mjs projects team-members list --project-id 150
node {baseDir}/scripts/hivebrite.mjs projects team-members add --project-id 150 --user-id 123 --role "lead"
node {baseDir}/scripts/hivebrite.mjs projects team-members update --project-id 150 --id 5 --role "member"
node {baseDir}/scripts/hivebrite.mjs projects team-members remove --project-id 150 --id 5 --confirm
```

### Memberships

```bash
# Types
node {baseDir}/scripts/hivebrite.mjs memberships types list
node {baseDir}/scripts/hivebrite.mjs memberships types read --id 160
node {baseDir}/scripts/hivebrite.mjs memberships types create --name "Premium" --price 99 --currency EUR
node {baseDir}/scripts/hivebrite.mjs memberships types update --id 160 --price 149
node {baseDir}/scripts/hivebrite.mjs memberships types delete --id 160 --confirm

# Subscriptions
node {baseDir}/scripts/hivebrite.mjs memberships subscriptions list
node {baseDir}/scripts/hivebrite.mjs memberships subscriptions list --user-id 123
node {baseDir}/scripts/hivebrite.mjs memberships subscriptions read --id 170
node {baseDir}/scripts/hivebrite.mjs memberships subscriptions create --user-id 123 --type-id 160
node {baseDir}/scripts/hivebrite.mjs memberships subscriptions update --id 170 --status "active"
node {baseDir}/scripts/hivebrite.mjs memberships subscriptions delete --id 170 --confirm

# Payment options
node {baseDir}/scripts/hivebrite.mjs memberships payment-options --type-id 160
```

### Engagement Scoring

```bash
node {baseDir}/scripts/hivebrite.mjs engagement rankings
node {baseDir}/scripts/hivebrite.mjs engagement user-rank --user-id 123
```

### Payment Accounts

```bash
node {baseDir}/scripts/hivebrite.mjs payment-accounts list
node {baseDir}/scripts/hivebrite.mjs payment-accounts read --id 180
```

### Categories

```bash
node {baseDir}/scripts/hivebrite.mjs categories list
node {baseDir}/scripts/hivebrite.mjs categories read --id 190
node {baseDir}/scripts/hivebrite.mjs categories create --name "Technology"
node {baseDir}/scripts/hivebrite.mjs categories update --id 190 --name "Tech & Innovation"
node {baseDir}/scripts/hivebrite.mjs categories delete --id 190 --confirm
```

### Current Locations

```bash
node {baseDir}/scripts/hivebrite.mjs current-locations list
node {baseDir}/scripts/hivebrite.mjs current-locations read --id 200
```

### Media Center

```bash
# Files
node {baseDir}/scripts/hivebrite.mjs media files list
node {baseDir}/scripts/hivebrite.mjs media files list --folder-id 10
node {baseDir}/scripts/hivebrite.mjs media files read --id 210
node {baseDir}/scripts/hivebrite.mjs media files create --name "logo.png" --url "https://example.com/logo.png"
node {baseDir}/scripts/hivebrite.mjs media files update --id 210 --name "new-logo.png"
node {baseDir}/scripts/hivebrite.mjs media files delete --id 210 --confirm
node {baseDir}/scripts/hivebrite.mjs media files move --id 210 --folder-id 20
node {baseDir}/scripts/hivebrite.mjs media files download-url --id 210

# Folders
node {baseDir}/scripts/hivebrite.mjs media folders list
node {baseDir}/scripts/hivebrite.mjs media folders read --id 220
node {baseDir}/scripts/hivebrite.mjs media folders create --name "Photos" --parent-id 10
node {baseDir}/scripts/hivebrite.mjs media folders update --id 220 --name "Event Photos"
node {baseDir}/scripts/hivebrite.mjs media folders delete --id 220 --confirm
node {baseDir}/scripts/hivebrite.mjs media folders move --id 220 --parent-id 30

# Root folder
node {baseDir}/scripts/hivebrite.mjs media root-folder
```

### Audit Logs

```bash
node {baseDir}/scripts/hivebrite.mjs audit-logs list
```

### Admins

```bash
node {baseDir}/scripts/hivebrite.mjs admins list
node {baseDir}/scripts/hivebrite.mjs admins read --id 230
node {baseDir}/scripts/hivebrite.mjs admins create --email "admin@example.com" --firstname John --role "admin"
node {baseDir}/scripts/hivebrite.mjs admins update --id 230 --role "super_admin"
node {baseDir}/scripts/hivebrite.mjs admins delete --id 230 --confirm
```

### Mentoring

```bash
# Mentee profiles
node {baseDir}/scripts/hivebrite.mjs mentoring mentees list
node {baseDir}/scripts/hivebrite.mjs mentoring mentees read --id 240
node {baseDir}/scripts/hivebrite.mjs mentoring mentees create --user-id 123 --program-id 10
node {baseDir}/scripts/hivebrite.mjs mentoring mentees update --id 240 --status "active"
node {baseDir}/scripts/hivebrite.mjs mentoring mentees delete --id 240 --confirm

# Mentor profiles
node {baseDir}/scripts/hivebrite.mjs mentoring mentors list
node {baseDir}/scripts/hivebrite.mjs mentoring mentors read --id 250
node {baseDir}/scripts/hivebrite.mjs mentoring mentors create --user-id 456 --program-id 10
node {baseDir}/scripts/hivebrite.mjs mentoring mentors update --id 250 --status "active"
node {baseDir}/scripts/hivebrite.mjs mentoring mentors delete --id 250 --confirm

# Programs
node {baseDir}/scripts/hivebrite.mjs mentoring programs list
node {baseDir}/scripts/hivebrite.mjs mentoring programs read --id 10
node {baseDir}/scripts/hivebrite.mjs mentoring programs create --name "Leadership 2026"
node {baseDir}/scripts/hivebrite.mjs mentoring programs update --id 10 --status "active"
node {baseDir}/scripts/hivebrite.mjs mentoring programs delete --id 10 --confirm

# Relationships
node {baseDir}/scripts/hivebrite.mjs mentoring relationships list
node {baseDir}/scripts/hivebrite.mjs mentoring relationships read --id 260
node {baseDir}/scripts/hivebrite.mjs mentoring relationships create --mentor-profile-id 250 --mentee-profile-id 240 --program-id 10
node {baseDir}/scripts/hivebrite.mjs mentoring relationships update --id 260 --status "completed"
node {baseDir}/scripts/hivebrite.mjs mentoring relationships delete --id 260 --confirm

# Customizable attributes
node {baseDir}/scripts/hivebrite.mjs mentoring customizable-attributes
```

### Order Management (manual transactions)

```bash
node {baseDir}/scripts/hivebrite.mjs orders create --user-id 123 --amount 50 --currency EUR --description "Manual payment"
node {baseDir}/scripts/hivebrite.mjs orders update --id 270 --amount 75
node {baseDir}/scripts/hivebrite.mjs orders delete --id 270 --confirm
```

### Email Analytics

```bash
node {baseDir}/scripts/hivebrite.mjs email-analytics deliveries
node {baseDir}/scripts/hivebrite.mjs email-analytics deliveries --campaign-id 20
```

### Forums

```bash
node {baseDir}/scripts/hivebrite.mjs forums list
node {baseDir}/scripts/hivebrite.mjs forums read --id 280
node {baseDir}/scripts/hivebrite.mjs forums create --title "General Discussion" --body "Welcome to the forum!"
node {baseDir}/scripts/hivebrite.mjs forums update --id 280 --title "Updated Title"
node {baseDir}/scripts/hivebrite.mjs forums delete --id 280 --confirm
```

### Notifications

```bash
node {baseDir}/scripts/hivebrite.mjs notifications list
```

### Sub-Networks (clusters)

```bash
node {baseDir}/scripts/hivebrite.mjs sub-networks clusters
```

### User Data Fields

```bash
node {baseDir}/scripts/hivebrite.mjs user-data-fields list
```

### Donations

```bash
# Funds
node {baseDir}/scripts/hivebrite.mjs donations funds list
node {baseDir}/scripts/hivebrite.mjs donations funds read --id 290
node {baseDir}/scripts/hivebrite.mjs donations funds create --name "Scholarship Fund" --goal 10000 --currency EUR
node {baseDir}/scripts/hivebrite.mjs donations funds update --id 290 --goal 15000
node {baseDir}/scripts/hivebrite.mjs donations funds delete --id 290 --confirm

# Campaigns
node {baseDir}/scripts/hivebrite.mjs donations campaigns list
node {baseDir}/scripts/hivebrite.mjs donations campaigns read --id 300
node {baseDir}/scripts/hivebrite.mjs donations campaigns create --name "Year-End Drive" --fund-id 290
node {baseDir}/scripts/hivebrite.mjs donations campaigns update --id 300 --name "Updated Campaign"
node {baseDir}/scripts/hivebrite.mjs donations campaigns delete --id 300 --confirm

# Donations
node {baseDir}/scripts/hivebrite.mjs donations items list
node {baseDir}/scripts/hivebrite.mjs donations items list --fund-id 290
node {baseDir}/scripts/hivebrite.mjs donations items read --id 310
node {baseDir}/scripts/hivebrite.mjs donations items create --user-id 123 --amount 100 --currency EUR --fund-id 290
node {baseDir}/scripts/hivebrite.mjs donations items update --id 310 --status "completed"
node {baseDir}/scripts/hivebrite.mjs donations items delete --id 310 --confirm

# Gift
node {baseDir}/scripts/hivebrite.mjs donations gift --id 320

# Customizable attributes
node {baseDir}/scripts/hivebrite.mjs donations customizable-attributes
```

### Pagination (all list commands)

All list commands support pagination:

```bash
node {baseDir}/scripts/hivebrite.mjs users list --limit 50 --page 2
node {baseDir}/scripts/hivebrite.mjs events list --limit 100 --page 3
```

## Security

- Auth method: Bearer token or OAuth 2.0 with auto-refresh (password/refresh_token grant)
- No secrets or tokens printed to stdout
- All delete operations require explicit `--confirm` flag
- Built-in rate limiting with exponential backoff retry (3 attempts)
- OAuth tokens cached in `~/.cache/openclaw/hivebrite-token.json`
- Lazy config validation (only checked when a command runs)

## Dependencies

- `commander` — CLI framework
- `dotenv` — environment variable loading
- Node.js built-in `fetch` (requires Node >= 18)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels 🇧🇪 🇲🇦
X: [@altf1be](https://x.com/altf1be)
