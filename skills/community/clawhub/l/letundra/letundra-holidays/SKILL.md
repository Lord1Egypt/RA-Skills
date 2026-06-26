---
name: letundra-holidays
description: "Государственные праздники и фестивали в разных странах мира."
metadata: {"openclaw":{"emoji":"🎉","requires":{"bins":[]},"homepage":"https://letundra.com"}}
---

# Letundra Holidays

Праздники и выходные дни в разных странах.

## Когда использовать

- "Какие праздники в Таиланде?"
- "Выходные в Индии"
- "Когда Сонгкран?"

## Workflow

```
{{web_fetch url="https://letundra.com/ru/countries/{slug}/"}}
```

Извлеки секцию с праздниками.

## Output format

```markdown
# 🎉 Праздники в [Страна]

### Январь
- 1 января — Новый год
```
