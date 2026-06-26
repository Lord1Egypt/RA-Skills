---
name: letundra-news
description: "Новости авиации и путешествий с letundra.com. Получение последних новостей, фильтрация по странам и авиакомпаниям."
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":[]},"homepage":"https://letundra.com"}}
---

# Letundra News

Получение новостей авиации и путешествий с letundra.com.

## Когда использовать

- "Новости авиации"
- "Что нового об Emirates?"
- "Новости о Таиланде"
- "Акции авиакомпаний"

## Workflow

1. **Определи URL**
   - Общие новости: `https://letundra.com/ru/news/`
   - По тегу: `https://letundra.com/ru/news/?taglist={tag}`

2. **Получи данные через web_fetch**
   ```
   {{web_fetch url="https://letundra.com/ru/news/"}}
   ```

3. **Извлеки новости** из HTML
   - Заголовки (h2, h3)
   - Даты
   - Ссылки
   - Теги

## Output format

```markdown
# 📰 Новости

## Заголовок
📅 Дата
🔗 [Читать](url)
```

## Failure handling

- Сайт недоступен: "Новости временно недоступны"
