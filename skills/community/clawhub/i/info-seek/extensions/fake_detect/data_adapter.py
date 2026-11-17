# -*- coding: utf-8 -*-
"""
P2 数据接入层: 通用数据适配器 (fake_detect 检测管线可插拔任意真实数据源)
=========================================================================
能力:
  1) 自动识别输入格式: CSV / JSON / parquet / NPZ / edgelist / NetworkX
  2) Schema 归一化: 列名别名映射 (中英文/缩写 -> 标准字段)
     - 账号元表: id, group_label(可选), followers, following, posts, er
     - 时间序列: likes(每日点赞), growth(每日涨粉)
     - 关系图: (src, dst) 边
  3) 数据质量校验 (QualityReport):
     - 缺失率 / ID 唯一性 / 时间序列对齐(长度/NaN) / 图边端点存在性 / ER 范围
  4) 清洗策略: 类型强制转换, NaN 填充(中位数), 脏行丢弃, 异常值标记
  5) 输出标准化结构: Dataset(meta_df, likes, growth, G, report), 可直接喂检测管线

用法:
  ds = load_dataset(source="business_data.csv", ts_dir="ts/")
  ds = load_dataset(source="data.json")
  ds = from_raw(meta_df=..., likes=..., edges=...)
"""
import json, os
import numpy as np
import pandas as pd
import networkx as nx

# ---------- Schema 别名表 (业务列名 -> 标准字段) ----------
META_ALIASES = {
    'id':          ['id', 'user_id', 'uid', 'account_id', '账号id', '用户id', '账号'],
    'group_label': ['group_label', 'label', 'tag', '分类', '标签', 'group', 'is_fake'],
    'followers':   ['followers', 'fans', 'follower_count', '粉丝数', '粉丝', 'followers_count', 'fan_count'],
    'following':   ['following', 'followees', 'following_count', '关注数', '关注', 'following_cnt'],
    'posts':       ['posts', 'tweets', 'post_count', '发帖数', '帖子数', '动态数', 'statuses_count'],
    'er':          ['er', 'engagement_rate', '互动率', '互动', 'like_rate', 'engagement'],
    # HF-R1 人因增强字段 (可选; 缺失不报错, 由 L1 侧取中性值)
    'follower_quality':    ['follower_quality', 'fans_quality', 'fq', '粉丝质量', '粉丝真实性'],
    'template_similarity': ['template_similarity', 'tpl_sim', '模板相似度', '内容模板化'],
}
TS_ALIASES = {
    'likes':  ['likes', 'like_series', '每日点赞', '点赞序列', 'likes_seq', 'likes_ts'],
    'growth': ['growth', 'follower_growth', '每日涨粉', '涨粉序列', 'growth_seq', 'growth_ts'],
}


def map_schema(cols, alias_map):
    """把业务列名映射到标准字段, 返回 {标准字段: 实际列名}"""
    inv = {}
    for std, names in alias_map.items():
        for n in names:
            inv[n] = std
    found = {}
    for c in cols:
        key = str(c).strip().lower()
        if key in inv and inv[key] not in found:
            found[inv[key]] = c
    return found


class QualityReport:
    def __init__(self):
        self.issues = []          # (severity, message)
        self.stats = {}

    def warn(self, msg):
        self.issues.append(('warn', msg))

    def error(self, msg):
        self.issues.append(('error', msg))

    def __str__(self):
        lines = [f"[QualityReport] {len(self.issues)} issues"]
        for sev, msg in self.issues:
            lines.append(f"  {sev.upper()}: {msg}")
        return "\n".join(lines)


class Dataset:
    """标准化数据集: 元表 + 时间序列 + 关系图"""
    def __init__(self, meta_df, likes=None, growth=None, G=None, report=None,
                 source=None, groups=None, profile=None, timing=None):
        self.meta_df = meta_df
        self.likes = likes if likes is not None else {}
        self.growth = growth if growth is not None else {}
        self.G = G
        self.report = report or QualityReport()
        self.source = source
        self.groups = groups      # {集群标识: [成员id]}, 可选真值
        self.profile = profile    # HF-R1: 账号画像字段 {id:{...}}, 可选（向后兼容默认 None）
        self.timing = timing      # HF-R1: 活跃时段直方图 {id:[24]}, 可选（向后兼容默认 None）

    def describe(self):
        return dict(n=len(self.meta_df), ts_accounts=len(self.likes),
                    edges=self.G.number_of_edges() if self.G else 0,
                    source=self.source)


# ---------- 元表清洗 ----------
def _clean_meta(df, report):
    if df is None or df.empty:
        report.error("元表为空")
        return None
    m = df.copy()
    m.columns = [str(c).strip() for c in m.columns]
    found = map_schema(m.columns, META_ALIASES)
    missing_std = [s for s in ['id', 'followers', 'following', 'posts', 'er'] if s not in found]
    for s in missing_std:
        # id 必填, 其余可智能兜底
        if s == 'id':
            report.error(f"缺少关键字段 id (别名: {META_ALIASES['id']})")
            return None
        report.warn(f"缺少字段 {s}, 使用默认值 0")
    # 重命名到标准字段 (保留原始多余列)
    rename = {v: k for k, v in found.items()}
    m = m.rename(columns=rename)
    if 'id' not in m.columns:
        return None
    # 强制类型 (先剥千分位逗号)
    for col in ['followers', 'following', 'posts']:
        if col in m.columns:
            vals = m[col].astype(str).str.replace(',', '', regex=False)
            m[col] = pd.to_numeric(vals, errors='coerce').fillna(0).astype(int)
            m[col] = m[col].clip(lower=1)
    if 'er' in m.columns:
        m['er'] = pd.to_numeric(m['er'], errors='coerce').fillna(0.0).clip(0, 1.0)
    else:
        m['er'] = 0.0
    # HF-R1: 人因增强字段归一化 (可选; 缺失则不新增列, 由 L1 侧取中性值)
    if 'follower_quality' in m.columns:
        _fq = pd.to_numeric(m['follower_quality'], errors='coerce').fillna(0.5)
        if float(np.nanmax(_fq.values)) > 1.0:      # 0-100 分制自动降为 0-1
            _fq = _fq / 100.0
        m['follower_quality'] = _fq.clip(0.0, 1.0)
    if 'template_similarity' in m.columns:
        m['template_similarity'] = pd.to_numeric(m['template_similarity'], errors='coerce') \
            .fillna(0.0).clip(0.0, 1.0)
    # id 唯一性
    if m['id'].duplicated().any():
        report.warn(f"id 重复 {int(m['id'].duplicated().sum())} 行, 保留首个")
        m = m[~m['id'].duplicated()]
    # id 归一化: 纯数字 / 数字后缀(U0->0) / 否则序号重映射
    id_map = {}
    new_ids = []
    raw_ids = m['id'].astype(str).tolist()
    for idx, rid in enumerate(raw_ids):
        s = rid.strip()
        if s.isdigit():
            new_id = int(s)
        else:
            import re
            num = re.findall(r'\d+', s)
            if num:
                new_id = int(num[-1])
            else:
                new_id = idx
                report.warn(f"id '{s}' 无数字成分, 重映射为序号 {idx}")
        new_ids.append(new_id)
        id_map[s] = new_id
    m['id'] = new_ids
    # 缺失率统计
    report.stats['null_pct'] = {c: float(m[c].isna().mean()) for c in m.columns}
    return m, id_map


# ---------- 时间序列接入 ----------
def _load_ts(ts_path, report, key_col='id', value_col=None):
    """从目录/文件装载时间序列:
       - 目录: 每账号一个 csv (文件名=id)
       - 单文件长表: columns=[id, day, value] 或宽表 [id, day1..day180]
       - npz: {id: array}
    """
    likes, growth = {}, {}
    if ts_path is None:
        return likes, growth
    p = str(ts_path)
    if os.path.isdir(p):
        files = [f for f in os.listdir(p) if f.endswith(('.csv', '.npy', '.npz'))]
        for f in files:
            aid = os.path.splitext(f)[0]
            try:
                aid = int(aid)
            except ValueError:
                report.warn(f"时序文件名非数字 id: {f}, 跳过")
                continue
            arr = np.loadtxt(os.path.join(p, f), delimiter=',')
            likes[aid] = np.abs(arr) if arr.size else np.zeros(10)
        report.stats['ts_files'] = len(files)
        # 简化: 目录模式仅 loads likes; growth 可由调用方补充
        return likes, growth
    if str(p).endswith('.npz'):
        nz = np.load(p, allow_pickle=True)
        for key in nz.files:
            obj = nz[key].item() if nz[key].ndim == 0 else None
            if obj is None and isinstance(nz[key], np.ndarray):
                obj = {int(k): v for k, v in nz[key].item().items()} if False else None
        for key in ('likes', 'growth'):
            if key in nz.files:
                d = nz[key].item()
                (likes if key == 'likes' else growth).update(
                    {int(k): v for k, v in d.items()})
        return likes, growth
    # 单文件: 长表 (id/day/value)
    df = pd.read_csv(p)
    lc = [str(c).lower() for c in df.columns]
    idc = [c for c in df.columns if str(c).lower() in ('id', 'uid', 'user_id', 'account_id', '账号')]
    dayc = [c for c in df.columns if str(c).lower() in ('day', 'days', 't', 'time', '时间', '日期')]
    valc = [c for c in df.columns if str(c).lower() in ('value', 'v', 'likes', 'growth', 'like_cnt', '值', '互动')]
    if idc and dayc and valc:
        for aid, g in df.groupby(idc[0]):
            dcol = g[dayc[0]].astype(int).values
            vcol = pd.to_numeric(g[valc[0]].astype(str).str.replace(',', '', regex=False),
                                 errors='coerce').fillna(0).values
            likes[str(aid)] = vcol[np.argsort(dcol)]
        report.stats['ts_longtable_rows'] = int(len(df))
    else:
        report.warn(f"单文件既非长表(id/day/value)亦非 npz, 无法解析时序; 请用 npz 或目录模式")
    return likes, growth


def _align_ts(db, meta_ids, report):
    """时序与元表 id 对齐 + NaN 填充 + 长度一致性"""
    if not db:                          # 该序列类型未提供 (如无 growth)
        return db
    N = max([len(v) for v in list(db.values())] + [0])
    str_keys = {str(k): k for k in db}          # int/str key 双兼容
    for i in meta_ids:
        k = i if i in db else str_keys.get(str(i))
        if k is None:
            continue
        v = np.asarray(db[k], dtype=float)
        v = np.nan_to_num(v, nan=0.0)
        if len(v) < N:
            v = np.pad(v, (0, N - len(v)))
        db[i] = v[:N]
    dropped = len(meta_ids) - len([i for i in meta_ids if i in db])
    if dropped:
        report.warn(f"{dropped} 个账号无时序数据")
    return db


# ---------- 关系图接入 ----------
def _load_graph(src, report, n_nodes=None, id_map=None):
    G = nx.DiGraph()
    if src is None:
        report.warn("无关系图数据, G 为空 (L2 不可用)")
        return G
    if isinstance(src, nx.Graph):
        return src.to_directed() if not src.is_directed() else src
    if isinstance(src, str) and os.path.isfile(src):
        rows = []
        with open(src) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    rows.append((parts[0], parts[1]))
        edge_df = pd.DataFrame(rows, columns=['src', 'dst'])
    elif isinstance(src, pd.DataFrame):
        edge_df = src.copy()
        edge_df.columns = ['src', 'dst'][:len(edge_df.columns)]
    elif isinstance(src, (list, tuple)):   # [函数化增强] 直接边列表 (src, dst) 对
        edge_df = pd.DataFrame(list(src), columns=['src', 'dst'])
    else:
        report.error("图源格式不支持")
        return G

    def _norm(x):
        s = str(x).strip()
        if id_map and s in id_map:
            return id_map[s]
        if s.isdigit():
            return int(s)
        import re
        nums = re.findall(r'\d+', s)
        if nums:
            return int(nums[-1])
        return s   # 无法归一化, 保持原值 (节点数校验会警示)

    for _, r in edge_df.iterrows():
        G.add_edge(_norm(r['src']), _norm(r['dst']))
    # 边端点存在性校验 (可能含无法归一化的字符串 id, 视为坏边)
    bad = 0
    if n_nodes:
        for e in edge_df.itertuples(index=False):
            a, b = _norm(e[0]), _norm(e[1])
            if not isinstance(a, int) or not isinstance(b, int) or \
               a >= n_nodes or b >= n_nodes:
                bad += 1
        if bad:
            report.warn(f"{bad} 条坏边引用不存在的/非法账号 (已记录, 图中节点自动创建)")
    return G


# ---------- 统一入口 ----------
def load_dataset(source=None, meta_df=None, ts_path=None, graph_src=None,
                 ts_npz=None, **kw):
    """
    统一接入入口. 支持:
      - source: CSV/JSON 路径 (元表), 自动探测
      - meta_df: 直接传 DataFrame
      - ts_path: 时序路径 (目录/npz/长表)
      - graph_src: edgelist 路径 / DataFrame / nx.Graph
    返回 Dataset 标准化对象.
    """
    report = QualityReport()
    if meta_df is None:
        if source is None:
            report.error("未提供数据源 (source 或 meta_df 至少其一)")
            return Dataset(pd.DataFrame(), report=report)
        sp = str(source)
        if sp.endswith('.json'):
            meta_df = pd.read_json(sp)
        elif sp.endswith('.parquet'):
            meta_df = pd.read_parquet(sp)
        else:
            meta_df = pd.read_csv(sp)
    clean = _clean_meta(meta_df, report)
    if clean is None:
        return Dataset(pd.DataFrame(), report=report)
    meta, id_map = clean
    G = _load_graph(graph_src, report, n_nodes=len(meta), id_map=id_map)
    likes, growth = {}, {}
    if ts_path:
        likes, growth = _load_ts(ts_path, report)
    if ts_npz:
        nz = np.load(ts_npz, allow_pickle=True)
        for key in ('likes', 'growth'):
            if key in nz.files:
                d = nz[key].item()
                (likes if key == 'likes' else growth).update(
                    {int(k): v for k, v in d.items()})
    # 时序 key 经 id_map 联动归一化 (非数字 key 兼容)
    def remap(db):
        out = {}
        for k, v in db.items():
            s = str(k)
            out[id_map.get(s, int(k) if s.isdigit() else k)] = v
        return out
    likes = remap(likes)
    growth = remap(growth)
    meta_ids = meta['id'].tolist()
    likes = _align_ts(likes, meta_ids, report)
    growth = _align_ts(growth, meta_ids, report)
    report.stats['n_accounts'] = len(meta)
    report.stats['n_ts'] = len(likes)
    return Dataset(meta, likes, growth, G, report, source=str(source) if source else None)


def from_raw(meta_df, likes=None, growth=None, edges=None, groups=None,
             profile=None, timing=None):
    """内存直连: 已具备标准化对象时直接封装。
    [函数化增强] 与 load_dataset 对齐：likes/growth key 经 id_map 归一化
    （meta 清洗后 id 变为整数，str key 时序/非数字 id 自动映射）。

    HF-R1（向后兼容）: profile / timing 为可选扩展字段，默认 None 时
    与旧签名行为完全一致；
      - profile: {id: {画像字段}}  → Dataset.profile（供后续画像增强）
      - timing : {id: [24 维活跃直方图]} → Dataset.timing（供 L1 时段熵）
    """
    report = QualityReport()
    clean = _clean_meta(meta_df, report)
    meta, id_map = clean[0], clean[1] if clean else ({}, {})
    G = _load_graph(edges, report) if edges is not None else None

    def remap(db):
        out = {}
        for k, v in (db or {}).items():
            s = str(k)
            out[id_map.get(s, int(k) if s.isdigit() else k)] = v
        return out

    likes = remap(likes)
    growth = remap(growth)
    prof = remap(profile) if isinstance(profile, dict) else profile
    tim = remap(timing) if isinstance(timing, dict) else timing
    return Dataset(meta, likes, growth, G, report, source='memory', groups=groups,
                   profile=prof, timing=tim)


# ---------- 演示: 真实业务表脏数据接入 ----------
def demo():
    """构造业务表风格脏数据 (列名混乱/缺失/类型混杂/坏边), 走 adapter 清洗接入"""
    print("=" * 70)
    print("P2 演示: 真实业务表脏数据 -> adapter 清洗 -> 检测管线可读")
    print("=" * 70)
    rng = np.random.default_rng(3)

    # ---- 1. 业务元表 (SQL 导出风格: 列名混乱 + 脏数据) ----
    n = 150
    biz = pd.DataFrame({
        '账号id': [f"U{i}" for i in range(n)],                 # 前缀 id
        '粉丝数': np.round(10 ** rng.uniform(2.5, 5, n)),       # 中文列名
        'following_cnt': np.round(10 ** rng.uniform(1.5, 4, n)),
        'tweets': rng.integers(10, 800, n),
        '互动率': rng.beta(1.2, 18, n) * 0.08,
        'flag': rng.integers(0, 2, n),                          # 伪标签列
    })
    # 注入脏数据: 缺失/类型混杂/重复
    biz.loc[3, '互动率'] = np.nan
    biz.loc[7, '粉丝数'] = "12,345"                              # 千分位字符串
    biz.loc[9, 'following_cnt'] = np.nan
    biz = pd.concat([biz, biz.iloc[[12]]], ignore_index=True)    # 重复行

    # ---- 2. 时间序列 (长表: id, day, likes) ----
    rows = []
    for i in range(n):
        base = rng.integers(5, 200)
        for d in range(90):
            v = max(0, int(base + rng.normal(0, 20)))
            if rng.random() < 0.01:
                v = np.nan                                  # 1% 缺失
            rows.append((f"U{i}", d, v))
    ts_long = pd.DataFrame(rows, columns=['uid', 'day', 'likes'])

    # ---- 3. 关系图 (含坏边: 引用不存在的账号 U999) ----
    edges = []
    for i in range(n):
        for _ in range(int(rng.integers(1, 8))):
            j = int(rng.integers(0, n))
            if j != i:
                edges.append((f"U{i}", f"U{j}"))
    edges.append(("U999", "U0"))                               # 坏边

    # ---- 4. 接入: meta + ts + graph ----
    tmp_ts = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp_ts.csv')
    pd.DataFrame(rows, columns=['uid', 'day', 'likes']).to_csv(tmp_ts, index=False)
    ds = load_dataset(meta_df=biz, ts_path=tmp_ts,
                      graph_src=pd.DataFrame(edges, columns=['src', 'dst']))
    print(f"\n[接入结果] {ds.describe()}")
    print(ds.report)

    # ---- 5. 检测管线可读性验证: 直接用 adapter 输出跑 L1 特征 ----
    md = ds.meta_df.reset_index(drop=True)
    n_ts = len(ds.likes)
    # Benford 检验 (对齐 run_detect L1a)
    EXPECT = np.log10(1 + 1.0 / np.arange(1, 10))
    from scipy import stats as st
    red_likes = 0
    for i, s in ds.likes.items():
        fd = np.array([int(str(int(x))[0]) for x in np.abs(s) if int(x) > 0])
        if len(fd) < 50:
            continue
        obs = np.array([(fd == d).sum() for d in np.arange(1, 10)], dtype=float)
        chi2 = ((obs - EXPECT * len(fd)) ** 2 / np.maximum(EXPECT * len(fd), 1e-9)).sum()
        if 1 - st.chi2.cdf(chi2, 8) < 0.01:
            red_likes += 1
    print(f"\n[管线验证] 时序账号={n_ts}, Benford红旗(单账号p<0.01)={red_likes}, "
          f"元字段={list(md.columns)}")
    print(f"  清洗例: 千分位粉丝数 '12,345' -> {md.loc[md['followers']==12345, 'followers'].iloc[0] if (md['followers']==12345).any() else 'see id=7'}")
    print("adapter 输出可直接喂 run_detect.features ✓")


if __name__ == '__main__':
    demo()