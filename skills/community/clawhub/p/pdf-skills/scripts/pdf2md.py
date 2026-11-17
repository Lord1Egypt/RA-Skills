# -*- coding: utf-8 -*-
"""PDF -> Markdown (stable)"""
import sys, os, re, tempfile, datetime, hashlib, requests
from urllib.parse import unquote

def download(u):
    if u.startswith('http'):
        r = requests.get(u, timeout=60, headers={'User-Agent':'Mozilla/5.0'})
        return r.content
    with open(u, 'rb') as f:
        return f.read()

def extract(data):
    import fitz
    tmp = tempfile.mktemp(suffix='.pdf')
    with open(tmp, 'wb') as f:
        f.write(data)
    try:
        doc = fitz.open(tmp)
        pages = []
        for i in range(len(doc)):
            p = doc[i]
            text = p.get_text('text')
            imgs = p.get_images()
            scanned = len((text or '').strip()) < 50 and len(imgs) > 0
            pages.append({
                'num': i+1,
                'text': text or '',
                'images': len(imgs),
                'scanned': scanned
            })
        doc.close()
        return pages
    finally:
        try:
            os.unlink(tmp)
        except:
            pass

def clean(text):
    if not text:
        return ""
    text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)
    text = re.sub(r'([\u4e00-\u9fff])\s+([a-zA-Z])', r'\1\2', text)
    text = re.sub(r'([a-zA-Z])\s+([\u4e00-\u9fff])', r'\1\2', text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = text.split('\n')
    lines = [l.rstrip() for l in lines]
    lines = [l for l in lines if not re.match(r'^\s*\d+\s*$', l.strip())]
    return '\n'.join(lines)

def seq_from_url(u):
    m = re.search(r'/(\d+)_', u)
    return m.group(1).zfill(2) if m else "00"

def sid_from_url(u):
    """从URL中提取标准号"""
    fname = u.split('/')[-1]
    for pat in [
        r'(DG-?TJ08-\d+(?:-\d+)?)',
        r'(DGTJ08-\d+(?:-\d+)?)',
        r'(DG-?TJ\d+-\d+(?:-\d+)?)',
        r'(DGTJ\d+-\d+(?:-\d+)?)',
        r'(CJJ[ -]?\d+(?:[ -]\d+)?)',
        r'(GB/?T?\d+(?:[ -]\d+)?)',
        r'(SHA\d+(?:[ -]\d+)?)',
        r'(DB31/?T?\d+(?:[ -]\d+)?)',
        r'(GA/?T?\d+(?:[ -]\d+)?)',
    ]:
        m = re.search(pat, fname, re.IGNORECASE)
        if m:
            sid = m.group(1)
            sid = re.sub(r'^DG/?TJ', 'DG-TJ', sid, flags=re.I)
            sid = re.sub(r'^DGTJ', 'DG-TJ', sid, flags=re.I)
            return sid.upper()
    return "Unknown"

def category_from_url(u):
    cats = [
        ('道路养护', ['道路', '沥青', '掘路', '桥梁', '人行道', '路面']),
        ('绿化养护', ['绿化', '园林', '行道树', '草坪', '立体绿化', '栽植土', '植物']),
        ('排水防汛', ['排水', '防汛', '管道', '污水']),
        ('市容环卫', ['保洁', '清扫', '市容', '环卫']),
        ('安全管理', ['文明施工', '安全']),
        ('交通设施', ['声屏障', '交通', '标志', '标线']),
    ]
    for cat, kw in cats:
        for k in kw:
            if k in u:
                return cat
    return '市政养护'

def title_from_url(u):
    if '/yanghu/' in u:
        fname = u.split('/')[-1]
        t = unquote(fname.replace('.pdf', ''))
        t = re.sub(r'[-_]+', ' ', t)
        t = re.sub(r'\s+', ' ', t).strip()
        return t
    return "Unknown"

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf2md.py <pdf_url_or_path> [output_md]")
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) >= 3 else None
    if not out:
        d = os.path.dirname(src) if os.path.exists(src) else '.'
        seq = seq_from_url(src)
        sid = sid_from_url(src)
        out = os.path.join(d, "%s_%s.md" % (seq, sid))

    print("Downloading...")
    data = download(src)
    print("Extracting...")
    pages = extract(data)
    print("Pages: %d" % len(pages))

    for p in pages:
        p['text'] = clean(p['text'])

    chars = sum(len(p['text']) for p in pages)
    scanned = sum(1 for p in pages if p['scanned'])
    pwt = sum(1 for p in pages if p['text'].strip())

    title = title_from_url(src)
    sid = sid_from_url(src)
    cat = category_from_url(src)
    sq = seq_from_url(src)

    print("Title: " + title)
    print("Standard: " + sid)

    body_parts = []
    for p in pages:
        if p['text'].strip():
            body_parts.append("## Page %d\n\n%s" % (p['num'], p['text']))
    body = '\n\n'.join(body_parts)

    md5 = hashlib.md5()
    md5.update(''.join(p['text'] for p in pages).encode('utf-8'))
    dh = md5.hexdigest()[:8]

    fm = []
    fm.append('---')
    fm.append('title: "' + title + '"')
    fm.append('standard_id: "' + sid + '"')
    fm.append('category: "' + cat + '"')
    fm.append('seq: "' + sq + '"')
    fm.append('date: "' + datetime.date.today().isoformat() + '"')
    fm.append('source: "' + src + '"')
    fm.append('doc_hash: "' + dh + '"')
    fm.append('pages_total: ' + str(len(pages)))
    fm.append('pages_with_text: ' + str(pwt))
    fm.append('pages_scanned: ' + str(scanned))
    fm.append('total_chars: ' + str(chars))
    fm.append('---')
    fm.append('')
    fm.append('# ' + title)
    fm.append('')
    fm.append('> Standard: ' + sid + ' | Category: ' + cat)
    fm.append('')
    fm.append('## Metadata')
    fm.append('')
    fm.append('| Item | Value |')
    fm.append('|-----|-----|')
    fm.append('| Total Pages | ' + str(len(pages)) + ' |')
    fm.append('| Pages with Text | ' + str(pwt) + ' |')
    if scanned > 0:
        fm.append('| Scanned Pages | ' + str(scanned) + ' |')
    fm.append('| Total Characters | ' + str(chars) + ' |')
    fm.append('')
    if scanned > 0:
        fm.append('> Note: %d pages are scanned images' % scanned)
        fm.append('')
    fm.append('## Content')
    fm.append('')

    md = '\n'.join(fm) + body

    with open(out, 'w', encoding='utf-8') as f:
        f.write(md)

    print("[OK] " + out + " (%.1fKB)" % (len(md) / 1024))

if __name__ == '__main__':
    main()
