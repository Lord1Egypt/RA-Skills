import json, os, shutil, sys

sys.stdout.reconfigure(encoding='utf-8')

folder = r'C:\Users\taizun\Desktop\Document\文献\LLM\LLMxGame Theory'
manifest_out = os.path.join(os.path.dirname(__file__), 'manifest_verified.json')

with open(manifest_out, 'r', encoding='utf-8') as f:
    m = json.load(f)

def sanitize(name):
    for ch in '<>:"/\\|?*':
        name = name.replace(ch, '')
    return name.strip()

backup_dir = os.path.join(folder, f'_backup_20260530_120302')
os.makedirs(backup_dir, exist_ok=True)

for entry in m[9:]:  # only entries 10-15 (0-indexed)
    fname = entry['filename']
    src = os.path.join(folder, fname)
    year = entry['year'] or '????'
    venue = entry['venue'] or ''
    title = entry['title']
    new_name = f'[{year}]' + (f' [{venue}]' if venue else '') + ' ' + title + '.pdf'
    new_name = sanitize(new_name)
    dst = os.path.join(folder, new_name)

    # Backup
    try:
        shutil.copy2(src, os.path.join(backup_dir, fname))
    except Exception as e:
        print(f'[BACKUP FAIL] {fname}: {e}')

    # Rename using os.rename (Unicode-safe on Windows)
    try:
        os.rename(src, dst)
        print(f'[OK] {fname}')
        print(f'     -> {new_name}')
    except Exception as e:
        print(f'[FAIL] {fname}: {e}')

print('\nDone')