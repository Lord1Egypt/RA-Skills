#!/usr/bin/env python3
"""
领域词典管理器
支持：自动领域检测、加载内置词典、合并用户自定义词典、应用术语修正
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ─── 领域检测关键词表 ──────────────────────────────────────────────────────────
DOMAIN_DETECTION_KEYWORDS: Dict[str, List[str]] = {
    "finance": [
        "证券", "股票", "基金", "期货", "期权", "债券", "理财", "资管",
        "量化", "对冲", "衍生品", "融券", "融资", "大宗交易", "定增",
        "IPO", "估值", "净值", "收益率", "回撤", "夏普", "仓位", "持仓",
        "方正证券", "中信证券", "华泰证券", "申万", "招商证券",
        "私募", "公募", "FOF", "MOM", "ETF", "A股", "港股",
        "T+0", "T+1", "融资融券", "大宗", "解禁", "限售",
        "涨停", "跌停", "熔断", "涨幅", "跌幅"
    ],
    "architecture": [
        "设计院", "建筑", "结构", "施工图", "方案", "预算", "造价",
        "CAD", "BIM", "Revit", "暖通", "给排水", "电气", "消防",
        "规划", "容积率", "建筑面积", "地下室", "幕墙", "钢结构",
        "验收", "报规", "审图", "建委", "规划局", "住建"
    ],
    "technology": [
        "API", "接口", "数据库", "后端", "前端", "部署", "服务器",
        "云计算", "大数据", "人工智能", "机器学习", "深度学习",
        "Python", "Java", "JavaScript", "React", "Docker", "Kubernetes",
        "需求", "产品", "迭代", "敏捷", "Sprint", "版本", "上线"
    ],
    "medical": [
        "患者", "诊断", "治疗", "手术", "药物", "临床", "医院",
        "科室", "主任", "住院", "门诊", "影像", "检验", "病例",
        "医保", "药品", "医疗器械", "适应症", "禁忌症", "副作用"
    ],
    "legal": [
        "合同", "法院", "律师", "诉讼", "仲裁", "合规", "监管",
        "条款", "违约", "赔偿", "知识产权", "专利", "商标",
        "法律", "法规", "规定", "条例", "许可证", "资质"
    ]
}

DOMAIN_NAMES: Dict[str, str] = {
    "finance": "金融",
    "architecture": "建筑设计",
    "technology": "科技互联网",
    "medical": "医疗健康",
    "legal": "法律合规",
    "general": "通用"
}


def detect_domain(text: str, threshold: int = 3) -> Tuple[str, Dict[str, int]]:
    """自动检测文本所属领域

    Args:
        text: 待检测文本
        threshold: 最少命中关键词数才确认领域（默认3个）

    Returns:
        (detected_domain, {domain: hit_count})
    """
    text_lower = text.lower()
    scores: Dict[str, int] = {}

    for domain, keywords in DOMAIN_DETECTION_KEYWORDS.items():
        hit_count = sum(1 for kw in keywords if kw.lower() in text_lower)
        scores[domain] = hit_count

    best_domain = max(scores, key=lambda d: scores[d])
    best_score = scores[best_domain]

    if best_score < threshold:
        return "general", scores

    return best_domain, scores


class DomainDictionary:
    """领域词典管理器"""

    def __init__(self, domain: str = "auto", custom_file: Optional[str] = None):
        """
        Args:
            domain: 领域名称（'auto' 则在 apply_corrections 时自动检测）
            custom_file: 用户自定义词典文件路径（JSON 格式，结构同 glossary.json）
        """
        self.domain = domain
        self.custom_file = custom_file
        self._auto_detected = False

        if domain != "auto":
            self.dictionary = self._load_dictionary(domain)
            self._merge_custom(custom_file)
        else:
            self.dictionary = {}  # 延迟加载

    def _load_dictionary(self, domain: str) -> dict:
        """加载领域词典"""
        script_dir = Path(__file__).parent
        dictionary_path = script_dir.parent / "domains" / domain / "glossary.json"

        if not dictionary_path.exists():
            if domain != "general":
                print(f"[INFO] 领域词典不存在: {domain}，使用空词典")
            return {}

        try:
            with open(dictionary_path, "r", encoding="utf-8") as f:
                dictionary = json.load(f)
            print(f"[OK] 已加载领域词典: {dictionary.get('domain_name', domain)}")
            return dictionary
        except Exception as e:
            print(f"[WARN] 加载领域词典失败: {e}")
            return {}

    def _merge_custom(self, custom_file: Optional[str]) -> None:
        """合并用户自定义词典"""
        if not custom_file:
            return
        custom_path = Path(custom_file)
        if not custom_path.exists():
            print(f"[WARN] 自定义词典不存在: {custom_path}")
            return
        try:
            with open(custom_path, "r", encoding="utf-8") as f:
                custom = json.load(f)

            # 合并 corrections
            existing_corrections = {item["wrong"]: item for item in self.dictionary.get("corrections", [])}
            for item in custom.get("corrections", []):
                existing_corrections[item["wrong"]] = item  # 用户优先覆盖
            self.dictionary.setdefault("corrections", [])
            self.dictionary["corrections"] = list(existing_corrections.values())

            # 合并 entities
            for category, items in custom.get("entities", {}).items():
                existing = self.dictionary.setdefault("entities", {}).setdefault(category, [])
                for item in items:
                    if item not in existing:
                        existing.append(item)

            print(f"[OK] 已合并自定义词典: {custom_path.name}"
                  f"（+{len(custom.get('corrections', []))} 修正规则，"
                  f"+{sum(len(v) for v in custom.get('entities', {}).values())} 实体）")
        except Exception as e:
            print(f"[WARN] 自定义词典合并失败: {e}")

    def apply_corrections(self, text: str) -> Tuple[str, List[dict]]:
        """应用术语修正

        Args:
            text: 原始转写文本

        Returns:
            (修正后的文本, 修正报告列表)
        """
        # 如果是 auto 模式，先自动检测领域
        if self.domain == "auto" and not self._auto_detected:
            detected_domain, scores = detect_domain(text)
            self._auto_detected = True
            self.domain = detected_domain
            domain_name = DOMAIN_NAMES.get(detected_domain, detected_domain)
            top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
            score_str = ", ".join(f"{DOMAIN_NAMES.get(d, d)}:{s}" for d, s in top_scores)
            print(f"[AUTO] 自动检测领域: {domain_name}（评分: {score_str}）")

            if detected_domain != "general":
                self.dictionary = self._load_dictionary(detected_domain)
                self._merge_custom(self.custom_file)
            else:
                print("[INFO] 未检测到明确领域，跳过词典修正")
                return text, []

        if not self.dictionary:
            return text, []

        corrections = self.dictionary.get("corrections", [])
        if not corrections:
            return text, []

        corrected_text = text
        correction_report = []

        for item in corrections:
            wrong = item.get("wrong", "")
            right = item.get("right", "")
            confidence = item.get("confidence", 0.5)
            note = item.get("note", "")

            if not wrong or not right:
                continue
            # 跳过自引用（wrong == right 的保留项）
            if wrong == right:
                continue
            # 低置信度跳过
            if confidence < 0.65:
                continue

            pattern = re.compile(re.escape(wrong), re.IGNORECASE)
            matches = pattern.findall(corrected_text)

            if matches:
                corrected_text = pattern.sub(right, corrected_text)
                correction_report.append({
                    "wrong": wrong,
                    "right": right,
                    "count": len(matches),
                    "confidence": confidence,
                    "note": note
                })

        return corrected_text, correction_report

    def get_entities(self) -> Dict[str, List[str]]:
        """获取实体列表"""
        if not self.dictionary:
            return {}
        return self.dictionary.get("entities", {})

    def get_corrections_report(self, correction_report: List[dict]) -> str:
        """生成修正报告文本

        Args:
            correction_report: 修正报告列表

        Returns:
            修正报告文本
        """
        if not correction_report:
            return "无需修正"

        lines = ["术语修正报告："]
        lines.append("-" * 50)

        for item in correction_report:
            lines.append(f"  {item['wrong']} → {item['right']} (出现次数: {item['count']}, 置信度: {item['confidence']})")
            if item.get("note"):
                lines.append(f"    注: {item['note']}")

        lines.append("-" * 50)
        lines.append(f"总计修正: {len(correction_report)} 项")

        return "\n".join(lines)


def main():
    """测试领域词典"""
    # 测试文本
    test_text = """
    客户持有50万日元，希望配置稳健型产品。
    最近光波派股票表现不错，微博也发布了新机。
    少白客群体对收益率要求较低。
    """

    # 加载词典
    dictionary = DomainDictionary("finance")

    # 应用修正
    corrected, report = dictionary.apply_corrections(test_text)

    # 输出结果
    print("原始文本:")
    print(test_text)
    print("\n修正后文本:")
    print(corrected)
    print("\n" + dictionary.get_corrections_report(report))

    # 输出实体列表
    entities = dictionary.get_entities()
    print("\n实体列表:")
    for category, items in entities.items():
        print(f"  {category}: {', '.join(items[:5])}")


if __name__ == "__main__":
    main()
