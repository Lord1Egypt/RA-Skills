#!/usr/bin/env python3
"""
HPM 求解器调试脚本 v2
修复：约数过滤需要考虑 maxqty 限制
"""

import json
import os
import re
import argparse
from itertools import product
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ============ 数据类 ============

@dataclass
class Item:
    """物品"""
    name: str
    price: int  # 实际价格（已乘系数）
    base_price: int  # 原始价格
    currency: str
    category: str
    maxqty: int  # 最大购买数量


@dataclass
class EquivalenceGroup:
    """等价物品组"""
    base_price: int  # 原始价格
    actual_price: int  # 实际价格
    items: List[str]  # 物品名称列表
    category: str
    maxqty: int  # 最大购买数量
    
    def __repr__(self):
        names = " | ".join(self.items)
        return f"[{names}] = {self.actual_price}, maxqty={self.maxqty}"


@dataclass
class Solution:
    """求解结果"""
    groups: List[Tuple[EquivalenceGroup, int]]  # (等价组, 数量)
    total_cost: int
    residual: int
    is_perfect: bool
    
    def get_quantities(self) -> Dict[str, int]:
        """展开为物品数量字典"""
        result = {}
        for group, qty in self.groups:
            if qty > 0:
                for item in group.items:
                    result[item] = result.get(item, 0) + qty
        return result


# ============ 数据预处理 ============

class DataPreprocessor:
    """数据预处理器 - 合并等价物品"""
    
    @staticmethod
    def group_by_price(items: List[Item]) -> List[EquivalenceGroup]:
        """按实际价格分组，合并等价物品"""
        print(f"\n[DEBUG] group_by_price 输入: {len(items)} 个物品")
        
        price_groups = defaultdict(list)
        
        for item in items:
            key = (item.price, item.category)
            price_groups[key].append(item)
            print(f"  [DEBUG] 分组: price={item.price}, category={item.category}, item={item.name}, maxqty={item.maxqty}")
        
        groups = []
        for (price, category), item_list in price_groups.items():
            base_prices = list(set(i.base_price for i in item_list))
            base_price = min(base_prices) if base_prices else price
            
            # 取该组中所有物品的maxqty的最小值（保守策略）
            maxqtys = [i.maxqty for i in item_list if i.maxqty > 0]
            maxqty = min(maxqtys) if maxqtys else 99
            
            group = EquivalenceGroup(
                base_price=base_price,
                actual_price=price,
                items=[i.name for i in item_list],
                category=category,
                maxqty=maxqty
            )
            groups.append(group)
            print(f"  [DEBUG] 创建等价组: {group}")
        
        result = sorted(groups, key=lambda g: g.actual_price)
        print(f"[DEBUG] group_by_price 输出: {len(result)} 个等价组")
        return result
    
    @staticmethod
    def filter_by_divisibility(groups: List[EquivalenceGroup], target: int) -> List[EquivalenceGroup]:
        """
        约数过滤：只有当低价物品能完全替代高价物品时，才过滤高价物品
        
        关键修复：考虑 maxqty 限制
        - 如果低价物品的 maxqty * price < 高价物品的 price，则不能过滤高价物品
        - 因为低价物品买不够数量来替代高价物品
        """
        print(f"\n[DEBUG] filter_by_divisibility 输入: {len(groups)} 个等价组, 目标={target}")
        
        kept = []
        
        for group in groups:
            can_replace = False
            for kept_group in kept:
                # 检查是否是倍数关系
                if group.actual_price % kept_group.actual_price == 0:
                    ratio = group.actual_price // kept_group.actual_price
                    # 关键检查：低价物品能否买够数量来替代高价物品？
                    # 需要买 ratio 个低价物品才能替代 1 个高价物品
                    # 如果低价物品的 maxqty < ratio，则无法替代
                    if kept_group.maxqty >= ratio:
                        can_replace = True
                        print(f"  [DEBUG] 过滤: {group.actual_price} 是 {kept_group.actual_price} 的 {ratio} 倍")
                        print(f"           低价物品 maxqty={kept_group.maxqty} >= ratio={ratio}，可以替代，跳过")
                        break
                    else:
                        print(f"  [DEBUG] 保留: {group.actual_price} 是 {kept_group.actual_price} 的 {ratio} 倍")
                        print(f"           但低价物品 maxqty={kept_group.maxqty} < ratio={ratio}，无法替代，保留")
            
            if not can_replace:
                kept.append(group)
                print(f"  [DEBUG] 保留: {group}")
        
        print(f"[DEBUG] filter_by_divisibility 输出: {len(kept)} 个运算组")
        return kept


# ============ 核心求解器 ============

class HPMSolverDebug:
    """HPM交易求解器 - 调试版"""
    
    def solve(self, target_diamond: int, items: List[Item]) -> Optional[Solution]:
        """宝石求解"""
        print(f"\n{'='*60}")
        print(f"[DEBUG] 开始求解: 目标宝石={target_diamond}")
        print(f"[DEBUG] 输入物品数量: {len(items)}")
        for item in items:
            print(f"  - {item.name}: price={item.price}, base_price={item.base_price}, maxqty={item.maxqty}")
        
        # 数据预处理：分组 + 过滤
        groups = DataPreprocessor.group_by_price(items)
        filtered_groups = DataPreprocessor.filter_by_divisibility(groups, target_diamond)
        
        if not filtered_groups:
            print("[ERROR] 过滤后没有可用的运算组！")
            return None
        
        print(f"\n[DEBUG] 最终参与运算的等价组:")
        for g in filtered_groups:
            print(f"  - {g}")
        
        min_price = min(g.actual_price for g in filtered_groups)
        print(f"\n[DEBUG] 最小价格: {min_price}")
        
        # 穷举求解
        # 注意：max_quantity 应该考虑 maxqty 限制
        max_quantities = [min(target_diamond // g.actual_price, g.maxqty) for g in filtered_groups]
        print(f"\n[DEBUG] 各组的最大数量限制:")
        for g, mq in zip(filtered_groups, max_quantities):
            print(f"  - {g.items[0]}: 价格={g.actual_price}, maxqty={g.maxqty}, 计算max={target_diamond // g.actual_price}, 实际max={mq}")
        
        # 计算组合数
        total_combos = 1
        for mq in max_quantities:
            total_combos *= (mq + 1)
        
        print(f"\n[DEBUG] 总组合数: {total_combos}")
        
        if total_combos > 10000000:
            print("[WARN] 组合数过多，使用启发式求解")
            return self._heuristic_solve(target_diamond, filtered_groups, min_price)
        
        best_solution = None
        ranges = [range(mq + 1) for mq in max_quantities]
        
        combo_count = 0
        for combo in product(*ranges):
            combo_count += 1
            cost = sum(n * g.actual_price for n, g in zip(combo, filtered_groups))
            y = target_diamond - cost
            
            # 打印前10个组合和接近目标的组合
            if combo_count <= 10 or (0 <= y < min_price * 2):
                combo_str = ", ".join(f"{g.items[0]}×{n}" for n, g in zip(combo, filtered_groups) if n > 0)
                print(f"  [DEBUG] 组合#{combo_count}: [{combo_str}] cost={cost}, residual={y}")
            
            if 0 <= y < min_price:
                solution_groups = [
                    (g, n) for n, g in zip(combo, filtered_groups) if n > 0
                ]
                solution = Solution(solution_groups, cost, y, is_perfect=(y == 0))
                
                print(f"\n[DEBUG] 找到有效解！cost={cost}, residual={y}, is_perfect={y == 0}")
                
                if solution.is_perfect:
                    return solution
                
                if best_solution is None or y < best_solution.residual:
                    best_solution = solution
                    print(f"  [DEBUG] 更新最佳解: residual={y}")
        
        print(f"\n[DEBUG] 穷举完成，共检查 {combo_count} 个组合")
        if best_solution:
            print(f"[DEBUG] 最佳解: cost={best_solution.total_cost}, residual={best_solution.residual}")
        else:
            print("[ERROR] 未找到任何有效解！")
        
        return best_solution
    
    def _heuristic_solve(self, target: int, groups: List[EquivalenceGroup],
                         min_price: int) -> Optional[Solution]:
        """启发式求解"""
        print("\n[DEBUG] 使用启发式求解...")
        
        sorted_groups = sorted(groups, key=lambda g: g.actual_price, reverse=True)
        best_solution = [None]
        
        def greedy(remaining: int, idx: int, current: List[Tuple[EquivalenceGroup, int]]) -> bool:
            if idx >= len(sorted_groups):
                if 0 <= remaining < min_price:
                    sol = Solution(current.copy(), target - remaining, remaining,
                                  is_perfect=(remaining == 0))
                    if best_solution[0] is None or remaining < best_solution[0].residual:
                        best_solution[0] = sol
                    return remaining == 0
                return False
            
            g = sorted_groups[idx]
            max_n = min(remaining // g.actual_price, g.maxqty)
            
            for n in range(max_n, -1, -1):
                current.append((g, n))
                if greedy(remaining - n * g.actual_price, idx + 1, current):
                    return True
                current.pop()
            
            return False
        
        greedy(target, 0, [])
        return best_solution[0]


def parse_user_config(config_text: str) -> List[Item]:
    """解析用户提供的配置表"""
    print(f"\n[DEBUG] 解析用户配置表...")
    
    items = []
    
    # 解析菜品-宝石
    food_diamond_match = re.search(r'菜品-宝石:(.*?)(?=植物-宝石:|菜品-金币:|$)', config_text, re.DOTALL)
    if food_diamond_match:
        section = food_diamond_match.group(1)
        item_matches = re.findall(r'\{name:\s*"([^"]+)",\s*price:\s*(\d+),\s*maxqty:\s*(\d+)\}', section)
        for name, price, maxqty in item_matches:
            item = Item(
                name=name,
                price=int(price),
                base_price=int(price),
                currency="diamond",
                category="foods",
                maxqty=int(maxqty)
            )
            items.append(item)
            print(f"  [DEBUG] 解析菜品-宝石: {item}")
    
    # 解析植物-宝石
    plant_diamond_match = re.search(r'植物-宝石:(.*?)(?=菜品-宝石:|植物-金币:|$)', config_text, re.DOTALL)
    if plant_diamond_match:
        section = plant_diamond_match.group(1)
        item_matches = re.findall(r'\{name:\s*"([^"]+)",\s*price:\s*(\d+),\s*maxqty:\s*(\d+)\}', section)
        for name, price, maxqty in item_matches:
            item = Item(
                name=name,
                price=int(price),
                base_price=int(price),
                currency="diamond",
                category="plants",
                maxqty=int(maxqty)
            )
            items.append(item)
            print(f"  [DEBUG] 解析植物-宝石: {item}")
    
    print(f"[DEBUG] 共解析出 {len(items)} 个物品")
    return items


def main():
    # 用户提供的配置表
    config_text = '''菜品-宝石: 1. {name: "野心与荣耀之宴", price: 14, maxqty: 99} 2. {name: "霍格沃兹盛宴", price: 14, maxqty: 99} 3. {name: "智慧与风雅之宴", price: 14, maxqty: 99} 植物-宝石: 1. {name: "水仙", price: 2, maxqty: 20} 2. {name: "嗅幻草", price: 6, maxqty: 10}'''
    
    target_diamond = 50
    
    # 解析配置
    items = parse_user_config(config_text)
    
    # 求解
    solver = HPMSolverDebug()
    result = solver.solve(target_diamond, items)
    
    # 输出结果
    print(f"\n{'='*60}")
    print("## 🧙 HPM 求解结果")
    print("")
    
    if result:
        status = "✅ 完美解" if result.is_perfect else "⚠️ 近似解"
        print(f"### 💎 宝石：{result.total_cost + result.residual} → {status}")
        print("")
        
        print("| 物品组 | 数量 | 单价 | 小计 |")
        print("|--------|------|------|------|")
        
        for group, qty in sorted(result.groups, key=lambda x: -x[1]):
            if qty > 0:
                names = " | ".join(group.items)
                subtotal = qty * group.actual_price
                print(f"| {names} | {qty} | {group.actual_price}宝石 | {subtotal}宝石 |")
        
        print(f"| **合计** | - | - | **{result.total_cost}宝石** |")
        print("")
        
        if result.is_perfect:
            print("✅ 残值：0（刚好花光）")
        else:
            print(f"⚠️ 残值：{result.residual}宝石")
    else:
        print("❌ 未找到解！")


if __name__ == "__main__":
    main()
