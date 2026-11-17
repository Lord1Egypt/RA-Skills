#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
one-novel-skill 模拟仿真引擎

读者模拟 + 编辑审核 + 弃坑预测 + 完本评估。
算法驱动，不依赖 LLM 判断。
"""

import math


class SimulationEngine:
    """读者/编辑/运营仿真器"""


    def analyze(self, text, **kwargs):
        """读者模拟分析"""
        issues = []
        chapter = kwargs.get("ch", 0)
        if text:
            result = self.simulate_reader(chapter, text)
            eng = result.get("engagement", 0)
            if eng < 0.5:
                issues.append(f"[模拟] 读者参与度 {eng:.2f} 偏低，建议优化段落节奏或对话密度")
            tns = result.get("tension", 0)
            if tns < 0.3:
                issues.append(f"[模拟] 紧张度 {tns:.2f} 偏低，建议增加冲突或悬念")
        return issues

    @staticmethod
    def simulate_reader(chapter_num: int, text: str, previous_engagement: float = 1.0) -> dict:
        """模拟单个读者的阅读反应"""
        wc = len(text)
        # 字数区间评分（最优 2000-3000 字）
        word_score = 1.0
        if wc < 1500:
            word_score = 0.4
        elif wc < 2000:
            word_score = 0.8
        elif wc > 4000:
            word_score = 0.6
        elif wc > 3000:
            word_score = 0.9

        # 段落节奏评分
        paras = [p for p in text.split('\n') if p.strip()]
        para_lens = [len(p) for p in paras]
        avg_para = sum(para_lens) / max(len(para_lens), 1)

        para_score = 1.0
        if avg_para > 200:
            para_score = 0.6  # 段落太长
        elif avg_para < 30:
            para_score = 0.8  # 太碎

        # 对话密度评分（只计左引号，避免 ASCII " 同时计左右）
        quote_count = text.count("\u201c") + text.count("\u2018") + text.count("\u300c")
        dialog_ratio = quote_count / max(wc, 1)
        dialog_score = 1.0
        if dialog_ratio < 0.02:
            dialog_score = 0.5  # 对话太少
        elif dialog_ratio > 0.5:
            dialog_score = 0.7  # 对话太多

        # 综合参与度
        engagement = previous_engagement * (word_score * 0.4 + para_score * 0.3 + dialog_score * 0.3)

        # 读者情绪推断
        tension = 0.5
        interest = 0.6
        if '?' in text[:500]:  # 开头有问号 = 设悬念
            tension += 0.2
            interest += 0.15
        if '！' in text:  # 感叹 = 情绪高点
            tension += 0.1

        return {
            "chapter": chapter_num,
            "engagement": round(engagement, 3),
            "tension": round(min(1.0, tension), 2),
            "interest": round(min(1.0, interest), 2),
            "word_score": round(word_score, 2),
            "para_score": round(para_score, 2),
            "dialog_score": round(dialog_score, 2),
            "would_continue": engagement > 0.5,
        }

    @staticmethod
    def simulate_editor(text: str, genre: str = "都市", platform: str = "番茄") -> dict:
        """模拟编辑审核"""
        wc = len(text)

        # 字数检查
        issues = []
        if wc < 1500:
            issues.append("字数不足，建议增至2000+")
        elif wc > 4000:
            issues.append("字数超标，建议压缩至3000以内")

        # 开头强度
        opening = text[:300]
        if not any(c in opening for c in ["?", "？", "！", "!", "\u201c"]):
            issues.append("开头300字缺少钩子（无问号/感叹号/对话）")

        # 结尾强度（已移除句号误判）

        # 总体评分
        score = 85  # 基准
        score -= len(issues) * 5
        score = max(0, min(100, score))

        return {
            "score": score,
            "passed": score >= 60,
            "issues": issues,
            "grade": "S" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C",
        }

    @staticmethod
    def predict_retention(chapters_analyzed: list, total_planned: int) -> dict:
        """根据参考数据中的弃书点模型预测留存"""
        if not chapters_analyzed:
            return {"预测弃坑章节": 0, "二刷概率": 0, "留存曲线": [], "风险区间": []}

        engagement_values = [c.get("engagement", 0.5) for c in chapters_analyzed]
        avg_engagement = sum(engagement_values) / max(len(engagement_values), 1)

        # 参考数据：高风险弃书区间
        risk_zones = [(1, 3, "开篇弃书"), (15, 20, "首次倦怠"), (50, 60, "中期疲软")]
        active_risks = []
        for start, end, label in risk_zones:
            if end <= total_planned:
                # 检查该区间是否有章节已分析
                zone_chapters = [c for c in chapters_analyzed if start <= c.get("chapter", 0) <= end]
                if zone_chapters:
                    zone_avg = sum(c.get("engagement", 0.5) for c in zone_chapters) / len(zone_chapters)
                    if zone_avg < 0.5:
                        active_risks.append({"区间": f"第{start}-{end}章", "原因": label, "平均参与度": round(zone_avg, 3)})

        # 留存曲线：参考数据模型
        decay = 0.95 + (0.01 * max(0, avg_engagement - 0.6))  # 高参与度=低衰减
        retention = [decay ** i * avg_engagement for i in range(total_planned)]

        # P2-5 FIX: Python `or` 短路求值误用，改为 set 合并
        RISK_CHAPTERS = {1, 2, 3, 15, 16, 17, 18, 19, 20, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60}
        predicted_drop = total_planned
        for i, r in enumerate(retention):
            if (i + 1) in RISK_CHAPTERS:
                r *= 0.85  # 高风险区间额外折损
            if r < 0.3:
                predicted_drop = i + 1
                break

        # 二刷概率
        reread_prob = min(1.0, max(0.0, (avg_engagement * 0.6 + 0.2)))

        return {
            "预测弃坑章节": predicted_drop,
            "风险区间": active_risks,
            "二刷概率": round(reread_prob, 2),
            "平均参与度": round(avg_engagement, 3),
            "留存曲线": [round(r, 3) for r in retention[:50]],
        }

    @staticmethod
    def full_report(state, chapters_data: list, total_planned: int) -> str:
        """[UTILITY] 生成完整的模拟运营报告 — 有实代码但未在管线中自动调用"""
        retention = SimulationEngine.predict_retention(chapters_data, total_planned)
        avg_eng = sum(c.get("engagement", 0) for c in chapters_data) / max(len(chapters_data), 1)
        avg_score = sum(c.get("score", 80) for c in chapters_data) / max(len(chapters_data), 1) if chapters_data else 0

        lines = []
        lines.append("【模拟运营报告】")
        lines.append(f"  已写: {len(chapters_data)}章 / 计划: {total_planned}章")
        lines.append(f"  平均参与度: {avg_eng:.1%}")
        lines.append(f"  平均编辑评分: {avg_score:.0f}/100")
        lines.append(f"  预测最大留存: {retention['预测弃坑章节']}章")
        lines.append(f"  估算二刷概率: {retention['二刷概率']:.0%}")
        risk_chapters = retention.get('风险区间', [])
        if risk_chapters:
            lines.append(f"  风险章节: {risk_chapters}")
        else:
            lines.append(f"  风险章节: 暂无")
        lines.append("")
        lines.append("【弃坑预警】")
        if retention['预测弃坑章节'] < total_planned:
            lines.append(f"  ⚠️ 预计在第{retention['预测弃坑章节']}章左右出现弃坑高峰")
            lines.append(f"     建议在第{max(1,retention['预测弃坑章节']-5)}章附近安排高潮")
        else:
            lines.append("  ✅ 全本留存预测良好")

        lines.append("")
        lines.append("【完本建议】")
        if chapters_data and chapters_data[-1].get("engagement", 0) < 0.4:
            lines.append("  ⚠️ 近期章节参与度下滑，建议加速收束支线")
        else:
            lines.append("  ✅ 参与度稳定，按原计划推进")
        return "\n".join(lines)



