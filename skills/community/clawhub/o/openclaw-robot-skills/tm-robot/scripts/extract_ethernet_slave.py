#!/usr/bin/env python3
"""Extract TM Ethernet Slave communication manual content"""
import fitz
import sys

doc = fitz.open(r'C:\Users\JMO\AppData\Local\Temp\ethernet_slave.pdf')

output = []
for i in range(len(doc)):
    text = doc[i].get_text()
    if len(text.strip()) > 100:
        output.append(f'\n=== Page {i+1} ===')
        output.append(text)

with open(r'C:\Users\JMO\.openclaw\workspace\skills\tm-robot\docs\ethernet_slave_content.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f'Extracted {len(doc)} pages')
