# Permission profiles

Use least privilege for your scenario.

## mail-only

- `Mail.ReadWrite`
- `Mail.Send` (optional if you send messages)
- `offline_access`

## calendar-only

- `Calendars.ReadWrite`
- `offline_access`

## contacts-only

- `Contacts.ReadWrite`
- `offline_access`

## full-suite

- `Mail.ReadWrite`
- `Mail.Send`
- `Calendars.ReadWrite`
- `Files.ReadWrite.All`
- `Contacts.ReadWrite`
- `offline_access`

## Client ID guidance

- The public default `client_id` in this repository is for quick testing only.
- For production, register and use your own Microsoft Entra App Registration.
- A `client_id` is not a secret, but ownership, consent, and operational control matter for production.
