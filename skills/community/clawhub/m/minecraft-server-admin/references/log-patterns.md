# Minecraft Server Log Patterns

## Common Log Meanings

### Performance

| Log line | Meaning | Suggested response |
|---|---|---|
| `Can't keep up! Running Xms behind` | TPS is dropping / server is overloaded | Under 1000ms: usually a spike; over 5000ms: investigate |
| `Saving chunks for level 'world'` | Auto-save event | Normal |
| `Preparing spawn area: X%` | Startup world preparation | Normal during startup |
| `Done (X.XXXs)! For help, type "help"` | Server finished starting | Record startup time if needed |

### Player Activity

| Log line | Meaning |
|---|---|
| `PlayerName joined the game` | Player joined |
| `PlayerName left the game` | Player left normally |
| `PlayerName lost connection: Timed out` | Network timeout |
| `PlayerName lost connection: You have been kicked` | Player was kicked |
| `PlayerName was kicked for flying` | Anti-cheat / server rule enforcement |
| `PlayerName issued server command: /cmd` | Player executed a command |

### Errors

| Level | Prefix | Meaning |
|---|---|---|
| WARN | `[HH:MM:SS] [Server thread/WARN]` | Warning, usually non-fatal |
| ERROR | `[HH:MM:SS] [Server thread/ERROR]` | Error worth investigating |
| Stack trace | `at com.xxx.xxx` | Exception trace |

## Common Issues

### `FAILED TO BIND TO PORT`
Port is already in use.
- Check another Minecraft instance or another process on the same port
- Change `server-port` or stop the conflicting process

### `java.net.SocketException: Connection reset`
Player or network disconnect. Usually not a server-side problem.

### `java.lang.OutOfMemoryError`
Java heap exhausted.
- Increase JVM memory settings such as `-Xmx4G -Xms2G`
- Investigate plugins, view distance, or chunk load pressure

### `Skipping Entity with id XXX`
Corrupt or invalid entity data was skipped.
Usually harmless unless repeated frequently.

### `RCON cannot parse color codes`
The server returned color-coded output over RCON.
Strip `§` formatting codes in the client/parser.

## TPS Guide

TPS target is 20.

| TPS | State | Typical interpretation |
|---|---|---|
| 18–20 | Healthy | No major concern |
| 15–18 | Mild lag | Occasional warnings |
| 10–15 | Noticeable lag | Players will feel it |
| <10 | Severe | Immediate investigation needed |

Paper/Spigot can use `/tps`; vanilla often requires inference from lag warnings.

## Common Log Locations

| Environment | Path |
|---|---|
| Vanilla | `./logs/latest.log` |
| Paper/Spigot | `./logs/latest.log` |
| Pterodactyl | `/home/container/logs/latest.log` or panel log view |
| Most panels | `logs/latest.log` relative to server root |
