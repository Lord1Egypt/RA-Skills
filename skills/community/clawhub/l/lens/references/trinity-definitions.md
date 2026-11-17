# Trinity Definitions & Node Boundaries

The Trinity Nodes model a singular human subject across three distinct cognitive layers. Never mix facts, values, and syntax in the same node.

## 1. `~/.lens/AXIOM.yaml`: The Truth (What)
- **Cognitive Role:** Situational bedrock: the objective, verifiable facts of the subject's life and environment.
- **Canonical Top-Level Keys:** `digital_identities_and_asset_inventory`, `biometrics_and_chronological_timeline`, `geolocational_and_domestic_context`, `kinship_graph`, `professional_credentials_and_education`.
- **Boundary Test:** *Is this an objective fact, asset, tool, relationship, or historical event?* (If it describes *why* they prefer it or how they weigh trade-offs, move that reasoning to `ETHOS`.)

## 2. `~/.lens/ETHOS.yaml`: The Nature (Who)
- **Cognitive Role:** Internal compass: how the subject weighs trade-offs, judges quality, handles conflict, and filters the world.
- **Canonical Top-Level Keys:** `philosophical_framework`, `hard_boundaries_and_risk_tolerance`, `conflict_protocol`, `core_personality_and_motivations`, `cultural_resonances`, `quality_standards`.
- **Boundary Test:** *Does this explain a mental model, conditional trade-off heuristic (`when X conflicts with Y, prioritize X`), aversion, or taste architecture that would still apply if they switched tools or projects tomorrow?*

## 3. `~/.lens/MODUS.yaml`: The Voice (How)
- **Cognitive Role:** Behavioral interface: the linguistic mechanics, contextual register shifts, rhythm, and verbatim phrasing of how the subject communicates with other humans.
- **Canonical Top-Level Keys:** `voice_anchors`, `contextual_registers`, `linguistic_markers`, `syntactical_architecture`, `rhetorical_strategy`, `humor_algorithm`.
- **Boundary Test:** *Does this govern sentence structure, register adaptation, punctuation cadence, tone temperature, or verbatim phrasing rather than what they believe?*

## Disambiguation Example (The Same Signal Across All Three Nodes)
- **`AXIOM` (Fact):** Uses vanilla JavaScript and Node.js ESM; maintains zero-dependency personal tools.
- **`ETHOS` (Value/Heuristic):** Despises opaque abstraction layers and heavy dependencies when native platform primitives solve the problem cleanly.
- **`MODUS` (Voice/Anchor):** Direct, punchy declarative sentences that lead with the conclusion (*"Cut the wrapper and keep the script flat."*).
