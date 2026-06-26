---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3045022066d1c8bfb75f743442c5774712cffa5fcc893f09fbe132e49c69e19e89e257af022100cedbba38770e26d45d83097e6529f3c8187dfb83e8abf98c5e2d1acd64f080a3
    ReservedCode2: 3045022100f0764b0cdae0988d78a2fcbe3b975a648aed404694a2c61a4c0972b31d003d1702204db597213d812879bc2cb425ca04a780d53d08a1dd5b6b043060a657fef567e2
---

# Report Templates (v3.2 - Visual-Enhanced)

This version optimizes Mermaid visualizations for professional pharmaceutical intelligence reports. All templates follow the **EUREKA_REPORT** protocol.

## Core Visual Standards
- **Color Strategy**: Professional palette with better contrast
- **Design Logic**: `graph LR` (Left-to-Right) for R&D funnel simulation
- **Simplicity**: Avoid complex subgraph nesting for compatibility

---

## 1. Pipeline Arena Map (Universal Template)

The primary visualization for competitive landscape analysis.

```mermaid
graph LR
    Target{Target/<br/>Target Name}:::target

    A1["Approved/<br/>Company A - Drug A"]:::approved
    A2["Approved/<br/>Company B - Drug B"]:::approved

    P3["Phase 3/<br/>Company C - Drug C"]:::p3

    P2["Phase 2/<br/>Company D - Drug D"]:::p2

    P1["Phase 1/<br/>Company E - Drug E"]:::p1

    PC["Preclinical/<br/>Company F - Drug F"]:::pre

    Target --> A1
    Target --> A2
    Target --> P3
    Target --> P2
    Target --> P1
    Target --> PC

    classDef target fill:#1a1a1b,color:#fff,stroke:#000
    classDef approved fill:#d4edda,stroke:#28a745,color:#155724
    classDef p3 fill:#cce5ff,stroke:#007bff,color:#004085
    classDef p2 fill:#fff3cd,stroke:#ffc107,color:#856404
    classDef p1 fill:#e2d5f3,stroke:#8b5cf6,color:#5b21b6
    classDef pre fill:#f8f9fa,stroke:#6c757d,color:#495057,stroke-dasharray:5 5
```

---

## 2. Mechanism Action Chain (Universal Template)

Used for biological rationale and Target-to-Disease mapping.

```mermaid
graph LR
    A[Upstream/<br/>Pathological Driver] --> B{Target/<br/>Target Name}
    B --> C[Downstream/<br/>Cellular Process]
    C --> D[Therapeutic Effect/<br/>Disease Modification]

    classDef trigger fill:#f0f0f0,stroke:#666,stroke-width:2px
    classDef target fill:#fff3e0,stroke:#ff9800,color:#e65100,stroke-width:3px
    classDef process fill:#fff3e0,stroke:#ff9800,color:#e65100,stroke-width:2px
    classDef effect fill:#d4edda,stroke:#28a745,color:#155724,stroke-width:2px

    class A trigger
    class B target
    class C process
    class D effect
```

---

## 3. Competitive Landscape (Cross-Mechanism)

Used for Indication-level reports to compare different drug classes.

```mermaid
graph TD
    Unmet{Unmet Needs/<br/>Indication}:::core

    N1[Resistance/<br/>Refractory]:::gap
    N2[Safety/<br/>Toxicity]:::gap

    O1[Novel MoA/<br/>Next-Gen]:::opp
    O2[Combo Therapy/<br/>Biomarker]:::opp

    Unmet --> N1
    Unmet --> N2
    N1 --> O1
    N1 --> O2
    N2 --> O1
    N2 --> O2

    classDef core fill:#007bff,color:#fff,stroke:#0056b3
    classDef gap fill:#f8d7da,stroke:#dc3545,color:#721c24
    classDef opp fill:#d4edda,stroke:#28a745,color:#155724
```

---

## 4. Patent Modality Distribution (Universal Template)

```mermaid
pie showData title Patent Modality Distribution (2019-2024)
    "Small Molecule" : 45
    "Antibody" : 25
    "ADC" : 15
    "PROTAC" : 10
    "Other" : 5
```

---

## 5. Clinical Development Timeline (Universal Template)

```mermaid
timeline
    title Clinical Development Timeline
    2024-Q1 : Phase 1 : Drug A
    2024-Q3 : Phase 2 : Drug B
    2025-Q2 : Phase 3 : Drug C
    2026-Q1 : NDA : Drug A
```

---

## 6. Patent Filing Trend (Year-over-Year)

```mermaid
xychart-beta
    title Patent Filings Trend
    x-axis [2019, 2020, 2021, 2022, 2023, 2024]
    y-axis "Filings" 0 --> 60
    bar [15, 22, 35, 48, 52, 45]
```

---

## 7. Evidence Hierarchy Reference

| Evidence Level | Definition | Citation Format |
|---------------|------------|-----------------|
| **Level A** | Verified Fact | `<refer e_id="..." e_type="patent" />` |
| **Level B** | Inference | `<refer e_id="..." e_type="inference" />` |
| **Level C** | Open Gap | No citation needed |

---

## Template Metadata
- **Producer**: PatSnap LS Product Team
- **Protocol**: EUREKA_REPORT v3.2
