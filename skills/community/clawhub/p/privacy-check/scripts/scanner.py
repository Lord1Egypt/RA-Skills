#!/usr/bin/env python3
"""
隐私敏感信息扫描器 (Privacy Check) v1.0.1

扫描文件中的敏感个人信息：身份证号、手机号、邮箱、银行卡号、
信用卡号、SSN、护照号、驾驶证号、微信号、支付宝号等。
支持 JSON/CSV/HTML 报告输出、白名单忽略、文件类型过滤。

用法:
    python3 scripts/scanner.py --file data.csv
    python3 scripts/scanner.py --dir ./data/ --output report.json
    python3 scripts/scanner.py --file data.csv --format html --output report.html
    python3 scripts/scanner.py --dir ./data/ --ignore "^#|// " --ext .txt,.csv
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ============ 正则模式 ============
# (pattern_id, regex, description, severity, validation_type)
# validation_type: None / "ip" / "luhn" / "luhn16"

PATTERNS = [
    ("china_id",
     r"\b[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b",
     "中国大陆身份证号", "高", None),
    ("china_phone",
     r"\b1[3-9]\d{9}\b",
     "中国大陆手机号", "高", None),
    ("email",
     r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
     "电子邮件地址", "中", None),
    ("bank_card",
     r"\b[1-9]\d{11,18}\b",
     "银行卡号（Luhn校验）", "高", "luhn"),
    ("credit_card",
     r"\b(?:4\d{3}|5[1-5]\d{2}|3[47]\d{2}|6011|65\d{2})\d{10,15}\b",
     "信用卡号（Luhn校验）", "高", "luhn"),
    ("ssn",
     r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b",
     "美国社会安全号(SSN)", "高", None),
    ("china_passport",
     r"\b[1-9]\d{8}[A-Za-z0-9]\b",
     "中国护照号", "高", None),
    ("hk_passport",
     r"\b[A-Za-z]{2}\d{6,8}\b",
     "港澳护照号", "高", None),
    ("tw_passport",
     r"\b\d{9}\b",
     "台湾护照号", "中", None),
    ("driver_license",
     r"\b[1-9]\d{17}[\dXx]\b",
     "中国大陆驾驶证号", "高", None),
    ("wechat_id",
     r"\b[A-Za-z][A-Za-z0-9_-]{5,19}\b",
     "微信号", "中", None),
    ("alipay_id",
     r"\b(?:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|1[3-9]\d{9})\b",
     "支付宝账号（邮箱/手机）", "中", None),
    ("ip_address",
     r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
     "IP地址", "低", "ip"),
    ("china_postal",
     r"\b\d{6}\b",
     "邮政编码", "低", None),
    ("api_key",
     r"\b(?:sk-[A-Za-z0-9]{20,}|api[_-]?key['\"]?\s*[:=]\s*['\"]?[A-Za-z0-9]{16,})\b",
     "API密钥", "高", None),
]


def _luhn_check(card_num):
    """Luhn 算法校验。"""
    if not card_num.isdigit():
        return False
    digits = [int(d) for d in card_num]
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def _validate_match(pid, match_text):
    """根据 validation_type 校验匹配结果。"""
    pat = next((p for p in PATTERNS if p[0] == pid), None)
    if pat is None or pat[4] is None:
        return True
    vtype = pat[4]
    if vtype == "ip":
        parts = match_text.split(".")
        if any(int(p) > 255 for p in parts):
            return False
        return True
    if vtype == "luhn":
        return _luhn_check(match_text)
    return True


def _mask(text, ptype):
    """脱敏处理。"""
    if ptype == "china_id":
        return text[:4] + "**********" + text[-4:]
    elif ptype == "china_phone":
        return text[:3] + "****" + text[-4:]
    elif ptype == "email":
        at = text.find("@")
        return text[:3] + "****" + text[at:]
    elif ptype in ("bank_card", "credit_card"):
        return text[:4] + "**********" + text[-4:]
    elif ptype == "ssn":
        return "***-**-" + text[-4:]
    elif ptype in ("china_passport", "hk_passport", "tw_passport"):
        return text[:2] + "******" + text[-2:]
    elif ptype == "driver_license":
        return text[:4] + "**************" + text[-2:]
    elif ptype == "wechat_id":
        return text[:2] + "****" + text[-2:]
    elif ptype == "alipay_id":
        if "@" in text:
            at = text.find("@")
            return text[:3] + "****" + text[at:]
        return text[:3] + "****" + text[-4:]
    elif ptype == "api_key":
        return text[:8] + "..." + text[-4:]
    elif ptype == "ip_address":
        parts = text.split(".")
        parts[1] = "***"
        return ".".join(parts)
    else:
        return text[:3] + "***" + text[-3:] if len(text) > 6 else "***"


def _mask_text(text):
    """对文本中所有PII模式进行脱敏处理。"""
    chars = list(text)
    for pid, pat_regex, desc, severity, _ in PATTERNS:
        for match in re.finditer(pat_regex, text):
            if _validate_match(pid, match.group()):
                masked_val = _mask(match.group(), pid)
                s, e = match.start(), match.end()
                chars[s:e] = list(masked_val)
    return "".join(chars)


def _get_context(lines, idx, window=1, mask=True):
    """获取匹配行的上下文。"""
    start = max(0, idx - window - 1)
    end = min(len(lines), idx + window)
    ctx = [l.strip()[:80] for l in lines[start:end]]
    if mask:
        ctx = [_mask_text(l) for l in ctx]
    return ctx


def _should_ignore(line, ignore_patterns):
    """检查行是否匹配忽略模式。"""
    if not ignore_patterns:
        return False
    for pat in ignore_patterns:
        if re.search(pat, line):
            return True
    return False


def scan_file(filepath, patterns=None, ignore_patterns=None, include_context=False):
    """扫描单个文件中的敏感信息。"""
    if patterns is None:
        patterns = PATTERNS
    ext = Path(filepath).suffix.lower()
    findings = []

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        return [{"file": filepath, "error": str(e)}]

    lines = content.split("\n")
    for idx, line in enumerate(lines, 1):
        if _should_ignore(line, ignore_patterns):
            continue
        for pid, pat_regex, desc, severity, _ in patterns:
            for match in re.finditer(pat_regex, line):
                if not _validate_match(pid, match.group()):
                    continue
                findings.append({
                    "file": filepath,
                    "line": idx,
                    "type": pid,
                    "description": desc,
                    "severity": severity,
                    "match": _mask(match.group(), pid),
                    "context": _get_context(lines, idx) if include_context else [],
                })
    return findings


def scan_path(path, patterns=None, ignore_patterns=None, allowed_exts=None, include_context=False):
    """扫描文件或目录，支持按扩展名过滤。"""
    if os.path.isfile(path):
        if allowed_exts:
            ext = Path(path).suffix.lower()
            if ext not in allowed_exts:
                return []
        return scan_file(path, patterns, ignore_patterns, include_context)

    results = []
    for root, _, files in os.walk(path):
        for fname in files:
            fpath = os.path.join(root, fname)
            if allowed_exts:
                ext = Path(fpath).suffix.lower()
                if ext not in allowed_exts:
                    continue
            results.extend(scan_file(fpath, patterns, ignore_patterns, include_context))
    return results


def _ascii_bar(value, max_value, width=20):
    """生成 ASCII 条形图。"""
    if max_value == 0:
        return "░" * 0
    filled = int((value / max_value) * width)
    return "█" * filled + "░" * (width - filled)


def generate_report(findings, output_path=None, output_format="json"):
    """生成扫描报告。"""
    by_type = defaultdict(list)
    by_severity = defaultdict(list)
    for f in findings:
        if "error" in f:
            continue
        by_type[f["type"]].append(f)
        by_severity[f["severity"]].append(f)

    severity_order = ["高", "中", "低"]

    report = {
        "scan_time": datetime.now().isoformat(),
        "total_findings": len([f for f in findings if "error" not in f]),
        "errors": len([f for f in findings if "error" in f]),
        "by_type": {k: len(v) for k, v in sorted(by_type.items(),
                    key=lambda x: -len(x[1]))},
        "by_severity": {k: len(v) for k, v in sorted(by_type.items())},
        "details": findings,
        "security_notice": "本报告包含脱敏后的敏感数据信息，请妥善保管，避免泄露或被未授权访问。",
        "recommendation": "为减少敏感数据聚合风险，建议使用默认模式（不包含上下文）。如需上下文，请使用 --context 参数。",
    }

    if output_format == "json":
        out = json.dumps(report, indent=2, ensure_ascii=False)
    elif output_format == "csv":
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["file", "line", "type", "description", "severity", "match"])
        for f in findings:
            if "error" in f:
                continue
            w.writerow([f["file"], f["line"], f["type"],
                        f["description"], f["severity"], f["match"]])
        out = buf.getvalue()
    elif output_format == "html":
        out = _generate_html_report(report, by_type)
    else:
        out = json.dumps(report, indent=2, ensure_ascii=False)

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(out)
    return out


def _generate_html_report(report, by_type):
    """生成 HTML 格式扫描报告。"""
    max_count = max((len(v) for v in by_type.values()), default=0)
    bar_rows = ""
    for t, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
        pat = next((p for p in PATTERNS if p[0] == t), None)
        desc = pat[2] if pat else t
        sev = pat[3] if pat else "-"
        count = len(items)
        bar = _ascii_bar(count, max_count, 30)
        bar_rows += (
            f"<tr><td>{desc}</td><td>{sev}</td>"
            f"<td><pre style='margin:0'>{bar}</pre></td>"
            f"<td style='text-align:right'>{count}</td></tr>\n"
        )

    sev_rows = ""
    for s in ["高", "中", "低"]:
        c = report["by_severity"].get(s, 0)
        sev_rows += f"<tr><td>{s}</td><td>{c}</td></tr>\n"

    detail_rows = ""
    for f in report["details"][:100]:  # 最多显示100条
        if "error" in f:
            detail_rows += (
                f"<tr class='error'><td>{f['file']}</td>"
                f"<td>-</td><td>-</td><td>-</td>"
                f"<td>错误: {f['error']}</td><td></td></tr>\n"
            )
        else:
            ctx = " | ".join(f.get("context", []))
            detail_rows += (
                f"<tr><td>{f['file']}</td><td>{f['line']}</td>"
                f"<td>{f['description']}</td><td>{f['severity']}</td>"
                f"<td>{f['match']}</td><td>{ctx[:60]}</td></tr>\n"
            )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8">
<title>Privacy Check 报告 - {report['scan_time'][:10]}</title>
<style>
body {{ font-family: -apple-system, 'PingFang SC', sans-serif; margin: 20px; color: #222; }}
h1, h2 {{ color: #1a1a2e; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0; }}
th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; }}
th {{ background: #16213e; color: #fff; font-weight: 500; }}
tr:nth-child(even) background: #f5f5f5; }}
.error {{ background: #ffe0e0; }}
.summary {{ display: flex; gap: 20px; margin: 20px 0; }}
.summary-card {{ background: #f0f4ff; border-radius: 8px; padding: 12px 20px; flex:1; }}
.summary-card h3 {{ margin: 0 0 4px; font-size: 14px; color: #555; }}
.summary-card .num {{ font-size: 28px; font-weight: 700; color: #16213e; }}
footer {{ margin-top: 30px; font-size: 12px; color: #888; }}
</style>
</head>
<body>
<h1>🔍 Privacy Check 扫描报告</h1>
<p>扫描时间: {report['scan_time']}</p>
<div class="summary">
  <div class="summary-card"><h3>发现总数</h3><div class="num">{report['total_findings']}</div></div>
  <div class="summary-card"><h3>扫描错误</h3><div class="num">{report['errors']}</div></div>
  <div class="summary-card"><h3>PII类型</h3><div class="num">{len(by_type)}</div></div>
</div>

<h2>按严重级别</h2>
<table><tr><th>级别</th><th>数量</th></tr>{sev_rows}</table>

<h2>按类型分布</h2>
<table><tr><th>类型</th><th>级别</th><th>分布</th><th>数量</th></tr>{bar_rows}</table>

<h2>详细发现（前100条）</h2>
<table>
<tr><th>文件</th><th>行</th><th>类型</th><th>级别</th><th>匹配内容(脱敏)</th><th>上下文</th></tr>
{detail_rows}
</table>
<footer>本工具仅辅助检测，不构成专业合规审计。报告由 Privacy Check v1.0.1 生成。</footer>
</body>
</html>
"""
    return html


def print_summary(report):
    """打印扫描摘要（含 ASCII 条形图）。"""
    by_type = defaultdict(list)
    for f in report["details"]:
        if "error" not in f:
            by_type[f["type"]].append(f)
    max_count = max((len(v) for v in by_type.values()), default=0)

    print(f"\n{'='*50}")
    print(f"🔍 隐私敏感信息扫描报告")
    print(f"{'='*50}")
    print(f"扫描时间: {report['scan_time']}")
    print(f"发现总数: {report['total_findings']}")
    print()
    print("⚠️  安全提醒：本报告包含脱敏后的敏感数据信息，")
    print("   请妥善保管扫描结果，避免泄露或被未授权访问。")
    if any(f.get("context") for f in report.get("details", []) if "error" not in f):
        print()
        print("   🔒 上下文信息已包含在报告中。默认模式下上下文是关闭的，")
        print("   如需关闭请上传时不带 --context 参数。")

    if report["errors"]:
        print(f"扫描错误: {report['errors']}")
    print()

    sev_order = ["高", "中", "低"]
    if report["by_severity"]:
        print("按严重级别:")
        for s in sev_order:
            c = report["by_severity"].get(s, 0)
            if c:
                print(f"  [{s}] {c} 项")
    print()

    if by_type:
        print("按类型分布（ASCII 条形图）:")
        for t, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
            pat = next((p for p in PATTERNS if p[0] == t), None)
            desc = pat[2] if pat else t
            count = len(items)
            bar = _ascii_bar(count, max_count)
            print(f"  {bar} {desc}: {count}")

    if report["details"]:
        print(f"\n前 10 条发现:")
        for i, f in enumerate(report["details"][:10], 1):
            if "error" in f:
                print(f"  {i}. [错误] {f['file']}: {f['error']}")
            else:
                ctx = " | ".join(f.get("context", []))
                print(f"  {i}. [{f['severity']}] {f['description']} "
                      f"@ {Path(f['file']).name}:{f['line']} → {f['match']}")
                if ctx:
                    print(f"     上下文: {ctx[:60]}")


def main():
    parser = argparse.ArgumentParser(
        description="隐私敏感信息扫描器 (Privacy Check v1.0.1)")
    parser.add_argument("--file", help="扫描单个文件")
    parser.add_argument("--dir", help="扫描目录")
    parser.add_argument("--output", help="输出报告路径")
    parser.add_argument("--format", choices=["json", "csv", "html"],
                        default="json", help="输出格式（默认 JSON）")
    parser.add_argument("--ignore", help="忽略模式（正则表达式，可多次使用）",
                        action="append", default=[])
    parser.add_argument("--ext", help="文件扩展名过滤（逗号分隔，例: .txt,.csv）")
    parser.add_argument("--context", action="store_true",
                        help="包含上下文信息（默认关闭以减少敏感数据聚合风险）")
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)

    allowed_exts = None
    if args.ext:
        allowed_exts = {e.strip().lower() if e.strip().startswith(".")
                        else "." + e.strip().lower()
                        for e in args.ext.split(",")}

    path = args.file or args.dir
    findings = scan_path(path, ignore_patterns=args.ignore or None,
                         allowed_exts=allowed_exts,
                         include_context=args.context)
    report_data = json.loads(generate_report(findings, None, "json"))
    report_data["scan_time"] = datetime.now().isoformat()

    output_format = args.format
    generate_report(findings, args.output, output_format)

    print_summary(report_data)

    if args.output:
        fmt_name = output_format.upper()
        print(f"\n📄 报告已保存: {args.output} ({fmt_name})")


if __name__ == "__main__":
    main()
