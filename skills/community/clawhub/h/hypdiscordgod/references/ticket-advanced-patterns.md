# Ticket Advanced Patterns

Use this reference when implementing richer ticket workflows.

## Claim Flow

- Allow staff to claim ownership of a ticket.
- Persist `claimed_by_user_id`.
- Prevent double-claim unless admins override.
- Show claim state in the ticket channel.

## Reopen Flow

- Reopen only from an archived/closed state.
- Restore or recreate access as needed.
- Mark who reopened and when if auditability matters.

## Transcript Flow

- Export before delete when the server wants records.
- Keep transcript format simple and durable.
- Include timestamps, author tags, and message content.
- Note limitations around attachments, embeds, and deleted content unless explicitly handled.
