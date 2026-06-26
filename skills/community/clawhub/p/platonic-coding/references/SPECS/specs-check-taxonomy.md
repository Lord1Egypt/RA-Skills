# Check Taxonomy

## Objective

Verify consistent use of terminology across all RFC files and check against canonical terms in rfc-namings.md.

## Inputs

- **Specs Directory**: Path to the specs directory

## Steps

1. **Load Canonical Terms**
   - Read `rfc-namings.md`
   - Extract all terms from the Terminology Index table
   - Create a list of canonical terms (normalize to lowercase for comparison)

2. **Scan Active RFC Files**
   - Find all RFC files matching `RFC-*.md`
   - Exclude supporting files and deprecated RFCs
   - Only process RFCs with Status: Draft, Review, or Frozen

3. **Extract Terms from Each RFC**
   For each RFC, identify:
   - Terms that are defined (look for definitions)
   - Terms that are used (capitalized words, acronyms)
   - Terms in tables, lists, and definitions

4. **Compare Against Canonical Terms**
   For each term found in RFCs:
   - Check if it matches a canonical term (case-insensitive)
   - Check for similar terms (potential conflicts)
   - Check for deprecated terms (if rfc-namings.md marks any)

5. **Check Consistency**
   - Verify same term is used consistently across RFCs
   - Check for variations (e.g., "World Model" vs "world model" vs "WorldModel")
   - Identify terms used but not defined
   - Identify terms defined but not in namings

6. **Generate Report**
   Create a report with:
   - **Errors**: Inconsistent terminology usage
   - **Warnings**: Terms that might conflict or need review

## Comparison Rules

### Exact Match
- Term matches canonical term exactly (case-insensitive)
- ✅ No issue

### Similar Match
- Term is similar to canonical term (e.g., "WorldModel" vs "World Model")
- ⚠️ Warning: Potential inconsistency

### No Match
- Term not found in canonical terms
- ⚠️ Warning: Term may need to be added to namings

### Deprecated Term
- Term matches a deprecated term
- ❌ Error: Should not use deprecated terms

## Output Format

### Errors

```
❌ Errors Found:
- RFC-002: Uses deprecated term "OldTerm" (replaced by "NewTerm")
- RFC-003: Inconsistent term "WorldModel" (canonical: "World Model")
```

### Warnings

```
⚠️  Warnings:
- RFC-001: Term "NewConcept" is used but not defined in rfc-namings.md
- RFC-002: Term "Stream" used inconsistently (sometimes "stream", sometimes "Stream")
- RFC-004: Similar term "DataModel" might conflict with canonical "Data Model"
```

## Verification Checklist

After checking, verify:

- [ ] All terms match canonical terms (or are new terms to be added)
- [ ] No deprecated terms are used
- [ ] Terms are used consistently across RFCs
- [ ] New terms are properly defined
- [ ] Terminology matches rfc-namings.md

## Notes

- **Focus on defined terms**, not every capitalized word
- **Case sensitivity**: Canonical terms may have specific capitalization
- **Abbreviations**: Check both full term and abbreviation
- **Plural forms**: Consider singular/plural variations
- **Compound terms**: Check for variations in spacing/hyphenation

## Best Practices

- Terms should be defined before first use
- Terms should match canonical definitions exactly
- New terms should be added to rfc-namings.md
- Deprecated terms should be replaced with current terms
