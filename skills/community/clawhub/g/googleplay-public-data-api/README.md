# Google Play Public Data API

A read-only OpenClaw/Hermes skill for ReplyNodes' production Google Play data API.

## Coverage

The skill documents all eleven production operations: app details, search, similar apps, permissions, reviews, developer apps, categories, category apps, suggestions, availability, and data safety.

## Safety

The skill uses only public store data through `https://api.replynodes.com`. It never uses Google account credentials, cookies, OAuth sessions, publishing paths, catalog enumeration, or write operations. Keep the ReplyNodes API key in an environment variable and out of logs and reports.

## Pricing

The production capability matrix currently prices each operation at $0.003 per call. Check capabilities before making paid requests.
