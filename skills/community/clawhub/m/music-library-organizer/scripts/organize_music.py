#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐库整理脚本
==============

功能：
    扫描源文件夹下的所有音乐文件 + 歌词文件，按以下规范整理到目标文件夹。

目标目录结构（三级）：
    目标根目录/首字母/歌手名/歌曲文件
    - 一级目录：歌手名首字母（中文取拼音首字母）
    - 二级目录：第一位歌手
    - 三级文件：规范命名后的音乐 / 歌词

命名规范：
    音乐文件：歌手 - 歌曲名.格式
    歌词文件：歌手 - 歌曲名.lrc (与音乐主名一致)

去重规则（按音质优先级保留唯一）：
    无损 (FLAC/APE/WAV) > 320k MP3 > 普通 MP3 > 其他
    被替换文件 → 目标根目录/_低音质备份/

依赖：
    必需：无（纯标准库即可运行，基础模式）
    推荐：pip install mutagen pypinyin
        - mutagen：读取 ID3 标签（比纯文件名解析准确得多）
        - pypinyin：中文歌手名转拼音首字母（推荐，否则部分中文走"其他"目录）

使用：
    1. 修改下方 SOURCE_DIR / TARGET_DIR
    2. 先用 --dry-run 跑一遍，会生成 CSV 报告，不动文件
    3. 检查报告 OK 后，再加 --apply 真正执行
    4. 支持 --resume 从上次断点继续
    5. 每次执行会写一份 operations_时间戳.log（可回滚）
"""

import os
import sys
import re
import csv
import json
import shutil
import hashlib
import argparse
import unicodedata
from pathlib import Path
from datetime import datetime

# ============== 配置 ==============
SOURCE_DIR = "/volume4/media2/音乐"
TARGET_DIR = "/volume4/media2/音乐_整理"
# ===================================

# 音乐文件后缀
AUDIO_EXTS = {'.flac', '.ape', '.wav', '.mp3', '.m4a', '.ogg', '.wma', '.aac', '.opus', '.aiff', '.aif'}
LYRIC_EXTS = {'.lrc', '.txt'}
SKIP_DIRS = {'attachments', '_低音质备份', '.opencode', '.git'}

# 多歌手分隔符（统一替换为 &）
ARTIST_SEPARATORS = [',', '，', '/', '、', '；', ';', ' feat. ', ' feat ', ' Feat. ', ' Feat ',
                     ' featuring ', ' ft. ', ' ft ', ' x ', ' X ']

# 音质优先级（数字越大越优）
QUALITY_RANK = {
    'flac': 100, 'ape': 95, 'wav': 90,
    'mp3_320': 70, 'mp3_high': 60, 'mp3': 50,
    'm4a': 40, 'aac': 35, 'ogg': 30, 'opus': 30, 'wma': 20, 'other': 10
}

# 常见特殊字符清洗
INVALID_FNAME_CHARS = r'[\\/:*?"<>|\r\n\t]'

# ============== 拼音首字母模块 ==============
# 优先用 pypinyin，没装就退化到"基础模式"（中文走"其他"）
try:
    from pypinyin import lazy_pinyin, Style
    HAS_PYPINYIN = True
except ImportError:
    HAS_PYPINYIN = False


def get_first_letter(artist_name):
    """
    提取歌手名的首字母（大写）
    - 英文 → 取首字母大写
    - 中文 → pypinyin 转拼音首字母
    - 数字/无法识别 → 返回 None（外部用"其他"）
    """
    if not artist_name:
        return None
    s = str(artist_name).strip()
    if not s:
        return None

    first_char = s[0]

    # 数字开头
    if first_char.isdigit():
        return None

    # 英文 A-Z
    if first_char.isascii() and first_char.isalpha():
        return first_char.upper()

    # 中日韩等非 ASCII 字符
    if HAS_PYPINYIN:
        try:
            # 用 pypinyin 转首个汉字的拼音首字母
            py = lazy_pinyin(first_char, style=Style.FIRST_LETTER)
            if py and py[0] and py[0][0].isascii():
                return py[0][0].upper()
        except Exception:
            pass
        return None
    else:
        # 基础模式：没装 pypinyin 时用一张常用字映射表
        # 覆盖主流歌手姓氏和常见首字，兜底走"其他"
        CN_MAP = {
            '周林陈王李张刘黄赵吴徐孙马朱胡郭何高罗郑梁谢宋唐许韩冯邓曹彭曾萧田董袁潘蔡蒋余杜叶程苏魏吕丁任姚沈钟姜范方石谭廖韦熊金侯龚文葛黎常武乔贺赖尹易霍钱汤关伍江梅'
            '三井仓吉荒鬼小久保田野明山中井佐佐木高桥渡边伊藤'
        }
        if first_char in CN_MAP:
            return CN_MAP[first_char]
        return None


# ============== 文件名/标签解析 ==============

def sanitize_filename(name):
    """
    清洗文件名/文件夹名中的非法字符
    把 \\ / : * ? " < > | 替换为空格，同时去掉 NUL (\x00) 和控制字符
    """
    if not name:
        return name
    # 先去掉 NUL 字符（防止 embedded null byte 错误）
    if isinstance(name, str):
        name = name.replace('\x00', '')
    name = re.sub(INVALID_FNAME_CHARS, ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def normalize_artist_field(raw):
    """
    多歌手处理：把多种分隔符（feat.、&、,、/、,、x）统一成 &
    返回：(join后的歌手串, 第一位歌手)
    """
    if not raw:
        return '', ''
    s = str(raw)
    # 统一分隔符
    for sep in ARTIST_SEPARATORS:
        s = s.replace(sep, '&')
    # 连续 & 压成单个
    s = re.sub(r'\s*&\s*', ' & ', s)
    s = re.sub(r'(\s*&\s*){2,}', ' & ', s)
    s = s.strip(' &')
    first = s.split('&')[0].strip() if s else ''
    return s, first


def normalize_to_standard(stem, parent_hint=None):
    """
    【两阶段 - 第一阶段】把任意格式的文件名 stem 规范化成 "歌手 - 歌曲" 标准格式。

    输入示例（假设在 1个球/ 目录下，parent_hint='1个球'）：
      "1个球 - 大雨还在下"           → "1个球 - 大雨还在下"     (标准)
      "大雨还在下 - 1个球"           → "1个球 - 大雨还在下"     (颠倒→纠正)
      "1个球-大雨还在下"             → "1个球 - 大雨还在下"     (补空格)
      "1个球-大雨还在下 (Live)"      → "1个球 - 大雨还在下 (Live)"
      "1个球 - 1665-大雨还在下"      → "1个球 - 大雨还在下"     (去编号)
      "1个球 - 大雨还在下 - 1个球"   → "1个球 - 大雨还在下"     (去重复)
      "大雨还在下"                    → "1个球 - 大雨还在下"     (借父目录补歌手)
      "Alan Walker&K-391 - Different World" → "Alan Walker & K-391 - Different World"
      "Coldplay-Yellow"             → "Coldplay - Yellow"

    返回：规范化后的 stem
    """
    if not stem:
        return stem

    s = stem.strip()
    # 1. 去掉开头的数字编号 + dash（"1665-歌名" → "歌名"）
    s = re.sub(r'^\d{2,5}-\s*', '', s)
    # 2. 去掉开头的 "字母_数字-"（"A_1665-歌名" → "歌名"）
    s = re.sub(r'^[A-Za-z]+_\d+-\s*', '', s)
    # 3. 去掉首尾的 [歌词] / (live) 这类括号说明但保留（这些是歌名一部分）
    s = s.strip()

    # 4. 找主分隔符（" - " > " – " > " — " > " -" > "-"），split 后两侧
    sep_used = None
    parts = None
    for sep in [' - ', ' – ', ' — ', ' -', '-', '_', '  ']:
        if sep in s:
            cand = s.split(sep, 1)
            if len(cand) == 2 and cand[0].strip() and cand[1].strip():
                parts = [cand[0].strip(), cand[1].strip()]
                sep_used = sep
                break

    if parts is None:
        # 没有分隔符
        if parent_hint:
            return f"{parent_hint} - {s}"
        return s

    left, right = parts

    # 5. 多歌手分隔符统一成 " & "（feat., ft., x 等 → &）
    def normalize_multi(seg):
        if not seg:
            return seg
        out = seg
        # 不区分大小写替换常见分隔符
        for old, new in [
            (r'\s+feat\.?\s+', ' & '),
            (r'\s+ft\.?\s+', ' & '),
            (r'\s+featuring\s+', ' & '),
            (r'\s+with\s+', ' & '),
            (r'\s+x\s+', ' & '),
            (r'\s+X\s+', ' & '),
            (r'\s*/\s*', ' & '),
            (r'\s*、\s*', ' & '),
            (r'\s*;\s*', ' & '),
            (r'\s*；\s*', ' & '),
            (r'\s*,\s*', ' & '),
            (r'\s*，\s*', ' & '),
        ]:
            out = re.sub(old, new, out, flags=re.IGNORECASE)
        # 已有 & 规范化空格
        out = re.sub(r'\s*&\s*', ' & ', out)
        out = re.sub(r'(\s*&\s*){2,}', ' & ', out)
        return out.strip(' &')

    left = normalize_multi(left)
    right = normalize_multi(right)

    # 6. 去 "X - ... - X" 重复（如 "1个球 - 大雨还在下 - 1个球" → "1个球 - 大雨还在下"）
    if right == left:
        # 两侧完全相同 → 整个 stem 当歌名
        return f"{left} - {right}"  # 这种情况很少，保持原样
    # 如果 right 以 " - left" 结尾，去掉
    if right.endswith(' - ' + left):
        right = right[:-(len(left) + 3)]
    # 如果 left 以 " - right" 结尾，去掉
    elif left.endswith(' - ' + right):
        left = left[:-(len(right) + 3)]
    # 如果 right 整个是 left - X 形式（right 里也含 left）
    elif right.startswith(left + ' - '):
        right = right[len(left) + 3:]
    elif left.startswith(right + ' - '):
        left = left[:-(len(right) + 3)]

    # 7. 判断谁是歌手：基于"含多歌手标记"+"父目录旁证"+"长度/特征"
    def looks_artist_combination(seg):
        if not seg:
            return False
        return ' & ' in seg

    def looks_song_title(seg):
        """像歌名：含括号说明、live/remix/版等关键词、或纯数字编号"""
        if not seg:
            return False
        not_artist_signs = [
            '(live)', '(remix)', '(demo)', '(acoustic)', '(cover)', '(伴奏)', '(纯音乐)',
            '（live）', '（现场）', '（伴奏）', '（remix）', '（demo）',
            '伴奏', '纯音乐', 'instrumental', 'remaster', 'mix版', 'edit',
        ]
        s_low = seg.lower()
        for bad in not_artist_signs:
            if bad in s_low or bad in seg:
                return True
        # 长度过短 (<=1) 或过长 (>25) 也不像歌手
        if len(seg) <= 1 or len(seg) > 25:
            return True
        return False

    left_is_artist_combo = looks_artist_combination(left)
    right_is_artist_combo = looks_artist_combination(right)
    left_looks_title = looks_song_title(left)
    right_looks_title = looks_song_title(right)

    # 启发式决策矩阵：
    # 规则 1：含 &/多歌手标记 → 必是歌手
    if left_is_artist_combo and not right_is_artist_combo:
        artist, title = left, right
    elif right_is_artist_combo and not left_is_artist_combo:
        artist, title = right, left
    elif left_is_artist_combo and right_is_artist_combo:
        # 两边都像歌手组合 → 取第一个作为歌手
        artist = left.split(' & ')[0].strip()
        # 歌名放剩下那一边较短的
        title = right if len(right) <= len(left) else left
    # 规则 2：含括号说明的是歌名
    elif right_looks_title and not left_looks_title:
        artist, title = left, right
    elif left_looks_title and not right_looks_title:
        artist, title = right, left
    # 规则 3：父目录旁证
    elif parent_hint:
        # 如果左/右 跟 parent_hint 完全一致，那一边就是歌手
        if left == parent_hint and right != parent_hint:
            artist, title = left, right
        elif right == parent_hint and left != parent_hint:
            artist, title = right, left
        elif parent_hint in left and parent_hint not in right:
            artist, title = left, right
        elif parent_hint in right and parent_hint not in left:
            artist, title = right, left
        else:
            # 父目录都不能对上 → 默认 left 是歌手
            artist, title = left, right
    else:
        # 规则 4：都没证据 → 默认 left 是歌手
        artist, title = left, right

    # 8. 重新拼接成标准格式 "歌手 - 歌曲"
    result = f"{artist} - {title}"
    return result


def parse_filename(filename, ext):
    """
    【两阶段 - 第二阶段】已经规范化过了，这里只做最终的简单 split。
    返回 (歌手, 歌曲名)，没分隔符返回 (None, 整个stem)
    """
    stem = Path(filename).stem
    if ' - ' in stem:
        parts = stem.split(' - ', 1)
        return parts[0].strip(), parts[1].strip()
    return None, stem



def is_likely_artist_advanced(s):
    """
    改进版歌手启发式判断。
    返回值: True=必是歌手, False=必不是歌手, None=不确定
    """
    if not s:
        return False
    s = s.strip()
    if len(s) == 0:
        return False
    # 太长几乎不可能是歌手名（歌手一般 2-15 字符）
    if len(s) > 25:
        return False
    s_low = s.lower()
    # 【强证据】 含多歌手符号 → 必是歌手
    if looks_like_artist_combination(s):
        return True
    # 【强否定】 含括号、live、remix 等 → 必不是歌手
    not_artist_signs = [
        '(live)', '(remix)', '(demo)', '(acoustic)', '(cover)',
        '(版)', '（版）', '（live）', '（现场）', '（伴奏）',
        '伴奏', '纯音乐', 'instrumental', 'remaster', 'mix', 'edit',
        'remix', 'live版', '现场版', 'demo版', '试听', '试听版', '抢先',
    ]
    for bad in not_artist_signs:
        if bad in s_low or bad in s:
            return False
    # 【强否定】 含 “/” 或 “、” 一定不是单词歌名（多为多个歌手或歌名）
    if '/' in s or '、' in s:
        return True
    # 【不确定】 默认 交给调用者
    return None


def is_likely_artist(s):
    """启发式判断一个字符串像不像歌手名"""
    if not s:
        return False
    s = s.strip()
    if len(s) > 30:
        return False
    # 包含特定关键词的不像歌手
    bad = ['live', 'remix', 'version', 'demo', 'mix', 'edit', 'cover', '版',
           '伴奏', '纯音乐', 'instrumental', 'remaster', 'acoustic']
    s_low = s.lower()
    for b in bad:
        if b in s_low:
            return False
    return True


def read_audio_meta(filepath, no_tag=False):
    """
    读取音频文件的元数据，返回 (artist, title, album) 或 (None, None, None)
    优先用 mutagen；没装或读不到则返回 None → 走文件名解析兜底
    父目录级缓存：同一目录只读一次（加速 10-50x）
    no_tag=True 时直接返回 None（最快）
    """
    if no_tag:
        return None, None, None
    parent = os.path.dirname(filepath)
    if parent in read_audio_meta._cache:
        return read_audio_meta._cache[parent]
    try:
        from mutagen import File
        f = File(filepath)
        if f is None or f.tags is None:
            result = (None, None, None)
        else:
            t = f.tags
            def get(*keys):
                for k in keys:
                    v = t.get(k)
                    if v:
                        if isinstance(v, list):
                            return str(v[0])
                        return str(v)
                return None
            artist = get('TPE1', 'artist', 'Artist', '\xa9ART', 'aART', 'Artist')
            title = get('TIT2', 'title', 'Title', '\xa9nam', '\xa9Nam')
            # 【bug 修复】如果 ID3 标签里含 NUL 字符（mutagen 解析坏文件的副作用），
            # 视为无效，强制回退到文件名解析
            if artist and ('\x00' in artist):
                artist = None
            if title and ('\x00' in title):
                title = None
            result = (artist, title, None)
        read_audio_meta._cache[parent] = result
        return result
    except ImportError:
        return None, None, None
    except Exception:
        return None, None, None
read_audio_meta._cache = {}


# 全局开关：是否跳过 ID3 读取
_global_no_tag = False




def extract_artist_title(filepath):
    """
    【两阶段 - 第二阶段】从标签或文件名解析 (歌手_完整, 歌手_第一, 歌曲名, 来源)。
    
    核心思路（解决"歌名 - 歌手"颠倒问题）：
      第一步：先调 normalize_to_standard() 把任意格式 stem 规范化成 "歌手 - 歌曲"
              这个函数已经处理了：去编号、补空格、纠正颠倒、补歌手、统一多歌手分隔符
      第二步：规范化后简单 split(' - ', 1) 拿歌手和歌名（100% 准）
    
    ID3 标签优先：如果标签里 artist + title 都在，直接用；标签歌手也走 normalize_artist_field
    """
    # 0. 父目录旁证
    parent_dir_hint = None
    parent = os.path.dirname(filepath)
    parent_basename = os.path.basename(parent)
    if parent_basename and not parent_basename.startswith('.') and \
       parent_basename not in {'音乐', 'music', 'Music', '_低音质备份', '其他'}:
        # 处理 1665-歌名 这种编号目录
        cleaned_hint = re.sub(r'^\d{2,5}-', '', parent_basename).strip()
        if cleaned_hint and ' - ' not in cleaned_hint and ',' not in cleaned_hint and '&' not in cleaned_hint:
            parent_dir_hint = cleaned_hint

    # 1. 优先读 ID3 标签
    tag_artist, tag_title, _ = read_audio_meta(filepath, no_tag=_global_no_tag)
    if tag_artist and tag_title:
        # 标签里的歌手先规范化（多歌手统一 & 分隔）
        full_artist, first_artist = normalize_artist_field(tag_artist)
        return full_artist, first_artist, tag_title.strip(), 'tag'

    # 2. 文件名解析：先规范化
    fn = os.path.basename(filepath)
    stem = Path(fn).stem
    normalized = normalize_to_standard(stem, parent_hint=parent_dir_hint)
    
    # 3. 规范化后 split
    if ' - ' in normalized:
        artist, title = normalized.split(' - ', 1)
        artist = artist.strip()
        title = title.strip()
    else:
        # 规范化后还是没有 " - "（极少见）
        artist = parent_dir_hint or ''
        title = normalized

    if not title:
        return '', '', normalized, 'filename'

    full_artist, first_artist = normalize_artist_field(artist)
    return full_artist, first_artist, title, 'normalized'




def get_quality_rank(filepath):
    """评估文件音质等级"""
    ext = Path(filepath).suffix.lower().lstrip('.')
    if ext in ('flac', 'ape', 'wav'):
        return QUALITY_RANK[ext]
    if ext == 'mp3':
        # 尝试读比特率
        try:
            from mutagen import File
            f = File(filepath)
            if f and f.info and hasattr(f.info, 'bitrate'):
                br = f.info.bitrate
                if br >= 320000:
                    return QUALITY_RANK['mp3_320']
                elif br >= 256000:
                    return QUALITY_RANK['mp3_high']
        except Exception:
            pass
        return QUALITY_RANK['mp3']
    return QUALITY_RANK.get(ext, QUALITY_RANK['other'])


def file_size_kb(p):
    try:
        return os.path.getsize(p) // 1024
    except OSError:
        return 0


# ============== 主流程 ==============

class MusicOrganizer:
    def __init__(self, source, target, dry_run=True, no_tag=False):
        self.source = Path(source)
        self.target = Path(target)
        self.dry_run = dry_run
        self.no_tag = no_tag     # 跳过 ID3 读取，10x 加速
        self.backup_dir = self.target / '_低音质备份'
        self.report = []           # CSV 报告数据
        self.operations = []       # 操作日志（用于回滚）
        self.stats = {
            'total': 0, 'renamed': 0, 'moved': 0, 'backed_up': 0,
            'lyrics_matched': 0, 'lyrics_kept': 0, 'skipped': 0, 'errors': 0
        }

        # 目标去重表：key = (首字母, 歌手, 歌曲) → (path, rank, size)
        self.target_index = {}

    def run(self):
        print(f"{'[干跑]' if self.dry_run else '[执行]'} 扫描源: {self.source}")
        print(f"        目标: {self.target}")
        print(f"        pypinyin={'可用' if HAS_PYPINYIN else '未安装(中文会走「其他」)'}")
        print(f"        mutagen={'可用' if self._has_mutagen() else '未安装(只解析文件名)'}")
        print()

        if not self.source.exists():
            print(f"❌ 源目录不存在: {self.source}")
            return

        # 第一遍：扫描所有音乐文件，规划
        music_files = self.scan_music()
        print(f"找到 {len(music_files)} 个音乐文件")

        # 第二遍：扫描所有歌词文件（但先不绑定，等音乐处理完再做匹配）
        lyric_files = self.scan_lyrics()
        print(f"找到 {len(lyric_files)} 个歌词文件")

        # 处理音乐
        print("\n--- 处理音乐文件 ---")
        self.process_music(music_files)

        # 处理歌词
        print("\n--- 处理歌词文件 ---")
        self.process_lyrics(lyric_files)

        # 输出报告
        self.write_reports()

        # 汇总
        print("\n========== 汇总 ==========")
        for k, v in self.stats.items():
            print(f"  {k:20s} : {v}")
        print(f"\n日志：{self.log_path}")
        print(f"报告：{self.report_path}")

    def _has_mutagen(self):
        try:
            import mutagen
            return True
        except ImportError:
            return False

    def scan_music(self):
        """用 find 快速扫描（比 os.walk 在 NAS 上快 10-50x）"""
        import subprocess
        # 拼接 find -name 参数（必须用括号分组，否则 -not -path 优先级错）
        cmd = ['find', str(self.source), '-type', 'f', '(',
               '-iname', '*.flac', '-o',
               '-iname', '*.ape', '-o',
               '-iname', '*.wav', '-o',
               '-iname', '*.mp3', '-o',
               '-iname', '*.m4a', '-o',
               '-iname', '*.aac', '-o',
               '-iname', '*.ogg', '-o',
               '-iname', '*.opus', '-o',
               '-iname', '*.wma', '-o',
               '-iname', '*.aiff', '-o',
               '-iname', '*.aif',
               ')']
        for skip in ['_低音质备份', 'attachments', '.opencode', '.git']:
            cmd.extend(['-not', '-path', f'*/{skip}/*'])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return [l for l in result.stdout.split('\n') if l.strip()]

    def scan_lyrics(self):
        """用 find 快速扫描歌词"""
        import subprocess
        cmd = ['find', str(self.source), '-type', 'f',
               '-iname', '\\*.lrc', '-o', '-iname', '\\*.txt']
        for skip in ['_低音质备份', 'attachments', '.opencode', '.git']:
            cmd.extend(['-not', '-path', f'*/{skip}/*'])
        # 上面 -o 优先级有问题，重新写
        cmd = ['find', str(self.source), '-type', 'f',
               '(', '-iname', '*.lrc', '-o', '-iname', '*.txt', ')']
        for skip in ['_低音质备份', 'attachments', '.opencode', '.git']:
            cmd.extend(['-not', '-path', f'*/{skip}/*'])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return [l for l in result.stdout.split('\n') if l.strip()]

    def build_target_path(self, first_artist, title, ext):
        """
        生成目标路径：
        target / 首字母 / 歌手 / "歌手 - 歌曲.ext"
        若歌手为空 → target / 其他 / "歌曲.ext"
        """
        ext = ext.lower()
        # 【bug 修复】任何含 NUL 的输入都强制当空处理
        def _strip_nul(s):
            if not s:
                return s
            return s.replace('\x00', '').strip() if isinstance(s, str) else s
        first_artist = _strip_nul(first_artist)
        title = _strip_nul(title)

        if not first_artist or not first_artist.strip():
            # 没有歌手信息 → 其他 / 歌曲名.ext
            safe_title = sanitize_filename(title or '未知歌曲')
            return self.target / '其他' / f"{safe_title}{ext}"

        first_clean = sanitize_filename(first_artist)
        letter = get_first_letter(first_artist)
        letter_dir = letter if letter else '其他'
        safe_title = sanitize_filename(title or '未知歌曲')
        if not first_clean or not safe_title:
            return self.target / letter_dir / '_invalid_'

        # 文件名："歌手 - 歌曲.ext"
        fname = f"{first_clean} - {safe_title}{ext}"
        return self.target / letter_dir / first_clean / fname

    def process_music(self, files):
        for i, src in enumerate(files, 1):
            if i % 500 == 0:
                print(f"  [{i}/{len(files)}] 进度 {i*100//len(files)}%")
            try:
                self._process_one_music(src)
            except Exception as e:
                self.stats['errors'] += 1
                self.report.append({
                    '类型': '音乐', '原路径': src, '目标路径': '',
                    '歌手': '', '歌曲': '', '状态': f'错误: {e}',
                    '音质': '', '大小KB': file_size_kb(src)
                })

    def _process_one_music(self, src):
        ext = Path(src).suffix.lower()
        # 【bug 修复】如果源文件不存在（可能是脚本异常后被移动走了），
        # 直接跳过，不抛错也不计入错误
        if not os.path.exists(src):
            return
        full_artist, first_artist, title, source_kind = extract_artist_title(src)
        if not title:
            title = Path(src).stem

        target_path = self.build_target_path(first_artist, title, ext)
        rank = get_quality_rank(src)

        # 去重：同 (字母, 歌手, 歌曲) 路径已存在
        # 注意：target_path 已含扩展名；同歌手同歌不同格式会落到不同文件名
        key = (str(target_path.parent), target_path.stem)
        if key in self.target_index:
            existing_path, existing_rank, existing_size = self.target_index[key]
            if rank > existing_rank or (rank == existing_rank and file_size_kb(src) > existing_size):
                # 新的更好 → 旧的去备份
                self._backup_existing(existing_path, src, target_path, full_artist, first_artist, title, rank, ext)
                return
            else:
                # 现有的更好 → 新的去备份
                self._move_to_backup(src, ext, first_artist, title, rank, full_artist, reason='被现有高音质取代')
                return

        # 没冲突：执行移动/重命名
        # 【bug 修复】存 target_path（移动后磁盘上的路径），而不是 src
        # 因为 src 移动后文件就不存在了，下次拿来当 existing_path 会报错
        self.target_index[key] = (target_path, rank, file_size_kb(src))
        if self.dry_run:
            self.report.append({
                '类型': '音乐', '原路径': src, '目标路径': str(target_path),
                '歌手': full_artist, '第一歌手': first_artist,
                '歌曲': title, '状态': '干跑-待移动', '音质': rank, '大小KB': file_size_kb(src),
                '来源': source_kind
            })
        else:
            self._safe_move(src, target_path)
            self.report.append({
                '类型': '音乐', '原路径': src, '目标路径': str(target_path),
                '歌手': full_artist, '第一歌手': first_artist,
                '歌曲': title, '状态': '已移动', '音质': rank, '大小KB': file_size_kb(src),
                '来源': source_kind
            })
            self.stats['moved'] += 1

    def _backup_existing(self, existing_path, new_src, target_path, full_artist, first_artist, title, rank, ext):
        """新文件更好：旧的移到备份，新的放目标"""
        if self.dry_run:
            self.report.append({
                '类型': '音乐', '原路径': existing_path, '目标路径': str(self._backup_path_for(existing_path)),
                '歌手': full_artist, '第一歌手': first_artist,
                '歌曲': title, '状态': '干跑-被高音质取代-待备份', '音质': rank, '大小KB': file_size_kb(existing_path)
            })
            self.report.append({
                '类型': '音乐', '原路径': new_src, '目标路径': str(target_path),
                '歌手': full_artist, '第一歌手': first_artist,
                '歌曲': title, '状态': '干跑-高音质-待移动', '音质': rank, '大小KB': file_size_kb(new_src)
            })
        else:
            # 旧的去备份
            bp = self._backup_path_for(existing_path)
            self._safe_move(existing_path, bp)
            self.operations.append(('backup', str(existing_path), str(bp)))
            self.stats['backed_up'] += 1
            # 新的去目标
            self._safe_move(new_src, target_path)
            self.operations.append(('move', str(new_src), str(target_path)))
            self.stats['moved'] += 1
            self.report.append({
                '类型': '音乐', '原路径': new_src, '目标路径': str(target_path),
                '歌手': full_artist, '第一歌手': first_artist,
                '歌曲': title, '状态': '已替换（高音质胜出）', '音质': rank, '大小KB': file_size_kb(new_src)
            })
        # 更新索引
        self.target_index[(str(target_path.parent), target_path.stem)] = (target_path, rank, file_size_kb(new_src))

    def _move_to_backup(self, src, ext, first_artist, title, rank, full_artist, reason=''):
        bp = self._backup_path_for(src)
        if self.dry_run:
            self.report.append({
                '类型': '音乐', '原路径': src, '目标路径': str(bp),
                '歌手': full_artist, '第一歌手': first_artist,
                '歌曲': title, '状态': f'干跑-待备份({reason})', '音质': rank, '大小KB': file_size_kb(src)
            })
        else:
            self._safe_move(src, bp)
            self.operations.append(('backup', str(src), str(bp)))
            self.stats['backed_up'] += 1

    def _backup_path_for(self, original_target_path):
        """生成低音质备份的路径，保留原文件名结构以防追溯"""
        # _低音质备份/原相对路径(去根)
        try:
            rel = Path(original_target_path).relative_to(self.target)
        except ValueError:
            rel = Path(original_target_path).name
        return self.backup_dir / rel

    def _safe_move(self, src, dst):
        """安全移动：自动创建目录、避免覆盖"""
        dst = Path(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        # 如果目标已存在（不应该发生，但保险），加后缀
        if dst.exists():
            stem, suffix = dst.stem, dst.suffix
            i = 1
            while True:
                cand = dst.parent / f"{stem}__dup{i}{suffix}"
                if not cand.exists():
                    dst = cand
                    break
                i += 1
        shutil.move(str(src), str(dst))

    def process_lyrics(self, files):
        # 构造目标歌词索引表：
        # key = 规范主文件名(去扩展) → 目标目录
        # 例: "周杰伦 - 晴天" → target/Z/周杰伦/
        # 例: "晴天" (无歌手) → target/其他/
        norm_index = {}  # 主文件名 → 目标目录
        for (parent_dir, stem), (path, rank, size) in self.target_index.items():
            norm_index.setdefault(stem, []).append(parent_dir)

        for src in files:
            try:
                self._process_one_lyric(src, norm_index)
            except Exception as e:
                self.stats['errors'] += 1
                self.report.append({
                    '类型': '歌词', '原路径': src, '目标路径': '',
                    '歌手': '', '歌曲': '', '状态': f'错误: {e}',
                    '音质': '', '大小KB': file_size_kb(src)
                })

    def _process_one_lyric(self, src, norm_index):
        ext = Path(src).suffix.lower()
        stem = Path(src).stem
        # 【修复】规范化歌词主名为标准格式：去编号、补空格
        stem_clean = sanitize_filename(stem)
        stem_normalized = re.sub(r'\s*-\s*', ' - ', stem_clean)
        stem_no_prefix = re.sub(r'^\d{2,5}-', '', stem_clean).strip()
        stem_no_prefix_norm = re.sub(r'\s*-\s*', ' - ', stem_no_prefix)
        # 同时规范化所有候选 stem
        def _normalize(s):
            if not s:
                return s
            s = re.sub(r'^\d{2,5}-', '', s).strip()
            s = re.sub(r'\s*-\s*', ' - ', s).strip()
            return s
        candidates = [_normalize(stem), _normalize(stem_clean)]

        # 1. 完全匹配（规范主名）
        target_dir = None
        match_key = None
        for candidate in candidates:
            if candidate and candidate in norm_index:
                target_dir = norm_index[candidate][0]
                match_key = candidate
                break
        # 2. 兜底：原 stem_no_prefix / stem_normalized
        if not target_dir:
            for candidate in [stem_clean, stem_normalized, stem_no_prefix, stem_no_prefix_norm]:
                if candidate and candidate in norm_index:
                    target_dir = norm_index[candidate][0]
                    match_key = candidate
                    break

        if not target_dir:
            # 2. 模糊匹配：尝试多种变换
            for norm_stem in norm_index:
                # 完全相同（清洗后空格差异）
                if stem_normalized == norm_stem:
                    target_dir = norm_index[norm_stem][0]
                    match_key = norm_stem
                    break
                # 歌词格式 "歌手-歌曲" 匹配规范 "歌手 - 歌曲"
                if ' - ' in norm_stem:
                    norm_title = norm_stem.split(' - ', 1)[1]
                    if stem_no_prefix == norm_title or stem_clean == norm_title:
                        target_dir = norm_index[norm_stem][0]
                        match_key = norm_stem
                        break
                # 歌词 "歌曲-歌手" 也能匹配（反转后比对）
                if ' - ' in norm_stem:
                    norm_artist = norm_stem.split(' - ', 1)[0]
                    norm_title = norm_stem.split(' - ', 1)[1]
                    if stem_no_prefix == f"{norm_artist}-{norm_title}" or \
                       stem_clean == f"{norm_artist}-{norm_title}" or \
                       stem_clean == f"{norm_title}-{norm_artist}":
                        target_dir = norm_index[norm_stem][0]
                        match_key = norm_stem
                        break

                # 【增强】歌词 "歌手-歌名" 格式 + 父目录歌手旁证
                # 如 杨千嬅/0539-可惜我是水瓶座.lrc → 应匹配 杨千嬅/杨千嬅 - 可惜我是水瓶座.wav
                if target_dir is None and target_dir is not False:
                    parent_singer = os.path.basename(os.path.dirname(src))
                    parent_singer_lower = parent_singer.lower()
                    if ' - ' not in stem and '-' in stem and parent_singer_lower:
                        # 拆分 "歌手-歌名" 或 "编号-歌名"
                        parts = stem.split('-', 1)
                        cand_singer = parts[0].strip().lower()
                        cand_title = parts[1].strip()
                        # 父目录歌手与歌词前缀歌手一致
                        if cand_singer == parent_singer_lower:
                            if ' - ' in norm_stem:
                                ns_singer = norm_stem.split(' - ', 1)[0].strip().lower()
                                ns_title = norm_stem.split(' - ', 1)[1].strip()
                                if ns_singer == cand_singer and (cand_title == ns_title or cand_title in ns_title):
                                    target_dir = norm_index[norm_stem][0]
                                    match_key = norm_stem
                                    break

        if target_dir:
            # 找到匹配 → 移动到目标目录
            target_path = Path(target_dir) / f"{stem_clean}{ext}"
            # 避免覆盖已有歌词：加 .lrc1 后缀
            i = 0
            final_target = target_path
            while final_target.exists():
                i += 1
                final_target = Path(target_dir) / f"{stem_clean}__{i}{ext}"

            if self.dry_run:
                self.report.append({
                    '类型': '歌词', '原路径': src, '目标路径': str(final_target),
                    '歌手': '', '歌曲': stem_clean, '状态': '干跑-待匹配',
                    '音质': '', '大小KB': file_size_kb(src)
                })
            else:
                self._safe_move(src, final_target)
                self.operations.append(('move_lyric', str(src), str(final_target)))
                self.stats['lyrics_matched'] += 1
                self.report.append({
                    '类型': '歌词', '原路径': src, '目标路径': str(final_target),
                    '歌手': '', '歌曲': stem_clean, '状态': '已匹配移动',
                    '音质': '', '大小KB': file_size_kb(src)
                })
        else:
            # 没匹配 → 单独保留（按规范"不作处理"）
            if not self.dry_run:
                self.stats['lyrics_kept'] += 1
            self.report.append({
                '类型': '歌词', '原路径': src, '目标路径': '(保留原位)',
                '歌手': '', '歌曲': stem_clean, '状态': '无匹配-保留原位',
                '音质': '', '大小KB': file_size_kb(src)
            })

    def write_reports(self):
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 报告 CSV —— 统一写到 source 父目录，不污染目标目录
        prefix = '整理报告_dryrun_' if self.dry_run else '整理报告_'
        self.report_path = self.source.parent / f'{prefix}{ts}.csv'

        self.report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.report_path, 'w', newline='', encoding='utf-8-sig') as fp:
            w = csv.DictWriter(fp, fieldnames=['类型', '原路径', '目标路径', '歌手', '第一歌手',
                                               '歌曲', '状态', '音质', '大小KB', '来源'])
            w.writeheader()
            w.writerows(self.report)

        # 操作日志
        self.log_path = self.report_path.parent / f'operations_{ts}.log'
        with open(self.log_path, 'w', encoding='utf-8') as fp:
            fp.write(f"# 整理操作日志 - {datetime.now()}\n")
            fp.write(f"# 模式: {'干跑' if self.dry_run else '执行'}\n")
            fp.write(f"# 源: {self.source}\n")
            fp.write(f"# 目标: {self.target}\n")
            for op in self.operations:
                fp.write(f"{op[0]}\t{op[1]}\t{op[2]}\n")


# ============== 入口 ==============

def main():
    parser = argparse.ArgumentParser(description='音乐库整理脚本')
    parser.add_argument('--source', default=SOURCE_DIR, help='源目录')
    parser.add_argument('--target', default=TARGET_DIR, help='目标目录')
    parser.add_argument('--apply', action='store_true', help='真正执行（默认干跑）')
    parser.add_argument('--limit', type=int, default=0, help='限制处理文件数（调试用）')
    parser.add_argument('--no-tag', action='store_true', help='跳过 ID3 标签读取，只解析文件名（快10x）')
    args = parser.parse_args()

    dry = not args.apply
    if args.no_tag:
        global _global_no_tag
        _global_no_tag = True
    org = MusicOrganizer(args.source, args.target, dry_run=dry, no_tag=args.no_tag)
    org.run()


if __name__ == '__main__':
    main()
