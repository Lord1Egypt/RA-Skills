---
name: l4d2-server
description: Left 4 Dead 2 服务器管理助手。支持：(1) 记录和管理多台 L4D2 服务器（别名、IP、端口）(2) 通过 A2S 协议查询服务器状态（玩家数、地图、名称等）(3) 通过 RCON 执行服务器命令。触发词：L4D2、求生之路、服务器状态、rcon、a2s 查询。
---

# L4D2 服务器管理助手

管理 Left 4 Dead 2 游戏服务器，支持状态查询和远程指令执行。

## 配置文件

服务器配置存储在：`~/.openclaw/workspace/config/l4d2-servers.json`

### 配置结构

```json
{
  "servers": {
    "alias": {
      "host": "192.168.1.100",
      "port": 27015,
      "rcon_password": "your_rcon_password"
    }
  }
}
```

## 功能

### 1. 服务器管理

添加/修改服务器：
```
添加服务器 别名=myserver IP=192.168.1.100 端口=27015 RCON密码=xxx
```

列出已配置的服务器：
```
列出所有 L4D2 服务器
```

### 2. 状态查询

查询服务器状态：
```
查询 myserver 状态
查询 192.168.1.100:27015 状态
```

**查询优先级：**
1. 如果服务器配置了 `rcon_password` → 使用 RCON `status` 命令（信息更详细，含玩家 IP、延迟、丢包等）
2. 如果没有 RCON 密码 → 使用 A2S 协议查询（基础信息：名称、地图、玩家数）

**RCON status 输出字段：**
- hostname: 服务器名称
- map: 当前地图
- players: 玩家数/最大玩家数
- 玩家列表: userid, name, steamid, connected, ping, loss, state, rate, adr

### 3. RCON 命令执行

执行服务器命令：
```
在 myserver 上执行 status
在 myserver 上执行 changelevel c5m1_waterfront
在 myserver 上执行 sm_kick playername
```

常用 RCON 命令：
- `status` - 查看服务器状态和玩家列表
- `hostname` - 查看服务器名称
- `changelevel <map>` - 切换地图
- `sm_kick <name>` - 踢出玩家（需要 SourceMod）
- `sm_ban <name> <duration>` - 封禁玩家
- `sv_cheats 1/0` - 开关作弊模式
- `nb_delete_all` - 清除所有感染
- `z_difficulty` - 查看当前难度
- `mp_gamemode` - 查看当前游戏模式

常用地图代码：
- 战役: c1m1_hotel, c2m1_highway, c3m1_plankcountry, c4m1_milltown_a, c5m1_waterfront
- 生存: l4d2_stadium_city, l4d2_riverbed_dam
- 对抗: c1m4_atrium (牺牲)

## 脚本

### A2S 查询

```bash
python3 scripts/a2s_query.py <host> [port] [--json]
```

默认端口 27015，`--json` 输出 JSON 格式。

### RCON 命令

```bash
python3 scripts/rcon_cmd.py <host> <port> <password> <command>
```

## 配置文件操作

读取配置：
```bash
cat ~/.openclaw/workspace/config/l4d2-servers.json
```

添加服务器到配置：
```bash
# 使用 jq 操作
jq '.servers.myserver = {"host": "192.168.1.100", "port": 27015, "rcon_password": "xxx"}' \
  ~/.openclaw/workspace/config/l4d2-servers.json > /tmp/l4d2.json && \
  mv /tmp/l4d2.json ~/.openclaw/workspace/config/l4d2-servers.json
```

## 注意事项

1. RCON 密码敏感，配置文件应设置适当权限
2. A2S 查询不需要密码，RCON 操作需要密码
3. 部分命令需要服务器安装 SourceMod 插件