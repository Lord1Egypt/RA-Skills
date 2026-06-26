---
name: issue-finder
version: "1.6.0"
description: "Discover valuable GitHub issues with smart positive-label detection and analyze bug fix feasibility. Use when: (1) Finding good issues to contribute, (2) Auto-detecting positive contribution signals via labels, (3) Analyzing issue quality and fix difficulty, (4) Prioritizing high-value issues by maintainer signals."
---

# GitHub Issue Finder & Analyzer

Systematically discover and evaluate GitHub issues for open source contribution opportunities.

## Core Workflow

### 1. Issue Discovery

#### 1.1 Positive Label Detection (v1.6.0 新增)

**核心概念**: 现代项目使用自动化标签系统标记 issue 的贡献价值。优先寻找带有**正向标签**的 issues。

**正向标签分类**:

| 类别 | 标签模式 | 含义 | 优先级 |
|------|----------|------|--------|
| 可修复性 | `*:fix-shape-*`, `*:queueable-fix`, `*:queue_fix_pr` | 已被分析并确认可修复 | ⭐⭐⭐⭐⭐ |
| 可复现性 | `*:source-repro`, `reproducible`, `confirmed` | 问题已被复现验证 | ⭐⭐⭐⭐⭐ |
| 影响评估 | `impact:*`, `severity:*`, `priority:*` | 明确的影响范围评估 | ⭐⭐⭐⭐ |
| 价值评级 | `issue-rating: *`, `value:*`, `diamond`, `gold` | 官方价值评级 | ⭐⭐⭐⭐⭐ |
| 贡献邀请 | `good first issue`, `help wanted`, `contributions welcome` | 明确邀请贡献 | ⭐⭐⭐⭐ |
| 范围标记 | `scope:*`, `area:*`, `module:*` | 清晰的修改范围 | ⭐⭐⭐ |

**OpenClaw 正向标签示例**:

```bash
# ClawSweeper 自动化标签（高价值信号）
gh issue list --repo openclaw/openclaw --label "clawsweeper:fix-shape-clear" --state open
gh issue list --repo openclaw/openclaw --label "clawsweeper:queueable-fix" --state open
gh issue list --repo openclaw/openclaw --label "clawsweeper:source-repro" --state open

# 影响评估标签
gh issue list --repo openclaw/openclaw --label "impact:auth-provider" --state open

# 价值评级标签（🦞 diamond lobster = 最高价值）
gh issue list --repo openclaw/openclaw --label "issue-rating: 🦞 diamond lobster" --state open
gh issue list --repo openclaw/openclaw --label "issue-rating: *" --state open
```

**通用正向标签发现流程**:

```bash
# 1. 先探索仓库的标签系统
gh api repos/owner/repo/labels --paginate | jq '.[].name'

# 2. 识别正向标签模式
# 查找包含以下关键词的标签：
# - fix, queue, repro, confirm, impact, rating, value, contribution
# - good, help, welcome, easy, beginner, junior

# 3. 按优先级批量查询
gh issue list --repo owner/repo --state open \
  --label "fix-shape-clear,queueable-fix,source-repro" \
  --json number,title,labels,createdAt
```

#### 1.2 传统标签发现

```bash
# 经典贡献标签
gh issue list --repo owner/repo --label "good first issue" --state open
gh issue list --repo owner/repo --label "help wanted" --state open

# 缺陷和功能
gh issue list --repo owner/repo --label "bug" --state open
gh issue list --repo owner/repo --label "enhancement" --state open

# 跨仓库搜索
gh search issues --label "good first issue,help wanted" --state open --limit 20
```

#### 1.3 标签优先级矩阵

**Tier 1 - 立即行动** (维护者明确标记为值得修复):
- `*:fix-shape-*` / `*:queueable-*` / `*:queue_fix_pr`
- `*:source-repro` / `confirmed` / `reproducible`
- `issue-rating: 🦞` / `value:high` / `priority:critical`

**Tier 2 - 高优先级** (有明确贡献信号):
- `good first issue` / `help wanted` / `contributions welcome`
- `impact:*` / `severity:high`
- `scope:*` (清晰范围)

**Tier 3 - 标准候选**:
- `bug` / `enhancement` / `feature`
- `documentation` / `performance`

**Tier 4 - 谨慎评估**:
- 无正向标签的普通 issue
- 需要自行判断价值

### 2. Issue Evaluation Framework

Read the referenced evaluation criteria: [references/evaluation-criteria.md](references/evaluation-criteria.md)

#### Feasibility Assessment

**Bug Fix Feasibility**:
1. **Reproducibility** - Can you reproduce the issue?
2. **Root Cause** - Is the cause identifiable from issue description/code?
3. **Scope** - How many files/components affected?
4. **Dependencies** - Does fix require changes to external dependencies?
5. **Test Coverage** - Are there existing tests? Can you write tests?

**Feature Implementation Feasibility**:
1. **Clarity** - Is the feature well-defined?
2. **Alignment** - Does it fit project's roadmap/vision?
3. **Complexity** - New code vs. modifying existing code?
4. **Breaking Changes** - Will it break existing functionality?
5. **Maintainability** - Long-term maintenance implications?

#### Value Assessment

**Contribution Value Score** (1-10):

| Factor | Weight | Criteria |
|--------|--------|----------|
| Impact | 30% | User-facing vs internal, number of affected users |
| Learning | 25% | New skills/concepts learned |
| Community | 20% | Maintainer responsiveness, community activity |
| Complexity | 15% | Time investment vs. value gained |
| Portfolio | 10% | Demonstrable value for portfolio/career |

**Scoring Guide**:
- **9-10**: High impact, great learning, active maintainers
- **7-8**: Good contribution opportunity
- **5-6**: Moderate value, consider carefully
- **1-4**: Low ROI, skip unless specific reason

### 3. Issue Analysis Process

#### Step 1: Gather Information

```bash
# Get issue details
gh issue view <issue-number> --repo owner/repo

# Check issue comments/discussion
gh issue view <issue-number> --repo owner/repo --comments

# Check linked PRs
gh pr list --repo owner/repo --search "fixes #<issue-number>"

# Check project files
gh api repos/owner/repo/contents
```

#### Step 2: Analyze Codebase Context

```bash
# Clone or navigate to repo
cd /path/to/repo

# Understand structure
find . -type f -name "*.ts" | head -20

# Check recent commits
git log --oneline -20

# Look for similar patterns
grep -r "related_functionality" --include="*.ts"
```

#### Step 3: Generate Analysis Report

Use the template: [references/analysis-template.md](references/analysis-template.md)

**Report Structure**:
1. Issue Summary
2. Root Cause Analysis (for bugs) / Feature Scope (for features)
3. Proposed Solution Approach
4. Estimated Effort
5. Risk Assessment
6. Learning Opportunities
7. Recommendation

### 4. Decision Framework

**Go/No-Go Checklist**:

✅ **Proceed if**:
- Issue is well-documented
- Maintainers are responsive (< 1 week avg)
- You understand the affected code
- Effort matches available time
- Clear path to solution

❌ **Skip if**:
- Issue is unclear or lacks details
- Maintainers unresponsive for months
- Requires deep domain expertise you lack
- Breaking changes or major refactoring needed
- No clear acceptance criteria

### 5. Execution Strategy

Once you've identified a good issue:

1. **Comment on issue** - Express interest, ask clarifying questions
2. **Wait for maintainer feedback** - Get assigned before starting
3. **Create feature branch** - `fix/issue-number-description`
4. **Implement incrementally** - Small, focused commits
5. **Test thoroughly** - Unit tests, integration tests
6. **Document changes** - Update docs if needed
7. **Submit PR** - Reference issue, describe changes

## Advanced Techniques

### Pattern-Based Issue Finding

Search for specific code patterns that indicate common issues:

```bash
# Find TODO comments
gh search code "TODO" --repo owner/repo

# Find deprecated patterns
gh search code "deprecated" --repo owner/repo --language TypeScript

# Find error handling gaps
gh search code "catch.*{}" --repo owner/repo
```

### Project Health Indicators

Before investing time, check project health:

```bash
# Recent activity
gh repo view owner/repo --json updatedAt,pushedAt

# Contributor count
gh api repos/owner/repo/contributors --paginate | jq length

# Open issues/PRs ratio
gh repo view owner/repo --json openIssuesCount,openPullRequestsCount

# CI/CD status
gh api repos/owner/repo/actions/workflows
```

**Healthy Project Signs**:
- Recent commits (within days/weeks)
- Active PR reviews
- CI/CD passing
- Maintainers respond to issues/PRs
- Clear contributing guidelines

### Batch Analysis

For analyzing multiple issues efficiently:

```bash
# Export issues to JSON for analysis
gh issue list --repo owner/repo --state open --limit 50 --json number,title,labels,state,createdAt,comments

# Use the analysis script
python3 scripts/analyze_issues.py --repo owner/repo --output report.md
```

## Best Practices

1. **Start Small** - Begin with `good first issue` or documentation
2. **Understand Before Coding** - Read code, understand patterns
3. **Communicate Early** - Comment on issue before starting work
4. **Test Your Changes** - Write tests, run existing tests
5. **Follow Conventions** - Match project's coding style
6. **Be Patient** - Reviews take time, iterate on feedback

## Common Pitfalls

- Starting work without maintainer acknowledgment
- Missing existing PRs that address the same issue
- Underestimating scope or complexity
- Ignoring project conventions and patterns
- Submitting large, unfocused PRs

## Quick Reference

**Issue Labels Priority** (easiest to hardest):
1. `documentation` → `good first issue` → `help wanted`
2. `bug` (small scope) → `bug` (medium scope)
3. `enhancement` (small) → `feature` (medium) → `feature` (large)

**Time Estimation Guide**:
- **Hours**: Documentation, typo fixes, config changes
- **Days**: Small bug fixes, minor features, test additions
- **Weeks**: Medium bugs, moderate features, refactoring
- **Months**: Large features, architectural changes

**Success Indicators**:
- Clear issue description
- Reproducible steps (for bugs)
- Maintainer engagement
- Existing similar PRs to learn from
- Well-structured codebase