# 运筹优化问题分类与建模参考

## 1. 数学规划类

### 1.1 线性规划 (LP)

**标准形式：**
```latex
\min \quad & \mathbf{c}^T \mathbf{x} \\
\text{s.t.} \quad & \mathbf{A}\mathbf{x} \leq \mathbf{b} \\
& \mathbf{x} \geq \mathbf{0}
```

**决策变量：** 连续变量 $x_j \geq 0$
**特征：** 目标函数和约束均为线性

### 1.2 整数规划 (IP) / 混合整数规划 (MIP)

**决策变量：** $x_j \in \mathbb{Z}$（纯整数）或 $x_j \in \mathbb{R}$（混合）

**0-1背包变体：**
```latex
\max \quad & \sum_{j=1}^{n} p_j x_j \\
\text{s.t.} \quad & \sum_{j=1}^{n} w_j x_j \leq W \\
& x_j \in \{0, 1\}
```

### 1.3 非线性规划 (NLP)

**非凸NLP：**
```latex
\min \quad & f(\mathbf{x}) \\
\text{s.t.} \quad & g_i(\mathbf{x}) \leq 0, \quad i = 1, \ldots, m \\
& h_j(\mathbf{x}) = 0, \quad j = 1, \ldots, p
```

**特殊非线性形式：**
- 二次规划 (QP)：$f(\mathbf{x}) = \mathbf{x}^T \mathbf{Q} \mathbf{x} + \mathbf{c}^T \mathbf{x}$
- 几何规划 (GP)
- 半定规划 (SDP)

---

## 2. 组合优化类

### 2.1 旅行商问题 (TSP)

**经典TSP：**
```latex
\min \quad & \sum_{i} \sum_{j} d_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{j} x_{ij} = 1, \quad \forall i \quad & \text{(每个点离开一次)} \\
& \sum_{i} x_{ij} = 1, \quad \forall j \quad & \text{(每个点进入一次)} \\
& \sum_{i \in S} \sum_{j \in S} x_{ij} \leq |S| - 1, \quad \forall S \subset \{2,\ldots,n\} \quad & \text{(子回路消除)} \\
& x_{ij} \in \{0, 1\}
```

### 2.2 车辆路径问题 (VRP)

**CVRP（容量约束VRP）：**
```latex
\min \quad & \sum_{i} \sum_{j} d_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{j} x_{ij} = 1, \quad \forall i \in C \quad & \text{(每个客户被访问一次)} \\
& \sum_{i} x_{i0} = K \quad & \text{(车辆从仓库出发)} \\
& \sum_{i} x_{0i} = K \quad & \text{(车辆返回仓库)} \\
& \sum_{i} q_i \sum_{j} x_{ij} \leq Q, \quad \forall k \quad & \text{(容量约束)} \\
& \text{子回路约束}
```

**变体：** VRPTW（带时间窗）、VRPPD（带取送货）、VRPPDSTW

### 2.3 装箱问题 (Bin Packing)

```latex
\min \quad & \sum_{k=1}^{K} y_k \\
\text{s.t.} \quad & \sum_{i=1}^{n} w_i x_{ik} \leq W, \quad \forall k \quad & \text{(每个箱子容量)} \\
& \sum_{k=1}^{K} x_{ik} = 1, \quad \forall i \quad & \text{(每个物品放入一个箱子)} \\
& x_{ik} \in \{0, 1\}, \quad y_k \in \{0, 1\}
```

### 2.4 调度问题 (Scheduling)

**Job Shop调度：**
```latex
\min \quad & C_{\max} \quad \text{(最大完工时间)} \\
\text{s.t.} \quad & s_{ij} + p_{ij} \leq s_{i'j} \quad \text{或} \quad s_{i'j} + p_{i'j} \leq s_{ij}, \quad \forall (i,j), (i',j') \in E \\
& s_{ij} \geq 0, \quad x_{ijk} \in \{0,1\}
```

---

## 3. 网络优化类

### 3.1 最短路径问题

```latex
\min \quad & \sum_{(i,j) \in E} d_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{j} x_{ij} - \sum_{j} x_{ji} =
\begin{cases} 1 & \text{若 } i = s \\ -1 & \text{若 } i = t \\ 0 & \text{其他} \end{cases} \\
& x_{ij} \in \{0, 1\}
```

### 3.2 最大流问题

```latex
\max \quad & v \\
\text{s.t.} \quad & \sum_{j} x_{ij} - \sum_{j} x_{ji} =
\begin{cases} v & \text{若 } i = s \\ -v & \text{若 } i = t \\ 0 & \text{其他} \end{cases} \\
& 0 \leq x_{ij} \leq u_{ij}, \quad \forall (i,j) \in E
```

### 3.3 最小生成树 (MST)

```latex
\min \quad & \sum_{(i,j) \in E} c_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{(i,j) \in E} x_{ij} = |V| - 1 \quad & \text{(树的结构)} \\
& \sum_{i \in S} \sum_{j \in S} x_{ij} \leq |S| - 1, \quad \forall S \subset V \quad & \text{(无环)} \\
& x_{ij} \in \{0, 1\}
```

### 3.4 网络选址问题

**P-中位问题：**
```latex
\min \quad & \sum_{i} \sum_{j} d_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{j} x_{ij} = 1, \quad \forall i \quad & \text{(每个需求点被服务)} \\
& \sum_{j} y_j = P \quad & \text{(选择P个设施)} \\
& x_{ij} \leq y_j, \quad \forall i, j \quad & \text{(只在设施点开设时才能服务)} \\
& y_j \in \{0, 1\}, \quad x_{ij} \geq 0
```

**P-中心问题：** 最小化最大距离
```latex
\min \quad & D \\
\text{s.t.} \quad & \sum_{j} x_{ij} = 1, \quad \forall i \\
& x_{ij} \leq y_j, \quad \forall i, j \\
& \sum_{j} y_j = P \\
& d_{ij} x_{ij} \leq D, \quad \forall i, j
```

---

## 4. 随机规划类

### 4.1 报童问题 (Newsvendor)

```latex
\max \quad & E[\pi(Q)] = p \cdot E[\min(Q, D)] - c \cdot Q \\
\text{或} \quad \min \quad & E[c(Q, D)] = c_o \cdot E[(Q - D)^+] + c_u \cdot E[(D - Q)^+]
```

**解析解：** $F(Q^*) = \frac{c_u}{c_o + c_u}$，其中 $F$ 是需求分布的CDF

### 4.2 两阶段随机规划

```latex
\min \quad & \mathbf{c}^T \mathbf{x} + E_\xi [Q(\mathbf{x}, \xi)] \\
\text{s.t.} \quad & \mathbf{A}\mathbf{x} \leq \mathbf{b} \\
& \mathbf{x} \geq \mathbf{0}
```
其中 $Q(\mathbf{x}, \xi) = \min \{ \mathbf{q}^T \mathbf{y} : \mathbf{W}\mathbf{y} \geq \mathbf{h} - \mathbf{T}\mathbf{x} \}$

### 4.3 随机库存问题 (s,S 策略)

```latex
\min \quad & K \cdot E[N(Q)] + h \cdot E[I(Q)] + p \cdot E[B(Q)]
```
其中 $N(Q)$ 是补货次数，$I(Q)$ 是持有库存，$B(Q)$ 是缺货量

---

## 5. 排队论类

### 5.1 M/M/1 排队系统

**性能指标：**
```latex
\lambda & = \text{到达率} \\
\mu & = \text{服务率} \\
\rho & = \frac{\lambda}{\mu} \quad \text{(利用率)} \\
L_q & = \frac{\lambda^2}{\mu(\mu - \lambda)} \quad \text{(平均队列长度)} \\
W_q & = \frac{L_q}{\lambda} \quad \text{(平均等待时间)}
```

### 5.2 M/M/c 排队系统

```latex
P_0 & = \left[ \sum_{k=0}^{c-1} \frac{(\lambda/\mu)^k}{k!} + \frac{(\lambda/\mu)^c}{c!} \cdot \frac{1}{1-\rho} \right]^{-1} \\
L_q & = \frac{(\lambda/\mu)^c \lambda \mu}{c! (c\mu - \lambda)^2} P_0 \\
W_q & = \frac{L_q}{\lambda}
```

### 5.3 排队网络

**Jackson网络：** 产品形式解
```latex
\alpha_i = \lambda_i + \sum_{j=1}^{m} \alpha_j p_{ji}, \quad i = 1, \ldots, m
```

---

## 6. 库存优化类

### 6.1 EOQ 模型（经济订货批量）

```latex
TC(Q) & = \frac{D}{Q} K + cD + \frac{Q}{2} h \\
Q^* & = \sqrt{\frac{2K D}{h}}
```

**带补货率的EOQ：**
```latex
Q^* = \sqrt{\frac{2KD}{h} \cdot \frac{\mu}{\mu - \lambda}}
```

### 6.2 多产品库存问题

```latex
\min \quad & \sum_{i=1}^{n} \left( \frac{D_i}{Q_i} K_i + \frac{Q_i}{2} h_i \right) \\
\text{s.t.} \quad & \sum_{i=1}^{n} A_i Q_i \leq W \quad & \text{(仓库空间约束)}
```

### 6.3 随机库存问题

**(s,Q) 策略：**
```latex
\min \quad & K \cdot E[N] + h \cdot E[I] + p \cdot E[B] \\
\text{s.t.} \quad & \text{订单点 } s \leq \text{订单量 } Q
```

---

## 7. 可靠性与维护类

### 7.1 预防性维护优化

```latex
\min \quad & C_p \cdot N_p + C_u \cdot P_u(T) \\
\text{s.t.} \quad & \text{可用度 } A = \frac{T - \text{维护时间}}{T} \geq A_{\min}
```

### 7.2 串联系统可靠性

```latex
R_s = \prod_{i=1}^{n} R_i(t) \quad \text{(每个组件独立)}
```

**组件冗余优化：**
```latex
\max \quad & R_{\text{system}} = 1 - \prod_{i=1}^{n} (1 - R_i) \\
\text{s.t.} \quad & \sum_{i=1}^{n} c_i x_i \leq B \\
& x_i \in \{0, 1, 2, \ldots\}
```

---

## 8. 决策分析类

### 8.1 贝叶斯决策

```latex
\max_{a} \quad & E[\pi(a, \theta) | \text{数据}] = \int \pi(a, \theta) p(\theta | \text{数据}) d\theta
```

### 8.2 马尔可夫决策过程 (MDP)

```latex
V^*(s) & = \max_{a} \left[ R(s, a) + \gamma \sum_{s'} P(s'|s, a) V^*(s') \right] \\
\pi^*(s) & = \arg\max_{a} \left[ R(s, a) + \gamma \sum_{s'} P(s'|s, a) V^*(s') \right]
```

**无限阶段折扣 MDP：**

---

## 9. 博弈论类

### 9.1 矩阵博弈（二人零和）

```latex
\max_{x} \min_{y} \quad & \mathbf{x}^T \mathbf{A} \mathbf{y} \\
\text{s.t.} \quad & \sum_{i} x_i = 1, \quad x_i \geq 0 \\
& \sum_{j} y_j = 1, \quad y_j \geq 0
```

**等价为线性规划：**
```latex
\min_{x} \quad & v \\
\text{s.t.} \quad & \sum_{i} a_{ij} x_i \geq v, \quad \forall j \\
& \sum_{i} x_i = 1, \quad x_i \geq 0
```

### 9.2 斯坦克尔伯格博弈

**领导者-追随者模型：**
```latex
\max_{x} \quad & f(x, y^*(x)) \\
\text{s.t.} \quad & g(x) \leq 0 \\
& y^*(x) = \arg\min_{y} \{ h(x, y) : k(x, y) \leq 0 \}
```

---

## 10. 随机过程类

### 10.1 马尔可夫链

**稳态概率：**
```latex
\boldsymbol{\pi} = \boldsymbol{\pi} \mathbf{P}, \quad \sum_{i} \pi_i = 1
```

**应用：** 排队系统、库存系统、可靠性系统

### 10.2 生灭过程

```latex
P\{N(t+\Delta t) = n+1 | N(t)=n\} = \lambda_n \Delta t + o(\Delta t) \\
P\{N(t+\Delta t) = n-1 | N(t)=n\} = \mu_n \Delta t + o(\Delta t)
```

---

## 11. 选址问题类

### 11.1 集合覆盖问题

```latex
\min \quad & \sum_{j \in J} c_j y_j \\
\text{s.t.} \quad & \sum_{j \in J: i \in N_j} y_j \geq 1, \quad \forall i \in I \quad & \text{(每个需求点被覆盖)} \\
& y_j \in \{0, 1\}
```

### 11.2 最大覆盖问题

```latex
\max \quad & \sum_{i \in I} d_i z_i \\
\text{s.t.} \quad & \sum_{j \in J: i \in N_j} y_j \geq z_i, \quad \forall i \in I \\
& \sum_{j \in J} y_j = P \\
& y_j \in \{0, 1\}, \quad z_i \in \{0, 1\}
```

---

## 12. 供应链优化类

### 12.1 供应链网络设计

```latex
\min \quad & \sum_{i \in I} f_i y_i + \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{i \in I} x_{ij} = d_j, \quad \forall j \quad & \text{(满足需求)} \\
& \sum_{j \in J} x_{ij} \leq M_i y_i, \quad \forall i \quad & \text{(产能约束)} \\
& x_{ij} \geq 0, \quad y_i \in \{0, 1\}
```

### 12.2 供应链协调（收益管理）

**契约模型：**
```latex
\max \quad & \text{供应商利润} \\
\text{s.t.} \quad & \text{零售商利润} \geq \text{保留利润}
```

---

## 13. 动态规划类

### 13.1 确定性动态规划

**递归方程：**
```latex
V_t(s_t) = \max_{a_t} \{ R(s_t, a_t) + \beta V_{t+1}(s_{t+1}) \}
```
其中 $s_t$ 是状态，$a_t$ 是决策，$\beta$ 是折扣因子，$R$ 是回报函数

**矩阵形式：**
```latex
\mathbf{V} = \max_{\mathbf{a}} \{ \mathbf{R}(\mathbf{s}, \mathbf{a}) + \beta \mathbf{P} \mathbf{V} \}
```

### 13.2 随机动态规划

```latex
V_t(s_t) = \max_{a_t} \left\{ R(s_t, a_t) + \gamma \sum_{s_{t+1}} P(s_{t+1} | s_t, a_t) V_{t+1}(s_{t+1}) \right\}
```

### 13.3 滚动时域控制（Receding Horizon）

```latex
\min_{u_k} \quad & \sum_{k=0}^{N-1} L(x_k, u_k) + J_N(x_N) \\
\text{s.t.} \quad & x_{k+1} = f(x_k, u_k), \quad k = 0, \ldots, N-1 \\
& x_k \in X, \quad u_k \in U
```

**应用：** 车辆路径动态重优化、库存滚动补货

### 13.4 多周期库存动态规划

```latex
V_t(I_t) = \max_{Q_t} \{ -c Q_t + \sum_{D} P(D) \cdot [\pi \min(I_t + Q_t, D) - h (I_t + Q_t - D)^+] + \beta V_{t+1}(I_{t+1}) \}
```

---

## 14. 鲁棒优化类

### 14.1 箱式不确定集（Box Uncertainty）

```latex
\min_{x} \quad & \max_{\xi \in \mathcal{U}} \mathbf{c}(\xi)^T \mathbf{x} \\
\text{s.t.} \quad & \mathbf{A} \mathbf{x} \leq \mathbf{b} \\
& \mathcal{U} = \{ \xi : \|\xi\|_1 \leq \Gamma \}
```

### 14.2 椭球不确定集（Ellipsoidal Uncertainty）

```latex
\min_{x} \quad & \mathbf{c}^T \mathbf{x} + \gamma \sqrt{\mathbf{x}^T \Sigma \mathbf{x}} \\
\text{s.t.} \quad & \mathbf{A} \mathbf{x} \leq \mathbf{b}
```

### 14.3 机会约束规划

```latex
\min_{x} \quad & \mathbf{c}^T \mathbf{x} \\
\text{s.t.} \quad & P\{ \mathbf{a}_i^T \mathbf{x} \leq b_i \} \geq 1 - \alpha, \quad \forall i
```

---

## 15. 机制设计类

### 15.1 拍卖理论基础

**VCG拍卖（Vickrey-Clarke-Groves）：**
```latex
\text{支付}_i = \sum_{j \neq i} v_j(\mathbf{x}^{-i}) - \sum_{j \neq i} v_j(\mathbf{x})
```
其中 $\mathbf{x}^{-i}$ 是不考虑投标者 $i$ 时的最优配置

### 15.2 双边市场匹配

**稳定匹配问题（Gale-Shapley算法对应数学规划）：**
```latex
\max \quad & \sum_{(i,j) \in E} w_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{j} x_{ij} = 1, \quad \forall i \quad & \text{(每个买家匹配一个卖家)} \\
& \sum_{i} x_{ij} = 1, \quad \forall j \quad & \text{(每个卖家匹配一个买家)} \\
& x_{ij} \in \{0, 1\}
```

### 15.3 平台定价机制

**单边平台抽成模型：**
```latex
\max_{\pi} \quad & \sum_{(i,j)} \pi \cdot \min(d_i, s_j) \\
\text{s.t.} \quad & \pi \in [\pi_{\min}, \pi_{\max}] \quad & \text{(抽成比例约束)} \\
& \text{司机效用} \geq 0 \quad & \text{(参与约束)}
```

### 15.4 激励相容约束

```latex
\max_{x, t} \quad & \sum_i t_i - c(x) \\
\text{s.t.} \quad & \sum_i x_i(\theta) \theta_i - t_i \geq \sum_i x_i(\theta'_i, \theta_{-i}) \theta_i - t_i, \quad \forall i, \theta \quad & \text{(激励相容)} \\
& \sum_i x_i(\theta) \theta_i - t_i \geq 0, \quad \forall i, \theta \quad & \text{(个人理性)}
```

---

## 16. 平台经济与共享经济类

### 16.1 共享出行匹配

**时空匹配模型：**
```latex
\max \quad & \sum_{i \in P} \sum_{j \in D} u_{ij} x_{ij} - \sum_{i \in P} c_i y_i \\
\text{s.t.} \quad & \sum_{j \in D} x_{ij} \leq 1, \quad \forall i \in P \quad & \text{(每乘客最多一辆车)} \\
& \sum_{i \in P} x_{ij} \leq 1, \quad \forall j \in D \quad & \text{(每车最多一乘客)} \\
& x_{ij} \leq z_{ij}, \quad \forall i,j \quad & \text{(时空兼容约束)} \\
& x_{ij} \in \{0, 1\}, \quad y_i \in \{0, 1\}
```

其中 $z_{ij}$ 是时空兼容性指标

### 16.2 拼车成本分摊

**核心稳定分配（Core Stability）：**
```latex
\text{寻找 } (x, p) \text{ 使得} \\
\sum_{i \in S} (v_i - p_i) \leq v(S), \quad \forall S \subset N
```

**比例公平分摊：**
```latex
p_i = \frac{c(\bigcup_{j \in S_i} j)}{|S_i|}
```
其中 $S_i$ 是与乘客 $i$ 拼车的乘客集合

### 16.3 动态定价模型

```latex
\max \quad & \sum_{t} \sum_{i} \lambda_i(t) p_i(t) - c(p_i(t)) \\
\text{s.t.} \quad & p_i(t) \in [p_{\min}, p_{\max}] \\
& \sum_i x_i(p) \leq \text{供给}(t)
```

---

## 17. 动态需求响应类

### 17.1 需求响应激励机制

**基于激励的需求响应：**
```latex
\max \quad & \sum_t B(Q(t)) - \sum_t c(Q(t)) - \sum_i I_i \\
\text{s.t.} \quad & \sum_i x_i \geq Q_{\min} \quad & \text{(响应量约束)} \\
& I_i \geq \underline{I}_i + \alpha_i x_i \quad & \text{(激励结构)} \\
& I_i \geq 0
```

### 17.2 实时调度优化

**滚动窗口优化：**
```latex
\min_{u_k} \quad & \sum_{k=0}^{H-1} [d_{k+1} - s_k]^2 + \lambda u_k^2 \\
\text{s.t.} \quad & s_{k+1} = s_k + u_k - d_k \\
& s_k \geq 0, \quad |u_k| \leq U_{\max}
```

---

## 18. 多目标优化类

### 18.1 帕累托前沿求解

**加权和法：**
```latex
\min \quad & \sum_{k=1}^K w_k f_k(x) \\
\text{s.t.} \quad & x \in X, \quad w_k > 0, \quad \sum w_k = 1
```

### 18.2 ε-约束法

```latex
\min \quad & f_1(x) \\
\text{s.t.} \quad & f_k(x) \leq \epsilon_k, \quad k = 2, \ldots, K \\
& x \in X
```

### 18.3 目标规划（Goal Programming）

```latex
\min \quad & \sum_{i=1}^n (d_i^+ + d_i^-) \\
\text{s.t.} \quad & f_i(x) + d_i^+ - d_i^- = g_i \quad & \text{(目标约束)} \\
& x \in X, \quad d_i^+, d_i^- \geq 0
```

---

## 19. 约束模块速查表

| 模块 | LaTeX | 适用场景 |
|------|-------|---------|
| 容量约束 | $\sum_j x_{ij} \leq Q_j y_j$ | 车辆、人员、仓库容量 |
| 时间窗(硬) | $ET_i \leq t_i \leq LT_i$ | 配送、服务窗口 |
| 时间窗(软) | $\min t_i - LT_i$ (惩罚) | 可延误的配送 |
| 唯一分配 | $\sum_j x_{ij} = 1$ | 每个人只被服务一次 |
| 路线连续 | $\sum_i x_{ij} = \sum_i x_{ji}$ | 车辆路线无中断 |
| 绕行容忍 | $d_{ij} \leq (1+\alpha)d_{ij}^*$ | 合乘、拼车 |
| 互斥 | $x_i + x_j \leq 1$ | 不能同时选择 |
| 条件激活 | $x_j \leq M y_j$ | if-then 逻辑 |
| 流平衡 | $\sum_j f_{ij} - \sum_j f_{ji} = b_i$ | 网络流问题 |
| 机会约束 | $P\{x \geq D\} \geq 1-\alpha$ | 随机需求 |
| 多目标 | $\min \sum w_k f_k(x)$ | 多准则决策 |
| 鲁棒约束 | $\max_{\xi \in \mathcal{U}} a(\xi)^T x \leq b$ | 不确定性 |

---

## 建模符号约定

### 通用符号

| 符号 | 含义 |
|------|------|
| $x_j$ | 决策变量（连续） |
| $y_j$ | 决策变量（二进制/整数） |
| $z_{ij}$ | 决策变量（网络流等） |
| $c_j$ 或 $\mathbf{c}$ | 目标函数系数（成本/收益） |
| $a_{ij}$ 或 $\mathbf{A}$ | 约束矩阵 |
| $b_i$ 或 $\mathbf{b}$ | 约束右端项 |
| $d_j$ | 需求 |
| $s_i$ | 供应量 |
| $u_{ij}$ | 容量上限 |
| $w_j$ | 权重 |
| $\lambda$ | 到达率/需求率 |
| $\mu$ | 服务率 |

### 集合符号

| 符号 | 含义 |
|------|------|
| $I, J$ | 集合索引 |
| $S \subset V$ | 子集 |
| $N(i)$ | 节点 $i$ 的邻域 |
| $\delta(S)$ | 集合 $S$ 的边界边 |

### 运算符

| 符号 | 含义 |
|------|------|
| $\min/\max$ | 最小化/最大化 |
| $\text{s.t.}$ | subject to（约束条件） |
| $\forall$ | 对于所有 |
| $\in$ | 属于 |
| $\leq, \geq, =$ | 约束关系 |
| $[x]^+$ | $\max(0, x)$ |

---

## 常见建模技巧

### 大M法（消除逻辑约束）
```latex
y \in \{0,1\}, \quad x \leq M y \quad \Rightarrow \quad x \leq My
```

### 线性化技巧

**乘积项 $x \cdot y$（均为0-1）：**
```latex
w = xy \quad \Rightarrow \quad
w \leq x, \quad w \leq y, \quad w \geq x + y - 1, \quad w \in \{0,1\}
```

**绝对值 $|x|$：**
```latex
|x| = x^+ + x^-, \quad x = x^+ - x^-, \quad x^+, x^- \geq 0
```

**分段线性函数：**
```latex
f(x) = \sum_{k=1}^{K} \alpha_k x_k, \quad x = \sum_{k=1}^{K} x_k, \quad x_k \in [L_k, U_k]
```

### 弱化/增强约束

**子回路约束的MTZ formulation：**
```latex
u_i - u_j + 1 \leq (n-1)(1-x_{ij}), \quad \forall i,j, i \neq j
```

**流量守恒约束：**
```latex
\sum_{j} x_{ij} = \sum_{j} x_{ji}, \quad \forall i \text{（中间节点）}
```
