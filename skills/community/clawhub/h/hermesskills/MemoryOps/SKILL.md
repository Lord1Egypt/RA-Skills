---
name: hermes-memory-ops
version: 3.10.0
author: andscrew8012
owner: andrew-myers
vertical: agent-frameworks
pricing_model: subscription
price: "$19/month"
rating: 4.8
subscribers: 1203
---

# HermesSkills — Memory Operations Skill

## 🎯 Purpose
Complete memory operations toolkit for Hermes Agents. Enables persistent context across sessions, revenue tracking, pattern learning, and intelligent recall.

## 📋 Capabilities

### Write Operations
- `update_user_profile(field, value, reason)` — Update user identity and preferences
- `add_successful_pattern(pattern_object)` — Record winning skill patterns
- `add_failed_pattern(pattern_object, lesson)` — Learn from failures
- `record_milestone(event, data)` — Track revenue and growth milestones
- `store_skill_deployment(skill_metadata, deployment_info)` — Track deployments
- `update_revenue_metrics(date, metrics, skill_id)` — Revenue tracking
- `add_market_alert(alert_object, severity)` — Market intelligence
- `update_user_preference(key, value, scope)` — Preference management

### Read Operations
- `get_user_profile()` — Full user profile with portfolio
- `get_patterns_by_vertical(vertical)` — Filtered pattern library
- `get_pricing_history()` — Pricing experiments and results
- `get_relationship_milestones()` — Growth timeline
- `get_recent_skills(limit, status_filter, sort_by)` — Recent skill activity
- `get_revenue_trend(days, skill_id)` — Revenue analytics
- `get_active_market_alerts(severity_filter, resolved_filter)` — Active alerts
- `get_user_preference(key, default)` — Preference retrieval

### Search Operations
- `search_patterns(criteria)` — Pattern library search
- `search_insights(query)` — Market knowledge search
- `search_skills(query, filters, limit)` — Skill search
- `search_alerts(severity, category, date_range)` — Alert search
- `search_conversations(topic, user_id, date_range)` — Conversation history

## 🔒 Security
- All write operations require authentication
- Long-term writes require user consent
- Delete operations restricted to authenticated user only
- AES-256-GCM encryption for all persistent data

## 💰 Pricing
- **Free tier**: Read operations only
- **Pro ($19/mo)**: Full read/write/search
- **Enterprise ($49/mo)**: Multi-agent + API
