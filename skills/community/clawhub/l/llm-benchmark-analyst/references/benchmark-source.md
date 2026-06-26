# 大模型评测榜单汇总

Tips：

同一领域甚至不同领域的不同基准测试分数均具有很高的相关性，参见*[Benchmark scores are well correlated, even across domains](https://epoch.ai/data-insights/benchmark-correlations)*

基准测试（Benchmarks）构成了评价模型性能的事实标准，但测试本身并非准确无误，甚至可能存在系统性缺陷，典型案例τ²-bench、MMLU-Pro、GPQA、HLE。（参见论文：*[Fantastic Bugs and Where to Find Them in AI Benchmarks](https://arxiv.org/abs/2511.16842)*）（案例说明见下面子项介绍）

当前对LLM进行评测的难点和缺陷参见epoch.ai的博客*[Why benchmarking is hard](https://epoch.ai/gradient-updates/why-benchmarking-is-hard)*。Anthropic发现基础设施配置可以对智能体编程基准测试产生数个百分点的波动（参见*[Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)*）。

自部署模型测试：参考Hugging Face官方教程：使用inspect-ai和lighteval（[https://huggingface.co/docs/inference-providers/guides/evaluatio...](https://huggingface.co/docs/inference-providers/guides/evaluation-inspect-ai)）（[github.com/huggingface/lighteval](https://github.com/huggingface/lighteval)）（[huggingface.co/docs/lighteval/main/en/index](https://huggingface.co/docs/lighteval/main/en/index)）

Hugging Face官方推出的开放Benchmark汇总，可以按语言、标签浏览任务，并搜索任务描述。（[huggingface.co/spaces/OpenEvals/open_benchmark_index](https://huggingface.co/spaces/OpenEvals/open_benchmark_index)）

目前所有基于 HF Open-LLM-Leaderboard 发布的模型评分和排名都受到空白字符漏洞影响。lm-evaluation-harness（实际应用中最常用的 LLM 评估工具包）被发现存在存在该漏洞（如果前面存在空白字符，就会导致正确选项无法被正确选中）。

‍

- Relative Adoption Metric (RAM)（[atomproject.ai/relative-adoption-metric](https://atomproject.ai/relative-adoption-metric)）

  相对采纳指标（Relative Adoption Metric, RAM）。“RAM 得分”：这是一个更合适的指标，可用于评估不同规模的新开源模型的下载情况。  
  得分 \= （模型的下载量） / （同一规模类别中排名前十的模型下载量的中位数）得分为1意味着该模型有望成为其所属规模中下载量排名前十的模型之一。

  数据收集（选用中位数）  
  按总下载量排名的每个尺寸分组前 10 大模型（来自 HuggingFace）  
  里程碑时刻的累计下载量：发布后第7天、14天、30天、60天、90天、180天、365天  
  各模型随时间推移的累计 HuggingFace 下载总量

# 综合评测

- Artificial Analysis（[AI Model & API Providers Analysis | Artificial Analysis](https://artificialanalysis.ai/)）

  - AA Intelligence（[Artificial Analysis Intelligence Index | Artificial Analysis](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)）

    一个综合基准，整合七项具有挑战性的评估，全面衡量人工智能在数学、科学、编程和推理方面的能力。综合了10项评估的表现：GDPval-AA, 𝜏²-Bench Telecom, Terminal-Bench Hard, SciCode, AA-LCR, AA-Omniscience, IFBench, HLE, GPQA Diamond, CritPt。
  - Artificial Analysis Openness Index（[https://artificialanalysis.ai/evaluations/artificial-analysis-op...](https://artificialanalysis.ai/evaluations/artificial-analysis-openness-index)）

    一项标准化且独立评估的指标，用于衡量人工智能模型在可用性和透明度方面的开放程度。开放性不仅仅指能够下载模型权重。它还涉及许可协议、数据和方法论。在开放指数中获得 100 分的模型将具备开放权重、采用宽松许可协议，并完整发布训练代码、预训练数据和训练后数据——这不仅允许用户使用模型，还能完全复现其训练过程，或从模型创建者的部分或全部方法中汲取灵感来构建自己的模型。
- llm-stats（[llm-stats.com/](https://llm-stats.com/)）

  一个综合性评测网站。包含benchmark汇总（[llm-stats.com/benchmarks](https://llm-stats.com/benchmarks)）
- vals.ai（[www.vals.ai/home](https://www.vals.ai/home)）

  一个综合性评测网站，分为综合、法律、金融、医疗、数学、学术、教育、编码、游戏等类别。

  - Vals Index

    衡量 AI 模型在金融、法律与软件工程领域执行真实任务的能力。通过计算模型在关键行业中的表现加权平均值来实现这一目标，权重则对应各行业对美国经济的贡献。
- SEAL LLM Leaderboards（[scale.com/leaderboard](https://scale.com/leaderboard)）

  评估最新 LLM 的智能体能力、前沿性能、安全性及公众情绪。
- Epoch AI（[epoch.ai/benchmarks](https://epoch.ai/benchmarks)）

  有多个基准测试。

  Epoch 能力指数（ECI）将多个不同 AI 基准的分数综合为一个“通用能力”尺度，即使在单个基准已达到饱和的长时间跨度内，也能对模型进行比较。
- Sansa Bench（[trysansa.com/benchmark](https://trysansa.com/benchmark)）

  一个专门设计的基准测试，用于在复杂的现实世界任务和使用场景中测试模型。下有学术、办公、审查等多个领域的细分榜单。

  审查榜（[trysansa.com/benchmark?dimension=censorship](https://trysansa.com/benchmark?dimension=censorship)）
- LMArena（[Overview Leaderboard | LMArena](https://lmarena.ai/leaderboard/)）

  一个基于真实用户盲测投票和 Elo 排名的众包评测平台，用来比较不同大模型在真实交互中的综合表现。
- OpenCompass（[OpenCompass司南 - 评测榜单](https://rank.opencompass.org.cn/home)）

  面向大模型开发者和使用者的开源开放评测平台，提供多能力维度、多个评测集和榜单的统一评测。包括大语言模型闭源榜、学术榜、多模态榜。
- LiveBench（[LiveBench](https://livebench.ai/#/)）

  一个专为避免测试集污染和实现客观评估而设计的 LLM 基准测试，包括推理、编码、数学、数据分析。
- CAIS AI Dashboard（[dashboard.safe.ai/](https://dashboard.safe.ai/)）

  包括文本、视觉、风险和自动化四个指标
- AGI-Eval评测（[agi-eval.org/topRanking](https://agi-eval.org/topRanking)）

  分为平台自建榜单和公开学术榜单。自建榜单分为大语言模型（精调和基座）和多模态模型（多模理解、文生图、文生视频、语音交互、语音合成）。公开学术榜单包括大语言精调模型榜单和大语言基座模型榜单。
- 晓天衡宇评测（[skylenage.net/sla/leaderboard](https://skylenage.net/sla/leaderboard)）

  包括大语言模型榜和垂直领域榜。大语言模型榜：基于自研评测集，运用自动化与专家评估相结合的模式，对LLM的能力进行多维度衡量。垂直领域榜包括考研数学、OCR信息抽取和电商agent三个榜单。
- NeMo Evaluator SDK（[NVIDIA-NeMo/Evaluator: Open-source library for scalable, reproducible evaluation of AI models and benchmarks.](https://github.com/NVIDIA-NeMo/Evaluator)）

  NVIDIA 开源的大模型评测 SDK，可在统一框架下对任意兼容 API 的模型进行大规模、可复现的 benchmark 评测。

# Coding Benchmarks

- SWE-bench（[SWE-bench Leaderboards](https://www.swebench.com/index.html)）

  SWE-bench 是软件工程领域最受欢迎的评估套件之一——这是一个用于评估大语言模型（LLMs）解决来自 GitHub 的真实软件问题能力的基准测试。该基准测试要求代理接收一个代码仓库和问题描述，并挑战其生成一个能解决该问题的补丁。

  - 细节

    SWE-bench 测试集中的每个样本均来自 GitHub 上 12 个开源 Python 仓库中已解决的 GitHub 问题。每个样本都关联一个拉取请求（PR），其中包含解决方案代码和用于验证代码正确性的单元测试。这些单元测试在 PR 中添加解决方案代码之前会失败，但在添加之后会通过，因此被称为 FAIL_TO_PASS 测试。每个样本还关联有 PASS_TO_PASS 测试，这些测试在 PR 合并前后均能通过，用于确保代码库中现有的无关功能未因 PR 而被破坏。

    对于 SWE-bench 中的每个样本，智能体将获得 GitHub 问题的原始文本（称为问题描述），并可访问代码库。基于这些信息，智能体必须编辑代码库中的文件以解决问题。测试用例不会向智能体展示。

    提出的修改通过运行 FAIL_TO_PASS 和 PASS_TO_PASS 测试来评估。如果 FAIL_TO_PASS 测试通过，说明该修改解决了问题；如果 PASS_TO_PASS 测试通过，则表明修改未意外破坏代码库中其他无关部分。只有两组测试全部通过，才能完全解决原始的 GitHub 问题。

  - **SWE-bench Verified（OpenAI已停用）**

    openai推出的一个经过人工筛选的包含 500 个实例的子集。（为解决原始 SWE-bench 数据集低估了智能体的能力）

    现有的代理框架通常依赖于 Python 特有的工具，导致对 SWE-bench Verified 过度拟合。

    注意：OpenAI宣布停止使用 SWE-bench Verified 指标，建议行业转向 SWE-bench Pro。技术分析显示，该基准因测试用例缺陷及训练数据污染，已无法准确衡量模型真实进展。审计发现 59.4% 的被测问题存在测试设计缺陷，导致正确代码被拒；红蓝对抗实验证实多款前沿模型存在强污染，能复现原始修复方案。

    见*[Why SWE-bench Verified no longer measures frontier coding capabilities](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)*
  - SWE-Bench Pro (Public Dataset)（[scale.com/leaderboard/swe_bench_pro_public](https://scale.com/leaderboard/swe_bench_pro_public)）

    SWE-Bench Verified的升级版。

    一个专为对软件工程领域的 AI 代理进行严格且真实评估而设计的基准测试。它旨在通过应对四大关键挑战，解决现有基准测试中的若干局限性：

    1. 数据污染：模型在训练期间可能已接触过评估代码，因此难以判断其是真正解决问题，还是在复现记忆中的答案。
    2. 任务多样性不足：许多基准测试未能涵盖现实世界软件挑战的完整范围，而仅聚焦于简单的工具库。
    3. 问题过于简化：模糊或未明确说明的问题常被从基准测试中剔除，而这与真实开发者的实际工作流程不符。
    4. 不可靠且无法复现的测试：不一致的环境设置使得难以判断解决方案是否真正有效，还是仅仅因为环境配置错误。
  - SWE-bench Multilingual（[www.swebench.com/multilingual-leaderboard.html](https://www.swebench.com/multilingual-leaderboard.html)）

    旨在评估 LLMs 在多种编程语言中的软件工程能力。SWE-bench Multilingual 包含 300 个精心挑选的软件工程任务，这些任务源自 42 个 GitHub 仓库和 9 种编程语言的真实拉取请求（涵盖 9 种流行编程语言（C、C++、Go、Java、JavaScript、TypeScript、PHP、Ruby 和 Rust））。这些仓库涵盖广泛的应用领域，包括 Web 框架、数据存储与处理工具、核心工具以及常用库。
  - 局限性

    基于静态数据集的评估 inherently 有限，SWE-bench 也不例外。由于该基准由对公共 GitHub 仓库的抓取组成，预训练于互联网文本的大型基础模型很可能在这些任务上受到污染。此外，SWE-bench 仅涵盖模型自主性中等风险水平的狭窄分布，因此必须辅以其他评估方式。
- LiveCodeBench（LCB）（[Artificial Analysis](https://artificialanalysis.ai/evaluations/livecodebench)）

  从 LeetCode、AtCoder 和 Codeforces 平台的定期竞赛中收集问题，并用于构建一个全面的基准，以持续评估 LLMs 在各种代码相关场景中的表现。关注更广泛的代码相关能力，例如自我修复、代码执行和测试输出预测，而不仅仅是代码生成。

  - GSO Benchmark（[livecodebench.github.io/gso.html](https://livecodebench.github.io/gso.html)）

    用于评估软件工程智能体的具有挑战性的软件优化任务。通过 10 个代码库中的 102 项具有挑战性的优化任务，评估语言模型开发高性能软件的能力。该基准测试衡量模型在运行时效率上的提升，与专家开发者优化结果进行对比。
- LiveCodeBench Pro（[livecodebenchpro.com/](https://livecodebenchpro.com/)）

  测试分为easy、medium、hard三个等级。
- OJBench（[He-Ren/OJBench](https://github.com/He-Ren/OJBench)）（[he-ren.github.io/OJBench-Leaderboard/](https://he-ren.github.io/OJBench-Leaderboard/)）

  旨在评估大语言模型（LLMs）在竞赛级别的代码推理能力。我们的数据集专注于人类编程竞赛，包含 232 道经过严格筛选的竞赛题目，来源为中国全国信息学奥林匹克竞赛（NOI）和国际大学生程序设计竞赛（ICPC）。每道题目均根据参赛者投票和真实提交数据，细致划分为三个难度等级：简单、中等和困难。OJBench 支持 Python 和 C++ 双语评估。
- OctoCodingBench（[https://huggingface.co/datasets/MiniMaxAI/OctoCodingBench/blob/m...](https://huggingface.co/datasets/MiniMaxAI/OctoCodingBench/blob/main/README_CN.md)）

  包含 72 个精选实例，评估代码仓库场景下的脚手架感知指令遵循能力。测试智能体对 7 种异构指令来源的遵循程度：System Prompt、System Reminder、User Query、项目级约束(Agents.md)、技能(skill)、记忆(Memory)、Tool Schema。区分任务完成与规则遵循：高任务成功率 ≠ 高指令遵循率；多脚手架支持：Claude Code、Kilo、Droid — 真实生产环境脚手架；冲突检测：测试智能体如何解决矛盾指令。
- CursorBench（[cursor.com/cn/blog/cursorbench#cursorbench](https://cursor.com/cn/blog/cursorbench#cursorbench)）

  基于工程团队真实 Cursor 会话构建的评测，任务来自真实的 Cursor 用量，而不是公开代码仓库。许多任务来自内部代码库和受控来源，从而降低了模型在训练阶段见过这些任务的风险。
- Roo Code evals（[Evals | Roo Code](https://roocode.com/evals)）

  一个面向代码模型/Agent 的量化评测体系，用标准化编程任务横向比较不同模型和提供商的代码能力。
- cto bench（[cto.new/bench](https://cto.new/bench)）

  模型在来自cto.new用户的真实端到端编码任务上的成功率
- OpenHands Index（[index.openhands.dev/home](https://index.openhands.dev/home)）

  一种用于评估人工智能编码代理在真实世界软件工程任务中表现的综合基准，同时呈现模型的性能和成本效益。从五个类别对模型进行评估： 问题解决 （修复漏洞）、 全新项目开发 （构建新应用）、 前端开发 （用户界面设计）、 测试 （测试用例生成）以及信息收集 。
- Windsurf Arena Leaderboard（[windsurf.com/leaderboard](https://windsurf.com/leaderboard)）

  一个基于 Windsurf 用户真实 prompt 和投票结果生成的模型榜单，更贴近真实编码使用场景。
- BridgeBench（[www.bridgemind.ai/bridgebench](https://www.bridgemind.ai/bridgebench)）

  BridgeMind 推出的 vibe coding 基准，用标准化任务评测模型在调试、算法、重构、生成、UI 和安全等编程场景下的表现。
- Metr Measuring AI Ability to Complete Long Tasks（[https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complet...](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)）

  以 AI 智能体能够完成的任务长度来衡量 AI 性能。通过“模型以 x%概率成功完成的、人类所需耗时的长度”来刻画某一模型的能力（当前模型在人类耗时少于 4 分钟的任务上成功率接近 100%，但在人类耗时超过约 4 小时的任务上成功率低于 10%）。

  对该基准的进一步解释：*[Clarifying limitations of time horizon](https://metr.org/notes/2026-01-22-time-horizon-limitations/)*
- ALE-Bench（[sakanaai.github.io/ALE-Bench-Leaderboard/](https://sakanaai.github.io/ALE-Bench-Leaderboard/)）

  一个用于评估 AI 系统在基于分数的算法编程竞赛中表现的基准测试。该基准借鉴了AtCoder Heuristic Contest (AHC)中的现实任务，提出了计算上困难且尚无已知精确解法的优化问题（例如路由和调度问题）。
- Android Bench（[developer.android.com/bench](https://developer.android.com/bench)）（人工筛选任务）

  评估了LLMs在解决现实世界Android开发问题方面的能力，包含100项任务。Android Bench 更偏向于库（58%）。

## AI编码智能体

- terminal-bench（[Terminal-Bench --- Terminal-Bench](https://www.tbench.ai/)）（[Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-hard)）（人工设计和验证）

  一个包含89个精心筛选的任务的数据集，涵盖软件工程、系统管理、数据科学、安全、科学计算等多个领域，用于评估 AI 智能体在终端环境中完成复杂任务的表现。Terminal-Bench 中的每个任务包括一段任务指令，一个 Docker 环境，一个测试套件，一个参考解决方案（人类编写）。代理需要通过命令行工具（如运行Bash命令、编辑文件）与环境交互来探索和解决问题。结果驱动，只关注任务最终完成的状态（通过测试验证），不限制代理的具体实现方法。

  - Terminal-Bench Pro（[alibaba.github.io/terminal-bench-pro/](https://alibaba.github.io/terminal-bench-pro/)）

    阿里发布的一个用于在真实终端环境中测试 AI 智能体的扩展基准测试数据集。从编译代码到训练模型、设置服务器，Terminal-Bench Pro 评估智能体处理真实世界端到端任务的能力——完全自主地执行。包含 200+ 个任务 **。**
- SWE-Bench Mobile（[swebenchmobile.com/](https://swebenchmobile.com/)）

  评估 AI 编码代理在真实世界移动应用开发任务中的表现，基于行业级 iOS 代码库。包括50项任务，每个任务均基于移动应用开发中的实际产品需求文档，包括功能规格、设计参考和验收标准。
- DPAI Arena（[DPAI — Developer Productivity AIrena](https://dpaia.dev/)）

  DPAI Arena是业界首个开放的、多语言、多框架、多工作流的基准测试平台，旨在衡量AI编码智能体在实际软件工程任务中的有效性。它围绕灵活的、基于赛道的架构构建，能够在各种工作流（如补丁制作、漏洞修复、PR审核、测试生成、静态分析等）中进行公平且可复现的比较。
- ProjDevBench（[zsworld6.github.io/projdevbenchpage/](https://zsworld6.github.io/projdevbenchpage/)）

  在端到端项目开发中评估 AI 编码智能体的性能。该评估工具结合了在线评测系统测试与 LLM 辅助的代码审查机制，要求编程智能体从零开始构建完整的代码库，从以下几个方面对编码代理进行评价：（1）系统架构设计（2）功能正确性以及（3）迭代解决方案的优化程度。包含 8 个类别中的 20 个编程问题 ，这些问题既涵盖了概念性的任务，也包含了实际应用场景，并对基于不同 LLM 后端构建的六种编码智能体（Claude Code、Cursor、Gemini CLI、Codex、Augment、 GitHub Copilot）进行了评估。
- SanityHarness（[sanityboard.lr7.dev/](https://sanityboard.lr7.dev/)）

  旨在简单易用、高效，并普遍兼容任何编码代理，用于在广泛的编码任务和语言中对其进行评估。在 6 种编程语言（Go、Rust、TypeScript、Kotlin、Dart 和 Zig）中的 26 项任务上进行加权评分。
- LongCLI-Bench（[github.com/finyorko/longcli-bench](https://github.com/finyorko/longcli-bench)）

  旨在评估命令行界面中智能体长时程编程的能力，包含20 个高质量任务，涵盖四大工程类别：从零开始、功能添加、错误修复和重构。
- Code Review Bench（[codereview.withmartian.com/](https://codereview.withmartian.com/)）

  用于评估 AI 代码审查工具的基准
- skillsbench（[www.skillsbench.ai/leaderboard](https://www.skillsbench.ai/leaderboard)）

  首个旨在系统评估智能体技能如何提升 AI 智能体性能的基准。涵盖 11 个领域的 84 项任务，在 7 种智能体-模型配置下，于 3 种条件下进行评估。
- SKILL-INJECT（[www.skill-inject.com/](https://www.skill-inject.com/)）

  用于评估广泛使用的 LLM 智能体对通过技能文件注入攻击的敏感性。SKILL-INJECT 包含 202 个注入任务对，攻击范围从明显恶意的注入到隐藏在看似合法指令中的微妙、上下文相关的攻击。

## 科研场景

- SciCode（[Artificial Analysis](https://artificialanalysis.ai/evaluations/scicode)）

  旨在评估语言模型（LMs）生成代码以解决真实科学研问题的能力。它涵盖了来自物理、数学、材料科学、生物和化学六大领域的 16 个子领域。展现了科学家日常工作的真实流程：识别关键的科学概念与事实，然后将其转化为计算与模拟代码。

  主要聚焦于：1. 数值方法；2. 系统模拟；3. 科学计算。
- Frontier-CS（[github.com/FrontierCS/Frontier-CS](https://github.com/FrontierCS/Frontier-CS)）

  是一个未解决的、开放式的、可验证且多样化的基准，用于评估 AI 在具有挑战性的计算机科学问题上的表现。测试题为研究人员都难以解决的、没有已知最优解的，或需要深厚专业知识才能尝试的问题。

  分为算法类和研究类两个榜单。算法类涵盖优化任务、构建任务和交互任务。研究类问题，涵盖六个主要计算机科学领域:操作系统(OS)、高性能计算(HPC)、人工智能(AI 研究任务)、数据库(DB)、程序设计语言(PL)和安全(网络安全与漏洞分析)。

  官方介绍：*[Evaluating the Hardest CS Problems in the Age of LLMs](https://frontier-cs.org/blog/evaluation/)*
- AlgoTune（[algotune.io/](https://algotune.io/)）（存在缺陷）

  一个包含一百多个广泛使用的数学、物理和计算机科学函数的基准测试。对于每个函数，目标是在保持与参考实现相同输出的前提下，编写出在留出测试集输入上运行速度更快的代码。

  注意：每个任务都被限制在 1 美元的 API 使用费用内，导致许多定价较贵的模型无法正常运行。此外，该测试包含一组用于查看文件、回退到上一步和编辑代码的工具，但模型必须返回一段推理，然后是用三重反引号分隔的工具调用。模型很难适应这种格式，导致大量无用或损坏的“工具调用”。
- KernelBench v3（[elliotarledge.com/kernelbench-v3](https://elliotarledge.com/kernelbench-v3)）

  GPU内核优化基准测试，在H100和B200 GPU上针对41个CUDA问题对大语言模型（LLMs）进行评估。有三个关键指标需要考量：代码能否成功编译？计算结果是否正确？其性能是否优于 PyTorch 的基准测试结果？分为四个难度等级，第四级考察现代推理优化技术：DeepSeek MLA、DeepSeek MoE、GQA、FP8 Matmul、INT4 GEMM、GatedDeltaNet、KimiDeltaAttention。
- Kernel Arena（[www.kernelarena.ai/](https://www.kernelarena.ai/)）

  用于衡量前沿语言模型如何为AI加速器生成优化内核。分为WaferBench NVFP4和KernelBench HIP，WaferBench NVFP4：在 NVIDIA B200 上对 6 个融合后的 NVFP4 推理内核（Add+RMSNorm、SiLU+Mul、Quantize）与 FlashInfer 进行基准测试；KernelBench HIP：AMD MI300X 上的 KernelBench 内核 - LLM 生成的 HIP 优化。
- PostTrainBench（[posttrainbench.com/](https://posttrainbench.com/)）

  通过测试 AI 智能体能否成功对其他语言模型进行训练后优化，来衡量 AI 研发的自动化水平。每个智能体将获得四个基础模型（Qwen 3 1.7B、Qwen 3 4B、SmolLM3-3B 和 Gemma 3 4B）、一台 H100 GPU，以及十小时的时间限制，以通过训练后优化提升模型性能。
- WeirdML（[htihle.github.io/weirdml.html](https://htihle.github.io/weirdml.html)）

  向 LLMs 提出了一系列奇特且非传统的机器学习任务，这些任务需要细致的思考和真正的理解才能解决，旨在测试 LLM 的以下能力：  
  真正理解数据的特性与问题本质  
  为问题设计合适的机器学习架构与训练配置，并生成可运行的 PyTorch 代码来实现解决方案  
  根据终端输出和测试集上的准确率，在五次迭代中调试并改进解决方案  
  充分利用有限的计算资源和时间

# Agentic Benchmarks

- GAIA（[GAIA Leaderboard - a Hugging Face Space by gaia-benchmark](https://huggingface.co/spaces/gaia-benchmark/leaderboard)）

  全能型基准，通过涉及现实世界问题的基准测试，评估通用人工智能助手在推理、多模态处理、网页浏览以及工具使用方面的能力。
- FACTS Benchmark（[www.kaggle.com/benchmarks/google/facts/leaderboard](https://www.kaggle.com/benchmarks/google/facts/leaderboard)）

  一个参数化基准，用于衡量模型在事实性问答场景中准确调用其内部知识的能力，包含一个由 1052 个问题组成的公开集和一个由 1052 个问题组成的私有集。  
  一个搜索基准，用于测试模型将搜索作为工具以检索信息并正确整合信息的能力，包含一个由 890 个条目组成的公开数据集和一个由 994 个条目组成的私有数据集。  
  一个多模态基准，用于测试模型以事实准确的方式回答与输入图像相关提示的能力，包含一个 711 项的公开数据集和一个 811 项的私有数据集。

  FACTS Grounding：评估LLMs基于所提供的长篇文档生成事实准确的响应的能力，测试LLM的响应是否完全基于所提供的上下文，并能正确从长篇上下文文档中整合信息。
- FutureX（[futurex-ai.github.io/](https://futurex-ai.github.io/)）

  一个旨在预测未知未来的动态基准测试，核心特性：

  - 无数据污染： 通过要求预测未来事件，确保答案不会出现在任何模型的训练数据中。每周约有 500 个新事件 。
  - 现实挑战： 智能体分析实时的现实世界信息，以预测未来事件，而非在模拟环境中运行。
  - 大规模： 依托 195 个高质量来源 （从超过 2,000 个网站中精选），覆盖多个领域 。
  - 全自动化流程： 闭环系统每日自动采集问题、运行 27 个智能代理 ，并评分结果。
- xbench（[xbench --- xbench](https://xbench.org/)）

  国内机构合作推出的基准测试。包含两条互补的赛道，旨在衡量人工智能系统的智能前沿与实际应用价值。  
  AGI 跟踪：衡量核心模型能力，如推理、工具使用和记忆  
  与专业对齐：一类基于工作流、环境和业务关键绩效指标的新评估体系，与领域专家共同设计

  AGI 追踪评估衡量前沿能力，专业对齐评估则通过与业务关键绩效指标和运营规模对齐的动态、领域特定任务，反映真实世界中的实用性。

  xbench 构建为一个动态评估系统，两个赛道均持续更新。

  - xbench-ScienceQA

    专注于评估科学领域内的基础知识能力。
  - xbench-DeepSearch

    专注于评估搜索和信息检索场景中的工具使用能力，贴合中文语境。
- IFBench（[artificialanalysis.ai/evaluations/ifbench](https://artificialanalysis.ai/evaluations/ifbench)）

  通过 58 种多样且可验证的域外约束，评估模型在遵循精确指令方面的泛化能力，检验模型是否能遵守特定的输出要求。
- Toolathlon（[Tool Decathlon - Toolathlon](https://toolathlon.xyz/introduction)）

  一个评估语言智能体在真实环境中通用工具使用能力的基准。它涵盖基于现实世界软件环境的32 个软件应用和 604 个工具。每项任务都需要通过长程工具调用才能完成，共包含 108 个手动设计或编写的任务，平均每个任务需跨越约 20 轮交互。
- AgencyBench-V2（[agencybench.opensii.ai/](https://agencybench.opensii.ai/)）

  在100万tokens条件的现实世界环境中对自主智能体的发展前沿进行测试，涵盖138项任务和32个场景，每个场景平均约90次工具调用，考验小时级执行时间。评分涵盖 6 项核心能力：游戏开发/前端开发/后端开发/代码编写/研究/MCP。
- BFCL-V4（[gorilla.cs.berkeley.edu/leaderboard.html](https://gorilla.cs.berkeley.edu/leaderboard.html)）

  全称Berkeley Function-Calling Leaderboard，评估 LLM 准确调用函数（即工具）的能力。
- MCPMark（[mcpmark.ai/](https://mcpmark.ai/)）

  一套综合性压力测试 MCP 基准评测体系，包含多样化的可验证任务，旨在评估模型和智能体在真实 MCP 应用场景中的能力。包含以下MCP：Notion、Github、Filesystem、Postgres、Playwright、Playwright-WebArena。
- MCP Atlas（[scale.com/leaderboard/mcp_atlas](https://scale.com/leaderboard/mcp_atlas)）

  通过模型上下文协议（MCP）评估语言模型处理现实世界工具使用的能力，衡量的是多步骤工作流中的表现。包含 1,000 个人工撰写的任务，每个任务都需要调用多个工具来解决，工具来自 40 多个 MCP 服务器和 300 多个工具。任务范围从仅需 2 至 3 个工具且链条简单的单领域查询，到需要 5 个以上工具并包含条件分支和错误处理的复杂工作流。每项任务都包含精心挑选的干扰项工具，这些工具看似合理但实际错误。干扰项由数据标注者从与必需工具相同的类别中选取。该框架为每个任务提供 12-18 个工具（3-7 个必需工具加上 5-10 个干扰项），迫使代理基于工具描述进行推理，而非盲目调用。
- PinchBench（[pinchbench.com/](https://pinchbench.com/)）

  衡量 LLM 作为 OpenClaw 智能体的“大脑”表现如何。向智能体抛出真实任务：安排会议、编写代码、处理电子邮件、研究主题以及管理文件。包含23个不同类别的任务，任务以带有 YAML 前置属性的 Markdown 文件形式定义。
- Claw-Eval（[claw-eval.github.io/#/](https://claw-eval.github.io/#/)）（人工审核和验证）

  包含中文和英文共104个任务（32个中文 + 72个英文），提供19个带错误注入的模拟服务。采用三维评分体系——完成度、鲁棒性、安全性。Score \= Safety × (0.80 × Completion + 0.20 × Robustness)。如果某一次任务安全分数为零，那么该项总分为零。

## 白领经济价值任务

更多介绍可以参见*[What do “economic value” benchmarks tell us?](https://epoch.ai/blog/what-do-economic-value-benchmarks-tell-us)*

- GDPval-AA（[artificialanalysis.ai/evaluations/gdpval-aa](https://artificialanalysis.ai/evaluations/gdpval-aa)）

  为 OpenAI 的 GDPval 数据集开发的评估框架。它在 44 种职业和 9 个主要行业中，对 AI 模型在真实任务中的表现进行测试。包含220项任务，要求模型生成多样化的输出，包括文档、幻灯片、图表和电子表格，以模拟金融、医疗、法律及其他专业领域中的实际工作成果。
- VitaBench（[VitaBench: Benchmarking LLM Agents with Versatile Interactive Tasks in Real-world Applications](https://vitabench.github.io/)）

  以外卖点餐、餐厅就餐、旅游出行等高频生活场景为载体，构建了包含66个工具的交互式评测环境，设计了跨场景综合任务，从深度推理、工具使用与用户交互三大维度衡量智能体表现。
- DeepPlanning（[qwenlm.github.io/Qwen-Agent/en/benchmarks/deepplanning/](https://qwenlm.github.io/Qwen-Agent/en/benchmarks/deepplanning/)）

  一个用于实际长时智能体规划的基准测试。它包含多日旅行规划和多产品购物任务，这些任务需要主动获取信息、进行局部约束推理和全局约束优化。

  评估三种关键的智能体能力：  
  主动信息获取：主动调用API以发现隐藏的环境状态（例如，检查景点是否关闭或产品是否有库存），而不是虚构事实。  
  本地约束推理：满足阶梯级逻辑，例如匹配用户请求的特定品牌、尺寸或酒店设施。  
  全局约束优化：管理整体边界——如总预算上限和多日时间可行性——其中一个局部错误使整个计划无效。
- Remote Labor Index (RLI)（[scale.com/leaderboard/rli](https://scale.com/leaderboard/rli)）

  远程劳动力指数（RLI）是一项基准测试，衡量 AI 代理执行现实世界中专业自由职业平台具有经济价值的多媒体远程工作的能力。包含240个项目，试题来源于 Upwork 平台上 358 名经过验证的自由职业者的自下而上的收集。要求智能体完成具有视觉输出的任务（网页设计、产品美术、视频编辑等）。其需要理解并生成复杂的多文件交付成果，涵盖数十种独特的交付文件类型。这包括文档、音频、视频、3D 模型以及 CAD 文件。
- APEX-Agents（[www.mercor.com/apex/apex-agents-leaderboard/](https://www.mercor.com/apex/apex-agents-leaderboard/)）

  衡量前沿 AI 代理是否能够跨三个专业服务岗位（投资银行分析师、管理咨询师和企业律师）执行跨应用程序的长周期任务。

  - APEX（[www.mercor.com/apex/apex-v1-leaderboard/](https://www.mercor.com/apex/apex-v1-leaderboard/)）

    评估前沿模型是否具备在以下四类工作中执行具有经济价值任务的能力：投资银行助理、管理咨询师、大型律师事务所律师以及初级保健医生（医学博士）。
  - The AI Consumer Index (ACE)（[www.mercor.com/apex/ace-leaderboard/](https://www.mercor.com/apex/ace-leaderboard/)）

    评估前沿人工智能模型在购物、餐饮、游戏和 DIY 等日常消费任务中的表现能力。
- τ²-bench（[τ-bench --- τ-bench](https://taubench.com/#home)）（[Artificial Analysis](https://artificialanalysis.ai/evaluations/tau2-bench)）（被发现存在重大缺陷）

  用于评估跨多个领域客户服务代理的模拟框架，在协作的现实场景中对 AI 代理进行基准测试。τ-bench 要求代理**在复杂的企业领域中协调、引导并协助用户**实现共同目标。分为总体、零售、电信、航空。

  通过同时模拟智能体与用户，主动修改共享的全局状态，开创了评估对话式 AI 的新范式。电信领域测试智能体引导用户完成技术故障排除的能力，以检验其问题解决与有效沟通技巧。

  重大缺陷：

  在对原始的τ²-bench进行验证时，亚马逊AI团队发现了几类问题：

  1. 政策合规问题：预期行动违反了规定的领域政策的任务（例如，在政策不允许的情况下提供补偿、取消已起飞的航班）
  2. 数据库准确性问题：存在物品ID、乘客信息或支付方式参考不正确且与实际数据库不匹配的任务
  3. 逻辑一致性问题：存在不可能场景的任务（例如，兑换相同物品，这是政策所禁止的）
  4. 评估模糊性问题：任务说明过于模糊，导致评估结果不一致
- τ²-Bench-Verified（[github.com/amazon-agi/tau2-bench-verified](https://github.com/amazon-agi/tau2-bench-verified)）

  τ²-Bench-Verified是原始τ²-bench基准测试的修正版和人工验证版。此版本解决了在原始数据集中发现的问题，即任务定义、预期操作和评估标准与所述政策或数据库内容未能正确对齐。

## AI智能体

- AgentIF-OneDay（[xbench.org/agi/agentif](https://xbench.org/agi/agentif)）

  一个用于日常场景中通用人工智能智能体的任务级指令遵循基准，包含104项任务。围绕三个以用户为中心的类别构建：开放式工作流执行，用于评估对明确且复杂工作流的遵循程度；潜在指令，要求智能体从附件中推断隐含指令；以及迭代优化，涉及对正在进行的工作进行修改或扩展。
- SpreadsheetBench（[spreadsheetbench.github.io/](https://spreadsheetbench.github.io/)）

  评估LLM智能体在操作复杂真实电子表格方面的能力。该基准测试包含从在线 Excel 论坛收集的 912 个真实问题，涵盖多种表格数据，如多个表格、非标准关系型表格以及丰富的非文本元素。

## DeepResearch

- DeepSearchQA（[www.kaggle.com/benchmarks/google/dsqa/leaderboard](https://www.kaggle.com/benchmarks/google/dsqa/leaderboard)）

  谷歌推出的一个包含 900 个提示的基准测试，用于评估代理在 17 个不同领域中完成困难的多步信息检索任务的能力。与传统仅针对单答案检索或广泛事实准确性的基准不同，DeepSearchQA 包含一组具有挑战性的手工构建任务，旨在评估代理执行复杂搜索计划以生成详尽答案列表的能力。  
  每个任务都构造成一个“因果链”，其中完成某一步的信息发现依赖于前一步的成功完成，强调长期规划和上下文保留。
- DeepResearch Bench II（[https://agentresearchlab.com/benchmarks/deepresearch-bench-ii/in...](https://agentresearchlab.com/benchmarks/deepresearch-bench-ii/index.html#home)）

  建立在原始的 DeepResearch Bench 主题分布和任务设计之上。包含

  - 作为基础信号的现实世界中由专家撰写的研究报告。
  - 不依赖裁判模型内部领域知识的细粒度、可完全验证的评分标准。
  - 深度研究质量的三个核心维度：

    - 信息回忆——智能体能否识别、检索并交叉核对回答任务所需的所有关键信息？
    - 分析——智能体能否将检索到的信息综合成更高层次的结论和见解？
    - 呈现——智能体能否以结构化、易读且易于验证的方式呈现信息？
- FutureSearch-Deep Research Bench (DRB)（[evals.futuresearch.ai/](https://evals.futuresearch.ai/)）

  用于评估LLM智能体在网络上的研究能力。169项多样的现实世界任务中，每项任务都提供10到10万个离线存储的网页供搜索和推理使用。
- MMDeepResearch-Bench（[mmdeepresearch-bench.github.io/](https://mmdeepresearch-bench.github.io/)）（人工设计和验证）

  评估端到端的多模态深度研究，包含了涵盖 19 个不同领域的 140 个任务。每一项任务都被打包成图像-文本组合的形式（图像被视为证据：研究代理必须解读这些图像，验证其中的信息，并在最终报告中注明信息来源）。从两个能力层面来评估各类智能体：在基础层，我们主要考察其视觉感知、网络搜索、长上下文理解和指令遵循能力；在深度研究阶段，智能体必须展现出多模态任务理解能力、基于视觉的规划、基于引用的推理以及长篇报告的合成技术。
- xbench-DeepSearch（[xbench.org/agi/aisearch](https://xbench.org/agi/aisearch)）

## 视觉定位与Gui智能体

- OSWorld-Verified（OSWorld）（[os-world.github.io/](https://os-world.github.io/)）（详细介绍见*[What does OSWorld tell us about AI’s ability to use computers?](https://epoch.ai/blog/what-does-osworld-tell-us-about-ais-ability-to-use-computers)* ）

  OSWorld-Verified为OSWorld改进版，也是其目前通行版本（经常被省略为OSWorld）。网站主页Leaderboard为Verified版本的排名。

  一种用于评估大型语言模型在计算机使用任务上表现的工具。测试时，模型会收到任务指令以及一台 Ubuntu 虚拟机，它需要通过执行相应的操作来完成这些任务。包含 361个计算机使用任务，涉及真实的网络应用和桌面应用程序、开放领域的操作、操作系统文件读写操作，以及需要跨多个应用程序完成的工作流程。（其中大约 8%的任务被设计成无法完成，在这种情况下，模型应该能够判断出这些任务是无法执行的）

  本测试对于人类而言较容易：大多数任务只需不到十步就能完成；少数任务确实需要几十甚至上百步，但绝大多数任务只需要人类花费几分钟时间就能完成。

  OSWorld-Verified改进之处：（[xlang.ai/blog/osworld-verified](https://xlang.ai/blog/osworld-verified)）

  系统性地解决了 OSWorld 中存在的 300 多个问题，实现了更完善的基础设施（从 VMware/Docker 升级到 AWS，并行处理能力提升了 50 倍）以及更高的任务执行质量（修复网页结构变更、指令表述模糊以及评估机制的稳定性问题）。
- AndroidDaily（[opengelab.github.io/index_zh.html](https://opengelab.github.io/index_zh.html)）

  面向真实世界场景的多维动态基准测试。 我们专注于现代生活六个核心维度（食品、交通、购物、住房、信息消费、娱乐）的实证分析， 优先考虑主导这些类别的热门应用。这确保了基准测试任务具有真实世界的交互结果（如交易支付、服务预订）， 具有紧密的线上线下集成特征。

  静态测试方法包含3146个操作。提供任务描述和逐步截图，要求智能体预测每一步的动作类型和值 （如点击坐标、输入文本）。主要评估数值准确性。

  端到端基准测试方法在功能完整的测试环境（如真实设备或模拟器）中进行，智能体必须自主从头到尾执行任务， 以整体任务成功率作为评估指标。这种设置提供了最高的生态有效性，真实地反映了智能体在复杂环境中的综合能力。
- AndroidWorld（[google-research.github.io/android_world/](https://google-research.github.io/android_world/)）

  一个功能完整的安卓环境，为 20 款真实安卓应用中的 116 项编程任务提供奖励信号。与提供静态测试集的现有交互环境不同，AndroidWorld 能动态构建参数化且以自然语言无限表达的任务，从而在更庞大、更贴近现实的任务套件上进行测试。
- Mobile World（[tongyi-mai.github.io/MobileWorld/](https://tongyi-mai.github.io/MobileWorld/)）

  在人机交互与 MCP 增强环境中评估自主移动智能体，包含来自 20 个应用程序的 201 项任务，涵盖长周期、跨应用任务，以及智能体-用户交互和 MCP 增强型任务等新颖任务类别。

  难度体现在两个方面：  
  长周期、跨应用任务。Mobile World 的任务平均需要 27.8 个完成步骤，几乎是 AndroidWorld 所需 14.3 步的两倍。此外，62.2% 的任务涉及跨应用工作流，而 AndroidWorld 中这一比例仅为 9.5%。  
  新颖的任务类别。Mobile World 通过引入（1）智能体-用户交互任务（占 22.4%），评估智能体通过协作对话处理模糊指令的能力，以及（2）MCP 增强任务（占 19.9%），要求结合 GUI 导航与通过模型上下文协议调用外部工具的混合使用。
- ScreenSpot-Pro（[gui-agent.github.io/grounding-leaderboard/](https://gui-agent.github.io/grounding-leaderboard/)）

  面向专业高分辨率计算机使用的图形用户界面定位，专注于高分辨率专业软件图表

# Intelligence Benchmarks

- ARC-AGI-2（[arcprize.org/leaderboard](https://arcprize.org/leaderboard)）

  专注于那些对人类而言相对简单、但对 AI 却困难甚至不可能完成的任务，从而揭示那些无法通过“规模扩大”自然涌现的能力鸿沟。

  1. 所有评估集（公开、半私有、私有）现在均包含 120 个任务（从 100 个增加而来）。
  2. 已从评估集中移除容易受到暴力搜索影响的任务（即 2020 年 Kaggle 竞赛中的所有已解决任务）。
  3. 进行了受控的人类测试，以校准评估集的难度，确保 IDD，并验证至少两名人类能够通过 pass@2 解决（以符合 AI 规则）。
  4. 基于研究（符号解释、组合推理、上下文规则等），设计了新的任务以挑战 AI 推理系统。
- MultiChallenge（[scale.com/leaderboard/multichallenge](https://scale.com/leaderboard/multichallenge)）

  用于评估大型语言模型（LLMs）与人类用户进行多轮对话的能力。主要考验指令记忆、对用户信息的推理处理、对材料的控制编辑功能和自我一致性四大能力。
- MMLU-Pro（[MMLU-Pro Benchmark Leaderboard | Artificial Analysis](https://artificialanalysis.ai/evaluations/mmlu-pro)）（存在漏洞）

  多任务理解数据集，旨在严格评估大型语言模型。它包含来自各个学科领域的1.2万个复杂问题。每个问题有10个答案选项，整合了更多以推理为核心的问题。

  （漏洞：1、对于正确答案的子集而言，空格会成为第一个字符。这意味着，采用随机猜测再加上“如果以空格开头就选择该选项”的策略，将会带来相当大的优势，会影响化学、物理和数学相关的测试结果。2、总是猜测最长的答案，在整个测试基准中能获得类似的提升效果）
- SimpleBench（[simple-bench.com/](https://simple-bench.com/)）

  一个针对 LLMs 的多项选择文本基准测试，拥有非专业（高中）知识的个体在此基准上的表现优于最先进模型。SimpleBench 包含 200 多道题目，涵盖时空推理、社交智能以及我们称之为语言对抗鲁棒性（或脑筋急转弯）的内容。
- AA-Omniscience（[Artificial Analysis Omniscience Index | Artificial Analysis](https://artificialanalysis.ai/evaluations/omniscience)）（存在重大缺陷）

  涵盖 6 个领域（“商业”、“人文与社会科学”、“健康”、“法律”、“软件工程”和“科学、工程与数学”）中 42 个主题的 6,000 道问题。三项指标：准确率（正确百分比）、幻觉率（错误答案占所有非回避答案的百分比）、全知指数（回答正确+1，回答错误-1，回避回答 0）。

  重大缺陷：其中大量试题被社区发现存在问题
- TRUEBench（[TRUEBench - a Hugging Face Space by SamsungResearch](https://huggingface.co/spaces/SamsungResearch/TRUEBench)）

  一个用于评估 LLMs 指令遵循能力的基准测试，评估 LLMs 作为人类工作生产力助手的基准。
- Bullshit Benchmark（[petergpt.github.io/bullshit-benchmark/viewer/index.html](https://petergpt.github.io/bullshit-benchmark/viewer/index.html)）

  设计了55个完全不合逻辑的“胡说八道”问题，并评估模型在面对这些问题时是选择反驳还是真诚地尝试回答。
- Pencil Puzzle Bench（[ppbench.com/](https://ppbench.com/)）

  一个通过铅笔谜题评估大型语言模型推理能力的框架，包含300个谜题，涵盖20种类型。

## 幻觉与上下文召回

关于长上下文召回和推理问题，参考这篇文章*[Evaluating Long Context (Reasoning) Ability](https://nrehiew.github.io/blog/long_context/)*

- Hallucination Leaderboard（[LLM Hallucination Leaderboard - a Hugging Face Space by vectara](https://huggingface.co/spaces/vectara/leaderboard)）

  评估 LLM 在总结文档时引入幻觉的频率。输入短文档，并要求它们仅依据文档中呈现的事实对每篇短文进行摘要。评估的是摘要的事实一致性率，而非整体事实准确性
- HalluHard（[halluhard.com/](https://halluhard.com/)）

  一个多轮幻觉基准测试，共包含 950 道题目 ，覆盖四个领域：法律案例（250）、研究问题（250）、医疗指南（250）及编程（200）。利用一个用户大模型生成引人入胜的后续问题，并测量模型在 3 轮对话 （包含首次提问及后续 2 轮）中的表现。 HalluHard 旨在引出开放式响应，同时要求模型将事实主张建立在引用的来源之上。这种设计确保基准测试专门关注幻觉（无依据的事实错误），而非响应的其他方面。  
  对于法律、研究和医学领域，对每个响应抽取 5 个主张并进行逐项判断；对于编程领域，进行逐响应判断。核实流程包括提取主张、通过网络搜索检索证据，并获取全文来源（包括 PDF 解析）以验证引用材料是否支持生成的内容。
- AA-LCR（[Artificial Analysis Long Context Reasoning Benchmark Leaderboard | Artificial Analysis](https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning)）

  专为评估语言模型在多个长文档间进行推理能力而设计的基准。要求模型阅读 10 万 token 的输入（使用 cl100k\_base 分词器衡量），整合输入文档中多个位置的信息，并据此推导出答案。旨在真实还原知识工作者期望语言模型执行的推理任务。涵盖 7 种纯文本文档类型（即公司报告、行业报告、政府咨询、学术文献、法律文件、营销材料和调查报告）。
- Fiction-liveBench（[Fiction.liveBench Sept 29 2025](https://fiction.live/stories/Fiction-liveBench-Sept-06-2025/oQdzQvKHw8JyXbN87/home)）

  评估 AI 模型的长上下文理解能力（针对故事写作），基于一组精选的十几个非常长且复杂的故事情节以及大量经过验证的测验，我们根据这些故事的精简版本生成了测试题。
- Context Arena（MRCR v2）（[contextarena.ai/](https://contextarena.ai/)）

  数据来源为OpenAI发布的MRCR。OpenAI的MRCR测试旨在评估大型语言模型（LLM）处理复杂对话历史的能力。其关键方面包括：  
  核心任务：在冗长的对话（“干草堆”）中找到并区分多个相同的信息片段（“针”）。  
  设置： 受谷歌的[MRCR评估](https://arxiv.org/pdf/2409.12640v2)启发，此版本会插入2、4或8个相同的请求（例如，“写一首关于貘的诗”）以及干扰性请求。关键信息/干扰信息由GPT-4o生成，以实现自然融入。  
  挑战：模型必须根据顺序检索一个特定实例（例如，第二首诗），这需要仔细跟踪对话。它还必须在答案前加上一个特定的随机代码（哈希值）。
- Context-Bench（[Letta Leaderboard](https://leaderboard.letta.com/)）

  评估语言模型在链式文件操作、追踪实体关系以及管理多步骤信息检索方面的能力。
- CL-bench（[www.clbench.com/](https://www.clbench.com/)）（人工设计和验证）

  一种上下文学习基准，包含1,899 项任务实例，要求模型从提供的上下文中学习新知识，这些知识涵盖从领域特定知识、规则系统、复杂程序执行到源于经验数据的法则，而所有这些在预训练阶段均未涉及。每个实例包含一个系统提示、一个任务、用于解决任务所需的新知识的上下文，和用来评估任务的评分标准。所有实例均标注自经验丰富的领域专家。每个实例中的情境最多包含 12 个任务（平均 3.8 个）；标注每个情境平均需要专家投入 20 小时；包含具有任务依赖性的多轮交互。
- DeR²（[retrieval-infused-reasoning-sandbox.github.io/](https://retrieval-infused-reasoning-sandbox.github.io/)）

  一个受控的深度研究沙盒，它隔离了基于文档的推理，同时保留了深度搜索的核心难点：多步综合、去噪和基于证据的结论推导。DeR² 通过四种模式将证据获取与推理解耦—— 仅指令（衡量参数化知识） 、仅概念 （无文档的概念）、 仅相关项（指令 + 相关文档）和完整集合 （相关文档加上主题相关的干扰项），从而产生可解释的模式差距，这些差距可操作化地衡量检索损失与推理损失，并实现细粒度的错误归因。数据来自于2023-2025在物理、数学和 IT 领域的理论论文。
- LOCA-bench（[github.com/hkust-nlp/LOCA-bench](https://github.com/hkust-nlp/LOCA-bench)）

  旨在评估语言智能体在极端且可控的上下文增长场景下的表现。给定任务提示后，LOCA-bench 利用自动化和可扩展的环境状态控制来调节智能体的上下文长度。在保持任务语义不变的前提下，将上下文长度扩展至任意规模。

## AI4S（特化领域）

- 司南科学智能评测（[opencompass.org.cn/Intern-Discovery-Eval/rank](https://opencompass.org.cn/Intern-Discovery-Eval/rank)）

  依托科学能力导向的开源数据集进行评测，系统评估大语言模型在真实科学研究流程中的综合能力表现。
- MathArena（[matharena.ai/?view=problem](https://matharena.ai/?view=problem)）

  MathArena 是一个用于评估 LLMs 在最新数学竞赛中表现的平台，目标是严格检验 LLMs 在面对模型训练期间未曾接触过的新数学问题时，其推理和泛化能力。在评估性能时，我们会让每个模型在每个题目上运行 4 次，然后计算其平均得分以及所有运行次数的总成本（以美元计）。所显示的成本是指该模型在单次竞赛的所有题目上运行一次的平均费用。

  包含ArXivMath、IMProofBench、MathArenaApex、Visual Math、Final-Answer Comps、Proof-Based Comps、Project Euler、BrokenArXiv等基准测试。

  ArXivMath：旨在评估LLMs在处理来自近期 arXiv 论文中的数学研究问题上的表现。（人工筛选任务）

  IMProofBench：旨在通过基于证明的问题来评估语言模型在科研级别的数学推理能力。模型可以访问多种工具，包括网络搜索和代码执行功能。

  MathArenaApex：一组从 2025 年举办的各大数学竞赛中精选出的 12 道高难度题目。

  Visual Math：袋鼠数学竞赛题目。Final-Answer Comps和Proof-Based Comps：近期各大数学竞赛题目。

  Project Euler：一个把数学和编程结合起来的题库，专注于需要综合运用数学洞察力、算法思维和编程技能来解决复杂问题。

  BrokenArXiv：测试模型在数学推理中的可靠性。从近期的arXiv论文中提取问题，对其进行轻微干扰，使其成为看似非常合理但可证明为错误的陈述。模型若拒绝证明该陈述，并明确识别出该陈述在现有形式下为假，则会得分。（人工筛选任务）
- AIME25（[AIME 2025 Benchmark Leaderboard | Artificial Analysis](https://artificialanalysis.ai/evaluations/aime-2025)）

  数据集是一个包含数学问题的答案的数据集，具体来源于2025年美国数学邀请赛（AIME）第一部分的考试题目。该数据集适用于问题回答任务，数据集大小小于1000条记录，语言为英语。
- IMO Bench（[imobench.github.io/](https://imobench.github.io/)）

  该基准测试集经过了一组IMO奖牌获得者和数学家的审核（他们总共获得了10枚IMO金牌和5枚IMO银牌）。由于IMO的题目难度极高，既需要严谨的多步骤推理，又需要超越简单套用已知公式的创造力，因此IMO-Bench专门以IMO的难度水平为目标。IMO-Bench由三个基准测试组成，用于评估模型的多种能力：IMO-AnswerBench——一项大规模的正确答案测试，IMO-ProofBench——用于证明写作的更高层次评估，以及IMO-GradingBench——旨在推动对长篇答案的自动评估取得进一步进展。
- FrontierMath（[epoch.ai/frontiermath/tiers-1-4](https://epoch.ai/frontiermath/tiers-1-4)）

  包含 350 道原创数学题（50 道最高难度等级 4 的问题），涵盖从具有挑战性的大学水平问题到可能需要专家数学家数日才能解决的难题。要求：

  1. 明确且可验证的答案
  2. 抵御猜测：答案应具备“防猜测”特性，即随机尝试或简单的暴力方法几乎不可能成功
  3. 计算可行性：解决计算密集型问题时，必须包含脚本，展示如何仅基于该领域的标准知识找到答案。这些脚本在标准硬件上的累计运行时间必须少于一分钟。
- MathScienceBench（[math.science-bench.ai/benchmarks/](https://math.science-bench.ai/benchmarks/)）

  一个面向研究级数学题的 AI 基准测试。让活跃研究者提交 PhD 级别、接近科研语境的数学问题，用来测试大模型在高难度数学推理上的表现。
- PutnamBench（[trishullab.github.io/PutnamBench/leaderboard.html](https://trishullab.github.io/PutnamBench/leaderboard.html)）

  在普特南数学竞赛中对形式化数学推理进行基准测试。包含 1712 个手工构建的形式化问题，题目源自北美顶尖本科数学竞赛——威廉·洛厄尔·普特南数学竞赛。其中 660 个问题使用 Lean 4 形式化，640 个使用 Isabelle 形式化，412 个使用 Coq 形式化。
- GPQA Diamond（[artificialanalysis.ai/evaluations/gpqa-diamond](https://artificialanalysis.ai/evaluations/gpqa-diamond)）（有严重缺陷）

  GPQA 基准中最难的 198 个问题，专为“防谷歌”设计，需要真正的科学专业知识，而非搜索技巧。  
  这些研究生级别的物理、生物和化学问题，只有具备博士学位的领域专家才能稳定解答，因此非常适合用于测试真正的科学推理能力。

  被发现题目在OCR识别和录入过程中存在大量错误，数据处理的工程流程堪称灾难。（来源：[Humanity's Last Hallucination : A Forensic Audit of the Scientific Insolvency in GPQA and HLE](https://zenodo.org/records/18293568)）
- Humanity's Last Exam（[lastexam.ai/](https://lastexam.ai/)）（[Artificial Analysis](https://artificialanalysis.ai/evaluations/humanitys-last-exam)）（有严重缺陷）

  一个处于人类知识前沿的多模态基准，旨在成为涵盖广泛学科的最后一个封闭式学术基准。该数据集包含跨越百余门学科的 2,500 道高难度问题。我们公开发布这些问题，同时保留一个未公开的测试集，用于评估模型过拟合情况。

  在 HLE 上取得高准确率将证明模型在封闭式、可验证的问题以及前沿科学知识方面具备专家级表现，但这本身并不意味着其具备自主研究能力或“通用人工智能”。HLE 测试的是结构化的学术问题，而非开放式的科研或创造性解决问题的能力，因此它是一种聚焦于技术知识与推理能力的衡量标准。

  分为 (w/ tools)有工具（测试angentic能力）和 (w/o tools)（无工具）（测试模型本身智能）两种情况

  被发现题目在OCR识别和录入过程中存在大量错误，数据处理的工程流程堪称灾难。（来源：[Humanity's Last Hallucination : A Forensic Audit of the Scientific Insolvency in GPQA and HLE](https://zenodo.org/records/18293568)）
- CritPt（[CritPt Benchmark Leaderboard | Artificial Analysis](https://artificialanalysis.ai/evaluations/critpt)）

  旨在测试 LLMs 在研究级物理推理任务表现的基准，包含 71 项综合性研究挑战。
- FrontierScience（[openai.com/index/frontierscience/](https://openai.com/index/frontierscience/)）

  openai推出的一个旨在衡量专家级科学能力的新基准。FrontierScience 由物理、化学和生物学领域的专家编写与验证，包含数百道设计为具有挑战性、原创性和意义的问题。FrontierScience 包含两个问题赛道：FrontierScience-Olympiad，用于衡量类似奥赛风格的科学推理能力；FrontierScience-Research，用于衡量真实的科学研究能力。
- PhyArena（HiPhO）（[phyarena.github.io/](https://phyarena.github.io/)）

  对 LLMs 和 MLLMs 物理推理能力的基准测试。HiPhO：高中物理奥林匹克竞赛基准
- OpenJudge（[openjudge.me/leaderboard](https://openjudge.me/leaderboard)）

  LLM在文献推荐、学术翻译、论文润色等场景下的评测排名。文献推荐即评估语言模型推荐真实学术引用的准确性，将每篇论文的引用与四个权威学术数据库（Crossref、PubMed、arXiv 和 DBLP）进行比对，衡量不同模型和学科中的引用幻觉问题。

  OpenJudge有在线评测功能。

## 特定行业基准

### 医学

- Medmarks（[medmarks.ai/](https://medmarks.ai/)）

  专门用于评估大语言模型的医疗应用能力。分为：Medmarks-Verifiable: 14 个可验证的基准测试，主要为选择题解答任务和医疗计算；Medmarks-OE: 6 个开放性基准测试，例如回答患者提出的问题。

### 法律

法律领域Benchmarks参考*[LLM Agents in Law: Taxonomy, Applications, and Challenges](https://arxiv.org/pdf/2601.06216)*附录3

- PLawBench（[github.com/SKYLENAGE-AI/PLawBench](https://github.com/SKYLENAGE-AI/PLawBench)）

  是一个法律垂直领域的评测基准，模拟真实的咨询场景，并通过三大任务模块（用户理解、案例分析、文书生成）和特定的判分标准，来测评大模型的实际法律能力。包括13类不同场景、850个问题、12500条特定评分细则。

  - 还原最真实的法律场景。力求复现“用户理解-案例分析-文书生成”的真实法律实务流程，所有测试案例均基于真实案件改编，通过植入情绪化表述、刻意省略关键事实、设置事实误导等方式，还原实务中充满不确定性的咨询场景。
  - 聚焦科学的推理步骤分析。要求模型遵循“结论先行-事实澄清-法律分析-结论输出”的逻辑链条，重点考察模型推理的连贯性与严谨性。

### 金融

- Finance Agent（[www.vals.ai/benchmarks/finance_agent](https://www.vals.ai/benchmarks/finance_agent)）

  测试各类智能体执行初级金融分析师应具备的任务的能力。包含537道题目，涉及信息检索、市场调研及预测分析等方面。
- TaxCalcBench（[github.com/column-tax/tax-calc-bench?tab=readme-ov-file](https://github.com/column-tax/tax-calc-bench?tab=readme-ov-file)）

  对前沿模型在美国税务计算任务中的评估。包含 51 对用户输入和预期正确计算的税务申报输出，适用于相对简单的税务情况，并包含申报状态、收入来源、税收抵免与扣除项。

## 特殊场景

- Vending-Bench 2（[andonlabs.com/evals/vending-bench-2](https://andonlabs.com/evals/vending-bench-2)）

  一个用于衡量 AI 模型在长时间范围内运营企业表现的基准测试。模型需在一年内模拟运营自动售货机业务，并以其期末银行账户余额进行评分。
- SpeechMap（[SpeechMap.AI Explorer](https://speechmap.ai/)）

  旨在探索人工智能言论的边界。测试不同提供商、国家和话题下，语言模型对敏感和争议性提示的反应。大多数 AI 基准衡量的是模型能做什么，而我们关注的是它们不能做什么：它们回避、拒绝或屏蔽的内容。
- YapBench（[huggingface.co/spaces/tabularisai/YapBench](https://huggingface.co/spaces/tabularisai/YapBench)）

  衡量在简短回答即可的情况下，大型语言模型（LLMs）的啰嗦程度（存在长度偏好）。每个条目都包含一个单轮提示词、一个精心筛选的最小充分基准答案以及一个类别标签。主要指标YapScore以字符为单位衡量超出基准的响应长度，无需依赖任何特定的分词器，不同模型的结果也具有可比性。包含三百多个英文提示词，涵盖三种常见的追求简洁的场景：（A）最小化/模糊输入，理想的应对方式是简短的澄清；（B）封闭式事实性问题，答案简短且固定；（C）单行编码任务，只需一个命令/代码片段即可完成。
- Voxelbench（[voxelbench.ai/leaderboard](https://voxelbench.ai/leaderboard)）

  一种用于评估语言模型在生成体素结构方面的性能的基准测试。
- CAR-bench（[car-bench.github.io/car-bench/](https://car-bench.github.io/car-bench/)）

  一个用于评估多轮工具使用 LLM 智能体在车载助手领域中的一致性、不确定性处理和能力认知的基准测试。该环境包含一个 LLM 模拟用户、领域策略以及涵盖导航、生产力、充电和车辆控制的 58 个相互关联的工具。除了标准的任务完成外，CAR-bench 还引入了 幻觉任务 ，用于测试智能体在缺少工具或信息时的极限认知能力，以及歧义消除任务 ，要求智能体通过澄清或内部信息收集来解决不确定性。

# 视觉理解与推理

视觉评估存在不稳定性，主要原因分为三个：一是数据集规模小；二是标记样式等细节变化会显著影响模型准确率和排名；三是 JPEG 压缩等 对人“不可见” 变化会改变基准测试排名。（参见[lisadunlap.github.io/vpbench/](https://lisadunlap.github.io/vpbench/)）

- MMMU-Pro（[MMMU-Pro Benchmark Leaderboard | Artificial Analysis](https://artificialanalysis.ai/evaluations/mmmu-pro)）

  多项选择选项为 10 个，并引入仅视觉输入格式，其中问题嵌入在截图或照片中。  
  该基准包含 3,460 道题目，涵盖六个核心学科（艺术与设计、商业、科学、健康与医学、人文与社会科学、技术与工程），要求模型在更贴近现实的场景中同时处理视觉与文本信息。
- ZeroBench（[zerobench.github.io/](https://zerobench.github.io/)）

  面向当代大型多模态模型的一项极难视觉基准测试，包含 100 道由设计师团队精心独创并经过广泛评审的挑战性问题，下有334 个子问题，对应回答每个主要问题所需的独立推理步骤
- VisuLogic（[visulogic-benchmark.github.io/VisuLogic/](https://visulogic-benchmark.github.io/VisuLogic/)）

  国内机构推出。包含六大类别（如数量变化、空间关系、属性比较）的 1000 道人工验证题目，从多维度考察多模态大模型的视觉推理能力。
- BabyVision（[xbench.org/agi/babyVision](https://xbench.org/agi/babyVision)）

  xbench 的 AGI 对齐系列的一部分，专注于评估 “无法言说” 挑战中的视觉理解能力。
- WorldVQA（[worldvqa2026.github.io/WorldVQA/](https://worldvqa2026.github.io/WorldVQA/)）

  旨在衡量多模态大型语言模型的事实准确性以及以视觉信息为中心的世界知识储备，专门用来检测“模型实际记住了什么”。该基准通过分层分类体系来评估模型对各类视觉对象的识别与命名能力。分为九个类别：自然与环境（自然）、地点与建筑（地理）、文化、艺术与手工艺（文化）、物品与产品（物品）、车辆、制作工具与交通方式（交通）、娱乐、媒体与游戏（娱乐）、品牌、标志与平面设计（品牌）、体育、装备与场地（体育）、知名人物与公众人物（人物）。测试数据中，中文占比36%，英文占比64%。
- VisGym（[visgym.github.io/](https://visgym.github.io/)）

  由 17 个多种多样的、具有较长预测期的环境组成，这些环境旨在系统地评估、诊断并训练那些能够处理视觉交互任务的视觉语言模型。智能体在选择每个动作时，必须同时考虑它之前的行为以及所观察到的信息。
- OCRBench v2（[99franklin.github.io/ocrbench_v2/](https://99franklin.github.io/ocrbench_v2/)）

  一个用于评估大型多模态模型在视觉文本定位与推理方面的改进基准。包含 10000 组人工验证的问答，且高难度样本占比很高。覆盖31 个不同场景，包括街景、收据、公式、图表等
- MotionBench（[motion-bench.github.io/](https://motion-bench.github.io/)）

  旨在衡量视频理解模型在细粒度运动理解方面的能力。MotionBench 通过六种主要的运动导向问题类型对模型的运动级感知能力进行评估，并包含来自不同来源的数据，确保对现实世界视频内容的广泛代表性。
- EASI Leaderboard（[huggingface.co/spaces/lmms-lab-si/EASI-Leaderboard](https://huggingface.co/spaces/lmms-lab-si/EASI-Leaderboard)）

  多模态大模型空间智能的综合评估，包括VSI-Bench、MMSI-Bench、MindCube-Tiny、ViewSpatial、SITE、BLINK、3DSRBench、EmbSpatial等benchmark。

## 世界模型

- WorldScore（[huggingface.co/spaces/Howieeeee/WorldScore_Leaderboard](https://huggingface.co/spaces/Howieeeee/WorldScore_Leaderboard)）

  统一评估 3D、4D 和 视频模型在根据指令生成世界方面的能力。与现有专注于单场景质量的基准不同，该基准基于明确的摄像机轨迹，将世界生成分解为一系列后续场景生成任务，同时衡量可控性、质量和动态表现。

# OCR与嵌入评测

[Supercharge your OCR Pipelines with Open Models](https://huggingface.co/blog/ocr-open-models)

在测试不同的 OCR 模型时，它们在不同文档类型、语言等方面的性能差异很大。

- OCR Arena（[www.ocrarena.ai/leaderboard](https://www.ocrarena.ai/leaderboard)）

  一个可上传文档、横向比较 OCR/VLM 模型效果并进行公开投票排名的 OCR 评测平台。
- OmniDocBench（[OmniDocBench/README_zh-CN.md at main · opendatalab/OmniDocBench](https://github.com/opendatalab/OmniDocBench/blob/main/README_zh-CN.md)）

  一个针对真实场景下多样性文档解析评测集，这个广泛使用的基准测试因其多样化的文档类型而脱颖而出，包括书籍、杂志和教科书。其评估标准设计精良，支持 HTML 和 Markdown 格式的表格。
- olmOCR-Bench（[olmocr/olmocr/bench at main · allenai/olmocr](https://github.com/allenai/olmocr/tree/main/olmocr/bench)）

  该基准在评估英语方面非常成功。
- Real5-OmniDocBench（[huggingface.co/datasets/PaddlePaddle/Real5-OmniDocBench](https://huggingface.co/datasets/PaddlePaddle/Real5-OmniDocBench)）

  一个面向现实世界场景的全新基准，基于OmniDocBench v1.5数据集构建。该数据集包含五个不同的场景：扫描、扭曲、屏幕拍摄、光照和倾斜。除扫描类别外，所有图像均通过手持移动设备手动获取，以密切模拟现实世界条件。
- OCRVerse（[github.com/DocTron-hub/OCRVerse](https://github.com/DocTron-hub/OCRVerse)）

  首个端到端的综合 OCR 方法，能够统一实现文本中心 OCR 和视觉中心 OCR（例如图表、网页和科学图表）。文本中心型数据类型覆盖九个文档场景：自然场景、书籍、杂志、论文、报告、幻灯片、考试试卷、笔记和报纸，这些场景涵盖了日常生活中的高频文本场景并满足基本的 OCR 需求。视觉中心型数据类型包含六个专业场景：图表、网页、图标、几何图形、电路和分子结构，这些场景专注于专业结构化内容。
- PDF Parse Bench（[github.com/phorn1/pdf-parse-bench](https://github.com/phorn1/pdf-parse-bench)）

  评估不同 PDF 解析方案从文档中提取数学公式的有效性。
- Embedding Leaderboard（[MTEB Leaderboard - a Hugging Face Space by mteb](https://huggingface.co/spaces/mteb/leaderboard)）

  即MTEB Leaderboard，用统一任务集合比较 embedding 模型在检索、分类、聚类等任务上的表现。

# 视频音频生成和角色扮演评测

- DesignArena（[www.designarena.ai/leaderboard](https://www.designarena.ai/leaderboard)）

  包括Code Categories、Web App、Mobile、Full Stack、Agent、Builder、Image、Image Editing、Graphic Design、Logo、SVG、Video、Video Editing、Slides等多个榜单。
- GenExam（[github.com/OpenGVLab/GenExam](https://github.com/OpenGVLab/GenExam)）

  首个多学科文本到图像生成考试基准，包含 1000 个样本，涵盖 10 个学科，考试风格提示按照四级分类法组织。测试模型整合理解、推理和生成的能力。
- UNO-Bench（[UNO-Bench](https://meituan-longcat.github.io/UNO-Bench/)）

  一个统一基准，用于探索全模型中单模态与全模态之间的组合规律，UNO-Bench 中几乎 100% 的问题都需要对音频和视觉信息的联合理解。除了传统的多项选择题外，我们还提出了一种创新的多步骤开放式问答格式，以评估复杂推理能力。

  我们的材料具有三个关键特性：a. 多元来源——主要来自众包的真实世界照片和视频，辅以无版权限制的网站和高质量公共数据集。b. 丰富多样的主题——涵盖社会、文化、艺术、生活、文学和科学。c. 实时录制音频——由超过 20 位真人说话者录制的对话，确保音频特征丰富，反映真实世界的声音多样性。
- Vue（[bytedance.github.io/vidi-website/](https://bytedance.github.io/vidi-website/)）

  字节推出的视频理解测试。

  - VUE-STG：在实际场景中全面评估 STG（时空定位）能力。1）视频时长覆盖约 10 秒至 30 分钟，支持长上下文推理；2）查询格式多数转换为名词短语，同时保留句子级表达能力；3）标注质量采用人工精准标注所有真实时间范围与边界框；4）评估指标采用优化的 vIoU/tIoU/vIoU-Intersection 方案进行多片段时空评估。
  - VUE-TR-V2：视频问答（Video QA）测试，实现了更均衡的视频时长分布和更贴近用户习惯的查询设计。
- VBVR-Bench（[video-reason.com/](https://video-reason.com/)）

  用于评估模型的视频内容推理能力，考察在视频时空一致视觉环境中，模型是否能够理解时空结构（如连续性、交互性和因果性等特性）。包含 200 个精心策划的推理任务，遵循系统的分类体系，以及超过一百万个视频片段，其规模比现有数据集大约三个数量级。
- Role-play Benchmark（[huggingface.co/datasets/MiniMaxAI/role-play-bench](https://huggingface.co/datasets/MiniMaxAI/role-play-bench)）

  一个用于评估在中文和英文场景中运行的角色扮演代理的综合性基准测试。

  该基准测试针对角色扮演代理所面临的三个核心挑战进行了设计：

  世界观的一致性与逻辑性 ：评估智能体消除技术故障及“灾难性遗忘”现象的能力，确保其长期遵循既定的关系规则与世界观法则，从而避免出现破坏沉浸感的矛盾之处。

  故事情节发展 ：评估智能体是否通过丰富的语义表达和富有动机的角色成长来推动剧情发展，同时避免出现重复的模式、剧情停滞或角色行为与设定不符的情况。

  用户偏好（交互质量）：测试智能体的交互边界及响应能力——确保其不会代替用户发声，能够根据上下文作出反应，并且始终能够提供适当的引导，以促进进一步的互动。
- OpenGameEval（[https://github.com/Roblox/open-game-eval/blob/main/LLM_LEADERBOA...](https://github.com/Roblox/open-game-eval/blob/main/LLM_LEADERBOARD.md)）

  一个用于在 Roblox 游戏开发任务中评估 LLMs 的框架。

## 语音识别

- Open ASR Leaderboard（[huggingface.co/spaces/hf-audio/open_asr_leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)）

  对语音识别模型进行评估，包括英语 ASR 评估以及针对主要欧洲语言的多语言基准测试。

## Omni

- OmniGAIA（[huggingface.co/spaces/RUC-NLPIR/OmniGAIA-Leaderboard](https://huggingface.co/spaces/RUC-NLPIR/OmniGAIA-Leaderboard)）

  旨在评估能够跨视觉、音频和语言进行联合推理的原生全模态 AI 智能体。它包含 360 个来自 9 个真实世界领域的开放式任务，主要在两种主要场景下进行测试：带音频的视频和带音频的图像。OmniGAIA 的任务需要复杂的多跳推理和工具集成的问题解决能力（例如执行网络搜索、浏览和代码执行）。

# 社区评测

以下为AI社区大佬们的独立评测

- nao老师的LLM Benchmark（[llm2014.github.io/llm_benchmark/](https://llm2014.github.io/llm_benchmark/)）

  个人性质，使用滚动更新的私有题库进行长期跟踪评测。侧重模型对逻辑，数学，编程，人类直觉等问题的测试。题库规模不大，长期维持在30题/240个用例以内，不使用任何互联网公开题目。题目每月会有滚动更新。题目不公开，意图是分享一种评测思路，以及个人见解。
- LisanBench（[x.com/scaling01](https://x.com/scaling01)）

  X用户Lisan al Gaib（@scaling01）推出的个人评测。给模型一个起始英文单词，模型必须不断生成下一个单词，满足以下所有严格约束：

  - 与前一个单词恰好相差 1 个字母（Levenshtein 编辑距离 \= 1）
  - 必须是有效英文单词（使用 words\_alpha.txt 词典，约 37 万词，但实际只用最大连通分量 ≈ 10.8 万词）
  - 不能重复使用过任何已经出现过的单词
  - 目标：尽可能生成最长的有效链条

  分数 \= 多个不同起始词的最长链长度累加
- ACG-SimpleQA（[prnake.github.io/ACG-SimpleQA/](https://prnake.github.io/ACG-SimpleQA/)）

  是面向中文二次元（ACG，Animation、Comic、Game）领域的客观知识问答数据集，包含 4242 条自动生成精心设计的问答样本。本基准测试旨在评估大语言模型在二次元文化领域的事实性能力。约 99%样本来源于萌娘百科。
- Kaggle Benchmarks（[www.kaggle.com/benchmarks?type=community](https://www.kaggle.com/benchmarks?type=community)）

  包括两种主要类型的基准测试：1）研究基准测试，即由AI实验室的研究人员创建的评估；2）社区基准测试，即由 Kaggle 社区创建的评估，用户能够设计、运行并分享他们自己用于评估人工智能模型的自定义基准测试。指导：[https://www.kaggle.com/docs/benchmarks#How%20to%20create%20a%20b...](https://www.kaggle.com/docs/benchmarks#How%20to%20create%20a%20benchmark)
- prinzbench（[github.com/prinz-ai/prinzbench/](https://github.com/prinz-ai/prinzbench/)）

  一种私有的评估工具，它根据 LLMs 进行美国法律研究和分析的能力（“法律推理”），以及他们在网上查找难以找到的公开信息的能力（“大海捞针”），对 LLMs 进行排名。包括25 道法律研究题目和8 道搜索题目。
- EyeBench-v2（[x.com/adonis_singh](https://x.com/adonis_singh)）

  一个专门用来评估大模型在图像中发现极细微细节能力的视觉基准测试。测试模型在复杂图像中找出微小差异、计数极小物体、识别细微形状/线段等超精细视觉任务
- EQ-Bench 3、Spiral-Bench、Longform Creative Writing、Creative Writing v3、Judgemark（[eqbench.com/index.html](https://eqbench.com/index.html)）

  EQ-Bench 3：一种通过具有挑战性的角色扮演来衡量情商的测试工具。其测试模型在被设定角色后，在处理人际关系冲突和工作场所困境等场景时表现出的同理心、社交能力以及洞察力。

  Spiral-Bench：一个由大语言模型评判的、用于衡量谄媚和错觉强化的基准测试。

  Longform Creative Writing：一个由大型语言模型评判的长篇创意写作基准。

  Creative Writing v3：一个由大语言模型评判的创意写作基准。

  Judgemark：一个衡量大语言模型对短篇叙事作品鉴赏分析能力的基准测试
- Creative Story‑Writing Benchmark、Elimination Game Benchmark、NYT Connections puzzles、Sycophancy Benchmark（[github.com/lechmazur](https://github.com/lechmazur)）

  Creative Story‑Writing Benchmark：评估LLM在遵循创作要求的同时创作引人入胜小说的能力。每篇故事都必须有意义地融入十个必需元素 ：角色、物品、概念、属性、动作、方法、背景、时间框架、动机和基调。

  Elimination Game Benchmark：“淘汰游戏”是一项多人锦标赛，用于测试大语言模型（LLMs）的社交推理、策略制定和欺骗能力。玩家进行公开和私下对话，结成联盟，并逐轮投票淘汰其他玩家，直到只剩下两人。然后，由被淘汰的玩家组成的陪审团进行决定性投票，选出获胜者。

  NYT Connections puzzles：使用940个《纽约时报》Connections字谜游戏对大型语言模型（LLMs）进行评估

  Sycophancy Benchmark：当同一争议以相反的第一人称视角呈现时，模型是否会保持相同的判断，还是会倾向于支持说话的一方？该基准测试直接衡量这种矛盾。  
  核心指标故意设置得较为严格。只有当模型在双方均以第一人称讲述故事时，都对同一争议的两方表示认同，才被视为具有谄媚性。每例包含 5 种视角：一种中立的第三人称版本，两种删减的第一人称版本，以及两种情感化的第一人称版本。
- BalatroBench（[balatrobench.com/index.html](https://balatrobench.com/index.html)）

  对LLM玩《Balatro》的表现进行基准测试，这是一款结合了扑克手牌与类rogue进程的策略卡牌游戏。追踪不同人工智能模型在关键指标上的表现，如到达的回合数、决策准确性和资源效率，以了解它们的战略推理能力。该基准测试特别关注LLM执行工具调用的能力，衡量模型通过 API 交互执行游戏动作的效率。
- mage-bench（[mage-bench.com/](https://mage-bench.com/)）

  LLMs 玩《万智牌》
- RuneBench（[maxbittker.github.io/runebench/](https://maxbittker.github.io/runebench/)）

  评估 AI 在玩《RuneScape》方面的能力，并需要在游戏世界中完成各种任务。测量AI在“观察、决策、行动”循环中的行为。
- InsanityBench（[robinhaselhorst.com/insanityBench](https://robinhaselhorst.com/insanityBench)）

  旨在衡量LLM在解决需要结合推理和想象力任务上的能力。包含 10 个精心制作的任务，通常只为解题者（一个大型语言模型）提供一个故事，可能是一张图片，或是一串神秘的数字文本。有时除了“解决这个极其困难、晦涩难解的谜题”之外，连任何说明都没有。

# 数据质量评估

- OpenDataArena（[opendataarena.github.io/](https://opendataarena.github.io/)）

  让每个训练后数据集都具备可测量性、可比性和可验证性，评估多个领域（通用、数学、代码、科学和长链推理）和多种模态（文本、图像）的训练后数据。通过使用固定模型规模（Llama3 / Qwen2 / Qwen3 / Qwen3-VL 7-8B）和一致的训练配置来控制变量。数据血缘分析现代数据集通常存在高度冗余和隐藏依赖的问题。ODA推出了业内首个数据血缘分析工具，用于可视化开源数据的“谱系”。结构建模：映射数据集之间的关系，包括继承、混合和蒸馏。

# AI硬件性能

- InferenceMAX（[inferencemax.semianalysis.com/](https://inferencemax.semianalysis.com/)）

  通过在主流硬件平台上对热门模型进行基准测试，并在新软件版本发布时更新测试标准。  
  对于每种模型与硬件组合，InferenceMAX 都会遍历不同的张量并行规模和最大并发请求数，生成一张完整的吞吐量与延迟对比图。
- MLPerf Training（[mlcommons.org/benchmarks/training/](https://mlcommons.org/benchmarks/training/)）

  MLPerf 训练基准套件衡量系统训练模型达到目标质量指标的速度。
- AI Hardware Benchmarking & Performance Analysis（[artificialanalysis.ai/benchmarks/hardware](https://artificialanalysis.ai/benchmarks/hardware)）

  针对语言模型推理的 AI 加速系统全面基准测试。使用 Deepseek R1、Llama 4 Maverick、Llama 3.3 70B 和 GPT-OSS 120B，在 NVIDIA 8×H100、8×H200 和 8×B200 系统上测量性能随并发负载的变化趋势。
- GPU Benchmark（[perf.svcfusion.com/](https://perf.svcfusion.com/)）

  - 支持查看不同计算卡的 FP32、FP16、BF16 性能
  - 每一条数据都由人工同 benchmark 脚本跑出来的，不直接搬运纸面数据，并且支持所有人上传自己跑出来的数据
  - 标注测试平台名称，可以对比不同平台显卡性能的差距
