#!/usr/bin/env python3
"""Infoseek 密钥泄漏扫描器（v1.0.1 PATCH / 合规审计项）

扫描代码库/配置中疑似硬编码的 API key / token / 密码：
- 常见 key 模式：sk-xxx / sk-ant-xxx / AKIA...（AWS）/ ghp_xxx（GitHub PAT）
- 赋值模式：XXX_API_KEY = 'literal' / "literal"
- 环境变量模板残留：${env:...} / $VAR 不应误报（白名单）

用法:
    python scripts/leak_scan.py [--path .] [--exclude dist,node_modules,.git] [--json]

退出码: 0=无泄漏 1=发现疑似泄漏
"""
import argparse
import json
import re
import sys
from pathlib import Path

# 疑似 key 字面量模式（覆盖主流格式）
KEY_PATTERNS = [
    (re.compile(r'\bsk-[A-Za-z0-9-]{16,}\b'), 'OpenAI/通用 sk- key'),
    (re.compile(r'\bsk-ant-[A-Za-z0-9-]{20,}\b'), 'Anthropic sk-ant key'),
    (re.compile(r'\bAKIA[0-9A-Z]{16}\b'), 'AWS Access Key'),
    (re.compile(r'\bghp_[A-Za-z0-9]{30,}\b'), 'GitHub Personal Access Token'),
    (re.compile(r'\bgho_[A-Za-z0-9]{30,}\b'), 'GitHub OAuth Token'),
    (re.compile(r'\bAIza[0-9A-Za-z_-]{30,}\b'), 'Google API Key'),
    (re.compile(r'\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\b'), 'JWT token'),
    (re.compile(r'\b[0-9a-f]{32,40}\b'), '疑似 SHA/HEX 密钥（32-40 hex）'),
    (re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b'), 'Slack token'),
]

# 赋值模式：VAR = 'literal'（key 相关变量名）
ASSIGN_PATTERN = re.compile(
    r"(?im)^\s*(?P<var>[A-Z][A-Z0-9_]*(?:_API_KEY|_TOKEN|_SECRET|_PASSWORD|_PASSWD|_CLIENT_SECRET)"
    r")\s*[=:]\s*['\"](?P<val>[^'\"]{8,})['\"]")

# 白名单：这些值不误报（env 占位 / 示例 / mock）
SAFE_VALUES = {
    'xxx', 'your-key-here', 'example', 'changeme', 'test', 'dummy', 'placeholder',
    'sk-test', 'sk-demo', 'sk-example', 'NOT_SET', '<key>', 'YOUR_API_KEY',
}

# 文件扩展名白名单（只扫源码/配置/文档）
SCAN_EXTS = {'.py', '.js', '.ts', '.tsx', '.json', '.yaml', '.yml', '.env',
             '.toml', '.ini', '.sh', '.md', '.txt'}


def scan_file(path: Path, findings: list) -> None:
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return
    for line_no, line in enumerate(text.splitlines(), 1):
        # 1) key 字面量模式
        for pat, desc in KEY_PATTERNS:
            for m in pat.finditer(line):
                val = m.group(0)
                if val.lower() in SAFE_VALUES or val.startswith('sk-test') or val.startswith('sk-demo'):
                    continue
                findings.append({
                    'file': str(path), 'line': line_no, 'pattern': desc,
                    'value': val[:20] + ('...' if len(val) > 20 else ''),
                })
        # 2) 赋值模式（跳过含 os.environ / getenv / input 的行）
        if ('API_KEY' in line or '_TOKEN' in line or '_SECRET' in line) and \
           'environ' not in line and 'getenv' not in line and 'KeyManager' not in line:
            for m in ASSIGN_PATTERN.finditer(line):
                val = m.group('val')
                if val.lower() in SAFE_VALUES or val.startswith('sk-test') or val.startswith('sk-demo'):
                    continue
                findings.append({
                    'file': str(path), 'line': line_no,
                    'pattern': f"硬编码赋值 {m.group('var')}",
                    'value': val[:20] + ('...' if len(val) > 20 else ''),
                })


def main() -> int:
    ap = argparse.ArgumentParser(description='Infoseek 密钥泄漏扫描器')
    ap.add_argument('--path', default='.', help='扫描根目录（默认当前目录）')
    ap.add_argument('--exclude', default='dist,node_modules,.git,.venv,__pycache__',
                    help='排除目录（逗号分隔）')
    ap.add_argument('--json', action='store_true', help='JSON 输出')
    args = ap.parse_args()

    root = Path(args.path).resolve()
    excludes = {x.strip() for x in args.exclude.split(',') if x.strip()}
    findings = []
    files = 0

    for p in root.rglob('*'):
        if not p.is_file():
            continue
        if any(part in excludes for part in p.parts):
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue
        files += 1
        scan_file(p, findings)

    # 去重（同文件同行同值）
    seen = set()
    unique = []
    for f in findings:
        k = (f['file'], f['line'], f['value'])
        if k not in seen:
            seen.add(k)
            unique.append(f)

    if args.json:
        print(json.dumps({'files_scanned': files, 'findings': unique,
                          'leak_count': len(unique)}, ensure_ascii=False, indent=2))
    else:
        print(f"扫描完成: {files} 文件 | 疑似泄漏 {len(unique)} 处")
        for f in unique[:50]:
            print(f"  ⚠️ {f['file']}:{f['line']} [{f['pattern']}] {f['value']}")
        if len(unique) > 50:
            print(f"  ... 还有 {len(unique)-50} 处（用 --json 查看全部）")

    return 1 if unique else 0


if __name__ == '__main__':
    sys.exit(main())
