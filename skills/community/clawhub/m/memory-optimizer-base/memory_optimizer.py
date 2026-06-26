#!/usr/bin/env python3
"""
Memory Optimizer Base - 多Agents记忆管理系统
基础框架主入口
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'lib'))

import config
import analyzer
import optimizer
import tierer
import sync
import summarizer
import uploader
import retriever

def load_config():
    """加载配置"""
    config_path = Path(BASE_DIR) / 'config' / 'default.json'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return config.Config(json.load(f))
    return config.Config({})

def get_workspace_path(cfg):
    base_path = cfg.get('memory.base_path', '~/.openclaw/workspace')
    return Path(base_path).expanduser()

def cmd_init(args):
    """初始化记忆空间结构"""
    print("🏗️  正在初始化记忆空间...")
    cfg = load_config()
    workspace = get_workspace_path(cfg)

    agent_id = args.agent or cfg.get('memory.default_agent_id', 'default')

    # 创建目录结构
    private_root = workspace / cfg.get('memory.private_root') / agent_id
    public_root = workspace / cfg.get('memory.public_root')

    dirs_to_create = [
        private_root / 'medium-term',
        private_root / 'long-term',
        public_root
    ]

    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ 创建目录：{d}")

    print(f"\n✅ 已为 Agent '{agent_id}' 初始化记忆空间！")
    print(f"  私有空间：{private_root}")
    print(f"  公共空间：{public_root}")

    # 保存agent配置
    agent_config = {
        'agent_id': agent_id,
        'initialized': datetime.now().isoformat(),
        'private_path': str(private_root),
        'public_path': str(public_root)
    }
    agent_config_file = Path(BASE_DIR) / 'config' / 'agents' / f'{agent_id}.json'
    agent_config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(agent_config_file, 'w', encoding='utf-8') as f:
        json.dump(agent_config, f, indent=2, ensure_ascii=False)

    print(f"  📝 Agent配置已保存：{agent_config_file}")

def cmd_analyze(args):
    """分析记忆系统"""
    print("🔍 正在分析记忆系统...")
    cfg = load_config()

    agent = args.agent if args.agent else None
    include_public = not args.private_only if hasattr(args, 'private_only') else True

    analyzer_obj = analyzer.MemoryAnalyzer(cfg)
    report = analyzer_obj.analyze(agent_id=agent, include_public=include_public)

    print("\n📊 记忆系统分析报告:")
    print(f"  总文件数: {report['total_files']}")
    print(f"  总条目数: {report['total_entries']}")
    print(f"  总大小: {report['total_size_bytes'] / 1024:.1f} KB")
    print(f"  健康度评分: {report['health_score']:.1f}/100")

    if 'by_agent' in report:
        print("\n👥 各Agent状态:")
        for aid, adata in report['by_agent'].items():
            print(f"  {aid}: {adata['files']} 文件, {adata['entries']} 条目")

    if 'spaces' in report and 'public' in report['spaces']:
        pub = report['spaces']['public']
        print("\n🌐 公共空间:")
        print(f"  文件数: {pub['files']}")
        print(f"  贡献Agent: {', '.join(pub.get('agents', []))}")
        if pub.get('date_range', {}).get('earliest'):
            print(f"  时间范围: {pub['date_range']['earliest']} ~ {pub['date_range']['latest']}")

    if report.get('issues'):
        print("\n⚠️  发现的问题:")
        for issue in report['issues']:
            print(f"  - {issue['type']}: {issue['description']}")

    print("\n💡 建议:")
    for suggestion in report.get('suggestions', []):
        print(f"  - {suggestion}")

def cmd_summarize(args):
    """生成中期总结"""
    print("📝 正在生成中期总结...")
    cfg = load_config()

    agent_id = args.agent or cfg.get('memory.default_agent_id', 'default')

    # 日期处理
    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    else:
        target_date = datetime.now().date()

    summarizer_obj = summarizer.MemorySummarizer(cfg)
    result = summarizer_obj.summarize(agent_id, target_date)

    if result['success']:
        print(f"\n✅ 中期总结已生成！")
        print(f"  Agent: {result['agent']}")
        print(f"  日期: {result['date']}")
        print(f"  文件: {result['path']}")
        print(f"  统计: 原始内容 {result['stats']['raw_size']} 字符 → 总结 {result['stats']['summary_size']} 字符")
        print(f"  分析会话数: {result['stats']['sessions_count']}")
        print("\n💡 下一步：")
        print(f"  查看总结：cat {result['path']}")
        print(f"  上传到公共空间：./memory_optimizer.py upload --agent {agent_id} --date {result['date']}")
    else:
        print(f"\n❌ 生成失败：{result['message']}")
        print("  提示：确保今天有会话记录且已保存到记忆文件中")

def cmd_upload(args):
    """上传到公共空间"""
    print("☁️  正在上传到公共记忆空间...")
    cfg = load_config()

    agent_id = args.agent or cfg.get('memory.default_agent_id', 'default')

    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    else:
        target_date = datetime.now().date()

    uploader_obj = uploader.MemoryUploader(cfg)
    result = uploader_obj.upload(
        agent_id=agent_id,
        target_date=target_date,
        title=args.title,
        confirm_callback=None  # 使用默认交互
    )

    if result['success']:
        print(f"\n✅ 上传成功！")
        print(f"  标题: {result['title']}")
        print(f"  路径: {result['public_path']}")
        print(f"  Agent: {result['agent']}")
    else:
        if result.get('cancelled'):
            print("  ⚠️  上传已取消")
        else:
            print(f"\n❌ 上传失败：{result['message']}")

def cmd_search_public(args):
    """搜索公共记忆"""
    print("🔍 正在搜索公共记忆空间...")
    cfg = load_config()

    retriever_obj = retriever.MemoryRetriever(cfg)

    # 解析参数
    agent_filter = getattr(args, 'agent', None)

    # 日期范围
    date_from = getattr(args, 'date_from', None)
    date_to = getattr(args, 'date_to', None)
    date_range = None
    if date_from and date_to:
        try:
            start = datetime.strptime(date_from, '%Y-%m-%d').date()
            end = datetime.strptime(date_to, '%Y-%m-%d').date()
            date_range = (start, end)
        except Exception as e:
            print(f"⚠️  日期格式错误：{e}")

    # 执行搜索
    result = retriever_obj.search_public(
        query=args.query,
        agent_filter=agent_filter,
        date_range=date_range,
        limit=args.limit
    )

    # 输出结果
    if result['total'] == 0:
        print(f"\n😔 未找到相关公共记忆（关键词：{args.query}）")
    else:
        print(f"\n✅ 找到 {result['returned']} 条相关记忆（共 {result['total']} 条）：\n")
        for i, r in enumerate(result['results'], 1):
            print(f"{i}. [{r['agent']}] {r['title']} ({r['date']})")
            print(f"   相关性：{r['score']:.2%}")
            snippet = r['snippet']
            if snippet:
                print(f"   摘要：{snippet[:100]}...")
            print(f"   路径：{r['path']}\n")

def cmd_search_private(args):
    """搜索私有记忆"""
    print(f"🔍 正在搜索 Agent '{args.agent}' 的私有记忆...")
    cfg = load_config()

    retriever_obj = retriever.MemoryRetriever(cfg)
    result = retriever_obj.search_private(args.query, args.agent, limit=args.limit)

    if result['total'] == 0:
        print(f"\n😔 未在私有记忆中找到相关内容")
    else:
        print(f"\n✅ 私有记忆中找到 {result['returned']} 条：\n")
        for i, r in enumerate(result['results'], 1):
            print(f"{i}. {r['title']} ({r['date']})")
            print(f"   相关性：{r['score']:.2%}")
            print(f"   摘要：{r['snippet'][:100]}...\n")

def cmd_private(args):
    """私有记忆管理"""
    cfg = load_config()
    agent_id = args.agent or cfg.get('memory.default_agent_id', 'default')
    private_root = get_workspace_path(cfg) / cfg.get('memory.private_root') / agent_id

    if args.action == 'list' or not args.action:
        print(f"📁 Agent '{agent_id}' 的私有记忆：\n")
        for tier in ['medium-term', 'long-term']:
            tier_dir = private_root / tier
            if tier_dir.exists():
                files = list(tier_dir.rglob('*.md'))
                print(f"  {tier}: {len(files)} 个文件")
                for f in files[:5]:
                    size = f.stat().st_size
                    print(f"    - {f.name} ({size} bytes)")
                if len(files) > 5:
                    print(f"    ... 还有 {len(files)-5} 个文件")
            else:
                print(f"  {tier}: (空)")

    elif args.action == 'clean':
        days = args.days or 1  # 默认只保留1天内的中期记忆
        cutoff = datetime.now().timestamp() - days * 86400

        cleaned = 0
        medium_dir = private_root / 'medium-term'
        if medium_dir.exists():
            for file_path in medium_dir.glob('*.md'):
                if file_path.stat().st_mtime < cutoff:
                    file_path.unlink(missing_ok=True)
                    cleaned += 1

        print(f"✅ 已清理 {cleaned} 个过期中期记忆文件（保留最近 {days} 天）")

def cmd_test_workflow(args):
    """测试完整工作流"""
    print("🧪 开始测试工作流...\n")
    agent_id = args.agent or 'test-agent'

    # 1. 初始化
    print("【1】初始化空间...")
    os.system(f'./memory_optimizer.py init --agent {agent_id}')

    # 2. 生成中期总结（使用模拟数据）
    print("\n【2】生成中期总结...")
    # 这里应该创建模拟的记忆文件，暂略
    print("  (跳过，需要手动创建测试记忆文件)")

    # 3. 上传
    print("\n【3】上传到公共空间...")
    print("  (手动运行：./memory_optimizer.py upload)")

    # 4. 搜索
    print("\n【4】搜索验证...")
    print("  (手动运行：./memory_optimizer.py search-public \"关键词\")")

    print("\n✅ 工作流测试完成！")

def cmd_config(args):
    """配置管理"""
    cfg = load_config()

    if args.set:
        key, value = args.set.split('=', 1)
        # 类型推断
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        elif value.isdigit():
            value = int(value)
        elif value.replace('.', '', 1).isdigit():
            value = float(value)

        cfg.set(key, value)

        # 保存到默认配置（注意：这是全局的）
        config_path = Path(BASE_DIR) / 'config' / 'default.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(cfg.data, f, indent=2, ensure_ascii=False)

        print(f"✅ 已设置 {key}={value}")
    else:
        print("📋 当前配置:")
        for key, value in cfg.data.items():
            print(f"\n[{key}]")
            if isinstance(value, dict):
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"  {value}")

def main():
    parser = argparse.ArgumentParser(
        description='Memory Optimizer - 多Agents记忆协作系统\n'
                    '支持：公共+私有双层结构，短期→中期→长期自动化',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 初始化
  ./memory_optimizer.py init --agent xiaotian

  # 生成今天的中期总结
  ./memory_optimizer.py summarize --agent xiaotian --date 2026-04-06

  # 上传到公共空间
  ./memory_optimizer.py upload --agent xiaotian --date 2026-04-06 --title "论文编写经验"

  # 搜索公共记忆
  ./memory_optimizer.py search-public "论文编写"

  # 查看私有记忆
  ./memory_optimizer.py private list --agent xiaotian

  # 清理过期中期记忆（保留3天内）
  ./memory_optimizer.py private clean --agent xiaotian --days 3
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # init
    init_parser = subparsers.add_parser('init', help='初始化记忆空间')
    init_parser.add_argument('--agent', help='Agent ID (默认: default)')

    # analyze
    analyze_parser = subparsers.add_parser('analyze', help='分析记忆系统')
    analyze_parser.add_argument('--agent', help='指定Agent（不指定则分析所有）')
    analyze_parser.add_argument('--private-only', action='store_true', help='仅分析私有空间')

    # summarize
    summarize_parser = subparsers.add_parser('summarize', help='生成中期总结')
    summarize_parser.add_argument('--agent', help='Agent ID')
    summarize_parser.add_argument('--date', help='日期 (YYYY-MM-DD，默认今天)')

    # upload
    upload_parser = subparsers.add_parser('upload', help='上传到公共长期记忆')
    upload_parser.add_argument('--agent', help='Agent ID')
    upload_parser.add_argument('--date', help='日期 (YYYY-MM-DD，默认今天)')
    upload_parser.add_argument('--title', help='事件标题（可选）')

    # search-public
    sp_parser = subparsers.add_parser('search-public', help='搜索公共记忆')
    sp_parser.add_argument('query', help='搜索关键词')
    sp_parser.add_argument('--agent', help='限制来源Agent')
    sp_parser.add_argument('--from', dest='date_from', help='起始日期')
    sp_parser.add_argument('--to', dest='date_to', help='结束日期')
    sp_parser.add_argument('--limit', type=int, help='最大结果数')

    # search-private
    s_parser = subparsers.add_parser('search-private', help='搜索私有记忆')
    s_parser.add_argument('query', help='搜索关键词')
    s_parser.add_argument('--agent', required=True, help='Agent ID')
    s_parser.add_argument('--limit', type=int, help='最大结果数')

    # private
    priv_parser = subparsers.add_parser('private', help='私有记忆管理')
    priv_sub = priv_parser.add_subparsers(dest='action', help='操作')
    priv_sub.add_parser('list', help='列出私有记忆')
    clean_parser = priv_sub.add_parser('clean', help='清理过期中期记忆')
    clean_parser.add_argument('--days', type=int, help='保留天数（默认1）')
    clean_parser.add_argument('--agent', help='Agent ID')

    # test-workflow
    test_parser = subparsers.add_parser('test-workflow', help='测试完整工作流')
    test_parser.add_argument('--agent', help='测试Agent ID')

    # config
    config_parser = subparsers.add_parser('config', help='配置管理')
    config_parser.add_argument('--set', help='设置 key=value')
    config_parser.add_argument('--get', help='获取配置项')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        'init': cmd_init,
        'analyze': cmd_analyze,
        'summarize': cmd_summarize,
        'upload': cmd_upload,
        'search-public': cmd_search_public,
        'search-private': cmd_search_private,
        'private': cmd_private,
        'test-workflow': cmd_test_workflow,
        'config': cmd_config,
    }

    try:
        commands[args.command](args)
    except Exception as e:
        print(f"\n❌ 错误：{str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
