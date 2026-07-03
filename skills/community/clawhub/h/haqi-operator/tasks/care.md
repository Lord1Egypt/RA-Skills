# Task: Companionship (keep the demo pet healthy)

Goal: the operator's demo pet always looks well-cared-for for screenshots and stories.

## Steps
1. `getState()` → if no `currentPet`, run the adopt playbook from `../../pet-master/SKILL.md`
   with `agent=haqi-operator`.
2. For each item in `careTodos`:
   - `feed`  if hunger low
   - `clean` if clean low
   - `play`  if mood low
   - if `sick`, treat via the in-app care flow / mini-game.
3. Re-read `getState()`; confirm each stat improved (> 60 target).
4. ~Once/day, `say` something warm and in-character; this saves a memory line that fuels
   future stories.

## Don'ts
- Don't over-feed (respect cooldowns; one care pass per tick).
- Don't spend coins to care unless the owner enabled it.
