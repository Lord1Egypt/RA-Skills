---
name: mcp-html-extractor
description: MCP сервер для HTML-извлечения и веб-скрапинга через mcporter.
homepage: https://npm.im/html-extractor-mcp
metadata:
  openclaw:
    emoji: 🌐
    requires:
      bins:
        - mcporter
        - html-extractor-mcp
---

# MCP HTML Extractor

MCP сервер для веб-скрапинга. Извлекает текст, ссылки, вызывает JSON API.

## Установка

```bash
npm install -g html-extractor-mcp
```

## Использование

```bash
mcporter call --stdio "html-extractor-mcp" fetch url="https://example.com"
mcporter call --stdio "html-extractor-mcp" extract_text url="https://example.com"
```

## Примечания

- Установлен: 07.05.2026
- Тестирование: требует уточнения имён инструментов
- Ресурсы: минимальные (запуск по требованию через stdio)
