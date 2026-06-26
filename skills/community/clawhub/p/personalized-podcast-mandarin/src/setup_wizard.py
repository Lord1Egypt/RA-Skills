# -*- coding: utf-8 -*-
"""
配置向导
交互式引导用户完成初次配置，包括 API Keys 和 Persona 创建
"""

import sys
import json
from typing import Optional, Dict, Any, Tuple, List
from pathlib import Path
from pydantic import BaseModel

from .config_loader import ConfigLoader
from .persona_extractor import extract_persona
from .preset_manager import PresetManager


class HostPersonaSimple(BaseModel):
    """简化版主持人人格结构（用于SetupWizard解析）"""
    name: str
    archetype: str = "观察者"
    attitude: str = "curious"
    voice_gender: str = "male"
    signature_phrases: List[str] = []
    pace: str = "normal"


class TwoHostsResult(BaseModel):
    """两个主持人的解析结果"""
    host_a: HostPersonaSimple
    host_b: HostPersonaSimple


# ------------------------------------------------------------------
# 模块级工具函数（可被外部直接调用，无需实例化 SetupWizard）
# ------------------------------------------------------------------

def save_double_persona(user_id: str, host_a: Dict, host_b: Dict) -> None:
    """保存双主持人配置，并同步设为默认 persona"""
    from .persona_manager import PersonaManager

    manager_a = PersonaManager(user_id, "host_a")
    manager_a.save(host_a)

    manager_b = PersonaManager(user_id, "host_b")
    manager_b.save(host_b)

    # 同步保存为 default.json，确保下次 Pipeline 能直接加载
    default_manager = PersonaManager(user_id, "default")
    default_manager.save({"host_a": host_a, "host_b": host_b})


def select_voice(archetype: str, gender: str, attitude: str) -> str:
    """根据特征选择音色"""
    try:
        from src.voice_selector import VoiceSelector
        return VoiceSelector().suggest_voice(
            archetype=archetype,
            gender=gender,
            attitude=attitude
        )
    except:
        # 默认音色
        if gender == "male":
            return "zh_male_liufei_uranus_bigtts"
        else:
            return "zh_female_vv_uranus_bigtts"


def expand_to_full_persona(traits: Dict) -> Dict:
    """将特征扩展为完整persona结构"""
    name = traits.get("name", "主持人")
    archetype = traits.get("archetype", "观察者")
    attitude = traits.get("attitude", "curious")
    gender = traits.get("voice_gender", "female")

    # 选择音色
    voice_id = select_voice(archetype, gender, attitude)

    return {
        "identity": {
            "name": name,
            "archetype": archetype,
            "core_drive": f"展现{archetype}特质，与搭档形成良好互动",
            "chemistry": "与搭档自然互动，形成对话节奏"
        },
        "expression": {
            "pace": traits.get("pace", "normal"),
            "sentence_length": "mixed",
            "signature_phrases": traits.get("signature_phrases", [])[:3],
            "attitude": attitude,
            "voice_id": voice_id
        },
        "memory_seed": []
    }


def detect_gender(persona: Dict) -> str:
    """检测persona的性别"""
    voice_id = persona.get('expression', {}).get('voice_id', '')
    if 'female' in voice_id or 'nvsheng' in voice_id:
        return "female"
    elif 'male' in voice_id or 'nansheng' in voice_id:
        return "male"
    return "female"  # 默认


def generate_complementary_host(base_host: Dict) -> Dict:
    """生成与host_a互补的host_b"""
    # 简单规则：如果A是追问者，B是讲故事的人；如果A理性，B感性
    archetype_map = {
        "追问者": "讲故事的人",
        "讲故事的人": "追问者",
        "观察者": "吐槽者",
        "吐槽者": "观察者",
        "质疑者": "实践者",
        "实践者": "质疑者",
        "理想主义者": "观察者"
    }

    a_archetype = base_host['identity']['archetype']
    b_archetype = archetype_map.get(a_archetype, "观察者")

    a_gender = detect_gender(base_host)
    b_gender = "male" if a_gender == "female" else "female"

    traits = {
        "name": "搭档",
        "archetype": b_archetype,
        "attitude": "curious" if base_host['expression']['attitude'] == "skeptical" else "playful",
        "voice_gender": b_gender
    }

    return expand_to_full_persona(traits)


class SetupWizard:
    """交互式配置向导"""

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.config_loader = ConfigLoader()
        self.config: Dict[str, Any] = {}

    def run(self) -> bool:
        """
        运行配置向导

        Returns:
            是否配置成功
        """
        print("=" * 60)
        print("🎙️ AI播客生成器 - 首次使用配置向导")
        print("=" * 60)
        print()

        # 检查当前配置状态
        missing = self.config_loader.check_missing_configs()

        # 1. 配置 Doubao API
        if not missing.get("doubao_api_key"):
            print("✓ Doubao API Key 已配置")
        else:
            if not self._setup_doubao():
                return False

        # 2. 配置 TTS（可选）
        if not missing.get("tts_app_id") or not missing.get("tts_access_token"):
            print("✓ TTS 配置已存在")
        else:
            self._setup_tts()

        # 3. 创建 Persona（可选但推荐）
        self._setup_persona()

        print()
        print("=" * 60)
        print("✅ 配置完成！你可以开始使用 AI播客生成器了。")
        print("=" * 60)
        print()

        return True

    def _setup_doubao(self) -> bool:
        """配置 Doubao API"""
        print("📋 步骤 1/3: 配置 Doubao API（用于生成播客内容）")
        print("-" * 60)
        print("你需要提供火山引擎 Doubao API 的以下信息：")
        print("  - API Key: 用于访问大模型")
        print("  - Endpoint ID: 模型接入点（如 ep-20240328-xxx）")
        print()
        print("💡 获取方式: 火山引擎控制台 > 模型推理 > 在线推理")
        print()

        # API Key
        api_key = input("请输入 Doubao API Key: ").strip()
        if not api_key:
            print("❌ API Key 不能为空")
            print("   提示：如果你已有环境变量配置，可使用 --skip-setup 跳过向导")
            return False

        # Endpoint ID（可选）
        endpoint_id = input("请输入 Endpoint ID（可选，直接回车跳过）: ").strip()
        if not endpoint_id:
            endpoint_id = "ep-20240328-default"

        # 模型选择
        print()
        print("选择模型：")
        print("  1. Doubao-Seed-2.0-lite（默认，轻量快速）")
        print("  2. Doubao-Pro-32k（功能更强）")
        choice = input("请输入选项（1/2，默认1）: ").strip() or "1"

        model = "Doubao-Seed-2.0-lite" if choice == "1" else "Doubao-Pro-32k"

        # 保存配置
        success = self.config_loader.save_config(
            "doubao",
            api_key=api_key,
            endpoint_id=endpoint_id,
            model=model
        )

        if success:
            print("✓ Doubao 配置已保存")
            # 立即加载到环境变量
            self.config_loader.load()
            return True
        else:
            print("❌ 配置保存失败")
            return False

    def _setup_tts(self) -> bool:
        """配置 TTS（可选）"""
        print()
        print("📋 步骤 2/3: 配置 TTS（用于生成音频，可选）")
        print("-" * 60)
        print("如果你需要生成播客音频，请提供火山引擎 TTS 配置：")
        print()

        choice = input("是否现在配置 TTS？(y/n，默认n）: ").strip().lower()
        if choice != "y":
            print("跳过 TTS 配置，你可以稍后手动添加")
            return True

        print()
        print("💡 获取方式: 火山引擎控制台 > 语音技术 > 语音合成")
        print()

        app_id = input("请输入 App ID: ").strip()
        access_token = input("请输入 Access Token: ").strip()
        secret_key = input("请输入 Secret Key（可选）: ").strip()

        if not app_id or not access_token:
            print("⚠️ App ID 和 Access Token 不能为空，跳过 TTS 配置")
            return True

        success = self.config_loader.save_config(
            "tts",
            app_id=app_id,
            access_token=access_token,
            secret_key=secret_key or ""
        )

        if success:
            print("✓ TTS 配置已保存")
            self.config_loader.load()
            return True
        else:
            print("❌ TTS 配置保存失败")
            return True  # TTS 是可选的

    def _setup_persona(self) -> bool:
        """配置双主持人 - 简化版4选项"""
        print()
        print("📋 步骤 3/3: 配置你的播客搭档")
        print("-" * 60)
        print("播客需要两位主持人对话。你想怎么创建他们？\n")
        print("  1️⃣  风格预设（最快）")
        print("      一键使用：鲁豫有约、十三邀、圆桌派、罗永浩、李诞...\n")
        print("  2️⃣  一句话描述（最自由）")
        print("      如：'像鲁豫那样温暖的女主持，搭配沉稳理性的男嘉宾'\n")
        print("  3️⃣  从文档提取")
        print("      上传人物访谈/自传，提取真实人格\n")
        print("  4️⃣  使用默认")
        print("      阿明（追问者）+ 小北（讲故事的人）\n")

        choice = input("请选择（1-4，默认1）: ").strip() or "1"

        if choice == "1":
            return self._setup_preset_personas()
        elif choice == "2":
            return self._setup_one_line_personas()
        elif choice == "3":
            return self._setup_document_personas()
        else:
            return self._setup_default_personas()

    def _setup_preset_personas(self) -> bool:
        """使用风格预设"""
        print()
        preset_manager = PresetManager()
        preset_manager.print_preset_menu()

        choice = input("请选择风格编号（1-8，默认1）: ").strip() or "1"

        try:
            choice_idx = int(choice) - 1
            presets = preset_manager.list_presets()

            if choice_idx < 0 or choice_idx >= len(presets):
                print("⚠️ 无效选择，使用默认配置")
                return self._setup_default_personas()

            selected_preset = presets[choice_idx]
            preset_name = selected_preset["name"]

            print()
            print(preset_manager.get_preset_summary(preset_name))
            print()

            confirm = input(f"确认使用 '{preset_name}'？(y/n，默认y）: ").strip().lower()
            if confirm == "n":
                return self._setup_preset_personas()  # 重新选择

            # 应用预设
            preset_config = preset_manager.apply_preset(preset_name)

            # 保存双主持人配置
            self._save_double_persona(
                preset_config["persona_config"]["host_a"],
                preset_config["persona_config"]["host_b"]
            )

            print()
            print(f"✓ 已应用 '{preset_name}' 风格")
            print(f"  主持人A: {preset_config['persona_config']['host_a']['identity']['name']}")
            print(f"  主持人B: {preset_config['persona_config']['host_b']['identity']['name']}")

            return True

        except Exception as e:
            print(f"⚠️ 配置失败: {e}")
            return self._setup_default_personas()

    def _setup_one_line_personas(self) -> bool:
        """一句话描述双主持人（合并了详细自定义）"""
        print()
        print("📝 描述你的双主持人")
        print("-" * 40)
        print("请用一句话描述两位主持人，或选择模板：\n")

        templates = {
            "a": ("互补型", "知性理性的女主持 + 幽默风趣的男搭档"),
            "b": ("对立型", "犀利追问的女记者 + 圆滑回避的政客"),
            "c": ("搭档型", "两个都爱吐槽的损友"),
            "d": ("师生型", "博学的导师 + 好奇的学徒"),
        }

        for key, (name, example) in templates.items():
            print(f"  [{key}] {name}: {example}")
        print()

        user_input = input("你的描述（或输入a/b/c/d）: ").strip()

        # 处理模板选择
        if user_input.lower() in templates:
            template_name, template_example = templates[user_input.lower()]
            print(f"\n已选择模板 [{template_name}]")
            user_desc = input(f"请基于模板描述（直接回车使用示例）: ").strip()
            if not user_desc:
                user_desc = template_example
        else:
            user_desc = user_input

        if not user_desc:
            print("⚠️ 未输入描述，使用默认")
            return self._setup_default_personas()

        print(f"\n🤖 正在分析: '{user_desc}'")

        try:
            host_a, host_b = self.parse_two_personas(user_desc)

            # 预览并确认
            print(f"\n已生成:")
            print(f"  A: {host_a['identity']['name']} ({host_a['identity']['archetype']})")
            print(f"     风格: {host_a['expression']['attitude']} | 口头禅: {', '.join(host_a['expression']['signature_phrases'][:2])}")
            print(f"  B: {host_b['identity']['name']} ({host_b['identity']['archetype']})")
            print(f"     风格: {host_b['expression']['attitude']} | 口头禅: {', '.join(host_b['expression']['signature_phrases'][:2])}")

            confirm = input("\n确认？(y/n/adjust，默认y）: ").strip().lower()

            if confirm == "n":
                return self._setup_one_line_personas()  # 重新输入
            elif confirm == "adjust":
                host_a, host_b = self._adjust_personas(host_a, host_b)

            # 保存
            self._save_double_persona(host_a, host_b)
            print("\n✓ 双主持人配置已保存")
            return True

        except Exception as e:
            print(f"⚠️ 生成失败: {e}")
            return self._setup_default_personas()

    def _setup_document_personas(self) -> bool:
        """从文档提取双主持人"""
        print()
        print("📄 从文档提取人物")
        print("-" * 40)
        print("方式：")
        print("  1. 粘贴文本")
        print("  2. 输入文件路径")

        method = input("\n请选择（1/2，默认1）: ").strip() or "1"

        text = ""
        if method == "1":
            print("\n请粘贴文本（输入 END 结束）：")
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                except EOFError:
                    break
            text = "\n".join(lines)
        else:
            path = input("文件路径: ").strip()
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                print(f"⚠️ 读取失败: {e}")
                return self._setup_default_personas()

        if len(text) < 100:
            print("⚠️ 文本太短，无法提取有效特征")
            return self._setup_default_personas()

        print(f"\n🤖 正在分析文本（{len(text)}字）...")

        try:
            # 使用 extract_persona 提取，但尝试识别多个人物
            # 这里简化处理，实际可以扩展 extractor 支持多人物
            personas = self._extract_multiple_personas(text)

            if len(personas) < 1:
                print("⚠️ 未检测到人物特征")
                return self._setup_default_personas()

            print(f"\n检测到 {len(personas)} 个人物特征：")
            for i, p in enumerate(personas, 1):
                name = p['identity']['name'] or f"人物{i}"
                archetype = p['identity']['archetype']
                print(f"  {i}. {name} - {archetype}")

            if len(personas) >= 2:
                a_idx = int(input("\n请选择主持人A（编号，默认1）: ") or "1") - 1
                b_idx = int(input("请选择主持人B（编号，默认2）: ") or "2") - 1
                host_a = personas[a_idx]
                host_b = personas[b_idx]
            else:
                # 只有一个人物，生成一个互补的
                host_a = personas[0]
                host_b = self._generate_complementary_host(host_a)
                print(f"\n只检测到1个人物，已自动生成互补的B:")

            self._save_double_persona(host_a, host_b)
            print(f"\n✓ 已设置: {host_a['identity']['name']} + {host_b['identity']['name']}")
            return True

        except Exception as e:
            print(f"⚠️ 提取失败: {e}")
            return self._setup_default_personas()

    def _setup_default_personas(self) -> bool:
        """使用默认配置"""
        print("\n使用系统默认配置: 阿明 + 小北")
        # 不创建自定义persona，系统会使用 default-persona.json
        return True

    def parse_two_personas(self, description: str) -> Tuple[Dict, Dict]:
        """
        从一句话描述解析两位主持人
        可以作为公共方法被外部调用
        """
        system_prompt = """从用户描述中提取两个播客主持人的人格特征。

描述格式可能是：
- "像X那样...，搭配像Y那样..."（明确两个人）
- "A风格的...，搭配B风格的..."（特征描述）
- 整体氛围描述（需推断两个人）

请输出JSON格式：
{
    "host_a": {
        "name": "主持人名称，如'鲁豫'、'阿明'",
        "archetype": "观察者/讲故事的人/质疑者/实践者/吐槽者/理想主义者",
        "attitude": "curious/skeptical/playful/mournful/authoritative",
        "voice_gender": "male/female",
        "signature_phrases": ["口头禅1", "口头禅2"],
        "pace": "fast/normal/slow"
    },
    "host_b": {
        ...
    }
}"""

        try:
            from src.volcano_client_requests import create_ark_client_requests
            client = create_ark_client_requests()

            result, _ = client.chat_completion(
                system_prompt=system_prompt,
                user_message=f"描述：{description}",
                output_schema=TwoHostsResult,
                temperature=0.7
            )
            parsed = result.model_dump()

            # 扩展为完整 persona 结构
            host_a = expand_to_full_persona(parsed["host_a"])
            host_b = expand_to_full_persona(parsed["host_b"])

            return host_a, host_b

        except Exception as e:
            # 如果解析失败，使用默认值
            print(f"⚠️ 解析描述失败: {e}，使用默认配置")
            return self._get_default_host_a(), self._get_default_host_b()

    def _adjust_personas(self, host_a: Dict, host_b: Dict) -> Tuple[Dict, Dict]:
        """微调主持人配置"""
        print("\n🔧 微调主持人")
        print("  1. 调整A的名称/性格")
        print("  2. 调整B的名称/性格")
        print("  3. 重新生成")
        print("  4. 完成")

        choice = input("\n请选择（1-4，默认4）: ").strip() or "4"

        if choice == "1":
            name = input(f"A名称（当前: {host_a['identity']['name']}）: ").strip()
            if name:
                host_a['identity']['name'] = name
        elif choice == "2":
            name = input(f"B名称（当前: {host_b['identity']['name']}）: ").strip()
            if name:
                host_b['identity']['name'] = name
        elif choice == "3":
            return self.parse_two_personas(input("重新描述: "))

        return host_a, host_b

    def _extract_multiple_personas(self, text: str) -> list:
        """从长文本提取多个人物"""
        # 简化实现：提取一个主要人物，如果文本长则分段提取
        # 实际可以扩展为更复杂的多人物检测

        try:
            from src.persona_extractor import extract_persona
            # 截取文本前半部分提取第一个人
            first_half = text[:4000] if len(text) > 4000 else text
            persona1 = extract_persona(first_half, raise_on_error=False)

            if len(text) > 2000:
                # 从后半部分尝试提取第二个人
                second_half = text[-4000:] if len(text) > 4000 else text
                persona2 = extract_persona(second_half, raise_on_error=False)

                # 如果两个人物有明显区别，返回两个
                if (persona1['identity']['archetype'] != persona2['identity']['archetype'] or
                    persona1['identity']['name'] != persona2['identity']['name']):
                    return [persona1, persona2]

            return [persona1]
        except:
            return []

    def _generate_complementary_host(self, host_a: Dict) -> Dict:
        """生成与host_a互补的host_b（委托到模块级函数）"""
        return generate_complementary_host(host_a)

    def _save_double_persona(self, host_a: Dict, host_b: Dict):
        """保存双主持人配置，并同步设为默认 persona（委托到模块级函数）"""
        save_double_persona(self.user_id, host_a, host_b)

    def _get_default_host_a(self) -> Dict:
        """获取默认主持人A"""
        return {
            "identity": {"name": "阿明", "archetype": "追问者", "core_drive": "", "chemistry": ""},
            "expression": {"pace": "normal", "sentence_length": "mixed", "signature_phrases": [], "attitude": "skeptical", "voice_id": "zh_male_liufei_uranus_bigtts"},
            "memory_seed": []
        }

    def _get_default_host_b(self) -> Dict:
        """获取默认主持人B"""
        return {
            "identity": {"name": "小北", "archetype": "讲故事的人", "core_drive": "", "chemistry": ""},
            "expression": {"pace": "normal", "sentence_length": "mixed", "signature_phrases": [], "attitude": "curious", "voice_id": "zh_female_vv_uranus_bigtts"},
            "memory_seed": []
        }


def run_setup_wizard(user_id: str = "default") -> bool:
    """便捷函数：运行配置向导"""
    wizard = SetupWizard(user_id)
    return wizard.run()


def ensure_configured(user_id: str = "default", auto_wizard: bool = True) -> bool:
    """
    确保配置已就绪，未配置时自动启动向导

    Args:
        user_id: 用户ID
        auto_wizard: 是否自动启动配置向导

    Returns:
        是否已配置
    """
    loader = ConfigLoader()

    if loader.is_fully_configured():
        # 已配置，加载到环境变量
        loader.load()
        return True

    if auto_wizard:
        print("🔔 检测到首次使用，启动配置向导...")
        print()
        return run_setup_wizard(user_id)

    return False
