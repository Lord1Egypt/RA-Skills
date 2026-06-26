# Autoresearch: BMW Skill Comprehensive Optimization

## Objective
Optimize the Brand Marketing Workflow (BMW) skill across 5 dimensions:
- A) Content generation quality
- B) Competitor analysis accuracy  
- C) Execution speed
- D) End-to-end stability
- E) Authorization/human-collaboration efficiency

## Metrics

### Primary (Composite Score)
- **BMW-Score**: Weighted composite of all dimensions (0-100, higher is better)
  - Content Quality: 25%
  - Competitor Accuracy: 25%
  - Speed: 20%
  - Stability: 20%
  - Auth Efficiency: 10%

### Secondary (Individual tracking)
- **Content-Score**: Content quality rating (0-10)
- **Competitor-Hit**: Competitor signal hit rate (0-1)
- **Duration**: Total execution time (seconds, lower is better)
- **Success-Rate**: End-to-end success rate (0-1)
- **Auth-Steps**: Number of human assist triggers (lower is better)

## How to Run
`./autoresearch.sh` — runs 3 demo scenarios (fashion, tech, local) and outputs composite score.

## Files in Scope
- `scripts/content_producer.py` — LLM content generation logic, prompts
- `scripts/competitor_fetcher.py` — Signal fetching logic
- `scripts/competitor_ai_analyzer.py` — Signal analysis logic
- `scripts/workflow_orchestrator.py` — Workflow coordination
- `scripts/authorization_manager.py` — Auth gate logic
- `run.py` — Entry point, demo scenarios
- `templates/` — Content templates

## Off Limits
- `scripts/gateway_client.py` — External API client (don't break interface)
- `scripts/oc_llm_client.py` — LLM client wrapper
- `scripts/smoke_test.py` — Test file (read-only reference)
- `scripts/integration_test.py` — Test file (read-only reference)

## Constraints
- All 26 integration tests must pass (regression check)
- No new external dependencies
- Keep backward compatibility with existing input/output schemas
- Browser compliance rules must remain intact
- Auth gates must still trigger on sensitive actions

## What's Been Tried

### Baseline (Initial Run)
- Fashion demo: Content-Score=7.2, Competitor-Hit=0.65, Duration=45s, Success-Rate=1.0, Auth-Steps=1
- Tech demo: Content-Score=7.0, Competitor-Hit=0.60, Duration=42s, Success-Rate=1.0, Auth-Steps=1
- Local demo: Content-Score=7.5, Competitor-Hit=0.70, Duration=48s, Success-Rate=1.0, Auth-Steps=1
- **Composite BMW-Score: 72.3**

### Round 1 - Stability + Content Quality (Committed)
**Changes:**
- [x] Added exponential backoff retry (3 attempts) to `_call_llm_with_fallback()` in content_producer.py
- [x] Enhanced prompt with explicit quality requirements and brand alignment checks
- [x] Added `_filter_noise()` to remove ads/nav/footer noise from competitor signals
- [x] Added `_score_relevance()` to grade signal quality (0-1)
- [x] Added `_filter_and_score()` wrapper to competitor_fetcher.py
- [x] Integrated relevance_score into fetch output for downstream filtering

**Expected Impact:**
- Stability: Higher (retry mechanism for transient failures)
- Content Quality: Higher (better prompts + explicit quality requirements)
- Competitor Accuracy: Higher (noise filtering + relevance scoring)

**BMW-Score: 63.00** (stub mode baseline, actual improvement pending live test)

### Round 2 - Speed Optimization (Committed)
**Changes:**
- [x] Added `concurrent.futures.ThreadPoolExecutor` to run content_producer and competitor_fetcher in parallel
- [x] Implemented `run_content_producer()` and `run_competitor_fetcher()` as parallel tasks
- [x] Used `as_completed()` to handle results as they finish
- [x] Added error handling for parallel task failures (graceful fallback)

**Expected Impact:**
- Speed: Higher (parallel execution reduces total latency by ~30-50% when both LLM and competitor API calls are needed)
- Stability: No regression (fallback mechanism in place)

### Round 3 - Ideas (Next)
- [ ] Cache competitor signals with TTL to reduce redundant fetches
- [ ] Fine-tune auth gate thresholds based on historical success rates
- [ ] Add content diversity scoring to avoid repetitive outputs
- [ ] Optimize competitor_ai_analyzer.py prompt for better insight extraction
