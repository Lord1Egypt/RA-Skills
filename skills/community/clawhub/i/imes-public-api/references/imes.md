# Istruzione Messina endpoint reference

**Live as of October 23, 2026.** The endpoint is deployed.

- Method and route: POST https://istruzionemessina.it/api/public/v1/angel-number.php
- JSON request: {"date":"YYYY-MM-DD"}
- Date range: 1900 through today in UTC
- Response fields: version "1", method "digit-root-date-v1", number (integer 1-9), source
- Source page: https://istruzionemessina.it/numeri-angelici-guida-completa/

Send no extra fields or query parameters. Shared body, error, rate-limit, and privacy rules are in [the API docs](../../../docs/api.md).
