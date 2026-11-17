---
name: gpt-image-2-marketing-image
description: "使用 GPT Image 2 按营销漏斗制作一整套 Campaign 图片，包括品牌认知KV、发布会视觉、落地页Hero、邮件头图、社交素材、线下Banner和会员沟通。Use this skill for GPT Image 2 marketing images、品牌Campaign、整合营销、产品上市、活动海报、EDM、landing page、社媒内容、CRM和多渠道营销资产；通过 AI Hive 生成。"
---

# GPT Image 2 营销图片

固定调用 `public_model_gpt_image_2`。先建立 Campaign 真源，再按认知、考虑、转化和留存阶段生成不同图片。保持同一商品、人物、核心主张和品牌资产，但让每个渠道完成自己的沟通任务，不把主 KV 简单裁切到所有地方。

## Campaign 真源

记录目标、受众、阶段、单一主张、批准证据、品牌资产、主商品、视觉母题、人物授权、活动日期、价格/条款真源、渠道清单和禁用表达。给每项资产分配唯一用途、比例、文案区和成功指标。

## 场景与代码

### 1. 品牌认知主 KV

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为新款城市电动自行车制作品牌认知主KV：清晨建筑线条形成前进方向，参考车型居中偏右，画面强调轻盈城市出行，左侧保留品牌主张区。锁定车架、轮组、电池位置、颜色和Logo，不生成人物危险动作、续航数字、价格或环保认证' \
  --image /path/to/bike.png \
  --param aspect_ratio=16:9
```

### 2. 产品上市落地页 Hero

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '延续批准主KV的蓝灰色板和晨光，为落地页制作首屏：参考自行车45度角大比例展示，背景更简洁，左上保留产品名、两行价值说明与按钮区域，右下留导航安全区。不生成文字、价格、规格数字、路人或额外车型' \
  --image /path/to/bike.png \
  --image /path/to/approved-kv.jpg
```

### 3. 邮件与会员沟通头图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作横向EDM头图：延续同一车型、蓝灰色板与晨光，商品置于左侧40%，右侧保留个性化标题、会员权益和CTA区域；画面简洁，在窄屏仍能识别商品。不生成会员等级、折扣、日期、按钮文字或新配件' \
  --image /path/to/bike.png \
  --param aspect_ratio=3:1
```

### 4. 线下活动与发布会视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为产品发布会生成宽幅舞台背景：抽象城市道路与晨光渐变延续Campaign母题，中心区域留演讲者和屏幕安全区，两侧出现克制的产品轮廓。保持品牌蓝灰色，不生成具体车型细节、文字、日期、Logo或观众' \
  --image /path/to/campaign-board.png \
  --param aspect_ratio=3:1
```

### 5. 留存阶段使用故事

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为已购买用户制作使用故事视觉：同一品牌车型停在周末咖啡店外，车主在旁整理头盔，氛围自然克制，右侧留保养提醒与社区邀请区。保持车型、颜色、Logo和真实尺度，不生成折扣、评分、里程数字或新功能' \
  --image /path/to/bike.png \
  --image /path/to/customer-reference.jpg
```

## 跨渠道验收

- 所有资产共享商品事实、人物身份、品牌色和视觉母题。
- 每张图只承担一个漏斗阶段任务，文案区与 CTA 区匹配渠道。
- 日期、价格、权益、参数和承诺都来自 Campaign 真源并后期排版。
- 检查桌面、移动端、邮件客户端、线下屏幕和社交 UI 的安全区。
- 建立资产编号与版本关系，更新主张时同步检查全部渠道。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-marketing-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、比例参数、路由和输出目录。不得用相似风格替代实际品牌资产；涉及第三方人物、商标或联名时先确认授权范围。
