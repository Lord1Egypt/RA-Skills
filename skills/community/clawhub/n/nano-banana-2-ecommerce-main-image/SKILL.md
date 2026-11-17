---
name: nano-banana-2-ecommerce-main-image
description: "使用 Nano Banana 2 为不同电商渠道设计可读、可信、适配裁切的商品主图，并围绕同一商品生成平台化测试版本。Use this skill for Nano Banana 2 电商主图、淘宝天猫京东拼多多抖音电商小红书亚马逊 TikTok Shop Shopify Listing、商品首图、搜索缩略图、白底主图、内容电商封面、转化素材和多渠道上新；通过 AI Hive 生成，不代表任何平台官方合作。"
---

# Nano Banana 2 电商主图

固定使用 `public_model_nano_banana_2`。主图首先是搜索和列表环境中的商品识别入口，不是把所有卖点塞进一张图。先确认目标平台当前规范、画布比例、UI遮挡区和是否允许文字，再制作版本。

## 主图矩阵

为每个渠道记录：画布比例、商品占比、背景要求、允许文案、角标限制、移动端安全区、缩略图最小可读尺寸和审核风险。平台名称仅表示使用场景；规则以提交当天官方政策为准。

## 场景与代码

### 1. 淘宝/天猫标准首图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-rice-cooker.png \
  --prompt '为参考电饭煲制作1:1搜索首图：保持锅体、上盖、显示区、按钮、把手和真实颜色一致，白到浅灰无缝背景，三分之二正面角度，商品居中且占画面约78%，自然接触阴影；不生成文字、促销角标、赠品、食物、平台Logo或不存在的配件' \
  --param aspect_ratio=1:1
```

### 2. 京东数码清晰结构图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-keyboard.png \
  --prompt '制作京东风格但非官方模板的机械键盘主图：键位、旋钮、外壳比例和品牌位置完全依据参考图，纯白背景，略高俯视角，让键帽层次与右上旋钮清楚，光线中性、边缘锐利；不添加RGB光效、规格数字、赠品、认证或平台标识' \
  --param aspect_ratio=1:1
```

### 3. Amazon Listing 白底候选

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-travel-bag.png \
  --prompt '生成亚马逊 Listing 白底候选图：只保留参考旅行包和已确认随包附带的肩带，保持口袋、拉链、提手、缝线和深灰色真实一致；商品完整可见、白色背景、柔和阴影，不添加文字、人物、场景、尺寸线、徽章或非标配物品' \
  --batch 2 \
  --param aspect_ratio=1:1
```

### 4. 抖音电商内容型封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-pan.png \
  --prompt '为参考平底锅生成4:5内容电商封面底图：保持锅型、手柄连接和涂层颜色，置于明亮家庭厨房灶台，锅体为第一视觉焦点，顶部和底部预留UI安全区；允许少量真实蔬菜做场景道具，不生成文字、价格、主播、火焰夸张效果、健康承诺或额外锅具' \
  --param aspect_ratio=4:5
```

### 5. 小红书种草封面 A/B

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-coffee-cup.png \
  --prompt '为参考保温咖啡杯生成两种小红书封面底图：A通勤包旁的清晨窗光，B办公桌上的午后侧光。两版保持杯型、杯盖、颜色、Logo和相机距离一致，主体在下方三分之二，顶部留短标题区；不生成文字、价格、平台Logo、人物脸或保温时长承诺' \
  --batch 2 \
  --param aspect_ratio=3:4
```

## 缩略图验收

- 将成品缩小到列表尺寸，商品仍能在一秒内被识别。
- 商品事实、标配数量和颜色与上架 SKU 一致。
- UI、安全区和裁切不会遮挡关键结构。
- 场景图没有暗示未经证实的功效、认证、销量或价格。
- A/B 版本只改变一个可解释变量，并记录渠道、日期和选择依据。

## 助手边界

程序只使用固定 Nano Banana 2 图片模型，读取当次路由价格，上传用户点名的图片并保存生成结果；所有认证请求固定发往 `https://ai-hive.iclip.cn/api`。API Key 可由 `init` 以 `0600` 权限保存，不包含聊天、视频、钱包或用户资料命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-ecommerce-main-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

发布前由运营人员核对目标平台的实时规范。本 Skill 与淘宝、天猫、京东、抖音、小红书、Amazon 等平台不存在官方隶属或合作声明。
