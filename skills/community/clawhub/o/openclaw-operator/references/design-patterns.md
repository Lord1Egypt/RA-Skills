# Agentic Design Patterns for OpenClaw

Mapping of the Agentic Design Patterns framework (Gulli, 2025) to OpenClaw operational concerns. This reference explains each pattern and how it's applied in the bundled scripts and guardrails.

## Applied Patterns

### Pattern 2: Routing

**Concept:** Route tasks to appropriate processing paths based on type, priority, or resource requirements. Prevents bottlenecks by ensuring different task types don't compete for the same execution slot.

**OpenClaw application:** Session lane architecture. Interactive messages route to `agent:main:main`, cron jobs route to dedicated `agent:main:cron:<name>` lanes. This separation means a slow cron can never block a user's message.

**Implementation:** The cron lane validator in `session-health-watchdog.sh` enforces this by flagging any cron job configured to use the main lane.

### Pattern 11: Goal Monitoring

**Concept:** Continuously track whether the agent's capabilities remain aligned with its goals. Detect drift before it causes failures.

**OpenClaw application:** Bootstrap budget monitoring. AGENTS.md defines the agent's goals and capabilities. If it grows beyond the 20K limit, capabilities silently degrade as instructions get truncated. The budget check catches this drift early.

**Implementation:** `bootstrap-budget-check.sh` provides section-by-section analysis with tiered thresholds (75%/85%/95%).
### Pattern 12: Exception Handling

**Concept:** Structured responses to failures. Instead of crashing or silently failing, the system detects exceptions, classifies severity, and either self-heals or escalates to a human.

**OpenClaw application:** The watchdog script classifies every detected issue as WARN or CRIT, aggregates them, and reports via the agent's Telegram channel. This turns silent failures (like a slowly growing session) into visible alerts.

**Implementation:** `session-health-watchdog.sh` with its `add_alert` function and severity-based exit codes.

### Pattern 16: Resource-Aware Optimization

**Concept:** Monitor resource consumption and optimize before limits are hit. Plan operations with awareness of memory, token, time, and storage budgets.

**OpenClaw application:** Session size monitoring (5MB/10MB thresholds) and bootstrap budget tracking prevent the gateway from hitting Node.js heap limits or compaction timeouts. The thresholds are set well below the failure points to allow time for intervention.

**Implementation:** Both bundled scripts include resource monitoring. The watchdog checks session sizes and the budget check tracks character utilization.

### Pattern 19: Evaluation & Monitoring

**Concept:** Systematically observe system behavior over time to detect patterns, trends, and anomalies that point-in-time checks might miss.

**OpenClaw application:** Gateway log scanning for recurring error patterns. A single stuck-session warning is noise; 50 in an hour is a deadlock. The watchdog's 15-minute window scan turns raw log entries into actionable signal.

**Implementation:** The recent-errors section of `session-health-watchdog.sh` and the failure patterns catalog in `references/failure-patterns.md`.
### Pattern 20: Prioritization

**Concept:** When multiple issues exist, address the highest-impact one first. Triage prevents wasted effort on low-priority problems while critical ones persist.

**OpenClaw application:** The Quick Start triage order in SKILL.md is ranked by frequency and impact from real log data. Lane deadlocks (#1) caused 4,605 warnings; sandbox write failures (#8) caused only 8. Fix the deadlock first.

**Implementation:** The ordered triage list in the skill's Quick Start section.

## Patterns to Consider Adding

These patterns from the framework could enhance OpenClaw operations in the future:

### Pattern 3: Parallelization
Running diagnostic checks in parallel instead of sequentially. The watchdog currently runs checks in series, which is fine for a 30-min cron but could be optimized for on-demand diagnostics.

### Pattern 7: Reflection
Having the agent periodically evaluate its own performance — analyzing response times, success rates, and user satisfaction trends. Could be implemented as a weekly self-assessment cron.

### Pattern 14: Context Management
More sophisticated session lifecycle management — proactive rotation of high-traffic sessions before they hit size limits, archival of inactive sessions, and context summarization.

### Pattern 18: Feedback Integration
Closing the loop between detected failures and AGENTS.md updates. When the watchdog finds a new failure pattern, it could propose an AGENTS.md amendment to prevent recurrence.