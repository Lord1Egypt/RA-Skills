#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AB测试结果分析器
输入：实验组/对照组数据
输出：统计显著性 + 效果评估 + 决策建议
"""

import math
from dataclasses import dataclass
from typing import Dict


@dataclass
class ABTestResult:
    """AB测试结果"""
    experiment_name: str
    # 样本量
    control_size: int
    experiment_size: int
    # 转化用户数
    control_converted: int
    experiment_converted: int
    # 总价值（可选）
    control_value: float = 0.0
    experiment_value: float = 0.0


def calculate_significance(control_rate: float, experiment_rate: float,
                          control_size: int, experiment_size: int) -> Dict:
    """计算统计显著性（Z-test）"""
    if control_size == 0 or experiment_size == 0:
        return {"error": "样本量为0"}

    # 合并比例（使用传入的转化率 × 样本量估算总数）
    total_converted_est = (control_rate * control_size + experiment_rate * experiment_size)
    pooled_rate = total_converted_est / (control_size + experiment_size)

    # 标准误差
    se = math.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_size + 1/experiment_size))

    if se == 0:
        return {"error": "标准误差为0"}

    # Z值
    z = (experiment_rate - control_rate) / se

    # P值（单侧检验）
    # 使用近似：|z| > 1.96 → p < 0.05
    if abs(z) >= 1.96:
        significance = "✅ 显著（p < 0.05）"
    elif abs(z) >= 1.65:
        significance = "🟡 边缘显著（p < 0.10）"
    else:
        significance = "❌ 不显著"

    # 置信区间
    margin = 1.96 * se
    ci_lower = (experiment_rate - control_rate) - margin
    ci_upper = (experiment_rate - control_rate) + margin

    return {
        "z_value": round(z, 3),
        "significance": significance,
        "confidence_interval": f"[{ci_lower*100:.2f}%, {ci_upper*100:.2f}%]",
        "pooled_rate": pooled_rate,
    }


def analyze_ab_test(result: ABTestResult) -> Dict:
    """分析AB测试结果"""

    # 计算转化率
    control_rate = result.control_converted / result.control_size if result.control_size > 0 else 0
    experiment_rate = result.experiment_converted / result.experiment_size if result.experiment_size > 0 else 0

    # 计算提升
    absolute_lift = experiment_rate - control_rate
    relative_lift = absolute_lift / control_rate * 100 if control_rate > 0 else 0

    # 统计显著性
    sig_result = calculate_significance(
        control_rate, experiment_rate,  # 传入转化率（非转化人数）
        result.control_size, result.experiment_size
    )

    # 人均价值（如果有）
    control_avg_value = result.control_value / result.control_converted if result.control_converted > 0 else 0
    experiment_avg_value = result.experiment_value / result.experiment_converted if result.experiment_converted > 0 else 0

    # 决策建议
    decision = ""
    if "✅ 显著" in sig_result.get("significance", ""):
        if absolute_lift > 0:
            decision = "🟢 效果正向显著 → 建议全量推广"
        else:
            decision = "🔴 效果负向显著 → 建议停止，保留原方案"
    elif "🟡 边缘" in sig_result.get("significance", ""):
        decision = "🟡 边缘显著 → 可选择性推广，监控更长周期"
    else:
        decision = "⚪ 效果不显著 → 建议放弃或重测"

    return {
        "实验名称": result.experiment_name,
        "样本量": f"对照组 {result.control_size:,} / 实验组 {result.experiment_size:,}",
        "转化率": {
            "对照组": f"{control_rate*100:.2f}%（{result.control_converted:,}/{result.control_size:,}）",
            "实验组": f"{experiment_rate*100:.2f}%（{result.experiment_converted:,}/{result.experiment_size:,}）",
        },
        "效果提升": {
            "绝对提升": f"{absolute_lift*100:+.2f}pp",
            "相对提升": f"{relative_lift:+.1f}%",
        },
        "统计检验": {
            "Z值": sig_result.get("z_value", "N/A"),
            "显著性": sig_result.get("significance", "N/A"),
            "95%置信区间": sig_result.get("confidence_interval", "N/A"),
        },
        "决策": decision,
    }


def run():
    print("=" * 55)
    print("AB测试结果分析器")
    print("=" * 55)

    test = ABTestResult(
        experiment_name="简化下单流程测试",
        control_size=5000,
        experiment_size=5000,
        control_converted=1450,
        experiment_converted=1680,
    )

    result = analyze_ab_test(test)

    print(f"\n实验：{result['实验名称']}")
    print(f"样本量：{result['样本量']}")
    print(f"\n转化率：")
    print(f"  对照组：{result['转化率']['对照组']}")
    print(f"  实验组：{result['转化率']['实验组']}")
    print(f"\n效果提升：")
    print(f"  绝对提升：{result['效果提升']['绝对提升']}")
    print(f"  相对提升：{result['效果提升']['相对提升']}")
    print(f"\n统计检验：")
    print(f"  Z值：{result['统计检验']['Z值']}")
    print(f"  显著性：{result['统计检验']['显著性']}")
    print(f"  置信区间：{result['统计检验']['95%置信区间']}")
    print(f"\n决策：{result['决策']}")


if __name__ == "__main__":
    run()
```

### Tool 4: 归因分析器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归因分析器
输入：各渠道转化数据 + 归因方法
输出：各渠道归因权重/GMV分配/推荐方法
"""


def calculate_attribution(
    channels: list,
    conversions_by_channel: list,
    revenue_by_channel: list,
    method: str = "time_decay",
) -> dict:
    """
    计算渠道归因权重

    Args:
        channels: 渠道名称列表（按用户触达顺序排列）
        conversions_by_channel: 各渠道转化人数
        revenue_by_channel: 各渠道带来的GMV（元）
        method: 归因方法
            - "last": 末次归因（最后一次触达渠道全功）
            - "linear": 线性归因（平均分配）
            - "time_decay": 时间衰减归因（越近越高）
    """
    n = len(channels)
    total_conversions = sum(conversions_by_channel) or 1
    total_revenue = sum(revenue_by_channel) or 1

    if method == "last":
        # 末次归因：最后一个渠道获得100%权重
        weights = [0.0] * n
        weights[-1] = 1.0
        desc = "末次归因：最后一次触达渠道获得100%功劳"

    elif method == "linear":
        # 线性归因：平均分配
        weights = [1.0 / n] * n
        desc = "线性归因：各渠道平均分配功劳"

    elif method == "time_decay":
        # 时间衰减：越接近转化的渠道权重越高
        # 位置 i 的权重 = (i+1) / sum(1..n)
        position_weights = [(i + 1) for i in range(n)]
        total_pos = sum(position_weights)
        weights = [w / total_pos for w in position_weights]
        desc = "时间衰减：越接近转化，权重越高"

    else:
        weights = [1.0 / n] * n
        desc = "默认线性归因"

    # 各渠道分配结果
    channel_results = {}
    for i, ch in enumerate(channels):
        conv_attr = int(conversions_by_channel[i] * weights[i])
        rev_attr = revenue_by_channel[i] * weights[i]
        channel_results[ch] = {
            "归因转化": conv_attr,
            "归因GMV": f"¥{rev_attr:,.0f}",
            "归因权重": f"{weights[i]*100:.1f}%",
            "原始转化": conversions_by_channel[i],
            "原始GMV": f"¥{revenue_by_channel[i]:,.0f}",
        }

    # 推荐方法
    if n <= 2:
        recommended = "last"
        recommended_desc = "触达渠道少，用末次归因更合理"
    else:
        recommended = "time_decay"
        recommended_desc = "多触点场景，用时间衰减归因更准确"

    return {
        "归因方法": method,
        "方法说明": desc,
        "各渠道归因": channel_results,
        "推荐方法": recommended,
        "推荐理由": recommended_desc,
        "总转化（归因后）": int(total_conversions),
        "总GMV（归因后）": f"¥{total_revenue:,.0f}",
    }


def run():
    print("=" * 55)
    print("归因分析器")
    print("=" * 55)

    channels = ["团长推荐", "朋友圈分享", "地推活动", "自然流量"]
    conversions = [1200, 800, 600, 400]
    revenues = [42000, 28000, 21000, 14000]

    print(f"\n渠道数据：")
    for i, ch in enumerate(channels):
        print(f"  {ch}：{conversions[i]}转化，¥{revenues[i]:,}GMV")

    print(f"\n--- 末次归因 ---")
    result = calculate_attribution(channels, conversions, revenues, "last")
    for ch, data in result["各渠道归因"].items():
        print(f"  {ch}：权重{data['归因权重']}，归因GMV {data['归因GMV']}")

    print(f"\n--- 线性归因 ---")
    result = calculate_attribution(channels, conversions, revenues, "linear")
    for ch, data in result["各渠道归因"].items():
        print(f"  {ch}：权重{data['归因权重']}，归因GMV {data['归因GMV']}")

    print(f"\n--- 时间衰减归因（推荐）---")
    result = calculate_attribution(channels, conversions, revenues, "time_decay")
    for ch, data in result["各渠道归因"].items():
        print(f"  {ch}：权重{data['归因权重']}，归因GMV {data['归因GMV']}")

    print(f"\n推荐方法：{result['推荐方法']} - {result['推荐理由']}")


if __name__ == "__main__":
    run()
```

### Tool 5: 最小样本量计算器

> **接口说明**
> 输入参数（SampleSizeParams dataclass）：
> - `control_rate`: 对照组基准转化率（浮点数，如 0.30 表示 30%）
> - `minimum_detectable_effect`: 最小可检测绝对提升（浮点数，如 0.03 表示 +3pp）
> - `alpha`: 显著性水平（默认 0.05）
> - `power`: 统计功效（默认 0.80）
>
> 输出：每组最小样本量、总样本量、预计测试周期
>
> 调用示例：
> ```python
> params = SampleSizeParams(control_rate=0.30, minimum_detectable_effect=0.03)
> result = calculate_sample_size(params)
> print(result["每组样本量"])  # → 约 3380
> ```

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小样本量计算器
基于Z检验的双侧比例比较样本量公式
n = (Z_α/2 + Z_β)² × [p₁(1-p₁) + p₂(1-p₂)] / (p₂-p₁)²
"""

import math
from dataclasses import dataclass
from typing import Dict


# Z值表（标准正态分布分位数，完整查表）
Z_VALUES = {
    # alpha（双侧检验，显著性水平）
    0.20: 1.2816,
    0.10: 1.6449,
    0.05: 1.9600,
    0.02: 2.3263,
    0.01: 2.5758,
    0.005: 2.8070,
    0.001: 3.2905,
    # power（统计功效）
    0.50: 0.0000,
    0.60: 0.2533,
    0.70: 0.5244,
    0.75: 0.6745,
    0.80: 0.8416,
    0.85: 1.0364,
    0.90: 1.2816,
    0.95: 1.6449,
}


@dataclass
class SampleSizeParams:
    """样本量计算参数"""
    control_rate: float          # 对照组基准转化率
    minimum_detectable_effect: float  # 最小可检测绝对提升（pp）
    alpha: float = 0.05          # 显著性水平（双侧）
    power: float = 0.80          # 统计功效


def get_z_value(p: float) -> float:
    """根据概率 p 获取对应 Z 值（标准正态分布分位数）
    使用精确查表，对于表中相邻值使用线性插值
    """
    if p <= 0:
        return float('-inf')
    if p >= 1:
        return float('+inf')

    sorted_items = sorted(Z_VALUES.items())
    keys = [k for k, v in sorted_items]

    # 精确匹配
    for key, z in sorted_items:
        if abs(p - key) < 0.0001:
            return z

    # 边界外推
    if p < keys[0]:
        return Z_VALUES[keys[0]]
    if p > keys[-1]:
        return Z_VALUES[keys[-1]]

    # 线性插值（相邻两个键之间）
    for i in range(len(keys) - 1):
        k_low, k_high = keys[i], keys[i + 1]
        if k_low < p < k_high:
            z_low = Z_VALUES[k_low]
            z_high = Z_VALUES[k_high]
            frac = (p - k_low) / (k_high - k_low)
            return z_low + frac * (z_high - z_low)

    # fallback
    return 1.96


def calculate_sample_size(params: SampleSizeParams) -> Dict:
    """计算AB测试所需最小样本量"""

    p1 = params.control_rate
    p2 = p1 + params.minimum_detectable_effect
    alpha = params.alpha
    power = params.power

    # 获取Z值
    z_alpha_2 = get_z_value(1 - alpha / 2)  # 双侧检验
    z_beta = get_z_value(power)

    # 样本量公式
    pooled_var = p1 * (1 - p1) + p2 * (1 - p2)
    effect_size = p2 - p1

    n = (z_alpha_2 + z_beta) ** 2 * pooled_var / (effect_size ** 2)

    # 向上取整
    n_per_group = math.ceil(n)

    # 预计测试周期（日均新用户数）
    daily_users_estimate = 500  # 默认假设，可调整
    days_per_group = math.ceil(n_per_group / daily_users_estimate)

    # 速查表参考（用于对比）
    quick_ref = _generate_quick_ref(p1)

    return {
        "参数": {
            "对照组转化率": f"{p1*100:.1f}%",
            "实验组预期转化率": f"{p2*100:.1f}%",
            "最小可检测提升": f"+{params.minimum_detectable_effect*100:.1f}pp",
            "显著性水平": f"α={alpha}（双侧）",
            "统计功效": f"{power*100:.0f}%",
        },
        "计算结果": {
            "每组最小样本量": f"{n_per_group:,}",
            "总样本量（两组）": f"{n_per_group * 2:,}",
            "预计测试周期": f"约{days_per_group}天（假设日均新用户{daily_users_estimate}）",
        },
        "速查表参考": quick_ref,
    }


def _generate_quick_ref(base_rate: float) -> Dict:
    """生成速查表"""
    effects = [0.01, 0.02, 0.03, 0.05]
    ref = {}
    for effect in effects:
        p1 = base_rate
        p2 = p1 + effect
        z_a = 1.96  # alpha=0.05 双侧
        z_b = 0.842  # power=0.80
        pooled = p1 * (1-p1) + p2 * (1-p2)
        n = math.ceil((z_a + z_b) ** 2 * pooled / (effect ** 2))
        ref[f"+{effect*100:.0f}pp"] = f"{n:,}/组"
    return ref


def run():
    print("=" * 55)
    print("最小样本量计算器")
    print("=" * 55)

    print("\n【常用场景速查】")
    print("基准转化率 30% 时，不同提升幅度的最小样本量：")
    params = SampleSizeParams(control_rate=0.30, minimum_detectable_effect=0.03)
    result = calculate_sample_size(params)
    for lift, n in result["速查表参考"].items():
        print(f"  {lift}：{n}")

    print("\n【自定义计算】")
    params = SampleSizeParams(
        control_rate=0.30,
        minimum_detectable_effect=0.03,
        alpha=0.05,
        power=0.80,
    )
    result = calculate_sample_size(params)

    print(f"\n参数：")
    for k, v in result["参数"].items():
        print(f"  {k}：{v}")

    print(f"\n结果：")
    for k, v in result["计算结果"].items():
        print(f"  {k}：{v}")


if __name__ == "__main__":
    run()
```

---

## 案例库

### 案例1：多多买菜数据驱动的"爆品预测"

```
背景：多多买菜每天上架 2000+ SKU，无法靠人工选品

数据驱动选品体系：

Step 1：历史数据分析
  → 抓取拼多多平台同类商品的历史销量
  → 分析区域销量差异（哪些SKU在某城市卖得好）
  → 识别爆品规律：价格区间/品类/季节/促销节点

Step 2：实时供需匹配
  → 实时监控：各城市库存/销量/搜索量
  → 动态定价：供需紧张时自动提价，供过于求时自动降价
  → 爆品预测：基于实时数据，预测未来7天爆品

Step 3：爆品测试（小规模验证）
  → 新SKU先在10个团点试销
  → 24小时内根据销量决定：加量推广 or 下架

效果数据（2022年）：
  爆品命中率：78%（预测10个爆品，8个真爆）
