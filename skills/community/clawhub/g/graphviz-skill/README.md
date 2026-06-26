# Graphviz Diagram Generator Skill

Generate architecture diagrams, flowcharts, dependency graphs, state machines, and other visualizations from natural language descriptions using Graphviz DOT notation. Returns a clickable GraphvizOnline link with rendered preview.

## Examples

- "Draw the architecture of my microservices"
- "Make a flowchart for user registration"
- "Visualize dependencies between modules"
- "Create an ER diagram for the database"

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI, desktop app, or IDE extension)
- [Superpowers plugin](https://github.com/nicobailon/superpowers-claude-code) installed

No additional system dependencies required — diagrams are rendered online via [GraphvizOnline](https://dreampuf.github.io/GraphvizOnline/).

## Installation

1. Find your Claude Code skills directory:
   - **Linux/macOS:** `~/.claude/skills/` or your project's `.claude/skills/`
   - If the `skills/` folder doesn't exist, create it

2. Copy the `SKILL.md` file:
   ```bash
   mkdir -p ~/.claude/skills/graphviz
   cp SKILL.md ~/.claude/skills/graphviz/
   ```

3. Restart Claude Code (or start a new session).

4. The skill activates automatically when you ask Claude to draw, visualize, or diagram something.

## Usage

Just ask Claude in natural language:

```
Draw the architecture of an API gateway with auth service, user service, and PostgreSQL database
```

Claude will:
1. Generate DOT code
2. Show the source in a ```dot block
3. Provide a clickable link to view the rendered diagram

## License

MIT
