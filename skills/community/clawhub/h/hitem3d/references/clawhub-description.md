# Hitem3D

## 中文版

**短描述**  
把图片直接变成可交付 3D 资产：自动识别单图、多视角、人像、打印、AR 或批量任务，默认完成提交、等待、下载和结果交付，不把用户丢在 task id 上。

**长描述**  
Hitem3D 是一个面向生产使用的 image-to-3D skill。它不只是把 Hitem3D API 包一层，而是像一个 3D 生产操作员一样工作：先判断你的真实意图，再选更合适的模型、分辨率、输出格式和成本档位，最后把生成结果下载到本地并明确告诉你保存路径、输出格式、模型参数和预估积分消耗。

**核心亮点**
- 支持单图生成、人像 / 胸像、多视角重建、批量目录处理
- 支持 `GLB`、`OBJ`、`STL`、`FBX`、`USDZ` 导出
- 支持 3D 打印、Apple AR / Quick Look、常规资产生产等不同场景
- 自动区分多视角与批处理，避免把不同任务类型混跑
- 对高成本或大批量任务先提醒，减少误烧 credits
- 默认执行提交 → 轮询 → 下载 → 结果汇报的完整交付链路

**适合人群**
- AIGC 3D 团队
- 电商 / 产品视觉团队
- 游戏、玩具、角色、潮玩概念流程
- 3D 打印工作流
- 需要 `GLB` / `USDZ` 的 AR 内容团队

**示例提示词**
- “把这张产品图变成 3D”
- “给我一个 STL，我要拿去打印”
- “这 4 张前后左右图生成一个更准的模型”
- “把 `designs/` 里的图全部转成 GLB”
- “查下 Hitem3D 还剩多少积分”

**默认策略**
- 常规高质量：`hitem3dv2.0` + `1536` + `GLB`
- 人像 / 胸像：`scene-portraitv2.1` + `1536pro`
- 3D 打印：优先 `STL` + mesh-only
- Apple AR：优先 `USDZ`
- 低成本试跑：`hitem3dv1.5` + `512`

**成本参考**
- 最低约 `5 credits / 次`
- 常规高质量约 `50 credits / 次`
- 高质量人像约 `70 credits / 次`

**信任说明**  
当前版本已完成结构、交互流、参数校验、脚本能力和发布包层面的整理；若要对外宣称“生产级实战验证完成”，仍建议基于真实 `HITEM3D_AK` / `HITEM3D_SK` 跑完 live validation。

## English

**Short description**  
Turn images into production-grade 3D assets from chat, with smart intent routing for single-image, portrait, multi-view, print-ready, AR-ready, and batch workflows.

**Long description**  
Hitem3D is a production-oriented image-to-3D skill built for real delivery, not just raw API access. It behaves like a 3D operator: it identifies the likely workflow, selects sensible defaults, warns before expensive runs, waits for task completion, downloads the output, and reports the saved file path, output format, model, resolution, and estimated credit cost.

**Key highlights**
- Single-image generation for products, renders, concept art, and illustrations
- Portrait / bust mode for faces, avatars, and human likeness workflows
- Multi-view reconstruction from 2–4 images for better geometry fidelity
- Batch folder processing with per-file result summaries
- Export to `GLB`, `OBJ`, `STL`, `FBX`, and `USDZ`
- Cost-aware defaults with confirmation for expensive or large batch runs
- Full submit → wait → download workflow instead of leaving users with raw task IDs

**Best-fit users**
- AIGC 3D teams
- E-commerce and product-visual teams
- 3D printing pipelines
- Game, toy, and collectible concept workflows
- AR teams that need `GLB` or `USDZ` outputs

**Example prompts**
- “Turn this product image into a 3D model.”
- “Give me an STL for 3D printing.”
- “Use these four front/back/left/right images to reconstruct a more accurate model.”
- “Convert all images in `designs/` to GLB.”
- “Check my remaining Hitem3D credits.”

**Trust note**  
This version is strong on workflow design, packaging, and operator behavior. Complete the live-validation checklist with real credentials before publicly claiming full production validation.
