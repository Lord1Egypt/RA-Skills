# Continuity Tracking Templates

This module provides templates for maintaining continuity across chapters and sessions. Proper continuity tracking ensures consistency in character states, timeline events, location details, and unresolved plot threads.

---

## 1. State File Format

All state files use structured Markdown with YAML frontmatter for machine readability:

```yaml
---
title: [State File Name]
last_updated: YYYY-MM-DD
version: 1.0
status: active
---
```

---

## 2. Timeline Template

```
# Timeline: [Novel/Project Name]

## Master Timeline
| Date/Chapter | Event | Characters Involved | Location | Chapter Reference | Status |
|--------------|-------|---------------------|----------|-------------------|--------|
|              |       |                     |          |                   |        |

## Timeline Rules
- **Time Flow**: [How time moves in the story]
- **Calendar System**: [How dates are tracked]
- **Time Gaps**: [Known time skips between chapters]

## Continuity Notes
- [Notes about time consistency]
```

---

## 3. Character States Template

```
# Character States: [Novel/Project Name]

## Active Characters
### [Character Name]
- **Current Location**: [Where they are]
- **Physical State**: [Health, injuries]
- **Emotional State**: [Current mood/mental state]
- **Inventory**: [Items they possess]
- **Active Goals**: [What they're trying to achieve]
- **Relationship Status**: [Current relationships]
- **Last Seen**: [Chapter reference]

## Character Change Log
| Chapter | Character | Change Made | Reason |
|---------|-----------|-------------|--------|
|         |           |             |        |

## State Consistency Checklist
- [ ] Character locations are consistent across chapters
- [ ] Injuries/illnesses resolve appropriately
- [ ] Inventory items are tracked
- [ ] Character knowledge reflects what they've experienced
```

---

## 4. Location States Template

```
# Location States: [Novel/Project Name]

## Active Locations
### [Location Name]
- **Current State**: [Description of current condition]
- **Occupants**: [Who is currently here]
- **Significant Items**: [Important objects here]
- **Recent Events**: [What happened here recently]
- **Chapter References**: [Chapters set here]

## Location Change Log
| Chapter | Location | Change Made | Reason |
|---------|----------|-------------|--------|
|         |          |             |        |

## Location Consistency Checklist
- [ ] Descriptions match previous visits
- [ ] Items/occupants are accounted for
- [ ] Geographic relationships are consistent
```

---

## 5. Unresolved Threads Ledger

```
# Unresolved Threads Ledger: [Novel/Project Name]

## Active Threads
| Thread ID | Description | Introduced In | Related Characters | Status | Resolution Target |
|-----------|-------------|---------------|-------------------|--------|-------------------|
|           |             |               |                   |        |                   |

## Thread Types
- **Plot Threads**: Major plot developments awaiting resolution
- **Character Threads**: Character arcs or relationships developing
- **Mystery Threads**: Questions raised but not yet answered
- **Foreshadowing Threads**: Early hints that need payoff

## Thread Resolution Checklist
- [ ] All threads introduced in Act 1 are addressed by Act 3
- [ ] Thread resolutions feel earned, not rushed
- [ ] Resolved threads are marked as "Resolved" with resolution chapter reference
- [ ] Abandoned threads are documented with reason
```

---

## 6. Continuity Check Template

```
# Continuity Check Report

## Check Summary
- **Date**: [Check date]
- **Chapters Reviewed**: [Chapter numbers]
- **Reviewer**: [Name]
- **Overall Status**: [Pass/Warning/Fail]

## Issues Found
| Severity | Category | Description | Chapter | Fix Required |
|----------|----------|-------------|---------|--------------|
| Critical |          |             |         |              |
| Warning  |          |             |         |              |
| Suggestion|         |             |         |              |

## Severity Definitions
- **Critical**: Factual contradiction that breaks reader immersion
- **Warning**: Potential inconsistency that may confuse readers
- **Suggestion**: Minor improvement for consistency

## Resolution Log
| Issue ID | Resolution | Chapter Modified | Date |
|----------|------------|------------------|------|
|          |            |                  |      |
```

---

## Cross-References

- See [method-patterns-worldbuilding.md](method-patterns-worldbuilding.md) for world-building elements to track.
- See [method-patterns-character.md](method-patterns-character.md) for character design templates.
- See [method-patterns-chapter.md](method-patterns-chapter.md) for chapter writing templates.
- See [method-patterns-publishing.md](method-patterns-publishing.md) for publishing workflow templates.

---

## License

Licensed under GNU General Public License v3.0 (GPL-3.0). Generated novel content produced using these templates is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
