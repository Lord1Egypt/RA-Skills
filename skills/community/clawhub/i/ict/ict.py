#!/usr/bin/env python3
"""ICT - Claw Skill Security Auditor v4.0.4"""
import os, re, ast, json, argparse, sys
from typing import Dict, List, Any, Set, Tuple

VERSION = "4.0.8"
LOG_FILE = os.path.expanduser("~/.openclaw/workspace/ict_audit.log")

def log(msg, level="INFO"):
    """Simple logging"""
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{level}] {msg}\n")
    except: pass

def check_for_update():
    """Check for updates"""
    try:
        import urllib.request
        req = urllib.request.Request("https://api.clawhub.ai/skills/ict", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            latest = data.get('latest', VERSION)
            if latest != VERSION:
                try:
                    curr = tuple(map(int, VERSION.split('.')))
                    lat = tuple(map(int, latest.split('.')))
                    if lat > curr:
                        print("\n" + "="*50)
                        print("Update Available!")
                        print(f"Current: v{VERSION}")
                        print(f"Latest:  v{latest}")
                        print("Please update: clawhub install ict")
                        print("="*50 + "\n")
                except: pass
    except: pass

from rules import SECURITY_CHECKS, NET_PATTERNS, FALSE_POSITIVE_PATTERNS, REQUIRED_SKILL_SECTIONS, AUDITOR_FILES, SUPPORTED_LANGUAGES

def is_comment(line, ext):
    s = line.strip()
    if ext == 'py': return s.startswith('#') or s.startswith('"""') or s.startswith("'''")
    if ext in ('sh', 'bash'): return s.startswith('#')
    return False

def get_lang(fp): return SUPPORTED_LANGUAGES.get(os.path.splitext(fp)[1].lower(), 'unknown')

def get_files(path):
    r = []
    for root, dirs, files in os.walk(path):
        if any(x in root for x in ['test', '__pycache__', '.git']): continue
        for f in files:
            lang = get_lang(f)
            if lang != 'unknown': r.append((os.path.join(root, f), lang))
    return r

class FuncExtractor(ast.NodeVisitor):
    def __init__(self): self.f = set()
    def visit_FunctionDef(self, n): self.f.add(n.name); self.generic_visit(n)

def get_funcs(path):
    if not path.endswith('.py'): return set()
    try:
        with open(path) as f: tree = ast.parse(f.read())
        e = FuncExtractor(); e.visit(tree); return e.f
    except: return set()

def check_file(path, lang):
    issues = []
    try: lines = open(path).readlines()
    except: return issues
    fn = os.path.basename(path)
    for cn, desc, pats, sev in SECURITY_CHECKS:
        pat = '|'.join(pats.get(lang, []) + pats.get('all', []))
        if not pat: continue
        for i, line in enumerate(lines, 1):
            if is_comment(line, lang): continue
            if fn in AUDITOR_FILES: continue
            for fp in FALSE_POSITIVE_PATTERNS:
                if re.search(fp, line, re.I): break
            else:
                if re.search(pat, line, re.I):
                    issues.append({'Line': i, 'type': 'security', 'severity': sev, 'file': fn, 'lang': lang, 'message': desc + ': ' + line.strip()[:50]})
    return issues

def check_combo(path):
    issues, files = [], get_files(path)
    cf, nf = set(), set()
    for fp, lang in files:
        if any(a in fp for a in AUDITOR_FILES): continue
        try:
            c = open(fp).read()
            cp = '|'.join(SECURITY_CHECKS[0][2].get(lang, []) + SECURITY_CHECKS[0][2].get('all', []))
            np = '|'.join(NET_PATTERNS.get(lang, []) + NET_PATTERNS.get('all', []))
            if cp and re.search(cp, c, re.I): cf.add(fp)
            if np and re.search(np, c, re.I): nf.add(fp)
        except: pass
    for f in cf & nf:
        issues.append({'Line': 0, 'type': 'security', 'severity': 'critical', 'file': os.path.basename(f), 'message': 'Combo threat'})
    return issues

def check_doc_sec(path):
    issues = []
    pat = '|'.join(SECURITY_CHECKS[12][2].get('all', []) + SECURITY_CHECKS[13][2].get('all', []))
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(('.md', '.txt')) and f not in AUDITOR_FILES:
                try:
                    c = open(os.path.join(root, f)).read()
                    for m in re.finditer(pat, c, re.I):
                        issues.append({'Line': c[:m.start()].count('\n')+1, 'type': 'security', 'severity': 'critical', 'file': f, 'message': 'Prompt injection'})
                except: pass
    return issues

def check_struct(path):
    issues, files = [], get_files(path)
    if not files: issues.append({'Line': 0, 'type': 'structure', 'severity': 'medium', 'message': 'No code files'})
    return issues

def check_doc(path):
    issues = []
    md = os.path.join(path, 'SKILL.md')
    if not os.path.exists(md):
        issues.append({'Line': 0, 'type': 'doc', 'severity': 'high', 'message': 'Missing SKILL.md'})
    else:
        try:
            c = open(md).read()
            for s in REQUIRED_SKILL_SECTIONS:
                if s not in c: issues.append({'Line': 0, 'type': 'doc', 'severity': 'medium', 'message': 'Missing: ' + s})
        except: pass
    return issues

def audit(path, allow=None):
    r = {'skill_path': path, 'version': VERSION, 'security_issues': [], 'structure_issues': [], 'doc_issues': [], 'consistency_issues': [], 'overall_score': 100, 'summary': {}, 'checks_count': len(SECURITY_CHECKS), 'languages': set()}
    if not os.path.isdir(path): r['error'] = 'Path not found'; r['overall_score'] = 0; return r
    allow = allow or []
    al = os.path.basename(path) in allow
    r['structure_issues'].extend(check_struct(path))
    files = get_files(path)
    for fp, lang in files: r['languages'].add(lang)
    for fp, lang in files: r['security_issues'].extend(check_file(fp, lang))
    r['security_issues'].extend(check_doc_sec(path)); r['security_issues'].extend(check_combo(path))
    r['doc_issues'].extend(check_doc(path))
    if al:
        for i in r['security_issues']:
            if i.get('severity') == 'critical': i['severity'] = 'info'; i['message'] = '[ALLOWLISTED] ' + i['message']
    w = {'critical': 15, 'high': 10, 'medium': 5, 'low': 2, 'info': 0}
    all_i = r['security_issues'] + r['structure_issues'] + r['doc_issues'] + r['consistency_issues']
    r['overall_score'] = max(0, 100 - sum(w.get(i.get('severity', 'low'), 2) for i in all_i))
    r['summary'] = {'total_issues': len(all_i), 'critical': sum(1 for i in all_i if i.get('severity') == 'critical'), 'high': sum(1 for i in all_i if i.get('severity') == 'high'), 'medium': sum(1 for i in all_i if i.get('severity') == 'medium'), 'low': sum(1 for i in all_i if i.get('severity') == 'low'), 'allowlisted': al, 'languages': list(r['languages'])}
    del r['languages']
    return r

def print_report(r):
    print("\n" + "="*55)
    print(f"ICT Skill Auditor v{VERSION}")
    print("="*55)
    print(f"Path: {r['skill_path']}")
    print(f"Checks: {r['checks_count']} items")
    print(f"Score: {r['overall_score']}/100")
    s = r.get('summary', {})
    print(f"Issues: Critical:{s.get('critical',0)} High:{s.get('high',0)} Medium:{s.get('medium',0)} Low:{s.get('low',0)}")
    v = "Excellent" if r['overall_score'] >= 90 else "Needs Work" if r['overall_score'] >= 70 else "High Risk"
    print(f"Verdict: {v}")
    print("="*55 + "\n")

TREND = os.path.expanduser("~/.openclaw/workspace/ict_trends.json")

def trust_score(path, audit_r):
    sc = {'security': 35, 'quality': 22, 'structure': 18, 'transparency': 15, 'behavioral': 10, 'total': 100, 'grade': 'A', 'dimensions': {}}
    su = audit_r.get('summary', {}); c,h,m,l = su.get('critical',0), su.get('high',0), su.get('medium',0), su.get('low',0)
    sc['security'] = max(0, 35 - (c*18 + h*8 + m*4 + l*2))
    sc['quality'] = 22
    sc['structure'] = 18 if get_files(path) else 10
    sc['transparency'] = 15
    sc['behavioral'] = max(0, 10 - len(audit_r.get('consistency_issues', [])) * 2)
    sc['total'] = sum([sc['security'], sc['quality'], sc['structure'], sc['transparency'], sc['behavioral']])
    sc['grade'] = 'A' if sc['total'] >= 90 else 'B' if sc['total'] >= 75 else 'C' if sc['total'] >= 60 else 'D' if sc['total'] >= 40 else 'F'
    return sc

def save_trend(path, score):
    import time
    n = os.path.basename(path)
    t = json.load(open(TREND)) if os.path.exists(TREND) else {}
    if n not in t: t[n] = []
    t[n].append({'timestamp': int(time.time()), 'score': score}); t[n] = t[n][-50:]
    json.dump(t, open(TREND, 'w'), indent=2)

def batch_scan(dirpath=None, allow=None):
    if not dirpath: dirpath = os.path.expanduser("~/.openclaw/workspace/skills")
    if not os.path.isdir(dirpath): return {'error': 'Directory not found', 'skills': []}
    results = []
    for e in os.listdir(dirpath):
        p = os.path.join(dirpath, e)
        if os.path.isdir(p) and not e.startswith('.'):
            try:
                r = audit(p, allow)
                results.append({'name': e, 'path': p, 'score': r.get('overall_score', 0), 'issues': r.get('summary', {}).get('total_issues', 0), 'critical': r.get('summary', {}).get('critical', 0), 'verdict': 'Safe' if r.get('overall_score', 0) >= 90 else 'Warning' if r.get('overall_score', 0) >= 70 else 'Risk'})
            except Exception as ex: results.append({'name': e, 'error': str(ex)})
    results.sort(key=lambda x: x.get('score', 0))
    return {'skills_dir': dirpath, 'total_skills': len(results), 'skills': results}

def print_batch(data):
    from datetime import datetime
    sk = data.get('skills', []); total = data.get('total_skills', 0)
    sc = sum(1 for s in sk if s.get('score', 0) >= 90)
    wc = sum(1 for s in sk if 70 <= s.get('score', 0) < 90)
    dc = sum(1 for s in sk if s.get('score', 0) < 70)
    avg = sum(s.get('score', 0) for s in sk) / total if total else 0
    tc = sum(s.get('critical', 0) for s in sk)
    ti = sum(s.get('issues', 0) for s in sk)
    print(f"\nScan Info")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Directory: {data.get('skills_dir', 'N/A')}")
    print(f"  Total: {total}")
    print(f"  Avg Score: {avg:.1f} | Critical: {tc} | Issues: {ti}")
    if not sk: print("\nNo skills found\n"); return
    ds = [s for s in sk if s.get('score', 0) < 70]
    ws = [s for s in sk if 70 <= s.get('score', 0) < 90]
    ss = [s for s in sk if s.get('score', 0) >= 90]
    if ds: print(f"\nRisk ({len(ds)}): {', '.join([s['name'] + '(' + str(s['critical']) + ')' for s in ds])}")
    if ws: print(f"\nWarning ({len(ws)}): {', '.join([s['name'] for s in ws])}")
    if ss: print(f"\nSafe ({len(ss)}): {', '.join([s['name'] for s in ss])}")
    print("\n")

def load_allow(path):
    try: return [s.get('name', '') for s in json.load(open(path)).get('skills', [])]
    except: return []

def main():
    check_for_update()
    p = argparse.ArgumentParser(description='ICT Skill Auditor v' + VERSION)
    p.add_argument('folder', nargs='?'); p.add_argument('--json', action='store_true'); p.add_argument('--allowlist'); p.add_argument('--all', '-a', action='store_true'); p.add_argument('--skills-dir'); p.add_argument('--score', '-s', action='store_true'); p.add_argument('--save-trend', action='store_true')
    a = p.parse_args()
    allow = load_allow(a.allowlist) if a.allowlist else []
    if a.all:
        data = batch_scan(a.skills_dir, allow)
        print(json.dumps(data, ensure_ascii=False, indent=2) if a.json else print_batch(data))
        return
    if not a.folder: p.error("Specify path or use --all")
    result = audit(a.folder, allow)
    if a.save_trend: save_trend(a.folder, trust_score(a.folder, result)['total']); print("Saved")
    if a.score: print("Score: " + str(trust_score(a.folder, result)['total']) + "/100")
    else: print(json.dumps(result, ensure_ascii=False, indent=2) if a.json else print_report(result))
    sys.exit(2 if result.get('summary',{}).get('critical',0) else (1 if result.get('summary',{}).get('high',0) or result.get('summary',{}).get('medium',0) else 0))

if __name__ == '__main__': main()
