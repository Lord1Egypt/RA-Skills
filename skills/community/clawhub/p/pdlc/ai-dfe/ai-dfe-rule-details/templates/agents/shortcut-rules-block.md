<!-- This block is appended into the destination workspace's.kiro/steering/workspace-rules.md
     between the AI-DFE markers below. Marker-fenced for clean ownership. -->

<!-- BEGIN AI-DFE AGENT SHORTCUTS -->
**`DHC__` shortcut triggers Data-Fabric Health Check.** When the user types `DHC__` (uppercase, double underscore) anywhere in a prompt, invoke the `data-fabric-health-check` agent (`.kiro/agents/data-fabric-health-check.md`) — a bootstrap readiness check that answers "can AI-DFE operate in this workspace?". It validates preconditions, discovery, operational readiness, and (if data exists) proves one gather→shape→distribute cycle, then produces a verdict (HEALTHY / DEGRADED / NOT READY / IDLE). Read-only (except `DHC__ fix`). Run it first when installing DFE. Modifiers: `DHC__ verbose`, `DHC__ fix`.

**`DFA__` shortcut triggers the Data-Fabric Integrity Agent.** When the user types `DFA__` (uppercase, double underscore) anywhere in a prompt, invoke the `data-fabric-agent` (`.kiro/agents/data-fabric-agent.md`) and run a read-only integrity pass over `{family}-ws/data/` — 18 checks across 5 categories (Schema Conformance, Registry Integrity, Manifest Consistency, Freshness, Territory & Lineage). Report-only — it never writes data; it names the `DAT__` operation that fixes each finding. Sub-commands: `DFA__` (full), `DFA__ schema`, `DFA__ registry`, `DFA__ manifest`, `DFA__ freshness`, `DFA__ territory`. Treat `DFA__` as a direct command to run the agent.

> **Note:** `DHC__` (readiness — *can* DFE run here?) and `DFA__` (integrity — *is* the data surface correct?) are both report-only agents. The data **operations** trigger is `DAT__` (gather/shape/distribute/discover/aggregate/cleanup/master), which produces and refreshes the data surface. `DAT__` changes things; `DHC__` and `DFA__` only look.
<!-- END AI-DFE AGENT SHORTCUTS -->
