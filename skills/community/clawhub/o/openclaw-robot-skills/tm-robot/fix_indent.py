import re

with open(r'C:/Users/JMO/.openclaw/workspace/skills/tm-robot/tm_robot.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed = []
for i, line in enumerate(lines):
    # Fix the broken except block - line after "except Exception as e:" should be indented
    if 'except Exception as e:' in line and i+1 < len(lines):
        next_line = lines[i+1]
        # Check if next line is not properly indented
        if next_line.startswith('            print') and not next_line.startswith('                '):
            fixed.append(line)
            fixed.append('                ' + next_line.lstrip())
            continue
    fixed.append(line)

with open(r'C:/Users/JMO/.openclaw/workspace/skills/tm-robot/tm_robot.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed)

print('Fixed!')
