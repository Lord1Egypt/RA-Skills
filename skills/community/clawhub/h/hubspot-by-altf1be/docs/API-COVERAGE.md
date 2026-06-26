# HubSpot API — Coverage & Limitations

This document lists all API resources, what this skill covers, and what's excluded with reasons.

## Covered

| Resource | API | Commands | Notes |
|----------|-----|----------|-------|
| Contacts | CRM v3 | list, search, create, read, update, delete | Full CRUD with pagination |
| Companies | CRM v3 | list, search, create, read, update, delete | Full CRUD with pagination |
| Deals | CRM v3 | list, search, create, read, update, delete | Full CRUD with pagination |
| Tickets | CRM v3 | list, search, create, read, update, delete | Full CRUD with pagination |
| Owners | CRM v3 | list, read | Read-only (managed via HubSpot UI) |
| Pipelines | CRM v3 | list | Deals and tickets pipelines with stages |
| Associations | CRM v4 | list, create, delete | v4 associations API |
| Properties | CRM v3 | list | For any object type |
| Notes | CRM v3 | list | Engagement objects |
| Emails | CRM v3 | list | Engagement objects |
| Calls | CRM v3 | list | Engagement objects |
| Tasks | CRM v3 | list | Engagement objects |
| Meetings | CRM v3 | list | Engagement objects |
| Blog Posts | CMS v3 | list, read, create, update | Full CRUD (no delete — use HubSpot UI) |
| Site Pages | CMS v3 | list, read | Read-only |
| Domains | CMS v3 | list | Read-only |
| Email Campaigns | Email v1 | list, read | Legacy API (still functional) |
| Forms | Marketing v3 | list, read | Read-only |
| Marketing Emails | Marketing Emails v1 | list, read, stats | Includes send/open/click statistics |
| Contact Lists | Contacts v1 | list, read | Static and dynamic (smart) lists |
| Conversations | Conversations v3 | list, read | Inbox threads |
| Messages | Conversations v3 | list | Messages within threads |
| Workflows | Automation v3 | list, read | Read-only |

## Not Covered — With Reasons

### Custom Objects (`/crm/v3/schemas`, `/crm/v3/objects/{objectType}`)
- **Reason:** Requires schema discovery per portal — too dynamic for a generic CLI. Users can use the generic CRM v3 endpoints by name if needed.

### Files / File Manager (`/files/v3/files`)
- **Reason:** File upload/download requires multipart handling and large binary support — better suited for dedicated tools.

### HubDB (`/cms/v3/hubdb`)
- **Reason:** HubDB is a CMS-specific database feature used for dynamic pages. Niche use case, low CLI value.

### Transactional Email (`/transactional/v1/email`)
- **Reason:** Sends real emails to real recipients. Too risky for a CLI tool without a full confirmation/preview workflow.

### Webhooks (`/webhooks/v3`)
- **Reason:** Webhook management requires a running server to receive callbacks — not suitable for CLI.

### CRM Extensions / Timeline Events
- **Reason:** Requires app-level configuration. Admin-only, low general CLI value.

### Analytics (`/analytics/v2`)
- **Reason:** Complex reporting queries better served by HubSpot's dashboard UI or dedicated BI tools.

### CRM Imports (`/crm/v3/imports`)
- **Reason:** Bulk CSV import requires file handling and asynchronous job tracking.

### Social Media (`/broadcast/v1`)
- **Reason:** Legacy API, limited functionality. Separate social tools are more appropriate.

## Candidates for Future Versions

| Resource | Priority | Why |
|----------|----------|-----|
| Custom Objects | High | Growing adoption, could support via dynamic schema discovery |
| Files / File Manager | Medium | Useful for CMS content management workflows |
| HubDB | Medium | Useful for CMS-heavy portals |
| CRM Imports | Medium | Bulk data operations are common |
| Analytics | Low | Complex queries, better in HubSpot UI |
| Transactional Email | Low | Needs extensive safety guardrails |

## Categorized Exclusions

### Enterprise-Only Features
- Custom Objects (Enterprise tier for custom schemas)
- Advanced Workflows (some triggers/actions are Enterprise-only)

### Read-Only / No Write API
- Analytics (query-only)
- Some CMS page properties

### Admin-Only
- Webhook configuration
- CRM Extensions / Timeline Events
- Account settings / User provisioning

### UI-Internal / No CLI Value
- Drag-and-drop email editor
- Landing page builder
- Dashboard designer
- Social media composer

---

*Based on HubSpot API v3/v4 specification*
*Last updated: 2026-03-20*
