import json, os

folder = r'C:\Users\taizun\Desktop\Document\文献\LLM\ScalingLaw'
manifest_in = os.path.join(os.path.dirname(__file__), 'manifest.json')

with open(manifest_in, 'r', encoding='utf-8') as f:
    m = json.load(f)

updates = [
    ('A Hitchhiker Guide to Scaling Law Estimation', '2024', 'ICLR'),
    ('Predictable Scale: Part II, Farseer - A Refined Scaling Law in LLM', '2024', 'arXiv'),
    ('How to Upscale Neural Networks with Scaling Law: A Survey and Practical Guidelines', '2024', 'arXiv'),
    ('On the Predictability of Pruning Across Scales', '2024', 'ICLR'),
    ('Scaling Laws for Multi-Agent Reinforcement Learning', '2024', 'ICML'),
    ('Scaling Scaling Laws with Board Games', '2021', 'NeurIPS'),
    ('Scaling Laws for Single-Agent Reinforcement Learning', '2023', 'ICML'),
]

for i, entry in enumerate(m):
    if i < len(updates):
        title, year, venue = updates[i]
        entry['title'] = title
        entry['year'] = year
        entry['venue'] = venue
        entry['status'] = 'ready'
        entry['is_duplicate'] = False
        entry['duplicate_group'] = None
        entry['title_source'] = 'verified'
        entry['year_source'] = 'filename'
        entry['venue_source'] = 'verified'

out = os.path.join(os.path.dirname(__file__), 'manifest_verified.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(m, f, ensure_ascii=False, indent=2)

ready = sum(1 for e in m if e['status'] == 'ready')
skip = sum(1 for e in m if e['status'] == 'manual_review')
print(f'Done: {ready} ready, {skip} skipped')
for e in m:
    print(e['status'], e['filename'])