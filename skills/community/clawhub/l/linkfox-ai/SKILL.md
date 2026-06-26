---
name: linkfoxai
description: "调用 LinkFox AI 开放平台 AI 作图/视频 API（换模特、抠图、扩图、场景裂变、智能修图、套图、姿势裂变、带货口播、图转视频等）。适用场景：(1) AI 任务创建与结果轮询，(2) 通过 api-call 调用任意开放平台接口，(3) 素材连通性测试。"
metadata: {"clawdbot":{"emoji":"🦊","requires":{"env":["LINKFOXAI_API_KEY"]}}}
---

# LinkFoxAI - LinkFox AI 开放平台 Skill

LinkFoxAI 让 OpenClaw 调用 LinkFox AI 开放平台 AI 作图/视频能力：换模特、自动抠图、场景裂变、智能扩图、高清放大、消除笔、智能修图、商品套图、服装套图、姿势裂变、带货口播、图转视频等。

## 配置

1. **获取凭证**：注册 [紫鸟开放平台](https://open.ziniao.com)，认证开发者并创建 LinkFox 卖家应用，然后在 [linkfox.com/team/api-guide](https://www.linkfox.com/team/api-guide) 将应用绑定到团队，获取 API Key。
2. **环境变量**：`LINKFOXAI_API_KEY`（单一 API Key，配置一个 Key 即可调用全部接口）
3. **自定义 Base URL**（可选）：默认 `https://sbappstoreapi.ziniao.com/openapi-router`。若无固定 IP，设置 `LINKFOXAI_BASE_URL=https://sbappstoreapi-proxy.linkfox.com` 并配置白名单。

## 必须使用 sessions_spawn 调度作图任务

AI 作图任务需要排队和生成时间（通常 10 秒 ~ 5 分钟，**极端情况下可能因服务端超时或队列积压导致单个任务耗时超过 30 分钟**）。**务必通过 `sessions_spawn` 将作图任务派发到子会话**，让主会话保持响应。脚本的 `--wait` 参数会自动轮询直到出结果。

### 超时处理策略（AI 自行判断）

当作图任务超时（`--timeout` 耗尽仍未返回结果）时，AI 应根据具体情况自主选择以下策略，无需等待用户指令：

1. **延长轮询时间**：将 `--timeout` 增大到 1800（30 分钟），`--interval` 建议 10~30 秒，适用于重要任务或用户明确愿意等待的场景。
2. **告知用户并继续后台等待**：向用户说明任务仍在生成中，预估剩余时间，并在后台子会话中继续轮询；完成后主动汇报结果。
3. **任务分拆重试**：若任务参数含多图（如 `--output-num 4`），可拆分为多个单图任务并行提交，降低单个任务超时概率。
4. **放弃并报错**：仅当用户明确要求快速返回、或超时时间已大幅超出合理范围（> 40 分钟）时，才终止轮询并告知用户稍后手动查询任务 ID。

> 默认建议：将 `sessions_spawn` 的 `runTimeoutSeconds` 设为 **1800**，`--timeout` 设为 **1700**，以覆盖绝大多数超时场景。仅在明确知道该类型任务通常很快时才缩小超时值。

### 标准调度模板

```
sessions_spawn:
  task: |
    Run: <skill>/scripts/linkfoxai.py change-model --wait --timeout 1700 \
         --image-url "<模特原图>" --head-url "<头部图>" --output-num 4
    解析输出 JSON，提取 resultList 中的图片 URL 汇报给用户。
    如果 status=4（失败），报告 errorMsg。
    如果超时仍未完成，告知用户任务 ID 以便后续手动查询。
  label: "LinkFoxAI: AI 换模特"
  mode: "run"
  runTimeoutSeconds: 1800
  cleanup: "keep"
```

### 并行调度多个独立任务

```
# 子任务 1
sessions_spawn:
  task: "Run: <skill>/scripts/linkfoxai.py cutout --wait --timeout 1700 --image-url '<url>' --sub-type 1 ..."
  label: "LinkFoxAI: 自动抠图"
  mode: "run"
  runTimeoutSeconds: 1800

# 子任务 2
sessions_spawn:
  task: "Run: <skill>/scripts/linkfoxai.py scene-fission --wait --timeout 1700 --image-url '<url>' ..."
  label: "LinkFoxAI: 场景裂变"
  mode: "run"
  runTimeoutSeconds: 1800
```

### 通用接口调用（api-call）

对于脚本没有专属命令的接口（如 AI 穿衣、商品替换、饰品文字等），使用 `api-call` 传入路径和 JSON body：

```
sessions_spawn:
  task: |
    Run: <skill>/scripts/linkfoxai.py api-call \
         --path /linkfox-ai/image/v2/make/fittingRoom \
         --body '{"upperOriginUrl":"<上衣图>","modelImageUrl":"<模特图>","outputNum":2}'
    获取返回的 data.id，然后运行：
    <skill>/scripts/linkfoxai.py poll --id <task_id> --timeout 1700
    解析结果汇报给用户。如果超时仍未完成，告知用户任务 ID 以便后续手动查询。
  label: "LinkFoxAI: AI 穿衣"
  mode: "run"
  runTimeoutSeconds: 1800
```

## 脚本命令一览

### 基础命令

| 命令 | 说明 |
|------|------|
| `material-list --type <1-10>` | 作图素材列表（可用于连通性测试） |
| `upload-base64 --file <路径>` | base64 上传图片，返回 viewUrl |
| `make-info --id <任务ID>` | 查询作图结果（单次） |
| `poll --id <任务ID> [--interval 3] [--timeout 300]` | 轮询作图结果直到成功/失败 |
| `refresh --id <图片ID> [--format jpg]` | 刷新结果图片地址（注意是图片 ID，非任务 ID） |
| `api-call --path <路径> --body '<JSON>'` | 通用 API 调用，可调任意开放平台接口 |

### 作图快捷命令（均支持 `--wait`）

| 命令 | 说明 |
|------|------|
| `change-model --image-url <url> --head-url <url> [--scene-url <url>] [--output-num 1-4]` | AI 换模特 |
| `cutout --image-url <url> --sub-type <1/2/3/9/12/13> [--cloth-class tops,coat,...]` | 自动抠图 |
| `scene-fission --image-url <url> [--strength 0.5] [--prompt "描述"] [--provider SCENE_FISSION_REALISTIC]` | 场景裂变 |
| `expand-image --image-url <url> --width 1024 --height 1024 [--prompt "描述"]` | 智能扩图 |
| `super-resolution --image-url <url> --magnification 2 [--enhance]` | 图片高清放大 |
| `image-edit --image-url <url> --prompt "描述" [--provider BANANA_PRO/WAN2_7/SEEDREAM5] [--template 白底图]` | 智能修图 |
| `erase --image-url <url> --mask-url <url>` | 消除笔 |
| `sales-video --prompt "口播文案" --video-type SEED [--image-list <url1> <url2>] [--video-time 10] [--aspect-ratio 9:16] [--is-pro] [--resolution 720p]` | 带货口播（SORA/WAN/SEED/SEED_FAST/HAPPY_HORSE）。resolution：SEED 480p/720p/1080p, SEED_FAST 480p/720p, HAPPY_HORSE 720p/1080p |
| `image-to-video --image-url <url> --video-type SEED [--image-list <url1> <url2>] [--prompt "描述"] [--video-time 10] [--resolution 720p] [--aspect-ratio 9:16] [--voice] [--camera single] [--prompt-optimizer]` | 图转视频（KLING/V/WAN/SEED/SEED_FAST/HAILUO/HAPPY_HORSE）。支持多图模式（--image-list），各模型参数详见 references/image-make.md |
| `video-reclone --ref-video-url <url> --ref-image-list <url1> <url2> --video-type SEED --duration 10 --resolution 720P --sale-country CN --target-language zh [--ratio 9:16] [--product-info "商品信息"]` | 视频复刻（SEED/SEED_FAST）。参考视频+商品图AI复刻生成新视频。resolution/saleCountry/targetLanguage必填 |
| `product-material --image-list <url1> [<url2>...] --seller-point "卖点" [--provider BANANA_PRO] [--a-plus-num 2] [--seller-type-num 2] [--scene-type-num 1] [--close-up-type-num 1] [--white-bg-type-num 1] [--resolution 2K] [--no-text]` | 商品套图V3（A+/卖点/场景/特写/白底，各类型最大12）。--no-text 开启无字模式 |
| `wear-collection --image-list <url1> [<url2>...] --seller-point "卖点" [--provider BANANA_PRO] [--a-plus-num 2] [--model-type-num 2] [--ins-type-num 1] [--seller-type-num 1] [--size-type-num 1] [--white-type-num 1] [--resolution 2K] [--no-text]` | 服装套图V2（A+/模特/种草/卖点/尺码/白底，各类型最大12）。--no-text 开启无字模式 |

所有作图快捷命令均支持 `--wait [--timeout 300] [--interval 3]`，提交任务后自动轮询直到完成。

### 其他能力（通过 api-call 调用）

以下能力通过 `api-call --path <路径> --body '<JSON>'` 调用，接口详情见 `references/image-make.md`：

| 能力 | 路径 |
|------|------|
| AI 换模特 2.0 | `/linkfox-ai/image/v2/make/changeModelFixed` |
| 模特换场景 | `/linkfox-ai/image/v2/make/modelChangeScene` |
| AI 穿衣-上下装 | `/linkfox-ai/image/v2/make/fittingRoom` |
| AI 穿衣-连体衣 | `/linkfox-ai/image/v2/make/fittingRoomSuit` |
| AI 穿戴 | `/linkfox-ai/image/v2/make/intelligentWear` |
| 商品替换 | `/linkfox-ai/image/v2/make/shopReplace` |
| 场景图生成 | `/linkfox-ai/image/v2/make/aiDraw` |
| 相似图裂变 | `/linkfox-ai/image/v2/make/imageToImage` |
| 精细抠图-创建 | `/linkfox-ai/v2/process/result/interactCutout/create` |
| 精细抠图-结果 | `/linkfox-ai/v2/process/result/interactCutout/info` |
| 图片翻译 | `/linkfox-ai/image/v3/make/imageTransl` |
| 手部修复 | `/linkfox-ai/image/v2/make/handRepair` |
| 局部重绘 | `/linkfox-ai/image/v2/make/areaRepair` |
| 印花提取 | `/linkfox-ai/image/v2/make/printExtract` |
| 手持商品 | `/linkfox-ai/image/v2/make/handHeld` |
| 饰品文字 | `/linkfox-ai/image/v2/make/linkedWord` |
| 商品精修 | `/linkfox-ai/image/v2/make/productRepair` |
| 图片获取描述词-创建 | `/linkfox-ai/v2/process/result/imageToPrompt/create` |
| 图片获取描述词-结果 | `/linkfox-ai/v2/process/result/imageToPrompt/info` |
| 智能修图 | `/linkfox-ai/image/v2/make/imageEditV2` |
| 智能修图-多图 | `/linkfox-ai/image/v2/make/multiImageFusionV2` |
| 商品套图 | 已有快捷命令 `product-material`（也可用 api-call） |
| 服装套图 | 已有快捷命令 `wear-collection`（也可用 api-call） |
| 姿势裂变 | `/linkfox-ai/image/v2/make/modelPoseFission` |
| 带货口播 | `/linkfox-ai/image/v2/make/salesVideo` |
| 图转视频 | `/linkfox-ai/image/v2/make/imageToVideo` |

## 连通性测试

使用作图素材接口验证凭证和网络是否正常（无需上传图片）：

```bash
<skill>/scripts/linkfoxai.py material-list --type 1
```

或对 OpenClaw 说：「用 LinkFoxAI 拉取作图素材列表」。

## 错误处理

- 错误码（如 ERR_FORBIDDEN、ERR_NOT_HAVE_TEAM_PRIVILEGE、TEAM_PERMISSION_EXPIRE）见 `references/open-platform.md`。
- 需先将应用绑定团队且团队已开通套餐。
- 作图任务失败时 `status=4`，检查 `errorCode` 和 `errorMsg`。
- 常见问题：参数校验失败（ERR_FILED_VALIDATE）、图片审核不通过（ERR_IMAGE_MAKE_AUDIT）、点数不足（ERR_IMAGE_MAKE_WILL_OUT）。
- 若调用新增能力，需使用对应 V2/V3 路径，否则可能出现参数不兼容或能力不可用。

## 参考文档

- `references/open-platform.md` — 接入流程、API 基础地址、错误码
- `references/image-make.md` — 全部作图接口及带货口播接口的完整参数与注意事项

## 示例

1. **连通性**：「用 LinkFoxAI 拉取作图素材列表」→ 脚本执行 `material-list --type 1`
2. **AI 换模特**：「用 LinkFoxAI 做一次 AI 换模特，原图 xxx，头部图 xxx，出 4 张」→ `change-model --wait --output-num 4`
3. **自动抠图**：「用 LinkFoxAI 把这张图抠图」→ `cutout --wait --sub-type 1`
4. **智能修图**：「用 LinkFoxAI 把这张图改成白底图」→ `image-edit --wait --prompt "白底图" --template 白底图`（高质量：加 `--provider BANANA_PRO`）
5. **带货口播**：「用 LinkFoxAI 生成一条 10 秒带货口播视频，竖版」→ `sales-video --wait --video-type WAN --video-time 10 --aspect-ratio 9:16 --prompt "..."`
6. **带货口播(SEED)**：「用 LinkFoxAI 生成一条 SEED 15 秒口播视频」→ `sales-video --wait --video-type SEED --video-time 15 --prompt "..."`
7. **图转视频**：「用 LinkFoxAI 把这张图生成 SEED 视频」→ `image-to-video --wait --image-url <url> --video-type SEED --video-time 10`
8. **商品套图**：「用 LinkFoxAI 生成商品套图，2张A+、2张卖点图、1张场景图」→ `product-material --wait --image-list <url> --seller-point "轻量透气运动鞋" --provider BANANA_PRO --a-plus-num 2 --seller-type-num 2 --scene-type-num 1`
9. **服装套图**：「用 LinkFoxAI 生成服装套图，含模特图和种草图」→ `wear-collection --wait --image-list <url> --seller-point "时尚连衣裙" --provider BANANA_PRO --model-type-num 2 --ins-type-num 1 --seller-type-num 1`
10. **视频复刻**：「用 LinkFoxAI 复刻这个视频，换成我的商品图」→ `video-reclone --wait --ref-video-url <video_url> --ref-image-list <img1> <img2> --video-type SEED --duration 10 --resolution 720P --sale-country CN --target-language zh --ratio 9:16`
11. **视频复刻(SEED_FAST)**：「用SEED_FAST快速复刻视频」→ `video-reclone --wait --ref-video-url <video_url> --ref-image-list <img1> --video-type SEED_FAST --duration 10 --resolution 720P --sale-country US --target-language en`
12. **套图无字模式**：「用 LinkFoxAI 生成商品套图，不要文字」→ `product-material --wait --image-list <url> --seller-point "..." --no-text --a-plus-num 2`
13. **图转视频(多图)**：「用 KLING 多图模式生成15秒视频」→ `image-to-video --wait --image-list <url1> <url2> --video-type KLING --video-time 15 --resolution 720p --aspect-ratio 16:9`
14. **通用调用**：「用 LinkFoxAI 做 AI 穿衣」→ `api-call --path /linkfox-ai/image/v2/make/fittingRoom --body '{...}'` + `poll --id <id>`
