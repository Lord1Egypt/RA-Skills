---
name: linkfox-expert-aigc-imagegen-mannequin-to-model
description: 人台换模特图生成。传入人台图（dress form / mannequin）+ 可选模特/背景参考图，生成真人模特穿着该服装的电商展示图。仅处理人台图输入；平铺图或已有模特图走 linkfox-aigc-imagegen-cloth（type=MODEL_IMAGE）。
---

# 人台换模特图生成

把人台图（dress form / mannequin）上的服装"穿"到真人模特身上，生成一张保留原衣服穿着效果的电商展示图。内部含多步骤编排（textgen 智能提词 → imagegen 出图），通过 AI 图片解读动态生成出图 prompt，比固定模板更精准地处理不同品类与穿搭组合。

> ⚠ 与 `linkfox-aigc-imagegen-cloth`（type=MODEL_IMAGE）的区别：该类型使用内联固定模板 + 直接出图，适用于平铺图/人台图/已有模特图等多种输入；本 skill 专门处理人台图输入，走 textgen 做动态图片解读后生成精准 prompt（含品类判断、半身自动补全、Black Box 服装保真锚定），再出图。两者并行存在，按输入类型和精度需求选用。

## 适用场景

将人台/模型架上的服装换成真人模特穿着效果，生成电商展示图。

| 场景 | 说明 |
|------|------|
| 人台图直出模特 | 只给人台图，AI 自动推导模特画像（肤色/发型/体型）与场景，生成真人上身图 |
| 指定模特复刻 | 额外给模特参考图，生成的模特 100% 复刻该参考人的五官/发型/肤色/身材 |
| 指定背景场景 | 额外给背景参考图，场景按参考背景复刻 |
| 用户自定义指令 | 通过 customerKeywords 指定模特画像、姿势、场景等额外要求 |

## 不适用

- 平铺图（衣服摊平拍摄）→ 走 `linkfox-aigc-imagegen-cloth`（type=MODEL_IMAGE）
- 已有模特图换姿势/换动作裂变 → 走模特裂变能力
- 非服饰类商品场景图 → 走 `linkfox-aigc-imagegen-product`
- Ins 风种草大片/卖点图/A+ 图 → 走对应 skill
- 一次性问"这张图好不好看"之类的纯解读，不生成新图

## 输入参数

只列运行时入参；textgen system prompt 内联固化在本 skill 内，不作为入参暴露。

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `imageUrls` | string[] | 必填 | 图片列表，按顺序：第 1 张=人台图（必填，前端强制），第 2 张=模特参考图（可选），第 3 张=背景参考图（可选） |
| `customerKeywords` | string | "" | 用户补充提示词（模特画像/姿势/场景等额外要求），映射 textgen prompt 的 `{customer_keywords}` |
| `ratio` | string | 1:1 | 图片比例，原样透传给 imagegen 的 `aspectRatio` |
| `resolution` | string | 2K | 分辨率，2K / 4K |
| `provider` | string | BANANA_PRO | 生图模型，用户可选：`BANANA_PRO` / `GPT_2_IMAGE` / `BANANA_2` / `AIDRAW_EDIT` / `WAN2_7` |

> 字段映射规范：`customerKeywords` 为 null 或空时替换成空字符串 `""`，避免占位符残留在最终 prompt 里。

## 流水线步骤

> **推荐路径**：步骤 1 完成后，用 `run_mannequin.py` **一次调用**完成构参 → textgen → imagegen 全链路，避免 bash 链式拼接导致 `command` 截断或空命令。
>
> **路径铁律**：本 skill 脚本属 `<本skill根目录>`；textgen / imagegen 脚本属各自 skill 目录。当前工作目录不固定，**一律用绝对路径调用，不要用裸 `scripts/...` 相对路径**。其中 `<本skill根目录>` = 本 SKILL.md 所在目录；`<textgen根目录>` / `<imagegen根目录>` 分别通过 `skill:linkfox-aigc-textgen` / `skill:linkfox-aigc-imagegen` 解析其 SKILL.md 所在目录的绝对路径取得。
>
> **禁止**：手动用 Write 构造 textgen 参数文件（必须经 `build_textgen_params.py`）、用 bash heredoc 内嵌长 prompt/JSON、把大段文本塞进 Bash `command` 参数。`InputValidationError: command missing` 是 Agent 工具层空命令错误，不是 textgen/imagegen 业务失败——出现时应改用本 skill 脚本，不要原样重试空 Bash。

### 步骤 1：校验图片 URL 可访问性

- **输入**：`imageUrls`
- **操作**：逐项检查 `imageUrls` 中的值，保持原顺序（人台图在第 1 位，模特参考图在第 2 位如有，背景参考图在第 3 位如有）：
  - 已是公开 URL（http/https 开头）→ 直接透传
  - 本地文件路径（非 http/https）→ 调 `linkfox-file-upload` 上传获得公开 URL 后替换
- **输出**：`imageUrls`（全部为公开可访问的 HTTPS URL）
- **用途**：作为 textgen 的视觉输入与 imagegen 的参考图输入。

### 步骤 2–3：全链路出图（推荐）

- **输入**：步骤 1 的 `imageUrls`、`customerKeywords`、`ratio`、`resolution`、`provider`
- **操作**：
  1. 用 Write 把任务参数落成 JSON 文件（小文件，仅入参，不含 prompt 正文）`<mannequin_job.json>`：
     ```json
     {
       "imageUrls": ["https://..."],
       "customerKeywords": "",
       "provider": "BANANA_PRO",
       "ratio": "1:1",
       "resolution": "2K",
       "textgen_script": "<textgen根目录>/scripts/aigc_textgen.py",
       "imagegen_script": "<imagegen根目录>/scripts/aigc_imagegen.py"
     }
     ```
  2. 执行编排器（**仅此一次 Bash 调用**）：
     ```bash
     python <本skill根目录>/scripts/run_mannequin.py --params-file <mannequin_job.json>
     ```
  3. 编排器在进程内完成：读 `templates/mannequin.txt` 构参 → textgen `--content-only` → imagegen 出图；瞬时网络错误每步自动重试 1 次。
- **输出**：模特上身图（stdout 含 `Saved full response:` 后的本地路径，原封不动透传展示）
- **用途**：最终交付给用户的图片产物。

### 分步调试（仅排查问题时使用）

#### 步骤 2a：构参

```bash
python <本skill根目录>/scripts/build_textgen_params.py \
  --image-urls '<步骤1的URL JSON数组>' \
  --customer-keywords "<customerKeywords>" \
  --out "$DATADIR/textgen_mannequin.json"
```

#### 步骤 2b：textgen 改写

按 textgen SKILL.md 链式调用（机制见 textgen SKILL.md `--content-only`）：

```bash
PROMPT=$(python <textgen根目录>/scripts/aigc_textgen.py --stdin --content-only < "$DATADIR/textgen_mannequin.json")
```

#### 步骤 3：imagegen 出图

```bash
PARAMS=$(jq -nc --arg p "$PROMPT" --argjson imgs '<步骤1的URL JSON数组>' \
  '{prompt:$p, imageUrls:$imgs, provider:"<provider>", outputNum:1, aspectRatio:"<ratio>", resolution:"<resolution>", quality:"high"}')
python <imagegen根目录>/scripts/aigc_imagegen.py "$PARAMS"
```

- **skill 输出原封不动透传**：`linkfox-aigc-imagegen` 自行完成调用与输出，本 skill 不做二次包装、不截取、不重新输出。

---

## 错误处理与失败护栏

### textgen 失败处理（步骤 2）

| 失败类型 | 判断依据 | 处理 |
|----------|----------|------|
| 网络/超时 | 连接失败、timeout | 最多重试 1 次；再失败向用户报告 |
| 模型返回空 | 返回文本为空或明显非 prompt 格式 | 不重试，向用户报告"提词模型未能生成有效 prompt"，建议调整输入图或补充 customerKeywords |
| 其它错误 | 401/配额/5xx | 不重试，如实告知用户 |

### imagegen 失败处理（步骤 3）

> `linkfox-aigc-imagegen` 对业务失败也返回 exit 0，不能靠退出码判断成败。

- **成功**：stdout 含 `Saved full response: ["xxx.png", ...]`（JSON 数组路径）→ 图片已落盘，取路径展示。
- **失败**：stdout 含 `Saved full response: xxx.json`（单个 JSON 文件路径）→ 无图片产物，需读该 JSON 查看错误详情。

| 失败类型 | 判断依据 | 处理 |
|----------|----------|------|
| 参数非法 | errmsg 指向 provider/aspectRatio/resolution 等入参 | 用 `AskUserQuestion` 让用户重选参数后重跑 |
| 认证失败 | errcode==401 | 停止，提示用户配置 API Key |
| 瞬时错误 | 网络/超时/连接失败 | 最多自动重试 1 次；再失败报告用户 |
| 其它错误 | 配额、内容被拒、5xx | 不重试，如实告知 |

**硬性护栏**：
- ❌ 禁止因生图失败改调任何其它 skill
- ❌ 禁止无上限重试
- ❌ 禁止把失败的返回体当成功继续往下走

---

## 执行自检

每次出图后，agent 在收尾时确认：

- [ ] 步骤 1 所有参考图都成功转为公开可访问 URL（本地路径已通过 linkfox-file-upload 上传），人台图在第一张
- [ ] textgen 返回了有效的英文 prompt（非空、非错误信息），且 `{customer_keywords}` 已由 `build_textgen_params.py` 替换
- [ ] 步骤 3 imagegen 成功返回图片路径（非 JSON 错误文件）
- [ ] 服装款式、颜色、纹理与人台图上的原衣服一致（Black Box Rule 生效）
- [ ] 若传了模特参考图：模特五官/发型/肤色已复刻
- [ ] 若传了背景参考图：背景已按参考处理
- [ ] provider / ratio / resolution 已按用户入参透传

## 已知局限

- 依赖 textgen 的图片理解能力：如果人台图拍摄角度刁钻、光线极差或服装特征不明显，textgen 可能误判品类导致 Completion Rule 补错搭配。
- textgen 返回的 prompt 为英文且 ≤512 tokens，极复杂场景（多层搭配、大量配饰）可能被截断。
- Black Box Rule 不描述目标服装细节（靠 img2img 参考图锚定），如果 imagegen 模型对参考图的还原力不足，服装细节可能偏差——此时建议换 provider 重试。
- 本 skill 只接受人台图输入；平铺图/已有模特图走 `linkfox-aigc-imagegen-cloth`（type=MODEL_IMAGE）。
- 仅产出单张图片；多张需求由套图编排层调度。
- 多一步 textgen 调用意味着比固定模板链路多 5-15 秒延迟。

---

## 提示词正文（textgen System Prompt）

> 正文固化于 `scripts/templates/mannequin.txt`（v3.1b），由 `build_textgen_params.py` 读取并按 `{customer_keywords}` 填充。model=`GEM_3_1_PRO`，thinkingLevel=`medium`。修改 prompt 请改模板文件，勿在 SKILL.md 内嵌副本。
