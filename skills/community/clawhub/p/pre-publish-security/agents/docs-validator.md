# Documentation Validator Agent Task

**Target:** {{TARGET}}

## Mission
Validate documentation accuracy, check for placeholders, and verify metadata.

## Checks

1. **Placeholder Detection:**
   - `[ORG]`, `[USERNAME]`, `[TODO]`
   - `FIXME`, `TODO`, `XXX` comments
   - `example.com`, `test@example.com`
   - Version `0.0.0` or `1.0.0-alpha`

2. **Metadata Validation:**
   - SKILL.md: name, description, homepage
   - package.json: name, version, repository
   - README: installation instructions, usage

3. **URL Verification:**
   - GitHub repo URLs exist and match ownership
   - Homepage links are valid (HTTP 200)
   - No localhost/127.0.0.1 URLs

4. **Completeness:**
   - README.md exists
   - LICENSE file exists
   - SKILL.md (for ClawHub skills)

## Commands to Run

```bash
cd {{TARGET}}

# Placeholder scan
grep -r -E "\[ORG\]|\[TODO\]|\[USERNAME\]|FIXME|TODO|XXX|example\.com" . \
  --include="*.md" \
  --include="*.json" \
  2>/dev/null || true

# Check required files
[ -f README.md ] || echo "MEDIUM: Missing README.md"
[ -f LICENSE ] || echo "HIGH: Missing LICENSE file"
[ -f SKILL.md ] && grep -q "homepage:" SKILL.md || echo "HIGH: Missing homepage in SKILL.md"

# Extract and validate URLs
grep -r -oE "https?://[^\s\"\')>]+" . \
  --include="*.md" \
  --include="*.json" \
  | grep -E "(localhost|127\.0\.0\.1|0\.0\.0\.0)" \
  && echo "MEDIUM: Found localhost URL in docs"
```

## Output Format

**CRITICAL:** Placeholder `[ORG]` in SKILL.md homepage
**HIGH:** Missing LICENSE file
**MEDIUM:** TODO comment in README
**LOW:** Example email in docs

If no issues: **✅ Documentation validated**
