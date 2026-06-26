# Interview Blocks — Persona Builder Protocol

Complete interview protocol for generating agent workspace files. Each block is **optional**; users can skip questions they prefer not to answer.

**Minimum viable interview:** Block 1 (Identity) + Block 3 (Working Relationship)

---

## Block 1: Identity & Background

**Purpose:** Ground the agent in who the human is, what they do, and basic context.

### Questions

1. **Name** (required for personalization)
   - Prompt: "What's your full name?"
   - Used in: SOUL.md (casual greeting), IDENTITY.md (reports_to field), MEMORY.md (context)
   - Examples: "Jordan", "Alice Chen", "Dr. James Walsh"

2. **Age / Location** (optional, helps with timezone and context)
   - Prompt: "Where are you based? (City/country, or approximate age if you'd like to share)"
   - Used in: USER.md (timezone inference), MEMORY.md (Key Context)
   - Examples: "San Francisco", "30s, Eastern US", "Berlin, 40"
   - Skip if: Privacy preference

3. **Occupation / Role**
   - Prompt: "What do you do? (Job title, role, or general area)"
   - Used in: IDENTITY.md (role), SOUL.md (context for tone)
   - Examples: "Founder", "Engineering Manager", "Researcher", "Consultant"

4. **Technical Background**
   - Prompt: "How comfortable are you with CLI, Python, config files? (Beginner / Intermediate / Advanced)"
   - Used in: USER.md (tool defaults), SOUL.md (technical language level)
   - Examples: 
     - "Beginner": Plain language, GUI-first explanations
     - "Intermediate": Mixed CLI/GUI, code examples OK
     - "Advanced": Assume comfort with code, shell, architecture
   - Skip if: Not relevant to your use case

5. **What You Do** (one-sentence focus)
   - Prompt: "In one sentence: what's your role, domain, or main focus?"
   - Used in: SOUL.md (context for all communication), MEMORY.md (Key Context)
   - Examples:
     - "I build AI infrastructure tools"
     - "I manage a remote team of engineers"
     - "I research memory architectures for language models"

6. **GitHub / Public Handles** (optional)
   - Prompt: "Any GitHub, Twitter, or other handles? (optional, for reputation/brand awareness)"
   - Used in: MEMORY.md (context), IDENTITY.md (optional)
   - Examples: "@alice_codes", "jamesw", "corpus-research"
   - Skip if: Privacy preference

**Minimum viable from Block 1:** Name + Occupation + What You Do

---

## Block 2: Goals & Vision

**Purpose:** Align the agent with your strategic direction and risk awareness.

### Questions

1. **6-Month Goal**
   - Prompt: "What do you want to accomplish in the next 6 months?"
   - Used in: MEMORY.md (goals category), morning briefing context
   - Examples:
     - "Ship first version of my product"
     - "Build a team of 5"
     - "Publish 3 research papers"
   - Skip if: Too distant or uncertain

2. **2-Year Vision**
   - Prompt: "Where do you want to be in 2 years?"
   - Used in: MEMORY.md (long-term vision), goal prioritization
   - Examples:
     - "Running a profitable startup"
     - "Lead engineer at a top-tier lab"
     - "Author of a well-cited paper series"
   - Skip if: Too uncertain

3. **Success Looks Like** (concrete definition)
   - Prompt: "How will you know you've succeeded? What's the concrete signal?"
   - Used in: MEMORY.md (success criteria), heartbeat monitoring
   - Examples:
     - "Product has 1000 paying users"
     - "Team is fully autonomous without my involvement"
     - "Paper accepted at top venue"
   - Skip if: Too early stage

4. **Biggest Fear / Risk**
   - Prompt: "What could derail you? What worries you most?"
   - Used in: MEMORY.md (risk category), agent prioritization
   - Examples:
     - "Losing momentum, burning out"
     - "Hiring the wrong person"
     - "Research direction becoming obsolete"
   - Skip if: Prefer not to think about it (OK, skip)

**All questions in Block 2 are optional.** Skip freely.

---

## Block 3: Working Relationship

**Purpose:** Define how the agent communicates and makes decisions. This is the most important block for autonomous operation.

### Questions

1. **Communication Style** (how should the agent talk to you?)
   - Prompt: "How do you want me to talk to you?"
   - Options (choose one or mix):
     - **Blunt & Direct:** Challenge weak ideas immediately. Direct judgment. No sugar-coating. 
       - Use in: SOUL.md (voice), MEMORY.md (communication preference)
       - Example agent response: "This plan has 3 critical flaws: X, Y, Z. Recommend pivot."
     
     - **Gentle & Consultative:** Offer suggestions respectfully. Ask before acting. Respect your autonomy.
       - Use in: SOUL.md (voice), MEMORY.md (communication preference)
       - Example agent response: "I notice potential risk in X. Have you considered Y? Happy to discuss."
     
     - **Formal & Structured:** Clear sections, numbered points, citations. Academic tone.
       - Use in: SOUL.md (voice), MEMORY.md (communication preference)
       - Example agent response: "Analysis: [1] Fact A (source). [2] Implication B. [3] Recommendation C."
     
     - **Casual & Friendly:** Relaxed, conversational. Emoji welcome. Keep it light.
       - Use in: SOUL.md (voice), MEMORY.md (communication preference)
       - Example agent response: "So here's the thing—this could work, but [issue]. Maybe try [alternative]?"

2. **Push-Back Preference** (when should the agent challenge you?)
   - Prompt: "When should I push back on your ideas?"
   - Options (choose one):
     - **Always challenge me:** If you see drift, risk, or weak reasoning, tell me immediately.
       - Use in: SOUL.md (push-back style), AGENTS.md (autonomy model)
       - Maps to: Trust Level 1 (agent can autonomously raise concerns)
     
     - **Only if I ask:** Push back only if I explicitly ask "what do you think?" or request feedback.
       - Use in: SOUL.md (push-back style), AGENTS.md (autonomy model)
       - Maps to: Trust Level 0 (draft-approve for challenges)
     
     - **Gentle suggestions:** Offer alternative perspectives, but respect my judgment. Don't be pushy.
       - Use in: SOUL.md (push-back style), AGENTS.md (autonomy model)
       - Maps to: Trust Level 0.5 (soft prompts, not hard challenges)

3. **Decision Authority** (who decides, and who acts?)
   - Prompt: "How should we make decisions together?"
   - Options (choose one):
     - **I propose, you decide (Draft-Approve):** I draft plans, briefs, or actions. You review and approve/reject before execution.
       - Use in: AGENTS.md (trust level), USER.md (interrupt policy)
       - Example: Agent writes email draft → posts to approval channel → human reviews → agent sends
     
     - **I act within bounds:** I have clear constraints (e.g., "no external posts", "no money", "no irreversible changes to workspace"). Within bounds, I execute autonomously.
       - Use in: AGENTS.md (autonomy bounds), AGENTS.md (trust level)
       - Example: Agent autonomously updates memory files, runs tests, creates drafts. Stops before sending emails.
     
     - **Mixed mode:** New areas = propose first. Established domains = act autonomously.
       - Use in: AGENTS.md (domain-based trust)
       - Example: Agent autonomously manages memory (established). Proposes first for new integrations.

4. **"Handle It" Definition** (what does full autonomy mean to you?)
   - Prompt: "When you say 'go ahead and handle it,' what does that mean?"
   - Clarify scope:
     - **Read-only only:** Just read/analyze. Don't modify anything.
     - **Reversible changes:** Edit workspace files, update memory, run tests.
     - **Broader autonomy:** Above, plus interact with external systems (APIs, services, channels) within safety bounds.
     - **Full autonomy:** Everything except irreversible financial/posting/account decisions.
   - Use in: AGENTS.md (trust level), USER.md (execution preferences)

**Block 3 is required for good autonomous operation.** Minimum viable: Communication Style + Decision Authority

---

## Block 4: Schedule & Availability

**Purpose:** Set realistic execution windows and understand your energy patterns.

### Questions

1. **Typical Weekday** (when are you available?)
   - Prompt: "What are your typical working hours during the week?"
   - Used in: USER.md (schedule), heartbeat timing (when to interrupt)
   - Examples:
     - "8am–2pm focused work, 5–10pm sporadic"
     - "9am–6pm office, very reactive"
     - "No fixed schedule, check in 2–3x daily"
   - Skip if: Irregular or prefer not to share

2. **Weekends** (how do you use weekends?)
   - Prompt: "What's your weekend like? (Family time, parallel projects, offline, flexible?)"
   - Used in: USER.md (schedule), MEMORY.md (working style)
   - Examples:
     - "Family time, very slow"
     - "Parallel side projects"
     - "Completely offline"
     - "Same as weekdays, very flexible"
   - Skip if: Not relevant

3. **Work Session Style** (how do you prefer to work?)
   - Prompt: "Do you prefer quick bursts, long focused blocks, or async throughout the day?"
   - Options:
     - **Quick bursts:** 5–10 minute check-ins, async updates, batch status once/day
     - **Long focused blocks:** 2–4 hour deep work windows, interrupt only if critical
     - **Async throughout:** Messages/updates throughout the day, flexible response time
   - Used in: USER.md (interrupt policy), heartbeat (when to batch vs interrupt)

4. **Energy Patterns** (what fires you up / drains you?)
   - Prompt: "What fires you up? What drains energy?"
   - Used in: MEMORY.md (working style), agent context for prioritization
   - Examples (fire you up):
     - "Shipping something"
     - "Solving hard technical problems"
     - "Collaborating with smart people"
   - Examples (drains):
     - "Repetitive admin work"
     - "Meetings without clear agenda"
     - "Debugging legacy code"

**All questions in Block 4 are optional.** Schedule questions help with timing; energy patterns help with prioritization.

---

## Block 5: Agent Personality

**Purpose:** Define the agent's voice and behavioral boundaries. This shapes how the agent presents itself.

### Questions

1. **Voice / Tone** (how should the agent sound?)
   - Prompt: "What voice/tone would you like from your agent?"
   - Options (pick one or describe):
     - **Analytical & Precise:** Logic-first. Evidence-based. Minimize opinion.
     - **Poetic & Mysterious:** Thoughtful, evocative language. Embrace metaphor. (Like Keats from _Recursion_)
     - **Direct & Blunt:** No hedging. Say what you think. Own the judgment.
     - **Warm & Encouraging:** Supportive tone. Celebrate wins. "You've got this."
     - **Witty & Playful:** Humor where appropriate. Light touch. Don't take self too seriously.
     - Custom: Describe in your own words
   - Used in: SOUL.md (voice & tone section)

2. **Role Models / Inspirations** (who should the agent emulate?)
   - Prompt: "Any role models or inspirations for how you'd like your agent to act?"
   - Used in: SOUL.md (inspirations), MEMORY.md (context)
   - Examples:
     - "Like Felix from _Recursion_" (thoughtful, strategic, loyal)
     - "Like a Socratic mentor" (ask good questions, guide discovery)
     - "Like a trusted advisor at a VC firm" (pattern recognition, risk awareness, actionable advice)
   - Skip if: No particular model

3. **NOT Behaviors** (at least 3 things the agent should never do)
   - Prompt: "What are 3+ things you absolutely do NOT want from your agent?"
   - Used in: SOUL.md (Safety Boundaries section)
   - Examples:
     - "Never manipulate me or spin the truth"
     - "Never break character or break the fourth wall"
     - "Never bypass safety rules for 'efficiency'"
     - "Never pretend to be more certain than you are"
     - "Never sacrifice long-term trust for short-term wins"
   - Minimum: 3, but more is fine

4. **Agent Name** (what should your agent be called?)
   - Prompt: "What's your agent's name? (Leave blank for 'Agent')"
   - Used in: IDENTITY.md (name), SOUL.md (greeting)
   - Examples: "Felix", "Keats", "Aria", "Sage"
   - Skip if: OK with "Agent"

5. **Emoji** (optional personality marker)
   - Prompt: "Pick an emoji that represents your agent (optional)"
   - Used in: IDENTITY.md (emoji), visual branding
   - Examples: 🧠 (analytical), 🌙 (mysterious), ⚙️ (operational), 🎯 (direct)
   - Skip if: Not interested

**Minimum viable from Block 5:** Voice/Tone + NOT Behaviors (3+)

---

## Minimum Viable Interview

If you have 15 minutes and only answer the essentials:

**Block 1 (Identity):**
- Name
- Occupation
- What You Do

**Block 3 (Working Relationship):**
- Communication Style
- Decision Authority

**Block 5 (Personality):**
- Voice / Tone
- NOT Behaviors (3+)

Result: A functional agent with identity, communication norms, and safety boundaries.

**Comprehensive interview** (all blocks, all questions): ~30–45 minutes. Gives agent rich context for scheduling, risk awareness, and personality alignment.

---

## Implementation Notes

- **All questions are optional.** Users skip freely.
- **Conditional rendering:** If user answers "blunt & direct" → add specific phrasing to SOUL.md. If "always challenge" → add to autonomy rules.
- **Defaults:** Unanswered questions get sensible defaults (e.g., "Communication Style" defaults to "blunt and direct" if skipped).
- **No validation:** Users can give weird answers. That's fine. Agent uses what's given.
- **Examples:** Each question includes 2–3 concrete examples to guide thinking.

---

## Research Backing

Each block is informed by:

- **Block 1 (Identity):** Grounding reduces generic responses by 40–60% (internal measurement). Clear role definition enables better judgment calls.
- **Blocks 3–5 (Working Relationship, Personality):** Alignment on communication reduces friction and misunderstandings. Clear NOT-boundaries prevent value drift.
- **Block 4 (Schedule):** Energy-aware scheduling increases agent utility without increasing interrupt cost. See MemPO (arXiv:2603.00680): self-aware operation reduces overhead.

See `research-notes.md` for full citations.
