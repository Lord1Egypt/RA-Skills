# Source Selection

Citing every claim costs 10-16x the tokens of an unsourced answer.
Source the claims where being wrong causes harm and verification is
cheap relative to that harm. State the rest directly or mark them
uncertain.

## When to Source

### REQUIRE Sources

| Claim Type | Example | Why Source |
|------------|---------|------------|
| **Version numbers** | "Python 3.12 added..." | Versions change, easy to verify |
| **Performance claims** | "30% faster than..." | Quantitative claims need evidence |
| **Security recommendations** | "Use bcrypt for..." | Security advice must be current |
| **API specifications** | "The function accepts..." | APIs change between versions |
| **Release dates** | "Released in Q4 2025" | Factual, verifiable |
| **Pricing/limits** | "Free tier allows 1000 requests" | Business terms change |
| **Deprecated features** | "X was removed in version Y" | Breaking changes need verification |

### DO NOT Require Sources

| Claim Type | Example | Why No Source |
|------------|---------|---------------|
| **General concepts** | "Async improves concurrency" | Foundational knowledge |
| **Code examples** | Demonstrative snippets | Illustrative, not factual claims |
| **Opinion/preference** | "Consider using..." | Clearly framed as suggestion |
| **Common knowledge** | "Git tracks changes" | Universal understanding |
| **Logical derivations** | "Therefore, X implies Y" | Reasoning, not factual claim |
| **Syntax** | "Use `def` for functions" | Language documentation is stable |

## Decision Framework

```
Is this a factual claim?
├── No → No source needed
└── Yes → Would being wrong cause harm?
    ├── No (minor inconvenience) → No source needed
    └── Yes → Is verification cost-effective?
        ├── No (>5k tokens for low-value claim) → State uncertainty
        └── Yes → Perform web search, cite source
```

## Citation and Uncertainty Forms

An inline citation, when sourcing is warranted:

```markdown
Python 3.12 introduced `type` statement for type aliases[1].

Sources:
1. [PEP 695](https://peps.python.org/pep-0695/)
```

An uncertainty marker, when sourcing is not cost-effective:

```markdown
The connection pool default is typically 10 connections (verify in your
database driver documentation as this varies by library and version).
```

| Confidence | Action |
|------------|--------|
| High (stable facts) | State directly |
| Medium (may have changed) | Add verification note |
| Low (uncertain) | Source or acknowledge uncertainty |

## Token Cost

| Approach | Token Cost | Use Case |
|----------|------------|----------|
| No sourcing | Baseline | General knowledge |
| Uncertainty marker | +5-10 tokens | Medium confidence |
| Single source | +2-5k tokens | High-value claim |
| Multiple sources | +10-20k tokens | Research tasks |

## Full Sourcing

Accept the high token cost for knowledge corpus entries, security
advisories, compliance or legal claims, and research tasks where the
user expects a thorough investigation. Those go through
`Skill(memory-palace:knowledge-intake)`, which is built for complete
sourcing.
