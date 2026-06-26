#!/usr/bin/env python3
"""Chinese to Pinyin Converter"""
import sys
import json

# Pinyin database (simplified - common characters)
PINYIN_MAP = {
    '的': 'de', '一': 'yī', '是': 'shì', '了': 'le', '在': 'zài', '不': 'bù', '有': 'yǒu',
    '人': 'rén', '这': 'zhè', '中': 'zhōng', '大': 'dà', '为': 'wéi', '上': 'shàng', '个': 'gè',
    '国': 'guó', '我': 'wǒ', '以': 'yǐ', '要': 'yào', '他': 'tā', '时': 'shí', '来': 'lái',
    '用': 'yòng', '们': 'men', '生': 'shēng', '到': 'dào', '作': 'zuò', '地': 'dì', '于': 'yú',
    '出': 'chū', '就': 'jiù', '分': 'fēn', '对': 'duì', '成': 'chéng', '会': 'huì', '可': 'kě',
    '主': 'zhǔ', '发': 'fā', '年': 'nián', '动': 'dòng', '同': 'tóng', '工': 'gōng', '也': 'yě',
    '能': 'néng', '下': 'xià', '过': 'guò', '子': 'zǐ', '说': 'shuō', '产': 'chǎn', '种': 'zhǒng',
    '面': 'miàn', '而': 'ér', '方': 'fāng', '后': 'hòu', '多': 'duō', '定': 'dìng', '行': 'xíng',
    '学': 'xué', '所': 'suǒ', '民': 'mín', '得': 'dé', '经': 'jīng', '十': 'shí', '三': 'sān',
    '之': 'zhī', '进': 'jìn', '着': 'zhe', '等': 'děng', '部': 'bù', '度': 'dù', '家': 'jiā',
    '里': 'lǐ', '新': 'xīn', '力': 'lì', '请': 'qǐng', '联': 'lián', '合': 'hé', '机': 'jī',
    '无': 'wú', '心': 'xīn', '量': 'liàng', '多': 'duō', '么': 'me', '事': 'shì', '知': 'zhī',
    '间': 'jiān', '去': 'qù', '什': 'shén', '么': 'me', '还': 'hái', '天': 'tiān', '日': 'rì',
    '本': 'běn', '月': 'yuè', '年': 'nián', '好': 'hǎo', '小': 'xiǎo', '伙': 'huǒ', '伴': 'bàn',
    '你': 'nǐ', '好': 'hǎo', '世': 'shì', '界': 'jiè', '北': 'běi', '京': 'jīng', '上': 'shàng',
    '海': 'hǎi', '深': 'shēn', '圳': 'zhèn', '广': 'guǎng', '州': 'zhōu', '杭': 'háng', '州': 'zhōu',
    '成': 'chéng', '都': 'dōu', '重': 'chóng', '庆': 'qìng', '天': 'tiān', '津': 'jīn', '南': 'nán',
    '京': 'jīng', '西': 'xī', '安': 'ān', '武': 'wǔ', '汉': 'hàn', '长': 'cháng', '沙': 'shā',
    '郑': 'zhèng', '州': 'zhōu', '沈': 'shěn', '阳': 'yáng', '哈': 'hā', '尔': 'ěr', '滨': 'bīn',
}

TONE_MAP = {
    'a': 'ā á ǎ à', 'e': 'ē é ě è', 'i': 'ī í ǐ ì', 'o': 'ō ó ǒ ò', 'u': 'ū ú ǔ ù',
    'v': 'ǖ ǘ ǚ ǜ', 'ü': 'ǖ ǘ ǚ ǜ'
}

def strip_tones(py):
    for k, v in TONE_MAP.items():
        tones = v.split()
        for t in tones[1:]:
            py = py.replace(t, k)
    return py

def convert(text, no_tone=False, initial_only=False):
    """Convert Chinese text to pinyin"""
    result = []
    
    for char in text:
        if char in PINYIN_MAP:
            py = PINYIN_MAP[char]
            if no_tone:
                py = strip_tones(py)
            if initial_only:
                py = py[0].upper() if py else ''
            result.append(py)
        elif char.isascii() and not char.isspace():
            result.append(char)
        elif char in ',.?!，。？！、；;：:':
            result.append(char)
        # skip whitespace
    
    return ' '.join(result)

def main():
    args = sys.argv[1:]
    no_tone = '--no-tone' in args
    initial = '--initial' in args
    text = ' '.join([a for a in args if not a.startswith('--')])
    
    if not text:
        print(json.dumps({
            "usage": "python3 pinyin.py <中文文本> [--no-tone] [--initial]",
            "examples": [
                "python3 pinyin.py 你好世界",
                "python3 pinyin.py 你好世界 --no-tone",
                "python3 pinyin.py 北京上海 --initial"
            ]
        }, ensure_ascii=False, indent=2))
        return
    
    result = convert(text, no_tone=no_tone, initial_only=initial)
    mode = "首字母" if initial else ("无声音调" if no_tone else "标准拼音")
    print(json.dumps({"input": text, "pinyin": result, "mode": mode}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
