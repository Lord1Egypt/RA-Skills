import re
content = open(r'C:/Users/JMO/.openclaw/workspace/skills/tm-robot/docs/svr_socket_content.txt', encoding='utf-8').read()
# Find JSON-style key names
items = re.findall(r'"(\w+)":\s*[{\d["\[]', content)
unique = sorted(set(items))
for u in unique:
    print(u)
print('Total:', len(unique))
