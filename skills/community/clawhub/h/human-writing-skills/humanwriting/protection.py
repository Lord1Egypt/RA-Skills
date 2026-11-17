from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


SERIOUS_DOCUMENT_TYPES = {
    "academic-paper",
    "formal-document",
    "news-report",
    "legal",
    "technical",
}
FORMAL_DOCUMENT_CUE = re.compile(
    r"公文|正式文件|通知书|通报|请示|批复|纪要|公函|函件|函复|决定书|实施意见|管理办法|暂行规定|"
    r"official document|formal memorandum|official notice|administrative notice",
    re.IGNORECASE,
)
NARRATIVE_DOCUMENT_TYPES = {"fiction", "webnovel", "self-media"}
SERIOUS_TASK_PATTERN = re.compile(
    r"(?:学术|科研|研究)?论文|新闻(?:稿|报道|报告)|公文|正式文件|通知|通报|请示|批复|纪要|"
    r"法律文书|合同(?:条款|文本)?|"
    r"判决书|起诉状|答辩状|法律意见书|技术文档|接口文档|API\s*文档|"
    r"academic paper|research paper|news report|official document|formal memorandum|legal document|contract|"
    r"technical documentation|API documentation|"
    r"\b(?:article scientifique|rapport de recherche|reportage|article de presse|document juridique|documentation technique|"
    r"artículo científico|informe de investigación|noticia periodística|documento jurídico|documentación técnica|"
    r"artigo científico|relatório de pesquisa|reportagem jornalística|documento jurídico|documentação técnica)\b|"
    r"研究論文|学術論文|新聞記事|法律文書|技術文書|بحث علمي|تقرير صحفي|وثيقة قانونية|توثيق تقني",
    re.IGNORECASE,
)
ACADEMIC_CUE = re.compile(
    r"研究(?:方法|结果|结论)|实验(?:方法|结果)|样本量|显著性|置信区间|"
    r"参考文献|\b(?:doi|methodology|results?|conclusion|sample size)\b|p\s*[<=>]|"
    r"\b(?:étude|résultats|échantillon|investigación|resultados|amostra|pesquisa|resultados)\b|"
    r"研究|結果|考察|調査|دراسة|نتائج|بحث",
    re.IGNORECASE,
)
NEWS_CUE = re.compile(
    r"据.{0,30}(?:报道|消息)|记者|通讯员|消息人士|新闻发布会|截至.{0,20}[时日]|"
    r"\b(?:reported by|according to|news conference|spokesperson|selon|a déclaré|"
    r"según|declaró|segundo|afirmou)\b|によると|報道|記者|بحسب|صرح|أفاد",
    re.IGNORECASE,
)
LEGAL_CUE = re.compile(
    r"本合同|甲方|乙方|第[一二三四五六七八九十百\d]+条|依法|法定|"
    r"判决如下|诉讼请求|违约责任|管辖法院|hereby|pursuant to|"
    r"\b(?:governing law|liability|jurisdiction|contrat|tribunal|juridiction|"
    r"contrato|tribunal|jurisdição|jurisdicción)\b|契約|裁判所|法令|العقد|المحكمة|القانون",
    re.IGNORECASE,
)
TECHNICAL_CUE = re.compile(
    r"\bAPI\b|接口参数|请求参数|返回值|错误码|版本号|配置文件|数据类型|"
    r"函数签名|schema|endpoint|request|response|error code|configuration|"
    r"data type|function signature|\b(?:schéma|paramètre|réponse|esquema|parámetro|resposta|"
    r"parâmetro|configuração)\b|設定|引数|戻り値|الإعدادات|المعاملات|استجابة",
    re.IGNORECASE,
)
MULTILINGUAL_FORMAL_CUE = re.compile(
    r"\b(?:communiqué officiel|note administrative|arrêté|circulaire|"
    r"comunicado oficial|resolução administrativa|resolución administrativa|ofício)\b|"
    r"公文書|通達|告示|公式声明|تعميم رسمي|مذكرة رسمية|قرار إداري",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ProtectedItem:
    kind: str
    value: str
    count: int


@dataclass(frozen=True)
class ProtectionDifference:
    kind: str
    value: str
    expected_count: int
    actual_count: int


@dataclass(frozen=True)
class ProtectionReport:
    ok: bool
    source_items: tuple[ProtectedItem, ...]
    missing_or_changed: tuple[ProtectionDifference, ...]
    added: tuple[ProtectionDifference, ...]

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "source_items": [asdict(item) for item in self.source_items],
            "missing_or_changed": [asdict(item) for item in self.missing_or_changed],
            "added": [asdict(item) for item in self.added],
        }


CITATION_PATTERN = re.compile(r"\\cite\{[^}]+\}|\[[0-9][0-9,;\s\-–—]*\]")
EQUATION_PATTERN = re.compile(r"\$\$.*?\$\$|\$[^$\n]+\$", re.DOTALL)
NAMED_TERM_PATTERN = re.compile(
    r"《[^》\n]{2,60}》|\b[A-Z]{2,}(?:[ -][A-Z0-9]{2,})*\b|"
    r"\b[A-Z][A-Za-z0-9]*(?:[-_.][A-Za-z0-9]+)+\b"
)
PROTECTED_PATTERNS = [
    ("fenced-code", re.compile(r"```.*?```", re.DOTALL)),
    ("source-quote", re.compile(r"(?m)^\s*>\s+.+$")),
    ("inline-code", re.compile(r"`[^`\n]+`")),
    ("url", re.compile(r"https?://[^\s)>]+")),
    ("citation", CITATION_PATTERN),
    ("equation", EQUATION_PATTERN),
    ("named-term", NAMED_TERM_PATTERN),
]
NUMBER_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_.])[+-]?\d+(?:\.\d+)?(?:\s*(?:%|毫米|厘米|米|公里|秒|分钟|小时|"
    r"元|美元|岁|mg|g|kg|mm|cm|km|ms|s|min|h))?",
    re.IGNORECASE,
)


def detect_serious_document(
    text: str = "",
    document_type: str = "auto",
    task: str = "",
) -> tuple[bool, str]:
    """Return whether protected-content rules should auto-load.

    Exact numbers alone never count as a serious-document signal.
    """
    if document_type in NARRATIVE_DOCUMENT_TYPES:
        return False, f"Narrative document type `{document_type}` suppresses auto-protection."
    if document_type in SERIOUS_DOCUMENT_TYPES:
        return True, f"Serious document type `{document_type}` requires factual preservation."
    if document_type not in {"auto", "general", "argumentative"}:
        raise ValueError(f"Unknown document type: {document_type}")
    if SERIOUS_TASK_PATTERN.search(task):
        return True, "The task explicitly requests a serious factual document."

    has_citation = bool(CITATION_PATTERN.search(text))
    has_equation = bool(EQUATION_PATTERN.search(text))
    academic = len({match.casefold() for match in ACADEMIC_CUE.findall(text)}) >= 2 and (has_citation or has_equation)
    legal_hits = len({match.casefold() for match in LEGAL_CUE.findall(text)})
    technical_hits = len({match.casefold() for match in TECHNICAL_CUE.findall(text)})
    news_hits = len({match.casefold() for match in NEWS_CUE.findall(text)})
    formal_hits = len({match.casefold() for pattern in (FORMAL_DOCUMENT_CUE, MULTILINGUAL_FORMAL_CUE) for match in pattern.findall(text)})
    if academic:
        return True, "Academic cues occur with a citation or equation."
    if legal_hits >= 2:
        return True, "Multiple legal-document cues were detected."
    if technical_hits >= 2 and ("`" in text or "```" in text or "http" in text):
        return True, "Multiple technical-document cues occur with code or a URL."
    if news_hits >= 2:
        return True, "Multiple attributed news-report cues were detected."
    if formal_hits >= 2:
        return True, "Multiple official-document cues were detected."
    return False, "No strong serious-document evidence was detected."


def _overlaps(span: tuple[int, int], occupied: list[tuple[int, int]]) -> bool:
    return any(span[0] < end and start < span[1] for start, end in occupied)


def extract_protected_items(text: str, terms: list[str] | None = None) -> list[ProtectedItem]:
    values: list[tuple[str, str]] = []
    occupied: list[tuple[int, int]] = []
    for kind, pattern in PROTECTED_PATTERNS:
        for match in pattern.finditer(text):
            if _overlaps(match.span(), occupied):
                continue
            values.append((kind, match.group(0)))
            occupied.append(match.span())
    for match in NUMBER_PATTERN.finditer(text):
        if not _overlaps(match.span(), occupied):
            values.append(("number", match.group(0)))
    for term in dict.fromkeys(terms or []):
        if term:
            values.extend(("explicit-term", term) for _ in range(text.count(term)))
    counts = Counter(values)
    return [
        ProtectedItem(kind, value, count)
        for (kind, value), count in sorted(counts.items(), key=lambda item: (item[0][0], item[0][1]))
    ]


def compare_protected_content(
    source: str,
    candidate: str,
    terms: list[str] | None = None,
) -> ProtectionReport:
    source_items = extract_protected_items(source, terms)
    candidate_items = extract_protected_items(candidate, terms)
    source_counts = {(item.kind, item.value): item.count for item in source_items}
    candidate_counts = {(item.kind, item.value): item.count for item in candidate_items}
    missing = []
    added = []
    for key, expected in source_counts.items():
        actual = candidate_counts.get(key, 0)
        if actual < expected:
            missing.append(ProtectionDifference(key[0], key[1], expected, actual))
    for key, actual in candidate_counts.items():
        expected = source_counts.get(key, 0)
        if actual > expected:
            added.append(ProtectionDifference(key[0], key[1], expected, actual))
    return ProtectionReport(
        ok=not missing and not added,
        source_items=tuple(source_items),
        missing_or_changed=tuple(missing),
        added=tuple(added),
    )


def compare_protected_files(
    source_path: str,
    candidate_path: str,
    terms: list[str] | None = None,
) -> ProtectionReport:
    source = Path(source_path).read_text(encoding="utf-8")
    candidate = Path(candidate_path).read_text(encoding="utf-8")
    return compare_protected_content(source, candidate, terms)


def build_protection_manifest(text: str, terms: list[str] | None = None) -> str:
    items = extract_protected_items(text, terms)
    present_explicit_terms = {
        item.value for item in items if item.kind == "explicit-term"
    }
    items.extend(
        ProtectedItem("explicit-term", term, max(1, text.count(term)))
        for term in dict.fromkeys(terms or [])
        if term and term not in present_explicit_terms
    )
    lines = [
        "# Protected Content Manifest",
        "",
        "Preserve every listed item and occurrence count exactly. Flag suspected errors instead of changing them.",
        "",
        "| Kind | Count | Value |",
        "| --- | --- | --- |",
    ]
    for item in items:
        value = item.value.replace("\n", " ").replace("|", "\\|")
        if len(value) > 160:
            value = value[:157] + "..."
        lines.append(f"| {item.kind} | {item.count} | `{value}` |")
    if not items:
        lines.append("| none detected | 0 | Add explicit `--protect-term` values if needed. |")
    return "\n".join(lines)


def format_protection_report(report: ProtectionReport, output_format: str = "markdown") -> str:
    if output_format == "json":
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n"
    lines = [
        "# Protected Content Verification",
        "",
        f"- Status: {'PASS' if report.ok else 'FAIL'}",
        "- Scope: literal token counts only; this does not verify actor, polarity, uncertainty, attribution, or claim meaning.",
        f"- Source items: {len(report.source_items)}",
        f"- Missing or changed: {len(report.missing_or_changed)}",
        f"- Added protected-looking items: {len(report.added)}",
        "",
        "## Missing or changed",
        "",
        "| Kind | Expected | Actual | Value |",
        "| --- | --- | --- | --- |",
    ]
    for item in report.missing_or_changed:
        value = item.value.replace("\n", " ").replace("|", "\\|")
        lines.append(f"| {item.kind} | {item.expected_count} | {item.actual_count} | `{value}` |")
    if not report.missing_or_changed:
        lines.append("| none | - | - | - |")
    lines.extend(
        [
            "",
            "## Added protected-looking items",
            "",
            "| Kind | Source | Candidate | Value |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in report.added:
        value = item.value.replace("\n", " ").replace("|", "\\|")
        lines.append(f"| {item.kind} | {item.expected_count} | {item.actual_count} | `{value}` |")
    if not report.added:
        lines.append("| none | - | - | - |")
    return "\n".join(lines) + "\n"
