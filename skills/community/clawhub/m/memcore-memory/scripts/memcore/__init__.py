"""
MemCore — MemOS-inspired memory enhancement for OpenClaw.

四层记忆模型（对标 MemOS L1→L2→L3→Skill）+ 三层检索 + 反馈闭环

L1 trace : 结构化步骤记录（action, observation, reflection, value_score）
L2 policy: 跨日志模式自动归纳 → 策略建议
L3 world : 压缩的环境认知 → SOUL.md/AGENTS.md 更新建议
Skill    : 高价值模式自动结晶 → skills/ 创建/更新建议
"""

__version__ = "0.1.0"
