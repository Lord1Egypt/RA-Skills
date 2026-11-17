#!/usr/bin/env python3
"""美团API详情重抓 - 修复响应参数 + 新增方案↔API映射"""
from playwright.sync_api import sync_playwright
import re, json, os, time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
API_DETAIL_DIR = SKILL_DIR / "api_details"
SOLUTIONS_DIR = SKILL_DIR / "solutions"
REFERENCES_DIR = SKILL_DIR / "references"
API_DETAIL_DIR.mkdir(exist_ok=True)

TYPES = 'int|long|string|boolean|decimal|object|array<[^>]*>|float|double|date|json|number|bigint'
REQ_PAT = re.compile(rf'([a-z][a-zA-Z0-9]*?)({TYPES})?(\d*)(是|否)([\u4e00-\u9fa5，。、；：""''！？…—\u3000\-/a-zA-Z0-9%+()（）,.\s]+?)(?=[a-z][a-zA-Z0-9]*?(?:{TYPES})?\d*(?:是|否)|$)')
RESP_PAT = re.compile(rf'([a-z][a-zA-Z0-9]*?)({TYPES})([\u4e00-\u9fa5][\u4e00-\u9fa5，。、；：""''！？…—\u3000\-/a-zA-Z0-9%+()（）,.\s]*?)(?=[a-z][a-zA-Z0-9]*?(?:{TYPES})|$)')

def log(msg):
    print(msg, flush=True)

def parse_req(text):
    text = re.sub(r'^.*?示例值', '', text)
    return [{"name": m.group(1), "type": m.group(2) or "", "required": m.group(4) == "是",
             "description": m.group(5).strip().rstrip('0123456789').strip()}
            for m in REQ_PAT.finditer(text)]

def parse_resp(text):
    text = re.sub(r'^.*?示例值', '', text)
    return [{"name": m.group(1), "type": m.group(2) or "",
             "description": m.group(3).strip().rstrip('0123456789').strip()}
            for m in RESP_PAT.finditer(text)]

def path_to_url(p):
    return f"https://developer.meituan.com/docs/api/{p.replace('/', '-').lstrip('-')}"

def extract_paths():
    ap = {}
    for fn in sorted(os.listdir(REFERENCES_DIR)):
        if not fn.endswith("_API列表.md"): continue
        cat = fn.replace("_API列表.md", "")
        content = open(REFERENCES_DIR / fn).read()
        paths = sorted(set(p for p in re.findall(r'/rms/[a-zA-Z0-9/_\-]+', content) if len(p) > 10))
        ap[cat] = paths
    return ap

def extract_detail_fixed(page):
    c = page.text_content('body')
    d = {"method": "POST", "path": "", "request_params": [], "response_params": [], "response_example": ""}
    mp = re.search(r'(GET|POST)\s+(/rms/\S+)', c)
    if mp: d["method"], d["path"] = mp.group(1), mp.group(2)
    
    # 请求参数
    rs = c.find("业务请求参数")
    if rs < 0: rs = c.find("请求参数")
    if rs > 0:
        re2 = c.find("公共响应参数", rs)
        if re2 < 0: re2 = c.find("请求示例", rs)
        if re2 < 0: re2 = c.find("响应示例", rs)
        if re2 > rs: d["request_params"] = parse_req(c[rs:re2])
    
    # 响应参数 - FIX: 直接找"业务响应参数"
    rp = c.find("业务响应参数")
    if rp > 0:
        rp2 = c.find("请求示例", rp)
        if rp2 < 0: rp2 = c.find("响应示例", rp)
        if rp2 > rp: d["response_params"] = parse_resp(c[rp:rp2])
    
    # JSON示例
    es = c.find("响应示例")
    if es > 0:
        ee = c.find("异常示例", es)
        if ee < 0: ee = c.find("错误码", es)
        if ee < 0: ee = min(es + 3000, len(c))
        jm = re.search(r'\{[\s\S]*?"code"\s*:\s*"[^"]*"[\s\S]*?\n\}', c[es:ee])
        if not jm: jm = re.search(r'\{[\s\S]{50,2000}\}', c[es:ee])
        if jm: d["response_example"] = jm.group(0)[:3000]
    return d

def build_solution_api_mapping():
    """从12个解决方案文档中提取引用的API列表"""
    log("\n=== 方案↔API映射 ===")
    
    # 从各方案文档中提取API路径
    mapping = {}
    for fn in sorted(os.listdir(SOLUTIONS_DIR)):
        if not fn.endswith(".md"): continue
        content = open(SOLUTIONS_DIR / fn).read()
        sol_name = fn.replace(".md", "")
        
        # 查找API列表区域
        apis = []
        # 模式1: docs/api/xxx (完整文档链接)
        api_urls = re.findall(r'/docs/api/(rms-[^\s\)]+)', content)
        for u in api_urls:
            # rms-base-v1-auth-resources-poi-get → /rms/base/v1/auth/resources/poi/get
            path = '/' + u.replace('-', '/', 2).replace('v1/', 'v1/').replace('v2/', 'v2/').replace('v3/', 'v3/')
            # 更简单：把所有的 - 改成 /，去掉第一个 /
            parts = u.split('-')
            # 重建: rms -> /rms, 然后每个part
            path = '/' + '/'.join(parts)
            apis.append(path)
        
        # 模式2: /rms/xxx 直接引用的路径
        rms_paths = re.findall(r'(/rms/[a-zA-Z0-9/_\-]+)', content)
        apis.extend(rms_paths)
        
        # 去重
        apis = list(set(apis))
        
        if apis:
            mapping[sol_name] = apis
            log(f"  {sol_name}: {len(apis)} APIs")
    
    # 保存
    out = SKILL_DIR / "solution_api_mapping.json"
    out.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding='utf-8')
    log(f"  💾 {out} ({len(mapping)} 方案, {sum(len(v) for v in mapping.values())} 条映射)")
    return mapping

# === 主流程 ===
log("🦞 美团修复: 响应参数 + 方案映射")

# 1. 方案映射
build_solution_api_mapping()

# 2. 重抓响应参数
all_paths = extract_paths()
total = sum(len(v) for v in all_paths.values())

p = sync_playwright().start()
browser = p.chromium.launch(headless=True,
    args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
ctx = browser.new_context(
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36',
    viewport={'width': 1440, 'height': 900}, locale='zh-CN')
page = ctx.new_page()
page.add_init_script('''
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
    Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN','zh','en']});
''')

try:
    n = 0; summary = {}
    for cat, paths in all_paths.items():
        log(f"\n📦 {cat}: {len(paths)} APIs")
        results = []; t0 = time.time()
        
        for path in paths:
            n += 1
            url = path_to_url(path)
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=10000)
                page.wait_for_timeout(300)
                title = page.title()
                if 'Error' in title or '拦截' in title:
                    time.sleep(3)
                    page.goto(url, wait_until='domcontentloaded', timeout=10000)
                    page.wait_for_timeout(300)
                    title = page.title()
                detail = extract_detail_fixed(page)
                detail["title"] = title; detail["api_path"] = path; detail["doc_url"] = url
                results.append(detail)
                log(f"  [{n}/{total}] {title[:55]} | req={len(detail['request_params'])} resp={len(detail['response_params'])}")
            except Exception as e:
                log(f"  [{n}/{total}] ❌ {path}: {str(e)[:60]}")
                results.append({"api_path": path, "error": str(e)})
            time.sleep(0.3)
            if n % 50 == 0: time.sleep(2)
        
        out = API_DETAIL_DIR / f"{cat}.json"
        out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
        ok = len([r for r in results if 'request_params' in r])
        hr = sum(1 for r in results if r.get('response_params'))
        summary[cat] = {"total": len(results), "ok": ok, "resp_ok": hr, "elapsed": f"{time.time()-t0:.0f}s"}
        log(f"  💾 {cat}.json (req={ok} resp={hr})")

    (API_DETAIL_DIR / "_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    total_resp = sum(v['resp_ok'] for v in summary.values())
    log(f"\n📊 响应参数覆盖率: {total_resp}/{total}")

finally:
    browser.close()
    p.stop()
