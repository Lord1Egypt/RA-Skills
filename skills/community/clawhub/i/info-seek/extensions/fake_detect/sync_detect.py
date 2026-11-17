# -*- coding: utf-8 -*-
"""
extensions/fake_detect/sync_detect.py — 时序同步检测（v1.0.0 · 函数化提取）

来源：fake_detect_test/sync_test.py（评估脚本）函数化提取，仅保留核心检测函数。
定位：L1 小集群时序同步兜底信号（≤10 人 @ ≤0.25 密度小集群的唯一可行信号——
     纯图结构检测在此场景 ≈0.57 组级命中物理极限，共享涨粉事件是仅剩协调信号）。

纯时序、与图结构完全解耦：
  1) spike 二值化     : g > mean(g) + z*std(g) 且 >= abs_thr
  2) 成对 min-覆盖    : C[i,j] = min(overlap/n_i, overlap/n_j)   (Jaccard 抗噪替代)
  3) 强边图           : A >= overlap_min 且 C >= cover_thr  -> 连边
  4) 局部净化准团     : 迭代剔除组内强边最少成员至内部高边占比 >= frac_thr
  5) 准团级同步后验   : group_j = 多数成员共同 spike 日 / 并集日 >= group_j_thr
  6) 规模带过滤       : [min_size, max_size]（2 人同期不算协调；超大团交给 L1/L2）

用法:
    from sync_detect import detect_sync
    susp, comps = detect_sync(growth, sorted(growth.keys()))
    # susp: 同步成员 id 集合 | comps: [{id,...} 准团成员集 列表]
"""
import numpy as np
import networkx as nx


# ---------- 时序同步特征 ----------
def spike_binarize(g, z=3.0, abs_thr=3.0):
    """涨粉事件二值化: 显著高于自身基线 -> 事件日"""
    g = np.asarray(g, dtype=float)
    thr = float(np.mean(g) + z * np.std(g))
    thr = max(thr, abs_thr)
    return (g > thr).astype(np.uint8)


def dilate_spikes(S, r=1):
    """事件日 1D 膨胀 ±r 天: 容忍跨账号 1-2 天的时间抖动 (事件对齐鲁棒性)"""
    Sd = S.copy()
    for shift in range(1, r + 1):
        Sd[:, :-shift] |= S[:, shift:]
        Sd[:, shift:] |= S[:, :-shift]
    return Sd


def coverage_matrix(S):
    """
    min-覆盖矩阵: C[i,j] = min(overlap/n_i, overlap/n_j)
      - 事件同步语义: 双方事件日的重合率 (Jaccard 被个别噪声 spike 日 + 并集膨胀拖累)
      - 真集群成员对 C≈0.5-1.0, 随机脉冲账号对 C<0.2
    """
    A = S @ S.T
    ni = S.sum(axis=1).astype(float)
    Ci = A / np.maximum(ni[:, None], 1.0)
    Cj = A / np.maximum(ni[None, :], 1.0)
    C = np.minimum(Ci, Cj)
    return C, A


def local_clique_membership(B, Sd, min_size=3, frac_thr=0.5,
                            common_frac=0.7, group_j_thr=0.15):
    """
    局部净化式准团判定 + 准团级同步后验 (v8):
      1) 净化: 从强邻居集 N'(u) 开始, 迭代剔除"组内强边数最少"的节点,
         直到 N'(u)∪{u} 内部高边占比 >= frac_thr 且规模 >= min_size
      2) 同步后验: 准团内 >= common_frac 比例的成员共同 spike 的日数 / 并集日数
         - 真共享事件: 事件核心日多数成员同触达 -> group_j 0.25-0.45
         - 随机脉冲重叠 (孤立水军/正常噪声): 无集中共同日 -> group_j ~0.0x
      报告单元 = 净化收敛准团本身 (不连通聚合, 与规模过滤解耦)
      返回 (member_bool, cliques)
    """
    n = B.shape[0]
    member = np.zeros(n, dtype=bool)
    cliques = []
    nb_list = [np.flatnonzero(B[i]).tolist() for i in range(n)]
    for u in range(n):
        nb = [v for v in nb_list[u] if v != u]
        while len(nb) >= min_size - 1:
            m = sorted(nb + [u])
            sub = B[np.ix_(m, m)]
            k = len(m)
            frac = float(sub[np.triu_indices(k, 1)].mean())
            if frac >= frac_thr:
                common = int((Sd[m].sum(axis=0) >= max(2, int(np.ceil(common_frac * k)))).sum())
                union = int((Sd[m].sum(axis=0) > 0).sum())
                group_j = common / max(union, 1)
                if group_j >= group_j_thr:
                    member[u] = True
                    cliques.append(frozenset(m))
                break
            # 剔除组内强边最少的成员 (u 永久保留, 噪声节点优先出局)
            deg_in = sub.sum(axis=1)
            worst = m[int(np.argmin(deg_in))] if k > 1 else u
            if worst == u:
                break
            nb.remove(worst)
    return member, cliques


def report_components(member, B, min_size=3, max_size=50):
    """
    把同步成员按其强边连通归并为组件, 应用规模带 [min_size, max_size]:
      - min_size: 2 人同期不算协调 (排除情侣号/互粉对)
      - max_size: 孤立水军 170人随机重叠大网 = 非同步网络, 由 L1/L2 负责;
        同步检测器只报"小规模真同步组" (≤小集群任务定位), 大团整体不输出
        -> 搭在大团上的边缘账号 (含正常噪声) 随之从输出消失
    """
    n = B.shape[0]
    Gs = nx.Graph()
    Gs.add_nodes_from(range(n))
    ei, ej = np.where(np.triu(B, 1) & member[:, None] & member[None, :])
    Gs.add_edges_from(zip(ei.tolist(), ej.tolist()))
    comps = [set(c) for c in nx.connected_components(Gs)
             if min_size <= len(c) <= max_size and all(member[x] for x in c)]
    return comps


def run_counts(S):
    """每账号原始 spike 连续段(簇)数: 真集群=3个分散事件=3簇, 噪声注入=1-2簇"""
    pad = np.zeros((S.shape[0], 1), dtype=np.uint8)
    S2 = np.concatenate([pad, S, pad], axis=1)
    return ((np.diff(S2.astype(np.int8), axis=1) == 1).sum(axis=1)).astype(int)


def detect_sync(growth, ids_order, cover_thr=0.4, overlap_min=2, min_size=3,
                frac_thr=0.5, z=3.0, abs_thr=4.0, dilate=1,
                min_spike_days=5, min_clusters=2, max_size=50,
                common_frac=0.7, group_j_thr=0.15):
    """
    全部账号时序同步检测, 返回 (susp_set, comps)
      spike 二值化 -> ±1天膨胀 -> min-覆盖矩阵 -> 强边B -> 局部净化准团判定
      + 准团级同步后验 (group_j: 多数成员共同日/并集日 > 0.15)
      账号级过滤: min_spike_days / min_clusters
      组件级过滤: [min_size, max_size] 规模带 (report_components)
    """
    N = len(ids_order)
    # 矩阵宽度按输入序列最大长度动态分配（函数化改进：原评估脚本固定 180 天）
    seq_len = max((len(np.asarray(growth[i], dtype=float)) for i in ids_order), default=180)
    S = np.zeros((N, seq_len), dtype=np.uint8)
    for k, i in enumerate(ids_order):
        S[k] = spike_binarize(growth[i], z=z, abs_thr=abs_thr)
    Sd = dilate_spikes(S, r=dilate) if dilate > 0 else S
    C, A = coverage_matrix(Sd)
    B = (A >= overlap_min) & (C >= cover_thr)
    keep = np.ones(N, dtype=bool)
    if min_spike_days > 0:
        keep &= Sd.sum(axis=1) >= min_spike_days
    if min_clusters > 0:
        keep &= run_counts(S) >= min_clusters
    if not keep.all():
        B = B & keep[:, None] & keep[None, :]
    member, cliques = local_clique_membership(B, Sd, min_size=min_size, frac_thr=frac_thr,
                                              common_frac=common_frac, group_j_thr=group_j_thr)
    # 报告单元 = 净化准团 (去重), size 带过滤后取并集
    comps = [set(c) for c in set(cliques) if min_size <= len(c) <= max_size]
    susp = set()
    for c in comps:
        susp |= {ids_order[k] for k in c}
    return susp, comps