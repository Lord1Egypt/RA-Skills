# Data Flow Diagram

```mermaid
flowchart TD
    A[User request: count same name] --> B[scripts/query.py]
    B --> C[load_data(): scripts/data.json]
    C --> D[normalize_gender / normalize_province]
    D --> E[query(name, gender, province)]
    E --> F[Keep records whose name + filters match]
    F --> G{Any match?}
    G -- yes --> H[Sum counts -> total; build by_gender / by_province]
    G -- no --> I[Set matched=false + explicit message]
    H --> J{format}
    I --> J
    J -- markdown --> K[render_markdown()]
    J -- text --> L[render_text()]
    J -- json --> M[render_json()]
    K --> N[stdout or --output file]
    L --> N
    M --> N
```

No network, CLI, SDK, or cloud resource is involved at any step.