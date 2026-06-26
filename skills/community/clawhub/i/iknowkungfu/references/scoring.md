# Trust Scoring — Full Methodology

## Overview

Every recommended skill gets a trust score from 0 to 5 stars. The score reflects safety and reliability, not quality of implementation. A 5-star skill is probably safe and well-maintained. It might still be mediocre at its job.

## Factor Weights

| Factor | Weight | What it measures |
|---|---|---|
| Downloads | 25% | Community adoption, battle-tested |
| Stars | 20% | Community endorsement |
| Author reputation | 15% | Track record of the developer |
| Recency | 15% | Active maintenance |
| Permission scope | 15% | Principle of least privilege |
| Security | 10% | Known flags or suspicious patterns |

## Scoring Each Factor (0-5 scale)

### Downloads (25%)
| Downloads | Score |
|---|---|
| 10,000+ | 5.0 |
| 5,000-9,999 | 4.0 |
| 1,000-4,999 | 3.0 |
| 200-999 | 2.0 |
| 50-199 | 1.0 |
| <50 | Disqualified |

### Stars (20%)
| Stars | Score |
|---|---|
| 100+ | 5.0 |
| 50-99 | 4.0 |
| 20-49 | 3.0 |
| 5-19 | 2.0 |
| 1-4 | 1.0 |
| 0 | 0.5 |

### Author Reputation (15%)
| Criteria | Score |
|---|---|
| Known ecosystem contributor (OpenClaw core, multiple popular skills) | 5.0 |
| Multiple skills with good download counts | 4.0 |
| Single well-received skill | 3.0 |
| New author, skill looks legitimate | 2.0 |
| No information available | 1.0 |

### Recency (15%)
| Last Updated | Score |
|---|---|
| Within 30 days | 5.0 |
| 31-60 days | 4.0 |
| 61-90 days | 3.0 |
| 91-180 days | 2.0 |
| 180+ days | 1.0 |

### Permission Scope (15%)
| Permissions | Score |
|---|---|
| filesystem:read only | 5.0 |
| filesystem:read + write | 4.0 |
| + network:outbound (justified by purpose) | 3.0 |
| + network:outbound (unclear justification) | 2.0 |
| Broad permissions without clear need | 1.0 |

### Security (10%)
| Status | Score |
|---|---|
| Clean VirusTotal, minimal permissions | 5.0 |
| Clean VirusTotal, moderate permissions | 4.0 |
| No VirusTotal data, looks clean | 3.0 |
| Minor flags but likely false positive | 2.0 |
| VirusTotal flags present | Disqualified |

## Calculating the Final Score

```
final = (downloads * 0.25) + (stars * 0.20) + (author * 0.15) + 
        (recency * 0.15) + (permissions * 0.15) + (security * 0.10)
```

Round to one decimal place. Display as stars: ★ 4.2

## Automatic Disqualification

Never recommend a skill if ANY of these are true:
- Fewer than 50 downloads
- Known VirusTotal flags (not false positives)
- No author attribution
- Requests both network:outbound AND filesystem:write without clear justification in its description
- Description is vague or generic ("do everything", "ultimate tool")

## Edge Cases

**High downloads but bad permissions**: Cap the score at 3.0 and add a note: "Popular but requests broad permissions. Review before installing."

**New skill from reputable author**: Allow minimum 2.0 floor even with low downloads, if the author has other trusted skills. Note: "New from a trusted author."

**Reasoning requirement**: Every trust score must be explainable in one sentence. "★ 4.2: 5K downloads, active author, minimal permissions, updated this month." Include this in the recommendation output.
