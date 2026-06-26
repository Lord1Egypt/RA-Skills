#!/usr/bin/env python3
"""Extract SVR/Listen Node content from TMflow manual"""
import fitz

doc = fitz.open(r'D:\思锐工作目录\TM机器人\19888-400_RevP_Software Manual TMflow_SW1.88.pdf')

results = []
for i in range(len(doc)):
    text = doc[i].get_text()
    # Look for Listen Node related content
    if ('Listen' in text and len(text.strip()) > 150) or \
       ('SVR' in text and 'Server' in text) or \
       ('State Variable' in text and len(text.strip()) > 100):
        results.append((i+1, text))

print(f'Found {len(results)} relevant pages')
for pg, txt in results:
    print(f'\n=== Page {pg} ===')
    print(txt[:3000])
    print('---')
