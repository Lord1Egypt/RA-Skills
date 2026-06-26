#!/usr/bin/env python3
"""Extract SVR/Socket variable reading content from TM API manual"""
import fitz

doc = fitz.open(r'D:\思锐工作目录\TM机器人\Software_TM-Robot-Management-API-Manual_1.04_1.02_all-languages\TM Robot Management API User Manual v1.04 Rev1.02_EN.pdf')

output = []
for i in range(39, 60):
    text = doc[i].get_text()
    output.append(f'\n=== Page {i+1} ===')
    output.append(text[:4000])

with open(r'C:\Users\JMO\.openclaw\workspace\skills\tm-robot\docs\svr_socket_content.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('Done')
