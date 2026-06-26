# 一、基本信息
1.paper：《mHC: Manifold-Constrained Hyper-Connections》

2.github：未知

3.会议：未知

# 二、文章理解
## 1. 研究背景与动机 (Motivation)
### 1.1 残差连接的演变
深度学习的成功很大程度上归功于 **残差连接 (Residual Connection)**。标准的残差连接公式为：

$ x_{l+1} = x_l + \mathcal{F}(x_l, \mathcal{W}_l) $

其中 $ x_l $ 是第 $ l $ 层的输入，$ \mathcal{F} $ 是残差函数（如 Attention 或 FFN）。这种结构保证了 **恒等映射 (Identity Mapping)** 属性，即信号可以无损地从浅层传播到深层，这是深层网络能够训练的关键。

### 1.2 Hyper-Connections (HC) 的引入
为了提升模型性能，近期的研究提出了 **Hyper-Connections (HC)**。

+ **核心思想**：扩展残差流（Residual Stream）的宽度。将特征维度从 $ C $ 扩展到 $ n \times C $（$ n $ 是扩展率）。
+ **HC 的传播公式**：

$ x_{l+1} = \mathcal{H}^{res}_l x_l + \mathcal{H}^{post \top}_l \mathcal{F}(\mathcal{H}^{pre}_l x_l, \mathcal{W}_l) $

+ 其中，$ \mathcal{H}^{res}_l \in \mathbb{R}^{n \times n} $ 是一个可学习的混合矩阵，用于在扩展后的残差流内部混合信息。

**动机：** HC 通过增加拓扑复杂度和残差流宽度提升了性能，且不显著增加 FLOPs。但随着模型规模增大，HC 暴露出了严重的稳定性问题。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/57569306/1767535158747-34ab19e4-bec9-4f80-bb38-e36d876b77d9.png)

## 2. 核心问题 (Problem Statement)
作者指出原始的 HC 存在两大核心挑战：

### 2.1 数值不稳定性 (Numerical Instability)
这是最致命的问题。在 HC 中，$ \mathcal{H}^{res}_l $ 是无约束的可学习矩阵。当网络层数加深时，信号在层间的传播由多个 $ \mathcal{H}^{res} $ 的乘积决定：

$ x_L \approx \left( \prod_{i=1}^{L-1} \mathcal{H}^{res}_{L-i} \right) x_l + \dots $

+ **信号爆炸**：由于 $ \mathcal{H}^{res} $ 没有约束，连乘后会导致信号幅度和梯度范数不受控地放大（Exploding）或消失。
+ **破坏恒等映射**：它破坏了 ResNet 最核心的“恒等映射”属性，导致大规模训练时 Loss 突然激增（Loss Spike），难以收敛。

### 2.2 系统开销 (System Overhead)
虽然 FLOPs 没怎么变，但 **显存访问 (Memory Access / IO)** 变了。

+ **IO 瓶颈**：由于残差流变宽了 $ n $ 倍，读写操作的数据量剧增（Memory Wall 问题）。
+ **通信开销**：在流水线并行（Pipeline Parallelism）中，跨阶段通信量增加了 $ n $ 倍。



## 3. 解决方法 (Methodology): mHC
DeepSeek 团队提出了 **mHC (Manifold-Constrained Hyper-Connections)**，即“流形约束的超级连接”。方案分为**数学原理**和**工程实现**两部分。

### 3.1 数学原理：流形约束与 Sinkhorn-Knopp
为了恢复“恒等映射”的稳定性，作者并没有简单地强制 $ \mathcal{H}^{res} = I $（这会失去混合信息的能力），而是将 $ \mathcal{H}^{res} $ 投影到一个特殊的流形上——**双随机矩阵 (Doubly Stochastic Matrices)**。

#### 定义与约束
将 $ \mathcal{H}^{res}_l $ 约束在 Birkhoff 多胞形 $ \mathcal{P}_{\mathcal{M}^{res}} $ 中：

$ \mathcal{P}_{\mathcal{M}^{res}}(\mathcal{H}^{res}) := \{ \mathcal{H}^{res} \in \mathbb{R}^{n \times n} \mid \mathcal{H}^{res} \mathbf{1}_n = \mathbf{1}_n, \mathbf{1}_n^\top \mathcal{H}^{res} = \mathbf{1}_n^\top, \mathcal{H}^{res} \geqslant 0 \} $

也就是说，**矩阵的每一行之和为 1，每一列之和也为 1，且元素非负**。

#### 为什么要这样做？（理论优势）
1. **范数保持 (Norm Preservation)**：双随机矩阵的谱范数有上界 $ ||\mathcal{H}^{res}||_2 \leq 1 $，这天然地防止了梯度爆炸。

:::info
定义矩阵 $ A \in \mathbb{R}^{n \times n} $ 为双随机矩阵，即满足：

1. **非负性**：$ A_{ij} \ge 0 $
2. **行和为1**：$ \sum_{j=1}^n A_{ij} = 1, \forall i $
3. **列和为1**：$ \sum_{i=1}^n A_{ij} = 1, \forall j $

我们需要证明的是谱范数 $ \|A\|_2 \le 1 $。  
注：谱范数定义为 $ \|A\|_2 = \sqrt{\lambda_{\max}(A^T A)} = \sigma_{\max}(A) $（最大奇异值）。



线性代数中有一个著名的不等式，关联了谱范数、由行和诱导的 $ \infty $-范数、由列和诱导的 $ 1 $-范数：

$ \|A\|_2 \le \sqrt{\|A\|_1 \|A\|_\infty} $

**证明步骤：**

1. **计算 **$ \infty $**-范数（最大行和）**：  
$ \|A\|_\infty = \max_{i} \sum_{j=1}^n |A_{ij}| $。  
由于 $ A $ 是非负且行和为 1 的矩阵，故：

$ \|A\|_\infty = 1 $

2. **计算 **$ 1 $**-范数（最大列和）**：  
$ \|A\|_1 = \max_{j} \sum_{i=1}^n |A_{ij}| $。  
由于 $ A $ 是非负且列和为 1 的矩阵，故：

$ \|A\|_1 = 1 $

3. **代入不等式**：

$ \|A\|_2 \le \sqrt{1 \cdot 1} = 1 $

**结论：** 双随机矩阵的谱范数不大于 1。

:::



2. **组合封闭性 (Compositional Closure)**：双随机矩阵相乘后依然是双随机矩阵。这意味着无论网络多深，这种稳定性都能保持。

:::info
证明分为三个部分：**非负性**、**行和为 1**、**列和为 1**。

1. 非负性证明 (Non-negativity)

**定义**：对于双随机矩阵，$ A_{ik} \ge 0 $ 且 $ B_{kj} \ge 0 $。  
**计算**：矩阵 $ C $ 的第 $ (i, j) $ 个元素为：

$ C_{ij} = \sum_{k=1}^n A_{ik} B_{kj} $

**推导**：  
因为 $ A_{ik} $ 和 $ B_{kj} $ 都是非负实数，所以它们的积 $ A_{ik} B_{kj} \ge 0 $。  
非负数之和依然是非负数，因此：

$ C_{ij} \ge 0 $

2. 行和为 1 的证明 (Row Sums)

**目标**：证明对于任意行 $ i $，$ \sum_{j=1}^n C_{ij} = 1 $。  
**已知**：$ B $ 的行和为 1，即 $ \sum_{j=1}^n B_{kj} = 1 $；$ A $ 的行和为 1。

**推导**：

$ \begin{aligned}
\sum_{j=1}^n C_{ij} &= \sum_{j=1}^n \left( \sum_{k=1}^n A_{ik} B_{kj} \right) \\
&= \sum_{k=1}^n A_{ik} \underbrace{\left( \sum_{j=1}^n B_{kj} \right)}_{\text{B 的行和，等于 1}} \quad \text{(交换求和顺序)} \\
&= \sum_{k=1}^n A_{ik} \cdot 1 \\
&= \underbrace{\sum_{k=1}^n A_{ik}}_{\text{A 的行和，等于 1}} \\
&= 1
\end{aligned} $



3. 列和为 1 的证明 (Column Sums)

**目标**：证明对于任意列 $ j $，$ \sum_{i=1}^n C_{ij} = 1 $。  
**已知**：$ A $ 的列和为 1，即 $ \sum_{i=1}^n A_{ik} = 1 $；$ B $ 的列和为 1。

**推导**：

$ \begin{aligned}
\sum_{i=1}^n C_{ij} &= \sum_{i=1}^n \left( \sum_{k=1}^n A_{ik} B_{kj} \right) \\
&= \sum_{k=1}^n \underbrace{\left( \sum_{i=1}^n A_{ik} \right)}_{\text{A 的列和，等于 1}} B_{kj} \quad \text{(交换求和顺序)} \\
&= \sum_{k=1}^n 1 \cdot B_{kj} \\
&= \underbrace{\sum_{k=1}^n B_{kj}}_{\text{B 的列和，等于 1}} \\
&= 1
\end{aligned} $

:::



3. **几何解释**：可以看作是特征的凸组合（Convex Combination），起到了信息融合的作用，而不是无界的放大。

#### 实现算法：Sinkhorn-Knopp
作者使用 Sinkhorn-Knopp 算法将原始的可学习矩阵投影到双随机矩阵上。  
首先计算动态系数得到 $ \tilde{\mathcal{H}}^{res}_l $，然后进行迭代归一化：

$ M^{(0)} = \exp(\tilde{\mathcal{H}}^{res}_l) $

$ M^{(t)} = \mathcal{T}_r \left( \mathcal{T}_c (M^{(t-1)}) \right) $

其中 $ \mathcal{T}_r $ 和 $ \mathcal{T}_c $ 分别是行归一化和列归一化。实验中迭代 20 次即可收敛。

:::info
**Sinkhorn-Knopp 算法**（通常简称 Sinkhorn 算法）是这篇 DeepSeek 论文中实现“流形约束”的核心工具。简单来说，它的作用是：**把一个任意的非负矩阵，通过迭代的方式，“硬挤”成一个双随机矩阵（Doubly Stochastic Matrix）。**它就像是一个“整形手术”，输入是一个形状不规则的矩阵，输出是一个完美符合“行和为1、列和为1”要求的矩阵。

1. 算法流程：交替归一化

Sinkhorn-Knopp 的逻辑非常简单直观，核心就是六个字：**行归一，列归一**。

假设给你一个非负方阵 $ A $（在论文中，这个 $ A = \exp(\tilde{\mathcal{H}}^{res}) $，即经过 exp 变换保证非负的原始权重），要把变成双随机矩阵 $ S $。

#### 步骤如下：
1. **初始化**：令 $ S^{(0)} = A $。
2. **行归一化 (Row Normalization)**：  
把矩阵的每一行除以该行的和，使得行和变为 1。
3. **列归一化 (Column Normalization)**：  
把上一步得到的矩阵，每一列除以该列的和，使得列和变为 1。
4. **循环**：  
重复步骤 2 和 3，直到收敛（或者达到预设的迭代次数，论文用了 20 次）。



2. 一个直观的数值例子

假设输入矩阵 $ A = \begin{bmatrix} 1 & 1 \\ 1 & 10 \end{bmatrix} $。  
目标：让它行和列和都为 1。

**第一轮迭代：**

1. **行归一化**：
    - 第一行和 = 2，第二行和 = 11。
    - 除以行和：

$ \begin{bmatrix} 1/2 & 1/2 \\ 1/11 & 10/11 \end{bmatrix} \approx \begin{bmatrix} 0.5 & 0.5 \\ 0.09 & 0.91 \end{bmatrix} $

    - _现状：行和是 1 了，但列和分别是 _$ 0.59 $_ 和 _$ 1.41 $_，还不是 1。_
2. **列归一化**：
    - 第一列和 $ \approx 0.59 $，第二列和 $ \approx 1.41 $。
    - 除以列和：

$ \begin{bmatrix} 0.5/0.59 & 0.5/1.41 \\ 0.09/0.59 & 0.91/1.41 \end{bmatrix} \approx \begin{bmatrix} 0.85 & 0.35 \\ 0.15 & 0.65 \end{bmatrix} $

    - _现状：列和是 1 了，但行和变成 _$ 1.2 $_ 和 _$ 0.8 $_，又歪了！_

**关键点**：虽然每次归一化列的时候会破坏行的和，反之亦然，但数学上证明了，**这种破坏程度会随着迭代次数呈线性收敛，最终趋于稳定**。

经过多次迭代后，它最终会收敛到一个同时满足行和为 1、列和为 1 的矩阵。



3. 数学本质与 Sinkhorn 定理

Sinkhorn 定理（1964）保证了上述过程的理论依据。

**定理内容**：  
对于一个元素严格为正的方阵 $ A $，存在唯一的两个对角矩阵 $ D_1 $ 和 $ D_2 $（且对角元素为正），使得：

$ S = D_1 A D_2 $

是一个双随机矩阵。

在算法中：

+ 行归一化 相当于左乘一个对角矩阵 $ D_r $（调整行的缩放）。
+ 列归一化 相当于右乘一个对角矩阵 $ D_c $（调整列的缩放）。

所以整个迭代过程本质上就是在寻找这两个对角缩放矩阵。



4. 为什么 DeepSeek 论文要用它？

在 mHC 中使用 Sinkhorn-Knopp 有三个巨大的优势：

1. **<font style="color:#DF2A3F;">可微性 (Differentiability)</font>**<font style="color:#DF2A3F;">：  
</font><font style="color:#DF2A3F;">整个过程只包含加法、除法和矩阵乘法。这意味着它是</font>**<font style="color:#DF2A3F;">完全可微</font>**<font style="color:#DF2A3F;">的。梯度可以直接穿过 Sinkhorn 层，反向传播去更新原始的参数 </font>$ \tilde{\mathcal{H}}^{res} $<font style="color:#DF2A3F;">。</font>
2. **约束满足 (Constraint Satisfaction)**：  
它能把参数强行拉回到 Birkhoff 多胞形（双随机矩阵集合）上。正如我们之前证明的，这直接保证了 $ \| \mathcal{H}^{res} \|_2 \le 1 $，解决了梯度爆炸。
3. **计算高效 (Efficiency)**：  
虽然是迭代算法，但通常只需很少的迭代次数（论文中设为 $ T_{max}=20 $）就能得到非常好的近似解。而且这些操作极其适合 GPU 并行计算（全是矩阵点操作）。

:::

PyTorch 代码实现Sinkhorn-Knopp算法：

```python
import torch

def sinkhorn_knopp(log_alpha, n_iters=20):
    """
    输入: log_alpha (原始的可学习参数, 形状 [N, N])
    输出: 双随机矩阵 S
    """
    # 1. 保证非负性：取指数
    # 注意：为了数值稳定性，通常先减去最大值再 exp
    M = torch.exp(log_alpha - log_alpha.max())
    
    # 2. 迭代归一化
    for _ in range(n_iters):
        # 行归一化 (Row Normalization)
        # M 除以 行和
        M = M / (M.sum(dim=1, keepdim=True) + 1e-8) # 加 epsilon 防除零
        
        # 列归一化 (Column Normalization)
        # M 除以 列和
        M = M / (M.sum(dim=0, keepdim=True) + 1e-8)
        
    return M

# 测试
logits = torch.randn(4, 4)
doubly_stochastic_matrix = sinkhorn_knopp(logits)

print("行和:", doubly_stochastic_matrix.sum(dim=1)) 
# 输出应接近 [1., 1., 1., 1.]
print("列和:", doubly_stochastic_matrix.sum(dim=0)) 
# 输出应接近 [1., 1., 1., 1.]
```

**总结**：  
Sinkhorn-Knopp 是连接“无约束的神经网络参数”和“严格的数学流形约束”之间的桥梁。它让 DeepSeek 能够既享受参数学习的灵活性，又拥有数学上的稳定性保证。



## 4. 实验结果 (Experiments)
作者在 DeepSeek-V3 架构（MoE）上进行了验证，主要关注 27B 参数的模型，扩展率 $ n=4 $。

### 4.1 稳定性分析
+ **Loss 曲线**：mHC 完全消除了原始 HC 在 12k 步左右出现的 Loss 激增现象，训练曲线非常平滑。
+ **梯度范数**：原始 HC 的梯度范数极不稳定，而 mHC 的梯度范数保持在健康范围内。
+ **增益幅度 (Gain Magnitude)**：HC 的信号增益可能达到 3000 倍（导致爆炸），而 mHC 被严格控制在 1.6 左右。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/57569306/1767535744001-6619f6a6-10a5-4434-afe2-da36ff2d58af.png)

### 4.2 性能对比
+ 在 BBH, DROP, GSM8K, MATH, MMLU 等主流 Benchmark 上，**mHC 全面超越 Baseline**，并且在大多数任务上也优于原始 HC。
+ 特别是在推理任务（BBH, DROP）上提升显著。

### 4.3 扩展性 (Scaling)
+ **Compute Scaling**：从 3B 到 27B，mHC 始终保持相对于 Baseline 的性能优势。
+ **开销**：在 $ n=4 $ 的情况下，引入 mHC 仅增加了 **6.7%** 的训练时间开销（得益于上述的工程优化），这是完全可接受的。











