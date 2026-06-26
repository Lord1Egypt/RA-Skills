#!/usr/bin/env python3
"""
Music Weekly — Setup Script

Initializes everything needed for a new user:
  1. Creates ~/.config/music-weekly/config.json with sensible defaults
  2. Creates the Notion database with all required fields (optional)
  3. Creates the history log file
  4. Creates required directories
"""

import json, os, sys, urllib.request, argparse

# --- Constants ---

DEFAULT_CONFIG = {
    "notion_api_key": "",
    "notion_db_id": "",
    "delivery_channel": "telegram",
    "delivery_target": "",
    "covers_dir": os.path.expanduser("~/.openclaw/workspace/covers"),
    "media_dir": os.path.expanduser("~/.openclaw/media/qqbot"),
    "history_log": os.path.expanduser("~/.openclaw/workspace/music-recommended-log.md"),
    "sender_name": "🎵 音乐编辑",
}

CONFIG_DIR = os.path.expanduser("~/.config/music-weekly")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

NOTION_API_VERSION = "2025-09-03"

# Database property definitions
DB_PROPERTIES = {
    "名称":           {"title": {}},
    "艺术家":         {"rich_text": {}},
    "发行日期":       {"date": {}},
    "流派":           {"select": {"options": [
        {"name": "Indie Rock", "color": "blue"},
        {"name": "Electronic", "color": "purple"},
        {"name": "K-Pop", "color": "pink"},
        {"name": "Jazz", "color": "orange"},
        {"name": "Hip-Hop", "color": "red"},
        {"name": "R&B", "color": "yellow"},
        {"name": "Alternative", "color": "green"},
        {"name": "Pop", "color": "default"},
        {"name": "Classical", "color": "brown"},
        {"name": "Folk", "color": "gray"},
    ]}},
    "综合评分":       {"number": {"format": "number"}},
    "收听状态":       {"select": {"options": [
        {"name": "未听", "color": "default"},
        {"name": "已听", "color": "green"},
        {"name": "循环中", "color": "blue"},
        {"name": "想听", "color": "yellow"},
    ]}},
    "专辑类型":       {"select": {"options": [
        {"name": "全长", "color": "blue"},
        {"name": "EP", "color": "green"},
        {"name": "单曲", "color": "yellow"},
    ]}},
    "厂牌":           {"rich_text": {}},
    "评论来源":       {"rich_text": {}},
    "推荐短语":       {"rich_text": {}},
    "推荐理由":       {"rich_text": {}},
    "Apple Music链接": {"url": {}},
    "音乐分布":       {"multi_select": {"options": [
        {"name": "🇺🇸 美国", "color": "blue"},
        {"name": "🇬🇧 英国", "color": "purple"},
        {"name": "🇨🇦 加拿大", "color": "red"},
        {"name": "🇦🇺 澳大利亚", "color": "default"},
        {"name": "🇨🇳 中国", "color": "yellow"},
        {"name": "🇯🇵 日本", "color": "pink"},
        {"name": "🇰🇷 韩国", "color": "green"},
        {"name": "🇫🇷 法国", "color": "default"},
        {"name": "🇩🇪 德国", "color": "default"},
        {"name": "🇧🇷 巴西", "color": "green"},
    ]}},
    "周次":           {"rich_text": {}},
    "推送日期":       {"date": {}},
    "封面URL":        {"files": {}},
    "个人喜欢程度":   {"select": {"options": [
        {"name": "一般", "color": "default"},
        {"name": "喜欢", "color": "green"},
        {"name": "超爱", "color": "red"},
    ]}},
    "个人备注":       {"rich_text": {}},
}


def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def step(text, status="..."):
    print(f"  [{status}] {text}")


# --- Step 1: Config ---

def create_config(api_key="", parent_page_id="", channel="telegram", target=""):
    """Create config file with defaults."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    config = dict(DEFAULT_CONFIG)
    if api_key:
        config["notion_api_key"] = api_key
    if channel:
        config["delivery_channel"] = channel
    if target:
        config["delivery_target"] = target

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    step("Config file created", "✅")
    step(CONFIG_PATH, "📁")
    return config


# --- Step 2: Create directories ---

def create_dirs(config):
    """Create required directories if they don't exist."""
    dirs_to_create = [
        os.path.dirname(config["history_log"]),
        config["covers_dir"],
    ]
    # media_dir is only needed for qqbot, but create it anyway
    if config.get("media_dir"):
        dirs_to_create.append(config["media_dir"])

    for d in set(dirs_to_create):
        os.makedirs(d, exist_ok=True)
        step(f"{d}", "📁")
    step("Directories ready", "✅")


# --- Step 3: History log ---

def create_history_log(config):
    """Create the history log file with header if not exists."""
    path = config["history_log"]
    if os.path.exists(path):
        step(f"Already exists ({len(open(path).readlines())} lines)", "📄")
        return

    with open(path, "w") as f:
        f.write("# 音乐推荐记录（避免重复）\n")
        f.write("# 格式：周次期别 | 艺术家 - 专辑名 | 发行日期 | Apple Music ID | 推荐日期\n")
        f.write("# 每次推荐前先查此文件！\n")
    step(f"Created ({path})", "✅")


# --- Step 4: Create Notion database ---

def create_notion_database(api_key, parent_page_id):
    """
    Create the Notion database with all required fields.

    The database is created as a child of the given parent page.
    The user must have already shared the parent page with the integration.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }

    body = {
        "parent": {"page_id": parent_page_id},
        "title": [{"text": {"content": "🎵 音乐周报"}}],
        "properties": DB_PROPERTIES,
    }

    req = urllib.request.Request(
        "https://api.notion.com/v1/databases",
        data=json.dumps(body).encode(),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            db_id = data["id"]
            db_url = data.get("url", f"https://notion.so/{db_id.replace('-', '')}")
            print(f"\n  🎉 数据库创建成功！")
            print(f"  📋 名称：🎵 音乐周报")
            print(f"  🆔 UUID：{db_id}")
            print(f"  🔗 链接：{db_url}")
            return db_id
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        msg = err.get("message", str(e))
        print(f"\n  ❌ 创建失败: {msg}")
        print(f"\n  常见原因：")
        print(f"    1. parent_page_id 不对——确认页面已与集成共享")
        print(f"    2. 集成没权限——在页面上点⋯→「连接到」→选择你的集成")
        print(f"    3. API Key 不正确")
        return None


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Music Weekly — Initialize your music recommendation system"
    )
    parser.add_argument("--notion-key", help="Notion API key (starts with ntn_)")
    parser.add_argument("--parent-page", help="Notion page ID where to create the database")
    parser.add_argument("--channel", default="telegram",
                        help="Delivery channel (qqbot/telegram/discord/signal/wecom/feishu)")
    parser.add_argument("--target", help="Delivery target ID for the channel")
    parser.add_argument("--auto", action="store_true",
                        help="Auto mode: skip prompts, use defaults if not specified")

    args = parser.parse_args()

    print_header("🎵 Music Weekly — 初始化向导")
    print("  这个脚本将帮你完成首次配置。")
    print("  不传参数时进入交互模式，传参数则静默执行。")

    # --- Step 1: Config ---
    print_header("Step 1/4: 创建配置文件")

    api_key = args.notion_key or ""
    channel = args.channel or "telegram"
    target = args.target or ""
    parent_page = args.parent_page or ""

    if not args.auto and not api_key:
        print("\n  你的 Notion API Key 在哪里？")
        print("  1. 打开 https://notion.so/my-integrations")
        print("  2. 新建集成或复制已有集成的密钥")
        print("  3. 密钥以 ntn_ 开头\n")
        api_key = input("  请输入 Notion API Key: ").strip()

    if not args.auto and not target:
        print(f"\n  推送频道设为: {channel}")
        target = input(f"  请输入 {channel} 的目标 ID: ").strip()

    config = create_config(api_key, parent_page, channel, target)

    # --- Step 2: Dirs ---
    print_header("Step 2/4: 创建目录")
    create_dirs(config)

    # --- Step 3: History log ---
    print_header("Step 3/4: 创建推荐记录文件")
    create_history_log(config)

    # --- Step 4: Notion database ---
    print_header("Step 4/4: 创建 Notion 数据库")

    db_id = config.get("notion_db_id", "")

    if not api_key:
        step("No API key provided, skipping", "⏭")
    elif db_id:
        step(f"Database already configured ({db_id[:12]}...)", "✅")
    elif not parent_page and not args.notion_key:
        step("No --parent-page provided, skipping (you can create manually)", "⏭")
        print("\n  手动创建指南：")
        print("  1. 在 Notion 中新建一个空白页面")
        print("  2. 命名为「🎵 音乐周报」")
        print("  3. 创建数据库（/database）并添加所需的列")
        print("  4. 从 URL 中复制 UUID 到配置文件")
    else:
        # We have an API key and parent page, try to create
        if not parent_page and args.notion_key:
            if not args.auto:
                parent_page = input("  请输入父页面 ID（数据库将创建在此页面下）: ").strip()

        if parent_page:
            print("  正在创建数据库...")
            new_db_id = create_notion_database(api_key, parent_page)
            if new_db_id:
                config["notion_db_id"] = new_db_id
                with open(CONFIG_PATH, "w") as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                step("Config updated with database ID", "✅")
        else:
            step("No parent page ID, skipping", "⏭")

    # --- Done ---
    print_header("✅ 初始化完成！")
    print(f"  配置文件：{CONFIG_PATH}")
    print(f"  未填的项可以随时编辑该文件。")
    print()
    print(f"  ▶ 验证配置：python3 scripts/notion_utils.py config")
    print(f"  ▶ 开始工作：按 workflow.md 中的步骤执行")
    print()

    # Show summary
    with open(CONFIG_PATH) as f:
        final_config = json.load(f)
    for k, v in final_config.items():
        hidden = v
        if k == "notion_api_key" and v:
            hidden = v[:12] + "..." + v[-4:]
        print(f"    {k}: {hidden or '—（待填写）'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
