---
name: letundra-currency
description: "Курсы валют стран мира к рублю. Конвертация валют для планирования бюджета путешествий."
metadata: {"openclaw":{"emoji":"💱","requires":{"bins":[]},"homepage":"https://letundra.com"}}
---

# Letundra Currency

Курсы валют с letundra.com.

## Когда использовать

- "Курс бата к рублю"
- "Сколько стоит 1000 батов в рублях?"
- "Валюта ОАЭ"

## Workflow

```
{{web_fetch url="https://letundra.com/ru/countries/{slug}/"}}
```

Извлеки секцию с курсом валют.

## Output format

```markdown
# 💱 Курс [Валюта]

**1 [валюта] = X.XX RUB**
```
