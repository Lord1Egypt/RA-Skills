# Vanilla Command Reference — Minecraft Java Edition 1.21.x

Permission levels: 0 = everyone, 2 = operator, 4 = console/full admin.

---

## Player Management (level 2)

```text
/list                              Show online players
/kick <player> [reason]            Kick a player
/ban <player> [reason]             Ban a player account
/ban-ip <player|ip> [reason]       Ban an IP address
/pardon <player>                   Unban a player
/pardon-ip <ip>                    Unban an IP
/whitelist add <player>            Add to whitelist
/whitelist remove <player>         Remove from whitelist
/whitelist list                    Show whitelist
/whitelist on|off                  Enable/disable whitelist
/whitelist reload                  Reload whitelist file
/op <player>                       Grant operator privileges
/deop <player>                     Remove operator privileges
```

## Items and Player State (level 2)

```text
/give <player> <item> [count]      Give items
/clear <player> [item] [count]     Clear items (omit item to clear all)
/gamemode <mode> [player]          Set game mode
  - survival / s / 0
  - creative / c / 1
  - adventure / a / 2
  - spectator / sp / 3
/xp add <player> <amount> [points|levels]   Add XP
/xp set <player> <amount> [points|levels]   Set XP
/effect give <player> <effect> [duration] [amplifier]
/effect clear <player> [effect]    Clear effects
```

## Common Effect IDs

```text
minecraft:speed
minecraft:slowness
minecraft:haste
minecraft:mining_fatigue
minecraft:strength
minecraft:instant_health
minecraft:instant_damage
minecraft:jump_boost
minecraft:nausea
minecraft:regeneration
minecraft:resistance
minecraft:fire_resistance
minecraft:water_breathing
minecraft:invisibility
minecraft:blindness
minecraft:night_vision
minecraft:hunger
minecraft:weakness
minecraft:poison
minecraft:wither
minecraft:health_boost
minecraft:absorption
minecraft:saturation
minecraft:glowing
minecraft:levitation
minecraft:luck
minecraft:bad_luck
minecraft:slow_falling
minecraft:conduit_power
minecraft:dolphins_grace
```

## Teleportation (level 2)

```text
/tp <player> <x> <y> <z>           Teleport to coordinates
/tp <player> <target>              Teleport to another player
/tp <x> <y> <z>                    Teleport self (not useful from console)
/teleport ...                      Alias for /tp
```

Relative coordinates use `~`:

```text
/tp PlayerName ~ ~10 ~
```

## World Management (level 2)

```text
/time set <value|day|night|noon|midnight>
  - day = 1000
  - noon = 6000
  - night = 13000
  - midnight = 18000
/time add <amount>
/time query daytime|gametime|day

/weather clear [duration]
/weather rain [duration]
/weather thunder [duration]

/difficulty peaceful|easy|normal|hard
/difficulty 0|1|2|3

/gamerule <rule> [value]
```

## Common Gamerules

```text
keepInventory           true/false
DoFireTick              true/false
DoDaylightCycle         true/false
DoWeatherCycle          true/false
DoMobSpawning           true/false
DoMobLoot               true/false
mobGriefing             true/false
naturalRegeneration     true/false
showDeathMessages       true/false
sendCommandFeedback     true/false
commandBlockOutput      true/false
playersSleepingPercentage 0-100
maxEntityCramming       int
spawnRadius             int
```

## Broadcast and Messaging (level 2)

```text
/say <message>                    Server broadcast
/msg <player> <message>           Private message
/me <action>                      Action message

/title <player|@a> title <JSON>
/title <player|@a> subtitle <JSON>
/title <player|@a> actionbar <JSON>
/title <player|@a> clear
/title <player|@a> times <fadeIn> <stay> <fadeOut>
```

JSON text examples:

```json
{"text":"Message","color":"gold","bold":true}
{"text":"Warning","color":"red"}
{"text":"Custom color","color":"#FF5500"}
```

## Structures and Chunks (level 2)

```text
/locate structure minecraft:<structure>
/locate biome minecraft:<biome>
/fill <x1 y1 z1> <x2 y2 z2> <block> [replace|keep|outline|hollow]
/setblock <x> <y> <z> <block>
/clone <x1 y1 z1> <x2 y2 z2> <dx> <dy> <dz>
/forceload add <from> [to]
/forceload remove <from> [to]
/forceload query [pos]
```

## Common Structure Names

```text
minecraft:village
minecraft:stronghold
minecraft:mineshaft
minecraft:desert_pyramid
minecraft:jungle_pyramid
minecraft:igloo
minecraft:mansion
minecraft:monument
minecraft:pillager_outpost
minecraft:ruined_portal
minecraft:bastion_remnant
minecraft:nether_fortress
minecraft:end_city
minecraft:ancient_city
minecraft:trial_chambers
```

## Entity Selectors

```text
@a    all players
@p    nearest player
@r    random player
@e    all entities
@s    command source
```

Examples:

```text
[type=minecraft:zombie]
[name="PlayerName"]
[distance=..10]
[x=0,y=64,z=0,distance=..5]
[team=red]
[scores={kills=10..}]
[nbt={Health:5f}]
```

## Save and Maintenance (level 4 / console)

```text
/save-all [flush]   Save all chunks
/save-on            Enable auto-save
/save-off           Disable auto-save (use carefully)
/stop               Stop the server cleanly
/reload             Reload data packs/functions
/debug start        Start profiling
/debug stop         Stop profiling and save report
/perf start         Performance report (Paper)
```

## Common Item IDs for /give

```text
minecraft:diamond
minecraft:diamond_pickaxe
minecraft:netherite_ingot
minecraft:diamond_sword
minecraft:enchanted_golden_apple
minecraft:elytra
minecraft:totem_of_undying
minecraft:shulker_box
minecraft:command_block
minecraft:barrier
minecraft:structure_block
```
