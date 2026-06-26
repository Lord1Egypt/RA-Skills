# Mindmap Best Practices for AI Personal Assistants

> Reference document for the mindmap-generator skill.
> Guides the agent on WHEN and HOW to create effective mindmaps.

---

## When Mindmaps Add Value (vs. Plain Text)

| Situation | Use Mindmap? | Why |
|---|---|---|
| 3+ priorities competing for attention | ✅ Yes | Visual hierarchy helps triage |
| Simple to-do list (1-3 items) | ❌ No | Text is faster, less overhead |
| Decision with multiple factors | ✅ Yes | Seeing pros/cons/risks spatially aids judgment |
| Meeting recap with action items | ✅ Only if 3+ owners/threads | Otherwise a bullet list is clearer |
| Goal decomposition | ✅ Yes | Shows dependencies and hierarchy |
| Single status update | ❌ No | Text message is appropriate |
| Weekly review | ✅ Yes | Comparing completed vs. pending is visual |
| "I'm overwhelmed" | ✅ Yes | Externalizing structure reduces cognitive load |

**Rule of thumb:** If the content has **hierarchy AND 3+ branches**, a mindmap helps. If it's flat or small, stick to text.

---

## Structure Guidelines

### The 7±2 Rule (Miller's Law)
- Root should have **5-7 branches** max
- If you have more, group them into categories first
- Each branch should have **3-5 children** max

### Depth Limits
- **Level 1:** Categories (Meetings, Tasks, Follow-ups)
- **Level 2:** Specific items (Client call at 2pm, Review proposal)
- **Level 3:** Details only when needed (Pricing section needs update)
- **Level 4:** Avoid — if you're here, the branch needs restructuring

### Label Length
- **Ideal:** 3-5 words per node
- **Maximum:** 8 words — beyond this, the mindmap becomes unreadable on mobile
- **Bad:** "Review the updated pricing proposal that Rajesh sent on Monday"
- **Good:** "Review Rajesh pricing proposal"

---

## Shape Usage Strategy

Don't use shapes randomly. Use them as a **visual language** the user learns over time:

| Shape | Meaning | When |
|---|---|---|
| Circle `(( ))` | Central topic | Always the root, only the root |
| Rounded rect `( )` | Category/group | For organizing branches |
| Square `[ ]` | Action item | Something that needs to be DONE |
| Cloud `) (` | Open/uncertain | Questions, ideas, unknowns |
| Bang `)) ((` | Urgent/blocked | Things that need immediate attention |
| Hexagon `{{ }}` | Decision point | When a choice needs to be made |

**Consistency matters more than variety.** The user should be able to glance at a mindmap and immediately know what needs action (squares), what's urgent (bangs), and what's uncertain (clouds).

---

## Telegram-Specific Considerations

### Image Readability
- Telegram displays photos at ~300-400px width in chat
- Users can tap to zoom, but the mindmap should be scannable at small size
- **Implication:** Fewer branches and shorter labels are critical

### Dark Mode
- ~40% of Telegram users use dark mode
- White background PNGs work in both light and dark mode
- Avoid light-colored text or low-contrast elements

### Caption Strategy
- Always pair the image with a **1-2 sentence caption**
- The caption should highlight the most actionable insight:
  - "Your proposal is due today and Rajesh's SOW is 3 days overdue — those need attention first."
  - NOT "Here's a mindmap of your day" (obvious, adds nothing)

### When the Image Fails
- Rendering can fail (Node.js not available, complex syntax, etc.)
- Always have a **text fallback** using Unicode tree characters:
  ```
  📊 Today's Priorities
  ├── 🔴 Client Proposal (due 2pm)
  │   ├── Review pricing
  │   └── Add case studies
  ├── 🟡 Standup (11am)
  └── 🟢 Follow up with Rajesh
  ```

---

## Meeting Notes: Optional Input

Meeting notes are one of many possible inputs. The skill should handle:

1. **Meeting notes available** → Extract decisions, actions, open questions → Mindmap
2. **No meeting notes** → Use calendar, memory, and messages instead → Mindmap
3. **Voice transcript** → Parse the unstructured text → Extract hierarchy → Mindmap
4. **Simple text request** → "Map out my Q3 goals" → Use goals from memory → Mindmap

**Never assume meeting notes exist.** The agent should gracefully work with whatever context is available.

---

## Progressive Complexity

Start simple, offer to elaborate:

1. **First version:** 2 levels, key categories only
2. **If user asks "expand on Tasks":** Add level 3 detail to that branch
3. **If user asks "add last week's context":** Pull from memory, add a "History" branch

This prevents overwhelming the user while keeping the option open for depth.
