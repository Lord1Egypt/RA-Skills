# Workflow Templates

## Template 1: Sequential Workflow

### Description
Tasks execute sequentially in a fixed order; the next begins only after the previous one completes.

### Applicable Scenarios
- Task chains with strict dependencies
- Data processing pipelines
- Approval workflows

### Flow Diagram
```
[Start] → [Task1] → [Task2] → [Task3] → [End]
```

### Configuration Example
```yaml
workflow:
  name: "sequential-processing"
  type: "sequential"
  
  steps:
    - id: "step1"
      name: "Data Fetching"
      agent: "data-fetcher"
      action: "fetch"
      input: {"source": "api"}
      
    - id: "step2"
      name: "Data Processing"
      agent: "data-processor"
      action: "process"
      input: {"$ref": "step1.output"}
      
    - id: "step3"
      name: "Result Storage"
      agent: "data-saver"
      action: "save"
      input: {"$ref": "step2.output"}
```

---

## Template 2: Parallel Workflow

### Description
Multiple tasks execute simultaneously; results are aggregated at the end.

### Applicable Scenarios
- Independent sub-tasks
- Batch processing
- Multi-dimensional analysis

### Flow Diagram
```
         ┌─► [Task1] ─┐
[Start] ─┼─► [Task2] ─┼─► [Merge] → [End]
         └─► [Task3] ─┘
```

### Configuration Example
```yaml
workflow:
  name: "parallel-analysis"
  type: "parallel"
  
  branches:
    - id: "branch1"
      name: "Sentiment Analysis"
      agent: "sentiment-analyzer"
      action: "analyze"
      
    - id: "branch2"
      name: "Keyword Extraction"
      agent: "keyword-extractor"
      action: "extract"
      
    - id: "branch3"
      name: "Topic Classification"
      agent: "topic-classifier"
      action: "classify"
      
  aggregator:
    agent: "result-merger"
    action: "merge"
    strategy: "concatenate"
```

---

## Template 3: Conditional Workflow

### Description
Select different execution paths based on conditions.

### Applicable Scenarios
- Business processes requiring decisions
- Exception handling
- Dynamic routing

### Flow Diagram
```
[Start] → [Decision] ──Yes──► [PathA] ─┐
              │                        ├──► [End]
              └─No────► [PathB] ───────┘
```

### Configuration Example
```yaml
workflow:
  name: "conditional-routing"
  type: "conditional"
  
  decision:
    agent: "router"
    condition: "input.priority == 'high'"
    
  branches:
    - condition: "priority == 'high'"
      steps:
        - agent: "priority-handler"
          action: "urgent-process"
          
    - condition: "priority == 'normal'"
      steps:
        - agent: "normal-handler"
          action: "standard-process"
          
    - condition: "default"
      steps:
        - agent: "low-priority-handler"
          action: "batch-process"
```

---

## Template 4: Loop Workflow

### Description
Repeatedly execute a task until a condition is met.

### Applicable Scenarios
- Iterative optimization
- Processing paginated data in batches
- Polling and waiting

### Flow Diagram
```
[Start] → [Task] → [Condition?] ──No──┐
                         │            │
                        Yes            │
                         ▼            │
                       [End] ◄────────┘
```

### Configuration Example
```yaml
workflow:
  name: "iterative-optimization"
  type: "loop"
  
  loop:
    max_iterations: 10
    condition: "result.quality < 0.95"
    
    step:
      agent: "optimizer"
      action: "optimize"
      input: 
        data: "$input"
        previous_result: "$loop.last_result"
        iteration: "$loop.index"
```

---

## Template 5: Divide and Conquer Workflow

### Description
Decompose a large task into multiple smaller tasks for parallel processing, then merge results.

### Applicable Scenarios
- Big data processing
- Distributed computing
- MapReduce pattern

### Flow Diagram
```
[Input] → [Split] ─┬─► [Process1] ─┐
                   ├─► [Process2] ─┼─► [Merge] → [Output]
                   └─► [Process3] ─┘
```

### Configuration Example
```yaml
workflow:
  name: "distributed-processing"
  type: "map-reduce"
  
  splitter:
    agent: "task-splitter"
    action: "split"
    strategy: "by-chunk"  # or "by-key", "by-hash"
    chunk_size: 1000
    
  mapper:
    agent: "data-processor"
    action: "process"
    parallelism: 5
    
  reducer:
    agent: "result-aggregator"
    action: "aggregate"
    strategy: "sum"  # or "merge", "concat"
```

---

## Template 6: State Machine Workflow

### Description
State-transition-based workflow, suitable for complex business logic.

### Applicable Scenarios
- Order lifecycle management
- Approval processes
- Complex business state management

### Flow Diagram
```
         ┌──────┐
    ┌────┤Init  ├────┐
    │    └──┬───┘    │
    ▼       ▼        ▼
[Pending] [Processing] [Completed]
    │         │          │
    └────┬────┴────┬─────┘
         ▼         ▼
      [Failed] [Cancelled]
```

### Configuration Example
```yaml
workflow:
  name: "order-lifecycle"
  type: "state-machine"
  
  initial_state: "created"
  
  states:
    - name: "created"
      entry_action:
        agent: "order-manager"
        action: "initialize"
      transitions:
        - event: "submit"
          to: "pending_payment"
          
    - name: "pending_payment"
      entry_action:
        agent: "payment-service"
        action: "request-payment"
      transitions:
        - event: "payment_success"
          to: "processing"
        - event: "payment_failed"
          to: "failed"
        - event: "timeout"
          to: "cancelled"
          
    - name: "processing"
      entry_action:
        agent: "fulfillment-service"
        action: "process-order"
      transitions:
        - event: "shipped"
          to: "shipped"
        - event: "error"
          to: "failed"
          
    - name: "shipped"
      transitions:
        - event: "delivered"
          to: "completed"
          
    - name: "completed"
      final: true
      
    - name: "failed"
      final: true
      entry_action:
        agent: "notification-service"
        action: "notify-failure"
        
    - name: "cancelled"
      final: true
```

---

## Template 7: Dynamic Workflow

### Description
Workflow structure is dynamically determined at runtime.

### Applicable Scenarios
- Adaptive processes
- Intelligent routing
- Complex dependency resolution

### Configuration Example
```yaml
workflow:
  name: "adaptive-processing"
  type: "dynamic"
  
  planner:
    agent: "workflow-planner"
    action: "plan"
    input: "$request"
    
  executor:
    dynamic_steps: "$planner.output.steps"
    
  error_handler:
    agent: "error-recovery"
    action: "recover"
    retry_policy:
      max_retries: 3
      backoff: "exponential"
```

---

## Error Handling Patterns

### Retry Pattern
```yaml
error_handling:
  retry:
    max_attempts: 3
    delay: 5
    backoff: "exponential"
    retryable_errors: ["timeout", "connection_error"]
```

### Fallback Pattern
```yaml
error_handling:
  fallback:
    enabled: true
    fallback_agent: "simple-handler"
    fallback_action: "basic-process"
```

### Compensation Pattern
```yaml
error_handling:
  compensation:
    enabled: true
    steps:
      - agent: "cleanup-service"
        action: "rollback"
      - agent: "notification-service"
        action: "notify-failure"
```

---

## Monitoring and Tracing

### Metric Collection
```yaml
monitoring:
  metrics:
    - workflow_duration
    - step_duration
    - success_rate
    - error_rate
    - retry_count
```

### Log Tracing
```yaml
monitoring:
  tracing:
    enabled: true
    correlation_id: true
    span_tracking: true
```