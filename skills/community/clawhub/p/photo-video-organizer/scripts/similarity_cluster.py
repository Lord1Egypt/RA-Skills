#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 相似聚类（Tier B）：按(拍摄日期,地理位置)分组 → 组内CLIP余弦聚类 → 大组多级递归细分 → 25%保留
# 用法: python similarity_cluster.py <exif_json> <clip_cache_json> [TH] [TH_SUB] [SPLIT_MIN] [out_csv] [out_json]
# 只读，不移动文件。排除已不存在的文件（已移走的）。
import os, sys, json, csv
import numpy as np
from collections import defaultdict

def groups_of(exif):
    g = defaultdict(list)
    for p, v in exif.items():
        d = v.get('date'); gps = v.get('gps')
        key = (d, (round(gps[0],2), round(gps[1],2))) if (d and gps) else (d, None)
        g[key].append(p)
    return g

def quality(p, exif):
    v = exif.get(p, {})
    try: sz = float(v.get('size') or 0)
    except Exception: sz = 0
    has_gps = 1 if v.get('gps') else 0
    nonwx = 0 if 'weixin' in os.path.basename(p).lower() else 1
    return (sz, has_gps, nonwx)

def main():
    exif = json.load(open(sys.argv[1], encoding='utf-8'))
    cache = json.load(open(sys.argv[2], encoding='utf-8'))
    TH = float(sys.argv[3]) if len(sys.argv) > 3 else 0.88
    TH_SUB = float(sys.argv[4]) if len(sys.argv) > 4 else 0.94
    SPLIT_MIN = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    out_csv = sys.argv[6] if len(sys.argv) > 6 else os.path.join(os.getcwd(), '相似候选清单.csv')
    out_json = sys.argv[7] if len(sys.argv) > 7 else os.path.join(os.getcwd(), 'sim_groups.json')
    groups = groups_of(exif)
    out_groups = []; gid = 0; total_move = 0
    for key, members in groups.items():
        emb = [p for p in members if p in cache and cache[p].get('vec') and os.path.exists(p)]
        if len(emb) < 2: continue
        vecs = np.array([cache[p]['vec'] for p in emb], dtype=np.float32)
        norms = np.linalg.norm(vecs, axis=1, keepdims=True); norms[norms==0]=1
        sim = (vecs/norms) @ (vecs/norms).T
        n = len(emb)
        def uf_cluster(idxs, thr):
            parent = {i:i for i in idxs}
            def find(x):
                while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
                return x
            for ii in range(len(idxs)):
                for jj in range(ii+1, len(idxs)):
                    if sim[idxs[ii]][idxs[jj]] >= thr:
                        ra,rb=find(idxs[ii]),find(idxs[jj])
                        if ra!=rb: parent[ra]=rb
            d=defaultdict(list)
            for i in idxs: d[find(i)].append(i)
            return list(d.values())
        def rec_split(idxs, thr):
            if len(idxs) <= SPLIT_MIN or thr > 0.98: return [idxs]
            sub = uf_cluster(idxs, thr); res = []
            for s in sub:
                if len(s) > SPLIT_MIN and thr+0.02 <= 0.98: res.extend(rec_split(s, thr+0.02))
                else: res.append(s)
            return res
        for idxs in uf_cluster(list(range(n)), TH):
            if len(idxs) < 2: continue
            final = rec_split(idxs, TH_SUB) if len(idxs) > SPLIT_MIN else [idxs]
            for sub in final:
                if len(sub) < 2: continue
                gid += 1
                paths = [emb[i] for i in sub]
                ps = sorted(paths, key=lambda p: quality(p,exif), reverse=True)
                keep_n = max(1, min(5, round(0.25*len(paths))))
                keep, moves = ps[:keep_n], ps[keep_n:]
                pm = 0.0
                for ii,i in enumerate(sub):
                    for j in sub[ii+1:]: pm = max(pm, float(sim[i][j]))
                out_groups.append({'gid':gid,'date':key[0],'loc':key[1],'keep':keep,'move':moves,'sim_max':pm})
                total_move += len(moves)
    with open(out_csv,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['组号','日期','位置','保留文件','候选移除数','候选移除文件','最高相似度'])
        for g in out_groups:
            w.writerow([g['gid'],g['date'],g['loc'],' | '.join(os.path.basename(x) for x in g['keep']),
                        len(g['move']),' | '.join(os.path.basename(x) for x in g['move']), round(g['sim_max'],3)])
    json.dump(out_groups, open(out_json,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"相似组: {len(out_groups)}, 候选移除: {total_move} → {out_csv}")

if __name__ == '__main__':
    main()
