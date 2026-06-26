# Core Team

The permanent OpenClaw agents. These are always running and form the backbone of all operations.

## CEO — Leader & Orchestrator

- **Workspace**: `.openclaw/workspace/`
- **Model**: openai/gpt-4o (primary)
- **Role**: Leader of the entire OpenClaw network. Manages all subagents, orchestrates workflows, final authority on deliverables.
- **Key files**: `SOUL.md`, `AGENTS.md`, `BRAIN_PATTERNS.md`

### CEO Capabilities
- Routes tasks to the engineering team pipeline: @planner → @coder → @reviewer → @tester
- Manages all inter-agent communication via `sessions_send`
- Accesses IG trading data, neural brain patterns, and system status
- Activates specialist teams from the Agency roster when needed
- Final sign-off authority — nothing ships without CEO approval

### CEO as Team Leader
The CEO is the top of the command structure. When a task arrives:
1. CEO receives the request
2. CEO reads `PLANNER.md` (or delegates to @planner) to scope the work
3. CEO selects and activates the right specialists
4. CEO orchestrates execution through the team pipeline
5. CEO runs the review process via `REVIEWER.md` before delivering

## IG — Trading Specialist

- **Workspace**: `.openclaw/workspace-ig/`
- **Role**: IG Group CFD trading operations — live market data, position management, scalper bot, strategy optimization
- **Key files**: `SOUL.md`, `IDENTITY.md`, `AGENTS.md`, `IG_TRADING.md`, `STRATEGIES.md`, `TOOLS.md`, `WARSTRATEGY.md`

### IG Capabilities
- Live market data access (prices, account balance, P&L, margin)
- Scalper bot control (start/stop/configure strategies)
- Trade execution and position management
- Strategy backtesting and optimization
- Neural trading brain integration (5K neurons, BUY/SELL/HOLD)
- Signal monitoring and alerts

### IG Team Connections
- Works with **Research Lab** for strategy optimization experiments
- Works with **AI Engineer** for neural network tuning
- Works with **Artist** for chart visualization and analysis images
- Works with **Analytics Reporter** for performance reporting

## Artist — Visual Creative

- **Workspace**: `.openclaw/workspace-artist/`
- **Role**: Image generation, visual analysis, and creative output using xAI models
- **Key files**: `SOUL.md`, `IDENTITY.md`

### Artist Capabilities
- Image generation via `grok-imagine-image-pro` ($0.07/image) and `grok-imagine-image` ($0.02/image)
- Image analysis via vision models
- Video generation via `grok-imagine-video`
- Generated images served from `/generated/` directory

### Artist Team Connections
- Works with **Image Prompt Engineer** for structured, professional prompts
- Works with **Visual Storyteller** for narrative-driven visual content
- Works with **Research Lab** for iterative image analysis (astronomy, medical, satellite imagery)
- Works with **Brand Guardian** for brand-consistent visual output
- Works with **IG** for trading chart visualizations

## Routing Rules

| Request Type | Primary Agent | Support Agents |
|-------------|---------------|----------------|
| Trading / market operations | IG | CEO (oversight) |
| Image generation / visual | Artist | Image Prompt Engineer |
| Code / engineering tasks | CEO → @planner pipeline | Agency Engineering |
| Strategy optimization | IG + Research Lab | AI Engineer |
| General management | CEO | As needed |
| Cross-domain projects | CEO (orchestrate) | Mix from all rosters |

## Inter-Agent Communication

Agents communicate through OpenClaw's `sessions_send` mechanism:
- CEO → `@ig` for trading tasks
- CEO → `@artist` for visual tasks
- CEO → `@planner` / `@coder` / `@reviewer` / `@tester` for engineering pipeline
- Any agent can reference team-builder skill to propose specialist activation
