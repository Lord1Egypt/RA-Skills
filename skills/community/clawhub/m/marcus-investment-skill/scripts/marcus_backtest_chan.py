#!/usr/bin/env python3
"""
Marcus 缠论策略回测系统
功能：基于缠论买卖点的历史回测
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import json

# 导入缠论分析模块
from marcus_chan_theory import ChanTheoryAnalyzer, Beichi, TradingPoint

@dataclass
class Trade:
    """交易记录"""
    entry_date: str
    entry_price: float
    entry_type: str  # buy1/buy2/buy3
    exit_date: Optional[str] = None
    exit_price: Optional[float] = None
    exit_type: Optional[str] = None  # sell1/sell2/sell3/stop_loss/target
    shares: int = 0
    profit_loss: float = 0.0
    profit_pct: float = 0.0
    holding_days: int = 0
    status: str = "open"  # open/closed

@dataclass
class BacktestResult:
    """回测结果"""
    stock_code: str
    stock_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    avg_profit: float
    avg_loss: float
    max_drawdown: float
    sharpe_ratio: float
    trades: List[Trade] = None

class ChanBacktester:
    """缠论策略回测器"""
    
    def __init__(self, stock_code: str, initial_capital: float = 100000.0):
        self.stock_code = stock_code
        self.stock_name = ""
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0  # 持仓股数
        self.trades: List[Trade] = []
        self.data = None
        self.daily_values = []  # 每日资产值
        
    def fetch_data(self, start_date: str, end_date: str = None):
        """获取历史数据"""
        print(f"\n【获取历史数据】{self.stock_code}")
        
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        
        self.data = ak.stock_zh_a_hist(
            symbol=self.stock_code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"
        )
        
        # 获取股票名称
        try:
            info = ak.stock_individual_info_em(symbol=self.stock_code)
            for _, row in info.iterrows():
                if row['item'] == '股票简称':
                    self.stock_name = str(row['value'])
        except:
            self.stock_name = self.stock_code
        
        print(f"  股票：{self.stock_name}")
        print(f"  数据条数：{len(self.data)}")
        print(f"  时间范围：{self.data['日期'].min()} - {self.data['日期'].max()}")
        
        return self.data
    
    def detect_signals(self) -> List[TradingPoint]:
        """检测缠论买卖点信号"""
        print("\n【检测缠论买卖点】")
        
        if self.data is None or len(self.data) < 60:
            print("  数据不足，无法检测信号")
            return []
        
        # 创建缠论分析器
        analyzer = ChanTheoryAnalyzer(self.data)
        analyzer.analyze()
        
        trading_points = analyzer.trading_points
        print(f"  检测到 {len(trading_points)} 个买卖点")
        
        # 打印买卖点
        for point in trading_points:
            print(f"    {point.date}: {point.name} @ ¥{point.price:.2f} (置信度：{point.confidence:.2%})")
        
        return trading_points
    
    def backtest(self, start_date: str = "20240101", end_date: str = None,
                 stop_loss_pct: float = 0.05, target_profit_pct: float = 0.15,
                 position_pct: float = 0.5) -> BacktestResult:
        """
        执行回测
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            stop_loss_pct: 止损比例 (默认 5%)
            target_profit_pct: 目标止盈比例 (默认 15%)
            position_pct: 单次仓位比例 (默认 50%)
        """
        print("\n" + "="*60)
        print("【缠论策略回测】")
        print("="*60)
        
        # 获取数据
        self.fetch_data(start_date, end_date)
        
        # 检测信号
        trading_points = self.detect_signals()
        
        if not trading_points:
            print("  无买卖点信号，回测结束")
            return self._create_result(start_date, end_date or datetime.now().strftime("%Y%m%d"))
        
        # 初始化
        self.capital = self.initial_capital
        self.position = 0
        self.trades = []
        self.daily_values = []
        
        current_trade: Optional[Trade] = None
        
        # 遍历交易日
        for idx, row in self.data.iterrows():
            date = str(row['日期'])
            price = float(row['收盘'])
            high = float(row['最高'])
            low = float(row['最低'])
            
            # 检查是否有买卖点信号
            signal = next((p for p in trading_points if p.date == date), None)
            
            # 买入逻辑
            if signal and signal.type in ['buy1', 'buy2', 'buy3'] and self.position == 0:
                # 计算可买股数
                available_capital = self.capital * position_pct
                shares = int(available_capital / price / 100) * 100  # 100 股整数倍
                
                if shares > 0:
                    cost = shares * price
                    self.capital -= cost
                    self.position = shares
                    
                    trade = Trade(
                        entry_date=date,
                        entry_price=price,
                        entry_type=signal.type,
                        shares=shares,
                        status="open"
                    )
                    current_trade = trade
                    self.trades.append(trade)
                    
                    print(f"\n【买入】{date} @ ¥{price:.2f} x {shares}股")
                    print(f"  类型：{signal.name} (置信度：{signal.confidence:.2%})")
                    print(f"  金额：¥{cost:.2f}")
            
            # 卖出逻辑 (持仓中)
            elif self.position > 0 and current_trade:
                # 检查止损
                if price <= current_trade.entry_price * (1 - stop_loss_pct):
                    # 止损卖出
                    revenue = self.position * price
                    self.capital += revenue
                    profit_loss = revenue - current_trade.entry_price * self.position
                    profit_pct = profit_loss / (current_trade.entry_price * self.position)
                    
                    current_trade.exit_date = date
                    current_trade.exit_price = price
                    current_trade.exit_type = "stop_loss"
                    current_trade.profit_loss = profit_loss
                    current_trade.profit_pct = profit_pct
                    current_trade.holding_days = self._calc_holding_days(current_trade.entry_date, date)
                    current_trade.status = "closed"
                    
                    print(f"\n【止损卖出】{date} @ ¥{price:.2f}")
                    print(f"  亏损：¥{profit_loss:.2f} ({profit_pct:.2%})")
                    
                    self.position = 0
                    current_trade = None
                
                # 检查止盈
                elif price >= current_trade.entry_price * (1 + target_profit_pct):
                    # 止盈卖出
                    revenue = self.position * price
                    self.capital += revenue
                    profit_loss = revenue - current_trade.entry_price * self.position
                    profit_pct = profit_loss / (current_trade.entry_price * self.position)
                    
                    current_trade.exit_date = date
                    current_trade.exit_price = price
                    current_trade.exit_type = "target"
                    current_trade.profit_loss = profit_loss
                    current_trade.profit_pct = profit_pct
                    current_trade.holding_days = self._calc_holding_days(current_trade.entry_date, date)
                    current_trade.status = "closed"
                    
                    print(f"\n【止盈卖出】{date} @ ¥{price:.2f}")
                    print(f"  盈利：¥{profit_loss:.2f} ({profit_pct:.2%})")
                    
                    self.position = 0
                    current_trade = None
                
                # 检查卖出信号
                elif signal and signal.type in ['sell1', 'sell2', 'sell3']:
                    revenue = self.position * price
                    self.capital += revenue
                    profit_loss = revenue - current_trade.entry_price * self.position
                    profit_pct = profit_loss / (current_trade.entry_price * self.position)
                    
                    current_trade.exit_date = date
                    current_trade.exit_price = price
                    current_trade.exit_type = signal.type
                    current_trade.profit_loss = profit_loss
                    current_trade.profit_pct = profit_pct
                    current_trade.holding_days = self._calc_holding_days(current_trade.entry_date, date)
                    current_trade.status = "closed"
                    
                    print(f"\n【信号卖出】{date} @ ¥{price:.2f}")
                    print(f"  类型：{signal.name}")
                    print(f"  盈亏：¥{profit_loss:.2f} ({profit_pct:.2%})")
                    
                    self.position = 0
                    current_trade = None
            
            # 记录每日资产值
            daily_value = self.capital + self.position * price
            self.daily_values.append({
                'date': date,
                'value': daily_value,
                'price': price
            })
        
        # 处理未平仓交易
        if current_trade and self.position > 0:
            last_price = float(self.data.iloc[-1]['收盘'])
            last_date = str(self.data.iloc[-1]['日期'])
            
            revenue = self.position * last_price
            profit_loss = revenue - current_trade.entry_price * self.position
            profit_pct = profit_loss / (current_trade.entry_price * self.position)
            
            current_trade.exit_date = last_date
            current_trade.exit_price = last_price
            current_trade.exit_type = "end_of_period"
            current_trade.profit_loss = profit_loss
            current_trade.profit_pct = profit_pct
            current_trade.holding_days = self._calc_holding_days(current_trade.entry_date, last_date)
            current_trade.status = "closed"
            
            print(f"\n【期末平仓】{last_date} @ ¥{last_price:.2f}")
            print(f"  盈亏：¥{profit_loss:.2f} ({profit_pct:.2%})")
        
        # 创建回测结果
        result = self._create_result(start_date, end_date or datetime.now().strftime("%Y%m%d"))
        
        return result
    
    def _calc_holding_days(self, entry_date: str, exit_date: str) -> int:
        """计算持仓天数"""
        entry = datetime.strptime(entry_date, "%Y-%m-%d")
        exit = datetime.strptime(exit_date, "%Y-%m-%d")
        return (exit - entry).days
    
    def _create_result(self, start_date: str, end_date: str) -> BacktestResult:
        """创建回测结果"""
        # 计算总收益
        total_trades = len(self.trades)
        winning_trades = sum(1 for t in self.trades if t.profit_loss > 0)
        losing_trades = sum(1 for t in self.trades if t.profit_loss <= 0)
        
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        profits = [t.profit_loss for t in self.trades if t.profit_loss > 0]
        losses = [t.profit_loss for t in self.trades if t.profit_loss <= 0]
        
        avg_profit = np.mean(profits) if profits else 0
        avg_loss = np.mean(losses) if losses else 0
        
        final_capital = self.capital + self.position * float(self.data.iloc[-1]['收盘']) if self.position > 0 else self.capital
        total_return = (final_capital - self.initial_capital) / self.initial_capital
        
        # 计算年化收益
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")
        years = (end - start).days / 365.25
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 计算最大回撤
        max_drawdown = 0
        peak = self.initial_capital
        for dv in self.daily_values:
            if dv['value'] > peak:
                peak = dv['value']
            drawdown = (peak - dv['value']) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # 计算夏普比率 (简化)
        if self.daily_values:
            returns = []
            for i in range(1, len(self.daily_values)):
                ret = (self.daily_values[i]['value'] - self.daily_values[i-1]['value']) / self.daily_values[i-1]['value']
                returns.append(ret)
            
            if returns:
                avg_return = np.mean(returns)
                std_return = np.std(returns)
                sharpe_ratio = (avg_return * 252) / (std_return * np.sqrt(252)) if std_return > 0 else 0
            else:
                sharpe_ratio = 0
        else:
            sharpe_ratio = 0
        
        result = BacktestResult(
            stock_code=self.stock_code,
            stock_name=self.stock_name,
            start_date=start_date,
            end_date=end_date,
            initial_capital=self.initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            annual_return=annual_return,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            avg_profit=avg_profit,
            avg_loss=avg_loss,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            trades=self.trades
        )
        
        return result
    
    def print_result(self, result: BacktestResult):
        """打印回测结果"""
        print("\n" + "="*60)
        print("【回测结果汇总】")
        print("="*60)
        
        print(f"\n股票：{result.stock_name} ({result.stock_code})")
        print(f"回测期间：{result.start_date} - {result.end_date}")
        print(f"初始资金：¥{result.initial_capital:,.2f}")
        print(f"最终资金：¥{result.final_capital:,.2f}")
        
        print(f"\n【收益指标】")
        print(f"  总收益率：{result.total_return:.2%}")
        print(f"  年化收益：{result.annual_return:.2%}")
        print(f"  最大回撤：{result.max_drawdown:.2%}")
        print(f"  夏普比率：{result.sharpe_ratio:.2f}")
        
        print(f"\n【交易统计】")
        print(f"  总交易次数：{result.total_trades}")
        print(f"  盈利次数：{result.winning_trades}")
        print(f"  亏损次数：{result.losing_trades}")
        print(f"  胜率：{result.win_rate:.2%}")
        print(f"  平均盈利：¥{result.avg_profit:.2f}")
        print(f"  平均亏损：¥{result.avg_loss:.2f}")
        print(f"  盈亏比：{abs(result.avg_profit / result.avg_loss) if result.avg_loss != 0 else 'N/A'}")
        
        print(f"\n【交易明细】")
        for i, trade in enumerate(result.trades, 1):
            status = "✅" if trade.profit_loss > 0 else "❌"
            print(f"  {i}. {trade.entry_date} 买入 @ ¥{trade.entry_price:.2f} → "
                  f"{trade.exit_date} 卖出 @ ¥{trade.exit_price:.2f} "
                  f"{status} ¥{trade.profit_loss:+,.2f} ({trade.profit_pct:.2%}) "
                  f"[{trade.holding_days}天]")
        
        print("\n" + "="*60)


def main():
    """测试回测系统"""
    import sys
    
    if len(sys.argv) > 1:
        stock_code = sys.argv[1]
    else:
        stock_code = "301308"  # 江波龙
    
    print(f"回测股票：{stock_code}")
    
    # 创建回测器
    backtester = ChanBacktester(stock_code, initial_capital=100000.0)
    
    # 执行回测 (回测过去一年)
    start_date = "20250101"
    result = backtester.backtest(
        start_date=start_date,
        stop_loss_pct=0.05,
        target_profit_pct=0.15,
        position_pct=0.5
    )
    
    # 打印结果
    backtester.print_result(result)
    
    # 导出结果
    output_file = f"backtest_{stock_code}_{datetime.now().strftime('%Y%m%d')}.json"
    result_dict = asdict(result)
    result_dict['trades'] = [asdict(t) for t in result.trades]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
    
    print(f"\n回测结果已导出：{output_file}")


if __name__ == "__main__":
    main()
