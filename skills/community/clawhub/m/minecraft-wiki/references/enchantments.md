# Minecraft Enchantment Reference (Java Edition 1.21.x)

---

## Incompatible Enchantment Groups

The following enchantments within the same group are mutually exclusive (only one per item):

| Group | Mutually Exclusive Enchantments |
|-------|-------------------------------|
| Protection | Protection / Fire Protection / Blast Protection / Projectile Protection |
| Damage | Sharpness / Smite / Bane of Arthropods |
| Gathering | Silk Touch ↔ Fortune |
| Infinity | Infinity ↔ Mending |

---

## Weapon Enchantments (Sword / Axe)

| Enchantment | Max Level | Effect | Notes |
|-------------|----------|--------|-------|
| Sharpness | V | +1.25 damage/level | Best general-purpose choice |
| Smite | V | +2.5 damage/level vs undead | Dedicated for zombie farms |
| Bane of Arthropods | V | +2.5 damage/level vs arthropods | Spiders/bees/silverfish |
| Knockback | II | +3 blocks knockback/level | Useful in PvP |
| Fire Aspect | II | Ignites target for 3/8 seconds | Cooks dropped meat |
| Looting | III | Increases rare drop chance | ~+1% chance per level |
| Sweeping Edge | III | Increases sweep attack damage | Sword only |
| Mending | I | Repairs durability with XP | Treasure enchantment |
| Unbreaking | III | Reduces durability loss chance | 1/(level+1) |
| Curse of Vanishing | I | Item disappears on death | Negative |

**Optimal sword**: Sharpness V + Knockback II + Fire Aspect II + Looting III + Mending I + Unbreaking III

---

## Bow / Crossbow Enchantments

| Enchantment | Max Level | Effect |
|-------------|----------|--------|
| Power | V | +25% damage/level |
| Punch | II | +3 blocks knockback/level |
| Flame | I | Ignites target |
| Infinity | I | Consumes only 1 arrow for unlimited shots (incompatible with Mending) |
| Piercing | IV | Passes through N+1 entities |
| Mending | I | Treasure enchantment |
| Quick Charge | III | Reduces reload time by 0.25s/level |

**Note**: Infinity ↔ Mending are incompatible — choose based on your play style.

---

## Tool Enchantments (Pickaxe / Axe / Hoe)

| Enchantment | Max Level | Effect | Applies To |
|-------------|----------|--------|-----------|
| Efficiency | V | Mining speed +30%^level | All tools |
| Fortune | III | Multiplies block drops | Mining/farming |
| Silk Touch | I | Drops the block itself | Incompatible with Fortune |
| Unbreaking | III | Same as above | All tools |
| Mending | I | Same as above | All tools |

**Fortune vs Silk Touch**:
- Fortune: diamond ore → up to 4 diamonds; coal/redstone/lapis also benefit
- Silk Touch: picks up the ore block itself (for decoration or later processing)

---

## Armor Enchantments

| Enchantment | Max Level | Effect | Applicable Slot |
|-------------|----------|--------|----------------|
| Protection | IV | 4% damage reduction per level per piece, 80% cap across all pieces | All |
| Fire Protection | IV | Reduces fire damage and burn duration | All |
| Blast Protection | IV | Reduces explosion damage | All (chestplate ideal) |
| Projectile Protection | IV | Reduces projectile damage | All |
| Thorns | III | Reflects damage to attackers | All (but increases durability loss) |
| Respiration | III | Adds 15s/level of underwater breathing | Helmet |
| Aqua Affinity | I | Restores normal mining speed underwater | Helmet |
| Depth Strider | III | Reduces water movement slowdown | Boots |
| Feather Falling | IV | Reduces fall damage | Boots |
| Swift Sneak | III | Reduces sneaking speed penalty | Leggings (treasure) |
| Frost Walker | II | Creates frosted ice when walking on water | Boots (treasure) |
| Soul Speed | III | Increases speed on soul sand/soil | Boots |
| Mending | I | Treasure enchantment | All |
| Unbreaking | III | Reduces durability loss | All |
| Curse of Binding | I | Cannot remove equipped item | All (negative) |

**Optimal survival armor set**:
- Helmet: Protection IV + Respiration III + Aqua Affinity I + Unbreaking III + Mending
- Chestplate: Protection IV + Unbreaking III + Mending
- Leggings: Protection IV + Swift Sneak III + Unbreaking III + Mending
- Boots: Protection IV + Feather Falling IV + Depth Strider III + Soul Speed III + Unbreaking III + Mending

---

## Fishing Rod Enchantments

| Enchantment | Max Level | Effect |
|-------------|----------|--------|
| Luck of the Sea | III | Reduces junk, increases treasure chance |
| Lure | III | Reduces wait time (−5s/level) |
| Unbreaking | III | Standard durability |
| Mending | I | Treasure enchantment |

---

## Treasure Enchantment Sources

Treasure enchantments (✨) cannot be obtained from the enchanting table (unless noted):

| Enchantment | Obtainable From |
|-------------|----------------|
| Mending | Fishing / Villager trading / Loot chests |
| Infinity | Enchanting table / Fishing |
| Swift Sneak | Ancient City loot chests only |
| Frost Walker | Loot chests / Villager trading |
| Soul Speed | Bastion remnant loot chests / Piglin bartering |
| Curse of Binding | Fishing / Loot chests |
| Curse of Vanishing | Fishing / Loot chests |

---

## Enchanting Table Setup

1. Place the enchanting table surrounded by **15 bookshelves** (1 block of air between table and shelves, shelves at 2 blocks distance)
2. Bookshelf count vs max enchantment level: 0 = level 1, 15 = level 30
3. Max-level enchantment requires **3 lapis lazuli + 30 experience levels**
4. Unsatisfied with options? Spend 1 lapis lazuli to re-roll (only refreshes the bottom two options)
