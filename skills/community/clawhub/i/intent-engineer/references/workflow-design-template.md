# Phase 2: Workflow Design Template

This template will guide you through the process of designing the specific tasks and workflows your agent will perform.

## 1. Task Decomposition

**Question:** How can you break down the high-level goal into smaller, concrete tasks?

**Your Answer:**
```
High-Level Goal: [From Phase 1]

Task 1: [e.g., Receive customer support request]
- Description: [What does this task involve?]
- Inputs: [What data or information is needed?]
- Outputs: [What is the expected output?]
- Owner: [Agent or Human?]

Task 2: [e.g., Analyze customer request and categorize issue]
- Description: [What does this task involve?]
- Inputs: [What data or information is needed?]
- Outputs: [What is the expected output?]
- Owner: [Agent or Human?]

Task 3: [e.g., Generate response and provide solution]
- Description: [What does this task involve?]
- Inputs: [What data or information is needed?]
- Outputs: [What is the expected output?]
- Owner: [Agent or Human?]

Task 4: [e.g., Escalate to human if necessary]
- Description: [What does this task involve?]
- Inputs: [What data or information is needed?]
- Outputs: [What is the expected output?]
- Owner: [Agent or Human?]
```

**Guidance:** Break down your high-level goal into 4-8 concrete tasks. For each task, specify the inputs, outputs, and whether it will be performed by the agent or a human.

---

## 2. Workflow Design

**Question:** How will these tasks flow together? What is the overall workflow?

**Your Answer:**

### Workflow Diagram

```
[Task 1: Receive Request]
         ↓
[Task 2: Analyze & Categorize]
         ↓
    [Decision Point: Can agent handle?]
    /                                \
  YES                                NO
   ↓                                  ↓
[Task 3: Generate Response]    [Task 4: Escalate to Human]
   ↓                                  ↓
[Task 5: Send Response]         [Task 5: Send to Human]
   ↓                                  ↓
[Task 6: Log Interaction]       [Task 6: Log Interaction]
   ↓                                  ↓
   └─────────────────┬────────────────┘
                     ↓
              [Workflow Complete]
```

### Workflow Description

**Workflow Name:** [e.g., Customer Support Request Processing]

**Trigger:** [What triggers this workflow? e.g., Customer submits support request]

**Steps:**

1.  **[Task Name]**: [Brief description]
    - Condition: [If applicable, what condition must be met?]
    - Action: [What does the agent do?]
    - Next Step: [What happens next?]

2.  **[Task Name]**: [Brief description]
    - Condition: [If applicable, what condition must be met?]
    - Action: [What does the agent do?]
    - Next Step: [What happens next?]

3.  **[Decision Point]**: [What decision must be made?]
    - If [Condition A]: Go to [Task Name]
    - If [Condition B]: Go to [Task Name]

4.  **[Task Name]**: [Brief description]
    - Condition: [If applicable, what condition must be met?]
    - Action: [What does the agent do?]
    - Next Step: [What happens next?]

**Completion Condition:** [What indicates the workflow is complete?]

**Guidance:** Use a clear, step-by-step format. Include decision points and branching logic. Make sure each step is concrete and actionable.

---

## 3. Error Handling and Edge Cases

**Question:** What could go wrong? How should the agent handle errors and edge cases?

**Your Answer:**
```
Edge Case 1: [e.g., Customer request is ambiguous]
- Detection: [How will the agent detect this?]
- Action: [What should the agent do?]
- Escalation: [Should this be escalated to a human?]

Edge Case 2: [e.g., Agent lacks required information]
- Detection: [How will the agent detect this?]
- Action: [What should the agent do?]
- Escalation: [Should this be escalated to a human?]

Edge Case 3: [e.g., System error or API failure]
- Detection: [How will the agent detect this?]
- Action: [What should the agent do?]
- Escalation: [Should this be escalated to a human?]
```

**Guidance:** Think about potential errors and edge cases. For each one, describe how the agent should detect and handle it.

---

## 4. Resource Requirements

**Question:** What resources does the agent need to execute this workflow?

**Your Answer:**
```
Data Sources:
- [e.g., Customer database]
- [e.g., Product catalog]
- [e.g., Knowledge base]

APIs:
- [e.g., CRM API]
- [e.g., Email API]
- [e.g., Analytics API]

Tools:
- [e.g., Text analysis tool]
- [e.g., Sentiment analysis tool]
- [e.g., Translation tool]

Templates:
- [e.g., Email response template]
- [e.g., Escalation notification template]
```

**Guidance:** List all the resources the agent will need. These will become the basis for the `scripts/`, `references/`, and `templates/` directories in Phase 3.

---

## 5. Performance Metrics

**Question:** How will you measure the performance of this workflow?

**Your Answer:**
```
Metric 1: [e.g., Average resolution time]
- Target: [e.g., < 24 hours]
- Measurement Method: [How will you measure this?]

Metric 2: [e.g., Customer satisfaction score]
- Target: [e.g., > 90%]
- Measurement Method: [How will you measure this?]

Metric 3: [e.g., Escalation rate]
- Target: [e.g., < 10%]
- Measurement Method: [How will you measure this?]

Metric 4: [e.g., First-contact resolution rate]
- Target: [e.g., > 80%]
- Measurement Method: [How will you measure this?]
```

**Guidance:** Define metrics that capture both efficiency and quality. Include metrics that help you identify when the workflow is not performing as expected.

---

## 6. Next Steps

Once you have completed this template, you are ready to move on to **Phase 3: Build the Context Infrastructure**. Use the resources you identified in Section 4 to guide your implementation.
