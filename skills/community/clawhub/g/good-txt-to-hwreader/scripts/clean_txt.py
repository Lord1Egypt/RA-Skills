#!/usr/bin/env python3
"""
TXT 电子书清理脚本 v4.1
功能：修复乱码、去除广告、规范化排版
新增：正常文本保护机制、上下文验证
"""

import re
import sys
import chardet
from pathlib import Path

# 常见中文词汇保护词库（高频词）
PROTECTED_WORDS = {
    # 常见名词
    '门', '窗', '路', '山', '水', '风', '雨', '云', '花', '树',
    '人', '手', '眼', '心', '身', '头', '面', '口', '足', '耳',
    '道', '观', '寺', '庙', '宫', '殿', '楼', '阁', '亭', '台',
    # 常见动词
    '走', '来', '去', '看', '听', '说', '想', '做', '开', '关',
    '站', '坐', '躺', '跑', '跳', '飞', '落', '起', '入', '出',
    # 常见副词
    '缓缓', '慢慢', '轻轻', '静静', '悄悄', '渐渐', '渐渐', '徐徐',
    '突然', '忽然', '猛然', '竟然', '果然', '依然', '虽然', '自然',
    # 常见形容词
    '大', '小', '高', '低', '长', '短', '快', '慢', '新', '旧',
    '好', '坏', '美', '丑', '善', '恶', '真', '假', '实', '虚',
    # 常见时间词
    '今天', '明天', '昨天', '现在', '以后', '以前', '当时', '此时',
    # 常见方位词
    '上', '下', '左', '右', '前', '后', '里', '外', '中', '内',
}

# 常见句子结构模式（用于验证句子完整性）
SENTENCE_PATTERNS = {
    # 主语 + 谓语
    'subject_verb': r'[\u4e00-\u9fff]{1,4}(是|有|在|到|从|向|往|把|被|让|叫|给)',
    # 名词 + 副词 + 动词（如 "门缓缓打开"）
    'noun_adv_verb': r'[\u4e00-\u9fff]{1,2}(缓缓|慢慢|轻轻|静静|悄悄|渐渐|徐徐)[\u4e00-\u9fff]{1,2}',
    # 动词 + 补语（如 "走出来"、"跑过去"）
    'verb_comp': r'(走|跑|飞|跳|爬|游|飘|落)(出|进|过|回|上|下|起|开|来|去)',
}


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


def is_protected_context(text: str, position: int, window: int = 10) -> bool:
    """
    检查指定位置是否在受保护的上下文中
    
    Args:
        text: 完整文本
        position: 要检查的位置
        window: 上下文窗口大小
    
    Returns:
        True 如果在受保护的上下文中
    """
    # 获取上下文
    start = max(0, position - window)
    end = min(len(text), position + window)
    context = text[start:end]
    
    # 检查是否包含受保护词汇
    for word in PROTECTED_WORDS:
        if word in context:
            return True
    
    # 检查是否匹配常见句子结构
    for pattern_name, pattern in SENTENCE_PATTERNS.items():
        if re.search(pattern, context):
            return True
    
    return False


def validate_sentence_after_removal(original: str, removed: str, after: str) -> bool:
    """
    验证删除后的句子是否仍然通顺
    
    Args:
        original: 原始句子
        removed: 被删除的内容
        after: 删除后的句子
    
    Returns:
        True 如果删除后句子仍然通顺
    """
    # 如果删除的是空格或标点，通常没问题
    if not removed.strip() or removed in '，。！？、；：""''（）':
        return True
    
    # 检查删除后是否出现异常结构
    abnormal_patterns = [
        r'[\u4e00-\u9fff]大[\u4e00-\u9fff]',  # "X大X" 结构（如 "道观大打开"）
        r'[\u4e00-\u9fff]小[\u4e00-\u9fff]',  # "X小X" 结构
        r'[\u4e00-\u9fff]{2}[\u4e00-\u9fff]{2}',  # 四字无意义组合
    ]
    
    for pattern in abnormal_patterns:
        if re.search(pattern, after) and not re.search(pattern, original):
            # 删除后出现了异常结构
            return False
    
    return True


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
        (r'【[^】]*精彩[^】]*】?', 0, '方括号广告'),
        (r'【[^】]*访问[^】]*】?', 0, '方括号广告'),
        (r'【[^】]*$', 0, '方括号广告'),  # 只有开头没有结尾的方括号
        
        # ===== 圆括号广告 =====
        (r'（[^）]*本章[^）]*未完[^）]*）', 0, '圆括号广告'),
        (r'（[^）]*翻页[^）]*）', 0, '圆括号广告'),
        (r'（[^）]*精彩[^）]*继续[^）]*）', 0, '圆括号广告'),
        (r'（[^）]*访问[^）]*）', 0, '圆括号广告'),
        (r'（[^）]*支持[^）]*正版[^）]*）', 0, '圆括号广告'),
        (r'（[^）]*购买[^）]*）', 0, '圆括号广告'),
        (r'（[^）]*请[^）]*访问[^）]*）', 0, '圆括号广告'),
        (r'\([^)]*本章[^)]*未完[^)]*\)', 0, '圆括号广告'),
        (r'\([^)]*翻页[^)]*\)', 0, '圆括号广告'),
        
        # ===== 星号装饰广告 =====
        (r'\*{3,}[^*\n]*\*{3,}', 0, '星号广告'),
        (r'☆{2,}[^☆\n]*☆{2,}', 0, '星号广告'),
        (r'★{2,}[^★\n]*★{2,}', 0, '星号广告'),
        (r'✦{2,}[^✦\n]*✦{2,}', 0, '星号广告'),
        (r'✧{2,}[^✧\n]*✧{2,}', 0, '星号广告'),
        
        # ===== 分隔线广告 =====
        (r'—{5,}', 0, '分隔线广告'),
        (r'═{5,}', 0, '分隔线广告'),
        (r'━{5,}', 0, '分隔线广告'),
        (r'─{5,}', 0, '分隔线广告'),
        (r'_{5,}', 0, '分隔线广告'),
        (r'~{5,}', 0, '分隔线广告'),
        (r'={5,}', 0, '分隔线广告'),
        (r'-{5,}', 0, '分隔线广告'),
        (r'\.{10,}', 0, '分隔线广告'),
        
        # ===== 特殊字符装饰广告 =====
        (r'◆{3,}[^◆\n]*◆{3,}', 0, '装饰广告'),
        (r'◇{3,}[^◇\n]*◇{3,}', 0, '装饰广告'),
        (r'●{3,}[^●\n]*●{3,}', 0, '装饰广告'),
        (r'○{3,}[^○\n]*○{3,}', 0, '装饰广告'),
        (r'■{3,}[^■\n]*■{3,}', 0, '装饰广告'),
        (r'□{3,}[^□\n]*□{3,}', 0, '装饰广告'),
        (r'▲{3,}[^▲\n]*▲{3,}', 0, '装饰广告'),
        (r'△{3,}[^△\n]*△{3,}', 0, '装饰广告'),
        (r'▶{3,}[^▶\n]*▶{3,}', 0, '装饰广告'),
        (r'▷{3,}[^▷\n]*▷{3,}', 0, '装饰广告'),
        (r'►{3,}[^►\n]*►{3,}', 0, '装饰广告'),
        (r'▼{3,}[^▼\n]*▼{3,}', 0, '装饰广告'),
        (r'▽{3,}[^▽\n]*▽{3,}', 0, '装饰广告'),
        (r'◀{3,}[^◀\n]*◀{3,}', 0, '装饰广告'),
        (r'◁{3,}[^◁\n]*◁{3,}', 0, '装饰广告'),
        (r'◄{3,}[^◄\n]*◄{3,}', 0, '装饰广告'),
        
        # ===== 纯文本广告（无符号包裹）=====
        (r'^关注公众号[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^关注微信[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^本书首发于[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^请记住本站[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^记住本站[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^本站域名[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^无弹窗[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^无广告[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^最新章节[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^第一时间[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^扫码[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^推荐[^\n]*阅读[^\n]*$', re.MULTILINE, '文本广告'),
        (r'^热门推荐[^\n]*$', re.MULTILINE, '文本广告'),
        
        # ===== 章节末尾广告 =====
        (r'^ps[：:][^\n]*$', re.MULTILINE | re.IGNORECASE, '章节广告'),
        (r'^PS[：:][^\n]*$', re.MULTILINE, '章节广告'),
        (r'^本章说[：:][^\n]*$', re.MULTILINE, '章节广告'),
        (r'^作者有话说[：:][^\n]*$', re.MULTILINE, '章节广告'),
        (r'^作者说[：:][^\n]*$', re.MULTILINE, '章节广告'),
        (r'^求推荐票[^\n]*$', re.MULTILINE, '章节广告'),
        (r'^求月票[^\n]*$', re.MULTILINE, '章节广告'),
        (r'^求收藏[^\n]*$', re.MULTILINE, '章节广告'),
        (r'^求打赏[^\n]*$', re.MULTILINE, '章节广告'),
        (r'^求票[^\n]*$', re.MULTILINE, '章节广告'),
        (r'^感谢[^\n]*打赏[^\n]*$', re.MULTILINE, '章节广告'),
        (r'^感谢[^\n]*投[^\n]*票[^\n]*$', re.MULTILINE, '章节广告'),
        
        # ===== 防盗章节 =====
        (r'^防盗章节[^\n]*$', re.MULTILINE, '防盗章节'),
        (r'^本章为防盗[^\n]*$', re.MULTILINE, '防盗章节'),
        (r'^请.*分钟后刷新[^\n]*$', re.MULTILINE, '防盗章节'),
        (r'^防盗[^\n]*刷新[^\n]*$', re.MULTILINE, '防盗章节'),
        
        # ===== URL/域名广告 =====
        (r'https?://[^\s<>"{}|\\^`\[\]]+', 0, 'URL广告'),
        (r'www\.[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,}[^\s]*', 0, 'URL广告'),
        (r'm\.[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,}[^\s]*', 0, 'URL广告'),
        (r'[a-zA-Z0-9][-a-zA-Z0-9]*\.(com|net|org|cn|io|xyz|top|vip|cc|me)[^\s]*', 0, 'URL广告'),
        
        # ===== 二维码相关 =====
        (r'\[二维码\]', 0, '二维码广告'),
        (r'二维码[^\n]*', 0, '二维码广告'),
        (r'扫码[^\n]*关注[^\n]*', 0, '二维码广告'),
        
        # ===== 推荐广告 =====
        (r'推荐[：:][^\n]*《[^》]+》[^\n]*', 0, '推荐广告'),
        (r'《[^》]+》[^《\n]*推荐[^\n]*', 0, '推荐广告'),
        (r'同类推荐[^\n]*', 0, '推荐广告'),
        (r'猜你喜欢[^\n]*', 0, '推荐广告'),
        (r'《[^》]+》作者[：:][^\n]*', 0, '推荐广告'),
        (r'《[^》]+》正在[^\n]*', 0, '推荐广告'),
        (r'《[^》]+》连载[^\n]*', 0, '推荐广告'),
        (r'《[^》]+》完结[^\n]*', 0, '推荐广告'),
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
        # ===== 经典乱码字符 =====
        ('锟斤拷', ''),
        ('锟斤', ''),
        ('烫烫烫', ''),
        ('屯屯屯', ''),
        ('锘', ''),  # BOM标记残留
        
        # ===== 常见编码错误组合 =====
        ('鏈枃', '本文'),
        ('銆€銆€', ''),
        ('銆€', ''),
        ('鈥斅', '——'),
        
        # ===== 引号乱码组合 =====
        ('鈥溄', '"'),
        ('鈥澨', '"'),
        ('鈥橈拷', '''),
        ('鈥橈拷', '''),
        ('锛堬拷', '（'),
        ('锛堬拷', '）'),
        ('銆愩', '【'),
        ('銆愩', '】'),
        
        # ===== 特殊符号乱码（引号、破折号等）=====
        ('â€"', '—'),      # 破折号
        ('â€œ', '"'),      # 左双引号
        ('â€', '"'),       # 右双引号
        ('â€˜', '''),      # 左单引号
        ('â€™', '''),      # 右单引号
        ('â€¦', '…'),      # 省略号
        ('â€€', ' '),      # 空格
        
        # ===== 标点符号乱码 =====
        ('锛€', '，'),
        ('锛', '，'),
        ('锛', '。'),
        ('锛', '？'),
        ('锛', '！'),
        ('锛', '：'),
        ('锛', '；'),
        ('锛', '、'),
        ('熲', '？'),
        # 全角标点乱码
        ('ï¼Œ', '，'),
        ('ï¼›', '；'),
        ('ï¼š', '：'),
        ('ï¼Ÿ', '？'),
        ('ï¼', '！'),
        ('ï¼ˆ', '（'),
        ('ï¼‰', '）'),
        ('ï¼', '.'),
        
        # ===== 单字符乱码 =====
        ('鈥', '"'),
        ('鈥', '"'),
        ('銆', ''),
        ('溄', '"'),
        ('澨', '"'),
        ('堬拷', ''),
        ('拷', ''),
        
        # ===== UTF-8 编码错误（精确映射）=====
        ('å…³', '关'),
        ('åœ¨', '在'),
        ('æœ‰', '有'),
        ('å•Š', '啊'),
        ('çŽ°', '现'),
        
        # ===== GBK/GB2312 编码错误（常见字）=====
        # 注意：这些映射需要根据实际文件编码情况调整
        # 由于编码复杂性，这里只保留最确定的映射
        
        # ===== 双重编码错误（常见词组）=====
        ('æˆ\'çš"', '我的'),
        ('ä½ å¥½', '你好'),
        ('è¿™æ˜¯', '这是'),
        
        # ===== HTML 实体编码残留 =====
        ('&nbsp;', ' '),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&amp;', '&'),
        ('&quot;', '"'),
        ('&#39;', "'"),
        ('&apos;', "'"),
        
        # ===== 混合编码乱码 =====
        ('銆€', ''),
        ('鈥€', ''),
        ('熲€', ''),
        ('銆€銆€', ''),
        ('鈥€鈥€', ''),
    ]
    
    for wrong, correct in mojibake_pairs:
        count = text.count(wrong)
        if count > 0:
            removed = len(wrong) * count - len(correct) * count
            if removed > 0:
                stats['乱码修复'] = stats.get('乱码修复', 0) + removed
            text = text.replace(wrong, correct)
    
    # ===== HTML 数字实体编码 =====
    # &#x4e2d; → 中 (十六进制)
    def decode_hex_entity(match):
        try:
            return chr(int(match.group(1), 16))
        except:
            return match.group(0)
    text = re.sub(r'&#x([0-9a-fA-F]+);', decode_hex_entity, text)
    
    # &#20013; → 中 (十进制)
    def decode_dec_entity(match):
        try:
            return chr(int(match.group(1)))
        except:
            return match.group(0)
    text = re.sub(r'&#(\d+);', decode_dec_entity, text)
    
    # ===== Unicode 转义残留 =====
    # \u4e2d → 中
    def decode_unicode_escape(match):
        try:
            return chr(int(match.group(1), 16))
        except:
            return match.group(0)
    text = re.sub(r'\\u([0-9a-fA-F]{4})', decode_unicode_escape, text)
    
    # ===== 清理残留的特殊乱码字符 =====
    before_len = len(text)
    # 只清理明确的乱码字符，不清理可能是正常文本的内容
    text = re.sub(r'[銆鈥熲锛堬拷溄澨]', '', text)
    removed = before_len - len(text)
    if removed > 0:
        stats['乱码修复'] = stats.get('乱码修复', 0) + removed
    
    # ===== 清理 UTF-8 编码错误残留 =====
    before_len = len(text)
    # 清理常见的乱码组合
    text = re.sub(r'å[…œ][³Š]', '', text)  # å…³, åœŠ 等
    text = re.sub(r'æ[œ‰][‰œ]', '', text)  # æœ‰ 等
    text = re.sub(r'ç[Ž°][°Ž]', '', text)  # çŽ° 等
    # 清理 GBK 编码错误残留
    text = re.sub(r'[æç][œ‰ˆš°Ž‰][€œ‰ˆš°Ž‰]', '', text)
    removed = before_len - len(text)
    if removed > 0:
        stats['乱码修复'] = stats.get('乱码修复', 0) + removed
    
    # ===== 清理控制字符 =====
    # NULL字符
    if '\x00' in text:
        count = text.count('\x00')
        stats['乱码修复'] = stats.get('乱码修复', 0) + count
        text = text.replace('\x00', '')
    
    # EOF标记
    if '\x1a' in text:
        count = text.count('\x1a')
        stats['乱码修复'] = stats.get('乱码修复', 0) + count
        text = text.replace('\x1a', '')
    
    # BOM 标记
    if '\ufeff' in text:
        count = text.count('\ufeff')
        stats['乱码修复'] = stats.get('乱码修复', 0) + count
        text = text.replace('\ufeff', '')
    
    # 替换字符
    if '�' in text:
        count = text.count('�')
        stats['乱码修复'] = stats.get('乱码修复', 0) + count
        text = text.replace('�', '')
    
    # ===== 清理特殊空格 =====
    # NBSP (非断行空格)
    if '\xa0' in text:
        count = text.count('\xa0')
        stats['乱码修复'] = stats.get('乱码修复', 0) + count
        text = text.replace('\xa0', ' ')
    
    # 全角空格
    if '\u3000' in text:
        count = text.count('\u3000')
        stats['乱码修复'] = stats.get('乱码修复', 0) + count
        text = text.replace('\u3000', ' ')
    
    # ===== 清理重复的"烫"和"屯"字（常见乱码）=====
    text = re.sub(r'烫{3,}', '', text)
    text = re.sub(r'屯{3,}', '', text)
    
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
    
    # Chapter X 标题
    text = re.sub(r'([^\n\n])(\n?)(Chapter\s*\d+)', 
                  r'\1\n\n\3', text, flags=re.IGNORECASE)
    
    # 数字章节 (1. 标题)
    text = re.sub(r'^[ \t]*(\d+)[\.、\s]+([^\n]{1,30})$', 
                  r'\n\n\1. \2\n\n', text, flags=re.MULTILINE)
    
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


def generate_report(input_path: str, original_len: int, cleaned_len: int, stats: dict, output_path: str) -> str:
    """生成 Markdown 格式的清理报告"""
    total_removed = original_len - cleaned_len
    
    report = f"""# 《{Path(input_path).stem}》清理报告

## 📊 清理统计

| 指标 | 数值 |
|-----|------|
| 原文长度 | {original_len:,} 字符 |
| 清理后长度 | {cleaned_len:,} 字符 |
| 移除内容 | {total_removed:,} 字符 ({total_removed/original_len*100:.1f}%) |

## 🔧 问题分类统计

| 问题类型 | 移除字符数 | 占比 |
|---------|-----------|------|
"""
    
    if stats:
        sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        for category, count in sorted_stats:
            percent = count / total_removed * 100 if total_removed > 0 else 0
            report += f"| {category} | {count:,} | {percent:.1f}% |\n"
    else:
        report += "| 无问题发现 | - | - |\n"
    
    report += f"""
## 📁 输出文件

- **清理后文件**: `{Path(output_path).name}`
- **编码**: UTF-8
- **状态**: 已准备好导入阅读器

---
*由 good-txt-to-hwreader 技能生成*
"""
    
    return report


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
    
    # 生成报告文件
    report_path = output_path.replace('.txt', '_清理报告.md') if output_path else input_path.replace('.txt', '_清理报告.md')
    report = generate_report(input_path, original_len, cleaned_len, stats, output_path or input_path)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告文件: {report_path}")
    
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
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace('.txt', '_清理版.txt')
    
    clean_txt(input_path, output_path)


if __name__ == '__main__':
    main()
