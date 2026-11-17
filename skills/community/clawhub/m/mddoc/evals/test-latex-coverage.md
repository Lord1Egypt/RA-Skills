# LaTeX 数学公式覆盖测试（IHKYoung 手册 + 完整补全）

本文件测试所有已实现的 LaTeX 数学公式语法。

---

## 矩阵环境

### bmatrix（方括号）

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}
$$

### pmatrix（圆括号）

$$
\begin{pmatrix} x_{11} & x_{12} \\ x_{21} & x_{22} \end{pmatrix}
$$

### vmatrix（单竖线行列式）

$$
\begin{vmatrix} a & b \\ c & d \end{vmatrix}
$$

### Vmatrix（双竖线范数）

$$
\begin{Vmatrix} a & b \\ c & d \end{Vmatrix}
$$

### matrix（无括号）

$$
\begin{matrix} 1 & 0 \\ 0 & 1 \end{matrix}
$$

---

## cases 环境（分段函数）

$$
f(x) = \begin{cases} 0 & x < 0 \\ x^2 & 0 \leq x < 1 \\ 1 & x \geq 1 \end{cases}
$$

---

## align 环境（多行对齐）

$$
\begin{align} x + y &= 2 \\ x - y &= 0 \end{align}
$$

---

## 字体命令

### 粗体

行内: $\mathbf{A} = \mathbf{B} + \mathbf{C}$

### 斜体

行内: $\mathit{variable}$

### 手写体（花体）

行内: $\mathcal{L}$ $\mathcal{A}$

### 黑板粗体

行内: $\mathbb{R}$ $\mathbb{N}$ $\mathbb{Z}$ $\mathbb{C}$

### 正体（罗马体）

行内: $\mathrm{Var}(X)$

### 等宽体

行内: $\mathtt{code}$

### 粗体符号

$\boldsymbol{\alpha} + \bm{\beta} = \mathbb{E}[X]$

---

## 希腊字母

### 小写

$\alpha$ $\beta$ $\gamma$ $\delta$ $\epsilon$ $\varepsilon$ $\zeta$ $\eta$ $\theta$ $\vartheta$

$\iota$ $\kappa$ $\lambda$ $\mu$ $\nu$ $\xi$ $\pi$ $\rho$ $\sigma$ $\tau$ $\upsilon$ $\phi$ $\varphi$ $\chi$ $\psi$ $\omega$

### 大写

$\Gamma$ $\Delta$ $\Theta$ $\Lambda$ $\Xi$ $\Pi$ $\Sigma$ $\Upsilon$ $\Phi$ $\Psi$ $\Omega$

### 变体

$\varpi$ $\varrho$ $\varsigma$

---

## 二元运算符

$+$ $-$ $\times$ $\div$ $\cdot$ $\oplus$ $\ominus$ $\otimes$ $\oslash$ $\odot$ $\star$ $\circ$ $\bullet$ $\pm$ $\mp$

---

## 关系符号

$=$ $\neq$ $\approx$ $\equiv$ $<$ $>$ $\leq$ $\geq$ $\ge$ $\le$ $\ne$

$\ll$ $\gg$ $\prec$ $\succ$ $\preceq$ $\succeq$ $\sim$ $\nsim$ $\simeq$ $\asymp$ $\propto$

---

## 逻辑符号

$\wedge$ $\vee$ $\neg$ $\Rightarrow$ $\Leftrightarrow$ $\forall$ $\exists$ $\nexists$ $\top$ $\bot$

---

## 集合符号

$\emptyset$ $\in$ $\notin$ $\subseteq$ $\subset$ $\nsubseteq$ $\supset$ $\supseteq$ $\nsupseteq$ $\cup$ $\cap$ $\setminus$

---

## 箭头

$\to$ $\gets$ $\leftarrow$ $\rightarrow$ $\Rightarrow$ $\Leftarrow$ $\leftrightarrow$ $\Leftrightarrow$

$\longrightarrow$ $\longleftarrow$ $\mapsto$ $\longmapsto$ $\uparrow$ $\downarrow$ $\updownarrow$

$\Uparrow$ $\Downarrow$ $\Updownarrow$

---

## 分数与根式

### 分数

$\frac{a}{b}$ $\dfrac{1}{2}$ $\tfrac{1}{3}$

$$
\frac{d}{dx} f(x) \qquad \frac{\partial f}{\partial x}
$$

### 根式

$\sqrt{x}$ $\sqrt[n]{x}$

---

## 指数与对数

$a^b$ $e^x$ $\log x$ $\ln x$ $\log_a b$ $\exp(x)$

---

## 极限

$\lim_{x \to a} f(x)$ $\lim_{x \to \infty} f(x)$

---

## 积分与求和

$\int f(x)dx$ $\int_{a}^{b} f(x)dx$ $\iint$ $\iiint$

$\sum_{i=1}^{n} x_i$ $\prod_{i=1}^{n} x_i$

---

## 重音符号

$\hat{x}$ $\bar{x}$ $\vec{v}$ $\dot{x}$ $\ddot{x}$ $\tilde{x}$

$$
\overrightarrow{AB} = \overleftarrow{BA}
$$

---

## 定界符

$$
\left( \frac{a + b}{c} \right) \qquad \left[ \frac{x}{y} \right]
$$

---

## 函数名

$\sin$ $\cos$ $\tan$ $\cot$ $\sec$ $\csc$

$\arcsin$ $\arccos$ $\arctan$

$\sinh$ $\cosh$ $\tanh$ $\coth$

$\log$ $\lg$ $\ln$ $\exp$

$\lim$ $\max$ $\min$ $\sup$ $\inf$

$\det$ $\dim$ $\ker$ $\gcd$

---

## 文本

$\text{当且仅当}$ $x \text{ is even}$

---

## 间距

$a\,b$ $a\quad b$ $a\qquad b$

---

## 颜色

$\textcolor{red}{红色文字}$ $\textcolor{blue}{蓝色文字}$

---

## 转义字符

$\#$ $\$ $ \% $ \& $ \_ $ \{ $ \} $ \backslash $

---

## 综合复杂公式

$$
\frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

$$
A\mathbf{v} = \lambda \mathbf{v}
$$

$$
\mathbb{E}[X] = \sum_{x} x\,P(X=x)
$$

$$
\mathrm{Var}(X) = \mathbb{E}[(X - \mathbb{E}[X])^2]
$$

$$
D_{KL}(P \parallel Q) = \sum_x P(x) \log \frac{P(x)}{Q(x)}
$$

$$
\frac{1}{N} \sum_{i=1}^{N} (y_i - (w^T x_i + b))^2
$$
