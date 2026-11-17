# 常用数学建模算法速查

> 本文档整理数学建模竞赛中最高频使用的算法及其 Python 实现框架，供专家快速调用。

---

## 一、优化类问题

### 1.1 线性规划（Linear Programming）

**适用场景**：资源分配、运输问题、生产计划等目标函数和约束均为线性的问题。

**Python 实现**：
```python
from scipy.optimize import linprog

# 标准形式: min c^T x, s.t. A_ub x <= b_ub, A_eq x = b_eq, bounds
c = [-1, -2]              # 目标函数系数（注意负号表示求max）
A_ub = [[1, 1], [2, 1]]   # 不等式约束系数矩阵
b_ub = [5, 8]             # 不等式约束右端
bounds = [(0, None), (0, None)]  # 变量范围

result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
print(f"最优值: {-result.fun}, 最优解: {result.x}")
```

### 1.2 整数规划 / 0-1 规划

**适用场景**：选址问题、指派问题、背包问题。

**Python 实现（PuLP）**：
```python
from pulp import *

prob = LpProblem("IP_Problem", LpMinimize)
x = LpVariable.dicts("x", range(5), cat='Binary')  # 0-1变量

prob += lpSum([c[i] * x[i] for i in range(5)])
prob += lpSum([a[i] * x[i] for i in range(5)]) >= b

prob.solve()
print(f"最优值: {value(prob.objective)}")
```

### 1.3 非线性规划

**适用场景**：参数估计、曲线拟合、最优控制。

```python
from scipy.optimize import minimize

def objective(x):
    return x[0]**2 + x[1]**2  # 目标函数

def constraint(x):
    return x[0] + x[1] - 1    # 约束: x[0] + x[1] >= 1

cons = {'type': 'ineq', 'fun': constraint}
bounds = [(-10, 10), (-10, 10)]

result = minimize(objective, x0=[0, 0], bounds=bounds, constraints=cons)
print(result.x)
```

---

## 二、微分方程模型

### 2.1 ODE（常微分方程）

**适用场景**：传染病模型(SIR)、种群增长、物理运动、化学反应动力学。

```python
from scipy.integrate import solve_ivp

def sir_model(t, y, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

sol = solve_ivp(sir_model, [0, 100], [0.99, 0.01, 0], 
                args=(0.3, 0.1), max_step=0.1)
```

### 2.2 PDE（偏微分方程）

**适用场景**：热传导、波动方程、扩散模型。

```python
import numpy as np
# 有限差分法求解一维热传导方程
def heat_1d_fdm(u0, alpha, dx, dt, nt):
    nx = len(u0)
    u = u0.copy()
    r = alpha * dt / dx**2
    for n in range(nt):
        u_new = u.copy()
        for i in range(1, nx-1):
            u_new[i] = u[i] + r * (u[i+1] - 2*u[i] + u[i-1])
        u = u_new
    return u
```

---

## 三、统计与回归模型

### 3.1 线性回归 / 多元回归

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"R² = {r2_score(y_test, y_pred):.4f}")
print(f"MSE = {mean_squared_error(y_test, y_pred):.4f}")
print(f"系数: {model.coef_}, 截距: {model.intercept_}")
```

### 3.2 逻辑回归（分类问题）

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

### 3.3 主成分分析（PCA）

**适用场景**：降维、指标综合评价、消除多重共线性。

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=0.95)  # 保留95%方差
X_pca = pca.fit_transform(X_scaled)
print(f"保留主成分数: {pca.n_components_}")
print(f"各主成分贡献率: {pca.explained_variance_ratio_}")
```

---

## 四、评价与决策模型

### 4.1 层次分析法（AHP）

```python
import numpy as np

def ahp_weight(comparison_matrix):
    """AHP法计算权重"""
    eigvals, eigvecs = np.linalg.eig(comparison_matrix)
    max_eigval = np.max(eigvals.real)
    max_eigvec = eigvecs[:, np.argmax(eigvals.real)].real
    weights = max_eigvec / np.sum(max_eigvec)
    
    n = len(comparison_matrix)
    CI = (max_eigval - n) / (n - 1)
    RI_dict = {1:0, 2:0, 3:0.58, 4:0.90, 5:1.12, 6:1.24, 7:1.32, 8:1.41}
    CR = CI / RI_dict[n]
    return weights, CR
```

### 4.2 TOPSIS 法

```python
def topsis(data, weights, criteria_types):
    """
    data: 原始数据矩阵
    weights: 权重向量
    criteria_types: 1表示效益型，-1表示成本型
    """
    norm_data = data / np.sqrt((data**2).sum(axis=0))
    weighted = norm_data * weights
    ideal_best = np.where(criteria_types==1, weighted.max(axis=0), weighted.min(axis=0))
    ideal_worst = np.where(criteria_types==1, weighted.min(axis=0), weighted.max(axis=0))
    d_best = np.sqrt(((weighted - ideal_best)**2).sum(axis=1))
    d_worst = np.sqrt(((weighted - ideal_worst)**2).sum(axis=1))
    scores = d_worst / (d_best + d_worst)
    return scores
```

---

## 五、预测模型

### 5.1 时间序列模型（ARIMA）

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(data, order=(p, d, q))
fitted = model.fit()
forecast = fitted.forecast(steps=10)
print(fitted.summary())
```

### 5.2 灰色预测 GM(1,1)

```python
def gm11(data, predict_n=5):
    """GM(1,1)灰色预测模型"""
    x0 = np.array(data, dtype=float)
    x1 = np.cumsum(x0)
    z1 = (x1[:-1] + x1[1:]) / 2.0
    B = np.column_stack([-z1, np.ones(len(z1))])
    Y = x0[1:]
    a, b = np.linalg.inv(B.T @ B) @ B.T @ Y
    pred = [(x0[0] - b/a) * (1 - np.exp(a)) * np.exp(-a*k) for k in range(len(x0)+predict_n)]
    return pred
```

### 5.3 BP 神经网络

```python
from sklearn.neural_network import MLPRegressor

model = MLPRegressor(hidden_layer_sizes=(64, 32), activation='relu',
                     max_iter=1000, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

---

## 六、图论与网络模型

### 6.1 最短路（Dijkstra）

```python
import networkx as nx

G = nx.DiGraph()  # 有向图
G.add_weighted_edges_from([(1, 2, 3), (1, 3, 7), (2, 3, 2)])
path = nx.shortest_path(G, source=1, target=3, weight='weight')
length = nx.shortest_path_length(G, source=1, target=3, weight='weight')
```

### 6.2 最小生成树 / TSP 问题

```python
mst = nx.minimum_spanning_tree(G)
# TSP 用启发式方法
from python_tsp.heuristics import solve_tsp_simulated_annealing
```

---

## 七、聚类分析

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

model = KMeans(n_clusters=3, random_state=42)
labels = model.fit_predict(X)
score = silhouette_score(X, labels)
```

---

## 八、蒙特卡洛模拟

```python
import numpy as np

def monte_carlo_pi(n):
    """蒙特卡洛方法估计圆周率"""
    points = np.random.uniform(-1, 1, (n, 2))
    inside = np.sum(points[:,0]**2 + points[:,1]**2 <= 1)
    return 4 * inside / n
```

---

## 九、数据预处理常用方法

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

# 缺失值处理
df.fillna(df.mean(), inplace=True)
df.interpolate(method='linear', inplace=True)

# 标准化
scaler = StandardScaler()
X_std = scaler.fit_transform(X)

# 归一化
scaler = MinMaxScaler()
X_norm = scaler.fit_transform(X)

# 异常值检测（IQR法）
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
outliers = (df < (Q1 - 1.5*IQR)) | (df > (Q3 + 1.5*IQR))
```

---

> **使用建议**：根据题目特点选择模型，优先使用经典成熟的方法（如线性规划、回归、ODE），在有充分理由时才选用复杂的机器学习方法。建模的核心在于对问题的理解和模型的恰当选择，而非堆砌复杂算法。
