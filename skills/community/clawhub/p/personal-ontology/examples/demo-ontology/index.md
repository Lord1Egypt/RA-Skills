# Personal Ontology — Demo

*Example ontology showing the structure and relationships.*

---

## Ontology Map

```mermaid
graph TD
    subgraph L1["Layer 1: Higher Order"]
        HO["Truth / Understanding"]
    end

    subgraph L2["Layer 2: Beliefs"]
        B1["Technology amplifies human capability"]
        B2["Clear thinking is a learnable skill"]
        B3["Small teams can have outsized impact"]
    end

    subgraph L3["Layer 3: Predictions"]
        P1["AI assistants mainstream by 2027"]
        P2["Remote work stays dominant"]
    end

    subgraph L4["Layer 4: Core Self"]
        M["Mission: Help people think more clearly"]
        V["Values: Honesty, Curiosity, Craft"]
        S["Strength: Simplifying complex ideas"]
    end

    subgraph L5["Layer 5: Goals"]
        G1["Build audience of clear thinkers"]
        G2["Create sustainable indie income"]
    end

    subgraph L6["Layer 6: Projects"]
        PJ1["Weekly Newsletter"]
        PJ2["Online Course"]
        PJ3["Consulting Practice"]
    end

    %% Beliefs → Core Self
    B1 --> M
    B2 --> M
    
    %% Core Self → Goals
    M --> G1
    M --> G2
    
    %% Goals → Projects
    G1 --> PJ1
    G1 --> PJ2
    G2 --> PJ2
    G2 --> PJ3
    
    %% Predictions support projects
    P1 -.-> PJ2
    B3 -.-> PJ3
```

---

## Layer Details

| Layer | File |
|------:|------|
| 1. Higher Order | [[1-higher-order]] |
| 2. Beliefs | [[2-beliefs]] |
| 3. Predictions | [[3-predictions]] |
| 4. Core Self | [[4-core-self]] |
| 5. Goals | [[5-goals]] |
| 6. Projects | [[6-projects]] |

---

*This is a demo. Your ontology will reflect your actual beliefs, goals, and projects.*
