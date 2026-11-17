#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具引擎合集 — 合并4个小引擎: digital/learning/statistics/data
合并 digital.py / statistics.py / engines_learning.py 消除重复类
"""

import json
import math
import re
from pathlib import Path


# ============ DigitalEngine ============

class DigitalEngine:
    """数字引擎 — 数值计算与转换 + 平台适配"""

    def __init__(self):
        pass

    def analyze(self, text, **kwargs):
        """文本分析 — 平台字数合规检查"""
        issues = []
        platform = kwargs.get("platform", "")
        if platform in ("起点", "晋江"):
            wc = len(text) if text else 0
            if wc < 2000:
                issues.append(f"[数字] 平台{platform}建议单章≥2000字，当前{wc}字")
        return issues

    def available(self):
        return True

    @staticmethod
    def metrics(data):
        if not data:
            return {}
        if isinstance(data, dict):
            values = [v for v in data.values() if isinstance(v, (int, float))]
            if not values:
                return {"total_items": len(data)}
            return {"total": len(data), "sum": round(sum(values), 2),
                    "mean": round(sum(values)/len(values), 2),
                    "max": round(max(values), 2), "min": round(min(values), 2)}
        if isinstance(data, (list, tuple)):
            values = [v for v in data if isinstance(v, (int, float))]
            return {"count": len(values), "sum": round(sum(values), 2),
                    "mean": round(sum(values)/len(values), 2)} if values else {"count": len(data)}
        return {"value": data}

    @staticmethod
    def normalize(values):
        if not values:
            return []
        mx, mn = max(values), min(values)
        span = mx - mn
        if span == 0:
            return [0.5] * len(values)
        return [round((v - mn) / span, 4) for v in values]

    @staticmethod
    def encode(text):
        if not text:
            return []
        chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        sents = len([s for s in re.split(r"[。！？]", text) if s.strip()])
        paras = len([p for p in text.split("\n") if p.strip()])
        return [chars, sents, max(1, paras), round(chars/max(sents,1),1), round(chars/max(paras,1),1)]

    @staticmethod
    def moving_average(values, window=5):
        if len(values) < window:
            return [round(sum(values)/len(values), 2)] * len(values)
        result = []
        for i in range(len(values) - window + 1):
            result.append(round(sum(values[i:i+window])/window, 2))
        return result


# ============ LearningEngine ============

class LearningEngine:
    """学习引擎 — AI模式检测 + 经验积累与优化"""

    def __init__(self):
        self.history = []
        self.patterns = {}
        self._lessons = []

    def analyze(self, text, **kwargs):
        """本章质量分析：匹配已知问题同类型+记录新问题"""
        if not text or len(text) < 50:
            return []
        issues = []
        from datetime import datetime as _dt
        if self._lessons:
            for lesson in self._lessons[-20:]:
                if lesson["issue"][:10] in text or lesson["fix"][:10] in text:
                    issues.append(f"[learn] 已知问题模式: {lesson['issue'][:30]} (来源: {lesson['source']})")
        patterns = {
            "P0禁用词": ["毋庸置疑", "不可否认", "值得一提的是", "命运的齿轮"],
            "情绪直接告知": ["感到", "觉得", "认为", "知道"],
            "结尾泛化": ["总而言之", "综上所述", "更大的挑战还在后面"],
        }
        for ptype, keywords in patterns.items():
            hits = [(kw, text.count(kw)) for kw in keywords if text.count(kw) > 0]
            if hits:
                top3 = "; ".join(f"'{w}'x{c}" for w, c in sorted(hits, key=lambda x: -x[1])[:3])
                issues.append(f"[learn/{ptype}] {top3}")
        if issues:
            for iss in issues[:3]:
                self.record_lesson(iss, "auto-detect", "analyze")
        return issues

    def record_lesson(self, issue: str, fix: str, source: str = ""):
        """记录一条修复教训"""
        from datetime import datetime as _dt
        self._lessons.append({
            "ts": _dt.now().isoformat(),
            "issue": issue, "fix": fix, "source": source
        })

    def get_similar_issues(self, new_issue: str) -> list:
        """查找相似历史问题"""
        return [l for l in self._lessons if l["issue"][:20] in new_issue or new_issue[:20] in l["issue"]][:3]

    def to_dict(self):
        return {"lessons": self._lessons, "patterns": self.patterns, "history": self.history}

    def available(self):
        return True

    def record(self, action, result):
        self.history.append({"action": action, "result": result})
        passed = result.get("passed", False) if isinstance(result, dict) else bool(result)
        key = action[:10]
        if key not in self.patterns:
            self.patterns[key] = {"total": 0, "passed": 0, "scores": []}
        self.patterns[key]["total"] += 1
        if passed:
            self.patterns[key]["passed"] += 1
        if isinstance(result, dict) and "score" in result:
            self.patterns[key]["scores"].append(result["score"])

    def best_practices(self):
        tips = []
        for action, stats in self.patterns.items():
            if stats["total"] >= 3:
                rate = stats["passed"] / stats["total"]
                avg_s = sum(stats["scores"]) / max(len(stats["scores"]), 1) if stats["scores"] else 0
                tips.append({"action": action, "pass_rate": rate, "avg_score": avg_s,
                             "verdict": "稳定" if rate >= 0.8 else "需调整"})
        return tips or [{"action": "无数据", "pass_rate": 0, "avg_score": 0, "verdict": "需积累"}]

    def improve(self):
        improvements = []
        for action, stats in self.patterns.items():
            if stats["total"] >= 3 and stats["passed"] / stats["total"] < 0.5:
                improvements.append(action + "通过率低 - 建议调整")
        return improvements or ["无优化建议"]

    def analyze_trend(self):
        all_scores = []
        for s in self.patterns.values():
            all_scores.extend(s.get("scores", []))
        if len(all_scores) < 3:
            return {"trend": "样本不足", "samples": len(all_scores)}
        recent = sum(all_scores[-3:]) / 3
        early = sum(all_scores[:3]) / 3
        diff = recent - early
        return {"trend": "上升" if diff > 5 else "下降" if diff < -5 else "稳定"}


# ============ StatisticsEngine ============

class StatisticsEngine:
    """统计引擎 — 分布/百分位/基线匹配 + 文本统计分析"""

    def __init__(self):
        pass

    def analyze(self, text, **kwargs):
        """文本统计分析 — 句长/字数检查"""
        issues = []
        if not text:
            return issues
        wc = len(text)
        try:
            import re as _re
            sentences = [s for s in _re.split(r'[。！？.!?]', text) if s.strip()]
            avg_sent_len = sum(len(s) for s in sentences) / max(len(sentences), 1)
            if avg_sent_len > 40:
                issues.append(f"[统计] 平均句长{avg_sent_len:.0f}字，超过常规上限40字，建议拆分长句")
        except Exception:
            pass
        if wc < 500:
            issues.append(f"[统计] 单章{wc}字偏短，建议至少1500字")
        return issues

    def available(self):
        return True

    @staticmethod
    def distribution(values):
        if not values:
            return {"mean": 0, "std": 0, "min": 0, "max": 0, "p5": 0, "p95": 0}
        sv = sorted(values)
        n = len(sv)
        mean = sum(sv) / n
        var = sum((x - mean) ** 2 for x in sv) / n
        return {
            "mean": round(mean, 2),
            "std": round(math.sqrt(var), 2),
            "min": round(sv[0], 2),
            "max": round(sv[-1], 2),
            "p5": round(sv[int(n * 0.05)], 2),
            "p95": round(sv[int(n * 0.95)], 2),
        }

    @staticmethod
    def percentile(values, p):
        sv = sorted(values)
        if not sv:
            return 0
        return sv[int(len(sv) * p / 100)]

    @staticmethod
    def match_baseline(values, baseline):
        """将数据与基线对比，返回偏差"""
        dist = StatisticsEngine.distribution(values)
        issues = []
        for key in ["mean", "std", "p5", "p95"]:
            if key in baseline and key in dist:
                diff = abs(dist[key] - baseline[key])
                threshold = baseline.get(key, 0)
                if threshold == 0:
                    threshold = 0.01
                if diff > threshold * 0.3:
                    issues.append(f"{key}偏差{diff:.1f}")
        return issues


# ============ DataEngine ============

class DataEngine:
    """小说数据管理

    安全说明: load() 默认限制在 book_dir 目录内，
    防止路径遍历攻击。如果明确需要读外部文件，
    请传 allowed_prefix 参数覆盖默认白名单。
    """

    def __init__(self, allowed_prefix=None):
        """
        Args:
            allowed_prefix: 路径白名单前缀。默认为 None 表示不限制（不推荐）。
                            构造函数中传入会在所有 load() 调用中作为默认白名单。
        """
        self._default_prefix = allowed_prefix

    def load(self, path, allowed_prefix=None):
        p = Path(path)
        # 使用实例级默认白名单，除非显式覆盖
        prefix = allowed_prefix if allowed_prefix is not None else self._default_prefix
        if prefix is not None:
            try:
                p.relative_to(Path(prefix))
            except ValueError:
                print(f"  [WARN] DataEngine.load: 路径 {path} 不在允许前缀 {prefix} 内")
                return {}
        if p.exists() and p.is_file():
            return json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        return {}

    def merge(self, sources):
        result = {}
        for src in sources:
            if isinstance(src, dict):
                result.update(src)
        return result

    def query(self, dataset, condition):
        if not isinstance(dataset, dict):
            return []
        key = condition.get("key", "")
        val = condition.get("value", "")
        if key in dataset:
            data = dataset[key]
            if isinstance(data, list):
                return [d for d in data if isinstance(d, dict) and any(val == v for v in d.values())]
        return []

    def export(self, data, fmt):
        if fmt == "json":
            return json.dumps(data, ensure_ascii=False, indent=2)
        return str(data)


# === ChapterPath utility (P0-7) ===
def chapter_path(book_dir, ch, subdir="正文", ext=".txt"):
    d = Path(book_dir) / subdir
    d.mkdir(parents=True, exist_ok=True)
    return d / (f"第{ch:03d}章{ext}")

def chapter_spec_path(book_dir, ch, ext=".json"):
    return chapter_path(book_dir, ch, "规格", ext)


def build_quote_mask(text):
    """构建引号位图：返回与 text 等长的 bool 列表，True=在引号内。
    
    统一处理中文引号对(“/”)、日文引号(「/」)
    和 ASCII 双引号("")。ASCII 双引号奇数次=开，偶数次=关。
    """
    in_quote = [False] * len(text)
    for q_open, q_close in [('\u201c', '\u201d'), ('\u300c', '\u300d')]:
        depth = 0
        for i, c in enumerate(text):
            if c == q_open:
                depth += 1
            elif c == q_close:
                depth = max(0, depth - 1)
            elif depth > 0:
                in_quote[i] = True
    # ASCII 双引号：奇数次打开，偶数次关闭
    ascii_depth = 0
    for i, c in enumerate(text):
        if c == '"':
            if ascii_depth % 2 == 0:
                # 打开引号
                ascii_depth = 1
            else:
                # 关闭引号
                ascii_depth = 0
                for j in range(i - 1, -1, -1):
                    if text[j] == '"':
                        break
                    in_quote[j] = True
        elif ascii_depth > 0:
            in_quote[i] = True
    return in_quote


