#!/usr/bin/env python3
"""MarketingForce T云 Website CMS Client - Full Featured

Usage:
  mf_client.py test                - Test token validity
  mf_client.py sites               - List all websites
  mf_client.py sitelist            - List all domains (console)

  # Article Management
  mf_client.py articles [page] [rows]  - List articles
  mf_client.py article <id>            - Get article detail
  mf_client.py save-article <json>     - Create/update article
  mf_client.py delete-article <id>     - Delete article
  mf_client.py categories              - List article categories

  # Product Management
  mf_client.py products [page] [rows]  - List products
  mf_client.py product <id>            - Get product detail
  mf_client.py product-cats            - List product categories
  mf_client.py product-tags            - List product tags

  # Short Video
  mf_client.py videos [page] [rows]    - List short videos

  # Recommendation
  mf_client.py keywords [page] [rows]  - List recommendation keywords
  mf_client.py anchors [page] [rows]   - List anchor points

  # Marketing/Inquiries
  mf_client.py forms [page] [rows]     - List forms
  mf_client.py inquiries [page] [rows] - List inquiry messages
  mf_client.py inquiry-stats           - Inquiry statistics

  # Resource Library
  mf_client.py images [page] [rows]    - List images
  mf_client.py image-dirs              - Image directory tree
  mf_client.py albums [page] [rows]    - List albums

  # Site Settings
  mf_client.py site-config             - Site configuration
  mf_client.py navigation              - Navigation menu
  mf_client.py menus                   - Page menu list
  mf_client.py theme                   - Current theme
  mf_client.py seo-params              - SEO parameters
  mf_client.py seo-tkd                 - TKD settings
  mf_client.py mail-config             - Mail config
  mf_client.py customer-service        - Customer service config
  mf_client.py plugins                 - All plugin settings

  # SEO
  mf_client.py seo-keywords [page]     - SEO keywords list
  mf_client.py seo-keyword-stats       - Keyword statistics
  mf_client.py forbidden-words         - Forbidden/sensitive words
  mf_client.py site-score              - Site evaluation score

  # Spider Analytics
  mf_client.py spider                  - Spider hot pages
  mf_client.py spider-trend            - Spider trend data

  # Dashboard
  mf_client.py dashboard               - Home dashboard
  mf_client.py site-diag               - Site diagnostics

  # Multi-Language
  mf_client.py languages               - Available languages

  # User Center
  mf_client.py members [page]          - Member list
  mf_client.py member-ranks            - Member ranks

  # AI
  mf_client.py ai-tasks [page]         - AI task list
  mf_client.py ai-extract [page]       - AI extract list

  # System
  mf_client.py system-logs [page]      - System logs
  mf_client.py backups                 - Backup list

  # Templates
  mf_client.py templates [page] [rows] - List site templates
"""
import json, os, sys, urllib.request, urllib.error, urllib.parse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")

CMS_BASE = "https://api.71360.com/api/app/site-admin-api/admin_cms"
ADMIN_BASE = "https://api.71360.com/api/app/site-admin-api/admin"
SITE_BASE = "https://api.71360.com/api/app/obor-nginx-php/tweb"
CONSOLE_BASE = "https://api.71360.com/api/app/aggregateservice-web/api"
PLUGIN_BASE = "https://api.71360.com/api/app/site-admin-api/plugin"
AI_BASE = "https://api.71360.com/api/app/site-admin-api/admin_ai"

def load_tokens():
    x_token = os.environ.get("MF_X_TOKEN", "")
    admin_token = os.environ.get("MF_ADMIN_TOKEN", "")
    if not x_token and os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line.startswith("MF_X_TOKEN="):
                    x_token = line.split("=", 1)[1]
                elif line.startswith("MF_ADMIN_TOKEN="):
                    admin_token = line.split("=", 1)[1]
    if not x_token:
        print("Error: MF_X_TOKEN not found. Create .env file.")
        sys.exit(1)
    return x_token, admin_token

def api_call(url, method="GET", data=None, params=None):
    x_token, admin_token = load_tokens()
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"X-Token": x_token, "Accept": "application/json"}
    if admin_token:
        headers["admin-token"] = admin_token
    if data:
        headers["Content-Type"] = "application/json"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except:
            return {"error": e.code}
    except Exception as e:
        return {"error": str(e)}

def pjson(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def get_info(data):
    """Extract info from nested data.info structure"""
    if isinstance(data, dict) and "info" in data:
        return data["info"]
    return data

# === Commands ===

def cmd_test():
    r = api_call(f"{CONSOLE_BASE}/Home/GetServerTime")
    print(f"Token valid! Server time: {r.get('data')}" if r.get("success") else f"Failed: {r}")

def cmd_sites():
    pjson(api_call(f"{SITE_BASE}/site/weblist"))

def cmd_sitelist():
    r = api_call(f"{CONSOLE_BASE}/Marketing/siteList", method="POST", data={"pageIndex": 1, "pageSize": 20})
    if r.get("code") == 200:
        for i in r["data"]:
            print(f"  [{i['DomainID']}] {i['Domain']} -> {i.get('MainUrl','')}")

def cmd_articles(page=1, rows=10):
    r = api_call(f"{CMS_BASE}/article/getlist", params={"type": 1, "rows": rows, "page": page, "disabled": "false"})
    if r.get("code") == 200 and r.get("data"):
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("rows", []):
            cat = i.get("relation_category", {}).get("name", "")
            print(f"  [{i['id']}] [{cat}] {i['title']}  (clicks:{i.get('click',0)})")

def cmd_article(aid):
    r = api_call(f"{CMS_BASE}/article/edit", params={"id": aid})
    if r.get("code") == 200 and r.get("data"):
        d = get_info(r["data"])
        for k in ["id","title","category_id","author","summary","img","status","sort","seo_title","seo_keywords","seo_description"]:
            print(f"{k}: {d.get(k, '')}")
        c = d.get("content", "")
        print(f"\ncontent ({len(c)} chars): {c[:300]}...")

def cmd_categories():
    r = api_call(f"{CMS_BASE}/category/getlist", params={"type": 1})
    if r.get("code") == 200:
        for i in r["data"].get("list", []):
            print(f"  [{i['id']}] {i['name']} (sort:{i.get('sort',0)}) url:{i.get('url','')}")

def cmd_products(page=1, rows=10):
    r = api_call(f"{CMS_BASE}/goods/getlist", params={"type": 2, "rows": rows, "page": page, "disabled": "false"})
    if r.get("code") == 200 and r.get("data"):
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("rows", []):
            t = i.get("relation_type", {}).get("name", "")
            print(f"  [{i['id']}] [{t}] {i['name']}  (clicks:{i.get('click',0)})")

def cmd_product(pid):
    r = api_call(f"{CMS_BASE}/goods/edit", params={"id": pid})
    if r.get("code") == 200 and r.get("data"):
        d = get_info(r["data"])
        for k in ["id","name","type_id","summary","img","price_sell","brand","sort","disabled","seo_title","seo_keywords","seo_description"]:
            print(f"{k}: {d.get(k, '')}")
        c = d.get("content", "")
        print(f"\ncontent ({len(c)} chars): {c[:300]}...")

def cmd_product_cats():
    r = api_call(f"{CMS_BASE}/goodsType/getlist", params={"type": 2})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("rows", []):
            print(f"  [{i['id']}] {i.get('name','')} (sort:{i.get('sort',0)})")

def cmd_product_tags():
    r = api_call(f"{CMS_BASE}/goodsTab/getlist", params={"type": 2})
    if r.get("code") == 200:
        pjson(r["data"])

def cmd_videos(page=1, rows=10):
    r = api_call(f"{CMS_BASE}/DyVideo/sVideoList", params={"rows": rows, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("list", []):
            print(f"  [{i.get('id')}] {i.get('title','')}")

def cmd_keywords(page=1, rows=10):
    r = api_call(f"{ADMIN_BASE}/keyword/list", params={"rows": rows, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("data", []):
            print(f"  [{i.get('id')}] {i.get('keyword', i.get('name',''))}")

def cmd_anchors(page=1, rows=10):
    r = api_call(f"{CMS_BASE}/AnchorPoint/anchorList", params={"rows": rows, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("data", []):
            print(f"  [{i.get('id')}] {i.get('keyword','')} -> {i.get('url','')}")

def cmd_forms(page=1, rows=10):
    r = api_call(f"{ADMIN_BASE}/form/getlist", params={"rows": rows, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("rows", []):
            print(f"  [{i.get('id')}] {i.get('name','')}")

def cmd_inquiries(page=1, rows=10):
    r = api_call(f"{ADMIN_BASE}/form/msglist", params={"rows": rows, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("rows", []):
            print(f"  [{i.get('id')}] {i.get('name','')} {i.get('phone','')} {i.get('email','')} | {i.get('content','')[:50]}")

def cmd_inquiry_stats():
    r = api_call(f"{ADMIN_BASE}/form/msgCount")
    pjson(r.get("data", r))

def cmd_images(page=1, rows=10):
    r = api_call(f"{ADMIN_BASE}/image", params={"rows": rows, "page": page})
    pjson(r.get("data", r))

def cmd_image_dirs():
    pjson(api_call(f"{ADMIN_BASE}/image/dirTree"))

def cmd_albums(page=1, rows=10):
    r = api_call(f"{CMS_BASE}/album/getlist", params={"rows": rows, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("rows", []):
            print(f"  [{i.get('id')}] {i.get('name','')}")

def cmd_site_config():
    r = api_call(f"{ADMIN_BASE}/SysConfig/siteConfig")
    if r.get("code") == 200:
        d = r["data"]
        for k in ["title","ico_pic","no_copy","keywords_lib","verify","ban_right","site_icp","site_police"]:
            if k in d:
                print(f"  {k}: {str(d[k])[:100]}")

def cmd_navigation():
    r = api_call(f"{ADMIN_BASE}/navigation")
    if r.get("code") == 200:
        for i in r["data"]:
            print(f"  [{i.get('id')}] {i.get('name','')} (sort:{i.get('sort',0)})")

def cmd_menus():
    r = api_call(f"{ADMIN_BASE}/menu/getlist")
    if r.get("code") == 200:
        for i in r["data"]:
            print(f"  [{i.get('id')}] {i.get('name','')}")

def cmd_theme():
    pjson(api_call(f"{ADMIN_BASE}/theme"))

def cmd_seo_params():
    r = api_call(f"{ADMIN_BASE}/SysConfig/seoParams")
    if r.get("code") == 200:
        for i in r["data"]:
            print(f"  {i}")

def cmd_seo_tkd():
    pjson(api_call(f"{ADMIN_BASE}/SysConfig/seoTkd"))

def cmd_mail_config():
    pjson(api_call(f"{ADMIN_BASE}/SysConfig/mailConfig"))

def cmd_customer_service():
    r = api_call(f"{ADMIN_BASE}/Sysconfig/getCustomerService")
    if r.get("code") == 200:
        d = r["data"]
        print(f"Position: {d.get('position')} Style: {d.get('style')}")
        for k, v in d.get("info", {}).items():
            print(f"  {k}: show={v.get('isShow')} sort={v.get('sort')}")

def cmd_plugins():
    plugins = ["floatvideo","floatphonebottom","baidushare","bizqq","location","xiongzhang","Xysen/floatqq","Xysen/sharebtn","ByteDanceVerify"]
    for p in plugins:
        name = p.split("/")[-1]
        r = api_call(f"{PLUGIN_BASE}/{p}/get") if "/" not in p else api_call(f"{PLUGIN_BASE}/{p}")
        code = r.get("code", "?")
        has_data = bool(r.get("data"))
        print(f"  [{code}] {name}: {'OK' if has_data else 'empty/no data'}")

def cmd_seo_keywords(page=1):
    r = api_call(f"{ADMIN_BASE}/Words/wordsList", params={"rows": 10, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("list", [])[:10]:
            print(f"  [{i.get('id')}] {i.get('keyword','')} rank:{i.get('rank',0)}")

def cmd_seo_keyword_stats():
    r = api_call(f"{ADMIN_BASE}/Words/wordsNum")
    pjson(r.get("data", r))

def cmd_forbidden_words():
    r = api_call(f"{ADMIN_BASE}/Words/forbiddenWords")
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)} sensitsumall: {d.get('sensitsumall', 0)}")

def cmd_site_score():
    r = api_call(f"{ADMIN_BASE}/SiteScore/status")
    print(f"Status: {r.get('data', {}).get('status', '?')}")
    r2 = api_call(f"{ADMIN_BASE}/SiteScore/evaluate")
    if r2.get("code") == 200:
        print(f"Evaluation: {r2.get('data', 'N/A')}")

def cmd_spider():
    r = api_call(f"{ADMIN_BASE}/Spider/hotTop")
    if r.get("code") == 200:
        for i in r["data"]:
            print(f"  [{i.get('id')}] spider:{i.get('spider_cnt_sum',0)} included:{i.get('included',0)} | {i.get('title','')}")
            print(f"       {i.get('url','')}")

def cmd_spider_trend():
    r = api_call(f"{ADMIN_BASE}/Spider/trendDataAverage")
    if r.get("code") == 200:
        d = r["data"]
        y = d.get("yesterday", {})
        t = d.get("thirty", {})
        print(f"Yesterday: {y.get('num',0)} spiders, avg {y.get('average',0)}")
        print(f"30 days: {t.get('num',0)} spiders, avg {t.get('average',0)}")

def cmd_dashboard():
    print("=== Site Setting State ===")
    r = api_call(f"{ADMIN_BASE}/home/siteSettingState")
    if r.get("code") == 200: pjson(r["data"])
    print("\n=== Statistics ===")
    r = api_call(f"{ADMIN_BASE}/home/statistics")
    if r.get("code") == 200: pjson(r["data"])
    print("\n=== Task List ===")
    r = api_call(f"{ADMIN_BASE}/home/taskList")
    if r.get("code") == 200: pjson(r["data"])

def cmd_site_diag():
    r = api_call(f"{ADMIN_BASE}/home/siteDiag")
    if r.get("code") == 200: pjson(r["data"])

def cmd_languages():
    r = api_call(f"{ADMIN_BASE}/SyncData/getLanguages")
    if r.get("code") == 200:
        for i in r["data"]:
            print(f"  {i}")
    r2 = api_call(f"{ADMIN_BASE}/language/list")
    print(f"\nActive languages: {r2.get('data', [])}")

def cmd_members(page=1):
    r = api_call(f"{ADMIN_BASE}/ucenterMember/list", params={"rows": 10, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("list", []):
            print(f"  {i}")

def cmd_member_ranks():
    r = api_call(f"{ADMIN_BASE}/ucenterMember/rankList")
    if r.get("code") == 200:
        for i in r["data"]:
            print(f"  [{i.get('id')}] {i.get('name','')}")

def cmd_ai_tasks(page=1):
    r = api_call(f"{AI_BASE}/taskList", params={"rows": 10, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("data", []):
            print(f"  [{i.get('id')}] {i.get('name', i.get('title',''))}")

def cmd_ai_extract(page=1):
    r = api_call(f"{CMS_BASE}/AiExtract/index", params={"rows": 10, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("data", []):
            print(f"  [{i.get('id')}] {i.get('name', i.get('title',''))}")

def cmd_system_logs(page=1):
    r = api_call(f"{ADMIN_BASE}/System/getLogList", params={"rows": 10, "page": page})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("data", [])[:10]:
            print(f"  [{i.get('id')}] {i.get('username','')} {i.get('action','')} | {i.get('addtime','')}")

def cmd_backups():
    pjson(api_call(f"{ADMIN_BASE}/System/backupList"))

def cmd_templates(page=1, rows=10):
    r = api_call(f"{SITE_BASE}/pub/tplist", params={"page": page, "rows": rows})
    if r.get("code") == 200:
        d = r["data"]
        print(f"Total: {d.get('total', 0)}")
        for i in d.get("list", []):
            print(f"  [{i['id']}] {i.get('theme_title','')} ({i.get('industryName','')}) selects:{i.get('select_number',0)}")

def cmd_save_article(json_file):
    with open(json_file) as f:
        article_data = json.load(f)
    r = api_call(f"{CMS_BASE}/article/save", method="POST", data=article_data)
    pjson(r)
    if r.get("code") == 200:
        print("\nArticle saved successfully!")

def cmd_delete_article(aid):
    pjson(api_call(f"{CMS_BASE}/article/remove", method="POST", data={"id": int(aid)}))

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    a = sys.argv
    cmds = {
        "test": lambda: cmd_test(),
        "sites": cmd_sites,
        "sitelist": cmd_sitelist,
        "articles": lambda: cmd_articles(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "article": lambda: cmd_article(int(a[2])),
        "save-article": lambda: cmd_save_article(a[2]),
        "delete-article": lambda: cmd_delete_article(a[2]),
        "categories": cmd_categories,
        "products": lambda: cmd_products(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "product": lambda: cmd_product(int(a[2])),
        "product-cats": cmd_product_cats,
        "product-tags": cmd_product_tags,
        "videos": lambda: cmd_videos(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "keywords": lambda: cmd_keywords(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "anchors": lambda: cmd_anchors(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "forms": lambda: cmd_forms(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "inquiries": lambda: cmd_inquiries(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "inquiry-stats": cmd_inquiry_stats,
        "images": lambda: cmd_images(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "image-dirs": cmd_image_dirs,
        "albums": lambda: cmd_albums(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
        "site-config": cmd_site_config,
        "navigation": cmd_navigation,
        "menus": cmd_menus,
        "theme": cmd_theme,
        "seo-params": cmd_seo_params,
        "seo-tkd": cmd_seo_tkd,
        "mail-config": cmd_mail_config,
        "customer-service": cmd_customer_service,
        "plugins": cmd_plugins,
        "seo-keywords": lambda: cmd_seo_keywords(int(a[2]) if len(a)>2 else 1),
        "seo-keyword-stats": cmd_seo_keyword_stats,
        "forbidden-words": cmd_forbidden_words,
        "site-score": cmd_site_score,
        "spider": cmd_spider,
        "spider-trend": cmd_spider_trend,
        "dashboard": cmd_dashboard,
        "site-diag": cmd_site_diag,
        "languages": cmd_languages,
        "members": lambda: cmd_members(int(a[2]) if len(a)>2 else 1),
        "member-ranks": cmd_member_ranks,
        "ai-tasks": lambda: cmd_ai_tasks(int(a[2]) if len(a)>2 else 1),
        "ai-extract": lambda: cmd_ai_extract(int(a[2]) if len(a)>2 else 1),
        "system-logs": lambda: cmd_system_logs(int(a[2]) if len(a)>2 else 1),
        "backups": cmd_backups,
        "templates": lambda: cmd_templates(int(a[2]) if len(a)>2 else 1, int(a[3]) if len(a)>3 else 10),
    }
    if cmd in cmds:
        cmds[cmd]()
    else:
        print(f"Unknown: {cmd}\n{__doc__}")

if __name__ == "__main__":
    main()
