# Content Templates for Image Breaker

Reusable templates for common document types.

## Medical/Lab Document

```markdown
# {Document Title}

## Overview
Brief description of what this test/document measures and why it matters.

## Key Measurements

| Metric | Reference Range | Interpretation |
|--------|----------------|----------------|
| Metric 1 | <100 units | Low risk |
| Metric 2 | 100-200 units | Moderate risk |
| Metric 3 | >200 units | High risk |

## Detailed Breakdown

### What It Measures
- Bullet point explanation
- Another point

### Why It Matters
Explanation of clinical significance.

### How to Read Results
Step-by-step interpretation guide.

## Comparison to Standard Tests

| Standard Test | NMR/Advanced Test | Key Difference |
|---------------|-------------------|----------------|
| LDL-C | LDL-P | Particle count vs cholesterol |

## Action Items

**If results show X:**
- Action 1
- Action 2

**If results show Y:**
- Action 1
- Action 2

## Reference
- **Source:** [URL]
- **Type:** Lab reference / Clinical guideline
- **Extracted:** {date}
```

## Research Paper

```markdown
# {Paper Title}

## Overview
One-paragraph summary of the study.

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Study Details
- **Authors:** Name et al.
- **Published:** Journal, Year
- **Study Type:** RCT / Meta-analysis / Observational
- **Sample Size:** N participants

## Methods
Brief description of methodology.

## Results
Main results with specific numbers/percentages.

## Clinical Implications
What this means for practice/protocols.

## Limitations
- Limitation 1
- Limitation 2

## Reference
- **DOI:** 10.xxxx/xxxxx
- **Source:** [URL]
- **Extracted:** {date}
```

## Protocol/Guide Document

```markdown
# {Protocol Name}

## Overview
What this protocol addresses and who it's for.

## Indications
When to use this protocol:
- Indication 1
- Indication 2

## Protocol Steps

### Phase 1: [Phase Name]
- **Duration:** X weeks
- **Dosing:** X mg/day
- **Frequency:** Daily/Weekly

### Phase 2: [Phase Name]
- **Duration:** X weeks
- **Dosing:** X mg/day
- **Frequency:** Daily/Weekly

## Monitoring
What to track during the protocol:
- Biomarker 1 (frequency)
- Biomarker 2 (frequency)

## Expected Outcomes
What success looks like.

## Safety Considerations
- Contraindication 1
- Side effect to watch for
- When to stop

## Reference
- **Source:** [URL or Author]
- **Type:** Clinical protocol / Treatment guide
- **Extracted:** {date}
```

## Business/Marketing Document

```markdown
# {Document Title}

## Key Message
Main positioning or value proposition.

## Target Audience
Who this is for.

## Core Content

### Section 1
Content...

### Section 2
Content...

## Actionable Insights
What to do with this information:
- Insight 1
- Insight 2

## Quotes/Key Phrases
> "Notable quote from document"

## Reference
- **Source:** [URL]
- **Type:** Marketing material / Business doc
- **Extracted:** {date}
```

## Technical Reference

```markdown
# {System/Tool Name}

## Overview
What this system/tool does.

## Key Components

### Component 1
Description and function.

### Component 2
Description and function.

## Usage Examples

```language
code example 1
```

```language
code example 2
```

## Configuration

| Setting | Value | Purpose |
|---------|-------|---------|
| setting1 | value | explanation |

## Common Issues
- Issue 1: Solution
- Issue 2: Solution

## Reference
- **Source:** [URL]
- **Type:** Technical documentation
- **Extracted:** {date}
```

## General Template Selection Guide

**Use Medical/Lab template for:**
- Bloodwork results
- Lab reference ranges
- Diagnostic criteria
- Medical guidelines

**Use Research Paper template for:**
- Academic studies
- Clinical trials
- Meta-analyses
- Scientific papers

**Use Protocol/Guide template for:**
- Treatment protocols
- Supplement stacks
- Training programs
- Step-by-step procedures

**Use Business/Marketing template for:**
- Copy ideas
- Marketing materials
- Competitor analysis
- Business documents

**Use Technical Reference template for:**
- API documentation
- Software tools
- System architecture
- Configuration guides

## Adaptation Guidelines

1. **Always include Overview** - Reader should know what this is in first paragraph
2. **Use tables for data** - Makes numerical information scannable
3. **Action items when relevant** - Help user know what to do next
4. **Source attribution** - Always include where content came from
5. **Preserve key formatting** - Bold important terms, use headers for hierarchy
