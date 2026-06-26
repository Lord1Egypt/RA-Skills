#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
孔夫子拍卖搜索脚本 - 使用 xbrowser 自动化
用法: python kongfz_search_xbrowser.py --keyword "安康文字"
"""

import sys, io, os, subprocess, json, re, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

XB_PATH = r"C:\Program Files\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs"

def run_xb(args):
    """运行 xb 命令并返回 JSON 结果"""
    cmd = ["node", XB_PATH] + args
    print(f"[CMD] {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding='utf-8')
    output = result.stdout.strip()
    
    # xb batch 输出是一个大的 JSON 对象
    try:
        data = json.loads(output)
        return data
    except json.JSONDecodeError:
        # 如果不是纯 JSON，尝试找到 JSON 部分
        # 查找最后一个 { 开头的位置
        last_brace = output.rfind('\n{')
        if last_brace == -1:
            last_brace = output.find('{')
        if last_brace != -1:
            try:
                data = json.loads(output[last_brace:])
                return data
            except:
                pass
        return {"ok": False, "error": "No JSON found", "raw": output[:500]}

def search_auction(keyword, max_results=20):
    """搜索拍卖区拍品"""
    
    # Step 1: Init
    print("=== 初始化 xbrowser ===")
    result = run_xb(["init"])
    if not result.get("ok"):
        print(f"❌ 初始化失败: {result.get('error')}")
        return []
    
    # Step 2: 使用 batch 执行完整搜索流程
    print(f"=== 搜索关键词: {keyword} ===")
    
    batch_cmds = [
        "open 'https://search.kongfz.com/adv.html?type=pm'",
        "wait --load networkidle",
        "snapshot -i",
        f"fill @e21 {keyword}",
        "press Enter",
        "wait --load networkidle",
        "snapshot -i",
        "get text body"
    ]
    
    batch_args = ["run", "--browser", "cft", "batch", "--bail"] + batch_cmds
    result = run_xb(batch_args)
    
    if not result.get("ok"):
        print(f"❌ 搜索失败: {result.get('error', 'Unknown error')}")
        print(f"详情: {json.dumps(result, ensure_ascii=False)[:500]}")
        return []
    
    # 解析结果
    batch_result = result.get("data", {}).get("result", [])
    items = []
    body_text = ""
    
    for step in batch_result:
        cmd = step.get("command", [''])[0]
        if cmd == "get" and step.get("result", {}).get("text"):
            body_text = step["result"]["text"]
            print(f"\n=== 搜索结果页面文本（前3000字）===")
            print(body_text[:3000])
            break
        elif cmd == "snapshot" and step.get("result", {}).get("snapshot"):
            # 可以从 snapshot 中解析拍品
            snapshot_text = step["result"]["snapshot"]
            print(f"\n=== Snapshot 内容（前2000字）===")
            print(snapshot_text[:2000])
    
    if not body_text:
        print("⚠️ 未获取到页面文本")
        return []
    
    # 解析拍品信息
    items = parse_items(body_text, keyword)
    return items

def parse_items(text, keyword):
    """从页面文本中解析拍品信息"""
    items = []
    
    # 按行分割
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    current_item = {}
    for i, line in enumerate(lines):
        # 检测价格（￥开头）
        if line.startswith('￥'):
            if current_item:
                # 检查是否安康相关
                check_ankang(current_item, keyword)
                items.append(current_item)
                if len(items) >= 50:  # 限制数量
                    break
                current_item = {}
        # 检测拍品标题（heading 元素，较长文本）
        elif len(line) > 10 and '￥' not in line and '秒' not in line and '件在拍' not in line:
            if not current_item.get('title'):
                current_item['title'] = line
        # 检测作者
        elif line.startswith('作者:'):
            current_item['author'] = line.replace('作者:', '').strip()
        # 检测出版社
        elif line.startswith('出版社:') or line.startswith('出版人:'):
            current_item['publisher'] = line.split(':', 1)[1].strip() if ':' in line else ''
        # 检测剩余时间
        elif '时' in line and '分' in line and '秒' in line:
            current_item['time_left'] = line
        # 检测拍主
        elif '件在拍' in line:
            match = re.search(r'(.+)\s+\d+件在拍', line)
            if match:
                current_item['seller'] = match.group(1).strip()
    
    # 处理最后一个
    if current_item:
        check_ankang(current_item, keyword)
        items.append(current_item)
    
    return items

def check_ankang(item, keyword):
    """检查是否与关键词相关，标记优先级"""
    title = item.get('title', '')
    text = json.dumps(item, ensure_ascii=False)
    
    # 使用传入的 keyword 来判断
    if keyword in title or keyword in text:
        item['priority'] = 'high'
    elif '安康' in title or '安康' in text:
        item['priority'] = 'medium'
    else:
        item['priority'] = 'low'

def main():
    parser = argparse.ArgumentParser(description='孔夫子拍卖搜索')
    parser.add_argument('--keyword', default='安康文字', help='搜索关键词')
    parser.add_argument('--region', default='安康', help='地区筛选')
    parser.add_argument('--max', type=int, default=20, help='最大结果数')
    
    args = parser.parse_args()
    
    print(f"🔍 开始搜索孔夫子拍卖区...")
    print(f"   关键词: {args.keyword}")
    print(f"   地区筛选: {args.region}")
    print()
    
    items = search_auction(args.keyword, args.max)
    
    if not items:
        print("\n⚠️ 未找到相关拍品")
        return
    
    # 按优先级分类
    high = [i for i in items if i.get('priority') == 'high']
    medium = [i for i in items if i.get('priority') == 'medium']
    
    print(f"\n✅ 检索完成，共找到 {len(items)} 件拍品")
    print(f"   高优先级: {len(high)} 件")
    print(f"   中优先级: {len(medium)} 件")
    print()
    
    if high:
        print("📚 高优先级（立即提示）")
        for i, item in enumerate(high, 1):
            print(f"{i}. {item.get('title', 'N/A')}")
            if item.get('author'):
                print(f"   作者: {item['author']}")
            if item.get('time_left'):
                print(f"   剩余时间: {item['time_left']}")
            print()
    
    if medium:
        print("📋 中优先级（已记录）")
        for i, item in enumerate(medium, 1):
            print(f"{i}. {item.get('title', 'N/A')}")
            print()

if __name__ == '__main__':
    main()
