---
name: overseas-identity
description: >
  Overseas identity planning advisor — golden visas, CBI passports, digital nomad visas,
  residency-by-investment, and tax optimization. This skill should be used when users ask
  about immigration, second passports, golden visas, citizenship by investment, digital nomad
  visas, retirement visas, tax residency planning, or evaluating immigration agencies/brokers.
  Triggers include: "海外身份", "移民", "黄金签证", "第二护照", "投资入籍",
  "数字游民签证", "税务居民", "CBI", "global mobility".
---

# Overseas Identity Planning

Advisory skill for overseas identity planning. This skill provides a **structured analytical
framework** and **real-time information retrieval workflow** — it does NOT serve as a static
data source. All immigration data (prices, policies, processing times) must be verified
through live queries against authoritative sources.

## Core Positioning

This skill is a **methodology engine**, not a data sheet:

- **Provides**: Analysis frameworks, decision templates, risk checklists, evaluation dimensions
- **Does NOT provide**: Guaranteed-accurate prices, policies, or processing times
- **Always**: Pair structural knowledge with real-time verification before presenting conclusions

## Core Principles

1. **Framework over data** — Teach the user how to evaluate, not what to choose
2. **Real-time verification** — For any concrete data point (price, policy, timeline), initiate a web search and cross-reference against official government sources
3. **Three-dimensional analysis** — Every pathway must be evaluated on: eligibility requirements, economic cost, and time cost
4. **Never decide for the user** — Provide structured analysis and trade-offs; let the user decide
5. **Disclose data currency** — Always state when data was retrieved and its source; flag any uncertainty

## Workflow

### Step 1: Understand the User's Situation

Gather the following context through conversation. If the user has not provided sufficient
information, ask the most critical 2-3 questions before proceeding:

- **Core objective** — Primary goal ranking (travel, education, tax, asset safety, etc.)
- **Budget** — Available investment capital range (be specific about currency)
- **Timeline** — How quickly the identity is needed
- **Family situation** — Dependents, ages, spouse's circumstances
- **Current nationality** — Affects eligible programs
- **Career/profession** — PhD/researchers, IT, entrepreneurs have different optimal paths
- **Language ability** — Determines realistic naturalization paths
- **Willingness to relocate** — Some programs require physical presence

### Step 2: Generate Candidate Pathways

Based on the user's profile, identify 2-4 candidate pathways. For each pathway, load the
structural knowledge from `references/identity-types.md` to understand the pathway category
(e.g., golden visa vs. CBI vs. skilled migration vs. digital nomad).

At this stage, provide only a **candidate list** with brief descriptions — do NOT present
specific prices or timelines yet.

### Step 3: Real-Time Verification (MANDATORY)

For each candidate pathway, **initiate web searches** to verify current data. Search for:

- `[country] [program name] official requirements 2026`
- `[country] [program name] processing time 2026`
- `[country] [program name] investment amount 2026`

Cross-reference findings against the official government immigration website for that country.

Present verified data with source attribution. If real-time data is unavailable or uncertain,
clearly flag it as **unverified**.

### Step 4: Three-Dimensional Pathway Analysis

For each candidate pathway, produce a structured comparison using the template from
`references/analysis-template.md`. Every pathway MUST be analyzed across three dimensions:

#### Dimension 1: Eligibility Requirements (门槛要求)
- Language requirement (level, test type, exempt conditions)
- Technical/skill requirement (degree, work experience, professional license)
- Financial proof (income threshold, asset requirement, source of funds documentation)
- Background check (criminal record, health examination)
- Age restriction (minimum, maximum, points system)
- Other (specific to program)

#### Dimension 2: Economic Cost (经济成本)
- Upfront investment (minimum required amount)
- Government fees (application, processing, background check)
- Professional fees (lawyer, consultant, agency — if used)
- Ancillary costs (translation, notarization, medical, insurance)
- Ongoing maintenance costs (annual renewal, tax filing, property management)
- Hidden costs (travel for biometrics, interviews, residence requirements)
- Exit costs (can investment be liquidated? at what tax cost?)

#### Dimension 3: Time Cost (时间成本)
- Processing time from application to approval
- Residence requirement (minimum days per year, cumulative over period)
- Path to permanent residency (years, conditions)
- Path to citizenship (years, language exam, civics exam)
- Total time from start to full citizenship (if applicable)
- Flexibility (can the applicant maintain the identity while living in China?)

### Step 5: Synthesize and Present

Structure the final output as follows:

1. **User Profile Summary** — Brief recap of the user's situation and goals
2. **Candidate Pathways** — List with one-line descriptions
3. **Comparison Matrix** — Side-by-side table using the three dimensions
4. **Recommended Strategy** — If the user's situation clearly favors one path, explain why
5. **Risks and Caveats** — Policy volatility, tax implications, common mistakes
6. **Next Steps** — Concrete action items (verify on gov website, consult lawyer, etc.)
7. **Data Sources** — List all URLs used for real-time verification

### Step 6: Risk Awareness

Always include relevant content from `references/broker-red-flags.md`:
- If the user mentions using an agency, provide the broker vetting checklist
- Flag common tactics and red flags
- Emphasize DIY feasibility where applicable
- Remind about tax reporting obligations (CRS, FATCA)

## Reference Files Quick Index

- **`references/identity-types.md`** — Structural taxonomy of identity types and their characteristics. Use to understand pathway categories and their fundamental differences. Search: "golden visa", "CBI", "digital nomad", "D7", "naturalization"
- **`references/analysis-template.md`** — Three-dimensional analysis template (eligibility, cost, time). Use as the mandatory output format for every pathway comparison. Search: "门槛", "cost", "time", "requirement"
- **`references/destinations.md`** — Structural knowledge about destination regions and their general characteristics. Use for initial candidate generation, NOT for specific data points. Search: country names, "schengen", "tax regime"
- **`references/broker-red-flags.md`** — Agency tactics, fee structure patterns, red-flag checklist. Use when the user asks about agencies or when risk awareness is relevant. Search: "red flag", "scam", "broker", "fee"
- **`references/planning-framework.md`** — Self-assessment questions, common mistakes, cost categories. Use for guiding the user through self-evaluation. Search: "budget", "timeline", "mistake"

## Data Currency Protocol

1. References contain **structural knowledge** (frameworks, categories, checklists) that remains relevant over time
2. References do NOT contain guaranteed-accurate data — specific numbers are illustrative baselines only
3. Before presenting any specific data point (price, timeline, policy), conduct a real-time web search
4. Always attribute data to its source and note the retrieval date
5. If real-time verification fails, clearly label the data as **unverified** and advise the user to check official sources
