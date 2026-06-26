# Command Patterns - Minecraft

Use this file for commands, datapacks, selectors, scoreboards, and command block logic.

## Safe Command Workflow

1. Confirm edition and version.
2. Confirm whether cheats or operator rights exist.
3. Start with the smallest selector and a harmless output command.
4. Add conditions one by one.
5. Only then move to world-changing commands.

## Command Recipe Template

```text
Goal:
Edition/version:
Command access: yes | no
Target entity or block:
Where it should run:
What should happen if no target matches:
```

## Reliable Patterns

- Test selectors with a harmless message or tag before using `/kill`, `/tp`, or `/effect`.
- For scoreboards, define objective, writer, reader, and reset condition explicitly.
- For datapacks, separate setup functions from tick functions so the failure surface is visible.
- For repeating command blocks, document whether they are always active or redstone-triggered.

## High-Risk Moves

- bulk `/fill` and `/clone` in live areas
- selector logic copied from another edition
- scoreboard loops without reset logic
- datapack functions that assume a namespace or load order that does not exist
