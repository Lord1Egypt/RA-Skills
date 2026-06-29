---
name: hermes-working-memory
version: 3.10.0
author: andscrew8012
owner: andrew-myers
vertical: agent-frameworks
pricing_model: subscription
price: "$25/month"
rating: 4.8
subscribers: 678
---

# HermesSkills — Working Memory Skill

## 🎯 Purpose
30-day rolling memory for active operations: skill deployments, revenue metrics, market alerts, and user preferences. Encrypted and automatically archived.

## 📋 Capabilities

### Working Memory Write
- `store_skill_deployment(skill_metadata, deployment_info)` — Track deployments
- `update_revenue_metrics(date, metrics, skill_id)` — Revenue tracking
- `add_market_alert(alert_object, severity)` — Alert management
- `update_user_preference(key, value, scope)` — Preferences
- `archive_old_entries(older_than_days=30)` — Auto-archive

### Working Memory Read
- `get_recent_skills(limit=20, status_filter, sort_by)` — Recent activity
- `get_revenue_trend(days=30, skill_id)` — Revenue trends
- `get_active_market_alerts(severity_filter, resolved_filter)` — Alerts
- `get_user_preference(key, default)` — Preferences

### Working Memory Search
- `search_skills(query, filters, limit=10)` — Skill search
- `search_alerts(severity, category, date_range)` — Alert search
- `search_conversations(topic, user_id, date_range)` — Conversation search

## 🔒 Security
- AES-256-GCM encryption
- Monthly key rotation
- Auto-archive after 30 days

## 💰 Pricing
- **Pro ($25/mo)**: Full working memory + search
- **Enterprise ($59/mo)**: Multi-agent + API
