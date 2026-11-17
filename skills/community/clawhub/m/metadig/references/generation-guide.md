# 生成指南：选模型、估积分、定参数、产物去哪

本文帮你把用户的自然语言需求落成一条正确、不浪费积分的 `metadig gen` 命令。

## 先查目录，再做决定

```bash
metadig models --json > /tmp/metadig-models.json
```

一次拿全量目录后本地筛选，不要为每个字段反复调用。判断顺序：

1. **过滤不可用**：`disabled: true`（停用）直接排除；`tags` 含 `plan-only`（会员专属）时，若用户是免费档会被拒绝——不确定就先用非会员模型，或问用户是否有订阅。
2. **按方式筛**（视频）：`modes` 必须包含你要用的方式（`text-to-video` / `first-to-video` / `first-last-to-video` / `reference-to-video`）。
3. **按参数筛**：需要 9:16 就看 `ratiosText`（视频）/ `ratiosText` `ratiosImage`（图片）是否含 `9:16`；需要 10 秒就看 `durations`（或按渠道 / 分辨率的细分表）；需要带声音就看 `audio: true`。
4. **按价格排**：同等能力下看 `creditsMap` 选便宜的；`pricing_promo` 非空表示活动折扣，表内已是折后价。
5. **用户没有偏好**：用目录里该类第一个可用模型（目录顺序即平台推荐顺序），这也是 `gen` 不传 `-m` 时的默认。

模型 ID 只从目录里拷，不要凭记忆写；目录会随平台上下架变化。

## 积分估算

平台按积分计费，1 元 ≈ 10 积分（用户在网页充值 / 订阅）。估算规则：

| 类型 | 计价 | 估算方法 |
| --- | --- | --- |
| 图片 | 每张按分辨率 | `creditsMap["2K"]` × 张数；多渠道模型另有 `"priority:2K"` 这类渠道键，优先取与所用 `--channel` 匹配的键 |
| 视频 | 按渠道 × 时长 × 分辨率 | `creditsMap["<渠道>:<时长>s:<分辨率>"]`（如 `"priority:5s:720p"`）**已是该时长的总价**，不用再乘秒数；没有渠道键时用 `"<时长>s:<分辨率>"`；带声音看 `creditsMapWithAudio`；带参考视频通常加价（目录 `description` 里会写） |
| 语音 | 每 200 字 | `creditPer200Chars` × ceil(字数 / 200) |
| 音乐 | 每 5 秒或每首 | 有 `creditPer5Seconds`：× (时长 / 5)；否则 `credits` 是按首价 |

对话把估算结果给用户时用「约 N 积分」——服务端是权威，最终实扣以任务记录为准（`metadig history` 的 `credit` 列）。

**报价门槛**：单条视频、任何批量（≥3 条）、4K 出图、带参考视频，都先报方案再提交。单张普通出图（几积分）可以直接做。

**不扣费的情况**：任务失败、取消、超时都不扣积分（预留会释放）。**提交超时不等于失败**，见 `common-pitfalls.md`。

## 图片参数

| 参数 | 取值 | 说明 |
| --- | --- | --- |
| `--ratio` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` … | 以模型 `ratiosText`（文生）/ `ratiosImage`（图生）为准；图生图不传时优先 `auto`（跟随参考图） |
| `--resolution` | `1K` `2K` `4K` | 价格随分辨率走；4K 可能仅会员可用 |
| `-n` | 1~N | 张数；部分模型（如同步出图链路）固定单张，多传也只出一张 |
| `-r` | 文件或 URL，可重复 | 有则图生图；张数 ≤ `maxReferenceImages` |
| `--channel` | `priority` / `stable` 等 | 不传用 `channels[0]`；渠道影响价格与档位 |
| `--quality` / `--format` | 见模型 `qualities` / `outputFormats` | 一般不用传 |

提示词建议：写清主体、场景、光线、风格、构图，用具体的视觉词而不是抽象形容；要复用同一主角时把外观特征（发型、服装、颜色）写死并配参考图。

## 视频参数与方式

| 想要 | 用 | 素材参数 |
| --- | --- | --- |
| 从零生成一段画面 | 文生视频 | 不传素材 |
| 让一张图动起来 / 用图定首帧 | 首帧生视频 | `--first <图>` |
| 从 A 画面过渡到 B 画面 | 首尾帧生视频 | `--first <图A> --last <图B>`（首尾同图 = 循环镜头） |
| 保持人物 / 产品 / 风格一致，或参考一段视频的运镜 | 参考生视频 | `-r <图>`（可多张）、`--ref-video <视频>`、`--ref-audio <音频>` |

规则：

- `--last` 必须与 `--first` 同用；`--first/--last` 与 `-r/--ref-video/--ref-audio` 不能混用。
- 参考素材数量 ≤ 模型的 `maxReferenceImages / maxReferenceVideos / maxReferenceAudios`（有的模型要求音频必须伴随图或视频）。
- 时长 `-d` 取模型 `durations`（部分模型按分辨率 / 渠道细分，`durationsByResolution` / `durationsByChannel` 优先）；默认 5 秒。
- 分辨率默认 `720p`；`1080p` 更贵，`480p` 便宜适合试跑。
- `--audio` 让支持的模型带环境音 / 对白，有的模型恒带声（目录 `description` 会说明）。
- 比例默认 `16:9`；竖屏短视频用 `9:16`。

先用 `--no-wait` 试跑一条看效果，满意再批量，是最省积分的做法。

## 语音（TTS）

`metadig gen speech "<文本>" --voice <音色ID>`，默认音色 `male-qn-qingse`。可用音色：

| 音色 ID | 名称 | 适合 |
| --- | --- | --- |
| `male-qn-qingse` | 青涩青年 | 清爽干净的年轻男声（默认） |
| `male-qn-jingying` | 精英青年 | 沉稳自信的职场男声 |
| `male-qn-badao` | 霸道青年 | 低沉有力 |
| `male-qn-daxuesheng` | 青年大学生 | 阳光朝气 |
| `female-shaonv` | 少女 | 清脆灵动 |
| `female-yujie` | 御姐 | 成熟知性 |
| `female-chengshu` | 成熟女性 | 端庄大气，适合旁白 |
| `female-tianmei` | 甜美女性 | 温柔甜美 |
| `junlang_nanyou` | 俊朗男友 | 温柔磁性 |
| `chunzhen_xuedi` | 纯真学弟 | 干净纯真的少年音 |
| `lengdan_xiongzhang` | 冷淡学长 | 清冷疏离 |
| `badao_shaoye` | 霸道少爷 | 傲娇强势 |
| `bingjiao_didi` | 病娇弟弟 | 黏人偏执 |
| `tianxin_xiaoling` | 甜心小玲 | 甜美元气少女 |
| `qiaopi_mengmei` | 俏皮萌妹 | 活泼俏皮 |
| `wumei_yujie` | 妩媚御姐 | 妩媚慵懒 |
| `diadia_xuemei` | 嗲嗲学妹 | 软糯娇嗲 |
| `danya_xuejie` | 淡雅学姐 | 温婉淡雅 |
| `clever_boy` | 聪明男童 | 机灵活泼童声 |
| `cute_boy` | 可爱男童 | 软萌童声 |
| `lovely_girl` | 萌萌女童 | 奶声奶气 |
| `cartoon_pig` | 卡通猪小琪 | 卡通角色音 |

旁白 / 解说选 `female-chengshu` 或 `male-qn-jingying`；短视频口播选 `female-shaonv` / `male-qn-qingse`。长文本按 200 字计价，先数字数报价。

## 音乐

`metadig gen music "<风格描述>" [--lyrics "<歌词>" | --instrumental] [-d <秒>]`

- 风格描述写清曲风、情绪、节奏、乐器、用途（如「轻快的夏日流行，吉他 + 鼓，适合 vlog 开场」）。
- `--lyrics` 给完整歌词（换行用 `\n` 或直接多行字符串）；`--instrumental` 纯音乐时歌词被忽略。
- 时长：模型有 `maxDuration` 时按 5 秒计价、默认 40 秒、`-d` 自动钳进范围；没有则按首计价、`-d` 无效。

## 产物去哪

**默认落画布。** 每个任务归属一个画布项目。提交成功那一刻画布上出现「生成中」占位节点，完成后节点自动变成成品；用户开着画布时实时可见，没开下次打开就在。这样命令行产物和用户手动做的在同一张画布上，可以接着连线、改图、进时间线剪辑。告诉用户「已落到画布项目 X 的节点上」时，`--json` 输出里的 `nodeId` 就是节点 ID。

**不想弄乱画布**：加 `--no-canvas`，产物只进项目的「历史文件」（网页里可拖回画布）。

**项目归属**：

- 解析顺序 `-p <项目ID>` > 当前目录（含父目录）的 `.metadig/project.json` > 全局默认项目 > 自动创建「CLI 项目」并记为默认。
- 一个片子一个目录：`mkdir demo && cd demo && metadig project create "demo" && metadig project use <项目ID>`，此后该目录及子目录里的所有生成都归到这个项目。
- `metadig project current` 看当前生效的是哪个。

**下载到本地**：生成命令加 `-o ./exports`；已完成任务用 `metadig download <任务ID> -o ./exports`。文件名 `<任务ID前 8 位>-<序号>-<源文件名>`。产物 URL 是平台对象存储的公网地址，可直接给用户或写进文档。

## 一个完整示例

从零做一条带配音的短片素材，并向用户逐步汇报：

```bash
mkdir autumn && cd autumn
metadig project create "秋日短片"            # 记下输出的项目 ID
metadig project use <项目ID>

# 1. 查价并报方案（略）
metadig models --type video --json | jq '.video[] | {modelId, credits, modes, durations}'

# 2. 封面图
metadig gen image "秋天的银杏大道，午后逆光，电影感" --ratio 16:9 --resolution 2K -o ./exports --json

# 3. 用封面做首帧出 5 秒视频（用上一步 files[0]）
metadig gen video "镜头缓慢向前推进，落叶飘下" --first ./exports/<封面文件> -d 5 -o ./exports --json

# 4. 旁白
metadig gen speech "秋天来了，银杏叶把整条街染成了金色。" --voice female-chengshu -o ./exports --json
```

跑完告诉用户：三个产物都在「秋日短片」画布上，本地副本在 `./exports/`，实际消耗见 `metadig history`。
