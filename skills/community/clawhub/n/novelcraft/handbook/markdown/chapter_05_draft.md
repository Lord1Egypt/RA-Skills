# Chapter 5: Tips & Troubleshooting

## Best Practices

### 1. Configure Before Starting

Change defaults **before** you begin. Retroactive adjustments are tedious.

### 2. Use the Project Manifest

The manifest is your overview. Update status changes immediately.

### 3. Accept Compromises

The output is a **first draft**. Perfection comes in post-processing.

### 4. Sequence is Sacred

Never write two chapters simultaneously. Continuity suffers otherwise.

### 5. Visuals = Bonus

Without images, the workflow works just the same. Visuals are optional.

## Common Problems

### Problem: Chapter is REJECTED

**Cause:** Too many foreign characters, continuity errors, too few words.

**Solution:**
1. Check UTF-8 encoding
2. Re-read previous chapter
3. Check word count
4. Max 3 revisions, then rewrite

### Problem: Images take forever

**Cause:** Server overloaded or large images.

**Solution:**
- Note time, don't wait
- Continue with chapters
- Create PDF without images
- Check again later

### Problem: Config is ignored

**Cause:** Wrong level or typo in YAML.

**Solution:**
- Check path: `~/.openclaw/workspace/novelcraft/config/`
- Validate YAML syntax
- Higher level checks lower levels

### Problem: Review scores seem arbitrary

**Cause:** Understanding weights.

**Solution:**
- UTF-8 is ×3 — most important
- Word count ×2 — counts a lot
- Grammar only ×1 — less critical

## Resources

| Resource | Path |
|----------|------|
| Skill Docs | `~/.openclaw/skills/novelcraft/SKILL.md` |
| Config Schema | `~/.openclaw/workspace/novelcraft/config/CONFIG-SCHEMA.md` |
| Templates | `~/.openclaw/skills/novelcraft/templates/` |
| Manifest Template | `~/.openclaw/workspace/novelcraft/config/PROJECT-MANIFEST-TEMPLATE.md` |

## Conclusion

Novelcraft is a tool, not magic. With realistic expectations and some patience, functional book drafts emerge that you can use as a foundation for your creativity.

Happy writing!

---

*Version: 3.0.0 — Standardized Config Schema*
