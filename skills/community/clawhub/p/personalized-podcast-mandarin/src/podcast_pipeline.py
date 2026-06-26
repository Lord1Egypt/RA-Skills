# -*- coding: utf-8 -*-
"""
AI播客生成完整Pipeline
整合Unified Research Agent + Script Generator + TTS
"""
import sys
sys.path.insert(0, '.')

import os
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    os.environ.pop(k, None)

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import uuid
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
from pydantic import BaseModel

from src.volcano_client_requests import create_ark_client_requests
from src.web_scraper import WebScraper, WebScraperError
from src.pdf_parser import PDFParser, PDFParserError
from src.tts_controller import VolcanoTTSController
from src.persona_manager import PersonaManager, DoublePersonaManager, check_first_time as check_first_time_global
from src.memory_skill import MemorySkill
from src.config_loader import ConfigLoader
from src.setup_wizard import ensure_configured

class UnifiedResearchResult(BaseModel):
    """Unified Research Agent输出"""
    schema_version: str = "1.0"
    session_id: str
    execution_info: dict
    result: dict
    metadata: dict

from src.script_generator import ScriptGenerator


class PodcastPipeline:
    """播客生成Pipeline"""

    def __init__(self, api_key: Optional[str] = None, user_id: str = "default", persona_name: str = "default", skip_client_init: bool = False):
        self.session_id = uuid.uuid4().hex[:12]
        self.user_id = user_id
        self.persona_name = persona_name

        # 加载prompts
        self._load_prompts()

        # 加载配置
        self._load_configs(persona_name)

        # 自动加载配置（从 private/ 或环境变量）
        if not skip_client_init:
            config = ConfigLoader().load()
            if api_key is None:
                api_key = config.get("doubao_api_key")
            self.client = create_ark_client_requests(api_key=api_key)
        else:
            self.client = None

    def _load_prompts(self):
        """加载所有agent prompts"""
        prompt_dir = Path(__file__).parent.parent / "agents"

        with open(prompt_dir / "unified-research-agent.md", "r", encoding="utf-8") as f:
            self.research_prompt = f.read()

        with open(prompt_dir / "script-generator.md", "r", encoding="utf-8") as f:
            self.script_prompt = f.read()

    def _load_configs(self, persona_name: str = "default"):
        """加载配置"""
        config_dir = Path(__file__).parent.parent / "config"

        # 尝试加载指定Persona，如果不存在则使用默认
        persona_manager = PersonaManager(self.user_id, persona_name)
        if persona_manager.exists():
            self.default_persona = persona_manager.load()
            self.using_user_persona = True
        else:
            # 回退到default persona
            default_manager = PersonaManager(self.user_id, "default")
            if default_manager.exists():
                self.default_persona = default_manager.load()
                self.using_user_persona = True
            else:
                # 再回退：尝试组合 host_a + host_b
                host_a_manager = PersonaManager(self.user_id, "host_a")
                host_b_manager = PersonaManager(self.user_id, "host_b")
                if host_a_manager.exists() and host_b_manager.exists():
                    self.default_persona = {
                        "host_a": host_a_manager.load(),
                        "host_b": host_b_manager.load()
                    }
                    self.using_user_persona = True
                else:
                    with open(config_dir / "default-persona.json", "r", encoding="utf-8") as f:
                        self.default_persona = json.load(f)
                    self.using_user_persona = False

        # 加载风格模板
        self.style_templates = {}
        style_dir = config_dir / "styles"
        if style_dir.exists():
            for style_file in style_dir.glob("*.json"):
                with open(style_file, "r", encoding="utf-8") as f:
                    self.style_templates[style_file.stem] = json.load(f)

        # 初始化Memory子Skill
        self.memory_skill = MemorySkill(self.user_id)

    def _resolve_persona(
        self,
        persona_config: Optional[dict],
        persona_description: Optional[str],
        preset: Optional[str],
        document_text: Optional[str] = None,
        verbose: bool = False
    ) -> dict:
        """
        解析 persona 配置。
        如果传入了 persona_config 直接返回；否则委托给 PersonaResolver。
        """
        # 1. 直接传入的 config 最高优先级（外层 Agent 已决定）
        if persona_config:
            if verbose:
                print(f"  使用自定义 persona 配置")
            return persona_config

        # 2. 委托给 PersonaResolver（处理 preset / description / document / default 全逻辑）
        from .persona_resolver import PersonaResolver
        resolver = PersonaResolver(self.user_id, skip_client_init=(self.client is None))
        if self.client:
            resolver.client = self.client

        result = resolver.resolve(
            explicit_description=persona_description,
            document_text=document_text,
            preset_name=preset,
            verbose=verbose
        )
        return result.persona_config

    @staticmethod
    def _infer_persona_from_source(source: str) -> tuple[str, Optional[str]]:
        """
        轻量级正则推断：从自然语言输入中提取话题和 persona 描述。
        仅用于 standalone CLI 无显式参数时的兜底解析。

        返回: (topic, persona_description)
        persona_description 为 None 表示未检测到 persona 意图。
        """
        import re

        s = source.strip()
        predefined_styles = {"深度对谈", "观点交锋", "发散漫谈", "高效传达", "喜剧风格"}

        patterns = [
            # 用...风格/口吻/方式/腔调(来讲/来/分析/聊聊/解读/说/介绍/讨论)...
            r"^用(.+?)(?:的)?(?:风格|口吻|方式|语气|腔调)(?:来)?(?:讲|分析|聊聊|解读|说|介绍|讨论)(.+)$",
            # 像...那样/一样(来讲/来/讲/分析/聊聊/解读/说/主持)...
            r"^像(.+?)(?:那样|一样)(?:来讲|来|讲|分析|聊聊|解读|说|介绍|讨论|主持)(.+)$",
            # 像...那样/一样...
            r"^像(.+?)(?:那样|一样)(.+)$",
            # 以...的(风格|口吻|角度|身份|腔调)(来讲/来/分析/聊聊/解读/说)...
            r"^以(.+?)(?:的)?(?:风格|口吻|角度|身份|腔调)(?:来)?(?:讲|分析|聊聊|解读|说|介绍|讨论)(.+)$",
            # 让...来(讲/分析/聊聊/解读/说/介绍/讨论/主持)...
            r"^让(.+?)来(?:讲|分析|聊聊|解读|说|介绍|讨论|主持)(.+)$",
            # 让...(讲/分析/聊聊/解读/说/介绍/讨论/主持)...
            r"^让(.+?)(?:讲|分析|聊聊|解读|说|介绍|讨论|主持)(.+)$",
        ]

        for pattern in patterns:
            m = re.match(pattern, s, re.IGNORECASE)
            if m:
                persona_desc = m.group(1).strip()
                topic = m.group(2).strip()
                # 去除 topic 前的冗余连接词和动词
                topic = re.sub(r"^(?:的|来讲|来|讲|分析|聊聊|解读|说|介绍|讨论|主持)?(.+)$", r"\1", topic).strip()
                if not topic:
                    topic = s
                # 过滤掉纯风格名（避免把风格当 persona）
                if persona_desc in predefined_styles:
                    return topic, None
                return topic, persona_desc

        return s, None

    def check_first_time(self) -> bool:
        """检查是否首次使用（没有Persona）"""
        return check_first_time_global(self.user_id)

    def get_user_persona_status(self) -> dict:
        """获取用户Persona状态"""
        return {
            "has_persona": self.using_user_persona,
            "user_id": self.user_id,
            "memory_stats": self.memory_skill.get_stats()
        }

    def _extract_source_content(self, source: str, source_type: str, verbose: bool = False) -> str:
        """
        根据 source_type 提取原始内容

        Args:
            source: 主题/URL/PDF路径
            source_type: topic|url|pdf
            verbose: 是否打印详细日志

        Returns:
            提取的文本内容
        """
        if source_type == "url":
            if verbose:
                print(f"  正在抓取 URL: {source[:60]}...")
            try:
                scraper = WebScraper()
                content = scraper.fetch(source)
                if verbose:
                    print(f"  ✓ 抓取成功，内容长度: {len(content)} 字符")
                return content
            except WebScraperError as e:
                if verbose:
                    print(f"  ✗ 抓取失败: {e}")
                raise

        elif source_type == "pdf":
            if verbose:
                print(f"  正在解析 PDF: {source}")
            try:
                parser = PDFParser()
                content = parser.parse(source)
                if verbose:
                    print(f"  ✓ 解析成功，内容长度: {len(content)} 字符")
                return content
            except PDFParserError as e:
                if verbose:
                    print(f"  ✗ 解析失败: {e}")
                raise

        else:
            # topic 类型，直接返回主题
            return source

    def generate(
        self,
        source: str,
        source_type: str = "topic",
        style: str = "深度对谈",
        persona_config: Optional[dict] = None,
        persona_description: Optional[str] = None,
        preset: Optional[str] = None,
        document_text: Optional[str] = None,
        output_dir: str = "./output",
        verbose: bool = True,
        research_package: Optional[dict] = None,
        skip_audio: bool = False,
        pause_before_audio: bool = False,
        target_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        生成完整播客

        Args:
            source: 主题/URL/PDF路径
            source_type: topic|url|pdf
            style: 风格模板名称，用户随意指定，不与persona绑定
            persona_config: 自定义persona配置
            persona_description: 一句话描述双主持人（如"像鲁豫那样温暖的女主持搭配沉稳男嘉宾"）
            preset: 预设名称（如"鲁豫有约-鲁豫"）
            document_text: 从文档中提取persona的原始文本
            output_dir: 输出目录
            verbose: 是否打印详细日志
            research_package: 外部Sub-Agent提供的Research Package（可选）
            skip_audio: 是否跳过音频生成
            pause_before_audio: 是否在音频生成前暂停，等待用户确认
            target_length: 用户显式指定的目标字数（优先级最高），默认由大纲动态计算

        Returns:
            完整结果字典
        """
        if verbose:
            print("=" * 80)
            print("AI播客生成Pipeline")
            print(f"Session ID: {self.session_id}")
            print(f"Source: {source}")
            print(f"User Style: {style}")
            print("=" * 80)

        # 处理 persona 配置（委托给 PersonaResolver）
        persona = self._resolve_persona(
            persona_config=persona_config,
            persona_description=persona_description,
            preset=preset,
            document_text=document_text,
            verbose=verbose
        )

        # Memory 闭环：将 persona 中的 memory_seed 同步到 MemorySkill
        memory_synced = self._sync_memory_from_persona(persona)
        if verbose and memory_synced:
            print(f"  已同步 persona memory_seed 到记忆库")

        # Step 1: Research & Narrative
        research_pkg = self._run_research(
            source=source,
            source_type=source_type,
            style=style,
            persona=persona,
            verbose=verbose,
            research_package=research_package
        )

        if not research_pkg:
            return {"error": "Research failed", "session_id": self.session_id}

        # 用户指定的 style 优先于 research_package 中的 style_selected，解耦 persona 与风格
        effective_style = self._resolve_style(user_style=style, research_pkg=research_pkg)
        research_pkg["style_selected"] = effective_style
        if verbose:
            print(f"  生效风格: {effective_style}")

        # 大纲预览：无论什么模式都展示给用户
        if verbose:
            self._print_outline(research_pkg, user_target_length=target_length)

        if verbose and target_length:
            print(f"  用户指定目标字数: {target_length}")

        # Step 2: Script Generation
        generator = ScriptGenerator(
            client=self.client,
            memory_skill=self.memory_skill,
            script_prompt=self.script_prompt
        )
        full_script = generator.generate(
            research_pkg=research_pkg,
            persona=persona,
            effective_style=effective_style,
            verbose=verbose,
            target_length=target_length
        )

        if not full_script:
            return {"error": "Script generation failed", "session_id": self.session_id}

        # Step 3: Audio Generation (TTS)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 检查点：如用户要求先检查文本，则暂停等待确认
        if pause_before_audio:
            print("\n[检查点] 文本脚本已生成。")
            print(f"  Markdown 文件: {output_path / f'podcast_{self.session_id}.md'}")
            print("  按 Enter 继续生成音频，或输入 'skip' 跳过音频生成: ", end="")
            try:
                user_input = input().strip().lower()
                if user_input == "skip":
                    skip_audio = True
            except EOFError:
                pass

        audio_file = None
        if not skip_audio:
            audio_file = self._generate_audio(
                script=full_script,
                persona=persona,
                output_dir=output_path,
                verbose=verbose
            )

        # Step 4: Save results
        json_file = output_path / f"podcast_{self.session_id}.json"
        md_file = output_path / f"podcast_{self.session_id}.md"

        result = {
            "session_id": self.session_id,
            "source": source,
            "source_type": source_type,
            "style": effective_style,
            "research": research_pkg,
            "script": full_script,
            "audio_path": str(audio_file) if audio_file else None,
            "json_path": str(json_file),
            "markdown_path": str(md_file),
            "timestamp": datetime.now().isoformat()
        }

        # 保存JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 保存Markdown
        self._save_markdown(result, md_file)

        if verbose:
            print(f"\n结果已保存:")
            print(f"  JSON: {json_file}")
            print(f"  Markdown: {md_file}")
            if audio_file:
                print(f"  Audio: {audio_file}")

        # 生成并展示摘要
        if verbose:
            from .summary_generator import SummaryGenerator
            print()
            summary_gen = SummaryGenerator(result)
            summary_gen.print_summary(verbose=True)

        return result

    def _run_research(
        self,
        source: str,
        source_type: str,
        style: str,
        persona: dict,
        verbose: bool,
        research_package: Optional[dict] = None
    ) -> Optional[dict]:
        """运行Research Agent（优先使用外部传入的research_package，否则本地LLM fallback）"""
        if research_package is not None:
            if verbose:
                print("\n[Step 1] Research & Narrative (使用外部Sub-Agent Research Package)...")
            try:
                from src.schema import ResearchPackage
                pkg = ResearchPackage.model_validate(research_package)
                if verbose:
                    print(f"  ✓ 外部Research Package已接收")
                    print(f"    风格: {pkg.style_selected}")
                    print(f"    Segments: {len(pkg.segments)}")
                return pkg.model_dump()
            except Exception as e:
                if verbose:
                    print(f"  ✗ 外部Research Package验证失败: {e}")
                    print(f"  → 回退到本地Research...")

        if verbose:
            print("\n[Step 1] Research & Narrative...")

        # 根据 source_type 提取原始内容
        try:
            raw_content = self._extract_source_content(source, source_type, verbose)
        except (WebScraperError, PDFParserError) as e:
            if verbose:
                print(f"  ✗ 内容提取失败: {e}")
            return None

        # 判断风格是否由用户指定
        # 如果style是列表中的具体风格，视为用户指定
        # 如果style是"auto"或未指定，视为自动判断
        predefined_styles = ["深度对谈", "观点交锋", "发散漫谈", "高效传达", "喜剧风格"]
        style_specified = style in predefined_styles

        input_data = {
            "mode": "unified",
            "current_stage": "broad",
            "completed_stages": [],
            "context": {
                "source": source,
                "source_type": source_type,
                "raw_content": raw_content[:50000]  # 限制长度避免超限
            },
            "style_template": style if style_specified else "auto",
            "style_specified_by_user": style_specified,
            "persona_config": persona
        }

        try:
            result, tokens = self.client.chat_completion(
                system_prompt=self.research_prompt,
                user_message=json.dumps(input_data, ensure_ascii=False),
                output_schema=UnifiedResearchResult,
                temperature=0.7,
                max_tokens=8192
            )

            if verbose:
                print(f"  ✓ 完成")
                print(f"    阶段: {result.execution_info.get('completed_stages', [])}")
                print(f"    深度: {result.metadata.get('research_depth', 'unknown')}")
                print(f"    风格: {result.result.get('style_selected', 'unknown')}")
                print(f"    Token: {tokens}")

            return result.result

        except Exception as e:
            if verbose:
                print(f"  ✗ 失败: {e}")
            return None

    def _sync_memory_from_persona(self, persona: dict) -> bool:
        """从 persona 配置中提取 memory_seed 并同步到 MemorySkill，确保注入闭环"""
        memory_seeds = []

        # 双主持人格式
        if "host_a" in persona:
            for host_key in ["host_a", "host_b"]:
                host = persona.get(host_key, {})
                seeds = host.get("memory_seed", [])
                if seeds:
                    memory_seeds.extend(seeds)

        # 单主持人格式
        elif "identity" in persona:
            seeds = persona.get("memory_seed", [])
            if seeds:
                memory_seeds.extend(seeds)

        if memory_seeds:
            return self.memory_skill.init_from_persona(memory_seeds)
        return False

    def _resolve_style(self, user_style: str, research_pkg: dict) -> str:
        """
        确定最终生效风格：用户指定的 style 优先于 research_package 中的 style_selected
        persona 与风格解耦，用户可随意指定任何风格名称
        """
        if user_style and user_style.strip() and user_style.strip().lower() != "auto":
            return user_style.strip()
        # auto 模式或空值，回退到研究阶段的结果
        return research_pkg.get("style_selected") or research_pkg.get("style_template", "深度对谈")

    def _print_outline(self, research_pkg: dict, user_target_length: Optional[int] = None):
        """打印完整大纲供用户查看"""
        print("\n[大纲预览]")
        print("-" * 40)
        content_outline = research_pkg.get("content_outline")
        if content_outline:
            text = content_outline[:300]
            print(f"整体大纲：{text}{'...' if len(content_outline) > 300 else ''}")
        else:
            print("整体大纲：无")

        segments = research_pkg.get("segments", [])
        estimated_total = sum(seg.get("estimated_length", 500) for seg in segments)
        if user_target_length is not None and user_target_length > 0:
            print(f"预计总字数：{user_target_length} 字（用户指定）")
        else:
            print(f"预计总字数：{estimated_total} 字（由大纲动态计算）")

        for seg in segments:
            seg_id = seg.get("segment_id", "?")
            est = seg.get("estimated_length", 500)
            print(f"\n▸ {seg_id} | {seg.get('narrative_function', '')} | 约 {est} 字")
            dramatic = seg.get("dramatic_goal", "")
            if dramatic:
                print(f"  目标：{dramatic}")
            outline = seg.get("outline")
            if outline:
                text = outline[:200]
                print(f"  分镜：{text}{'...' if len(outline) > 200 else ''}")
        print("-" * 40)

    def generate_audio(self, script: List[Dict], persona: dict, output_dir: str, verbose: bool = True) -> Optional[Path]:
        """
        公共接口：根据已生成的脚本单独生成音频

        Args:
            script: 脚本内容（分段格式）
            persona: Persona配置
            output_dir: 输出目录
            verbose: 是否打印详细日志

        Returns:
            音频文件路径，如果失败则返回None
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        return self._generate_audio(script, persona, output_path, verbose)

    def _save_markdown(self, result: dict, output_file: Path):
        """保存为Markdown格式"""
        source_type = result.get('source_type', 'topic')
        audio_path = result.get('audio_path')

        md = f"""# {result['source']}

**Session ID**: {result['session_id']}
**生成时间**: {result['timestamp']}
**输入类型**: {source_type}
**风格**: {result['style']}
"""

        if audio_path:
            md += f"**音频文件**: {audio_path}\n"

        md += """
---

"""

        script = result.get("script", [])
        total_words = sum(seg.get("word_count", 0) for seg in script)
        total_lines = sum(len(seg.get("lines", [])) for seg in script)

        md += f"""## 播客信息

- **总行数**: {total_lines}
- **总字数**: {total_words}
- **预估时长**: {total_words // 3 // 60}分{total_words // 3 % 60}秒

---

"""

        for seg in script:
            md += f"""## {seg['segment_id']}

**Key Moments**: {', '.join(seg.get('key_moments', [])[:2])}

"""
            for line in seg.get("lines", []):
                speaker = line.get("speaker", "?")
                text = line.get("text", "")
                md += f"**{speaker}**: {text}\n\n"

            md += f"\n*{seg.get('summary', '')}*\n\n---\n\n"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md)

    def _generate_audio(
        self,
        script: List[Dict],
        persona: dict,
        output_dir: Path,
        verbose: bool = False
    ) -> Optional[Path]:
        """
        生成音频文件

        Args:
            script: 脚本内容（分段格式）
            persona: Persona配置
            output_dir: 输出目录
            verbose: 是否打印详细日志

        Returns:
            音频文件路径，如果失败则返回None
        """
        # 检查是否有 TTS 配置
        if not os.getenv("VOLCANO_TTS_ACCESS_TOKEN"):
            if verbose:
                print(f"  [TTS] 未配置 VOLCANO_TTS_ACCESS_TOKEN，跳过音频生成")
                print(f"        设置环境变量后可启用 TTS 功能")
            return None

        try:
            if verbose:
                print(f"\n[Step 3] Audio Generation...")
                print(f"  正在初始化 TTS 控制器...")

            controller = VolcanoTTSController()

            # 转换脚本格式以兼容 TTS 控制器
            # 将分段格式转换为行列表
            all_lines = []
            for seg in script:
                for line in seg.get("lines", []):
                    all_lines.append(line)

            if not all_lines:
                if verbose:
                    print(f"  ✗ 没有可用的对话内容")
                return None

            if verbose:
                print(f"  共 {len(all_lines)} 句对话待合成")
                print(f"  开始生成音频（预计2-3分钟）...")

            # 创建输出路径
            output_path = output_dir / f"podcast_{self.session_id}.mp3"

            # 为了兼容现有的 TTS 控制器，创建一个简单的数据类
            from src.schema import ScriptVersion, DialogueLine, TokenUsage

            script_version = ScriptVersion(
                schema_version="1.0",
                session_id=self.session_id,
                outline_checksum="",
                lines=[
                    DialogueLine(
                        speaker=line.get("speaker", "A"),
                        text=line.get("text", "")
                    )
                    for line in all_lines
                ],
                word_count=sum(len(line.get("text", "")) for line in all_lines),
                estimated_duration_sec=len(all_lines) * 3,
                token_usage=TokenUsage(input=0, output=0, total=0)
            )

            # 调用 TTS 生成
            # 传递 persona_config 以使用自定义音色
            result_path = controller.generate_dual_audio(
                script=script_version,
                output_path=output_path,
                persona_config=persona
            )

            if verbose:
                print(f"  ✓ 音频生成完成")
                print(f"    文件: {result_path}")

            return Path(result_path)

        except Exception as e:
            if verbose:
                print(f"  ✗ 音频生成失败: {e}")
            return None


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="AI播客生成Pipeline")
    parser.add_argument("source", help="主题/URL/PDF路径")
    parser.add_argument("--type", default="topic", choices=["topic", "url", "pdf"], help="输入类型")
    parser.add_argument("--style", default="深度对谈", help="风格模板")
    parser.add_argument("--output", default="./output", help="输出目录")
    parser.add_argument("--api-key", help="API Key (可选，默认从环境变量读取)")
    parser.add_argument("--skip-setup", action="store_true", help="跳过配置检查（CI/CD 使用）")
    parser.add_argument("--user-id", default="default", help="用户ID")
    parser.add_argument("--skip-audio", action="store_true", help="跳过音频生成")
    parser.add_argument("--review", action="store_true", help="在音频生成前暂停，等待用户确认")
    parser.add_argument("--target-length", type=int, default=None, help="显式指定目标字数（覆盖大纲估算）")
    parser.add_argument("--persona-description", help="一句话描述双主持人（如'像鲁豫那样温暖的女主持搭配沉稳男嘉宾'）")
    parser.add_argument("--preset", help="使用预设风格（如'鲁豫有约-鲁豫'、'十三邀-许知远'）")
    parser.add_argument("--persona-from-doc", help="从文档文件路径提取主持人人格")
    parser.add_argument("--interactive", action="store_true", help="交互式选择风格（已有配置时有效）")

    args = parser.parse_args()

    document_text = None
    if args.persona_from_doc:
        try:
            with open(args.persona_from_doc, "r", encoding="utf-8") as f:
                document_text = f.read()
        except Exception as e:
            print(f"❌ 读取文档失败: {e}")
            return 1

    # 检查并加载配置（首次使用触发向导）
    if not args.skip_setup:
        if not ensure_configured(user_id=args.user_id, auto_wizard=True):
            print("❌ 配置未完成，无法继续")
            return 1
    else:
        # 仅加载已有配置
        ConfigLoader().load()

    # 处理交互式风格选择（已有配置且未指定新风格时）
    persona_description = args.persona_description
    preset = args.preset

    is_tty = sys.stdin.isatty()
    has_persona_input = bool(args.preset or args.persona_description or args.persona_from_doc)

    from .persona_manager import check_first_time, PersonaManager
    is_first = check_first_time(args.user_id)

    if is_first and not has_persona_input:
        # 首次使用：必须主动确认主持人风格
        if is_tty:
            print("\n🔔 首次使用 detected.")
            print("请描述你想要的双主持人风格（例如：'像鲁豫那样温暖的女主持搭配沉稳男嘉宾'）：")
            desc = input("> ").strip()
            if desc:
                persona_description = desc
            else:
                print("未输入描述，进入预设选择...")
                from .preset_manager import PresetManager
                pm = PresetManager()
                pm.print_preset_menu()
                p_choice = input("选择预设编号（直接回车使用默认）: ").strip()
                if p_choice:
                    try:
                        idx = int(p_choice) - 1
                        presets = pm.list_presets()
                        if 0 <= idx < len(presets):
                            preset = presets[idx]["name"]
                    except:
                        print("⚠️ 无效选择，使用系统默认")
        else:
            print("❌ 首次使用必须指定 --preset、--persona-description 或 --persona-from-doc")
            return 1
    elif not is_first and is_tty and (args.interactive or not has_persona_input):
        # 非首次：已有配置，询问用户
        print("\n检测到已有主持人配置")
        host_a = PersonaManager(args.user_id, "host_a").load()
        if host_a:
            print(f"当前: {host_a['identity']['name']} ({host_a['identity']['archetype']})")

        print("\n  1. 使用当前配置继续")
        print("  2. 一句话更换风格")
        print("  3. 选择其他预设")
        print("  4. 查看当前配置详情")

        choice = input("\n请选择（1-4，默认1）: ").strip() or "1"

        if choice == "2":
            desc = input("请输入新风格描述: ").strip()
            if desc:
                persona_description = desc
        elif choice == "3":
            from .preset_manager import PresetManager
            pm = PresetManager()
            pm.print_preset_menu()
            p_choice = input("选择预设编号（1-8）: ").strip()
            try:
                idx = int(p_choice) - 1
                presets = pm.list_presets()
                if 0 <= idx < len(presets):
                    preset = presets[idx]["name"]
            except:
                print("⚠️ 无效选择，使用当前配置")
        elif choice == "4":
            # 显示详情
            host_b = PersonaManager(args.user_id, "host_b").load()
            if host_a and host_b:
                print(f"\n主持人A: {host_a['identity']['name']}")
                print(f"  原型: {host_a['identity']['archetype']}")
                print(f"  风格: {host_a['expression']['attitude']}")
                print(f"\n主持人B: {host_b['identity']['name']}")
                print(f"  原型: {host_b['identity']['archetype']}")
                print(f"  风格: {host_b['expression']['attitude']}")
            input("\n按回车继续...")
    elif not is_tty and not has_persona_input:
        # 非交互式环境下尝试轻量级正则推断
        inferred_source, inferred_persona = PodcastPipeline._infer_persona_from_source(args.source)
        if inferred_persona:
            print(f"[推断] 从输入中提取到 persona 描述: {inferred_persona}")
            args.source = inferred_source
            persona_description = inferred_persona

    pipeline = PodcastPipeline(api_key=args.api_key, user_id=args.user_id)
    result = pipeline.generate(
        source=args.source,
        source_type=args.type,
        style=args.style,
        persona_description=persona_description,
        preset=preset,
        document_text=document_text,
        output_dir=args.output,
        skip_audio=args.skip_audio,
        pause_before_audio=args.review,
        target_length=args.target_length
    )

    if "error" in result:
        print(f"\n生成失败: {result['error']}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
