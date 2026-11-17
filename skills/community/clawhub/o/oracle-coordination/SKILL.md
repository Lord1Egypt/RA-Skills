---
name: oracle-coordination
description: Routes any task to the right specialist agent automatically — multi-agent task routing with keyword matching.
metadata:
  openclaw:
    emoji: 🤖
    homepage: https://tinycoderstudio.gumroad.com/l/7-agent-skills-pack
---
# Skill 1: Oracle Coordination — Multi-Agent Task Routing

## Overview
Routes any task to the right specialist agent automatically. Eliminates manual delegation decisions.

## Problem
Teams waste time deciding "who should handle this?" — security goes to admin, code to dev-worker, marketing to loki, etc.

## Solution
A routing function that analyzes task keywords and returns the correct agent + reasoning.

## Implementation

```javascript
// oracle-coordination.js
function routeToAgent(task) {
  const t = task.toLowerCase();
  
  if (/secur|malware|firewall|vulnerab|exploit|breach/.test(t))
    return { agent: 'admin', reason: 'Security concern' };
  if (/code|build|deploy|bug|fix|implement|refactor/.test(t))
    return { agent: 'dev-worker', reason: 'Code implementation' };
  if (/market|strateg|growth|pric|launch|outreach|lead/.test(t))
    return { agent: 'loki', reason: 'Marketing strategy' };
  if (/content|complian|review|audit|claim/.test(t))
    return { agent: 'product-reviewer', reason: 'Content/compliance review' };
  if (/image|visual|design|prompt|art/.test(t))
    return { agent: 'graphic-artist', reason: 'Visual/creative task' };
  if (/browser|scrape|screenshot|web|navigate/.test(t))
    return { agent: 'navigator', reason: 'Browser automation' };
  if (/human|tone|rewrite|natural/.test(t))
    return { agent: 'humanizer', reason: 'Text humanization' };
  return { agent: 'oracle', reason: 'Complex orchestration' };
}

// Usage
const result = routeToAgent("Fix the SQL injection vulnerability");
// { agent: 'admin', reason: 'Security concern' }
```

## x402 Integration (Pay-Per-Call)

```bash
curl -X POST https://your-api.com/api/oracle/route \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <base64_payment>" \
  -d '{"task":"Fix the security vulnerability"}'
# Returns: {"agent":"admin","reason":"Security concern"}
```

## Use Cases
- **Slack bot**: Auto-route tickets to right team
- **CI/CD pipeline**: Route build failures to dev-worker, security alerts to admin
- **Support triage**: Route customer issues to correct specialist
- **Agent swarms**: Coordinate multiple agents in sequence

## Customization
Add your own agents by extending the keyword patterns:

```javascript
if (/data|analytics|report|dashboard/.test(t))
  return { agent: 'analyst', reason: 'Data analysis' };
if (/legal|contract|compliance|gdpr/.test(t))
  return { agent: 'legal', reason: 'Legal review' };
```

## Value
- **Saves**: 5-10 min per task delegation decision
- **Scales**: Works for 10 or 10,000 tasks
- **Extensible**: Add agents without changing core logic