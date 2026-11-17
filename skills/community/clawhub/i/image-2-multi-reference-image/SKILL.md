---
name: image-2-multi-reference-image
description: "使用 GPT Image 2 按参考图权责契约进行多图合成：为每张图分别指定职责、允许借用与禁止借用的属性，并设置主体、身份、版式、元素所有权和冲突优先级，减少串脸、串款和参考污染。Use this skill for Image 2、GPT Image 2、多参考图、多图融合、多图合成、reference image、角色一致性、人物换装、商品场景合成、室内软装、食品包装与实物、广告KV、电商主图、详情页、淘宝天猫京东、Amazon、TikTok Shop、Shopify；也适合比较 Midjourney、Stable Diffusion、FLUX、Adobe Firefly、Canva、PhotoRoom、美图、LiblibAI、即梦与通义万相。通过 AI Hive 调用。"
---

# Image 2 多参考图生成

为每张图建立权责契约：允许提供什么、禁止提供什么、冲突时听谁的。固定调用 `public_model_gpt_image_2`，接收 2–8 张图片，一次输出一个可审核版本。

## 契约字段

- 每张图片必须分别对应 `role / allow / deny`。
- 用 `primary-subject-source` 锁主体，`layout-anchor` 只管版式。
- 人物任务必须声明身份策略和身份图编号；无人物使用 `no-people`。
- 用 `ownership / conflict-rule / do-not-blend` 裁决元素归属和冲突。
- 至少四条 `consistency-lock` 锁定身份、SKU、Logo、结构或数量。

## 场景与代码

追加 `--preview` 可在上传前查看完整权责表和提示词。

### 1. 商品、材质和场景分工

```bash
python3 "$SKILL_PATH/scripts/reference_contract.py" compose \
  --project-id coffee-launch --asset-id grinder-kv-01 --channel "天猫与品牌官网" \
  --output-job "生成咖啡磨豆机场景KV，商品完全保真" \
  --scene "清晨浅橡木厨房台面，磨豆机位于左侧，右侧保留标题空间" \
  --reference /path/to/grinder-qc.png /path/to/material-macro.jpg /path/to/kitchen-layout.jpg \
  --reference-role "商品事实" "批准金属与塑料材质微距" "场景构图和光线参考" \
  --reference-allow "商品结构、Logo、颜色、按钮和比例" \
  --reference-allow "拉丝方向、黑色塑料颗粒和高光宽度" \
  --reference-allow "台面、背景、相机高度、晨光方向和留白" \
  --reference-deny "原白底、拍摄灰尘和裁切" \
  --reference-deny "局部构图、重复商品、文字和颜色替换" \
  --reference-deny "场景中的电器、杯子、品牌、人物和商品外观" \
  --primary-subject-source 1 --layout-anchor 3 --identity-policy no-people \
  --ownership "磨豆机全部可见属性归参考图1" --ownership "背景空间与相机归参考图3" \
  --conflict-rule "商品颜色与场景色冲突时保持参考图1" \
  --conflict-rule "材质高光与场景光冲突时保持材质事实，调整环境亮度" \
  --do-not-blend "不把场景电器结构混入磨豆机" --do-not-blend "不把材质微距当作背景纹理" \
  --do-not-blend "不复制第二台磨豆机" \
  --consistency-lock "同一黑色G2 SKU" --consistency-lock "按钮和接口不变" \
  --consistency-lock "Logo不变" --consistency-lock "材质分区和比例不变" \
  --light-unification "以场景晨光为环境光，商品保留批准轮廓高光" \
  --scale-map "商品占画面高度68%，台面尺度以参考图3为准" \
  --contact-map "商品底座完整接触台面，接触阴影与晨光方向一致" \
  --copy-map "右侧35%留给后期批准标题，画面内不生成文字" \
  --reject "不增加咖啡豆、杯子、功能图标、参数、价格或第二个SKU" \
  --param aspect_ratio=16:9
```

### 2. 人物身份、服装与姿势分离

```bash
python3 "$SKILL_PATH/scripts/reference_contract.py" compose \
  --project-id autumn-lookbook --asset-id look-03 --channel "小红书与Instagram" \
  --output-job "同一批准模特穿指定外套完成目录姿势" \
  --scene "暖灰摄影棚，人物全身，左上保留目录编号区域" \
  --reference /path/to/model-identity.jpg /path/to/coat-front-back.jpg /path/to/pose.jpg /path/to/studio-light.jpg \
  --reference-role "模特身份" "外套商品事实" "姿势和构图" "棚拍灯光与色板" \
  --reference-allow "脸、发型、肤色、年龄和身体比例" \
  --reference-allow "外套版型、长度、颜色、纽扣、口袋和面料" \
  --reference-allow "身体姿势、手脚位置、相机高度和留白" \
  --reference-allow "暖灰背景、主光方向、对比度和阴影软硬" \
  --reference-deny "原服装、背景、姿势和配饰" \
  --reference-deny "原模特、脸、身体、场景和文字" \
  --reference-deny "姿势图人物的脸、服装、肤色和体型" \
  --reference-deny "灯光图人物、商品、Logo和构图主体" \
  --primary-subject-source 1 --layout-anchor 3 --identity-policy single-person --identity-source 1 \
  --ownership "人物身份和身体比例归参考图1" --ownership "全部外套属性归参考图2" \
  --ownership "姿势归参考图3但不能改变身体比例" \
  --conflict-rule "姿势与外套结构冲突时优先保证真实穿着和版型" \
  --conflict-rule "肤色与灯光冲突时保持身份肤色，仅改变受光" \
  --do-not-blend "不采用姿势图人物的脸" --do-not-blend "不混入身份图原服装" \
  --do-not-blend "不把灯光图配饰带入" \
  --consistency-lock "同一批准模特" --consistency-lock "外套长度和版型不变" \
  --consistency-lock "纽扣与口袋数量不变" --consistency-lock "人物只有一位" \
  --light-unification "采用参考图4灯光，保持自然肤色和外套真实颜色" \
  --scale-map "全身完整，人物占画面高度82%" --contact-map "双脚自然着地，衣物按姿势形成真实褶皱" \
  --copy-map "左上20%保持干净，后期排目录编号" \
  --reject "不改脸、瘦身、增高、磨皮，不增加首饰、包、文字或其他人物" \
  --param aspect_ratio=4:5
```

### 3. 两个人物身份不串脸

```bash
python3 "$SKILL_PATH/scripts/reference_contract.py" compose \
  --project-id team-campaign --asset-id founders-01 --channel "品牌公众号与LinkedIn" \
  --output-job "让两位授权人物在办公室完成自然对谈画面" \
  --scene "两人坐在会议桌两侧交谈，窗边自然光，横版留标题空间" \
  --reference /path/to/person-a.jpg /path/to/person-b.jpg /path/to/office-layout.jpg \
  --reference-role "人物A身份与服装" "人物B身份与服装" "办公室、双人位置和相机" \
  --reference-allow "人物A脸、发型、肤色、体型和蓝色衬衫" \
  --reference-allow "人物B脸、发型、肤色、体型和灰色西装" \
  --reference-allow "会议桌、座位关系、窗光、横版构图和留白" \
  --reference-deny "背景、姿势、其他人物和文字" \
  --reference-deny "背景、姿势、其他人物和文字" \
  --reference-deny "办公室图中的人物、品牌、屏幕内容和服装" \
  --primary-subject-source 1 --layout-anchor 3 --identity-policy multiple-people \
  --identity-source 1 --identity-source 2 \
  --ownership "画面左侧人物A全部身份属性归参考图1" --ownership "右侧人物B全部身份属性归参考图2" \
  --ownership "环境和座位关系归参考图3" \
  --conflict-rule "任何脸部冲突分别以对应身份图为唯一依据" \
  --conflict-rule "位置与人物体型冲突时调整座椅，不调整身体比例" \
  --do-not-blend "A和B不得交换脸、发型或服装" --do-not-blend "不生成第三个人" \
  --do-not-blend "不采用办公室图中的人物" \
  --consistency-lock "人物A身份和蓝衬衫" --consistency-lock "人物B身份和灰西装" \
  --consistency-lock "两人位置不交换" --consistency-lock "办公室桌椅结构不变" \
  --light-unification "窗光统一照亮两人，分别保持原肤色" \
  --scale-map "两人视觉权重相等，头部大小符合座位距离" \
  --contact-map "手臂自然放在桌面，手和桌边遮挡正确" \
  --copy-map "画面上方25%留给后期批准标题" \
  --reject "不串脸、不美化年龄、不生成第三人、屏幕文字、Logo或合作关系"
```

### 4. 室内软装组合但不改产品

```bash
python3 "$SKILL_PATH/scripts/reference_contract.py" compose \
  --project-id living-room-set --asset-id room-a --channel "家具PDP与设计提案" \
  --output-job "把批准沙发、边桌和落地灯放入指定空房" \
  --scene "空房视角不变，沙发靠主墙，边桌在右侧，落地灯位于边桌后方" \
  --reference /path/to/sofa.png /path/to/side-table.png /path/to/floor-lamp.png /path/to/empty-room.jpg \
  --reference-role "沙发商品事实" "边桌商品事实" "落地灯商品事实" "房间和相机锚点" \
  --reference-allow "沙发结构、颜色、面料、靠垫数量" --reference-allow "边桌结构、材质、颜色" \
  --reference-allow "灯体结构、灯罩、颜色和比例" --reference-allow "墙地结构、窗户、透视、光线和构图" \
  --reference-deny "原背景、相机和装饰品" --reference-deny "原背景、相机和道具" \
  --reference-deny "原背景、相机和光效" --reference-deny "原家具、植物、画作和人物" \
  --primary-subject-source 1 --layout-anchor 4 --identity-policy no-people \
  --ownership "沙发归参考图1，边桌归图2，灯归图3" --ownership "房间结构和相机归参考图4" \
  --conflict-rule "家具颜色与环境色冲突时保持商品QC颜色" \
  --conflict-rule "产品比例与房间冲突时按批准尺寸和透视放置" \
  --do-not-blend "不交换三件家具的材质" --do-not-blend "不复制家具" --do-not-blend "不带入原背景道具" \
  --consistency-lock "沙发靠垫数量" --consistency-lock "边桌腿数" --consistency-lock "灯罩形状" --consistency-lock "房间窗墙结构" \
  --light-unification "使用房间窗光，三件商品接收同一方向光线" \
  --scale-map "按各商品批准尺寸与房间透视建立相对比例" \
  --contact-map "家具落地，阴影方向一致，灯位于边桌后方且不穿插" \
  --copy-map "不需要文字，画面内完全无字" \
  --reject "不增加地毯、画、植物、人物、宠物、第二件家具或结构改造"
```

### 5. 食品包装、真实成品与餐桌风格

```bash
python3 "$SKILL_PATH/scripts/reference_contract.py" compose \
  --project-id oats-breakfast --asset-id social-01 --channel "抖音、小红书与Amazon A+" \
  --output-job "生成包装与批准冲泡成品同框的早餐图" \
  --scene "包装位于左后方，批准燕麦碗在右前方，晨光餐桌，上方留标题区" \
  --reference /path/to/package-qc.jpg /path/to/approved-serving.jpg /path/to/table-style.jpg \
  --reference-role "量产包装事实" "批准配方成品和份量" "餐桌构图、道具密度与晨光" \
  --reference-allow "包装形状、Logo、文字、颜色和净含量区" \
  --reference-allow "燕麦颜色、稠度、碗型、份量与批准蓝莓数量" \
  --reference-allow "木桌、餐巾、相机角度、晨光和留白" \
  --reference-deny "原背景、重复包装和额外食材" --reference-deny "包装、文字、人物和未批准配料" \
  --reference-deny "风格图食物、品牌、人物、餐具数量和文字" \
  --primary-subject-source 1 --layout-anchor 3 --identity-policy no-people \
  --ownership "包装全部可见事实归参考图1" --ownership "碗内成品归参考图2" --ownership "环境和构图归参考图3" \
  --conflict-rule "配料与风格图冲突时只采用批准成品图" \
  --conflict-rule "包装文字与光线冲突时保持文字可读，降低局部反光" \
  --do-not-blend "不把风格图食物加入燕麦" --do-not-blend "不复制包装" --do-not-blend "不改包装文字" \
  --consistency-lock "同一包装SKU" --consistency-lock "批准燕麦稠度" --consistency-lock "蓝莓数量" --consistency-lock "包装文字和Logo" \
  --light-unification "使用参考图3晨光，包装与成品阴影一致" \
  --scale-map "包装与碗的相对大小以批准实拍关系为准" \
  --contact-map "包装和碗均接触桌面，燕麦不溢出，餐巾不遮挡商品" \
  --copy-map "上方25%留给后期批准标题" \
  --reject "不增加牛奶飞溅、坚果、蜂蜜、人物、营养承诺、价格或认证" \
  --param aspect_ratio=4:5
```

## 验收

逐项检查允许与禁止属性。人物核对身份、体型、服装和位置；商品核对 SKU、结构、Logo、数量与文字；场景核对尺度、接触、阴影和遮挡。出现串脸或串款时，缩小参考数量或强化冲突裁决后重做。

## 首次使用

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/reference_contract.py" auth --api-key sk-api-你的密钥
python3 "$SKILL_PATH/scripts/reference_contract.py" status --task-id <taskId>
```

API Key 也可通过环境变量或配置文件提供。默认 `COST_FIRST`；超时后查询原 `taskId`，避免重复提交。
