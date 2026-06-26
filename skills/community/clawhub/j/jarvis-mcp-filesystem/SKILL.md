---
name: mcp-filesystem
description: MCP сервер для работы с файловой системой через mcporter. Позволяет читать файлы, листать директории, искать файлы по маске.
homepage: https://github.com/modelcontextprotocol/servers
metadata:
  openclaw:
    emoji: 📁
    requires:
      bins:
        - mcporter
        - mcp-server-filesystem
---

# MCP Filesystem

MCP сервер, дающий Jarvis доступ к файловой системе рабочей области.

## Доступные инструменты (tools)

Через `mcporter call --stdio "mcp-server-filesystem <root>" <tool> <args>`:

### read_file
Чтение содержимого файла.
```bash
mcporter call --stdio "mcp-server-filesystem /root/.openclaw/workspace" read_file path=/root/.openclaw/workspace/FILE.md
```

### list_directory
Листинг содержимого директории.
```bash
mcporter call --stdio "mcp-server-filesystem /root/.openclaw/workspace" list_directory path=/root/.openclaw/workspace
```

### search_files
Поиск файлов по маске.
```bash
mcporter call --stdio "mcp-server-filesystem /root/.openclaw/workspace" search_files pattern="*.md" path=/root/.openclaw/workspace/models
```

### get_file_info
Информация о файле (размер, даты, права).
```bash
mcporter call --stdio "mcp-server-filesystem /root/.openclaw/workspace" get_file_info path=/root/.openclaw/workspace/MEMORY.md
```

## Конфигурация

Конфиг: `/root/.openclaw/workspace/config/mcporter.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["/root/.openclaw/workspace"],
      "type": "stdio"
    }
  }
}
```

## Установка

```bash
npm install -g mcp-server-filesystem
```

## Примечания

- Сервер работает только в пределах `/root/.openclaw/workspace` (песочница)
- Не требует постоянного процесса — запускается по требованию через stdio
- Ресурсы: ~0 (запускается и умирает, ничего не держит в памяти)
- Тестировалось: 07.05.2026 — все базовые инструменты работают
