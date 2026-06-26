#!/usr/bin/env python3
"""
HPM 交易求解器 - 完整版 v5
新特性：
1. 双系数模型：p(food系数) + q(plant系数)
2. 数据预处理：合并等价物品，减少运算规模
3. 约数过滤优化：维护 filter_table，只保留 miniPriceCell 进行穷举
4. 替换还原：穷举成功后，用高价物品替换等值的低价物品组合
5. 优化输出：显示等价物品组和倍率关系
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
    maxqty: int = 99  # 最大购买数量，默认99


@dataclass
class EquivalenceGroup:
    """等价物品组"""
    base_price: int  # 原始价格
    actual_price: int  # 实际价格
    items: List[str]  # 物品名称列表
    category: str
    maxqty: int = 99  # 最大购买数量
    
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


@dataclass
class CacheUnit:
    """缓存单元"""
    base_cost: int
    combo: Dict[str, int]
    description: str
    created_at: str


@dataclass
class HistoryRecord:
    """历史记录"""
    timestamp: str
    target_gold: int
    target_diamond: int
    multiplier_p: float  # food系数
    multiplier_q: float  # plant系数
    solution_gold: Optional[Dict]
    solution_diamond: Optional[Dict]
    is_perfect: bool


# ============ 持久化管理 ============

class PersistenceManager:
    """数据持久化管理"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.data_dir = self.base_path / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.base_prices_file = self.data_dir / "base_prices.json"
        self.cache_file = self.data_dir / "cache.json"
        self.history_file = self.data_dir / "history.json"
        
        self._init_files()
    
    def _init_files(self):
        if not self.base_prices_file.exists():
            self._write_json(self.base_prices_file, {
                "version": 1,
                "updated_at": None,
                "base_prices": {
                    "foods": {"gold": {}, "diamond": {}},
                    "plants": {"gold": {}, "diamond": {}}
                }
            })
        
        if not self.cache_file.exists():
            self._write_json(self.cache_file, {
                "version": 1,
                "updated_at": None,
                "units": {
                    "gold_100": [], "gold_200": [], "gold_500": [], "gold_1000": [],
                    "diamond_10": [], "diamond_50": [], "diamond_100": []
                }
            })
        
        if not self.history_file.exists():
            self._write_json(self.history_file, {"version": 1, "records": []})
    
    def _read_json(self, path: Path) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_json(self, path: Path, data: dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_base_prices(self) -> Dict:
        data = self._read_json(self.base_prices_file)
        return data.get("base_prices", {
            "foods": {"gold": {}, "diamond": {}},
            "plants": {"gold": {}, "diamond": {}}
        })
    
    def save_base_prices(self, prices: Dict):
        data = {
            "version": 1,
            "updated_at": datetime.now().isoformat(),
            "base_prices": prices
        }
        self._write_json(self.base_prices_file, data)
    
    def load_cache(self) -> dict:
        return self._read_json(self.cache_file)
    
    def save_cache(self, cache: dict):
        cache["updated_at"] = datetime.now().isoformat()
        self._write_json(self.cache_file, cache)
    
    def load_history(self, limit: int = 100) -> List[dict]:
        data = self._read_json(self.history_file)
        return data.get("records", [])[-limit:]
    
    def add_history(self, record: HistoryRecord):
        data = self._read_json(self.history_file)
        data["records"].append(asdict(record))
        if len(data["records"]) > 100:
            data["records"] = data["records"][-100:]
        self._write_json(self.history_file, data)


# ============ 数据预处理 ============

class DataPreprocessor:
    """数据预处理器 - 合并等价物品"""
    
    @staticmethod
    def group_by_price(items: List[Item]) -> List[EquivalenceGroup]:
        """按实际价格分组，合并等价物品"""
        print(f"[DEBUG] group_by_price 输入: {len(items)} 个物品")
        
        price_groups = defaultdict(list)
        
        for item in items:
            key = (item.price, item.category)
            price_groups[key].append(item)
        
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

class HPMSolver:
    """HPM交易求解器 v5"""
    
    def __init__(self, persistence: PersistenceManager):
        self.persistence = persistence
    
    def solve(self, target_gold: int, target_diamond: int,
              multiplier_p: float, multiplier_q: float) -> Dict:
        """
        主求解入口
        
        数学模型：
        (plantA*n1 + plantB*n2 + ...) * q + (foodA*m1 + foodB*m2 + ...) * p = 目标金额
        """
        base_prices = self.persistence.load_base_prices()
        
        # 构建物品列表（应用双系数）
        all_items = self._build_items_with_dual_multiplier(
            base_prices, multiplier_p, multiplier_q
        )
        
        # 按货币分组
        gold_items = [i for i in all_items if i.currency == "gold"]
        diamond_items = [i for i in all_items if i.currency == "diamond"]
        
        # 求解
        gold_result = None
        diamond_result = None
        
        if target_gold > 0 and gold_items:
            gold_result = self._solve_currency(target_gold, gold_items, "gold")
        
        if target_diamond > 0 and diamond_items:
            diamond_result = self._solve_currency(target_diamond, diamond_items, "diamond")
        
        # 保存历史
        record = HistoryRecord(
            timestamp=datetime.now().isoformat(),
            target_gold=target_gold,
            target_diamond=target_diamond,
            multiplier_p=multiplier_p,
            multiplier_q=multiplier_q,
            solution_gold=gold_result.get_quantities() if gold_result else None,
            solution_diamond=diamond_result.get_quantities() if diamond_result else None,
            is_perfect=(gold_result.is_perfect if gold_result else True) and 
                      (diamond_result.is_perfect if diamond_result else True)
        )
        self.persistence.add_history(record)
        
        return {
            "gold": gold_result,
            "diamond": diamond_result,
            "multiplier_p": multiplier_p,
            "multiplier_q": multiplier_q,
            "stats": {
                "gold_items_before": len(gold_items),
                "gold_groups_after": len(DataPreprocessor.group_by_price(gold_items)),
                "gold_groups_filtered": 0  # 将在 _solve_currency 中更新
            }
        }
    
    def _build_items_with_dual_multiplier(self, base_prices: Dict,
                                           multiplier_p: float,
                                           multiplier_q: float) -> List[Item]:
        """构建物品列表，应用双系数"""
        items = []
        
        for category in ["foods", "plants"]:
            multiplier = multiplier_p if category == "foods" else multiplier_q
            
            for currency in ["gold", "diamond"]:
                if category in base_prices and currency in base_prices[category]:
                    for name, base_price in base_prices[category][currency].items():
                        actual_price = int(base_price * multiplier)
                        items.append(Item(
                            name=name,
                            price=actual_price,
                            base_price=base_price,
                            currency=currency,
                            category=category,
                            maxqty=99  # 默认99
                        ))
        
        return items
    
    def _solve_currency(self, target: int, items: List[Item], 
                        currency: str) -> Optional[Solution]:
        """单货币求解"""
        print(f"\n{'='*60}")
        print(f"[DEBUG] 开始求解: 目标{currency}={target}")
        
        # 数据预处理：分组 + 过滤
        groups = DataPreprocessor.group_by_price(items)
        miniPriceCell, filter_table = DataPreprocessor.filter_by_divisibility(groups, target)
        
        if not miniPriceCell:
            print("[ERROR] 过滤后没有可用的运算组！")
            return None
        
        print(f"\n[DEBUG] 最终参与穷举的等价组 (miniPriceCell):")
        for g in miniPriceCell:
            print(f"  - {g}")
        
        if filter_table:
            print(f"\n[DEBUG] 过滤关系表 (filter_table):")
            for r in filter_table:
                print(f"  - {r}")
        
        min_price = min(g.actual_price for g in miniPriceCell)
        print(f"\n[DEBUG] 最小价格: {min_price}")
        
        # 穷举求解（使用 miniPriceCell）
        max_quantities = [min(target // g.actual_price, g.maxqty) for g in miniPriceCell]
        print(f"\n[DEBUG] 各组的最大数量限制:")
        for g, mq in zip(miniPriceCell, max_quantities):
            print(f"  - {g.items[0]}: 价格={g.actual_price}, maxqty={g.maxqty}, 实际max={mq}")
        
        # 计算组合数
        total_combos = 1
        for mq in max_quantities:
            total_combos *= (mq + 1)
        
        print(f"\n[DEBUG] 总组合数: {total_combos}")
        
        if total_combos > 10000000:
            print("[WARN] 组合数过多，使用启发式求解")
            return self._heuristic_solve(target, miniPriceCell, min_price, filter_table)
        
        best_solution = None
        ranges = [range(mq + 1) for mq in max_quantities]
        
        combo_count = 0
        for combo in product(*ranges):
            combo_count += 1
            cost = sum(n * g.actual_price for n, g in zip(combo, miniPriceCell))
            y = target - cost
            
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
                        solution, filter_table, target
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
                best_solution, filter_table, target
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
        if not filter_table:
            print("[DEBUG] 没有过滤关系，跳过替换")
            return solution
        
        print(f"\n[DEBUG] 尝试用高价物品替换低价物品组合...")
        
        # 当前解的物品数量
        quantities = solution.get_quantities()
        print(f"[DEBUG] 当前解: {quantities}")
        
        # 按 ratio 从大到小排序 filter_table，优先替换大倍数
        sorted_filter_table = sorted(filter_table, key=lambda r: r.ratio, reverse=True)
        
        # 记录替换操作
        remaining_quantities = quantities.copy()
        new_groups = []
        
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
                    # 添加高价物品到新解
                    new_groups.append((relation.high_price_group, actual_replace))
                    
                    # 更新剩余数量
                    remaining_quantities[low_item_name] -= actual_replace * ratio
                    print(f"[DEBUG] 替换: {actual_replace}个 {relation.high_price_group.items[0]}({high_price}) "
                          f"<-> {actual_replace * ratio}个 {low_item_name}({low_price})")
        
        if not new_groups:
            print("[DEBUG] 没有可替换的组合，返回原解")
            return solution
        
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
    
    def _heuristic_solve(self, target: int, groups: List[EquivalenceGroup],
                         min_price: int, filter_table: List[FilterRelation]) -> Optional[Solution]:
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
        
        if best_solution[0]:
            return self._try_replace_with_high_price(best_solution[0], filter_table, target)
        
        return None


# ============ 报告格式化 ============

def format_report(result: Dict) -> str:
    """格式化输出报告"""
    lines = []
    lines.append("## 🧙 HPM 求解结果")
    lines.append("")
    
    # 参数
    lines.append("### 📊 参数")
    lines.append(f"- Food系数(p)：{result['multiplier_p']}")
    lines.append(f"- Plant系数(q)：{result['multiplier_q']}")
    lines.append("")
    
    # 金币结果
    if result["gold"]:
        gold_sol = result["gold"]
        status = "✅ 完美解" if gold_sol.is_perfect else "⚠️ 近似解"
        lines.append(f"### 💰 金币：{gold_sol.total_cost + gold_sol.residual:,} → {status}")
        lines.append("")
        
        lines.append("| 物品组 | 数量 | 单价 | 小计 |")
        lines.append("|--------|------|------|------|")
        
        for group, qty in sorted(gold_sol.groups, key=lambda x: -x[1]):
            if qty > 0:
                names = " | ".join(group.items)
                subtotal = qty * group.actual_price
                lines.append(f"| {names} | {qty} | {group.actual_price:,}金 | {subtotal:,}金 |")
        
        lines.append(f"| **合计** | - | - | **{gold_sol.total_cost:,}金** |")
        lines.append("")
        
        if gold_sol.is_perfect:
            lines.append("✅ 残值：0（刚好花光）")
        else:
            lines.append(f"⚠️ 残值：{gold_sol.residual}金")
        lines.append("")
    
    # 宝石结果
    if result["diamond"]:
        diamond_sol = result["diamond"]
        status = "✅ 完美解" if diamond_sol.is_perfect else "⚠️ 近似解"
        lines.append(f"### 💎 宝石：{diamond_sol.total_cost + diamond_sol.residual:,} → {status}")
        lines.append("")
        
        lines.append("| 物品组 | 数量 | 单价 | 小计 |")
        lines.append("|--------|------|------|------|")
        
        for group, qty in sorted(diamond_sol.groups, key=lambda x: -x[1]):
            if qty > 0:
                names = " | ".join(group.items)
                subtotal = qty * group.actual_price
                lines.append(f"| {names} | {qty} | {group.actual_price:,}宝石 | {subtotal:,}宝石 |")
        
        lines.append(f"| **合计** | - | - | **{diamond_sol.total_cost:,}宝石** |")
        lines.append("")
        
        if diamond_sol.is_perfect:
            lines.append("✅ 残值：0（刚好花光）")
        else:
            lines.append(f"⚠️ 残值：{diamond_sol.residual}宝石")
    
    return "\n".join(lines)


def format_base_prices(prices: Dict) -> str:
    """格式化原始价格表"""
    lines = ["## 📋 原始价格表", ""]
    
    for category in ["foods", "plants"]:
        if category not in prices:
            continue
        
        cat_name = "菜品" if category == "foods" else "植物"
        lines.append(f"### {'🍽️' if category == 'foods' else '🌱'} {cat_name}")
        
        for currency in ["gold", "diamond"]:
            if currency in prices[category] and prices[category][currency]:
                cur_name = "💰 金币" if currency == "gold" else "💎 宝石"
                lines.append(f"\n**{cur_name}**")
                lines.append("| 物品 | 基础价格 |")
                lines.append("|------|----------|")
                for name, price in sorted(prices[category][currency].items()):
                    unit = "金" if currency == "gold" else "宝石"
                    lines.append(f"| {name} | {price}{unit} |")
        
        lines.append("")
    
    return "\n".join(lines)


def format_history(history: List[dict]) -> str:
    """格式化历史记录"""
    if not history:
        return "暂无历史记录"
    
    lines = ["## 📜 求解历史", ""]
    lines.append("| 时间 | 金币 | 宝石 | p | q | 状态 |")
    lines.append("|------|------|------|-----|-----|------|")
    
    for record in history[-10:]:
        ts = record["timestamp"][:16]
        gold = record["target_gold"]
        diamond = record["target_diamond"]
        p = record.get("multiplier_p", 1.0)
        q = record.get("multiplier_q", 1.0)
        status = "✅" if record["is_perfect"] else "⚠️"
        lines.append(f"| {ts} | {gold:,} | {diamond:,} | {p} | {q} | {status} |")
    
    return "\n".join(lines)


# ============ 命令处理 ============

def handle_solve(args, persistence, solver):
    """处理求解命令"""
    result = solver.solve(
        target_gold=args.gold or 0,
        target_diamond=args.diamond or 0,
        multiplier_p=args.p or 1.0,
        multiplier_q=args.q or 1.0
    )
    print(format_report(result))


def handle_price_view(args, persistence):
    prices = persistence.load_base_prices()
    print(format_base_prices(prices))


def handle_history(args, persistence):
    history = persistence.load_history(args.limit)
    print(format_history(history))


# ============ 主程序 ============

def main():
    parser = argparse.ArgumentParser(description="HPM交易求解器 v5")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 求解命令
    solve_parser = subparsers.add_parser("solve", help="求解购买组合")
    solve_parser.add_argument("--gold", "-g", type=int, help="金币目标")
    solve_parser.add_argument("--diamond", "-d", type=int, help="宝石目标")
    solve_parser.add_argument("-p", type=float, default=1.0, 
                              help="Food系数（菜品乘算系数）")
    solve_parser.add_argument("-q", type=float, default=1.0,
                              help="Plant系数（植物乘算系数）")
    
    # 价格命令
    price_parser = subparsers.add_parser("price", help="价格管理")
    price_parser.add_argument("action", choices=["view"], help="操作")
    
    # 历史命令
    history_parser = subparsers.add_parser("history", help="查看历史")
    history_parser.add_argument("--limit", "-l", type=int, default=10)
    
    args = parser.parse_args()
    
    base_path = Path(__file__).parent.parent
    persistence = PersistenceManager(str(base_path))
    solver = HPMSolver(persistence)
    
    if args.command == "solve":
        handle_solve(args, persistence, solver)
    elif args.command == "price":
        if args.action == "view":
            handle_price_view(args, persistence)
    elif args.command == "history":
        handle_history(args, persistence)
    else:
        # 自然语言模式
        import sys
        text = " ".join(sys.argv[1:])
        
        # 解析自然语言
        gold_match = re.search(r"(?:金币|金)[：:\s]*(\d+)", text)
        diamond_match = re.search(r"宝石[：:\s]*(\d+)", text)
        p_match = re.search(r"[pP][：:\s=]*([\d.]+)", text)
        q_match = re.search(r"[qQ][：:\s=]*([\d.]+)", text)
        
        gold = int(gold_match.group(1)) if gold_match else 0
        diamond = int(diamond_match.group(1)) if diamond_match else 0
        p = float(p_match.group(1)) if p_match else 1.0
        q = float(q_match.group(1)) if q_match else 1.0
        
        if gold or diamond:
            result = solver.solve(gold, diamond, p, q)
            print(format_report(result))
        elif "历史" in text:
            history = persistence.load_history()
            print(format_history(history))
        elif "价格" in text:
            prices = persistence.load_base_prices()
            print(format_base_prices(prices))
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
