#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 按用户决定可逆移动：读决定CSV(move行) → 移入子文件夹，保留mtime，写日志+回滚脚本
# 用法: python move_reversible.py <decision_csv> <root_folder> <subdir_name> [--go]
# decision_csv 列: gid,decision,filename  (decision=move 的移走)
# 不带 --go 为校验模式(只统计不移动)
import csv, os, sys, json, shutil

def main():
    dec = sys.argv[1]; root = sys.argv[2]; subname = sys.argv[3]
    GO = '--go' in sys.argv
    subdir = os.path.join(root, subname)
    moves = []
    with open(dec, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['decision'].strip() == 'move':
                moves.append((r.get('gid',''), r['filename']))
    print(f"决定移除: {len(moves)} 个", flush=True)
    ok, missing, already = [], [], []
    for gid, fn in moves:
        src = os.path.join(root, fn); dst = os.path.join(subdir, fn)
        if os.path.exists(dst): already.append((gid, fn))
        elif os.path.exists(src): ok.append((gid, fn, src, dst))
        else: missing.append((gid, fn))
    print(f"  可移动: {len(ok)} | 已在子文件夹: {len(already)} | 源不存在: {len(missing)}", flush=True)
    if missing:
        for gid, fn in missing[:20]: print(f"    缺: gid{gid} {fn}", flush=True)
    if not GO:
        print("[校验模式] 未移动。加 --go 执行。", flush=True); return
    os.makedirs(subdir, exist_ok=True)
    log = []; done = fail = 0
    for gid, fn, src, dst in ok:
        try:
            mt = os.path.getmtime(src); shutil.move(src, dst); os.utime(dst, (mt, mt))
            log.append({'gid': gid, 'file': fn, 'from': src, 'to': dst, 'ok': True}); done += 1
        except Exception as e:
            log.append({'gid': gid, 'file': fn, 'from': src, 'to': dst, 'ok': False, 'err': str(e)}); fail += 1
        if (done+fail) % 50 == 0:
            json.dump(log, open(dec + '_move_log.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(f"  已移动 {done}/{len(ok)} 失败{fail}", flush=True)
    json.dump(log, open(dec + '_move_log.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    rb = dec + '_rollback.py'
    with open(rb, 'w', encoding='utf-8') as f:
        f.write("# -*- coding: utf-8 -*-\nimport os,shutil,json\n")
        f.write(f"log=json.load(open({dec+'_move_log.json'!r},encoding='utf-8'))\nn=0\n")
        f.write("for x in log:\n  if not x['ok']:continue\n  if os.path.exists(x['to']):\n    shutil.move(x['to'],x['from']);n+=1\n")
        f.write("print(f'回滚 {n} 个')\n")
    print(f"完成: 成功{done} 失败{fail}\n子文件夹: {subdir}\n日志: {dec}_move_log.json\n回滚: python {rb}")

if __name__ == '__main__':
    main()
