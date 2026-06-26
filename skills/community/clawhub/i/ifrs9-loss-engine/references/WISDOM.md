# Cross-Project Wisdom

Total: **10**

## `CW-REGTECH-001` — Input bounds validation before statistical computation
**From**: finance-bp-062--ifrs9, finance-bp-067--firesale_stresstest · **Applicable to**: regtech-compliance

Statistical functions like norm.ppf() and cumprod() have strict input requirements that, if violated, produce infinite or NaN values corrupting entire pipelines. Always validate inputs against domain constraints (DDP in (0,1), counts > 0) before passing to statistical functions. Apply to any statistical or inverse-CDF computation.

## `CW-REGTECH-002` — Graph/topology invariant verification before construction
**From**: finance-bp-060--AMLSim, finance-bp-067--firesale_stresstest · **Applicable to**: regtech-compliance

Before constructing graph structures (transaction networks, transition matrices), verify invariants: sum(in-degrees) = sum(out-degrees), matrix row sums = 1.0, degree sequence length divisibility. This catches data corruption early before expensive graph construction operations. Apply to any bipartite or directed graph generation.

## `CW-REGTECH-003` — Regulatory amortization window discipline
**From**: finance-bp-062--ifrs9 · **Applicable to**: regtech-compliance

IFRS 9 mandates different ECL calculation windows: exactly 12-month for Stage 1 (11 zero-indexed iterations), full remaining tenor for Stage 2/3. Mixing these up violates compliance requirements. Always encode stage-specific window logic explicitly rather than reusing a single loop variable across stages.

## `CW-REGTECH-004` — Fingerprint composition must include all request dimensions
**From**: finance-bp-071--opensanctions · **Applicable to**: regtech-compliance

Cache keys must include all request parameters that affect response content: URL, HTTP method, authentication headers, and request body for state-changing methods. POST requests with different bodies returning identical cache is a silent data corruption bug. Always compose fingerprints from the union of all content-affecting parameters.

## `CW-REGTECH-005` — Floating-point zero-equivalence with explicit epsilon tolerance
**From**: finance-bp-067--firesale_stresstest · **Applicable to**: regtech-compliance

IEEE 754 floating-point precision causes exact zero comparisons to fail in financial calculations. Always use eps=1e-9 tolerance for zero-equivalence checks in market clearing, leverage ratios, and price impact calculations. This prevents division-by-zero crashes and incorrect cash transfers.

## `CW-REGTECH-006` — Stage classification threshold ordering enforcement
**From**: finance-bp-062--ifrs9 · **Applicable to**: regtech-compliance

IFRS 9 SICR thresholds must be ordered: BUCKETS 2-3 trigger Stage 2, BUCKETS >=4 trigger Stage 3. Applying thresholds in wrong order or omitting absolute DPD triggers causes material ECL misstatement. Validate threshold ordering and document bucket-to-stage mapping explicitly.

## `CW-REGTECH-007` — Initialization-before-use dependency ordering
**From**: finance-bp-067--firesale_stresstest · **Applicable to**: regtech-compliance

Operational dependencies must initialize before dependent objects use them: AssetMarket before bank registration, CSV file existence before parsing, entity ID before statement addition. Violations cause AttributeError or FileNotFoundError that abort entire initialization. Always encode dependency ordering explicitly in initialization sequences.

## `CW-REGTECH-008` — Sufficient entity ID collision prevention
**From**: finance-bp-071--opensanctions · **Applicable to**: regtech-compliance

Entity IDs must include enough identifying attributes (dataset prefix, source, identifier type, document number) to guarantee uniqueness. Collisions create false equivalence between unrelated entities, directly causing false positive sanctions matches. Include the maximum available discriminating attributes in ID construction.

## `CW-REGTECH-009` — Hub selection with candidate removal before addition
**From**: finance-bp-060--AMLSim · **Applicable to**: regtech-compliance

When selecting hub accounts for typology placement, always call remove_typology_candidate BEFORE add_node for each selected account. Reversing this order causes hub self-selection (accounts choosing themselves) and duplicate assignment across overlapping patterns. Apply to any allocation algorithm with candidate pooling.

## `CW-REGTECH-010` — Insolvency detection before operational decisions
**From**: finance-bp-067--firesale_stresstest · **Applicable to**: regtech-compliance

Banks below the insolvency threshold (3% leverage) must trigger default immediately, not enter the deleveraging decision logic. Checking operational thresholds before insolvency creates zombie banks with negative equity. Always gate operational decisions on prior insolvency state.
