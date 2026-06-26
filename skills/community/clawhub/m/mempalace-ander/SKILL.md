---
name: mempalace
description: Integración con MemPalace para gestión de memoria semántica persistente. Use when you need to search, add, or query memories stored in a MemPalace palace. Supports semantic search, knowledge graph queries, and memory management via ChromaDB-based storage.
---

# MemPalace Skill

Este skill proporciona acceso a MemPalace, un sistema de memoria semántica persistente basado en ChromaDB.

## Ubicación del Palacio

Por defecto: `~/.mempalace/palace`

## Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `scripts/search.py` | Búsqueda semántica en el palacio |
| `scripts/add_memory.py` | Añadir nueva memoria al palacio |
| `scripts/status.py` | Estado del palacio (drawers, wings, rooms) |
| `scripts/kg_query.py` | Consultar el knowledge graph |

## Uso

### Búsqueda Semántica
```bash
python3 scripts/search.py "query de búsqueda" [--limit 5] [--wing wing_name] [--room room_name]
```

### Añadir Memoria
```bash
python3 scripts/add_memory.py --wing wing_name --room room_name --content "contenido a guardar" [--source-file archivo.txt]
```

### Estado del Palacio
```bash
python3 scripts/status.py
```

### Consultar Knowledge Graph
```bash
python3 scripts/kg_query.py --entity "nombre_entidad" [--direction both|incoming|outgoing]
```

## Referencias

Para documentación completa de las herramientas MCP disponibles, ver `references/mcp_tools.md`.
