"""Batch re-parse all months with 志华 data"""
import sqlite3, subprocess, sys

DB = '/workspace/data/ka_commission_audit.db'
months = ['202309', '202310', '202311', '202312', '202401', '202402', '202403', '202404', '202405', '202406']

conn = sqlite3.connect(DB)
c = conn.cursor()

for m in months:
    print(f'\n=== Parsing {m} ===')
    # Delete old data
    c.execute("DELETE FROM raw_records WHERE month=?", (m,))
    conn.commit()
    
    # Run parser
    result = subprocess.run(['python3', '/workspace/scripts/parse_one_month.py', m], 
                          capture_output=True, text=True, timeout=120)
    print(result.stdout)
    if result.stderr:
        print(f'STDERR: {result.stderr[:500]}')

conn.close()
print('\n=== All months done ===')
