#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def run(name):
    out = subprocess.check_output([sys.executable, str(ROOT/'scripts/check_names.py'), str(ROOT/'fixtures'/name)], text=True)
    return json.loads(out)

def main():
    success = run('success.json')
    failure = run('failure.json')
    assert success['variants']['小岚'] == ['zhou-lan-a']
    assert not any(rule == {'speaker': 'grandma', 'address': '小岚', 'target': 'zhou-lan-b'} for rule in json.load(open(ROOT/'fixtures/success.json', encoding='utf-8'))['rules'])
    assert any(x[0] == '第3章·3' and x[1] == '小岚' and x[2] == '错称' for x in success['findings'])
    assert any(x[0] == '第3章·6' and x[1] == '小友' and x[2] == '错称' and '未获批准' in x[3] for x in success['findings'])
    assert any(x[0] == '第3章·1' and x[1] == '小岚' for x in success['findings']) is False
    assert any(x[0] == '第3章·6' and x[1] == '小友' and x[2] == '错称' for x in success['findings'])
    assert not any(x[1] == '周蓝' and x[2] == '错称' for x in success['findings'])
    assert any(x[1] == '老周' and x[2] == '待确认' for x in failure['findings'])
    # A rule is scoped to its approved target, even when speaker and wording match.
    assert any(x[0] == '第3章·3' and '登记归属周岚' in x[3] and '三者同时匹配的批准规则' in x[3] for x in success['findings'])
    address_error = next(x for x in success['findings'] if x[0] == '第3章·3')
    assert '仅核对此处' in address_error[4] and '周蓝' in address_error[4], address_error
    typo = next(x for x in success['findings'] if x[0] == '第3章·5')
    assert typo[2] == '错称' and typo[1] == '周篮' and '周岚' in typo[4], typo
    import tempfile
    sample = {
        'people':[{'id':'s','name':'说话人','aliases':[]},{'id':'a','name':'甲','aliases':['同名']},{'id':'b','name':'乙','aliases':['同名']}],
        'rules':[{'speaker':'s','address':'宝贝','target':'a'},{'speaker':'s','address':'宝贝','target':'b'}],
        'mentions':[{'anchor':'x1','token':'宝贝','kind':'address','speaker':'s','target':'a'}, {'anchor':'x2','token':'宝贝','kind':'address','speaker':'s','target':'b'}, {'anchor':'x3','token':'同名','kind':'name','target':'b'}, {'anchor':'x4','token':'甲','kind':'name','target':'ghost'}, {'anchor':'x5','token':'甲','kind':'address','speaker':'ghost','target':'a'}, {'anchor':'x6','token':'甲','kind':'address','speaker':'s','target':'a'}, {'anchor':'x7','token':'同名','kind':'name'}, {'anchor':'x8','token':'同名','kind':'address','speaker':'s'}]
    }
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.json') as f:
        json.dump(sample, f, ensure_ascii=False); f.flush()
        out = json.loads(subprocess.check_output([sys.executable, str(ROOT/'scripts/check_names.py'), f.name], text=True))
    assert not any(row[0] in {'x1','x2','x3'} for row in out['findings']), out['findings']
    assert {row[0] for row in out['findings']} == {'x4','x5','x6','x7','x8'}, out['findings']
    assert all(row[2] == '待确认' for row in out['findings'] if row[0] in {'x4','x5'}), out['findings']
    assert next(row for row in out['findings'] if row[0] == 'x7')[2] == '待确认', out['findings']
    duplicate_mismatch = dict(sample)
    duplicate_mismatch['people'] = sample['people'] + [{'id':'c','name':'丙','aliases':[]}]
    duplicate_mismatch['mentions'] = [{'anchor':'x8','token':'同名','kind':'name','target':'c'}]
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.json') as f:
        json.dump(duplicate_mismatch, f, ensure_ascii=False); f.flush()
        mismatch_out=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/check_names.py'),f.name],text=True))
    assert mismatch_out['findings'][0][2] == '错称' and '全局替换' in mismatch_out['findings'][0][4], mismatch_out['findings']
    # Multiple owners do not make an address pending when its explicit target
    # is a third person: none of those owners can be the target.
    duplicate_address = dict(duplicate_mismatch)
    duplicate_address['mentions'] = [{'anchor':'x9','token':'同名','kind':'address','speaker':'s','target':'c'}]
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.json') as f:
        json.dump(duplicate_address, f, ensure_ascii=False); f.flush()
        duplicate_address_out = json.loads(subprocess.check_output([sys.executable, str(ROOT/'scripts/check_names.py'), f.name], text=True))
    duplicate_address_finding = duplicate_address_out['findings'][0]
    assert duplicate_address_finding[2] == '错称', duplicate_address_out['findings']
    assert '甲、乙' in duplicate_address_finding[3] and '丙' in duplicate_address_finding[3], duplicate_address_finding
    assert '仅核对此处' in duplicate_address_finding[4] and '全局替换' in duplicate_address_finding[4], duplicate_address_finding
    # A shared alias in an address without a target ID is unresolvable and
    # must remain pending rather than being treated as a wrong address.
    ambiguous_address = next(row for row in out['findings'] if row[0] == 'x8')
    assert ambiguous_address[2] == '待确认' and '同名或同别名' in ambiguous_address[3], ambiguous_address
    # A known name is still a wrong address if a valid speaker and target
    # lack this exact approved triple; it must not be downgraded to pending.
    unapproved = next(row for row in out['findings'] if row[0] == 'x6')
    assert unapproved[2] == '错称' and '未获批准' in unapproved[3], unapproved
    missing_speaker=json.loads(json.dumps(sample)); missing_speaker['mentions']=[{'anchor':'x7','token':'宝贝','kind':'address','target':'a'}]
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.json') as f:
        json.dump(missing_speaker, f, ensure_ascii=False); f.flush()
        missing_out=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/check_names.py'),f.name],text=True))
    assert missing_out['findings'][0][3] == '缺少说话人 ID'
    print('PASS: approved triples pass; unresolved shared names/aliases and unknown IDs await confirmation.')
if __name__ == '__main__': main()
