#!/usr/bin/env python3
"""Extract TM Ethernet Slave communication content"""
import fitz

pdf_path = r'D:\思锐工作目录\TM机器人\Omron TM Ethernet SlaveͨѶ����.pdf'
try:
    doc = fitz.open(pdf_path)
    print(f'Total pages: {len(doc)}')
    
    output = []
    for i in range(len(doc)):
        text = doc[i].get_text()
        if len(text.strip()) > 200:
            output.append(f'\n=== Page {i+1} ===')
            output.append(text[:4000])
    
    with open(r'C:\Users\JMO\.openclaw\workspace\skills\tm-robot\docs\ethernet_slave_content.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f'Extracted {len(output)//2} pages')
except Exception as e:
    print(f'Error: {e}')
