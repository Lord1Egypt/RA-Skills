# Docs-First Workflow

> **Never touch code without reading documentation first**
> Priority: CRITICAL | Category: Quality Control

## Overview

The single biggest source of agent errors is attempting solutions without consulting existing documentation. This skill enforces a mandatory reconnaissance phase before any code changes.

## The Problem

Agents love to improvise. When faced with a task, they often:
- Skip existing docs and "guess" the solution
- Implement workarounds for documented features
- Break systems by ignoring established patterns
- Waste tokens reinventing documented solutions

## The Solution: Mandatory Recon Phase

### BEFORE Any Code Change

```
┌─────────────────────────────────────────────────────────────┐
│                   RECONNAISSANCE PHASE                       │
│              (Must complete before BUILD)                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. SEARCH → Find relevant documentation                   │
│   2. READ → Understand existing solutions                    │
│   3. VALIDATE → Confirm approach matches conventions         │
│   4. DOCUMENT → Record findings before proceeding            │
│                                                              │
│   Only AFTER completing all 4 steps:                         │
│   └─→ Proceed to BUILD phase                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Reconnaissance Protocol

### Step 1: SEARCH

**Objective**: Find ALL relevant documentation

```yaml
search_locations:
  project_docs:
    - "README.md"
    - "docs/**/*"
    - "**/README.md"
    - "CONTRIBUTING.md"
    - "ARCHITECTURE.md"

  code_docs:
    - "Inline comments near target code"
    - "Docstrings in related modules"
    - "Type definitions and interfaces"

  external_docs:
    - "Official library documentation"
    - "API references"
    - "Known issue trackers"

  search_strategy:
    - "Start broad (project-level docs)"
    - "Narrow to specific (module-level docs)"
    - "Check examples and tests"
    - "Look for 'how-to' guides"
```

### Search Commands Template

```bash
# Find relevant documentation
find . -name "*.md" -type f | grep -E "(README|CONTRIBUTING|docs)"

# Find related code with docs
grep -r "function_name\|class_name" --include="*.py" --include="*.js" -A 5

# Check for existing patterns
grep -r "pattern_name" --include="*.py" --include="*.js"

# Look for tests that show usage
find . -path "*/test*" -name "*.py" -o -name "*.js"
```

### Step 2: READ

**Objective**: Understand existing solutions and patterns

```yaml
reading_focus:
  architecture:
    - "How is this system organized?"
    - "What are the key abstractions?"
    - "Where does this change fit?"

  patterns:
    - "How are similar problems solved?"
    - "What conventions exist?"
    - "What patterns should I follow?"

  constraints:
    - "What are the known limitations?"
    - "What are the 'don't do this' items?"
    - "What dependencies exist?"

  examples:
    - "How do tests handle this?"
    - "What examples exist in codebase?"
    - "What are the common usage patterns?"
```

### Reading Checklist

Before proceeding, you must be able to answer:

- [ ] What is the existing architecture for this area?
- [ ] What patterns are used for similar functionality?
- [ ] What are the documented do's and don'ts?
- [ ] What examples exist in the codebase?
- [ ] What tests show expected usage?
- [ ] What external docs apply?

### Step 3: VALIDATE

**Objective**: Confirm your approach matches established conventions

```yaml
validation_questions:
  architecture_fit:
    - "Does this fit the existing architecture?"
    - "Am I using established patterns?"
    - "Am I following project conventions?"

  solution_exists:
    - "Is there already a solution for this?"
    - "Can I use an existing feature?"
    - "Am I reinventing something documented?"

  compatibility:
    - "Is this compatible with existing code?"
    - "Will this break existing patterns?"
    - "Are there migration paths documented?"

  best_practice:
    - "Does this follow documented best practices?"
    - "Am I ignoring any warnings in docs?"
    - "Is there a recommended approach I'm missing?"
```

### Step 4: DOCUMENT

**Objective**: Record reconnaissance findings BEFORE proceeding

Create/Update `recon-[task-name].md`:

```markdown
# Reconnaissance: [Task Name]

**Date**: YYYY-MM-DD
**Agent**: [Agent Name]
**Task**: [Brief description]

## Documentation Reviewed

### Project Documentation
- [ ] README.md - [Key findings]
- [ ] ARCHITECTURE.md - [Key findings]
- [ ] CONTRIBUTING.md - [Key findings]
- [ ] Other: [List any other docs]

### Code Documentation
- [ ] [Module/File] - [Key findings]
- [ ] [Module/File] - [Key findings]

### External Documentation
- [ ] [URL/Source] - [Key findings]

## Existing Solutions Found

### Solution 1: [Name]
**Location**: [File/Function]
**Description**: [What it does]
**Relevance**: [Why it matters for this task]

### Solution 2: [Name]
**Location**: [File/Function]
**Description**: [What it does]
**Relevance**: [Why it matters for this task]

## Patterns Identified

1. **[Pattern Name]**
   - **Example**: [Code location]
   - **Usage**: [How it's used]

2. **[Pattern Name]**
   - **Example**: [Code location]
   - **Usage**: [How it's used]

## Constraints & Warnings

### Known Constraints
- [Constraint 1]
- [Constraint 2]

### Documented Warnings
- [Warning 1]
- [Warning 2]

## Proposed Approach

### What I Will Do
1. [Step 1]
2. [Step 2]

### How It Follows Documentation
- **Pattern Used**: [Which pattern]
- **Convention Followed**: [Which convention]
- **Documentation Reference**: [Which docs]

### Risks Identified
- [Risk 1] - [Mitigation]
- [Risk 2] - [Mitigation]

## Pre-Build Validation

- [ ] Approach follows documented patterns
- [ ] No existing solution is being ignored
- [ ] All constraints are respected
- [ ] All warnings are acknowledged
- [ ] Examples in codebase are consistent with approach

## Approval to Proceed

✅ All reconnaissance complete. Ready to proceed to BUILD phase.
```

## Forbidden Actions

These actions are PROHIBITED until reconnaissance is complete:

```yaml
prohibited_until_recon:
  - "Making any code changes"
  - "Creating new files"
  - "Modifying configuration"
  - "Running build commands"
  - "Writing tests (until pattern is understood)"
  - "Installing new dependencies (until verified not existing)"
```

## Example: Adding Authentication

### ❌ WITHOUT Docs-First (What Agents Do)

```
"I'll add JWT authentication. Let me create a new auth module
with custom token handling... [builds from scratch]"

Result: 500 lines of code, reinvents wheel, breaks existing patterns
```

### ✅ WITH Docs-First (Correct Approach)

```
RECON PHASE:
1. SEARCH: Find auth-related files
   - Found: auth/ directory already exists
   - Found: JWT utilities in utils/jwt.py
   - Found: Auth middleware in middleware/auth.py

2. READ: Understand existing system
   - Project uses passport-js pattern
   - Tokens already generated in utils/jwt.py
   - Middleware already handles validation

3. VALIDATE: Check approach
   - New endpoint should use existing jwt.py
   - Should follow passport-js pattern
   - Tests show expected usage

4. DOCUMENT: Record findings
   [Creates recon-auth-endpoint.md]

BUILD PHASE:
"I'll add the login endpoint using the existing JWT utilities
in utils/jwt.py, following the passport-js pattern shown in
the existing auth middleware."

Result: 20 lines of code, uses existing system, follows patterns
```

## Reconnaissance Quality Gates

### Minimum Requirements

Before proceeding to BUILD, reconnaissance must include:

```yaml
minimum_requirements:
  docs_read:
    minimum: 3
    types:
      - "Project-level (README, CONTRIBUTING)"
      - "Module-level (ARCHITECTURE, guides)"
      - "Code-level (docstrings, comments)"

  solutions_found:
    minimum: 1
    description: "At least one existing relevant solution"

  patterns_identified:
    minimum: 2
    description: "At least two architectural patterns"

  constraints_documented:
    minimum: 1
    description: "At least one constraint or warning"

  findings_recorded:
    required: true
    format: "recon-[task].md file created"
```

### Quality Scoring

```yaml
scoring:
  excellent:
    score: 5
    description: "Found existing solution, no new code needed"
    action: "USE EXISTING SOLUTION"

  good:
    score: 4
    description: "Clear path forward, patterns identified"
    action: "Proceed with confidence"

  acceptable:
    score: 3
    description: "Adequate information, some ambiguity"
    action: "Proceed with caution"

  insufficient:
    score: 1-2
    description: "Missing critical information"
    action: "COMPLETE RECONNAISSANCE"

  failed:
    score: 0
    description: "No reconnaissance performed"
    action: "MUST COMPLETE RECON PHASE"
```

## Integration with Other Skills

### With execution-discipline.md
```yaml
integration:
  before_build:
    skill: "docs-first"
    phase: "RECONNAISSANCE"
    output: "recon-[task].md"

  after_recon:
    skill: "execution-discipline"
    phase: "BUILD"
    input: "recon-[task].md"
```

### With scope-control.md
```yaml
integration:
  boundary_check:
    during: "VALIDATE step of recon"
    question: "Does this approach respect documented boundaries?"
```

## Enforcement

### Automatic Checks

```yaml
pre_build_checks:
  - name: "Recon file exists"
    check: "file exists: recon-*.md"
    fail_action: "Complete reconnaissance phase"

  - name: "Solutions documented"
    check: "recon file contains 'Existing Solutions' section"
    fail_action: "Document existing solutions"

  - name: "Patterns identified"
    check: "recon file contains 'Patterns Identified' section"
    fail_action: "Identify architectural patterns"

  - name: "Approval marked"
    check: "recon file contains 'Approval to Proceed'"
    fail_action: "Complete validation checklist"
```

### Manual Override

In rare cases where reconnaissance is impossible:

```yaml
override_conditions:
  - "No documentation exists (greenfield project)"
  - "Documentation is demonstrably wrong"
  - "Emergency fix (post-mortem required)"

override_protocol:
  1: "Document why reconnaissance is skipped"
  2: "Create plan assuming no patterns exist"
  3: "Get explicit approval"
  4: "Create documentation for future agents"
```

## Verification

After implementing this skill, verify compliance:

```bash
# Check for recon files
find ~/.openclaw/workspace -name "recon-*.md"

# Verify recon precedes changes
openclaw logs last --check-phase-order

# Measure recon quality
openclaw metrics recon-completeness
```

## Key Takeaway

**20 minutes of reconnaissance saves 2 hours of rework.** Always read before writing.

---

**Related Skills**: `execution-discipline.md`, `scope-control.md`, `testing-protocol.md`
