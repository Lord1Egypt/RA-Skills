# MemPalace MCP Tools Reference

MemPalace expone 19 herramientas MCP organizadas en categorías.

## Read Tools (Lectura)

### mempalace_status
Palace overview — total drawers, wing and room counts.

**Input:** None

**Output:**
```json
{
  "total_drawers": 150,
  "wings": {"wing_user": 50, "wing_code": 100},
  "rooms": {"meetings": 30, "decisions": 20},
  "palace_path": "~/.mempalace/palace"
}
```

---

### mempalace_list_wings
List all wings with drawer counts.

**Input:** None

**Output:**
```json
{"wings": {"wing_user": 50, "wing_code": 100}}
```

---

### mempalace_list_rooms
List rooms within a wing (or all rooms if no wing given).

**Input:**
```json
{"wing": "wing_user"}  // optional
```

**Output:**
```json
{"wing": "wing_user", "rooms": {"diary": 10, "preferences": 40}}
```

---

### mempalace_get_taxonomy
Full taxonomy: wing → room → drawer count.

**Input:** None

**Output:**
```json
{"taxonomy": {"wing_user": {"diary": 10, "preferences": 40}}}
```

---

### mempalace_get_aaak_spec
Get the AAAK dialect specification — the compressed memory format MemPalace uses.

**Input:** None

---

### mempalace_search
Semantic search. Returns verbatim drawer content with similarity scores.

**Input:**
```json
{
  "query": "string",      // required
  "limit": 5,             // optional, default 5
  "wing": "wing_name",    // optional filter
  "room": "room_name"     // optional filter
}
```

---

### mempalace_check_duplicate
Check if content already exists in the palace before filing.

**Input:**
```json
{
  "content": "string",    // required
  "threshold": 0.9        // optional, default 0.9
}
```

---

### mempalace_kg_query
Query the knowledge graph for an entity's relationships.

**Input:**
```json
{
  "entity": "Max",                    // required
  "as_of": "2026-04-01",              // optional date filter
  "direction": "both"                 // both|incoming|outgoing
}
```

---

### mempalace_kg_timeline
Chronological timeline of facts.

**Input:**
```json
{"entity": "Max"}  // optional - omit for full timeline
```

---

### mempalace_kg_stats
Knowledge graph overview: entities, triples, relationship types.

**Input:** None

---

### mempalace_traverse
Walk the palace graph from a room. Shows connected ideas across wings.

**Input:**
```json
{
  "start_room": "chromadb-setup",  // required
  "max_hops": 2                    // optional, default 2
}
```

---

### mempalace_find_tunnels
Find rooms that bridge two wings — the hallways connecting domains.

**Input:**
```json
{
  "wing_a": "wing_code",   // optional
  "wing_b": "wing_user"    // optional
}
```

---

### mempalace_graph_stats
Palace graph overview: total rooms, tunnel connections, edges between wings.

**Input:** None

## Write Tools (Escritura)

### mempalace_add_drawer
File verbatim content into the palace. Checks for duplicates first.

**Input:**
```json
{
  "wing": "wing_name",           // required
  "room": "room_name",           // required
  "content": "verbatim text",    // required
  "source_file": "path.txt",     // optional
  "added_by": "mcp"              // optional, default "mcp"
}
```

---

### mempalace_delete_drawer
Delete a drawer by ID. Irreversible.

**Input:**
```json
{"drawer_id": "drawer_xxx"}  // required
```

---

### mempalace_kg_add
Add a fact to the knowledge graph.

**Input:**
```json
{
  "subject": "Max",
  "predicate": "loves",
  "object": "chess",
  "valid_from": "2026-01-01",     // optional
  "source_closet": "drawer_xxx"   // optional
}
```

---

### mempalace_kg_invalidate
Mark a fact as no longer true.

**Input:**
```json
{
  "subject": "Max",
  "predicate": "has",
  "object": "ankle_injury",
  "ended": "2026-03-01"  // optional, default today
}
```

---

### mempalace_diary_write
Write to your personal agent diary in AAAK format.

**Input:**
```json
{
  "agent_name": "Varg",           // required
  "entry": "SESSION:2026-04-04|...",  // required, AAAK format
  "topic": "general"              // optional
}
```

---

### mempalace_diary_read
Read your recent diary entries.

**Input:**
```json
{
  "agent_name": "Varg",   // required
  "last_n": 10            // optional, default 10
}
```

## AAAK Dialect

AAAK es un formato de memoria comprimida usado por MemPalace.

**Formato:**
- **ENTITIES:** Códigos de 3 letras mayúsculas. ALC=Alice, JOR=Jordan, etc.
- **EMOCIONES:** Marcadores *action* antes/durante texto. *warm*=joy, *fierce*=determined, *raw*=vulnerable
- **ESTRUCTURA:** Campos separados por pipes. FAM: family | PROJ: projects | ⚠: warnings
- **FECHAS:** Formato ISO (2026-03-31)
- **IMPORTANCIA:** ★ a ★★★★★ (escala 1-5)

**Ejemplo:**
```
FAM: ALC→♡JOR | 2D(kids): RIL(18,sports) MAX(11,chess+swimming) | BEN(contributor)
```
