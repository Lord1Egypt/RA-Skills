#!/usr/bin/env python3
"""
TXT 电子书清理脚本 v4.0
功能：修复乱码、去除广告、规范化排版
"""

import re
import sys
import chardet
from pathlib import Path


def detect_encoding(file_path: str) -> str:
    """自动检测文件编码"""
    with open(file_path, 'rb') as f:
        raw = f.read(100000)  # 读取前100KB用于检测
        result = chardet.detect(raw)
        encoding = result['encoding'] or 'utf-8'
        # 常见编码别名处理
        if encoding.upper() in ('GB2312', 'GB18030'):
            encoding = 'GBK'
        return encoding


def read_file(file_path: str) -> str:
    """读取文件，自动处理编码"""
    encoding = detect_encoding(file_path)
    print(f"检测到编码: {encoding}")
    
    # 尝试多种编码
    encodings_to_try = [encoding, 'GBK', 'UTF-8', 'GB2312', 'BIG5']
    
    for enc in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=enc, errors='strict') as f:
                content = f.read()
                # 检查是否有大量乱码特征
                if content.count('�') < len(content) * 0.01:  # 乱码少于1%
                    return content
        except:
            continue
    
    # 最后尝试用 errors='replace'
    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
        return f.read()


def remove_ads(text: str, stats: dict = None) -> str:
    """移除常见广告"""
    if stats is None:
        stats = {}
    
    # 广告模式（按优先级排序）- 添加分类标签
    ad_patterns = [
        # 完整广告行
        (r'^[^一-龥]*更多精彩小说[^一-龥]*请访问[^一-龥]*$\n?', 0, '网站水印'),
        (r'^[^一-龥]*本文来自[^一-龥]*$\n?', 0, '网站水印'),
        (r'^本文来自\s*\n', 0, '网站水印'),
        (r'^[^一-龥]*首发[^一-龥]*$\n?', 0, '网站水印'),
        (r'^[^一-龥]*本书由[^一-龥]*整理[^一-龥]*$\n?', 0, '推广信息'),
        (r'^[^一-龥]*下载[^一-龥]*请到[^一-龥]*$\n?', 0, '推广信息'),
        (r'^[^一-龥]*温馨提示[^一-龥]*$\n?', 0, '推广信息'),
        (r'^[^一-龥]*转载请注明出处[^一-龥]*$\n?', 0, '推广信息'),
        (r'^[^一-龥]*独家首发[^一-龥]*$\n?', 0, '推广信息'),
        
        # 分隔线广告
        (r'^=+[^=\n]*=+\s*$', 0, '分隔线'),
        (r'^-+[^-\n]*-+\s*$', 0, '分隔线'),
        (r'^\*+[^*\n]*\*+\s*$', 0, '分隔线'),
        
        # URL 行
        (r'^[^一-龥]*www\.[a-z0-9\-]+\.[a-z]+[^一-龥]*$\n?', 0, 'URL'),
        (r'^[^一-龥]*https?://[^\s<>"]+[^一-龥]*$\n?', 0, 'URL'),
        
        # 行内广告（更宽松的匹配）
        (r'更多精彩小说[^，。！？\n]*', 0, '网站水印'),
        (r'本文来自[^，。！？\n]*', 0, '网站水印'),
        (r'本书由[^，。！？\n]*整理[^，。！？\n]*', 0, '推广信息'),
        (r'下载[^，。！？\n]*请到[^，。！？\n]*', 0, '推广信息'),
        (r'温馨提示[^，。！？\n]*', 0, '推广信息'),
        (r'转载请注明出处[^，。！？\n]*', 0, '推广信息'),
        (r'独家首发[^，。！？\n]*', 0, '推广信息'),
        (r'www\.[a-z0-9\-]+\.[a-z]+', 0, 'URL'),
        (r'https?://[^\s<>"]+', 0, 'URL'),
        
        # 常见广告语（方括号格式）
        (r'【[^】]*下载[^】]*】', 0, '方括号广告'),
        (r'【[^】]*APP[^】]*】', 0, '方括号广告'),
        (r'【[^】]*收藏[^】]*】', 0, '方括号广告'),
        (r'【[^】]*订阅[^】]*】', 0, '方括号广告'),
        (r'【[^】]*关注[^】]*】', 0, '方括号广告'),
        (r'【[^】]*作者[^】]*】', 0, '方括号广告'),
        (r'【[^】]*红袖[^】]*】', 0, '方括号广告'),
        (r'【[^】]*正版[^】]*】', 0, '方括号广告'),
        (r'【[^】]*防盗[^】]*】', 0, '方括号广告'),
        (r'【[^】]*QQ[^】]*】', 0, '方括号广告'),
        (r'【[^】]*微信[^】]*】', 0, '方括号广告'),
        (r'【[^】]*群[^】]*】', 0, '方括号广告'),
        (r'【[^】]*书[^】]*】', 0, '方括号广告'),
        (r'【[^】]*追更[^】]*】', 0, '方括号广告'),
        (r'【[^】]*支持[^】]*】', 0, '方括号广告'),
        (r'【[^】]*交流[^】]*】', 0, '方括号广告'),
        (r'【[^】]*阅读[^】]*】', 0, '方括号广告'),
        (r'【[^】]*小说[^】]*】', 0, '方括号广告'),
        (r'【[^】]*网站[^】]*】', 0, '方括号广告'),
        (r'【[^】]*APP[^】]*】', 0, '方括号广告'),
        (r'【[^】]*app[^】]*】', 0, '方括号广告'),
        (r'【[^】]*App[^】]*】', 0, '方括号广告'),
        # 不完整方括号广告（如 "【更多精彩，请访问"）
        (r'【[^】]*$', 0, '方括号广告'),
        # 方括号开头的广告行（即使没有闭合）
        (r'^【[^】]*\n', 0, '方括号广告'),
        # 方括号内容（即使不完整，包含广告关键词）
        (r'【[^】]*(?:精彩|访问|下载|APP|关注|订阅|收藏|支持|正版|防盗|微信|QQ|群|书|追更|阅读|小说|网站|app|App)[^】]*】?', 0, '方括号广告'),
    ]
    
    for pattern, flags, category in ad_patterns:
        before_len = len(text)
        if flags == 0:
            text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)
        else:
            text = re.sub(pattern, '', text, flags=flags)
        removed = before_len - len(text)
        if removed > 0:
            stats[category] = stats.get(category, 0) + removed
    
    return text


def fix_mojibake(text: str, stats: dict = None) -> str:
    """修复常见乱码"""
    if stats is None:
        stats = {}
    
    # 乱码映射表 - 按长度降序排列，先替换长的
    mojibake_pairs = [
        # 常见编码错误组合
        ('鏈枃', '本文'),
        ('銆€銆€', ''),
        ('銆€', ''),
        ('鈥斅', '——'),
        
        # 引号乱码组合
        ('鈥溄', '"'),
        ('鈥澨', '"'),
        ('鈥橈拷', '''),
        ('鈥橈拷', '''),
        ('锛堬拷', '（'),
        ('锛堬拷', '）'),
        ('銆愩', '【'),
        ('銆愩', '】'),
        
        # 标点符号乱码
        ('锛€', '，'),
        ('锛', '，'),
        ('锛', '。'),
        ('锛', '？'),
        ('锛', '！'),
        ('锛', '：'),
        ('锛', '；'),
        ('锛', '、'),
        ('熲', '？'),
        
        # 单字符乱码
        ('鈥', '"'),
        ('鈥', '"'),
        ('銆', ''),
        ('溄', '"'),
        ('澨', '"'),
        ('堬拷', ''),
        ('拷', ''),
        
        # UTF-8 编码错误常见乱码
        ('å…³', ''),
        ('åœ¨', ''),
        ('æœ‰', ''),
        ('å•Š', ''),
        ('çŽ°', ''),
        ('锟斤拷', ''),
        ('锟斤', ''),
    ]
    
    for wrong, correct in mojibake_pairs:
        count = text.count(wrong)
        if count > 0:
            removed = len(wrong) * count - len(correct) * count
            if removed > 0:
                stats['乱码修复'] = stats.get('乱码修复', 0) + removed
            text = text.replace(wrong, correct)
    
    # 清理残留的特殊乱码字符
    before_len = len(text)
    text = re.sub(r'[銆鈥熲锛堬拷溄澨]', '', text)
    removed = before_len - len(text)
    if removed > 0:
        stats['乱码修复'] = stats.get('乱码修复', 0) + removed
    
    # 清理 UTF-8 编码错误残留
    before_len = len(text)
    text = re.sub(r'[åæçœ‰…³œŠŽ°•]', '', text)
    removed = before_len - len(text)
    if removed > 0:
        stats['乱码修复'] = stats.get('乱码修复', 0) + removed
    
    # 清理 BOM 标记
    if '\ufeff' in text:
        count = text.count('\ufeff')
        stats['乱码修复'] = stats.get('乱码修复', 0) + count
        text = text.replace('\ufeff', '')
    
    # 清理替换字符
    if '�' in text:
        count = text.count('�')
        stats['乱码修复'] = stats.get('乱码修复', 0) + count
        text = text.replace('�', '')
    
    return text


def normalize_spaces(text: str, stats: dict = None) -> str:
    """规范化空格"""
    if stats is None:
        stats = {}
    
    # 移除所有控制字符（ASCII 0-31，除了换行符）
    before_len = len(text)
    text = re.sub(r'[\x00-\x09\x0b-\x1f]', '', text)
    removed = before_len - len(text)
    if removed > 0:
        stats['控制字符'] = stats.get('控制字符', 0) + removed
    
    # 移除中文之间的多余空格（如 "宗  主" -> "宗主"）
    # 注意：只移除空格和制表符，不移除换行符
    before_len = len(text)
    for _ in range(3):
        text = re.sub(r'([\u4e00-\u9fff])[ \t]+([\u4e00-\u9fff])', r'\1\2', text)
    removed = before_len - len(text)
    if removed > 0:
        stats['多余空格'] = stats.get('多余空格', 0) + removed
    
    # 移除行内多余空格（保留段落开头的缩进）
    lines = text.split('\n')
    result = []
    for line in lines:
        # 保留行首空格（缩进）
        stripped = line.lstrip()
        if stripped:
            # 计算原有缩进
            indent = line[:len(line) - len(stripped)]
            # 移除行内多余空格
            cleaned = re.sub(r'[ \t]+', '', stripped)
            result.append(indent + cleaned)
        else:
            result.append(line)
    
    return '\n'.join(result)


def normalize_punctuation(text: str) -> str:
    """规范化标点符号"""
    # 保护省略号 ...（先替换为临时标记）
    text = text.replace('...', '<<<ELLIPSIS>>>')
    
    # 英文标点转中文（在中文语境下）
    punct_replacements = [
        (r'([\u4e00-\u9fff]),', r'\1，'),
        (r',([\u4e00-\u9fff])', r'，\1'),
        (r'([\u4e00-\u9fff])\.', r'\1。'),
        (r'\.([\u4e00-\u9fff])', r'。\1'),
        (r'([\u4e00-\u9fff])\?', r'\1？'),
        (r'\?([\u4e00-\u9fff])', r'？\1'),
        (r'([\u4e00-\u9fff])!', r'\1！'),
        (r'!([\u4e00-\u9fff])', r'！\1'),
        (r'([\u4e00-\u9fff]):', r'\1：'),
        (r':([\u4e00-\u9fff])', r'：\1'),
        (r'([\u4e00-\u9fff]);', r'\1；'),
        (r';([\u4e00-\u9fff])', r'；\1'),
        (r'([\u4e00-\u9fff])\(', r'\1（'),
        (r'\)([\u4e00-\u9fff])', r'）\1'),
    ]
    
    for pattern, replacement in punct_replacements:
        text = re.sub(pattern, replacement, text)
    
    # 恢复省略号
    text = text.replace('<<<ELLIPSIS>>>', '...')
    
    # 统一引号
    text = re.sub(r'"([^"]*)"', r'"\1"', text)
    text = re.sub(r"'([^']*)'", r"'\1'", text)
    
    # 省略号规范化（只处理6个点以上的情况）
    text = re.sub(r'\.{6,}', '……', text)
    text = re.sub(r'。{6,}', '……', text)
    # 保留3-5个点的情况，不转换
    
    # 破折号规范化
    text = re.sub(r'-{2,}', '——', text)
    text = re.sub(r'~{2,}', '——', text)
    
    # 修复重复标点
    text = re.sub(r'，+', '，', text)
    text = re.sub(r'。+', '。', text)
    text = re.sub(r'！+', '！', text)
    text = re.sub(r'？+', '？', text)
    text = re.sub(r'，。', '。', text)
    text = re.sub(r'，？', '？', text)
    text = re.sub(r'，！', '！', text)
    
    # 修复省略号格式（混合格式如 。.。 -> ……）
    text = re.sub(r'。\.\。', '……', text)
    text = re.sub(r'\。\。', '……', text)
    # 保留单独的 .. 不转换
    
    # 移除单独成行的标点
    text = re.sub(r'^[，。！？、；：]+\s*$', '', text, flags=re.MULTILINE)
    
    # 移除重复的"屯"字（常见乱码）
    text = re.sub(r'屯{2,}', '', text)
    
    return text


def normalize_format(text: str, stats: dict = None) -> str:
    """规范化排版"""
    if stats is None:
        stats = {}
    
    # 统一换行符
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # 规范化章节标题
    # 第X章/节/回 标题处理
    # 1. 确保章节号和章节名之间有空格
    text = re.sub(r'(第[一二三四五六七八九十百千万零\d]+[章节回])([^\s\n第])', 
                  r'\1 \2', text)
    # 2. 在标题前添加空行
    text = re.sub(r'([^\n\n])(\n?)(第[一二三四五六七八九十百千万零\d]+[章节回])', 
                  r'\1\n\n\3', text)
    # 3. 章节标题后换行 - 基于行分析
    # 如果一行包含章节标题且后面还有超过15个字的内容，则在章节名后换行
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        # 检查是否是章节标题行
        match = re.match(r'(第[一二三四五六七八九十百千万零\d]+[章节回][ \t]+)([^\n]+)', line)
        if match:
            prefix = match.group(1)  # "第X章 "
            rest = match.group(2)    # 章节名+可能的内容
            # 如果rest超过8个字，说明后面有正文内容
            if len(rest) > 8:
                # 章节名通常是2-6个字
                chapter_name = rest[:6] if len(rest) > 6 else rest
                content = rest[6:] if len(rest) > 6 else ''
                if content:
                    line = prefix + chapter_name + '\n' + content
        new_lines.append(line)
    text = '\n'.join(new_lines)
    
    # 移除多余空行（保留最多2个连续空行）
    before_len = len(text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    removed = before_len - len(text)
    if removed > 0:
        stats['多余空行'] = stats.get('多余空行', 0) + removed
    
    # 移除行首行尾空格
    lines = [line.strip() for line in text.split('\n')]
    
    # 段落缩进
    result = []
    for line in lines:
        # 章节标题不缩进
        if re.match(r'^第[一二三四五六七八九十百千万零\d]+[章节回]', line):
            result.append(line)
        elif re.match(r'^Chapter\s*\d+', line, re.IGNORECASE):
            result.append(line)
        elif re.match(r'^\d+\.', line):
            result.append(line)
        elif line:  # 非空行添加缩进
            result.append('  ' + line)
        else:
            result.append(line)
    
    text = '\n'.join(result)
    
    # 移除首尾空白
    text = text.strip()
    
    return text


def clean_txt(input_path: str, output_path: str = None) -> str:
    """主清理函数"""
    print(f"处理文件: {input_path}")
    
    # 读取文件
    text = read_file(input_path)
    original_len = len(text)
    
    # 统计字典
    stats = {}
    
    # 清理流程（顺序很重要）
    text = fix_mojibake(text, stats)      # 先修复乱码
    text = remove_ads(text, stats)        # 再移除广告
    text = normalize_spaces(text, stats)  # 规范空格
    text = normalize_punctuation(text)    # 规范标点
    text = normalize_format(text, stats)  # 最后排版
    
    # 统计
    cleaned_len = len(text)
    total_removed = original_len - cleaned_len
    
    print(f"\n{'='*50}")
    print(f"清理报告")
    print(f"{'='*50}")
    print(f"原文长度: {original_len} 字符")
    print(f"清理后长度: {cleaned_len} 字符")
    print(f"移除内容: {total_removed} 字符 ({total_removed/original_len*100:.1f}%)")
    
    # 问题分类统计
    if stats:
        print(f"\n{'─'*50}")
        print(f"问题分类统计:")
        print(f"{'─'*50}")
        # 按移除数量排序
        sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        for category, count in sorted_stats:
            percent = count / total_removed * 100 if total_removed > 0 else 0
            bar = '█' * int(percent / 5)  # 每5%一个方块
            print(f"  {category:12} {count:5} 字符 ({percent:5.1f}%) {bar}")
    
    print(f"{'='*50}\n")
    
    # 输出
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"输出文件: {output_path}")
    
    return text


def main():
    if len(sys.argv) < 2:
        print("TXT 电子书清理工具 v4.0")
        print("用法: python clean_txt.py <input.txt> [output.txt]")
        print("")
        print("功能:")
        print("  - 自动检测编码 (GBK/UTF-8/GB2312/BIG5)")
        print("  - 移除广告 (网站水印、推广信息、方括号广告)")
        print("  - 修复乱码 (编码错误、标点符号、UTF-8错误)")
        print("  - 规范空格 (移除中文间多余空格)")
        print("  - 规范排版 (章节标题、段落缩进)")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace('.txt', '_cleaned.txt')
    
    clean_txt(input_path, output_path)


if __name__ == '__main__':
    main()
