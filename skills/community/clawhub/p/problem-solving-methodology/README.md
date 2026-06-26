# Problem Solving

Structured problem diagnosis and resolution methodology for OpenClaw.

## Features

- 🔍 **Systematic Diagnosis**: Map call chains and trace data flow end-to-end
- 🎯 **Root Cause Analysis**: Three-question framework to confirm true causes
- 🛠️ **Solution Design**: Compare multiple approaches on effectiveness, risk, and reversibility
- ✅ **Rigorous Verification**: Multi-level testing including regression checks
- 📝 **Post-Mortem Reviews**: Extract learnings to prevent recurrence

## When to Use

**Use this skill when:**
- Problem cause is unclear and requires investigation
- A previous fix attempt failed
- Issue involves multiple components interacting
- Modifications carry risk or side effects
- You'd need to say "可能是..." to explain the cause

**Skip for:**
- Obvious one-liner fixes
- Clear error messages with known solutions
- User says "just fix it" for simple issues

## The Process

1. **Define**: Turn vague symptoms into precise problem statements
2. **Diagnose**: Trace data flow, verify each step, confirm root cause
3. **Design**: Generate and compare at least 2 solution candidates
4. **Execute**: Change one variable at a time with rollback plan
5. **Verify**: Reproduce trigger, check regressions, test durability
6. **Review**: Extract lessons for future prevention

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install problem-solving
```

### Manual Installation

Clone to `~/.openclaw/skills/problem-solving`

## Usage

The skill activates automatically when appropriate. You can also explicitly request it:

```
帮我分析一下这个问题
Use structured problem solving for this issue
Let's diagnose this systematically
```

## Anti-Patterns to Avoid

- **Guess-and-fix**: See symptom → change immediately
- **Surface fix**: Change bad value without asking why
- **Multi-change**: Change 3 things at once
- **Premature victory**: "Should be fixed" without verification

## License

MIT License - see [LICENSE](LICENSE) file
