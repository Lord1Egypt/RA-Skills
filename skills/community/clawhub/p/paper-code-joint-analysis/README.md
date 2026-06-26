# Paper-Code Joint Analysis Skill

当前版本 / Current package version: `1.0.9`



## 中文简介

`paper-code-joint-analysis` 是一个只能在 **Codex** 中使用的论文与开源代码联合分析 skill。它的目标不是单独阅读论文，也不是单独浏览仓库，而是把论文中的理论、公式、算法步骤、实验设置与源码中的真实类、方法、参数、命令和日志入口逐项对应起来，帮助用户用代码理解论文。

分析结果最后使用网页展示，是为了让用户可以直接使用 Codex 的注释功能在页面上圈选不懂的地方，并基于选中的内容继续提问。

感谢 Bristol 的刘欣阳同学提供的素材（SemiDFL）。


适合用于：

- 通过开源实现理解论文方法；
- 对照公式、算法与真实训练流程；
- 找出论文没有披露但代码中体现的参数、默认值、随机性和实验细节；
- 整理论文每个表格、图、消融和补充实验对应的代码入口与复现实验命令；
- 生成 UML、时序图、数据流图和静态网页读者页面；
- 判断如果要修改论文提出的方法，最小需要改哪些文件和方法。

注意：这个包不是 Python 库、命令行工具、浏览器插件或独立网页应用。它必须由 Codex 读取并调用；其中的脚本和模板也默认由 Codex 在项目工作目录中执行。

## 使用方式：只能在 Codex 中自然语言调用

推荐做法：

1. 新建一个空的 Codex 项目工作目录。
2. 将 `paper-code-joint-analysis.skill.zip`、目标论文和目标源码放在这个空项目下。
3. `example/` 中已经提供 SemiDFL 示例论文 [`semidfl-paper.pdf`](example/semidfl-paper.pdf)、示例源码 [`semidfl-code.zip`](example/semidfl-code.zip)、示例截图和示例提示词 [`prompt.txt`](example/prompt.txt)。
4. 复现示例时，把示例论文、示例源码和 skill 压缩包一起放到空项目下，然后按 [`example/overview.jpg`](example/overview.jpg) 左侧上方展示的提示词提问即可；同一提示词也已经作为 `example/prompt.txt` 提供。
5. 如果分析自己的论文和代码，在 Codex 对话中明确要求使用这个 skill，并提供论文 PDF、arXiv 链接或标题，以及源码仓库链接或本地源码路径。
6. 如果只想静态分析，要明确说“不运行训练”；如果要复现实验，要说明允许安装依赖和运行脚本。

示例提示词：

简单版本：

```text
请使用 paper-code-joint-analysis.skill.zip 里的 skill，对 semidfl-paper.pdf 和 semidfl-code.zip 里的代码进行联合分析，并使用 skill 里的网页模板展示结果。
```

完整版本：

```text
请使用 paper-code-joint-analysis.skill.zip 里的 paper-code-joint-analysis skill，
联合分析这篇论文和它的官方代码。不运行训练，只做静态分析。
请输出完整论文解读报告、理论到代码映射、每个实验对应的代码用例、
由论文解读报告产生的阅读疑问及源码回答、
论文未披露但代码显示的实现细节、UML/时序图、基于论文框架提出新模型或新算法时应修改的核心函数指南，
并生成一个可在 Codex 中打开的静态网页。

论文：<PDF 路径或 arXiv 链接>
源码：<GitHub 链接或本地路径>
```

如果研究领域有关键执行机制，也应直接说明。例如联邦学习或去中心化联邦学习论文，应要求特别分析通信、拓扑、参数交换和聚合。

MIT-0.
