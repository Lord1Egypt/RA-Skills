"""One-shot DRAFT-ONLY helper for Juejin.

SAFETY NOTES
------------
By default this helper ONLY creates a draft on the user's Juejin account.
It will NEVER publish publicly unless ALL of the following are true:

1. The caller explicitly passes the ``--publish`` command-line flag, AND
2. The environment variable ``JUEJIN_CONFIRM_PUBLISH=1`` is set, AND
3. The user types ``yes`` at the interactive confirmation prompt.

This three-factor gate is intentional: automated agents should never be
able to publish public content to a user's account without an explicit,
human-in-the-loop final approval step.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from juejin_skill.auth import JuejinAuth
from juejin_skill.publisher import ArticlePublisher


def _confirm_publish() -> bool:
    """Three-factor final approval gate before any public publish."""
    if os.environ.get("JUEJIN_CONFIRM_PUBLISH") != "1":
        print("⚠️  JUEJIN_CONFIRM_PUBLISH=1 is not set; staying in draft-only mode.")
        return False
    try:
        answer = input(
            "\n⚠️  You are about to PUBLISH PUBLICLY to the logged-in Juejin account.\n"
            "    Type 'yes' (all lowercase) to confirm, anything else cancels: "
        ).strip()
    except EOFError:
        # Non-interactive environment: refuse to publish.
        print("⚠️  No interactive TTY detected; refusing to publish.")
        return False
    return answer == "yes"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a DRAFT article on Juejin (draft-only by default)."
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help=(
            "Request public publishing after the draft is created. "
            "Still requires JUEJIN_CONFIRM_PUBLISH=1 and interactive 'yes' confirmation."
        ),
    )
    args = parser.parse_args()

    # Load cookie
    auth = JuejinAuth()
    cookie = auth.load_cookie()
    if not cookie:
        print("❌ No cookie found. Run login first.")
        return 1
    print("✅ Cookie loaded")

    # Initialize publisher
    pub = ArticlePublisher(cookie=cookie)

    # Get tags
    frontend_id = "6809637767543259144"
    tags = pub.search_tags(frontend_id)
    print(f"🏷️  Got {len(tags)} tags")
    for i, t in enumerate(tags[:10]):
        print(f"  [{i+1}] {t['tag_name']}")

    selected_tags = [tags[0]["tag_id"]] if tags else []

    # Article content
    content = """## 前言

这是一篇通过 **Juejin Skills** 自动发布工具发送的测试文章。

## 功能介绍

Juejin Skills 是一个基于 Python 的掘金操作工具集，支持：

- 🔥 **热门排行榜查询** - 获取各分类热门文章
- 📤 **文章自动发布** - Markdown 一键发布到掘金
- 📥 **文章下载** - 将掘金文章保存为 Markdown 格式

## 技术实现

- 使用 `httpx` 进行 API 调用
- 使用 `Playwright` 实现浏览器登录获取 Cookie
- 基于掘金官方 API 接口

## 总结

如果你觉得这个工具有用，欢迎 Star ⭐！
"""

    title = "Hello Juejin - 来自自动发布工具的测试文章"
    brief = "这是一篇通过 Juejin Skills 自动发布工具发送的测试文章"

    print("\n� Creating draft (draft-only mode)...")
    result = pub.publish_markdown(
        content=content,
        title=title,
        category_id=frontend_id,
        tag_ids=selected_tags,
        brief_content=brief,
        save_draft_only=True,
    )
    print(f"\n📋 Draft result: {json.dumps(result, indent=2, ensure_ascii=False)}")

    if not (result.get("success") and result.get("draft_id")):
        print("❌ Draft creation failed; aborting.")
        return 2

    draft_id = result["draft_id"]
    print(f"\n🎉 Draft created! draft_id={draft_id}")
    print("   Review it at https://juejin.cn/editor/drafts/<draft_id> before publishing.")

    if not args.publish:
        print("\nℹ️  Draft-only mode (default). Pass --publish to request public publishing.")
        return 0

    if not _confirm_publish():
        print("\n🛑 Public publish cancelled. The draft remains in your Juejin account.")
        return 0

    print("\n📤 Publishing draft publicly (explicitly confirmed by user)...")
    result2 = pub.publish_markdown(
        content=content,
        title=title,
        category_id=frontend_id,
        tag_ids=selected_tags,
        brief_content=brief,
        save_draft_only=False,
        allow_public_publish=True,
    )
    print(f"\n📋 Publish Result: {json.dumps(result2, indent=2, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
