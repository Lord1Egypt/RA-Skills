#!/usr/bin/env python3
"""
Ledger CLI - 命令行记账工具

Usage:
    python cli.py list                           # 列出所有账本
    python cli.py show --name 测试账本               # 查看所有交易
    python cli.py show --name 测试账本 --month 2026-03  # 查看单月汇总
    python cli.py show --name 测试账本 --from 2026-01 --to 2026-03  # 日期范围
    python cli.py trend --name 测试账本 --from 2026-01 --to 2026-03  # 余额趋势
    python cli.py add --name 测试账本 --date 2026-03-20 --amount -50 --category 餐饮  # 添加交易

默认账本: 兔兔
"""
import sys
import os
import argparse

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.ledger import (
    create_ledger,
    add_transaction,
    batch_add_transactions,
    set_opening_balance,
)
from src.services.report import (
    get_transactions,
    get_monthly_summary,
    get_balance_trend,
    get_ledger_date_range,
)
from src.db.connection import get_db_path
from datetime import datetime, timedelta

# 默认账本
DEFAULT_LEDGER = "兔兔"


def print_transactions_markdown(transactions, title=None):
    """Markdown 格式的交易表格"""
    lines = []
    
    if title:
        lines.append(f"**{title}**")
    
    if not transactions:
        lines.append("(无交易记录)")
        print("\n".join(lines))
        return
    
    # Markdown 表格头
    lines.append("| 日期 | 分类 | 金额 | 账户 | 备注 |")
    lines.append("| --- | --- | --- | --- | --- |")
    
    income = 0.0
    expense = 0.0
    
    for t in transactions:
        amount = t['amount']
        if amount > 0:
            income += amount
            amount_str = f"+{amount:.2f}"
        else:
            expense += amount
            amount_str = f"{amount:.2f}"
        
        desc = t.get('description', '') or ''
        lines.append(f"| {t['date']} | {t['category']} | {amount_str} | {t['account']} | {desc} |")
    
    # 汇总
    lines.append("")
    lines.append(f"**收入**: +{income:.2f}")
    lines.append(f"**支出**: {expense:.2f}")
    lines.append(f"**合计**: {income + expense:.2f}")
    
    print("\n".join(lines))


def print_transactions_table(transactions, title=None, markdown=False):
    """人类友好的交易表格打印"""
    if markdown:
        return print_transactions_markdown(transactions, title)
    if title:
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    if not transactions:
        print("  (无交易记录)")
        return
    
    # 表头
    print(f"  {'日期':<12} {'分类':<10} {'金额':<12} {'账户':<8} {'备注'}")
    print("  " + "-" * 60)
    
    # 收入和支出统计
    income = 0.0
    expense = 0.0
    
    for t in transactions:
        amount = t['amount']
        amount_str = f"+{amount:.2f}" if amount > 0 else f"{amount:.2f}"
        
        if amount > 0:
            income += amount
        else:
            expense += amount
        
        # 截断过长的描述
        desc = t.get('description', '')[:15]
        if t.get('description', '') and len(t.get('description', '')) > 15:
            desc += "..."
        
        print(f"  {t['date']:<12} {t['category']:<10} {amount_str:<12} {t['account']:<8} {desc}")
    
    # 汇总行
    print("  " + "-" * 60)
    print(f"  {'收入':.<12} +{income:.2f}")
    print(f"  {'支出':.<12} {expense:.2f}")
    print(f"  {'合计':.<12} {income + expense:.2f}")


def cmd_create(args):
    """创建账本"""
    ledger_name = args.name
    try:
        create_ledger(ledger_name)
        print(f"\n✅ 账本 '{ledger_name}' 已创建")
        print(f"   数据库位置: {get_db_path(ledger_name)}")
    except Exception as e:
        print(f"\n❌ 创建失败: {e}")


def cmd_list(args):
    """列出所有账本"""
    base_path = os.path.expanduser("~/.openclaw/skills_data/ledger")
    if os.path.exists(base_path):
        ledgers = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        print(f"\n{'='*60}")
        print(f" 📚 账本列表")
        print(f"{'='*60}")
        for ledger in sorted(ledgers):
            db_path = get_db_path(ledger)
            if os.path.exists(db_path):
                print(f"  ✅ {ledger}")
            else:
                print(f"  ⏳ {ledger}")
    else:
        print("暂无账本")


def cmd_show(args):
    """查看交易"""
    ledger_name = args.name or DEFAULT_LEDGER
    month = args.month
    start = args.start
    end = args.end
    markdown = getattr(args, 'markdown', False)
    
    if month:
        # 查看单月汇总
        summary = get_monthly_summary(ledger_name, month)
        
        if markdown:
            print(f"**📊 {ledger_name} - {month} 月度汇总**")
            print(f"- 期初余额: {summary['opening']:.2f}")
            print(f"- 本月收入: +{summary['income']:.2f}")
            print(f"- 本月支出: {summary['expense']:.2f}")
            print(f"- 期末余额: {summary['closing']:.2f}")
            print(f"- 交易笔数: {len(summary['transactions'])}")
        else:
            print(f"\n{'='*60}")
            print(f" 📊 {ledger_name} - {month} 月度汇总")
            print(f"{'='*60}")
            print(f"  期初余额: {summary['opening']:.2f}")
            print(f"  本月收入: +{summary['income']:.2f}")
            print(f"  本月支出: {summary['expense']:.2f}")
            print(f"  ─────────────")
            print(f"  期末余额: {summary['closing']:.2f}")
            print(f"\n  交易笔数: {len(summary['transactions'])}")
        
        if summary['transactions']:
            print_transactions_table(summary['transactions'], f"{month} 月交易明细", markdown=markdown)
    
    elif start and end:
        # 日期范围
        # 生成月份列表
        start_year, start_month = map(int, start.split('-'))
        end_year, end_month = map(int, end.split('-'))
        
        months = []
        year, month = start_year, start_month
        while (year < end_year) or (year == end_year and month <= end_month):
            months.append(f"{year}-{month:02d}")
            month += 1
            if month > 12:
                month = 1
                year += 1
        
        all_trans = get_transactions(ledger_name, None)
        
        filtered = []
        for t in all_trans:
            trans_month = t['date'][:7]
            if trans_month in months:
                filtered.append(t)
        
        print_transactions_table(filtered, f"📅 {ledger_name} - {start} 至 {end}")
    
    else:
        # 查看所有交易
        transactions = get_transactions(ledger_name, None)
        print_transactions_table(transactions, f"📒 {ledger_name} - 全部交易记录")


def cmd_trend(args):
    """余额趋势"""
    ledger_name = args.name or DEFAULT_LEDGER
    start = args.start
    end = args.end
    
    if not start:
        start = "2026-01"
    if not end:
        end = "2026-03"
    
    # 生成月份列表
    start_year, start_month = map(int, start.split('-'))
    end_year, end_month = map(int, end.split('-'))
    
    months = []
    year, month = start_year, start_month
    while (year < end_year) or (year == end_year and month <= end_month):
        months.append(f"{year}-{month:02d}")
        month += 1
        if month > 12:
            month = 1
            year += 1
    
    trend = get_balance_trend(ledger_name, months)
    
    print(f"\n{'='*60}")
    print(f" 📈 {ledger_name} - 余额趋势")
    print(f"{'='*60}")
    
    for item in trend:
        balance = item['balance']
        bar = "█" * int(abs(balance) / 1000)
        if balance < 0:
            bar = "▓" * int(abs(balance) / 1000)
        print(f"  {item['month']}: {balance:>10.2f} | {bar}")


def to_pinyin(text):
    """将中文转换为拼音"""
    try:
        from pypinyin import lazy_pinyin
        return ''.join(lazy_pinyin(text))
    except ImportError:
        return text


def cmd_chart(args):
    """绘制账单折线图"""
    import matplotlib.pyplot as plt
    import matplotlib
    from datetime import timedelta
    matplotlib.use('Agg')  # 非交互式后端
    
    # 配置字体
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 支持多个账本
    ledger_names = args.name if args.name else [DEFAULT_LEDGER]
    user_start = args.start
    user_end = args.end
    output_path = args.output
    
    # 收集所有账本中有交易的日期范围
    all_min_date = None
    all_max_date = None
    
    for ledger_name in ledger_names:
        date_range = get_ledger_date_range(ledger_name)
        if date_range['start']:
            if all_min_date is None or date_range['start'] < all_min_date:
                all_min_date = date_range['start']
            if all_max_date is None or date_range['end'] > all_max_date:
                all_max_date = date_range['end']
    
    if not all_min_date or not all_max_date:
        print("没有找到交易记录")
        return
    
    # 如果用户指定了范围，则使用用户的范围
    start = user_start or all_min_date[:7]  # YYYY-MM
    end = user_end or all_max_date[:7]
    
    # 获取日期范围内的交易
    start_year, start_month = map(int, start.split('-'))
    end_year, end_month = map(int, end.split('-'))
    
    months = []
    year, month = start_year, start_month
    while (year < end_year) or (year == end_year and month <= end_month):
        months.append(f"{year}-{month:02d}")
        month += 1
        if month > 12:
            month = 1
            year += 1
    
    # 生成完整日期范围（从有交易的第一天开始）
    start_date = datetime.strptime(all_min_date, '%Y-%m-%d')
    if end_month == 12:
        end_date = datetime(end_year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(end_year, end_month + 1, 1) - timedelta(days=1)
    
    all_dates = []
    current = start_date
    while current <= end_date:
        all_dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    # 颜色列表
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # 绘图
    plt.figure(figsize=(14, 6))
    
    for idx, ledger_name in enumerate(ledger_names):
        # 获取账本交易
        all_trans = get_transactions(ledger_name, None)
        
        filtered = []
        for t in all_trans:
            trans_month = t['date'][:7]
            if trans_month in months:
                filtered.append(t)
        
        if not filtered:
            print(f"⚠️ {ledger_name}: 没有找到交易记录")
            continue
        
        # 按日期排序，同一天内按时间戳排序
        filtered.sort(key=lambda x: (x['date'], x.get('created_at', '')))
        
        # 建立日期到交易列表的映射
        date_to_trans = {}
        for t in filtered:
            date_str = t['date']
            if date_str not in date_to_trans:
                date_to_trans[date_str] = []
            date_to_trans[date_str].append(t)
        
        # 计算累计余额
        cumulative = 0
        x_positions = []
        y_balances = []
        
        for i, date_str in enumerate(all_dates):
            if date_str in date_to_trans:
                for t in date_to_trans[date_str]:
                    cumulative += t['amount']
                x_positions.append(i)
                y_balances.append(cumulative)
        
        # 绘制折线（将账本名转为拼音）
        color = colors[idx % len(colors)]
        label_pinyin = to_pinyin(ledger_name)
        plt.plot(x_positions, y_balances, marker='o', linewidth=1.5, markersize=4, 
                 label=label_pinyin, color=color)
    
    # x轴：只标注有交易之后的周一日期
    x_labels = [''] * len(all_dates)
    first_trans_date = all_min_date  # 第一笔交易日期
    
    for i, date_str in enumerate(all_dates):
        # 只标注从第一笔交易日期开始的周一
        if date_str >= first_trans_date:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if date.weekday() == 0:  # 周一
                x_labels[i] = date_str
    
    # 设置x轴范围和标签
    plt.xlim(-1, len(all_dates))
    plt.xticks(range(len(x_labels)), x_labels, rotation=45, ha='right')
    
    # 标题使用拼音
    if len(ledger_names) == 1:
        title = f'{to_pinyin(ledger_names[0])} Balance Chart ({start}~{end})'
    else:
        title = f'Multi-Ledger Balance Chart ({start}~{end})'
    
    plt.xlabel('Date (Monday labeled)')
    plt.ylabel('Cumulative Balance')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        print(f"✅ 图表已保存到: {output_path}")
    else:
        default_path = os.path.expanduser(f"~/.openclaw/skills_data/ledger/{ledger_names[0]}/chart.png")
        plt.savefig(default_path)
        print(f"✅ 图表已保存到: {default_path}")


def cmd_add(args):
    """添加交易"""
    ledger_name = args.name or DEFAULT_LEDGER
    date = args.date or datetime.now().strftime('%Y-%m-%d')
    amount = args.amount
    category = args.category or "其他"
    account = args.account or "现金"
    description = args.description or ""
    
    add_transaction(ledger_name, {
        'date': date,
        'amount': amount,
        'category': category,
        'account': account,
        'description': description
    })
    
    print(f"\n✅ 已添加交易: {date} {amount} {category}")
    
    # 打印该月汇总
    month = date[:7]
    summary = get_monthly_summary(ledger_name, month)
    
    print(f"\n{'='*60}")
    print(f" 📊 {ledger_name} - {month} 月度汇总")
    print(f"{'='*60}")
    print(f"  期初余额: {summary['opening']:.2f}")
    print(f"  本月收入: +{summary['income']:.2f}")
    print(f"  本月支出: {summary['expense']:.2f}")
    print(f"  ─────────────")
    print(f"  期末余额: {summary['closing']:.2f}")


def cmd_range(args):
    """输出账本日期范围"""
    ledger_name = args.name or DEFAULT_LEDGER
    
    date_range = get_ledger_date_range(ledger_name)
    
    if date_range['start'] is None:
        print(f"账本 '{ledger_name}' 没有交易记录")
    else:
        print(f"{date_range['start']} {date_range['end']}")


def main():
    parser = argparse.ArgumentParser(
        description='Ledger CLI - 记账工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python cli.py list                           列出所有账本
  python cli.py show --name 兔兔               查看所有交易
  python cli.py show --name 兔兔 --month 2026-03  查看单月汇总
  python cli.py show --name 兔兔 --from 2026-01 --to 2026-03  日期范围
  python cli.py trend --name 兔兔              余额趋势(默认2026-01~2026-03)
  python cli.py trend --name 兔兔 --from 2026-01 --to 2026-03  余额趋势
  python cli.py chart --name 兔兔             绘制折线图
  python cli.py chart --name 兔兔 --from 2026-01 --to 2026-03  绘制折线图
  python cli.py add --name 兔兔 --date 2026-03-20 --amount -50 --category 餐饮  添加交易

默认账本: {DEFAULT_LEDGER}
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建账本')
    create_parser.add_argument('--name', type=str, required=True, help='账本名称')
    
    # list 命令
    subparsers.add_parser('list', help='列出所有账本')
    
    # range 命令
    range_parser = subparsers.add_parser('range', help='查看账本日期范围')
    range_parser.add_argument('--name', type=str, default=None, help='账本名称')
    
    # show 命令
    show_parser = subparsers.add_parser('show', help='查看交易')
    show_parser.add_argument('--name', type=str, default=None, help='账本名称')
    show_parser.add_argument('--month', type=str, default=None, metavar='YYYY-MM', help='月份')
    show_parser.add_argument('--from', dest='start', type=str, default=None, metavar='YYYY-MM', help='开始月份')
    show_parser.add_argument('--to', dest='end', type=str, default=None, metavar='YYYY-MM', help='结束月份')
    show_parser.add_argument('--markdown', action='store_true', help='输出 Markdown 格式')
    
    # trend 命令
    trend_parser = subparsers.add_parser('trend', help='余额趋势')
    trend_parser.add_argument('--name', type=str, default=None, help='账本名称')
    trend_parser.add_argument('--from', dest='start', type=str, default=None, metavar='YYYY-MM', help='开始月份')
    trend_parser.add_argument('--to', dest='end', type=str, default=None, metavar='YYYY-MM', help='结束月份')
    trend_parser.add_argument('--markdown', action='store_true', help='输出 Markdown 格式')
    
    # chart 命令
    chart_parser = subparsers.add_parser('chart', help='绘制账单折线图')
    chart_parser.add_argument('--name', type=str, nargs='+', default=None, help='账本名称（支持多个）')
    chart_parser.add_argument('--from', dest='start', type=str, default=None, metavar='YYYY-MM', help='开始月份')
    chart_parser.add_argument('--to', dest='end', type=str, default=None, metavar='YYYY-MM', help='结束月份')
    chart_parser.add_argument('--output', type=str, default=None, help='输出图片路径')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加交易')
    add_parser.add_argument('--name', type=str, default=None, help='账本名称')
    add_parser.add_argument('--date', type=str, default=None, help='日期 (YYYY-MM-DD)，默认当天')
    add_parser.add_argument('--amount', type=float, required=True, help='金额')
    add_parser.add_argument('--category', type=str, default=None, help='分类')
    add_parser.add_argument('--account', type=str, default=None, help='账户')
    add_parser.add_argument('--description', type=str, default='', help='备注')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        cmd_create(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'range':
        cmd_range(args)
    elif args.command == 'show':
        cmd_show(args)
    elif args.command == 'trend':
        cmd_trend(args)
    elif args.command == 'chart':
        cmd_chart(args)
    elif args.command == 'add':
        cmd_add(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
