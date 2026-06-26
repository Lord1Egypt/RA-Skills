# -*- coding: utf-8 -*-
"""
Script Generator
负责播客对话脚本的生成（流式完整生成 + 分段生成 fallback）
"""
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel


class SegmentScript(BaseModel):
    """Script Generator输出（分段模式）"""
    schema_version: str = "1.0"
    session_id: str
    segment_id: str
    lines: List[dict]
    word_count: int
    estimated_duration_sec: int
    segment_summary: str
    key_moments: List[str]


class FullScript(BaseModel):
    """Script Generator输出（流式完整模式）"""
    schema_version: str = "1.0"
    session_id: str
    lines: List[dict]
    word_count: int
    estimated_duration_sec: int
    script_summary: str
    key_moments: List[str]
    segments: Optional[List[dict]] = None  # 可选的分段信息


class ScriptGenerator:
    """播客脚本生成器"""

    def __init__(self, client=None, memory_skill=None, script_prompt: Optional[str] = None):
        self.client = client
        self.memory_skill = memory_skill
        if script_prompt is not None:
            self.script_prompt = script_prompt
        else:
            self._load_prompt()

    def _load_prompt(self):
        """加载 script-generator prompt"""
        prompt_dir = Path(__file__).parent.parent / "agents"
        with open(prompt_dir / "script-generator.md", "r", encoding="utf-8") as f:
            self.script_prompt = f.read()

    def _ensure_client(self):
        """延迟初始化 LLM client"""
        if self.client is None:
            from .config_loader import ConfigLoader
            from .volcano_client_requests import create_ark_client_requests
            config = ConfigLoader().load()
            self.client = create_ark_client_requests(
                api_key=config.get("doubao_api_key"),
                model=config.get("doubao_model")
            )

    def generate(
        self,
        research_pkg: dict,
        persona: dict,
        effective_style: str,
        verbose: bool = False,
        use_streaming: bool = True,
        target_length: Optional[int] = None
    ) -> List[Dict]:
        """
        生成脚本

        Args:
            use_streaming: 是否使用流式生成（默认True，解决超时问题）
            target_length: 用户显式指定的目标字数
        """
        if verbose:
            print("\n[Step 2] Script Generation...")
            if use_streaming:
                print("  [Mode] Streaming (流式生成)")
            else:
                print("  [Mode] Segmented (分段生成)")

        # segments 可能在 outline/outline_result 内部，需要兼容处理
        segments = research_pkg.get("segments", [])
        if not segments and "outline_result" in research_pkg:
            segments = research_pkg["outline_result"].get("segments", [])
        if not segments and "outline" in research_pkg:
            segments = research_pkg["outline"].get("segments", [])

        if not segments:
            if verbose:
                print("  ✗ 无可用segments")
            return []

        # 解析目标字数：用户指定 > 大纲各段之和 > 默认2500
        if target_length is not None and target_length > 0:
            target_words = target_length
        else:
            target_words = sum(seg.get("estimated_length", 500) for seg in segments)
            if target_words <= 0:
                target_words = 2500
            # safety floor: 与 schema 下限对齐，避免 prompt 和校验冲突
            if target_words < 300:
                target_words = 300

        target_lines = max(20, target_words // 45)

        if verbose:
            print(f"  目标总字数: {target_words} 字 / 约 {target_lines} 句")

        if use_streaming:
            return self.generate_streaming(
                research_pkg, persona, segments, effective_style, verbose, target_words, target_lines
            )
        else:
            return self.generate_segmented(
                research_pkg, persona, segments, effective_style, verbose, target_words
            )

    def generate_streaming(
        self,
        research_pkg: dict,
        persona: dict,
        segments: List[dict],
        effective_style: str,
        verbose: bool,
        target_words: int,
        target_lines: int
    ) -> List[Dict]:
        """流式生成完整脚本"""
        self._ensure_client()

        # 构建包含所有segments的输入
        all_materials = self._get_all_materials(research_pkg)

        # 根据所有段主题召回相关记忆
        all_focuses = [seg.get("content_focus", "") for seg in segments if seg.get("content_focus")]
        retrieved_memories = []
        seen = set()
        for focus in all_focuses:
            for mem in self.memory_skill.retrieve(focus, top_k=2):
                if mem not in seen:
                    seen.add(mem)
                    retrieved_memories.append(mem)

        if verbose and retrieved_memories:
            print(f"  召回相关记忆: {len(retrieved_memories)} 条（来自 {len(all_focuses)} 个主题）")

        # 构建增强的Persona注入（包含记忆）
        persona_injection = self._build_persona_injection(persona, retrieved_memories)

        tw_min = int(target_words * 0.85)
        tw_max = int(target_words * 1.15)
        tl_min = int(target_lines * 0.85)
        tl_max = int(target_lines * 1.15)

        # 流式生成使用完整脚本prompt
        # 注意：script_prompt 中含有 {{}} 模板语法，不能与 f-string 混用
        streaming_prompt = self.script_prompt + "\n\n## Persona注入（当前用户设定）\n" + persona_injection + f"""

## 完整脚本生成模式（流式输出）

本次任务要求生成完整播客脚本，一次性输出所有对话内容。

### 输出格式要求
必须输出符合以下JSON Schema的完整对象：
```json
{{
  "schema_version": "1.0",
  "session_id": "任意字符串",
  "lines": [
    {{"speaker": "A", "text": "第一句对话内容"}},
    {{"speaker": "B", "text": "第二句对话内容"}},
    ...（继续生成所有对话，至少{tl_min}-{tl_max}句）
  ],
  "word_count": {target_words},
  "estimated_duration_sec": {max(120, target_words // 3 // 60 * 60)},
  "script_summary": "整体脚本的核心进展概述",
  "key_moments": ["高光时刻1", "高光时刻2", "高光时刻3", "高光时刻4", "高光时刻5"]
}}
```

### 重要提示
1. 直接输出JSON，不要包裹在markdown代码块中
2. 确保JSON格式完整，所有括号正确闭合
3. **lines数组必须包含至少{tl_min}-{tl_max}句对话**，覆盖所有segment的内容
4. **总字数必须达到{tw_min}-{tw_max}字**，确保内容深度和完整性
5. 保持对话的自然流畅和逻辑连贯
6. 每个segment的内容都要充分展开，不要简略
7. 平均分配内容给各segment，不要前松后紧或前紧后松
"""

        input_data = {
            "task": "生成完整播客脚本（流式模式）",
            "segments_outline": [
                {
                    "segment_id": seg.get("segment_id", f"seg_{i+1:02d}"),
                    "narrative_function": seg.get("narrative_function", "setup"),
                    "dramatic_goal": seg.get("dramatic_goal", ""),
                    "content_focus": seg.get("content_focus", ""),
                    "estimated_length": seg.get("estimated_length", 600),
                    "outline": seg.get("outline")   # 新增
                }
                for i, seg in enumerate(segments)
            ],
            "persona_config": self._build_persona_config_for_input(persona),
            "materials": all_materials,
            "narrative_context": self._get_narrative_context(research_pkg),
            "style_config": self._get_style_config(effective_style),
            "requirements": {
                "total_segments": len(segments),
                "total_lines_target": f"至少{tl_min}-{tl_max}句对话",
                "total_words_target": f"{tw_min}-{tw_max}字",
                "output_format": "JSON格式完整脚本，直接输出可解析的JSON对象",
                "content_depth": "每个segment都要充分展开，详细探讨，不要简略"
            }
        }

        try:
            dynamic_max_tokens = min(20000, max(4096, target_words * 2 + 3000))
            if verbose:
                estimated_min = max(1, target_words // 250)
                print(f"  开始流式生成（预计{estimated_min}-{estimated_min+2}分钟）...")

            result, tokens = self.client.chat_completion_stream(
                system_prompt=streaming_prompt,
                user_message=json.dumps(input_data, ensure_ascii=False),
                output_schema=FullScript,
                temperature=0.8,
                max_tokens=dynamic_max_tokens,
                timeout=300,
                verbose=verbose
            )

            # 将完整脚本转换为分段格式（兼容现有输出）
            lines = result.lines
            total_lines = len(lines)

            # Speaker 校验与兜底：按设计决定初始说话人
            first_initiator = segments[0].get("persona_dynamics", {}).get("who_initiates", "A") if segments else "A"
            last_valid_speaker = first_initiator if first_initiator in ("A", "B") else "A"
            for line in lines:
                speaker = line.get("speaker", "")
                if speaker not in ("A", "B"):
                    line["speaker"] = last_valid_speaker
                else:
                    last_valid_speaker = speaker

            # 按 estimated_length 比例分配行数
            total_estimated = sum(seg.get("estimated_length", 1) for seg in segments)
            proportions = [seg.get("estimated_length", 1) / total_estimated for seg in segments]

            full_script = []
            current_idx = 0
            for i, seg in enumerate(segments):
                if i == len(segments) - 1:
                    seg_lines_count = total_lines - current_idx
                else:
                    seg_lines_count = int(total_lines * proportions[i])
                    seg_lines_count = max(1, seg_lines_count)

                start_idx = current_idx
                end_idx = start_idx + seg_lines_count
                current_idx = end_idx

                seg_lines = lines[start_idx:end_idx]
                seg_word_count = sum(len(line.get("text", "")) for line in seg_lines)

                full_script.append({
                    "segment_id": seg.get("segment_id", f"seg_{i+1:02d}"),
                    "lines": seg_lines,
                    "summary": f"本段聚焦：{seg.get('content_focus', '')}",
                    "key_moments": result.key_moments[i*2:(i+1)*2] if result.key_moments else [],
                    "word_count": seg_word_count
                })

            if verbose:
                print(f"  ✓ 完成，共 {total_lines} 句 / {result.word_count} 字")

            return full_script

        except Exception as e:
            if verbose:
                print(f"  ✗ 流式生成失败: {e}")
                print(f"  → 回退到分段生成...")
            return self.generate_segmented(
                research_pkg, persona, segments, effective_style, verbose, target_words
            )

    def generate_segmented(
        self,
        research_pkg: dict,
        persona: dict,
        segments: List[dict],
        effective_style: str,
        verbose: bool,
        target_words: int = 2500
    ) -> List[Dict]:
        """分段生成脚本（fallback模式）"""
        self._ensure_client()

        full_script = []
        previous_summary = None
        num_segments = len(segments)

        for i, seg_design in enumerate(segments, 1):
            if verbose:
                print(f"\n  [{i}/{num_segments}] {seg_design.get('segment_id', '?')}...", end=" ")

            # 按本段主题召回记忆
            seg_focus = seg_design.get("content_focus", "")
            seg_memories = self.memory_skill.retrieve(seg_focus, top_k=2)
            persona_injection = self._build_persona_injection(persona, seg_memories)

            seg_target = seg_design.get("estimated_length", target_words // num_segments if num_segments > 0 else 500)
            seg_target_words_min = int(seg_target * 0.8)
            seg_target_words_max = int(seg_target * 1.2)

            input_data = {
                "segment_design": seg_design,
                "persona_snapshot": {
                    "host_a": {
                        "base_profile": persona.get("host_a", {}),
                        "recent_quirks": [],
                        "current_stance": ""
                    },
                    "host_b": {
                        "base_profile": persona.get("host_b", {}),
                        "recent_quirks": [],
                        "current_stance": ""
                    },
                    "relationship_state": "老搭档"
                },
                "shared_history": [],
                "materials": self._get_segment_materials(seg_design, research_pkg),
                "previous_segment_summary": previous_summary,
                "narrative_context": self._get_narrative_context(research_pkg),
                "style_config": self._get_style_config(effective_style),
                "requirements": {
                    "target_words": f"{seg_target_words_min}-{seg_target_words_max}字",
                    "allocation": "本段内容需围绕 segment_design 展开，不抢其他段的戏"
                }
            }

            try:
                seg_max_tokens = min(16000, max(4096, seg_target * 2 + 2000))
                seg_prompt = self.script_prompt + "\n\n## Persona注入（当前用户设定）\n" + persona_injection
                result, tokens = self.client.chat_completion(
                    system_prompt=seg_prompt,
                    user_message=json.dumps(input_data, ensure_ascii=False),
                    output_schema=SegmentScript,
                    temperature=0.8,
                    max_tokens=seg_max_tokens
                )

                full_script.append({
                    "segment_id": seg_design.get("segment_id", f"seg_{i:02d}"),
                    "lines": result.lines,
                    "summary": result.segment_summary,
                    "key_moments": result.key_moments,
                    "word_count": result.word_count
                })

                previous_summary = result.segment_summary

                if verbose:
                    print(f"✓ {len(result.lines)}句/{result.word_count}字")

            except Exception as e:
                if verbose:
                    print(f"✗ 失败: {e}")
                raise

        return full_script

    def _build_persona_injection(self, persona: dict, retrieved_memories: List[str]) -> str:
        """
        构建Persona注入文本 - 高优先级角色设定
        """
        def _build_host_section(host_key: str, host: dict) -> List[str]:
            identity = host.get("identity", {})
            expression = host.get("expression", {})

            lines = []
            lines.append(f"### {host_key}")
            name = identity.get('name') or ('主持人A' if 'A' in host_key else '主持人B')
            archetype = identity.get('archetype', '观察者')
            lines.append(f"【姓名】{name}")
            lines.append(f"【人设】{archetype}")

            if identity.get("core_drive"):
                lines.append(f"【核心驱动力】{identity.get('core_drive')}")

            if identity.get("chemistry"):
                lines.append(f"【互动风格】与搭档互动时，{identity.get('chemistry')}")

            lines.append("【表达风格】")
            lines.append(f"- 语速：{expression.get('pace', 'normal')}")
            lines.append(f"- 句长偏好：{expression.get('sentence_length', 'mixed')}")

            phrases = expression.get("signature_phrases", [])
            if phrases:
                lines.append(f"- 标志性用语：{', '.join(['「' + p + '」' for p in phrases])}")

            lines.append(f"- 整体态度：{expression.get('attitude', 'curious')}")

            voice_id = expression.get("voice_id", "")
            if voice_id:
                lines.append(f"- 音色ID：{voice_id}")

            return lines

        lines = []
        lines.append("=" * 60)
        lines.append("【高优先级】主持人角色设定 - 必须严格遵循")
        lines.append("=" * 60)
        lines.append("以下角色设定优先级最高，生成对话时必须严格遵循这些人格特征，")
        lines.append("禁止偏离或回到默认设定。")
        lines.append("")

        # 双主持人格式
        if "host_a" in persona and "host_b" in persona:
            lines.extend(_build_host_section("主持人A", persona["host_a"]))
            lines.append("")
            lines.extend(_build_host_section("主持人B", persona["host_b"]))
        # 单主持人格式（兼容旧版）
        elif "identity" in persona:
            lines.extend(_build_host_section("主持人", persona))
        else:
            # 兜底：把整个字典打印出来
            lines.append("【原始配置】")
            lines.append(str(persona))

        if retrieved_memories:
            lines.append("")
            lines.append("【可选记忆】（仅当话题直接相关时自然引用）")
            for mem in retrieved_memories:
                lines.append(f"- {mem}")

        lines.append("")
        lines.append("=" * 60)
        lines.append("【角色设定结束】对话生成必须严格遵循上述人格设定")
        lines.append("=" * 60)

        return "\n".join(lines)

    def _build_persona_config_for_input(self, persona: dict) -> dict:
        """
        为Script Generator构建persona_config输入
        统一格式：host_a/host_b 都是三层结构（identity/expression/memory_seed）
        """
        # 检查是否是双主持人格式（有 host_a/host_b 键）
        if "host_a" in persona and "host_b" in persona:
            # 新的统一格式
            host_a = persona["host_a"]
            host_b = persona["host_b"]

            return {
                "host_a": {
                    "base_profile": {
                        "name": host_a.get("identity", {}).get("name", ""),
                        "archetype": host_a.get("identity", {}).get("archetype", ""),
                        "core_drive": host_a.get("identity", {}).get("core_drive", ""),
                        "expression_style": f"{host_a.get('expression', {}).get('pace', '')}，"
                                            f"{host_a.get('expression', {}).get('attitude', '')}，"
                                            f"常用：{', '.join(host_a.get('expression', {}).get('signature_phrases', []))}",
                        "voice_id": host_a.get("expression", {}).get("voice_id", "")
                    },
                    "memory_seed": host_a.get("memory_seed", []),
                    "role": "对话发起者"
                },
                "host_b": {
                    "base_profile": {
                        "name": host_b.get("identity", {}).get("name", ""),
                        "archetype": host_b.get("identity", {}).get("archetype", ""),
                        "core_drive": host_b.get("identity", {}).get("core_drive", ""),
                        "expression_style": f"{host_b.get('expression', {}).get('pace', '')}，"
                                            f"{host_b.get('expression', {}).get('attitude', '')}，"
                                            f"常用：{', '.join(host_b.get('expression', {}).get('signature_phrases', []))}",
                        "voice_id": host_b.get("expression", {}).get("voice_id", "")
                    },
                    "memory_seed": host_b.get("memory_seed", []),
                    "role": "追问者/观点补充者"
                },
                "relationship": "老搭档"
            }

        # 兼容旧格式（单层结构或单主持人格式）
        if "identity" in persona:
            # 单主持人新格式
            return {
                "host_a": {
                    "base_profile": {
                        "name": persona["identity"].get("name", ""),
                        "archetype": persona["identity"].get("archetype", ""),
                        "core_drive": persona["identity"].get("core_drive", ""),
                        "expression_style": f"{persona.get('expression', {}).get('pace', '')}，"
                                            f"{persona.get('expression', {}).get('attitude', '')}，"
                                            f"常用：{', '.join(persona.get('expression', {}).get('signature_phrases', []))}",
                        "voice_id": persona.get("expression", {}).get("voice_id", "")
                    },
                    "role": "对话发起者"
                },
                "host_b": {
                    "base_profile": {
                        "name": "小北",
                        "archetype": "讲故事的人",
                        "role": "追问者/观点补充者"
                    },
                    "role": "追问者/观点补充者"
                },
                "relationship": "老搭档"
            }

        # 回退到最简单的格式
        return {
            "host_a": {
                "base_profile": persona.get("host_a", {}),
                "role": "对话发起者/观点阐述者"
            },
            "host_b": {
                "base_profile": persona.get("host_b", {}),
                "role": "追问者/观点补充者"
            },
            "relationship": "老搭档"
        }

    def _get_all_materials(self, research_pkg: dict) -> List[dict]:
        """获取所有可用的materials"""
        # 尝试多个可能的位置
        materials = research_pkg.get("enriched_materials", [])
        if not materials and "deep_result" in research_pkg:
            materials = research_pkg["deep_result"].get("enriched_materials", [])
        if not materials and "broad_result" in research_pkg:
            materials = research_pkg["broad_result"].get("preliminary_materials", [])
        return materials

    def _get_segment_materials(self, seg_design: dict, research_pkg: dict) -> List[dict]:
        """获取segment所需的materials"""
        materials_to_use = seg_design.get("materials_to_use", [])
        # enriched_materials 可能在 deep_result 内部
        all_materials = research_pkg.get("enriched_materials", [])
        if not all_materials and "deep_result" in research_pkg:
            all_materials = research_pkg["deep_result"].get("enriched_materials", [])

        # 根据material_id匹配
        result = []
        for mat in all_materials:
            mat_id = mat.get("material_id", "")
            if mat_id in materials_to_use:
                result.append(mat)

        # 如果没有匹配到，返回前3条
        if not result and all_materials:
            result = all_materials[:3]

        return result

    def _get_narrative_context(self, research_pkg: dict) -> dict:
        """获取叙事上下文（hook和central_insight）"""
        # 首先尝试直接从research_pkg获取
        hook = research_pkg.get("hook", "")
        central_insight = research_pkg.get("central_insight", "")
        content_outline = research_pkg.get("content_outline")

        # 如果没有，尝试从insight_result.narrative_design获取
        if not hook and "insight_result" in research_pkg:
            narrative_design = research_pkg["insight_result"].get("narrative_design", {})
            hook = narrative_design.get("hook", "")
            # central_insight可能在tension_design中
            tension_design = narrative_design.get("tension_design", {})
            central_insight = tension_design.get("central_conflict", "")

        return {
            "hook": hook,
            "central_insight": central_insight,
            "content_outline": content_outline
        }

    def _get_style_config(self, style_name: str) -> dict:
        """获取风格模板配置"""
        # 从已加载的模板中查找
        style_templates = {}
        style_dir = Path(__file__).parent.parent / "config" / "styles"
        if style_dir.exists():
            for style_file in style_dir.glob("*.json"):
                with open(style_file, "r", encoding="utf-8") as f:
                    style_templates[style_file.stem] = json.load(f)

        if style_name in style_templates:
            config = style_templates[style_name]
            # 提取Script Agent需要的字段
            return {
                "name": config.get("name", style_name),
                "content_characteristics": config.get("content_characteristics", {}),
                "persona_interaction": config.get("persona_interaction", {}),
                "special_instructions": config.get("special_instructions", "")
            }

        # 默认配置
        return {
            "name": style_name,
            "content_characteristics": {
                "data_density": "高",
                "storytelling_ratio": "中",
                "debate_intensity": "中"
            },
            "persona_interaction": {
                "interaction_frequency": "高"
            },
            "special_instructions": ""
        }
