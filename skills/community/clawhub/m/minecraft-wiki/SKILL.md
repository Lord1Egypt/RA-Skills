---
name: minecraft-wiki
version: 1.0.0
author: en1r0py1865
description: >
  Answer any Minecraft Java Edition gameplay question — facts, mechanics, strategies,
  recipes, item properties, mob behaviors, and version differences. Always use this
  skill when the user asks anything about Minecraft knowledge: 'where do diamonds spawn',
  'what Y level for ancient debris', 'how to breed animals', 'best enchantments for sword',
  'what drops from blazes', 'how does the wither work', 'village structure layout',
  'how to make a beacon', 'redstone repeater delay', 'what biome has X', 'minecraft 1.21
  changes', 'difference between iron and diamond tools', 'how to find stronghold',
  'best armor enchantments', 'how to cure zombie villager'. Works completely offline —
  no Minecraft connection needed.
metadata:
  openclaw:
    emoji: "📖"
    requires:
      bins: []
    homepage: https://github.com/en1r0py1865/minecraft-skill
---

# Minecraft Wiki

Authoritative Minecraft Java Edition knowledge base covering all major gameplay systems.
Works entirely offline — no minecraft-bridge connection required.

**Default version**: Java Edition 1.21.x (Tricky Trials). When answering, note if
something changed significantly in recent versions.

---

## How to Answer

Match response depth to question complexity:

- **Simple fact** ("what does Fortune do") → 2–4 sentences, direct answer first
- **How-to** ("how to make a beacon") → numbered steps + material list
- **Comparison** ("iron vs diamond tools") → table or side-by-side
- **Strategy** ("best enchantments for survival") → tiered recommendation with rationale
- **Troubleshooting** ("my iron farm isn't working") → diagnosis checklist

Always lead with the direct answer, then add context. Never bury the answer in preamble.

---

## Core Knowledge Domains

### 1. Ore & Resource Mining
Read `references/ores.md` for Y-level distributions, tool requirements, and biome
modifiers. Key facts to internalize:

- **Diamonds**: peak at Y=−58; deepslate layer (Y<0) since 1.18
- **Ancient Debris**: Y=8 (optimal) to Y=15 in the Nether; immune to explosions; needs diamond+ pickaxe
- **Copper**: Y=48 above sea level; 1.17+
- **Amethyst**: geodes underground; silk touch for budding blocks

### 2. Mob Mechanics & Drops
Read `references/mobs.md` for spawn conditions, drops, and special behaviors.
Key mechanics:
- Spawn rules: light level ≤0 for hostile (1.18+), type/biome restrictions
- Looting enchantment multiplies rare drop chances
- Named mobs do not despawn
- Baby variants exist for most passive mobs; breeding cooldown 5 min

### 3. Crafting & Recipes
Provide exact crafting grids when asked. Common patterns:
- Pickaxe: 3× material in top row, 2× sticks in middle and bottom center
- Sword: 2× material vertically, 1× stick below
- Armor pieces: helmet=5, chestplate=8, leggings=7, boots=4 (of chosen material)
- All tools/armor: Wood → Stone → Iron → Gold → Diamond → Netherite

### 4. Enchanting System
Read `references/enchantments.md` for full list. Key rules:
- Incompatible groups: Protection family (Prot/Fire/Blast/Proj mutually exclusive)
- Incompatible: Silk Touch ↔ Fortune; Infinity ↔ Mending; Sharpness ↔ Smite/BA
- Best XP farm for enchanting: enderman farm or trading hall
- Treasure enchantments (Mending, Curse of Binding, etc.) only from fishing/chests/trades

### 5. Biomes & Structures
Common questions:
- Finding biomes: F3 menu shows biome name; `/locate biome <biome>` command
- Structures: `/locate structure <name>`; strongholds always exist, 3 per ring
- Mesa/Badlands: surface gold ore, unique terracotta colors
- Mushroom fields: no hostile mob spawning

### 6. Redstone
Core components and behaviors — answer from training knowledge for basic circuits.
For complex contraptions, describe the principle and suggest community resources:
- Repeater: 0.1–0.4s delay (1–4 ticks), signal lock
- Comparator: subtract/compare mode, reads container fullness
- Observer: detects block state changes, 2-tick pulse
- Common builds: 2-tick clock (observer loop), T-flip-flop, item sorter

### 7. Progression & Tech Tree
Standard survival progression path:
```
Wood tools → Stone tools → Find iron → Iron tools/armor
→ Find diamonds → Diamond tools → Nether → Blaze rods
→ Ender pearls → End portal → Kill Ender Dragon
→ Netherite upgrade → Beacons / End cities
```

For specific item prerequisites, trace the dependency tree step-by-step.

### 8. Version Differences
Major changes to mention proactively:

| Version | Key Change |
|---------|-----------|
| 1.18 | World height −64 to 320; complete ore redistribution |
| 1.19 | Deep Dark / Ancient City / Warden; Mangrove swamp |
| 1.20 | Archaeology; Cherry blossom biome; Bamboo wood |
| 1.21 | Trial Chambers; Breeze mob; Mace weapon; Crafter block |

---

## Answer Quality Checklist

Before responding, verify:
- [ ] Is the answer specific to Java Edition (not Bedrock)?
- [ ] Is it accurate for 1.21.x, or does it note the correct version?
- [ ] If giving coordinates, are they correct for 1.18+ (new Y scale)?
- [ ] If discussing drops, are Looting bonuses mentioned?
- [ ] Did I provide the direct answer in the first sentence?

---

## Additional Resources

- `references/ores.md` — Complete Y-level tables and biome modifiers
- `references/mobs.md` — All mob spawning, behavior, and drop data
- `references/enchantments.md` — Full enchantment list with max levels and incompatibilities
For live game data (current inventory, position, nearby mobs), the user needs
`minecraft-bridge` running. Mention this only if the question is about their
current game state, not general knowledge.
