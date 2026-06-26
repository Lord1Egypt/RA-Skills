#!/usr/bin/env python3
"""存储记忆到 mflow"""
import sys
sys.path.insert(0, 'C:\\Users\\wry08\\.openclaw\\skills\\oclaw-hermes\\scripts')
from mflow import MFlowEngine, MemoryEntry
from datetime import datetime
import hashlib
import time

engine = MFlowEngine()

# 存储 Skill 记忆
entry = MemoryEntry(
    id=hashlib.md5(f"skill_cn_construction_mediation_{time.time()}".encode()).hexdigest()[:16],
    layer="skill",
    content="""Skill: cn-construction-mediation 使用经验

使用场景：建设工程商事调解咨询
核心能力：
1. 调解流程设计
2. 利益方识别与分析
3. BATNA/WATNA评估
4. 调解协议起草
5. 司法确认指导

最佳实践：
- 结合《商事调解条例》最新规定
- 参考大连建工调解模式
- 引入工程造价专业鉴定
- 注重调解窗口期把握

相关法规：
- 《商事调解条例》（2026年5月1日施行）
- 《人民调解法》
- 《民事诉讼法》第201-202条
- 《建设工程施工合同（示范文本）》GF-2017-0201""",
    source="deerflow",
    timestamp=datetime.now(),
    metadata={"skill_name": "cn-construction-mediation", "category": "engineering"}
)

success = engine.store(entry)
print(f"Skill 记忆存储: {'成功' if success else '失败'}")

# 存储即时记忆 - 当前会话
entry2 = MemoryEntry(
    id=hashlib.md5(f"instant_session_{time.time()}".encode()).hexdigest()[:16],
    layer="instant",
    content="用户请求：向量检索相关记忆和经验，利用 hermes 五层记忆体 mflow 进行记忆更新。已执行：1)查看mflow统计 2)存储建设工程商事调解研究报告到长期记忆 3)存储Skill使用经验到技能记忆层",
    source="hermes",
    timestamp=datetime.now(),
    metadata={"session_id": "2026-04-11-22-25", "action": "memory_update"}
)

success2 = engine.store(entry2)
print(f"即时记忆存储: {'成功' if success2 else '失败'}")

# 显示当前统计
stats = engine.get_stats()
print(f"\n记忆统计:")
print(f"  总计: {stats.get('total_count', 0)} 条")
print(f"  长期记忆: {stats.get('long_count', 0)} 条")
print(f"  技能记忆: {stats.get('skill_count', 0)} 条")
print(f"  即时记忆: {stats.get('instant_count', 0)} 条")
print(f"  未同步: {stats.get('unsynced_count', 0)} 条")
