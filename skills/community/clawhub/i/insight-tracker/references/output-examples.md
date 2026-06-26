# Insight Output Examples

## Example 1: Daily Insight Record

```markdown
# Insights - 2024-03-15

## New Insights

### INS-001: Validation catches 80% of skill issues
- **Content**: Running validate-skill.sh before packaging catches most common errors
- **Source**: Session analysis
- **Tags**: pattern, process
- **Priority**: high
- **Status**: active
- **Created**: 2024-03-15T09:30:00Z
- **References**: INS-003

### INS-002: Users prefer dated filenames
- **Content**: When given the choice, users consistently prefer YYYY-MM-DD format
- **Source**: User feedback
- **Tags**: user-preference, pattern
- **Priority**: medium
- **Status**: active
- **Created**: 2024-03-15T10:15:00Z

### INS-003: Scripts need executable bit
- **Content**: Many script failures are due to missing chmod +x
- **Source**: Debugging session
- **Tags**: technical, risk
- **Priority**: high
- **Status**: active
- **Created**: 2024-03-15T11:00:00Z
- **References**: INS-001

## Summary
- Total insights: 3
- High priority: 2
- New tags: technical
```

## Example 2: Weekly Summary

```markdown
# Insights Summary - Week of 2024-03-11

## By Priority

### High (5)
1. INS-001: Validation catches 80% of issues
2. INS-003: Scripts need executable bit
3. INS-005: Memory files need rotation
4. INS-007: Cross-skill dependencies exist
5. INS-009: Test coverage below 50%

### Medium (3)
1. INS-002: Users prefer dated filenames
2. INS-004: Templates speed up scaffolding
3. INS-008: References help new users

### Low (2)
1. INS-006: Color output preferred
2. INS-010: Emoji usage varies by user

## By Tag

- pattern: 4 insights
- technical: 3 insights
- process: 2 insights
- user-preference: 2 insights
- risk: 1 insight

## Actions
- [ ] Address INS-003: Add chmod to scaffold
- [ ] Address INS-005: Implement rotation
- [ ] Archive INS-006: Low value
```

## Example 3: Search Results

```markdown
# Insight Search Results

Query: "validation" (3 matches)

### INS-001: Validation catches 80% of skill issues
- **Priority**: high | **Status**: active
- **Tags**: pattern, process
- **Content**: Running validate-skill.sh before packaging catches most common errors

### INS-011: Validation should check YAML syntax
- **Priority**: medium | **Status**: active
- **Tags**: technical, opportunity
- **Content**: Current validator doesn't check YAML frontmatter syntax

### INS-015: Validation performance acceptable
- **Priority**: low | **Status**: archived
- **Tags**: technical
- **Content**: Validation runs in under 1s for most skills
```
