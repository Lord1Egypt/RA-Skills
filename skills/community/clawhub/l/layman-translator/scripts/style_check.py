#!/usr/bin/env python3
# 文风扫描：按「可疑表达清单」扫一篇稿子，报命中位置与条数，不下合格判定。
# 它只读取文件、不修改任何东西；是 `scripts/fact_anchor_check.py` 之外的第二个独立复核接口。
#
# 清单对应 `references/毛病词典.md` 21 条里「可机器扫描」的部分，另附一条自指 AI 标志。
# 语义/结构类症状无法正则化——辩证收束、成对清单、孤儿句、未解释术语、拟人化、
# 伪精确数字、分点过密、小标题过密、铺垫比喻成段——由第三道通读时按毛病词典人工查。
# 判据只有一条：删掉它这段话有没有少东西，没少就删。命中是信号，不是违规。
#
# 用法（Windows / WSL / Ubuntu / macOS 通用，工作区根目录执行）：
#   python <skill_dir>/scripts/style_check.py "gongzuoliu/试跑/<日期_样本名>/02_二创稿.md"

import re
import sys
from pathlib import Path

RULES = [
    ('破折号', r'——'),
    ('对比结构 不是X而是Y', r'不是[^。\r\n]{0,12}而是'),
    ('空排名 最值钱/最要紧', r'最[值要紧关键重核本质]'),
    ('强化词 真正/恰恰/才是', r'真正|恰恰|才是|无非'),
    ('模板化收束', r'综上所述|总而言之|总的来说|综上|不难发现|值得一提|归根结底'),
    ('空洞祈使', r'一定要|务必|让我们|从今天起|行动起来'),
    ('自指 AI', r'作为一个\s*AI|作为语言模型|作为一个大模型'),
    ('绝对化 唯一/众所周知', r'唯一|众所周知|毋庸置疑|毫无疑问|无与伦比|不言而喻'),
    ('凭空时间锚', r'随着[^。\r\n]{0,16}(?:到来|的出现|的发展)|在这个[^。\r\n]{0,8}时代'),
    ('无出处权威断言', r'研究表明|业内公认|专家建议|业内人士|有数据显示'),
    ('脑内坐标', r'这一层|上一层|上面那|如上所述|见上文|往前翻'),
    ('跨章回指', r'前面讲过|前面提到|下一章|后面会讲|见第[一二三四五六七八九十百\d]+章'),
    ('名词化堆叠与空泛词', r'赋能|抓手|闭环|生态|维度|颗粒度|实现了[^。\r\n]{0,8}提升'),
]
RULES = [(name, re.compile(pat)) for name, pat in RULES]


def paint(s, code):
    return '\033[{}m{}\033[0m'.format(code, s) if sys.stdout.isatty() else s


def main():
    if len(sys.argv) != 2:
        print('Usage: python style_check.py <target.md>', file=sys.stderr)
        return 2
    target = sys.argv[1]
    with open(target, encoding='utf-8', newline='') as f:
        text = f.read()

    chars = len(text)
    lines = text.split('\n')

    print()
    print(paint('文风扫描：{}（{} 字，{} 行）'.format(target, chars, len(lines)), 36))
    print(paint('命中是信号，不是违规。只在它「只给排名、不给信息」时才改。', 90))
    print()

    total = 0
    for name, regex in RULES:
        hits = len(regex.findall(text))
        total += hits
        density = ''
        if name == '破折号' and chars > 0:
            density = '（每 500 字 {:.2f} 处）'.format(hits / chars * 500)
        print('{:<22} {} 处 {}'.format(name, hits, density))
        if hits > 0:
            shown = 0
            for i, line in enumerate(lines):
                if regex.search(line):
                    if shown >= 8:
                        print(paint('    ……（其余略）', 33))
                        break
                    snippet = line.strip()
                    if len(snippet) > 64:
                        snippet = snippet[:64] + '…'
                    print(paint('    第 {} 行  {}'.format(i + 1, snippet), 33))
                    shown += 1

    print()
    print('合计命中 {} 处'.format(total))
    print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
