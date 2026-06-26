#!/usr/bin/env python3
"""
Guitar Chord Identifier - 和弦工具
- 正向查询：和弦名 -> 音 + 和弦图
- 反向查询：几个音 -> 和弦名
"""

import re
import subprocess

# 音名到半音数的映射
NOTE_TO_SEMITONE = {
    'C': 0, 'C#': 1, 'DB': 1, 'D': 2, 'D#': 3, 'EB': 3,
    'E': 4, 'F': 5, 'F#': 6, 'GB': 6, 'G': 7, 'G#': 8,
    'AB': 8, 'A': 9, 'A#': 10, 'BB': 10, 'B': 11
}

SEMITONE_TO_NOTE = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
    6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
}

# 常见和弦的音程（相对于根音）
CHORD_INTERVALS = {
    # 三和弦
    'major': [0, 4, 7],           # 大三
    'minor': [0, 3, 7],           # 小三
    'diminished': [0, 3, 6],      # 减三
    'augmented': [0, 4, 8],       # 增三
    'sus2': [0, 2, 7],            # 挂二
    'sus4': [0, 5, 7],           # 挂四
    
    # 七和弦
    'maj7': [0, 4, 7, 11],        # 大七
    '7': [0, 4, 7, 10],          # 属七
    'm7': [0, 3, 7, 10],         # 小七
    'm7b5': [0, 3, 6, 10],       # 半减七
    'dim7': [0, 3, 6, 9],        # 减七
    'aug7': [0, 4, 8, 10],       # 增七
    'maj7#5': [0, 4, 8, 11],     # 大七升五
    '7#5': [0, 4, 8, 10],        # 属七升五
    '7b5': [0, 4, 6, 10],         # 属七降五
    'mMaj7': [0, 3, 7, 11],      # 小大七
    
    # 九和弦
    'maj9': [0, 4, 7, 11, 14],   # 大九
    '9': [0, 4, 7, 10, 14],      # 属九
    'm9': [0, 3, 7, 10, 14],     # 小九
}

# 中文名称映射
CHORD_NAMES_CN = {
    'major': ' major',
    'minor': 'm 小',
    'diminished': 'dim 减',
    'augmented': 'aug 增',
    'sus2': 'sus2 挂二',
    'sus4': 'sus4 挂四',
    'maj7': 'maj7 大七',
    '7': '7 属七',
    'm7': 'm7 小七',
    'm7b5': 'm7b5 半减七',
    'dim7': 'dim7 减七',
    'aug7': 'aug7 增七',
    'maj7#5': 'maj7#5 大七升五',
    '7#5': '7#5 属七升五',
    '7b5': '7b5 属七降五',
    'mMaj7': 'mMaj7 小大七',
    'maj9': 'maj9 大九',
    '9': '9 属九',
    'm9': 'm9 小九',
}


def normalize_note(note):
    """标准化音名"""
    note = note.strip()
    # 处理重音符号
    note = note.replace('♯', '#').replace('♭', 'b').replace('♮', '')
    
    # 第一步：处理降号（在转大写之前！）
    replacements_flat = {
        'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#',
        'db': 'C#', 'eb': 'D#', 'gb': 'F#', 'ab': 'G#', 'bb': 'A#',
    }
    for old, new in replacements_flat.items():
        note = note.replace(old, new)
    
    # 转大写
    note = note.upper()
    
    # 第二步：处理重降 (bb) -> 升一个半音 (比如 bb = A#)
    note = note.replace('BB', 'A#')
    
    return note
    """将音名列表转换为半音数列表"""
    semitones = []
    for note in notes:
        normalized = normalize_note(note)
        if normalized in NOTE_TO_SEMITONE:
            semitones.append(NOTE_TO_SEMITONE[normalized])
        else:
            print(f"警告：无法识别音名 '{note}'")
            return None
    return list(set(semitones))  # 去重但保持原始顺序


def find_root(semitones):
    """找到可能的根音"""
    # 尝试以每个音为根音
    roots = []
    for i in range(12):
        shifted = [(s - i) % 12 for s in semitones]
        roots.append(shifted)
    return roots


def identify_chord(semitones):
    """识别和弦"""
    if not semitones or len(semitones) < 2:
        return None
    
    results = []
    
    # 尝试以每个音为根音
    for root_idx in range(12):
        # 计算相对于根音的音程（不排序，保留相对关系）
        shifted = [(s - root_idx) % 12 for s in semitones]
        # 排序用于匹配
        shifted_sorted = sorted(set(shifted))
        
        # 尝试匹配每种和弦类型（精确匹配）
        for chord_type, intervals in CHORD_INTERVALS.items():
            if shifted_sorted == intervals:
                root_note = SEMITONE_TO_NOTE[root_idx]
                results.append({
                    'root': root_note,
                    'type': chord_type,
                    'name': root_note + chord_type.replace('maj7', 'maj7').replace('m7', 'm7').replace('7', '7')
                })
    
    # 去重并返回
    unique_results = []
    seen = set()
    for r in results:
        key = (r['root'], r['type'])
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    return unique_results


def format_result(results):
    """格式化结果输出"""
    if not results:
        return "无法识别这个和弦，可能是非常见和弦或输入有误"
    
    output = []
    for r in results[:5]:  # 最多显示5个
        cn_name = CHORD_NAMES_CN.get(r['type'], r['type'])
        output.append(f"  • {r['root']}{cn_name}")
    
    return '\n'.join(output)


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python chord_identifier.py <音1> [音2] [音3] ...")
        print("例如: python chord_identifier.py C E G")
        print("      python chord_identifier.py C E G B")
        sys.exit(1)
    
    notes = sys.argv[1:]
    print(f"输入音: {', '.join(notes)}")
    
    semitones = notes_to_semitones(notes)
    if semitones is None:
        sys.exit(1)
    
    print(f"半音数: {semitones}")
    
    results = identify_chord(semitones)
    print(f"\n识别结果:\n{format_result(results)}")


def identify_and_print(notes):
    """反向查询并打印结果"""
    print(f"输入音: {', '.join(notes)}")
    
    semitones = notes_to_semitones(notes)
    if semitones is None:
        sys.exit(1)
    
    print(f"半音数: {semitones}")
    
    results = identify_chord(semitones)
    print(f"\n识别结果:\n{format_result(results)}")


def parse_chord_name(chord_name):
    """解析和弦名，返回 (根音, 类型)"""
    # 匹配根音 + 和弦类型
    # 例如: Cmaj7 -> (C, maj7), Am -> (A, minor), G7 -> (G, 7)
    chord_name = chord_name.strip()
    
    # 根音
    root_match = re.match(r'^([A-Ga-g][#b]?)(.*)$', chord_name)
    if not root_match:
        return None, None
    
    root = normalize_note(root_match.group(1))
    chord_type = root_match.group(2).strip() if root_match.group(2) else 'major'
    
    # 标准化和弦类型
    type_mapping = {
        '': 'major',
        'm': 'minor',
        'min': 'minor',
        'minor': 'minor',
        'dim': 'diminished',
        'dim7': 'dim7',
        'aug': 'augmented',
        '+': 'augmented',
        'sus': 'sus4',
        'sus2': 'sus2',
        'sus4': 'sus4',
        '7': '7',
        'maj7': 'maj7',
        'maj9': 'maj9',
        '9': '9',
        'm7': 'm7',
        'm9': 'm9',
        'm7b5': 'm7b5',
        'mMaj7': 'mMaj7',
        'aug7': 'aug7',
        '7#5': '7#5',
        '7b5': '7b5',
        'maj7#5': 'maj7#5',
    }
    
    chord_type = type_mapping.get(chord_type, chord_type)
    
    return root, chord_type


def get_chord_notes(root, chord_type):
    """获取和弦的所有音"""
    if root not in NOTE_TO_SEMITONE:
        return None
    
    root_semitone = NOTE_TO_SEMITONE[root]
    
    if chord_type not in CHORD_INTERVALS:
        return None
    
    intervals = CHORD_INTERVALS[chord_type]
    notes = [(root_semitone + i) % 12 for i in intervals]
    
    # 转换为音名
    note_names = [SEMITONE_TO_NOTE[n] for n in notes]
    return note_names


def get_ascii_chord(chord_name):
    """调用 ascii_chord 获取和弦图"""
    import os
    # 转换和弦名格式
    chord_name = chord_name.replace('bb', '#')
    
    try:
        home = os.path.expanduser('~')
        cwd = os.path.join(home, 'workspace', 'ascii_chord')
        result = subprocess.run(
            ['cargo', 'run', '--', 'get', chord_name],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except Exception as e:
        return None


def chord_lookup(chord_name, show_diagram=False):
    """正向查询和弦"""
    root, chord_type = parse_chord_name(chord_name)
    
    if root is None:
        return f"无法解析和弦名: {chord_name}"
    
    # 获取音
    notes = get_chord_notes(root, chord_type)
    if notes is None:
        return f"不支持的和弦类型: {chord_type}"
    
    # 获取中文名称
    cn_name = CHORD_NAMES_CN.get(chord_type, chord_type)
    
    result = f"**{root}{cn_name}**\n"
    result += f"音: {', '.join(notes)}\n"
    
    # 获取和弦图
    if show_diagram:
        # 转换格式给 ascii_chord
        ascii_chord_name = root
        if chord_type != 'major':
            ascii_chord_name += chord_type.replace('major', '').replace('minor', 'm')
        
        # 尝试获取和弦图
        diagram = get_ascii_chord(ascii_chord_name)
        if diagram:
            result += f"\n```\n{diagram}\n```"
        else:
            result += f"\n(注: ascii_chord 不支持此和弦类型)"
    
    return result


# 音阶数据
SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],  # 自然小调
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'blues': [0, 3, 5, 6, 7, 10],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
}

SCALE_NAMES_CN = {
    'major': '大调音阶',
    'minor': '自然小调',
    'harmonic_minor': '和声小调',
    'melodic_minor': '旋律小调',
    'pentatonic_major': '大调五声音阶',
    'pentatonic_minor': '小调五声音阶',
    'blues': '蓝调音阶',
    'dorian': 'Dorian',
    'phrygian': 'Phrygian',
    'lydian': 'Lydian',
    'mixolydian': 'Mixolydian',
    'locrian': 'Locrian',
}


def get_chord_inversions(chord_name, show_diagram=False):
    """和弦转位"""
    root, chord_type = parse_chord_name(chord_name)
    
    if root is None:
        return f"无法解析和弦名: {chord_name}"
    
    notes = get_chord_notes(root, chord_type)
    if notes is None:
        return f"不支持的和弦类型: {chord_type}"
    
    cn_name = CHORD_NAMES_CN.get(chord_type, chord_type)
    
    result = f"**{root}{cn_name}** 转位:\n"
    
    # 原位
    result += f"\n原位: {', '.join(notes)}\n"
    if show_diagram:
        diagram = get_ascii_chord(root + chord_type.replace('major', '').replace('minor', 'm'))
        if diagram and 'Unknown chord' not in diagram:
            result += f"\n```\n{diagram}\n```"
        else:
            # 用我们自己的图
            diagram = get_chord_fretboard_diagram(notes)
            if diagram:
                result += f"\n(指板图)\n```\n{diagram}\n```"
    
    # 转位
    for i in range(1, len(notes)):
        inverted = notes[i:] + notes[:i]
        result += f"\n第{i}转位: {', '.join(inverted)}\n"
        
        if show_diagram:
            inv_root = inverted[0]
            inv_chord_name = inv_root + chord_type.replace('major', '').replace('minor', 'm')
            diagram = get_ascii_chord(inv_chord_name)
            if diagram and 'Unknown chord' not in diagram:
                result += f"```\n{diagram}\n```"
            else:
                # 用我们自己的图
                diagram = get_chord_fretboard_diagram(inverted)
                if diagram:
                    result += f"(指板图)\n```\n{diagram}\n```"
    
    return result


def get_drop2_voicings(chord_name):
    """计算 drop2 和弦 voicing
    
    Drop2: 把七和弦的第二高音(纯五度)降一个八度
    例如 Cmaj7 (C-E-G-B) → drop2 → C-G-B-E
    """
    root, chord_type = parse_chord_name(chord_name)
    
    if root is None:
        return f"无法解析和弦名: {chord_name}"
    
    # 获取和弦音
    notes = get_chord_notes(root, chord_type)
    if notes is None:
        return f"不支持的和弦类型: {chord_type}"
    
    # 只支持七和弦的 drop2
    if len(notes) != 4:
        return f"Drop2 只支持七和弦(4音)，当前和弦有 {len(notes)} 个音"
    
    cn_name = CHORD_NAMES_CN.get(chord_type, chord_type)
    result = f"**{root}{cn_name}** Drop2 Voicings:\n"
    
    # 七和弦音程: R, 3, 5, 7
    # Drop2: R, 5, 7, 3 (把五度音降八度)
    intervals = CHORD_INTERVALS.get(chord_type, [])
    if len(intervals) != 4:
        return f"无法计算 drop2: 缺少音程信息"
    
    root_semitone = NOTE_TO_SEMITONE[root]
    
    # 计算各个音的半音数
    # 原位: R, 3, 5, 7
    original = [(root_semitone + i) % 12 for i in intervals]
    
    # Drop2: R, 5, 7, 3
    # 即：根音不变，5度降八度，7度不变，3度不变
    drop2_voicing = [
        original[0],  # R (root)
        original[2],  # 5 (fifth) - dropped octave = now below 7
        original[3],  # 7 (seventh)
        original[1],  # 3 (third) - now the highest
    ]
    
    # 转成音符名
    drop2_notes = [SEMITONE_TO_NOTE[n] for n in drop2_voicing]
    
    result += f"\n原位: {', '.join(notes)}\n"
    result += f"Drop2: {', '.join(drop2_notes)}\n"
    
    # 标记各音程
    result += f"\n音程分析:\n"
    result += f"  低音(R): {drop2_notes[0]}\n"
    result += f"  纯五度(5): {drop2_notes[1]} (降八度)\n"
    result += f"  大七度(7): {drop2_notes[2]}\n"
    result += f"  大三度(3): {drop2_notes[3]} (最高音)\n"
    
    # 显示常见的 drop2 指型
    result += f"\n--- 常见 Guitar Voicings ---\n"
    
    # 常见 drop2 指型 (从低到高弦)
    # 这些是基于吉他指板的常见位置
    common_voicings = {
        'maj7': [
            {'name': 'Root pos.', 'frets': 'X-3-2-1-1-0', 'strings': 'C,G,B,E'},
            {'name': '1st inv.', 'frets': 'X-X-0-2-1-0', 'strings': 'E,C,G,B'},
            {'name': '2nd inv.', 'frets': 'X-0-0-0-1-0', 'strings': 'G,B,E,C'},
            {'name': '3rd inv.', 'frets': 'X-3-3-2-1-0', 'strings': 'B,E,G,C'},
        ],
        '7': [
            {'name': 'Root pos.', 'frets': 'X-3-2-1-1-0', 'strings': 'C,G,Bb,E'},
            {'name': '1st inv.', 'frets': 'X-X-0-2-1-3', 'strings': 'E,C,G,Bb'},
            {'name': '2nd inv.', 'frets': 'X-0-0-0-1-0', 'strings': 'G,Bb,E,C'},
            {'name': '3rd inv.', 'frets': 'X-3-3-2-1-3', 'strings': 'Bb,E,G,C'},
        ],
        'm7': [
            {'name': 'Root pos.', 'frets': 'X-3-5-3-4-3', 'strings': 'C,Gb,Bb,Eb'},
            {'name': '1st inv.', 'frets': 'X-X-0-3-1-3', 'strings': 'Eb,C,Gb,Bb'},
            {'name': '2nd inv.', 'frets': 'X-0-0-0-3-0', 'strings': 'Gb,Bb,Eb,C'},
            {'name': '3rd inv.', 'frets': 'X-3-3-1-1-3', 'strings': 'Bb,Eb,Gb,C'},
        ],
    }
    
    if chord_type in common_voicings:
        for v in common_voicings[chord_type]:
            result += f"\n**{v['name']}**: {v['frets']}\n"
            result += f"  音: {v['strings']}\n"
    
    return result


def drop2_lookup(chord_name):
    """Drop2 和弦查询"""
    return get_drop2_voicings(chord_name)


def get_scale_notes(root, scale_type):
    """获取音阶的所有音"""
    if root not in NOTE_TO_SEMITONE:
        return None
    
    root_semitone = NOTE_TO_SEMITONE[root]
    
    if scale_type not in SCALES:
        return None
    
    intervals = SCALES[scale_type]
    notes = [(root_semitone + i) % 12 for i in intervals]
    note_names = [SEMITONE_TO_NOTE[n] for n in notes]
    return note_names


def get_chord_fretboard_diagram(notes):
    """生成和弦指板图（自己画的，不依赖 ascii_chord）"""
    # 转换音符为半音数
    note_semitones = []
    for note in notes:
        if note in NOTE_TO_SEMITONE:
            note_semitones.append(NOTE_TO_SEMITONE[note])
    
    if not note_semitones:
        return None
    
    # 吉他标准调弦: E A D G B E
    open_strings = [4, 9, 2, 7, 11, 4]
    fret_range = 5
    
    lines = []
    
    # 品格标注行
    header = "  "
    for fret in range(fret_range + 1):
        header += str(fret) + " "
    lines.append(header.rstrip())
    
    # 每根弦一行
    string_names = ['E', 'A', 'D', 'G', 'B', 'E']
    
    for s in range(6):
        line = string_names[s] + " "
        
        for fret in range(fret_range + 1):
            note = (open_strings[s] + fret) % 12
            
            if note in note_semitones:
                if note == note_semitones[0]:  # 根音
                    line += "O "
                else:
                    line += "X "
            else:
                line += ". "
        
        lines.append(line.rstrip())
    
    return '\n'.join(lines)


def get_scale_diagram(root, scale_type):
    """生成 ASCII 音阶图"""
    if root not in NOTE_TO_SEMITONE:
        return None
    
    root_semitone = NOTE_TO_SEMITONE[root]
    
    if scale_type not in SCALES:
        return None
    
    intervals = SCALES[scale_type]
    
    # 吉他标准调弦: E A D G B E
    open_strings = [4, 9, 2, 7, 11, 4]
    
    # 品格 0-5
    fret_range = 5
    
    # 用简单字符避免宽度问题
    # X = 音阶音, O = 根音, . = 空位
    # 横向：品格0 → 品格5
    
    lines = []
    
    # 品格标注行
    header = "  "  # 2空格
    for fret in range(fret_range + 1):
        header += str(fret) + " "
    lines.append(header.rstrip())
    
    # 每根弦一行
    string_names = ['E', 'A', 'D', 'G', 'B', 'E']
    
    for s in range(6):
        line = string_names[s] + " "
        
        for fret in range(fret_range + 1):
            note = (open_strings[s] + fret) % 12
            
            if note in intervals:
                if note == root_semitone:
                    line += "O "
                else:
                    line += "X "
            else:
                line += ". "
        
        lines.append(line.rstrip())
    
    return '\n'.join(lines)


def scale_lookup(chord_name, show_diagram=False):
    """查询音阶"""
    chord_name = chord_name.strip()
    
    match = re.match(r'^([A-Ga-g][#b]?)\s+(.+)$', chord_name)
    if not match:
        root, chord_type = parse_chord_name(chord_name)
        if root is None:
            return f"无法解析: {chord_name}"
        
        if chord_type in ['major', 'm', 'minor', '']:
            scale_type = 'major' if chord_type in ['major', ''] else 'minor'
        else:
            scale_type = chord_type
    else:
        root = normalize_note(match.group(1))
        scale_type = match.group(2).strip().lower()
    
    scale_mapping = {
        'major': 'major',
        'minor': 'minor',
        'm': 'minor',
        'natural minor': 'minor',
        'harmonic minor': 'harmonic_minor',
        'melodic minor': 'melodic_minor',
        'pentatonic': 'pentatonic_major',
        'pentatonic major': 'pentatonic_major',
        'pentatonic minor': 'pentatonic_minor',
        'blues': 'blues',
        'dorian': 'dorian',
        'phrygian': 'phrygian',
        'lydian': 'lydian',
        'mixolydian': 'mixolydian',
        'locrian': 'locrian',
    }
    
    scale_type = scale_mapping.get(scale_type, scale_type)
    
    if scale_type not in SCALES:
        return f"不支持的音阶类型: {scale_type}\n支持的类型: {', '.join(SCALES.keys())}"
    
    notes = get_scale_notes(root, scale_type)
    if notes is None:
        return f"无法获取音阶: {root} {scale_type}"
    
    cn_name = SCALE_NAMES_CN.get(scale_type, scale_type)
    
    result = f"**{root} {cn_name}**\n"
    result += f"音阶: {', '.join(notes)}\n"
    
    if show_diagram:
        diagram = get_scale_diagram(root, scale_type)
        if diagram:
            result += f"\n```\n{diagram}\n```"
    
    return result


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  正向查询: python chord_identifier.py <和弦名>")
        print("           例如: python chord_identifier.py Cmaj7")
        print("  反向查询: python chord_identifier.py --identify <音1> [音2] ...")
        print("           例如: python chord_identifier.py --identify C E G")
        print("  带和弦图: python chord_identifier.py <和弦名> --diagram")
        print("  和弦转位: python chord_identifier.py --inversion <和弦名>")
        print("           例如: python chord_identifier.py --inversion C7")
        print("  Drop2和弦: python chord_identifier.py --drop2 <和弦名>")
        print("           例如: python chord_identifier.py --drop2 Cmaj7")
        print("  音阶查询: python chord_identifier.py --scale <调式>")
        print("           例如: python chord_identifier.py --scale 'C major'")
        print("           例如: python chord_identifier.py --scale 'A minor' --diagram")
        sys.exit(1)
    
    # 检查参数
    if sys.argv[1] == '--identify':
        # 反向查询
        notes = sys.argv[2:]
        identify_and_print(notes)
    elif sys.argv[1] == '--drop2':
        # Drop2 和弦查询
        chord_name = sys.argv[2]
        print(drop2_lookup(chord_name))
    elif sys.argv[1] == '--inversion':
        # 和弦转位
        chord_name = sys.argv[2]
        show_diagram = '--diagram' in sys.argv
        print(get_chord_inversions(chord_name, show_diagram=show_diagram))
    elif sys.argv[1] == '--scale':
        # 音阶查询
        chord_name = sys.argv[2]
        show_diagram = '--diagram' in sys.argv
        print(scale_lookup(chord_name, show_diagram=show_diagram))
    elif '--diagram' in sys.argv:
        # 带和弦图的正向查询
        chord_name = sys.argv[1]
        print(chord_lookup(chord_name, show_diagram=True))
    else:
        # 正向查询
        chord_name = sys.argv[1]
        print(chord_lookup(chord_name, show_diagram=False))


if __name__ == '__main__':
    main()
