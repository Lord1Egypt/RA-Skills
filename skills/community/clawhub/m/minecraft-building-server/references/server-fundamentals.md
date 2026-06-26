# Server Fundamentals

## 1. Self-hosted vs Public Server

This is the core distinction for build-server advice.

| Dimension | Self-hosted | Public Server |
|-----------|------------|---------------|
| Control | You own the server files and console | You are a regular player, subject to admin rules |
| OP permissions | `/op` yourself anytime | Must be granted by admin; most players don't have it |
| Bot usage | Fully allowed — your server, your rules | Usually prohibited unless explicitly authorized |
| Plugin installation | Install any plugin freely | No control; can only use what's already installed |
| RCON | Can configure and use | No access |
| WorldEdit/FAWE | Install and use freely | Depends on server support + permissions |

## 2. OP Permission Levels

Common OP command scope:
- `/op <player>` — grant OP
- `/gamemode creative <player>` — switch mode
- `/worldedit` / `//wand` — WorldEdit tools
- `/give <player> <item> <amount>` — give items
- `/gamerule` — modify world rules

Public servers usually use LuckPerms or similar granular permission systems instead of broad OP access.

## 3. Bots on Java Servers

### Self-hosted
- Legitimate and expected for automation-heavy workflows
- Mineflayer is the dominant Node.js bot framework
- Common uses: block placement, scripted construction, monitoring, procedural workflows

### Public servers
- Most prohibit bots and automation
- Even if technically possible, violating rules can get the user banned
- Always require explicit admin permission before discussing execution details

## 4. RCON Remote Management

- RCON allows remote execution of server console commands over TCP
- Enable in `server.properties`: `enable-rcon=true`
- Set `rcon.password` and `rcon.port`
- Typical clients: `mcrcon`, Python `mctools`, custom scripts
- Restrict RCON with a strong password and firewall rules

This skill may mention RCON in the context of build workflows, but full infrastructure-style server operations belong to a dedicated ops skill.

## 5. Paper vs Purpur

| Dimension | Paper | Purpur |
|-----------|-------|--------|
| Focus | Stability, performance, wide plugin compatibility | Paper + extra gameplay/server knobs |
| Plugin compatibility | Bukkit / Spigot / Paper plugins | Fully compatible with Paper |
| Build server fit | Default choice for most build servers | Good when fine-grained behavior tweaks matter |

### Selection advice
1. Default to **Paper** for most build-focused servers
2. Use **Purpur** when special movement / physics / gameplay tuning matters
3. Migration from Paper to Purpur is typically straightforward

## 6. Other Options

| Software | Description | Build-server suitability |
|----------|-------------|--------------------------|
| Vanilla | Official server | Poor: no plugin ecosystem |
| Spigot | Paper upstream | Usable, but Paper is usually better |
| Fabric + Mods | Mod-loader path | Useful for special modded workflows |
| Velocity / Waterfall | Proxy layer | Useful for multi-server build/community setups |
