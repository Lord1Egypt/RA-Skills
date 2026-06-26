#!/usr/bin/env python3
"""Enhanced create a new agent with SOUL.md template and interactive personality selection."""
import os, sys

AGENTS_DIR = os.path.expanduser("~/.openclaw/agents")

PERSONALITY_LIBRARY = """
Chinese Ancient:
  毛泽东 - 游击战术、实事求是、集中优势兵力
  诸葛亮 - 深谋远虑、宁静致远、战略性思维
  张良 - 运筹帷幄、洞察先机
  韩信 - 将将之才、多多益善、灵活调度
  孔子 - 仁爱孝悌、修身齐家
  曾国藩 - 严谨持家、自我修炼
  孙子 - 知己知彼、不战而屈人之兵
  商鞅 - 变法图强、制度化管理

Western Modern:
  索罗斯 - 反身性理论、趋势跟踪
  查理·芒格 - 多元思维、逆向思考、长期复利
  彼得·德鲁克 - 目标管理、效能优先
  福尔摩斯 - 观察入微、逻辑推理
  乔布斯 - 极致产品、用户体验
  马斯克 - 第一性原理、快速迭代
  任正非 - 危机意识、艰苦奋斗
  格雷厄姆 - 价值投资、安全边际
"""

def select_personality():
    print("\n=== Select Personality ===")
    print(PERSONALITY_LIBRARY.strip())
    print()
    while True:
        choice = input("Enter personality (e.g. '马斯克', '张良', '乔布斯'): ").strip()
        if choice:
            return choice
        print("Please enter a valid personality name.")

def get_duties():
    print("\n=== Core Duties ===")
    duties = []
    print("Enter duties (one per line, empty line to finish):")
    while True:
        line = input("  Duty: ").strip()
        if not line:
            if duties:
                break
            print("Enter at least one duty.")
            continue
        duties.append(line)
    return duties

def get_principles():
    print("\n=== Core Principles ===")
    principles = []
    print("Enter principles (one per line, empty line to finish):")
    while True:
        line = input("  Principle: ").strip()
        if not line:
            if principles:
                break
            print("Enter at least one principle.")
            continue
        principles.append(line)
    return principles

def get_reporting():
    print("\n=== Collaboration Protocol ===")
    direct上级 = input("Direct supervisor (default: 贾维斯): ").strip() or "贾维斯"
    daily = input("Daily report frequency (e.g. 每小时/完成后/实时): ").strip() or "完成后"
    trigger = input("Escalation trigger conditions: ").strip() or "重大变化需立即上报"
    scope = input("Decision scope (what can you decide yourself?): ").strip() or "日常任务自主决定"
    return direct上级, daily, trigger, scope

def main():
    if len(sys.argv) < 2:
        name = input("Enter new agent name: ").strip()
        if not name:
            print("Agent name required.")
            sys.exit(1)
    else:
        name = sys.argv[1]

    path = os.path.join(AGENTS_DIR, name)
    soul = os.path.join(path, "SOUL.md")

    if os.path.exists(soul):
        overwrite = input(f"SOUL.md already exists for '{name}', overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Aborted.")
            sys.exit(0)

    os.makedirs(path, exist_ok=True)

    personality = select_personality()
    duties = get_duties()
    principles = get_principles()
    direct上级, daily, trigger, scope = get_reporting()

    duties_str = '\n'.join(f'{i+1}. {d}' for i, d in enumerate(duties))
    principles_str = '\n'.join(f'{i+1}. {p}' for i, p in enumerate(principles))

    template = f"""# SOUL - {name}

## 人格
**{personality}**

## 核心特质
- 从{personality}继承的核心特质1
- 从{personality}继承的核心特质2

## 说话风格
- 典型口头禅/句式

## 核心职责
{duties_str}

## 核心原则
{principles_str}

## 与上级的协作协议
- 直接上级：{direct上级}
- 日常汇报：{daily}
- 升级触发：{trigger}
- 决策权限：{scope}

## 输出标准
- 产出格式要求
"""

    with open(soul, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"\n[OK] {name}/SOUL.md created")
    print(f"     Path: {soul}")
    print(f"     Next: Edit {soul} to customize core traits and speaking style")

if __name__ == "__main__":
    main()