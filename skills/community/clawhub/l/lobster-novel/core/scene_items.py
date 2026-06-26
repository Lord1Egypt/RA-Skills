#!/usr/bin/env python3
"""
SceneItemVerifier — 写前场景物品校验机制

解决问题：LLM 在写小说时会根据训练数据统计模式自动填充场景物品，
导致出现不符合世界观设定的物品（如海煤、土豆、巧克力等）。

机制：
  Phase 1: 根据章节规划 + Bible，LLM 列举本场景应该出现的物品清单
  Phase 2: 规则引擎 + LLM 交叉验证，剔除不合理的物品
  Phase 3: 将验证后的物品注入 writing prompt，限制 LLM 只使用清单内的物品

用法：
  verifier = SceneItemVerifier(project_dir, api_key)
  items = verifier.verify_chapter(chapter_num, chapter_plan)

  从 pipeline 调用：
  pipeline = Pipeline(project_dir)
  pipeline.verify_scene_items(chapter_num, chapter_plan)
"""

import json, re, os, urllib.request, time, logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('SceneItemVerifier')


# ═══════════════════════════════════════════════════════════════
#  Data Models
# ═══════════════════════════════════════════════════════════════

@dataclass
class SceneItem:
    """A physical item that appears in a scene."""
    name: str
    category: str         # furniture / tool / clothing / food / weapon / container / decor / ...
    location: str         # where in the scene (e.g., "酒馆吧台", "角色身上")
    reason: str           # why this item fits here
    verified: bool = False
    warning: str = ""

    def to_prompt(self) -> str:
        return f"- {self.name}（{self.category}，位于{self.location}）"


@dataclass
class SceneItemChecklist:
    """Complete verified item checklist for one chapter."""
    chapter: int
    scenes: List[str]              # scene names
    items: List[SceneItem]         # verified items (pass Phase 2)
    rejected: List[str]            # items rejected during Phase 2 (with reason)
    warnings: List[str]            # flagged inconsistencies
    verified_at: str = ""

    def prompt_injection(self) -> str:
        lines = [
            "## 本章场景物品清单（已校验）",
            "写作时只能使用以下物品，不要自行添加不属于本世界的物品：",
            "",
        ]
        for item in self.items:
            lines.append(item.to_prompt())
        if self.rejected:
            lines += ["", "### 以下物品已被排除："]
            for r in self.rejected:
                lines.append(f"- ❌ {r}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  World Compatibility Rules
# ═══════════════════════════════════════════════════════════════

# 这些规则从 Bible 中自动提取 + 硬编码的常识规则
HARD_RULES = {
    "no_industrial": [
        "煤", "煤炭", "燃煤", "煤矿", "发电机", "电灯", "电线",
        "蒸汽机", "锅炉", "铁轨", "火车", "汽车", "引擎",
    ],
    "no_new_world_crops": [
        "土豆", "马铃薯", "番茄", "西红柿", "玉米", "烟草",
        "辣椒", "咖啡", "可可", "巧克力", "南瓜", "向日葵",
    ],
    "no_anachronism": [
        "手机", "电话", "电脑", "电视", "塑料", "尼龙",
        "手枪", "步枪", "子弹", "炸药", "TNT",
    ],
    # 注：fishing village 应有的物品不用放在禁止列表里
    # LLM Phase 1 自然会给渔村场景生成渔网/鱼叉等合理物品
    # 禁止列表只放确实不该出现的
}

# 每个类别的例子列表（用于校验合理性）
CATEGORY_EXAMPLES = {
    "酒馆场景": [
        "木桌", "长凳", "吧台", "木杯", "陶杯", "麦酒",
        "油灯", "蜡烛", "壁炉", "木柴", "火钳",
        "抹布", "木桶", "酒瓶", "鲁特琴", "骰子",
    ],
    "普通人家": [
        "木床", "草垫", "毛毯", "陶碗", "木勺",
        "炊锅", "火塘", "柴堆", "水缸",
    ],
    "码头/渔村": [
        "渔网", "缆绳", "船桨", "鱼筐", "海藻",
        "海漂木", "贝壳", "盐", "咸鱼",
    ],
    "佣兵/冒险者": [
        "长剑", "匕首", "皮甲", "背包", "水袋",
        "磨刀石", "火种盒", "绷带",
    ],
}


# ═══════════════════════════════════════════════════════════════
#  Main Verifier
# ═══════════════════════════════════════════════════════════════

class SceneItemVerifier:
    """写前场景物品校验器。"""

    def __init__(self, project_dir: Path, api_key: str = ""):
        self.dir = Path(project_dir)
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")

        # Load Bible
        bible_file = self.dir / "bible.json"
        if bible_file.exists():
            self.bible = json.loads(bible_file.read_text(encoding="utf-8"))
        else:
            self.bible = {}
            logger.warning("bible.json not found, using empty bible")

        # Extract world rules
        self.world_rules = {}
        for rule in self.bible.get("world_rules", []):
            self.world_rules[rule["name"]] = rule["description"]

        # Build local rules from Bible + hard-coded
        self.local_rules = self._build_local_rules()

    def _build_local_rules(self) -> Dict[str, str]:
        rules = {
            "world_setting": self.world_rules.get("自建世界观：泰伦大陆", "fantasy midieval"),
            "location_detail": self.world_rules.get("灰港镇设定", "fishing village"),
        }
        # Extract tech level / economy indicators
        setting_text = json.dumps(self.bible, ensure_ascii=False).lower()
        if any(k in setting_text for k in ["渔村", "偏僻", "小镇", "渔港"]):
            rules["economy"] = "poor_fishing_village"
        if any(k in setting_text for k in ["帝国", "首都", "贸易"]):
            rules["economy"] = "urban_trading"
        return rules

    # ── Phase 1: LLM generates scene items ────────────────────

    def _llm_chat(self, messages: list, temp: float = 0.5, max_tokens: int = 2048) -> str:
        """Call LLM API."""
        payload = json.dumps({
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temp,
            "max_tokens": max_tokens,
        }).encode("utf-8")
        for attempt in range(3):
            try:
                req = urllib.request.Request(
                    "https://api.deepseek.com/v1/chat/completions", data=payload,
                    headers={"Content-Type": "application/json",
                             "Authorization": f"Bearer {self.api_key}"})
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.warning(f"LLM call failed (attempt {attempt+1}): {e}")
                if attempt < 2:
                    time.sleep(2 ** attempt)
        raise RuntimeError("LLM call failed after 3 retries")

    def _extract_json(self, text: str) -> dict:
        """Extract JSON from LLM response."""
        clean = re.sub(r'```(?:json)?\s*', '', text)
        clean = re.sub(r'\s*```', '', clean)
        start = clean.find('{')
        end = clean.rfind('}')
        if start >= 0 and end > start:
            clean = clean[start:end+1]
        return json.loads(clean)

    def _phase1_generate_items(self, chapter_summary: str, location: str,
                                character_focus: List[str]) -> List[SceneItem]:
        """Phase 1: LLM generates plausible scene items."""
        # Build Bible context
        world_text = json.dumps(self.world_rules, ensure_ascii=False, indent=2)
        char_text = json.dumps({
            k: v for k, v in self.bible.get("characters", {}).items()
            if k in character_focus or not character_focus
        }, ensure_ascii=False, indent=2)

        system_prompt = (
            "你是 DND 5e 奇幻世界的场景道具设计师。\n"
            "你的任务是根据场景描述，列出该场景中合情合理的物理物品。\n"
            "标准：只包含这个经济水平、技术水平和地理环境下会出现的物品。\n"
            "原则：偏僻渔村不应该有内地工业品，穷人不该有奢侈品。"
        )

        user_prompt = f"""请列出以下场景中会出现的所有物理物品（家具/工具/衣物/食物/武器/容器/装饰品等）。

## 世界观设定
{world_text}

## 场景信息
- 概要：{chapter_summary}
- 地点：{location}
- 登场角色：{', '.join(character_focus) if character_focus else '未指定'}

## 经济水平判断
{self.local_rules.get('economy', 'unknown')}

输出JSON格式：
{{
  "items": [
    {{
      "name": "物品名称",
      "category": "家具/工具/衣物/食物/武器/容器/装饰/其他",
      "location": "物品在场景中的位置",
      "reason": "为什么这个物品出现在这里（结合设定的解释）"
    }}
  ],
  "notes": "对场景物品设计的补充说明"
}}

要求：
1. 只列出物理物品，不包括抽象概念
2. 数量8-15个，选最有代表性的
3. 符合渔村/小镇的经济水平（穷、物资匮乏、以渔业为主）
4. 物品来源说明：本地制造/外地运入/渔民自己做的
5. ⚠️ 注意：这个设定里没有煤炭工业，取暖烧的是海漂木和海藻
"""

        response = self._llm_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])

        try:
            data = self._extract_json(response)
            items = []
            for it in data.get("items", []):
                items.append(SceneItem(
                    name=it["name"],
                    category=it.get("category", "其他"),
                    location=it.get("location", "场景中"),
                    reason=it.get("reason", ""),
                ))
            return items
        except Exception as e:
            logger.error(f"Phase 1 JSON parse failed: {e}")
            logger.debug(f"Raw: {response[:500]}")
            return []

    # ── Phase 2: Rule-based consistency check ────────────────

    def _phase2_check_items(self, items: List[SceneItem]) -> List[SceneItem]:
        """Phase 2: Rule-based consistency check against hard rules + world rules."""
        economy = self.local_rules.get("economy", "")
        location_detail = self.local_rules.get("location_detail", "")

        verified_items = []
        rejected = []

        for item in items:
            reasons = []

            # Rule 1: Check hard NO list（整词匹配，避免子串误杀）
            item_words = set(re.split(r'[\/，、（）()\s/]', item.name))
            for category, forbidden in HARD_RULES.items():
                for word in forbidden:
                    if word in item_words:
                        reasons.append(f"触犯规则[{category}]：'{word}' 不在本世界科技/农业水平内")
                        break

            # Rule 2: Economy-level check
            if economy == "poor_fishing_village":
                # 穷渔村不应该有昂贵或难以获取的物品
                expensive_keywords = ["丝绸", "天鹅绒", "银器", "金杯", "水晶",
                                      "象牙", "大理石", "油画", "挂毯",
                                      "精金", "秘银", "魔法"]
                for kw in expensive_keywords:
                    if kw in item.name:
                        reasons.append(f"经济不匹配：'{kw}' 是奢侈品，偏僻渔村不可能有")

            # Rule 3: Tech level check
            if "蒸汽" in item.name or "机械" in item.name:
                reasons.append(f"技术不匹配：本世界没有蒸汽工业")

            if reasons:
                rejected.append(f"{item.name}（{'；'.join(reasons)}）")
                item.verified = False
                item.warning = "; ".join(reasons)
            else:
                item.verified = True
                verified_items.append(item)

        return verified_items, rejected

    # ── Phase 3: Inject into prompt ──────────────────────────

    def format_prompt_injection(self, checklist: SceneItemChecklist) -> str:
        """Format verified items as prompt injection block."""
        return checklist.prompt_injection()

    # ── Full Pipeline ────────────────────────────────────────

    def verify_chapter(self, chapter_num: int,
                       chapter_plan: dict,
                       location: str = "",
                       character_focus: List[str] = None) -> SceneItemChecklist:
        """Run full verification pipeline for one chapter."""
        summary = chapter_plan.get("summary", str(chapter_plan))
        loc = location or chapter_plan.get("location", "未指定")
        chars = character_focus or chapter_plan.get("character_focus", [])

        logger.info(f"🔍 校验第{chapter_num}章场景物品...")

        # Phase 1
        items = self._phase1_generate_items(summary, loc, chars)
        if not items:
            logger.warning(f"Phase 1 未生成物品，跳过校验")
            return SceneItemChecklist(
                chapter=chapter_num,
                scenes=[loc],
                items=[],
                rejected=[],
                warnings=["Phase 1 物品生成失败"],
                verified_at=datetime.now().isoformat(),
            )

        logger.info(f"   Phase 1: {len(items)} 个候选物品")

        # Phase 2
        verified, rejected = self._phase2_check_items(items)

        # Build warnings for rejected items
        warnings = []
        if rejected:
            warnings.append(f"排除 {len(rejected)} 个不合理物品：{'、'.join(rejected)}")

        result = SceneItemChecklist(
            chapter=chapter_num,
            scenes=[loc],
            items=verified,
            rejected=rejected,
            warnings=warnings,
            verified_at=datetime.now().isoformat(),
        )

        summary_line = f"   Phase 2: {len(verified)} 个通过 | {len(rejected)} 个被排除"
        if rejected:
            summary_line += f"\n   ❌ 排除: {'、'.join(rejected)}"
        logger.info(summary_line)

        return result

    def verify_from_file(self, plan_path: Path, chapter_num: int) -> SceneItemChecklist:
        """Verify items for a chapter given the volume plan JSON."""
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        for ch in plan.get("chapters", []):
            if ch["number"] == chapter_num:
                return self.verify_chapter(chapter_num, ch)
        raise ValueError(f"Chapter {chapter_num} not found in {plan_path}")

    def inject_into_prompt(self, chapter_num: int,
                           chapter_plan: dict,
                           original_prompt: str) -> str:
        """Run verification and inject results into the writing prompt."""
        checklist = self.verify_chapter(chapter_num, chapter_plan)
        injection = self.format_prompt_injection(checklist)

        # Insert before the "请写出完整小说正文" line
        marker = "请写出完整"
        if marker in original_prompt:
            modified = original_prompt.replace(marker, f"\n{injection}\n\n{marker}", 1)
        else:
            modified = original_prompt + "\n\n" + injection

        return modified, checklist


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scene item verifier for lobster-novel")
    parser.add_argument("chapter", type=int, help="Chapter number to verify")
    parser.add_argument("--project", default=str(Path(__file__).resolve().parent.parent),
                        help="Project directory")
    parser.add_argument("--plan", default="plans/volume_01_plan.json",
                        help="Volume plan JSON file (relative to project)")
    args = parser.parse_args()

    project_dir = Path(args.project)
    verifier = SceneItemVerifier(project_dir)
    plan_path = project_dir / args.plan

    checklist = verifier.verify_from_file(plan_path, args.chapter)

    print("\n" + "=" * 60)
    print(f"✅ 第{args.chapter}章物品校验完成")
    print("=" * 60)
    print(f"\n通过物品 ({len(checklist.items)}个):")
    for item in checklist.items:
        print(f"  ✅ {item.name}（{item.category}，位于{item.location}）")
    if checklist.rejected:
        print(f"\n❌ 被排除:")
        for r in checklist.rejected:
            print(f"  ❌ {r}")
    print(f"\n📊 校验注入 Prompt 块:")
    print(checklist.prompt_injection())
