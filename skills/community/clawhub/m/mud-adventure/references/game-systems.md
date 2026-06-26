# 游戏系统设计指南

## 1. 物品系统

### 物品类型

```python
items = {
    "物品名": {
        "name": "显示名称",
        "desc": "描述文字",
        "type": "weapon|armor|consumable|key|quest|treasure",
        "effect": None,           # consumable 类型时有效
        "attack_bonus": 0,        # weapon 攻击力加成
        "defense_bonus": 0,       # armor 防御力加成
        "stackable": False,       # 是否可堆叠
        "quantity": 1,            # 初始数量
    }
}
```

### 物品效果函数

```python
def apply_effect(item_name, player):
    effects = {
        "治疗药水": lambda p: (p.__setitem__("hp", min(p["max_hp"], p["hp"]+30)), "恢复了30HP")[1],
        "力量药水": lambda p: (p.__setitem__("attack", p["attack"]+2), "攻击力+2")[1],
        "解毒草": lambda p: (p.__setitem__("状态", "正常"), "中毒解除了")[1],
    }
    if item_name in effects:
        msg = effects[item_name](player)
        print(f"  {msg}")
        return True
    return False
```

## 2. 战斗系统

### 基础战斗循环

```python
import random

def combat(player, enemy, player_turn=True):
    while player["hp"] > 0 and enemy["hp"] > 0:
        if player_turn:
            # 玩家回合
            dmg = random.randint(max(1, player["attack"]-2), player["attack"]+2)
            enemy["hp"] -= dmg
            print(f"  你造成了 {dmg} 点伤害。")
        else:
            # 敌人回合
            dmg = random.randint(max(1, enemy["attack"]-2), enemy["attack"]+2)
            player["hp"] -= dmg
            print(f"  敌人造成了 {dmg} 点伤害。")
        player_turn = not player_turn
    return player["hp"] > 0
```

### 属性设计参考

| 玩家等级 | 推荐 HP | 推荐攻击 | 怪物 HP 范围 | 怪物攻击范围 |
|---------|--------|---------|------------|------------|
| 1 | 50-80 | 5-8 | 15-30 | 3-6 |
| 3 | 80-120 | 10-15 | 30-60 | 6-12 |
| 5 | 120-180 | 15-22 | 60-100 | 12-20 |
| 10 | 200-300 | 25-40 | 100-200 | 20-35 |

### 伤害公式变体

```python
# 暴击版本
def combat_crit(player, enemy):
    base_dmg = random.randint(player["attack"]-2, player["attack"]+2)
    crit = random.random() < 0.15  # 15%暴击率
    dmg = base_dmg * 2 if crit else base_dmg
    if crit:
        print(f"  💥 暴击！造成了 {dmg} 点伤害！")
    return dmg
```

## 3. 任务系统

### 任务状态机

```python
tasks = {
    "找回钥匙": {
        "name": "找回钥匙",
        "desc": "森林隐士需要你帮他找回丢失的钥匙",
        "stage": "active",    # inactive / active / complete / failed
        "target": "古老的钥匙",
        "reward": {"item": "治疗药水", "qty": 2, "gold": 50},
        "requires": [],          # 前置任务ID列表
        "on_complete": lambda p: print("  隐士感激地递给你两瓶药水！"),
    }
}

def check_task_completion():
    for task_id, task in tasks.items():
        if task["stage"] == "active":
            if task_id == "找回钥匙" and "古老的钥匙" in player["inventory"]:
                task["stage"] = "complete"
                grant_reward(task["reward"])
                task["on_complete"](player)
```

### 任务类型

| 类型 | 描述 | 触发方式 |
|------|------|---------|
| 收集 | 找到指定物品 | 检查背包 |
| 击杀 | 击败特定敌人 | 检查 flags |
| 探索 | 到达指定房间 | 检查 location |
| 对话 | 与 NPC 交谈 | 检查 flags |
| 护送 | 带 NPC 到某处 | 检查 NPC 位置 |
| 组合 | 多个子任务 | 检查复合条件 |

## 4. 对话树设计

```python
def dialogue_tree(npc_id):
    tree = {
        "root": [
            {"text": "你想问什么？", "options": [
                {"text": "这里发生了什么", "next": "story"},
                {"text": "你能帮帮我吗", "next": "quest"},
                {"text": "再见", "next": "bye"},
            ]}
        ],
        "story": [
            {"text": "很久以前，这里发生过一场大战...", "options": [
                {"text": "继续听", "next": "story_more"},
                {"text": "我明白了", "next": "root"},
            ]}
        ],
        "quest": [
            {"text": "帮我找回丢失的钥匙，我就告诉你宝藏的位置。",
             "action": "accept_quest",
             "options": [
                {"text": "接受任务", "next": "root", "action": "start_quest"},
                {"text": "让我想想", "next": "root"},
            ]}
        ],
        "bye": [
            {"text": "后会有期，旅人。", "action": "end"}
        ]
    }
    # 对话遍历逻辑略
```

## 5. 存档与读档

```python
import json, os

SAVE_FILE = "savegame.json"

def save_game():
    data = {
        "player": player,
        "rooms_snapshot": {k: v.get("items", []) for k, v in rooms.items()},
        "npc_states": {k: v["hp"] for k, v in npcs.items()},
        "tasks": {k: t["stage"] for k, t in tasks.items()},
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("  💾 游戏已保存。")

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("  没有找到存档。")
        return False
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    player.update(data["player"])
    for room_id, items in data["rooms_snapshot"].items():
        rooms[room_id]["items"] = items
    for npc_id, hp in data["npc_states"].items():
        npcs[npc_id]["hp"] = hp
    for task_id, stage in data["tasks"].items():
        if task_id in tasks:
            tasks[task_id]["stage"] = stage
    print("  📂 游戏已加载。")
    return True
```

## 6. 多结局设计

```python
endings = {
    "hero": {
        "condition": lambda p: p["flags"].get("击败守卫") and p["flags"].get("拿到宝藏"),
        "title": "英雄结局",
        "text": "你击败了守卫，取回了宝藏，成为传说……"
    },
    "neutral": {
        "condition": lambda p: p["flags"].get("拿到宝藏") and not p["flags"].get("击败守卫"),
        "title": "投机结局",
        "text": "你从侧门偷走了宝藏，但未能证明自己的勇气……"
    },
    "death": {
        "condition": lambda p: p["hp"] <= 0,
        "title": "死亡结局",
        "text": "你倒在了迷雾森林中，化作了森林的一部分……"
    },
    "secret": {
        "condition": lambda p: p["flags"].get("隐藏结局触发"),
        "title": "隐藏结局",
        "text": "你发现了森林最深处的秘密……"
    }
}

def check_ending():
    for ending_id, ending in endings.items():
        if ending["condition"](player):
            print(f"\n\n{'='*40}")
            print(f"  【{ending['title']}】")
            print(f"  {ending['text']}")
            print(f"{'='*40}")
            return True
    return False
```
