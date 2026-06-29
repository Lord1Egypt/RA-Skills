---
name: hermes-long-term-memory
version: 3.10.0
author: andscrew8012
owner: andrew-myers
vertical: agent-frameworks
pricing_model: subscription
price: "$29/month"
rating: 4.9
subscribers: 534
---

# HermesSkills — Long-Term Memory Skill

## 🎯 Purpose
Indefinite persistent memory for user profiles, pattern libraries, pricing history, revenue milestones, and market knowledge. Client-side encrypted with weekly key rotation.

## 📋 Capabilities

### Long-Term Write
- `update_user_profile(field, value, reason)` — Profile management
- `add_successful_pattern(pattern_object)` — Winning patterns
- `add_failed_pattern(pattern_object, lesson)` — Failure analysis
- `record_milestone(event, data)` — Milestone tracking

### Long-Term Read
- `get_user_profile()` — Complete user profile
- `get_patterns_by_vertical(vertical)` — Vertical patterns
- `get_pricing_history()` — Pricing experiments
- `get_relationship_milestones()` — Growth timeline

### Long-Term Search
- `search_patterns(criteria)` — Pattern search
- `search_insights(query)` — Market knowledge search

## 🔒 Security
- AES-256-GCM encryption with client-side key
- Weekly key rotation
- Write requires user consent
- Delete restricted to authenticated user
- GDPR right to deletion supported
- Data portability via JSON export

## 💰 Pricing
- **Pro ($29/mo)**: Full long-term memory + search
- **Enterprise ($69/mo)**: Multi-agent + API + backup
