import json, pandas as pd

# Read holdings analysis
with open(r'C:\Users\Administrator\.qclaw\workspace-ag01\data\trend_scan\holdings_analysis.json', 'r', encoding='utf-8') as f:
    ha = json.load(f)

# Read trend scan
ts = pd.read_csv(r'C:\Users\Administrator\.qclaw\workspace-ag01\data\trend_scan\trend_scan_2026-04-13.csv')
ts['code'] = ts['code'].astype(str).str.zfill(6)

# Check for holdings in trend scan
codes = [p['code'].zfill(6) for p in ha['positions']]
print('Trend scan:', len(ts), 'stocks, mean score:', round(ts['final_score'].mean(), 1))
print('Holdings:', len(ha['positions']))
print()
for c in codes:
    match = ts[ts['code']==c]
    if not match.empty:
        r = match.iloc[0]
        level = r['level'].replace('\U0001f7e2','').replace('\U0001f7e1','').replace('\U0001f7e0','').replace('\U0001f7df','').replace('\U0001f7e3','').strip()
        print('%s trend_score=%d level=%s' % (c, int(r.final_score), level))
    else:
        print('%s not in trend scan (score < 55)' % c)
