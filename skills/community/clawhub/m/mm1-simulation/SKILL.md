---
name: 队列模拟服务
description: 一个用于M/M/1和M/M/c队列系统模拟和分析的Model Context Protocol服务器，提供全面的资源、工具和提示。
version: 1.0.0
---

# 队列模拟服务

一个用于M/M/1和M/M/c队列系统模拟和分析的Model Context Protocol服务器，提供全面的资源、工具和提示。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Validate M/M/1 configuration parameters

Checks parameter validity and system stability condition.

Args:
    arrival_rate: Customer arrival rate (λ)
    service_rate: Service rate (μ)
    simulation_time: Simulation duration

Returns:
    Dictionary with validation result:
        - valid: bool
        - errors: List[str] (if any)
        - warnings: List[str] (if any)
        - utilization: float (if valid) | `scripts.tools.validate_config` |
| Calculate theoretical M/M/1 performance metrics

Uses exact formulas to compute steady-state performance.

Args:
    arrival_rate: λ (customers per time unit)
    service_rate: μ (customers per time unit)

Returns:
    Dictionary of theoretical metrics:
        - utilization: ρ = λ/μ
        - avg_queue_length: L_q = ρ²/(1-ρ)
        - avg_num_in_system: L = ρ/(1-ρ)
        - avg_waiting_time: W_q
        - avg_system_time: W

Raises:
    ValueError: If system is unstable (λ >= μ) | `scripts.tools.calculate_metrics` |
| Run M/M/1 queue simulation using SimPy

Executes discrete event simulation and returns performance metrics.

Args:
    arrival_rate: λ (customers per time unit)
    service_rate: μ (customers per time unit)
    simulation_time: Duration of simulation
    random_seed: Random seed for reproducibility

Returns:
    Dictionary with:
        - simulation_metrics: Dict of simulated values
        - theoretical_metrics: Dict of exact values
        - comparison: Comparison analysis
        - config: Simulation configuration used | `scripts.tools.run_simulation` |
| Compare simulation results with theoretical values

Analyzes accuracy of simulation by comparing against exact formulas.

Args:
    simulation_metrics: Dictionary of simulated performance metrics
    arrival_rate: λ used in simulation
    service_rate: μ used in simulation

Returns:
    Comparison analysis with:
        - comparisons: Per-metric comparison
        - mean_abs_error_pct: Average error
        - max_error_pct: Maximum error
        - within_10pct: bool
        - accuracy_grade: Quality assessment | `scripts.tools.compare_results` |
| Recommend simulation parameters for target utilization

Suggests appropriate arrival rate, service rate, and simulation time
for a given target utilization level.

Args:
    target_utilization: Desired ρ (default: 0.7)
    service_rate: Fixed μ (if None, suggests μ=10)
    min_customers: Minimum customers to simulate

Returns:
    Recommended parameters and expected metrics | `scripts.tools.recommend_parameters` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.validate_config
工具描述：Validate M/M/1 configuration parameters

Checks parameter validity and system stability condition.

Args:
    arrival_rate: Customer arrival rate (λ)
    service_rate: Service rate (μ)
    simulation_time: Simulation duration

Returns:
    Dictionary with validation result:
        - valid: bool
        - errors: List[str] (if any)
        - warnings: List[str] (if any)
        - utilization: float (if valid)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|arrival_rate|number|true| |null|
|service_rate|number|true| |null|
|simulation_time|number|false|10000.0|null|

---

## scripts.tools.calculate_metrics
工具描述：Calculate theoretical M/M/1 performance metrics

Uses exact formulas to compute steady-state performance.

Args:
    arrival_rate: λ (customers per time unit)
    service_rate: μ (customers per time unit)

Returns:
    Dictionary of theoretical metrics:
        - utilization: ρ = λ/μ
        - avg_queue_length: L_q = ρ²/(1-ρ)
        - avg_num_in_system: L = ρ/(1-ρ)
        - avg_waiting_time: W_q
        - avg_system_time: W

Raises:
    ValueError: If system is unstable (λ >= μ)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|arrival_rate|number|true| |null|
|service_rate|number|true| |null|

---

## scripts.tools.run_simulation
工具描述：Run M/M/1 queue simulation using SimPy

Executes discrete event simulation and returns performance metrics.

Args:
    arrival_rate: λ (customers per time unit)
    service_rate: μ (customers per time unit)
    simulation_time: Duration of simulation
    random_seed: Random seed for reproducibility

Returns:
    Dictionary with:
        - simulation_metrics: Dict of simulated values
        - theoretical_metrics: Dict of exact values
        - comparison: Comparison analysis
        - config: Simulation configuration used
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|arrival_rate|number|true| |null|
|service_rate|number|true| |null|
|simulation_time|number|false|10000.0|null|
|random_seed|integer|false|42.0|null|

---

## scripts.tools.compare_results
工具描述：Compare simulation results with theoretical values

Analyzes accuracy of simulation by comparing against exact formulas.

Args:
    simulation_metrics: Dictionary of simulated performance metrics
    arrival_rate: λ used in simulation
    service_rate: μ used in simulation

Returns:
    Comparison analysis with:
        - comparisons: Per-metric comparison
        - mean_abs_error_pct: Average error
        - max_error_pct: Maximum error
        - within_10pct: bool
        - accuracy_grade: Quality assessment
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|simulation_metrics|object|true| |null|
|arrival_rate|number|true| |null|
|service_rate|number|true| |null|

---

## scripts.tools.recommend_parameters
工具描述：Recommend simulation parameters for target utilization

Suggests appropriate arrival rate, service rate, and simulation time
for a given target utilization level.

Args:
    target_utilization: Desired ρ (default: 0.7)
    service_rate: Fixed μ (if None, suggests μ=10)
    min_customers: Minimum customers to simulate

Returns:
    Recommended parameters and expected metrics
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|target_utilization|number|false|0.7|null|
|service_rate|null|false| |null|
|min_customers|integer|false|1000.0|null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据