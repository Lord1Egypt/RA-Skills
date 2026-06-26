# Dangerous Cost Patterns & Safe Alternatives

## Critical Risk Patterns

### 1. Unbounded While Loop + API Call

**Dangerous:**
```python
while not task.is_done():
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=task.get_messages()
    )
    task.update(response)
```

**Why it's dangerous:** If `task.is_done()` never returns True (bug, edge case, ambiguous stopping criteria), this runs forever. At ~$0.03/call, 1000 iterations = $30. Overnight with fast calls = thousands of dollars.

**Safe alternative:**
```python
MAX_ITERATIONS = 20
COST_LIMIT = 5.00  # dollars

cost_tracker = CostTracker()

for iteration in range(MAX_ITERATIONS):
    if task.is_done():
        break
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=task.get_messages(),
        max_tokens=2000  # Cap output tokens
    )
    task.update(response)
    
    cost_tracker.add(response.usage)
    if cost_tracker.total_cost > COST_LIMIT:
        logger.error(f"Cost limit reached: ${cost_tracker.total_cost:.2f}")
        break
else:
    logger.warning(f"Max iterations ({MAX_ITERATIONS}) reached without completion")
```

---

### 2. Recursive Agent Delegation Without Depth Limit

**Dangerous:**
```python
class Agent:
    def solve(self, problem):
        if self.can_solve(problem):
            return self.direct_solve(problem)
        
        sub_problems = self.decompose(problem)
        return [Agent().solve(sub) for sub in sub_problems]  # Recursive!
```

**Why it's dangerous:** Each decomposition can create N sub-agents, each of which may decompose further. Depth 5 with branching factor 3 = 3^5 = 243 API calls. Depth 10 = 59,049 calls.

**Safe alternative:**
```python
class Agent:
    def __init__(self, max_depth: int = 3, budget: float = 10.0):
        self.max_depth = max_depth
        self.budget = budget
        self.spent = 0.0
    
    def solve(self, problem, depth: int = 0):
        if depth >= self.max_depth:
            logger.warning(f"Max depth {self.max_depth} reached, solving directly")
            return self.direct_solve(problem)
        
        if self.spent >= self.budget:
            raise BudgetExhausted(f"Spent ${self.spent:.2f} of ${self.budget:.2f}")
        
        if self.can_solve(problem):
            result = self.direct_solve(problem)
            self.spent += result.cost
            return result
        
        sub_problems = self.decompose(problem)[:3]  # Cap branching factor
        results = []
        for sub in sub_problems:
            result = self.solve(sub, depth + 1)
            self.spent += result.cost
            results.append(result)
        return results
```

---

### 3. Retry Without Max Attempts

**Dangerous:**
```python
def call_api(prompt):
    while True:
        try:
            return client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
        except APIError:
            time.sleep(1)  # Retry forever
```

**Why it's dangerous:** If the API returns a non-transient error (invalid request, content policy violation), this retries forever. Each retry costs money for calls that get partially processed.

**Safe alternative:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    retry=retry_if_exception_type((APIConnectionError, RateLimitError)),
    reraise=True
)
def call_api(prompt):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
```

---

### 4. Multi-Agent Without Shared Budget

**Dangerous:**
```python
# Each agent has no spending awareness
researcher = Agent(model="gpt-4o")
writer = Agent(model="gpt-4o")
reviewer = Agent(model="gpt-4o")

# No coordination on spend
research = researcher.run(topic)      # Unknown cost
draft = writer.run(research)          # Unknown cost
review = reviewer.run(draft)          # Unknown cost
# Total: 3 agents x unknown iterations = ???
```

**Safe alternative:**
```python
class BudgetPool:
    def __init__(self, total: float):
        self.total = total
        self.spent = 0.0
        self._lock = threading.Lock()
    
    def request(self, amount: float) -> bool:
        with self._lock:
            if self.spent + amount > self.total:
                return False
            self.spent += amount
            return True

pool = BudgetPool(total=10.00)

researcher = Agent(model="gpt-4o", budget_pool=pool, allocation=0.4)  # 40%
writer = Agent(model="gpt-4o", budget_pool=pool, allocation=0.4)      # 40%
reviewer = Agent(model="claude-haiku-4-5", budget_pool=pool, allocation=0.2)  # 20%
```

---

## High Risk Patterns

### 5. Batch Processing Without Checkpointing

**Dangerous:**
```python
results = []
for doc in ten_thousand_documents:
    result = process(doc)  # API call
    results.append(result)
# If it fails at doc 9999, you've wasted 9998 calls
save(results)
```

**Safe:** Checkpoint after each item or batch (see optimization.md section 7).

---

### 6. Missing max_tokens

**Dangerous:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
    # No max_tokens — model may generate up to context limit
)
```

**Why:** Without `max_tokens`, the model can generate its full context window of output. For GPT-4o, that's 16K output tokens = ~$0.16 per call just for output. For tasks that need 100 tokens of output, you're potentially paying 160x more.

**Safe:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=1000  # Set appropriate limit for the task
)
```

---

### 7. Embedding Entire Codebases Naively

**Dangerous:**
```python
# Embed every file, including binaries, node_modules, etc.
for file in Path(".").rglob("*"):
    text = file.read_text()
    embed(text)
```

**Safe:**
```python
INCLUDE_EXTENSIONS = {".py", ".js", ".ts", ".md", ".txt"}
EXCLUDE_DIRS = {"node_modules", ".git", "vendor", "__pycache__", "dist"}

for file in Path(".").rglob("*"):
    if file.suffix not in INCLUDE_EXTENSIONS:
        continue
    if any(excluded in file.parts for excluded in EXCLUDE_DIRS):
        continue
    
    text = file.read_text()
    # Chunk large files to avoid wasting embedding context
    for chunk in chunk_text(text, max_tokens=500):
        embed(chunk)
```

---

## Medium Risk Patterns

### 8. Re-processing on Every Run

**Pattern:** Running the same analysis on unchanged files.

**Fix:** Hash inputs and cache outputs:
```python
import hashlib

def cached_process(content: str, cache_dir: Path = Path(".cache")):
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
    cache_file = cache_dir / f"{content_hash}.json"
    
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    
    result = expensive_api_call(content)
    cache_dir.mkdir(exist_ok=True)
    cache_file.write_text(json.dumps(result))
    return result
```

### 9. Using Chat Models for Embedding

**Pattern:** Using `gpt-4o` to generate text representations instead of embedding models.

**Fix:** Use dedicated embedding models:
- `text-embedding-3-small`: $0.02/1M tokens (vs $2.50/1M for GPT-4o input alone)
- That's a 125x cost difference

### 10. Full Context on Every Turn

**Pattern:** Sending the complete conversation history on every API call in a chatbot.

**Fix:** Implement sliding window or summarization:
```python
def prepare_messages(history: list, max_turns: int = 10):
    if len(history) <= max_turns:
        return history
    
    # Summarize older turns
    old = history[:-max_turns]
    summary = summarize(old)  # One cheap call
    recent = history[-max_turns:]
    
    return [{"role": "system", "content": f"Previous context: {summary}"}] + recent
```

## Pattern Detection Regex Cheat Sheet

Quick patterns for scanning codebases:

| Pattern | Regex |
|---------|-------|
| While-loop API call | `while.*:\s*\n.*\.(create\|generate\|complete\|chat)` |
| Missing max_tokens | `\.create\((?!.*max_tokens).*\)` |
| No retry limit | `while True:.*except.*:\s*\n\s*(continue\|pass\|time\.sleep)` |
| Recursive agent | `def (run\|solve\|execute).*\n.*self\.(run\|solve\|execute)` |
| Unbounded batch | `for.*in.*:\s*\n.*\.(create\|generate)(?!.*checkpoint)` |
