#!/usr/bin/env python3
"""Extract content around pages 145-155 from TMflow manual (Variable System)"""
import fitz

doc = fitz.open(r'D:\思锐工作目录\TM机器人\19888-400_RevP_Software Manual TMflow_SW1.88.pdf')

output = []
for i in range(143, 160):
    text = doc[i].get_text()
    output.append(f'\n=== Page {i+1} ===')
    output.append(text[:5000])

with open(r'C:\Users\JMO\.openclaw\workspace\skills\tm-robot\docs\variable_system_content.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f'Extracted pages 143-160')
