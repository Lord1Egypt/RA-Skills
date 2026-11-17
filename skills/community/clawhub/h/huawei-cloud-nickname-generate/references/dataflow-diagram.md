# Data Flow Diagram

```mermaid
flowchart TD
    A[User request: generate a nickname] --> B[scripts/generate_nickname.py]
    B --> C[load_data(): scripts/nickname_data.json]
    C --> D[generate_nicknames count / seed / style / length]
    D --> E{style given on CLI?}
    E -- yes --> F[normalize style, source=cli]
    E -- no --> G[Pick a style at random]
    F --> H{length given on CLI?}
    G --> H
    H -- yes --> I[normalize length, source=cli]
    H -- no --> J[Pick a length bucket at random]
    I --> K[Choose a pattern for the bucket]
    J --> K
    K --> L[Per slot: morphemes matching the style]
    L --> M{Strict match for the slot?}
    M -- yes --> N[Draw one morpheme]
    M -- no --> O[Relax the slot; record fallback]
    O --> N
    N --> P[Concatenate slots -> nickname; de-duplicate the batch]
    P --> Q{format}
    Q -- markdown --> R[render_markdown]
    Q -- text --> S[render_text]
    Q -- json --> T[render_json]
    R --> U[stdout or --output file]
    S --> U
    T --> U
```

No network, CLI, SDK, or cloud resource is involved at any step.