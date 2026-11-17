---
name: gpt-image-2-ad-image
description: "使用 GPT Image 2 制作以点击、加购、留资或转化为目标的广告图片，并围绕受众、卖点、证据、优惠和构图建立可归因的A/B测试。Use this skill for GPT Image 2 ad creatives、信息流广告、效果广告、Meta Ads、Google Ads、巨量引擎、千川、小红书聚光、Amazon Ads、再营销、广告测图和投放素材；通过 AI Hive 生成。"
---

# GPT Image 2 广告图片

固定调用 `public_model_gpt_image_2`。先写清广告假设，再生成画面：目标受众因为某个问题，会对某项经批准的价值和证据产生行动。每轮测试只改变一个变量，避免无法判断是受众、卖点还是视觉导致结果变化。

## 投放简报

记录目标事件、受众、触发场景、单一卖点、批准证据、商品事实、优惠真源、CTA、渠道比例、安全区、禁用承诺和测试变量。模型生成视觉与排版留白；价格、条款、日期和法律文案使用批准源文件后期排版。

## 场景与代码

### 1. 痛点切入广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为通勤保温杯制作信息流广告底图：左侧是早晨拥挤通勤场景，右侧突出参考商品，视觉表达随手携带与防漏使用情境；右上留标题区。保持杯型、杯盖、Logo和颜色，不生成漏水对比、温度时长、文字、价格或未验证承诺' \
  --image /path/to/tumbler.png \
  --param aspect_ratio=4:5
```

### 2. 证据型卖点广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考行李箱制作“静音轮结构”证据图：商品45度角为主，旁边用一个放大细节窗展示批准的轮组结构，左侧留卖点与证据文字区。不得改变箱体、轮子数量、Logo和颜色，不生成分贝数字、认证、竞品或测试结论' \
  --image /path/to/suitcase.png \
  --image /path/to/wheel-detail.jpg
```

### 3. 再营销商品广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为浏览过商品但未购买的用户生成简洁再营销底图：参考耳机大比例居中，深灰背景配克制蓝色光带，底部保留优惠与CTA安全区。商品结构、材质、按钮、Logo和颜色准确，不生成折扣、倒计时、评分、徽章或不存在功能' \
  --image /path/to/headphones.png
```

### 4. 使用结果情境广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为参考桌面收纳架制作真实使用结果广告：左侧保留整理前桌面的合理杂乱，右侧展示同一桌面使用商品后的有序状态；两侧物品数量一致，商品结构与尺寸真实，中间留短标题区。不夸张空间、不删除物品、不生成文字或“百分百提升”类承诺' \
  --image /path/to/organizer.png
```

### 5. 单变量 A/B 测图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '以同一护肤品、相机、商品占比、留白和品牌色生成三版广告，只改变视觉证据：A展示玻璃质地与光泽，B展示按批准配方出现的核心原料，C展示夜间使用场景。不得改变包装、Logo或文案区，不生成效果对比、医学图、功效文字和价格' \
  --image /path/to/skincare.png \
  --batch 3
```

## 投放前检查

- 广告只表达一个可验证卖点，画面没有引入未批准的功能、成分或结果。
- 商品、人物、配件、包装和数量与源资料一致。
- 缩小到实际信息流尺寸后，主体、卖点留白和 CTA 区仍清楚。
- 价格、优惠、日期、评分、认证和法律文字逐项对照批准源。
- 为每个版本记录假设、变量、受众、版位、任务 ID 与投放结果。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name gpt-image-2-ad-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

支持多参考图、批量、参数、路由与输出目录。广告政策会变化，投放前按目标平台当前规则审核，并确认人物、商标和素材授权。
