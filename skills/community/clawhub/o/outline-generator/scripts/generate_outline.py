#!/usr/bin/env python3
"""生成小说 15 节拍结构化大纲 - Optimized Version"""

import argparse
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.table import Table
    from rich.text import Text
except ImportError as e:
    print(
        f"错误: 缺少依赖库 {e.name}, 请运行: pip install pyyaml rich", file=sys.stderr
    )
    sys.exit(1)


VALID_TYPES: List[str] = ["玄幻", "都市", "科幻", "历史"]
CONFIG_DIR: Path = Path(__file__).parent.parent / "configs"
CONFIG_FILE: Path = CONFIG_DIR / "types.yml"

console = Console()


class OutlineGenerator:
    """小说大纲生成器 - 优化版本"""

    BEAT_ATOMS = [
        "力量",
        "力量体系",
        "解开真相",
        "组织",
        "秘境",
        "奇特现象",
        "关键技能",
        "阴谋",
        "独特手段",
        "更高境界",
        "系统",
        "秘法",
        "危机",
        "机遇",
        "盟友",
        "背叛",
        "救赎",
        "命运",
        "选择",
        "代价",
    ]

    BEAT_TEMPLATES = {
        "玄幻": [
            ("力量体系", "修炼突破", "境界提升", "秘境探索", "古老传承"),
            ("宗门争斗", "天材地宝", "远古遗迹", "丹药器灵", "妖兽血魄"),
        ],
        "都市": [
            ("商业竞争", "人脉关系", "神秘组织", "隐藏身份", " propel 事件"),
            ("家族秘辛", "商业帝国", "权谋斗争", "科技革新", "娱乐圈风波"),
        ],
        "科幻": [
            ("星际坐标", "人工智能", "文明冲突", "时间悖论", "维度旅行"),
            ("基因进化", "外星科技", "宇宙真相", "意识上传", "机械义体"),
        ],
        "历史": [
            ("权谋斗争", "历史变革", "名将登场", "王朝兴衰", "文化碰撞"),
            ("宫廷秘辛", "民间义士", "外交策略", "军事谋略", "经济改革"),
        ],
    }

    BEAT_DESCRIPTIONS = [
        "描写主角在{type_name}世界中的初始状态，建立基调和氛围，暗示主角的独特之处或潜在矛盾。",
        "通过配角的对话或内心独白，含蓄表达本作的主题思想。",
        "某种超自然现象或重大事件预告改变即将到来。",
        "重大事件发生，彻底改变主角的人生轨迹。",
        "主角明确自己想要达成的目标，这是推动整个故事的驱动力。",
        "主角进入新的世界或规则体系，开始适应和学习。",
        "主角在新环境中探索、学习，完成一系列小挑战。",
        "获得关键盟友、装备或知识，为下一阶段做准备。",
        "主角面临第一次真正的、严肃的考验。",
        "遇到关键的导师或盟友，形成重要合作关系。",
        "遭遇主要对手或敌对势力，冲突升级。",
        "故事中点的高潮战斗/事件，虚假的胜利或真实的失败。",
        "最黑暗的时刻，主角失去一切或陷入绝境。",
        "重生时刻，获得新的力量、认知或盟友。",
        "与最终 BOSS 的决战，解决所有核心矛盾。",
        "回到开场画面的场景，但已不同，展现主角的转变。",
    ]

    def __init__(
        self, type_name: str, theme: str, word_count: int, config: Dict[str, Any]
    ) -> None:
        """初始化生成器

        Args:
            type_name: 小说类型
            theme: 主题描述
            word_count: 目标字数
            config: 类型配置
        """
        self.type_name = type_name
        self.theme = theme
        self.word_count = word_count
        self.config = config
        self.start_time = time.time()
        self.stats: Dict[str, Any] = {}

    def _select_keywords(self, count: int = 6) -> List[str]:
        """随机选择关键词

        Args:
            count: 需要选择的关键词数量

        Returns:
            随机选择的关键词列表
        """
        available = self.BEAT_ATOMS.copy()
        random.shuffle(available)
        selected = available[:count]

        type_specific = self.BEAT_TEMPLATES.get(self.type_name, ([], []))
        if type_specific and random.random() > 0.5:
            category = random.choice(type_specific)
            if len(category) >= count:
                selected = list(category)[:count]

        return selected

    def _calculate_structure(self) -> Dict[str, int]:
        """计算卷数和章数结构

        Returns:
            包含卷数、总章数、每卷章数的字典
        """
        try:
            min_vol = self.config.get("min_volumes", 2)
            max_vol = self.config.get("max_volumes", 4)
            min_chapter_words = self.config.get("min_chapter_words", 2500)
            max_chapter_words = self.config.get("max_chapter_words", 3500)
            min_chapters_per_vol = self.config.get("min_chapters_per_vol", 20)
            max_chapters_per_vol = self.config.get("max_chapters_per_vol", 30)

            avg_chapter_words = (min_chapter_words + max_chapter_words) / 2

            total_chapters = max(1, int(self.word_count / avg_chapter_words))

            volumes = random.randint(min_vol, max_vol)
            chapters_per_vol = max(
                min_chapters_per_vol,
                min(max_chapters_per_vol, max(1, total_chapters // volumes)),
            )

            actual_total = chapters_per_vol * volumes

            return {
                "volumes": volumes,
                "total_chapters": actual_total,
                "chapters_per_vol": chapters_per_vol,
                "avg_chapter_words": int(avg_chapter_words),
                "word_count_deviation": self.word_count
                - actual_total * int(avg_chapter_words),
            }
        except (TypeError, ZeroDivisionError) as e:
            console.print(f"[red]错误: 结构计算失败 - {e}[/red]")
            return {
                "volumes": 2,
                "total_chapters": 100,
                "chapters_per_vol": 50,
                "avg_chapter_words": 3000,
                "word_count_deviation": 0,
            }

    def _get_beat_words(self, beat_index: int) -> int:
        """计算每个节拍的字数

        Args:
            beat_index: 节拍索引 (0-14)

        Returns:
            该节拍应分配的字数
        """
        ratios = [
            0.01,  # 1. 开场画面
            0.01,  # 2. 主题呈现
            0.02,  # 3. 预示
            0.04,  # 4. 催化剂
            0.04,  # 5. 确定目标
            0.06,  # 6. 上路
            0.08,  # 7. 探索
            0.06,  # 8. 约会
            0.08,  # 9. 考验
            0.06,  # 10. 伙伴
            0.08,  # 11. 敌人
            0.12,  # 12. 战斗（中点高潮）
            0.08,  # 13. 低谷
            0.06,  # 14. 高地
            0.12,  # 15. 终极战斗
        ]

        if beat_index == 15:  # 结局画面
            return int(self.word_count * 0.01)

        if 0 <= beat_index < len(ratios):
            return int(self.word_count * ratios[beat_index])

        return 0

    def _generate_beat_content(
        self, beat_index: int, keywords: List[str], structure: Dict[str, int]
    ) -> str:
        """生成单个节拍的内容

        Args:
            beat_index: 节拍索引 (0-15)
            keywords: 关键词列表
            structure: 结构信息

        Returns:
            节拍内容字符串
        """
        beat_num = beat_index + 1
        words = self._get_beat_words(beat_index)
        kw = keywords[beat_index % min(len(keywords), 6)]

        theme_context = self.theme[:30] + "..." if len(self.theme) > 30 else self.theme

        if beat_index == 0:
            return f"""### {beat_num}. 开场画面 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[0].format(type_name=self.type_name)}

> 主角在{self.type_name}世界的日常场景，通过细节展现世界规则和主角的特殊之处。
> 一个平静的早晨/夜晚/战斗场景，暗示即将到来的变故。
> {theme_context}的主题初步显露。
"""
        elif beat_index == 1:
            return f"""### {beat_num}. 主题呈现 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[1]}

> 通过重要配角的对话或内心独白，含蓄表达本作核心主题。
> "真正的{kw}来自于内心的坚持" - 主要配角谈及某件往事时说道。
> 这句话将在结局时被主角重新理解和践行。
"""
        elif beat_index == 2:
            return f"""### {beat_num}. 预示 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[2]}

> 天空出现异象（雷暴、极光、星辰异动）或主角获得神秘物品产生共鸣。
> 世界法则出现细微波动，预示大变将至。
> 主角首次感受到自己与世界的特殊联系。
"""
        elif beat_index == 3:
            return f"""### {beat_num}. 催化剂 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[3]}

> 突发事件彻底改变主角人生轨迹：意外穿越/继承遗产/被卷入阴谋/获得奇遇。
> 首次接触{self.type_name}世界的核心规则或{kw}体系。
> 旧世界崩塌，新世界大门开启。
"""
        elif beat_index == 4:
            return f"""### {beat_num}. 确定目标 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[4]}

> "我一定要{kw}!" - 主角立下坚定决心。
> 初步制定行动计划，寻找第一位导师或盟友。
> 获得第一桶关键资源（丹药、功法、情报）。
"""
        elif beat_index == 5:
            return f"""### {beat_num}. 上路 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[5]}

> 进入{self.type_name}的新世界，遭遇规则冲击和文化碰撞。
> 首次尝试使用新力量/知识，经历失败但学到宝贵经验。
> 结识第一批同门/伙伴，建立初步信任。
"""
        elif beat_index == 6:
            return f"""### {beat_num}. 探索 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[6]}

> 在新环境中探索，完成一系列小挑战，逐步适应。
> 尝试用{self.type_name}特有的方式解决问题，取得初步成功。
> 发现{kw}现象，开始思考其背后的深层真相。
> 结识第一位重要盟友，建立生死之交。
"""
        elif beat_index == 7:
            return f"""### {beat_num}. 约会 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[7]}

> 获得导师/长辈的认可，得到核心资源或重要信息。
> 学习/掌握{kw}，实力得到质的飞跃。
> 装备升级/获得ByKey Item，为下一阶段做准备。
"""
        elif beat_index == 8:
            return f"""### {beat_num}. 考验 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[8]}

> 参加大比/闯关/完成任务，遭遇强大对手的严峻考验。
> 绝境中爆发，利用{self.type_name}特有的智慧或技能奇迹取胜。
> 获得重要奖励/Easter Egg，为未来埋下关键伏笔。
"""
        elif beat_index == 9:
            return f"""### {beat_num}. 伙伴 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[9]}

> 结识亦师亦友的关键伙伴，双方能力完美互补。
> 共同制定下一步计划，明确团队分工和目标。
> 建立稳固的伙伴关系，Mutual respect 基础。
"""
        elif beat_index == 10:
            return f"""### {beat_num}. 敌人 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[10]}

> 对手首次展现强大实力，给主角造成重大挫折。
> 揭露对手的{kw}计划，紧张感急剧升级。
> 主角势力与敌对势力正式交锋，全面战争爆发。
"""
        elif beat_index == 11:
            return f"""### {beat_num}. 战斗（中点高潮）({words:,} 字)
> {self.BEAT_DESCRIPTIONS[11]}

> 绝境反击，利用独特{kw}逆转看似不可能的局势。
> 表面胜利，实则付出惨重代价（盟友牺牲/重要资源丢失/被误导）。
> 阶段性目标达成，但揭示这只是更大阴谋的冰山一角。
> 世界格局剧变，真正的挑战才刚刚开始。
"""
        elif beat_index == 12:
            return f"""### {beat_num}. 低谷 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[12]}

> 盟友背叛/牺牲/重伤，主角陷入自我怀疑和自我否定。
> 敌人全面压制，失去重要能力/资源/盟友。
> 意识到自己一直被误导，或低估了对手的真实实力。
> 世界陷入最黑暗的时刻，希望仿佛破灭。
"""
        elif beat_index == 13:
            return f"""### {beat_num}. 高地 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[13]}

> 在废墟中顿悟，理解{kw}的真正含义。
> 获得关键助力（神秘人物现身/古老遗物觉醒/隐藏实力爆发）。
> 重新审视局势，制定全新的复仇/救赎/救世计划。
> 地位/实力/认知全面跃升，准备最终反击。
"""
        elif beat_index == 14:
            return f"""### {beat_num}. 终极战斗 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[14]}

> 与最终 BOSS 的全面决战，决战不仅是力量，更是{self.type_name}理念的终极碰撞。
> 主角用完整的{kw}体系或超凡智慧击败对手。
> 前期所有伏笔在此刻回收，形成完美的叙事闭环。
> 世界法则重塑，新的纪元开启。
"""
        else:
            return f"""### {beat_num}. 结局画面 ({words:,} 字)
> {self.BEAT_DESCRIPTIONS[15]}

> 回到开场画面的场景，但一切已不同，展现主角的脱胎换骨。
> 与开场形成镜像对比，观众能清晰看到主角的成长弧光。
> 暗示新的开始或续集线索（可选），留下余韵。
"""

    def _generate_role_arcs(self, structure: Dict[str, int]) -> str:
        """生成角色弧光表格

        Args:
            structure: 结构信息

        Returns:
            角色弧光 Markdown 表格
        """
        protagonist_start = self.config.get("protagonist_start", "平凡/迷茫/弱小")
        protagonist_end = self.config.get("protagonist_end", "强大/明悟/领袖")
        ally_start = self.config.get("ally_start", "陌生/怀疑")
        ally_end = self.config.get("ally_end", "生死之交/左膀右臂")
        enemy_start = self.config.get("enemy_start", "强大/神秘")
        enemy_end = self.config.get("enemy_end", "落败/顿悟/死亡")

        return f"""## 角色弧光

| 角色 | 起始状态 | 转折点 | 最终状态 |
|------|----------|--------|----------|
| 主角 | {protagonist_start} | 催化剂事件（第4节拍） | {protagonist_end} |
| 主要盟友 | {ally_start} | 考验阶段（第9节拍） | {ally_end} |
| 对手 | {enemy_start} | 中点高潮（第12节拍） | {enemy_end} |
"""

    def _generate_worldbuilding(self, keywords: List[str]) -> str:
        """生成世界观设定

        Args:
            keywords: 关键词列表

        Returns:
            世界观设定 Markdown 内容
        """
        power_system = self.config.get("power_system", "多层级修炼体系")
        core_conflict = self.config.get("core_conflict", "个人成长 vs 世界规则")
        location_1 = self.config.get("location_1", "主角起点")
        location_2 = self.config.get("location_2", "重要事件发生地")
        location_3 = self.config.get("location_3", "最终决战地")
        ranks = self.config.get("ranks", "根据类型设定")
        growth_method = self.config.get("growth_method", "实战修炼/资源积累/机缘顿悟")
        restrictions = self.config.get("restrictions", "资源不足/境界瓶颈/天道压制")

        keywords_preview = ", ".join(keywords[:5]) if keywords else "无特殊要素"

        return f"""## 世界观设定

### {self.type_name}世界核心规则

1. **力量体系**: {power_system}
2. **核心冲突**: {core_conflict}
3. **关键地点**: 
   - {location_1} - 故事起点
   - {location_2} - 重要转折
   - {location_3} - 最终决战
4. **独特要素**: {keywords_preview}

### 力量体系（简略）

- **阶段划分**: {ranks}
- **成长方式**: {growth_method}
- **限制条件**: {restrictions}
"""

    def _generate_foreshadowing(self) -> str:
        """生成关键伏笔

        Returns:
            伏笔列表 Markdown 内容
        """
        return """## 关键伏笔

1. **玉佩/古籍**: 第3节拍获得，第14节拍揭示真实身份/起源
2. **神秘势力**: 第11节拍出现，第15节拍揭示与主角的渊源
3. **配角的遗言**: 第13节拍，暗示更大的真相
4. **奇特现象**: 第2节拍预示，第14节拍解密
5. **盟友的警告**: 第10节拍，后期成为关键线索
"""

    def _generate_writing_tips(self) -> str:
        """生成写作建议

        Returns:
            写作建议 Markdown 内容
        """
        return """## 写作建议

- **节奏把控**: 前 3 节拍快速建立世界观，中段保持张力，结局高潮迭起
- **伏笔回收**: 重要道具/台词/人物在后续关键节点回收
- **节奏变化**: 每 3-5 章安排一个小高潮，每 10-15 章安排一个大高潮
- **字数分配**: 按节拍标注的字数比例控制，确保重点突出
- **人物塑造**: 每个重要角色至少展现2-3次成长变化
"""

    def generate(self) -> str:
        """生成完整大纲

        Returns:
            完整大纲 Markdown 字符串
        """
        keywords = self._select_keywords(10)
        structure = self._calculate_structure()

        metadata = f"""# 小说大纲

**书名**: [待定]
**类型**: {self.type_name}
**主题**: {self.theme}
**目标字数**: {self.word_count:,} 字
**预计卷数**: {structure["volumes"]} 卷
**预计总章数**: {structure["total_chapters"]} 章
**平均每章字数**: {structure["avg_chapter_words"]} 字
**字数偏差**: {structure["word_count_deviation"]:+,} 字

---

## 节拍结构（15节拍）
"""

        beats_content = ""
        for i in range(15):
            beats_content += self._generate_beat_content(i, keywords, structure)

        outline = f"""{metadata}

{beats_content}
---
"""

        outline += self._generate_role_arcs(structure)
        outline += "\n---\n\n"
        outline += self._generate_worldbuilding(keywords)
        outline += "\n---\n\n"
        outline += self._generate_foreshadowing()
        outline += "\n---\n\n"
        outline += self._generate_writing_tips()

        outline += "\n---\n\n"
        outline += f"*大纲生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*  \n"
        outline += "*版本: v6.0 (Optimized with Rich)*"

        self.stats = {
            "keywords_used": keywords,
            "structure": structure,
            "total_beats": 15,
            "calculation_time": time.time() - self.start_time,
        }

        return outline

    def get_statistics(self) -> Dict[str, Any]:
        """获取生成统计信息

        Returns:
            统计信息字典
        """
        return self.stats


def load_config() -> Dict[str, Any]:
    """加载配置文件

    Returns:
        配置字典

    Raises:
        SystemExit: 配置文件加载失败
    """
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        console.print(f"[red]错误: 配置文件不存在[/red] → [blue]{CONFIG_FILE}[/blue]")
        sys.exit(1)
    except yaml.YAMLError as e:
        console.print(f"[red]错误: 配置文件格式错误[/red] → [yellow]{e}[/yellow]")
        sys.exit(1)
    except PermissionError:
        console.print("[red]错误: 无权限读取配置文件[/red]")
        sys.exit(1)


def validate_args(args: argparse.Namespace) -> None:
    """验证命令行参数

    Args:
        args: 解析后的参数对象

    Raises:
        SystemExit: 验证失败
    """
    errors = []

    if args.type not in VALID_TYPES:
        errors.append(f"无效的类型 '{args.type}'，可选: {', '.join(VALID_TYPES)}")

    if args.word_count <= 0:
        errors.append("字数必须是正整数")

    if not args.output.lower().endswith(".md"):
        errors.append("输出文件必须是 .md 格式")

    if errors:
        for error in errors:
            console.print(f"[red]错误: {error}[/red]")
        sys.exit(1)


def create_output_directories(output_path: str) -> Path:
    """创建输出目录

    Args:
        output_path: 输出文件路径

    Returns:
        输出目录 Path 对象

    Raises:
        SystemExit: 创建失败
    """
    try:
        path = Path(output_path)
        if path.parent and str(path.parent) != ".":
            path.parent.mkdir(parents=True, exist_ok=True)
        return path
    except OSError as e:
        console.print(f"[red]错误: 无法创建输出目录[/red] → [yellow]{e}[/yellow]")
        sys.exit(1)


def save_outline(content: str, output_path: Path) -> bool:
    """保存大纲文件

    Args:
        content: 大纲内容
        output_path: 输出路径

    Returns:
        保存是否成功
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError as e:
        console.print(
            f"[red]错误: 无法写入文件 {output_path}[/red] → [yellow]{e}[/yellow]"
        )
        return False


def display_final_stats(stats: Dict[str, Any]) -> None:
    """显示生成统计信息

    Args:
        stats: 统计信息字典
    """
    stats_table = Table(title="📈 生成统计", show_header=True, header_style="bold cyan")
    stats_table.add_column("指标", style="magenta")
    stats_table.add_column("数值", style="green")

    structure = stats.get("structure", {})

    stats_table.add_row("计算耗时", f"{stats.get('calculation_time', 0):.3f} 秒")
    stats_table.add_row(
        "类型",
        stats.get("keywords_used", ["未知"])[0]
        if stats.get("keywords_used")
        else "未知",
    )
    stats_table.add_row("卷数", str(structure.get("volumes", 0)))
    stats_table.add_row("总章数", str(structure.get("total_chapters", 0)))
    stats_table.add_row("平均章长", f"{structure.get('avg_chapter_words', 0):,} 字")

    console.print(stats_table)


def display_success_panel(output_path: Path, outline: str) -> None:
    """显示成功面板

    Args:
        output_path: 输出路径
        outline: 大纲内容（用于预览）
    """
    preview = outline[:500] + "..." if len(outline) > 500 else outline

    console.print(
        Panel(
            Markdown(preview),
            title="[green]✅ 大纲生成成功[/green]",
            border_style="green",
            subtitle=f"📄 {output_path}",
            width=80,
        )
    )


def print_header() -> None:
    """打印程序标题"""
    console.print("\n")
    console.print(
        Panel(
            Text.from_markup(
                "[bold cyan]📖 小说大纲生成器 v6.0[/bold cyan]\n"
                "[dim]基于 15 节拍结构的智能大纲生成[/dim]"
            ),
            border_style="bold cyan",
        )
    )
    console.print("\n")


def main() -> None:
    """主函数"""
    print_header()

    parser = argparse.ArgumentParser(
        description="生成小说 15 节拍结构化大纲 - Optimized Version"
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=VALID_TYPES,
        help=f"小说类型: {', '.join(VALID_TYPES)}",
    )
    parser.add_argument("--theme", required=True, help="小说主题描述")
    parser.add_argument(
        "--word-count", type=int, required=True, help="目标字数（正整数）"
    )
    parser.add_argument("--output", required=True, help="输出文件路径（.md 格式）")
    parser.add_argument("--show-preview", action="store_true", help="预览生成内容")

    args = parser.parse_args()

    console.print("[yellow]正在加载配置...[/yellow]")
    config = load_config()

    console.print("[yellow]正在验证参数...[/yellow]")
    validate_args(args)

    console.print("[yellow]正在生成大纲...[/yellow]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Generating outline...", total=1.0)

        generator = OutlineGenerator(
            args.type, args.theme, args.word_count, config.get(args.type, {})
        )
        outline = generator.generate()

        progress.update(task, advance=1.0)

    output_path = create_output_directories(args.output)

    console.print("[yellow]正在保存文件...[/yellow]")
    if save_outline(outline, output_path):
        console.print(f"[green]✓ 大纲已保存到[/green] → [blue]{output_path}[/blue]")

        if args.show_preview:
            display_success_panel(output_path, outline)

        stats = generator.get_statistics()
        display_final_stats(stats)

        console.print(f"\n[green]字符总数: {len(outline):,}[/green]")
        console.print(f"[green]目标字数: {args.word_count:,}[/green]")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
