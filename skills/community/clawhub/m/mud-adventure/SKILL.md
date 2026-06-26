---
name: mud-adventure
description: 文字冒险型 MUD 游戏创作助手。用于快速搭建文字冒险游戏的世界观、地图、NPC、物品、任务与对话树。当用户说"做 MUD"、"写文字冒险"、"创建mud游戏"、"搭建mud世界"时触发。
---

# MUD Adventure Skill

文字冒险型 MUD 游戏创作技能包。帮你从零构建可运行的单文件 Python MUD 游戏。

## 快速开始

游戏核心只需一个 Python 文件（`game.py`），运行方式：

```bash
python game.py
```

首次使用，按以下流程构建游戏：

```
世界观设计 → 地图建模 → 人物/物品 → 对话/任务 → 合并到 game.py
```

详细设计指南见 `references/world-design.md`（世界观、故事结构）
详细系统指南见 `references/game-systems.md`（战斗、物品、任务）
示例代码见 `references/examples.md`

## 默认游戏模板

以下模板可直接复制到 `game.py` 运行，内含 3 个房间、1 个 NPC、1 个战斗场景：

```python
import random

# ============ 世界设定 ============
TITLE = "迷雾森林"
AUTHOR = "石头龙虾二号"

# ============ 房间定义 ============
rooms = {
    "入口": {
        "name": "森林入口",
        "desc": "你站在一棵巨大的古橡树下，晨雾弥漫，四周静得只能听见自己的呼吸。",
        "exits": {"北": "大厅", "东": "小屋"},
        "items": [],
        "npcs": [],
    },
    "大厅": {
        "name": "迷雾大厅",
        "desc": "雾气中隐约可见一座石制大厅，墙壁上刻着模糊的文字。",
        "exits": {"南": "入口", "北": "宝藏室"},
        "items": ["古老的钥匙"],
        "npcs": ["守卫"],
    },
    "小屋": {
        "name": "林间小屋",
        "desc": "一间破旧的小木屋，窗户透出微弱的烛光。",
        "exits": {"西": "入口"},
        "items": ["治疗药水"],
        "npcs": ["隐士"],
    },
    "宝藏室": {
        "name": "隐藏宝藏室",
        "desc": "你推开门，金光闪闪的宝物堆满了整个房间！",
        "exits": {"南": "大厅"},
        "items": ["黄金剑"],
        "npcs": [],
        "locked": True,
    },
}

# ============ NPC 定义 ============
npcs = {
    "守卫": {
        "name": "石甲守卫",
        "desc": "一个身披石甲的沉默战士，目光警惕地盯着你。",
        "hp": 30,
        "attack": 8,
        "dialogue": {
            "你好": "守卫冷哼一声：'想过去？先证明你的实力！'",
            "挑战": "守卫举起巨剑：'那就来吧！'",
            "离开": "守卫退回阴影中，不再说话。",
        },
        "hostile": True,
    },
    "隐士": {
        "name": "森林隐士",
        "desc": "一位白发苍苍的老人，正对着烛火沉思。",
        "hp": 20,
        "attack": 0,
        "dialogue": {
            "你好": "隐士微微一笑：'旅人，这片森林藏着许多秘密。'",
            "帮助": "隐士点点头：'在大厅的墙壁上，有打开宝藏室的提示。'",
            "离开": "隐士挥挥手：'愿森林保佑你。'",
        },
        "hostile": False,
    },
}

# ============ 物品定义 ============
items = {
    "古老的钥匙": {"name": "古老的钥匙", "desc": "一把生锈但依然坚固的钥匙。", "effect": None},
    "治疗药水": {"name": "治疗药水", "desc": "散发淡蓝色光芒的恢复药剂。", "effect": "heal"},
    "黄金剑": {"name": "黄金剑", "desc": "传说中的宝剑，剑身流淌着金色的光芒。", "effect": "power"},
}

# ============ 玩家状态 ============
player = {
    "hp": 100,
    "max_hp": 100,
    "attack": 10,
    "inventory": [],
    "location": "入口",
    "flags": {"大厅_交谈过": False, "击败守卫": False},
}

# ============ 核心函数 ============
def print_intro():
    print(f"\n{'='*50}")
    print(f"  🎮 {TITLE}")
    print(f"  作者：{AUTHOR}")
    print(f"{'='*50}\n")
    print("输入 'help' 查看所有命令。\n")

def show_room():
    room = rooms[player["location"]]
    locked_msg = " [门被锁住了]" if room.get("locked") and not player["flags"].get("有钥匙") else ""
    print(f"\n📍 【{room['name']}】{locked_msg}")
    print(f"  {room['desc']}")
    exits = "、".join(room["exits"].keys())
    print(f"  出口：{exits}")
    if room.get("items"):
        print(f"  物品：{', '.join(room['items'])}")
    if room.get("npcs"):
        print(f"  NPC：{', '.join(room['npcs'])}")

def show_help():
    print("""
  help     - 显示此帮助
  look     - 环顾四周
  go <方向> - 向指定方向移动（北/南/东/西/前/后）
  look <物品>- 查看物品
  take <物品> - 拾取物品
  inventory - 查看背包
  use <物品> - 使用物品
  talk <NPC> - 与NPC交谈
  attack <NPC>- 攻击敌人
  status    - 查看角色状态
  quit      - 退出游戏
  """)

def move(direction):
    room = rooms[player["location"]]
    if direction not in room["exits"]:
        print("  你无法往那个方向走。")
        return
    target = room["exits"][direction]
    if rooms[target].get("locked") and not player["flags"].get("有钥匙"):
        print(f"  {rooms[target]['name']}的门是锁着的。你需要找到钥匙。")
        return
    player["location"] = target
    show_room()

def take_item(item_name):
    room = rooms[player["location"]]
    for i, item in enumerate(room.get("items", [])):
        if item_name in item or item in item_name:
            player["inventory"].append(item)
            room["items"].pop(i)
            if item == "古老的钥匙":
                player["flags"]["有钥匙"] = True
            print(f"  你拾取了「{item}」。")
            return
    print("  这里没有这个东西。")

def use_item(item_name):
    for i, item in enumerate(player["inventory"]):
        if item_name in item or item in item_name:
            if items[item]["effect"] == "heal":
                heal = min(30, player["max_hp"] - player["hp"])
                player["hp"] += heal
                player["inventory"].pop(i)
                print(f"  你喝下了「{item}」，恢复了 {heal} 点生命！")
            elif items[item]["effect"] == "power":
                player["attack"] += 5
                player["inventory"].pop(i)
                print(f"  你装备了「{item}」，攻击力提升！")
            else:
                print(f"  你使用了「{item}」。")
            return
    print("  你的背包里没有这个东西。")

def talk_to(target):
    room = rooms[player["location"]]
    if target not in room.get("npcs", []):
        print("  这里没有这个人。")
        return
    npc = npcs[target]
    print(f"\n  👤 {npc['name']}：{npc['desc']}")
    print("\n  你想说什么？（输入选项前的关键词）")
    for key in npc["dialogue"]:
        print(f"    - {key}")
    choice = input("\n  > ").strip()
    if choice in npc["dialogue"]:
        print(f"\n  {npc['dialogue'][choice]}")
        if choice == "帮助" and target == "隐士":
            player["flags"]["大厅_交谈过"] = True
    else:
        print("  对方没有回应……")

def combat(enemy_id):
    if enemy_id not in npcs:
        print("  这里没有这个敌人。")
        return
    enemy = npcs[enemy_id]
    print(f"\n  ⚔️  你向 {enemy['name']} 发起了战斗！")
    while enemy["hp"] > 0 and player["hp"] > 0:
        dmg_to_enemy = random.randint(max(1, player["attack"]-3), player["attack"]+3)
        enemy["hp"] -= dmg_to_enemy
        print(f"  你造成了 {dmg_to_enemy} 点伤害。")
        if enemy["hp"] <= 0:
            print(f"\n  🎉 你击败了 {enemy['name']}！")
            player["flags"]["击败守卫"] = True
            rooms[player["location"]]["npcs"].remove(enemy_id)
            if "守卫" in enemy_id:
                rooms["宝藏室"]["locked"] = False
            return
        dmg_to_player = random.randint(max(1, enemy["attack"]-2), enemy["attack"]+2)
        player["hp"] -= dmg_to_player
        print(f"  {enemy['name']} 对你造成了 {dmg_to_player} 点伤害！")
        print(f"  你的生命值：{player['hp']}/{player['max_hp']}")
        if player["hp"] <= 0:
            print("\n  💀 你倒下了……游戏结束。")
            return
    print(f"\n  敌人生命值：{enemy['hp']}")

def main():
    print_intro()
    show_room()
    while True:
        cmd = input("\n> ").strip()
        if not cmd:
            continue
        parts = cmd.split(maxsplit=1)
        verb = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        if verb in ("q", "quit", "exit"):
            print("\n  再见，旅人！👋\n")
            break
        elif verb in ("help", "h", "?"):
            show_help()
        elif verb in ("look", "l"):
            if arg:
                for item in rooms[player["location"]].get("items", []):
                    if arg in item:
                        print(f"  {items[item]['desc']}")
                        break
                else:
                    print("  你没有看到这个东西。")
            else:
                show_room()
        elif verb in ("go", "walk", "移动", "走"):
            move(arg)
        elif verb in ("n", "s", "e", "w", "north", "south", "east", "west", "北", "南", "东", "西"):
            dir_map = {"n":"北","s":"南","e":"东","w":"西","north":"北","south":"南","east":"东","west":"西"}
            move(dir_map.get(verb, verb))
        elif verb in ("take", "get", "捡", "拿"):
            take_item(arg)
        elif verb in ("inv", "inventory", "i", "背包", "物品"):
            if player["inventory"]:
                print("  背包：" + "、".join(player["inventory"]))
            else:
                print("  背包是空的。")
        elif verb in ("use", "use", "使用"):
            use_item(arg)
        elif verb in ("talk", "chat", "说", "谈"):
            talk_to(arg if arg else input("  和谁交谈？> ").strip())
        elif verb in ("attack", "kill", "打", "攻击", "fight"):
            room_npcs = rooms[player["location"]].get("npcs", [])
            if not room_npcs:
                print("  这里没有可以攻击的目标。")
            elif len(room_npcs) == 1:
                combat(room_npcs[0])
            else:
                combat(arg if arg else input("  攻击谁？> ").strip())
        elif verb in ("status", "sta", "状态"):
            print(f"  HP：{player['hp']}/{player['max_hp']} | 攻击：{player['attack']}")

if __name__ == "__main__":
    main()
```

## 扩展指南

### 添加新房间
在 `rooms` 字典中新增键值对，定义 `name`、`desc`、`exits`、`items`、`npcs`。

### 添加新 NPC
在 `npcs` 字典中定义，设置 `name`、`desc`、`hp`、`attack`、`dialogue`、`hostile`。

### 添加新物品
在 `items` 字典中定义，设置 `name`、`desc`、`effect`（None/heal/power/custom）。

### 添加战斗系统
参考 `references/game-systems.md` 中的战斗系统设计，可扩展：经验值、等级、怪物掉落、魔法技能。

### 添加任务系统
参考 `references/game-systems.md` 中的任务系统，用 `player["flags"]` 跟踪任务进度。
