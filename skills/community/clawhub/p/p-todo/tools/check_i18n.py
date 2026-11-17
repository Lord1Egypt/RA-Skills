# -*- coding: utf-8 -*-
"""
i18n 文件校验工具：检查 9 个语言文件 key 是否齐全、格式符是否一致。

用法：
    python -X utf8 tools/check_i18n.py
退出码 0 = 全部通过；1 = 有问题（并列出详情）
"""
import io
import os
import re
import sys

BASE = os.path.join(os.path.dirname(__file__), '..', 'src', 'main', 'resources', 'i18n')
LANGS = ['zh', 'zh_tw', 'en', 'ja', 'ko', 'fr', 'de', 'es', 'pt']


def load(path):
    d = {}
    with io.open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            d[k.strip()] = v
    return d


def main():
    files = {}
    for lang in LANGS:
        p = os.path.join(BASE, 'texts_%s.properties' % lang)
        if not os.path.exists(p):
            print('[缺失文件] %s' % p)
            return 1
        files[lang] = load(p)

    base = set(files['zh'])
    ok = True

    for lang in LANGS[1:]:
        s = set(files[lang])
        missing = base - s
        extra = s - base
        empty = [k for k, v in files[lang].items() if not v.strip()]
        if missing:
            ok = False
            print('[%s 缺失 %d 个 key]' % (lang, len(missing)))
            for k in sorted(missing):
                print('   - %s' % k)
        if extra:
            print('[%s 多余 %d 个 key（zh 没有，可删可留）]' % (lang, len(extra)))
            for k in sorted(extra):
                print('   - %s' % k)
        if empty:
            ok = False
            print('[%s 空值 key]' % lang)
            for k in empty:
                print('   - %s' % k)

    # 格式符一致性
    for k in base:
        zh_fmt = sorted(re.findall(r'%(?:[0-9]*\$)?[ds]', files['zh'][k]))
        for lang in LANGS[1:]:
            if k not in files[lang]:
                continue
            other_fmt = sorted(re.findall(r'%(?:[0-9]*\$)?[ds]', files[lang][k]))
            if zh_fmt != other_fmt:
                ok = False
                print('[%s 格式符不一致] key=%s zh=%s %s=%s' % (
                    lang, k, zh_fmt, lang, other_fmt))

    if ok:
        print('ALL OK：9 个语言文件 key 齐全、格式符一致（zh 共 %d 个 key）' % len(base))
        return 0
    print('存在上述问题，请修复。')
    return 1


if __name__ == '__main__':
    sys.exit(main())
