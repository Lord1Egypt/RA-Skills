---
name: mem-scan
description: Global Memory Bank Deep Scan and Task Analysis Workflow — Multi-repo aware. Use when the user invokes $mem-scan or asks for this workflow by name.
---

# mem-scan (Sage Adaptation)

This skill is adapted from a personal Codex skill. Key changes:
- **Multi-repo scan:** Searches across workspace AND all project repos (`code/*/memory-bank/`)
- **Cross-repo deduplication:** Identifies when tasks exist in multiple locations
- **Project awareness:** Checks if task belongs to a specific project repo

## Global Memory Bank Deep Scan and Task Analysis Workflow

### Overview
This workflow performs a comprehensive scan of ALL memory banks (workspace + project repos) to identify existing tasks, subtasks, and implementation docs relevant to user-specified content, and determines if new documentation needs to be created.

### Step 0: Multi-Repo Discovery
- **Scan ALL memory bank locations:**
  - `~/.openclaw/workspace/memory-bank/` (workspace)
  - `~/.openclaw/workspace/code/*/memory-bank/` (project repos: timesarrow, mb-core, etc.)
- **Identify active project:** Determine which repo the current work belongs to
- **Prevent duplicates:** Check if task already exists in another repo's memory-bank

### Step 3: Relevance Assessment Matrix
Create a relevance matrix for identified content:

```
| Content Type | Found Tasks | Relevance Score | Action Needed |
|--------------|--------------|-----------------|---------------|
| Bug Fix      | TXX, TYY     | High (85%)      | Update existing |
| New Feature  | None         | N/A             | Create new task |
| Enhancement  | TZZ          | Medium (60%)    | Create subtask |
| Architecture | META-XX      | High (90%)      | Update META task |
```

### Step 4: Gap Analysis
- **Missing Coverage**: Identify areas not covered by existing tasks
- **Overlap Detection**: Find duplicate or overlapping work
- **Dependency Mapping**: Map relationships between existing and needed work
- **Priority Assessment**: Determine urgency and impact

### Step 5: Task Creation/Update Recommendations
Based on the analysis, recommend specific actions:

#### A. Update Existing Tasks
- **When**: Content aligns 70%+ with existing task
- **Action**: Update task file with new information
- **Template**: Use existing task structure
- **Registry**: Update status and timestamps in `tasks.md`

#### B. Create New Subtasks
- **When**: Content is subset of existing larger task
- **Action**: Create subtask linked to parent
- **Template**: Use task-template.md with parent reference
- **Registry**: Add to tasks.md with dependency link

#### C. Create New Tasks
- **When**: Content represents entirely new work area
- **Action**: Create new task with appropriate ID
- **Template**: Use task-template.md
- **Registry**: Add to tasks.md with proper classification

#### D. Create Implementation Details
- **When**: Technical documentation is needed
- **Action**: Create implementation detail file
- **Template**: Use appropriate implementation template
- **Reference**: Link from relevant task(s)

#### E. Update META Tasks
- **When**: Architectural or cross-cutting concerns
- **Action**: Update relevant META task
- **Template**: Follow META task structure
- **Impact**: Document cross-task implications

### Step 6: Approval Request
Prepare detailed recommendation for user approval:

```
## Memory Bank Analysis Results

### Content Analyzed
- **Type**: [Bug Fix/New Feature/Enhancement/etc]
- **Scope**: [Brief description]
- **Impact**: [High/Medium/Low]

### Existing Related Items Found
- **Tasks**: [List of relevant tasks with IDs]
- **Implementation Docs**: [List of relevant docs]
- **Recent Sessions**: [List of relevant sessions]

### Recommended Actions
1. **Update Task TXX**: [Reason] - [Estimated effort]
2. **Create Subtask TXXa**: [Reason] - [Estimated effort]
3. **New Task TZZ**: [Reason] - [Estimated effort]
4. **Implementation Doc**: [Title] - [Reason]

### Approval Required
- [ ] Approve all recommended actions
- [ ] Approve specific items (list which)
- [ ] Request modifications to recommendations
- [ ] Decline all recommendations
```

### Step 7: Execution (If Approved)
- **Follow Memory Bank Update Workflow**: Execute approved actions using `/mem-update` workflow
- **Maintain Compliance**: Follow all v6.12 integrated rules
- **Update Registries**: Ensure all cross-references are updated
- **Document Decisions**: Record rationale in appropriate files

### Step 8: Verification
- **Cross-Reference Check**: Verify all links and references work
- **Template Compliance**: Ensure all files follow templates
- **Registry Consistency**: Verify tasks.md matches actual files
- **Session Documentation**: Update current session with analysis results

### Step 9: Reporting
Generate summary report:

```
## Memory Bank Analysis Summary

**Content**: [User input description]
**Analysis Date**: [Timestamp]
**Items Scanned**: [Number of files checked]
**Related Items Found**: [Count]
**New Items Created**: [Count]
**Items Updated**: [Count]

### Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

### Actions Taken
- [Action 1]
- [Action 2]
- [Action 3]

### Impact Assessment
- **Task Coverage**: [Percentage of relevant areas now covered]
- **Documentation Quality**: [Improvement description]
- **Development Efficiency**: [Expected improvement]
```

### Usage Examples

#### Example 1: Bug Fix Analysis
**Input**: "Fixed PDF viewer navigation issue on mobile"
**Analysis**: Finds T31 (PDF System), T52 (Offline Storage), mobile-related tasks
**Recommendation**: Update T31 with mobile-specific fix details

#### Example 2: New Feature Analysis
**Input**: "Add voice note recording for papers"
**Analysis**: No existing tasks found for voice features
**Recommendation**: Create new task T84 for Voice Notes System

#### Example 3: Architecture Change
**Input**: "Migrate from React Query to TanStack Query v5"
**Analysis**: Finds multiple tasks using React Query (T61, T75, etc.)
**Recommendation**: Create META task for migration plan, update affected tasks

### Automation Notes
- **Keyword Matching**: Uses fuzzy matching for task relevance
- **Dependency Tracking**: Maintains relationship graph
- **Template Generation**: Auto-generates task structures
- **Compliance Checking**: Validates against v6.12 rules
- **Impact Assessment**: Estimates development effort and priority

### Integration with Other Workflows
- **Feeds Into**: `/mem-update` workflow for execution
- **References**: Task templates and implementation patterns
- **Maintains**: Consistency with memory bank architecture
- **Supports**: Both development and documentation workflows

### Quality Assurance
- **Duplicate Detection**: Prevents creation of redundant tasks
- **Gap Analysis**: Ensures comprehensive coverage
- **Consistency Checking**: Maintains format and structure standards
- **Traceability**: Full audit trail of decisions and changes
