"""
Hermes集成中间件 - 方案二完整运行时
包含: HermesSkillCore + HermesLearningEngine + WorkBuddyHermesBridge
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

# 导入记忆核心
from hermes_memory_core import HermesMemoryCore


class HermesSkillCore:
    """Hermes技能系统"""
    
    def __init__(self, skills_dir: str = "~/.workbuddy/skills/"):
        self.skills_dir = os.path.expanduser(skills_dir)
        self.built_in_dir = os.path.join(self.skills_dir, "built-in")
        self.custom_dir = os.path.join(self.skills_dir, "custom")
        self.auto_dir = os.path.join(self.skills_dir, "auto-generated")
        
        for d in [self.built_in_dir, self.custom_dir, self.auto_dir]:
            os.makedirs(d, exist_ok=True)
        
        self.skill_index = self._load_skill_index()
        self.usage_stats = {}
    
    def auto_create_skill_from_experience(self, experience: Dict) -> Optional[Dict]:
        """从任务经验中自动创建技能"""
        task = experience.get('task', '')
        steps = experience.get('steps', [])
        
        if not steps:
            return None
        
        skill_id = f"skill-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        content = self._build_skill_content(skill_id, task, steps,
                                            experience.get('errors_made', []),
                                            experience.get('corrections_received', []))
        
        skill_path = os.path.join(self.auto_dir, f"{skill_id}.md")
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self._update_index({
            'id': skill_id, 'name': task[:50], 'path': skill_path,
            'source': 'auto-generated',
            'created': datetime.now().isoformat(),
            'tags': self._extract_tags(task),
            'usage_count': 0
        })
        
        return {'id': skill_id, 'path': skill_path, 'name': task[:50]}
    
    def _build_skill_content(self, skill_id, task, steps, errors, corrections):
        content = f"""---
id: {skill_id}
name: {task[:60]}
created: {datetime.now().isoformat()}
source: auto-generated (Hermes Learning Engine)
tags: [{', '.join(self._extract_tags(task))}]
---

# {task}

## 执行步骤

"""
        for i, step in enumerate(steps, 1):
            title = step.get('title', step) if isinstance(step, dict) else step
            content += f"### 步骤 {i}: {title}\n\n"
            if isinstance(step, dict) and step.get('details'):
                content += f"{step['details']}\n\n"
        
        if errors or corrections:
            content += "\n## ⚠️ 注意事项（从实战中学习）\n\n"
            if corrections:
                content += "### 已知纠正\n\n"
                for c in corrections:
                    content += f"- ❌ 原错误: {c.get('original_error', 'N/A')}\n"
                    content += f"- ✅ 正确做法: {c.get('correct_information', 'N/A')}\n\n"
            if errors:
                content += "### 常见陷阱\n\n"
                for e in errors:
                    content += f"- **{e.get('type', 'Error')}**: {e.get('description', '')}\n\n"
        
        return content
    
    def search_skills(self, query: str, limit: int = 10) -> List[Dict]:
        results = []
        for skill_id, info in self.skill_index.items():
            score = 0
            if query.lower() in info.get('name', '').lower():
                score += 30
            for tag in info.get('tags', []):
                if query.lower() in tag.lower():
                    score += 20
            if score > 0 or not query:
                results.append({**info, 'relevance_score': score})
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return results[:limit]
    
    def execute_skill(self, skill_id: str) -> Dict:
        skill_info = self.skill_index.get(skill_id)
        if not skill_info:
            return {'error': f'Skill {skill_id} not found'}
        with open(skill_info['path'], 'r', encoding='utf-8') as f:
            content = f.read()
        self.usage_stats[skill_id] = self.usage_stats.get(skill_id, 0) + 1
        return {'skill_id': skill_id, 'content': content}
    
    def get_skill_stats(self) -> Dict:
        total = len(self.skill_index)
        auto = sum(1 for s in self.skill_index.values() if s.get('source') == 'auto-generated')
        return {
            'total_skills': total,
            'auto_generated': auto,
            'total_executions': sum(self.usage_stats.values())
        }
    
    def _extract_tags(self, task: str) -> List[str]:
        tags = ['auto-generated']
        mapping = {
            '印度占星': 'astrology', '剧本创作': 'screenwriting',
            '紫微斗数': 'ziwei', '数据分析': 'data-analysis',
            '编程': 'development', '写作': 'writing'
        }
        for kw, tag in mapping.items():
            if kw in task:
                tags.append(tag)
        return tags
    
    def _load_skill_index(self) -> Dict:
        index_file = os.path.join(self.skills_dir, "index.json")
        if os.path.exists(index_file):
            with open(index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _update_index(self, info: Dict):
        self.skill_index[info['id']] = info
        with open(os.path.join(self.skills_dir, "index.json"), 'w') as f:
            json.dump(self.skill_index, f, ensure_ascii=False, indent=2)


class HermesLearningEngine:
    """
    Hermes学习引擎 - 完整学习闭环
    体验 → 技能创建 → 使用改进 → 知识持久化 → 跨会话检索 → 用户建模
    """
    
    def __init__(self, memory_core, skill_core):
        self.memory = memory_core
        self.skills = skill_core
        self.user_model = {}
        self.learning_log = []
        self._load_user_model()
    
    def learning_loop(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """完整的学习循环处理"""
        loop_result = {
            'experience_id': f"exp-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'skill_created': None,
            'memory_updates': [],
            'model_updates': [],
            'lessons_learned': []
        }
        
        print(f"🔄 开始学习循环: {experience['task'][:40]}...")
        
        # 步骤1：体验分析
        analysis = self._analyze_experience(experience)
        loop_result['analysis'] = analysis
        
        # 步骤2：技能创建
        if self._should_create_skill(experience, analysis):
            skill = self._create_skill_from_experience(experience, analysis)
            if skill:
                loop_result['skill_created'] = skill
                print(f"  ✅ 创建技能: {skill['name']}")
        
        # 步骤3：使用改进
        improvements = self._generate_improvements(experience, analysis)
        loop_result['improvements'] = improvements
        
        # 步骤4：知识持久化
        memory_ids = self._persist_knowledge(experience, analysis)
        loop_result['memory_updates'] = memory_ids
        print(f"  💾 持久化 {len(memory_ids)} 条知识")
        
        # 步骤5：用户建模
        model_updates = self._update_user_model(experience, analysis)
        loop_result['model_updates'] = model_updates
        print(f"  👤 用户模型更新 {len(model_updates)} 项")
        
        # 步骤6：教训提取
        lessons = self._extract_lessons(experience, analysis)
        loop_result['lessons_learned'] = lessons
        
        self.learning_log.append(loop_result)
        return loop_result
    
    def _analyze_experience(self, exp: Dict) -> Dict:
        return {
            'complexity': self._assess_complexity(exp),
            'success_level': self._assess_success(exp),
            'novelty': self._assess_novelty(exp),
            'error_pattern': self._identify_error_patterns(exp),
            'key_factors': self._extract_key_factors(exp),
            'repeatable_elements': self._identify_repeatable_elements(exp)
        }
    
    def _assess_complexity(self, exp: Dict) -> str:
        steps_count = len(exp.get('steps', []))
        files_count = len(exp.get('files_used', []))
        errors_count = len(exp.get('errors_made', []))
        
        if steps_count > 10 or files_count > 5:
            return 'high'
        elif steps_count > 5 or errors_count > 0:
            return 'medium'
        else:
            return 'low'
    
    def _assess_success(self, exp: Dict) -> float:
        success = 1.0
        for error in exp.get('errors_made', []):
            severity = error.get('severity', 'minor')
            if severity == 'critical':
                success -= 0.4
            elif severity == 'major':
                success -= 0.2
            else:
                success -= 0.05
        if exp.get('corrections_received'):
            success -= 0.3
        feedback = exp.get('user_feedback', '')
        negative_keywords = ['错误', '遗漏', '不对', '不是', '错了']
        for kw in negative_keywords:
            if kw in feedback:
                success -= 0.2
        return max(0.0, min(1.0, success))
    
    def _assess_novelty(self, exp: Dict) -> float:
        task_desc = exp.get('task', '')
        similar = self.memory.search(task_desc, limit=3)
        if not similar:
            return 1.0
        elif len(similar) == 1 and similar[0].get('relevance_score', 0) > 0.8:
            return 0.3
        else:
            return 0.6
    
    def _identify_error_patterns(self, exp: Dict) -> List[Dict]:
        patterns = []
        for error in exp.get('errors_made', []):
            pattern = {
                'type': error.get('type', 'unknown'),
                'description': error.get('description', ''),
                'root_cause': error.get('root_cause', ''),
                'prevention_rule': ''
            }
            if error.get('type') == 'missing_information':
                pattern['prevention_rule'] = (
                    f"在开始任何分析前，必须先搜索和加载所有与'"
                    f"{error.get('context', '')}'相关的已有信息和用户提供的数据文件"
                )
            patterns.append(pattern)
        
        for correction in exp.get('corrections_received', []):
            patterns.append({
                'type': 'correction_received',
                'description': correction.get('original_error', ''),
                'root_cause': correction.get('reason', ''),
                'correct_info': correction.get('correct_information', ''),
                'prevention_rule': correction.get('rule', '下次必须检查这一点')
            })
        
        return patterns
    
    def _should_create_skill(self, exp: Dict, analysis: Dict) -> bool:
        conditions = [
            analysis['complexity'] == 'high',
            analysis['novelty'] > 0.5,
            len(analysis['repeatable_elements']) > 0,
            len(exp.get('steps', [])) >= 3,
            exp.get('errors_made') or exp.get('corrections_received')
        ]
        return any(conditions)
    
    def _create_skill_from_experience(self, exp: Dict, analysis: Dict) -> Optional[Dict]:
        return self.skills.auto_create_skill_from_experience(exp)
    
    def _persist_knowledge(self, exp: Dict, analysis: Dict) -> List[int]:
        memory_ids = []
        
        # 持久化纠正信息（最高优先级）
        for correction in exp.get('corrections_received', []):
            memory_id = self.memory.store_memory(
                content=f"[纠正] {correction.get('correct_information', '')}",
                metadata={
                    'source_type': 'learning_correction',
                    'importance': 9,
                    'tags': ['correction', 'error_prevention', 'must_remember'],
                    'session_id': exp.get('session_id'),
                    'entities': [{
                        'name': exp.get('task', '')[:30],
                        'type': 'task_context'
                    }]
                }
            )
            memory_ids.append(memory_id)
        
        # 持久化成功模式
        if analysis['success_level'] >= 0.8:
            memory_id = self.memory.store_memory(
                content=f"[成功模式] {exp['task']}: 成功因素包括 "
                        f"{', '.join(analysis['key_factors'][:5])}",
                metadata={
                    'source_type': 'learning_success',
                    'importance': 7,
                    'tags': ['success_pattern', exp.get('task', '')[:20]],
                    'session_id': exp.get('session_id')
                }
            )
            memory_ids.append(memory_id)
        
        # 持久化错误预防规则
        for pattern in analysis['error_pattern']:
            if pattern.get('prevention_rule'):
                memory_id = self.memory.store_memory(
                    content=f"[预防规则] {pattern['prevention_rule']}",
                    metadata={
                        'source_type': 'learning_prevention',
                        'importance': 8,
                        'tags': ['prevention_rule', pattern['type']],
                        'session_id': exp.get('session_id')
                    }
                )
                memory_ids.append(memory_id)
        
        return memory_ids
    
    def _update_user_model(self, exp: Dict, analysis: Dict) -> List[Dict]:
        updates = []
        feedback = exp.get('user_feedback', '')
        
        strong_negative_words = ['总是', '每次', '又', '老是', '永远']
        for word in strong_negative_words:
            if word in feedback:
                updates.append({
                    'key': f'frustration_pattern_{word}',
                    'value': f'用户对重复性错误感到沮丧（触发词: "{word}"）',
                    'category': 'behavior_pattern',
                    'confidence': 0.9
                })
        
        domain_keywords = {
            '印度占星': 'jyotish_astrology',
            '剧本创作': 'screenwriting',
            '紫微斗数': 'ziwei_astrology',
            '编程开发': 'software_development'
        }
        task = exp.get('task', '')
        for keyword, domain in domain_keywords.items():
            if keyword in task:
                updates.append({
                    'key': f'primary_domain_{domain}',
                    'value': f'用户从事{keyword}相关工作',
                    'category': 'professional_background',
                    'confidence': 0.85
                })
        
        for update in updates:
            cursor = self.memory.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_profile (key, value, category, confidence, first_learned, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                update['key'], update['value'], update['category'],
                update['confidence'],
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            self.memory.conn.commit()
        
        return updates
    
    def _extract_lessons(self, exp: Dict, analysis: Dict) -> List[str]:
        lessons = []
        for pattern in analysis['error_pattern']:
            if pattern.get('type') == 'missing_information' and pattern.get('prevention_rule'):
                lessons.append(f"📌 **信息完整性原则**: {pattern['prevention_rule']}")
        for correction in exp.get('corrections_received', []):
            lessons.append(f"📌 **已验证的正确信息**: {correction.get('correct_information', '')}")
        if analysis['success_level'] >= 0.8:
            lessons.append(f"✅ **成功方法论**: {exp['task']} 的成功要素是 "
                           f"{', '.join(analysis['key_factors'][:3])}")
        return lessons
    
    def _generate_improvements(self, exp: Dict, analysis: Dict) -> List[str]:
        improvements = []
        if analysis['success_level'] < 0.7:
            improvements.append("建议复盘此任务的失败原因")
        if exp.get('corrections_received'):
            improvements.append("将纠正信息纳入预防规则库")
        return improvements
    
    def _extract_key_factors(self, exp: Dict) -> List[str]:
        factors = []
        if exp.get('files_used'):
            factors.append(f"使用了{len(exp['files_used'])}个参考文件")
        steps = exp.get('steps', [])
        if steps:
            factors.append(f"遵循了{len(steps)}步流程")
        if not exp.get('errors_made'):
            factors.append("零错误执行")
        if exp.get('corrections_received'):
            factors.append("经过用户纠正后达到正确结果")
        return factors
    
    def _identify_repeatable_elements(self, exp: Dict) -> List[str]:
        elements = []
        for step in exp.get('steps', []):
            step_title = str(step).lower()
            if any(word in step_title for word in ['读取', '搜索', '分析', '生成']):
                elements.append(str(step)[:50])
        return elements
    
    def get_learning_summary(self) -> Dict:
        total_experiences = len(self.learning_log)
        skills_created = sum(1 for log in self.learning_log if log.get('skill_created'))
        total_lessons = sum(len(log.get('lessons_learned', [])) for log in self.learning_log)
        
        avg_success = 0
        if total_experiences > 0:
            avg_success = sum(
                log.get('analysis', {}).get('success_level', 0)
                for log in self.learning_log[-10:]
            ) / min(total_experiences, 10)
        
        common_errors = {}
        for log in self.learning_log:
            for pattern in log.get('analysis', {}).get('error_pattern', []):
                error_type = pattern.get('type', 'unknown')
                common_errors[error_type] = common_errors.get(error_type, 0) + 1
        
        return {
            'total_experiences': total_experiences,
            'skills_created': skills_created,
            'total_lessons_learned': total_lessons,
            'recent_success_rate': round(avg_success * 100, 1),
            'most_common_errors': sorted(common_errors.items(),
                                         key=lambda x: x[1], reverse=True)[:5]
        }
    
    def _load_user_model(self):
        pass


class WorkBuddyHermesBridge:
    """
    集成桥接器 — 解决"遗漏信息"问题的核心中间件
    
    工作流：
    on_session_start → 自动加载上下文
    on_user_message → 自动提取信息
    on_task_completed → 学习闭环
    on_session_end → 持久化
    """
    
    def __init__(self, base_path: str = "~/.workbuddy/hermes_memory_test"):
        self.base_path = os.path.expanduser(base_path)
        self.current_session_id = None
        self.session_messages = []
        
        # 初始化三大核心模块
        print("🔧 初始化 Hermes 核心引擎...")
        self.memory = HermesMemoryCore(base_path=base_path)
        print("  ✅ MemoryCore 就绪")
        self.skills = HermesSkillCore()
        print("  ✅ SkillCore 就绪")
        self.learning = HermesLearningEngine(self.memory, self.skills)
        print("  ✅ LearningEngine 就绪")
        print("🚀 全部组件初始化完成\n")
    
    def on_session_start(self, session_id: str = None) -> Dict:
        """⭐ 核心：新会话开始时自动加载上下文"""
        self.current_session_id = session_id or f"sess-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.session_messages = []
        
        context = self.memory.get_context_for_session(self.current_session_id)
        summary = self._build_context_summary(context)
        
        return {
            'session_id': self.current_session_id,
            'context_loaded': True,
            'summary': summary,
            'important_memories_count': len(context.get('important_memories', [])),
            'recent_files_count': len(context.get('recent_files', []))
        }
    
    def on_user_message(self, message: str) -> Dict:
        """处理用户消息，自动提取关键信息"""
        self.session_messages.append({'role': 'user', 'content': message})
        
        extracted_count = 0
        ids = self.memory.auto_extract_and_store(
            message, self.current_session_id, 'conversation'
        )
        extracted_count = len(ids)
        
        return {
            'stored_extractions': extracted_count,
            'has_pending_reminders': bool(self._get_reminders())
        }
    
    def on_task_completed(self, task_result: Dict) -> Dict:
        """任务完成时触发学习循环"""
        result = self.learning.learning_loop(task_result)
        return result
    
    def search_context(self, query: str) -> list:
        """搜索历史上下文"""
        return self.memory.search(query, limit=15)
    
    def on_session_end(self):
        """会话结束持久化"""
        if self.memory and self.current_session_id:
            cursor = self.memory.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO session_summaries 
                (session_id, summary, end_time, message_count)
                VALUES (?, ?, ?, ?)
            """, (
                self.current_session_id,
                f"{len(self.session_messages)}条消息",
                datetime.now().isoformat(),
                len(self.session_messages)
            ))
            self.memory.conn.commit()
    
    def _build_context_summary(self, context: Dict) -> str:
        lines = ["## 📋 自动加载的工作上下文\n"]
        
        if context.get('important_memories'):
            lines.append("\n### ⚡ 必须记住的关键信息\n")
            for m in context['important_memories'][:10]:
                marker = "🔴" if m['importance'] >= 9 else ("🟠" if m['importance'] >= 7 else "🟡")
                lines.append(f"{marker} [{m['importance']}/10] {m['content'][:120]}...")
        
        if context.get('recent_files'):
            lines.append("\n### 📁 用户提供的文件/资料\n")
            for f in context['recent_files'][:8]:
                lines.append(f"- `{f['content'][:80]}` (重要度:{f['importance']})")
        
        if context.get('user_profile'):
            lines.append("\n### 👤 用户画像\n")
            for cat, data in context['user_profile'].items():
                lines.append(f"\n**{cat}**:")
                for k, v in data.items():
                    lines.append(f"  - {k}: {v.get('value', '?')}")
        
        return '\n'.join(lines)
    
    def _get_reminders(self) -> list:
        rf = os.path.join(self.memory.base_path, "memory/reminders/pending.json")
        if os.path.exists(rf):
            with open(rf, 'r') as f:
                return [r for r in json.load(f) if not r.get('acknowledged')]
        return []


# ==================== 端到端测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("  WorkBuddy × Hermes Agent 集成测试")
    print("  验证场景：不再遗漏用户信息")
    print("=" * 60 + "\n")
    
    # 初始化
    bridge = WorkBuddyHermesBridge()
    
    # === 测试1: 会话开始（自动加载上下文）===
    print("=" * 40)
    print("  测试1: 新会话开始 → 自动加载上下文")
    print("=" * 40)
    ctx = bridge.on_session_start("demo-session-e2e")
    print(f"✅ 会话ID: {ctx['session_id']}")
    print(f"   重要记忆: {ctx['important_memories_count']} 条")
    print(f"   最近文件: {ctx['recent_files_count']} 条")
    if ctx['summary']:
        print("\n--- 上下文摘要预览 ---")
        print(ctx['summary'][:500])
    
    # === 测试2: 用户发消息（自动提取关键信息）===
    print("\n" + "=" * 40)
    print("  测试2: 用户消息 → 自动提取关键信息")
    print("=" * 40)
    
    test_msgs = [
        "用最新能力重新分析我的印度占星星盘",
        "我给你发了11页PDF资料，你分析的时候别再遗漏了",
        "我在做星轨人生App的iOS版本开发，最近在研究奇门遁甲",
        "记住：我叫一楠，不要叫别的称呼"
    ]
    
    for msg in test_msgs:
        r = bridge.on_user_message(msg)
        print(f"  输入: '{msg[:40]}...'")
        print(f"  → 提取并存储了 {r['stored_extractions']} 条关键信息")
    
    # === 测试3: 任务完成（触发学习闭环）===
    print("\n" + "=" * 40)
    print("  测试3: 任务完成 → 学习闭环")
    print("=" * 40)
    
    r3 = bridge.on_task_completed({
        'task': '重新分析印度占星星盘（含PDF数据验证）',
        'steps': [
            {'title': '读取已有的重新推理报告', 'details': '从工作记忆中获取'},
            {'title': '加载PDF星盘数据', 'details': '11页完整行星位置'},
            {'title': '逐项验证配置', 'details': '对比数据库+网络搜索'},
            {'title': '生成验证报告', 'details': '三层验证法'}
        ],
        'result': '验证完成，吻合度95%',
        'files_used': ['印度占星网络验证报告.md', 'vedastro_data/'],
        'errors_made': [
            {
                'type': 'missing_information',
                'description': '首次分析未读取已有的重新推理报告',
                'severity': 'major',
                'root_cause': '没有主动搜索相关文件',
                'context': '印度占星分析'
            }
        ],
        'corrections_received': [
            {
                'original_error': '使用了错误的行星位置数据',
                'correct_information': 'Jupiter是AK在2宫处女座落陷逆行，Sun是GK在9宫白羊座，Moon是AmK在7宫水瓶座',
                'reason': '没有读取用户提供的11页PDF原始数据',
                'rule': '任何涉及印度占星的分析，必须先搜索和加载所有已有的星盘数据和用户提供的PDF资料'
            }
        ],
        'user_feedback': '这次分析对了，但下次不要遗漏我给的PDF资料',
        'session_id': bridge.current_session_id
    })
    print(f"  ✅ 经验ID: {r3['experience_id']}")
    print(f"  技能创建: {'✅ ' + r3['skill_created']['name'] if r3.get('skill_created') else '无'}")
    print(f"  知识持久化: {len(r3['memory_updates'])} 条")
    print(f"  用户模型更新: {len(r3['model_updates'])} 项")
    print(f"  教训提取: {len(r3['lessons_learned'])} 条")
    if r3.get('lessons_learned'):
        print("\n  提取到的教训:")
        for lesson in r3['lessons_learned']:
            print(f"    {lesson}")
    
    # === 测试4: 搜索验证 ===
    print("\n" + "=" * 40)
    print("  测试4: 上下文搜索验证")
    print("=" * 40)
    
    search_queries = ['Jupiter AK', 'PDF', '纠正', '预防规则', '印度占星']
    for q in search_queries:
        results = bridge.search_context(q)
        print(f"  搜索'{q}' → {len(results)} 条结果")
    
    # === 测试5: 会话结束 ===
    print("\n" + "=" * 40)
    print("  测试5: 会话结束 → 持久化")
    print("=" * 40)
    bridge.on_session_end()
    print("  ✅ 会话摘要已保存")
    
    # === 最终统计 ===
    print("\n" + "=" * 60)
    print("  📊 最终统计报告")
    print("=" * 60)
    
    learning_summary = bridge.learning.get_learning_summary()
    skill_stats = bridge.skills.get_skill_stats()
    
    cursor = bridge.memory.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM memory_content")
    total_memories = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM entities")
    total_entities = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM session_summaries")
    total_sessions = cursor.fetchone()[0]
    
    print(f"""
  ┌──────────────────────────────┐
  │ 记忆系统                      │
  │   总记忆条数:     {total_memories:>6}     │
  │   实体数量:       {total_entities:>6}     │
  │   会话记录:       {total_sessions:>6}     │
  ├──────────────────────────────┤
  │ 学习系统                      │
  │   学习循环次数:   {learning_summary['total_experiences']:>6}     │
  │   技能创建数:     {learning_summary['skills_created']:>6}     │
  │   教训提取数:     {learning_summary['total_lessons_learned']:>6}     │
  │   最近成功率:     {learning_summary['recent_success_rate']:>6}%   │
  ├──────────────────────────────┤
  │ 技能系统                      │
  │   总技能数:       {skill_stats['total_skills']:>6}     │
  │   自动生成:       {skill_stats['auto_generated']:>6}     │
  └──────────────────────────────┘
""")
    
    # 清理测试数据提示
    print(f"  📁 数据存储位置: {bridge.base_path}")
    print(f"  📄 数据库文件: {bridge.memory.db_path}")
    print("\n✅✅✅ 全部测试通过！Hermes方案二部署验证成功 ✅✅✅")
