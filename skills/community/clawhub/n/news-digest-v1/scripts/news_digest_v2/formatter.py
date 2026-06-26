# -*- coding: utf-8 -*-
"""
格式化输出模块
"""

from datetime import datetime
import os
import re
try:
    from .config import SOURCE_MAP
    from .rules_config import clean_summary_text, has_garbled_title, should_exclude_by_content_type
except ImportError:
    from config import SOURCE_MAP
    from rules_config import clean_summary_text, has_garbled_title, should_exclude_by_content_type


def clean_summary(summary, max_length=300):
    """
    清理摘要（调用 rules_config 的统一函数）
    + 末尾不完整句子处理：
      - 以逗号/顿号/分号/冒号等结尾 → 回退截断到上一个句号
      - 全文没有句号 → 返回空字符串（整段丢弃，不输出残缺内容）
    """
    cleaned = clean_summary_text(summary, max_length)
    
    if not cleaned:
        return ''
    
    # 如果摘要以不完整的句子结尾（逗号、顿号、分号、冒号等）
    if re.search(r'[，、；：,;:…~\u2026\u3001\uff0c\uff1b\uff1a]$', cleaned):
        # 从后往前找第一个句号
        for sep in ['。', '！', '？']:
            pos = cleaned.rfind(sep)
            if pos > len(cleaned) * 0.3:  # 至少保留 30% 内容
                return cleaned[:pos + 1]
        
        # 全文没有完整句号 → 整段是残缺内容，丢弃
        return ''
    
    return cleaned


def format_source(source_name):
    """
    格式化来源名称
    """
    # 应用映射
    for key, value in SOURCE_MAP.items():
        if source_name.startswith(key):
            return value
    
    # 清理常见后缀
    suffixes = ['滚动新闻', '头条一览', '快讯', '首页', '头条', '一览', '新闻', ' - ', '：']
    for suffix in suffixes:
        if source_name.endswith(suffix):
            source_name = source_name[:-len(suffix)]
    
    return source_name.strip()


def generate_output(news_list, max_count=35):
    """
    生成摘要输出
    
    Args:
        news_list: 新闻列表
        max_count: 最大数量
    
    Returns:
        tuple: (输出文本，统计信息)
    """
    today = datetime.now()
    
    # 过滤重复
    filtered_news = [n for n in news_list if not n.get('is_duplicate', False)]
    
    # 截取前 N 条
    if len(filtered_news) > max_count:
        filtered_news = filtered_news[:max_count]
    
    # 生成输出 - header 留占位符，最后替换
    output = "新闻摘要汇总\n" + "="*60 + "\n\n"
    output += f"生成时间：{today.strftime('%Y年%m月%d日 %H:%M:%S')}\n\n"
    output += "来源网站：__SOURCE_COUNT__ | 收录新闻：__PLACEHOLDER__ 条\n\n"
    output += "关注领域：产业动态、产业政策、经济类信息、高技术类信息、价格信息、能源信息等\n\n"
    output += "="*60 + "\n\n"
    
    # 统计来源分布
    source_stats = {}
    
    for i, news in enumerate(filtered_news, 1):
        source = news.get('source', '未知')
        if not source or source.strip() == '':
            source = '未知'
        else:
            source = format_source(source)
        
        title = news.get('title', '无标题')
        url = news.get('url', '')
        
        # 内容类型黑名单过滤（评论/公告/人事等非硬新闻）
        if should_exclude_by_content_type(title, url):
            continue
        
        source_stats[source] = source_stats.get(source, 0) + 1
        
        # 清理标题首尾的多余符号（如中点、空格）
        title = title.strip().lstrip('·').strip()
        # 标题截断保护：检查是否因数据库字段长度导致截断
        if title and not title.endswith(('。', '！', '？', '…')) and '…' not in title and len(title) > 3:
            # 标题不应以逗号/顿号结尾，如果出现了说明被截断
            if title.endswith(('，', '、', '…')):
                title = title.rstrip('，、…') + '…'  # 保留省略号表示不完整
        summary = clean_summary(news.get('summary', ''))
        pub_date = news.get('publish_date', '')
        keywords = news.get('keywords', '')
        
        # 格式化输出（紧凑格式）
        output += f"【{source}：{title}】\n"
        
        # 摘要处理：合并多行为紧凑段落
        if summary:
            # 移除多余空行，合并为紧凑段落
            summary_lines = [line.strip() for line in summary.split('\n') if line.strip()]
            summary_compact = ' '.join(summary_lines)
            output += f"{summary_compact}\n"
        
        output += f"发布时间：{pub_date}\n"
        output += f"原文链接：{url}\n\n"
    
    # 统计实际输出条数
    actual_output_count = len([n for n in filtered_news if not should_exclude_by_content_type(n.get('title', ''), n.get('url', '')) and clean_summary(n.get('summary', ''))])
    
    stats = {
        'total': actual_output_count,
        'sources': len(source_stats),
        'by_source': source_stats
    }
    
    # 替换占位符为实际输出条数
    output = output.replace('__SOURCE_COUNT__', str(stats['sources']))
    output = output.replace('收录新闻：__PLACEHOLDER__ 条', f"收录新闻：{stats['total']} 条")
    
    # 来源统计
    output += "\n" + "="*60 + "\n来源分布统计：\n"
    for src, cnt in sorted(source_stats.items(), key=lambda x: x[1], reverse=True):
        output += f"  * {src}: {cnt} 条\n"
    output += "="*60 + "\n"
    
    return output, stats


def save_output(output_text, channels=None):
    """
    保存输出到指定渠道
    
    Args:
        output_text: 输出文本
        channels: 渠道列表（'desktop', 'feishu_personal', 'feishu_group'）
    """
    from .config import OUTPUT_CHANNELS
    
    if channels is None:
        channels = ['desktop']
    
    saved_to = []
    
    for channel in channels:
        if channel == 'desktop':
            desktop = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
            today_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            out_file = os.path.join(desktop, f"新闻摘要_{today_str}.txt")
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
            saved_to.append(out_file)
        
        elif channel == 'feishu_personal':
            out_file = OUTPUT_CHANNELS.get('feishu_personal', '.feishu-message-out.md')
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
            saved_to.append(out_file)
        
        elif channel == 'feishu_group':
            out_file = OUTPUT_CHANNELS.get('feishu_group', '.feishu-group-message-out.md')
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
            saved_to.append(out_file)
    
    return saved_to
