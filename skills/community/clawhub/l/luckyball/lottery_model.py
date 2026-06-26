# -*- coding: utf-8 -*-
"""
双色球预测模型 v3.0
改进:
  1. 蓝球 AR(1) 均值回归模型 — 利用历史自相关 r≈-0.72
  2. 红球 pointwise 排序 — 单分类器 + 号码特征, 对 33 个球打分取 Top-6
  3. 增强特征: 十神、地支藏干、纳音、节气距离
  4. 滚动回测框架 — walk-forward 评估真实命中率
"""

import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 基础常量
# =============================================================================

TIAN_GAN  = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DI_ZHI    = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
TG_WX     = ['木', '木', '火', '火', '土', '土', '金', '金', '水', '水']  # 天干五行
TG_YY     = ['阳','阴','阳','阴','阳','阴','阳','阴','阳','阴']          # 天干阴阳
DZ_WX     = ['水','土','木','木','土','火','火','土','金','金','土','水'] # 地支五行
DZ_YY     = ['阳','阴','阳','阴','阳','阴','阳','阴','阳','阴','阳','阴']
WX_ORDER  = {'木':0, '火':1, '土':2, '金':3, '水':4}

# ---------------------------------------------------------------------------
# 地支藏干 (index 是 天干 0-9)
# ---------------------------------------------------------------------------
DZ_CANG_GAN = {
    0:  [9],           # 子: 癸
    1:  [5, 9, 7],     # 丑: 己 癸 辛
    2:  [0, 2, 4],     # 寅: 甲 丙 戊
    3:  [1],           # 卯: 乙
    4:  [4, 1, 9],     # 辰: 戊 乙 癸
    5:  [2, 6, 4],     # 巳: 丙 庚 戊
    6:  [3, 5],        # 午: 丁 己
    7:  [5, 3, 1],     # 未: 己 丁 乙
    8:  [6, 8, 4],     # 申: 庚 壬 戊
    9:  [7],           # 酉: 辛
    10: [4, 7, 3],     # 戌: 戊 辛 丁
    11: [8, 0],        # 亥: 壬 甲
}

# ---------------------------------------------------------------------------
# 纳音五行 (60 甲子 → 纳音五行 index: 0木1火2土3金4水)
# 每连续两个甲子共享同一纳音
# ---------------------------------------------------------------------------
_NAYIN_30 = [3,1,0,2, 3,1,4,2, 3,0,4,2, 1,0,4, 3,1,0,2, 3,1,4,2, 3,0,4,2, 1,0,4]
#          金火木土 金火水土 金木水土 火木水 金火木土 金火水土 金木水土 火木水
WX_IDX = {'木':0, '火':1, '土':2, '金':3, '水':4}

def _make_nayin_map():
    """生成 (gan, zhi) → na_yin_wuxing_idx 映射"""
    m = {}
    for i in range(60):
        gan = i % 10
        zhi = i % 12
        m[(gan, zhi)] = _NAYIN_30[i // 2]
    return m

NAYIN_MAP = _make_nayin_map()

# ---------------------------------------------------------------------------
# 节气 (day-of-year, 近似)
# ---------------------------------------------------------------------------
SOLAR_TERMS_DOY = [
    35, 50, 65, 80, 95, 110, 125, 141, 157, 172, 188, 204,
    219, 235, 251, 266, 281, 296, 311, 326, 341, 356, 370, 385
]
# 立春 雨水 惊蛰 春分 清明 谷雨 立夏 小满 芒种 夏至 小暑 大暑
# 立秋 处暑 白露 秋分 寒露 霜降 立冬 小雪 大雪 冬至 小寒 大寒

# =============================================================================
# 八字 & 特征提取
# =============================================================================

def calc_jdn(year, month, day):
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365*y + y//4 - y//100 + y//400 - 32045


def get_bazi(date_val, hour=21):
    """计算八字, 返回 0-indexed gan/zhi"""
    if hasattr(date_val, 'year'):
        year, month, day = date_val.year, date_val.month, date_val.day
    else:
        dt = datetime.strptime(str(date_val), '%Y-%m-%d')
        year, month, day = dt.year, dt.month, dt.day

    year_gan = (year - 3) % 10 or 10
    year_zhi = (year - 3) % 12 or 12
    month_gan = (year % 10 + month * 2) % 10 or 10
    month_zhi = (month + 2) % 12 or 12
    jdn = calc_jdn(year, month, day)
    day_gan = (jdn + 6) % 10 or 10
    day_zhi = (jdn + 6) % 12 or 12
    hour_zhi = (hour // 2 + 1) % 12 or 12
    hour_gan = (day_gan * 2 + hour_zhi - 1) % 10 or 10

    return {
        'nianzhu_gan': year_gan - 1,  'nianzhu_zhi': year_zhi - 1,
        'yuezhu_gan':  month_gan - 1, 'yuezhu_zhi':  month_zhi - 1,
        'rizhu_gan':   day_gan - 1,   'rizhu_zhi':   day_zhi - 1,
        'shizhu_gan':  hour_gan - 1,  'shizhu_zhi':  hour_zhi - 1,
    }


def calc_wuxing(bazi):
    """天干+地支主气五行计数"""
    wx = {'木':0, '火':0, '土':0, '金':0, '水':0}
    for k in ['nianzhu_gan','yuezhu_gan','rizhu_gan','shizhu_gan']:
        wx[TG_WX[bazi[k]]] += 1
    for k in ['nianzhu_zhi','yuezhu_zhi','rizhu_zhi','shizhu_zhi']:
        wx[DZ_WX[bazi[k]]] += 1
    return wx


def calc_canggan_wuxing(bazi):
    """地支藏干五行计数 (更深层的五行信息)"""
    wx = {'木':0, '火':0, '土':0, '金':0, '水':0}
    for k in ['nianzhu_zhi','yuezhu_zhi','rizhu_zhi','shizhu_zhi']:
        for gan in DZ_CANG_GAN[bazi[k]]:
            wx[TG_WX[gan]] += 1
    return wx


def get_shishen(day_gan_idx, other_gan_idx):
    """计算十神关系: 0比肩 1劫财 2食神 3伤官 4偏财 5正财 6七杀 7正官 8偏印 9正印"""
    de = TG_WX[day_gan_idx]     # 日干五行
    oe = TG_WX[other_gan_idx]   # 他干五行
    same_yy = TG_YY[day_gan_idx] == TG_YY[other_gan_idx]

    di = WX_ORDER[de]
    oi = WX_ORDER[oe]

    if di == oi:            # 同我
        return 0 if same_yy else 1        # 比肩 / 劫财
    if (di + 1) % 5 == oi:  # 我生
        return 2 if same_yy else 3        # 食神 / 伤官
    if (di + 2) % 5 == oi:  # 我克
        return 4 if same_yy else 5        # 偏财 / 正财
    if (di + 3) % 5 == oi:  # 克我
        return 6 if same_yy else 7        # 七杀 / 正官
    # 生我
    return 8 if same_yy else 9            # 偏印 / 正印


def get_nayin_wuxing(gan_idx, zhi_idx):
    """获取某个干支组合的纳音五行 index (0-4)"""
    return NAYIN_MAP.get((gan_idx, zhi_idx), 2)


def solar_term_distance(doy):
    """距离最近节气的天数 (正=已过, 负=未到), 归一化到 [-15, 15]"""
    best = 999
    for term_doy in SOLAR_TERMS_DOY:
        d = doy - term_doy
        if abs(d) < abs(best):
            best = d
        # 也考虑跨年情况
        for offset in [-365, 365]:
            d2 = doy - (term_doy + offset)
            if abs(d2) < abs(best):
                best = d2
    return best


def extract_features_enhanced(date_val, hour=21):
    """提取增强版特征 (v3.0)"""
    bazi = get_bazi(date_val, hour)
    wx = calc_wuxing(bazi)
    cg_wx = calc_canggan_wuxing(bazi)

    if hasattr(date_val, 'year'):
        dt = date_val
    else:
        dt = datetime.strptime(str(date_val), '%Y-%m-%d')

    doy = dt.timetuple().tm_yday
    day_gan = bazi['rizhu_gan']

    feat = {
        # --- 日期 ---
        'year': dt.year, 'month': dt.month, 'day': dt.day,
        'weekday': dt.weekday() if hasattr(dt, 'weekday') else pd.Timestamp(dt).dayofweek,
        'day_of_year': doy,
        'solar_term_dist': solar_term_distance(doy),

        # --- 天干 ---
        'nianzhu_gan': bazi['nianzhu_gan'], 'yuezhu_gan': bazi['yuezhu_gan'],
        'rizhu_gan': day_gan, 'shizhu_gan': bazi['shizhu_gan'],

        # --- 地支 ---
        'nianzhu_zhi': bazi['nianzhu_zhi'], 'yuezhu_zhi': bazi['yuezhu_zhi'],
        'rizhu_zhi': bazi['rizhu_zhi'], 'shizhu_zhi': bazi['shizhu_zhi'],

        # --- 五行主气 ---
        'mu': wx['木'], 'huo': wx['火'], 'tu': wx['土'], 'jin': wx['金'], 'shui': wx['水'],

        # --- 五行藏干 ---
        'cg_mu': cg_wx['木'], 'cg_huo': cg_wx['火'], 'cg_tu': cg_wx['土'],
        'cg_jin': cg_wx['金'], 'cg_shui': cg_wx['水'],

        # --- 纳音 (四柱) ---
        'nayin_nian': get_nayin_wuxing(bazi['nianzhu_gan'], bazi['nianzhu_zhi']),
        'nayin_yue':  get_nayin_wuxing(bazi['yuezhu_gan'],  bazi['yuezhu_zhi']),
        'nayin_ri':   get_nayin_wuxing(bazi['rizhu_gan'],   bazi['rizhu_zhi']),
        'nayin_shi':  get_nayin_wuxing(bazi['shizhu_gan'],  bazi['shizhu_zhi']),

        # --- 十神 (年/月/时干 对 日干的关系) ---
        'shishen_nian': get_shishen(day_gan, bazi['nianzhu_gan']),
        'shishen_yue':  get_shishen(day_gan, bazi['yuezhu_gan']),
        'shishen_shi':  get_shishen(day_gan, bazi['shizhu_gan']),

        # --- 阴阳标记 ---
        'nianzhu_yy': 0 if TG_YY[bazi['nianzhu_gan']] == '阳' else 1,
        'rizhu_yy':   0 if TG_YY[bazi['rizhu_gan']]   == '阳' else 1,
    }
    return feat, bazi, wx


# =============================================================================
# 号码特征 (用于 pointwise 排序)
# =============================================================================

def _number_tiangan(n):
    """号码 1-33 的天干序号 (0-9)"""
    return (n - 1) % 10


def _number_dizhi(n):
    """号码 1-33 的地支序号 (0-11)"""
    return (n - 1) % 12


def _number_wuxing(n):
    """号码的天干五行 index"""
    return WX_ORDER[TG_WX[_number_tiangan(n)]]


def number_features(n):
    """返回单个号码的属性向量 — 仅保留与八字可交互的相对特征, 不含原始数值"""
    return [
        _number_tiangan(n),         # 天干 0-9
        _number_dizhi(n),           # 地支 0-11
        _number_wuxing(n),          # 五行 0-4
        n % 2,                      # 奇偶
    ]


# =============================================================================
# 蓝球 AR(1) 均值回归模型
# =============================================================================

class BlueBallAR:
    """蓝球 AR(1) 模型: blue_t = mu + phi * (blue_{t-1} - mu)"""

    def __init__(self):
        self.mu = None      # 长期均值
        self.phi = None     # 自回归系数
        self.sigma = None   # 残差标准差

    def fit(self, blue_series):
        """拟合 AR(1), blue_series: list/array of blue ball values (1-16)"""
        y = np.array(blue_series, dtype=float)
        self.mu = np.mean(y)
        y_lag = y[:-1]
        y_cur = y[1:]
        # OLS: (y_cur - mu) = phi * (y_lag - mu)
        dy_lag = y_lag - self.mu
        dy_cur = y_cur - self.mu
        if np.var(dy_lag) > 1e-6:
            self.phi = np.dot(dy_cur, dy_lag) / np.dot(dy_lag, dy_lag)
        else:
            self.phi = 0.0
        self.sigma = np.std(dy_cur - self.phi * dy_lag)
        return self

    def predict(self, last_blue):
        """预测下一期蓝球 (连续值)"""
        if self.mu is None:
            return 8.5
        pred = self.mu + self.phi * (last_blue - self.mu)
        return np.clip(pred, 1, 16)

    def predict_discrete(self, last_blue):
        """预测下一期蓝球 (离散 1-16, 四舍五入)"""
        return int(round(self.predict(last_blue)))


# =============================================================================
# 主模型 v3.0
# =============================================================================

class LotteryModelV3:
    """双色球预测模型 v3.0"""

    def __init__(self):
        self.df_history = None
        self.feature_cols_base = [
            'year', 'month', 'day', 'weekday', 'day_of_year', 'solar_term_dist',
            'nianzhu_gan', 'nianzhu_zhi', 'yuezhu_gan', 'yuezhu_zhi',
            'rizhu_gan', 'rizhu_zhi', 'shizhu_gan', 'shizhu_zhi',
            'mu', 'huo', 'tu', 'jin', 'shui',
            'cg_mu', 'cg_huo', 'cg_tu', 'cg_jin', 'cg_shui',
            'nayin_nian', 'nayin_yue', 'nayin_ri', 'nayin_shi',
            'shishen_nian', 'shishen_yue', 'shishen_shi',
            'nianzhu_yy', 'rizhu_yy',
        ]
        # 排序模型特征 = 基础特征 + 号码特征
        self.feature_cols_rank = self.feature_cols_base + [
            'num_gan', 'num_zhi', 'num_wx', 'num_parity'
        ]
        self.model_red = None       # 红球排序分类器
        self.model_blue_rf = None   # 蓝球 RF 回归器
        self.model_blue_ar = None   # 蓝球 AR(1)
        self.backtest_results = None

    # ------------------------------------------------------------------
    # 数据加载
    # ------------------------------------------------------------------

    def load_history(self, filepath):
        df = pd.read_excel(filepath)
        df.columns = ['qi', 'date', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'blue']
        self.df_history = df

    # ------------------------------------------------------------------
    # 构建排序训练数据
    # ------------------------------------------------------------------

    def _build_rank_data(self, df):
        """为每期历史的每个号码(1-33)构建一行, label=1 表示开出"""
        rows = []
        labels = []
        for _, row in df.iterrows():
            feat, _, _ = extract_features_enhanced(row['date'])
            drawn = set([int(row['r1']), int(row['r2']), int(row['r3']),
                         int(row['r4']), int(row['r5']), int(row['r6'])])
            for n in range(1, 34):
                nf = number_features(n)
                x = [feat[c] for c in self.feature_cols_base] + nf
                rows.append(x)
                labels.append(1 if n in drawn else 0)
        return np.array(rows), np.array(labels)

    # ------------------------------------------------------------------
    # 训练
    # ------------------------------------------------------------------

    def train(self):
        if self.df_history is None:
            raise ValueError('Please load history data first')

        df = self.df_history

        # ---- 红球排序模型 ----
        X_rank, y_rank = self._build_rank_data(df)
        self.model_red = RandomForestClassifier(
            n_estimators=300, max_depth=10, min_samples_leaf=20,
            class_weight='balanced', random_state=42, n_jobs=-1
        )
        self.model_red.fit(X_rank, y_rank)

        # ---- 蓝球 RF 模型 ----
        records = []
        for _, row in df.iterrows():
            feat, _, _ = extract_features_enhanced(row['date'])
            feat['blue'] = row['blue']
            records.append(feat)
        df_blue = pd.DataFrame(records)
        Xb = df_blue[self.feature_cols_base].values
        yb = df_blue['blue'].values

        self.model_blue_rf = RandomForestRegressor(
            n_estimators=200, max_depth=8, min_samples_split=5, random_state=42
        )
        self.model_blue_rf.fit(Xb, yb)

        # ---- 蓝球 AR(1) 模型 ----
        blue_series = df['blue'].values
        self.model_blue_ar = BlueBallAR()
        self.model_blue_ar.fit(blue_series)

        print(f'[v3.0] Trained on {len(df)} periods')
        print(f'  Red rank model: {X_rank.shape[0]} samples, {y_rank.sum():.0f} positive')
        print(f'  Blue AR(1): mu={self.model_blue_ar.mu:.2f}, phi={self.model_blue_ar.phi:.4f}')
        return self

    # ------------------------------------------------------------------
    # 回测
    # ------------------------------------------------------------------

    def backtest(self, start_period=60):
        """Walk-forward 回测: 从第 start_period 期开始, 逐期预测并比对"""
        df = self.df_history
        results = []

        for i in range(start_period, len(df)):
            train_df = df.iloc[:i]
            test_row = df.iloc[i]

            # 训练子模型
            sub = LotteryModelV3()
            sub.df_history = train_df

            Xr, yr = sub._build_rank_data(train_df)
            sub.model_red = RandomForestClassifier(
                n_estimators=200, max_depth=8, min_samples_leaf=20,
                class_weight='balanced', random_state=42, n_jobs=-1
            )
            sub.model_red.fit(Xr, yr)

            # 蓝球 RF
            tf_records = []
            for _, tr in train_df.iterrows():
                f, _, _ = extract_features_enhanced(tr['date'])
                f['blue'] = tr['blue']
                tf_records.append(f)
            tf = pd.DataFrame(tf_records)
            sub.model_blue_rf = RandomForestRegressor(
                n_estimators=100, max_depth=6, random_state=42
            )
            sub.model_blue_rf.fit(
                tf[sub.feature_cols_base].values, tf['blue'].values
            )

            # 蓝球 AR
            sub.model_blue_ar = BlueBallAR()
            sub.model_blue_ar.fit(train_df['blue'].values)

            # 预测
            pred = sub.predict(test_row['date'])

            # 比对
            actual_red = set([int(test_row['r1']), int(test_row['r2']), int(test_row['r3']),
                              int(test_row['r4']), int(test_row['r5']), int(test_row['r6'])])
            actual_blue = int(test_row['blue'])
            hit_red = len(set(pred['pred_red']) & actual_red)
            hit_blue = 1 if pred['pred_blue'] == actual_blue else 0

            results.append({
                'qi': test_row['qi'],
                'date': test_row['date'],
                'pred_red': pred['pred_red'],
                'pred_blue': pred['pred_blue'],
                'actual_red': sorted(actual_red),
                'actual_blue': actual_blue,
                'hit_red': hit_red,
                'hit_blue': hit_blue,
            })

        self.backtest_results = results
        return results

    def backtest_summary(self):
        """回测摘要统计"""
        if not self.backtest_results:
            print('No backtest results. Run .backtest() first.')
            return

        n = len(self.backtest_results)
        red_hits = [r['hit_red'] for r in self.backtest_results]
        blue_hits = [r['hit_blue'] for r in self.backtest_results]

        # 理论期望: P(k) = C(6,k)*C(27,6-k)/C(33,6)
        from math import comb
        expected_red = sum(k * comb(6,k)*comb(27,6-k)/comb(33,6) for k in range(7))
        expected_blue = 1/16

        print(f'===== 回测摘要 (n={n}) =====')
        print(f'  红球平均命中: {np.mean(red_hits):.3f}  (随机期望: {expected_red:.3f})')
        print(f'  红球 ≥3 命中率: {sum(1 for h in red_hits if h>=3)/n*100:.1f}%')
        print(f'  蓝球命中率:    {np.mean(blue_hits)*100:.1f}%  (随机期望: {expected_blue*100:.1f}%)')
        print(f'  蓝球 AR phi:    {self.model_blue_ar.phi:.4f}')

        # 最近 20 期
        recent = red_hits[-20:]
        print(f'  最近20期红球均值: {np.mean(recent):.3f}')

        return {
            'n': n, 'mean_red': np.mean(red_hits), 'mean_blue': np.mean(blue_hits),
            'expected_red': expected_red, 'expected_blue': expected_blue,
            'red_ge3_pct': sum(1 for h in red_hits if h>=3)/n*100,
        }

    # ------------------------------------------------------------------
    # 预测
    # ------------------------------------------------------------------

    def _predict_red_score(self, date_val, hour=21):
        """对 33 个红球打分, 返回 [(号码, 得分), ...] 降序"""
        feat, _, _ = extract_features_enhanced(date_val, hour)
        base = [feat[c] for c in self.feature_cols_base]
        scores = []
        for n in range(1, 34):
            nf = number_features(n)
            x = np.array([base + nf])
            prob = self.model_red.predict_proba(x)[0][1]
            scores.append((n, prob))
        scores.sort(key=lambda t: t[1], reverse=True)
        return scores

    def predict(self, date_val, hour=21):
        """单次预测"""
        feat, bazi, wx = extract_features_enhanced(date_val, hour)
        Xb = np.array([[feat[c] for c in self.feature_cols_base]])

        # 红球: Top-6 排序分数
        scores = self._predict_red_score(date_val, hour)
        red_top6 = sorted([n for n, _ in scores[:6]])

        # 蓝球: RF + AR 加权
        blue_rf = self.model_blue_rf.predict(Xb)[0]
        if len(self.df_history) > 0:
            last_blue = self.df_history['blue'].iloc[-1]
        else:
            last_blue = 8
        blue_ar = self.model_blue_ar.predict(last_blue)
        # 权重: AR 占 60% (因为有统计信号), RF 占 40%
        blue_ens = 0.4 * blue_rf + 0.6 * blue_ar
        blue_ens = max(1, min(16, int(round(float(blue_ens)))))

        return {
            'date': date_val,
            'bazi': bazi,
            'wuxing': wx,
            'features': feat,
            'pred_red': red_top6,
            'pred_blue': blue_ens,
            'red_scores': scores[:12],  # Top 12 供参考
            'blue_rf': blue_rf,
            'blue_ar': blue_ar,
        }

    def predict_multi(self, date_val, hour=21, n=5):
        """多组预测 (结合排序采样)"""
        base = self.predict(date_val, hour)
        results = [base]

        scores = base['red_scores']
        # 对 Top-20 号码按概率采样生成变体
        top20 = [num for num, _ in scores[:20]]

        for i in range(1, n):
            # 使用带噪声的分数采样
            noisy_scores = []
            for num, prob in scores:
                noisy_scores.append((num, prob + np.random.normal(0, 0.02)))
            noisy_scores.sort(key=lambda t: t[1], reverse=True)
            red = sorted([num for num, _ in noisy_scores[:6]])

            # 蓝球变体: 在 ensemble 附近扰动
            b = base['pred_blue'] + np.random.choice([-2, -1, 0, 1, 2])
            b = max(1, min(16, int(b)))

            results.append({
                'date': date_val,
                'index': i + 1,
                'pred_red': red,
                'pred_blue': b,
            })

        return results, base

    # ------------------------------------------------------------------
    # 辅助
    # ------------------------------------------------------------------

    def get_feature_importance(self, top_n=15):
        """红球排序模型的特征重要性"""
        if self.model_red is None:
            print('Model not trained.')
            return []
        imp = self.model_red.feature_importances_
        idx = np.argsort(imp)[::-1]
        return [(self.feature_cols_rank[i], imp[i]) for i in idx[:top_n]]

    @property
    def blue_ar_phi(self):
        if self.model_blue_ar:
            return self.model_blue_ar.phi
        return None


# =============================================================================
# 主程序
# =============================================================================

if __name__ == '__main__':
    print('=' * 60)
    print('双色球预测模型 v3.0')
    print('蓝球AR(1) + 红球Pointwise排序 + 增强特征 + 回测')
    print('=' * 60)

    model = LotteryModelV3()
    model.load_history(r'C:\Users\a\luspace\双色球200期号码.xlsx')
    model.train()

    # 特征重要性
    print('\n【特征重要性 Top-10】')
    for feat, imp in model.get_feature_importance(10):
        print(f'  {feat}: {imp:.4f}')

    # 回测
    print('\n【滚动回测】')
    model.backtest(start_period=60)
    model.backtest_summary()

    # 预测下一期
    print('\n' + '=' * 60)
    target = datetime(2026, 6, 4)
    result = model.predict(target, hour=21)
    print(f'预测日期: {target.strftime("%Y-%m-%d")}')
    print(f'推荐红球: {result["pred_red"]}')
    print(f'推荐蓝球: {result["pred_blue"]}  (RF={result["blue_rf"]:.1f}, AR={result["blue_ar"]:.1f})')

    print('\n红球 Top-12 得分:')
    for n, s in result['red_scores']:
        bar = '█' * int(s * 200)
        print(f'  {n:2d}: {s:.4f} {bar}')

    print('\n*** 纯娱乐预测, 请理性购彩! ***')
