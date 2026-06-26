# Anti-Patterns (Cross-Project)

Total: **15**

## finance-bp-060--AMLSim (1)

### `AP-REGTECH-011` — Mismatched configuration parameters across coupled components <sub>(medium)</sub>

When TransactionGenerator and Nominator use different degree_threshold values, Nominator identifies hub accounts using different criteria than TransactionGenerator. This causes incorrect fan-in/fan-out candidate selection. Consequence: AML typology patterns placed on wrong accounts, invalidating simulation results.

## finance-bp-060--AMLSim, finance-bp-067--firesale_stresstest (1)

### `AP-REGTECH-002` — Self-loops in transaction graphs violate domain rules <sub>(high)</sub>

When generating directed transaction graphs or AML typologies, allowing source == destination edges creates self-loops. In AML simulation, self-loops represent accounts sending money to themselves, which is not a valid money laundering pattern. In fire-sale models, self-loops cause undefined behavior. Consequence: corrupted graph topology and invalid typology validation.

## finance-bp-060--AMLSim, finance-bp-071--opensanctions (1)

### `AP-REGTECH-001` — Missing attribute initialization on data structures <sub>(high)</sub>

When loading account lists or creating entity dictionaries, failing to initialize required list/dict attributes (e.g., normal_models, statement IDs) causes KeyError or ValueError at runtime. The code path that reads these structures assumes they exist, but the initialization path omits them. Consequence: pipeline crashes or data loss for affected entities.

## finance-bp-062--ifrs9 (3)

### `AP-REGTECH-005` — Incorrect amortization windows violate IFRS 9 compliance <sub>(high)</sub>

Stage 1 ECL requires exactly 12-month amortization (11 zero-indexed iterations) while Stage 2/3 requires full remaining tenor (tenor-1 iterations). Using identical windows for all stages causes ECL over/understatement. Consequence: regulatory non-compliance and materially incorrect loan loss provisions.

### `AP-REGTECH-010` — Incorrect cumulative PD ordering corrupts lifetime ECL term structure <sub>(high)</sub>

Using cumprod(1-conPD) without shift(1) and fillna(1) produces corrupted first-period survival probability. This cascades into all subsequent marginal and cumulative PD calculations, violating IFRS 9 lifetime ECL requirements. Consequence: systematically incorrect provisions across all remaining tenor periods.

### `AP-REGTECH-015` — Missing EAD component in ECL formula produces incomplete provisions <sub>(high)</sub>

IFRS 9 requires ECL = PD x LGD x EAD. When the EAD module is missing or not integrated, the ECL calculation is incomplete and unusable for provisioning. Consequence: regulatory rejection of ECL calculations, blocking of provisioning and reporting processes.

## finance-bp-062--ifrs9, finance-bp-067--firesale_stresstest (2)

### `AP-REGTECH-003` — Unvalidated floating-point inputs cause runtime crashes <sub>(high)</sub>

When parsing CSV files or computing statistical functions on raw data, failing to validate inputs against acceptable ranges (e.g., DDP near 0 or 1 for norm.ppf, unvalidated floats from CSV) causes ValueError or infinite/NaN values. Consequence: entire model crashes before simulation or corrupted downstream calculations.

### `AP-REGTECH-004` — Division by zero in financial calculations produces inf/NaN <sub>(high)</sub>

When calculating ratios like DDP (downgrade observations / total observations) or price impact denominators (total_quantities), zero-denominator cases are not guarded. The resulting inf/NaN propagates through all downstream calculations, corrupting CCI, ECL, or market clearing. Consequence: systematic data corruption across the entire calculation pipeline.

## finance-bp-067--firesale_stresstest (4)

### `AP-REGTECH-006` — Wrong leverage formula in threshold-based decisions <sub>(high)</sub>

Computing leverage as equity-to-liabilities (E/L) instead of equity-to-assets (E/A) produces different values. This causes deleveraging triggers and insolvency detection to fire at wrong thresholds. Consequence: zombie banks continue operating with negative equity, or healthy banks unnecessarily deleverage.

### `AP-REGTECH-007` — Confusing deleveraging buffer threshold with insolvency threshold <sub>(high)</sub>

Banks below 3% leverage are insolvent and must default, but deleveraging should trigger at 4% buffer. Using the same threshold eliminates the buffer zone, causing immediate default with no intermediate corrective action. Consequence: excessive bank failures amplify systemic contagion.

### `AP-REGTECH-013` — Order-dependent execution creates first-mover advantage bias <sub>(medium)</sub>

Without separating step() and act() phases, first-acting banks sell assets before others decide, creating systematic first-mover advantage. This distorts the competitive equilibrium and fire-sale dynamics. Consequence: unreliable systemic risk estimates that understate contagion for late-acting banks.

### `AP-REGTECH-014` — Immediate asset sales cause double-selling and undefined state <sub>(medium)</sub>

Executing asset sales immediately rather than queuing them to a buffer allows multiple banks holding the same asset to sell simultaneously without accounting for concurrent intentions. Consequence: undefined price impact and incorrect cash transfers in market clearing.

## finance-bp-071--opensanctions (3)

### `AP-REGTECH-008` — Cache keys omit request body for state-changing methods <sub>(high)</sub>

Using only URL for cache fingerprints on POST/PATCH requests means different request bodies return identical cached content. This causes stale data, missing entities, and data corruption in compliance screening pipelines. Consequence: sanctions matches missed or false positives from stale entity data.

### `AP-REGTECH-009` — ID collision in entity construction creates false sanctions matches <sub>(high)</sub>

When constructing entity IDs from source identifiers, insufficient identifying attributes cause different real-world entities to receive identical IDs. The database then merges them into one entity. Consequence: a sanctioned entity's ID matches an innocent entity, causing false positive compliance alerts.

### `AP-REGTECH-012` — Reverse property assignment corrupts entity construction <sub>(medium)</sub>

Stub (reverse) properties represent inverse relationships and raise InvalidData when directly assigned. Attempting to add values to stub properties instead of forward properties causes ValueError, aborting entity construction. Consequence: entities lost from output, incomplete compliance datasets.
