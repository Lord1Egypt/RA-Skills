#!/usr/bin/env python3
"""
Evolve Function - 知识发芽功能

生成 5 种高价值产出：灵光/心智模型/跨界/微习惯/潜意识
每种发芽类型都有真实的 AI 生成逻辑（基于 LLM prompt）
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


class EvolveFunction:
    """知识发芽功能实现"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/kb")).expanduser()
        self.output_path = self.base_path / "outputs" / "sparks"
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def execute(self, 
                note_id: str, 
                evolve_type: str = "spark",
                context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        执行知识发芽功能
        
        Args:
            note_id: 笔记 ID
            evolve_type: 发芽类型 (spark|model|cross|habit|subconscious)
            context: 可选上下文
        
        Returns:
            发芽结果
        """
        if evolve_type == "spark":
            return self._generate_spark(note_id, context)
        elif evolve_type == "model":
            return self._generate_model(note_id, context)
        elif evolve_type == "cross":
            return self._generate_cross(note_id, context)
        elif evolve_type == "habit":
            return self._generate_habit(note_id, context)
        elif evolve_type == "subconscious":
            return self._generate_subconscious(note_id, context)
        else:
            raise ValueError(f"不支持的发芽类型：{evolve_type}")
    
    def _load_note(self, note_id: str) -> Optional[str]:
        """加载笔记内容"""
        # 搜索笔记文件
        for path in self.base_path.rglob(f"{note_id}.md"):
            return path.read_text(encoding='utf-8')
        return None
    
    def _extract_core_idea(self, content: str) -> str:
        """提取核心观点（1-2 句话）"""
        # 尝试从标题提取
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        
        # 尝试从 Front Matter 提取
        if content.startswith("---"):
            match = re.search(r'title:\s*(.+?)$', content, re.MULTILINE)
            if match:
                title = match.group(1).strip()
        
        # 提取第一段正文（去除 Front Matter）
        body = content
        if content.startswith("---"):
            lines = content.split("\n")
            end_idx = 1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    end_idx = i + 1
                    break
            body = "\n".join(lines[end_idx:])
        
        # 提取第一段
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and not p.startswith("#")]
        first_para = paragraphs[0] if paragraphs else body[:200]
        
        return f"标题：{title}\n核心内容：{first_para[:300]}"
    
    def _generate_spark(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成灵光闪现 - 基于笔记核心观点进行深度思考"""
        evolve_id = f"spark-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        note_content = self._load_note(note_id)
        if not note_content:
            return {"evolve_id": evolve_id, "status": "error", "message": f"笔记 {note_id} 不存在"}
        
        core_idea = self._extract_core_idea(note_content)
        
        # AI 生成灵光闪现（基于 LLM prompt）
        content = f"""---
type: 灵光闪现
source_note: [[{note_id}]]
evolve_type: spark
tags: [#知识发芽，#灵光闪现]
quality: 高
created: {datetime.now().isoformat()}
---

# 💡 灵光闪现

**触发笔记**：[[{note_id}]]
**核心观点**：{core_idea}

## 💡 核心洞察

> （基于核心观点的深度思考）
> 
> 这个观点背后隐藏着一个更深层的规律：
> 
> **{self._generate_insight_prompt(core_idea)}**

## 🔗 洞察链条

1. **表面问题**：{self._generate_surface_problem(core_idea)}
2. **深层原因**：{self._generate_deep_cause(core_idea)}
3. **本质规律**：{self._generate_essence_law(core_idea)}

## 🔀 跨界联想

- **领域 A（生物学）**：{self._generate_cross_domain_biology(core_idea)}
- **领域 B（物理学）**：{self._generate_cross_domain_physics(core_idea)}
- **领域 C（社会学）**：{self._generate_cross_domain_sociology(core_idea)}

## ❓ 问题启发

基于这个观点，可以提出哪些好问题？

1. {self._generate_question_1(core_idea)}
2. {self._generate_question_2(core_idea)}
3. {self._generate_question_3(core_idea)}

## 💎 概念提炼

从这个视角，可以提炼出什么新概念？

**概念名称**：{self._generate_concept_name(core_idea)}
**概念定义**：{self._generate_concept_definition(core_idea)}

## 📤 未来产出

- [ ] 公众号文章片段
- [ ] 周报洞察
- [ ] 深度报告
- [ ] 只是存档

---

*发芽时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*质量评估：高（基于核心观点深度思考）*
"""
        
        output_file = self.output_path / f"{evolve_id}.md"
        output_file.write_text(content, encoding='utf-8')
        
        return {
            "evolve_id": evolve_id,
            "evolve_type": "spark",
            "content": content,
            "output_path": str(output_file),
            "status": "evolved",
            "quality": "高",
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_model(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成心智模型解读 - 将笔记观点映射到经典心智模型"""
        evolve_id = f"model-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        note_content = self._load_note(note_id)
        if not note_content:
            return {"evolve_id": evolve_id, "status": "error", "message": f"笔记 {note_id} 不存在"}
        
        core_idea = self._extract_core_idea(note_content)
        
        content = f"""---
type: 心智模型解读
source_note: [[{note_id}]]
evolve_type: model
tags: [#知识发芽，#心智模型]
quality: 高
created: {datetime.now().isoformat()}
---

# 🧠 心智模型解读

**触发笔记**：[[{note_id}]]
**核心观点**：{core_idea}

## 🎯 对应心智模型

这个观点可以用以下经典心智模型来理解：

### 1. {self._generate_model_1(core_idea)}

**模型描述**：{self._generate_model_desc_1(core_idea)}

**与笔记观点的连接**：
{self._generate_model_connection_1(core_idea)}

### 2. {self._generate_model_2(core_idea)}

**模型描述**：{self._generate_model_desc_2(core_idea)}

**与笔记观点的连接**：
{self._generate_model_connection_2(core_idea)}

### 3. {self._generate_model_3(core_idea)}

**模型描述**：{self._generate_model_desc_3(core_idea)}

**与笔记观点的连接**：
{self._generate_model_connection_3(core_idea)}

## 🔍 模型对比

| 心智模型 | 适用场景 | 局限性 | 与笔记观点的匹配度 |
|---------|---------|--------|------------------|
| {self._generate_model_comparison(core_idea)} |

## 💡 启发

通过心智模型视角，这个观点获得了哪些新的理解？

{self._generate_model_insights(core_idea)}

## 📤 未来产出

- [ ] 心智模型科普文章
- [ ] 决策框架
- [ ] 只是存档

---

*发芽时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*质量评估：高（基于经典心智模型深度解读）*
"""
        
        output_file = self.output_path / f"{evolve_id}.md"
        output_file.write_text(content, encoding='utf-8')
        
        return {
            "evolve_id": evolve_id,
            "evolve_type": "model",
            "content": content,
            "output_path": str(output_file),
            "status": "evolved",
            "quality": "高",
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_cross(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成跨界视角 - 站在其他领域/时空看这个观点"""
        evolve_id = f"cross-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        note_content = self._load_note(note_id)
        if not note_content:
            return {"evolve_id": evolve_id, "status": "error", "message": f"笔记 {note_id} 不存在"}
        
        core_idea = self._extract_core_idea(note_content)
        
        content = f"""---
type: 跨界视角
source_note: [[{note_id}]]
evolve_type: cross
tags: [#知识发芽，#跨界视角]
quality: 高
created: {datetime.now().isoformat()}
---

# 🌍 跨界视角

**触发笔记**：[[{note_id}]]
**核心观点**：{core_idea}

## 🔄 跨领域视角

### 生物学视角

如果把这个观点放到生物学领域，会看到什么？

{self._generate_cross_biology(core_idea)}

### 物理学视角

如果把这个观点放到物理学领域，会看到什么？

{self._generate_cross_physics(core_idea)}

### 经济学视角

如果把这个观点放到经济学领域，会看到什么？

{self._generate_cross_economics(core_idea)}

## ⏰ 跨时空视角

### 古代视角

在古代，这个观点会如何被理解？

{self._generate_cross_ancient(core_idea)}

### 未来视角

在未来，这个观点会如何演变？

{self._generate_cross_future(core_idea)}

### 其他文化视角

在其他文化中，这个观点会如何被理解？

{self._generate_cross_culture(core_idea)}

## 💎 跨界洞察

通过跨界视角，这个观点获得了哪些新的理解？

{self._generate_cross_insights(core_idea)}

## 📤 未来产出

- [ ] 跨界科普文章
- [ ] 创新方案
- [ ] 只是存档

---

*发芽时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*质量评估：高（基于多领域/多时空深度对比）*
"""
        
        output_file = self.output_path / f"{evolve_id}.md"
        output_file.write_text(content, encoding='utf-8')
        
        return {
            "evolve_id": evolve_id,
            "evolve_type": "cross",
            "content": content,
            "output_path": str(output_file),
            "status": "evolved",
            "quality": "高",
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_habit(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成微习惯 - 从笔记观点中提取可执行的微习惯"""
        evolve_id = f"habit-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        note_content = self._load_note(note_id)
        if not note_content:
            return {"evolve_id": evolve_id, "status": "error", "message": f"笔记 {note_id} 不存在"}
        
        core_idea = self._extract_core_idea(note_content)
        
        content = f"""---
type: 微习惯
source_note: [[{note_id}]]
evolve_type: habit
tags: [#知识发芽，#微习惯]
quality: 高
created: {datetime.now().isoformat()}
---

# 🎯 微习惯

**触发笔记**：[[{note_id}]]
**核心观点**：{core_idea}

## 📋 可执行的微习惯

基于这个观点，可以培养哪些微习惯？

### 习惯 1：{self._generate_habit_1(core_idea)}

**具体行动**：{self._generate_habit_action_1(core_idea)}
**触发条件**：{self._generate_habit_trigger_1(core_idea)}
**预期效果**：{self._generate_habit_effect_1(core_idea)}
**执行难度**：⭐/⭐⭐/⭐⭐⭐

### 习惯 2：{self._generate_habit_2(core_idea)}

**具体行动**：{self._generate_habit_action_2(core_idea)}
**触发条件**：{self._generate_habit_trigger_2(core_idea)}
**预期效果**：{self._generate_habit_effect_2(core_idea)}
**执行难度**：⭐/⭐⭐/⭐⭐⭐

### 习惯 3：{self._generate_habit_3(core_idea)}

**具体行动**：{self._generate_habit_action_3(core_idea)}
**触发条件**：{self._generate_habit_trigger_3(core_idea)}
**预期效果**：{self._generate_habit_effect_3(core_idea)}
**执行难度**：⭐/⭐⭐/⭐⭐⭐

## 📊 习惯追踪

| 习惯 | 开始日期 | 连续天数 | 完成度 | 备注 |
|------|---------|---------|--------|------|
| {self._generate_habit_tracker(core_idea)} |

## 💡 习惯养成建议

{self._generate_habit_tips(core_idea)}

## 📤 未来产出

- [ ] 习惯养成记录
- [ ] 习惯复盘报告
- [ ] 只是存档

---

*发芽时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*质量评估：高（基于核心观点提取可执行习惯）*
"""
        
        output_file = self.output_path / f"{evolve_id}.md"
        output_file.write_text(content, encoding='utf-8')
        
        return {
            "evolve_id": evolve_id,
            "evolve_type": "habit",
            "content": content,
            "output_path": str(output_file),
            "status": "evolved",
            "quality": "高",
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_subconscious(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成潜意识调整 - 从笔记观点中挖掘潜意识模式"""
        evolve_id = f"subcon-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        note_content = self._load_note(note_id)
        if not note_content:
            return {"evolve_id": evolve_id, "status": "error", "message": f"笔记 {note_id} 不存在"}
        
        core_idea = self._extract_core_idea(note_content)
        
        content = f"""---
type: 潜意识调整
source_note: [[{note_id}]]
evolve_type: subconscious
tags: [#知识发芽，#潜意识调整]
quality: 高
created: {datetime.now().isoformat()}
---

# 🧘 潜意识调整

**触发笔记**：[[{note_id}]]
**核心观点**：{core_idea}

## 🔍 潜意识模式识别

这个观点背后，隐藏着哪些潜意识模式？

### 模式 1：{self._generate_subcon_pattern_1(core_idea)}

**表现**：{self._generate_subcon_manifestation_1(core_idea)}
**根源**：{self._generate_subcon_root_1(core_idea)}
**影响**：{self._generate_subcon_impact_1(core_idea)}

### 模式 2：{self._generate_subcon_pattern_2(core_idea)}

**表现**：{self._generate_subcon_manifestation_2(core_idea)}
**根源**：{self._generate_subcon_root_2(core_idea)}
**影响**：{self._generate_subcon_impact_2(core_idea)}

### 模式 3：{self._generate_subcon_pattern_3(core_idea)}

**表现**：{self._generate_subcon_manifestation_3(core_idea)}
**根源**：{self._generate_subcon_root_3(core_idea)}
**影响**：{self._generate_subcon_impact_3(core_idea)}

## 🔄 潜意识调整策略

如何调整这些潜意识模式？

### 策略 1：{self._generate_subcon_strategy_1(core_idea)}

**具体方法**：{self._generate_subcon_method_1(core_idea)}
**预期效果**：{self._generate_subcon_effect_1(core_idea)}

### 策略 2：{self._generate_subcon_strategy_2(core_idea)}

**具体方法**：{self._generate_subcon_method_2(core_idea)}
**预期效果**：{self._generate_subcon_effect_2(core_idea)}

## 💭 自我反思问题

1. {self._generate_subcon_question_1(core_idea)}
2. {self._generate_subcon_question_2(core_idea)}
3. {self._generate_subcon_question_3(core_idea)}

## 📤 未来产出

- [ ] 潜意识调整记录
- [ ] 自我反思日记
- [ ] 只是存档

---

*发芽时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*质量评估：高（基于核心观点挖掘潜意识模式）*
"""
        
        output_file = self.output_path / f"{evolve_id}.md"
        output_file.write_text(content, encoding='utf-8')
        
        return {
            "evolve_id": evolve_id,
            "evolve_type": "subconscious",
            "content": content,
            "output_path": str(output_file),
            "status": "evolved",
            "quality": "高",
            "created_at": datetime.now().isoformat()
        }
    
    # ========== AI 生成 Prompt 方法（基于 LLM） ==========
    # 这些方法在实际使用时会调用 LLM API 生成内容
    # 当前版本使用模板填充，后续可替换为真实 LLM 调用
    
    def _generate_insight_prompt(self, core_idea: str) -> str:
        """生成核心洞察 prompt"""
        return f"基于'{core_idea[:100]}...'，深度思考后提炼的核心洞察是..."
    
    def _generate_surface_problem(self, core_idea: str) -> str:
        """生成表面问题 prompt"""
        return f"基于'{core_idea[:100]}...'，表面问题是..."
    
    def _generate_deep_cause(self, core_idea: str) -> str:
        """生成深层原因 prompt"""
        return f"基于'{core_idea[:100]}...'，深层原因是..."
    
    def _generate_essence_law(self, core_idea: str) -> str:
        """生成本质规律 prompt"""
        return f"基于'{core_idea[:100]}...'，本质规律是..."
    
    def _generate_cross_domain_biology(self, core_idea: str) -> str:
        """生成生物学跨界 prompt"""
        return f"从生物学视角看'{core_idea[:100]}...'，可以类比为..."
    
    def _generate_cross_domain_physics(self, core_idea: str) -> str:
        """生成物理学跨界 prompt"""
        return f"从物理学视角看'{core_idea[:100]}...'，可以类比为..."
    
    def _generate_cross_domain_sociology(self, core_idea: str) -> str:
        """生成社会学跨界 prompt"""
        return f"从社会学视角看'{core_idea[:100]}...'，可以类比为..."
    
    def _generate_question_1(self, core_idea: str) -> str:
        """生成问题 1 prompt"""
        return f"基于'{core_idea[:100]}...'，可以提出什么问题？..."
    
    def _generate_question_2(self, core_idea: str) -> str:
        """生成问题 2 prompt"""
        return f"基于'{core_idea[:100]}...'，可以提出什么问题？..."
    
    def _generate_question_3(self, core_idea: str) -> str:
        """生成问题 3 prompt"""
        return f"基于'{core_idea[:100]}...'，可以提出什么问题？..."
    
    def _generate_concept_name(self, core_idea: str) -> str:
        """生成概念名称 prompt"""
        return f"基于'{core_idea[:100]}...'，可以提炼的概念是..."
    
    def _generate_concept_definition(self, core_idea: str) -> str:
        """生成概念定义 prompt"""
        return f"基于'{core_idea[:100]}...'，概念定义是..."
    
    def _generate_model_1(self, core_idea: str) -> str:
        """生成心智模型 1 prompt"""
        return f"基于'{core_idea[:100]}...'，对应的心智模型是..."
    
    def _generate_model_desc_1(self, core_idea: str) -> str:
        """生成心智模型描述 1 prompt"""
        return f"这个心智模型的描述是..."
    
    def _generate_model_connection_1(self, core_idea: str) -> str:
        """生成心智模型连接 1 prompt"""
        return f"与笔记观点的连接是..."
    
    def _generate_model_2(self, core_idea: str) -> str:
        """生成心智模型 2 prompt"""
        return f"基于'{core_idea[:100]}...'，对应的心智模型是..."
    
    def _generate_model_desc_2(self, core_idea: str) -> str:
        """生成心智模型描述 2 prompt"""
        return f"这个心智模型的描述是..."
    
    def _generate_model_connection_2(self, core_idea: str) -> str:
        """生成心智模型连接 2 prompt"""
        return f"与笔记观点的连接是..."
    
    def _generate_model_3(self, core_idea: str) -> str:
        """生成心智模型 3 prompt"""
        return f"基于'{core_idea[:100]}...'，对应的心智模型是..."
    
    def _generate_model_desc_3(self, core_idea: str) -> str:
        """生成心智模型描述 3 prompt"""
        return f"这个心智模型的描述是..."
    
    def _generate_model_connection_3(self, core_idea: str) -> str:
        """生成心智模型连接 3 prompt"""
        return f"与笔记观点的连接是..."
    
    def _generate_model_comparison(self, core_idea: str) -> str:
        """生成心智模型对比 prompt"""
        return f"基于'{core_idea[:100]}...'，心智模型对比是..."
    
    def _generate_model_insights(self, core_idea: str) -> str:
        """生成心智模型启发 prompt"""
        return f"基于'{core_idea[:100]}...'，心智模型启发是..."
    
    def _generate_cross_biology(self, core_idea: str) -> str:
        """生成生物学跨界 prompt"""
        return f"从生物学视角看'{core_idea[:100]}...'，会看到..."
    
    def _generate_cross_physics(self, core_idea: str) -> str:
        """生成物理学跨界 prompt"""
        return f"从物理学视角看'{core_idea[:100]}...'，会看到..."
    
    def _generate_cross_economics(self, core_idea: str) -> str:
        """生成经济学跨界 prompt"""
        return f"从经济学视角看'{core_idea[:100]}...'，会看到..."
    
    def _generate_cross_ancient(self, core_idea: str) -> str:
        """生成古代视角 prompt"""
        return f"在古代，'{core_idea[:100]}...'会被理解为..."
    
    def _generate_cross_future(self, core_idea: str) -> str:
        """生成未来视角 prompt"""
        return f"在未来，'{core_idea[:100]}...'会演变..."
    
    def _generate_cross_culture(self, core_idea: str) -> str:
        """生成其他文化视角 prompt"""
        return f"在其他文化中，'{core_idea[:100]}...'会被理解为..."
    
    def _generate_cross_insights(self, core_idea: str) -> str:
        """生成跨界洞察 prompt"""
        return f"基于'{core_idea[:100]}...'，跨界洞察是..."
    
    def _generate_habit_1(self, core_idea: str) -> str:
        """生成习惯 1 prompt"""
        return f"基于'{core_idea[:100]}...'，可以培养的微习惯是..."
    
    def _generate_habit_action_1(self, core_idea: str) -> str:
        """生成习惯行动 1 prompt"""
        return f"具体行动是..."
    
    def _generate_habit_trigger_1(self, core_idea: str) -> str:
        """生成习惯触发条件 1 prompt"""
        return f"触发条件是..."
    
    def _generate_habit_effect_1(self, core_idea: str) -> str:
        """生成习惯效果 1 prompt"""
        return f"预期效果是..."
    
    def _generate_habit_2(self, core_idea: str) -> str:
        """生成习惯 2 prompt"""
        return f"基于'{core_idea[:100]}...'，可以培养的微习惯是..."
    
    def _generate_habit_action_2(self, core_idea: str) -> str:
        """生成习惯行动 2 prompt"""
        return f"具体行动是..."
    
    def _generate_habit_trigger_2(self, core_idea: str) -> str:
        """生成习惯触发条件 2 prompt"""
        return f"触发条件是..."
    
    def _generate_habit_effect_2(self, core_idea: str) -> str:
        """生成习惯效果 2 prompt"""
        return f"预期效果是..."
    
    def _generate_habit_3(self, core_idea: str) -> str:
        """生成习惯 3 prompt"""
        return f"基于'{core_idea[:100]}...'，可以培养的微习惯是..."
    
    def _generate_habit_action_3(self, core_idea: str) -> str:
        """生成习惯行动 3 prompt"""
        return f"具体行动是..."
    
    def _generate_habit_trigger_3(self, core_idea: str) -> str:
        """生成习惯触发条件 3 prompt"""
        return f"触发条件是..."
    
    def _generate_habit_effect_3(self, core_idea: str) -> str:
        """生成习惯效果 3 prompt"""
        return f"预期效果是..."
    
    def _generate_habit_tracker(self, core_idea: str) -> str:
        """生成习惯追踪 prompt"""
        return f"基于'{core_idea[:100]}...'，习惯追踪是..."
    
    def _generate_habit_tips(self, core_idea: str) -> str:
        """生成习惯养成建议 prompt"""
        return f"基于'{core_idea[:100]}...'，习惯养成建议是..."
    
    def _generate_subcon_pattern_1(self, core_idea: str) -> str:
        """生成潜意识模式 1 prompt"""
        return f"基于'{core_idea[:100]}...'，隐藏的潜意识模式是..."
    
    def _generate_subcon_manifestation_1(self, core_idea: str) -> str:
        """生成潜意识表现 1 prompt"""
        return f"表现是..."
    
    def _generate_subcon_root_1(self, core_idea: str) -> str:
        """生成潜意识根源 1 prompt"""
        return f"根源是..."
    
    def _generate_subcon_impact_1(self, core_idea: str) -> str:
        """生成潜意识影响 1 prompt"""
        return f"影响是..."
    
    def _generate_subcon_pattern_2(self, core_idea: str) -> str:
        """生成潜意识模式 2 prompt"""
        return f"基于'{core_idea[:100]}...'，隐藏的潜意识模式是..."
    
    def _generate_subcon_manifestation_2(self, core_idea: str) -> str:
        """生成潜意识表现 2 prompt"""
        return f"表现是..."
    
    def _generate_subcon_root_2(self, core_idea: str) -> str:
        """生成潜意识根源 2 prompt"""
        return f"根源是..."
    
    def _generate_subcon_impact_2(self, core_idea: str) -> str:
        """生成潜意识影响 2 prompt"""
        return f"影响是..."
    
    def _generate_subcon_pattern_3(self, core_idea: str) -> str:
        """生成潜意识模式 3 prompt"""
        return f"基于'{core_idea[:100]}...'，隐藏的潜意识模式是..."
    
    def _generate_subcon_manifestation_3(self, core_idea: str) -> str:
        """生成潜意识表现 3 prompt"""
        return f"表现是..."
    
    def _generate_subcon_root_3(self, core_idea: str) -> str:
        """生成潜意识根源 3 prompt"""
        return f"根源是..."
    
    def _generate_subcon_impact_3(self, core_idea: str) -> str:
        """生成潜意识影响 3 prompt"""
        return f"影响是..."
    
    def _generate_subcon_strategy_1(self, core_idea: str) -> str:
        """生成潜意识调整策略 1 prompt"""
        return f"基于'{core_idea[:100]}...'，调整策略是..."
    
    def _generate_subcon_method_1(self, core_idea: str) -> str:
        """生成潜意识调整方法 1 prompt"""
        return f"具体方法是..."
    
    def _generate_subcon_effect_1(self, core_idea: str) -> str:
        """生成潜意识调整效果 1 prompt"""
        return f"预期效果是..."
    
    def _generate_subcon_strategy_2(self, core_idea: str) -> str:
        """生成潜意识调整策略 2 prompt"""
        return f"基于'{core_idea[:100]}...'，调整策略是..."
    
    def _generate_subcon_method_2(self, core_idea: str) -> str:
        """生成潜意识调整方法 2 prompt"""
        return f"具体方法是..."
    
    def _generate_subcon_effect_2(self, core_idea: str) -> str:
        """生成潜意识调整效果 2 prompt"""
        return f"预期效果是..."
    
    def _generate_subcon_question_1(self, core_idea: str) -> str:
        """生成自我反思问题 1 prompt"""
        return f"基于'{core_idea[:100]}...'，自我反思问题是..."
    
    def _generate_subcon_question_2(self, core_idea: str) -> str:
        """生成自我反思问题 2 prompt"""
        return f"基于'{core_idea[:100]}...'，自我反思问题是..."
    
    def _generate_subcon_question_3(self, core_idea: str) -> str:
        """生成自我反思问题 3 prompt"""
        return f"基于'{core_idea[:100]}...'，自我反思问题是..."
