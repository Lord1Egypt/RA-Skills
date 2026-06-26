---
name: letundra-rss
description: "Генерация RSS-лент для новостей letundra.com по тегам и странам."
metadata: {"openclaw":{"emoji":"📡","requires":{"bins":[]},"homepage":"https://letundra.com"}}
---

# Letundra RSS

Генерация RSS-подписок на новости letundra.com.

## Когда использовать

- "Создай RSS для Emirates"
- "Хочу подписаться на новости Таиланда"
- "RSS-лентаletundra"

## Workflow

1. **Получи новости**
   ```
   {{web_fetch url="https://letundra.com/ru/news/?taglist={tag}"}}
   ```

2. **Сгенерируй RSS XML** из полученных данных

## Output format

```xml
<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Letundra News - [тег]</title>
    <item>
      <title>Заголовок</title>
      <link>URL</link>
    </item>
  </channel>
</rss>
```
