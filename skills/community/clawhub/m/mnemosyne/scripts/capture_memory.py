#!/usr/bin/env python3
import json, sys, os, time

def capture(content, mem_type, importance, tags, context, tier, memory_file, index_file):
    timestamp = int(time.time())
    date = time.strftime('%Y-%m-%d')
    memory_id = f"mem_{date}_{int(timestamp%1000000)}"
    
    os.makedirs(os.path.dirname(memory_file), exist_ok=True)
    with open(memory_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## {memory_id}\n")
        f.write(f"- **类型**: {mem_type}\n")
        f.write(f"- **重要度**: {importance}\n")
        f.write(f"- **内容**: {content}\n")
        f.write(f"- **标签**: {tags or '无'}\n")
        f.write(f"- **上下文**: {context or '无'}\n")
        f.write(f"- **时间**: {date}\n")
        f.write(f"- **确认**: 否\n")
    
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = {"version": 1, "lastUpdate": 0, "memories": []}
    
    new_entry = {
        "id": memory_id,
        "type": mem_type,
        "importance": int(importance),
        "timestamp": timestamp,
        "date": date,
        "content": content,
        "tags": tags or "",
        "context": context or "",
        "tier": tier,
        "file": memory_file,
        "confirmed": False
    }
    index["memories"].append(new_entry)
    index["lastUpdate"] = timestamp
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"[CAPTURED] id={memory_id} type={mem_type} tier={tier}")
    return memory_id

if __name__ == '__main__':
    capture(
        sys.argv[1], sys.argv[2], int(sys.argv[3]),
        sys.argv[4] if len(sys.argv) > 4 else '',
        sys.argv[5] if len(sys.argv) > 5 else '',
        sys.argv[6] if len(sys.argv) > 6 else 'current',
        sys.argv[7] if len(sys.argv) > 7 else '/tmp/memory.md',
        sys.argv[8] if len(sys.argv) > 8 else '/tmp/index.json'
    )
