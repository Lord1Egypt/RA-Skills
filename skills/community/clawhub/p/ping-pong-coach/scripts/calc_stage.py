#!/usr/bin/env python3
"""
根据学习年限计算乒乓球学习当前阶段和剩余时间

用法:
  python3 calc_stage.py <学习年限> [年龄]

示例:
  python3 calc_stage.py 1.5
  python3 calc_stage.py 2 12
"""

import sys
from typing import Optional

# 各阶段时长配置（单位：年）
STAGES = [
    {
        "stage": 1,
        "name": "定型握拍站姿球感",
        "duration_months": 3,  # 按最大值估算
        "keywords": ["握拍", "站姿", "球感", "颠球"]
    },
    {
        "stage": 2,
        "name": "正反手基础定点单项",
        "duration_months": 6,
        "keywords": ["正手", "反手", "攻球", "拨球", "定点"]
    },
    {
        "stage": 3,
        "name": "基础步法 + 发球搓球",
        "duration_months": 6,
        "keywords": ["步法", "发球", "搓球"]
    },
    {
        "stage": 4,
        "name": "下旋起拉 + 组合衔接",
        "duration_months": 12,
        "keywords": ["下旋", "起拉", "弧圈", "组合"]
    },
    {
        "stage": 5,
        "name": "台内小球 + 攻防相持",
        "duration_months": 12,
        "keywords": ["台内", "挑打", "拧拉", "相持"]
    },
    {
        "stage": 6,
        "name": "战术套路 + 高强度实战",
        "duration_months": 24,
        "keywords": ["战术", "套路", "实战", "比赛"]
    },
    {
        "stage": 7,
        "name": "个人特长打磨 + 选材竞技",
        "duration_months": None,  # 长期/终身
        "keywords": ["特长", "竞技", "打磨"]
    },
]


def calc_stage(learning_years: float, age: Optional[int] = None) -> dict:
    """
    根据学习年限计算当前阶段
    
    返回:
        {
            "current_stage": int,        # 当前阶段 (1-7)
            "current_stage_name": str,   # 当前阶段名称
            "total_months": int,         # 到阶段7的总月数
            "completed_months": float,    # 已完成的月数
            "remaining_months": float,    # 剩余月数
            "progress_percent": float,    # 总体进度百分比
            "current_stage_progress": float,  # 当前阶段内进度 %
            "is_beyond_all": bool,       # 是否已超过所有阶段
        }
    """
    total_months = sum(
        s["duration_months"] for s in STAGES if s["duration_months"]
    )  # = 63个月 ≈ 5.25年

    total_learning_months = learning_years * 12
    accumulated = 0.0

    for i, stage in enumerate(STAGES):
        if stage["duration_months"] is None:
            # 第7阶段：长期，持续精进
            if total_learning_months >= accumulated:
                return {
                    "current_stage": 7,
                    "current_stage_name": stage["name"],
                    "total_months": total_months,
                    "completed_months": total_learning_months,
                    "remaining_months": None,
                    "progress_percent": min(100, total_learning_months / total_months * 100),
                    "current_stage_progress": None,
                    "is_beyond_all": True,
                    "message": "已进入第7阶段（个人特长打磨+竞技），持续精进中！"
                }
            break

        stage_months = stage["duration_months"]

        if total_learning_months <= accumulated + stage_months:
            # 落在当前阶段内
            current_stage_progress = (total_learning_months - accumulated) / stage_months * 100
            return {
                "current_stage": stage["stage"],
                "current_stage_name": stage["name"],
                "total_months": total_months,
                "completed_months": total_learning_months,
                "remaining_months": total_months - total_learning_months,
                "progress_percent": total_learning_months / total_months * 100,
                "current_stage_progress": current_stage_progress,
                "is_beyond_all": False,
                "next_stage": STAGES[i + 1]["name"] if i + 1 < len(STAGES) else None,
            }

        accumulated += stage_months

    # 兜底：超过所有已知阶段
    return {
        "current_stage": 7,
        "current_stage_name": STAGES[-1]["name"],
        "total_months": total_months,
        "completed_months": total_learning_months,
        "remaining_months": 0,
        "progress_percent": 100,
        "current_stage_progress": 100,
        "is_beyond_all": False,
    }


def format_output(result: dict, age: Optional[int] = None) -> str:
    """格式化输出为友好文字"""
    lines = []
    lines.append("📊 乒乓球学习阶段分析")
    lines.append("=" * 30)

    if age:
        lines.append(f"👤 年龄：{age} 岁")
    lines.append(f"⏱️ 学习时长：{result['completed_months']:.1f} 个月（约 {result['completed_months']/12:.1f} 年）")
    lines.append("")

    if "message" in result and result.get("is_beyond_all"):
        lines.append(f"🎯 当前阶段：**第 {result['current_stage']} 阶段** — {result['current_stage_name']}")
        lines.append(f"   {result['message']}")
        return "\n".join(lines)

    lines.append(f"🎯 当前阶段：**第 {result['current_stage']} 阶段** — {result['current_stage_name']}")
    lines.append(f"   当前阶段进度：{result['current_stage_progress']:.0f}%")

    if result.get("next_stage"):
        lines.append(f"   下一阶段：{result['next_stage']}")

    lines.append("")
    lines.append(f"📈 总体进度：{result['progress_percent']:.0f}%（共 7 个阶段，约 {result['total_months']} 个月 ≈ {result['total_months']/12:.1f} 年）")

    if result['remaining_months'] is not None and result['remaining_months'] > 0:
        lines.append(f"⏳ 距全部阶段完成约需：{result['remaining_months']:.0f} 个月（约 {result['remaining_months']/12:.1f} 年）")
    elif result['remaining_months'] == 0:
        lines.append("✅ 已完成全部阶段的基础学习！")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 calc_stage.py <学习年限> [年龄]")
        print("示例: python3 calc_stage.py 1.5 10")
        sys.exit(1)

    try:
        years = float(sys.argv[1])
    except ValueError:
        print("错误: 学习年限必须是数字")
        sys.exit(1)

    age = int(sys.argv[2]) if len(sys.argv) >= 3 else None

    if years < 0:
        print("错误: 学习年限不能为负数")
        sys.exit(1)

    result = calc_stage(years, age)
    print(format_output(result, age))
