#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长桥手续费计算器
根据长桥官方费率表 + 账户交易量阶梯计算真实手续费
"""

from dataclasses import dataclass
from typing import Tuple

@dataclass
class FeeTier:
    """费率阶梯"""
    min_volume: float  # 最小交易量（美元）
    max_volume: float  # 最大交易量（美元）
    discount: float    # 折扣（0.9=9 折）

# 长桥美股期权官方费率（2026 年）
class LongportFeeCalculator:
    """长桥手续费计算器"""
    
    # 基础费率
    COMMISSION_RATE = 0.0065      # 佣金 0.65%
    COMMISSION_MIN = 1.0          # 最小佣金$1
    COMMISSION_MAX_RATIO = 0.01   # 最大佣金 1%
    
    EXCHANGE_FEE = 0.0004         # 交易所费用 0.04%
    CLEARING_FEE = 0.000119       # 清算费 0.0119%
    
    # 期权费用
    OPTION_CONTRACT_FEE = 0.00    # 期权佣金$0/张（免佣金推广）
    
    # 费率阶梯（按月交易量）
    FEE_TIERS = [
        FeeTier(0, 1000000, 1.0),      # <100 万：原价
        FeeTier(1000000, 5000000, 0.9), # 100-500 万：9 折
        FeeTier(5000000, 10000000, 0.8), # 500-1000 万：8 折
        FeeTier(10000000, float('inf'), 0.7), # >1000 万：7 折
    ]
    
    def __init__(self, monthly_volume: float = 0):
        """
        初始化
        :param monthly_volume: 月交易量（美元）
        """
        self.monthly_volume = monthly_volume
    
    def get_discount(self) -> float:
        """获取当前折扣"""
        for tier in self.FEE_TIERS:
            if tier.min_volume <= self.monthly_volume < tier.max_volume:
                return tier.discount
        return 1.0
    
    def calculate_fee(self, trade_value: float, is_option: bool = False) -> Tuple[float, dict]:
        """
        计算手续费
        :param trade_value: 交易金额（美元）
        :param is_option: 是否期权交易
        :return: (总手续费，费用明细)
        """
        discount = self.get_discount()
        
        # 佣金（打折后）
        commission = trade_value * self.COMMISSION_RATE * discount
        commission = max(commission, self.COMMISSION_MIN * discount)  # 最小佣金
        commission = min(commission, trade_value * self.COMMISSION_MAX_RATIO)  # 最大佣金
        
        # 交易所费用
        exchange_fee = trade_value * self.EXCHANGE_FEE
        
        # 清算费
        clearing_fee = trade_value * self.CLEARING_FEE
        
        # 期权合约费
        option_fee = 0.0
        if is_option:
            option_fee = self.OPTION_CONTRACT_FEE
        
        # 总费用
        total_fee = commission + exchange_fee + clearing_fee + option_fee
        
        fee_breakdown = {
            'commission': commission,
            'exchange_fee': exchange_fee,
            'clearing_fee': clearing_fee,
            'option_fee': option_fee,
            'discount': discount,
            'total_fee': total_fee,
            'fee_ratio': total_fee / trade_value if trade_value > 0 else 0,
        }
        
        return total_fee, fee_breakdown
    
    def calculate_option_fee(self, contract_price: float, contracts: int = 1) -> Tuple[float, dict]:
        """
        计算期权合约手续费
        :param contract_price: 期权合约价格
        :param contracts: 合约数量
        :return: (总手续费，费用明细)
        """
        trade_value = contract_price * contracts * 100  # 期权合约乘数 100
        return self.calculate_fee(trade_value, is_option=True)

# ========== 测试 ==========

if __name__ == "__main__":
    print("=" * 80)
    print("📊 长桥手续费计算器测试")
    print("=" * 80)
    
    # 测试不同交易量阶梯
    test_volumes = [500000, 2000000, 7000000, 15000000]
    
    for volume in test_volumes:
        calc = LongportFeeCalculator(monthly_volume=volume)
        discount = calc.get_discount()
        
        # 测试$10,000 交易
        trade_value = 10000
        fee, breakdown = calc.calculate_fee(trade_value)
        
        print(f"\n月交易量：${volume:,.0f}")
        print(f"  折扣：{discount*100:.0f}折")
        print(f"  交易金额：${trade_value:,.2f}")
        print(f"  总手续费：${fee:.2f}")
        print(f"  费率：{breakdown['fee_ratio']*100:.3f}%")
        print(f"  明细:")
        print(f"    佣金：${breakdown['commission']:.2f}")
        print(f"    交易所费：${breakdown['exchange_fee']:.2f}")
        print(f"    清算费：${breakdown['clearing_fee']:.2f}")
        print(f"    期权费：${breakdown['option_fee']:.2f}")
    
    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("=" * 80)
