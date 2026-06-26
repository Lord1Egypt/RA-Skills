# Cost Optimization Strategies

## 1. Model Tiering

Use the right model for the right task — not every call needs the most capable model.

### Tier Mapping

| Task Type | Recommended Tier | Examples |
|-----------|-----------------|----------|
| Classification / Routing | Nano/Mini | Sentiment analysis, intent detection, spam filtering |
| Extraction / Parsing | Mini/Small | JSON extraction, entity recognition, data normalization |
| Summarization | Small/Medium | Document summaries, changelog generation |
| Code generation | Medium/Large | Feature implementation, bug fixes |
| Complex reasoning | Large/Flagship | Architecture decisions, multi-step analysis |
| Creative writing | Medium/Large | Marketing copy, documentation |

### Implementation Pattern

```python
MODEL_TIERS = {
    "classify": "gpt-4.1-nano",      # $0.14/1M in+out
    "extract": "gpt-4.1-mini",       # $0.56/1M in+out
    "summarize": "claude-haiku-4-5",  # $1.20/1M in+out
    "generate": "claude-sonnet-4-6",  # $4.50/1M in+out
    "reason": "claude-opus-4-6",      # $22.50/1M in+out
}

def get_model(task_type: str) -> str:
    return MODEL_TIERS.get(task_type, MODEL_TIERS["generate"])
```

**Savings:** 10-100x reduction for simple tasks vs using a flagship model everywhere.

## 2. Prompt Caching

Reuse cached prefixes to slash input costs on repeated system prompts.

### Anthropic Prompt Caching

```python
# Mark the system prompt for caching — 90% savings on cache hits
response = client.messages.create(
    model="claude-sonnet-4-6",
    system=[{
        "type": "text",
        "text": long_system_prompt,
        "cache_control": {"type": "ephemeral"}  # Cache for 5 minutes
    }],
    messages=messages
)
```

- Cache write: 25% premium on first call
- Cache read: 90% discount on subsequent calls
- Break-even: 2nd call onwards
- TTL: 5 minutes (refreshed on each hit)

### OpenAI Automatic Caching

OpenAI caches automatically for prompts sharing a prefix >= 1024 tokens. No code changes needed — just structure prompts with static content first.

**Savings:** Up to 90% on input tokens for repetitive workflows.

## 3. Batch APIs

For non-urgent workloads, batch APIs offer 50% discounts.

### When to Use Batch

- Processing datasets (summarize 1000 documents)
- Generating embeddings for a corpus
- Running evaluations / benchmarks
- Nightly report generation
- Any workload where 24-hour latency is acceptable

### Anthropic Batch API

```python
batch = client.messages.batches.create(
    requests=[
        {"custom_id": f"doc-{i}", "params": {
            "model": "claude-sonnet-4-6",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": doc}]
        }}
        for i, doc in enumerate(documents)
    ]
)
# Poll for results — up to 24 hours
```

### OpenAI Batch API

```python
# Upload a JSONL file, then create a batch
batch = client.batches.create(
    input_file_id=file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)
```

**Savings:** 50% on both input and output tokens.

## 4. Token Reduction Techniques

### Compress System Prompts

```
# Before (verbose): ~150 tokens
You are a helpful assistant that helps users with their questions.
Please be concise and accurate in your responses. Always provide
sources when possible. If you don't know the answer, say so.

# After (tight): ~40 tokens
Concise, accurate answers. Cite sources. Say "I don't know" when unsure.
```

### Use Structured Output

```python
# Force JSON schema — prevents verbose explanations
response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_schema", "json_schema": schema},
    messages=messages
)
```

### Trim Context Window

- Only include relevant conversation history, not the entire thread
- Summarize earlier turns instead of including verbatim
- Remove successfully processed items from context

**Savings:** 20-60% token reduction depending on prompt bloat.

## 5. Early Termination

Stop agent loops when the answer is good enough.

```python
for i in range(max_iterations):
    result = agent.step()
    
    # Confidence-based early exit
    if result.confidence > 0.95:
        break
    
    # Diminishing returns detection
    if i > 3 and result.improvement < 0.01:
        logger.info(f"Converged at iteration {i}")
        break
    
    # Cost-based exit
    if cost_tracker.total > budget * 0.9:
        logger.warning("Approaching budget limit, stopping")
        break
```

**Savings:** 30-80% for tasks that converge early (most do).

## 6. Rate Limiting & Self-Throttling

Prevent burst spending with self-imposed limits.

```python
import time
from collections import deque

class CostThrottle:
    def __init__(self, max_cost_per_minute: float = 1.0):
        self.max_cost_per_minute = max_cost_per_minute
        self.recent_costs = deque()  # (timestamp, cost)
    
    def check(self, estimated_cost: float) -> bool:
        now = time.time()
        # Remove entries older than 1 minute
        while self.recent_costs and self.recent_costs[0][0] < now - 60:
            self.recent_costs.popleft()
        
        current_spend = sum(c for _, c in self.recent_costs)
        if current_spend + estimated_cost > self.max_cost_per_minute:
            wait = 60 - (now - self.recent_costs[0][0])
            raise CostLimitExceeded(f"Rate limit: wait {wait:.0f}s")
        
        return True
    
    def record(self, cost: float):
        self.recent_costs.append((time.time(), cost))
```

## 7. Checkpointing

Save intermediate results to avoid re-processing on failure.

```python
import json
from pathlib import Path

CHECKPOINT_FILE = Path("processing_checkpoint.json")

def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text())
    return {"processed": [], "results": {}, "total_cost": 0.0}

def save_checkpoint(state: dict):
    CHECKPOINT_FILE.write_text(json.dumps(state, indent=2))

# Resume from where we left off
state = load_checkpoint()
for doc_id in all_documents:
    if doc_id in state["processed"]:
        continue  # Skip already-processed docs
    
    result = process_document(doc_id)
    state["processed"].append(doc_id)
    state["results"][doc_id] = result
    state["total_cost"] += result.cost
    save_checkpoint(state)  # Save after each doc
```

**Savings:** 100% savings on re-processing after failures.

## 8. Cost-Aware Agent Architecture

Design multi-agent systems with cost as a first-class constraint.

```python
class BudgetedAgent:
    def __init__(self, name: str, budget: float, model_tier: str = "generate"):
        self.name = name
        self.budget = budget
        self.spent = 0.0
        self.model = MODEL_TIERS[model_tier]
    
    def can_afford(self, estimated_cost: float) -> bool:
        return self.spent + estimated_cost <= self.budget
    
    def execute(self, task):
        estimated = self.estimate_cost(task)
        if not self.can_afford(estimated):
            return self.fallback(task)  # Use cheaper model or skip
        
        result = self.call_api(task)
        self.spent += result.actual_cost
        return result
    
    def delegate(self, sub_agent, task, sub_budget: float):
        """Pass a portion of remaining budget to sub-agent."""
        sub_agent.budget = min(sub_budget, self.budget - self.spent)
        result = sub_agent.execute(task)
        self.spent += sub_agent.spent  # Roll up costs
        return result
```

## Strategy Selection Guide

| Situation | Best Strategy | Expected Savings |
|-----------|--------------|-----------------|
| Same prompt, many inputs | Prompt caching | 60-90% on input |
| Large batch, no urgency | Batch API | 50% |
| Simple tasks using GPT-4 | Model tiering | 80-99% |
| Agent loops | Early termination + caps | 30-80% |
| Long conversations | Context trimming | 20-50% |
| Unreliable pipeline | Checkpointing | Varies (prevents waste) |
| Burst workloads | Rate limiting | Prevents budget blowups |
