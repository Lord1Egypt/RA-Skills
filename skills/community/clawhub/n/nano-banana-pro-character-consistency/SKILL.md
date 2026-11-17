---
name: nano-banana-pro-character-consistency
description: "使用 Nano Banana Pro 在广告、社媒、短故事、虚拟模特和品牌 Campaign 中保持同一商业人物的脸、年龄、发型、体型、服装与身份连续。Use this skill for Nano Banana Pro character consistency、一致人物、虚拟模特、品牌代言人、数字人图片、连续场景、换装、表情动作表和系列广告；通过 AI Hive 使用人物参考图生成。"
---

# Nano Banana Pro 角色一致性图片

固定使用 `public_model_nano_banana_pro`。面向商业人物建立“身份锚点 + 造型版本 + 场景日志”。获得人物或肖像使用授权，并限定使用范围；不得把真实人物放入未经同意的敏感、误导或代言情境。

## 人物连续性表

记录脸型、五官比例、年龄表现、肤色、真实皮肤纹理、发型、身高体型、标志特征、批准妆容、基础服装、允许换装、表情范围、手势、禁止变化和授权范围。准备正面、三分之二侧面与全身批准参考图。

## 场景与代码

### 1. 从头像扩展全身造型

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据图1和图2锁定同一女性的脸型、五官、年龄、肤色、卷发和自然妆容，生成全身站姿商业肖像。使用图3批准的深蓝西装，身体比例自然，浅灰棚拍背景；不得年轻化、瘦脸、改变发色、服装结构或生成珠宝和Logo' \
  --image /path/to/face-front.jpg \
  --image /path/to/face-three-quarter.jpg \
  --image /path/to/approved-suit.jpg
```

### 2. 批准换装系列

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '保持人物身份、脸、年龄、卷发、体型和自然妆容，分别穿批准的通勤西装、周末针织、运动外套三套服装。每张全身正面、相同棚拍光线和相机高度；只改变服装，不生成新配饰、Logo、文字或身体变化' \
  --image /path/to/person-master.jpg \
  --image /path/to/three-approved-outfits.jpg \
  --batch 3
```

### 3. 多场景 Campaign 连续人物

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '让同一人物出现在晨间办公室、午后咖啡店、傍晚城市步行三个场景。锁定脸、发型、年龄、身材、深蓝西装与米色手袋，时间与环境光自然变化；不改变身份、服装、商品，不生成路人特写、文字或品牌' \
  --image /path/to/person-master.jpg \
  --image /path/to/bag.png \
  --batch 3
```

### 4. 表情与手势参考表

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一人物生成六格表情动作表：自然微笑、专注倾听、轻微惊喜、解释手势、指向左侧、双手放松。保持脸、年龄、发型、妆容、服装、相机与白色背景一致；表情克制真实，不夸张五官，不生成文字、道具或不同人物' \
  --image /path/to/person-master.jpg \
  --batch 6
```

### 5. 同一人物多版位广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '基于批准人物主视觉生成方形、4:5和9:16三个广告版位。人物身份、姿势、深蓝西装、手袋和背景光保持一致，只重新安排人物位置与标题留白以避开平台UI；不裁切脸和手袋，不生成文字、价格、按钮或新人' \
  --image /path/to/approved-character-keyart.jpg \
  --batch 3
```

## 身份验收

- 对照身份锚点检查五官比例、年龄、肤色、发型、体型和标志特征。
- 造型版本、妆容、服装与配饰符合批准表，不在场景间随机变化。
- 手部、姿势、身体比例和人物与商品接触关系自然。
- 场景日志记录服装、时间、动作、版位和参考图，避免连续内容穿帮。
- 确认肖像授权涵盖渠道、地区、期限和用途，并保留批准记录。

## 执行

### 脚本行为与数据边界

- `generate` 查询固定图片模型与实时路由价格，只上传命令中明确传入的参考图，提交图片任务、轮询状态并下载结果。
- `upload` 仅上传 `--file` 指定的单个图片；`task` 仅查询用户提供的任务 ID。
- `init` 可打开 AI Hive 的 Key 获取页，并把用户粘贴的 Key 写入 `~/.ai-hive/config.json`，文件权限设为 `0600`。
- 公开命令仅有 `generate`、`upload`、`task` 和 `init`；不提供聊天、视频、钱包或用户资料查询。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro-character-consistency
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多图、批量、比例、参数、路由和输出目录。涉及真人时明确标注合成用途，不制造虚假代言、新闻事件或身份陈述。
