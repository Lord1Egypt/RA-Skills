# Example: Intelligent Code Review System

## Scenario Description
Build a multi-agent collaborative code review system that simulates the code review process of a real development team.

## System Architecture

### Architecture Diagram
```
                    ┌──────────────┐
                    │  Code Commit │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Coordinator │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │ Architect    │ │ Security     │ │ Style        │
   └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Aggregator  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Review Report│
                    └──────────────┘
```

### Agent Role Definitions

#### 1. Coordinator
- **Responsibility**: Receive code submissions, distribute review tasks, coordinate agent work
- **Input**: Code submission information (PR, commit, branch, etc.)
- **Output**: Review task assignments
- **Capabilities**: Task scheduling, state management, timeout control

#### 2. Architect Agent
- **Responsibility**: Review code architecture design, design pattern application, module dependencies
- **Input**: Code changes, project structure
- **Output**: Architecture review comments
- **Check Items**:
  - Appropriate use of design patterns
  - Reasonable module coupling
  - Specification compliance of interface design
  - Scalability considerations

#### 3. Security Agent
- **Responsibility**: Vulnerability scanning, sensitive information detection, permission checks
- **Input**: Code changes
- **Output**: Security review comments
- **Check Items**:
  - SQL injection risks
  - XSS vulnerabilities
  - Sensitive information exposure
  - Unsafe dependencies
  - Permission control flaws

#### 4. Style Agent
- **Responsibility**: Code style checking, naming conventions, comment reviews
- **Input**: Code changes
- **Output**: Style review comments
- **Check Items**:
  - Code formatting standards
  - Naming conventions
  - Comment completeness
  - Code complexity

#### 5. Aggregator Agent
- **Responsibility**: Aggregate review results from all agents and generate a unified report
- **Input**: Review comments from each agent
- **Output**: Structured review report
- **Capabilities**: Deduplication, priority sorting, recommendation consolidation

## Workflow

```yaml
workflow:
  name: "code-review-workflow"
  type: "parallel"
  
  steps:
    - id: "receive"
      name: "Receive Code"
      agent: "coordinator"
      action: "receive_code"
      
    - id: "distribute"
      name: "Distribute Review"
      agent: "coordinator"
      action: "dispatch_review"
      parallel_branches:
        - id: "architect-review"
          agent: "architect-agent"
          action: "review_architecture"
          
        - id: "security-review"
          agent: "security-agent"
          action: "review_security"
          
        - id: "style-review"
          agent: "style-agent"
          action: "review_style"
      
    - id: "aggregate"
      name: "Aggregate Report"
      agent: "aggregator-agent"
      action: "aggregate_report"
      input:
        architect_result: "$architect-review.output"
        security_result: "$security-review.output"
        style_result: "$style-review.output"
      
    - id: "deliver"
      name: "Deliver Report"
      agent: "coordinator"
      action: "deliver_report"
      input:
        report: "$aggregate.output"
```

## Communication Protocol

### Message Format

```json
{
  "message_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z",
  "sender": "agent-id",
  "receiver": "agent-id",
  "message_type": "review_request|review_response|review_event",
  "correlation_id": "uuid",
  "payload": {
    "code_changes": {
      "files": ["src/main.py", "src/utils.py"],
      "diff": "...",
      "metadata": {
        "author": "developer@example.com",
        "commit_id": "abc123",
        "branch": "feature/new-feature"
      }
    },
    "review_result": {
      "issues": [
        {
          "severity": "high|medium|low",
          "category": "architecture|security|style",
          "file": "src/main.py",
          "line": 42,
          "message": "Issue description",
          "suggestion": "Improvement suggestion"
        }
      ],
      "summary": "Review summary"
    }
  }
}
```

## Task Decomposition

```
Code Review Task
├── Architecture Review
│   ├── Design pattern check
│   ├── Module dependency analysis
│   └── Interface design review
├── Security Review
│   ├── Vulnerability scanning
│   ├── Sensitive information detection
│   └── Dependency security check
└── Style Review
    ├── Code style check
    ├── Naming convention check
    └── Comment completeness check
```

## Output Example

### Review Report

```json
{
  "review_id": "review-123",
  "timestamp": "2024-01-01T00:00:00Z",
  "code_info": {
    "commit_id": "abc123",
    "author": "developer@example.com",
    "files_changed": 3
  },
  "summary": {
    "total_issues": 5,
    "high_severity": 1,
    "medium_severity": 2,
    "low_severity": 2,
    "status": "needs_fix"
  },
  "issues": [
    {
      "id": "SEC-001",
      "severity": "high",
      "category": "security",
      "agent": "security-agent",
      "file": "src/auth.py",
      "line": 45,
      "message": "SQL injection risk detected",
      "suggestion": "Use parameterized queries instead of string concatenation",
      "code_snippet": "..."
    },
    {
      "id": "ARC-001",
      "severity": "medium",
      "category": "architecture",
      "agent": "architect-agent",
      "file": "src/service.py",
      "line": 78,
      "message": "Class has multiple responsibilities; consider splitting",
      "suggestion": "Separate business logic from data access"
    }
  ],
  "recommendations": [
    "Fix high-priority security issues",
    "Refactor overly complex functions",
    "Add unit tests"
  ]
}
```

## Scalability Considerations

1. **New Review Dimensions**: Easily add agents for performance review, test coverage, etc.
2. **Customizable Rules**: Each agent's rules are configurable to suit different project requirements
3. **CI/CD Integration**: Can integrate with code repositories such as GitHub/GitLab
4. **Learning Capability**: Agents can learn from historical review data to improve accuracy