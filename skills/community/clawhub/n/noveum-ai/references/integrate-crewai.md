# Integrate: CrewAI

Requires Python 3.10+. One-call setup via an event listener that traces crews, agents,
tasks, and the LLM calls they make.

## 1. Install and initialize

```bash
pip install "noveum-trace[crewai]"
```

```python
import noveum_trace
from noveum_trace.integrations.crewai import setup_crewai_tracing

noveum_trace.init(project="<NOVEUM_PROJECT>", environment="production")
setup_crewai_tracing()   # attach BEFORE crews are constructed/kicked off
```

## 2. Placement

Call `setup_crewai_tracing()` in the same module/entrypoint where `Crew(...)` objects are
created, before `crew.kickoff()`. Nothing else changes in the crew definitions.

## 3. Coverage check

LLM calls made outside CrewAI (direct SDK usage, custom tools calling providers directly)
are not captured by the listener — wrap those per `integrate-openai-manual.md` §2.

## 4. Lifecycle

```python
import atexit
atexit.register(noveum_trace.shutdown)
```

CrewAI runs are often batch/CLI-style — exactly the shape that loses traces without an
explicit shutdown. Do not skip this.

Proceed to `verify-traces.md` for the acceptance check.
