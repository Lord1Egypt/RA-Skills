# Redstone Debug - Minecraft

Use this file for redstone contraptions, farms, villager systems, or automation failures.

## Debug Ladder

1. Confirm edition, version, and whether the design came from a Java-only tutorial.
2. Reproduce the bug in the smallest isolated module.
3. Check power source, tick timing, orientation, and observer updates.
4. Check entity pathing, spawn rules, or block-state assumptions.
5. Test one fix at a time.

## Common Failure Classes

| Symptom | Likely class | First check |
|---------|--------------|-------------|
| Clock never starts | power or update issue | direct power path and observer orientation |
| Works once then stalls | entity pathing or item flow | hopper locks, villagers, water flow, minecart stops |
| Farm rate is terrible | edition mismatch or spawn rules | sim distance, spawn spaces, mob caps, AFK spot |
| Random desync | chunk borders or unloading | chunk alignment and player distance |
| Server lag spike | too many entities or clocks | entity count, hopper chains, always-on loops |

## Default Advice Pattern

- Describe the exact failure.
- Mark the smallest module to isolate.
- Give one measurable test.
- Give one likely fix.
- State what result would confirm the diagnosis.
