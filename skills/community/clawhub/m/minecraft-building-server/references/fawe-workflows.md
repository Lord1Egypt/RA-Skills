# FAWE / WorldEdit Workflows

## 1. Core WorldEdit Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| Selection tool | `//wand` | Wooden axe selection |
| Fill | `//set <block>` | Fill selection |
| Replace | `//replace <old> <new>` | Replace blocks in selection |
| Copy / paste | `//copy` → `//paste` | Duplicate builds |
| Save schematic | `//schematic save <name>` | Export as `.schem` |
| Load schematic | `//schematic load <name>` → `//paste` | Import/paste |
| Undo | `//undo` | Undo last action |

## 2. Why FAWE Matters

FAWE (FastAsyncWorldEdit) is preferred for serious build servers because it provides:
- asynchronous large edits
- lower lag during big operations
- better performance for large schematic or region tasks
- advanced brushes, masks, and patterns

## 3. Recommended Build Workflow

1. Prototype in creative mode
2. Select and export the build as `.schem`
3. Transfer the file to the target server if needed
4. Load + paste with FAWE
5. Adjust orientation / terrain blending / cleanup

## 4. Large Schematic Advice

- Use FAWE async paste where available
- Skip air with appropriate options when needed
- Stage big pastes off to the side before final placement
- Keep backups before massive edits
- Use region planning to avoid overlap with existing work

## 5. Build-Context Automation Tips

- Use RCON or scripts to trigger schematic-related commands when appropriate
- Batch multiple schematic placements for scene assembly
- Keep coordinate systems explicit for modular builds

## 6. Boundary Note

This reference is about **building workflows** on a running server.
It does not cover plugin lifecycle, backups, or full server operations.
