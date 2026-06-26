# 示例代码片段

## 快速启动：最小可运行 MUD

```python
#!/usr/bin/env python3
rooms = {"start": {"name": "起点", "desc": "一切开始的地方。", "exits": {}}}
player = {"location": "start"}
while True:
    r = rooms[player["location"]]
    print(f"\n{r['name']}\n{r['desc']}")
    cmd = input("> ").strip()
    if cmd in r["exits"]:
        player["location"] = r["exits"][cmd]
```

## 方向别名映射

```python
DIR_ALIAS = {
    "n": "北", "north": "北",
    "s": "南", "south": "南",
    "e": "东", "east": "东",
    "w": "西", "west": "西",
    "u": "上", "up": "上",
    "d": "下", "down": "下",
    "前": "北", "后": "南", "左": "西", "右": "东",
}
```

## 带锁门的房间

```python
rooms = {
    "门厅": {
        "name": "石砌门厅",
        "desc": "巨大的橡木门挡住了去路。",
        "exits": {"北": "宝库"},
        "locked_exit": {"北": True},  # True=锁着
    }
}

def move(d):
    room = rooms[player["location"]]
    if d not in room["exits"]:
        print("  无路可走。")
        return
    if room.get("locked_exit", {}).get(d):
        print("  门锁着，你需要钥匙。")
        return
    player["location"] = room["exits"][d]
    print(f"  你进入了 {rooms[player['location']]['name']}。")
```

## 随机遭遇

```python
import random

ENCOUNTERS = [
    {"msg": "一只野狼从灌木丛中窜出！", "enemy": "野狼", "prob": 0.3},
    {"msg": "地上有一个闪闪发光的箱子。", "item": "银币×10", "prob": 0.2},
    {"msg": "这里一片寂静，什么也没发生。", "prob": 0.5},
]

def random_encounter():
    r = random.random()
    cumulative = 0
    for e in ENCOUNTERS:
        cumulative += e["prob"]
        if r < cumulative:
            print(f"  {e['msg']}")
            if "item" in e:
                player["inventory"].append(e["item"])
            if "enemy" in e:
                combat(e["enemy"])
            break
```

## 简易状态栏

```python
def status_bar():
    hp_bar = "█" * player["hp"] + "░" * (player["max_hp"] - player["hp"])
    print(f"\n  ┌─ 状态 ─────────────┐")
    print(f"  │ HP {player['hp']:3d}/{player['max_hp']:3d} {hp_bar} │")
    print(f"  │ 攻击: {player['attack']:3d}  金钱: {player.get('gold', 0):4d} │")
    print(f"  │ 等级: {player.get('level', 1):3d}  经验: {player.get('exp', 0):4d} │")
    print(f"  └────────────────────┘")
```

## 带颜色输出（Windows兼容）

```python
import os, sys

def supports_color():
    return sys.platform != "win32" or os.environ.get("TERM") or True

COLOR = {
    "red": "\033[91m", "green": "\033[92m",
    "yellow": "\033[93m", "blue": "\033[94m",
    "bold": "\033[1m", "reset": "\033[0m",
}

def cprint(text, color="reset"):
    if supports_color():
        print(f"{COLOR.get(color, '')}{text}{COLOR['reset']}")
    else:
        print(text)
```

## 自动生成房间描述（模板填充）

```python
ROOM_TEMPLATES = [
    "你站在{adjective}的{place}，{atmosphere}。",
    "四周是{feature}，{sound}。",
    "这里有{special}引起了你的注意。",
]

ADJECTIVES = ["阴暗潮湿", "明亮宽敞", "雾气缭绕", "寂静诡异"]
PLACES = ["洞穴", "大厅", "走廊", "密室"]
ATMOSPHERES = ["空气中有股奇怪的味道", "墙壁上刻着古老的符文", "微弱的烛光摇曳"]
FEATURES = ["散落的骸骨", "干涸的血迹", "被撬开的箱子"]
SOUNDS = ["远处传来滴水声", "风吹过缝隙发出呼啸", "一片死寂"]

def generate_room_desc():
    import random
    t = random.choice(ROOM_TEMPLATES)
    return t.format(
        adjective=random.choice(ADJECTIVES),
        place=random.choice(PLACES),
        atmosphere=random.choice(ATMOSPHERES),
        feature=random.choice(FEATURES),
        sound=random.choice(SOUNDS),
        special="一扇半掩的门" if random.random() > 0.5 else "一个发光的符文",
    )
```
