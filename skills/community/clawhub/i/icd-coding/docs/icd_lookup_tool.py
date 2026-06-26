#!/usr/bin/env python3
"""
ICD编码查找工具 - 诊断主导词 & 手术主导词 & 临床术语映射
支持：
1. 诊断主导词 → ICD-10编码（精确+模糊）
2. ICD-10编码 → 诊断主导词（反向）
3. 手术主导词 → ICD-9-CM-3编码（精确+模糊）
4. ICD-9-CM-3编码 → 手术主导词（反向）
5. 临床术语 → 国家临床版ICD-10编码（31,106条映射）
6. ICD-10编码 → 临床术语
7. 按科室查询临床术语
"""
import zipfile, xml.etree.ElementTree as ET2, re, json, os, sys

BASE = '/workspace/user_input_files'
OUT_DIR = '/workspace/skills/ICD-Coding/data'
os.makedirs(OUT_DIR, exist_ok=True)

# ─── 共用解析函数 ──────────────────────────────────────────────
def extract_xlsx(xlsx_path):
    with zipfile.ZipFile(xlsx_path) as z:
        with z.open('xl/sharedStrings.xml') as f:
            ss_tree = ET2.parse(f)
        NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        strings = [''.join(t.text or '' for t in si.findall('.//ns:t', NS))
                    for si in ss_tree.getroot().findall('.//ns:si', NS)]
        with z.open('xl/worksheets/sheet1.xml') as f:
            tree = ET2.parse(f)
        rows = []
        for row in tree.findall('.//ns:row', NS):
            cells = {}
            for c in row.findall('ns:c', NS):
                col = ''.join(ch for ch in c.get('r','') if ch.isalpha())
                v = c.find('ns:v', NS); t = c.get('t','')
                if v is not None and v.text is not None:
                    cells[col] = strings[int(v.text)] if t == 's' else v.text
            if cells: rows.append(cells)
        return strings, rows

def parse_diag_b(b):
    if not b or b == '主导词': return None, None
    m = re.match(r'^(.+?)\s*([A-Z]\d[\d.*\-+/()a-z ]*[A-Z0-9])\s*$', b.strip(), re.DOTALL)
    if m: return m.group(1).rstrip('，,([').strip(), m.group(2).strip()
    return b.strip(), None

def parse_surg_b(b):
    if not b or b == '主导词': return None, None
    m = re.match(r'^(.+?)\s*(\d{2,3}\.\d{1,2}[a-z0-9]*)\s*(\[.*\])?\s*$', b.strip())
    if m: return m.group(1).strip(), m.group(2).strip()
    m2 = re.match(r'^(.+?)\s+([A-Z]\d[\d.*\-+/() ]*[A-Z0-9])\s*$', b.strip(), re.DOTALL)
    if m2: return m2.group(1).rstrip('，,(').strip(), m2.group(2).strip()
    return b.strip(), None

def parse_sub(v):
    if not v: return None
    dashes = len(v) - len(v.lstrip('—'))
    txt = v.lstrip('—').strip()
    cm = re.search(r'(\d{2,3}\.\d{1,2}[a-z0-9]*)', txt)
    if not cm: cm = re.search(r'([A-Z]\d[\d.*\-+/() ]*[A-Z0-9*])', txt)
    return {'level': dashes, 'text': txt, 'code': cm.group(1).strip() if cm else None}

# ─── 构建诊断主导词 ────────────────────────────────────────────
def build_diag():
    _, rows = extract_xlsx(f'{BASE}/诊断主导词.xlsx')
    by_word, all_with_code = {}, []
    for row in rows[1:]:
        b = row.get('B', ''); word, code = parse_diag_b(b)
        if not word: continue
        subs = [parse_sub(row.get(c)) for c in ['C','D','E','F','G','H','I'] if row.get(c)]
        subs = [s for s in subs if s]
        entry = {'word': word, 'code': code, 'subs': subs}
        by_word.setdefault(word, []).append(entry)
        if code: all_with_code.append(entry)
    with open(f'{OUT_DIR}/diag_by_word.json','w',encoding='utf-8') as f: json.dump(by_word, f, ensure_ascii=False)
    with open(f'{OUT_DIR}/diag_all.json','w',encoding='utf-8') as f: json.dump(all_with_code, f, ensure_ascii=False)
    return by_word

def build_surg():
    _, rows = extract_xlsx(f'{BASE}/手术主导词.xlsx')
    by_word, all_with_code = {}, []
    for row in rows[1:]:
        b = row.get('B', ''); word, code = parse_surg_b(b)
        if not word: continue
        subs = [parse_sub(row.get(c)) for c in ['C','D','E','F','G','H','I'] if row.get(c)]
        subs = [s for s in subs if s]
        entry = {'word': word, 'code': code, 'subs': subs}
        by_word.setdefault(word, []).append(entry)
        if code: all_with_code.append(entry)
    with open(f'{OUT_DIR}/surg_by_word.json','w',encoding='utf-8') as f: json.dump(by_word, f, ensure_ascii=False)
    with open(f'{OUT_DIR}/surg_all.json','w',encoding='utf-8') as f: json.dump(all_with_code, f, ensure_ascii=False)
    return by_word

# ─── 查询函数 ──────────────────────────────────────────────────
def _fmt(e, label):
    path = f'[{label}] {e["code"]}'
    if e['subs']:
        path += '\n  查找路径:'
        for s in e['subs']:
            indent = '  ' + '──' * s['level']
            path += f'\n  {indent} {s["text"]}' + (f' → {s["code"]}' if s['code'] else '')
    return path

def lookup_diag_word(q):
    with open(f'{OUT_DIR}/diag_by_word.json', encoding='utf-8') as f: by_word = json.load(f)
    r = []
    if q in by_word:
        for e in by_word[q]:
            if e['code']: r.append({'type':'精确','word':q,**e,'display':_fmt(e,'ICD-10')})
    for kw, entries in by_word.items():
        if q in kw and kw != q and len(r) < 15:
            for e in entries:
                if e['code'] and not any(x.get('word')==kw for x in r):
                    r.append({'type':'包含','word':kw,**e,'display':_fmt(e,'ICD-10')})
    return r

def lookup_diag_code(q):
    with open(f'{OUT_DIR}/diag_by_word.json', encoding='utf-8') as f: by_word = json.load(f)
    r = []
    for word, entries in by_word.items():
        for e in entries:
            if e['code'] and q.upper() in e['code'].upper():
                r.append({'type':'code_match','code':e['code'],'word':word,'display':f'[主导词] {word}\n  ICD-10: {e["code"]}'})
    return r[:15]

def lookup_surg_word(q):
    with open(f'{OUT_DIR}/surg_by_word.json', encoding='utf-8') as f: by_word = json.load(f)
    r = []
    if q in by_word:
        for e in by_word[q]:
            if e['code']: r.append({'type':'精确','word':q,**e,'display':_fmt(e,'ICD-9-CM-3')})
    for kw, entries in by_word.items():
        if q in kw and kw != q and len(r) < 15:
            for e in entries:
                if e['code'] and not any(x.get('word')==kw for x in r):
                    r.append({'type':'包含','word':kw,**e,'display':_fmt(e,'ICD-9-CM-3')})
    return r

def lookup_surg_code(q):
    with open(f'{OUT_DIR}/surg_by_word.json', encoding='utf-8') as f: by_word = json.load(f)
    r = []
    for word, entries in by_word.items():
        for e in entries:
            if e['code'] and q in e['code']:
                r.append({'type':'code_match','code':e['code'],'word':word,'display':f'[手术主导词] {word}\n  ICD-9-CM-3: {e["code"]}'})
    return r[:15]

def lookup_clinical_term(q):
    """临床医学名词 → 国家临床版ICD-10编码"""
    with open(f'{OUT_DIR}/clinical_terms.json', encoding='utf-8') as f: data = json.load(f)
    r = []
    if q in data['by_name']:
        for e in data['by_name'][q]:
            also = f"\n  又称: {e['also']}" if e['also'] else ''
            former = f"\n  曾称: {e['former']}" if e['former'] else ''
            r.append({'type':'精确','name':q,**e,
                'display':f"【精确匹配】{q}\n  科室: {e['dept']}\n  英文: {e['ename']}{also}{former}\n  国家临床版ICD-10: {e['code']}  {e['icd_name']}"})
    for k, entries in data['by_name'].items():
        if q in k and k != q and len(r) < 12:
            for e in entries:
                if not any(x.get('name')==k for x in r):
                    r.append({'type':'包含','name':k,**e,
                        'display':f"【包含】{k}\n  科室: {e['dept']}\n  国家临床版ICD-10: {e['code']}  {e['icd_name']}"})
    return r

def lookup_clinical_code(q):
    """ICD-10编码 → 临床医学名词"""
    with open(f'{OUT_DIR}/clinical_terms.json', encoding='utf-8') as f: data = json.load(f)
    r = []
    for code, entries in data['by_code'].items():
        if q.upper() in code.upper():
            for e in entries:
                r.append({'type':'code','code':code,**e,
                    'display':f"【编码匹配】{code}  {e['icd_name']}\n  临床正名: {e['cname']}\n  科室: {e['dept']}\n  英文: {e['ename']}"})
    return r[:15]

def lookup_clinical_dept(q):
    """按科室查询临床术语"""
    with open(f'{OUT_DIR}/clinical_terms.json', encoding='utf-8') as f: data = json.load(f)
    r = []
    for dept, entries in data['by_dept'].items():
        if q in dept:
            r.append({'type':'dept','dept':dept,'count':len(entries),
                'display':f"【科室】{dept}（共{len(entries)}条术语）"})
    return r

# ─── CLI入口 ──────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('用法: python icd_lookup_tool.py <word|code|dept> <查询词> [--diag|--surg|--clinical]')
        print('诊断(ICD-10):  python icd_lookup_tool.py word 肺炎 --diag')
        print('诊断(ICD-10):  python icd_lookup_tool.py code I10 --diag')
        print('手术(ICD-9):   python icd_lookup_tool.py word 胆囊切除 --surg')
        print('临床术语映射:   python icd_lookup_tool.py word 肺癌 --clinical')
        print('临床编码映射:   python icd_lookup_tool.py code J18 --clinical')
        print('按科室查询:     python icd_lookup_tool.py dept 心内科 --clinical')
        sys.exit(1)
    mode, query = sys.argv[1], sys.argv[2]
    target = 'diag'
    for a in sys.argv[3:]:
        if a == '--surg': target = 'surg'
        if a == '--diag': target = 'diag'
        if a == '--clinical': target = 'clinical'
    if target == 'clinical':
        r = lookup_clinical_dept(query) if mode == 'dept' else (lookup_clinical_code(query) if mode == 'code' else lookup_clinical_term(query))
    elif target == 'diag':
        r = lookup_diag_word(query) if mode == 'word' else lookup_diag_code(query)
    else:
        r = lookup_surg_word(query) if mode == 'word' else lookup_surg_code(query)
    if not r:
        print(f'未找到 "{query}" 的相关结果')
    else:
        for item in r:
            tag = f'【{item.get("type","")}】' if item.get('type') else ''
            print(f'{tag} {item["display"]}')
            print()
