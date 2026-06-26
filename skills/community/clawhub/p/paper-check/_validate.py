import ast, sys

scripts = ['check_format.py', 'fix_format.py', 'generate_report.py']
ok = 0
for s in scripts:
    try:
        with open(f'scripts/{s}', 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        print(f'  {s}: SYNTAX OK')
        ok += 1
    except SyntaxError as e:
        print(f'  {s}: SYNTAX ERROR - {e}')

print(f'\nResult: {ok}/{len(scripts)} passed')
if ok == len(scripts):
    print('All scripts validated successfully!')
