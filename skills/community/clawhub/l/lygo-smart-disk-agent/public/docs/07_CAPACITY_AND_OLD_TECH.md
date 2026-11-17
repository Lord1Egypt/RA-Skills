# Capacity & old-tech performance

**Measured F:\ SmartDisk:** total ≈ 15.3 MB, free ≈ 14.8 MB before build.

## Rules
- Prefer **stdlib Python 3** + static HTML/JS/CSS  
- Cap mycelium events (rotate)  
- Cap log files  
- No node_modules on F:  
- No model weights on F: v1  

## Performance knobs (`config/smart_disk.json`)
- `num_predict` / max tokens low (256–512 default)  
- `temperature` 0.3 for tools  
- single concurrent chat  

## Upgrade path
| Tier | Media | Contents |
|------|-------|----------|
| Lean (this disk) | 16 MB | Kernel + portal + agent |
| Standard | 8–32 GB | + portable Ollama + 1B model |
| Full | 64 GB+ | + 3B model + optional Node gateway clone from USB |
