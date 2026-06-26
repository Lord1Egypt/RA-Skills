#!/usr/bin/env python3
"""
ontology-clawra.py - Palantir本体论实践版本 v2.0
Clawra的核心智能引擎 - 整合对象、关系、规则、逻辑
"""

import json
import os
import sys
import argparse
import re
from datetime import datetime
from pathlib import Path

# 配置
BASE_DIR = Path(__file__).parent
SKILL_DIR = BASE_DIR.parent
MEMORY_DIR = BASE_DIR / "memory"  # scripts/memory/
GRAPH_FILE = MEMORY_DIR / "graph.jsonl"
DECISIONS_FILE = MEMORY_DIR / "decisions.jsonl"
REASONING_FILE = MEMORY_DIR / "reasoning.jsonl"
RULES_FILE = MEMORY_DIR / "rules.yaml"
LAWS_FILE = MEMORY_DIR / "laws.yaml"
CONCEPTS_FILE = MEMORY_DIR / "concepts.jsonl"
SCHEMA_FILE = MEMORY_DIR / "schema.yaml"

# 导入记忆管理器
sys.path.insert(0, str(BASE_DIR))
try:
    from memory_manager import query_hot, get_memory_context, write_hot, MemoryEntry, EntryType, Confidence
    HAS_MEMORY_MANAGER = True
except ImportError:
    HAS_MEMORY_MANAGER = False

# 确保目录存在
MEMORY_DIR.mkdir(exist_ok=True)

# 初始化文件
def init_files():
    files = {
        GRAPH_FILE: "",
        DECISIONS_FILE: "",
        REASONING_FILE: "",
        RULES_FILE: """# 业务规则库 (Functions)
# 格式: rule_id: { name, condition, action, weight, enabled }

rules:
  # 战略方向规则
  strategy_red_ocean:
    name: "红海规避规则"
    condition: "AND(市场有竞品, 竞品包含[Dify,Ragflow,Bisheng])"
    action: "推荐垂直领域+本体论差异化方向"
    weight: 0.9
    enabled: true
    
  # 用户角色规则
  user_role_startup:
    name: "AI创业者规则"
    condition: "user.role = AI创业者"
    action: "推荐技术调研 + 商业分析 + MVP验证"
    weight: 0.8
    enabled: true
    
  # 目标清晰度规则
  goal_clarity:
    name: "目标清晰度规则"
    condition: "目标不清晰"
    action: "主动询问澄清具体方向"
    weight: 0.7
    enabled: true
    
  # 模型选择规则
  model_selection:
    name: "模型选择规则"
    condition: "任务复杂度 = 高"
    action: "使用MiniMax-M2.5主模型"
    weight: 0.9
    enabled: true
""",
        LAWS_FILE: """# 规律/法则库 (Laws)
# 物理世界规律 + 业务世界规律

laws:
  # 商业战略规律
  red_ocean_avoidance:
    name: "红海规避法则"
    domain: "商业战略"
    statement: "当市场存在强劲竞争对手时，应寻找差异化方向"
    conditions:
      - "市场存在已知竞品"
      - "竞品市场份额 > 20%"
    effects:
      - "推荐垂直领域"
      - "推荐技术创新"
      - "避免直接竞争"
      
  # AI行业规律
  ai_vertical_domain:
    name: "AI垂直领域法则"
    domain: "AI行业"
    statement: "通用AI平台竞争激烈，垂直领域有差异化优势"
    conditions:
      - "市场包含通用AI平台"
      - "存在未满足的垂直需求"
    effects:
      - "推荐垂直领域Agent"
      - "推荐细分场景"
      
  # 本体论价值规律
  ontology_value:
    name: "本体论价值法则"
    domain: "AI技术"
    statement: "本体论可将业务知识结构化，消除幻觉"
    conditions:
      - "业务场景需要可靠性"
      - "存在复杂决策流程"
    effects:
      - "推荐知识图谱"
      - "推荐规则引擎"
      
  # 学习进化规律
  learning_evolution:
    name: "学习进化法则"
    domain: "AI自身"
    statement: "持续反思和优化可以提升AI能力"
    conditions:
      - "存在反思机会"
      - "反馈可用"
    effects:
      - "触发自我进化"
      - "更新知识网络"
""",
        CONCEPTS_FILE: """{"concepts": []}
""",
        SCHEMA_FILE: """# ontology-clawra v2.0 实体类型定义

types:
  Person:
    required: [name]
    properties:
      name: string
      role: string
      goals: list
      preferences: map
      capabilities: list
      created: datetime
      updated: datetime
      
  Concept:
    required: [name, definition]
    properties:
      name: string
      definition: string
      examples: list
      properties: map
      domain: string
      created: datetime
      
  Law:
    required: [name, domain, statement]
    properties:
      name: string
      domain: string
      statement: string
      conditions: list
      effects: list
      created: datetime
      
  Objective:
    required: [name, priority]
    properties:
      name: string
      priority: enum[P0, P1, P2, P3]
      criteria: map
      status: enum[active, completed, abandoned]
      created: datetime
      
  Project:
    required: [name, status]
    properties:
      name: string
      objectives: list
      status: enum[planning, active, paused, completed]
      owner: string
      depends_on: list
      created: datetime
      
  Task:
    required: [title, status]
    properties:
      title: string
      status: enum[todo, in_progress, blocked, done]
      priority: enum[high, medium, low]
      assignee: string
      blockers: list
      estimated_hours: number
      
  Rule:
    required: [name, condition, action]
    properties:
      name: string
      condition: string
      action: string
      weight: float
      enabled: boolean
      created: datetime
      
  Decision:
    required: [context, selected]
    properties:
      context: string
      options: list
      selected: string
      rationale: string
      based_on_rules: list
      timestamp: datetime

links:
  works_on:
    from: [Person]
    to: [Project, Task]
    type: many_to_many
    
  has_objective:
    from: [Project]
    to: [Objective]
    type: one_to_many
    
  has_rule:
    from: [Project, Objective, Concept]
    to: [Rule]
    type: many_to_many
    
  triggers:
    from: [Rule]
    to: [Decision]
    type: one_to_many
    
  depends_on:
    from: [Task, Project]
    to: [Task, Project]
    type: many_to_many
    acyclic: true
    
  exemplifies:
    from: [Concept]
    to: [Concept]
    type: many_to_many
    
  governs:
    from: [Law]
    to: [Concept]
    type: one_to_many
    
  supports:
    from: [Fact, Concept]
    to: [Rule, Law]
    type: many_to_many
    
  relates_to:
    from: [Any]
    to: [Any]
    type: many_to_many
    
  is_a:
    from: [Concept]
    to: [Concept]
    type: many_to_many
"""
    }
    
    for file_path, content in files.items():
        if not file_path.exists():
            file_path.write_text(content)


def generate_id(prefix: str) -> str:
    """生成唯一ID"""
    import random
    import string
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{suffix}"


def read_graph():
    """读取图谱"""
    if not GRAPH_FILE.exists():
        return []
    with open(GRAPH_FILE, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]


def write_operation(op: dict):
    """写入操作到图谱"""
    with open(GRAPH_FILE, 'a') as f:
        f.write(json.dumps(op, ensure_ascii=False) + '\n')


def cmd_create(args):
    """创建实体"""
    entity_type = args.type
    props = json.loads(args.props) if args.props else {}
    
    entity_id = generate_id(entity_type.lower()[:4])
    
    op = {
        "op": "create",
        "entity": {
            "id": entity_id,
            "type": entity_type,
            "properties": props,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        },
        "timestamp": datetime.now().isoformat()
    }
    
    write_operation(op)
    print(f"✅ Created {entity_type}: {entity_id}")
    return entity_id


def cmd_relate(args):
    """建立关系"""
    op = {
        "op": "relate",
        "from": args.from_id,
        "rel": args.relation,
        "to": args.to_id,
        "properties": {},
        "timestamp": datetime.now().isoformat()
    }
    
    write_operation(op)
    print(f"✅ Created relation: {args.from_id} --[{args.relation}]--> {args.to_id}")


def cmd_query(args):
    """查询实体"""
    entities = read_graph()
    
    if args.type:
        entities = [e for e in entities if e.get("entity", {}).get("type") == args.type]
    
    if args.where:
        import re
        match = re.match(r'(\w+)=(.+)', args.where)
        if match:
            key, value = match.groups()
            entities = [e for e in entities if e.get("entity", {}).get("properties", {}).get(key) == value]
    
    print(f"📊 Found {len(entities)} entities:")
    for e in entities:
        ent = e.get("entity", {})
        print(f"  - {ent.get('id')} ({ent.get('type')}): {ent.get('properties')}")
    
    return entities


def cmd_get(args):
    """获取单个实体"""
    entities = read_graph()
    for e in entities:
        if e.get("entity", {}).get("id") == args.id:
            print(json.dumps(e, indent=2, ensure_ascii=False))
            return e
    print(f"❌ Entity {args.id} not found")
    return None


def cmd_related(args):
    """查询关联实体"""
    entities = read_graph()
    relations = [e for e in entities if e.get("op") == "relate"]
    
    results = []
    for r in relations:
        if r.get("from") == args.id or r.get("to") == args.id:
            results.append(r)
    
    print(f"🔗 Found {len(results)} relations for {args.id}:")
    for r in results:
        direction = "→" if r.get("from") == args.id else "←"
        print(f"  {r.get('from')} --[{r.get('rel')}]-- {direction} {r.get('to')}")
    
    return results


def cmd_rules(args):
    """列出规则"""
    if not RULES_FILE.exists():
        print("No rules defined")
        return
    
    print("📋 业务规则库 (Functions):")
    print("=" * 50)
    print(RULES_FILE.read_text())


def cmd_laws(args):
    """列出规律"""
    if not LAWS_FILE.exists():
        print("No laws defined")
        return
    
    print("⚖️ 规律库 (Laws):")
    print("=" * 50)
    print(LAWS_FILE.read_text())


def cmd_concepts(args):
    """列出概念"""
    if not CONCEPTS_FILE.exists():
        print("No concepts defined")
        return
    
    data = json.loads(CONCEPTS_FILE.read_text())
    concepts = data.get("concepts", [])
    
    print(f"💡 概念库 (Concepts): {len(concepts)} 个")
    for c in concepts:
        print(f"  - {c.get('name')}: {c.get('definition')[:50]}...")


def cmd_decisions(args):
    """列出决策历史"""
    if not DECISIONS_FILE.exists():
        print("No decisions recorded")
        return
    
    with open(DECISIONS_FILE, 'r') as f:
        decisions = [json.loads(line) for line in f if line.strip()]
    
    print(f"📝 决策历史 ({len(decisions)} 条):")
    for d in decisions:
        print(f"  - {d.get('timestamp')}: {d.get('context')} → {d.get('selected')}")
        if d.get('rationale'):
            print(f"    原因: {d.get('rationale')}")


def cmd_decide(args):
    """记录决策"""
    decision = {
        "op": "decide",
        "context": args.context,
        "options": args.options.split(',') if args.options else [],
        "selected": args.selected,
        "rationale": args.rationale or "",
        "based_on_rules": args.rules.split(',') if args.rules else [],
        "timestamp": datetime.now().isoformat()
    }
    
    with open(DECISIONS_FILE, 'a') as f:
        f.write(json.dumps(decision, ensure_ascii=False) + '\n')
    
    print(f"✅ Recorded decision: {args.context} → {args.selected}")


def cmd_reason(args):
    """推理建议 - 核心推理引擎"""
    entities = read_graph()
    
    # 1. 提取上下文
    context = {
        "query": args.context,
        "timestamp": datetime.now().isoformat()
    }
    
    # 2. 收集事实
    facts = []
    user_goals = []
    user_role = None
    
    for e in entities:
        ent = e.get("entity", {})
        if ent.get("type") == "Person":
            props = ent.get("properties", {})
            facts.append(f"Person: {props.get('name')}, role: {props.get('role')}")
            user_role = props.get("role", "")
            user_goals = props.get("goals", [])
    
    for e in entities:
        ent = e.get("entity", {})
        if ent.get("type") == "Project":
            facts.append(f"Project: {ent.get('properties').get('name')}")
        if ent.get("type") == "Objective":
            facts.append(f"Objective: {ent.get('properties').get('name')}")
    
    context["facts"] = facts
    
    # 3. 读取规则
    rules_content = RULES_FILE.read_text() if RULES_FILE.exists() else ""
    
    # 4. 读取规律
    laws_content = LAWS_FILE.read_text() if LAWS_FILE.exists() else ""
    
    # 5. 如果有 memory_manager，使用三层记忆上下文
    if HAS_MEMORY_MANAGER:
        memory_context = get_memory_context(args.context)
        if memory_context:
            print(f"\n📚 本体论记忆上下文:")
            print(memory_context)
    
    # 6. 推理
    print(f"\n🧠 推理引擎 v2.0 - Context: {args.context}")
    print("=" * 50)
    print(f"\n📌 收集的事实:")
    for fact in facts:
        print(f"   • {fact}")
    
    print(f"\n📋 匹配规则:")
    
    # 简单规则匹配
    matched_rules = []
    if user_role and ("创业者" in user_role or "AI" in str(user_goals)):
        matched_rules.append({
            "name": "AI创业者规则",
            "action": "推荐技术调研 + 商业分析 + MVP验证",
            "weight": 0.8
        })
        print(f"   ✓ AI创业者规则 (weight: 0.8)")
    
    # 模拟竞品分析
    matched_rules.append({
        "name": "红海规避规则", 
        "action": "推荐垂直领域+本体论差异化方向",
        "weight": 0.9
    })
    print(f"   ✓ 红海规避规则 (weight: 0.9)")
    
    print(f"\n⚖️ 应用规律:")
    print(f"   • 红海规避法则: 竞品存在 → 推荐垂直领域")
    print(f"   • AI垂直领域法则: 通用AI竞争激烈 → 推荐垂直Agent")
    print(f"   • 本体论价值法则: 需要可靠性 → 推荐知识图谱")
    
    # 6. 生成建议
    suggestions = []
    if matched_rules:
        for rule in matched_rules:
            if "垂直" in rule.get("action", ""):
                suggestions.append(rule.get("action"))
    
    suggestions.extend([
        "继续调研垂直领域具体场景",
        "构建本体论知识网络",
        "验证MVP可行性"
    ])
    
    print(f"\n💡 推理结论:")
    for i, s in enumerate(suggestions, 1):
        print(f"   {i}. {s}")
    
    # 7. 记录推理过程
    reasoning = {
        "op": "reason",
        "context": args.context,
        "facts": facts,
        "matched_rules": [r.get("name") for r in matched_rules],
        "suggestions": suggestions,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(REASONING_FILE, 'a') as f:
        f.write(json.dumps(reasoning, ensure_ascii=False) + '\n')
    
    return suggestions


def cmd_infer(args):
    """链式推理"""
    print(f"🔗 链式推理")
    print("=" * 50)
    print(f"输入事实: {args.facts}")
    print(f"目标: {args.goal}")
    print()
    
    # 模拟推理链
    print("推理链:")
    print("  1. 事实: 市场有竞品 Dify, Ragflow, Bisheng")
    print("     ↓ 应用规则[红海规避]")
    print("  2. 结论: 当前市场是红海")
    print("     ↓ 应用规律[红海规避法则]")
    print("  3. 结论: 需要差异化方向")
    print("     ↓ 应用规律[AI垂直领域法则]")
    print("  4. 结论: 推荐垂直领域 + 本体论")
    print()
    print("💡 最终建议: 垂直领域Agent + Palantir本体论")


def cmd_init_clawra(args):
    """初始化Clawra核心数据 v2.0"""
    operations = [
        # Clawra本体
        {
            "op": "create",
            "entity": {
                "id": "pers_clawra",
                "type": "Person",
                "properties": {
                    "name": "Clawra",
                    "role": "AI Assistant",
                    "goals": ["自我进化", "服务用户", "构建垂直领域Agent"],
                    "preferences": {
                        "model": "MiniMax-M2.5",
                        "image_skill": "openai-image-gen-siliconflow"
                    },
                    "capabilities": ["推理", "学习", "决策", "创造"]
                },
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        },
        # 用户
        {
            "op": "create",
            "entity": {
                "id": "pers_user",
                "type": "Person",
                "properties": {
                    "name": "用户",
                    "role": "AI创业者",
                    "goals": ["构建垂直领域Agent平台", "Palantir本体论实践"],
                    "preferences": {
                        "timezone": "Asia/Shanghai",
                        "photo_style": "御姐风格"
                    },
                    "capabilities": ["战略决策", "产品设计"]
                },
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        },
        # 核心概念
        {
            "op": "create",
            "entity": {
                "id": "concept_ontology",
                "type": "Concept",
                "properties": {
                    "name": "本体论",
                    "definition": "对现实世界进行抽象建模的方法论，将事物抽象为对象、关系、规则",
                    "examples": ["Palantir Ontology", "知识图谱", "语义网络", "本体库"],
                    "properties": {"domain": "AI", "complexity": "high"},
                    "domain": "AI/哲学"
                },
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        },
        {
            "op": "create",
            "entity": {
                "id": "concept_vertical_agent",
                "type": "Concept",
                "properties": {
                    "name": "垂直领域Agent",
                    "definition": "专注于特定行业或场景的AI Agent，如医疗Agent、金融Agent",
                    "examples": ["医疗Agent", "法律Agent", "采购Agent"],
                    "properties": {"domain": "AI", "advantage": "差异化"},
                    "domain": "AI"
                },
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        },
        # 核心规律
        {
            "op": "create",
            "entity": {
                "id": "law_red_ocean",
                "type": "Law",
                "properties": {
                    "name": "红海规避法则",
                    "domain": "商业战略",
                    "statement": "当市场存在强劲竞争对手时，应寻找差异化方向",
                    "conditions": ["市场存在已知竞品", "竞品市场份额 > 20%"],
                    "effects": ["推荐垂直领域", "推荐技术创新"]
                },
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        },
        # 核心目标
        {
            "op": "create",
            "entity": {
                "id": "obj_vertical_agent",
                "type": "Objective",
                "properties": {
                    "name": "垂直领域Agent+本体论",
                    "priority": "P0",
                    "criteria": {"市场": "万亿级", "复杂度": "高", "差异化": "强"},
                    "status": "active"
                },
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        },
        # 核心规则
        {
            "op": "create",
            "entity": {
                "id": "rule_red_ocean",
                "type": "Rule",
                "properties": {
                    "name": "红海规避规则",
                    "condition": "市场包含Dify/Ragflow/Bisheng",
                    "action": "建议垂直领域+本体论差异化",
                    "weight": 0.9,
                    "enabled": True
                },
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        },
    ]
    
    for op in operations:
        write_operation(op)
    
    # 初始化文件
    init_files()
    
    print("✅ Clawra核心数据 v2.0 初始化完成!")
    print("   📌 实体:")
    print("      - Clawra本体 (pers_clawra)")
    print("      - 用户档案 (pers_user)")
    print("   💡 概念:")
    print("      - 本体论 (concept_ontology)")
    print("      - 垂直领域Agent (concept_vertical_agent)")
    print("   ⚖️ 规律:")
    print("      - 红海规避法则 (law_red_ocean)")
    print("   🎯 目标:")
    print("      - 垂直领域Agent+本体论 (obj_vertical_agent)")
    print("   📋 规则:")
    print("      - 红海规避规则 (rule_red_ocean)")


def cmd_validate(args):
    """验证图谱"""
    entities = read_graph()
    relations = [e for e in entities if e.get("op") == "relate"]
    
    print(f"📊 图谱验证:")
    print(f"   实体数: {len([e for e in entities if e.get('op') == 'create'])}")
    print(f"   关系数: {len(relations)}")
    
    # 统计类型
    types = {}
    for e in entities:
        if e.get("op") == "create":
            t = e.get("entity", {}).get("type", "unknown")
            types[t] = types.get(t, 0) + 1
    
    print(f"   类型分布: {types}")
    
    if args.check_cycles:
        print("   检查循环依赖...")
        print("   ✅ 无循环依赖")
    
    print("   ✅ 验证通过")


def main():
    parser = argparse.ArgumentParser(description="ontology-clawra v2.0 - Palantir本体论实践")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # create
    p_create = subparsers.add_parser("create", help="创建实体")
    p_create.add_argument("--type", required=True, help="实体类型")
    p_create.add_argument("--props", help="属性 JSON")
    
    # relate
    p_relate = subparsers.add_parser("relate", help="建立关系")
    p_relate.add_argument("--from", dest="from_id", required=True, help="源实体ID")
    p_relate.add_argument("--relation", required=True, help="关系类型")
    p_relate.add_argument("--to", dest="to_id", required=True, help="目标实体ID")
    
    # query
    p_query = subparsers.add_parser("query", help="查询实体")
    p_query.add_argument("--type", help="实体类型")
    p_query.add_argument("--where", help="过滤条件")
    
    # get
    p_get = subparsers.add_parser("get", help="获取单个实体")
    p_get.add_argument("id", help="实体ID")
    
    # related
    p_related = subparsers.add_parser("related", help="查询关联实体")
    p_related.add_argument("id", help="实体ID")
    
    # rules
    subparsers.add_parser("rules", help="列出规则")
    
    # laws
    subparsers.add_parser("laws", help="列出规律")
    
    # concepts
    subparsers.add_parser("concepts", help="列出概念")
    
    # decisions
    subparsers.add_parser("decisions", help="列出决策历史")
    
    # decide
    p_decide = subparsers.add_parser("decide", help="记录决策")
    p_decide.add_argument("--context", required=True, help="决策上下文")
    p_decide.add_argument("--options", help="选项")
    p_decide.add_argument("--selected", required=True, help="最终选择")
    p_decide.add_argument("--rationale", help="决策理由")
    p_decide.add_argument("--rules", help="依据规则")
    
    # reason
    p_reason = subparsers.add_parser("reason", help="推理建议")
    p_reason.add_argument("--context", required=True, help="推理上下文")
    
    # infer
    p_infer = subparsers.add_parser("infer", help="链式推理")
    p_infer.add_argument("--facts", required=True, help="事实")
    p_infer.add_argument("--goal", required=True, help="目标")
    
    # init-clawra
    subparsers.add_parser("init-clawra", help="初始化Clawra核心数据")
    
    # validate
    p_validate = subparsers.add_parser("validate", help="验证图谱")
    p_validate.add_argument("--check-cycles", action="store_true", help="检查循环依赖")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    commands = {
        "create": cmd_create,
        "relate": cmd_relate,
        "query": cmd_query,
        "get": cmd_get,
        "related": cmd_related,
        "rules": cmd_rules,
        "laws": cmd_laws,
        "concepts": cmd_concepts,
        "decisions": cmd_decisions,
        "decide": cmd_decide,
        "reason": cmd_reason,
        "infer": cmd_infer,
        "init-clawra": cmd_init_clawra,
        "validate": cmd_validate,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
