# Data Flow

```
Plaid API → financial-sync → transactions.db (raw)
                                    ↓
                              Styx enrichment pipeline
                              (SearXNG + LLM + Google Places)
                                    ↓
                         styx.db (enriched merchants,
                                  transaction links)
                                    ↓
                    ┌───────────────┬───────────────┐
                    ↓               ↓               ↓
                 Taste          Rally           Vesper
              (restaurants)  (spending)     (briefings)
```