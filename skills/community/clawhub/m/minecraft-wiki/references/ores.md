# Minecraft Ore Distribution Reference (Java Edition 1.18+)

> Version 1.18 completely reworked ore distribution. The data below applies to 1.18.x through 1.21.x.

---

## Quick Reference Table

| Ore | Best Y Level | Distribution Type | Minimum Tool | 1.18+ Change |
|-----|-------------|-------------------|-------------|-------------|
| Coal | Y=96 | Triangular 0→256, peak 96 | Wooden Pickaxe | Also common near surface |
| Iron | Y=15 and Y=232 | Bimodal | Stone Pickaxe | Bimodal distribution, abundant in mountain surfaces |
| Copper | Y=48 | Triangular 0→96 | Stone Pickaxe | Added in 1.17 |
| Gold | Y=−16 | Triangular −64→32 | Iron Pickaxe | More in deep layers; mineshafts still apply |
| Lapis Lazuli | Y=0 | Triangular −64→64 | Stone Pickaxe | Highest concentration at Y=0 |
| Redstone | Y=−58 | Triangular −64→16 | Iron Pickaxe | Most abundant at deepest layers |
| Diamond | Y=−58 | Triangular −64→16 | Iron Pickaxe | **Completely redistributed** |
| Emerald | Y=236 | Mountain-only | Iron Pickaxe | Only in mountain biomes |

---

## Diamond Ore — Details

**Optimal mining Y level**: **Y=−58** (highest density; only 1 layer above lava danger zone)

**Mining strategy**:
1. Dig down to Y=−58 (the Y value shown in F3, not the Y+0.6 foot position in XYZ)
2. Branch mine every 3 blocks apart (to avoid missing veins)
3. Carry a water bucket to handle lava

**Fortune enchantment yields**:
- No enchantment: 1 ore = 1 diamond
- Fortune I: average 1.33/ore
- Fortune II: average 1.75/ore
- Fortune III: average 2.2/ore (max 4)

**Note**: Deepslate diamond ore (`deepslate_diamond_ore`) drops the same as regular diamond ore but takes slightly longer to mine.

---

## Netherite / Ancient Debris

**Location**: The Nether

| Y Level | Density |
|---------|---------|
| Y=8 | Very high (optimal) |
| Y=15 | Second best (avoids lava sea) |
| Y=22 | Moderate |

**Mining tips**:
- Use TNT or end crystals for blast mining (ancient debris is blast-resistant)
- Drink fire resistance potions before mining
- Each ancient debris smelts into 1 netherite scrap; 4 scraps = 1 netherite ingot

**Netherite ingot requirements**:
- Upgrade tools/weapons: 1 ingot each (at smithing table)
- Upgrade armor: 1 ingot each
- Full set: 8 ingots (4 armor pieces + 4 tools/weapons)

---

## Iron Ore — Bimodal Distribution

**Two peak locations**:
1. **Y=15** (underground peak, traditional mining layer)
2. **Y=232** (mountain peak, ideal for surface mining in mountain biomes)

**Recommendations**:
- Early game: mine around Y=15
- Mountain biomes: abundant surface iron ore, far more efficient than underground mining

---

## Gold Ore — Special Distribution

**Overworld**:
- Highest density at Y=−16
- Mineshafts and ruins contain extra gold ore

**Nether**:
- Uniform distribution across all Y levels (Y=10–117)
- **Nether Gold Ore**: drops 2–6 gold nuggets (not ingots)
- Fortune enchantment increases nugget yield
- Does not require an iron pickaxe; stone pickaxe is sufficient

**Special**: Zombified Piglin aggro mechanic — mining gold ore in the Nether does **not** trigger aggro

---

## Amethyst

- Generates inside amethyst geodes
- Geode locations: Y=−58 to Y=30, randomly placed
- Outer layers: smooth basalt → calcite → inner amethyst
- **Budding Amethyst**: cannot be moved; once broken, stops growing
- Harvesting: break amethyst clusters with any tool to drop 2 amethyst shards (Fortune increases yield)
- Silk Touch picks up the full amethyst cluster (for decoration)

---

## Biome-Specific Ore Modifiers

| Biome | Special Resource | Notes |
|-------|-----------------|-------|
| Mountains / Peaks | Emerald (peak at Y=236) | Only generates in mountain biomes |
| Swamp | Slightly more lapis lazuli | Probability slightly above average |
| Mineshaft / Ruins | All ores + gold blocks | Structures contain gold blocks and ores |
| Cliffs | Exposed iron ore | Iron ore visible on mountain surfaces |
