"""
四象限分类 + 规则匹配 Python 代码
供标准模型直接复制执行
"""


def classify_quadrant(sell_through_rate, stock_to_sales_ratio, on_market_days,
                      str_threshold=0.40, ssr_threshold=0.5):
    """
    四象限分类 + 生命周期修正

    输入：
      sell_through_rate: float, 售罄率（0~1）
      stock_to_sales_ratio: float, 库销比
      on_market_days: int, 到店天数
    输出：
      quadrant, signal, action
    """
    if sell_through_rate >= str_threshold and stock_to_sales_ratio < ssr_threshold:
        quadrant, signal, action = "Q1: 健康/热销", "🟢", "维持或考虑补货"
    elif sell_through_rate >= str_threshold and stock_to_sales_ratio >= ssr_threshold:
        quadrant, signal, action = "Q2: 过季尾货", "🟡", "促销清尾"
    elif sell_through_rate < str_threshold and stock_to_sales_ratio >= ssr_threshold:
        quadrant, signal, action = "Q3: 滞销积压", "🔴", "深度促销/退仓/转渠道"
    else:
        quadrant, signal, action = "Q4: 新品/观察", "🟡", "观察动销趋势"

    # 生命周期修正
    if on_market_days <= 30:
        if signal == "🔴":
            signal = "🟡"
            action = "新品期，暂观察"
            quadrant += "（新品修正：🔴→🟡）"
    elif on_market_days >= 90:
        if signal == "🟡" and sell_through_rate < str_threshold:
            signal = "🔴"
            action = "到店超90天仍滞销，升级为红灯"
            quadrant += "（成熟修正：🟡→🔴）"

    return quadrant, signal, action


def batch_classify(categories_data):
    """批量分类所有品类"""
    results = {"🔴": [], "🟡": [], "🟢": [], "🟢⚡": []}

    for cat in categories_data:
        quadrant, signal, action = classify_quadrant(
            cat["sell_through_rate"],
            cat["stock_to_sales_ratio"],
            cat.get("on_market_days", 60)
        )

        cat_result = {**cat, "quadrant": quadrant, "signal": signal, "action": action}

        if signal == "🟢" and cat.get("stock_to_sales_ratio", 1) < 0.15:
            signal = "🟢⚡"
            cat_result["signal"] = "🟢⚡"
            cat_result["action"] = "热销但库存极低，紧急补货"

        results[signal].append(cat_result)

    return results


def match_action_rules(classified_results):
    """对每个问题品类匹配行动规则"""
    action_plans = []

    for cat in classified_results.get("🔴", []):
        str_val = cat.get("sell_through_rate", 0)
        days = cat.get("on_market_days", 0)
        stock_value = cat.get("stock_mtv", 0)
        discount = cat.get("discount_rate", 1.0)

        if str_val < 0.20 and days > 60:
            if discount > 0.5:
                action = f"建议加大促销至 {max(0.3, discount - 0.2):.0%}"
            else:
                action = "当前已深折，考虑退仓/打包清仓"
            priority = "P0"
        elif str_val < 0.40:
            action = f"建议 {max(0.5, discount - 0.15):.0%} 促销"
            priority = "P1"
        else:
            action = "持续观察"
            priority = "P2"

        action_plans.append({
            "category": cat.get("category", ""),
            "signal": "🔴", "action": action, "priority": priority,
        })

    for cat in classified_results.get("🟢⚡", []):
        daily_sales = cat.get("retail_qty_daily", 0)
        stock_qty = cat.get("stock_qty", 0)
        days_remaining = stock_qty / daily_sales if daily_sales > 0 else 999

        if days_remaining < 7:
            action = f"紧急补货！建议 {daily_sales * 30:.0f} 件（30天量）"
            priority = "P0"
        else:
            action = f"建议补货 {daily_sales * 21:.0f} 件"
            priority = "P1"

        action_plans.append({
            "category": cat.get("category", ""),
            "signal": "🟢⚡", "action": action, "priority": priority,
        })

    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    action_plans.sort(key=lambda x: priority_order.get(x["priority"], 99))
    return action_plans
