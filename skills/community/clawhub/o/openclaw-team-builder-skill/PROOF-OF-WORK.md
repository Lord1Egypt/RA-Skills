# Proof of Work — Team Builder Skill

This document demonstrates the Team Builder skill in action, showing the Planner proposing teams for sample tasks that cross roster boundaries.

## Test 1: "Analyze Astronomy Photos for Star Classification"

### Input Task
> Analyze a set of deep-space telescope images. Identify and classify star types by color temperature and luminosity. Generate enhanced images highlighting each classification.

### Planner Output

```
## Team Proposal

### Task
Analyze deep-space telescope images for star classification with enhanced visualization

### Classification
- Domain: Visual Analysis + Research + Creative
- Mode: Sprint
- Estimated effort: 3-5 days

### Proposed Team

| Role | Agent | Roster | Activation Phase |
|------|-------|--------|-----------------|
| Leader | CEO | Core | Phase 1 |
| Scoping | Senior PM | Agency PM | Phase 1 |
| Image Acquisition | Artist | Core | Phase 2 |
| Prompt Engineering | Image Prompt Engineer | Agency Design | Phase 2 |
| Analysis Loop | Research Lab | Research | Phase 2 |
| ML Classification | AI Engineer | Agency Engineering | Phase 2 |
| Data Reporting | Analytics Reporter | Agency Support | Phase 3 |
| QA | Evidence Collector | Agency Testing | Phase 3 |
| Gate | Reality Checker | Agency Testing | Phase 3 |

### Execution Plan
1. Senior PM scopes: define classification categories, image set size, accuracy targets
2. Artist + Image Prompt Engineer process raw telescope images (contrast, filtering)
3. Research Lab runs iterative classification loop:
   - Metric: classification accuracy (% correctly typed stars)
   - In-scope: detection thresholds, color temperature bins, luminosity cutoffs
   - Budget: 5-min analysis pass per configuration
   - Loop: adjust parameters → re-classify → compare accuracy → keep/discard
4. AI Engineer tunes the classification model parameters
5. Artist generates enhanced visualization images with classification overlays
6. Analytics Reporter compiles results into a summary report
7. Evidence Collector validates classifications against known catalogs
8. Reality Checker certifies the final output

### Handoff Chain
Senior PM (scope) → Artist + Image Prompt Engineer (image prep) →
Research Lab + AI Engineer (classification loop) → Artist (enhanced visuals) →
Analytics Reporter (report) → Evidence Collector → Reality Checker

### Cross-Roster Integration Points
- Research Lab (autoresearch methodology) drives the iterative optimization
- Image Prompt Engineer (Agency Design) crafts prompts for Artist (Core) to enhance images
- AI Engineer (Agency Engineering) works alongside Research Lab for model tuning
- Analytics Reporter (Agency Support) formats results from Research Lab experiments
```

### Why This Works
- **Three rosters active**: Core (CEO, Artist), Agency (5 specialists from 4 divisions), Research Lab
- **Cross-pollination**: Research methodology applied to image analysis (not just ML training)
- **Artist + Design pairing**: Image Prompt Engineer structures prompts for Artist's xAI generation
- **Evidence-based QA**: Agency Testing division validates before shipping

---

## Test 2: "Optimize Silver Trading Strategy with Neural Brain"

### Input Task
> The silver futures scalper is showing a 25% win rate. Run an optimization experiment to improve it by tuning RSI thresholds, stop-loss distances, and the neural brain's training parameters.

### Planner Output

```
## Team Proposal

### Task
Optimize silver scalper strategy — improve win rate from 25% baseline

### Classification
- Domain: Trading + Research + AI
- Mode: Sprint
- Estimated effort: 1-2 weeks (continuous experiment loops)

### Proposed Team

| Role | Agent | Roster | Activation Phase |
|------|-------|--------|-----------------|
| Leader | CEO | Core | Phase 1 |
| Market Context | IG | Core | Phase 1 |
| Experiment Loop | Research Lab | Research | Phase 2 |
| Neural Tuning | AI Engineer | Agency Engineering | Phase 2 |
| Performance Test | Performance Benchmarker | Agency Testing | Phase 3 |
| QA | Evidence Collector | Agency Testing | Phase 3 |

### Execution Plan
1. IG provides: current strategy config, trade history, live market data for silver
2. Research Lab establishes baseline: current win rate (25%), P&L, Sharpe ratio
3. Research Lab experiment loop:
   - Metric: win rate (higher is better), secondary: Sharpe ratio
   - In-scope: RSI buy/sell thresholds, stopDistance, limitDistance, size
   - Budget: 5-min backtest per parameter combination
   - Loop: modify one parameter → backtest → compare win rate → keep/discard
4. AI Engineer tunes neural brain parameters in parallel:
   - Adjust preference zone neuron allocation
   - Modify sugar/pain reinforcement magnitudes
   - Test different feature vector compositions
5. Performance Benchmarker validates: execution speed, slippage simulation
6. Evidence Collector verifies: backtest results match live conditions

### Experiment Ledger (expected output)
id          metric  status   description
baseline    25.0    keep     current config — 25% win rate
exp-001     28.5    keep     RSI buy threshold 25→20
exp-002     24.0    discard  RSI sell threshold 75→80
exp-003     31.2    keep     stopDistance 15→12 with RSI 20
exp-004     30.8    discard  limitDistance 25→35 (worse risk-adjusted)
exp-005     33.1    keep     neural brain sugar magnitude 2.0→3.5
exp-006     0.0     crash    batch size 64→256 (OOM on brain)
...

### Risks
- Overfitting to historical data — mitigate with out-of-sample validation
- Live market conditions differ from backtest — staged rollout recommended
- Neural brain changes affect all instruments — isolate silver experiments
```

### Why This Works
- **IG + Research Lab**: Trading specialist provides domain context, Research Lab provides the experiment methodology
- **AI Engineer integration**: Neural brain tuning runs as part of the same optimization loop
- **Measurable outcomes**: Experiment ledger tracks every attempt with keep/discard decisions
- **Safety**: Performance Benchmarker and Evidence Collector validate before live deployment

---

## Test 3: "Build a Portfolio Allocation Dashboard Page" (Micro Mode)

### Input Task
> Add a new "Portfolio" tab to the trading dashboard showing allocation pie charts and rebalancing suggestions.

### Planner Output

```
## Team Proposal

### Task
New Portfolio tab with pie charts and rebalancing

### Classification
- Domain: Engineering + Trading
- Mode: Micro
- Estimated effort: 2-3 days

### Proposed Team

| Role | Agent | Roster | Activation Phase |
|------|-------|--------|-----------------|
| Leader | CEO | Core | Phase 1 |
| Frontend Build | Frontend Developer | Agency Engineering | Phase 2 |
| Data Source | IG | Core | Phase 2 |
| QA | Evidence Collector | Agency Testing | Phase 3 |

### Execution Plan
1. CEO scopes requirements via existing dashboard patterns
2. Frontend Developer builds the Portfolio tab using existing charting libraries
3. IG provides portfolio data (positions, allocations, P&L per instrument)
4. Evidence Collector screenshots desktop/tablet/mobile viewports

### Handoff Chain
CEO (scope) → Frontend Developer (build) + IG (data) → Evidence Collector (validate)
```

### Why This Works
- **Micro mode**: Small team, fast execution, right-sized for the task
- **No over-engineering**: Only 4 agents, no Research Lab needed for a UI feature
- **Existing patterns**: Leverages dashboard's existing tab system and charting

---

## Summary

| Test | Rosters Used | Agents | Mode | Key Cross-Team Integration |
|------|-------------|--------|------|---------------------------|
| Astronomy Photo Analysis | Core + Agency + Research | 9 | Sprint | Research loops on image analysis, Artist + Image Prompt Engineer |
| Silver Strategy Optimization | Core + Agency + Research | 6 | Sprint | IG + Research Lab experiment loop, AI Engineer neural tuning |
| Portfolio Dashboard | Core + Agency | 4 | Micro | Frontend Developer + IG data, Evidence Collector QA |

The Planner correctly:
1. Classified each task's domain
2. Selected the right mode (Micro/Sprint/Full) based on complexity
3. Composed teams from multiple rosters where beneficial
4. Defined clear activation phases and handoff chains
5. Included QA agents (Evidence Collector / Reality Checker) in every proposal
6. Leveraged cross-roster integration (Research + Artist, IG + Research Lab, etc.)
