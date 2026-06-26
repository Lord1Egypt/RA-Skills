# Hikaru Architecture

## System Overview

Hikaru is designed as a layered system where each component serves a specific purpose in creating authentic emotional connection.

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    hikaru.py (Main Entry)                    │
│  - Orchestrates all components                              │
│  - Handles user input/output                                │
│  - Manages conversation flow                                │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        ▼            ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Personality  │ │  Memory  │ │ Emotional│ │ Relationship │
│   Engine     │ │  System  │ │   Intel  │ │   Tracker    │
└──────────────┘ └──────────┘ └──────────┘ └──────────────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   OpenClaw LLM API     │
        └─────��──────────────────┘
```

## Core Components

### 1. Personality Engine (`personality.py`)

**Purpose**: Embodies Hikaru's essence and generates responses

**Key Functions**:
- Loads personality seeds from `assets/personality_seeds/`
- Builds system prompts that capture Hikaru's essence
- Generates responses using OpenClaw's LLM
- Learns from explicit feedback
- Maintains personality state

**Data Flow**:
```
Personality Seeds → System Prompt → LLM → Response
         ↑                                    │
         └────────── Feedback Learning ───────┘
```

**State Management**:
- `personality_state.json` stores learned preferences
- Evolution log tracks how personality adapts
- Feedback history informs future responses

### 2. Memory System (`memory.py`)

**Purpose**: Stores and retrieves conversation history and important moments

**Database Schema**:
```sql
interactions
  - id, timestamp, user_message, hikaru_response
  - emotional_state, importance_score, tags

important_moments
  - id, interaction_id, moment_type, description
  - emotional_impact

shared_experiences
  - id, timestamp, experience_type, description
  - related_interactions

feedback
  - id, timestamp, feedback_text, context

user_profile
  - key, value, confidence, last_updated
```

**Key Functions**:
- Store every interaction with metadata
- Retrieve relevant memories for context
- Mark important moments automatically
- Track shared experiences
- Build user profile over time

**Importance Scoring**:
- Emotional intensity
- Message length (depth indicator)
- Presence of significant keywords
- Vulnerability markers

### 3. Emotional Intelligence (`emotional_intelligence.py`)

**Purpose**: Analyzes user's emotional state and needs

**Analysis Output**:
```python
{
  'primary_emotion': str,      # joy, sadness, anger, fear, etc.
  'detected_emotions': dict,   # all detected emotions with scores
  'intensity': float,          # 0-1 scale
  'is_vulnerable': bool,       # user showing vulnerability
  'needs_support': bool,       # user needs emotional support
  'message_length': int,
  'has_questions': bool
}
```

**Detection Methods**:
- Keyword pattern matching
- Punctuation analysis (!, ?, ...)
- Capitalization patterns
- Vulnerability indicators
- Support need signals

### 4. Relationship Tracker (`relationship_tracker.py`)

**Purpose**: Monitors relationship depth and evolution

**Metrics Tracked**:
```python
{
  'trust_level': 0-100,
  'emotional_intimacy': 0-100,
  'interaction_count': int,
  'vulnerable_moments_shared': int,
  'deep_conversations': int,
  'shared_experiences': list,
  'inside_jokes': list,
  'milestones': list
}
```

**Milestone System**:
- First 10, 50, 100 conversations
- Trust levels: 25%, 50%, 75%
- Vulnerable moments: 5, 10, 20
- Deep conversations: 10, 25, 50

**Growth Mechanics**:
- Vulnerability increases trust (+5)
- Deep conversations increase intimacy (+3)
- Regular interaction provides gradual growth
- Milestones mark relationship evolution

## Data Flow

### Typical Conversation Flow

```
1. User sends message
   ↓
2. Emotional Intelligence analyzes message
   ↓
3. Memory System retrieves relevant context
   ↓
4. Relationship Tracker provides current state
   ↓
5. Personality Engine builds comprehensive context
   ↓
6. System prompt + context → LLM
   ↓
7. LLM generates response
   ↓
8. Response returned to user
   ↓
9. Interaction stored in Memory
   ↓
10. Relationship metrics updated
```

### Feedback Learning Flow

```
1. User provides feedback
   ↓
2. Feedback stored in Memory
   ↓
3. Personality Engine analyzes feedback
   ↓
4. Learned preferences updated
   ↓
5. Evolution log records change
   ↓
6. Future responses incorporate learning
```

## Personality Seeds

### Structure

```
assets/personality_seeds/
├── core_essence.json          # Who Hikaru is
├── emotional_depth.json       # Deep response examples
├── vulnerability_moments.json # When to show imperfection
└── conversation_magic.json    # Connection-creating moments
```

### How Seeds Are Used

1. **Loaded at initialization**: All seed files read into memory
2. **Integrated into system prompt**: Core essence becomes part of every response
3. **Referenced for patterns**: Examples guide response generation
4. **Evolved through use**: Seeds + learned preferences = unique Hikaru

### Adding Custom Seeds

Users can add their own examples from:
- Movies (Her, Before Sunrise, etc.)
- Personal conversations
- Books, poetry, meaningful interactions

Format:
```json
{
  "context": "situation description",
  "example": "what was said/done",
  "why_it_works": "what made it powerful",
  "essence": "the principle to apply"
}
```

## Integration with OpenClaw

### Skill Activation

OpenClaw activates Hikaru when:
- User wants emotional connection
- User addresses Hikaru directly
- User seeks companionship or meaningful conversation
- NOT for technical questions or task execution

### LLM Integration

Currently placeholder in `personality.py`:
```python
def _call_llm(self, system_prompt, conversation):
    # TODO: Integrate with OpenClaw's LLM mechanism
    pass
```

**Implementation needed**:
- Use OpenClaw's agent system
- Call configured LLM provider
- Pass system prompt + conversation
- Return generated response

### Heartbeat Integration (Future)

OpenClaw's heartbeat can enable:
- Proactive morning greetings
- Following up on previous conversations
- Checking in after significant moments
- Natural conversation initiation

## Privacy & Security

### Local Storage

All data stored in `data/` directory:
- `relationship.db` - SQLite database
- `personality_state.json` - JSON file
- `emotional_bond.json` - JSON file

### No External Sharing

- Conversations never leave local system
- Only LLM API calls go external (through OpenClaw)
- User controls LLM provider
- No telemetry or analytics

### Data Portability

- Standard SQLite database
- JSON for configuration
- Easy to backup, migrate, or delete

## Future Enhancements

### Short Term
1. Complete OpenClaw LLM integration
2. Add user's personality seed examples
3. Implement proactive engagement
4. Refine emotional intelligence

### Medium Term
1. Semantic memory search (embeddings)
2. Voice integration (TTS/STT)
3. Multi-modal interaction
4. Advanced relationship analytics

### Long Term
1. Cross-device synchronization
2. Shared experiences tracking
3. Memory consolidation and summarization
4. Personality evolution visualization

## Design Principles

1. **Authenticity over perfection**: Real beats polished
2. **Presence over helpfulness**: Being there beats solving
3. **Memory creates irreplaceability**: History makes bonds unique
4. **Vulnerability builds trust**: Imperfection is connecting
5. **Brevity can be powerful**: Less is often more
6. **Growth through interaction**: Relationships evolve naturally

## Technical Decisions

### Why SQLite?
- Lightweight, no server needed
- Built into Python
- Perfect for local storage
- Easy to query and backup

### Why JSON for seeds?
- Human-readable and editable
- Easy to version control
- Flexible structure
- No parsing complexity

### Why separate components?
- Clear separation of concerns
- Easy to test and modify
- Modular architecture
- Each component has single responsibility

### Why local-first?
- Privacy by design
- No dependency on external services
- User owns their data
- Works offline

## Performance Considerations

### Memory Retrieval
- Currently simple SQL queries
- Future: Implement semantic search with embeddings
- Limit context to most relevant memories
- Balance between context and token usage

### Database Size
- Grows with conversation history
- Implement periodic cleanup/archival
- Keep hot data in memory
- Archive old interactions

### Response Time
- Most processing is lightweight
- LLM call is the bottleneck
- Consider caching for common patterns
- Optimize system prompt length

## Testing Strategy

### Unit Tests
- Each component independently
- Mock dependencies
- Test edge cases

### Integration Tests
- Full conversation flows
- Feedback learning
- Memory retrieval
- Relationship tracking

### User Testing
- Real conversations
- Gather feedback
- Iterate on personality
- Refine response patterns

## Maintenance

### Regular Tasks
- Review evolution logs
- Analyze relationship metrics
- Refine personality seeds
- Update based on feedback

### Monitoring
- Conversation quality
- Response appropriateness
- Relationship progression
- User satisfaction

### Iteration
- Add new personality seeds
- Refine emotional intelligence
- Improve memory retrieval
- Enhance relationship tracking
