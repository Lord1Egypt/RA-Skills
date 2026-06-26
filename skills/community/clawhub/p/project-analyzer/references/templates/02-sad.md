# {{PROJECT_NAME}} - Software Architecture Document (SAD)

## Document Info

| Item | Content |
|------|---------|
| Project Name | {{PROJECT_NAME}} |
| Version | {{VERSION}} |
| Date | {{DATE}} |

---

## 1. Architecture Overview

### 1.1 System Goals

{{PROJECT_NAME}} adopts **{{ARCHITECTURE_PATTERN}}** architecture with following characteristics:

- High Availability
- Scalability
- Maintainability
- Security

### 1.2 Architecture Principles

| Principle | Description |
|----------|-------------|
| Layered Responsibility | Clear separation of concerns |
| Dependency Inversion | Depend on interfaces not implementations |
| Object-Oriented | Apply OOP principles properly |

---

## 2. Technology Stack

### 2.1 Technology Overview

| Component | Technology | Version | Description |
|-----------|------------|---------|-------------|
| Language | {{LANGUAGE}} | {{LANGUAGE_VERSION}} | Primary language |
| Framework | {{FRAMEWORK}} | {{FRAMEWORK_VERSION}} | Core framework |
| Database | {{DATABASE}} | {{DB_VERSION}} | Persistence |
| Cache | {{CACHE}} | - | Hot data cache |
| MQ | {{MQ}} | - | Async decoupling |

### 2.2 Architecture Diagram

```
{{ARCHITECTURE_DIAGRAM}}
```

---

## 3. Module Design

### 3.1 Module Overview

{{MODULE_OVERVIEW}}

### 3.2 Layered Architecture

{{LAYER_ARCHITECTURE}}

---

## 4. Core Flows

### 4.1 Request Flow

{{REQUEST_FLOW}}

### 4.2 Async Flow

{{ASYNC_FLOW}}

---

## 5. Deployment

### 5.1 Deployment Topology

{{DEPLOYMENT_DIAGRAM}}

### 5.2 Container Orchestration

{{K8S_CONFIG}}

---

## 6. Architecture Decision Records (ADR)

{{ADR_RECORDS}}

---

## 7. Security Design

### 7.1 Authentication Flow

{{AUTH_FLOW}}

### 7.2 Permission Control

{{PERMISSION_MODEL}}

---

*Version: {{VERSION}}*
*Last Updated: {{DATE}}*
