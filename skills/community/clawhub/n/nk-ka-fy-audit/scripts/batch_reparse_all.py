"""
Batch re-parse ALL months with fully fixed parser.
"""
import sqlite3, subprocess, os, sys

DB = '/workspace/data/ka_commission_audit.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

# Delete ALL existing data
c.execute('DELETE FROM raw_records')
c.execute('DELETE FROM brand_audit')
conn.commit()

# Get all month directories
months = sorted([d for d in os.listdir('/workspace/data') 
                 if len(d) == 6 and d.isdigit()])

print(f'Re-parsing {len(months)} months...')
for i, m in enumerate(months):
    print(f'  [{i+1}/{len(months)}] {m}...', end=' ')
    sys.stdout.flush()
    result = subprocess.run(['python3', '/workspace/scripts/parse_one_month.py', m],
                          capture_output=True, text=True, timeout=120)
    if result.stdout.strip():
        print(result.stdout.strip().split('\n')[0])
    if result.stderr:
        print(f'  STDERR: {result.stderr[:100]}')

conn.close()
print('\n✅ All months re-parsed!')
