#!/usr/bin/env python3
"""
HPM 求解器调试脚本 v4
优化：
1. filter_by_divisibility 维护 filter_table 记录约数关系
2. 只保留最小约数物品(miniPriceCell)进行穷举
3. 穷举成功后，用高价物品替换等值的低价物品组合
"""

import json
import os
import re
import argparse
from itertools import product
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict, field
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
    
    @property
    def max_value(self) -> int:
        """该组的最大总价值"""
        return self.actual_price * self.maxqty


@dataclass
class FilterRelation:
    """过滤关系记录"""
    high_price_group: EquivalenceGroup  # 被过滤的高价物品组
    low_price_group: EquivalenceGroup   # 用于替代的低价物品组
    ratio: int                          # 倍数关系 (high = low * ratio)
    
    def __repr__(self):
        return f"{self.high_price_group.actual_price} = {self.low_price_group.actual_price} × {self.ratio}"


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
    def filter_by_divisibility(groups: List[EquivalenceGroup], target: int) -> Tuple[List[EquivalenceGroup], List[FilterRelation]]:
        """
        约数过滤：维护 filter_table 记录约数关系
        
        返回：
        - miniPriceCell: 最小约数物品列表（用于穷举）
        - filter_table: 过滤关系记录（用于还原替换）
        """
        print(f"\n[DEBUG] filter_by_divisibility 输入: {len(groups)} 个等价组, 目标={target}")
        
        miniPriceCell = []  # 最小约数物品列表
        filter_table = []   # 过滤关系记录
        
        for group in groups:
            # 查找能否被已有的最小约数物品替代
            can_filter = False
            
            for low_group in miniPriceCell:
                # 检查是否是倍数关系
                if group.actual_price % low_group.actual_price == 0:
                    ratio = group.actual_price // low_group.actual_price
                    
                    # 条件1：低价物品能否买够数量来替代高价物品？
                    can_buy_enough = low_group.maxqty >= ratio
                    
                    # 条件2：低价物品的总价值是否足够达到目标？
                    can_reach_target = low_group.max_value >= target
                    
                    if can_buy_enough and can_reach_target:
                        # 可以过滤，记录关系
                        relation = FilterRelation(
                            high_price_group=group,
                            low_price_group=low_group,
                            ratio=ratio
                        )
                        filter_table.append(relation)
                        can_filter = True
                        print(f"  [DEBUG] 过滤: {group.actual_price} = {low_group.actual_price} × {ratio}")
                        print(f"           低价物品 maxqty={low_group.maxqty} >= ratio={ratio} ✓")
                        print(f"           低价物品 max_value={low_group.max_value} >= target={target} ✓")
                        break
                    else:
                        print(f"  [DEBUG] 检查: {group.actual_price} 是 {low_group.actual_price} 的 {ratio} 倍")
                        if not can_buy_enough:
                            print(f"           低价物品 maxqty={low_group.maxqty} < ratio={ratio} ✗ 无法买够数量")
                        if not can_reach_target:
                            print(f"           低价物品 max_value={low_group.max_value} < target={target} ✗ 无法达到目标")
            
            if not can_filter:
                miniPriceCell.append(group)
                print(f"  [DEBUG] 保留到 miniPriceCell: {group}")
        
        print(f"\n[DEBUG] filter_by_divisibility 输出:")
        print(f"  - miniPriceCell: {len(miniPriceCell)} 个运算组")
        print(f"  - filter_table: {len(filter_table)} 条过滤关系")
        
        return miniPriceCell, filter_table


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
        miniPriceCell, filter_table = DataPreprocessor.filter_by_divisibility(groups, target_diamond)
        
        if not miniPriceCell:
            print("[ERROR] 过滤后没有可用的运算组！")
            return None
        
        print(f"\n[DEBUG] 最终参与穷举的等价组 (miniPriceCell):")
        for g in miniPriceCell:
            print(f"  - {g}")
        
        print(f"\n[DEBUG] 过滤关系表 (filter_table):")
        for r in filter_table:
            print(f"  - {r}")
        
        min_price = min(g.actual_price for g in miniPriceCell)
        print(f"\n[DEBUG] 最小价格: {min_price}")
        
        # 穷举求解（使用 miniPriceCell）
        max_quantities = [min(target_diamond // g.actual_price, g.maxqty) for g in miniPriceCell]
        print(f"\n[DEBUG] 各组的最大数量限制:")
        for g, mq in zip(miniPriceCell, max_quantities):
            print(f"  - {g.items[0]}: 价格={g.actual_price}, maxqty={g.maxqty}, 计算max={target_diamond // g.actual_price}, 实际max={mq}")
        
        # 计算组合数
        total_combos = 1
        for mq in max_quantities:
            total_combos *= (mq + 1)
        
        print(f"\n[DEBUG] 总组合数: {total_combos}")
        
        best_solution = None
        ranges = [range(mq + 1) for mq in max_quantities]
        
        combo_count = 0
        for combo in product(*ranges):
            combo_count += 1
            cost = sum(n * g.actual_price for n, g in zip(combo, miniPriceCell))
            y = target_diamond - cost
            
            # 打印前10个组合和接近目标的组合
            if combo_count <= 10 or (0 <= y < min_price * 2):
                combo_str = ", ".join(f"{g.items[0]}×{n}" for n, g in zip(combo, miniPriceCell) if n > 0)
                print(f"  [DEBUG] 组合#{combo_count}: [{combo_str}] cost={cost}, residual={y}")
            
            if 0 <= y < min_price:
                solution_groups = [
                    (g, n) for n, g in zip(combo, miniPriceCell) if n > 0
                ]
                solution = Solution(solution_groups, cost, y, is_perfect=(y == 0))
                
                print(f"\n[DEBUG] 找到有效解！cost={cost}, residual={y}, is_perfect={y == 0}")
                
                if solution.is_perfect:
                    # 尝试用高价物品替换低价物品组合
                    optimized_solution = self._try_replace_with_high_price(
                        solution, filter_table, target_diamond
                    )
                    return optimized_solution
                
                if best_solution is None or y < best_solution.residual:
                    best_solution = solution
                    print(f"  [DEBUG] 更新最佳解: residual={y}")
        
        print(f"\n[DEBUG] 穷举完成，共检查 {combo_count} 个组合")
        if best_solution:
            print(f"[DEBUG] 最佳解: cost={best_solution.total_cost}, residual={best_solution.residual}")
            # 尝试替换
            optimized_solution = self._try_replace_with_high_price(
                best_solution, filter_table, target_diamond
            )
            return optimized_solution
        else:
            print("[ERROR] 未找到任何有效解！")
        
        return None
    
    def _try_replace_with_high_price(self, solution: Solution, 
                                      filter_table: List[FilterRelation],
                                      target: int) -> Solution:
        """
        尝试用高价物品替换低价物品组合
        
        例如：2×15 = 30，可以用 14×2 + 2×1 = 30 替换
        """
        print(f"\n[DEBUG] 尝试用高价物品替换低价物品组合...")
        
        # 当前解的物品数量
        quantities = solution.get_quantities()
        print(f"[DEBUG] 当前解: {quantities}")
        
        # 按 ratio 从大到小排序 filter_table，优先替换大倍数
        sorted_filter_table = sorted(filter_table, key=lambda r: r.ratio, reverse=True)
        
        # 记录替换操作
        replacements = []
        remaining_quantities = quantities.copy()
        
        for relation in sorted_filter_table:
            low_price = relation.low_price_group.actual_price
            high_price = relation.high_price_group.actual_price
            ratio = relation.ratio
            
            # 查找低价物品的数量
            low_item_name = relation.low_price_group.items[0]
            if low_item_name not in remaining_quantities:
                continue
            
            low_qty = remaining_quantities[low_item_name]
            
            # 计算可以替换多少个高价物品
            # 需要 ratio 个低价物品才能替换 1 个高价物品
            max_replace = low_qty // ratio
            
            if max_replace > 0:
                # 检查高价物品的 maxqty 限制
                high_maxqty = relation.high_price_group.maxqty
                
                # 实际替换数量
                actual_replace = min(max_replace, high_maxqty)
                
                if actual_replace > 0:
                    replacements.append({
                        'high_group': relation.high_price_group,
                        'low_group': relation.low_price_group,
                        'ratio': ratio,
                        'replace_count': actual_replace,
                        'low_qty_consumed': actual_replace * ratio
                    })
                    
                    # 更新剩余数量
                    remaining_quantities[low_item_name] -= actual_replace * ratio
                    print(f"[DEBUG] 替换: {actual_replace}个 {relation.high_price_group.items[0]}({high_price}宝石) "
                          f"<-> {actual_replace * ratio}个 {low_item_name}({low_price}宝石)")
        
        if not replacements:
            print("[DEBUG] 没有可替换的组合，返回原解")
            return solution
        
        # 构建新的解
        new_groups = []
        
        # 添加高价物品（替换后的）
        for rep in replacements:
            new_groups.append((rep['high_group'], rep['replace_count']))
        
        # 添加剩余的低价物品
        for group, qty in solution.groups:
            if qty > 0:
                item_name = group.items[0]
                remaining = remaining_quantities.get(item_name, 0)
                if remaining > 0:
                    new_groups.append((group, remaining))
        
        new_solution = Solution(
            groups=new_groups,
            total_cost=solution.total_cost,
            residual=solution.residual,
            is_perfect=solution.is_perfect
        )
        
        print(f"[DEBUG] 替换后的解: {new_solution.get_quantities()}")
        
        return new_solution


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


def format_solution(solution: Solution) -> str:
    """格式化输出解"""
    lines = []
    
    status = "✅ 完美解" if solution.is_perfect else "⚠️ 近似解"
    lines.append(f"### 💎 宝石：{solution.total_cost + solution.residual} → {status}")
    lines.append("")
    
    lines.append("| 物品组 | 数量 | 单价 | 小计 |")
    lines.append("|--------|------|------|------|")
    
    for group, qty in sorted(solution.groups, key=lambda x: -x[1]):
        if qty > 0:
            names = " | ".join(group.items)
            subtotal = qty * group.actual_price
            lines.append(f"| {names} | {qty} | {group.actual_price}宝石 | {subtotal}宝石 |")
    
    lines.append(f"| **合计** | - | - | **{solution.total_cost}宝石** |")
    lines.append("")
    
    if solution.is_perfect:
        lines.append("✅ 残值：0（刚好花光）")
    else:
        lines.append(f"⚠️ 残值：{solution.residual}宝石")
    
    return "\n".join(lines)


def main():
    # 用户提供的配置表
    config_text = '''菜品-宝石: 1. {name: "野心与荣耀之宴", price: 14, maxqty: 99} 2. {name: "霍格沃兹盛宴", price: 14, maxqty: 99} 3. {name: "智慧与风雅之宴", price: 14, maxqty: 99} 植物-宝石: 1. {name: "水仙", price: 2, maxqty: 20} 2. {name: "嗅幻草", price: 6, maxqty: 10}'''
    
    # 测试用例1：目标50宝石
    print("\n" + "="*80)
    print("测试用例1：目标50宝石")
    print("="*80)
    
    target_diamond = 50
    items = parse_user_config(config_text)
    solver = HPMSolverDebug()
    result = solver.solve(target_diamond, items)
    
    print(f"\n{'='*60}")
    print("## 🧙 HPM 求解结果")
    print("")
    if result:
        print(format_solution(result))
    else:
        print("❌ 未找到解！")
    
    # 测试用例2：目标30宝石
    print("\n" + "="*80)
    print("测试用例2：目标30宝石（验证替换逻辑：2×15 -> 14×2 + 2×1）")
    print("="*80)
    
    target_diamond = 30
    items = parse_user_config(config_text)
    solver = HPMSolverDebug()
    result = solver.solve(target_diamond, items)
    
    print(f"\n{'='*60}")
    print("## 🧙 HPM 求解结果")
    print("")
    if result:
        print(format_solution(result))
    else:
        print("❌ 未找到解！")


if __name__ == "__main__":
    main()
