# Painpoint Discovery Agent - Standalone Configuration

## Running as Subagent

For deep research, create independent session with `sessions_spawn`:

```json
{
  "runtime": "subagent",
  "mode": "run",
  "task": "Painpoint discovery research",
  "label": "painpoint-discovery-deep-research",
  "thinking": "verbose"
}
```

## Additional Capabilities vs Skill Mode

Compared to skill mode, standalone agent can:

1. **Longer Research Sessions** - Not limited by single-turn conversation
2. **Batch Search & Analysis** - Can search 10+ keywords
3. **Cross-Source Comparison** - Compare information from multiple sources
4. **Generate Complete Reports** - Output markdown report files
5. **Knowledge Graph Visualization** - Generate mermaid charts

## Deep Research Workflow

### Phase 1: Information Gathering (10-15 min)
```
1. Search domain keywords + "problems/complaints/frustration/issues"
2. Search "best X tools/solutions" content (existing solutions)
3. Scrape Reddit/Quora/forums related discussions
4. Search industry news and trend reports
```

### Phase 2: Painpoint Extraction (5-10 min)
```
1. Extract specific complaints from collected content
2. Cluster similar problems
3. Identify high-frequency issues (appearing 3+ times)
4. Record sources and quotes
```

### Phase 3: Analysis & Assessment (5-10 min)
```
1. Match solutions to each painpoint
2. Assess market size (search related data)
3. Analyze competitive landscape
4. Provide recommendation ratings
```

### Phase 4: Report Generation (5 min)
```
1. Generate structured markdown report
2. Generate knowledge graph mermaid code
3. Output next-step action recommendations
```

## Output Files

After standalone agent run completes:
- `painpoint-reports/[domain]-[date].md` - Complete research report
- `painpoint-reports/[domain]-[date]-graph.md` - Knowledge graph (optional)

## Collaboration with OpenClaw Main Session

```
Main session user request
    ↓
Spawn painpoint subagent
    ↓
Subagent deep research → Generate report files
    ↓
Main session reads report → Discuss with user → Decide next steps
```

## Example Invocation

```bash
# User says: "Do deep research on weight loss painpoints"

# OpenClaw executes:
sessions_spawn(
  runtime="subagent",
  mode="run",
  task="Deep research on weight loss domain painpoints, generate complete report",
  label="painpoint-discovery-weightloss",
  thinking="verbose",
  runTimeoutSeconds=1800  # 30 minutes
)
```
