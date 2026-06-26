<div align="center">

# 🧭 Identity Compass

### 你已经知道答案了。只是还看不见而已。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://python.org)

[English](README.md) · [한국어](README_KO.md) · [中文](#问题)

<br>
<img src="assets/compass-demo.jpg" alt="Identity Compass 演示" width="600">
<br><br>
<img src="assets/slide-01.png" alt="人生指南针 AI" width="500">

</div>

---

## 问题

你做过性格测试，在元旦立过目标，列过利弊清单。然而在真正关键的时刻——你还是会卡住。

**"我该换这份工作吗？"**
**"这段关系对我合适吗？"**
**"我走的方向对吗？"**

真正的答案已经在你心里了。它散落在你做过的数百个小决定中——让你兴奋的、让你疲惫的、你反复回来的、你悄悄回避的。

**没有人在追踪这些模式。直到现在。**

## Identity Compass 做什么

它观察你的对话。不是为了评判——而是为了**倾听**。

每当你表达偏好、拒绝某事、对一个想法眼前一亮、或在岔路口犹豫时——系统捕捉一根小小的指南针针。随着时间推移，这些针会对齐。一个方向浮现。

然后，当你面对真正的决定时，不再靠猜，你可以问：

> *"这个选择指向的方向，和我一直以来走的方向一样吗？"*

### 真实例子

| 你说... | 系统看到... |
|---------|-----------|
| "与其照别人的剧本走，不如自己搞" | 强自主性信号 |
| "那份工作薪资不错但就是执行" | 反模式：没有主人翁意识的执行 |
| "做那个副项目完全忘了时间" | 心流状态 → 核心价值指标 |
| "说实话，我挺羡慕她的生活方式" | 渴望信号 → 方向候选 |

你不用填表格。不用答问卷。你只需要……说话。指南针完成剩下的。

<div align="center">
<img src="assets/slide-02.png" alt="我们走对方向了吗？" width="500">
<br><em>你无数的选择真的在指向你的真正目标吗？</em>
<br><br>
<img src="assets/slide-03.png" alt="3D空间中的决策弹珠" width="500">
<br><em>每个决定都是一颗带方向向量的弹珠——选咖啡是小弹珠，换工作是大弹珠。</em>
</div>

## 你会得到什么

### 🎯 你的方向（H 向量）
一句话捕捉你是谁——不是你觉得自己应该是谁。

> *"选择自主而非结构，通过研究构建深度，追求创新而非舒适。"*

这不是星座运势。它是从你的实际决策中计算出来的。

### 📊 对齐分数（M）
一个 0 到 1 的数字，显示你最近的选择与你真正方向的对齐程度。

- **0.8+** → 完全锁定。决策一致。
- **0.5-0.7** → 大方向对，有些噪声。
- **0.3 以下** → 你在同时拉向多个方向。是时候反思了。

### ⚖️ 决策模拟
站在岔路口？每个选项都会被模拟：

```
选项 A：接受创业公司 offer
  → 对齐度从 0.68 → 0.72 ✅

选项 B：留在现在的工作
  → 对齐度从 0.68 → 0.61 ⚠️
```

不是"选项 A 更好"。而是：**"选项 A 更像'你'。"**

<div align="center">
<img src="assets/slide-06.png" alt="决策模拟" width="500">
<br><em>在做决定之前先模拟。</em>
</div>

### 🗺️ 你的决策地图
交互式可视化，每个过去的决定都是一颗弹珠——大小代表重要性，颜色代表对齐度。实时观察你的模式浮现。

## 适合谁

- **考虑转行的人** — "我知道该走了，但去哪里？"
- **创始人** — "我在做的真的是我关心的事吗？"
- **站在十字路口的人** — "感觉是对的但说不出为什么"
- **厌倦了泛泛建议的人** — 这是用*你的*数据构建的，不是模板

## 这不是什么

- ❌ 不是性格测试（不需要自我报告）
- ❌ 不是目标设定应用（目标会变；方向持久）
- ❌ 不是替你决定的 AI（给数据，不做决定）
- ❌ 不是云端服务（一切留在你的设备上）

<div align="center">
<img src="assets/slide-07.png" alt="标准AI vs 指南针AI" width="500">
<br><em>普通 AI 给你事实。指南针 AI 给你对齐。</em>
</div>

## 快速开始

### 1. 安装技能

```bash
# 方法 A：通过 ClawHub（推荐）
npx clawhub@latest install identity-compass

# 方法 B：手动
git clone https://github.com/ico1036/identity-compass.git
cp -r identity-compass/ ~/.openclaw/workspace/skills/identity-compass/
```

### 2. 设置 Obsidian vault

指南针将你的决策向量存储在 [Obsidian](https://obsidian.md) 兼容的 vault 中。只需创建文件夹：

```bash
mkdir -p ~/.openclaw/workspace/obsidian-vault/compass/{vectors,clusters,signals,prior}
```

### 3. 开始聊天

就这样。和你的 [OpenClaw](https://openclaw.ai) 代理正常聊天。指南针在检测到决策信号时自动激活。

代理在后台静默提取向量。没有表格，没有问卷。

### 4. 查看你的地图

```bash
cd ~/.openclaw/workspace/skills/identity-compass/scripts
python3 -m http.server 8742
# 打开 http://localhost:8742/visualize_2d.html
```

---

## 数据文件

| 文件 | 用途 | 自动生成？ |
|------|------|:---:|
| `compass_data.json` | 可视化数据 | ✅ |
| `vectors.json` | 原始决策向量 | ✅ |
| `magnetization.json` | H 方向 + M 分数 | ✅ |
| `sample_data.json` | 演示数据 | 已包含 |

> **注意：** 所有个人数据文件都在 `.gitignore` 中——永远不会离开你的设备。

---

<details>
<summary><b>🔬 工作原理（技术细节）</b></summary>

### 物理模型

Identity Compass 借鉴了**统计力学**。每个决定是一个具有方向和强度的磁性自旋。

- **H（磁场）** = 你的核心方向，通过辩证对话提取
- **M（磁化强度）** = 所有自旋向量与 H 的对齐程度
- **衰减** = 旧决定以 `0.95^(days/30)` 衰减——现在的你更重要

### 三轴

| 轴 | (+) | (−) |
|----|-----|-----|
| X | 自主性 | 结构 |
| Y | 深度 | 广度 |
| Z | 创新 | 稳定 |

### Phase 1：辩证法提取

不会问"你的目标是什么？"。使用四种对话模式：
1. **困境** — 强制权衡揭示隐藏优先级
2. **时间转换** — "5年前的你看到现在的你会怎么想？"
3. **矛盾指出** — "你说了X但做了Y……"
4. **完成** — "其实你已经知道了，不是吗？"

### Phase 2：贝叶斯向量收集

从每个决定中提取 3D 方向向量、权重（1-10）、Beta(α,β) 后验更新。

### Phase 3：虚拟模拟

新选择 → 虚拟弹珠 → ΔM 计算 → 对齐度比较。

</details>

---

## 贡献

这是早期阶段。欢迎 PR 和想法。

## 许可证

[MIT](LICENSE)

## 作者

**Jiwoong Kim** — [@ico1036](https://github.com/ico1036)

---

<div align="center">

*"指南针不会告诉你去哪里。*
*它只是让你看见你一直在朝哪个方向走。"*

</div>
