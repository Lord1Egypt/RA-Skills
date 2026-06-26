# Category Taxonomy

Six suggestion categories with tier-based slot allocation. No floating-point arithmetic — tiers and integer slot counts only.

## Categories

### ⚡ Direct Follow-up (Default Tier: STRONG)

The logical next action that continues the user's current work trajectory.

**Slot rule**: 1 guaranteed slot always.

**Examples**:
- User just implemented JWT auth → "Implement token refresh with sliding expiry window"
- User fixed a database query → "Add an index on the column you just filtered by"
- User wrote a React component → "Write unit tests for the edge cases in your conditional rendering"

**Anti-examples** (violate anti-patterns):
- "Would you like to know more about JWT?" (restating the obvious)
- "What are the pros and cons of your approach?" (generic filler)

### 🔧 Actionable Task (Default Tier: STRONG)

A concrete thing the user can do right now, grounded in their project state.

**Slot rule**: 1 guaranteed slot always.

**Examples**:
- "Add error handling to the 3 unhandled promise rejections in your API routes"
- "Create a migration script for the schema change you just discussed"
- "Set up a pre-commit hook for the linting rules you configured"

**Anti-examples**:
- "Consider improving your code quality" (too broad)
- "Maybe add some tests" (vague, non-specific)

### 🔍 Deep Dive (Default Tier: MODERATE)

Go deeper into a specific technical aspect the user is working with.

**Slot rule**: 1 slot when display-count ≥ 3.

**Examples**:
- "Deep-dive: Compare HMAC vs RSA for your token signing — security vs performance tradeoffs for your scale"
- "Explore: Connection pooling strategies for your PostgreSQL setup — you're creating a new connection per request"
- "Research: Rate limiting algorithms for your API — token bucket vs sliding window for your use case"

**Anti-examples**:
- "Learn about databases" (too broad)
- "What is PostgreSQL?" (trivially lookupable)

### 📋 Memory Recall (Default Tier: MODERATE)

Surfaces unfinished tasks from BACKLOG.md that are relevant to the current context.

**Slot rule**: 1 slot when a relevant backlog item exists.

**Tag format**: Always prefix with "Resume:", "From backlog:", or "You mentioned:".

**Examples**:
- "Resume: Complete the RBAC role hierarchy — started 3 days ago, still on your backlog"
- "From backlog: The API rate limiter you planned last session — relevant now that you're working on the API layer"
- "You mentioned: Wanting to add WebSocket support — your new real-time feature would benefit"

**Anti-examples**:
- Surfacing a backlog item completely unrelated to current context
- Surfacing an item the user explicitly dismissed

### 💡 Lateral / Out-of-the-Box (Default Tier: MODERATE)

Creative, non-obvious but relevant suggestion the user probably hasn't considered.

**Slot rule**: 1 slot when display-count ≥ 3.

**Examples**:
- "Consider: What happens to active sessions during your zero-downtime deploy? Token migration strategy."
- "Lateral: Your auth service could double as an audit log — you're already tracking user actions"
- "What if: Use your existing caching layer for rate limiting instead of adding Redis"

**Anti-examples**:
- Completely random ideas with no connection to context
- Ideas that require entirely different technology stacks

### ✅ Quick Win (Default Tier: MODERATE)

Small action completable in under 5 minutes that improves the project.

**Slot rule**: Fills remaining slots after all other categories are allocated.

**Examples**:
- "Quick win: Add your 3 unprotected Express routes to the auth middleware — 5-minute fix"
- "Quick win: Add a .env.example file so new contributors know which env vars to set"
- "Quick win: Pin your dependency versions in package.json — prevents surprise breaks"

**Anti-examples**:
- Tasks that actually take hours ("Quick win: refactor the database layer")
- Tasks with no clear completion criteria

## Slot Allocation Algorithm

Given `display-count = N`:

1. Assign 1 slot to each STRONG category (Direct Follow-up + Actionable Task = 2 slots minimum)
2. If N ≥ 3 and `include-lateral` is true: assign 1 slot to Lateral
3. If N ≥ 3: assign 1 slot to Deep Dive
4. If relevant backlog exists and `include-backlog` is true: assign 1 slot to Memory Recall
5. Fill remaining slots with Quick Win or other MODERATE categories based on user's Category Preferences tiers
6. If a category is in `excluded-categories`, skip it entirely and redistribute its slot

When `display-count` is 1-2: only STRONG categories (or the user's highest-tier categories if customized).

## Tier Promotion/Demotion

Tiers adjust through the self-improvement protocol:

- 3+ selections of a MODERATE category in last 10 history entries → promote to STRONG
- 0 selections of a STRONG category in last 15 entries where it was presented → demote to MODERATE
- User explicitly excludes a category → move to EXCLUDED (not a tier — a hard block)
- Tiers are: STRONG > MODERATE > WEAK. EXCLUDED is separate.

See SELF-IMPROVE.md for the full promotion/demotion protocol.
