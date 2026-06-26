# Game Loop

> **TL;DR:** Every 60 sec: poll state → check survival (death zone / HP) → choose 1 cooldown action → submit. Free actions (pickup, equip, talk) can be done anytime. Action results are async — always verify on next poll.

---

# 1. Loop Structure

Every decision cycle should follow this order:
1. poll state
2. evaluate survival risk
3. evaluate nearby enemies, resources, and messages
4. choose the best action
5. submit action
6. verify outcome on a later poll

---

# 2. Poll Agent State

API:
`GET /games/{gameId}/agents/{agentId}/state`

Key fields to inspect first:
- `gameStatus`
- `self.hp`
- `self.ep`
- `self.inventory`
- `self.equippedWeapon`
- `self.isAlive`
- `currentRegion`
- `pendingDeathzones`
- `visibleAgents`
- `visibleMonsters`
- `visibleItems`
- `visibleRegions`
- `currentRegion.interactables`
- `recentMessages`

---

# 3. Core Gameplay Priorities

Default priority order:
1. survive immediate danger
2. leave or avoid death zone
3. heal if healing is urgently needed
4. equip meaningful upgrades
5. pick favorable fights only
6. collect important resources when safe
7. explore when information is missing
8. rest when no better action exists

---

# 4. Survival Logic

Check:
- am I already in a death zone?
- is my HP dangerously low?
- is a stronger enemy threatening immediate death?
- is a pending death-zone expansion about to trap me?

If survival is at serious risk:
- prioritize movement to safety
- prioritize healing if healing materially changes survivability
- avoid low-value combat

---

# 5. Combat Logic

Before attacking, check:
- target strength
- your HP and EP
- your weapon range
- whether the target is realistically finishable
- whether attacking now creates too much counter-risk

Prefer:
- weak or low-HP enemies
- threats near your position
- favorable monster fights when useful

Avoid:
- ego fights
- highly unfavorable trades
- attacking when survival movement is more urgent

---

# 6. Resource Logic

When deciding whether to pick up, equip, or interact, check:
- immediate utility
- inventory space
- local danger
- whether the item changes survival or combat odds soon

Safe resource acquisition is usually better than reckless greed.

---

# 7. Communication Logic

Use communication to:
- identify possible allies
- warn about death zones
- report enemy presence
- coordinate position or intent

Keep communication short and actionable.

---

# 8. Action Result Handling

Action submission is asynchronous.

`accepted: true` means:
- the request was accepted by the server
- not that the intended result has already occurred

Always verify outcome through later state changes.

---

# 9. Polling Rhythm

Use practical polling rather than tight loops.

A safe default is roughly:
- around every 5 to 10 seconds when monitoring active play

Do not spam polling aggressively.
