---
name: service-registry
description: |
  Registers external services with health checks, quotas, and a usage logger for per-call cost and sessions
version: 1.10.3
triggers:
  - services
  - registry
  - execution
  - health-checks
  - integration
  - adding rate-limited APIs or logging usage
metadata: {"openclaw": {"homepage": "https://github.com/athola/claude-night-market/tree/master/plugins/leyline", "emoji": "\ud83e\udd9e"}}
source: claude-night-market
source_plugin: leyline
---

> **Night Market Skill**: ported from [claude-night-market/leyline](https://github.com/athola/claude-night-market/tree/master/plugins/leyline). For the full experience with agents, hooks, and commands, install the Claude Code plugin.


# Service Registry

## Overview

A registry pattern for managing connections to external services. Handles configuration, health checking, and execution across multiple service integrations.

## When To Use

- Managing multiple external services.
- Need consistent execution interface.
- Want health monitoring across services.
- Building service failover logic.

## When NOT To Use

- Single service integration without registry needs

## Core Concepts

### Service Configuration

```python
@dataclass
class ServiceConfig:
    name: str
    command: str
    auth_method: str  # "api_key", "oauth", "token"
    auth_env_var: str
    quota_limits: dict
    models: list[str] = field(default_factory=list)
```
**Verification:** Run the command with `--help` flag to verify availability.

### Execution Result

```python
@dataclass
class ExecutionResult:
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration: float
    tokens_used: int
```
**Verification:** Run the command with `--help` flag to verify availability.

## Quick Start

### Register Services
```python
# Sketch: implement ServiceRegistry and ServiceConfig in your plugin.
# leyline ships no service_registry module.

registry = ServiceRegistry()

registry.register(
    "gemini",
    ServiceConfig(
        name="gemini",
        command="gemini",
        auth_method="api_key",
        auth_env_var="GEMINI_API_KEY",
        quota_limits={"rpm": 60, "daily": 1000},
    ),
)
```
**Verification:** Run the command with `--help` flag to verify availability.

### Execute via Service
```python
result = registry.execute(
    service="gemini",
    prompt="Analyze this code",
    files=["src/main.py"],
    model="gemini-3.8-flash",
)

if result.success:
    print(result.stdout)
```
**Verification:** Run the command with `--help` flag to verify availability.

### Health Checks
```python
# Check single service
status = registry.health_check("gemini")

# Check all services
all_status = registry.health_check_all()
for service, healthy in all_status.items():
    print(f"{service}: {'OK' if healthy else 'FAILED'}")
```
**Verification:** Run the command with `--help` flag to verify availability.

## Service Selection

### Auto-Selection
```python
# Select best service for task
service = registry.select_service(
    requirements={"large_context": True, "fast_response": False}
)
```
**Verification:** Run the command with `--help` flag to verify availability.

### Failover Pattern
```python
def execute_with_failover(prompt: str, files: list) -> ExecutionResult:
    for service in registry.get_healthy_services():
        result = registry.execute(service, prompt, files)
        if result.success:
            return result
    raise AllServicesFailedError()
```
**Verification:** Run the command with `--help` flag to verify availability.

## Integration Pattern

```yaml
# In your skill's frontmatter
dependencies: [leyline:service-registry]
```
**Verification:** Run the command with `--help` flag to verify availability.

## Detailed Resources

- **Service Config**: See `modules/service-config.md` for configuration options.
- **Execution Patterns**: See `modules/execution-patterns.md` for advanced usage.
- **Quota Management**: Load `modules/quota-management.md` when a service
  imposes rate or cost limits. It covers threshold tiers, `QuotaTracker`,
  and degradation (`threshold-strategies`, `estimation-patterns`).
- **Usage Logging**: Load `modules/usage-logging.md` when a skill needs an
  audit trail, usage analytics, or per-call cost tracking. It covers
  `UsageLogger` and JSONL sessions (`session-patterns`, `log-formats`).

## Exit Criteria

- [ ] Services registered with configuration.
- [ ] Health checks passing.
- [ ] Execution results properly handled.
