# -*- coding: utf-8 -*-
"""修复 persona JSON 中的标签变量名"""
import json
import os

PERSONA_DIR = os.path.join(os.path.expanduser("~"), ".qclaw", "personas")

form_labels = {1: '很随意', 2: '偏随意', 3: '适中', 4: '偏正式', 5: '很正式'}
emot_labels = {1: '很冷淡', 2: '偏冷淡', 3: '适中', 4: '偏情绪化', 5: '情绪外露'}
humor_labels = {1: '很严肃', 2: '偏严肃', 3: '偶尔幽默', 4: '比较幽默', 5: '很幽默'}
conf_labels = {1: '很不自信', 2: '偏谨慎', 3: '适中', 4: '较自信', 5: '很自信'}

for fname in os.listdir(PERSONA_DIR):
    if not fname.endswith('.persona.json'):
        continue
    fpath = os.path.join(PERSONA_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        d = json.load(f)
    
    # Fix tone labels
    form = d['tone'].get('formality', 3)
    emot = d['tone'].get('emotion', 3)
    humor = d['tone'].get('humor', 3)
    conf = d['tone'].get('confidence', 3)
    
    d['tone']['formality_label'] = form_labels.get(form, '适中')
    d['tone']['emotion_label'] = emot_labels.get(emot, '适中')
    d['tone']['humor_label'] = humor_labels.get(humor, '偶尔幽默')
    d['tone']['confidence_label'] = conf_labels.get(conf, '适中')
    d['tone']['description'] = f"说话{form_labels.get(form, '适中')}，语气{emot_labels.get(emot, '适中')}，整体给人{humor_labels.get(humor, '偶尔幽默')}的感觉"
    
    # Fix snippet
    snippet = d.get('system_prompt_snippet', '')
    snippet = snippet.replace('emot_labels[emot]', emot_labels.get(emot, '适中'))
    d['system_prompt_snippet'] = snippet
    
    with open(fpath, 'w', encoding='utf-8') as f2:
        json.dump(d, f2, ensure_ascii=False, indent=2)
    print(f"Fixed: {fname}")

print("Done!")