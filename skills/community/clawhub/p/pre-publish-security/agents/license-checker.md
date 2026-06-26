# License Compliance Checker Agent Task

**Target:** {{TARGET}}

## Mission
Verify licensing compliance and flag legal issues.

## Checks

1. **License File:**
   - LICENSE or LICENSE.md exists
   - Contains valid open-source license text
   - Year and copyright holder present

2. **Dependency Licenses:**
   - NPM: Check for GPL/AGPL conflicts (if MIT/Apache project)
   - Verify all dependencies have licenses
   - Flag copyleft licenses in permissive projects

3. **Copyright Headers:**
   - Source files have copyright notices (if required)
   - Consistent copyright holder

4. **Attribution:**
   - NOTICE file if needed (Apache License 2.0)
   - Third-party attributions present

## Commands to Run

```bash
cd {{TARGET}}

# Check LICENSE file
if [ -f LICENSE ]; then
    head -5 LICENSE
else
    echo "HIGH: Missing LICENSE file"
fi

# NPM license check (if package.json exists)
if [ -f package.json ]; then
    npm list --depth=0 2>/dev/null || true
    # Check for GPL/AGPL
    npm list --json --depth=0 | jq -r '.dependencies | to_entries[] | select(.value.license | contains("GPL")) | .key' || true
fi

# Check for copyright notices
grep -r "Copyright" . --include="*.js" --include="*.py" --include="*.sh" | head -5 || true
```

## Output Format

**CRITICAL:** GPL dependency in MIT-licensed project
**HIGH:** Missing LICENSE file
**MEDIUM:** Inconsistent copyright holders
**LOW:** Missing copyright headers

If no issues: **✅ License compliance verified**
