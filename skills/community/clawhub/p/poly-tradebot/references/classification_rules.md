# Topic Classification Rules

## Keyword Triggers

### Geopolitics Classification
Article is classified as **geopolitics** if headline or content contains ANY of:

| Keyword | Context |
|---------|---------|
| Iran | Any mention of Iranian government, military, or actions |
| war | Armed conflict, military engagement |
| military | Military operations, deployments, strikes |
| conflict | Armed conflict, regional tensions |
| sanctions | Economic sanctions, trade restrictions |
| regime | Government leadership, political structure |
| IRGC | Islamic Revolutionary Guard Corps |
| drone | Drone strikes, UAV operations |
| missile | Missile attacks, defense systems |
| Strait of Hormuz | Chokepoint, shipping lane disruptions |
| UAE | United Arab Emirates involvement |
| Middle East tensions | Regional conflict escalation |
| Fujairah | Oil infrastructure, storage hub |
| tanker | Oil tanker attacks, shipping disruptions |
| airspace | Airspace closure, flight restrictions |

### Macroeconomics Classification
Article is classified as **macroeconomics** if headline or content contains ANY of:

| Keyword | Context |
|---------|---------|
| Fed | Federal Reserve, FOMC, monetary policy |
| Treasury yields | Bond yields, 10Y, 30Y rates |
| interest rates | Central bank rate decisions |
| inflation | CPI, price pressures, inflation expectations |
| central bank | RBA, ECB, BoE, BoJ policy decisions |
| CPI | Consumer Price Index |
| employment | Jobs data, unemployment, labor market |
| GDP | Economic growth, GDP prints |
| monetary policy | Rate hikes, cuts, quantitative easing |
| oil price | Economic impact (not military context) |
| stagflation | Growth slowdown + inflation |

## Disambiguation Rules

### Overlapping Keywords
If article contains BOTH geopolitics AND macroeconomics keywords:

1. **Primary focus test:** Which topic dominates the headline and lead paragraph?
2. **Action test:** Is the primary action military/geopolitical (→ geopolitics) or economic/policy (→ macroeconomics)?
3. **Default rule:** If equal weight, classify as **geopolitics** (war drives economic impact)

### Examples

| Headline | Classification | Rationale |
|----------|---------------|-----------|
| "Iran attacks UAE gas field, oil surges" | Geopolitics | Primary action is military attack |
| "Fed holds rates as oil shock fuels inflation" | Macroeconomics | Primary focus is Fed policy decision |
| "Treasury yields fall on Iran war, Fed decision looms" | Macroeconomics | Market reaction to war + Fed policy focus |
| "US-Iran ceasefire talks begin, oil drops 5%" | Geopolitics | Primary action is diplomatic/military |

## Freshness Filter

- **Preferred:** Articles published within last 24 hours
- **Acceptable:** Articles published within last 48 hours
- **Reject:** Articles older than 48 hours (unless major breaking development)

## Minimum Article Count

- **Target:** At least 3 articles per pipeline run
- **Fallback:** If only 1-2 articles match tags, expand to related topics (oil markets, defense stocks, Gulf state reactions)
