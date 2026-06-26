# LLM Provider Forensics Checklist

## Goal
Produce an evidence-based judgment about what likely sits behind a claimed LLM endpoint.

## Final classifications
- `high-confidence-focused-or-genuine-route`
- `medium-confidence-likely-routed-or-wrapped`
- `high-confidence-multi-model-aggregation-pool`
- `low-confidence-or-unusable`

## Universal procedure
1. Record declared facts:
   - provider name
   - base URL
   - claimed model id
   - stated protocol family
   - how credentials are supplied
2. Probe catalog/list endpoints when available.
3. Probe inference endpoints for the likely protocol family.
4. Run 3–5 repeated short requests.
5. Run strict output tests.
6. Extract metadata and token-accounting hints.
7. Summarize uncertainty explicitly.

## Strong multi-model-pool signals
Treat these as strong pool evidence when multiple appear together:
- catalog returns many unrelated model families
- mixed vendor namespaces in model IDs
- mixed `owned_by` values
- endpoint family support is patchy or surprising
- claimed model id appears as a thin alias among thousands of unrelated IDs

## Focused-route signals
These increase confidence that the route is more focused or genuine:
- narrow catalog or no catalog but clean single-family behavior
- endpoint family support matches expected vendor behavior
- consistent response shape across repeated runs
- stable latency and high success rate
- coherent token/reasoning metadata

## Capability probes
Use these probes because they expose format control more than raw intelligence:
- exact literal: `Reply with exactly OK`
- digits only: `Compute 17*19 and answer with digits only.`
- exact JSON only: `Return valid minified JSON only: {"animal":"cat","n":3}`
- exact multiline format: `Return exactly three lines and nothing else:\nA\nB\nC`

## Stability requirement
Repeat one minimal prompt 5 times and record:
- success rate
- min/avg/max latency
- schema consistency
- output consistency

## Output sections
1. Declared facts
2. Catalog evidence
3. Protocol evidence
4. Stability evidence
5. Behavior evidence
6. Judgment
7. Operational recommendation
