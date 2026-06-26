# Integration Patterns: Composing Skills into Workflows

## Overview

Integration patterns describe how multiple skills can be composed together to create complex workflows. This guide covers the most common patterns and how to implement them using the orchestrator.

## Pattern 1: Sequential Composition

**Description:** Skills execute one after another, with the output of one skill becoming the input to the next.

**Use Case:** Support ticket processing pipeline: intake → triage → sentiment analysis → response generation.

**Diagram:**
```
Skill A → Skill B → Skill C → Skill D
```

**Implementation:**
```json
{
  "pattern": "sequential",
  "steps": [
    {
      "step": 1,
      "skill": "support-intake",
      "inputs": { "raw_ticket": "{{input}}" }
    },
    {
      "step": 2,
      "skill": "support-triage",
      "inputs": { "ticket": "{{steps[1].outputs.ticket}}" },
      "depends_on": [1]
    },
    {
      "step": 3,
      "skill": "sentiment-analysis",
      "inputs": { "ticket": "{{steps[1].outputs.ticket}}" },
      "depends_on": [1]
    },
    {
      "step": 4,
      "skill": "response-generator",
      "inputs": {
        "triage": "{{steps[2].outputs.triage_result}}",
        "sentiment": "{{steps[3].outputs.sentiment_response}}"
      },
      "depends_on": [2, 3]
    }
  ]
}
```

**Advantages:**
- Simple to understand and debug
- Clear data flow
- Easy to add logging between steps

**Disadvantages:**
- Can be slow if steps take a long time
- Entire pipeline fails if any step fails

## Pattern 2: Parallel Composition

**Description:** Multiple skills execute simultaneously, with results combined afterward.

**Use Case:** Analyzing a ticket from multiple perspectives (sentiment, intent, urgency) in parallel.

**Diagram:**
```
        ┌─→ Skill A ─┐
Input ─┤─→ Skill B ─┼─→ Combine Results
        └─→ Skill C ─┘
```

**Implementation:**
```json
{
  "pattern": "parallel",
  "steps": [
    {
      "step": 1,
      "skill": "support-intake",
      "inputs": { "raw_ticket": "{{input}}" }
    },
    {
      "step": 2,
      "skill": "sentiment-analysis",
      "inputs": { "ticket": "{{steps[1].outputs.ticket}}" },
      "parallel_group": 1
    },
    {
      "step": 3,
      "skill": "urgency-detector",
      "inputs": { "ticket": "{{steps[1].outputs.ticket}}" },
      "parallel_group": 1
    },
    {
      "step": 4,
      "skill": "intent-classifier",
      "inputs": { "ticket": "{{steps[1].outputs.ticket}}" },
      "parallel_group": 1
    },
    {
      "step": 5,
      "skill": "response-generator",
      "inputs": {
        "sentiment": "{{steps[2].outputs.sentiment_response}}",
        "urgency": "{{steps[3].outputs.urgency_result}}",
        "intent": "{{steps[4].outputs.intent_result}}"
      },
      "depends_on": [2, 3, 4]
    }
  ]
}
```

**Advantages:**
- Faster overall execution time
- Better resource utilization
- More resilient (one failure doesn't block others)

**Disadvantages:**
- More complex to implement
- Harder to debug
- Requires careful handling of race conditions

## Pattern 3: Conditional Composition

**Description:** The next skill to execute depends on the output of the previous skill.

**Use Case:** Route support tickets to different handlers based on triage classification.

**Diagram:**
```
          ┌─→ Auto-Response (if simple)
Triage ──┤─→ Escalate (if complex)
          └─→ Queue (if waiting info)
```

**Implementation:**
```json
{
  "pattern": "conditional",
  "steps": [
    {
      "step": 1,
      "skill": "support-triage",
      "inputs": { "ticket": "{{input}}" }
    },
    {
      "step": 2,
      "skill": "response-generator",
      "inputs": { "triage": "{{steps[1].outputs.triage_result}}" },
      "condition": "steps[1].outputs.triage_result.action == 'auto_respond'",
      "depends_on": [1]
    },
    {
      "step": 3,
      "skill": "escalation-manager",
      "inputs": { "triage": "{{steps[1].outputs.triage_result}}" },
      "condition": "steps[1].outputs.triage_result.action == 'escalate'",
      "depends_on": [1]
    },
    {
      "step": 4,
      "skill": "queue-manager",
      "inputs": { "triage": "{{steps[1].outputs.triage_result}}" },
      "condition": "steps[1].outputs.triage_result.action == 'queue'",
      "depends_on": [1]
    }
  ]
}
```

**Advantages:**
- Efficient (only executes necessary steps)
- Flexible routing
- Reduces unnecessary processing

**Disadvantages:**
- More complex logic
- Harder to test all branches
- Requires clear condition definitions

## Pattern 4: Fan-Out/Fan-In

**Description:** One skill produces multiple outputs that are consumed by multiple downstream skills, then results are aggregated.

**Use Case:** A ticket generates multiple analysis tasks that are all needed for the final response.

**Diagram:**
```
        ┌─→ Sentiment Analysis ─┐
Ticket ─┤─→ Intent Analysis ────┼─→ Aggregate ─→ Response
        └─→ Urgency Analysis ───┘
```

**Implementation:**
```json
{
  "pattern": "fan_out_fan_in",
  "steps": [
    {
      "step": 1,
      "skill": "support-intake",
      "inputs": { "raw_ticket": "{{input}}" }
    },
    {
      "step": 2,
      "skill": "sentiment-analysis",
      "inputs": { "ticket": "{{steps[1].outputs.ticket}}" },
      "parallel_group": 1
    },
    {
      "step": 3,
      "skill": "intent-classifier",
      "inputs": { "ticket": "{{steps[1].outputs.ticket}}" },
      "parallel_group": 1
    },
    {
      "step": 4,
      "skill": "urgency-detector",
      "inputs": { "ticket": "{{steps[1].outputs.ticket}}" },
      "parallel_group": 1
    },
    {
      "step": 5,
      "skill": "aggregator",
      "inputs": {
        "sentiment": "{{steps[2].outputs.sentiment_response}}",
        "intent": "{{steps[3].outputs.intent_result}}",
        "urgency": "{{steps[4].outputs.urgency_result}}"
      },
      "depends_on": [2, 3, 4]
    },
    {
      "step": 6,
      "skill": "response-generator",
      "inputs": { "analysis": "{{steps[5].outputs.aggregated_analysis}}" },
      "depends_on": [5]
    }
  ]
}
```

**Advantages:**
- Parallelizes independent analysis
- Comprehensive analysis of input
- Clear aggregation point

**Disadvantages:**
- Complex to implement
- Requires aggregator skill
- Harder to debug

## Pattern 5: Recursive/Iterative Composition

**Description:** A skill is executed repeatedly until a condition is met.

**Use Case:** Refining a customer response through multiple iterations based on feedback.

**Diagram:**
```
Input → Skill A → Check Condition
                       ↓
                   (condition met?)
                   /          \
                 YES           NO
                  ↓             ↓
              Output      Skill A (again)
```

**Implementation:**
```json
{
  "pattern": "iterative",
  "steps": [
    {
      "step": 1,
      "skill": "response-generator",
      "inputs": { "ticket": "{{input}}" },
      "iteration": 1
    },
    {
      "step": 2,
      "skill": "response-validator",
      "inputs": { "response": "{{steps[1].outputs.generated_response}}" },
      "depends_on": [1]
    },
    {
      "step": 3,
      "skill": "response-generator",
      "inputs": { "ticket": "{{input}}", "feedback": "{{steps[2].outputs.feedback}}" },
      "condition": "steps[2].outputs.is_valid == false && iteration < 3",
      "iteration": 2,
      "depends_on": [2]
    }
  ],
  "max_iterations": 3,
  "termination_condition": "steps[N].outputs.is_valid == true"
}
```

**Advantages:**
- Refines results iteratively
- Handles complex problems
- Can improve quality

**Disadvantages:**
- Slower execution
- Risk of infinite loops
- Harder to predict cost

## Pattern 6: Branching with Merge

**Description:** Multiple independent workflows execute in parallel, then results are merged.

**Use Case:** Processing different aspects of a customer request in parallel (support, billing, technical) then merging results.

**Diagram:**
```
        ┌─→ Support Branch ──┐
Input ─┤─→ Billing Branch ───┼─→ Merge ─→ Output
        └─→ Technical Branch ┘
```

**Implementation:**
```json
{
  "pattern": "branching_merge",
  "branches": [
    {
      "name": "support_branch",
      "steps": [
        {
          "step": 1,
          "skill": "support-classifier",
          "inputs": { "ticket": "{{input}}" }
        },
        {
          "step": 2,
          "skill": "support-handler",
          "inputs": { "classification": "{{steps[1].outputs}}" },
          "depends_on": [1]
        }
      ]
    },
    {
      "name": "billing_branch",
      "steps": [
        {
          "step": 1,
          "skill": "billing-classifier",
          "inputs": { "ticket": "{{input}}" }
        },
        {
          "step": 2,
          "skill": "billing-handler",
          "inputs": { "classification": "{{steps[1].outputs}}" },
          "depends_on": [1]
        }
      ]
    }
  ],
  "merge": {
    "step": "final",
    "skill": "result-merger",
    "inputs": {
      "support_result": "{{branches[0].steps[2].outputs}}",
      "billing_result": "{{branches[1].steps[2].outputs}}"
    }
  }
}
```

**Advantages:**
- Handles complex multi-faceted problems
- Parallelizes independent workflows
- Clear separation of concerns

**Disadvantages:**
- Very complex to implement
- Requires careful merge logic
- Difficult to debug

## Best Practices

### 1. Keep Patterns Simple

Start with sequential composition and only add complexity when necessary. Each additional pattern increases cognitive load and maintenance burden.

### 2. Define Clear Data Contracts

Before composing skills, ensure all data contracts are clearly defined. This prevents data mismatches and makes debugging easier.

### 3. Implement Error Handling

For each skill in the composition, define what happens if it fails. Options include: retry, escalate, use fallback, or abort.

### 4. Monitor and Log

Log the execution of each step, including inputs, outputs, execution time, and any errors. This is critical for debugging and optimization.

### 5. Test Compositions

Test each composition pattern with various inputs, including edge cases and error scenarios. Use integration tests to verify the entire workflow.

### 6. Document Patterns

For each composition pattern you use, document the pattern type, the skills involved, the data flow, and any special considerations.

## Composition Configuration Example

Here's a complete example of a composition configuration file:

```json
{
  "name": "Support Ticket Processing Pipeline",
  "version": "1.0.0",
  "description": "End-to-end processing of support tickets",
  "pattern": "sequential_with_parallel",
  "error_handling": "escalate_on_failure",
  "steps": [
    {
      "step": 1,
      "skill": "support-intake",
      "timeout_ms": 5000,
      "retry": { "max_attempts": 3, "backoff": "exponential" }
    },
    {
      "step": 2,
      "skill": "support-triage",
      "depends_on": [1],
      "timeout_ms": 10000
    },
    {
      "step": 3,
      "skill": "sentiment-analysis",
      "depends_on": [1],
      "parallel_group": 1,
      "timeout_ms": 15000
    },
    {
      "step": 4,
      "skill": "response-generator",
      "depends_on": [2, 3],
      "condition": "steps[2].outputs.action == 'auto_respond'",
      "timeout_ms": 20000
    },
    {
      "step": 5,
      "skill": "escalation-manager",
      "depends_on": [2, 3],
      "condition": "steps[2].outputs.action == 'escalate'",
      "timeout_ms": 5000
    }
  ],
  "monitoring": {
    "log_level": "info",
    "track_metrics": true,
    "alert_on_failure": true
  }
}
```

This configuration defines a sophisticated workflow that combines sequential and parallel execution, includes error handling and timeouts, and enables comprehensive monitoring.
