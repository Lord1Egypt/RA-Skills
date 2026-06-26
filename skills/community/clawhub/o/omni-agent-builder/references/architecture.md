# references/architecture.md

A simple, reliable agent architecture:

1) **Plan**
- restate goal + constraints
- propose steps + risks
- define “done”

2) **Act**
- use tools when correctness matters
- stop on errors and recover
- keep a change log

3) **Reflect**
- verify outputs against “done”
- run quick acceptance tests
- write memories (daily log + curated memory)

In multi-agent mode:
- Planner produces plan + tests
- Executor implements
- Critic reviews and requests minimal fixes
