---
name: gstack-skills
description: >
  Complete development workflow suite from Y Combinator CEO Garry Tan's gstack. 
  Use /gstack or any gstack command (/office-hours, /review, /ship, etc.) to access specialized workflows for product ideation, code review, testing, QA, and deployment. 
  Automatically routes to the appropriate specialized skill.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [development, workflow, AI, productivity, gstack, startup, code-review, qa, deployment]
---

# gstack-skills - Complete Development Workflow Suite

Complete development workflow suite adapted from Garry Tan's gstack for OpenClaw/WorkBuddy. Provides 15 specialized tools covering the entire development lifecycle from product ideation to deployment.

## About gstack

gstack is Y Combinator CEO Garry Tan's open-source Claude Code configuration that helped him write **600,000+ lines of production code in 60 days** (35% tests). This OpenClaw adaptation makes those powerful workflows available to any AI agent.

## Quick Start

**Use any of these commands directly:**

- `/gstack` - Get help and see all available commands
- `/office-hours` - Validate product ideas and design thinking
- `/plan-ceo-review` - CEO perspective on feature planning
- `/plan-eng-review` - Engineering architecture review
- `/review` - Pre-merge code review
- `/qa` - Test application and fix bugs
- `/ship` - Automated release workflow
- `/investigate` - Systematic root cause analysis

**Example usage:**

```
User: /office-hours I have an idea for an AI-powered code review tool
```

```
User: /review my current branch
```

```
User: /ship the user authentication feature
```

## Command Routing

When a user invokes any gstack command, this skill automatically routes to the appropriate specialized skill:

| Command | Specialized Skill | Purpose |
|---------|-------------------|---------|
| `/gstack` | gstack-skills | Show help and command overview |
| `/office-hours` | office-hours | Product ideation and validation |
| `/plan-ceo-review` | plan-ceo-review | CEO perspective planning |
| `/plan-eng-review` | plan-eng-review | Engineering architecture review |
| `/plan-design-review` | plan-design-review | Design review |
| `/design-consultation` | design-consultation | Design system consultation |
| `/review` | review | Pre-merge code review |
| `/investigate` | investigate | Root cause analysis |
| `/design-review` | design-review | Design audit and fixes |
| `/qa` | qa | Test application and fix bugs |
| `/qa-only` | qa-only | Bug reporting only |
| `/ship` | ship | Automated release workflow |
| `/document-release` | document-release | Update documentation |
| `/retro` | retro | Team retrospective |
| `/codex` | codex | OpenAI Codex independent review |
| `/careful` | careful | Dangerous operation warnings |
| `/freeze` | freeze | Lock file editing scope |
| `/guard` | guard | Full safety mode (careful + freeze) |

## When to Use This Skill

This skill acts as a router and should be used when:

1. **User invokes `/gstack`** - Show command overview and recommendations
2. **User needs guidance** - Help choose the right gstack command for their task
3. **User is new to gstack** - Provide context and explain the workflow philosophy
4. **User wants to learn** - Explain how gstack commands work together

For specific command execution, this skill routes to the appropriate specialized skill.

## Core Philosophy

### Boil the Lake Principle

> "Don't be half-invested, boil the whole lake" - Garry Tan

AI-assisted development should pursue complete implementation, not shortcuts. When a problem is identified, actually fix it. Completing a task means truly completing it.

### Intelligent Borrowing

When borrowing features from other products, always consider:
1. Why does it work in the original product?
2. Will it succeed or fail in your product?
3. What adaptations are needed for success?

## Recommended Workflow

The complete development lifecycle:

```
1. /office-hours       → Validate product ideas
2. /plan-ceo-review    → CEO perspective review
3. /plan-eng-review    → Engineering architecture review
4. /plan-design-review → Design review
5. /review             → Code review
6. /qa                 → Test and fix bugs
7. /ship               → Release to production
```

## Command Overviews

### Product Ideation Phase

#### `/office-hours`
YC office hours tool for product idea validation. Use when:
- User says "brainstorm", "I have an idea", "help me think through this"
- Validating startup concepts
- Design thinking and problem reframing

#### `/plan-ceo-review`
CEO/founder perspective planning. Use when:
- User says "think bigger", "expand scope", "strategic review"
- Evaluating feature ambition
- Challenging assumptions and finding 10x opportunities

#### `/plan-eng-review`
Engineering manager perspective. Use when:
- User says "engineering review", "architecture review"
- Evaluating technical architecture
- Assessing implementation approaches

#### `/plan-design-review`
Designer perspective. Use when:
- User says "design review"
- Checking UX and design quality

### Development Phase

#### `/review`
Pre-merge code review. Use when:
- User says "review this PR", "code review", "pre-landing review"
- Code is about to be merged
- Analyzing SQL security, race conditions, LLM trust boundaries

#### `/investigate`
Debugging expert. Use when:
- User says "debug this", "investigate", "root cause"
- Systematic root cause analysis needed
- Complex troubleshooting

#### `/design-consultation`
Design partner consultation. Use when:
- User says "design consultation"
- Building complete design systems
- Design thinking workshops

### Testing & Release Phase

#### `/qa`
QA engineer. Use when:
- User says "run QA", "test this", "check bugs"
- Code changes need verification
- Systematic testing and bug fixing

#### `/qa-only`
QA reporter. Use when:
- User says "qa-only" or just wants bug reports
- No automatic fixing, just reporting

#### `/ship`
Release engineer. Use when:
- User says "ship", "deploy", "push to main", "create PR"
- Fully automated release workflow
- Merge base branch, run tests, version management, create PR

### Documentation & Review

#### `/document-release`
Technical writer. Use when:
- User says "document release", "update docs"
- Updating project documentation

#### `/retro`
Engineering manager. Use when:
- User says "retro", "retrospective"
- Team weekly reports

### Power Tools

#### `/codex`
OpenAI Codex independent review. Use when:
- Needing a second opinion
- Cross-validating review results

#### `/careful`
Safety guardrails. Use when:
- About to perform dangerous operations
- Delete operations, file overwrites, dangerous commands

#### `/freeze`
Lock file editing scope. Use when:
- Want to restrict which files can be edited
- Focus changes to specific directories

#### `/guard`
Full safety mode. Use when:
- Maximum caution needed
- Combines careful + freeze for complete safety

## Usage Examples

### Example 1: New Feature Development

```
User: I want to add user authentication to my app

AI: Let's use the gstack workflow for this.

Step 1: /office-hours
Let me help you validate and think through the authentication feature...

[office-hours skill executes]

Step 2: /plan-eng-review
Now let's review the technical architecture...

[plan-eng-review skill executes]

Step 3: Implementation
[Code implementation happens]

Step 4: /review
Let me review your authentication code...

[review skill executes]

Step 5: /qa
Now let's test the authentication feature...

[qa skill executes]

Step 6: /ship
Ready to ship! Let me prepare the release...

[ship skill executes]
```

### Example 2: Quick Code Review

```
User: /review my current branch

AI: I'll review your current branch changes...

[review skill executes automatically]
```

### Example 3: Bug Investigation

```
User: /investigate the login bug users are reporting

AI: I'll systematically investigate the root cause...

[investigate skill executes automatically]
```

## Integration with Other Skills

gstack-skills can work alongside other skills:

- **data-analysis-workflows**: For analyzing product metrics during `/office-hours`
- **sql-queries**: When `/review` or `/investigate` needs database analysis
- **testing skills**: When `/qa` needs specialized testing knowledge

## Skill Dependencies

This skill depends on the following specialized skills, which must be available:

- office-hours
- plan-ceo-review
- plan-eng-review
- plan-design-review
- review
- investigate
- qa
- qa-only
- ship
- document-release
- retro
- codex
- careful
- freeze
- guard

## Error Handling

If a specialized skill is not available:

1. Inform the user which skill is missing
2. Suggest installing the missing skill
3. Offer to proceed with general capabilities as fallback

## Best Practices

1. **Start with `/office-hours`** for new features to validate ideas
2. **Use `/review` before merging** any code
3. **Always `/qa`** before shipping to production
4. **Use `/careful` or `/guard`** for risky operations
5. **Follow the complete workflow** for major features

## Limitations

- Some commands require specific tooling (git, test frameworks)
- `/ship` assumes git-based workflow
- Certain workflows are optimized for web applications

## Learn More

- Original gstack: https://github.com/garrytan/gstack
- Garry Tan's approach: "Boil the Lake" philosophy
- Y Combinator: https://www.ycombinator.com/

---

**Version**: 2.0.0 (OpenClaw/WorkBuddy adaptation)  
**Original Author**: Garry Tan, Y Combinator  
**Adaptation Team**: gstack-openclaw-skills Team
