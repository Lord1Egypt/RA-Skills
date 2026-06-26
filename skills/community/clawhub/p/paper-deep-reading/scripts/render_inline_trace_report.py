#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


APPENDIX_HEADING = '# Appendix: Claim -> Evidence Index'
CLAIM_BULLET_RE = re.compile(r'^\s*-\s+\[(C\d+(?:\.\d+)*)\](?:\[[^\]]+\])?', re.MULTILINE)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def clean_latex_text(text: str) -> str:
    text = text.replace('~', ' ')
    text = re.sub(r'\\begin\{[^}]+\}', ' ', text)
    text = re.sub(r'\\end\{[^}]+\}', ' ', text)
    text = re.sub(r'\\(cite|ref|label|url|footnote)\{[^}]*\}', ' ', text)
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+\*?', ' ', text)
    text = text.replace('{', '').replace('}', '')
    return re.sub(r'\s+', ' ', text).strip()


def section_label(paragraph: dict) -> str:
    section_path = paragraph.get('section_path') or []
    if section_path:
        return ' > '.join(str(part) for part in section_path)
    kind = paragraph.get('kind') or ''
    if kind == 'abstract':
        return 'Abstract'
    return 'Front matter / unspecified'


def start_excerpt(text: str, n_words: int = 14) -> str:
    words = clean_latex_text(text).split()
    return ' '.join(words[:n_words])


def end_excerpt(text: str, n_words: int = 14) -> str:
    words = clean_latex_text(text).split()
    return ' '.join(words[-n_words:])


def detect_language(report_text: str, language: str) -> str:
    if language in {'en', 'zh'}:
        return language
    cjk_chars = sum(1 for char in report_text if '\u4e00' <= char <= '\u9fff')
    return 'zh' if cjk_chars >= 20 else 'en'


def claim_ids_in_body(report_text: str) -> list[str]:
    body = report_text.split(APPENDIX_HEADING, 1)[0]
    seen: set[str] = set()
    ordered: list[str] = []
    for claim_id in CLAIM_BULLET_RE.findall(body):
        if claim_id in seen:
            continue
        seen.add(claim_id)
        ordered.append(claim_id)
    return ordered


def localize(language: str) -> dict[str, str]:
    if language == 'zh':
        return {
            'interpretation_type': '判定类型',
            'statement': '结论',
            'research_role': '研究角色',
            'confidence': '置信度',
            'human_locators': '人工定位提示',
            'evidence': '证据',
            'source_file': '来源文件',
            'section_path': '章节路径',
            'lines': '行号',
            'page': '页码',
            'locator_method': '定位方式',
            'quote': '引用片段',
            'excerpt_window': '摘录窗口',
            'notes': '备注',
            'missing_manifest': 'traceability_manifest.json 中缺少该 claim。',
            'unknown': '未知',
            'not_available': '无',
        }
    return {
        'interpretation_type': 'Interpretation type',
        'statement': 'Statement',
        'research_role': 'Research role',
        'confidence': 'Confidence',
        'human_locators': 'Human locators',
        'evidence': 'Evidence',
        'source_file': 'Source file',
        'section_path': 'Section path',
        'lines': 'Lines',
        'page': 'Page',
        'locator_method': 'Locator method',
        'quote': 'Quote',
        'excerpt_window': 'Excerpt window',
        'notes': 'Notes',
        'missing_manifest': 'Missing from traceability_manifest.json.',
        'unknown': 'unknown',
        'not_available': 'n/a',
    }


def format_optional_value(value: object, unknown_label: str) -> str:
    if value is None:
        return unknown_label
    text = str(value).strip()
    return text or unknown_label


def format_line_span(evidence: dict, paragraph: dict | None, unknown_label: str) -> str:
    line_start = evidence.get('line_start')
    line_end = evidence.get('line_end')
    if paragraph:
        line_start = paragraph.get('line_start', line_start)
        line_end = paragraph.get('line_end', line_end)
    if line_start and line_end:
        return f'{line_start}-{line_end}'
    if line_start:
        return str(line_start)
    return unknown_label


def format_evidence_block(evidence: dict, paragraph: dict | None, labels: dict[str, str], index: int) -> list[str]:
    source_file = evidence.get('source_file') or evidence.get('doc')
    section_path = labels['unknown']
    excerpt_window = labels['not_available']

    if paragraph:
        source_file = paragraph.get('source_path', source_file)
        section_path = section_label(paragraph)
        excerpt_window = f'"{start_excerpt(paragraph.get("text", ""))}" -> "{end_excerpt(paragraph.get("text", ""))}"'

    if not source_file and evidence.get('paragraph_id'):
        source_file = evidence.get('paragraph_id')

    lines = format_line_span(evidence, paragraph, labels['unknown'])
    page = format_optional_value(evidence.get('page'), labels['not_available'])
    locator_method = format_optional_value(evidence.get('locator_method') or evidence.get('relation'), labels['not_available'])
    quote = format_optional_value(evidence.get('quote_text') or evidence.get('quote'), labels['not_available'])
    locator_snippets = evidence.get('locator_snippets')
    notes_value = evidence.get('notes')
    if isinstance(locator_snippets, list) and locator_snippets:
        snippet_text = '; '.join(str(item).strip() for item in locator_snippets if str(item).strip())
        if notes_value:
            notes_value = f'{notes_value} | Locator snippets: {snippet_text}'
        else:
            notes_value = f'Locator snippets: {snippet_text}'
    notes = format_optional_value(notes_value, labels['not_available'])

    return [
        f'### {labels["evidence"]} {index}',
        f'- {labels["source_file"]}: `{format_optional_value(source_file, labels["unknown"])}`',
        f'- {labels["section_path"]}: {section_path}',
        f'- {labels["lines"]}: {lines}',
        f'- {labels["page"]}: {page}',
        f'- {labels["locator_method"]}: `{locator_method}`',
        f'- {labels["quote"]}: {quote}',
        f'- {labels["excerpt_window"]}: {excerpt_window}',
        f'- {labels["notes"]}: {notes}',
    ]


def render_appendix(report_text: str, manifest: dict, paragraphs: dict, language: str) -> str:
    labels = localize(language)
    claim_ids = claim_ids_in_body(report_text)
    para_map = {
        item['paragraph_id']: item
        for item in paragraphs.get('paragraphs', [])
        if isinstance(item, dict) and item.get('paragraph_id')
    }
    claim_map = {
        item['claim_id']: item
        for item in manifest.get('claims', [])
        if isinstance(item, dict) and item.get('claim_id')
    }

    appendix_lines = [APPENDIX_HEADING, '']
    for claim_id in claim_ids:
        claim = claim_map.get(claim_id)
        appendix_lines.append(f'## {claim_id}')
        if not claim:
            appendix_lines.append(f'- {labels["notes"]}: {labels["missing_manifest"]}')
            appendix_lines.append('')
            continue

        appendix_lines.extend(
            [
                f'- {labels["interpretation_type"]}: {format_optional_value(claim.get("interpretation_type"), labels["unknown"])}',
                f'- {labels["statement"]}: {format_optional_value(claim.get("statement") or claim.get("claim_text"), labels["unknown"])}',
                f'- {labels["research_role"]}: {format_optional_value(claim.get("research_role"), labels["not_available"])}',
                f'- {labels["confidence"]}: {format_optional_value(claim.get("confidence"), labels["not_available"])}',
            ]
        )

        human_locators = claim.get('human_locators')
        if isinstance(human_locators, list) and human_locators:
            appendix_lines.append(f'- {labels["human_locators"]}:')
            for locator in human_locators:
                appendix_lines.append(f'  - {str(locator).strip()}')

        appendix_lines.append('')

        evidences = claim.get('evidences')
        if not isinstance(evidences, list):
            evidences = claim.get('evidence', [])
        for index, evidence in enumerate(evidences, start=1):
            if not isinstance(evidence, dict):
                continue
            paragraph = para_map.get(evidence.get('paragraph_id'))
            appendix_lines.extend(format_evidence_block(evidence, paragraph, labels, index))
            appendix_lines.append('')

    appendix = '\n'.join(appendix_lines).rstrip() + '\n'
    if APPENDIX_HEADING in report_text:
        body = report_text.split(APPENDIX_HEADING, 1)[0].rstrip()
        return body + '\n\n' + appendix
    return report_text.rstrip() + '\n\n' + appendix


def main() -> None:
    parser = argparse.ArgumentParser(description='Render the final claim-to-evidence appendix into report.md')
    parser.add_argument('--report', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--paragraphs', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--language', choices=['auto', 'en', 'zh'], default='auto')
    args = parser.parse_args()

    report_text = Path(args.report).read_text(encoding='utf-8')
    manifest = load_json(Path(args.manifest))
    paragraphs = load_json(Path(args.paragraphs))
    language = detect_language(report_text, args.language)
    rendered = render_appendix(report_text, manifest, paragraphs, language)

    Path(args.output).write_text(rendered, encoding='utf-8')


if __name__ == '__main__':
    main()
