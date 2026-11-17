---
name: linkfox-expert-aigc-imagegen-bestseller-replicate
description: 爆款复刻。上传商品原图 + 亚马逊 listing 链接/ASIN 或爆款参考图，自动将参考图的排版与风格套用到你的商品上批量生成新图。
---

# 爆款复刻（Bestseller Replicate）

参照销量好的亚马逊 listing 图片（或用户上传的爆款参考图），把它们的排版与风格套用到用户自己的商品原图上，逐张生成对应的新图。最终把"参考图 → 复刻图"对照展示给用户。

本 skill 编排 `linkfox-amazon-product-detail` 与 `linkfox-aigc-imagegen` 两个底层能力完成流程。

---

## 适用场景

卖家/运营看到一个卖得好的 listing，想让自己的商品也拥有同款图片效果（同样的排版、场景、模特呈现），按需触发、即时拿到一组复刻图。

| 场景 | 说明 |
|------|------|
| 对标亚马逊爆款 | 给一个亚马逊链接/ASIN + 自己的商品原图，复刻该 listing 的商品图集（主图与附图） |
| 对标自备参考图 | 直接上传几张看中的爆款商品图 + 自己的商品原图，逐张复刻（不限平台） |

## 不适用

- 纯从零生图、没有商品原图 → 直接用 `linkfox-aigc-imagegen`。
- 同款商品换图防关联/铺货（商品不变、只要视觉差异） → `linkfox-aigc-imagegen-image-fission`。
- 只要抠图/换背景/单点修图 → 不走本流程。
- 视频复刻 → `linkfox-viral-video-replicate`。

---

## 输入参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| product_image | image | — | 用户的商品原图（"图一"），1 张，必填，作为每次生成的主体 |
| amazon_input | string | — | 方式 A：亚马逊 listing 链接或 ASIN；从中解析 ASIN + 站点 |
| reference_images | list[image] | — | 方式 B：用户上传的参考爆款图（"图二"），可多张 |
| provider | string | GPT_2_IMAGE | 生图模型（imagegen 现支持 `BANANA`/`BANANA_2`/`BANANA_PRO`/`GPT_2_IMAGE`/`AIDRAW_EDIT`/`WAN2_7` 等）；本 skill 不锁枚举，直接透传给 imagegen，合法性由 imagegen 判定 |
| quality | string | high | 图片质量 `low`/`medium`/`high`，仅 `GPT_2_IMAGE` 生效 |
| resolution | string | 2K（缺省） | 图片分辨率，前端传了原样透传给 imagegen；前端未传时缺省 `2K`。本 skill 不校验枚举 |
| aspectRatio | string | 默认=逐张跟图二 | 复刻图宽高比。前端「默认比例」/「默认」/`auto`/空 → S3 逐张探测当前图二真实显示宽高，按原始像素组装 `W:H`（如 `1400:600`）传给 imagegen；用户选了具体比例（如 `1:1`、`16:9`）→ 所有复刻图统一透传该值 |
| include_aplus | boolean | true | **仅方式 A**。是否把 listing 的 A+ 图纳入参考图集；默认 `true`（主副图 + A+ 全量）。用户说「只要主图 / 仅主副图 / 不要 A+ / 不含 A+」或前端显式传 `false` 时设为 `false`，S2 只取 `productImageUrls` |

> 输入方式二选一：给了 `amazon_input` 走方式 A，给了 `reference_images` 走方式 B。`product_image` 两种方式都必填——它是所有复刻图的商品主体，缺了无法生成。
> `outputNum` 固定为 `1`（每张参考图出 1 张复刻图，构成 1:1 对照），不暴露给用户。`resolution` 由前端传入并原样透传给 imagegen；前端未传时缺省 `2K`，**不再强制覆盖前端传入的值**。

---

## 流水线步骤

> **执行编排**：步骤之间串行（S1→S2(仅方式A)→S2.5(仅方式A)→S3→S4），每步输出为下一步必需输入，不可乱序。**步骤 3 内部对每张参考图并发调用 `linkfox-aigc-imagegen`，最大并发 4**——各张之间无数据依赖，并发只在 S3 内开启，跨步骤不并发。

### 步骤 1：识别输入方式 + 校验参数（静默执行）

> **用户可见性**：本步骤静默执行，**不输出任何进度文案**（不要写"步骤1""解析参数"等字样）。仅在以下异常场景才对用户输出：缺 `product_image` 需请求补传、ASIN 格式有误需纠正。正常情况下直接进入步骤 2/3，用户无感知。

- **输入**：`product_image`、`amazon_input`(方式A)、`reference_images`(方式B)、`provider`、`quality`、`aspectRatio`、`include_aplus`(方式A，可空)
- **操作**：
  1. 先确认 `product_image` 存在——它是每张复刻图的商品主体，没有它整个流程无从开始；缺失时用 `AskUserQuestion` 请用户补上传，不要凭空继续。
  2. **图片 URL 校验**：检查 `product_image` 和 `reference_images`（方式 B）中的每个值：已是公开 URL（http/https 开头）→ 直接使用；本地文件路径（非 http/https）→ 调 `linkfox-file-upload` 上传获得公开 URL 后替换。确保所有图片地址为公开可访问的 HTTPS URL。
  3. 判定输入方式：给了亚马逊链接/ASIN → 方式 A；给了上传参考图 → 方式 B。两者都给时以方式 A 为准，并提示用户已忽略上传图（避免重复生成）。
  4. 方式 A 解析：从链接里提取 10 位 ASIN 与站点域名；只给了 ASIN 则站点默认 `amazon.com`；ASIN 不是 10 位字母数字时提示用户纠正，而不是硬跑。
  5. **A+ 范围（仅方式 A）**：解析 `include_aplus`，默认 `true`。用户自然语言含「只要主图 / 仅主副图 / 不要 A+ / 不含 A+ / 跳过 A+ / main images only」→ `false`；前端 `<linkfox-params-tag>` 或结构化参数里显式传 `includeAplus: false` / `include_aplus: false` → `false`。未提及且前端未传 → `true`。
  6. **参数透传规则**（合法性由 imagegen 判定，失败由「错误处理与失败护栏」兜底重选，本步不预拦、不转述原始报错）：
     - `provider`：父 agent 在调度前已收齐并透传（父 agent CLAUDE.md 强制不空传），本步**不再询问用户**；万一为空，按默认 `GPT_2_IMAGE` 静默兜底，**不弹 `AskUserQuestion`**
     - `aspectRatio`：**归一化**——值为「默认比例」/「默认」/`auto`/空/仅空白 → 记为默认模式，由 S3 逐张探测当前图二并组装比例；其余具体比例原样保留给 S3 全局透传。**禁止**把「默认比例」文案原样塞给 imagegen
     - `quality`：仅 `GPT_2_IMAGE` 生效（默认 `high`），其他模型忽略
     - `resolution`：前端传了原样透传给 imagegen；前端未传时缺省 `2K`
- **输出**：`input_mode`(A/B)、`product_image_url`（公开 URL）、`asins`+`amazonDomain`(方式A)、`include_aplus`(方式A，默认 true)、`provider`、`quality`、`resolution`(前端值/缺省 2K)、`aspectRatio`(可空；空=S3 逐张探测图二并回填 `W:H`)
- **用途**：`input_mode` 决定是否执行步骤 2；`asins/amazonDomain/include_aplus` 作为步骤 2 输入；原图 URL 与模型参数作为步骤 3 输入

### 步骤 2（仅方式 A）：抓取 listing 参考图

- **输入**：`asins`、`amazonDomain`、`include_aplus`（步骤 1 的输出）
- **操作**：调用 `linkfox-amazon-product-detail`，传 `asins`、`amazonDomain`，不开 `returnBoughtTogether`/`returnRelatedProducts`/`returnAuthorsReviews`（附加开关只增加成本，本 skill 用不到）。该 skill 对大响应有落盘策略（详情页字段多），响应较大时它会写入会话 `data/` 目录；**禁止**用 inline `jq` 手抠图片 URL——必须调用本 skill 的 `scripts/extract_reference_images.py` 从落盘 JSON 提取，避免漏 A+ 或解析不一致。
- **抽取命令（唯一正源）**：
  - `include_aplus=true`（默认）：`python <skill_path>/scripts/extract_reference_images.py <detail-json路径>`
  - `include_aplus=false`：同上，追加 `--main-only`
  - 从 stdout 一行 JSON 取 `reference_images`、`main_count`、`aplus_count`；脚本返回 `error` 时按抓取失败处理，提示用户换 ASIN 或重试
- **抽取规则（脚本内部实现，禁止 agent 自行改写）**：
  - 主副图 = `.products[0].productImageUrls[]`（保持原顺序）
  - A+ 图 = 解析 `.products[0].productDescription` 字符串为 JSON 数组，按 `position` 取每项 `image` 及嵌套 `carouselImages[].image`（有 A+ 时该字段为 JSON 字符串，见 `linkfox-amazon-product-detail/references/api.md`）
  - 合并顺序：主副图在前，A+ 在后；全链路 URL 去重（主图优先）
  - **不要**取 `imageUrl`（缩略图）、`thumbnail`、`reviewsImages` 等其它图片字段
  - **不要**尝试取 `aplusImages` / `mainImage` / `images` 等——响应里没有这些键；A+ 走 `productDescription` 解析，不是猜字段
- **输出**：`reference_images`（listing 参考图 URL 列表，作为"图二"集合）、`main_count`、`aplus_count`
- **用途**：作为步骤 2.5 数量告知与步骤 3 的参考图集

### 步骤 2.5（仅方式 A）：参考图数量告知

- **输入**：`reference_images`、`main_count`、`aplus_count`、`include_aplus`（步骤 2 的输出）
- **操作**：向用户输出 **1 行**数量文案，立即进入步骤 3。按场景选模板（只输出一行，不要表格）：
  - `include_aplus=true` 且 `aplus_count>0`：「共找到 N 张参考图（主副图 X 张 + A+ 图 Y 张），将逐张复刻。」（N=X+Y）
  - `include_aplus=false`：「共找到 N 张参考图（仅主副图），将逐张复刻。」
  - 其余（无 A+ 或 listing 未配置 A+）：「共找到 N 张参考图，将逐张复刻。」
- **输出**：`reference_images`（原样透传给步骤 3）

### 步骤 3：逐张配对生图（S3 内并发，最大 4）

- **输入**：`product_image`（图一）、`reference_images`（图二集，来自步骤 2.5 或方式 B 上传）、`provider`、`quality`、`aspectRatio`(可空)
- **操作**：对参考图集**并发**调用 skill `linkfox-aigc-imagegen`（唯一调用方式，禁止改用其它 skill 或直接调脚本），**最大并发 4**——各张之间无数据依赖，全程并发可显著缩短总耗时。每张调用的逻辑：
  1. 确定本张传给 imagegen 的 `aspectRatio`（**始终传该字段**）：
     - 步骤 1 归一化后有具体 `aspectRatio` → **所有复刻图统一透传该值**给 imagegen。
     - 步骤 1 归一化后为默认模式（含前端「默认比例」/空）→ 调用 `python <skill_path>/scripts/probe_image_size.py <当前图二URL>`，从输出 JSON 读取 `aspectRatio`；脚本已按 EXIF 方向校正显示宽高，并按原始像素组装 `W:H`、不约分，例如图二为 `1400×600` 时传 `"1400:600"`。每张图二独立探测，禁止复用其他参考图的比例。
     - 探测返回 `error` 或缺少合法 `aspectRatio` → 当前参考图按「错误处理与失败护栏」标记失败并跳过，不臆造比例；其他并发任务继续。
  2. 组装调用参数：
     - `imageUrls` = `[product_image_url, reference_image_url]`，顺序固定为 [图一原图, 图二参考图]，与固定提示词里的"图一/图二"一一对应，颠倒会让模型把参考商品当成主体。
     - `prompt`：**固定提示词的唯一正源在 `references/workflow.md`〈配对与提示词〉段**，运行时读取该段全文原样使用，不接受用户覆盖、不在 SKILL.md 或别处内联复制。
     - `provider`、`quality`（仅 GPT_2_IMAGE）**透传**给 imagegen；`aspectRatio` 必传：具体比例用步骤 1 的用户选项，默认模式用当前图二探测得到的原始 `W:H`，本 skill 不预校验 imagegen 的比例枚举
     - `outputNum` = `1`（一张参考图对应一张复刻图，构成 1:1 复刻）、`resolution` = 步骤 1 透传的前端值（前端未传则缺省 `2K`），不硬编码强制覆盖前端值
  3. **skill 输出原封不动透传**：`linkfox-aigc-imagegen` 自行完成调用与输出，本 skill 不做二次包装、不截取、不重新输出。
  4. **每调用一次都按「错误处理与失败护栏」独立判定成败**：成功才收集 `Saved full response:` 后的本地路径，失败按护栏处理。并发场景下**每张失败相互隔离**，单张失败不影响其它张推进，**不得**因一张失败终止整个队列、也**不得**换 skill 重试。
  5. 全部并发任务回收完毕后再进入步骤 4；收集成功的本地路径，记录失败的参考图及原因。
- **输出**：`replica_results`（参考图 → 复刻图本地路径的映射列表，含失败标记）
- **用途**：作为步骤 4 的对照展示输入

### 步骤 4：对照展示

> 图片本身已由步骤 3 各次 Bash stdout 里的 `Saved full response: [path]` 经 bridge 自动渲染给用户；本步只在对话正文补一段「竞品参考图 ↔ 复刻结果」对照表。

- **输入**：`replica_results`（步骤 3 的输出，含失败标记）
- **操作**：跳过失败项，把成功项**按下方示例的结构原样照抄**渲染对照表；失败项另列。
- **硬性约束**（示例本身无法表达的边界，违反即视为故障）：
  - 对照表**只**展示竞品参考图（图二）与复刻结果两列，**不要展示用户的商品原图（图一）**、不加额外列。
  - 复刻结果必须是**完整绝对路径**（`/root/.linkfox/.../xxx.png`），不得截断为文件名 / 相对路径，不得改用反引号纯路径、裸路径或 `Saved full response:` 行——bridge 不会消费正文里的 `Saved` 标记，写出来只会变成裸文本污染对话。
- **输出格式（即唯一真相源：列数 / 渲染形态 / 多张分隔 全部以此为准，正文不再重复描述）**：
  ```
  | 竞品参考图 | 复刻结果 |
  |------------|----------|
  | ![竞品图1](https://example.com/reference-1.jpg) | ![复刻结果1](/root/.linkfox/workspaces/linkfox/2026-06-13/xxx/media/linkfox-aigc-imagegen-1781254887993.png) |
  | ![竞品图2](https://example.com/reference-2.jpg) | ![复刻结果2](/root/.linkfox/workspaces/linkfox/2026-06-13/xxx/media/linkfox-aigc-imagegen-1781254891234.png) |
  ```
  失败项另列：
  ```
  **失败项：**
  - 竞品图 3：[失败原因]
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
| 其它错误 | 配额、内容被拒、服务端 5xx、未知 errcode 等 | **不重试**，把该张标记为失败并记录原因，继续处理队列里**其余参考图** |

**3. 硬性护栏（违反即视为故障）**
- ❌ **禁止因生图失败改调任何其它 skill**（包括 `aigc-imagegen` 之外的生图/编排 skill、product/cloth 系列等）——本 skill 的生图路径唯一，失败就按上表处理或上报，绝不"换一个 skill 试试"。
- ❌ **禁止无上限重试**：除"瞬时错误最多 1 次"外，同一张图的同一类失败不得反复重试。
- ❌ **禁止把失败的返回体当成功**继续往下走（展示空图、告诉用户"已生成"）。
- ✅ 整个队列跑完后，若存在失败项，在最终结果里**逐项注明失败原因**交给用户，由用户决定是否调整参数重跑。

---

## 执行自检

每次跑完流程，收尾时确认：

- [ ] 每张图都按「错误处理与失败护栏」判定过成败；成功项收集了 `Saved full response:` 后的本地路径，失败项在结果中注明原因
- [ ] 商品原图已确认存在，并作为每次调用的"图一"
- [ ] 方式 A：已用 `scripts/extract_reference_images.py` 提取参考图（`include_aplus=false` 时带 `--main-only`），未 inline `jq` 手抠、未掺入 `imageUrl`/`thumbnail`/`reviewsImages`，也未尝试不存在的 `aplusImages`/`mainImage`/`images` 键
- [ ] 方式 A：`include_aplus` 已按用户/前端意图解析（默认 true）；步骤 2.5 仅输出 1 行数量文案（含主副图/A+ 分项时按模板），未弹任何 `AskUserQuestion`、未做确认；方式 B 已跳过本步
- [ ] `imageUrls` 顺序为 `[原图, 参考图]`，与固定提示词的"图一/图二"一致
- [ ] 固定提示词取自 `references/workflow.md`〈配对与提示词〉唯一正源，**未在 SKILL.md 或别处内联复制**
- [ ] `aspectRatio`：S1 已区分默认模式与具体比例；默认模式已逐张 probe 当前图二并把原始显示宽高组装为 `W:H` 传给 imagegen，未约分、未复用其他图片比例；具体比例则所有复刻图统一透传用户选项
- [ ] `resolution` 按前端传入值透传给 imagegen；前端未传时缺省 `2K`，**未硬编码强制覆盖前端值**
- [ ] 步骤 3 已**并发**调用 `linkfox-aigc-imagegen`，最大并发不超过 4；单张失败相互隔离，未因一张失败终止整个队列
- [ ] 每张参考图都生成了对应复刻图；成功项的本地路径已按步骤 4 示例结构填进对照表（只放图二+复刻结果两列，未展示图一），失败项在结果中注明原因
- [ ] `provider` 透传、`aspectRatio` 按“具体比例优先，否则逐图探测”规则传入，未在本 skill 预校验 imagegen 枚举；imagegen 回非法值时用 `AskUserQuestion` 让用户重选，未转述原始报错
- [ ] 失败时未改调其它 skill、未无上限重试、未把失败返回体当成功

---

## 已知局限

- **平台覆盖**：方式 A 仅亚马逊；其他平台的爆款请走方式 B 上传参考图。ASIN 下架/地区不可见时无图返回，需提示用户换 ASIN。
- **提示词语言**：固定提示词为中文（业务约定），唯一正源在 `references/workflow.md`〈配对与提示词〉段；`linkfox-aigc-imagegen` 建议英文提示词效果更佳，若复刻效果不稳定，可在该正源处统一调整。
- **质量参数**：`quality` 仅 `GPT_2_IMAGE` 生效，其他模型忽略。
- **不做内容合规审核**：复刻产出不经平台合规校验，用户需自行确认是否符合目标平台规则。
