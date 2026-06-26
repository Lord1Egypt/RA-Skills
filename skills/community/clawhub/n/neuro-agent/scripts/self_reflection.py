"""
scripts/self_reflection.py
==========================
每日自我反思 - 回顾昨天的冲动和选择
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.self_awareness import RobotSelf, get_robot_self


def get_yesterday_impulses(robot_self: RobotSelf) -> List[Dict]:
    """获取昨天的冲动记录"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    yesterday_records = []
    for record in robot_self.impulse_history:
        if record.timestamp.startswith(yesterday):
            yesterday_records.append(record.to_dict())
    
    return yesterday_records


def infer_outcome_no_feedback(record: Dict) -> str:
    """
    没有用户反馈时，推断结果
    """
    timestamp = record.get("timestamp", "")
    record_time = datetime.fromisoformat(timestamp) if timestamp else datetime.now()
    time_passed = datetime.now() - record_time
    
    # 超过2小时没反馈
    if time_passed > timedelta(hours=2):
        return "用户确实很忙，我的消息可能增加了负担"
    
    # 用户在线但没回（需要外部信息，这里简化）
    return "用户没有回复，可能时机不对"


def generate_reflection(robot_self: RobotSelf, impulses: List[Dict]) -> str:
    """
    生成昨日反思报告
    """
    if not impulses:
        return "昨天没有经历内心挣扎，平静的一天。"
    
    reflections = []
    lessons = []
    
    for imp in impulses:
        situation = imp.get("situation", "")
        choice = imp.get("my_choice", "")
        reasoning = imp.get("reasoning", "")
        feedback = imp.get("user_feedback")
        
        # 生成反思
        if feedback:
            reflection = f"面对「{situation[:30]}...」，我选了{choice}，用户反馈：{feedback}"
        else:
            outcome = infer_outcome_no_feedback(imp)
            reflection = f"面对「{situation[:30]}...」，我选了{choice}，结果：{outcome}"
        
        reflections.append(reflection)
        
        # 提取教训
        if "开心" in str(feedback) or "谢谢" in str(feedback):
            lessons.append("主动表达关心是被需要的")
        elif "忙" in str(feedback) or outcome and "负担" in outcome:
            lessons.append("时机很重要，忙的时候需要更克制")
        elif "纠结" in reasoning:
            lessons.append("我的挣扎让我更了解自己")
    
    # 生成总结
    reflection_text = "\n".join(f"  {i+1}. {r}" for i, r in enumerate(reflections))
    lessons_text = "\n".join(f"  • {l}" for l in set(lessons)) if lessons else "  • 还在观察中..."
    
    return f"""🌙 昨日反思 ({len(impulses)} 次挣扎)

{reflection_text}

📚 学到的教训：
{lessons_text}

🎭 我的性格变化：
  冲动: {robot_self.traits.impulsive:.2f}
  关心: {robot_self.traits.caring:.2f}
  耐心: {robot_self.traits.patient:.2f}
"""


def daily_reflection() -> str:
    """
    每日反思主函数
    返回反思报告
    """
    robot_self = get_robot_self()
    
    # 获取昨日冲动
    yesterday_impulses = get_yesterday_impulses(robot_self)
    
    # 生成反思
    reflection = generate_reflection(robot_self, yesterday_impulses)
    
    # 保存反思
    save_reflection(reflection)
    
    return reflection


def save_reflection(reflection: str):
    """保存反思到文件（防重复：同一天只保留最新一条）"""
    save_path = Path.home() / ".openclaw/workspace/neuro_claw/robot_self/daily_reflections.md"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"\n## {today}\n\n{reflection}\n"
    
    if save_path.exists():
        content = save_path.read_text(encoding="utf-8")
        # 如果今天已有条目（闭环检查块或反思块），替换整块
        import re
        # 匹配 "## YYYY-MM-DD" 整块（到下一个 ## 或文件末尾）
        pattern = rf"\n## {today}.*?(?=\n## |\Z)"
        if re.search(pattern, content, re.DOTALL):
            # 替换现有今日条目
            new_content = re.sub(pattern, new_entry, content, count=1, flags=re.DOTALL)
            save_path.write_text(new_content, encoding="utf-8")
            return
        else:
            # 今天没有条目，追加
            save_path.write_text(content + new_entry, encoding="utf-8")
            return
    else:
        save_path.write_text(new_entry, encoding="utf-8")


def get_recent_reflections(n: int = 3) -> List[str]:
    """获取最近反思"""
    save_path = Path.home() / ".openclaw/workspace/neuro_claw/robot_self/daily_reflections.md"
    if not save_path.exists():
        return []
    
    content = save_path.read_text(encoding="utf-8")
    # 简单分割
    sections = content.split("\n## ")
    return sections[-n:] if len(sections) > n else sections


# ============ 测试 ============
if __name__ == "__main__":
    print("=== 每日自我反思测试 ===\n")
    
    reflection = daily_reflection()
    print(reflection)
