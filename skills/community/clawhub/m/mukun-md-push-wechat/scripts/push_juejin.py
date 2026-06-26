#!/usr/bin/env python3
"""
掘金草稿箱推送脚本：Markdown → 稀土掘金草稿箱

用法:
  # 新建草稿（默认）
  python3 push_juejin.py <input.md> [--title TITLE] [--digest DIGEST] [--category ID] [--tags IDS]

  # 更新已有草稿
  python3 push_juejin.py <input.md> --update DRAFT_ID [--title TITLE] [--digest DIGEST]

  # 查询标签
  python3 push_juejin.py --query-tags KEYWORD

  # 查询分类
  python3 push_juejin.py --query-categories

Markdown frontmatter 支持（YAML 区段）：
  ---
  title: 文章标题
  digest: 摘要（50-100字）
  category_id: "6809637769959178254"
  tag_ids: "6809640408797167623,6809640445233070098"
  cover_image: https://p1-juejin.byteimg.com/xxxxx
  ---
  # 文章标题

完整工作流:
  1. 读取 config.yaml 获取 juejin.cookie 和默认分类/标签
  2. 解析 Markdown frontmatter（标题、摘要、分类、标签）
  3. 扫描正文中的本地图片，尝试上传到掘金图床（通过 ImageX/gen_token）
  4. 替换 mark_content 中的本地图片为掘金 CDN URL
  5. 创建/更新草稿
"""

import hashlib
import hmac
import json
import os
import random
import re
import ssl
import sys
import zlib
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone

# ─── 配置路径 ───────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(os.path.expanduser("~/.md_push_wechat"), "config.yaml")
DRAFT_ID_FILE = os.path.join(os.path.expanduser("~/.md_push_wechat"), "juejin_draft_id.txt")
SUPPORTED_IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")

# 掘金 API 地址
JUEJIN_API = "https://api.juejin.cn"
IMAGEX_API = "https://imagex.bytedanceapi.com"

# 分类 ID 常量（可通过 --query-categories 在线获取最新列表）
CATEGORY_MAP = {
    "后端":      "6809637769959178254",
    "前端":      "6809637767543259144",
    "Android":   "6809635626879549454",
    "iOS":       "6809635626661445640",
    "人工智能":  "6809637773935378440",
    "AI":        "6809637773935378440",
    "开发工具":  "6809637771511070734",
    "工具":      "6809637771511070734",
    "代码人生":  "6809637776263217160",
    "阅读":      "6809637772874219534",
}


# ─── 配置加载 ───────────────────────────────────────────────

def load_config():
    """从 config.yaml 读取 juejin 配置"""
    if not os.path.exists(CONFIG_PATH):
        print(f"ERROR: 配置文件不存在: {CONFIG_PATH}")
        print("请创建配置文件并填写 juejin.cookie")
        print("参考: examples/config_example.yaml")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    config = {"cookie": "", "category_id": "", "tag_ids": ""}

    # 找到 juejin 段
    juejin_match = re.search(r'^juejin\s*:\s*$', content, re.MULTILINE)
    if not juejin_match:
        print("ERROR: config.yaml 中未找到 juejin 配置段")
        print("请参考 examples/config_example.yaml 添加 juejin 配置")
        sys.exit(1)

    # 提取 juejin 段内容（到下一个顶级 key 为止）
    juejin_start = juejin_match.end()
    juejin_section = content[juejin_start:]

    # 解析 key: value 对
    for line in juejin_section.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # 检查是否遇到下一个顶级 key（退出 juejin 段）
        if not line.startswith(" ") and not line.startswith("\t") and ":" in stripped:
            key = stripped.split(":")[0].strip()
            if key not in ("cookie", "category_id", "tag_ids"):
                break

        # 解析 cookie / category_id / tag_ids
        for field in ("cookie", "category_id", "tag_ids"):
            m = re.match(rf'^\s+{field}\s*:\s*(.+?)\s*(?:#.*)?$', line)
            if m:
                val = m.group(1).strip().strip("\"'")
                if val:
                    config[field] = val

    if not config["cookie"]:
        print("ERROR: 未找到 juejin.cookie 配置")
        print("请从浏览器登录掘金后，在 DevTools → Application → Cookies 中复制 Cookie")
        sys.exit(1)

    return config


def resolve_category(category_input: str) -> str:
    """将分类名称或 ID 转换为分类 ID"""
    if not category_input:
        return ""
    category_input = category_input.strip()
    # 纯数字 ID，直接返回
    if re.match(r'^\d+$', category_input):
        return category_input
    # 按名称查找
    return CATEGORY_MAP.get(category_input, category_input)


def resolve_tag_ids(tags_input: str) -> list:
    """将逗号分隔的标签 ID 串转为列表"""
    if not tags_input:
        return []
    return [t.strip() for t in tags_input.split(",") if t.strip()]


# ─── HTTP 请求 ──────────────────────────────────────────────

def api_request(method, url, data=None, cookie="", extra_headers=None, fatal=True):
    """通用 API 请求
    
    fatal=False 时不退出，返回 None 让调用方自行处理（用于图片上传等 best-effort 场景）
    """
    ctx = ssl.create_default_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://juejin.cn",
        "Referer": "https://juejin.cn/",
    }
    # GET/HEAD 请求不设 Content-Type（否则 ImageX API 返回 400）
    if method.upper() not in ("GET", "HEAD"):
        headers["Content-Type"] = "application/json; charset=utf-8"
    if cookie:
        headers["Cookie"] = cookie
    if extra_headers:
        headers.update(extra_headers)

    body = None
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"WARNING: HTTP {e.code} - {url.split('?')[0]}")
        if not fatal:
            return None


# 掘金 Web 客户端的固定 ID
JUEJIN_AID = "2608"
IMAGEX_SERVICE_ID = "73owjymdk6"

# ─── UUID 生成 ───────────────────────────────────────────────

def _generate_uuid():
    """生成 19 位随机 UUID（模拟掘金客户端 UUID）"""
    return str(random.randint(10**18, 10**19 - 1))


# ─── 图片上传（ImageX / gen_token） ─────────────────────────

def imagex_gen_token(uuid, cookie):
    """获取 ImageX 上传 STS Token

    接口：GET https://api.juejin.cn/imagex/v2/gen_token?aid=2608&uuid={uuid}&client=web

    返回 {AccessKeyId, SecretAccessKey, SessionToken} 或 None
    """
    url = f"{JUEJIN_API}/imagex/v2/gen_token?aid={JUEJIN_AID}&uuid={uuid}&client=web"
    ctx = ssl.create_default_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://juejin.cn",
        "Referer": "https://juejin.cn/",
        "Accept": "*/*",
        "Cookie": cookie,
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            if body.get("err_no", -1) != 0:
                print(f"WARNING: gen_token 失败: {body.get('err_msg', '未知错误')}")
                return None
            token_info = body.get("data", {}).get("token", {})
            return token_info
    except Exception as e:
        print(f"WARNING: gen_token 请求失败: {e}")
        return None


def _sigv4_sign(key, msg):
    """HMAC-SHA256 签名辅助"""
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _sigv4_auth(method, host, uri, query_params, body, timestamp, datestamp,
                sts_token, access_key, secret_key, region="cn-north-1", service="imagex"):
    """生成 AWS SigV4 Authorization 头

    掘金 ImageX 使用 AWS STS + SigV4 鉴权（从 HAR 逆向确认）。
    gen_token 返回临时 AccessKeyId/SecretAccessKey/SessionToken，
    后续 ApplyImageUpload/CommitImageUpload 必须用 SigV4 签名。

    query_params 为有序参数列表 [(k1, v1), (k2, v2), ...]（已经字母排序）。
    """
    # 按 key 字母排序构建 query string（AWS SigV4 要求）
    sorted_params = sorted(query_params, key=lambda x: x[0])
    query_string = urllib.parse.urlencode(sorted_params)

    canonical_headers = f"host:{host}\nx-amz-date:{timestamp}\nx-amz-security-token:{sts_token}\n"
    signed_headers = "host;x-amz-date;x-amz-security-token"
    payload_hash = hashlib.sha256(body if body else b"").hexdigest()

    canonical_request = (
        f"{method}\n{uri}\n{query_string}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    )
    hashed_cr = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()

    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{datestamp}/{region}/{service}/aws4_request"
    string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashed_cr}"

    k_date = _sigv4_sign(("AWS4" + secret_key).encode("utf-8"), datestamp)
    k_region = _sigv4_sign(k_date, region)
    k_service = _sigv4_sign(k_region, service)
    k_signing = _sigv4_sign(k_service, "aws4_request")
    signature = hmac.new(k_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    return f"{algorithm} Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}", query_string


def _imagex_auth_headers(method, host, uri, query_params, body, sts_token):
    """构建 ImageX 请求所需的鉴权 headers（SigV4 + x-amz-*）

    query_params 为有序参数列表 [(k1, v1), (k2, v2), ...]
    返回 (auth_headers_dict, query_string)
    """
    utc_now = datetime.now(timezone.utc)
    timestamp = utc_now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = utc_now.strftime("%Y%m%d")

    auth, query_string = _sigv4_auth(
        method, host, uri, query_params, body,
        timestamp, datestamp,
        sts_token.get("SessionToken", ""),
        sts_token.get("AccessKeyId", ""),
        sts_token.get("SecretAccessKey", ""),
    )
    return {
        "Authorization": auth,
        "x-amz-date": timestamp,
        "x-amz-security-token": sts_token.get("SessionToken", ""),
    }, query_string


def imagex_apply_upload(sts_token, filename):
    """申请 ImageX 上传地址

    接口：GET https://imagex.bytedanceapi.com/?Action=ApplyImageUpload&Version=2018-08-01&ServiceId=73owjymdk6

    返回 (upload_host, store_uri, auth, session_key) 或 (None,)*4
    """
    if not sts_token or not sts_token.get("SessionToken"):
        print("WARNING: STS Token 无效（缺少 SessionToken）")
        return None, None, None, None

    host = "imagex.bytedanceapi.com"
    params = [
        ("Action", "ApplyImageUpload"),
        ("ServiceId", IMAGEX_SERVICE_ID),
        ("Version", "2018-08-01"),
    ]
    auth_headers, query_string = _imagex_auth_headers("GET", host, "/", params, b"", sts_token)
    url = f"{IMAGEX_API}/?{query_string}"

    headers = {
        "Accept": "*/*",
        "Origin": "https://juejin.cn",
        "Referer": "https://juejin.cn/",
        **auth_headers,
    }
    resp = api_request("GET", url, cookie="", extra_headers=headers, fatal=False)

    if resp is None:
        return None, None, None, None

    result = resp.get("Result", {})
    upload_address = result.get("UploadAddress", {})
    upload_hosts = upload_address.get("UploadHosts", [])
    store_infos = upload_address.get("StoreInfos", [])
    session_key = upload_address.get("SessionKey", "")

    if upload_hosts and store_infos:
        host = upload_hosts[0]
        store_uri = store_infos[0].get("StoreUri", "")
        auth = store_infos[0].get("Auth", "")
        return host, store_uri, auth, session_key
    else:
        err = resp.get("ResponseMetadata", {}).get("Error", {})
        print(f"WARNING: ApplyImageUpload 响应异常: {err.get('Message', '无 UploadAddress')}")
        return None, None, None, None


def imagex_upload_file(upload_host, store_uri, auth, image_path):
    """上传文件二进制到 ImageX 存储节点

    接口：POST https://{upload_host}/{store_uri}
    """
    ctx = ssl.create_default_context()
    with open(image_path, "rb") as f:
        file_data = f.read()

    crc32_val = zlib.crc32(file_data) & 0xFFFFFFFF
    crc32_hex = f"{crc32_val:08x}"

    headers = {
        "Content-Type": "application/octet-stream",
        "Content-CRC32": crc32_hex,
        "Content-Disposition": 'attachment; filename="undefined"',
        "Content-Length": str(len(file_data)),
        "Origin": "https://juejin.cn",
        "Referer": "https://juejin.cn/",
        "Accept": "*/*",
    }
    if auth:
        headers["Authorization"] = auth

    upload_url = f"https://{upload_host}/{store_uri}"
    req = urllib.request.Request(upload_url, data=file_data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            resp_data = resp.read().decode("utf-8", errors="replace")
            return resp.status == 200
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"WARNING: 文件上传失败 HTTP {e.code}: {body[:200]}")
        return False
    except Exception as e:
        print(f"WARNING: 文件上传失败: {e}")
        return False


def imagex_commit_upload(sts_token, session_key, service_id):
    """确认上传完成

    接口：POST https://imagex.bytedanceapi.com/?Action=CommitImageUpload&SessionKey={sk}&ServiceId={sid}&Version=2018-08-01
    body 为空，鉴权用 SigV4
    """
    if not session_key:
        print("WARNING: SessionKey 为空，无法 commit")
        return None

    host = "imagex.bytedanceapi.com"
    sid = service_id or IMAGEX_SERVICE_ID
    params = [
        ("Action", "CommitImageUpload"),
        ("ServiceId", sid),
        ("SessionKey", session_key),
        ("Version", "2018-08-01"),
    ]
    auth_headers, query_string = _imagex_auth_headers("POST", host, "/", params, b"", sts_token)
    url = f"{IMAGEX_API}/?{query_string}"

    headers = {
        "Content-Length": "0",
        "Accept": "*/*",
        "Origin": "https://juejin.cn",
        "Referer": "https://juejin.cn/",
        **auth_headers,
    }

    resp = api_request("POST", url, cookie="", extra_headers=headers, fatal=False)
    if resp is None:
        return None

    results = resp.get("Result", {}).get("Results", [])
    if results:
        return results[0].get("Uri", "")
    return None


def imagex_get_img_url(uuid, store_uri, cookie):
    """获取图片最终 CDN URL

    接口：GET https://api.juejin.cn/imagex/v2/get_img_url?aid=2608&uuid={uuid}&uri={urlEncoded}&img_type=private

    返回 (main_url, backup_url) 或 (None, None)
    """
    encoded_uri = urllib.parse.quote(store_uri, safe="")
    url = (f"{JUEJIN_API}/imagex/v2/get_img_url"
           f"?aid={JUEJIN_AID}&uuid={uuid}"
           f"&uri={encoded_uri}&img_type=private")
    resp = api_request("GET", url, cookie=cookie, fatal=False)
    if resp is None:
        return None, None

    if resp.get("err_no", -1) != 0:
        print(f"WARNING: get_img_url 失败: {resp.get('err_msg', '')}")
        # 回退：根据 store_uri 拼出可能的 CDN URL
        return None, None

    data = resp.get("data", {})
    return data.get("main_url"), data.get("backup_url")


def upload_image_to_juejin(image_path, uuid, cookie):
    """上传单张图片到掘金图床，返回 (store_uri, cdn_url)

    流程（从 HAR 逆向分析）：
      1. gen_token  → 获取 STS Token（SessionToken）
      2. ApplyImageUpload → 获取上传地址（host + store_uri + SessionKey）
      3. POST 二进制文件到 tos-d-x-lf.douyin.com/{store_uri}
      4. CommitImageUpload → 确认上传
      5. get_img_url → 获取最终 CDN URL
    """
    if not os.path.exists(image_path):
        print(f"WARNING: 图片文件不存在: {image_path}")
        return None, None

    print(f"  上传图片: {os.path.basename(image_path)} ({os.path.getsize(image_path)//1024}KB)")

    # Step 1: gen_token
    sts_token = imagex_gen_token(uuid, cookie)
    if not sts_token:
        print(f"  WARNING: gen_token 失败")
        return None, None

    # Step 2: ApplyImageUpload
    host, store_uri, auth, session_key = imagex_apply_upload(sts_token, os.path.basename(image_path))
    if not host or not store_uri:
        print(f"  WARNING: ApplyImageUpload 失败")
        return None, None

    # Step 3: 上传二进制文件
    if not imagex_upload_file(host, store_uri, auth, image_path):
        print(f"  WARNING: 文件上传失败")
        return None, None

    # Step 4: CommitImageUpload
    committed_uri = imagex_commit_upload(sts_token, session_key, IMAGEX_SERVICE_ID)
    if not committed_uri:
        print(f"  WARNING: CommitImageUpload 失败")
        # 继续：即使 commit 失败也有可能上传成功了

    # Step 5: get_img_url → CDN URL
    uri_for_query = committed_uri or store_uri
    cdn_url, backup_url = imagex_get_img_url(uuid, uri_for_query, cookie)
    if not cdn_url:
        # 回退：手动构造可能的 CDN URL（不推荐，但兜底）
        clean_uri = uri_for_query.lstrip("/")
        cdn_url = f"https://p1-juejin.byteimg.com/{clean_uri}"

    print(f"  ✅ 上传成功: {cdn_url[:80]}...")
    return uri_for_query, cdn_url


# ─── 图片缓存（基于 config.yaml） ─────────────────────────

def _compute_file_hash(filepath):
    """计算文件内容 MD5，用于跨路径识别同一图片"""
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def _load_full_config():
    """读取 config.yaml 全部行"""
    if not os.path.exists(CONFIG_PATH):
        return []
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return f.readlines()


def _parse_image_cache(lines):
    """从 config.yaml 行列表中解析 image_cache 段

    返回: {"cover": {hash: media_id}, "content": {hash: url}, "juejin": {hash: cdn_url}}
    """
    cache = {"cover": {}, "content": {}, "juejin": {}}
    in_section = False
    in_subsection = None
    indent = None
    for line in lines:
        stripped = line.rstrip("\n").rstrip("\r")
        if re.match(r'^image_cache:\s*$', stripped):
            in_section = True
            indent = len(line) - len(line.lstrip())
            continue
        if not in_section:
            continue
        if not stripped or stripped.startswith("#"):
            continue
        # 检测是否已出 image_cache 段（缩进回到顶层）
        cur_indent = len(line) - len(line.lstrip())
        if cur_indent <= indent and not in_subsection:
            break
        # 检测子段
        for sub in ("cover", "content", "juejin"):
            if re.match(rf'^\s+{sub}:\s*$', stripped):
                in_subsection = sub
                break
        if in_subsection in ("cover", "content", "juejin"):
            continue
        # 解析键值对
        if in_subsection and cur_indent > indent + 2:
            kv_match = re.match(r'^\s+(\S+):\s*["\']?(\S+)["\']?\s*$', stripped)
            if kv_match:
                key, val = kv_match.group(1), kv_match.group(2).strip("\"'")
                if in_subsection in cache:
                    cache[in_subsection][key] = val
    return cache


def _save_image_cache_to_config(cache):
    """将 image_cache 写入 config.yaml

    缓存结构:
      image_cache:
        cover:
          <file_hash>: "<media_id>"
        content:
          <file_hash>: "<url>"
        juejin:
          <file_hash>: "<cdn_url>"

    1. 若已有 image_cache 段，替换之
    2. 若没有，追加到文件末尾
    3. 若缓存为空，删除 image_cache 段
    """
    lines = _load_full_config()

    # 找到 image_cache 段的位置
    section_start = -1
    section_end = -1
    for i, line in enumerate(lines):
        if re.match(r'^image_cache:\s*$', line.rstrip("\n")):
            section_start = i
            section_indent = len(line) - len(line.lstrip())
            for j in range(i + 1, len(lines)):
                stripped_l = lines[j].lstrip()
                if not stripped_l or stripped_l.startswith("#"):
                    continue
                cur_indent = len(lines[j]) - len(stripped_l)
                if cur_indent <= section_indent:
                    section_end = j
                    break
            if section_end == -1:
                section_end = len(lines)
            break

    # 构建新的 image_cache 段
    new_section = ["image_cache:\n"]
    for sub, label in [("cover", "cover"), ("content", "content"), ("juejin", "juejin")]:
        if cache.get(sub):
            new_section.append(f"    {label}:\n")
            for h, val in sorted(cache[sub].items()):
                new_section.append(f'        {h}: "{val}"\n')

    # 空缓存：移除 image_cache 段
    no_cache = not any(cache.get(k) for k in ("cover", "content", "juejin"))

    if section_start >= 0:
        if no_cache:
            lines = lines[:section_start] + lines[section_end:]
        else:
            lines = lines[:section_start] + new_section + lines[section_end:]
    elif not no_cache:
        if lines and not lines[-1].endswith("\n"):
            lines.append("\n")
        lines.append("\n")
        lines.extend(new_section)

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)


# ─── 正文图片解析与上传 ──────────────────────────────────────

def _normalize_image_token(token):
    """规范化图片标识文本用于模糊匹配"""
    token = token.strip().lower()
    token = os.path.splitext(token)[0]
    token = re.sub(r'[\s_\-]+', '', token)
    token = re.sub(r'[^\w\u4e00-\u9fff]', '', token)
    return token


def _list_local_images(md_file):
    """列出 Markdown 同级目录及子目录的候选图片文件"""
    md_dir = os.path.dirname(os.path.abspath(md_file)) or "."
    candidate_dirs = [md_dir, os.path.join(md_dir, "images"), os.path.join(md_dir, "assets")]
    image_paths = []
    for d in candidate_dirs:
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            path = os.path.join(d, name)
            if os.path.isfile(path) and name.lower().endswith(SUPPORTED_IMAGE_EXTS):
                image_paths.append(path)
    return image_paths


def _parse_md_image_target(target):
    """解析 Markdown 图片目标，处理可选 title 与 <...> 包裹语法"""
    target = target.strip()
    if not target:
        return ""
    angle_match = re.match(r'^<([^>]+)>(?:\s+["\'][^"\']*["\'])?$', target)
    if angle_match:
        return angle_match.group(1).strip()
    plain_match = re.match(r'^(\S+)(?:\s+["\'][^"\']*["\'])?$', target)
    if plain_match:
        return plain_match.group(1).strip()
    return target


def _resolve_image_to_file(md_file, img_target, img_alt, image_paths):
    """根据 Markdown 图片 target/alt 解析到本地文件路径"""
    md_dir = os.path.dirname(os.path.abspath(md_file)) or "."
    parsed = _parse_md_image_target(img_target)

    # 远程 URL
    if re.match(r'^https?://', parsed, re.IGNORECASE):
        return parsed, "remote"

    # 本地绝对/相对路径
    if parsed:
        unquoted = urllib.parse.unquote(parsed)
        direct = unquoted if os.path.isabs(unquoted) else os.path.join(md_dir, unquoted)
        if os.path.exists(direct) and os.path.isfile(direct):
            return os.path.abspath(direct), "path"

    # 按 alt 或 target 模糊匹配本地文件
    if not image_paths:
        return None, "missing"

    alt_key = _normalize_image_token(img_alt)
    target_key = _normalize_image_token(os.path.basename(parsed)) if parsed else ""
    keys = [k for k in [alt_key, target_key] if k]
    if not keys:
        return None, "missing"

    for k in keys:
        for path in image_paths:
            name_key = _normalize_image_token(os.path.basename(path))
            if k and (k == name_key or k in name_key or name_key in k):
                return os.path.abspath(path), "matched-alt"

    return None, "missing"


def replace_local_images(md_file, mark_content, uuid, cookie, enable_upload=True):
    """扫描 Markdown 中的本地图片，上传到掘金图床并替换引用

    基于文件内容 MD5 缓存到 config.yaml 的 image_cache.juejin 段，
    同一张图（即使路径不同）永久复用已上传的 CDN URL。

    返回: (updated_mark_content, upload_count, pics_list)
      - mark_content 中的本地引用替换为 CDN URL（如 https://p1-juejin.byteimg.com/xxx）
      - pics_list 为 [{pic_url: "完整CDN URL"}, ...]，用于文章 pics 字段
    """
    md_img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)\n]+)\)')
    refs = md_img_pattern.findall(mark_content)
    if not refs:
        return mark_content, 0, []

    image_paths = _list_local_images(md_file)
    lines = _load_full_config()
    cache = _parse_image_cache(lines)
    cache_updated = False
    replacements = {}  # old_src → cdn_url
    pics_list = []
    upload_count = 0

    for alt, target in refs:
        resolved, kind = _resolve_image_to_file(md_file, target, alt, image_paths)
        src_key = _parse_md_image_target(target).strip()
        if not src_key:
            continue

        if kind == "remote":
            # 已经是远程 URL，保持不变
            continue

        if not resolved or kind == "missing":
            print(f"  WARNING: 未找到本地图片文件: alt='{alt}', target='{target}'")
            continue

        if not enable_upload:
            print(f"  跳过图片上传（已禁用）: {os.path.basename(resolved)}")
            continue

        # 计算文件内容 MD5，查缓存
        fhash = _compute_file_hash(resolved)
        cached_url = cache["juejin"].get(fhash, "")
        if cached_url:
            print(f"  复用已缓存图片: {os.path.basename(resolved)} (hash: {fhash[:8]}...)")
            replacements[src_key] = cached_url
            pics_list.append({"pic_url": cached_url})
            upload_count += 1
            continue

        # 缓存未命中，上传图片
        store_uri, cdn_url = upload_image_to_juejin(resolved, uuid, cookie)
        if cdn_url:
            replacements[src_key] = cdn_url
            pics_list.append({"pic_url": cdn_url})
            upload_count += 1
            # 写入缓存
            cache["juejin"][fhash] = cdn_url
            cache_updated = True

    if cache_updated:
        _save_image_cache_to_config(cache)

    if not replacements:
        return mark_content, 0, []

    # 替换 mark_content 中的图片引用
    updated = mark_content
    for old_src, new_src in replacements.items():
        updated = updated.replace(f']({old_src})', f']({new_src})')
        encoded = urllib.parse.quote(old_src, safe="/:@+")
        updated = updated.replace(f']({encoded})', f']({new_src})')

    return updated, upload_count, pics_list


# ─── 草稿操作 ───────────────────────────────────────────────

def create_draft(title, mark_content, brief, category_id, tag_ids, cover_image, pics, uuid, cookie):
    """创建掘金草稿

    接口：POST https://api.juejin.cn/content_api/v1/article_draft/create?aid=2608&uuid={uuid}
    返回 draft_id
    """
    print(f"\n创建草稿: {title}")
    data = {
        "category_id": category_id or "0",
        "tag_ids": tag_ids or [],
        "link_url": "",
        "cover_image": cover_image or "",
        "is_gfw": 0,
        "title": title,
        "brief_content": brief,
        "is_english": 0,
        "is_original": 1,
        "edit_type": 10,  # Markdown 模式
        "html_content": "deprecated",
        "mark_content": mark_content,
        "theme_ids": [],
        "pics": pics or [],
    }

    url = f"{JUEJIN_API}/content_api/v1/article_draft/create?aid={JUEJIN_AID}&uuid={uuid}"
    resp = api_request("POST", url, data=data, cookie=cookie)

    err_no = resp.get("err_no", -1)
    if err_no != 0:
        # 处理嵌套错误
        inner_data = resp.get("data", {})
        inner_err = inner_data.get("err_no", 0) if isinstance(inner_data, dict) else 0
        if inner_err and inner_err != 0:
            print(f"ERROR: 创建草稿失败: {inner_data.get('err_msg', '未知错误')} (err_no={inner_err})")
        else:
            print(f"ERROR: 创建草稿失败: {resp.get('err_msg', '未知错误')} (err_no={err_no})")
        sys.exit(1)

    draft_id = resp["data"]["id"]
    print(f"✅ 草稿创建成功! draft_id: {draft_id}")
    print(f"   编辑地址: https://juejin.cn/editor/drafts/{draft_id}")

    # 保存 draft_id 供后续更新使用
    folder = os.path.dirname(DRAFT_ID_FILE)
    os.makedirs(folder, exist_ok=True)
    with open(DRAFT_ID_FILE, "w", encoding="utf-8") as f:
        f.write(draft_id)
    print(f"   draft_id 已保存到: {DRAFT_ID_FILE}")

    return draft_id


def update_draft(draft_id, title, mark_content, brief, category_id, tag_ids, cover_image, pics, uuid, cookie):
    """更新已有掘金草稿

    接口：POST https://api.juejin.cn/content_api/v1/article_draft/update?aid=2608&uuid={uuid}
    """
    print(f"\n更新草稿: {draft_id}")
    print(f"标题: {title}")

    data = {
        "id": draft_id,
        "category_id": category_id or "0",
        "tag_ids": tag_ids or [],
        "link_url": "",
        "cover_image": cover_image or "",
        "is_gfw": 0,
        "title": title,
        "brief_content": brief,
        "is_english": 0,
        "is_original": 1,
        "edit_type": 10,
        "html_content": "deprecated",
        "mark_content": mark_content,
        "theme_ids": [],
        "pics": pics or [],
    }

    url = f"{JUEJIN_API}/content_api/v1/article_draft/update?aid={JUEJIN_AID}&uuid={uuid}"
    resp = api_request("POST", url, data=data, cookie=cookie)

    err_no = resp.get("err_no", -1)
    if err_no != 0:
        print(f"ERROR: 更新草稿失败: {resp.get('err_msg', '未知错误')} (err_no={err_no})")
        sys.exit(1)

    print(f"✅ 草稿更新成功! draft_id: {draft_id}")


def query_tags(keyword="", limit=20):
    """查询掘金标签列表

    接口：POST https://api.juejin.cn/tag_api/v1/query_tag_list
    """
    print(f"查询标签（关键词: {keyword or '全部'}）...")
    data = {
        "cursor": "0",
        "key_word": keyword,
        "limit": limit,
        "sort_type": 1,
    }
    resp = api_request("POST", f"{JUEJIN_API}/tag_api/v1/query_tag_list", data=data)

    if resp.get("err_no", -1) != 0:
        print(f"ERROR: 查询标签失败: {resp.get('err_msg', '未知错误')}")
        sys.exit(1)

    tags = resp.get("data", [])
    if not tags:
        print("未找到标签")
        return

    print(f"\n找到 {len(tags)} 个标签:\n")
    print(f"  {'标签ID':<25} {'标签名称':<20} {'文章数':>8} {'关注数':>8}")
    print(f"  {'-'*25} {'-'*20} {'-'*8} {'-'*8}")
    for t in tags:
        tag = t.get("tag", {})
        tid = tag.get("tag_id", "")
        name = tag.get("tag_name", "")
        posts = tag.get("post_article_count", 0)
        followers = tag.get("concern_user_count", 0)
        print(f"  {tid:<25} {name:<20} {posts:>8} {followers:>8}")


def query_categories():
    """查询掘金文章分类列表

    接口：GET https://api.juejin.cn/tag_api/v1/query_category_briefs
    """
    print("查询掘金文章分类列表...")
    url = f"{JUEJIN_API}/tag_api/v1/query_category_briefs"
    try:
        resp = api_request("GET", url)
    except Exception as e:
        print(f"ERROR: 查询分类失败: {e}")
        sys.exit(1)

    if resp.get("err_no", -1) != 0:
        print(f"ERROR: 查询分类失败: {resp.get('err_msg', '未知错误')}")
        sys.exit(1)

    categories = resp.get("data", [])
    if not categories:
        print("未找到分类")
        return

    print(f"\n找到 {len(categories)} 个分类:\n")
    print(f"  {'category_id':<25} {'分类名称':<12} {'URL标识':<15}")
    print(f"  {'-'*25} {'-'*12} {'-'*15}")
    for c in categories:
        cid = str(c.get("category_id", ""))
        name = c.get("category_name", "")
        curl = c.get("category_url", "")
        print(f"  {cid:<25} {name:<12} {curl:<15}")

    print(f"\n💡 使用时传入 --category 后跟名称或 ID 即可，如：")
    print(f"   --category AI            # 按名称（支持中文/英文）")
    print(f"   --category 6809637773935378440  # 按 ID")


# ─── Markdown 解析 ──────────────────────────────────────────

def extract_frontmatter(md_file):
    """从 Markdown 文件提取 frontmatter 元数据

    支持字段：title, digest, category_id, tag_ids, cover_image
    """
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    meta = {
        "title": "",
        "digest": "",
        "category_id": "",
        "tag_ids": "",
        "cover_image": "",
    }

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            for line in fm.splitlines():
                for field in meta:
                    if line.strip().startswith(f"{field}:"):
                        val = line.split(":", 1)[1].strip().strip("\"'")
                        if val:
                            meta[field] = val

    # 回退：从 # 标题行提取
    if not meta["title"]:
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("# ") and not line.startswith("## "):
                meta["title"] = line[2:].strip()
                break

    if not meta["title"]:
        meta["title"] = os.path.splitext(os.path.basename(md_file))[0]

    return meta, content


def generate_brief(meta, body, min_len=50, max_len=100):
    """生成文章摘要（50-100字限制）"""
    # frontmatter 中已有 digest
    if meta.get("digest"):
        brief = meta["digest"]
        if min_len <= len(brief) <= max_len:
            return brief
        # 太短
        if len(brief) < min_len:
            plain = re.sub(r"[#*`>\[\]!]", "", body)
            plain = re.sub(r"\s+", " ", plain).strip()
            brief = (brief + " " + plain)[:max_len]
            return brief
        # 太长
        return brief[:max_len]

    # 自动生成摘要
    plain = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    plain = re.sub(r"[#*`>\[\]!]", "", plain)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) < min_len:
        return plain + " " * (min_len - len(plain))
    return plain[:max_len - 3] + "..."


# ─── 主入口 ─────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    args = sys.argv[1:]

    # --query-tags 模式
    if "--query-tags" in args:
        idx = args.index("--query-tags")
        keyword = ""
        if idx + 1 < len(args) and not args[idx + 1].startswith("--"):
            keyword = args[idx + 1]
        query_tags(keyword=keyword)
        return

    # --query-categories 模式
    if "--query-categories" in args:
        query_categories()
        return

    # 解析参数
    md_file = None
    title = None
    digest = None
    category = None
    tags_str = None
    cover = None
    update_mode = False
    update_draft_id = None

    i = 0
    while i < len(args):
        if args[i] == "--update":
            update_mode = True
            i += 1
            if i < len(args) and not args[i].startswith("--"):
                update_draft_id = args[i]
                i += 1
        elif args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--digest" and i + 1 < len(args):
            digest = args[i + 1]
            i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == "--tags" and i + 1 < len(args):
            tags_str = args[i + 1]
            i += 2
        elif args[i] == "--cover" and i + 1 < len(args):
            cover = args[i + 1]
            i += 2
        elif not md_file and not args[i].startswith("--"):
            md_file = args[i]
            i += 1
        else:
            i += 1

    if not md_file:
        print("ERROR: 请指定 Markdown 文件")
        print("用法: python3 push_juejin.py <input.md> [options]")
        sys.exit(1)

    if not os.path.exists(md_file):
        print(f"ERROR: 文件不存在: {md_file}")
        sys.exit(1)

    # 加载配置
    config = load_config()
    cookie = config["cookie"]

    # 解析 Markdown
    meta, full_content = extract_frontmatter(md_file)
    print(f"解析文件: {md_file}")

    # 优先级：命令行 > frontmatter > config.yaml
    final_title = title or meta.get("title", "")
    final_digest = digest or ""
    final_category = category or meta.get("category_id") or config.get("category_id", "")
    final_tags = tags_str or meta.get("tag_ids") or config.get("tag_ids", "")
    final_cover = cover or meta.get("cover_image", "")

    # 转换分类名称为 ID
    final_category = resolve_category(final_category)
    final_tag_list = resolve_tag_ids(final_tags)

    # 获取 Markdown 正文（去除 frontmatter）
    if full_content.startswith("---"):
        parts = full_content.split("---", 2)
        mark_content = parts[2].strip() if len(parts) >= 3 else full_content
    else:
        mark_content = full_content

    # 图片上传
    print(f"\n扫描并上传正文图片...")
    uuid = _generate_uuid()
    mark_content, upload_count, pics = replace_local_images(md_file, mark_content, uuid, cookie, enable_upload=True)
    if upload_count > 0:
        print(f"已上传 {upload_count} 张图片")

    # 生成摘要
    if final_digest:
        # 用户提供了摘要
        brief = final_digest
    else:
        brief = generate_brief(meta, full_content)

    # 输出摘要信息
    print(f"\n{'='*60}")
    print(f"  标题: {final_title}")
    print(f"  分类: {final_category or '（未指定）'}")
    print(f"  标签: {', '.join(final_tag_list) if final_tag_list else '（未指定）'}")
    print(f"  摘要: {brief[:60]}{'...' if len(brief) > 60 else ''}")
    print(f"  封面: {final_cover or '（无）'}")
    print(f"{'='*60}")

    # 创建或更新草稿
    if update_mode:
        if not update_draft_id:
            # 尝试从文件读取上次的 draft_id
            if os.path.exists(DRAFT_ID_FILE):
                with open(DRAFT_ID_FILE, "r", encoding="utf-8") as f:
                    update_draft_id = f.read().strip()
                print(f"从 juejin_draft_id.txt 读取 draft_id: {update_draft_id}")
            else:
                print("ERROR: --update 模式需要指定 draft_id")
                print("用法: python3 push_juejin.py <input.md> --update DRAFT_ID")
                sys.exit(1)

        update_draft(update_draft_id, final_title, mark_content, brief,
                     final_category, final_tag_list, final_cover,
                     pics, uuid, cookie)
        print(f"\n草稿已更新: https://juejin.cn/editor/drafts/{update_draft_id}")
    else:
        draft_id = create_draft(final_title, mark_content, brief,
                                final_category, final_tag_list, final_cover,
                                pics, uuid, cookie)
        print(f"\n完成! 草稿地址: https://juejin.cn/editor/drafts/{draft_id}")


if __name__ == "__main__":
    main()
