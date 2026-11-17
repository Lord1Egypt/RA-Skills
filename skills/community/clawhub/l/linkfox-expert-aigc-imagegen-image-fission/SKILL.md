---
name: linkfox-aigc-imagegen-image-fission
description: 电商图片裂变。将已有商品图裂变为视觉不同但商品不变的新图片（相似度可控），用于多平台多店铺铺货防关联。
---

# 图片裂变（Image Fission）

将电商 listing 图片裂变为视觉差异化的新图片，商品本身不变，用于多平台多店铺铺货防关联。

---

## 适用场景

| 场景 | 说明 |
|------|------|
| 多店铺铺货 | 同一商品在多个店铺上架，需要不同图片规避平台查重 |
| 批量裂变 | 一次性传入整组 listing 图片（主图、副图、A+ 图），逐张裂变 |
| 单张裂变 | 只对某一张图做裂变处理 |
| 按需触发 | 由生图 agent 的"图片裂变"模式调用，或用户意图匹配时直接调用 |

## 不适用

- 需要改变图片尺寸/比例的场景（本 skill 不做 resize）
- 跨平台风格转换（如亚马逊图转 TikTok 竖版）——裂变产出与原图同平台同风格
- 纯背景替换/抠图/合成——这些是独立能力，不走本 skill
- AI 从零生图（无原图输入）

---

## 输入参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| images | list[image] | — | 用户上传的图片列表（至少 1 张），支持主图、副图、A+ 图 |
| model | string | — | 生图模型，仅允许 `BANANA_PRO`（香蕉Pro）和 `GPT_2_IMAGE`（Image2）两个值；未指定时必须用 AskUserQuestion 让用户选择。不同模型支持的宽高比不同 |
| quality | string | — | 仅 `GPT_2_IMAGE` 模型支持，图片质量参数，由用户选择 |
| similarity_threshold | int | 60 | 相似度上限百分比，裂变后图片相似度需低于此值（prompt 约束） |
| fission_count | int | 1 | 每张原图裂变出几张新图，上限 10 |
| user_prompt | string | — | 用户附加提示词，拼接在基础 prompt 之后 |
| image_advice_list | list[object|string] | — | 每张原图对应的修改建议，顺序必须与 `images` 一致。对象可包含 `image`/`url`、`slot`/`label`、`type`、`advice`；用于 Listing Agent 的“逐图建议 + 重新作图”场景 |

---

## 流水线步骤

> **执行编排**：全串行，无并行空间。每步输出为下一步必需输入（S1→S2→S3→S4→S5），不可乱序或并发。

### 步骤 1：参数校验与模型确认

- **输入**：`images`、`model`、`quality`、`fission_count`、`user_prompt`、`image_advice_list`
- **操作**：
  1. 校验 `images` 非空
  2. **图片 URL 校验**：检查 `images` 中每个值：已是公开 URL（http/https 开头）→ 直接使用；本地文件路径（非 http/https）→ 调 `linkfox-file-upload` 上传获得公开 URL 后替换。确保所有图片地址为公开可访问的 HTTPS URL
  3. `model` 仅允许 `BANANA_PRO` 和 `GPT_2_IMAGE` 两个值；未指定或传入其他值时，用 `AskUserQuestion` 让用户从这两个中选择，不透传非法值给底层
  4. `quality` 仅 `GPT_2_IMAGE` 生效（用户未提供则询问），其他模型忽略
  5. **逐图建议校验**：如果传入 `image_advice_list`，其长度必须等于 `images.length`；不允许把多张图的建议压成一条全局建议。长度不一致时停止并用 `AskUserQuestion` 要求调用方补齐或确认只给建议不作图。
  6. **数量冲突检测**：检查 `user_prompt` 中是否包含明确的数量描述（匹配模式：`生成/裂变/出/画/要 N 张/幅/组/份`），若提取到的数量与 `fission_count` 参数不一致，则**以 `fission_count` 参数为准**，并在执行前告知用户：「您在描述中提到生成 X 张，但参数设置为 Y 张，将按参数生成 Y 张。」——不阻塞流程、不弹选择框，仅做信息提示后继续执行
- **输出**：`images`（全部为公开 URL）、`model`、`quality`（透传）、`image_advice_list`
- **用途**：作为步骤 2 和步骤 4 的模型配置输入

### 步骤 2：图片队列生成

- **输入**：`images`、`image_advice_list`
- **操作**：
  1. 根据用户上传的图片数量，将所有图片自动加入处理队列
  2. 若存在 `image_advice_list`，按数组下标把每张图和对应建议绑定成同一个队列项，保留 `slot`/`label`/`type` 等信息。若建议项是字符串，视为该图的 `advice`
- **输出**：`processing_queue`（待裂变的图片队列）
- **用途**：作为步骤 4 的逐张处理输入

### 步骤 3：组装 Prompt

- **输入**：`similarity_threshold`、`user_prompt`、`processing_queue`
- **操作**：
  1. 基础 prompt：`不要改变图中商品，帮我把这些图分别裂变成另外一张，相似度必须低于{similarity_threshold}%`
  2. 若 `user_prompt` 非空，拼接到基础 prompt 末尾：`{base_prompt}。{user_prompt}`
  3. 对 `processing_queue` 中每张图分别生成 `final_prompt`。如果队列项含逐图建议，在该图 prompt 末尾追加：`当前图片位置：{slot/label/type}。当前图片修改建议：{advice}`。
  4. 基础约束（不改变商品 + 相似度阈值）始终保留，`user_prompt` 与逐图建议只做叠加，不允许覆盖基础约束。
  5. 逐图建议只作用于对应原图；禁止把 A 图建议用于 B 图，禁止把逐图建议合并成一个全局 prompt 后传给所有图片。
- **输出**：`processing_queue`（每个队列项都带自己的 `final_prompt`）
- **用途**：作为步骤 4 的生图指令

### 步骤 4：逐张裂变生图

- **输入**：`processing_queue`（含逐图 `final_prompt`）、`model`、`quality`、`fission_count`
- **操作**：
  1. 遍历 `processing_queue`，对**每张图**单独调用 skill `linkfox-aigc-imagegen`（**唯一调用方式，禁止改用其它 skill 或直接调脚本**），传入参数：
     - `imageUrls`：只放**当前这一张**原图
     - `prompt`：当前队列项自己的 `final_prompt`
     - `provider`：本 skill 的 `model` 参数直接透传（仅允许 `BANANA_PRO` 或 `GPT_2_IMAGE`，必须由用户选择）
     - `outputNum`：固定 `1`，每次只生成一张；`fission_count > 1` 时对同一原图循环调用多次
     - `resolution`：默认 `1K`，不做放大
     - `aspectRatio`：按原图比例原样透传，无法判定时传 `1:1`，合法性由底层判定
     - `quality`：仅 `provider=GPT_2_IMAGE` 时传 `quality`，其它 provider 省略该字段
  2. **skill 输出原封不动透传**：`linkfox-aigc-imagegen` 自行完成调用与输出，本 skill 不做二次包装、不截取、不重新输出
  3. **每调用一次都按「错误处理与失败护栏」判定成败**：成功则该张完成，失败按护栏处理，**不得直接跳过当无事发生、也不得换 skill 重试**
  4. 收集成功的本地路径，记录失败的原图及原因
- **输出**：`fission_results`（原图→裂变图本地路径的映射列表，含失败标记）
- **用途**：作为步骤 5 的产出整理输入

### 步骤 5：产出整理与展示

> 图片本身已由步骤 4 各次 Bash stdout 里的 `Saved full response: [path]` 经 bridge 自动渲染给用户；本步只在对话正文补一段「原图 ↔ 裂变结果」对照表。

- **输入**：`fission_results`（含失败标记）
- **操作**：跳过失败项，把成功项**按下方示例的结构原样照抄**渲染对照表；失败项另列。
- **硬性约束**（示例本身无法表达的边界，违反即视为故障）：
  - 裂变结果必须是**完整绝对路径**（`/root/.linkfox/.../xxx.jpg`），不得截断为文件名 / 相对路径，不得改用反引号纯路径、裸路径或 `Saved full response:` 行——bridge 不会消费正文里的 `Saved` 标记，写出来只会变成裸文本污染对话。
  - 逐图修改建议（`image_advice_list`）只在步骤 3 进入 prompt，不进入本表。
- **输出格式（即唯一真相源：列数 / 渲染形态 / 多张分隔 全部以此为准，正文不再重复描述）**：
  ```
  | 原图 | 裂变结果 |
  |------|----------|
  | ![原图1](https://example.com/original-1.jpg) | ![裂变结果1-1](/root/.linkfox/workspaces/linkfox/2026-06-13/xxx/media/linkfox-aigc-imagegen-1781338777684.jpg)<br>![裂变结果1-2](/root/.linkfox/workspaces/linkfox/2026-06-13/xxx/media/linkfox-aigc-imagegen-1781338779012.jpg) |
  | ![原图2](https://example.com/original-2.jpg) | ![裂变结果2](/root/.linkfox/workspaces/linkfox/2026-06-13/xxx/media/linkfox-aigc-imagegen-1781338781456.jpg) |
  ```
  失败项另列：
  ```
  **失败项：**
  - 原图 3：[失败原因]
  ```
- **用途**：最终交付给用户。

---

## 错误处理与失败护栏

> `linkfox-aigc-imagegen` skill 对**业务失败也返回 exit 0**（不是非零退出），所以**不能靠命令退出码判断成败，必须解析 stdout**。

**1. 怎么判一次调用成败**
- **成功**：stdout 含 `Saved full response: ["xxx.png", ...]`（JSON 数组路径）→ 图片已落盘 media/，取路径展示。
- **失败**：stdout 含 `Saved full response: xxx.json`（单个 JSON 文件路径，非数组）→ 无图片产物，需读该 JSON 查看错误详情（`errcode`/`errmsg`/`error`）。

**2. 失败怎么处理（按类型分流，不允许即兴发挥）**
| 失败类型 | 判断依据 | 处理 |
|----------|----------|------|
| 参数非法 | `errmsg`/`errorMsg` 指向 `provider`/`model`、`aspectRatio`、`resolution`、`quality` 等入参不被接受 | 用 `AskUserQuestion` 让用户重选对应参数后**重跑当前这一张**；不转述原始报错 |
| 认证失败 | `errcode==401` 或提示 API Key | 停止并提示用户配置 `LINKFOX_AGENT_API_KEY`，不重试 |
| 瞬时错误 | `error` 为网络/超时/连接失败（`Connection failed`、timeout 等） | **最多自动重试 1 次**；再失败转「其它错误」 |
| 其它错误 | 配额、内容被拒、服务端 5xx、未知 errcode 等 | **不重试**，把该张标记为失败并记录原因，继续处理队列里**其余原图** |

**3. 硬性护栏（违反即视为故障）**
- ❌ **禁止因生图失败改调任何其它 skill**（包括 `linkfox-aigc-imagegen` 之外的生图/编排 skill、product/cloth 系列等）——本 skill 的生图路径唯一，失败就按上表处理或上报，绝不"换一个 skill 试试"。
- ❌ **禁止无上限重试**：除"瞬时错误最多 1 次"外，同一张图的同一类失败不得反复重试。
- ❌ **禁止把失败的返回体当成功**继续往下走（展示空图、告诉用户"已生成"）。
- ✅ 整个队列跑完后，若存在失败项，在最终结果里**逐项注明失败原因**交给用户，由用户决定是否调整参数重跑。

---

## 执行自检

每次跑完流程，agent 在收尾时确认：

- [ ] 每张图都按「错误处理与失败护栏」判定过成败；成功项的本地路径已按步骤 5 示例结构填进对照表，失败项注明原因
- [ ] 如果传入 `image_advice_list`，每张原图都只使用了自己的对应建议，且没有把逐图建议合并成一个全局 prompt
- [ ] 成功裂变图数量 = 成功原图数 × fission_count（失败原图不计入）
- [ ] 失败时未改调其它 skill、未无上限重试、未把失败返回体当成功
- [ ] 未对图片做尺寸变更

---

## 已知局限

- **相似度为 prompt 约束**：`similarity_threshold` 通过 prompt 语义引导模型降低相似度，非硬性校验机制；实际相似度可能偏离设定值
- **模型能力边界**：极复杂的图片（大量文字、密集排版）裂变效果可能不理想
- **不做内容审核**：裂变产出不经过合规检查，用户需自行确认是否符合目标平台规则
