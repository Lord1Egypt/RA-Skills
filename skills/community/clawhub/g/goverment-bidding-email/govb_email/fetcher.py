#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政府采购商机邮件发送工具 (govb-email)

自动抓取北京政采、湖南政采的商机数据，
生成 Excel 汇总文件，并通过邮件发送报告。

用法:
    govb-email [选项]

示例:
    govb-email                           # 发送昨日报告（默认）
    govb-email --today                   # 发送今日报告
    govb-email --date 2026-03-23        # 发送指定日期报告
    govb-email --keywords "模型,仿真"    # 使用自定义关键词筛选
    govb-email --to test@example.com     # 测试发送至指定收件人
"""

import sys
import os
from pathlib import Path

from govb_email.config import get_email_config


def _import_fetcher():
    """延迟导入避免循环依赖"""
    from govb_fetcher.fetcher import fetch_all_bidding, save_to_excel
    from govb_fetcher.config import get_output_dir
    return fetch_all_bidding, save_to_excel, get_output_dir


def get_high_recommend_items(results: dict) -> dict:
    """
    从各渠道数据中提取高推荐等级的项目。

    Args:
        results: fetch_all_bidding 返回的字典，key 为渠道名，value 为记录列表

    Returns:
        dict: 包含各渠道高推荐项目的字典，结构为 {'bjzc': [], 'hnzc': []}
    """
    result = {'bjzc': [], 'hnzc': []}

    # 北京政采
    for record in results.get('北京政采', []):
        if record.get('推荐等级') == '高':
            lot_name = record.get('标段名称', '').strip()
            proj_name = record.get('项目名称', '').strip()
            result['bjzc'].append({
                'title': (lot_name or proj_name)[:50],
                'method': record.get('招标方式', ''),
                'budget': record.get('合同估价(元)', ''),
                'purchaser': record.get('采购人', ''),
            })

    # 湖南政采
    for record in results.get('湖南政采', []):
        if record.get('推荐等级') == '高':
            result['hnzc'].append({
                'title': record.get('项目名称', '')[:50],
                'method': record.get('招标方式', ''),
                'budget': record.get('合同估价(元)', ''),
                'purchaser': record.get('采购人', ''),
            })

    return result


def send_email(date_str, results, excel_path, to_override=None):
    """
    发送商机报告邮件。

    Args:
        date_str: 报告日期字符串，格式 YYYY-MM-DD
        results: fetch_all_bidding 返回的字典
        excel_path: Excel 附件文件路径（由 get_output_dir() 计算）
        to_override: 覆盖默认收件人，用于测试发送
    """
    env_config = get_email_config()
    recipient_name = env_config['recipient_name']
    sender_name = env_config['sender_name']
    subject_prefix = env_config['subject_prefix']
    body_intro = env_config['body_intro']

    # 构建邮件主题
    subject = f"【{subject_prefix}】{date_str}"

    # 获取高推荐项目
    high_items = get_high_recommend_items(results)

    bjzc_list = results.get('北京政采', [])
    hnzc_list = results.get('湖南政采', [])

    # 构建邮件正文
    body = f"""{recipient_name}，{body_intro}

汇总如下：

【北京政采】{len(bjzc_list)}条（{date_str}）

高推荐项目：
"""

    if high_items['bjzc']:
        for i, item in enumerate(high_items['bjzc'], 1):
            budget = f" | 预算{item['budget']}" if item.get('budget') else ""
            purchaser = f" | {item['purchaser']}" if item.get('purchaser') else ""
            body += f"{i}. {item['title']}... | {item['method']}{budget}{purchaser}\n"
    else:
        body += "（暂无高推荐项目）\n"

    body += f"""
【湖南政采】{len(hnzc_list)}条（{date_str}）

高推荐项目：
"""

    if high_items['hnzc']:
        for i, item in enumerate(high_items['hnzc'], 1):
            budget = f" | 预算{item['budget']}" if item.get('budget') else ""
            purchaser = f" | {item['purchaser']}" if item.get('purchaser') else ""
            body += f"{i}. {item['title']}... | {item['method']}{budget}{purchaser}\n"
    else:
        body += "（暂无高推荐项目）\n"

    body += f"""
详情请见附件Excel。

{sender_name}"""

    # 确定收件人/抄送人
    if to_override:
        to_list = [to_override]
        cc_list = []
    else:
        to_list = env_config['to']
        cc_list = env_config['cc']

    try:
        send_email_via_smtp(subject, body, excel_path, to_list, cc_list)
        print("[SUCCESS] 邮件发送成功")
        return True
    except Exception as e:
        print(f"[ERROR] 邮件发送失败: {e}")
        return False


def send_email_via_smtp(subject, body, excel_path, to_list, cc_list):
    """
    使用 SMTP 直接发送邮件。

    Args:
        subject: 邮件主题字符串
        body: 邮件正文纯文本字符串
        excel_path: Excel 附件文件路径（文件不存在时跳过附件）
        to_list: 收件人列表
        cc_list: 抄送人列表

    Returns:
        bool: 发送成功返回 True
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    from email.header import Header
    from email.utils import formatdate

    env_config = get_email_config()
    SMTP_HOST = env_config['smtp_host']
    SMTP_PORT = int(env_config['smtp_port'])
    SMTP_USER = env_config['smtp_user']
    SMTP_PASSWORD = env_config['smtp_password']

    # 创建邮件，主题使用 RFC 2047 编码防止中文乱码
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = ', '.join(to_list)
    msg['Cc'] = ', '.join(cc_list)
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg['Date'] = formatdate()

    msg.attach(MIMEText(body.strip(), 'plain', 'utf-8'))

    # 添加附件（文件不存在时跳过）
    if excel_path and os.path.exists(excel_path):
        with open(excel_path, 'rb') as f:
            part = MIMEApplication(f.read(), _subtype='xlsx')
        filename_encoded = Header(os.path.basename(excel_path), 'utf-8').encode()
        part.add_header('Content-Disposition', 'attachment', filename=filename_encoded)
        msg.attach(part)
    elif excel_path:
        print(f"[WARNING] 附件不存在，跳过: {excel_path}")

    # 发送邮件
    smtp = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()

    print(f"[INFO] 邮件已发送（SMTP）至: {', '.join(to_list)}, 抄送: {', '.join(cc_list)}")
    return True


def send_bidding_report(date=None, keywords=None, to_override=None):
    """
    发送商机报告邮件。

    Args:
        date: 指定日期，格式 YYYY-MM-DD。默认为昨日
        keywords: 关键词列表，用于筛选商机。默认为 None，使用 govb_fetcher 配置的默认关键词
        to_override: 覆盖默认收件人，用于测试发送

    Returns:
        dict: fetch_all_bidding 返回的结果字典
    """
    from datetime import datetime, timedelta

    # 确定查询日期
    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"[INFO] 默认获取昨日商机: {date}")

    print(f"[INFO] 开始抓取商机信息 - 日期: {date}")

    # 抓取数据
    fetch_all_bidding, save_to_excel, get_output_dir = _import_fetcher()
    results = fetch_all_bidding(date, keywords=keywords)

    bjzc_count = len(results.get('北京政采', []))
    hnzc_count = len(results.get('湖南政采', []))
    print(f"[INFO] 采集完成: 北京政采{bjzc_count}条, 湖南政采{hnzc_count}条")

    # 保存 Excel
    output_path = get_output_dir() / f'政府采购商机汇总_{date}.xlsx'
    save_to_excel(results, output_path)
    print(f"[INFO] Excel 已保存: {output_path}")

    # 发送邮件
    send_email(date, results, output_path, to_override=to_override)

    return results


HELP_TEXT = """政府采购商机邮件发送工具

用法:
    govb-email [选项]

选项:
    --date DATE         日期，格式 YYYY-MM-DD
    --keywords WORDS   关键词，逗号分隔，如: 模型,仿真,AI
    --to ADDRESS       测试发送至指定收件人
    --today            发送今日报告
    --help             显示此帮助信息

示例:
    govb-email                           # 发送昨日报告（默认）
    govb-email --today                   # 发送今日报告
    govb-email --date 2026-03-23        # 发送指定日期报告
    govb-email --keywords "模型,仿真"    # 使用自定义关键词
    govb-email --to test@example.com    # 测试发送
"""


def main():
    """
    CLI 入口函数。

    支持的参数:
        --date DATE: 指定日期，格式 YYYY-MM-DD
        --keywords WORDS: 关键词，逗号分隔
        --to ADDRESS: 测试发送至指定收件人
        --today: 发送今日报告
        --help: 显示帮助信息
    """
    import argparse
    import fcntl
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description='政府采购商机邮件发送工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_TEXT
    )
    parser.add_argument('--date', type=str, help='日期，格式 YYYY-MM-DD')
    parser.add_argument('--keywords', type=str, help='关键词，逗号分隔')
    parser.add_argument('--to', type=str, help='测试发送至指定收件人（覆盖配置）')
    parser.add_argument('--today', action='store_true', help='发送今日报告')

    args = parser.parse_args()

    # --help 时显示帮助
    if '--help' in sys.argv:
        print(HELP_TEXT)
        sys.exit(0)

    # 确定日期
    date = args.date
    if args.today and date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    # 锁文件防止并发执行
    LOCK_FILE = '/tmp/govb_bidding_email.lock'

    try:
        lock_fd = open(LOCK_FILE, 'w')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (IOError, OSError):
        print("[INFO] 已有任务在运行，跳过本次执行")
        sys.exit(0)

    # 解析关键词
    keywords = None
    if args.keywords:
        keywords = args.keywords.split(',')

    # 发送报告
    try:
        send_bidding_report(date=date, keywords=keywords, to_override=args.to)
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()
        try:
            os.remove(LOCK_FILE)
        except Exception:
            pass


if __name__ == '__main__':
    main()
