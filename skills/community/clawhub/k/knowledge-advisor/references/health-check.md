# Health Check Reference

Self-monitoring thresholds, metrics, and scaling recommendations for the knowledge-advisor skill.

## Metrics

| Metric | Field in `_health.json` | How to Calculate |
|--------|------------------------|------------------|
| Book count | `book_count` | Count directories in `knowledge-base/` excluding `_`-prefixed files |
| Total frameworks | `total_frameworks` | Sum of `framework_count` from all `meta.json` files |
| Total principles | `total_principles` | Sum of `principle_count` from all `meta.json` files |
| Index token estimate | `index_estimated_tokens` | Word count of `_index.md` * 1.3 |
| Avg book tokens | `avg_book_tokens` | Total word count of all book files * 1.3 / book_count |
| Largest book tokens | `largest_book_tokens` | Word count of largest book directory * 1.3 |
| Domain count | `domains` | Count unique domains across all `meta.json` files |
| Languages | `languages` | Unique `language` values across all `meta.json` files |
| Scaling phase | `scaling_phase` | Current phase: V1, V1.5, V2, or V3 |

## Warning Thresholds

### Book Count
- **25 books**: INFO — "Approaching V1 limit. Your KB is healthy, but plan for V1.5 soon."
- **30 books**: WARNING — "Reached V1 recommended max. Upgrade to V1.5 (domain sub-indexes) before adding more books. This is a non-breaking restructure — no re-ingestion needed."
- **50 books**: WARNING — "Reached V1.5 limit. Upgrade to V2 (SQLite search layer) for better performance."

### Index Size
- **2,500 tokens**: INFO — "Master index is growing. Domain sub-indexes would keep queries faster."
- **3,000 tokens**: WARNING — "Master index is heavy. Strongly recommend splitting into domain sub-indexes."

### Single Book Size
- **6,000 tokens**: INFO — "Book '[name]' has a large extraction. Consider whether all items are essential."
- **8,000 tokens**: WARNING — "Book '[name]' exceeds recommended size. Consider condensing to key frameworks and principles only."

### Query Load
- If a single advisory query requires reading more than 5 book directories:
  - INFO — "This query loaded [N] book directories. Consider using domain filtering for faster results."

## Scaling Phase Recommendations

### When to recommend V1.5
Trigger: book_count >= 30 OR index_estimated_tokens > 2,500

Recommendation message:
```
📋 SCALING RECOMMENDATION: Upgrade to V1.5

Your knowledge base has grown past the V1 sweet spot. I recommend
splitting your master index into domain-specific sub-indexes:

  _index.md → _index-leadership.md, _index-strategy.md, etc.

Benefits:
• Domain queries load ~400 tokens instead of ~2,100+
• Cross-domain queries load only 2-3 sub-indexes
• No re-ingestion needed — same book files, better indexing

Would you like me to perform this restructure now?
```

### When to recommend V2
Trigger: book_count >= 50

Recommendation message:
```
📋 SCALING RECOMMENDATION: Upgrade to V2

With 50+ books, file-based search becomes slow. I recommend adding
a SQLite search layer:

• SQLite handles search and filtering (fast)
• Your markdown files stay as source of truth (human-readable)
• scripts/build-db.sh regenerates SQLite from files anytime

This requires the sqlite3 command-line tool.
```

### When to recommend V3
Trigger: book_count >= 200

Recommendation message:
```
📋 SCALING RECOMMENDATION: Upgrade to V3

With 200+ books, keyword matching may miss relevant frameworks.
Consider adding vector embeddings for semantic search.
```

## Health Report Format

```
📊 Knowledge Base Health Report

📈 Status: [HEALTHY | APPROACHING LIMIT | OVER LIMIT]
├── Books: [N] / [phase max] ([phase name])
├── Frameworks: [N] | Principles: [N]
├── Domains: [N]
├── Index size: ~[N] tokens (limit: [threshold])
├── Avg. query cost: ~[N] tokens
├── Languages: [list]
└── Scaling phase: [V1 | V1.5 | V2 | V3]

[Any warnings]
[Any scaling recommendations]
```

## Post-Ingestion Health Summary

After every ingestion, append a brief health line:

```
📊 KB Health: [N] books | Index: ~[N] tokens | Status: [status]
```

If any warning threshold is exceeded, show the full warning message instead of the brief line.
