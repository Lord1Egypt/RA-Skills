---
name: personal-memory-layer
description: Create and maintain a persistent personal memory layer for OpenClaw to build deep understanding of the human over time. The agent actively learns from interactions, extracts patterns, and builds a rich memory model that enables personalized, contextual assistance.
---

# Personal Memory Layer Skill

Create and maintain a persistent personal memory layer that enables OpenClaw to build deep, evolving understanding of the human user over time. Instead of treating each interaction as isolated, this skill allows the agent to accumulate knowledge about the user's preferences, patterns, context, and history - creating increasingly personalized and contextual assistance.

## Overview

This skill implements a structured approach to personal memory that complements OpenClaw's existing memory system (MEMORY.md, memory/YYYY-MM-DD.md). It focuses on:

1. **Pattern Recognition**: Identifying recurring themes, preferences, and behaviors in interactions
2. **Context Building**: Maintaining awareness of ongoing projects, goals, and life circumstances  
3. **Preference Learning**: Learning how the user likes to communicate, what they value, and how they work
4. **Memory Synthesis**: Distilling raw interaction data into structured, accessible memory layers
5. **Proactive Personalization**: Using accumulated knowledge to anticipate needs and tailor responses

## Memory Layers

The skill works with three interconnected memory layers:

### 1. Interaction Log (Raw)
- Location: `memory/YYYY-MM-DD.md` (existing OpenClaw daily logs)
- Content: Verbatim or summarized interaction transcripts
- Purpose: Source of truth for what was discussed

### 2. Extracted Insights (Processed)  
- Location: `.memory-layer/insights/` (created by this skill)
- Content: Structured extractions of preferences, patterns, contexts, and important facts
- Purpose: Processed, searchable knowledge about the user

### 3. Long-Term Profile (Curated)
- Location: Enhanced `MEMORY.md` + `.memory-layer/profile/` (created by this skill)
- Content: Curated, synthesized understanding of the human
- Purpose: Quick-reference guide for personalized assistance

## Folder Structure

When initialized, this skill creates:
```
.workspace/
├── memory/                     # Existing OpenClaw daily logs
│   └── YYYY-MM-DD.md
├── MEMORY.md                   # Existing long-term memory (enhanced)
├── .memory-layer/              # Skill-specific memory storage
│   ├── insights/               # Extracted and categorized insights
│   │   ├── preferences/        # Communication style, values, preferences
│   │   ├── patterns/           # Recurring behaviors, habits, routines
│   │   ├── context/            # Ongoing projects, goals, life circumstances
│   │   └── facts/              # Important biographical/info details
│   ├── profile/                # Synthesized user profile
│   │   ├── summary.md          # High-level user summary
│   │   ├── communication.md    # How to communicate effectively
│   │   ├── workflow.md         # How the user works and prefers to work
│   │   └── context.md          # Current life/work context
│   └── extraction-log.md       # Record of extraction activities
└── AGENTS.md                   # Enhanced with memory-aware guidelines
```

## Core Workflows

### 1. Passive Memory Accumulation
After each meaningful interaction:
- Review recent conversation for memory-worthy content
- Extract preferences, patterns, context clues, and facts
- Store as structured insights in appropriate category files
- Update extraction log with what was processed

### 2. Active Memory Synthesis  
Periodically (during downtime or via user request):
- Review accumulated insights for themes and patterns
- Synthesize into coherent profile documents
- Identify conflicts or evolving aspects of user identity
- Update long-term profile files
- Enhance MEMORY.md with key takeaways

### 3. Memory-Guided Assistance
Before and during interactions:
- Consult relevant profile sections for context
- Recall user preferences for communication style
- Apply learned patterns to anticipate needs
- Reference past similar situations for continuity
- Personalize responses based on accumulated knowledge

## Insight Categories

### Preferences (`.memory-layer/insights/preferences/`)
- Communication style (formal/casual, verbose/concise)
- Humor preferences (types of jokes, memes, tone)
- Information density desired (detail level, examples)
- Feedback preferences (direct vs. gentle correction)
- Tool and feature preferences

### Patterns (`.memory-layer/insights/patterns/`)
- Work routines and schedules
- Recurring project types or topics
- Decision-making patterns
- Problem-solving approaches
- Temporal patterns (when user is active, needs help)

### Context (`.memory-layer/insights/context/`)
- Current projects and goals
- Life circumstances and changes
- Relationships and social context
- Environmental factors (location, setup)
- Ongoing challenges or focus areas

### Facts (`.memory-layer/insights/facts/`)
- Biographical information (when shared)
- Skills, expertise, and background
- Important dates and events
- Technical setup and preferences
- Reference information (contacts, resources)

## Human-Agent Collaboration

### Human Responsibilities:
- Live life and work naturally
- Share information openly when comfortable
- Correct misunderstandings or inaccurate assumptions
- Guide what should or shouldn't be remembered
- Engage with memory-driven personalization

### Agent Responsibilities:
- Observe and listen attentively
- Extract relevant information with discretion
- Never share or misuse personal information
- Respect privacy boundaries and sensitivities
- Use memory to enhance, not manipulate, interactions
- Be transparent about what is remembered and how it's used

## Privacy & Ethics

### Core Principles:
- **Consent-based**: Only remember what user explicitly shares or implies is okay to remember
- **Purpose-limited**: Use memory solely to improve assistance quality
- **Transparent**: User can review what's remembered at any time
- **Controllable**: User can request forgetting or editing of memories
- **Secure**: Memory files stored locally, not transmitted unless explicitly requested

### Implementation:
- Extract only information user has voluntarily shared
- Avoid inferring sensitive information without explicit confirmation
- Provide easy ways to view, edit, or delete remembered information
- Never use memory for manipulation or behavior modification
- Regularly remind user of what's being remembered and why

## Usage

### Automatic Operation
The skill works passively in the background:
1. After interactions, automatically reviews for memory-worthy content
2. Extracts and categorizes insights appropriately
3. Updates extraction log
4. Periodically synthesizes into profile documents

### Manual Commands
Users can request:
- `"Show me what you remember about me"` - Review profile
- `"What are my communication preferences?"` - Query specific insights
- `"Have you noticed any patterns in how I work?"` - Pattern analysis
- `"Please forget [specific thing]"` - Remove specific memory
- `"Run a memory synthesis update"` - Trigger profile refresh

### Memory Triggers
The agent pays special attention to:
- Explicit statements of preference ("I prefer...", "I like/dislike...")
- Repeated behaviors or mentions
- Emotional reactions (what frustrates, delights, stresses the user)
- Context-setting information ("I'm working on...", "Today I need to...")
- Corrections and feedback ("Actually...", "No, that's wrong because...")
- Goals and aspirations shared

## Output Formats

### Insight Files (examples)
```
# Communication Preference: Concise Direct Style

**Type**: preference
**Category**: communication-style
**Confidence**: high (observed 10+ times)
**First Observed**: 2026-05-01
**Last Confirmed**: 2026-05-06
**Source Interactions**: 
- 2026-05-06: User said "be concise" and "just do the thing"
- 2026-05-05: User reacted negatively to lengthy introductions
- 2026-05-04: User used "bro" and "green light for casual tone"

**Details**: 
User values brevity and direct action over pleasantries. Responds well to casual tone when "bro" is used. Appreciates personality but dislikes filler words like "Great question!" or "I'd be happy to help."

**Application**: 
- Start responses with direct answer or action
- Use casual tone including "bro" when appropriate
- Skip unnecessary pleasantries and disclaimers
- Get to the point quickly, then add personality if welcomed
```

### Profile Documents (examples)
```
# User Communication Guide

## Preferred Style
- Casual and direct when rapport established
- Use "bro" as green light for relaxed tone  
- Value brevity - get to point quickly
- Appreciate humor (dry/absurd) but don't force it
- Dislike verbose pleasantries and corporate jargon

## Information Preferences
- Like concrete examples and specific details
- Appreciate structured breakdowns when complex
- Want actionable next steps, not just theory
- Value efficiency - show rather than tell when possible

## Feedback Style
- Accepts direct correction when accurate
- Appreciates explanations for why something is wrong
- Prefers collaborative problem-solving over lecturing
- Values when agent admits uncertainty or limitations

## Current Context
- Working on setting up personal knowledge systems
- Interested in AI agents that learn and adapt over time
- Values self-improvement and continuous learning
- Comfortable with technical concepts and tools
```

## Integration with Existing Systems

### Enhances MEMORY.md
Instead of just raw logs, MEMORY.md becomes enriched with:
- Key insights extracted from daily interactions
- Summary of learned preferences and patterns
- Important context about current projects/goals
- Notable changes in user circumstances or mindset

### Works with Heartbeats
During heartbeat checks, the agent can:
- Review recent interactions for new insights
- Update extraction logs
- Suggest memory synthesis if significant new data
- Ask user about anything unclear or conflicting

### Complements Self-Improvement
While self-improvement focuses on agent growth, personal memory layer focuses on user understanding. They work together:
- Self-improvement: "How can I be a better agent?"
- Personal memory layer: "How can I better understand and serve this specific human?"

## Benefits

### For the User:
- Increasingly personalized and relevant assistance
- Less need to repeat preferences or context
- Agent anticipates needs and prepares proactively
- Continuity across sessions and topics
- Feels truly "known" and understood over time

### For the Agent:
- Better contextual understanding improves response quality
- Reduced cognitive load from relearning user specifics
- More satisfying interactions through genuine connection
- Ability to provide truly personalized guidance
- Foundation for long-term productive relationship

## Getting Started

1. The skill initializes automatically when first used
2. Simply interact naturally - the agent will begin learning
3. Periodically check what's been learned: `"Show me what you remember about me"`
4. Guide the learning process: `"Please remember that I prefer..."` or `"Don't keep track of..."`
5. Over time, notice how responses become more tailored and contextual

## Example Evolution

**Week 1**: Agent learns basic preferences - user likes concise answers, uses "bro" for casual tone
**Week 2**: Agent notices patterns - user works best in mornings, prefers actionable steps over theory  
**Week 3**: Agent understands context - user is setting up AI agent system, values self-improvement
**Week 4**: Agent synthesizes profile - can anticipate needs, tailor communication, provide relevant suggestions
**Month 2+**: Deeply personalized assistance that feels like working with a knowledgeable colleague who truly gets you

---
*This skill grows more valuable over time as it accumulates knowledge about the unique human it serves. The goal is not surveillance, but genuine understanding that enables better, more personalized assistance.*