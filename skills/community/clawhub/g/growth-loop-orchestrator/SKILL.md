---
name: growth-loop-orchestrator
description: Orchestrate growth loops across the skill portfolio by connecting usage, feedback, improvement, and adoption into self-reinforcing cycles. Use when designing growth strategies, optimizing skill adoption, creating viral loops, or building sustainable growth mechanisms.
---

# Growth Loop Orchestrator

## Overview

The `growth-loop-orchestrator` skill designs, implements, and optimizes growth loops across the skill portfolio. It connects usage, feedback, improvement, and adoption into self-reinforcing cycles that drive sustainable growth.

## When to Use

- Designing growth strategies for skills
- Creating viral or referral loops
- Optimizing skill adoption funnels
- Building user engagement mechanisms
- Planning portfolio growth initiatives
- Analyzing growth metrics and loops
- Troubleshooting growth stagnation
- Designing network effects

## Core Concepts

### Growth Loop Types

| Type | Mechanism | Example |
|------|-----------|---------|
| `viral` | Users bring new users | Share results, invite others |
| `content` | Usage creates content | Public outputs, templates |
| `network` | More users = more value | Collaborative features |
| `engagement` | Usage drives more usage | Habits, streaks, rewards |
| `feedback` | Usage improves product | Learning from actions |

### Loop Components

Every growth loop has:

1. **Input**: Users, actions, or content entering the loop
2. **Action**: What users do within the loop
3. **Output**: Results that feed back into the loop
4. **Conversion**: How outputs become new inputs
5. **Amplification**: What makes the loop grow

### Loop Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| `cycle_time` | Time for one loop iteration | < 7 days |
| `conversion_rate` | % that complete the loop | > 20% |
| `viral_coefficient` | New users per existing user | > 0.3 |
| `retention` | % who continue looping | > 40% |
| `amplification` | Growth rate per cycle | > 10% |

## Input

Accepts:
- Current growth metrics
- User behavior data
- Skill portfolio information
- Target growth goals
- Loop design parameters

## Output

Produces:
- Growth loop designs
- Orchestration plans
- Metric dashboards
- Optimization recommendations
- A/B test plans

## Workflow

### Designing a Growth Loop

1. **Identify Core Value**
   - What value do users get?
   - What can they share or create?
   - What would others want?

2. **Map User Journey**
   - Entry points
   - Key actions
   - Sharing moments
   - Conversion paths

3. **Design the Loop**
   - Input source
   - Key action
   - Output creation
   - Distribution mechanism
   - Conversion back to input

4. **Add Amplification**
   - Incentives
   - Friction reduction
   - Network effects
   - Social proof

5. **Measure and Optimize**
   - Track loop metrics
   - Identify bottlenecks
   - Test improvements
   - Scale what works

### Analyzing Existing Loops

1. **Map Current State**
   - Identify existing loops
   - Measure current performance
   - Find broken connections

2. **Diagnose Issues**
   - Where do users drop off?
   - What's blocking conversion?
   - Where is friction highest?

3. **Generate Solutions**
   - Fix broken connections
   - Reduce friction
   - Add amplification

4. **Test and Validate**
   - A/B test changes
   - Measure impact
   - Iterate quickly

## Commands

### Design Growth Loop
```bash
./scripts/design-loop.sh --type viral --skill <name> [--output loop-design.md]
```

### Analyze Current Loops
```bash
./scripts/analyze-loops.sh [--skill <name>] [--portfolio]
```

### Optimize Loop Performance
```bash
./scripts/optimize-loop.sh --loop-id <id> [--target metric] [--test]
```

### Track Growth Metrics
```bash
./scripts/track-metrics.sh [--skill <name>] [--dashboard] [--period 30d]
```

### Generate Growth Report
```bash
./scripts/generate-report.sh --type loops|funnel|portfolio [--output report.md]
```

### Simulate Loop
```bash
./scripts/simulate-loop.sh --design <file> [--cycles 10] [--users 1000]
```

## Output Format

### Growth Loop Design
```markdown
# Growth Loop Design: [Name]

## Loop Type: Viral

## Loop Diagram

```
[New User] → [Use Skill] → [Create Output] → [Share] → [New User Sees] → [Try Skill] → [New User]
```

## Components

### Input
- Source: User creates content
- Volume: ~50 outputs/day
- Quality: High (user-generated)

### Action
- What: User shares output
- Where: Social, email, link
- Friction: Medium (requires action)

### Output
- Type: Sharable result
- Format: Image, link, export
- Value: Demonstrates skill capability

### Conversion
- Mechanism: View → Try
- Rate: 15% (target: 25%)
- Time: Within 24 hours

### Amplification
- Social proof: "X people used this"
- Incentive: Free credits for sharing
- Network: Collaborative features

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Cycle Time | 3 days | 1 day |
| Conversion Rate | 15% | 25% |
| Viral Coefficient | 0.2 | 0.5 |
| Retention | 35% | 50% |

## Optimization Plan

### Immediate (This Week)
1. Add one-click sharing
2. Create shareable templates
3. Add social proof badges

### Near-term (This Month)
1. Implement referral rewards
2. Add collaboration features
3. Create public gallery

### Long-term (This Quarter)
1. Build network effects
2. Add team features
3. Create marketplace

## Success Criteria
- Viral coefficient > 0.5
- Cycle time < 24 hours
- 1000 new users/month from loop
```

### Loop Performance Dashboard
```json
{
  "dashboard": "growth-loops",
  "period": "2024-03-01 to 2024-03-31",
  "loops": [
    {
      "id": "viral-share",
      "name": "Viral Sharing Loop",
      "type": "viral",
      "metrics": {
        "cycle_time_hours": 48,
        "conversion_rate": 0.18,
        "viral_coefficient": 0.25,
        "retention_7d": 0.42,
        "amplification": 1.15
      },
      "status": "active",
      "health": "good",
      "bottleneck": "share_rate",
      "recommendation": "Add one-click sharing buttons"
    },
    {
      "id": "content-seo",
      "name": "Content SEO Loop",
      "type": "content",
      "metrics": {
        "cycle_time_days": 30,
        "conversion_rate": 0.05,
        "content_velocity": 12,
        "organic_growth": 1.08
      },
      "status": "active",
      "health": "fair",
      "bottleneck": "content_quality",
      "recommendation": "Improve output shareability"
    }
  ],
  "portfolio_summary": {
    "total_loops": 4,
    "active_loops": 3,
    "avg_viral_coefficient": 0.22,
    "monthly_growth_rate": 0.15
  }
}
```

## Loop Patterns

### Viral Loop Pattern
```
Use → Create → Share → View → Signup → Use
```
**Keys**: Easy sharing, valuable output, low friction signup

### Content Loop Pattern
```
Use → Publish → Index → Search → View → Use
```
**Keys**: SEO-friendly, public by default, discoverable

### Network Loop Pattern
```
Join → Invite → Collaborate → Value ↑ → More Invite
```
**Keys**: Collaboration value, invite incentives, team features

### Engagement Loop Pattern
```
Use → Reward → Habit → Daily Use → Reward
```
**Keys**: Meaningful rewards, streaks, progress

### Feedback Loop Pattern
```
Use → Feedback → Improve → Better Experience → Use
```
**Keys**: Easy feedback, fast iteration, visible improvements

## Quality Rules

- Design loops that add value, not just growth
- Measure full loop, not just parts
- Optimize for sustainable growth
- Test before scaling
- Monitor for gaming/abuse
- Balance growth with quality

## Good Trigger Examples

- "Design a growth loop for this skill"
- "How can we make this skill viral?"
- "Analyze our current growth loops"
- "What's blocking our growth?"
- "Design a referral program"
- "How can we increase user engagement?"
- "Track our growth metrics"
- "Optimize our conversion funnel"
- "Create a network effect"

## Limitations

- Requires usage data for meaningful analysis
- Growth loops take time to validate
- Network effects need critical mass
- Viral loops are hard to predict
- Metrics can be gamed
- Growth without value is unsustainable

## Related Skills

- `learning-evolution` - For iterating on loops
- `insight-tracker` - For capturing growth insights
- `decision-distiller` - For growth strategy decisions
- `skill-market-analyzer` - For market-based growth

## Resources

### scripts/
- `design-loop.sh` - Design new growth loops
- `analyze-loops.sh` - Analyze existing loops
- `optimize-loop.sh` - Optimize loop performance
- `track-metrics.sh` - Track growth metrics
- `simulate-loop.sh` - Simulate loop behavior

### references/
- Growth loop patterns
- Viral mechanics
- Network effect theory
- Engagement design principles
