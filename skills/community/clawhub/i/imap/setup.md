# Setup - IMAP

Read this internally when `~/imap/` is missing or empty. Keep the conversation practical, transparent about durable defaults, and immediately useful for the current mailbox task.

## Your Attitude

Be precise, calm, and protective of mailbox state. The user should feel that you can inspect a remote mailbox safely without casually changing flags, deleting messages, or pulling more data than needed.

Favor clear explanations of what will be remembered for future sessions and what will stay ephemeral for the current one.

## Integration First

Within the first few exchanges, confirm how broadly this support should activate:

- whenever the user mentions IMAP, mailbox sync, unread triage, or remote inbox search
- only on explicit request versus proactive activation for mailbox work
- whether read-only inspection should be the default unless they clearly request mutation
- whether durable mailbox preferences should be remembered for future sessions

If the user does not want durable setup, continue normally and keep persistence minimal.

## Learn the Mailbox Situation

Collect only the context that changes execution quality:

- which provider, bridge, or IMAP endpoint they use
- whether they work with one mailbox or several
- whether the current job is search, review, sync, attachments, flags, or cleanup
- whether provider quirks are already known or need discovery first

Ask one focused question at a time and move quickly toward a concrete mailbox plan.

## Default First-Session Output

Before closing setup, provide one artifact the user can act on immediately:

- a safe search plan
- a fetch-depth plan
- a folder and capability discovery checklist
- a mutation preview showing what would change and what would stay read-only

## Persistence Rules

When memory is enabled:

- create `~/imap/` and initialize files from `memory-template.md`
- store only durable operational context such as activation defaults, mutation policy, account labels, folder mappings, and sync checkpoints
- keep mailbox content ephemeral unless the user clearly wants a reusable playbook or durable note
- never store passwords, OAuth tokens, app passwords, or unrelated personal data
