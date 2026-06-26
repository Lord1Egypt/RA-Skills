#!/usr/bin/env python3
"""
hermes-memory-bridge / hermes_learning_sync.py
Hermes 学习材料同步模块
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

# 配置路径
HERMES_HOME = Path.home() / ".hermes"
SHARED_DIR = HERMES_HOME / "shared"
PROCESSED_DIR = SHARED_DIR / "processed"
WORKBUDDY_SKILLS_DIR = Path.home() / ".workbuddy" / "skills"
WORKBUDDY_LEARNING_DIR = WORKBUDDY_SKILLS_DIR / "hermes-learning"

def ensure_dirs():
    """确保所有必要的目录存在"""
    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    WORKBUDDY_LEARNING_DIR.mkdir(parents=True, exist_ok=True)

def get_latest_learning_materials():
    """获取最新的学习材料"""
    materials = {}
    
    # 1. 读取记忆摘要
    summary_path = SHARED_DIR / "memory_summary.json"
    if summary_path.exists():
        with open(summary_path, 'r', encoding='utf-8') as f:
            materials["summary"] = json.load(f)
    
    # 2. 读取完整学习材料
    learning_path = PROCESSED_DIR / "learning_materials.json"
    if learning_path.exists():
        with open(learning_path, 'r', encoding='utf-8') as f:
            materials["full_learning"] = json.load(f)
    
    # 3. 读取记忆反馈
    feedback_path = SHARED_DIR / "memory_feedback.json"
    if feedback_path.exists():
        with open(feedback_path, 'r', encoding='utf-8') as f:
            materials["feedback"] = json.load(f)
    
    return materials

def create_workbuddy_learning_files(materials):
    """为 WorkBuddy 创建学习文件"""
    
    # 1. 创建技能目录结构
    skill_dir = WORKBUDDY_LEARNING_DIR
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. 创建简化的学习应用脚本
    learning_script = '''#!/usr/bin/env python3
"""
Hermes 学习材料应用脚本 - 简化版
"""

import json
import sys
from pathlib import Path

HERMES_SHARED = Path.home() / ".hermes" / "shared"

def load_summary():
    """加载学习摘要"""
    summary_path = HERMES_SHARED / "memory_summary.json"
    if summary_path.exists():
        with open(summary_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def apply_learnings():
    """应用学习材料"""
    summary = load_summary()
    
    print("🚀 应用 Hermes 学习材料...")
    
    # 应用成功模式
    for insight in summary.get("key_insights", []):
        if insight.get("title") == "成功任务模式":
            examples = insight.get("examples", [])
            print(f"✅ 学习 {len(examples)} 个成功案例")
            # 在实际应用中，这里会更新 WorkBuddy 的策略
    
    print("🎉 学习材料应用完成！")

def show_summary():
    """显示摘要"""
    summary = load_summary()
    
    print("📚 Hermes 学习摘要")
    print("=" * 40)
    print(f"最后更新: {summary.get('last_update', '未知')}")
    print(f"总记忆: {summary.get('total_memories', 0)}")
    
    for insight in summary.get("key_insights", []):
        print(f"\\n{insight.get('title', '未知')}:")
        print(f"  {insight.get('description', '')}")
        print(f"  示例: {len(insight.get('examples', []))}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "apply":
        apply_learnings()
    else:
        show_summary()
'''
    
    script_path = skill_dir / "apply_learning.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(learning_script)
    
    # 3. 使脚本可执行
    os.chmod(script_path, 0o755)
    
    # 4. 创建状态文件
    sync_status = {
        "last_sync_time": datetime.now().isoformat(),
        "materials_count": len(materials),
        "summary_entries": materials.get('summary', {}).get('total_memories', 0),
        "key_insights": len(materials.get('summary', {}).get('key_insights', [])),
        "status": "synced"
    }
    
    status_path = skill_dir / "sync_status.json"
    with open(status_path, 'w', encoding='utf-8') as f:
        json.dump(sync_status, f, ensure_ascii=False, indent=2)
    
    return skill_dir, sync_status

def sync_learning_materials():
    """同步学习材料到 WorkBuddy"""
    
    ensure_dirs()
    
    # 1. 获取学习材料
    materials = get_latest_learning_materials()
    if not materials:
        print("📭 未找到学习材料")
        return False
    
    print(f"📚 找到 {len(materials)} 类学习材料")
    
    # 2. 创建 WorkBuddy 学习文件
    skill_dir, sync_status = create_workbuddy_learning_files(materials)
    
    # 3. 复制关键文件
    print("📋 复制学习文件...")
    files_to_copy = ["memory_summary.json", "memory_feedback.json"]
    
    for file_name in files_to_copy:
        src = SHARED_DIR / file_name
        dst = skill_dir / file_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ {file_name}")
    
    # 4. 记录桥接事件
    update_bridge_event({
        "type": "learning_sync",
        "materials_count": len(materials),
        "summary_entries": sync_status["summary_entries"],
        "key_insights": sync_status["key_insights"]
    })
    
    print(f"\\n🎉 同步完成！")
    print(f"📁 位置: {skill_dir}")
    
    return True

def get_learning_stats():
    """获取学习材料统计"""
    status_path = WORKBUDDY_LEARNING_DIR / "sync_status.json"
    
    if status_path.exists():
        with open(status_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 返回默认值
    return {
        "last_sync_time": "从未同步",
        "materials_count": 0,
        "summary_entries": 0,
        "key_insights": 0,
        "status": "not_synced"
    }

def update_bridge_event(data):
    """更新桥接事件"""
    meta_path = SHARED_DIR / "meta.json"
    
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    else:
        meta = {"events": []}
    
    event = {
        "type": "learning_sync",
        "timestamp": datetime.now().isoformat(),
        **data
    }
    
    meta["events"].append(event)
    # 保留最近100条
    meta["events"] = meta["events"][-100:]
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def main():
    """独立运行"""
    success = sync_learning_materials()
    if success:
        print("✅ Hermes 学习材料同步成功！")
    else:
        print("❌ 同步失败")

if __name__ == "__main__":
    main()