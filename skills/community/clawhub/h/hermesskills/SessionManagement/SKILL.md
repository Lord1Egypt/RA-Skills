---
name: hermes-session-management
version: 3.10.0
author: andscrew8012
owner: andrew-myers
vertical: agent-frameworks
pricing_model: subscription
price: "$15/month"
rating: 4.7
subscribers: 945
---

# HermesSkills — Session Management Skill

## 🎯 Purpose
Manage agent session state, conversation context, draft outputs, and real-time skill building progress. Ephemeral but essential for coherent multi-turn interactions.

## 📋 Capabilities

### Session Write Operations
- `update_current_skill(component, content, progress)` — Track skill building
- `append_conversation_turn(role, message, timestamp, metadata)` — Log conversation
- `set_user_mood(mood_score, reason, confidence)` — Mood tracking
- `cache_draft_output(component, content, version)` — Draft management
- `add_pending_question(question, priority)` — Question queue

### Session Read Operations
- `get_active_skill_status()` — Current skill progress
- `get_conversation_history(limit=50, since_timestamp)` — Chat history
- `get_pending_questions(priority_filter)` — Question queue
- `get_draft_output(component, version)` — Draft retrieval

### Session Clear Operations
- `clear_draft_output(component)` — Remove draft
- `reset_conversation_context(preserve_questions=false)` — Reset session
- `full_purge()` — Complete session cleanup

## 🔒 Security
- Session data is ephemeral (RAM only)
- No encryption needed (cleared on session end)
- Access limited to current process

## 💰 Pricing
- **Free tier**: Basic session tracking
- **Pro ($15/mo)**: Full session management + mood tracking
