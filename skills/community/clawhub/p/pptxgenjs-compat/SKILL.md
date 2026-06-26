---
name: pptxgenjs-compat
description: >
  This skill should be used when generating PPT files with pptxgenjs (Node.js library).
  It provides a complete workflow for creating PowerPoint-compatible PPTX files that
  won't trigger the "PowerPoint found a problem with content" repair dialog.
  Covers: safe API usage patterns, post-processing fixes for known pptxgenjs defects,
  and compatibility verification. Trigger when: creating PPT with pptxgenjs, fixing
  pptxgenjs-generated PPTX files, or whenever "pptxgenjs" or "PPT" generation is mentioned.
---

# pptxgenjs Compatibility Skill

Generate PowerPoint-compatible PPTX files using pptxgenjs without triggering repair dialogs.

## The Core Problem

pptxgenjs has **6 known defects** (GitHub Issue #1449) that cause PowerPoint to show the "problem with content" repair dialog. The defects are baked into the library's XML generation and **cannot be avoided at the JavaScript level**. A mandatory post-processing step is required after every PPTX generation.

## Workflow

### Step 1: Generate PPTX with Safe API Patterns

When writing pptxgenjs code, follow these rules to minimize (but not eliminate) compatibility issues:

#### Forbidden APIs (will cause cross-version issues)

```
❌ shadow — generates complex OOXML effect chains unsupported in many PowerPoint versions
❌ transparency — inconsistent behavior across PowerPoint/WPS/LibreOffice versions
❌ String shape names like "oval", "roundedRectangle" — writes invalid prstGeom values
```

#### Safe Alternatives

```
✅ Use line borders instead of shadow for visual depth
✅ Use pre-mixed colors instead of transparency (calculate blended colors on dark backgrounds)
✅ Pre-render dimmed icon variants (dark PNG) instead of runtime image transparency
✅ Always use enum constants: pres.shapes.OVAL, pres.shapes.ROUNDED_RECTANGLE
```

#### Pre-mixed Color Calculation

To replace transparency on a dark background, calculate the blended color:
```
background #1A1A2E + white at 20% opacity → approximately #3A3A4E
```

For dimmed icons, render at design time with a dark color:
```javascript
const iconDim = await iconToBase64Png(FaShield, "3A4450", 256);  // dark variant
```

### Step 2: Post-Process with fix_pptx_compatibility.py

**This step is MANDATORY.** Even with perfect API usage, pptxgenjs generates invalid XML that must be fixed.

Run the bundled script:
```bash
python scripts/fix_pptx_compatibility.py <input.pptx> [output.pptx]
```

If output is omitted, the input file is overwritten in place.

The script fixes all 6 known defects:
1. **Phantom slideMaster overrides** in `[Content_Types].xml` — the #1 cause of repair dialogs. pptxgenjs registers non-existent slideMaster2~N.xml for every slide
2. **Invalid theme font references** — replaces `+mn-lt`, `+mn-ea`, `+mn-cs`, `+mj-lt`, `+mj-ea`, `+mj-cs` with `Microsoft YaHei`
3. **dirty= attribute** — removes non-standard pptxgenjs attribute
4. **p14:modId elements** — removes non-standard namespace elements
5. **Notes Slides/Masters** — removes broken notes files and their relationship references
6. **Zero-extent shapes and empty elements** — fixes `cx="0" cy="0"`, `<a:t></a:t>`, `<a:ln />`

### Step 3: Verify

Open the PPTX in PowerPoint to confirm no repair dialog appears. For automated verification, check:
- All Override PartNames in `[Content_Types].xml` point to existing files
- No `+mn-lt` style font references remain
- No `dirty=` attributes remain
- No `p14:` namespace prefixes remain in slide XMLs

## Common Mistakes to Avoid (Lessons from Real Incidents)

1. **Don't assume shadow/transparency fixes are enough** — The real root cause is usually phantom slideMaster overrides in Content_Types.xml, not visual effects
2. **Don't write validation scripts with `max()` fallback to 0 for `-1` values** — This causes false positives in element order checks
3. **Don't use single-line regex for XML that spans multiple lines** — Use `re.DOTALL` flag
4. **Don't skip post-processing** — Even if the PPTX looks fine in your version of PowerPoint, it may break in others
5. **Search for known issues FIRST** — Before diagnosing compatibility problems from scratch, check GitHub Issues for the library

## Reference

For the complete list of pptxgenjs defects with examples and fixes, see `references/pptxgenjs-pitfalls.md`.
