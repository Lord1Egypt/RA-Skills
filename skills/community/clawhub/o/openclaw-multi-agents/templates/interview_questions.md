# Interview Question Bank

**Use Case:** User Interviews during Planning Phase  
**Goal:** Deeply understand user workflows, pain points, and collaboration needs  
**Interview Date:** {{interview_date}}  
**Interviewee:** {{user_name}}

---

## Interview Guide

### Interview Principles

1. **Open-ended Questions** - Encourage detailed descriptions, avoid yes/no questions.
2. **Dig Deeper** - Use the "5 Whys" for each answer to uncover root causes.
3. **Specific Cases** - Ask the user to share specific scenarios and examples.
4. **No Preconceived Answers** - Avoid leading questions.
5. **Record Original Words** - Preserves the user's original way of expression.

### Recording Format

Each question's record should contain:
- **Summary of User's Answer** (Key points)
- **Specific Cases/Examples** (Specific examples)
- **Pain Point Marking** (Pain points identified)
- **Follow-up Items** (Follow-up items)
- **Importance Rating** (1-5, 5=Most critical)

---

## Core Question Set

### Category A: Workflow

#### Q1: Please describe your current complete process for completing [Task Type]
**Goal:** Understand the full picture of the current workflow  
**Expected Answer:** Step breakdown, involved tools, time allocation

**Follow-up Prompts:**
- In this process, which steps are completed manually?
- Roughly how long does each step take?
- Which tools or systems are involved?
- Are there any waiting or blocking stages in the process?

**Recording Template:**
```
Process Steps:
1. {{step_1}} - Duration: {{time_1}} - Tool: {{tool_1}}
2. {{step_2}} - Duration: {{time_2}} - Tool: {{tool_2}}
3. {{step_3}} - Duration: {{time_3}} - Tool: {{tool_3}}

Bottleneck Identification: {{bottlenecks}}
Automation Opportunities: {{automation_opportunities}}
Importance Rating: {{score}}/5
```

---

#### Q2: What are the inputs and outputs of this process?
**Goal:** Clarify task boundaries and data flow  
**Expected Answer:** Input data sources, output deliverable formats

**Follow-up Prompts:**
- Where does the input data come from? What is its format?
- Who does the output need to be delivered to? What are the format requirements?
- What temporary files or data are generated in between?
- Is there a quality check or acceptance stage?

**Recording Template:**
```
Input:
- Source: {{input_source}}
- Format: {{input_format}}
- Frequency: {{input_frequency}}

Output:
- Recipient: {{output_recipient}}
- Format: {{output_format}}
- Acceptance Criteria: {{acceptance_criteria}}

Importance Rating: {{score}}/5
```

---

### Category B: Pain Point Identification

#### Q3: In the current process, what are the three stages that make you feel most frustrated or inefficient?
**Goal:** Identify core pain points and determine optimization priority  
**Expected Answer:** Specific problem descriptions, frequency, impact level

**Follow-up Prompts:**
- How often does this problem occur?
- When it happens, how do you handle it?
- What are the consequences of this problem? (Time loss/Error/Stress)
- Have you tried to solve this problem? What was the result?
- If this problem were solved, how would it improve your work?

**Recording Template:**
```
Pain Point 1: {{pain_point_1}}
- Frequency: {{frequency_1}}
- Impact: {{impact_1}}
- Current Workaround: {{workaround_1}}
- Desired Improvement: {{desired_improvement_1}}
- Priority: P{{priority_1}}

Pain Point 2: {{pain_point_2}}
- Frequency: {{frequency_2}}
- Impact: {{impact_2}}
- Current Workaround: {{workaround_2}}
- Desired Improvement: {{desired_improvement_2}}
- Priority: P{{priority_2}}

Pain Point 3: {{pain_point_3}}
- Frequency: {{frequency_3}}
- Impact: {{impact_3}}
- Current Workaround: {{workaround_3}}
- Desired Improvement: {{desired_improvement_3}}
- Priority: P{{priority_3}}

Importance Rating: {{score}}/5
```

---

#### Q4: Can you share a recent difficult case that left a deep impression on you?
**Goal:** Understand pain points deeply through specific cases  
**Expected Answer:** Scenario description, problem occurrence process, solution

**Follow-up Prompts:**
- What was the situation at the time?
- How was the problem discovered?
- How long did you spend solving it?
- How was it eventually resolved?
- If it happened again, what kind of help would you want?

**Recording Template:**
```
Case Title: {{case_title}}
Date: {{case_date}}
Scenario Description: {{scenario}}
Problem Details: {{problem_details}}
Resolution Process: {{resolution_process}}
Time Spent: {{time_spent}}
Emotional Impact: {{emotional_impact}}
Learnings: {{learnings}}

Importance Rating: {{score}}/5
```

---

### Category C: Collaboration Requirements

#### Q5: What roles or personnel are involved in this process? How do they collaborate?
**Goal:** Understand team collaboration patterns and identify communication bottlenecks  
**Expected Answer:** Role list, collaboration methods, communication frequency

**Follow-up Prompts:**
- Who is involved in this process?
- What is everyone responsible for?
- How do you communicate? (Meetings/Email/Instant Messaging)
- What difficulties are there in collaboration?
- How is information passed? Is there any information loss or delay?

**Recording Template:**
```
Role List:
1. {{role_1}} - Responsibility: {{duty_1}} - Comm Method: {{comm_1}}
2. {{role_2}} - Responsibility: {{duty_2}} - Comm Method: {{comm_2}}
3. {{role_3}} - Responsibility: {{duty_3}} - Comm Method: {{comm_3}}

Collaboration Pain Points: {{collaboration_pain_points}}
Information Flow: {{information_flow}}
Decision Bottlenecks: {{decision_bottlenecks}}

Importance Rating: {{score}}/5
```

---

#### Q6: How do you hope AI Agents will integrate into this process? What is the ideal way to collaborate?
**Goal:** Collect user expectations for AI collaboration  
**Expected Answer:** Desired AI role, interaction method, degree of control

**Follow-up Prompts:**
- What role do you want AI to take? (Assistant/Expert/Executor)
- How do you want to interact with AI? (Natural language/Structured instructions)
- How much control do you want to maintain?
- Under what circumstances do you want AI to make autonomous decisions?
- In what situations do you want to be consulted?

**Recording Template:**
```
Expected AI Role: {{expected_ai_role}}
Interaction Preference: {{interaction_preference}}
Control Level: {{control_level}} (High/Medium/Low)
Autonomous Decision Scenarios: {{autonomous_scenarios}}
Consultation Scenarios: {{consultation_scenarios}}
Concerns/Worries: {{concerns}}

Importance Rating: {{score}}/5
```

---

### Category D: Quality Requirements

#### Q7: What are your quality standards for the output of this task?
**Goal:** Clarify quality expectations and design acceptance mechanisms  
**Expected Answer:** Quality indicators, acceptance criteria, common errors

**Follow-up Prompts:**
- What kind of output is considered "good"?
- What kind of errors are unacceptable?
- How do you check quality?
- What are common causes of quality issues?
- Are there any examples or templates to refer to?

**Recording Template:**
```
Quality Standards: {{quality_standards}}
Acceptance Checklist:
- [ ] {{check_1}}
- [ ] {{check_2}}
- [ ] {{check_3}}

Common Errors:
1. {{error_1}} - Frequency: {{freq_1}}
2. {{error_2}} - Frequency: {{freq_2}}

Quality Check Method: {{quality_check_method}}
Reference Examples: {{reference_examples}}

Importance Rating: {{score}}/5
```

---

#### Q8: If the result generated by AI needs modification, how do you want to provide feedback?
**Goal:** Design feedback loops and iteration mechanisms  
**Expected Answer:** Feedback method, expected number of iterations, modification preference

**Follow-up Prompts:**
- How do you usually point out problems?
- How many rounds of modification do you have patience for?
- Do you prefer a one-time complete modification or step-by-step adjustment?
- Under what circumstances would you choose to redo it yourself instead of modifying?

**Recording Template:**
```
Feedback Style: {{feedback_style}}
Iteration Expectation: {{iteration_expectation}}
Modification Preference: {{modification_preference}} (Complete/Step-by-step)
Redo Threshold: {{redo_threshold}}
Feedback Detail Level: {{feedback_detail_level}}

Importance Rating: {{score}}/5
```

---

### Category E: Scale and Expansion

#### Q9: What is the execution frequency and scale of this task? What will change in the future?
**Goal:** Assess system load and design scalability  
**Expected Answer:** Current frequency, data volume, growth expectations

**Follow-up Prompts:**
- How often is this task performed?
- How much data/how many items are processed each time?
- What is the difference between peak and off-peak periods?
- In the next 6-12 months, what changes will there be in scale?
- Is there a need for batch processing?

**Recording Template:**
```
Current Frequency: {{current_frequency}}
Single Batch Size: {{batch_size}}
Data Volume: {{data_volume}}
Peak/Valley Ratio: {{peak_ratio}}

Next 6-12 Months Expectation:
- Frequency Change: {{frequency_change}}
- Scale Change: {{scale_change}}
- New Requirements: {{new_requirements}}

Performance Requirements: {{performance_requirements}}
Scalability Needs: {{scalability_needs}}

Importance Rating: {{score}}/5
```

---

#### Q10: Besides the current process, what other related workflows might benefit from AI automation?
**Goal:** Identify expansion opportunities and plan long-term roadmap  
**Expected Answer:** Related workflows, priority, dependencies

**Follow-up Prompts:**
- What other similar workflows are there?
- What is the connection between these processes?
- If you could only automate one, which would you choose? Why?
- Which problem do you want to solve first?
- What is the long-term vision?

**Recording Template:**
```
Related Processes:
1. {{related_flow_1}} - Connection: {{rel_1}} - Priority: {{pri_1}}
2. {{related_flow_2}} - Connection: {{rel_2}} - Priority: {{pri_2}}
3. {{related_flow_3}} - Connection: {{rel_3}} - Priority: {{pri_3}}

Top Priority for Automation: {{top_priority}}
Selection Reasoning: {{selection_reasoning}}
Long-term Vision: {{long_term_vision}}
Roadmap Suggestion: {{roadmap_suggestion}}

Importance Rating: {{score}}/5
```

---

## Scoring and Evaluation Guide

### Importance Rating Standards

| Rating | Meaning | Action Suggestion |
|--------|---------|-------------------|
| 5 | Core Pain Point/Critical Requirement | Must be solved, Priority P0 |
| 4 | Important Pain Point/Strong Requirement | Should be solved, Priority P1 |
| 3 | Medium Pain Point/General Requirement | Can be considered, Priority P2 |
| 2 | Minor Pain Point/Low Priority | Optional optimization, Priority P3 |
| 1 | Not a Pain Point/No Requirement | Not processed for now |

### Pain Point Priority Matrix

```
Impact Level
    │
High│  P0: {{count_p0}}   P1: {{count_p1}}
    │
Med │  P1: {{count_p1b}}  P2: {{count_p2}}
    │
Low │  P2: {{count_p2b}}  P3: {{count_p3}}
    └───────────────────────────────
        Low          High
              Frequency
```

### Team Configuration Suggestion Scoring

| Dimension | Weight | Rating (1-5) | Weighted Score |
|-----------|--------|--------------|----------------|
| Process Complexity | 20% | {{score_complexity}} | {{weighted_1}} |
| Pain Point Severity | 25% | {{score_pain}} | {{weighted_2}} |
| Collaboration Needs | 20% | {{score_collaboration}} | {{weighted_3}} |
| Quality Requirements | 20% | {{score_quality}} | {{weighted_4}} |
| Scale/Scalability | 15% | {{score_scale}} | {{weighted_5}} |
| **Total Score** | 100% | - | **{{total_score}}** |

**Team Size Suggestion:**
- Total Score 4.0-5.0: Suggest 4-5 Agents (Manager + 3-4 Workers)
- Total Score 3.0-3.9: Suggest 3-4 Agents (Manager + 2-3 Workers)
- Total Score 2.0-2.9: Suggest 2-3 Agents (Manager + 1-2 Workers)
- Total Score < 2.0: Suggest 1-2 Agents (Manager may not be needed)

---

## Interview Record Summary

### Key Findings

1. **Core Pain Points:** {{key_finding_1}}
2. **Process Bottlenecks:** {{key_finding_2}}
3. **Collaboration Opportunities:** {{key_finding_3}}
4. **Quality Expectations:** {{key_finding_4}}
5. **Expansion Potential:** {{key_finding_5}}

### Recommended Team Configuration

Based on the interview results, the recommended configuration:

| Agent | Persona Suggestion | Task Category | Reason |
|-------|-------------------|---------------|--------|
| Manager | {{suggested_manager}} | {{suggested_manager_category}} | {{manager_reasoning}} |
| Worker 1 | {{suggested_worker1}} | {{suggested_worker1_category}} | {{worker1_reasoning}} |
| Worker 2 | {{suggested_worker2}} | {{suggested_worker2_category}} | {{worker2_reasoning}} |
| Worker 3 | {{suggested_worker3}} | {{suggested_worker3_category}} | {{worker3_reasoning}} |

### Next Steps

- [ ] Organize interview records
- [ ] Create Team Design Document
- [ ] Confirm solution with user
- [ ] Start Agent configuration

---

## Appendix: Persona Quick Reference

### Recommended by Role

| Role | Preferred Persona | Alternative Persona |
|------|-------------------|---------------------|
| Strategic Planning | Charlie Munger | Naval, Fu Sheng |
| Deep Development | Richard Feynman | Linus, Carmack |
| Code Review | W. Edwards Deming | Uncle Bob, Dijkstra |
| Project Management | Peter Drucker | Andy Grove |
| Product Design | Steve Jobs | Allen Zhang, Yu Jun |
| Copywriting | David Ogilvy | Ernest Hemingway, Seth Godin |
| User Experience | Donald Norman | Naoto Fukasawa |
| Quality Assurance | W. Edwards Deming | Jack Welch |

### Recommended by Task Category

| Task Category | Recommended Persona | Model Type |
|---------------|---------------------|------------|
| ultrabrain | Munger, Turing, Knuth | GPT/Gemini Pro |
| deep | Feynman, Linus, Carmack | GPT Codex |
| visual-engineering | Steve Jobs, Kenya Hara, Jony Ive | Gemini Pro |
| artistry | James Dyson, Seth Godin | Claude/GPT |
| writing | Hemingway, George Orwell, Lu Xun | Claude/Kimi |
| quick | Any | Grok/Haiku/Flash |

---

**Template Version:** 1.0.0  
**Applicable Skill:** Multi-Agent Orchestration  
**Last Updated:** 2026-03-19
