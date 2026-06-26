# Code Review Feedback Templates

This document provides templates for various code review scenarios. Choose the template that best fits your review context.

---

## Template 1: Standard Review (Default)

Use this for most PR reviews.

```markdown
## Review Summary

**PR**: [Title/Number]
**Files Changed**: X files
**Risk Level**:🔴 / /

---

###🔴 Issues (Must Fix)

1. **[Issue Title]** - `path/to/file.py:42`
   - **Problem**: [What's wrong and why it matters]
   - **Impact**: [Security risk, bug, performance issue, etc.]
   - **Suggestion**: 
     ```[language]
     // Current code
     problematic_code()
     
     // Suggested fix
     fixed_code()
     ```

---

###arnings (Should Address)

1. **[Issue Title]** - `path/to/file.js:15`
   - **Observation**: [What you noticed]
   - **Why it matters**: [Potential impact]
   - **Recommendation**: [How to improve]

---

###💡 (Consider)

1. **[Suggestion Title]**
   - **Current approach**: [What's there now]
   - **Alternative**: [Better approach with reasoning]

---

### ✅ Positive Notes

- [What was done well - be specific]
- [Good patterns or practices observed]

---

### Recommendation

**Status**: Approve / Approve with changes / Request changes

[One-line summary of overall assessment]
```

---

## Template 2: Security-Focused Review

Use for auth changes, payment processing, data handling, or when security is the primary concern.

```markdown
## Security Review

**PR**: [Title/Number]
**Review Type**: Security Audit
**Review Date**: [Date]

---

### Security Assessment

| Category | Status | Notes |
|----------|--------|-------|
| Authentication | ✅ Pass /❌ | [Details] |
| Authorization | ✅ Pass /❌ | [Details] |
| Input Validation | ✅ Pass /❌ | [Details] |
| Data Protection | ✅ Pass /❌ | [Details] |
| Injection Prevention | ✅ Pass /❌ | [Details] |
| Dependency Security | ✅ Pass /❌ | [Details] |

---

###🔴 Vulnerabilities

1. **[Vulnerability Type]** - CVSS: [Score]
   - **Location**: `path/to/file:line`
   - **Description**: [Technical details]
   - **Exploit Scenario**: [How it could be exploited]
   - **Remediation**: [Specific fix]
   - **References**: [CWE, OWASP links]

---

### Security Recommendations

1. **[Recommendation]**
   - **Priority**: High / Medium / Low
   - **Implementation**: [How to implement]

---

### Compliance Notes

- [GDPR, HIPAA, PCI-DSS, or other regulatory considerations]

---

### Final Verdict

**Security Status**: Approved / Approved with conditions / Rejected

[Summary and any conditions for approval]
```

---

## Template 3: Performance Review

Use for performance-critical changes, optimization PRs, or when performance concerns are raised.

```markdown
## Performance Review

**PR**: [Title/Number]
**Focus**: Performance Analysis

---

### Performance Impact Assessment

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Latency (p50) | [value] | [value] | [+/-X%] |
| Latency (p99) | [value] | [value] | [+/-X%] |
| Throughput | [value] | [value] | [+/-X%] |
| Memory Usage | [value] | [value] | [+/-X%] |
| CPU Usage | [value] | [value] | [+/-X%] |

---

###🔴 Issues

1. **[Issue]** - Impact: [High/Medium/Low]
   - **Location**: `path/to/file:line`
   - **Problem**: [What's causing the issue]
   - **Evidence**: [Benchmark, profiling data, or analysis]
   - **Optimization**: [Suggested fix]
   - **Expected Improvement**: [Estimated gain]

---

### Performance Optimizations Applied

✅ [Good optimizations already in the PR]

---

### Recommendations

1. **[Optimization]**
   - **Effort**: Low / Medium / High
   - **Impact**: Low / Medium / High
   - **Details**: [Implementation notes]

---

### Scalability Considerations

- [Notes on how this change behaves at scale]
- [Bottlenecks that may appear with increased load]

---

### Verdict

**Performance Impact**: Positive / Neutral / Negative

[Summary and recommendations]
```

---

## Template 4: Architecture Review

Use for significant architectural changes, new patterns, or system design modifications.

```markdown
## Architecture Review

**PR**: [Title/Number]
**Scope**: [Component/System affected]

---

### Architectural Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Cohesion | ✅ Good / Concern /❌ | [Details] |
| Coupling | ✅ Good / Concern /❌ | [Details] |
| Extensibility | ✅ Good / Concern /❌ | [Details] |
| Testability | ✅ Good / Concern /❌ | [Details] |
| Operability | ✅ Good / Concern /❌ | [Details] |

---

### Design Patterns Used

- [Pattern name]: [Where and how it's applied]

### Design Concerns

1. **[Concern]**
   - **Location**: [File/Module]
   - **Issue**: [What's problematic]
   - **Impact**: [Long-term consequences]
   - **Alternative**: [Better approach]

---

### Dependencies

**New Dependencies Added**:
- [Package]: [Justification] / Questionable

**Dependency Changes**:
- [Details of version updates or removals]

---

### Future Considerations

- [Technical debt introduced]
- [Migration path if needed]
- [Deprecation timeline if applicable]

---

### Verdict

**Architecture**: Approved / Approved with revisions / Needs redesign

[Summary with architectural rationale]
```

---

## Template 5: Quick Review (Small Changes)

Use for minor changes, bug fixes, documentation updates, or when you need a lightweight review.

```markdown
## Quick Review

**PR**: [Title/Number]
**Change Size**: Small (< 50 lines)

### ✅ Checks Passed
- [ ] Logic looks correct
- [ ] No obvious bugs
- [ ] Style consistent
- [ ] Tests included (if applicable)

### Notes
[Any observations or minor suggestions]

### Status
✅ Approved / Minor changes needed

[One-line summary]
```

---

## Template 6: Rejection with Explanation

Use when changes are fundamentally flawed and need significant rework.

```markdown
## Review: Changes Requested

**PR**: [Title/Number]
**Decision**:❌jected - Significant Rework Needed

---

### Critical Issues

This PR has fundamental issues that prevent approval:

1. **[Major Issue]**
   - **Problem**: [Detailed explanation]
   - **Why it's blocking**: [Impact on system]
   - **Required changes**: [What needs to be done]

2. **[Second Major Issue]**
   - [Same format]

---

### Design Concerns

The current approach has architectural problems:

- [Concern 1 with explanation]
- [Concern 2 with explanation]

---

### Suggested Path Forward

1. [Step to address issue 1]
2. [Step to address issue 2]
3. [Consider discussing approach before resubmitting]

---

### Resources

- [Links to relevant documentation or patterns]
- [Examples of correct implementation]

---

I'm available to discuss these concerns and help guide the implementation. Let's align on the approach before proceeding with code changes.
```

---

## Template 7: JSON Output (CI/CD Integration)

Use for automated review systems or when machine-readable output is needed.

```json
{
  "review": {
    "pr_id": "123",
    "reviewer": "code-review-v2",
    "timestamp": "2026-03-23T10:00:00Z",
    "summary": "Brief overview of findings",
    "risk_level": "medium",
    "recommendation": "approve_with_changes"
  },
  "issues": [
    {
      "id": 1,
      "severity": "critical",
      "category": "security",
      "file": "src/auth/login.py",
      "line": 42,
      "column": 8,
      "message": "SQL injection vulnerability via string interpolation",
      "code_snippet": "cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
      "suggestion": "Use parameterized query: cursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))",
      "references": ["CWE-89", "OWASP-A03:2021"]
    }
  ],
  "positive_notes": [
    "Good use of type hints throughout",
    "Comprehensive error handling"
  ],
  "metrics": {
    "files_reviewed": 5,
    "lines_added": 120,
    "lines_removed": 45,
    "issues_found": 3,
    "critical_count": 1,
    "warning_count": 1,
    "suggestion_count": 1
  }
}
```

---

## Template Selection Guide

| Scenario | Recommended Template |
|----------|---------------------|
| Standard PR review | Template 1: Standard Review |
| Auth, payment, sensitive data changes | Template 2: Security-Focused Review |
| Performance optimizations | Template 3: Performance Review |
| New architecture, design patterns | Template 4: Architecture Review |
| Small fixes, docs, config | Template 5: Quick Review |
| Fundamentally flawed PR | Template 6: Rejection with Explanation |
| Automated systems, CI/CD | Template 7: JSON Output |

---

## Tips for Effective Feedback

### DO:
- Be specific with file and line references
- Explain the "why" behind suggestions
- Provide code examples for fixes
- Acknowledge what was done well
- Use constructive, respectful language

### DON'T:
- Make vague comments ("this looks wrong")
- Nitpick on style if linter handles it
- Assume intent without asking
- Use harsh or dismissive language
- Focus only on problems without solutions
