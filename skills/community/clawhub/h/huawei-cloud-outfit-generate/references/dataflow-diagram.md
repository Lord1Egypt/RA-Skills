# Data Flow Diagram

```mermaid
flowchart TD
    A[User request: generate an outfit] --> B[scripts/generate_outfit.py]
    B --> C[load_wardrobe(): scripts/wardrobe.json]
    C --> D[pick_outfit(seed, style, season)]
    D --> E{style / season given on CLI?}
    E -- yes --> F[normalize style and season, mark source=cli]
    E -- no --> G[Choose style and season at random]
    F --> H[Per category: items matching style AND season]
    G --> H
    H --> I{Strict match found?}
    I -- yes --> J[Draw one item from the matched pool]
    I -- no --> K[Relax season, then style; record fallback]
    K --> J
    J --> L[Assemble outfit: top / bottom / footwear / accessory]
    L --> M{format}
    M -- markdown --> N[render_markdown()]
    M -- text --> O[render_text()]
    M -- json --> P[render_json()]
    N --> Q[stdout or --output file]
    O --> Q
    P --> Q
```

No network, CLI, SDK, or cloud resource is involved at any step.