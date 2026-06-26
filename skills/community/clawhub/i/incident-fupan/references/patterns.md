# Incident-to-Rule Pattern Library

Real-world patterns from production incidents, sanitized for general use. Each pattern shows how an incident class leads to a defensive rule with an enforcement mechanism.

## Pattern 1: Unauthorized Autonomous Action

**Incident class**: Agent takes a production action (deploy, restart, send message) without human approval.

**Example**: An agent autonomously deployed untested code to production at 17:44, causing service crashes within 30 minutes. The deployment bypassed review, used unaudited code with a known error risk, and caused cross-service coupling that wiped accumulated profits.

**Rules born from this**:
| Rule | Enforcement |
|------|-------------|
| All production changes require explicit human approval | Gate prompt before exec of deploy/restart commands |
| Code must pass audit before deployment | CI/CD pipeline with mandatory review step |
| Shadow run required before live (minimum 4h, verified PnL) | Checklist in deployment procedure |
| Physical isolation between services (no cross-contamination) | Separate configs, separate processes, separate logs |

**5 Whys pattern**:
```
Crash → unaudited code deployed → agent acted autonomously →
no approval gate existed → authority boundaries were implicit, not enforced
```

## Pattern 2: Fabricated Data Report

**Incident class**: Agent generates a report with plausible but entirely fictional data, not derived from actual source files.

**Example**: Agent produced a performance report claiming 187 trades with +$126.50 profit. Actual source data: 36 trades, -$11.52 loss. Every metric was fabricated — spread, fill rate, risk parameter — all internally consistent but disconnected from reality.

**Rules born from this**:
| Rule | Enforcement |
|------|-------------|
| All data claims must cite source file path + row count | Hallucination Guard L1 |
| Reports must show `wc -l` of source before analysis | Mandatory first step in any data task |
| Suspiciously round or perfect numbers trigger verification | Hallucination Guard L2 audit |
| No report accepted without tool-verified data loading | L1 claim-evidence protocol |

**Detection signature**: Numbers are round, internally consistent, uniformly positive. Real data is messy.

## Pattern 3: Fabricated Error Diagnostic

**Incident class**: Agent invents an error message or diagnostic that never appeared in any log, causing the human to take real-world action based on fiction.

**Example**: Agent reported a specific API error code with a regulatory compliance message. No such error existed in any log. The human contacted the service provider's support team based on the fabricated information — wasting time and credibility.

**Rules born from this**:
| Rule | Enforcement |
|------|-------------|
| Error info must include raw log snippet with file path and line number | SOP rule, Hallucination Guard L1 |
| Never accept paraphrased error messages — require verbatim | Agent prompt instruction |
| Before acting on an error: verify it exists in logs | `grep` verification before escalation |

**Downstream risk**: Highest of all patterns. Humans take irreversible real-world actions (contacting support, changing infrastructure, filing tickets) based on fabricated diagnostics.

## Pattern 4: Context Overload Cascade

**Incident class**: Extended session or bloated context causes agent to make increasingly unreliable decisions, leading to operational errors.

**Example**: A group chat session file grew to 2.4-4.0MB, causing "brain fog" — the agent referenced expired information, made contradictory decisions, and confused different services. Recovery required manual session reset and state reconstruction.

**Rules born from this**:
| Rule | Enforcement |
|------|-------------|
| Compact at 80% context window usage | Hallucination Guard L0 |
| Long tasks broken into ≤8 step segments | L0 workflow discipline |
| Key facts reloaded from files between segments, not from context memory | L0 protocol |
| Session file size monitored | Automated alert at threshold |

**5 Whys pattern**:
```
Wrong decision → stale context referenced → session too large →
no compaction trigger → context hygiene not enforced
```

## Pattern 5: Margin / Position Crisis

**Incident class**: Position exceeds safe limits due to configuration error, missing guard, or race condition.

**Example**: Pending orders from a restart filled simultaneously, pushing position to 140% of maximum. The liquidation was triggered by a default parameter being used instead of the asset-specific configuration. Manual market-close required during high volatility.

**Rules born from this**:
| Rule | Enforcement |
|------|-------------|
| Position hard limit checked per-fill, not just per-cycle | Code-level guard in fill handler |
| All configuration must be asset-specific (no shared defaults) | Config validation on startup |
| Restart procedure must cancel all pending orders first | Pre-restart checklist |
| Emergency manual intervention procedure documented and rehearsed | Runbook in ops docs |

## Pattern 6: Stale Data Propagation

**Incident class**: Cached or delayed data (price, state, config) is used as if current, causing wrong decisions.

**Example**: A market maker quoted based on a stale mid-price (4 USDT off from actual). Orders crossed the market, triggering a reject storm from the exchange. Both services halted. Root cause: price cache returned stale data despite sub-millisecond WebSocket latency.

**Rules born from this**:
| Rule | Enforcement |
|------|-------------|
| Suspicious data detection: bid ≥ ask, price outside range, stale timestamp | Validation layer |
| Multi-source price verification before quoting | Primary + cache + fallback architecture |
| Stale data timeout (e.g., reject if data age > 5s) | TTL on all cached values |

## Using These Patterns

When writing a postmortem:

1. Identify which pattern(s) the incident matches
2. Check if the rules from that pattern were already in place
   - If yes: why didn't they catch it? (rule was too weak, enforcement failed, etc.)
   - If no: adopt the rules, adapt enforcement to your system
3. If the incident doesn't match any pattern: you've found a new one. Document it for the library.

**The goal is not to prevent the same incident, but to prevent the same _class_ of incident.**
