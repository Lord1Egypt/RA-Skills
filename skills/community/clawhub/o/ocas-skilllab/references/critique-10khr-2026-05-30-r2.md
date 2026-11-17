# 10khr Session — 2026-05-30 (Round 2)

## Fixes Applied This Round

### ocas-imagine
- **Issue**: Duplicate "## Support file map" section (old version without "When to read" column at line 163, proper version at line 190)
- **Fix**: Removed old version (15 lines removed)
- **Result**: 220→206 lines, no duplicate sections

### ocas-multipass
- **Issue 1**: Trailing empty "## Support File Map" header at line 189
- **Issue 2**: Duplicate lowercase "When to use" / "When NOT to use" sections (lines 43-55)
- **Fix**: Removed trailing header + duplicate sections (15 lines removed)
- **Result**: 189→174 lines

### ocas-custodian
- **Issue**: Duplicate "When to use" / "When NOT to use" with lowercase headings (lines 44-59)
- **Fix**: Removed duplicate sections (17 lines removed)
- **Result**: 269→252 lines

### ocas-genie
- **Issue**: "## Pitfalls" heading instead of standard "## Gotchas"
- **Fix**: Renamed heading for consistency
- **Result**: No line change

## Structural Audit Results
All 31 ocas-* skills now have:
- ✅ Valid YAML frontmatter with license: MIT
- ✅ includes: references/** where refs/ exists
- ✅ When to Use / When NOT to Use (uppercase, single instance)
- ✅ Responsibility Boundary or Responsibility boundary
- ✅ Gotchas or Pitfalls section
- ✅ Support File Map with "When to read" column
- ✅ Code ratio under 20%

## Library State After Round 2
- Skills fixed: 5 (mentor, imagine, multipass, custodian, genie)
- Total lines removed: ~71
- All code ratios: passing
- All YAML: valid