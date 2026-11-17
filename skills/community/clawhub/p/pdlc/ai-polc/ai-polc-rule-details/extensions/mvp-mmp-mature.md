<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: MVP/MMP for Mature Products (Full Rules)

**Stage:** 7 (Release & Increment Slicing)
**Adds:** MMP scoping, version increment decision, migration epics, sunset planning

---

## When This Applies

A product is already live and serving users. The team is defining "what goes into the next major version." The challenge is different from 0→1 MVP:
- Existing users must not be broken
- Migration/compatibility is a real concern
- Some existing features may be deprecated
- "Minimum" now means "minimum to justify a new version" not "minimum to be viable"

---

## Additional Steps (extend Stage 7)

### Step 7.E1: MMP Criteria for Next Version

Ask: "What must be true for users to consider this a worthwhile new version?"

| Criterion | Description |
|-----------|------------|
| **New value** | At least {N} new capabilities that existing users want |
| **Quality bar** | No regression in existing functionality |
| **Migration path** | Clear upgrade path for existing users |
| **Market differentiation** | Something competitors don't have |
| **Stakeholder alignment** | Key stakeholders agree this justifies a version bump |

### Step 7.E2: Version Increment Decision

| Type | When | Example |
|------|------|---------|
| **Major** (v1→v2) | Breaking changes, significant new capabilities, new user segments | New payment engine replacing old |
| **Minor** (v1.1→v1.2) | New features, no breaking changes, backward compatible | Add crypto payments alongside existing |
| **Patch** (v1.2.1→v1.2.2) | Bug fixes, performance improvements, no new features | Fix payment timeout |

Decision: `POLC-D-NNN: Version {X} defined as {major|minor|patch} because {rationale}.`

### Step 7.E3: Migration/Compatibility Epics

For major versions, identify mandatory migration work:

| Migration Epic | Purpose | Blocking? |
|---|---|:---:|
| Data migration from v1 schema | Existing users don't lose data | ✅ Yes |
| API backward compatibility layer | v1 API consumers don't break | ✅ Yes |
| Feature flag for gradual rollout | De-risk the transition | No |
| Deprecation notices in v1 | Prepare users for change | No |

These epics enter the backlog and compete for priority like any other.

### Step 7.E4: Sunset/Deprecation Planning

For features being replaced in the new version:

| Feature Being Replaced | Replacement | Deprecation Timeline | Communication |
|---|---|---|---|
| Old payment flow | New async flow | v2 launch + 6 months sunset | In-app notice + email |
| Legacy API v1 | API v2 | v2 launch + 12 months | Developer notice + migration guide |

---

## Additional Output

When active, `release-plan.md` additionally contains:
- MMP criteria for the next version
- Version increment decision + rationale
- Migration/compatibility epic list
- Sunset/deprecation timeline
