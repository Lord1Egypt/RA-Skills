# Source strategy

## Priority order for the current target market

1. hh.ru
2. Habr Career
3. Telegram vacancy channels and chats
4. LinkedIn

## Why this order

- `hh.ru` gives the broadest coverage for the Russian market.
- `Habr Career` often has better signal for engineering vacancies.
- `Telegram` provides fresh leads but is noisy and duplicated.
- `LinkedIn` is useful mainly for stronger-than-local opportunities or international remote roles.

## Source-specific extraction hints

### hh.ru
Extract:
- title
- company
- salary range and currency
- gross/net if stated
- location
- remote/office/hybrid
- experience level
- employment type
- key stack

### Habr Career
Extract:
- title
- company
- salary range
- stack
- seniority
- product/domain
- remote/office/hybrid
- hiring process details if present

### Telegram
Extract from free text:
- title
- company
- stack
- salary or compensation hints
- remote/office/hybrid
- city or timezone
- contact handle or bot
- channel/chat source

For Telegram, also store raw text excerpt because structured extraction will be lossy.

### LinkedIn
Extract:
- title
- company
- location
- remote mode
- seniority
- stack hints
- application path

## Deduplication rules

Treat vacancies as possible duplicates when at least two of these match:
- same company + same/similar title
- same company + same stack + close salary
- same external URL
- Telegram post appears to mirror hh/Habr/LinkedIn posting

Prefer the richest source record as the canonical one and keep backlinks to duplicates.
