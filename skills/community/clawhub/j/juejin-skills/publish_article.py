"""Publish an article to Juejin - Full workflow script.

Usage:
    python publish_article.py
"""

import sys
import os

# Ensure the project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from juejin_skill.auth import JuejinAuth
from juejin_skill.publisher import ArticlePublisher


def main():
    print("=" * 60)
    print("  掘金文章发布工具")
    print("=" * 60)

    # ------------------------------------------------------------------ #
    # Step 1: Login / load cookie
    # ------------------------------------------------------------------ #
    auth = JuejinAuth()
    cookie = auth.load_cookie()

    if cookie:
        print("\n✅ 已检测到保存的 Cookie，正在验证...")
        # Quick validation
        from juejin_skill.api import JuejinAPI
        api = JuejinAPI(cookie=cookie)
        if api.is_authenticated():
            print("✅ Cookie 有效，无需重新登录。")
        else:
            print("⚠️  Cookie 已过期，需要重新登录。")
            cookie = ""
    
    if not cookie:
        print("\n🔐 即将打开浏览器，请在掘金页面完成登录（支持扫码、密码等方式）...")
        print("   登录成功后浏览器会自动关闭。\n")
        cookie = auth.login_with_browser(headless=False)
        if not cookie:
            print("❌ 登录失败或超时，请重试。")
            return

    # ------------------------------------------------------------------ #
    # Step 2: Initialize publisher and show categories
    # ------------------------------------------------------------------ #
    publisher = ArticlePublisher(cookie=cookie)

    print("\n📂 正在获取文章分类列表...")
    categories = publisher.get_categories()
    
    if not categories:
        print("⚠️  无法获取分类列表，将使用默认分类（前端）。")
        selected_category_id = "6809637767543259144"
        selected_category_name = "前端"
    else:
        print("\n可用分类：")
        for i, cat in enumerate(categories):
            print(f"  [{i+1}] {cat['category_name']} (ID: {cat['category_id']})")
        
        while True:
            choice = input(f"\n请选择分类编号 [1-{len(categories)}]（默认 1）: ").strip()
            if not choice:
                choice = "1"
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(categories):
                    selected_category_id = categories[idx]["category_id"]
                    selected_category_name = categories[idx]["category_name"]
                    break
                else:
                    print("编号无效，请重新输入。")
            except ValueError:
                print("请输入数字。")

    print(f"\n✅ 已选择分类: {selected_category_name}")

    # ------------------------------------------------------------------ #
    # Step 3: Search tags
    # ------------------------------------------------------------------ #
    print(f"\n🏷️  正在获取「{selected_category_name}」分类下的标签...")
    tags = publisher.search_tags(selected_category_id)
    
    selected_tag_ids = []
    if tags:
        print("\n热门标签（前 20）：")
        show_tags = tags[:20]
        for i, t in enumerate(show_tags):
            print(f"  [{i+1}] {t['tag_name']}")
        
        tag_input = input("\n请选择标签编号（多个用逗号分隔，如 1,3,5），回车跳过: ").strip()
        if tag_input:
            for part in tag_input.split(","):
                try:
                    tidx = int(part.strip()) - 1
                    if 0 <= tidx < len(show_tags):
                        selected_tag_ids.append(show_tags[tidx]["tag_id"])
                except ValueError:
                    pass
        if selected_tag_ids:
            print(f"✅ 已选择 {len(selected_tag_ids)} 个标签。")
    else:
        print("⚠️  未获取到标签，将跳过标签设置。")

    # ------------------------------------------------------------------ #
    # Step 4: Prepare article content
    # ------------------------------------------------------------------ #
    print("\n📝 准备文章内容...")
    
    # Check if user wants to publish from a file
    md_file = input("请输入 Markdown 文件路径（回车则使用示例文章）: ").strip()
    
    if md_file and os.path.isfile(md_file):
        filepath = md_file
        title_override = input("自定义标题（回车使用文件中的标题）: ").strip()
        brief = input("文章摘要（回车自动生成）: ").strip()

        mode = input(
            "\n发布模式？[d] 仅保存为草稿（默认） / [p] 公开发布: "
        ).strip().lower()
        publish_publicly = mode == "p"
        allow_public = False
        if publish_publicly:
            confirm = input(
                "⚠️  你即将公开发布到掘金账号，输入 'yes' 确认，其他任意键取消: "
            ).strip()
            if confirm != "yes":
                print("已取消公开发布，改为仅保存草稿。")
                publish_publicly = False
            else:
                allow_public = True

        result = publisher.publish_markdown(
            filepath=filepath,
            title=title_override if title_override else "",
            category_id=selected_category_id,
            tag_ids=selected_tag_ids,
            brief_content=brief,
            save_draft_only=not publish_publicly,
            allow_public_publish=allow_public,
        )
    else:
        if md_file and not os.path.isfile(md_file):
            print(f"⚠️  文件 {md_file} 不存在，将使用示例文章。\n")
        
        # Demo article
        title = input("请输入文章标题（回车使用示例标题）: ").strip()
        if not title:
            title = "Hello Juejin - 来自自动发布工具的测试文章"
        
        content = input("请输入文章内容（回车使用示例内容）: ").strip()
        if not content:
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

        brief = input("文章摘要（回车自动生成）: ").strip()

        # Default to draft-only; require an explicit opt-in for public publish.
        mode = input(
            "\n发布模式？[d] 仅保存为草稿（默认） / [p] 公开发布: "
        ).strip().lower()
        publish_publicly = mode == "p"
        allow_public = False
        if publish_publicly:
            confirm = input(
                "⚠️  你即将公开发布到掘金账号，输入 'yes' 确认，其他任意键取消: "
            ).strip()
            if confirm != "yes":
                print("已取消公开发布，改为仅保存草稿。")
                publish_publicly = False
            else:
                allow_public = True

        result = publisher.publish_markdown(
            content=content,
            title=title,
            category_id=selected_category_id,
            tag_ids=selected_tag_ids,
            brief_content=brief,
            save_draft_only=not publish_publicly,
            allow_public_publish=allow_public,
        )

    # ------------------------------------------------------------------ #
    # Step 5: Show result
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    if result.get("success"):
        print("🎉 发布成功！")
        if result.get("url"):
            print(f"   文章链接: {result['url']}")
        elif result.get("draft_id"):
            print(f"   草稿 ID: {result['draft_id']}")
        print(f"   消息: {result.get('message', '')}")
    else:
        print("❌ 发布失败！")
        print(f"   原因: {result.get('message', '未知错误')}")
        if result.get("raw"):
            print(f"   详细: {result['raw']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
