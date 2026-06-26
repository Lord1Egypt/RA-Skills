#!/usr/bin/env python3
"""基于结巴分词的中文人名提取辅助工具"""

import re
import os
import sys

def extract_names(text, top_n=100):
    """提取文本中的中国人名（简单基于姓氏词典）"""
    # 常见姓氏（百家姓前100）
    surnames = r'[赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄穆萧尹姚邵堪汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯咎管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左右崔吉钮龚程嵇邢滑裴陆荣翁荀羊于惠甄曲面加羊舌微巢关蒯相查后荆红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子车颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷利段干百里东郭南门呼延归海羊舌微生岳帅缑亢况后有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟]'

    # 简单的人名匹配（姓氏+1-2个汉字）
    pattern = re.compile(rf'{surnames}[\u4e00-\u9fff]{1,3}')
    names = pattern.findall(text)

    # 去重并统计频率
    name_freq = {}
    for name in names:
        name_freq[name] = name_freq.get(name, 0) + 1

    sorted_names = sorted(name_freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_names[:top_n]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python character_extract.py <novel.txt> [top_n]")
        sys.exit(1)

    file_path = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    names = extract_names(text, top_n)
    print(f"共提取到 {len(names)} 个人名：")
    for name, freq in names:
        print(f"  {name}: {freq}次")
