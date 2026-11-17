# -*- coding: utf-8 -*-
"""
L1 统计规则引擎 (参数化版)
============================
把 run_detect.py 中硬编码的 L1 规则提取为可配置引擎, 支持:
  1) 阈值参数化: 默认值 = 原硬编码基线 (回归无损), 可由 train_l1_thresholds.py 重训覆盖
  2) 互惠率规则插槽: P1 建议的 rec>=th 且度>=min_deg -> 红旗 (需图数据, 无图自动降级)
  3) 无标注回退: 关注比分位数在无正常账号标注时用全量分位数

规则集 (与 run_detect.py L1a-L1d 对齐, +L1e 互惠率, +HF-R1 L1f-L1i 可选增强):
  L1a Benford chi2:   benford_p < benford_alpha
  L1b ER 分档:        er < er_low | er > er_high
  L1c 增长导数:       spike_ratio > spike_ratio_th | spike_cnt >= spike_cnt_th
  L1d 关注比:         log_fr 超出正常[lo_q, hi_q]分位
  L1e 互惠率:         recip >= recip_th 且 (in_deg+out_deg) >= recip_min_deg   (P1 新增, 图可用时)
  L1f 活跃时段熵:     hour_entropy < hour_entropy_th   (HF-R1, 默认关闭; 需 timing 直方图)
  L1g 节奏规律:       rhythm_cv < rhythm_cv_th         (HF-R1, 默认关闭; likes 差分 CV)
  L1h 内容模板化:     tpl_ngram >= tpl_ngram_th        (HF-R1, 默认关闭; 需 template_similarity)
  L1i 粉丝质量回灌:   follower_quality < fq_low_th     (HF-R1, 默认关闭; follower_quality/zombie 派生)
聚合判定: n_flags >= n_flags_th -> 红旗 (水军)

HF-R1 说明: L1f-L1i 四条规则**默认关闭** (enabled=False)，仅扩展特征列与规则骨架，
不改既有 n_flags 聚合结果 -> 零回归；待真实样本校准 (train_l1_thresholds) 后按需开启。
"""
import numpy as np
import pandas as pd
from scipy import stats

EXPECT = np.log10(1 + 1.0 / np.arange(1, 10))

# ---- 默认阈值: 与 run_detect.py 原硬编码基线完全一致 (回归无损) ----
DEFAULT_THRESHOLDS = {
    'benford_alpha': 0.01,      # L1a Benford p 值阈值
    'er_low': 1e-4,             # L1b ER 下界
    'er_high': 0.05,            # L1b ER 上界
    'spike_ratio_th': 20.0,     # L1c 增长峰值/中位 阈值
    'spike_cnt_th': 3,          # L1c 尖峰天数阈值
    'fr_lo_q': 5,               # L1d 关注比低分位
    'fr_hi_q': 95,              # L1d 关注比高分位
    'n_flags_th': 2,            # 聚合: 红旗数阈值
    'recip_th': 0.5,            # L1e 互惠率阈值 (P1 建议)
    'recip_min_deg': 3,         # L1e 最小度 (入+出)
    'recip_enabled': True,      # L1e 开关 (图不可用时自动跳过)
    # ── HF-R1 新增规则 (默认关闭: 仅扩展字段+规则, 不动既有 n_flags 聚合 -> 零回归) ──
    'hour_entropy_th': 0.35,    # L1f 活跃时段熵下界 (< th -> 时段过集中, 疑似脚本)
    'rhythm_cv_th': 0.15,       # L1g 节奏变异系数上界 (< th -> 间隔极规律)
    'tpl_ngram_th': 0.72,       # L1h 内容模板化 n-gram 相似度上界 (>= th -> 套模板)
    'fq_low_th': 0.35,          # L1i 粉丝质量下界 (< th -> 僵尸粉占比高)
    'hour_entropy_enabled': False,   # L1f 开关 (HF-R1 默认关, 校准后按需开)
    'rhythm_enabled': False,         # L1g 开关
    'tpl_enabled': False,            # L1h 开关
    'fq_enabled': False,             # L1i 开关
}


def benford_pval(likes_series):
    """单账号每日点赞数首位 Benford chi2 p 值 (样本<50 返回 1.0 不判)"""
    s = np.abs(np.asarray(likes_series, dtype=float))
    fd = np.array([int(str(int(x))[0]) for x in s if int(x) > 0])
    if len(fd) < 50:
        return 1.0
    obs = np.array([(fd == d).sum() for d in np.arange(1, 10)], dtype=float)
    exp = EXPECT * len(fd)
    chi2 = ((obs - exp) ** 2 / np.maximum(exp, 1e-9)).sum()
    return float(1 - stats.chi2.cdf(chi2, 8))


def spike_feats(g):
    """增长曲线尖峰特征: (峰值/中位比, 尖峰天数)"""
    g = np.asarray(g, dtype=float)
    if g.size == 0:
        return 0.0, 0        # 无时序信号 -> 不触发 (空数组守卫, 非空行为不变)
    med = float(np.median(g)) + 1.0
    ratio = float(np.max(g) / med)
    thr = float(np.mean(g) + 3 * np.std(g))
    cnt = int((g > max(thr, 10)).sum())
    return ratio, cnt


def hour_entropy(hist):
    """活跃时段熵 (归一化 0-1): 24 时段活跃分布的不确定性。

    hist: 24 维活跃直方图 (来自 timing 数据)。分布越均匀 -> 越接近 1；
    时段越集中 (疑似脚本) -> 越接近 0。无有效直方图 -> 返回 1.0 (不触发)。
    """
    h = np.asarray(hist, dtype=float) if hist is not None else np.asarray([], dtype=float)
    h = h[h > 0]
    n = len(h)
    if n < 2:
        return 1.0
    p = h / h.sum()
    return float(-(p * np.log(p)).sum() / np.log(n))


def rhythm_cv(series):
    """节奏变异系数: 相邻值差分序列的 CV (std/mean)。

    发布/互动节奏越规律 -> CV 越小 (疑似定时/定量)。样本不足 -> 1.0 (不触发)。
    """
    s = np.asarray(series, dtype=float)
    if s.size < 3:
        return 1.0
    d = np.abs(np.diff(s))
    m = float(np.mean(d))
    if m <= 1e-9:
        return 0.0
    return float(np.std(d) / m)


def compute_l1_features(meta_df, likes, growth, G=None, timing=None):
    """
    计算全部 L1 特征, 返回带列的新 DataFrame (不修改入参):
      benford_p / er / spike_ratio / spike_cnt / log_fr
      recip / recip_deg / deg_in / deg_out   (G 可用时; 否则 0, 规则自动降级)
      hour_entropy / rhythm_cv / tpl_ngram / follower_quality   (HF-R1 新增; 恒计算为零成本纯特征)

    timing: {id: 24维活跃直方图} 可选 (HF-P0 ④), 缺失则该列返回 1.0 (不触发)。
    """
    df = meta_df.copy()
    # L1a Benford（时序缺失账号按不判处理）
    df['benford_p'] = [benford_pval(likes.get(i, [])) for i in df.index]
    # L1b ER
    df['er'] = df['er'].astype(float)
    # L1c 增长导数（序列缺失 -> 0/0 不触发）
    sr, sc = [], []
    for i in df.index:
        r_, c_ = spike_feats(growth.get(i, []))
        sr.append(r_)
        sc.append(c_)
    df['spike_ratio'] = sr
    df['spike_cnt'] = sc
    # L1d 关注比
    df['log_fr'] = np.log10((df['followers'].astype(float) + 1.0) /
                            (df['following'].astype(float) + 1.0))
    # L1e 互惠率 (P1: 双向关注比, 方向信号; 无图 -> 全 0 自动降级)
    df['recip'] = 0.0
    df['recip_deg'] = 0
    df['deg_in'] = 0
    df['deg_out'] = 0
    if G is not None:
        pred, succ = G.predecessors, G.successors
        for n in df.index:
            if n not in G:
                continue
            inb = set(pred(n))
            outb = set(succ(n))
            df.at[n, 'deg_in'] = len(inb)
            df.at[n, 'deg_out'] = len(outb)
            df.at[n, 'recip_deg'] = len(inb) + len(outb)
            df.at[n, 'recip'] = len(inb & outb) / max(len(inb | outb), 1)
    # ── HF-R1 新增特征 (零成本, 恒计算; 规则默认关闭故不影响既有判定) ──
    # L1f 活跃时段熵 (需 timing 24h 直方图; 缺失 -> 1.0 不触发)
    tmap = timing or {}
    df['hour_entropy'] = [hour_entropy(tmap.get(i) if tmap.get(i) is not None
                                       else tmap.get(str(i))) for i in df.index]
    # L1g 节奏变异系数 (likes 差分 CV; 无时序 -> 1.0)
    df['rhythm_cv'] = [rhythm_cv(likes.get(i, [])) for i in df.index]
    # L1h 内容模板化 n-gram 相似度 (meta 提供 template_similarity 时; 否则 0)
    if 'template_similarity' in df.columns:
        df['tpl_ngram'] = pd.to_numeric(df['template_similarity'], errors='coerce') \
            .fillna(0.0).clip(0.0, 1.0)
    else:
        df['tpl_ngram'] = 0.0
    # L1i 粉丝质量回灌 (follower_quality 优先, 否则 zombie_follower_ratio 取反; 缺省 0.5 中性)
    if 'follower_quality' in df.columns:
        df['follower_quality'] = pd.to_numeric(df['follower_quality'], errors='coerce') \
            .fillna(0.5).clip(0.0, 1.0)
    elif 'zombie_follower_ratio' in df.columns:
        _z = pd.to_numeric(df['zombie_follower_ratio'], errors='coerce').fillna(0.0).clip(0.0, 1.0)
        df['follower_quality'] = (1.0 - _z)
    else:
        df['follower_quality'] = 0.5
    return df


def apply_l1_rules(feats, thresholds=None, normal_mask=None):
    """
    按阈值聚合红旗, 返回 dict:
      benford / er / growth / fr / recip (各规则布尔)
      n_flags / pred (n_flags >= n_flags_th)
    normal_mask: 正常账号布尔, 用于关注比分位数 (None -> 全量分位数)
    """
    th = DEFAULT_THRESHOLDS.copy()
    if thresholds:
        th.update(thresholds)

    bp = feats['benford_p'].values < th['benford_alpha']
    er_red = ((feats['er'].values < th['er_low']) |
              (feats['er'].values > th['er_high']))
    gr = ((feats['spike_ratio'].values > th['spike_ratio_th']) |
          (feats['spike_cnt'].values >= th['spike_cnt_th']))

    fr = feats['log_fr'].values
    if normal_mask is not None and normal_mask.sum() > 0:
        q5, q95 = np.percentile(fr[normal_mask], [th['fr_lo_q'], th['fr_hi_q']])
    else:
        q5, q95 = np.percentile(fr, [th['fr_lo_q'], th['fr_hi_q']])
    fr_red = (fr < q5) | (fr > q95)

    # L1e 互惠率 (图可用且启用才生效; recip=0 且度=0 时天然不触发)
    rec_red = np.zeros(len(feats), dtype=bool)
    if th.get('recip_enabled', True):
        rec_red = ((feats['recip'].values >= th['recip_th']) &
                   (feats['recip_deg'].values >= th['recip_min_deg']))

    # ── HF-R1 新增规则 (默认关闭: enabled=False 时恒零向量, 不改变既有 n_flags -> 零回归) ──
    he_red = np.zeros(len(feats), dtype=bool)
    if th.get('hour_entropy_enabled', False) and 'hour_entropy' in feats.columns:
        he_red = feats['hour_entropy'].values < th['hour_entropy_th']
    rh_red = np.zeros(len(feats), dtype=bool)
    if th.get('rhythm_enabled', False) and 'rhythm_cv' in feats.columns:
        rh_red = feats['rhythm_cv'].values < th['rhythm_cv_th']
    tpl_red = np.zeros(len(feats), dtype=bool)
    if th.get('tpl_enabled', False) and 'tpl_ngram' in feats.columns:
        tpl_red = feats['tpl_ngram'].values >= th['tpl_ngram_th']
    fq_red = np.zeros(len(feats), dtype=bool)
    if th.get('fq_enabled', False) and 'follower_quality' in feats.columns:
        fq_red = feats['follower_quality'].values < th['fq_low_th']

    n_flags = (bp.astype(int) + er_red.astype(int) + gr.astype(int) +
               fr_red.astype(int) + rec_red.astype(int) +
               he_red.astype(int) + rh_red.astype(int) +
               tpl_red.astype(int) + fq_red.astype(int))
    pred = (n_flags >= th['n_flags_th']).astype(int)
    return dict(benford=bp, er=er_red, growth=gr, fr=fr_red, recip=rec_red,
                hour_entropy=he_red, rhythm=rh_red, tpl=tpl_red, follower_quality=fq_red,
                n_flags=n_flags, pred=pred)


def l1_rule_names():
    return ['benford', 'er', 'growth', 'fr', 'recip',
            'hour_entropy', 'rhythm', 'tpl', 'follower_quality']