#!/usr/bin/env python3
"""
新闻/文章推送脚本：Markdown → 微信兼容 HTML → 草稿箱

用法:
  # 文章模式（默认）
  python3 push_daily.py <input.md> [--title TITLE] [--cover COVER_IMAGE] [--digest DIGEST] [--media-id MEDIA_ID]

  # 新闻模式
  python3 push_daily.py --news <input.md> [--title TITLE] [--cover COVER_IMAGE] [--digest DIGEST] [--media-id MEDIA_ID]

  # 更新已有草稿（追加 --update，注意 input.md 必须在 --update 之前，否则会被误判为 media_id）
  python3 push_daily.py <input.md> --update [--title TITLE] [--cover COVER_IMAGE] [--digest DIGEST]
  python3 push_daily.py <input.md> --update MEDIA_ID [--title TITLE] [--cover COVER_IMAGE] [--digest DIGEST]
  python3 push_daily.py --article <input.md> --update [--title TITLE] [--cover COVER_IMAGE] [--digest DIGEST]
  python3 push_daily.py --news <input.md> --update [--title TITLE] [--cover COVER_IMAGE] [--digest DIGEST]

Markdown frontmatter 支持（在文件顶部加 YAML 区段，可省去 --title 和 --digest 参数）：
  ---
  title: 文章标题
  digest: 手动摘要（80字以内）
  ---
  # 文章标题（仍是必填）

封面图处理:
- media_id 获取优先级：命令行 --media-id > config.yaml wechat.media_id > config.yaml image_cache.cover > 上传
- 封面图基于文件内容 MD5 缓存到 config.yaml 的 image_cache.cover 段，同一张图永久复用
- 正文图片基于文件内容 MD5 缓存到 config.yaml 的 image_cache.content 段
- 默认封面图: ~/.md_push_wechat/封面图.png
- 文章模式默认封面图: ~/.md_push_wechat/AI文章封面.png（如存在）
- 1:1 裁剪坐标固定为 "1008,0,1872,864"

完整工作流:
  1. Markdown → 微信兼容 HTML (md2wechat_html.py，默认文章模式，新闻模式时加 --news 参数)
  2. 上传封面图（首次）
  3. 上传正文图片素材并替换 HTML 引用（支持缓存复用）
  4. 推送草稿箱 / 更新已有草稿（--update）

"""

import hashlib
import json
import os
import re
import ssl
import sys
import subprocess
import urllib.parse
import urllib.request

# ─── 配置 ───────────────────────────────────────────────


CONFIG_PATH = os.path.join(os.path.expanduser("~/.md_push_wechat"), "config.yaml")
API_BASE = "https://api.weixin.qq.com"
COVER_MEDIA_ID_FILE = os.path.join(os.path.expanduser("~/.md_push_wechat"), "cover_media_id.txt")
ARTICLE_COVER_MEDIA_ID_FILE = os.path.join(os.path.expanduser("~/.md_push_wechat"), "article_cover_media_id.txt")
DEFAULT_COVER = os.path.join(os.path.expanduser("~/.md_push_wechat"), "封面图.png")
DEFAULT_ARTICLE_COVER = os.path.join(os.path.expanduser("~/.md_push_wechat"), "AI文章封面.png")
MD2WECHAT_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "md2wechat_html.py")
IMAGE_MAP_FILE = os.path.join(os.path.expanduser("~/.md_push_wechat"), "image_asset_map.json")  # 旧缓存文件，迁移后不再使用
DRAFT_MEDIA_ID_FILE = os.path.join(os.path.expanduser("~/.md_push_wechat"), "draft_media_id.txt")

SUPPORTED_IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")

# ─── 工具函数 ───────────────────────────────────────────

def load_credentials():
    """从 config.yaml 读取 wechat.appid 和 wechat.secret"""
    if not os.path.exists(CONFIG_PATH):
        print(f"ERROR: 配置文件不存在: {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    appid_match = re.search(r"appid:\s+(\S+)", content)
    secret_match = re.search(r"secret:\s+(\S+)", content)
    if not appid_match or not secret_match:
        print("ERROR: 无法从配置文件中读取 appid/secret")
        sys.exit(1)
    return appid_match.group(1).strip(), secret_match.group(1).strip()


def load_config_media_id():
    """从 config.yaml 读取 wechat.media_id（封面图的永久素材 ID）"""
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"media_id:\s*(\S+)", content)
    return match.group(1).strip() if match else None


def get_access_token(appid, secret):
    """获取微信 access_token"""
    ctx = ssl.create_default_context()
    url = f"{API_BASE}/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = json.loads(resp.read())
    if "access_token" not in data:
        print(f"ERROR: 获取 access_token 失败: {json.dumps(data, ensure_ascii=False)}")
        sys.exit(1)
    return data["access_token"]


def upload_image(access_token, image_path):
    """上传图片到永久素材库，返回 media_id"""
    ctx = ssl.create_default_context()
    filename = os.path.basename(image_path)
    with open(image_path, "rb") as f:
        file_data = f.read()
    
    boundary = "----WechatDraftBoundary7MA4YWxkTrZu0gW"
    body_parts = []
    body_parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n".encode("utf-8")
    )
    body_parts.append(file_data)
    body_parts.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(body_parts)
    
    url = f"{API_BASE}/cgi-bin/material/add_material?access_token={access_token}&type=image"
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req, context=ctx) as resp:
        result = json.loads(resp.read())
    
    if "media_id" not in result:
        print(f"ERROR: 封面图上传失败: {json.dumps(result, ensure_ascii=False)}")
        sys.exit(1)
    
    return result["media_id"]


def upload_content_image(access_token, image_path):
    """上传正文图片到微信永久素材库（图文消息图片接口），返回 URL

    使用 cgi-bin/material/add_material?type=image，上传到永久素材库。
    返回的 url 可直接用于图文消息正文中的 <img> src 属性。
    """
    ctx = ssl.create_default_context()
    filename = os.path.basename(image_path)
    with open(image_path, "rb") as f:
        file_data = f.read()

    boundary = "----WechatContentImageBoundary7MA4YWxkTrZu0gW"
    body_parts = []
    body_parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n".encode("utf-8")
    )
    body_parts.append(file_data)
    body_parts.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(body_parts)

    # 使用永久素材上传接口，type=image
    url = f"{API_BASE}/cgi-bin/material/add_material?access_token={access_token}&type=image"
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req, context=ctx) as resp:
        result = json.loads(resp.read())

    image_url = result.get("url")
    if not image_url:
        print(f"ERROR: 正文图片上传失败: {json.dumps(result, ensure_ascii=False)}")
        sys.exit(1)
    return image_url


# ─── 图片解析工具 ───────────────────────────────────────

def _normalize_image_token(token):
    """规范化图片标识文本（描述或文件名）用于匹配"""
    token = token.strip().lower()
    token = os.path.splitext(token)[0]
    token = re.sub(r'[\s_\-]+', '', token)
    token = re.sub(r'[^\w\u4e00-\u9fff]', '', token)
    return token


def _parse_md_image_target(target):
    """解析 Markdown 图片目标，兼容可选 title 与 <...> 包裹语法"""
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


def _list_local_images(md_file):
    """列出 Markdown 同级目录及 images/assets 子目录可候选图片"""
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


def _resolve_md_image_to_file(md_file, img_target, img_alt, image_paths):
    """根据 Markdown 图片 target/alt 自动解析到本地文件路径"""
    md_dir = os.path.dirname(os.path.abspath(md_file)) or "."
    parsed_target = _parse_md_image_target(img_target)

    # 1) 已经是远程地址，直接返回
    if re.match(r'^https?://', parsed_target, re.IGNORECASE):
        return parsed_target, "remote"

    # 2) target 是本地路径（相对/绝对）
    if parsed_target:
        unquoted = urllib.parse.unquote(parsed_target)
        direct_path = unquoted if os.path.isabs(unquoted) else os.path.join(md_dir, unquoted)
        if os.path.exists(direct_path) and os.path.isfile(direct_path):
            return os.path.abspath(direct_path), "path"

    # 3) 按描述（alt）匹配本地图片文件名
    if not image_paths:
        return None, "missing"

    alt_key = _normalize_image_token(img_alt)
    target_key = _normalize_image_token(os.path.basename(parsed_target)) if parsed_target else ""
    keys = [k for k in [alt_key, target_key] if k]
    if not keys:
        return None, "missing"

    for k in keys:
        for path in image_paths:
            name_key = _normalize_image_token(os.path.basename(path))
            if k and (k == name_key or k in name_key or name_key in k):
                return os.path.abspath(path), "matched-alt"

    return None, "missing"


# ─── 图片缓存（基于 config.yaml） ────────────────────────

def _compute_file_hash(filepath):
    """计算文件内容 MD5，用于跨路径识别同一图片"""
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def _load_full_config():
    """读取 config.yaml 全部内容，返回 (lines, wechat_section_start, wechat_section_end)"""
    if not os.path.exists(CONFIG_PATH):
        return [], -1, -1
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


def _parse_image_cache(lines):
    """从 config.yaml 行列表中解析 image_cache 段

    返回: {"cover": {hash: media_id}, "content": {hash: url}}
    """
    cache = {"cover": {}, "content": {}}
    # 找到 image_cache: 行
    in_section = False
    in_subsection = None  # 'cover' or 'content'
    indent = None
    for i, line in enumerate(lines):
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
        if cur_indent <= indent and in_section and not in_subsection:
            break
        # 检测子段
        cover_match = re.match(r'^\s+cover:\s*$', stripped)
        content_match = re.match(r'^\s+content:\s*$', stripped)
        if cover_match:
            in_subsection = "cover"
            continue
        if content_match:
            in_subsection = "content"
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

    1. 若已有 image_cache 段，替换之
    2. 若没有，追加到文件末尾
    """
    lines = _load_full_config()

    # 找到 image_cache 段的位置
    section_start = -1
    section_end = -1
    wechat_indent = 0
    for i, line in enumerate(lines):
        if re.match(r'^image_cache:\s*$', line.rstrip("\n")):
            section_start = i
            section_indent = len(line) - len(line.lstrip())
            # 查找该段结束位置（下一个同级或更上级的 key）
            for j in range(i + 1, len(lines)):
                stripped = lines[j].lstrip()
                if not stripped or stripped.startswith("#"):
                    continue
                cur_indent = len(lines[j]) - len(stripped)
                if cur_indent <= section_indent:
                    section_end = j
                    break
            if section_end == -1:
                section_end = len(lines)
            break
        if re.match(r'^wechat:\s*$', line.rstrip("\n")):
            wechat_indent = len(line) - len(line.lstrip())

    # 构建新的 image_cache 段
    new_section = []
    new_section.append("image_cache:\n")
    if cache.get("cover"):
        new_section.append("    cover:\n")
        for h, mid in sorted(cache["cover"].items()):
            new_section.append(f'        {h}: "{mid}"\n')
    if cache.get("content"):
        new_section.append("    content:\n")
        for h, url in sorted(cache["content"].items()):
            new_section.append(f'        {h}: "{url}"\n')

    # 空缓存：移除 image_cache 段
    no_cache = not cache.get("cover") and not cache.get("content")

    if section_start >= 0:
        if no_cache:
            # 删除 image_cache 段
            lines = lines[:section_start] + lines[section_end:]
        else:
            # 替换 image_cache 段
            lines = lines[:section_start] + new_section + lines[section_end:]
    elif not no_cache:
        # 追加到文件末尾（保留 trailing newline）
        if lines and not lines[-1].endswith("\n"):
            lines.append("\n")
        lines.append("\n")
        lines.extend(new_section)

    try:
        folder = os.path.dirname(CONFIG_PATH)
        os.makedirs(folder, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except (PermissionError, OSError) as e:
        print(f"WARNING: 无法保存图片缓存到 config.yaml: {e}")


def _migrate_old_image_cache():
    """将旧 image_asset_map.json 迁移到 config.yaml"""
    old_map = {}
    if os.path.exists(IMAGE_MAP_FILE):
        try:
            with open(IMAGE_MAP_FILE, "r", encoding="utf-8") as f:
                old_map = json.load(f)
        except Exception:
            pass

    if not old_map:
        return

    # 检查旧 map 中的每个文件是否存在，计算 hash 并迁移
    lines = _load_full_config()
    current_cache = _parse_image_cache(lines)
    migrated = 0

    for filepath, url in old_map.items():
        if not os.path.exists(filepath):
            continue
        try:
            fhash = _compute_file_hash(filepath)
        except Exception:
            continue
        if fhash not in current_cache["content"]:
            current_cache["content"][fhash] = url
            migrated += 1

    if migrated > 0:
        _save_image_cache_to_config(current_cache)
        print(f"已迁移 {migrated} 条旧图片缓存到 config.yaml")
        # 删除旧缓存文件
        try:
            os.remove(IMAGE_MAP_FILE)
            print(f"已删除旧缓存文件: {IMAGE_MAP_FILE}")
        except OSError:
            pass

    # 迁移旧封面图缓存 txt 文件
    for cache_file in [COVER_MEDIA_ID_FILE, ARTICLE_COVER_MEDIA_ID_FILE]:
        if not os.path.exists(cache_file):
            continue
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                old_media_id = f.read().strip()
        except Exception:
            continue
        if not old_media_id:
            continue
        # 尝试找到对应的封面图文件
        cover_paths = [DEFAULT_COVER, DEFAULT_ARTICLE_COVER]
        for cp in cover_paths:
            if not os.path.exists(cp):
                continue
            try:
                fhash = _compute_file_hash(cp)
            except Exception:
                continue
            if fhash not in current_cache["cover"]:
                current_cache["cover"][fhash] = old_media_id
                _save_image_cache_to_config(current_cache)
                print(f"已迁移封面图缓存到 config.yaml (hash: {fhash[:8]}...)")
        try:
            os.remove(cache_file)
        except OSError:
            pass


# ─── 正文图片解析 / 上传 ─────────────────────────────────

def _load_image_asset_map():
    """已弃用：图片缓存已迁移到 config.yaml 的 image_cache 段"""
    return {}


def _save_image_asset_map(image_map):
    """已弃用：图片缓存已迁移到 config.yaml 的 image_cache 段"""
    pass


def replace_local_images_with_wechat_assets(md_file, html_content, access_token):
    """上传 Markdown 内本地图片并替换 HTML 为微信素材 URL

    工作流：
    1. 从原始 Markdown 提取所有图片引用
    2. 解析到本地文件（支持相对路径、alt 模糊匹配）
    3. 计算文件内容 MD5，查 config.yaml image_cache.content
    4. 命中则复用 URL；未命中则上传到永久素材库并写入缓存
    5. 将 HTML 中的图片 src 替换为微信素材 URL
    """
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    md_img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)\n]+)\)')
    refs = md_img_pattern.findall(md_text)
    if not refs:
        return html_content

    image_paths = _list_local_images(md_file)
    lines = _load_full_config()
    cache = _parse_image_cache(lines)
    updated = False
    replacements = {}

    for alt, target in refs:
        resolved, source_kind = _resolve_md_image_to_file(md_file, target, alt, image_paths)
        src_key = _parse_md_image_target(target).strip()
        if not src_key:
            continue

        if source_kind == "remote":
            replacements[src_key] = resolved
            continue

        if not resolved:
            print(f"WARNING: 未找到图片文件，跳过: alt='{alt}', target='{target}'")
            continue

        fhash = _compute_file_hash(resolved)
        wechat_url = cache["content"].get(fhash, "")
        if not wechat_url:
            print(f"上传正文图片: {resolved}")
            wechat_url = upload_content_image(access_token, resolved)
            cache["content"][fhash] = wechat_url
            updated = True
            print(f"正文图片 URL: {wechat_url}")
        else:
            print(f"复用已缓存正文图片: {resolved} (hash: {fhash[:8]}...)")

        replacements[src_key] = wechat_url
        replacements[urllib.parse.quote(src_key, safe="/:@+")] = wechat_url
        replacements[urllib.parse.unquote(src_key)] = wechat_url

    if updated:
        _save_image_cache_to_config(cache)

    if not replacements:
        return html_content

    for old_src, new_src in replacements.items():
        html_content = html_content.replace(f'src="{old_src}"', f'src="{new_src}"')

    return html_content


# ─── 封面图 / 推送 ──────────────────────────────────────

def get_cover_media_id(access_token, cover_path, article_mode=False, cmd_media_id=None):
    """获取封面图 media_id

    优先级：命令行 --media-id > config.yaml wechat.media_id > config.yaml image_cache.cover > 上传

    封面图基于文件内容 MD5 缓存到 config.yaml image_cache.cover 段，
    同一张封面图无论路径如何变化都会被识别并复用。
    """
    # 1. 命令行指定的 media_id 优先级最高
    if cmd_media_id:
        print(f"使用命令行指定的 media_id: {cmd_media_id}")
        return cmd_media_id

    # 2. config.yaml 中配置的固定 media_id
    config_media_id = load_config_media_id()
    if config_media_id:
        print(f"使用 config.yaml 配置的 media_id: {config_media_id}")
        return config_media_id

    # 3. 检查封面图是否存在
    if not os.path.exists(cover_path):
        print(f"ERROR: 封面图不存在: {cover_path}")
        sys.exit(1)

    # 4. 查 config.yaml 缓存（基于文件内容 hash）
    lines = _load_full_config()
    cache = _parse_image_cache(lines)
    fhash = _compute_file_hash(cover_path)
    cached_media_id = cache["cover"].get(fhash, "")
    if cached_media_id:
        print(f"复用已缓存封面图 media_id: {cached_media_id} (hash: {fhash[:8]}...)")
        return cached_media_id

    # 5. 上传封面图并缓存
    print(f"上传封面图: {cover_path}")
    media_id = upload_image(access_token, cover_path)
    print(f"封面图 media_id: {media_id}")

    cache["cover"][fhash] = media_id
    _save_image_cache_to_config(cache)
    print(f"封面图缓存已保存到 config.yaml (hash: {fhash[:8]}...)")

    return media_id


# 硬编码的 1:1 裁剪坐标（用于成语典故系列封面）
# 封面图尺寸 2016×864，1:1 裁剪取中心竖条
# 格式：X1_Y1_X2_Y2（归一化坐标，0~1，下划线分隔）
# 计算：X1=1008/2016=0.5，Y1=0，X2=1872/2016≈0.928571，Y2=864/864=1
HARDCODED_PIC_CROP_1_1 = "0.5_0_0.928571_1"


def push_draft(access_token, title, html_content, thumb_media_id, cover_path="", digest=""):
    """推送草稿箱"""
    return _push_single_draft(access_token, title, html_content, thumb_media_id, cover_path, digest)


def _make_article(title, html_content, thumb_media_id, digest="", pic_crop_1_1=""):
    """构建单篇图文消息结构"""
    article = {
        "article_type": "news",
        "title": title,
        "content": html_content,
        "thumb_media_id": thumb_media_id,
        "author": "木昆子",
        "need_open_comment": 1,
        "only_fans_can_comment": 1,
    }
    if digest:
        article["digest"] = digest
    if pic_crop_1_1:
        article["pic_crop_1_1"] = pic_crop_1_1
    return article


def _push_single_draft(access_token, title, html_content, thumb_media_id, cover_path="", digest=""):
    """推送单篇草稿"""
    # 生成摘要
    if not digest:
        # 先移除 <style> 和 <script> 块，再去除 HTML 标签
        clean_html = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", html_content, flags=re.IGNORECASE)
        clean_html = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", clean_html, flags=re.IGNORECASE)
        plain_text = re.sub(r"<[^>]+>", "", clean_html)
        plain_text = re.sub(r"\s+", " ", plain_text).strip()
        digest = plain_text[:120] if len(plain_text) > 120 else plain_text

    print(f"标题: {title}")
    print(f"摘要: {digest[:50]}{'...' if len(digest) > 50 else ''}")
    print(f"内容长度: {len(html_content)} 字符")

    pic_crop_1_1 = HARDCODED_PIC_CROP_1_1 if cover_path else ""
    if pic_crop_1_1:
        print(f"封面图 1:1 裁剪坐标: {pic_crop_1_1}")

    article = _make_article(title, html_content, thumb_media_id, digest, pic_crop_1_1)
    payload = {"articles": [article]}

    ctx = ssl.create_default_context()
    url = f"{API_BASE}/cgi-bin/draft/add?access_token={access_token}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req, context=ctx) as resp:
        result = json.loads(resp.read())

    if result.get("errcode") and result["errcode"] != 0:
        print(f"ERROR: 推送失败: {json.dumps(result, ensure_ascii=False)}")
        sys.exit(1)

    media_id = result.get("media_id", "")
    print(f"✅ 推送成功! media_id: {media_id}")
    return media_id


def update_draft(access_token, media_id, title, html_content, thumb_media_id, cover_path="", digest="", index=0):
    """更新已有草稿（修改标题、正文、封面等）

    与 push_draft（新建）的区别：
    - API: cgi-bin/draft/update（而非 draft/add）
    - 需要 media_id（指定要修改的草稿）和 index（多图文中的位置）
    - articles 是单个对象而非数组
    """
    # 生成摘要
    if not digest:
        # 先移除 <style> 和 <script> 块，再去除 HTML 标签
        clean_html = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", html_content, flags=re.IGNORECASE)
        clean_html = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", clean_html, flags=re.IGNORECASE)
        plain_text = re.sub(r"<[^>]+>", "", clean_html)
        plain_text = re.sub(r"\s+", " ", plain_text).strip()
        digest = plain_text[:120] if len(plain_text) > 120 else plain_text

    print(f"更新草稿 media_id: {media_id}, index: {index}")
    print(f"标题: {title}")
    print(f"摘要: {digest[:50]}{'...' if len(digest) > 50 else ''}")
    print(f"内容长度: {len(html_content)} 字符")

    pic_crop_1_1 = HARDCODED_PIC_CROP_1_1 if cover_path else ""
    if pic_crop_1_1:
        print(f"封面图 1:1 裁剪坐标: {pic_crop_1_1}")

    article = _make_article(title, html_content, thumb_media_id, digest, pic_crop_1_1)

    # 更新接口：articles 是 object，不是 array
    payload = {
        "media_id": media_id,
        "index": index,
        "articles": article,
    }

    ctx = ssl.create_default_context()
    url = f"{API_BASE}/cgi-bin/draft/update?access_token={access_token}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req, context=ctx) as resp:
        result = json.loads(resp.read())

    if result.get("errcode") and result["errcode"] != 0:
        print(f"ERROR: 更新草稿失败: {json.dumps(result, ensure_ascii=False)}")
        sys.exit(1)

    print(f"✅ 草稿更新成功! media_id: {media_id}")
    return media_id


def extract_frontmatter(md_file):
    """从 Markdown 文件提取 frontmatter 元数据（标题、摘要等）

    支持 YAML frontmatter 格式：
    ---
    title: 标题
    digest: 摘要（可选，80字以内）
    ---
    """
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析 YAML frontmatter（纯字符串解析，不依赖 yaml 模块）
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_block = parts[1]
            title = ""
            digest = ""
            for line in frontmatter_block.splitlines():
                line = line.strip()
                if line.startswith("title:"):
                    title = line[6:].strip().strip("\"'")
                elif line.startswith("digest:"):
                    digest = line[7:].strip().strip("\"'")
            # digest 独立于 title 返回，不互相依赖
            if not title:
                # 从 # 标题行提取
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
            if not title:
                title = "未命名日报"
            return title, digest

    # 回退：直接从 # 标题行提取
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip(), ""
    return "未命名日报", ""


# ─── 主入口 ─────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    args = sys.argv[1:]
    article_mode = True  # 默认文章模式
    update_mode = False
    update_media_id = None
    no_title = True  # 默认去除标题块
    config_path = None

    # 识别模式参数
    if "--news" in args:
        article_mode = False
        args = [a for a in args if a != "--news"]
    if "--article" in args:
        article_mode = True
        args = [a for a in args if a != "--article"]
    if "--no-title" in args:
        no_title = True
        args = [a for a in args if a != "--no-title"]
    if "--with-title" in args:
        no_title = False
        args = [a for a in args if a != "--with-title"]
    # 解析 --config 参数
    if "--config" in args:
        config_idx = args.index("--config")
        if config_idx + 1 < len(args):
            config_path = args[config_idx + 1]
            args.pop(config_idx)  # 移除 --config
            args.pop(config_idx)  # 移除路径值
    if "--update" in args:
        update_mode = True
        update_idx = args.index("--update")
        args.pop(update_idx)
        # --update 后可能跟一个可选的 media_id
        if update_idx < len(args) and not args[update_idx].startswith("--"):
            update_media_id = args.pop(update_idx)

    if not args:
        print(__doc__.strip())
        sys.exit(1)

    md_file = args[0]
    title = None
    digest = None
    cover = None
    media_id = None

    i = 1
    while i < len(args):
        if args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--cover" and i + 1 < len(args):
            cover = args[i + 1]
            i += 2
        elif args[i] == "--digest" and i + 1 < len(args):
            digest = args[i + 1]
            i += 2
        elif args[i] == "--media-id" and i + 1 < len(args):
            media_id = args[i + 1]
            i += 2
        else:
            i += 1

    # 根据模式设定默认封面图
    if cover is None:
        if article_mode and os.path.exists(DEFAULT_ARTICLE_COVER):
            cover = DEFAULT_ARTICLE_COVER
        else:
            cover = DEFAULT_COVER

    if not os.path.exists(md_file):
        print(f"ERROR: Markdown 文件不存在: {md_file}")
        sys.exit(1)

    # 0. 迁移旧缓存到 config.yaml（首次自动执行）
    _migrate_old_image_cache()

    # 1. 生成微信兼容 HTML
    base = os.path.splitext(md_file)[0]
    if article_mode:
        html_file = f"{base}_article_wechat.html"
        mode_label = "文章模式"
        cmd = [sys.executable, MD2WECHAT_SCRIPT]
        if config_path:
            cmd.extend(["--config", config_path])
        if not no_title:  # 用户显式传递了 --with-title
            cmd.append("--with-title")
        cmd.extend(["--article", md_file, html_file])
    else:
        html_file = f"{base}_news_wechat.html"
        mode_label = "新闻模式"
        cmd = [sys.executable, MD2WECHAT_SCRIPT]
        if config_path:
            cmd.extend(["--config", config_path])
        if not no_title:  # 用户显式传递了 --with-title
            cmd.append("--with-title")
        cmd.extend(["--news", md_file, html_file])

    print(f"步骤 1: Markdown → 微信兼容 HTML（{mode_label}）")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"ERROR: HTML 生成失败:\n{result.stderr}")
        sys.exit(1)
    print(result.stdout.strip())

    # 读取 HTML 内容
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 2. 获取标题和摘要（优先 frontmatter > 命令行参数 > 自动截取）
    frontmatter_title, frontmatter_digest = extract_frontmatter(md_file)
    if not title:
        title = frontmatter_title
    if not digest:
        digest = frontmatter_digest
    if digest:
        print(f"摘要（frontmatter）: {digest}")

    # 3. 获取凭证并上传封面图
    print(f"\n步骤 2: 获取凭证并处理封面图")
    appid, secret = load_credentials()
    token = get_access_token(appid, secret)
    thumb_media_id = get_cover_media_id(token, cover, article_mode=article_mode, cmd_media_id=media_id)

    # 4. 正文图片上传与替换（支持缓存复用）
    print(f"\n步骤 3: 上传正文图片素材并替换引用")
    html_content = replace_local_images_with_wechat_assets(md_file, html_content, token)

    # 5. 推送 / 更新草稿箱
    if update_mode:
        if update_media_id:
            target_media_id = update_media_id
        elif os.path.exists(DRAFT_MEDIA_ID_FILE):
            with open(DRAFT_MEDIA_ID_FILE, "r", encoding="utf-8") as f:
                target_media_id = f.read().strip()
            print(f"从 draft_media_id.txt 读取上次草稿 media_id: {target_media_id}")
        else:
            print("ERROR: --update 模式下需要指定 media_id，或确保 draft_media_id.txt 存在")
            sys.exit(1)

        print(f"\n步骤 4: 更新草稿箱 (media_id: {target_media_id})")
        result_media_id = update_draft(token, target_media_id, title, html_content, thumb_media_id, cover_path=cover, digest=digest)

        print(f"\n完成! 草稿已更新: {result_media_id}")
    else:
        print(f"\n步骤 4: 推送草稿箱")
        result_media_id = push_draft(token, title, html_content, thumb_media_id, cover_path=cover, digest=digest)

        # 保存 media_id 供后续 --update 使用
        folder = os.path.dirname(DRAFT_MEDIA_ID_FILE)
        os.makedirs(folder, exist_ok=True)
        with open(DRAFT_MEDIA_ID_FILE, "w", encoding="utf-8") as f:
            f.write(result_media_id)
        print(f"草稿 media_id 已保存到: {DRAFT_MEDIA_ID_FILE}")

        print(f"\n完成! 草稿 media_id: {result_media_id}")


if __name__ == "__main__":
    main()
