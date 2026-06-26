#!/usr/bin/env python3
# modules/browser_crawl.py - 通过 OpenClaw 浏览器采集 tophub AI 专题
"""
此模块提供两种采集方式：
1. script_mode: 生成可被主会话执行的 browser 工具命令序列，写入 JSON
2. 主会话读取命令并执行，完成后结果写入输出文件
"""
import sys, os, json, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# 熊叔关心的 AI 专题节点
TOPHUB_PAGES = [
    ("36氪AI",     "https://tophub.today/n/x9oz2O1oXb"),
    ("量子位",     "https://tophub.today/n/MZd7azPorO"),
    ("AIbase",     "https://tophub.today/n/ENeYylkeY4"),
    ("AI产品榜",   "https://tophub.today/n/proPKWkeq6"),
    ("PM-AI学习库","https://tophub.today/n/DOvnyGpoEB"),
    ("掘金AI",     "https://tophub.today/n/rYqoXz8dOD"),
    ("超神经",     "https://tophub.today/n/4MdA863vxD"),
]

BROWSER_TARGET = "C3F681509ABEF4D998FA04FD8AA93869"
OUTPUT_FILE = os.path.join(DATA_DIR, "tophub_ai_raw.json")

# 每个页面的提取 JS（提取表格 tr）
EXTRACT_JS = """() => {
  const rows = document.querySelectorAll('table tbody tr');
  const data = [];
  rows.forEach((row, i) => {
    const cells = row.querySelectorAll('td');
    if (cells.length >= 2) {
      const titleEl = cells[1].querySelector('a');
      const raw = titleEl ? titleEl.innerText.trim() : cells[1].innerText.trim();
      // 分离标题和热度
      const hotMatch = raw.match(/([\\u4e00-\\u9fa5a-zA-Z0-9\\s《》\"\"''\\-()（）]+?)\\s*([\\d\\.]+\\s*[万亿]?)/);
      const title = hotMatch ? hotMatch[1].trim() : raw;
      const hot = hotMatch ? hotMatch[2].trim() : '';
      const link = titleEl ? (titleEl.href || '') : '';
      data.push({ rank: i+1, title, hot, link });
    }
  });
  return data.slice(0, 30);
}"""


def generate_browser_commands():
    """
    生成完整的 browser 工具调用序列，用于主会话执行。
    返回一个 dict，包含所有命令和元数据。
    """
    commands = []
    for name, url in TOPHUB_PAGES:
        nav_cmd = {
            "step": len(commands) + 1,
            "action": "navigate",
            "targetId": BROWSER_TARGET,
            "url": url,
            "description": f"导航到 {name}"
        }
        commands.append(nav_cmd)

        extract_cmd = {
            "step": len(commands) + 1,
            "action": "evaluate",
            "targetId": BROWSER_TARGET,
            "fn": EXTRACT_JS,
            "description": f"提取 {name} 表格数据"
        }
        commands.append(extract_cmd)

        wait_cmd = {
            "step": len(commands) + 1,
            "action": "wait",
            "timeMs": 1500,
            "description": f"等待 {name} 渲染"
        }
        commands.append(wait_cmd)

    # 最后一步：汇总写入文件
    write_cmd = {
        "step": len(commands) + 1,
        "action": "write_results",
        "platforms": [name for name, _ in TOPHUB_PAGES],
        "output_file": OUTPUT_FILE,
        "description": "将采集结果写入 JSON 文件"
    }
    commands.append(write_cmd)

    manifest = {
        "date": time.strftime("%Y-%m-%d"),
        "sources": [name for name, _ in TOPHUB_PAGES],
        "browser_target": BROWSER_TARGET,
        "commands": commands,
        "output_file": OUTPUT_FILE,
        "total_steps": len(commands),
    }
    return manifest


def write_manifest():
    """生成命令清单并写入文件，供主会话读取执行"""
    manifest = generate_browser_commands()
    manifest_file = os.path.join(DATA_DIR, "tophub_cmd_manifest.json")
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"✅ 命令清单已写入: {manifest_file}")
    print(f"   共 {manifest['total_steps']} 步，涵盖: {', '.join(manifest['sources'])}")
    print(f"   请在主会话中执行 browser 工具命令序列")
    print(f"   完成后结果写入: {OUTPUT_FILE}")
    return manifest


def read_results():
    """读取浏览器采集结果"""
    if not os.path.exists(OUTPUT_FILE):
        return None
    with open(OUTPUT_FILE, encoding='utf-8') as f:
        return json.load(f)


def merge_with_raw(raw, tophub_data):
    """将 tophub 数据合并到 raw 字典"""
    if not tophub_data:
        return raw

    merged = dict(raw)
    sources = tophub_data.get('sources', [])
    data = tophub_data.get('data', {})

    for source in sources:
        items = data.get(source, [])
        if items and source not in merged:
            merged[source] = items
        elif items:
            # 追加（去重）
            existing_titles = {i['title'] for i in merged[source]}
            for item in items:
                if item['title'] not in existing_titles:
                    merged[source].append(item)

    return merged


def run_standalone():
    """直接运行：生成命令清单（实际采集由主会话 browser 工具执行）"""
    manifest = write_manifest()
    print("\n📋 下一步：在主会话执行以下 browser 工具调用序列")
    print("   或使用 sessions_spawn 启动子 agent 处理浏览器操作\n")

    # 打印每个 navigate 命令
    for cmd in manifest['commands']:
        if cmd['action'] == 'navigate':
            print(f"   [{cmd['step']}] browser → navigate: {cmd['url']}")
        elif cmd['action'] == 'evaluate':
            print(f"   [{cmd['step']}] browser → evaluate (提取数据)")


if __name__ == '__main__':
    run_standalone()
