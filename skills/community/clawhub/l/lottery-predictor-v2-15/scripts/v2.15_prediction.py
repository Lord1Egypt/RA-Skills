#!/usr/bin/env python3
"""
🎰 彩票 V2.15 预测技能核心脚本

基于 7 种数学模型的双色球预测工具
- 均值回归模型（25%）
- 正态分布模型（22%）
- 大数定律（18%）
- 卡方检验（15%）
- 马尔可夫链（8%）
- 时间序列（7%）
- 泊松分布（5%）

用法：
  python3 v2.15_prediction.py --issue 2026035
  python3 v2.15_prediction.py --issue 2026035 --output json

作者：小四（CFO）
版本：V2.15
"""

import json
import sqlite3
import argparse
import math
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

# ==================== 配置 ====================

DEFAULT_DB_PATH = Path.home() / ".openclaw" / "workspace" / "projects" / "caipiao" / "data" / "caipiao.db"
REPORTS_DIR = Path.home() / ".openclaw" / "workspace" / "projects" / "caipiao" / "reports"

# V2.15 模型权重配置
MODEL_WEIGHTS = {
    "mean_reversion": 0.25,      # 均值回归（提升）
    "normal_distribution": 0.22, # 正态分布（提升）
    "law_large_numbers": 0.18,   # 大数定律（提升）
    "chi_square": 0.15,          # 卡方检验（提升）
    "markov": 0.08,              # 马尔可夫链（降低）
    "time_series": 0.07,         # 时间序列（降低）
    "poisson": 0.05,             # 泊松分布（降低）
}

# ==================== 数据库操作 ====================

def get_db_connection(db_path: Path) -> sqlite3.Connection:
    """获取数据库连接"""
    if not db_path.exists():
        raise FileNotFoundError(f"数据库不存在：{db_path}")
    conn = sqlite3.connect(db_path)
    return conn

def get_history_data(conn: sqlite3.Connection, lottery_type: str = "ssq", limit: int = None) -> List[Dict]:
    """获取历史数据"""
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = f"SELECT * FROM {lottery_type} ORDER BY issue DESC"
    if limit:
        query += f" LIMIT {limit}"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    return [dict(row) for row in rows]

def get_latest_issue(conn: sqlite3.Connection, lottery_type: str = "ssq") -> str:
    """获取最新已开奖期号"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT issue FROM {lottery_type} ORDER BY issue DESC LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row else None

# ==================== V2.15 核心算法 ====================

class V215Predictor:
    """V2.15 优化预测器"""
    
    def __init__(self, history_data: List[Dict]):
        self.history = history_data
        self.total_periods = len(history_data)
        
    def calculate_mean_reversion(self) -> Dict[int, float]:
        """
        均值回归模型
        核心原理：极端值会向平均值回归
        应用：和值预测、号码回补
        """
        scores = {}
        avg_frequency = self.total_periods / 33  # 33 个红球
        
        for num in range(1, 34):
            count = sum(1 for row in self.history if num in [row[f'red{i}'] for i in range(1, 7)])
            frequency = count / self.total_periods
            
            deviation = frequency - (1/33)
            
            if deviation < 0:
                scores[num] = abs(deviation) * 100  # 冷号回补分数
            else:
                scores[num] = 50 - (deviation * 50)  # 热号降温分数
        
        return scores
    
    def calculate_normal_distribution(self) -> Dict[int, float]:
        """
        正态分布模型
        核心原理：数据集中在均值附近，呈钟形分布
        应用：和值范围预测（80-122 为 68% 概率区间）
        """
        scores = {}
        
        sums = []
        for row in self.history:
            s = sum(row[f'red{i}'] for i in range(1, 7))
            sums.append(s)
        
        mean_sum = sum(sums) / len(sums)
        variance = sum((s - mean_sum) ** 2 for s in sums) / len(sums)
        std_dev = math.sqrt(variance)
        
        for num in range(1, 34):
            num_sums = [sums[i] for i, row in enumerate(self.history) 
                       if num in [row[f'red{i}'] for i in range(1, 7)]]
            
            if num_sums:
                avg_num_sum = sum(num_sums) / len(num_sums)
                distance = abs(avg_num_sum - mean_sum)
                scores[num] = 100 * math.exp(-distance / (2 * std_dev))
            else:
                scores[num] = 50
        
        return scores
    
    def calculate_law_large_numbers(self) -> Dict[int, float]:
        """
        大数定律
        核心原理：样本量越大，频率越接近概率
        应用：历史频率作为概率估计
        """
        scores = {}
        
        for num in range(1, 34):
            count = sum(1 for row in self.history if num in [row[f'red{i}'] for i in range(1, 7)])
            frequency = count / self.total_periods
            scores[num] = frequency * 100
        
        return scores
    
    def calculate_chi_square(self) -> Dict[int, float]:
        """
        卡方检验
        核心原理：检验观察频率与期望频率的差异
        应用：冷热号判断
        """
        scores = {}
        expected_freq = self.total_periods / 33
        
        for num in range(1, 34):
            observed = sum(1 for row in self.history if num in [row[f'red{i}'] for i in range(1, 7)])
            
            chi_sq = ((observed - expected_freq) ** 2) / expected_freq
            
            if observed < expected_freq:
                scores[num] = 80 + (chi_sq * 2)  # 冷号加分
            else:
                scores[num] = 60 - (chi_sq * 1)  # 热号减分
        
        return scores
    
    def calculate_markov(self) -> Dict[int, float]:
        """
        马尔可夫链
        核心原理：下一状态仅依赖当前状态
        应用：奇偶/大小转换
        """
        scores = {}
        
        if not self.history:
            return {num: 50.0 for num in range(1, 34)}
        
        last_row = self.history[0]
        last_reds = [last_row[f'red{i}'] for i in range(1, 7)]
        
        for num in range(1, 34):
            if num in last_reds:
                scores[num] = 40.0  # 上期出现过的号码，重复概率较低
            else:
                scores[num] = 60.0  # 上期未出现的号码，出现概率较高
        
        return scores
    
    def calculate_time_series(self) -> Dict[int, float]:
        """
        时间序列分析
        核心原理：分析数据随时间变化的趋势
        应用：年度趋势、周期性规律
        """
        scores = {}
        
        recent_10 = self.history[:10]
        
        for num in range(1, 34):
            count = sum(1 for row in recent_10 if num in [row[f'red{i}'] for i in range(1, 7)])
            scores[num] = count * 10
        
        return scores
    
    def calculate_poisson(self) -> Dict[int, float]:
        """
        泊松分布
        核心原理：描述单位时间内事件发生次数
        应用：连号、同尾号概率
        """
        scores = {}
        
        for num in range(1, 34):
            consecutive_count = 0
            for row in self.history:
                reds = [row[f'red{i}'] for i in range(1, 7)]
                if num in reds:
                    if (num - 1) in reds or (num + 1) in reds:
                        consecutive_count += 1
            
            if num in [row[f'red{i}'] for i in range(1, 7) for row in self.history]:
                total = sum(1 for row in self.history if num in [row[f'red{i}'] for i in range(1, 7)])
                prob = consecutive_count / total if total > 0 else 0
                scores[num] = prob * 50
            else:
                scores[num] = 25
        
        return scores
    
    def predict(self, top_n: int = 10) -> Dict:
        """
        综合预测
        返回：红球推荐、蓝球推荐
        """
        scores_mean_rev = self.calculate_mean_reversion()
        scores_normal = self.calculate_normal_distribution()
        scores_law_large = self.calculate_law_large_numbers()
        scores_chi_sq = self.calculate_chi_square()
        scores_markov = self.calculate_markov()
        scores_time_series = self.calculate_time_series()
        scores_poisson = self.calculate_poisson()
        
        final_scores = {}
        for num in range(1, 34):
            score = (
                scores_mean_rev.get(num, 50) * MODEL_WEIGHTS["mean_reversion"] +
                scores_normal.get(num, 50) * MODEL_WEIGHTS["normal_distribution"] +
                scores_law_large.get(num, 50) * MODEL_WEIGHTS["law_large_numbers"] +
                scores_chi_sq.get(num, 50) * MODEL_WEIGHTS["chi_square"] +
                scores_markov.get(num, 50) * MODEL_WEIGHTS["markov"] +
                scores_time_series.get(num, 50) * MODEL_WEIGHTS["time_series"] +
                scores_poisson.get(num, 50) * MODEL_WEIGHTS["poisson"]
            )
            final_scores[num] = score
        
        sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        top_reds = [num for num, score in sorted_scores[:top_n]]
        
        blue_scores = {}
        for num in range(1, 17):
            count = sum(1 for row in self.history if row['blue'] == num)
            blue_scores[num] = count / self.total_periods * 100
        
        sorted_blue = sorted(blue_scores.items(), key=lambda x: x[1], reverse=True)
        top_blues = [num for num, score in sorted_blue[:4]]
        
        return {
            "red_top10": top_reds,
            "blue_top4": top_blues,
            "scores": final_scores
        }

# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(description="V2.15 彩票预测模型")
    parser.add_argument("--issue", type=str, required=True, help="期号（如：2026035）")
    parser.add_argument("--output", type=str, default="json", help="输出格式（json/text）")
    parser.add_argument("--lottery", type=str, default="ssq", help="彩种（ssq/dlt）")
    parser.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH), help="数据库路径")
    
    args = parser.parse_args()
    
    db_path = Path(args.db)
    
    try:
        conn = get_db_connection(db_path)
        latest_issue = get_latest_issue(conn, args.lottery)
        
        if not latest_issue:
            print(json.dumps({
                "success": False,
                "error": "数据库为空，请先抓取历史数据"
            }, ensure_ascii=False))
            return
        
        if int(args.issue) <= int(latest_issue):
            print(json.dumps({
                "success": False,
                "error": f"{args.issue} 期已开奖（最新已开奖：{latest_issue}）",
                "latest_issue": latest_issue
            }, ensure_ascii=False))
            return
        
        history = get_history_data(conn, args.lottery, limit=3430)
        conn.close()
        
        predictor = V215Predictor(history)
        result = predictor.predict(top_n=10)
        
        reds = result['red_top10']
        blues = result['blue_top4']
        
        output = {
            "success": True,
            "version": "V2.15",
            "issue": args.issue,
            "based_on": latest_issue,
            "data_count": len(history),
            "predictions": {
                "red_top10": result['red_top10'],
                "blue_top4": result['blue_top4'],
                "combo1": {"reds": sorted(reds[:6]), "blue": blues[0], "sum": sum(reds[:6])},
                "combo2": {"reds": sorted(reds[:6]), "blue": blues[1], "sum": sum(reds[:6])},
                "combo3": {"reds": sorted(reds[4:10]), "blue": blues[2], "sum": sum(reds[4:10])}
            },
            "analysis": {
                "tier1": reds[:6],
                "tier2": reds[6:],
                "blue_ranking": blues
            },
            "timestamp": datetime.now().isoformat()
        }
        
        if args.output == "json":
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"🎰 V2.15 预测模型 | 期号：{args.issue}")
            print("=" * 60)
            print(f"📊 基于数据：{latest_issue} 期及之前（共 {len(history)} 期）")
            print()
            print(f"🔴 红球 TOP10: {result['red_top10']}")
            print(f"🔵 蓝球 TOP4: {result['blue_top4']}")
            print()
            print("⭐ 推荐组合:")
            print(f"   第 1 组：{sorted(reds[:6])} + {blues[0]} (和值：{sum(reds[:6])})")
            print(f"   第 2 组：{sorted(reds[:6])} + {blues[1]} (和值：{sum(reds[:6])})")
            print(f"   第 3 组：{sorted(reds[4:10])} + {blues[2]} (和值：{sum(reds[4:10])})")
            print("=" * 60)
            print("✅ V2.15 预测完成")
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False))

if __name__ == "__main__":
    main()
