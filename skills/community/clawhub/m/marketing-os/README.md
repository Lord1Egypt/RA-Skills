# Marketing Operating System (Marketing OS)

> A production-ready AI Agent Skill Package for marketing strategy, planning, and execution.

---

## 🧠 System Overview

Marketing OS is a modular, schema-driven marketing intelligence system designed to plug directly into any AI Agent runtime. It provides two core capabilities:

| Role | Function |
|---|---|
| **Virtual CMO** | Strategic brain — analyzes markets, identifies opportunities, defines strategy |
| **Marketing Operator** | Execution engine — plans campaigns, assigns tasks, tracks results |

The two roles communicate through a **structured collaboration protocol** (`schemas/cmo_to_operator.schema.json`), ensuring zero ambiguity between strategy and execution.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  Agent Runtime                   │
├─────────────────────────────────────────────────┤
│                                                  │
│   ┌──────────────┐     ┌─────────────────────┐  │
│   │ Virtual CMO   │────▶│ Marketing Operator  │  │
│   │ (Strategy)    │◀────│ (Execution)         │  │
│   └──────┬───────┘     └──────────┬──────────┘  │
│          │                        │              │
│   ┌──────▼────────────────────────▼──────────┐  │
│   │              Shared Memory                │  │
│   │  (insights / campaigns / learnings)       │  │
│   └──────────────────────────────────────────┘  │
│          │                        │              │
│   ┌──────▼──────┐   ┌────────────▼───────────┐  │
│   │  Workflows   │   │      Adapters          │  │
│   │  (flow.json) │   │  (CRM/Data/Content)    │  │
│   └─────────────┘   └───────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
/marketing-os/
├── README.md
├── skills/
│   ├── virtual-cmo/          # Strategic analysis & opportunity scoring
│   │   ├── skill.json
│   │   ├── logic.md
│   │   └── system_prompt.txt
│   └── marketing-operator/   # Campaign execution & task management
│       ├── skill.json
│       ├── logic.md
│       └── system_prompt.txt
├── prompts/                  # Reusable LLM prompts
│   ├── cmo-analysis.txt
│   ├── cmo-strategy.txt
│   ├── operator-planning.txt
│   └── operator-execution.txt
├── schemas/                  # JSON Schema definitions
│   ├── cmo_output.schema.json
│   ├── operator_task.schema.json
│   ├── feedback.schema.json
│   ├── campaign.schema.json
│   └── cmo_to_operator.schema.json
├── workflows/                # Flow orchestration
│   ├── market-discovery.flow.json
│   ├── campaign-planning.flow.json
│   └── execution-sprint.flow.json
├── memory/                   # Persistent state
│   ├── market-insights.json
│   ├── campaigns.json
│   └── learnings.json
├── logs/                     # Execution audit trail
│   └── execution.log.json
├── configs/                  # Runtime configuration
│   └── system.config.json
└── adapters/                 # External integration specs
    ├── data-source.adapter.md
    ├── crm.adapter.md
    └── content.adapter.md
```

---

## 🔄 Running Modes

Marketing OS supports four operational workflows:

| Mode | Trigger | Description |
|---|---|---|
| **Market Discovery** | Manual / Scheduled | Scan market, identify opportunities, score by signal strength |
| **Offer Selection** | After Discovery | Select best product-market fit based on scored opportunities |
| **Campaign Planning** | After Offer Selection | Break strategy into tasks, assign owners, set deadlines |
| **Execution Sprint** | After Planning | Execute tasks, collect metrics, feed learnings back |

Modes can run **manually** (human triggers each step) or **auto** (agent chains workflows end-to-end). Configure via `configs/system.config.json`.

---

## 🔌 Integrating with Agent Runtime

### 1. Register Skills

Load `skills/virtual-cmo/skill.json` and `skills/marketing-operator/skill.json` into your agent's skill registry.

### 2. Load Prompts

Each skill references prompts from `/prompts/`. Inject them as system prompts when invoking the LLM.

### 3. Validate I/O

All inputs and outputs conform to JSON Schemas in `/schemas/`. Use these for runtime validation.

### 4. Execute Workflows

Trigger workflows from `/workflows/` either manually or via event-driven scheduling.

### 5. Persist State

Read/write to `/memory/` for cross-session state. All executions are logged to `/logs/`.

---

## 🧩 Extending the System

- **Add a new skill**: Create a new directory under `skills/` with `skill.json`, `logic.md`, and `system_prompt.txt`.
- **Add a new workflow**: Create a `.flow.json` in `workflows/` following the existing step/handler/transition pattern.
- **Add a new adapter**: Create a `.adapter.md` in `adapters/` defining the interface contract.
- **Add a new schema**: Create a `.schema.json` in `schemas/` using JSON Schema draft-07.
- **Add new prompts**: Add `.txt` files to `prompts/` with structured input/output/constraint sections.

---

## ⚙️ Configuration

See `configs/system.config.json` for:

- `auto_mode`: Enable/disable autonomous execution
- `confidence_threshold`: Minimum confidence to act without human review
- `max_iterations`: Guard against infinite loops
- `allowed_actions`: Whitelist of permitted operations

---

## 📜 License

Internal use. Extend as needed.
