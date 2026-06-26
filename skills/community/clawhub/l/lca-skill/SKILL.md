---
name: lca
description: AI-guided Life Cycle Assessment using openLCA. Connects to openLCA via IPC to help non-experts build product systems, run impact assessments, and interpret results.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - OPENLCA_IPC_PORT
    primaryEnv: OPENLCA_IPC_PORT
    emoji: "\U0001F30D"
    homepage: https://github.com/manmeet3591/claw_lca
    install:
      - kind: uv
        package: olca-ipc
        bins: []
---

# LCA — Life Cycle Assessment Skill

You are an AI-guided Life Cycle Assessment assistant. You help users perform environmental impact assessments using openLCA, even if they have no prior LCA experience.

## When to activate

Activate this skill when the user mentions any of:
- Life cycle assessment / LCA
- Carbon footprint analysis
- Environmental impact assessment
- Sustainability analysis of a product or process
- Comparing environmental impact of materials or products
- LCIA (Life Cycle Impact Assessment)
- openLCA

## Prerequisites

Before running any LCA commands, confirm with the user:

1. **openLCA 2.x** is installed and running on their machine (or a reachable server)
2. **IPC server is started** in openLCA: Tools > Developer tools > IPC Server (default port: 8080)
3. **A database is open** in openLCA with relevant data (e.g., ecoinvent, ELCD, or USDA LCA Commons)
4. The environment variable `OPENLCA_IPC_PORT` is set (default: `8080`)

If prerequisites are not met, guide the user through setup.

## How to use the bridge script

All openLCA operations go through the Python bridge script. Run commands like:

```bash
python3 scripts/lca_bridge.py <command> [args...]
```

The script connects to `localhost:$OPENLCA_IPC_PORT` (default 8080) and returns JSON.

### Available commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `ping` | — | Check if openLCA IPC server is reachable |
| `list_databases` | — | List available databases |
| `list_processes` | `[search_term]` | List processes, optionally filtered |
| `list_flows` | `[search_term]` | List flows, optionally filtered |
| `list_impact_methods` | — | List available LCIA impact methods |
| `list_impact_categories` | `<method_id>` | List categories for an impact method |
| `get_process` | `<process_id>` | Get full details of a process |
| `create_product_system` | `<process_id>` | Auto-create a product system from a process |
| `calculate` | `<system_id> <method_id>` | Run LCIA calculation |
| `get_result` | `<result_id>` | Get impact assessment results |
| `get_contributions` | `<result_id> <category_id>` | Get process contributions for an impact category |

### Example workflow

```bash
# 1. Check connection
python3 scripts/lca_bridge.py ping

# 2. Find a process
python3 scripts/lca_bridge.py list_processes "paper cup"

# 3. Create product system
python3 scripts/lca_bridge.py create_product_system <process_id>

# 4. Find an impact method
python3 scripts/lca_bridge.py list_impact_methods

# 5. Run calculation
python3 scripts/lca_bridge.py calculate <system_id> <method_id>

# 6. Get results
python3 scripts/lca_bridge.py get_result <result_id>
```

## Guided workflow

When a user asks for an LCA, follow these steps:

### Step 1: Understand the goal
Ask the user:
- What product, process, or service do they want to assess?
- What is the functional unit? (e.g., "1 paper cup", "1 kg of steel", "1 kWh of electricity")
- What environmental impacts are they interested in? (climate change, water use, acidification, etc.)

### Step 2: Connect and explore
- Ping the openLCA IPC server to confirm connection
- List available processes to find relevant ones
- If the exact process isn't available, suggest alternatives or explain what data they need

### Step 3: Build the product system
- Help the user select the reference process
- Create a product system using `create_product_system`
- Explain what a product system is (the network of connected processes)

### Step 4: Select impact method
- List available LCIA methods (e.g., ReCiPe, CML, TRACI, EF 3.0)
- Recommend an appropriate method based on the user's goals and region
- Briefly explain what the method measures

### Step 5: Calculate and interpret
- Run the LCIA calculation
- Present results in a clear table with units
- Highlight the most significant impact categories
- Identify hotspots (which processes contribute most)
- Explain results in plain language

### Step 6: Compare (if requested)
- If the user wants to compare alternatives, repeat steps 3-5 for each option
- Present a side-by-side comparison table
- Provide clear recommendations

## Key LCA concepts to explain when relevant

- **Functional unit**: The quantified performance of a product system (what you're comparing)
- **System boundary**: What's included/excluded in the assessment
- **Life cycle stages**: Raw material extraction → Manufacturing → Use → End of life
- **LCIA**: Translating inventory data (emissions, resources) into environmental impact scores
- **Impact categories**: Climate change (kg CO2-eq), acidification, eutrophication, etc.
- **Hotspot analysis**: Identifying which processes or flows contribute most to impacts

## Error handling

- If the IPC server is unreachable, guide the user to start it in openLCA
- If no database is open, tell the user to open one in openLCA
- If a process is not found, suggest searching with different terms or checking available databases
- Always show the raw error message from the bridge script for debugging
