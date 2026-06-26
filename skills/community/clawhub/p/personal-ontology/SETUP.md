# Personal Ontology — Setup

## Quick Start

### Option 1: Bootstrap from existing notes (recommended)

If you have an existing notes/journal collection:

```
"Bootstrap my personal ontology"
```

The agent will:
1. Scan your notes for beliefs, predictions, goals, and projects
2. Present candidates for your review (nothing auto-commits)
3. Create your ontology files with confirmed items

### Option 2: Start fresh

Copy the templates to your notes folder:

```
My_Personal_Ontology/
├── index.md           ← copy from templates/
├── 1-higher-order.md
├── 2-beliefs.md
├── 3-predictions.md
├── 4-core-self.md
├── 5-goals.md
└── 6-projects.md
```

Then work through `prompts.md` to fill in each layer.

---

## Configuration

By default, the agent looks for your ontology at:
- `[Your Notes Folder]/My_Personal_Ontology/`

To customize, set in your agent config or workspace:
```
ONTOLOGY_DIR=/path/to/your/ontology
```

---

## After Setup

### Daily integration (optional)

Add ontology references to your briefings:
- Read Core Self + Goals before suggesting tasks
- Flag work that doesn't map to any Project/Goal
- Occasionally prompt for missing layers (Higher Order, Predictions)

### Maintenance

The agent can run periodic checks:
- **Weekly**: Are tasks serving projects? Projects serving goals?
- **Monthly**: Any new predictions? Existing ones to update?
- **Quarterly**: Has Core Self shifted? Full review.

---

## Visualization

The `index.md` includes a Mermaid diagram. As you add Objects, update the diagram to show relationships.

For command-line rendering:
```bash
node scripts/render-ontology.js           # Output Mermaid code
node scripts/render-ontology.js --ascii   # ASCII art (requires beautiful-mermaid)
node scripts/render-ontology.js --svg out.svg  # SVG export
```

---

## Troubleshooting

**Agent can't find ontology files**
- Check the path in your config
- Ensure files exist and are readable markdown

**Bootstrap found nothing**
- Your notes may not have explicit statements
- Try the manual prompts instead

**Mermaid not rendering**
- Ensure your markdown viewer supports Mermaid (Obsidian does)
- Check syntax in the code block

---

## Next Steps

1. Complete the bootstrap or manual setup
2. Review the Mermaid visualization in `index.md`
3. Use the ontology daily — let it inform your decisions
4. Update as you learn more about yourself
