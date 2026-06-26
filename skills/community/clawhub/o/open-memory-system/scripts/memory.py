#!/usr/bin/env python3
"""
Open Memory System v3.1
Based on OpenViking + Microsoft Agent Memory + agent-memory
支持: Working/Short-Term/Long-Term/Persona/Episodic/Entity Memory
新增: 自动过期、版本管理
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# 配置
MEMORY_DIR = Path(os.environ.get("MEMORY_DIR", "/root/.openclaw/workspace/memory"))
CONFIG = {
    "working": "working.json",
    "short": "short-term/",
    "long": {
        "preferences": "user/preferences/",
        "entities": "user/entities/",
        "events": "user/events/",
    },
    "persona": "agent/persona/",
    "episodic": "agent/episodic/",
}

# 默认过期天数
DEFAULT_EXPIRE_DAYS = 90


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


# ========== Working Memory ==========

def set_working_memory(key: str, value: str):
    working_file = MEMORY_DIR / CONFIG["working"]
    data = {}
    if working_file.exists():
        data = json.loads(working_file.read_text())
    data[key] = {"value": value, "updated": datetime.now().isoformat()}
    working_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"💾 Working: {key}")


def get_working_memory(key: str = None) -> dict:
    working_file = MEMORY_DIR / CONFIG["working"]
    if not working_file.exists():
        return {}
    data = json.loads(working_file.read_text())
    if key:
        return data.get(key, {})
    return data


# ========== Short Term Memory ==========

def save_short_term(session_id: str, content: str):
    short_dir = MEMORY_DIR / CONFIG["short"]
    ensure_dir(short_dir)
    session_file = short_dir / f"{session_id}.md"
    existing = ""
    if session_file.exists():
        existing = session_file.read_text() + "\n\n---\n\n"
    session_file.write_text(f"{existing}{datetime.now().strftime('%H:%M')} - {content}")


def get_short_term(session_id: str) -> str:
    short_dir = MEMORY_DIR / CONFIG["short"]
    session_file = short_dir / f"{session_id}.md"
    if session_file.exists():
        return session_file.read_text()
    return ""


# ========== Long Term Memory ==========

def record_preference(key: str, value: str, reason: str = "", expires_days: int = None):
    """记录偏好 (支持过期)"""
    pref_dir = MEMORY_DIR / CONFIG["long"]["preferences"]
    ensure_dir(pref_dir)
    
    # 过期时间
    expires = None
    if expires_days:
        expires = (datetime.now() + timedelta(days=expires_days)).strftime('%Y-%m-%d')
    elif DEFAULT_EXPIRE_DAYS:
        expires = (datetime.now() + timedelta(days=DEFAULT_EXPIRE_DAYS)).strftime('%Y-%m-%d')
    
    pref_file = pref_dir / f"{key}.md"
    content = f"""# {key}

**值**: {value}
**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**原因**: {reason}
**过期**: {expires or "永不过期"}

## 详情
{value}
"""
    pref_file.write_text(content, encoding="utf-8")
    update_abstract(CONFIG["long"]["preferences"])
    print(f"✅ 偏好: {key}")


def record_entity(name: str, description: str, entity_type: str = "person", attributes: dict = None):
    """记录实体"""
    entity_dir = MEMORY_DIR / CONFIG["long"]["entities"]
    ensure_dir(entity_dir)
    
    # 属性转 JSON 字符串
    attr_str = ""
    if attributes:
        attr_str = "\n**属性**: " + json.dumps(attributes, ensure_ascii=False)
    
    entity_file = entity_dir / f"{name}.md"
    content = f"""# {name}

**类型**: {entity_type}
**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 描述
{description}
{attr_str}
"""
    entity_file.write_text(content, encoding="utf-8")
    update_abstract(CONFIG["long"]["entities"])
    print(f"✅ 实体: {name} ({entity_type})")


def record_event(title: str, description: str = "", outcome: str = None):
    """记录事件 (支持标记结果)"""
    date = datetime.now().strftime('%Y-%m-%d')
    event_dir = MEMORY_DIR / CONFIG["long"]["events"]
    ensure_dir(event_dir)
    event_file = event_dir / f"{date}.md"
    
    existing = ""
    if event_file.exists():
        existing = event_file.read_text(encoding="utf-8") + "\n\n---\n\n"
    
    outcome_str = f"\n**结果**: {outcome}" if outcome else ""
    
    content = f"""{existing}## {title}

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}{outcome_str}

### 描述
{description}
"""
    event_file.write_text(content, encoding="utf-8")
    update_abstract(CONFIG["long"]["events"])
    print(f"✅ 事件: {title}")


# ========== Persona Memory ==========

def set_persona(key: str, value: str):
    persona_dir = MEMORY_DIR / CONFIG["persona"]
    ensure_dir(persona_dir)
    persona_file = persona_dir / f"{key}.md"
    content = f"""# {key}

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 内容
{value}
"""
    persona_file.write_text(content, encoding="utf-8")
    print(f"✅ Persona: {key}")


def get_persona(key: str = None) -> dict:
    persona_dir = MEMORY_DIR / CONFIG["persona"]
    if key:
        persona_file = persona_dir / f"{key}.md"
        if persona_file.exists():
            return {"content": persona_file.read_text()}
        return {}
    result = {}
    for f in persona_dir.glob("*.md"):
        result[f.stem] = f.read_text()
    return result


# ========== Episodic Memory ==========

def record_episode(title: str, outcome: str, lessons: str, context: str = ""):
    """记录经验 (支持版本)"""
    episodic_dir = MEMORY_DIR / CONFIG["episodic"]
    ensure_dir(episodic_dir)
    
    date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date}-{outcome}.md"
    episode_file = episodic_dir / filename
    
    existing = ""
    if episode_file.exists():
        existing = episode_file.read_text(encoding="utf-8") + "\n\n---\n\n"
    
    content = f"""{existing}## {title}

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**结果**: {outcome}

### 上下文
{context}

### 教训
{lessons}
"""
    episode_file.write_text(content, encoding="utf-8")
    print(f"✅ Episodic: {title} ({outcome})")


def get_episodes(outcome: str = None, limit: int = 5) -> list:
    episodic_dir = MEMORY_DIR / CONFIG["episodic"]
    files = sorted(episodic_dir.glob("*.md"), reverse=True)
    if outcome:
        files = [f for f in files if outcome in f.name]
    return [f.read_text() for f in files[:limit]]


# ========== 自动过期 (来自 agent-memory) ==========

def cleanup_expired():
    """清理过期记忆"""
    today = datetime.now().strftime('%Y-%m-%d')
    cleaned = 0
    
    for category in CONFIG["long"].values():
        dir_path = MEMORY_DIR / category
        if not dir_path.exists():
            continue
        
        for md_file in dir_path.glob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            content = md_file.read_text(encoding="utf-8")
            
            # 检查过期时间
            for line in content.split('\n'):
                if line.startswith("**过期**:"):
                    expire_date = line.split(":")[1].strip()
                    if expire_date and expire_date != "永不过期":
                        if expire_date < today:
                            md_file.unlink()
                            cleaned += 1
                            print(f"🗑️ 删除过期: {md_file.name}")
                    break
    
    if cleaned:
        # 更新索引
        try:
            import subprocess
            subprocess.run(["python3", str(MEMORY_DIR / "index.py")], capture_output=True)
        except:
            pass
    
    return cleaned


def list_memories() -> dict:
    """列出所有记忆 (带统计)"""
    stats = {}
    
    # Preferences
    prefs = len(list((MEMORY_DIR / CONFIG["long"]["preferences"]).glob("*.md")))
    prefs = max(0, prefs - 1)
    stats["preferences"] = prefs
    
    # Entities
    stats["entities"] = len(list((MEMORY_DIR / CONFIG["long"]["entities"]).glob("*.md")))
    
    # Events
    stats["events"] = len(list((MEMORY_DIR / CONFIG["long"]["events"]).glob("*.md")))
    
    # Episodes
    stats["episodes"] = len(list((MEMORY_DIR / CONFIG["episodic"]).glob("*.md")))
    
    # Persona
    stats["persona"] = len(list((MEMORY_DIR / CONFIG["persona"]).glob("*.md")))
    
    return stats


# ========== 工具函数 ==========

def update_abstract(category: str):
    category_dir = MEMORY_DIR / category
    if not category_dir.exists():
        return
    files = [f for f in category_dir.glob("*.md") if not f.name.startswith(".")]
    if not files:
        return
    abstract = [f"- {f.stem}" for f in files]
    abstract_file = category_dir / ".abstract.md"
    content = f"# {Path(category).stem.capitalize()} 摘要\n\n**总数**: {len(files)}\n\n" + "\n".join(abstract)
    abstract_file.write_text(content, encoding="utf-8")


def read_core_memory():
    print("\n" + "=" * 50)
    print("🧠 读取核心记忆")
    print("=" * 50)
    
    working = get_working_memory()
    if working:
        print("\n📋 Working Memory:")
        for k, v in working.items():
            print(f"  {k}: {v.get('value', '')[:50]}")
    
    pref_abstract = MEMORY_DIR / CONFIG["long"]["preferences"] / ".abstract.md"
    if pref_abstract.exists():
        print("\n⭐ Preferences L0:")
        print(pref_abstract.read_text()[:300])
    
    print("\n" + "=" * 50)


def daily_summary():
    print("\n" + "=" * 50)
    print("📊 每日记忆总结")
    print("=" * 50)
    
    stats = list_memories()
    print(f"\nLong Term:")
    print(f"  偏好: {stats['preferences']}")
    print(f"  实体: {stats['entities']}")
    print(f"  事件: {stats['events']}")
    print(f"\nPersona: {stats['persona']}")
    print(f"Episodic: {stats['episodes']}")
    print("\n" + "=" * 50)


def main():
    if len(sys.argv) < 2:
        read_core_memory()
    elif sys.argv[1] == "read":
        read_core_memory()
    elif sys.argv[1] == "summary":
        daily_summary()
    elif sys.argv[1] == "cleanup":
        cleaned = cleanup_expired()
        print(f"🧹 清理了 {cleaned} 个过期记忆")
    elif sys.argv[1] == "stats":
        stats = list_memories()
        print(json.dumps(stats, indent=2))
    elif sys.argv[1] == "working" and len(sys.argv) >= 4:
        set_working_memory(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "pref" and len(sys.argv) >= 4:
        reason = sys.argv[4] if len(sys.argv) > 4 else ""
        expires = sys.argv[5] if len(sys.argv) > 5 else None
        if expires:
            expires = int(expires)
        record_preference(sys.argv[2], sys.argv[3], reason, expires)
    elif sys.argv[1] == "entity" and len(sys.argv) >= 4:
        entity_type = sys.argv[4] if len(sys.argv) > 4 else "person"
        record_entity(sys.argv[2], sys.argv[3], entity_type)
    elif sys.argv[1] == "event" and len(sys.argv) >= 3:
        desc = sys.argv[2] if len(sys.argv) > 2 else ""
        outcome = sys.argv[3] if len(sys.argv) > 3 else None
        record_event(sys.argv[2], desc, outcome)
    elif sys.argv[1] == "episode" and len(sys.argv) >= 4:
        context = sys.argv[4] if len(sys.argv) > 4 else ""
        record_episode(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "", context)
    elif sys.argv[1] == "persona" and len(sys.argv) >= 4:
        set_persona(sys.argv[2], sys.argv[3])
    else:
        print("""
🧠 Open Memory System v3.1
基于 OpenViking + agent-memory

使用方式:
  python memory.py                    # 读取核心记忆
  python memory.py read              # 同上
  python memory.py summary          # 每日总结
  python memory.py cleanup          # 清理过期记忆
  python memory.py stats            # 统计
  
  # Working Memory
  python memory.py working <key> <value>
  
  # Long Term Memory
  python memory.py pref <key> <value> [reason] [expires_days]
  python memory.py entity <name> <desc> [type]
  python memory.py event <title> [description] [outcome]
  
  # Persona
  python memory.py persona <key> <value>
  
  # Episodic
  python memory.py episode <title> <outcome> <lessons> [context]
""")


if __name__ == "__main__":
    main()
