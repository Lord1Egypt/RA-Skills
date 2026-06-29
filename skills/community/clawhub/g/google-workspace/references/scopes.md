# Google Workspace Scopes

Use the narrowest scope that supports the requested operation. Prefer read-only
scopes during discovery.

## Common Read Scopes

| Surface | Scope | Use |
| --- | --- | --- |
| Admin Directory users | `https://www.googleapis.com/auth/admin.directory.user.readonly` | List or inspect users, aliases, org units, and profile metadata |
| Admin Directory groups | `https://www.googleapis.com/auth/admin.directory.group.readonly` | Inspect groups and memberships |
| Gmail metadata | `https://www.googleapis.com/auth/gmail.metadata` | Inspect message metadata without message bodies |
| Calendar read | `https://www.googleapis.com/auth/calendar.readonly` | Inspect calendars and events |
| Drive metadata | `https://www.googleapis.com/auth/drive.metadata.readonly` | Inspect file IDs, owners, MIME types, and permission metadata |

## Write Scopes

Escalate to write scopes only after the user approves the exact change plan.

| Surface | Scope | Typical write |
| --- | --- | --- |
| Users | `https://www.googleapis.com/auth/admin.directory.user` | Create, suspend, rename, or update users |
| Groups | `https://www.googleapis.com/auth/admin.directory.group` | Create groups or update group settings |
| Group members | `https://www.googleapis.com/auth/admin.directory.group.member` | Add or remove group members |
| Gmail settings | `https://www.googleapis.com/auth/gmail.settings.basic` | Labels, filters, forwarding, POP/IMAP settings |
| Calendar | `https://www.googleapis.com/auth/calendar` | Create, update, or delete events/calendars |
| Drive | `https://www.googleapis.com/auth/drive` | Transfer ownership or change sharing |

## Domain-Wide Delegation Checklist

1. Confirm the service account email and client ID.
2. Confirm the exact OAuth scopes approved in Admin Console.
3. Confirm the subject user being impersonated.
4. Confirm the API endpoint and expected audit log.
5. Run read-only verification before writes.
