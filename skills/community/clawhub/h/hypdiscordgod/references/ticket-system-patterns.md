# Ticket System Patterns

Use this reference when implementing support tickets, applications, appeals, or private staff workflows.

## Core Flow

1. user opens ticket
2. bot creates or assigns private channel/thread
3. bot stores ticket state
4. staff interact with close/reopen/claim actions
5. bot archives or deletes according to policy

## Data Model

Typical fields:
- `ticket_id`
- `guild_id`
- `channel_id`
- `creator_user_id`
- `status`
- `claimed_by_user_id`
- `created_at`
- `closed_at`
- `topic` or `reason`

## Safety Rules

- Prevent duplicate open tickets when policy requires one-per-user.
- Validate staff permissions for claim/close/reopen actions.
- Handle missing channel/category gracefully.
- Consider transcript export before deletion.

## UX Guidance

- Use buttons for open/close/claim where possible.
- Send clear status messages when ticket state changes.
- Keep admin configuration separate from user-facing flows.
