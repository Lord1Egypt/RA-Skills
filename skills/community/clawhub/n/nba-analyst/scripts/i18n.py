"""
NBA 中英文映射模块
支持球队名、球员名、统计指标的中英互转
"""

import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


class I18N:
    def __init__(self):
        # 加载映射表
        self.teams_cn = self._load_json('teams_cn.json')
        self.players_cn = self._load_json('players_cn.json')
        self.stats_labels = self._load_json('stats_labels_cn.json')

        # 构建反向索引 (中文 → 英文)
        self.cn_to_en_player = {}
        for en, cn in self.players_cn.items():
            self.cn_to_en_player[cn] = en
            # 添加无连字符版
            cn_no_dash = cn.replace('-', '')
            self.cn_to_en_player[cn_no_dash] = en

        self.cn_to_en_team = {}
        for en, cn in self.teams_cn.items():
            self.cn_to_en_team[cn] = en

    def _load_json(self, filename):
        path = os.path.join(DATA_DIR, filename)
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # ==================== 球员名 ====================

    def player_en_to_cn(self, en_name: str) -> str:
        """英文球员名 → 中文"""
        return self.players_cn.get(en_name, en_name)

    def player_cn_to_en(self, cn_name: str) -> str:
        """中文球员名 → 英文"""
        # 精确匹配
        if cn_name in self.cn_to_en_player:
            return self.cn_to_en_player[cn_name]
        # 模糊匹配
        cn_lower = cn_name.lower().replace('-', '')
        for cn, en in self.cn_to_en_player.items():
            if cn_lower in cn.lower().replace('-', '') or cn.lower().replace('-', '') in cn_lower:
                return en
        return cn_name  # 返回原名

    def resolve_player_name(self, name: str) -> tuple:
        """智能解析球员名 → (english_name, chinese_name)"""
        # 是否包含中文字符
        if re.search(r'[\u4e00-\u9fff]', name):
            # 中文输入
            en = self.player_cn_to_en(name)
            cn = name
            return (en, self.player_en_to_cn(en) if en != name else name)
        else:
            # 英文输入或简写
            cn = self.player_en_to_cn(name)
            if cn != name:
                return (name, cn)
            return (name, name)

    # ==================== 球队名 ====================

    def team_en_to_cn(self, en_name: str) -> str:
        """英文球队名 → 中文"""
        return self.teams_cn.get(en_name, en_name)

    def team_cn_to_en(self, cn_name: str) -> str:
        """中文球队名 → 英文"""
        for en, cn in self.teams_cn.items():
            if cn_name in (cn, en):
                return en
        return cn_name

    def resolve_team_name(self, name: str) -> tuple:
        """智能解析球队名 → (english_name, chinese_name)"""
        if re.search(r'[\u4e00-\u9fff]', name):
            cn = name
            en = self.team_cn_to_en(name)
            return (en, cn)
        else:
            cn = self.team_en_to_cn(name)
            return (name, cn)

    # ==================== 统计指标 ====================

    def stat_label_cn(self, key: str) -> str:
        """统计指标 key → 中文标签"""
        label = self.stats_labels.get(key)
        if label:
            return label
        # Case-insensitive fallback
        for k, v in self.stats_labels.items():
            if k.lower() == key.lower():
                return v
        return key

    # ==================== 格式化 ====================

    def format_player_name(self, name: str, with_en: bool = False) -> str:
        """格式化球员名输出"""
        en, cn = self.resolve_player_name(name)
        if with_en and en != cn:
            return f"{cn} ({en})"
        return cn

    def format_team_name(self, name: str, with_en: bool = False) -> str:
        """格式化球队名输出"""
        en, cn = self.resolve_team_name(name)
        if with_en and en != cn:
            return f"{cn} ({en})"
        return cn

    def format_stat_value(self, key: str, value) -> str:
        """格式化统计数据"""
        label = self.stat_label_cn(key)
        if isinstance(value, float):
            return f"{label}: {value:.1f}"
        return f"{label}: {value}"

    def translate_dataframe_columns(self, df):
        """翻译 DataFrame 列名为中文"""
        if df is not None and hasattr(df, 'columns'):
            new_cols = [self.stat_label_cn(c) for c in df.columns]
            df.columns = new_cols
        return df
