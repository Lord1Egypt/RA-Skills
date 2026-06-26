---
name: multi-agent-collaboration-communication
description: Focused on multi-agent collaboration and communication scenarios, helping users build and manage complex distributed agent systems to achieve task decomposition, parallel processing, and collaborative work. Use this skill when users need to design multi-agent system architectures, plan task distribution schemes, establish inter-agent communication protocols, or implement distributed collaboration workflows.
---

# Multi-Agent Collaboration Communication

A guide to designing and implementing multi-agent collaboration systems.

## Core Capabilities

1. **System Architecture Design** - Design the overall architecture of multi-agent systems, including role definitions, communication topologies, and coordination mechanisms
2. **Task Decomposition and Distribution** - Break complex tasks into parallelizable sub-tasks and distribute them appropriately among different agents
3. **Communication Protocol Design** - Establish mechanisms for message passing, state synchronization, and result aggregation between agents
4. **Collaboration Workflow Orchestration** - Design workflows, handle dependencies, and manage execution order
5. **Conflict Resolution and Consistency** - Address resource contention, decision conflicts, and data consistency issues

## Quick Start

### Usage Workflow

```
User Requirements → System Analysis → Architecture Design → Task Decomposition → Communication Design → Workflow Orchestration → Output Delivery
```

### Typical Application Scenarios

- **Distributed Data Processing** - Multiple agents process different partitions of a large dataset in parallel
- **Complex Workflow Automation** - Multi-step business processes, with each step handled by a specialized agent
- **Intelligent Customer Service Systems** - Different agents handle different types of inquiries, collaborating to provide comprehensive service
- **Code Review and Generation** - Multiple specialized agents address dimensions such as architecture, security, and performance respectively
- **Scientific Research Collaboration** - Simulate a research team, with agents playing different roles (experimental design, data analysis, paper writing)

## Design Methodology

### 1. Role Definition

Each agent should have clear responsibility boundaries:

| Dimension | Description |
|-----------|-------------|
| **Core Responsibility** | The agent's primary function and task scope |
| **Input/Output** | What data it receives and what results it produces |
| **Capability Boundary** | What it can and cannot do |
| **Dependencies** | Which agents it depends on and which depend on it |

### 2. Communication Patterns

Choose the appropriate communication topology:

- **Star** - Central coordinator manages all communication
- **Bus** - Shared message bus with broadcast/subscribe model
- **Mesh** - Direct agent-to-agent communication, decentralized
- **Hierarchical** - Tree structure with escalation by level

### 3. Coordination Mechanisms

- **Master-Slave** - One master agent assigns tasks; multiple slave agents execute
- **Peer-to-Peer** - All agents collaborate as equals
- **Pipeline** - Data flows through multiple agents for sequential processing
- **Competitive** - Multiple agents compete for tasks; the best performer executes

## Workflow

### Step 1: Requirements Analysis

Understand the user's business scenario and objectives:
- What problem needs to be solved?
- What is the complexity and scale of the task?
- What are the requirements for real-time performance and reliability?
- What constraints exist?

### Step 2: Architecture Design

Design the overall system architecture:
- Determine the number and roles of agents
- Select the communication topology
- Define the coordination mechanism
- Design the data flow

**Reference** [references/architecture_patterns.md](references/architecture_patterns.md) for common architecture patterns

### Step 3: Task Decomposition

Break down complex tasks:
- Identify sub-tasks that can be parallelized
- Analyze task dependencies
- Estimate resource requirements for each sub-task
- Determine execution priorities

**Reference** [references/task_decomposition.md](references/task_decomposition.md) for task decomposition strategies

### Step 4: Communication Protocol Design

Define interaction rules between agents:
- Message format and encoding
- Communication protocol (synchronous/asynchronous)
- Error handling and retry mechanisms
- Timeout and circuit breaker strategies

**Reference** [references/communication_protocols.md](references/communication_protocols.md) for protocol design templates

### Step 5: Workflow Orchestration

Design the collaboration workflow:
- Define the workflow state machine
- Handle branching and conditional logic
- Design result aggregation strategies
- Implement monitoring and logging

**Reference** [references/workflow_templates.md](references/workflow_templates.md) for workflow templates

### Step 6: Output Delivery

Generate executable deliverables:
- System architecture diagram
- Agent role definition document
- Communication protocol specification
- Collaboration workflow code/configuration

## Best Practices

### Design Principles

1. **Single Responsibility** - Each agent does one thing and does it well
2. **Loose Coupling** - Agents communicate through standard interfaces to reduce dependencies
3. **Fault-Tolerant Design** - Account for agent failures, network interruptions, and other exceptions
4. **Observability** - Comprehensive logging, monitoring, and tracing mechanisms
5. **Incremental Evolution** - Start simple and gradually increase complexity

### Common Pitfalls

- **Over-Engineering** - Creating too many agents for simple tasks
- **Tight Coupling** - Direct dependencies on internal implementations between agents
- **Ignoring Boundaries** - Not defining clear responsibility boundaries
- **Lack of Fallback** - No backup plans for handling failure scenarios

## Resources

### references/
Detailed design reference documents:
- `architecture_patterns.md` - Common multi-agent architecture patterns
- `task_decomposition.md` - Task decomposition strategies and methods
- `communication_protocols.md` - Communication protocol design specifications
- `workflow_templates.md` - Reusable workflow templates

### assets/
Available templates and examples:
- `templates/` - Architecture design document templates, code scaffolding templates
- `examples/` - Implementation examples for typical scenarios

### scripts/
Auxiliary tool scripts:
- `generate_architecture.py` - Generate architecture diagrams and configurations
- `validate_design.py` - Validate the completeness of design solutions