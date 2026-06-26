---
name: monobank
description: >
  Answer Monobank balance questions by calling the Monobank API directly with a
  user-supplied per-request API token. Use when: скільки грошей у мене на
  монобанку, баланс mono, баланс Monobank, monobank accounts, monobank balance,
  checking Ukrainian Monobank cards and jars.
homepage: https://monobank-mcp.mandate.md
version: 1.2.0
category: finance
emoji: "💳"
author: Roman Krutovoy
author_url: https://krutovoy.me
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    endpoints:
      - https://api.monobank.ua/personal/client-info
---

# Monobank

Use this skill when the user asks about Monobank balances, for example:

- "скільки грошей у мене на монобанку?"
- "баланс mono"
- "monobank accounts"

## Privacy

Call the Monobank API directly. Do not route real user balances through a hosted MCP, proxy, or third-party server.

The user must provide `monobank_token` for each request. Never store it in files, env vars, memory, directives, logs, summaries, or future context.

If the token is missing, answer in Ukrainian:

```text
Потрібен API token monobank. Отримати можна тут: https://api.monobank.ua/
```

## API Call

Call:

```text
GET https://api.monobank.ua/personal/client-info
X-Token: <monobank_token>
Accept: application/json
```

Use an HTTP/fetch tool that can pass headers without printing them. Do not put the token into visible shell commands, logs, URLs, or final answers.

If direct HTTP access is unavailable, say in Ukrainian that an HTTP-capable runtime or tool is needed. Do not use hosted MCP for real balances.

## Errors and Limits

- `401` or `403`: say in Ukrainian that the Monobank API token was not accepted.
- `429`: say in Ukrainian that Monobank allows this endpoint no more than once per 60 seconds per token.
- Network or `5xx`: say in Ukrainian that Monobank API did not return the balance right now.
- Never show raw API errors if they may contain identifiers or token material.

## Data Handling

Amounts are minor units. Divide by 100 and show two decimals.

Currency codes:

- `980` -> `UAH`
- `840` -> `USD`
- `978` -> `EUR`
- unknown code -> `ISO-4217:<code>`

For each account:

- Label: `<type> **** <last4>` from `maskedPan[0]`.
- If `maskedPan` is absent, use a safe label like `<type>` or masked IBAN `IBAN UA12...3456`.
- Do not expose raw account IDs, send IDs, full IBANs, client ID, webhook URL, or token.

Credit-account semantics:

- Monobank raw `balance` means the amount available with credit already included.
- If `creditLimit > 0`, real account balance is `balance - creditLimit`.
- If `creditLimit == 0`, real account balance is `balance`.
- In the response, "доступно з кредитними" is raw `balance`.

Jars:

- Show jars separately after accounts.
- Format: `Банка <title>: <balance> з <goal>.`
- Omit `з <goal>` if `goal` is absent.

## Response Language

The skill instructions are in English, but user-facing balance answers must be in Ukrainian by default.

If the user explicitly asks to answer in another language, keep the same structure and translate only service labels. Do not translate card types, masked PANs, currencies, jar titles, or numbers.

## Response Format

Keep the response concise. Use this format:

```text
Monobank:

platinum **** 1286: баланс -42340.34 UAH; кредитний ліміт 80000.00 UAH; доступно з кредитними 37659.66 UAH.
white **** 5708: баланс 4102.17 UAH; доступно 4102.17 UAH.
black **** 7760: баланс 3.99 USD; доступно 3.99 USD.
black **** 2025: баланс 0.77 EUR; доступно 0.77 EUR.

Банка Фонд Meta Gamers: 0.97 UAH з 10000.00 UAH.
Банка На подарки: 9.49 UAH з 40000.00 UAH.
```
