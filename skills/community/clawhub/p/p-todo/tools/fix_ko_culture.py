# -*- coding: utf-8 -*-
"""texts_ko.properties 调整为更偏向朝鲜（平壤）文化语用词（非完全转换）"""
import io

p = r'src/main/resources/i18n/texts_ko.properties'
txt = io.open(p, encoding='utf-8').read()

# 朝韩典型用词差异：韩国语 → 文化语（朝鲜）
repls = [
    ('멤버', '성원'),     # 成员
    ('익명', '무명'),     # 匿名
    ('미지정', '미배정'),  # 未分配
    ('알림', '통지'),     # 通知（含 알림음→통지음）
    ('업데이트', '갱신'),  # 更新
    ('댓글', '덧글'),     # 评论（韩国 댓글 / 朝鲜 덧글）
]
for old, new in repls:
    n = txt.count(old)
    if n:
        txt = txt.replace(old, new)
        print('%s -> %s  x%d' % (old, new, n))
    else:
        print('%s -> %s  x0' % (old, new))

io.open(p, 'w', encoding='utf-8', newline='\n').write(txt)
print('done')
