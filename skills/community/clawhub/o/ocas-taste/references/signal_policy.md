# Taste Signal Policy

## Half-Life Decay
Signals beyond the configured half-life contribute proportionally less. Formula: effective_strength = strength × 0.5^(days_since / halflife_days).

## Reinforcement
Repeat signals for the same item reset the decay clock and increase effective strength. A restaurant visited 3 times in 6 months is stronger than one visited once 2 years ago.

## Domain Gating
Only domains listed in `domains.enabled` are active. Signals for disabled domains are stored but excluded from recommendations.

## First-Party Precedence
First-party behavioral evidence (actual consumption) always outweighs enriched or inferred metadata.

## Cross-Domain Linking
Cross-domain links are allowed only when the explanation is concrete and specific. "You liked X restaurant, and Y hotel has a similar design aesthetic based on your visits to both" is acceptable. "People who like X also like Y" without personal evidence is not.
