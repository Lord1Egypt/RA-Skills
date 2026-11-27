# -*- coding: utf-8 -*-
"""持久化数据 API 实测：persist_init / persist_set / persist_get 等"""
import sys, io, os, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *
import gm.api as gmapi

print('gm 版本检查：')
try:
    import importlib.metadata as md
    print('  gm-api', md.version('gm'))
except Exception as e:
    print('  ', e)

TOKEN = os.environ.get('GM_TOKEN', '')
set_token(TOKEN)
print('token 已设置\n')

BUCKET = 'gmquant_test_bucket'

def show(tag, val):
    print(f'[{tag}] {val!r}')

print('=' * 60)
print('TEST 1: persist_init 在纯数据查询模式下是否可用')
print('=' * 60)
try:
    st = persist_init(BUCKET, is_async=False)
    show('persist_init status', st)
    inited = (st == 0)
except Exception as e:
    print(f'  EXCEPTION: {type(e).__name__}: {e}')
    inited = False

print()
print('=' * 60)
print('TEST 2: persist_set 写入字符串')
print('=' * 60)
if inited:
    try:
        st = persist_set('stock_pool', 'SHSE.600519,SZSE.000001')
        show('persist_set status', st)
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 3: persist_get 读取')
    print('=' * 60)
    try:
        v = persist_get('stock_pool')
        show('persist_get', v)
        print('  预期 SHSE.600519,SZSE.000001 ->', 'PASS' if v == 'SHSE.600519,SZSE.000001' else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 4: persist_get 读取不存在的 key（应返回 None）')
    print('=' * 60)
    try:
        v = persist_get('not_exist_key_xyz')
        show('persist_get(missing)', v)
        print('  预期 None ->', 'PASS' if v is None else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 5: persist_set 覆盖写入已有 key')
    print('=' * 60)
    try:
        st = persist_set('stock_pool', 'SHSE.600000')
        show('persist_set(overwrite) status', st)
        v = persist_get('stock_pool')
        show('persist_get after overwrite', v)
        print('  预期 SHSE.600000 ->', 'PASS' if v == 'SHSE.600000' else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 6: persist_set_obj / persist_get_obj（JSON 对象读写）')
    print('=' * 60)
    try:
        pool = {'stocks': ['SHSE.600519', 'SZSE.000001'], 'updated_at': 20261127}
        st = persist_set_obj('stock_pool_obj', pool)
        show('persist_set_obj status', st)
        data = persist_get_obj('stock_pool_obj')
        show('persist_get_obj', data)
        print('  往返一致 ->', 'PASS' if data == pool else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 7: persist_get_all_keys')
    print('=' * 60)
    try:
        keys = persist_get_all_keys()
        show('persist_get_all_keys', keys)
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 8: persist_get_all_buckets')
    print('=' * 60)
    try:
        bks = persist_get_all_buckets()
        show('persist_get_all_buckets', bks)
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 9: persist_delete（删除单个 key）')
    print('=' * 60)
    try:
        st = persist_delete('stock_pool')
        show('persist_delete status', st)
        v = persist_get('stock_pool')
        show('persist_get after delete', v)
        print('  预期 None ->', 'PASS' if v is None else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 10: persist_delete 不存在的 key（幂等，应返回 0）')
    print('=' * 60)
    try:
        st = persist_delete('ghost_key_never_exists')
        show('persist_delete(missing) status', st)
        print('  预期 0 ->', 'PASS' if st == 0 else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 11: persist_clear（清空当前 bucket）')
    print('=' * 60)
    try:
        st = persist_clear()
        show('persist_clear status', st)
        keys = persist_get_all_keys()
        show('keys after clear', keys)
        print('  预期 [] ->', 'PASS' if not keys else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 12: persist_init 重复初始化同一 bucket（幂等）')
    print('=' * 60)
    try:
        st = persist_init(BUCKET, is_async=False)
        show('persist_init(same bucket again) status', st)
        print('  预期 0 ->', 'PASS' if st == 0 else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 13: persist_init 初始化不同 bucket（应报错 71006）')
    print('=' * 60)
    try:
        st = persist_init('another_bucket_xyz', is_async=False)
        show('persist_init(other bucket) status', st)
        print('  预期 非0 (71006) ->', 'PASS' if st != 0 else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 14: persist_delete_bucket 删除非当前绑定的 bucket')
    print('=' * 60)
    try:
        st = persist_delete_bucket('another_bucket_xyz')
        show('persist_delete_bucket status', st)
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')

    print()
    print('=' * 60)
    print('TEST 15: persist_delete_bucket 删除当前绑定的 bucket（应失败 71005）')
    print('=' * 60)
    try:
        st = persist_delete_bucket(BUCKET)
        show('persist_delete_bucket(current) status', st)
        print('  预期 非0 (71005) ->', 'PASS' if st != 0 else 'FAIL')
    except Exception as e:
        print(f'  EXCEPTION: {type(e).__name__}: {e}')
else:
    print('\n[跳过] persist_init 未成功，后续测试全部跳过')

print()
print('=' * 60)
print('TEST 16: persist_set 在未 persist_init 时调用（新进程验证）')
print('=' * 60)
print('  见独立脚本 test_persist_no_init.py')

print('\n完成')
