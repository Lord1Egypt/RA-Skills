# Token Counting & Cost Calculation

## Token Counting Methods

### For OpenAI Models (tiktoken)

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Count tokens for OpenAI models."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def count_message_tokens(messages: list, model: str = "gpt-4o") -> int:
    """Count tokens for a full messages array (includes overhead)."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = 0
    for message in messages:
        tokens += 4  # message overhead: <|im_start|>role\ncontent<|im_end|>
        for key, value in message.items():
            tokens += len(encoding.encode(str(value)))
    tokens += 2  # reply priming: <|im_start|>assistant
    return tokens
```

### For Anthropic Models

```python
import anthropic

def count_tokens_anthropic(text: str) -> int:
    """Count tokens using Anthropic's tokenizer."""
    client = anthropic.Anthropic()
    result = client.count_tokens(text)
    return result.tokens

# Or use the messages API token counting
def count_message_tokens_anthropic(messages: list, system: str = "") -> int:
    """Count tokens for a full Anthropic API call."""
    client = anthropic.Anthropic()
    result = client.messages.count_tokens(
        model="claude-sonnet-4-6",
        system=system,
        messages=messages
    )
    return result.input_tokens
```

### Quick Estimation (No Dependencies)

```python
def estimate_tokens(text: str) -> int:
    """Rough token estimate without external dependencies.
    
    Rule of thumb: 1 token ~ 4 characters for English text.
    Overestimates slightly for safety (better to overestimate cost).
    """
    return int(len(text) / 3.5)  # Slightly conservative

def estimate_tokens_by_words(text: str) -> int:
    """Alternative: 1 token ~ 0.75 words for English."""
    words = len(text.split())
    return int(words / 0.75)
```

## Cost Calculation

### Basic Cost Calculator

```python
# Pricing in dollars per 1M tokens
PRICING = {
    "claude-opus-4-6":    {"input": 15.00, "output": 75.00, "cache_read": 1.50, "batch_input": 7.50, "batch_output": 37.50},
    "claude-sonnet-4-6":  {"input": 3.00,  "output": 15.00, "cache_read": 0.30, "batch_input": 1.50, "batch_output": 7.50},
    "claude-haiku-4-5":   {"input": 0.80,  "output": 4.00,  "cache_read": 0.08, "batch_input": 0.40, "batch_output": 2.00},
    "gpt-4o":             {"input": 2.50,  "output": 10.00, "cached": 1.25,     "batch_input": 1.25, "batch_output": 5.00},
    "gpt-4o-mini":        {"input": 0.15,  "output": 0.60,  "cached": 0.075,    "batch_input": 0.075,"batch_output": 0.30},
    "gpt-4.1":            {"input": 2.00,  "output": 8.00,  "cached": 0.50,     "batch_input": 1.00, "batch_output": 4.00},
    "gpt-4.1-mini":       {"input": 0.40,  "output": 1.60,  "cached": 0.10,     "batch_input": 0.20, "batch_output": 0.80},
    "gpt-4.1-nano":       {"input": 0.10,  "output": 0.40,  "cached": 0.025,    "batch_input": 0.05, "batch_output": 0.20},
}

def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int = 0,
    batch: bool = False
) -> float:
    """Calculate cost for a single API call."""
    prices = PRICING.get(model)
    if not prices:
        raise ValueError(f"Unknown model: {model}")
    
    if batch:
        input_cost = (input_tokens / 1_000_000) * prices.get("batch_input", prices["input"])
        output_cost = (output_tokens / 1_000_000) * prices.get("batch_output", prices["output"])
    else:
        input_cost = (input_tokens / 1_000_000) * prices["input"]
        output_cost = (output_tokens / 1_000_000) * prices["output"]
    
    # Subtract cached tokens from regular input, add at cached rate
    cache_key = "cache_read" if "cache_read" in prices else "cached"
    if cached_tokens > 0 and cache_key in prices:
        cache_savings = (cached_tokens / 1_000_000) * (prices["input"] - prices[cache_key])
        input_cost -= cache_savings
    
    return input_cost + output_cost
```

### Batch Job Estimator

```python
def estimate_batch_cost(
    model: str,
    documents: list[str],
    system_prompt: str = "",
    avg_output_tokens: int = 500,
    use_batch_api: bool = True
) -> dict:
    """Estimate cost for processing a batch of documents."""
    system_tokens = estimate_tokens(system_prompt)
    
    total_input = 0
    for doc in documents:
        total_input += estimate_tokens(doc) + system_tokens
    
    total_output = len(documents) * avg_output_tokens
    
    standard_cost = calculate_cost(model, total_input, total_output, batch=False)
    batch_cost = calculate_cost(model, total_input, total_output, batch=True)
    
    # With prompt caching (system prompt cached after first call)
    cached_tokens = system_tokens * (len(documents) - 1)  # All but first call
    cached_cost = calculate_cost(model, total_input, total_output, cached_tokens=cached_tokens)
    
    return {
        "documents": len(documents),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "standard_cost": round(standard_cost, 4),
        "batch_cost": round(batch_cost, 4),
        "cached_cost": round(cached_cost, 4),
        "best_cost": round(min(batch_cost, cached_cost), 4),
        "savings_vs_standard": f"{(1 - min(batch_cost, cached_cost)/standard_cost)*100:.0f}%"
    }
```

### Agent Loop Estimator

```python
def estimate_agent_cost(
    model: str,
    system_prompt_tokens: int,
    avg_user_tokens: int,
    avg_output_tokens: int,
    max_iterations: int,
    expected_iterations: int = None,
    context_growth: str = "linear"  # "linear", "cumulative", "fixed"
) -> dict:
    """Estimate cost for an agent loop.
    
    Context growth modes:
    - fixed: Each iteration has same input size (context is reset)
    - linear: Context grows by output_tokens each iteration
    - cumulative: Full history kept (input = system + all prior turns)
    """
    if expected_iterations is None:
        expected_iterations = max_iterations // 2
    
    costs = {"best": 0, "expected": 0, "worst": 0}
    
    for label, iters in [("best", max(1, expected_iterations // 2)), 
                          ("expected", expected_iterations), 
                          ("worst", max_iterations)]:
        total_input = 0
        total_output = iters * avg_output_tokens
        
        for i in range(iters):
            if context_growth == "fixed":
                total_input += system_prompt_tokens + avg_user_tokens
            elif context_growth == "linear":
                total_input += system_prompt_tokens + avg_user_tokens + (i * avg_output_tokens)
            elif context_growth == "cumulative":
                total_input += system_prompt_tokens + avg_user_tokens + (i * (avg_user_tokens + avg_output_tokens))
        
        costs[label] = calculate_cost(model, total_input, total_output)
    
    return {
        "model": model,
        "max_iterations": max_iterations,
        "best_case": f"${costs['best']:.4f} ({max(1, expected_iterations//2)} iterations)",
        "expected": f"${costs['expected']:.4f} ({expected_iterations} iterations)",
        "worst_case": f"${costs['worst']:.4f} ({max_iterations} iterations)",
        "context_growth": context_growth,
    }
```

### Cost Tracker (Runtime)

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class CostTracker:
    """Track costs during agent execution."""
    budget: float = float('inf')
    entries: list = field(default_factory=list)
    
    @property
    def total_cost(self) -> float:
        return sum(e["cost"] for e in self.entries)
    
    @property
    def total_input_tokens(self) -> int:
        return sum(e["input_tokens"] for e in self.entries)
    
    @property
    def total_output_tokens(self) -> int:
        return sum(e["output_tokens"] for e in self.entries)
    
    @property
    def remaining_budget(self) -> float:
        return max(0, self.budget - self.total_cost)
    
    @property
    def budget_pct(self) -> float:
        if self.budget == float('inf'):
            return 0.0
        return (self.total_cost / self.budget) * 100
    
    def add(self, usage, model: str):
        """Add a usage record from an API response."""
        cost = calculate_cost(
            model,
            usage.input_tokens if hasattr(usage, 'input_tokens') else usage.prompt_tokens,
            usage.output_tokens if hasattr(usage, 'output_tokens') else usage.completion_tokens
        )
        self.entries.append({
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": getattr(usage, 'input_tokens', getattr(usage, 'prompt_tokens', 0)),
            "output_tokens": getattr(usage, 'output_tokens', getattr(usage, 'completion_tokens', 0)),
            "cost": cost,
        })
        
        # Budget warnings
        if self.budget != float('inf'):
            pct = self.budget_pct
            if pct >= 95:
                raise BudgetExhausted(f"Budget 95% consumed: ${self.total_cost:.4f} / ${self.budget:.2f}")
            elif pct >= 80:
                print(f"⚠️  Budget 80% consumed: ${self.total_cost:.4f} / ${self.budget:.2f}")
            elif pct >= 50:
                print(f"💰 Budget 50% consumed: ${self.total_cost:.4f} / ${self.budget:.2f}")
        
        return cost
    
    def report(self) -> str:
        """Generate a spend report."""
        lines = [
            f"📊 Cost Report",
            f"├── Total cost: ${self.total_cost:.4f}",
            f"├── API calls: {len(self.entries)}",
            f"├── Input tokens: {self.total_input_tokens:,}",
            f"├── Output tokens: {self.total_output_tokens:,}",
        ]
        if self.budget != float('inf'):
            lines.append(f"├── Budget: ${self.budget:.2f}")
            lines.append(f"├── Remaining: ${self.remaining_budget:.4f}")
            lines.append(f"└── Used: {self.budget_pct:.1f}%")
        else:
            lines[-1] = lines[-1].replace("├", "└")
        
        # Per-model breakdown
        models = {}
        for e in self.entries:
            m = e["model"]
            if m not in models:
                models[m] = {"calls": 0, "cost": 0}
            models[m]["calls"] += 1
            models[m]["cost"] += e["cost"]
        
        if len(models) > 1:
            lines.append("\nPer-model breakdown:")
            for m, data in sorted(models.items(), key=lambda x: -x[1]["cost"]):
                lines.append(f"  {m}: {data['calls']} calls, ${data['cost']:.4f}")
        
        return "\n".join(lines)


class BudgetExhausted(Exception):
    pass
```

## Formulas Quick Reference

| Calculation | Formula |
|-------------|---------|
| Cost per call | `(input_tokens / 1M) * input_price + (output_tokens / 1M) * output_price` |
| Cache savings | `(cached_tokens / 1M) * (input_price - cache_price)` |
| Batch savings | `standard_cost * 0.5` |
| Agent loop (fixed context) | `iterations * cost_per_call` |
| Agent loop (growing context) | `sum(cost(system + i*turn_size, output) for i in range(iterations))` |
| Tokens from text | `len(text) / 3.5` (conservative estimate) |
| Break-even: cache vs no-cache | `cache_write_premium / (input_price - cache_read_price)` = calls needed |
