# Core Dimensions

Use this file to collapse the benchmark universe into a smaller set of report axes. A benchmark may have one **primary dimension** and multiple **overlap tags**. Reports should synthesize at the dimension level first, then support claims with benchmark-level evidence.

If a benchmark is not mentioned here, consult `benchmark-source.md` and map it to the nearest dimension without creating a brand-new top-level dimension unless the user explicitly asks for a niche domain.

## 1) general capability and composite frontier
Use for `overall strongest`, `frontier models`, `general ability`, `综合能力`, `综合评测`.

Primary benchmark cluster:
- Artificial Analysis Intelligence
- Epoch Capability Index (ECI)
- LiveBench
- LMArena
- OpenCompass comprehensive boards
- llm-stats benchmark hub (discovery-first, not usually final evidence)
- Vals Index
- SEAL LLM Leaderboards
- Sansa Bench
- CAIS AI Dashboard (text and automation views)
- AGI-Eval comprehensive boards
- 晓天衡宇评测 large-language-model board

Overlap tags:
- reasoning
- coding
- math and science
- tool use
- human preference
- safety and risk

## 2) coding and software engineering
Use for `coding`, `software engineering`, `repo patching`, `debugging`, `frontend`, `terminal coding`, `agentic coding`.

Primary benchmark cluster:
- SWE-bench Pro
- SWE-bench Multilingual
- SWE-bench Mobile
- LiveCodeBench / GSO Benchmark / LiveCodeBench Pro
- OJBench
- CursorBench
- Roo Code evals
- cto bench
- OpenHands Index
- Windsurf Arena Leaderboard
- BridgeBench
- Code Review Bench
- SanityHarness
- LongCLI-Bench
- ProjDevBench
- Android Bench
- OctoCodingBench
- ALE-Bench
- OpenGameEval

Secondary pull-ins when the task is broader than plain code generation:
- Terminal-Bench / Terminal-Bench Pro
- Metr time-horizon analysis
- DesignArena code / web app / mobile / full stack / agent / builder categories
- MathArena Project Euler
- OpenJudge when research-oriented coding or citation tasks are relevant
- SciCode, Frontier-CS, KernelBench, Kernel Arena, PostTrainBench, WeirdML for research-heavy coding ability

Overlap tags:
- terminal use
- long-horizon tasks
- project development
- code review
- optimization
- instruction following

## 3) agentic tool use and workflow execution
Use for `tool use`, `function calling`, `mcp`, `workflow execution`, `assistant agent`, `agentic`.

Primary benchmark cluster:
- GAIA
- BFCL-V4
- Toolathlon
- AgencyBench-V2
- MCPMark
- MCP Atlas
- PinchBench
- Claw-Eval
- xbench AGI track
- AgentIF-OneDay
- SpreadsheetBench
- FACTS search and grounding tracks

Secondary pull-ins:
- IFBench for precise instruction following
- VitaBench and DeepPlanning for real planning with tool usage
- CAIS AI Dashboard automation
- SEAL and OpenCompass if they expose explicit agent/tool subscores

Overlap tags:
- function calling
- planning
- multi-step execution
- browsing and retrieval
- long context

## 4) deep research and search
Use for `deep research`, `search`, `multi-step retrieval`, `grounded synthesis`, `research agent`.

Primary benchmark cluster:
- DeepSearchQA
- DeepResearch Bench II
- FutureSearch Deep Research Bench
- MMDeepResearch-Bench
- xbench-DeepSearch
- DeR²
- FACTS grounding and search tracks
- HalluHard when grounded citation behavior matters

Secondary pull-ins:
- FutureX for dynamic real-world forecasting and search-heavy reasoning
- AA-LCR, Context Arena, Context-Bench, CL-bench, LOCA-bench when long-context retrieval is the bottleneck
- OmniGAIA when research requires audio + image + web evidence

Overlap tags:
- browsing
- citation grounding
- multimodal evidence
- long context
- synthesis quality

## 5) gui, computer use, and device operation
Use for `computer use`, `gui agent`, `desktop`, `mobile agent`, `screen grounding`, `device workflows`.

Primary benchmark cluster:
- OSWorld-Verified
- AndroidDaily
- AndroidWorld
- Mobile World
- ScreenSpot-Pro

Secondary pull-ins:
- CAIS AI Dashboard visual and automation views
- GAIA or AgencyBench-V2 if the task mixes GUI use with broader tool execution
- FACTS multimodal when factual image understanding is part of the task

Overlap tags:
- screenshot understanding
- multi-app workflows
- mobile ui
- visual grounding

## 6) reasoning, knowledge, and instruction following
Use for `intelligence`, `reasoning`, `knowledge`, `instruction following`, `iq-like tests`, `多轮对话推理`.

Primary benchmark cluster:
- ARC-AGI-2
- MultiChallenge
- MMLU-Pro
- SimpleBench
- TRUEBench
- Bullshit Benchmark
- Pencil Puzzle Bench
- IFBench
- AA-Omniscience
- FACTS knowledge track

Secondary pull-ins:
- Artificial Analysis Intelligence
- LiveBench reasoning-heavy slices
- community reasoning benchmarks such as LisanBench, nao benchmark, NYT Connections, InsanityBench
- xbench-ScienceQA when science knowledge matters

Overlap tags:
- symbolic reasoning
- conversation consistency
- instruction adherence
- world knowledge
- adversarial prompts

## 7) long context, memory, and factuality
Use for `long context`, `memory`, `recall`, `document reasoning`, `hallucination`, `citation fidelity`.

Primary benchmark cluster:
- Hallucination Leaderboard
- HalluHard
- AA-LCR
- Fiction-liveBench
- Context Arena (MRCR v2)
- Context-Bench
- CL-bench
- DeR²
- LOCA-bench

Secondary pull-ins:
- DeepResearch Bench II and FutureSearch when report writing and retrieval interact
- SpreadsheetBench for long spreadsheet state tracking
- MultiChallenge when conversational memory and consistency matter

Overlap tags:
- grounded summary
- long-document reasoning
- dialogue memory
- retrieval-infused reasoning

## 8) math, science, and research automation
Use for `math`, `scientific reasoning`, `physics`, `biology`, `chemistry`, `research coding`, `ai4s`.

Primary benchmark cluster:
- MathArena family (ArXivMath, IMProofBench, MathArenaApex, Visual Math, Final-Answer Comps, Proof-Based Comps, Project Euler, BrokenArXiv)
- AIME 2025
- IMO Bench
- FrontierMath
- MathScienceBench
- PutnamBench
- GPQA Diamond
- Humanity's Last Exam (with and without tools)
- CritPt
- FrontierScience
- PhyArena (HiPhO)
- 司南科学智能评测
- OpenJudge
- SciCode
- Frontier-CS
- AlgoTune
- KernelBench v3
- Kernel Arena
- PostTrainBench
- WeirdML

Overlap tags:
- olympiad math
- scientific qa
- research tasks
- optimization and kernels
- code-heavy science
- long-form proofs

## 9) vertical domains and economic value
Use for `law`, `finance`, `medical`, `economic value`, `customer service`, `planning`, `daily-life workflows`, `white-collar tasks`.

Primary benchmark cluster:
- GDPval-AA
- VitaBench
- DeepPlanning
- Remote Labor Index (RLI)
- APEX-Agents / APEX / ACE
- τ²-bench / τ²-Bench-Verified
- Medmarks
- PLawBench
- Finance Agent
- TaxCalcBench
- Vending-Bench 2
- CAR-bench

Secondary pull-ins:
- Vals Index for a composite view over finance, law, and software engineering
- Sansa Bench when office/review tasks matter
- OpenJudge for academic writing and citation workflows

Overlap tags:
- white-collar work
- customer service
- consumer tasks
- professional domains
- task economics

## 10) multimodal perception and world understanding
Use for `multimodal`, `vision`, `image reasoning`, `video`, `audio`, `ocr`, `omni`, `world knowledge from images`.

Primary benchmark cluster:
- MMMU-Pro
- ZeroBench
- VisuLogic
- BabyVision
- WorldVQA
- VisGym
- OCRBench v2
- MotionBench
- EASI Leaderboard benchmark family
- OmniGAIA
- UNO-Bench
- Vue
- VBVR-Bench
- WorldScore
- Open ASR Leaderboard

Secondary pull-ins:
- FACTS multimodal track
- MMDeepResearch-Bench
- GUI/computer-use benchmarks when the visual task is interactive
- OCR Arena, OmniDocBench, Real5-OmniDocBench, OCRVerse, PDF Parse Bench, Embedding Leaderboard when document perception or retrieval is central
- DesignArena image, image editing, graphic design, logo, svg, video, video editing, slides categories

Overlap tags:
- visual reasoning
- ocr and document parsing
- video understanding
- audio understanding
- grounded world knowledge

## secondary overlays
Use these only when the user explicitly asks, or when they materially change the conclusion.

### openness, adoption, and community signal
- Relative Adoption Metric (RAM)
- Artificial Analysis Openness Index
- community benchmarks: nao benchmark, LisanBench, ACG-SimpleQA, prinzbench, EyeBench-v2, EQ-Bench 3, Spiral-Bench, Longform Creative Writing, Creative Writing v3, Judgemark, Creative Story-Writing Benchmark, Elimination Game Benchmark, NYT Connections, Sycophancy Benchmark, BalatroBench, mage-bench, RuneBench, InsanityBench

### safety, censorship, and refusal behavior
- SpeechMap
- Sansa censorship board
- CAIS risk view
- SKILL-INJECT when prompt-injection robustness is central

### document intelligence and embeddings
- OCR Arena
- OmniDocBench
- Real5-OmniDocBench
- OCRVerse
- PDF Parse Bench
- Embedding Leaderboard

### data quality and hardware context
- OpenDataArena
- InferenceMAX
- MLPerf Training
- Artificial Analysis hardware benchmarks
- GPU Benchmark

## cross-category expansion triggers
When the user asks for one capability, do not stop at the obvious section. Expand like this:

- **coding** -> dimensions 2 + 3 + 8 + 1 + relevant community overlays
- **agentic coding** -> dimensions 2 + 3 + 5 + 8 + 9
- **reasoning / intelligence** -> dimensions 6 + 8 + 1 + selected community overlays
- **multimodal** -> dimensions 10 + 5 + 4 + 9
- **deep research** -> dimensions 4 + 7 + 10 + 3
- **long-context or grounding** -> dimensions 7 + 4 + 3
- **vertical domain analysis** -> dimension 9 plus any capability dimension that dominates the target workflow

## routing reminder
Keep reports compact by mapping evidence back to these dimensions. Do not create a separate top-level report section for every benchmark unless the user explicitly requests exhaustive coverage.
