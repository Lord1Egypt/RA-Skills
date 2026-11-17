# Formula-Rules｜数学公式书写规范知识库

> 生成 LaTeX 时必须严格遵守本规范。转换链路（LaTeX→MathML→OMML）对这些写法**已实测通过**。

## 一、数域符号

| 数域 | LaTeX | 示例 |
|---|---|---|
| 实数域 ℝ | `\mathbb{R}` | `x \in \mathbb{R}` |
| 复数域 ℂ | `\mathbb{C}` | `z \in \mathbb{C}` |
| 自然数 ℕ | `\mathbb{N}` | `n \in \mathbb{N}` |
| 整数域 ℤ | `\mathbb{Z}` | `k \in \mathbb{Z}` |
| 有理数域 ℚ | `\mathbb{Q}` | `q \in \mathbb{Q}` |

## 二、算子符号

| 符号 | LaTeX | 说明 |
|---|---|---|
| ∂ | `\partial` | 偏导数 |
| ∇ | `\nabla` | 梯度 |
| Δ | `\Delta` | 拉普拉斯算子（大写希腊 Delta） |
| ∞ | `\infty` | 无穷大 |
| ℏ | `\hbar` | 约化普朗克常数 |
| ⟨A⟩ | `\langle \hat{A} \rangle` | 算符期望值 |

**不等号学术论文标准写法**：用 `\le`、`\ge`，不要用 `<=`、`>=`：

```
✅ \alpha + \beta \le \gamma
❌ \alpha + \beta <= \gamma
```

同理：`\ne`（不是 `!=`）、`\approx`（不是 `~`）、`\ll` / `\gg`。

## 三、积分、求和（块公式）

| 结构 | LaTeX |
|---|---|
| 定积分 | `\int_{a}^{b} f(x)\,dx` |
| 多重积分 | `\iint_{D}`、`\iiint_{V}`、环路 `\oint_{C}` |
| 求和 | `\sum_{i=1}^{n} a_i` |
| 乘积 | `\prod_{i=1}^{n} a_i` |
| 极限 | `\lim_{n \to \infty} a_n` |

## 四、向量与矩阵

| 结构 | LaTeX |
|---|---|
| 向量粗体 | `\boldsymbol{x}` |
| 矩阵大写粗体 | `\boldsymbol{A}` |
| 方括号矩阵（优先） | `\boldsymbol{A} = \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}` |
| 圆括号矩阵 | `\begin{pmatrix} ... \end{pmatrix}` |
| 行列式 | `\begin{vmatrix} ... \end{vmatrix}` |
| 转置 | `\boldsymbol{A}^{\mathsf{T}}` 或 `A^T` |

## 五、多行推导对齐

统一用 `align` 环境，`&` 符号作为对齐标记：

```latex
\begin{align}
G(x,x') &= -\frac{1}{2ik}\int_{-\infty}^{\infty} e^{ik|x-x'|} V(x')\,dx' \\
        &= -\frac{1}{2ik} \left[ e^{ikR} \right]_{0}^{\infty}
\end{align}
```

> **脚本处理方式**：align 环境自动拆分为逐行公式、逐行居中写入 docx（每行仍是原生可编辑 OMML；编号 `\tag` 挂在最后一行）。`&` 对齐符在拆行时自动剥除。
> **禁止裸多行语法**：`a &= b \\ c &= d`（不在 align 环境内）链路不支持。

## 六、公式编号

用户需要编号的块公式，右侧添加 `\tag{数字}`：

```latex
$$ \rho(x) = |\psi(x)|^2 \tag{3.7} $$
```

脚本自动把 `\tag{3.7}` 转为公式尾部编号 `(3.7)`。章节式编号（3.7、4.1）由用户在 `\tag{}` 里自带，脚本不做自动连续编号。

## 七、完整符号速查

其余符号（希腊字母全集、二元运算符、关系符、箭头等）查 `symbol-table.md`。

## 八、转换链路实测边界（写 LaTeX 前自查）

**✅ 已实测支持**（可放心写）：

- 分式 `\frac{a}{b}`、根号 `\sqrt{x}` / `\sqrt[n]{x}`
- 上下标 `x_i^2`、`\hbar^2`、`a_{11}`
- 求和 / 积分 / 乘积 / 极限及上下限
- 希腊字母全表（含 `\hbar`）
- 矩阵 `bmatrix` / `pmatrix` / `vmatrix`
- 分段 `cases`
- 多行 `align` / `align*` / `aligned`（自动拆行）
- `\tag{...}` 编号
- 数域 `\mathbb{R}` 等
- 粗体 `\boldsymbol{...}`
- 公式内中文 `\text{且}`
- `\left[ ... \right]` 自动放大括号

**❌ 不支持**（写了会触发降级预案，保留 LaTeX 原文）：

- 未知命令（拼写错误的命令，如 `\fraz`）——**不会报错而是被静默当文本写入公式**，脚本质量校验会拦截并降级
- 裸 `& ... \\` 多行语法（必须包在 align 环境内）
- 需要外部宏包的扩展命令：physics 包（`\dv`、`\pdv`、`\braket`）、cancel 包（`\cancel`）等
  - **替代写法**：偏导用 `\frac{\partial f}{\partial x}`，不用 `\pdv{f}{x}`；bra-ket 用 `\langle \phi | \psi \rangle`，不用 `\braket{\phi|\psi}`

**⚠️ 谨慎使用**（行为不完全可控）：

- `\displaystyle`（对 MathML 转换无意义，省略）
- 复杂嵌套宏（自定义 `\newcommand` 展开不在链路能力内——展开后再喂）
