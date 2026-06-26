# Wiki Structure

```
База знаний/
├── raw/                 # Sources — NEVER modify
├── wiki/
│   ├── entities/       # People, companies, projects
│   ├── concepts/       # Ideas, terms, methods
│   └── summaries/      # Topic summaries
├── index.md            # Catalog
├── log.md              # Chronology
└── AGENTS.md          # AI instructions
```

## Raw vs Wiki

- **raw/** — immutable sources (articles, books, notes)
- **wiki/** — AI-generated pages (my territory)

## Key Pages

| File | Purpose |
|------|---------|
| `index.md` | Catalog of all wiki pages |
| `log.md` | Operation log (ingest/query/lint) |
| `AGENTS.md` | Instructions for AI |
