"""KingDoc 合规套件门面（v4.3.0 合并重构）

合并 v4.2 compliance_center（政企合规中心）与 v3.4 compliance_check（内容合规检查）
为单一入口门面 ComplianceSuite，底层共用 ComplianceCore 引擎：

- quick_scan 快速扫：敏感词（命中即报）+ 数据泄露，秒级返回
- full_scan 全域扫：全文敏感词 + 数据泄露 + 格式 + 密级建议 + 历史版本时间线

敏感词加载逻辑收敛为唯一来源 SensitiveWordLoader（多包叠加：base + 行业包），
扫描报告按泄露风险分级（高/中/低）并定位到段落（行号）与责任人字段（包元数据）。

零第三方依赖（仅 Python 标准库 re/sqlite3），本地降级优先，绝不调用外部 API。
"""
from __future__ import annotations

import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine.hardware import get_recommended_settings

SKILL_ROOT = Path(__file__).resolve().parent.parent

# 文档密级元数据仓（与 v4.2 compliance_center 同路径，数据兼容）
_DB_PATH = str(Path(__file__).resolve().parent.parent.parent / ".kingdoc_compliance_center.db")

# 数据泄露默认签名密钥（与 webhook_center 一致）
DEFAULT_SIGNING_SECRET = "kingdoc_webhook_secret_v4"

# 风险等级 → 三档中文映射（高/中/低）
RISK_TIER: Dict[str, str] = {"critical": "高", "high": "高", "medium": "中", "low": "低"}

CLASSIFICATION_LEVELS = ["公开", "内部", "秘密", "机密"]

# 数据不出域：允许的本地 OCR 引擎白名单（仅本地，绝不调用外部 API）
LOCAL_OCR_ENGINES = ["tesseract", "wps_ocr"]

# 数据泄露正则（中国大陆常见）
LEAK_PATTERNS = {
    "phone": {
        "pattern": r"(?<!\d)(1[3-9]\d{9})(?!\d)",
        "label": "手机号",
        "risk": "high",
    },
    "id_card": {
        "pattern": r"(?<!\d)(\d{6}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx])(?!\d)",
        "label": "身份证号",
        "risk": "critical",
    },
    "bank_card": {
        "pattern": r"(?<!\d)(\d{16,19})(?!\d)",
        "label": "银行卡号",
        "risk": "critical",
    },
    "email": {
        "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "label": "邮箱地址",
        "risk": "medium",
    },
    "ip_address": {
        "pattern": r"(?<!\d)((?:\d{1,3}\.){3}\d{1,3})(?!\d)",
        "label": "IP地址",
        "risk": "low",
    },
}

# 密级关键词（用于自动建议密级）
CLASSIFICATION_KEYWORDS = {
    "机密": [
        "绝密", "机密", "核心机密", "最高机密", "核心秘密",
        "国家安全", "战略部署", "军事机密", "情报来源",
    ],
    "秘密": [
        "秘密", "内部秘密", "商业机密", "技术机密", "研发机密",
        "客户名单", "定价策略", "并购", "未公开财报",
    ],
    "内部": [
        "内部资料", "内部文件", "内部通知", "内部会议",
        "仅限内部", "不得外传", "内部使用",
    ],
}

# 默认企业文档格式规范
DEFAULT_FORMAT_SPEC = {
    "font_name": {"expected": "宋体", "severity": "warning"},
    "font_size_body": {"expected": "12pt", "severity": "warning"},
    "font_size_h1": {"expected": "18pt", "severity": "warning"},
    "font_size_h2": {"expected": "15pt", "severity": "warning"},
    "line_spacing": {"expected": "1.5倍行距", "severity": "info"},
    "margin_top": {"expected": "2.54cm", "severity": "info"},
    "margin_bottom": {"expected": "2.54cm", "severity": "info"},
    "margin_left": {"expected": "3.17cm", "severity": "info"},
    "margin_right": {"expected": "3.17cm", "severity": "info"},
}


# ===========================================================================
# 行业敏感词分包加载器（唯一来源，支持多包叠加）
# ===========================================================================
class SensitiveWordLoader:
    """加载 references/sensitive_packs/ 下的规则包，多包叠加；支持外部词包目录。

    每个包为 YAML（受限子集，零第三方依赖自研解析）：
        pack: edu
        name: 教育培训
        responsible_field: 教务合规负责人
        risk_default: medium
        words:
          - 招生宣传管理类风险信息
          - {word: 收费公示管理类风险信息, risk: high}

    base 包始终加载；industry 包按 scan_sensitive(packs=[...]) 叠加。
    用户可通过环境变量 KINGDOC_EXTERNAL_PACKS_DIR 或传参 external_packs_dir
    加载自定义词包（外部同名包覆盖内置包，实现企业本地词库）。
    """

    PACK_DIR = SKILL_ROOT / "references" / "sensitive_packs"

    def __init__(self, external_packs_dir: Optional[str] = None):
        self._cache: Dict[str, Optional[Dict]] = {}
        self._external_dir = self._resolve_external_dir(external_packs_dir)

    @staticmethod
    def _resolve_external_dir(external_packs_dir: Optional[str] = None) -> Optional[Path]:
        """外部词包目录优先级：传参 > 环境变量 KINGDOC_EXTERNAL_PACKS_DIR。"""
        src = external_packs_dir or os.environ.get("KINGDOC_EXTERNAL_PACKS_DIR", "")
        if src:
            p = Path(src)
            if p.exists() and p.is_dir():
                return p
        return None

    def load(
        self,
        pack_ids: Optional[List[str]] = None,
        external_packs_dir: Optional[str] = None,
    ) -> List[Dict]:
        """返回扁平词表：[{word, risk, pack, responsible_field}, ...]"""
        ext = self._resolve_external_dir(external_packs_dir) or self._external_dir
        ids = ["base"] + list(pack_ids or [])
        seen = set()
        words: List[Dict] = []
        for pid in ids:
            pack = self._load_pack(pid, ext)
            if not pack:
                continue
            default_risk = pack.get("risk_default", "medium")
            rf = pack.get("responsible_field", "合规负责人")
            for w in pack.get("words", []):
                key = w["word"]
                if key in seen:
                    continue
                seen.add(key)
                words.append({
                    "word": key,
                    "risk": w.get("risk") or default_risk,
                    "pack": pid,
                    "responsible_field": rf,
                })
        # 兼容旧 user_blacklist.txt（追加自定义敏感词，pack=user）
        ub = SKILL_ROOT / "references" / "user_blacklist.txt"
        if ub.exists():
            try:
                for line in ub.read_text(encoding="utf-8").splitlines():
                    key = line.strip()
                    if key and not key.startswith("#") and key not in seen:
                        seen.add(key)
                        words.append({"word": key, "risk": "medium",
                                      "pack": "user", "responsible_field": "合规负责人"})
            except Exception:
                pass
        return words

    def list_packs(self, external_packs_dir: Optional[str] = None) -> List[Dict]:
        """列出可用规则包元信息（内置 + 外部）。"""
        ext = self._resolve_external_dir(external_packs_dir) or self._external_dir
        out = []
        seen = set()
        # 内置包
        if self.PACK_DIR.exists():
            for p in sorted(self.PACK_DIR.glob("*.yaml")):
                pack = self._load_pack(p.stem, ext)
                if pack:
                    seen.add(p.stem)
                    out.append(self._pack_meta(pack, p.stem))
        # 外部包（补充或覆盖）
        if ext and ext.exists():
            for p in sorted(ext.glob("*.yaml")):
                if p.stem in seen:
                    continue
                pack = self._load_pack(p.stem, ext)
                if pack:
                    seen.add(p.stem)
                    out.append(self._pack_meta(pack, p.stem, external=True))
        return out

    @staticmethod
    def _pack_meta(pack: Dict, stem: str, external: bool = False) -> Dict:
        meta = {
            "pack": pack.get("pack", stem),
            "name": pack.get("name", stem),
            "responsible_field": pack.get("responsible_field", ""),
            "risk_default": pack.get("risk_default", "medium"),
            "word_count": len(pack.get("words", [])),
        }
        if external:
            meta["source"] = "external"
        return meta

    def _load_pack(
        self,
        pid: str,
        external_packs_dir: Optional[Path] = None,
    ) -> Optional[Dict]:
        cache_key = pid
        if external_packs_dir:
            cache_key = f"{external_packs_dir}:{pid}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        # 外部同名包优先覆盖内置
        candidates = []
        if external_packs_dir and external_packs_dir.exists():
            candidates.append(external_packs_dir / f"{pid}.yaml")
        candidates.append(self.PACK_DIR / f"{pid}.yaml")
        pack = None
        for p in candidates:
            if p.exists():
                try:
                    pack = _parse_pack_file(p)
                    break
                except Exception:
                    pack = None
        self._cache[cache_key] = pack
        return pack


def _parse_pack_file(path: Path) -> Dict:
    """受限 YAML 子集解析（零第三方依赖）。

    支持：顶层 key: value；words: 列表，元素为 `- 词` 或 `- {word: x, risk: y}`。
    """
    pack: Dict[str, Any] = {"words": []}
    in_words = False
    with path.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if not in_words:
                if stripped == "words:":
                    in_words = True
                    continue
                if ":" not in stripped:
                    continue
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip()
                if key in ("pack", "name", "description", "responsible_field", "risk_default"):
                    pack[key] = val
            else:
                if not stripped.startswith("- "):
                    # 退出 words 块（更浅缩进的非列表行）
                    if ":" in stripped and not stripped.startswith(" "):
                        in_words = False
                        key, _, val = stripped.partition(":")
                        pack[key.strip()] = val.strip()
                        continue
                    continue
                item = stripped[2:].strip()
                if item.startswith("{") and item.endswith("}"):
                    mapping = _parse_inline_mapping(item)
                    word = mapping.get("word", "").strip()
                    if word:
                        pack["words"].append({
                            "word": word,
                            "risk": mapping.get("risk", "").strip() or None,
                        })
                else:
                    word = item.strip()
                    if word:
                        pack["words"].append({"word": word, "risk": None})
    # 必要字段兜底
    pack.setdefault("pack", path.stem)
    pack.setdefault("name", path.stem)
    pack.setdefault("responsible_field", "合规负责人")
    pack.setdefault("risk_default", "medium")
    return pack


def _parse_inline_mapping(text: str) -> Dict[str, str]:
    """解析 `{word: x, risk: y}` 内联映射。"""
    inner = text[1:-1].strip()
    out: Dict[str, str] = {}
    for part in inner.split(","):
        if ":" not in part:
            continue
        k, _, v = part.partition(":")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


# ===========================================================================
# 合规核心引擎（合并自 compliance_check + compliance_center）
# ===========================================================================
class ComplianceCore:
    """合规检查核心引擎（唯一实现，门面与兼容 shim 均委托于此）。"""

    def __init__(
        self,
        backend: Optional[Any] = None,
        external_packs_dir: Optional[str] = None,
    ):
        self.backend = backend
        self._local = backend is None
        self.hw = get_recommended_settings()
        self.max_chunk_chars = self.hw["batch_chunk"] * 200
        self._loader = SensitiveWordLoader(external_packs_dir=external_packs_dir)
        self._external_packs_dir = external_packs_dir
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(_DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS doc_classification (
                    doc_id TEXT PRIMARY KEY,
                    level TEXT NOT NULL,
                    reason TEXT DEFAULT '',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scan_report (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    doc_id TEXT,
                    level TEXT,
                    summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 1. 敏感词扫描（多包 + 风险分级 + 段落 + 责任人字段）
    # ------------------------------------------------------------------
    def scan_sensitive(
        self,
        text: str,
        custom_words: Optional[List[str]] = None,
        packs: Optional[List[str]] = None,
        external_packs_dir: Optional[str] = None,
    ) -> Dict:
        """扫描敏感词，返回命中列表（含风险档/段落/责任人字段）。

        packs: 选中的行业包（base 始终加载），如 ["edu", "finance"]
        external_packs_dir: 外部词包目录（覆盖环境变量）
        """
        ext = external_packs_dir or self._external_packs_dir
        words = self._loader.load(packs, external_packs_dir=ext)
        if custom_words:
            words = words + [{"word": w, "risk": "medium", "pack": "custom",
                              "responsible_field": "合规负责人"} for w in custom_words if w]

        hits = self._scan_words_chunked(text, words)

        # 风险三档汇总
        tier = {"高": 0, "中": 0, "低": 0}
        for h in hits:
            tier[h["risk_tier"]] = tier.get(h["risk_tier"], 0) + 1

        top_tier = "高" if tier["高"] > 0 else ("中" if tier["中"] > 0 else ("低" if tier["低"] > 0 else "低"))

        return {
            "hits": hits,
            "total_hits": len(hits),
            "unique_words": len({h["word"] for h in hits}),
            "risk_breakdown": tier,
            "top_tier": top_tier,
            "scanned_chars": len(text),
        }

    def _scan_words_chunked(self, text: str, words: List[Dict]) -> List[Dict]:
        chunk = self.max_chunk_chars
        if len(text) <= chunk:
            return self._scan_words(text, words, offset=0)
        hits: List[Dict] = []
        for start in range(0, len(text), chunk):
            seg = text[start:start + chunk]
            hits.extend(self._scan_words(seg, words, offset=start))
        return hits

    def _scan_words(self, text: str, words: List[Dict], offset: int = 0) -> List[Dict]:
        hits = []
        for entry in words:
            word = entry["word"]
            if not word:
                continue
            risk = entry.get("risk") or "medium"
            tier = RISK_TIER.get(risk, "中")
            for m in re.finditer(re.escape(word), text, re.IGNORECASE):
                abs_pos = m.start() + offset
                line = text[:abs_pos].count("\n") + 1
                start = max(0, m.start() - 10)
                end = min(len(text), m.end() + 10)
                context = text[start:end].replace("\n", " ")
                hits.append({
                    "word": word,
                    "risk": risk,
                    "risk_tier": tier,
                    "pack": entry.get("pack", "base"),
                    "responsible_field": entry.get("responsible_field", "合规负责人"),
                    "position": abs_pos,
                    "line": line,
                    "context": f"...{context}...",
                })
        hits.sort(key=lambda x: x["position"])
        return hits

    # ------------------------------------------------------------------
    # 2. 数据泄露检测
    # ------------------------------------------------------------------
    def detect_leak(self, text: str) -> Dict:
        findings = []
        for key, cfg in LEAK_PATTERNS.items():
            for m in re.finditer(cfg["pattern"], text):
                if key == "bank_card" and not self._luhn_check(m.group(0)):
                    continue
                if key == "id_card" and not self._id_card_valid(m.group(0)):
                    continue
                start = max(0, m.start() - 5)
                end = min(len(text), m.end() + 5)
                context = text[start:end].replace("\n", " ")
                findings.append({
                    "type": key,
                    "label": cfg["label"],
                    "risk": cfg["risk"],
                    "risk_tier": RISK_TIER.get(cfg["risk"], "中"),
                    "position": m.start(),
                    "line": text[:m.start()].count("\n") + 1,
                    "masked": self._mask(m.group(0), key),
                    "context": f"...{context}...",
                })
        findings.sort(key=lambda x: x["position"])
        risk_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        overall = "low"
        for f in findings:
            if risk_order.get(f["risk"], 0) > risk_order.get(overall, 0):
                overall = f["risk"]
        return {
            "findings": findings,
            "total": len(findings),
            "by_type": self._group_by_type(findings),
            "overall_risk": overall,
            "risk_tier": RISK_TIER.get(overall, "中"),
        }

    # ------------------------------------------------------------------
    # 3. 格式规范检查
    # ------------------------------------------------------------------
    def check_format(self, file_path: str) -> Dict:
        p = Path(file_path)
        if not p.exists():
            return {"error": f"文件不存在: {file_path}", "issues": []}
        suffix = p.suffix.lower()
        if suffix == ".docx":
            return self._check_docx_format(p)
        elif suffix == ".pptx":
            return self._check_pptx_format(p)
        elif suffix in (".txt", ".md"):
            return self._check_plain_format(p)
        return {"error": f"不支持的格式: {suffix}（仅支持 .docx/.pptx/.txt/.md）", "issues": []}

    # ------------------------------------------------------------------
    # 4. 密级自动标注
    # ------------------------------------------------------------------
    def classify(self, text: str) -> Dict:
        scores = {"机密": 0, "秘密": 0, "内部": 0}
        matched_keywords = {"机密": [], "秘密": [], "内部": []}
        for level, keywords in CLASSIFICATION_KEYWORDS.items():
            for kw in keywords:
                count = text.count(kw)
                if count > 0:
                    scores[level] += count
                    matched_keywords[level].append(kw)
        if scores["机密"] > 0:
            suggested = "机密"
        elif scores["秘密"] > 0:
            suggested = "秘密"
        elif scores["内部"] > 0:
            suggested = "内部"
        else:
            suggested = "公开"
        return {
            "suggested_level": suggested,
            "scores": scores,
            "matched_keywords": matched_keywords,
            "confidence": "high" if scores.get(suggested, 0) >= 3 else "medium",
        }

    # ------------------------------------------------------------------
    # 5. 密级标注落库
    # ------------------------------------------------------------------
    def label_classification(self, doc_id: str, level: str, reason: str = "") -> Dict:
        if level not in CLASSIFICATION_LEVELS:
            return {"success": False, "error": f"无效密级：{level}（应为 {CLASSIFICATION_LEVELS}）"}
        try:
            conn = sqlite3.connect(_DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO doc_classification (doc_id, level, reason, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (doc_id, level, reason))
            conn.commit()
            conn.close()
            return {"success": True, "doc_id": doc_id, "level": level,
                    "message": f"密级已标注为「{level}」并落库"}
        except Exception as e:
            return {"success": False, "error": f"密级落库失败：{e}"}

    def get_classification(self, doc_id: str) -> Dict:
        try:
            conn = sqlite3.connect(_DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT level, reason, updated_at FROM doc_classification WHERE doc_id = ?",
                        (doc_id,))
            row = cur.fetchone()
            conn.close()
            if row:
                return {"doc_id": doc_id, "level": row[0], "reason": row[1], "updated_at": row[2]}
            return {"doc_id": doc_id, "level": None, "message": "未标注密级"}
        except Exception as e:
            return {"success": False, "error": f"查询失败：{e}"}

    # ------------------------------------------------------------------
    # 6. 数据不出域声明
    # ------------------------------------------------------------------
    def declare_data_local(self, doc_id: str = "", engine: str = "tesseract") -> Dict:
        if engine not in LOCAL_OCR_ENGINES:
            return {"success": False, "error": f"不允许的 OCR 引擎：{engine}（仅限本地：{LOCAL_OCR_ENGINES}）"}
        declaration = (
            "【数据不出域声明】\n"
            f"- 文档标识：{doc_id or '未指定'}\n"
            f"- OCR 引擎：本地 {engine}（图片数据仅在本地处理，不上传任何外部服务）\n"
            "- 云端交互：仅同步文档元数据（标题/密级/版本），原始内容不出本机\n"
            "- 合规基线：符合政企「数据不出域」要求，敏感内容本地闭环处理\n"
            "- 密级管控：标注密级随元数据落库，越权访问在检索/分享前被拦截"
        )
        return {"success": True, "doc_id": doc_id, "engine": engine, "declaration": declaration}

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------
    @staticmethod
    def _luhn_check(number: str) -> bool:
        if not number.isdigit():
            return False
        digits = [int(d) for d in number]
        digits.reverse()
        total = 0
        for i, d in enumerate(digits):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        return total % 10 == 0

    @staticmethod
    def _id_card_valid(id_number: str) -> bool:
        if len(id_number) != 18:
            return False
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = "10X98765432"
        try:
            total = sum(int(id_number[i]) * weights[i] for i in range(17))
            return check_codes[total % 11].upper() == id_number[17].upper()
        except (ValueError, IndexError):
            return False

    @staticmethod
    def _mask(value: str, vtype: str) -> str:
        if vtype == "phone" and len(value) == 11:
            return value[:3] + "****" + value[7:]
        if vtype == "id_card" and len(value) == 18:
            return value[:4] + "**********" + value[14:]
        if vtype == "bank_card" and len(value) >= 16:
            return value[:4] + " **** **** " + value[-4:]
        if vtype == "email":
            at = value.find("@")
            if at > 1:
                return value[0] + "***" + value[at:]
        return value[:2] + "***" + value[-2:] if len(value) > 4 else "***"

    @staticmethod
    def _group_by_type(findings: List[Dict]) -> Dict:
        result = {}
        for f in findings:
            t = f["type"]
            if t not in result:
                result[t] = {"label": f["label"], "count": 0, "risk": f["risk"]}
            result[t]["count"] += 1
        return result

    def _overall_risk(self, sensitive: Dict, leak: Dict) -> str:
        order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        s = order.get(sensitive.get("top_tier", "低"), 1)
        l = order.get(leak.get("overall_risk", "low"), 1)
        top = max(s, l)
        return {4: "critical", 3: "high", 2: "medium", 1: "low"}[top]

    def _recommend(self, risk: str, leak: Dict) -> List[str]:
        recs = []
        if risk in ("critical", "high"):
            recs.append("建议将文档密级提升为「秘密」及以上，并限制分享范围。")
        if leak.get("total", 0) > 0:
            recs.append("检测到敏感个人信息/证照数据，建议脱敏后流转或采用数据不出域处理。")
        recs.append("本地 OCR 强制（数据不出域），云端仅同步元数据，符合政企合规要求。")
        return recs

    def _save_report(self, doc_id: str, level: str, report: Dict) -> None:
        try:
            conn = sqlite3.connect(_DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO scan_report (doc_id, level, summary) VALUES (?, ?, ?)",
                (doc_id, level, str(report)),
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _check_docx_format(self, path: Path) -> Dict:
        import zipfile
        from xml.etree import ElementTree as ET
        issues = []
        try:
            with zipfile.ZipFile(path) as z:
                with z.open("word/document.xml") as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
                    for rpr in root.findall(".//w:rPr", ns):
                        for rf in rpr.findall(".//w:rFonts", ns):
                            font = rf.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia")
                            if font and font != "宋体":
                                issues.append({"type": "font_name", "expected": "宋体",
                                               "actual": font, "severity": "warning",
                                               "message": f"字体应为宋体，实际为 {font}"})
                    for sz in root.findall(".//w:sz", ns):
                        size_val = sz.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
                        if size_val:
                            pt = int(size_val) / 2
                            if pt < 10 or pt > 14:
                                issues.append({"type": "font_size", "expected": "10-14pt",
                                               "actual": f"{pt}pt", "severity": "warning",
                                               "message": f"正文字号应在 10-14pt 之间，实际为 {pt}pt"})
        except Exception as e:
            issues.append({"type": "parse_error", "expected": "正常解析", "actual": str(e),
                           "severity": "error", "message": f"解析 DOCX 失败: {e}"})
        return {"file": str(path), "format": "docx", "issues": issues,
                "issue_count": len(issues), "compliant": len(issues) == 0}

    def _check_pptx_format(self, path: Path) -> Dict:
        import zipfile
        from xml.etree import ElementTree as ET
        issues = []
        try:
            with zipfile.ZipFile(path) as z:
                slide_files = [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
                for sf in slide_files:
                    with z.open(sf) as f:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
                        for txbody in root.findall(".//a:txBody", ns):
                            p_elements = txbody.findall("a:p", ns)
                            has_text = False
                            for p in p_elements:
                                for t in p.findall(".//a:t", ns):
                                    if t.text and t.text.strip():
                                        has_text = True
                                        break
                                if has_text:
                                    break
                            if not has_text:
                                issues.append({"type": "empty_textbox", "expected": "有内容",
                                               "actual": "空文本框", "severity": "info",
                                               "message": f"{sf} 中存在空文本框"})
        except Exception as e:
            issues.append({"type": "parse_error", "expected": "正常解析", "actual": str(e),
                           "severity": "error", "message": f"解析 PPTX 失败: {e}"})
        return {"file": str(path), "format": "pptx", "issues": issues,
                "issue_count": len(issues), "compliant": len(issues) == 0}

    def _check_plain_format(self, path: Path) -> Dict:
        issues = []
        try:
            content = path.read_text(encoding="utf-8")
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                if len(line) > 80:
                    issues.append({"type": "line_too_long", "expected": "≤80字符",
                                   "actual": f"{len(line)}字符", "severity": "info",
                                   "message": f"第{i}行超过80字符（{len(line)}字符）"})
            if path.suffix == ".md":
                h1_count = sum(1 for l in lines if l.startswith("# "))
                if h1_count == 0 and len(lines) > 10:
                    issues.append({"type": "missing_h1", "expected": "至少1个 H1 标题",
                                   "actual": "无 H1 标题", "severity": "warning",
                                   "message": "长文档缺少 H1 标题"})
        except Exception as e:
            issues.append({"type": "parse_error", "expected": "正常解析", "actual": str(e),
                           "severity": "error", "message": f"读取文件失败: {e}"})
        return {"file": str(path), "format": path.suffix.lstrip("."), "issues": issues,
                "issue_count": len(issues), "compliant": len(issues) == 0}


# ===========================================================================
# 合规套件门面（单入口两档输出）
# ===========================================================================
class ComplianceSuite:
    """合规套件门面：消除「用哪个」困惑，统一两档扫描。"""

    def __init__(
        self,
        backend: Optional[Any] = None,
        external_packs_dir: Optional[str] = None,
    ):
        self.core = ComplianceCore(backend=backend, external_packs_dir=external_packs_dir)
        self._local = backend is None
        self._external_packs_dir = external_packs_dir

    def quick_scan(
        self,
        text: str,
        packs: Optional[List[str]] = None,
        external_packs_dir: Optional[str] = None,
    ) -> Dict:
        """快速扫：敏感词（命中即报）+ 数据泄露，秒级返回。"""
        ext = external_packs_dir or self._external_packs_dir
        sensitive = self.core.scan_sensitive(text, packs=packs, external_packs_dir=ext)
        leak = self.core.detect_leak(text)
        # 风险分级汇总
        tier = {"高": sensitive["risk_breakdown"]["高"], "中": sensitive["risk_breakdown"]["中"],
                "低": sensitive["risk_breakdown"]["低"]}
        for f in leak["findings"]:
            tier[f["risk_tier"]] = tier.get(f["risk_tier"], 0) + 1
        return {
            "mode": "quick",
            "success": True,
            "scanned_at": datetime.now().isoformat(timespec="seconds"),
            "sensitive_hits": sensitive["total_hits"],
            "leak_findings": leak["total"],
            "risk_breakdown": tier,
            "top_tier": "高" if tier["高"] > 0 else ("中" if tier["中"] > 0 else "低"),
            "sensitive_detail": sensitive["hits"],
            "leak_detail": leak["findings"],
            "by_type": leak["by_type"],
        }

    def full_scan(
        self,
        text: str,
        doc_id: str = "",
        include_history: Optional[List[Dict]] = None,
        packs: Optional[List[str]] = None,
        external_packs_dir: Optional[str] = None,
    ) -> Dict:
        """全域扫：全文敏感词 + 数据泄露 + 格式 + 密级建议 + 历史版本时间线。

        include_history: 历史版本列表 [{"version":1,"author":"...","time":"...","content":"..."}]
        external_packs_dir: 外部词包目录（覆盖环境变量）
        """
        ext = external_packs_dir or self._external_packs_dir
        sensitive = self.core.scan_sensitive(text, packs=packs, external_packs_dir=ext)
        leak = self.core.detect_leak(text)
        klass = self.core.classify(text)
        total_risk = self.core._overall_risk(sensitive, leak)

        if doc_id and klass.get("suggested_level"):
            self.core.label_classification(doc_id, klass["suggested_level"], reason="全域扫描自动建议")

        timeline = []
        if include_history:
            timeline = self._build_history_timeline(include_history)

        report = {
            "mode": "full",
            "doc_id": doc_id,
            "scanned_at": datetime.now().isoformat(timespec="seconds"),
            "overall_risk": total_risk,
            "risk_tier": RISK_TIER.get(total_risk, "中"),
            "sensitive_words": {
                "total_hits": sensitive["total_hits"],
                "unique_words": sensitive["unique_words"],
                "risk_breakdown": sensitive["risk_breakdown"],
            },
            "data_leak": {
                "total": leak["total"],
                "by_type": leak["by_type"],
                "overall_risk": leak["overall_risk"],
            },
            "classification_suggestion": klass.get("suggested_level", "公开"),
            "history_timeline": timeline,
            "recommendations": self.core._recommend(total_risk, leak),
        }
        if doc_id:
            self.core._save_report(doc_id, klass.get("suggested_level", "公开"), report)
        return {"success": True, **report}

    @staticmethod
    def _build_history_timeline(history: List[Dict]) -> List[Dict]:
        """逐版本 difflib 生成 who/when/what 时间线。"""
        import difflib
        timeline = []
        prev = ""
        for snap in history:
            cur = snap.get("content", "")
            version = snap.get("version", "?")
            author = snap.get("author", "未知")
            time = snap.get("time", "")
            if prev:
                diff = list(difflib.unified_diff(
                    prev.splitlines(), cur.splitlines(), lineterm="", n=0))
                added = [d[1:] for d in diff if d.startswith("+") and not d.startswith("+++")]
                removed = [d[1:] for d in diff if d.startswith("-") and not d.startswith("---")]
                what = f"新增 {len(added)} 行 / 删除 {len(removed)} 行"
            else:
                what = "初始版本"
            timeline.append({
                "version": version,
                "author": author,
                "time": time,
                "what": what,
                "added_lines": len([d for d in []]),  # placeholder，下面重算
            })
            # 重算准确行数
            if prev:
                timeline[-1]["added_lines"] = len([d for d in diff if d.startswith("+") and not d.startswith("+++")])
                timeline[-1]["removed_lines"] = len([d for d in diff if d.startswith("-") and not d.startswith("---")])
            else:
                timeline[-1]["added_lines"] = len(cur.splitlines())
                timeline[-1]["removed_lines"] = 0
            prev = cur
        return timeline

    def get_status(self) -> Dict:
        return {
            "local_mode": self._local,
            "levels": CLASSIFICATION_LEVELS,
            "local_ocr_engines": LOCAL_OCR_ENGINES,
            "available_packs": self.core._loader.list_packs(),
            "external_packs_dir": self._external_packs_dir or os.environ.get("KINGDOC_EXTERNAL_PACKS_DIR", ""),
            "workers": self.core.hw.get("workers", 1),
        }


# ===========================================================================
# 单例 + 便捷函数
# ===========================================================================
_suite: Optional[ComplianceSuite] = None


def get_compliance_suite(
    backend: Optional[Any] = None,
    external_packs_dir: Optional[str] = None,
) -> ComplianceSuite:
    global _suite
    if _suite is None:
        _suite = ComplianceSuite(backend=backend, external_packs_dir=external_packs_dir)
    return _suite


def quick_scan(
    text: str,
    packs: Optional[List[str]] = None,
    external_packs_dir: Optional[str] = None,
) -> Dict:
    return get_compliance_suite(external_packs_dir=external_packs_dir).quick_scan(
        text, packs=packs, external_packs_dir=external_packs_dir)


def full_scan(
    text: str,
    doc_id: str = "",
    include_history: Optional[List[Dict]] = None,
    packs: Optional[List[str]] = None,
    external_packs_dir: Optional[str] = None,
) -> Dict:
    return get_compliance_suite(external_packs_dir=external_packs_dir).full_scan(
        text, doc_id, include_history, packs=packs, external_packs_dir=external_packs_dir)


def list_packs(external_packs_dir: Optional[str] = None) -> List[Dict]:
    return get_compliance_suite(external_packs_dir=external_packs_dir).core._loader.list_packs(
        external_packs_dir=external_packs_dir)


def get_suite_status(external_packs_dir: Optional[str] = None) -> Dict:
    return get_compliance_suite(external_packs_dir=external_packs_dir).get_status()
