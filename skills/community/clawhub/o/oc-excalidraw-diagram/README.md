# excalidraw-diagram

> An OpenClaw skill that generates Excalidraw hand-drawn diagrams from natural language descriptions.

## Features

- 🎨 Generates `.excalidraw` JSON files ready to open in [excalidraw.com](https://excalidraw.com) or the desktop app
- 📊 Supports 9 diagram types: flowchart, architecture, mind map, ER diagram, sequence diagram, swimlane, class diagram, relationship diagram, data flow diagram
- 🤖 Natural language input — just describe what you want
- 🖼️ Optional PNG export via Playwright headless browser

## Installation

**Option A — Manual:**
```bash
cp -r excalidraw-diagram ~/.openclaw/workspace/skills/
```

**Option B — ClaWHub (after publish):**
```bash
npx clawhub@latest install excalidraw-diagram
```

## Usage

Just describe the diagram in natural language:

> "Draw a flowchart for user login: start → enter credentials → validate → success/failure"

> "Create an architecture diagram for a microservices system with API gateway, auth service, and database"

> "Make a mind map for project management topics"

The skill will generate a `.excalidraw` file saved to your current working directory (or a path you specify).

## Export to PNG

See [`references/headless-export.md`](references/headless-export.md) for a validated Playwright script to export diagrams as PNG images.

**Prerequisites:**
```bash
pip install playwright
playwright install chromium
```

## Diagram Types

| Type | Trigger Keywords |
|------|-----------------|
| Flowchart | 流程图, flowchart, flow |
| Architecture | 架构图, architecture, system design |
| Mind Map | 思维导图, mind map, brainstorm |
| ER Diagram | ER图, entity relationship, database schema |
| Sequence Diagram | 时序图, sequence, interaction |
| Swimlane | 泳道图, swimlane, cross-functional |
| Class Diagram | 类图, class diagram, UML |
| Relationship | 关系图, relationship, network |
| Data Flow | 数据流图, DFD, data flow |

## File Structure

```
excalidraw-diagram/
├── SKILL.md                          # Main skill instructions
├── README.md                         # This file
└── references/
    ├── element-spec.md               # Excalidraw element JSON spec
    ├── diagram-templates.md          # Layout templates per diagram type
    ├── examples.md                   # Complete prompt+output examples
    └── headless-export.md            # PNG export via Playwright
```

## License

MIT — WanSan Team (OpenClaw)
