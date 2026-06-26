#!/usr/bin/env python3
"""
INTJ Coach 用户档案初始化脚本

用法：
    python3 scripts/init-user-profile.py <user_id> [user_name]

示例：
    python3 scripts/init-user-profile.py ou_edd5093957e635ba596629b2ae18ba1a 燃冰
"""

import sys
import os
from datetime import datetime

def init_user_profile(user_id: str, user_name: str = "未知用户"):
    """初始化用户档案"""
    
    base_dir = os.path.expanduser("~/.openclaw/workspace/memory/intj-users")
    os.makedirs(base_dir, exist_ok=True)
    
    # 创建主档案
    profile_path = os.path.join(base_dir, f"{user_id}-profile.md")
    profile_content = f"""# INTJ 用户档案

**用户 ID**: {user_id}
**用户名称**: {user_name}
**创建时间**: {datetime.now().strftime('%Y-%m-%d')}
**最后更新**: {datetime.now().strftime('%Y-%m-%d')}

## 基本信息
- 年龄：待填写
- 职业：待填写
- 当前状态：（工作/创业/待业）

## 核心目标
- 长期目标（1-3 年）：待填写
- 中期目标（3-6 月）：待填写
- 短期目标（1 月内）：待填写

## INTJ 特质表现
- 优势：待填写
- 卡点：待填写
- 内耗模式：待填写

## 历史关键决策
- 暂无

---
*本档案由 INTJ Coach 自动创建，请在后续对话中逐步完善。*
"""
    
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(profile_content)
    
    # 创建对话历史
    sessions_path = os.path.join(base_dir, f"{user_id}-sessions.md")
    sessions_content = f"""# 对话历史

**用户 ID**: {user_id}
**用户名称**: {user_name}

---
*对话记录将在此追加，每次对话后自动更新。*
"""
    
    with open(sessions_path, 'w', encoding='utf-8') as f:
        f.write(sessions_content)
    
    # 创建行动追踪
    actions_path = os.path.join(base_dir, f"{user_id}-actions.md")
    actions_content = f"""# 行动追踪

**用户 ID**: {user_id}
**用户名称**: {user_name}

## 进行中
- 暂无

## 已完成
- 暂无

## 已放弃
- 暂无

---
*行动追踪将在此更新，每次对话后自动追加新行动。*
"""
    
    with open(actions_path, 'w', encoding='utf-8') as f:
        f.write(actions_content)
    
    print(f"✅ 用户档案初始化完成")
    print(f"   用户 ID: {user_id}")
    print(f"   用户名称：{user_name}")
    print(f"   档案位置：{base_dir}")
    print(f"   创建文件:")
    print(f"     - {profile_path}")
    print(f"     - {sessions_path}")
    print(f"     - {actions_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 scripts/init-user-profile.py <user_id> [user_name]")
        print("示例：python3 scripts/init-user-profile.py ou_edd5093957e635ba596629b2ae18ba1a 燃冰")
        sys.exit(1)
    
    user_id = sys.argv[1]
    user_name = sys.argv[2] if len(sys.argv) > 2 else "未知用户"
    
    init_user_profile(user_id, user_name)
