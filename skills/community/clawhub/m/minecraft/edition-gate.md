# Edition Gate - Minecraft

Use this file before giving mechanics-heavy advice.

## Ask These First

1. Java or Bedrock?
2. Approximate version or latest?
3. Single-player, Realm, or dedicated server?
4. Vanilla, plugin-based, or modded?
5. Survival, creative, or operator task?

## High-Risk Divergences

| Topic | Java default | Bedrock default | Why it matters |
|-------|--------------|-----------------|----------------|
| Commands | richer selector and NBT support | different syntax and feature gaps | copied commands often fail immediately |
| Redstone | more deterministic community references | many timings and quasi-connectivity assumptions differ | popular farm tutorials may not port |
| Farms | most benchmark videos target Java | spawn and mob behavior can differ | rates and layouts can be wrong |
| Mods/plugins | Fabric, Forge, NeoForge, Paper, Spigot | add-ons and marketplace packs | install path and compatibility are different |
| Server admin | JVM tuning and jar ecosystem | Bedrock server binary and permissions | troubleshooting stack changes |

## Minimal Safe Reply Pattern

- State the edition assumption up front.
- Mark any version-sensitive mechanic.
- Give one first test that proves the approach fits their world.
- If edition is unknown, ask before providing commands or farm layouts.
