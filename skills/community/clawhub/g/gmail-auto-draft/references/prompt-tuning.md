# Prompt Tuning

Use these flags to customize the generated reply style.

## Agency profile

```bash
--agency-profile "We are a performance marketing agency focused on SaaS and eCommerce growth."
```

## Style rules

```bash
--style-rules "Be concise, include one CTA, avoid jargon, and keep response under 140 words."
```

## Query tuning

Default query avoids self-sent emails and already processed emails:

```text
in:inbox is:unread -from:me -label:openclaw_auto_drafted
```

Examples:

- Leads only:

```bash
--query "in:inbox is:unread subject:(proposal OR quote OR pricing) -from:me -label:openclaw_auto_drafted"
```

- Exclude newsletters:

```bash
--query "in:inbox is:unread -from:me -category:promotions -label:openclaw_auto_drafted"
```

## Review-safe mode

Keep `--mark-read` disabled during early testing.

## Production mode

Enable `--mark-read` to avoid re-processing unread messages repeatedly.
