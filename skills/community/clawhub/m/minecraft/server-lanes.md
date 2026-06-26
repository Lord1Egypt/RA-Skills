# Server Lanes - Minecraft

Use this file when the task is about hosting, mods, plugins, Realms, or multiplayer operations.

## Hosting Surface

| Surface | Typical stack | Best first move |
|---------|---------------|-----------------|
| Realm | managed multiplayer | confirm edition and available settings before suggesting admin changes |
| Java dedicated server | vanilla jar, Paper, Spigot, Fabric, Forge, NeoForge | confirm version, loader, JVM, and log path |
| Bedrock dedicated server | official bedrock server binary | confirm version, permissions, and add-on model |
| Modpack host | launcher or rented node | list loader, pack version, failing mods, and crash logs |
| Home host | Docker, systemd, or game panel | confirm backups, ports, RAM limit, and restart flow |

## Safe Troubleshooting Order

1. Version and loader compatibility
2. Clean startup logs
3. One failing plugin, mod, or datapack at a time
4. World backup before changing major components
5. Player-impact summary before applying fixes

## Recurring Issues

- wrong Java runtime for the server jar
- plugin version mismatch after server upgrade
- modpack dependency missing on client or server side
- world corruption risk after force-closing or failed migration
- lag blamed on RAM when entity load or view distance is the actual issue
