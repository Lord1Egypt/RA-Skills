# Council of Wisdom - AI Debate System

**Description:** A sophisticated multi-agent debate framework where two expert agents debate opposing viewpoints, managed by a referee, with 9 specialized council members voting on the most compelling argument. Includes automatic cleanup, multi-LLM provider support, and enterprise-grade monitoring, testing, and scalability.

## When to Use This Skill

Use Council of Wisdom when you need:
- Comprehensive analysis from multiple expert perspectives
- Balanced debate on complex topics with opposing viewpoints
- Decision-making with structured voting and reasoning
- Multi-provider AI evaluation (different LLMs per agent)
- Automatic agent lifecycle management (spawn → debate → vote → cleanup)
- Enterprise-grade monitoring, testing, feedback loops

**Common use cases:**
- Strategic decision analysis
- Technical architecture debates
- Product feature prioritization
- Risk assessment and mitigation planning
- Investment or business opportunity evaluation
- Policy or process design decisions

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     QUERY / ADVISE / TROUBLE                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    REFEREE AGENT                            │
│  • Receives query                                           │
│  • Orchestrates debate                                      │
│  • Manages council voting                                   │
│  • Delivers structured outcome                              │
└─────────────┬───────────────────────┬───────────────────────┘
              │                       │
              ▼                       ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│    MASTER DEBATER A     │  │    MASTER DEBATER B     │
│  • Domain expert #1     │  │  • Domain expert #2     │
│  • Persuasive arguments │  │  • Persuasive arguments │
│  • Opposing viewpoint   │  │  • Opposing viewpoint   │
└─────────────────────────┘  └─────────────────────────┘
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              COUNCIL OF 9 EXPERTS                            │
│  • Each is a non-human domain expert                        │
│  • Unique perspective & methodology                        │
│  • Vote on most convincing argument                         │
│  • Provide brief reasoning                                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 REFEREE AGGREGATION                         │
│  • Collects votes (9 total)                                 │
│  • Tally and determine winner                               │
│  • Structure outcome report                                 │
│  • Delete council agents & context                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              STRUCTURED OUTCOME REPORT                       │
│  • Winner declaration                                        │
│  • Vote tally                                                │
│  • Key arguments from each side                              │
│  • Council consensus insights                                │
│  • Actionable recommendations                                │
└─────────────────────────────────────────────────────────────┘
```

## Council of 9 - Expert Specializations

Each council member represents a distinct analytical framework:

1. **Logician** - Formal logic, fallacy detection, deductive reasoning
2. **Empiricist** - Evidence-based, data-driven, statistical analysis
3. **Pragmatist** - Real-world applicability, practical outcomes
4. **Ethicist** - Moral frameworks, stakeholder impact, fairness
5. **Futurist** - Long-term implications, trend analysis, scenarios
6. **Historian** - Precedent analysis, historical patterns, lessons
7. **Systems Thinker** - Holistic view, interconnected effects
8. **Risk Analyst** - Failure modes, mitigation, uncertainty
9. **Synthesizer** - Integration, common ground, hybrid solutions

## Core Components

### 1. Workspace Setup

Each Council of Wisdom instance has its own workspace:

```bash
council-of-wisdom init <project-name>
```

Creates:
```
council-of-wisdom/<project-name>/
├── workspace/
│   ├── strategy.md           # Project-specific strategy
│   ├── monitoring/
│   │   ├── metrics.md        # Key metrics definitions
│   │   ├── cadence.md        # Review cadences (daily/weekly/etc)
│   │   └── dashboard.json    # Metrics dashboard config
│   ├── testing/
│   │   ├── test-cases.md     # Test scenarios
│   │   └── quality-checks.md # Quality criteria
│   ├── feedback/
│   │   ├── feedback-log.md   # User feedback capture
│   │   └── improvement-queue.md
│   ├── prompts/
│   │   ├── referee.md        # Referee agent prompt
│   │   ├── debater-a.md      # Debater A prompt template
│   │   ├── debater-b.md      # Debater B prompt template
│   │   └── council/          # 9 council member prompts
│   │       ├── logician.md
│   │       ├── empiricist.md
│   │       └── ... (all 9)
│   ├── agents/
│   │   ├── referee.json      # Referee agent config
│   │   ├── debater-a.json    # Debater A config
│   │   ├── debater-b.json    # Debater B config
│   │   └── council.json      # Council member configs
│   ├── logs/                 # Debate transcripts, votes
│   └── reports/              # Final outcome reports
├── .github/                  # GitHub repo integration
└── README.md                 # Project documentation
```

### 2. GitHub Repository Integration

Every Council of Wisdom project has its own private GitHub repo:

```bash
# Auto-created during init
git remote add origin git@github.com:<username>/council-<project-name>.git
git branch -M main
git push -u origin main
```

**Features:**
- Private repository (enforced)
- Automated issue tracking for debates
- Wiki for knowledge base
- Actions for automated testing
- Releases for versioned outcomes

### 3. Multi-LLM Provider Support

Council members can use different LLM providers randomly:

```bash
# Enable multi-provider mode
council-of-wisdom config set multi-provider true

# Define available providers
council-of-wisdom config add-provider openai gpt-4
council-of-wisdom config add-provider anthropic claude-3-opus
council-of-wisdom config add-provider google gemini-pro
```

Each council member randomly receives a different provider for each debate, ensuring diverse reasoning patterns.

### 4. Agent Lifecycle Management

**Spawn → Debate → Vote → Cleanup**

```bash
# Full debate cycle
council-of-wisdom debate <topic> \
  --domain <domain> \
  --perspective-a "<perspective A>" \
  --perspective-b "<perspective B>"
```

**Automatic cleanup:**
- Council agents terminated after voting
- Context cleared (memory wiped)
- Logs archived to workspace
- Ready for next query in seconds

### 5. Strategy Framework

Every Council of Wisdom project has a strategy.md with:

**Required fields:**
- **Council Purpose:** What decisions this council makes
- **Domain Expertise:** Areas of specialization
- **Decision Criteria:** How to evaluate arguments
- **Stakeholders:** Who uses the decisions
- **Success Metrics:** What good looks like

Template: `templates/strategy-template.md`

### 6. Monitoring & Metrics

**5-Cadence Operating Rhythm:**

| Cadence | Focus | Metrics | Actions |
|---------|-------|---------|---------|
| **Daily** | Debate quality, agent performance | Vote distribution, argument depth, response time | Quick tuning, prompt adjustments |
| **Weekly** | Decision impact, user feedback | Adoption rate, satisfaction scores, outcome validity | Strategic prompt refinement |
| **Monthly** | Council effectiveness, ROI | Decision accuracy trend, cost efficiency, time-to-decision | Provider optimization, council composition |
| **Quarterly** | Strategic alignment, scalability | Business impact, stakeholder value, expansion readiness | Major upgrades, new domains |
| **Annually** | Vision review, long-term evolution | Year-over-year impact, innovation potential | Architecture evolution, new paradigms |

**Key Metrics Dashboard:**
```json
{
  "debate_metrics": {
    "total_debates": 0,
    "avg_debate_time": 0,
    "vote_distribution": {},
    "argument_quality_score": 0
  },
  "agent_metrics": {
    "council_diversity_index": 0,
    "provider_rotation_efficiency": 0,
    "context_cleanup_success_rate": 0
  },
  "outcome_metrics": {
    "decision_adoption_rate": 0,
    "outcome_validity": 0,
    "stakeholder_satisfaction": 0
  }
}
```

### 7. Testing Framework

**Test Categories:**

1. **Unit Tests** - Individual agent prompts
   ```bash
   council-of-wisdom test unit --agent logician
   ```

2. **Integration Tests** - Full debate flow
   ```bash
   council-of-wisdom test integration --scenario "complex-decision"
   ```

3. **Quality Checks** - Argument quality, logic depth
   ```bash
   council-of-wisdom test quality --topic <topic>
   ```

4. **Performance Tests** - Speed, resource usage
   ```bash
   council-of-wisdom test performance --load 10
   ```

**Test Scenarios:** See `templates/test-scenarios.md`

### 8. Feedback & Optimization Loop

**Feedback Capture:**

```bash
# Add user feedback
council-of-wisdom feedback add \
  --debate-id <id> \
  --rating 1-5 \
  --comment "<feedback>"

# View improvement queue
council-of-wisdom feedback queue
```

**Automated Optimization:**

```bash
# Run optimization cycle
council-of-wisdom optimize \
  --analyze last-7-days \
  --update-prompts \
  --tune-providers
```

**Optimization Targets:**
- Prompt engineering improvements
- Provider selection optimization
- Council composition tuning
- Argument depth maximization
- Decision accuracy enhancement

### 9. Scalability Features

**Horizontal Scaling:**
- Multiple concurrent debates (up to N instances)
- Distributed council member allocation
- Load balancing across providers

**Vertical Scaling:**
- Council expansion (9 → 12 → 15 members)
- Domain specialization layers
- Nested debates (sub-councils for sub-issues)

**Enterprise Features:**
- Rate limiting and quota management
- Priority queues for urgent decisions
- Audit trails and compliance logging
- Multi-tenant support

## Usage

### Initialize a New Council

```bash
council-of-wisdom init strategic-decisions
```

### Conduct a Debate

```bash
council-of-wisdom debate \
  "Should we invest in AI automation or human expertise for customer support?" \
  --domain "customer-support" \
  --perspective-a "AI automation prioritizes efficiency and scalability" \
  --perspective-b "Human expertise prioritizes empathy and complex problem-solving"
```

### View Outcome Report

```bash
council-of-wisdom report <debate-id>
```

### Run Daily Health Check

```bash
council-of-wisdom health-check
```

### Run Optimization Cycle

```bash
council-of-wisdom optimize --period weekly
```

## Examples

### Example 1: Technical Architecture Decision

```bash
council-of-wisdom debate \
  "Should we use microservices or monolithic architecture for our new product?" \
  --domain "software-architecture" \
  --perspective-a "Microservices offer scalability, independent deployment, and team autonomy" \
  --perspective-b "Monolithic architecture offers simplicity, lower operational overhead, and faster initial development"
```

**Outcome Report Structure:**
```markdown
# Debate Outcome Report

## Winner: Monolithic Architecture (6/9 votes)

## Vote Tally
- **Monolithic Architecture:** 6 votes (Logician, Empiricist, Pragmatist, Systems Thinker, Risk Analyst, Synthesizer)
- **Microservices:** 3 votes (Futurist, Ethicist, Historian)

## Key Arguments - Monolithic
1. **Development Velocity:** 3-5x faster initial time-to-market
2. **Operational Complexity:** 80% lower infrastructure overhead
3. **Team Coordination:** Reduced communication overhead by 60%

## Key Arguments - Microservices
1. **Future Scalability:** Better suited for 10x+ growth scenarios
2. **Technology Diversity:** Enables polyglot persistence and best-tool selection
3. **Fault Isolation:** Service failures don't cascade across entire system

## Council Insights
- **Consensus:** For a new product with uncertain market fit, monolithic architecture is strategically superior
- **Caveat:** If product validates and scales beyond 1M users, consider gradual migration to microservices
- **Risk Mitigation:** Design monolithic with modular boundaries to ease future migration

## Recommendation
**Adopt Monolithic Architecture for V1 with Modular Design**

### Action Plan
1. Build monolithic with clear module boundaries
2. Implement feature flags for gradual rollout
3. Monitor performance and architecture fit metrics
4. Re-evaluate architecture decision after 6 months or 500K users
```

### Example 2: Marketing Strategy Debate

```bash
council-of-wisdom debate \
  "Should we focus on SEO-driven content marketing or paid advertising for customer acquisition?" \
  --domain "marketing" \
  --perspective-a "SEO content builds sustainable, compounding organic traffic and authority" \
  --perspective-b "Paid ads provide immediate, scalable, and predictable customer acquisition"
```

## Advanced Features

### Custom Council Composition

Override default council with custom experts:

```bash
council-of-wisdom config set-council \
  --members "industry-expert,financial-analyst,legal-counsel,product-strategist,customer-advocate,technical-lead,operations-manager,brand-architect,growth-hacker"
```

### Nested Debates

For complex decisions, run sub-debates:

```bash
council-of-wisdom debate --nested \
  --main-topic "Should we enter the enterprise market?" \
  --sub-topic-1 "Pricing strategy" \
  --sub-topic-2 "Feature requirements" \
  --sub-topic-3 "Support infrastructure"
```

### Weighted Voting

Assign different weights to council members:

```bash
council-of-wisdom config set-weights \
  --councilmember logician:2 \
  --councilmember empiricist:2 \
  --councilmember others:1
```

### Debate Replay & Analysis

```bash
# Reconstruct and analyze past debates
council-of-wisdom replay <debate-id> --analyze

# Extract patterns across debates
council-of-wisdom analyze-patterns --period last-30-days
```

## Monitoring Dashboards

### Real-Time Monitoring

```bash
council-of-wisdom monitor --live
```

Shows:
- Active debates
- Agent status
- Provider health
- Queue depth

### Historical Analysis

```bash
council-of-wisdom analytics --period quarterly
```

Generates:
- Decision trend analysis
- Argument quality evolution
- Provider performance comparison
- Council member effectiveness

## Integration Points

### GitHub Integration

```bash
# Create issue for debate
council-of-wisdom debate --create-issue

# Push outcome report to repo
council-of-wisdom report <id> --push

# Sync with GitHub wiki
council-of-wisdom sync-wiki
```

### API Access (for automation)

```bash
# Start a debate via API
curl -X POST https://api.council-of-wisdom.com/v1/debates \
  -H "Authorization: Bearer <token>" \
  -d '{"topic": "...", "domain": "..."}'

# Get outcome
curl https://api.council-of-wisdom.com/v1/debates/<id>/outcome
```

### Webhooks

Configure webhooks for:
- Debate completion
- Vote finalization
- Outcome report generation
- Optimization alerts

## Troubleshooting

### Agent Stuck During Debate

**Symptom:** Debate not progressing beyond initial arguments

**Solutions:**
1. Check provider status: `council-of-wisdom status providers`
2. Review agent logs: `council-of-wisdom logs <agent-id>`
3. Restart debate: `council-of-wisdom debate --restart <debate-id>`

### Council Vote Deadlock (4-4 tie with 1 abstain)

**Symptom:** No clear winner

**Resolution:**
1. Automatic tiebreaker: Referee casts deciding vote
2. Extended debate: Add 2 rounds of rebuttal
3. Both perspectives documented as "equally valid with tradeoffs"

### Context Cleanup Failure

**Symptom:** Council agents not terminating

**Solutions:**
1. Force cleanup: `council-of-wisdom cleanup --force`
2. Check process status: `council-of-wisdom status agents`
3. Review logs: `council-of-wisdom logs cleanup`

### Poor Argument Quality

**Symptom:** Arguments are shallow or generic

**Optimization:**
```bash
# Run quality analysis
council-of-wisdom analyze-quality <debate-id>

# Auto-optimize prompts
council-of-wisdom optimize --focus prompt-engineering

# Test new prompts
council-of-wisdom test prompts --scenario quality-test
```

## Best Practices

1. **Define strategy first:** Always have a clear strategy.md before debating
2. **Iterate on prompts:** Regularly optimize based on feedback
3. **Monitor metrics:** Review metrics at each cadence
4. **Capture feedback:** Always collect user feedback on outcomes
5. **Archive outcomes:** Store all reports in GitHub for traceability
6. **Rotate providers:** Use multi-provider to avoid bias
7. **Regular cleanup:** Ensure context cleanup is working
8. **Version control:** Commit all prompt changes to git
9. **Test before deploy:** Run integration tests for new prompts
10. **Scale gradually:** Start with 9 council, expand only when needed

## Template Files

| Template | Purpose |
|----------|---------|
| `templates/strategy-template.md` | Strategy document for new councils |
| `templates/referee-prompt.md` | Referee agent prompt template |
| `templates/debater-prompt.md` | Debater agent prompt template |
| `templates/council-prompts/` | 9 council member prompts |
| `templates/test-scenarios.md` | Test cases for quality assurance |
| `templates/metrics-template.md` | Metrics definitions and targets |

## Reference Materials

| Topic | Reference |
|-------|-----------|
| Prompt Engineering Best Practices | [references/prompt-engineering.md](references/prompt-engineering.md) |
| Multi-Agent Orchestration | [references/agent-orchestration.md](references/agent-orchestration.md) |
| LLM Provider Comparison | [references/provider-comparison.md](references/provider-comparison.md) |
| Argumentation Theory | [references/argumentation-theory.md](references/argumentation-theory.md) |
| Monitoring Architecture | [references/monitoring-design.md](references/monitoring-design.md) |

---

*Council of Wisdom: Structured debate, collective intelligence, actionable decisions.*
