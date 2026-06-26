#!/usr/bin/env python3
# hot-radar.py - 热点收集雷达 主程序
"""
Usage:
  python3 hot-radar.py --mode daily
  python3 hot-radar.py --mode daily --notify
  python3 hot-radar.py --mode analyze --date 2026-05-23
  python3 hot-radar.py --mode compare --platforms zhihu,weibo
  python3 hot-radar.py --mode keywords
"""
import sys, os, json, argparse, datetime as dt

# 设置翻墙代理（Clash HTTP 代理，7897端口）
os.environ.setdefault('HTTPS_PROXY', 'http://127.0.0.1:7897')
os.environ.setdefault('HTTP_PROXY', 'http://127.0.0.1:7897')

sys.path.insert(0, os.path.dirname(__file__))
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SKILL_DIR)
DATA_DIR  = os.path.join(SKILL_DIR, 'data')
REPORT_DIR = os.path.join(SKILL_DIR, 'reports')
CONFIG_DIR = os.path.join(SKILL_DIR, 'config')

for _d in [DATA_DIR, REPORT_DIR, CONFIG_DIR]:
    os.makedirs(_d, exist_ok=True)


def load_config(name):
    path = os.path.join(CONFIG_DIR, name)
    if os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))
    return {}


def cmd_daily(notify=False, sync_bitable=False):
    """每日采集 + 分析 + 报告"""
    from modules.crawler import crawl_all
    from modules.analyzer import analyze
    from modules.reporter import generate_report

    today = dt.date.today().isoformat()
    out_file = os.path.join(DATA_DIR, f'{today}.json')

    print(f'\n📡 热点收集雷达 · {today}\n')

    # 1. 爬取
    print('🌐 正在采集多平台热搜...')
    raw = crawl_all()

    # 1b. 加载 tophub AI 专题数据（通过浏览器采集）
    tophub_file = os.path.join(DATA_DIR, 'tophub_ai_raw.json')
    if os.path.exists(tophub_file):
        try:
            tophub_data = json.load(open(tophub_file, encoding='utf-8'))
            tophub_raw = tophub_data.get('data', {})
            if tophub_raw:
                for platform, items in tophub_raw.items():
                    if items:
                        raw[platform] = items
                print(f'  🤖 已合并 tophub AI 专题数据: {tophub_data.get("sources", [])} ({sum(len(v) for v in tophub_raw.values())} 条)')
        except Exception as e:
            print(f'  ⚠️ tophub AI 数据加载失败: {e}')

    # 1c. 加载 tophub 财经专题数据
    finance_file = os.path.join(DATA_DIR, 'tophub_finance_raw.json')
    if os.path.exists(finance_file):
        try:
            finance_data = json.load(open(finance_file, encoding='utf-8'))
            finance_raw = finance_data.get('data', {})
            if finance_raw:
                for platform, items in finance_raw.items():
                    if items:
                        raw[platform] = items
                print(f'  💰 已合并 tophub 财经专题数据: {finance_data.get("sources", [])} ({sum(len(v) for v in finance_raw.values())} 条)')
        except Exception as e:
            print(f'  ⚠️ tophub 财经数据加载失败: {e}')

    # 保存原始数据
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump({'date': today, 'raw': raw}, f, ensure_ascii=False, indent=2)
    print(f'  ✅ 已保存原始数据: {out_file}\n')

    # 2. 分析
    print('🧠 正在分析话题...')
    analysis = analyze(raw)

    # 3. 生成报告
    print('📝 正在生成日报...')
    report_md = generate_report(today, raw, analysis)

    report_file = os.path.join(REPORT_DIR, f'{today}.md')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_md)
    print(f'  ✅ 日报已保存: {report_file}\n')

    # 4. 同步飞书多维表格
    if sync_bitable:
        try:
            from modules.bitable_sync import sync_to_bitable
            sync_to_bitable(raw, today)
        except Exception as e:
            print(f'  ⚠️ 飞书表格同步失败: {e}')

    # 5. 飞书推送
    if notify:
        try:
            from modules.notifier import send_report
            send_report(report_md, today)
        except Exception as e:
            print(f'  ⚠️ 飞书推送失败: {e}')

    print(f'\n🎉 完成！日报路径: {report_file}')
    return report_file


def cmd_analyze(date):
    """重新分析指定日期数据"""
    from modules.analyzer import analyze
    from modules.reporter import generate_report

    in_file = os.path.join(DATA_DIR, f'{date}.json')
    if not os.path.exists(in_file):
        print(f'❌ 数据文件不存在: {in_file}')
        return

    data = json.load(open(in_file, encoding='utf-8'))
    analysis = analyze(data['raw'])
    report_md = generate_report(date, data['raw'], analysis)
    print(report_md)


def cmd_compare(platforms):
    """跨平台对比"""
    from modules.crawler import crawl_platform

    print(f'\n📊 跨平台对比: {platforms}\n')
    results = {}
    for p in platforms:
        data = crawl_platform(p)
        results[p] = data
        print(f'  ✅ {p}: {len(data)} 条')

    return results


def cmd_keywords():
    """按关键词过滤"""
    from modules.crawler import crawl_all
    from modules.analyzer import filter_by_keywords

    config = load_config('keywords.json')
    keywords = (
        config.get('competitors', []) +
        config.get('industry', []) +
        config.get('alerts', [])
    )

    print(f'\n🔍 关键词监控: {keywords}\n')
    raw = crawl_all()
    matched = filter_by_keywords(raw, keywords)

    print(f'  匹配到 {sum(len(v) for v in matched.values())} 条:\n')
    for platform, items in matched.items():
        print(f'  [{platform}]')
        for item in items:
            print(f'    - {item["title"]}')

    return matched


def main():
    parser = argparse.ArgumentParser(description='📡 热点收集雷达')
    parser.add_argument('--mode', choices=['daily', 'analyze', 'compare', 'keywords'], default='daily')
    parser.add_argument('--date', help='YYYY-MM-DD，analyze模式用')
    parser.add_argument('--platforms', help='逗号分隔，compare模式用，如 zhihu,weibo')
    parser.add_argument('--notify', action='store_true', help='同时推送到飞书')
    parser.add_argument('--sync-bitable', action='store_true', help='同步到飞书多维表格')

    args = parser.parse_args()

    if args.mode == 'daily':
        cmd_daily(notify=args.notify, sync_bitable=args.sync_bitable)
    elif args.mode == 'analyze':
        cmd_analyze(args.date or dt.date.today().isoformat())
    elif args.mode == 'compare':
        pls = [p.strip() for p in (args.platforms or 'zhihu,weibo').split(',')]
        cmd_compare(pls)
    elif args.mode == 'keywords':
        cmd_keywords()


if __name__ == '__main__':
    main()
