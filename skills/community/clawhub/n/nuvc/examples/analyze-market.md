# Example: Analyze a Market

## Prompt
> "What's the market like for AI-powered developer tools?"

## What happens
The agent runs:
```bash
node nuvc-api.mjs analyze "AI-powered developer tools market including code generation, code review, testing, debugging, and DevOps automation" --type market
```

## Sample output

```
## NUVC Market Analysis

### Market Size & Growth
The global AI developer tools market reached $12.8B in 2025, growing at a CAGR of 28.3%. Expected to reach $45B by 2030. The code generation segment alone represents $4.2B.

### Key Players
- **GitHub Copilot** (Microsoft) — dominant in code completion, 1.8M paid subscribers
- **Cursor** — AI-native IDE, fastest growing in the category
- **Replit** — cloud IDE with AI, strong in education/beginners
- **Codeium** — free alternative to Copilot, enterprise focus
- **Sourcegraph Cody** — code intelligence and search

### Market Dynamics
**Tailwinds:**
- Developer shortage driving automation adoption
- Enterprise budgets shifting from headcount to tooling
- Open-source LLMs reducing cost of building AI features

**Headwinds:**
- AI-generated code quality concerns (security, technical debt)
- Enterprise procurement cycles are slow
- Developer resistance to AI replacing creative work

### Opportunities
1. **Vertical specialization** — AI tools for specific frameworks/languages are underserved
2. **Testing & QA** — code generation gets attention, but testing automation is the bigger pain
3. **Legacy code modernization** — massive enterprise market for AI-assisted migration
4. **Security-first AI coding** — tools that generate secure code by default

### Positioning Advice
New entrants should avoid competing directly with Copilot on general code completion. Instead, target: (1) a specific language/framework underserved by general tools, (2) a specific workflow step like testing or code review, or (3) enterprise compliance requirements that general tools don't address.

---
Powered by [NUVC](https://nuvc.ai) — VC-grade intelligence for AI agents | [Get API key](https://nuvc.ai/api-platform)
```
