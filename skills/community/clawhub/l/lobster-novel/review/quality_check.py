#!/usr/bin/env python3
"""
lobster-novel: quality review system

6 角色评审:
  Reader         - 阅读体验（开篇/节奏/画面感/钩子）
  Editor         - 技术质量（语法/风格/一致性/AI味）
  Storyteller    - 剧情逻辑（连续性/角色/伏笔）
  爽点分析师     - 网文节奏（爽点密度/情绪曲线/期待感）
  人物声线校验  - 角色一致性（对话风格/声线匹配）
  网文编辑      - 商业化视角（开篇钩子/付费点/章节末悬念）

Severity: P0 (must fix) / P1 (recommend) / P2 (optional)
"""
import json, re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple

# 确保 review 目录可导入同级模块
_review_dir = Path(__file__).parent
if str(_review_dir) not in __import__('sys').path:
    __import__('sys').path.insert(0, str(_review_dir))

# ═══════════════════════════════════════════════════════════════
#  AI味检测模式库（与 aigc_detect.py 同步扩展）
# ═══════════════════════════════════════════════════════════════

AIGC_PATTERNS = {
    "tell_not_show": [
        r"他明白[了]?", r"她明白[了]?", r"他懂[了]?", r"她懂[了]?",
        r"他意识到", r"她意识到",
        r"他感到", r"她感到",
        r"内心充满", r"心中涌起",
        r"他仿佛", r"她仿佛",
    ],
    "empty_emotion": [
        r"感到.*(悲伤|高兴|愤怒|开心|难过|孤独|恐惧)",
        r"内心.*(平静|波澜|挣扎|复杂)",
        r"一种.*的.*感[觉受]",
    ],
    "god_view": [
        r"所有人[都]?没想到",
        r"就在这时",
        r"只见",
        r"突然",
        r"原来如此",
        r"就这样",
    ],
    "template_phrase": [
        r"众所周知",
        r"不言而喻",
        r"不得不承认",
        r"真是太",
        r"多么.*啊",
        r"真是.*啊",
    ],
    "over_explain": [
        r"这.*意味着",
        r"换句话说",
        r"也就是[说]?",
        r"其实[就]?是",
    ],
    # ── 中文网文特有AI味 ──────────────────────────────────────
    "cliched_expression": [
        r"眼中闪过一丝",
        r"嘴角扬起一抹",
        r"心中一凛",
        r"眉头微皱",
        r"瞳孔一缩",
        r"脸色一变",
        r"冷笑一声",
        r"轻哼一声",
        r"冷哼一声",
        r"嘴角勾起一抹",
        r"眼中寒光一闪",
        r"心中暗道",
        r"心中大喜",
        r"心中一喜",
        r"心中一沉",
        r"心中一震",
        r"心头一紧",
        r"心底泛起",
    ],
    "dialogue_ai_tell": [
        r"说道[\u201c\u201c]([^\u201d\u201c]{5,})[\u201d\u201d]",
        r"淡淡道",
        r"冷冷道",
        r"淡淡一笑",
        r"微微一笑",
        r"冷笑道",
        r"轻声道",
        r"沉声道",
        r"厉声道",
        r"语气中带着",
        r"声音中带着一丝",
        r"语气冰冷",
        r"语气平淡",
        r"语气中透着",
    ],
    "pacing_issues": [
        r"接下来[，,]",
        r"然后[，,]",
        r"随后[，,]",
        r"就这样[，,]",
        r"过了[一二三四五六七八九十]+[天日]",
        r"转眼间[，,]",
        r"不知不觉[，,]",
    ],
    "shuangdian_density": [
        r"打脸",
        r"碾压",
        r"秒杀",
        r"震惊",
        r"目瞪口呆",
        r"不可思议",
        r"难以置信",
        r"全场哗然",
        r"一片哗然",
        r"众人皆惊",
    ],
}


@dataclass
class Issue:
    role: str         # 6角色之一
    severity: str     # P0 / P1 / P2
    category: str
    description: str
    line: int = 0
    suggestion: str = ""


@dataclass
class ReviewReport:
    chapter: int
    issues: List[Issue] = field(default_factory=list)
    scores: Dict[str, int] = field(default_factory=dict)
    passed: bool = False

    def to_text(self) -> str:
        lines = [f"# Chapter {self.chapter} Review Report\n"]
        if self.scores:
            lines.append("## 评分")
            for role, score in self.scores.items():
                lines.append(f"- {role}: {score}/100")
            lines.append("")

        p0 = [i for i in self.issues if i.severity == "P0"]
        p1 = [i for i in self.issues if i.severity == "P1"]
        p2 = [i for i in self.issues if i.severity == "P2"]

        if p0:
            lines.append(f"## P0（必须修）— {len(p0)}")
            for i in p0:
                lines.append(f"- [{i.role}] {i.description} (行~{i.line})")
                if i.suggestion:
                    lines.append(f"  修: {i.suggestion}")
            lines.append("")
        if p1:
            lines.append(f"## P1（建议修）— {len(p1)}")
            for i in p1:
                lines.append(f"- [{i.role}] {i.description}")
                if i.suggestion:
                    lines.append(f"  修: {i.suggestion}")
            lines.append("")
        if p2:
            lines.append(f"## P2（可选）— {len(p2)}")
            for i in p2:
                lines.append(f"- [{i.role}] {i.description}")
            lines.append("")

        if self.passed:
            lines.append("**结果: PASS** ✅")
        else:
            lines.append(f"**结果: FAIL** (P0: {len(p0)}) ❌")

        return "\n".join(lines)

    def to_json(self) -> str:
        return json.dumps({
            "chapter": self.chapter,
            "issues": [asdict(i) for i in self.issues],
            "scores": self.scores,
            "passed": self.passed,
        }, ensure_ascii=False, indent=2)


class QualityChecker:
    """静态质量检查（不含LLM）。6角色多维度快速扫描"""

    # ── 公用辅助 ──────────────────────────────────────────────
    # ── 角色 1: Reader（阅读体验）─────────────────────────────
    @staticmethod
    def _check_reader(text: str, lines: list, chinese_chars: int) -> List[Issue]:
        issues = []

        paragraphs = [p for p in text.split("\n\n") if p.strip()]

        # 章节末钩子检查（智能检测）
        if paragraphs:
            last = paragraphs[-1]
            # 显式钩子关键词
            explicit_hooks = ["?", "？", "!", "！", "突然", "竟然", "究竟", "什么"]
            # 文学性钩子（叙事收束但留有悬念）
            literary_hooks = ["还没有结束", "在等他", "在等待", "还没有", "未完",
                             "开始了", "不会结束", "批.*完", "第.*个.*到",
                             "继续前行", "下一站", "通往", "入口",
                             "方向", "标记", "坐标", "信号",
                             "还没", "还有", "不是结束", "只是开始",
                             "没有消失", "还在路上"]
            has_hook = any(i in last for i in explicit_hooks + ["?", "？"])
            has_literary_hook = any(re.search(p, last) for p in literary_hooks)
            is_end_marker = bool(re.search(r"-{3,}|批\d·完|完\n|^#.*完", last))

            if not has_hook and not has_literary_hook and not is_end_marker:
                issues.append(Issue(
                    role="Reader",
                    severity="P2",
                    category="缺钩子",
                    description="章节末尾缺悬念/钩子",
                    suggestion="章节末留一个问句、意外或未解线索",
                ))

        # 开篇钩子检查（前三段）
        if len(paragraphs) >= 3:
            opening = "".join(paragraphs[:3])
            opening_hooks = ["?", "？", "!", "！", "突然", "竟然", "奇怪", "什么"]
            if not any(i in opening for i in opening_hooks):
                issues.append(Issue(
                    role="Reader",
                    severity="P2",
                    category="开篇平淡",
                    description="前三段缺少悬念/冲突钩子",
                    suggestion="开篇用一个问句、冲突或新鲜事抓读者",
                ))

        # 字数检查
        if chinese_chars < 1000:
            issues.append(Issue(
                role="Reader",
                severity="P0",
                category="章节过短",
                description=f"仅{chinese_chars}中文字，目标2000+",
            ))
        elif chinese_chars > 5000:
            issues.append(Issue(
                role="Reader",
                severity="P2",
                category="章节过长",
                description=f"{chinese_chars}中文字，建议拆分",
            ))

        return issues

    # ── 角色 2: Editor（技术质量）─────────────────────────────
    @staticmethod
    def _check_editor(text: str, lines: list, chinese_chars: int) -> List[Issue]:
        issues = []

        # AI味模式扫描
        for cat, patterns in AIGC_PATTERNS.items():
            for pat in patterns:
                for m in re.finditer(pat, text):
                    ln = text[:m.start()].count("\n") + 1
                    severity = "P0" if cat == "template_phrase" else "P1"
                    suggestions = {
                        "tell_not_show": "用动作/表情代替直接说感受",
                        "cliched_expression": "换更自然的表达方式",
                        "dialogue_ai_tell": "让对话更口语化，去掉多余描写",
                        "pacing_issues": "用具体时间或事件转折代替模糊过渡",
                    }
                    suggestion = suggestions.get(cat, "用动作/细节代替抽象叙述")
                    issues.append(Issue(
                        role="Editor",
                        severity=severity,
                        category=f"AI味: {cat}",
                        description=f"'{m.group()[:30]}'",
                        line=ln,
                        suggestion=suggestion,
                    ))

        # 对话量
        dialog_lines = len(re.findall(r'[\u201c\u201c\u300c\u300e]([^\u201d\u201d\u300d\u300f]{5,})[\u201d\u201d\u300d\u300f]', text))
        if dialog_lines < 3 and chinese_chars > 1000:
            issues.append(Issue(
                role="Editor",
                severity="P1",
                category="对话不足",
                description=f"本章仅{dialog_lines}句对话",
                suggestion="考虑加个对话场景，调节叙事节奏",
            ))

        # 排版问题（中文排版规范）
        fullwidth_marks = len(re.findall(r'[，。！？；：、]', text))
        halfwidth_marks = len(re.findall(r'[,\.!?;:]', text))
        if halfwidth_marks > fullwidth_marks and chinese_chars > 500:
            issues.append(Issue(
                role="Editor",
                severity="P2",
                category="标点规范",
                description="中文应使用全角标点",
                suggestion="检查逗号句号是否为半角",
            ))

        return issues

    # ── 角色 3: Storyteller（剧情逻辑）─────────────────────────
    @staticmethod
    def _check_storyteller(text: str, lines: list) -> List[Issue]:
        issues = []

        # 人称一致性
        names_third = len(re.findall(r'[他她它]', text))
        names_first = len(re.findall(r'我', text))
        if names_third > 10 and names_first > 10:
            ratio = names_first / max(names_third, 1)
            if 0.3 < ratio < 3:
                issues.append(Issue(
                    role="Storyteller",
                    severity="P1",
                    category="人称混用",
                    description=f"第一人称'我'({names_first})与第三人称'他/她'({names_third})混用",
                    suggestion="统一叙事视角，一章内不要频繁切换人称",
                ))

        # 时间跳跃
        time_jumps = re.findall(r'(过了[一二三四五六七八九十百千]+[天日星期月年]|转眼|一晃|不知不觉)', text)
        if len(time_jumps) > 2:
            issues.append(Issue(
                role="Storyteller",
                severity="P1",
                category="时间跳跃频繁",
                description=f"本章出现{len(time_jumps)}次时间跳跃",
                suggestion="减少模糊时间过渡，用具体事件衔接",
            ))

        return issues

    # ── 角色 4: 爽点分析师（网文节奏）─────────────────────────
    @staticmethod
    def _check_shuangdian_analyst(text: str, lines: list, chinese_chars: int) -> List[Issue]:
        """网文节奏分析：爽点密度、情绪曲线、期待感管理"""
        issues = []

        # 爽点词频
        shuangdian_words = [
            "竟然", "没想到", "怎么可能", "不可思议", "震惊", "目瞪口呆",
            "秒杀", "碾压", "打脸", "全场哗然", "一片哗然", "众人皆惊",
            "突破", "觉醒", "爆发", "逆转", "翻盘", "反杀",
            "提升", "进阶", "收获", "获得", "奖励", "宝物",
            "终于", "总算", "这一刻",
        ]
        sd_count = sum(text.count(w) for w in shuangdian_words)
        paragraphs = [p for p in text.split("\n\n") if p.strip()]

        if chinese_chars > 1000:
            expected_sd = max(1, chinese_chars // 1000)
            if sd_count < expected_sd:
                issues.append(Issue(
                    role="爽点分析师",
                    severity="P1",
                    category="爽点不足",
                    description=f"本章{len(paragraphs)}段约{chinese_chars}字，仅{sd_count}个爽点关键词，期待{expected_sd}+",
                    suggestion="每千字至少1个爽点/转折，加个意外、打脸或收获",
                ))

        # 情绪曲线：检测章节中段是否有低谷/转折
        if len(paragraphs) >= 4:
            mid_start = len(paragraphs) // 3
            mid_end = 2 * len(paragraphs) // 3
            mid_text = "".join(paragraphs[mid_start:mid_end])
            tension_words = ["但", "然而", "却", "没想到", "突然", "危险", "危机", "困难", "挑战", "敌人"]
            tension_count = sum(mid_text.count(w) for w in tension_words)
            if tension_count < 3:
                issues.append(Issue(
                    role="爽点分析师",
                    severity="P2",
                    category="情绪平淡",
                    description="章节中段缺少情绪起伏（转折/冲突/危险）",
                    suggestion="在中段加一个小冲突或转折，制造情绪曲线",
                ))

        # 爽点的节奏分布（集中在前/中/后？）
        if paragraphs and sd_count >= 2:
            # 检查爽点是否均匀分布
            pass  # 高级分析：每段的爽点密度分布

        return issues

    # ── 角色 5: 人物声线校验───────────────────────────────────
    @staticmethod
    def _check_character_voice(text: str, lines: list) -> List[Issue]:
        """对话声线一致性检测（基础版）"""
        issues = []

        # 提取所有对话（引号内的内容）
        dialogs = re.findall(r'[\u201c\u201c\u300c]([^\u201d\u201d\u300d]{3,})[\u201d\u201d\u300d]', text)
        if len(dialogs) < 3:
            return issues

        # 检测对话长度分布（所有角色说话长度是否趋同）
        # AI生成的对话常常所有角色说差不多长度的句子
        dialog_lengths = [len(d) for d in dialogs]
        if dialog_lengths:
            avg_len = sum(dialog_lengths) / len(dialog_lengths)
            max_len = max(dialog_lengths)
            min_len = min(dialog_lengths)
            range_ratio = (max_len - min_len) / max(avg_len, 1)

            if range_ratio < 0.5 and len(dialogs) >= 5:
                issues.append(Issue(
                    role="人物声线校验",
                    severity="P1",
                    category="声线趋同",
                    description="所有角色对话长度相似，缺少声线差异化",
                    suggestion="不同角色的说话应有长短差异：主角多几句，配角简洁，反派有特色",
                ))

        # 检测AI味对话开头
        ai_dialog_leadins = ["说实话", "坦白说", "老实说", "换言之", "也就是说", "不得不承认"]
        for w in ai_dialog_leadins:
            count = text.count(w)
            if count > 0:
                issues.append(Issue(
                    role="人物声线校验",
                    severity="P2",
                    category=f"对话开头AI味",
                    description=f"对话中出现'{w}'共{count}次",
                    suggestion="真人说话不会总用总结性开场",
                ))

        return issues

    # ── 角色 6: 网文编辑（商业化视角）───────────────────────────
    @staticmethod
    def _check_webnovel_editor(text: str, lines: list, chinese_chars: int) -> List[Issue]:
        """商业化视角质量检查"""
        issues = []

        paragraphs = [p for p in text.split("\n\n") if p.strip()]

        # 开篇吸引力（前三段必须有冲突/悬念/新信息）
        if len(paragraphs) >= 3:
            opening = paragraphs[0] + paragraphs[1] + paragraphs[2]
            open_hooks = ["?", "？", "!", "！", "突然", "竟然", "怎么回事", "怎么回事?",
                          "什么", "该死", "糟了", "不好", "小心"]
            if not any(h in opening for h in open_hooks):
                issues.append(Issue(
                    role="网文编辑",
                    severity="P1",
                    category="开篇吸引力不足",
                    description="前三段缺乏钩子，读者可能划走",
                    suggestion="开篇3段内必须制造一个悬念/冲突/新信息，抓眼球",
                ))

        # 章节末付费点
        if paragraphs:
            last_para = paragraphs[-1]
            payoff_signals = ["?", "？", "!", "！", "下一章", "接下来", "等待", "究竟",
                              "到底是什么", "怎么回事", "要来了", "来了"]
            if not any(s in last_para for s in payoff_signals):
                issues.append(Issue(
                    role="网文编辑",
                    severity="P1",
                    category="付费点弱",
                    description="章节末悬念不够强烈，影响追读率",
                    suggestion="章节末用问句或预告制造'必看下一章'的冲动",
                ))

        # 高潮位置
        if chinese_chars > 1500 and len(paragraphs) >= 5:
            # 高潮应出现在章节70%-90%处
            climax_region_start = int(len(paragraphs) * 0.7)
            climax_text = "".join(paragraphs[climax_region_start:])
            climax_keywords = ["终于", "突然", "竟然", "!", "！", "爆发", "逆转", "这一刻"]
            if not any(k in climax_text for k in climax_keywords):
                issues.append(Issue(
                    role="网文编辑",
                    severity="P2",
                    category="高潮位置欠佳",
                    description="章节后30%缺少高潮/爆点",
                    suggestion="高潮应放在章节70-90%位置，然后留悬念收尾",
                ))

        return issues

    # ── 角色 7: 角色检查（配角密度/利用率）─────────────────────
    @staticmethod
    def _check_character_usage(text: str, lines: list, chinese_chars: int,
                                roster_path: Optional[Path] = None,
                                current_chapter: int = 0) -> List[Issue]:
        """调用 CharacterRoster 做配角质量检查"""
        issues = []
        if not roster_path or not roster_path.exists():
            return issues
        try:
            from memory.character_roster import CharacterRoster
            roster = CharacterRoster(roster_path)
            raw_issues = roster.quality_issues(max(current_chapter, 0))
            for r in raw_issues:
                sev = r.get("severity", "P1")
                issues.append(Issue(
                    role=r.get("role", "角色检查"),
                    severity=sev,
                    category=r.get("category", "角色问题"),
                    description=r.get("desc", ""),
                    suggestion=r.get("suggest", ""),
                ))
        except ImportError:
            pass
        except Exception as e:
            issues.append(Issue(
                role="角色检查", severity="P2",
                category="角色读取异常",
                description=f"读取角色名册失败: {e}",
            ))
        return issues

    # ── 主入口 ────────────────────────────────────────────────
    @staticmethod
    def check_text(text: str, chapter: int,
                   project_dir: Optional[Path] = None) -> ReviewReport:
        """
        6角色+角色检查 静态评审
        project_dir: 小说项目目录（传了就有角色检查）
        """
        lines = text.split("\n")
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])

        all_issues = []
        all_issues += QualityChecker._check_reader(text, lines, chinese_chars)
        all_issues += QualityChecker._check_editor(text, lines, chinese_chars)
        all_issues += QualityChecker._check_storyteller(text, lines)
        all_issues += QualityChecker._check_shuangdian_analyst(text, lines, chinese_chars)
        all_issues += QualityChecker._check_character_voice(text, lines)
        all_issues += QualityChecker._check_webnovel_editor(text, lines, chinese_chars)
        # 角色检查（如果提供了项目路径）
        if project_dir:
            # 同时检查 continuity/ 和根目录下的角色档案
            roster_paths = [project_dir / "continuity", project_dir]
            for rp in roster_paths:
                if rp.exists() and (rp / "character_roster.json").exists():
                    roster_path = rp
                    break
            else:
                roster_path = project_dir / "continuity"
            all_issues += QualityChecker._check_character_usage(
                text, lines, chinese_chars, project_dir, chapter)
            # Strand 节奏检查（从 story-state.json 读取）
            state_path = project_dir / "story-state.json"
            strand_score = 100  # 默认值，try 成功时覆盖
            if state_path.exists():
                try:
                    # 方法内 import 避免循环导入：strand_balance 依赖 quality_check 的 Issue/ReviewReport
                    from strand_balance import StrandAnalyzer
                    analyzer = StrandAnalyzer()
                    strand_report = analyzer.analyze_from_file(state_path, chapter)
                    all_issues += strand_report.issues
                    if strand_report.scores:
                        strand_score = strand_report.scores.get("Strand分析师", 0)
                except Exception as e:
                    all_issues.append(Issue(
                        role="Strand分析师", severity="P2",
                        category="Strand分析异常",
                        description=f"读取 story-state.json 失败: {e}",
                    ))

        # 汇总评分
        p0_count = sum(1 for i in all_issues if i.severity == "P0")
        p1_count = sum(1 for i in all_issues if i.severity == "P1")
        p2_count = sum(1 for i in all_issues if i.severity == "P2")
        base = 100
        penalty = p0_count * 15 + p1_count * 5 + p2_count * 2
        overall = max(base - penalty, 0)

        scores = {
            "Reader": max(100 - sum(1 for i in all_issues if i.role == "Reader" and i.severity == "P0") * 20, 0),
            "Editor": max(100 - sum(1 for i in all_issues if i.role == "Editor") * 5, 0),
            "Storyteller": max(100 - sum(1 for i in all_issues if i.role == "Storyteller") * 10, 0),
            "爽点分析师": max(100 - sum(1 for i in all_issues if i.role == "爽点分析师") * 15, 0),
            "人物声线校验": max(100 - sum(1 for i in all_issues if i.role == "人物声线校验") * 15, 0),
            "网文编辑": max(100 - sum(1 for i in all_issues if i.role == "网文编辑") * 10, 0),
            "Strand分析师": strand_score if project_dir and (project_dir / "story-state.json").exists() else None,
            "综合": overall,
        }
        # 移除 None 值
        scores = {k: v for k, v in scores.items() if v is not None}

        return ReviewReport(
            chapter=chapter,
            issues=all_issues,
            scores=scores,
            passed=p0_count == 0,
        )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="lobster-novel 6角色质量检查")
    parser.add_argument("file", help="章节文件路径")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    report = QualityChecker.check_text(text, 0)
    if args.json:
        print(report.to_json())
    else:
        print(report.to_text())
