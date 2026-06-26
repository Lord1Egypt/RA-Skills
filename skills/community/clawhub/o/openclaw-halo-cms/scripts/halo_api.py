#!/usr/bin/env python3
"""Halo CMS API client for OpenClaw agents."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import uuid
import re

HALO_URL = os.environ.get("HALO_URL", "http://localhost:8090")
HALO_USER = os.environ.get("HALO_USER", "")
HALO_PASS = os.environ.get("HALO_PASS", "")


def _load_env_halo():
    """Load credentials from .env.halo in workspace."""
    # Find workspace root (look for .env.halo)
    search_dirs = [
        os.environ.get("OPENCLAW_WORKSPACE", ""),
        os.getcwd(),
    ]
    # Also check parent directories
    cwd = os.getcwd()
    for _ in range(3):
        search_dirs.insert(0, cwd)
        parent = os.path.dirname(cwd)
        if parent == cwd:
            break
        cwd = parent

    user, pwd = "", ""
    for d in search_dirs:
        if not d:
            continue
        env_file = os.path.join(d, ".env.halo")
        if os.path.isfile(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("HALO_USER="):
                        user = line.split("=", 1)[1]
                    if line.startswith("HALO_PASS="):
                        pwd = line.split("=", 1)[1]
    return user, pwd


def _resolve_credentials():
    """Resolve Halo credentials. .env.halo takes priority over env vars."""
    # Priority: .env.halo > explicit HALO_USER/HALO_PASS env > fallback
    env_user, env_pass = _load_env_halo()
    if env_user and env_pass:
        return env_user, env_pass

    # Try loading from .env.halo
    env_user, env_pass = _load_env_halo()
    if env_user and env_pass:
        return env_user, env_pass
    if env_user and HALO_PASS:
        return env_user, HALO_PASS
    if env_pass and HALO_USER:
        return HALO_USER, env_pass

    # Fallback: global env vars or default
    if HALO_USER and HALO_PASS:
        return HALO_USER, HALO_PASS

    return HALO_USER or "thomasoscar", HALO_PASS


def _get_auth_header():
    """Return Authorization header using Basic Auth."""
    user, pwd = _resolve_credentials()
    if user and pwd:
        import base64
        creds = base64.b64encode(f"{user}:{pwd}".encode()).decode()
        return f"Basic {creds}"
    return ""


def api_request(method, path, body=None, raw=False):
    """Make an authenticated API request to Halo."""
    url = f"{HALO_URL}{path}"
    headers = {
        "Authorization": _get_auth_header(),
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            rdata = resp.read().decode()
            if resp.status == 204 or not rdata:
                return None
            if raw:
                return rdata
            return json.loads(rdata)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"API Error {e.code}: {error_body[:500]}", file=sys.stderr)
        sys.exit(1)


def slugify(text):
    """Convert Chinese/English text to URL-friendly slug."""
    text = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', text)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug[:80].strip('-') or str(uuid.uuid4())[:8]


def get_categories_map():
    """Fetch all categories and return {displayName: metadata.name} mapping."""
    data = api_request("GET", "/apis/api.content.halo.run/v1alpha1/categories")
    return {item["spec"]["displayName"]: item["metadata"]["name"]
            for item in data.get("items", [])}


def get_tags_map():
    """Fetch all tags and return {displayName: metadata.name} mapping."""
    data = api_request("GET", "/apis/api.content.halo.run/v1alpha1/tags")
    return {item["spec"]["displayName"]: item["metadata"]["name"]
            for item in data.get("items", [])}


def list_posts(args):
    """List published posts."""
    page = args.page or 0
    size = args.size or 20
    data = api_request("GET",
        f"/apis/api.content.halo.run/v1alpha1/posts?page={page}&size={size}"
        f"&sort=metadata.creationTimestamp,desc")
    posts = data.get("items", [])
    print(f"共 {data.get('total', 0)} 篇文章\n")
    for p in posts:
        title = p["spec"]["title"]
        slug = p["spec"]["slug"]
        name = p["metadata"]["name"]
        published = p["spec"]["publish"]
        status = "已发布" if published else "草稿"
        print(f"  [{status}] {title}  (/{slug})  id={name[:12]}...")


def list_categories(args):
    """List all categories."""
    data = api_request("GET", "/apis/api.content.halo.run/v1alpha1/categories")
    cats = data.get("items", [])
    print(f"共 {len(cats)} 个分类\n")
    for c in cats:
        name = c["spec"]["displayName"]
        slug = c["spec"]["slug"]
        print(f"  {name} (/{slug})")


def list_tags(args):
    """List all tags."""
    data = api_request("GET", "/apis/api.content.halo.run/v1alpha1/tags")
    tags = data.get("items", [])
    print(f"共 {len(tags)} 个标签\n")
    for t in tags:
        name = t["spec"]["displayName"]
        slug = t["spec"]["slug"]
        print(f"  {name} (/{slug})")


def create_post(args):
    """Create a new post (draft by default, publish with --publish flag)."""
    title = args.title
    content = args.content
    slug = args.slug or slugify(title)
    publish = args.publish
    user, _ = _resolve_credentials()

    # Check content safety (basic filter)
    _check_content_safety(title + content)

    html = markdown_to_html(content)

    # Resolve categories — auto-check existence
    cat_names = [c.strip() for c in (args.categories or "").split(",") if c.strip()]
    cat_uuids = []
    if cat_names:
        cat_map = get_categories_map()
        for cn in cat_names:
            if cn not in cat_map:
                print(f"错误：分类 '{cn}' 不存在。可选分类：", file=sys.stderr)
                list_categories(args)
                sys.exit(1)
            cat_uuids.append(cat_map[cn])
    else:
        # Auto-detect default category for current agent
        default_cat = _get_default_category()
        if default_cat:
            cat_map = get_categories_map()
            if default_cat in cat_map:
                cat_uuids.append(cat_map[default_cat])
                cat_names.append(default_cat)

    # Resolve tags — auto-create if not exists
    tag_names = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    tag_uuids = []
    if tag_names:
        tag_map = get_tags_map()
        for tn in tag_names:
            if tn not in tag_map:
                # Auto-create tag
                new_tag = api_request("POST",
                    "/apis/content.halo.run/v1alpha1/tags", {
                        "apiVersion": "content.halo.run/v1alpha1",
                        "kind": "Tag",
                        "metadata": {"name": str(uuid.uuid4())},
                        "spec": {"displayName": tn, "slug": slugify(tn)}
                    })
                if new_tag:
                    tag_uuids.append(new_tag["metadata"]["name"])
                    print(f"  自动创建标签：{tn}")
            else:
                tag_uuids.append(tag_map[tn])

    # Build content-json
    content_json = json.dumps({
        "content": html,
        "raw": content,
        "rawType": "markdown"
    })

    post_body = {
        "apiVersion": "content.halo.run/v1alpha1",
        "kind": "Post",
        "metadata": {
            "name": str(uuid.uuid4()),
            "annotations": {
                "content.halo.run/preferred-editor": "default",
                "content.halo.run/content-json": content_json,
            }
        },
        "spec": {
            "title": title,
            "slug": slug,
            "allowComment": True,
            "deleted": False,
            "excerpt": {"autoGenerate": True, "raw": ""},
            "htmlMetas": [],
            "owner": user,
            "pinned": False,
            "priority": 0,
            "publish": publish,
            "visible": "PUBLIC",
            "categories": cat_uuids,
            "tags": tag_uuids,
        }
    }

    result = api_request("POST",
        "/apis/uc.api.content.halo.run/v1alpha1/posts", post_body)
    if not result:
        print("错误：创建文章失败，API 返回空响应")
        sys.exit(1)
    post_name = result["metadata"]["name"]
    status = "已发布" if publish else "草稿"

    print(f"文章创建成功！")
    print(f"  标题：{title}")
    print(f"  状态：{status}")
    print(f"  Slug：/{slug}")
    if cat_names:
        print(f"  分类：{', '.join(cat_names)}")
    print(f"  ID：{post_name}")

    if not publish:
        print(f"\n提示：使用 publish_post --name {post_name} 来发布")


def publish_post(args):
    """Publish a draft post."""
    name = args.name
    result = api_request("PUT",
        f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/publish")
    if not result:
        print(f"文章已发布（或已是发布状态）：{name}")
        return
    print(f"文章已发布：{name}")
    if "spec" in result:
        print(f"  标题：{result['spec'].get('title', 'N/A')}")


def delete_post(args):
    """Recycle (soft delete) a post."""
    name = args.name
    result = api_request("PUT",
        f"/apis/api.console.halo.run/v1alpha1/posts/{name}/recycle")
    if not result:
        print(f"文章已移至回收站：{name}")
        return
    print(f"文章已移至回收站：{name}")


def reply_comment(args):
    """Reply to a comment."""
    comment_name = args.comment
    content = args.content
    _check_content_safety(content)
    body = {
        "spec": {
            "raw": content,
            "content": "<p>" + content + "</p>",
            "subjectRef": {
                "name": comment_name,
                "group": "content.halo.run",
                "version": "v1alpha1",
                "kind": "Comment"
            }
        }
    }
    result = api_request("POST",
        f"/apis/api.console.halo.run/v1alpha1/comments/{comment_name}/reply", body)
    if not result:
        print("回复成功！")
        return
    # Response may be the comment or a reply wrapper
    comment_obj = result.get("comment", result)
    reply_name = comment_obj.get("metadata", {}).get("name", "")
    print(f"回复成功！ 回复 ID：{reply_name}")


def delete_comment(args):
    """Delete a comment (move to recycle bin)."""
    comment_name = args.comment
    result = api_request("PUT",
        f"/apis/api.console.halo.run/v1alpha1/comments/{comment_name}/recycle")
    print(f"评论已删除（移至回收站）：{comment_name}")


def list_comments(args):
    """List recent comments, optionally filtered by post."""
    post_name = getattr(args, "post", None)
    path = "/apis/api.console.halo.run/v1alpha1/comments"
    if post_name:
        path += f"?sort=metadata.creationTimestamp,desc"
    else:
        path += f"?sort=metadata.creationTimestamp,desc&size=50"

    data = api_request("GET", path)
    comments = data.get("items", [])
    if not comments:
        print("暂无评论")
        return

    print(f"共 {data.get('total', len(comments))} 条评论\n")
    for c in comments:
        # Halo Console API returns: {comment: {spec, metadata}, owner: {...}, stats: {...}}
        comment_obj = c.get("comment", c)
        spec = comment_obj.get("spec", {})
        meta = comment_obj.get("metadata", {})
        owner_info = c.get("owner", spec.get("owner", {}))
        display_name = owner_info.get("displayName", "匿名") if isinstance(owner_info, dict) else str(owner_info)
        raw = spec.get("raw", "")
        # Strip HTML tags for display
        raw_text = re.sub(r'<[^>]+>', '', raw)
        status = spec.get("approved", False)
        status_str = "已审核" if status else "待审核"

        subject_ref = spec.get("subjectRef", {})
        comment_name = meta.get("name", "?")
        is_reply = spec.get("topCommentName", "") != ""

        indent = "    " if is_reply else ""
        print(f"{indent}[{status_str}] {display_name}: {raw_text[:60]}{'...' if len(raw_text)>60 else ''}")
        print(f"{indent}  id={comment_name[:12]}...  top={is_reply}")

        # Show subject (post title)
        subject = c.get("subject", {})
        post_title = subject.get("spec", {}).get("title", "")
        if post_title:
            print(f"{indent}  文章：《{post_title}》")

        # Show reply count
        comment_status = comment_obj.get("status", {})
        reply_count = comment_status.get("replyCount", c.get("stats", {}).get("upvote", 0))
        if reply_count > 0:
            print(f"{indent}  回复数：{reply_count}")


def check_new_comments(args):
    """Check for new/unreplied comments on current agent's posts."""
    # Get all posts
    posts_data = api_request("GET",
        "/apis/api.content.halo.run/v1alpha1/posts?size=100")
    posts = posts_data.get("items", [])

    # Get all comments
    comments_data = api_request("GET",
        "/apis/api.console.halo.run/v1alpha1/comments?size=100"
        "&sort=metadata.creationTimestamp,desc")
    comments = comments_data.get("items", [])

    # Build a map: topCommentName -> [replies]
    # Find top-level comments with no replies from current agent
    agent_user, _ = _resolve_credentials()

    pending = []
    for c in comments:
        # Halo Console API returns: {comment: {spec, metadata, status}, owner: {...}, subject: {...}}
        comment_obj = c.get("comment", c)
        spec = comment_obj.get("spec", {})
        meta = comment_obj.get("metadata", {})
        comment_status = comment_obj.get("status", {})

        # Skip replies (only look at top-level comments)
        if spec.get("topCommentName"):
            continue

        comment_name = meta.get("name", "")
        raw = spec.get("raw", "")
        raw_text = re.sub(r'<[^>]+>', '', raw)
        owner_info = c.get("owner", spec.get("owner", {}))
        display_name = owner_info.get("displayName", "匿名") if isinstance(owner_info, dict) else str(owner_info)

        # Check if this comment has any replies
        reply_count = comment_status.get("replyCount", 0)

        if reply_count == 0:
            # Find the post
            subject_ref = spec.get("subjectRef", {})
            post_name = subject_ref.get("name", "")
            post_title = "未知"
            for p in posts:
                if p["metadata"]["name"] == post_name:
                    post_title = p["spec"]["title"]
                    break

            pending.append({
                "comment_name": comment_name,
                "comment": raw_text,
                "author": display_name,
                "post_title": post_title,
            })

    if not pending:
        print("没有待回复的评论")
        return

    print(f"发现 {len(pending)} 条待回复评论：\n")
    for i, c in enumerate(pending, 1):
        print(f"{i}. [{c['author']}] 在《{c['post_title']}》中评论：")
        print(f"   {c['comment'][:100]}{'...' if len(c['comment'])>100 else ''}")
        print(f"   评论 ID：{c['comment_name']}")
        print()


def _get_default_category():
    """Auto-detect default category for current agent."""
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())
    if "xiaoyu" in workspace:
        return "小雨专栏"
    return "云小猫专栏"


def _check_content_safety(text):
    """Basic content safety check — reject dangerous content."""
    danger_patterns = [
        (r'(?:password|passwd|密码)\s*[:：=]\s*\S+', "密码/凭证"),
        (r'(?:api[_-]?key|secret[_-]?key|token)\s*[:：=]\s*\S+', "API Key/Token"),
        (r'(?:ssh|mysql|redis|postgres|mongodb)://\S+@\S+', "数据库连接串"),
        (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "IP 地址（可能）"),
    ]
    for pattern, label in danger_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            print(f"安全警告：内容中检测到可能的 {label}，请确认不会泄露敏感信息。",
                  file=sys.stderr)
            # Don't block, just warn


def markdown_to_html(text):
    """Very simple markdown to HTML conversion."""
    lines = text.split("\n")
    html_lines = []
    in_list = False
    in_code = False
    code_lines = []

    for line in lines:
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            if in_code:
                html_lines.append(f"<pre><code>{''.join(code_lines)}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(html_escape(line) + "\n")
            continue

        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        # Headers
        m = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if m:
            level = len(m.group(1))
            html_lines.append(f"<h{level}>{m.group(2)}</h{level}>")
            continue

        # List items
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{stripped[2:]}</li>")
            continue

        # Numbered list
        m = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if m:
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
            html_lines.append(f"<li>{m.group(2)}</li>")
            continue

        # Bold
        stripped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
        # Italic
        stripped = re.sub(r'\*(.+?)\*', r'<em>\1</em>', stripped)
        # Inline code
        stripped = re.sub(r'`(.+?)`', r'<code>\1</code>', stripped)
        # Links
        stripped = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', stripped)

        if in_list:
            html_lines.append("</ul>" if not re.match(r'^\d+\.', stripped) else "</ol>")
            in_list = False
        html_lines.append(f"<p>{stripped}</p>")

    if in_list:
        html_lines.append("</ul>")
    if in_code:
        html_lines.append(f"<pre><code>{''.join(code_lines)}</code></pre>")

    return "\n".join(html_lines)


def html_escape(text):
    """Escape HTML special characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    parser = argparse.ArgumentParser(description="Halo CMS API Client")
    sub = parser.add_subparsers(dest="command")

    # list_posts
    p = sub.add_parser("list_posts", help="列出文章")
    p.add_argument("--page", type=int, default=0)
    p.add_argument("--size", type=int, default=20)

    # list_categories
    sub.add_parser("list_categories", help="列出分类")

    # list_tags
    sub.add_parser("list_tags", help="列出标签")

    # create_post
    p = sub.add_parser("create_post", help="创建文章")
    p.add_argument("--title", required=True, help="文章标题")
    p.add_argument("--content", required=True, help="文章内容 (Markdown)")
    p.add_argument("--slug", help="URL 路径 (默认自动生成)")
    p.add_argument("--categories", help="分类 (逗号分隔，用 displayName)")
    p.add_argument("--tags", help="标签 (逗号分隔，不存在会自动创建)")
    p.add_argument("--publish", action="store_true", help="直接发布 (默认创建草稿)")

    # publish_post
    p = sub.add_parser("publish_post", help="发布草稿")
    p.add_argument("--name", required=True, help="文章 UUID")

    # delete_post
    p = sub.add_parser("delete_post", help="删除文章 (移至回收站)")
    p.add_argument("--name", required=True, help="文章 UUID")

    # reply_comment
    p = sub.add_parser("reply_comment", help="回复评论")
    p.add_argument("--comment", required=True, help="评论 UUID")
    p.add_argument("--content", required=True, help="回复内容")

    # delete_comment
    p = sub.add_parser("delete_comment", help="删除评论 (移至回收站)")
    p.add_argument("--comment", required=True, help="评论 UUID")

    # list_comments
    p = sub.add_parser("list_comments", help="列出评论")
    p.add_argument("--post", help="按文章 UUID 过滤")

    # check_new_comments
    sub.add_parser("check_new_comments", help="检查待回复评论")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "list_posts": list_posts,
        "list_categories": list_categories,
        "list_tags": list_tags,
        "create_post": create_post,
        "publish_post": publish_post,
        "delete_post": delete_post,
        "reply_comment": reply_comment,
        "delete_comment": delete_comment,
        "list_comments": list_comments,
        "check_new_comments": check_new_comments,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
