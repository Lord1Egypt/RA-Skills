# Minecraft Mob Reference (Java Edition 1.21.x)

---

## Spawning Rules (General)

- **Hostile mobs**: light level ≤ 0 (1.18+; was ≤ 7 before)
- **Spawn check**: each game tick randomly selects chunks and attempts spawning
- **Player distance limits**: no spawns within 24 blocks; entities despawn beyond 128 blocks (exceptions: named or leashed mobs)
- **Mob cap**: each dimension has a mob cap; no further spawns when full (except dungeon spawners)

---

## Common Hostile Mobs

### Zombie
- Spawns: light level ≤ 0, all land biomes
- Health: 20
- Attack: melee; may spawn reinforcements on Hard difficulty
- **Drops**: rotten flesh (0–2), iron ingot (rare), carrot/potato (rare), iron equipment (rare)
- **Special**: burns in sunlight; zombie villagers can be cured (weakness potion + golden apple)

### Skeleton
- Health: 20
- Attack: bow (keeps distance), maintains optimal range while moving
- **Drops**: arrows (0–2), bones (0–2), skeleton skull (rare / creeper explosion kill)
- **Special**: burns in sunlight; flees when attacked by wolves

### Creeper
- Health: 20
- Attack: detonates when close (1.5s countdown; hitting interrupts)
- **Drops**: gunpowder (0–2); drops a music disc if killed by a skeleton
- **Special**: does not burn in sunlight; scared by cats; struck by lightning becomes charged creeper (2× explosion power)

### Spider
- Health: 16
- Attack: passive during daytime (unless provoked); hostile at light level ≤ 11
- **Drops**: spider eye (0–1, Bane of Arthropods effective), string (0–2)

### Enderman
- Health: 40, 2.9 blocks tall
- Attack: triggered by direct eye contact; teleports and pursues; high melee damage
- Weakness: damaged by water/rain; carved pumpkin helmet prevents aggro from eye contact
- **Drops**: ender pearl (0–1)
- **Special**: randomly picks up and places blocks; teleports to dodge projectiles

### Blaze
- Spawns only in Nether fortresses (from spawners)
- Health: 20, flying
- Attack: launches 3 fireballs (burst fire)
- **Drops**: blaze rod (0–1, Looting bonus) — essential for brewing stands
- Weakness: snowball damage (−3 HP/hit); water damage

### Witch
- Health: 26
- Attack: throws potions (damage/slowness/poison/weakness)
- Defense: drinks healing/regeneration/speed potions
- **Drops**: glass bottles, glowstone dust, gunpowder, spider eyes, sugar, sticks, redstone

### Wither Skeleton
- Spawns only in Nether fortress corridors
- Health: 35, 2.4 blocks tall (can walk through 1-block-high passages)
- Attack: stone sword + **Wither effect** (black health bar, 10s duration)
- **Drops**: bones, stone sword (rare), **wither skeleton skull (2.5%)** — required to summon the Wither

### Warden
- Spawns in Ancient Cities (Deep Dark biome)
- Health: 500
- Attack: melee (30 damage) + sonic boom ranged attack (ignores armor, 10 damage)
- **Drops**: none (not intended to be killed for loot)
- **Special**: blind — tracks players by sound and vibrations; inflicts Darkness effect on nearby players; emerges from the ground when sculk shriekers are triggered 3 times

---

## Neutral / Passive Mobs

### Villager
- Professions: armorer, librarian, farmer, fisherman, etc. (determined by workstation block)
- Trading: uses emeralds as currency; unlocks higher-tier trades
- **Important**: curing a zombie villager (weakness potion + golden apple) grants permanent 1-emerald discounts
- Breeding: requires enough beds and food (bread/carrots/potatoes/beetroot)

### Iron Golem
- Natural spawn: villages with enough villagers (1 per 10 villagers)
- Player-built: 4 iron blocks (T-shape) + 1 carved pumpkin on top
- Health: 100
- **Drops**: iron ingots (3–5), poppies (0–2)
- Protects villagers; attacks hostile mobs

### Ender Dragon
- Location: The End (central island)
- Health: 200
- **Defeat rewards**: 12,000 XP + dragon egg + End gateway portal activated (access to End cities)
- **Strategy**:
  1. Destroy all end crystals (8 total, on tower tops + iron cages)
  2. Use bed explosions or bow to attack the dragon
  3. Melee the dragon when it perches on the fountain

### Wither
- Player-summoned: 4 soul sand (T-shape) + 3 wither skeleton skulls
- Health: 300 (hardest boss in Java Edition)
- Special: gains shield at half health (immune to projectiles), must use melee
- **Drops**: nether star — required to craft a beacon

---

## Boss Quick Reference

| Boss | Health | Difficulty | Reward |
|------|--------|------------|--------|
| Ender Dragon | 200 | ★★★ | Dragon egg, 12,000 XP |
| Wither | 300 | ★★★★★ | Nether star → Beacon |
| Elder Guardian | 80 | ★★★ | Wet sponge, prismarine; inflicts Mining Fatigue III | Ocean Monument |
| Raid Captain | 24 | ★★ | Bad Omen → triggers raid |
| Breeze (1.21) | 30 | ★★★ | Breeze rod → Mace |
