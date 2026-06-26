# Search and Fetch

Use this guide when the user needs precise mailbox retrieval.

## Search Principles

- Prefer server-side search over downloading full folders.
- Scope the folder first; cross-folder scans are more expensive and often noisier.
- Combine filters intentionally: dates, sender, subject fragments, flags, size, and UID ranges.
- Be explicit about what the server search can and cannot match reliably.

## Recommended Search Ladder

1. Confirm folder scope.
2. Use the narrowest server-side search that could succeed.
3. Fetch UIDs and lightweight metadata for the result set.
4. Expand to body parts or attachments only for the messages worth inspecting.

## Fetch Depth Ladder

### Level 1: Mailbox inventory
- folder names
- counts
- recent and unseen tallies

### Level 2: Lightweight message metadata
- UID
- flags
- internal date
- envelope
- selected headers such as From, To, Subject, Message-ID

### Level 3: Content sampling
- text/plain or text/html part preview
- specific body sections
- bodystructure or MIME map

### Level 4: Full content
- complete RFC822 source
- attachment download
- large body retrieval

Use the lowest level that solves the task.

## Charset and Text Handling

- Do not assume UTF-8 everywhere.
- Track declared charset and transfer encoding for each part.
- If the search result looks inconsistent, suspect server search semantics, MIME encoding, or provider indexing quirks before claiming the message is missing.

## Reporting Pattern

When presenting results, include:
- folder searched
- filters applied
- number of matches
- what was fetched
- whether anything remains uninspected

That makes follow-up fetches safer and faster.
