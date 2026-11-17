# -*- coding: utf-8 -*-
import io, re, glob, os

os.chdir('src/main')

issues = []
for f in glob.glob('**/*.java', recursive=True) + glob.glob('**/*.fxml', recursive=True):
    lines = io.open(f, encoding='utf-8').read().splitlines()
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*') or stripped.startswith('#'):
            continue
        for m in re.finditer(r'"([^"]*)"', line):
            s = m.group(1)
            if re.search(r'[\u4e00-\u9fff]', s):
                before = line[:m.start()]
                # i18n 调用：t("key") / I18n.t("key") / 形如 xxx.yyy 的 key 参数
                is_key = bool(re.search(r'(t|text|textf)\(\s*$', before))
                is_key = is_key or bool(re.match(r'^[a-z][a-z0-9]*(\.[a-z0-9]+)+$', s))
                if not is_key:
                    issues.append((f, i, s[:70]))

print('=== 疑似未 i18n 的中文字符串字面量 ===')
for f, i, s in issues:
    print('%s:%d  %s' % (f, i, s))
print('total:', len(issues))
