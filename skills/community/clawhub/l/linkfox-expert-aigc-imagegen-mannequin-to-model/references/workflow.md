# 业务流程详述：人台换模特

## 业务目标

将人台图（dress form / mannequin）上的服装"穿"到真人模特身上，生成一张保留原衣服穿着效果的电商展示图。通过 AI 图片解读动态生成出图 prompt，比固定模板更精准地处理不同品类与穿搭组合。

## 输入参数清单

| 参数 | 性质 | 默认 | 说明 |
|------|------|------|------|
| imageUrls | 运行时入参，必填 | — | 图片列表：第1张=人台图（必填），第2张=模特参考图（可选），第3张=背景参考图（可选） |
| customerKeywords | 运行时入参 | "" | 用户补充提示词（模特画像/姿势/场景等额外要求） |
| ratio | 运行时入参 | 1:1 | 图片比例，透传给 imagegen 的 aspectRatio |
| resolution | 运行时入参 | 2K | 分辨率，2K / 4K |
| provider | 运行时入参 | BANANA_PRO | 生图模型：BANANA_PRO / GPT_2_IMAGE / BANANA_2 / AIDRAW_EDIT / WAN2_7 |

## 步骤拆解

| 编号 | 动作 | 上游 | 下游 | 调用能力 |
|------|------|------|------|----------|
| S1 | 校验图片 URL 可访问性 | 用户输入 imageUrls | S2 | 校验 URL / linkfox-file-upload 上传 |
| S2 | 全链路出图（推荐） | S1 imageUrls + customerKeywords + ratio/resolution/provider | 用户 | `run_mannequin.py`（内调 build_textgen_params → textgen → imagegen） |
| S2' | 分步调试（可选） | S1 | S3 | build_textgen_params.py → linkfox-aigc-textgen → linkfox-aigc-imagegen |

## 核心机制

- **动态提词**：textgen 根据人台图做品类判断（上装/下装/连体）、半身补全逻辑（Completion Rule）、模特推理、场景构建，输出精准英文 prompt。
- **Black Box Rule**：不描述目标服装细节（靠 img2img 参考图锚定），避免文字描述与视觉信号冲突。
- **参考图复刻**：传了模特参考图则复刻五官/发型/肤色；传了背景参考图则复刻环境。

## 已知局限 / TBD

- 依赖 textgen 图片理解能力：角度刁钻/光线极差/特征不明显时可能误判品类。
- prompt ≤512 tokens，极复杂场景（多层搭配、大量配饰）可能被截断。
- Black Box Rule 靠 img2img 参考图锚定，模型还原力不足时服装细节可能偏差。
- 仅接受人台图输入；平铺图/已有模特图走 linkfox-aigc-imagegen-cloth（type=MODEL_IMAGE）。
- 仅产出单张；多张需求由套图编排层调度。
- 多一步 textgen 调用意味着比固定模板链路多 5-15 秒延迟。
