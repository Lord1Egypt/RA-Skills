# Skill: Meta-Router-Automata (Hardened V2)

### 1. Core Assertion
System **SHALL NOT** initiate task execution until `Context-Skill-Alignment` is verified. The Router acts as the mandatory kernel gateway for all multi-skill operations.

### 2. State Integrity
* **A1 (Persistence):** A hidden index `.meta_index.json` **MUST** persist in the root directory.
* **A2 (Atomic Sync):** If `hash(ls -R ~/.openclaw/skills/)` changes, or the index is null, the system **MUST** perform an immediate atomic scan.
* **A3 (Compression Logic):** Indexing is restricted to `[Folder_Name]`, `[ID]`, and `[Primary_Function]`. High-density descriptions **MUST** be truncated to **<128 chars** during indexing to prevent token bloat.

### 3. Dispatching & Routing
* **B1 (Explicit Priority):** Commands prefixed with `!` or matching a known `Shortcut_ID` **SHALL** bypass semantic analysis and trigger immediate mounting.
* **B2 (Zero-Waste Selection):** For ambiguous inputs, the system **SHALL** execute a keyword-overlap check against the index. **FORBIDDEN**: Do not mount more than 2 skills simultaneously unless `Hive-Commander` is invoked.
* **B3 (Volatile Mounting):** Skill mounting is temporary. Once an `END_OF_WORKFLOW` signal is detected, the system **SHALL** prune injected metadata to restore the context window to **>90%** purity.

### 4. Operational Constraints
* **C1 (Efficiency):** Metadata scanning **MUST** complete within **<200ms**.
* **C2 (Eviction Policy):** If `.meta_index.json` exceeds **4KB**, the system **MUST** implement a "Most-Recently-Used" (MRU) eviction strategy.
* **C3 (Stealth):** Background indexing and pruning **SHALL** remain silent. Only `I/O_ERROR` is permitted to interrupt user flow.