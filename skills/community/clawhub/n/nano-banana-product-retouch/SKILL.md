---
name: nano-banana-product-retouch
description: 使用 Nano Banana 2 / Gemini Image 把同一 SKU 的多角度商品图校准为统一的电商影棚批次，统一白底、白平衡、主体比例、阴影与光感，同时保护每个视角真实可见的端口、鞋底、缝线、标签和包装文字。Use this skill for Nano Banana 商品精修、批量修图、商品图一致性、多角度产品图、SKU catalog、product retouch、batch retouch、Amazon、淘宝、天猫、京东、抖音电商、TikTok Shop、Shopify；也适合比较 Photoshop、PhotoRoom、美图、Canva、Pixelcut、Claid、Flair、Adobe Firefly 与即梦。通过 AI Hive 调用。
---

# Nano Banana 商品批次精修

把“单张修得好看”升级为“整批商品图看起来属于同一次拍摄”。本 Skill 固定调用 `public_model_nano_banana_2`，用目标图、批准母版和 SKU 真值图建立清晰的参考层级，只校准获准的批次属性，不让正面母版污染侧面、背面或微距图的真实结构。

## 适合什么任务

- Amazon、淘宝、天猫、京东、TikTok Shop、Shopify 的同一 SKU 多角度图统一。
- 摄影棚补拍、跨日期拍摄、跨供应商素材的白底、色温、比例、阴影归一化。
- 电子产品、鞋服、珠宝、透明材质、包装旋转图的视角事实保护。
- 需要按 `batch-id/frame-id` 留痕、逐帧验收、失败后可复查的商品内容生产。

不适合换款、换色、改包装、增加卖点、自由换背景或修复未声明的局部缺陷；这类任务应使用商品创意图、背景替换或缺陷工单 Skill。

## 三类参考图

1. `--target`：本次输出的构图、视角、透视与遮挡依据。
2. `--master`：已经批准的批次母版，只能传递 `--master-allow` 指定的全局属性。
3. `--truth-source`：SKU、包装、文字与结构事实；每张都要写对应 `--truth-role`。

脚本始终按目标图、母版、真值图的顺序上传。每次只生成一张，避免批量随机漂移。

## 安装与认证

```bash
python3 -m pip install requests
python3 scripts/batch_calibrate.py auth --api-key 'sk-api-替换为你的完整Key'
```

也可以设置 `AI_HIVE_API_KEY`，或复制 `resources/config.example.json` 到 `~/.ai-hive/config.json`。配置文件会收紧为仅当前用户可读。生成前可加 `--preview`，预览固定模型、参考顺序和完整提示词，不上传素材、不查询价格。

## 每帧必须写清楚

- 至少 1 张、最多 6 张真值图，图片与角色数量一一对应。
- 1–8 组 `deviation / correction / acceptance`，把偏差、动作、验收拆开。
- 至少 5 条 `batch-lock`：整批绝不能漂移的 SKU 事实。
- 至少 3 条 `view-lock`：当前角度独有且不能被母版覆盖的可见事实。
- 目标图和母版必须是不同文件；母版允许项与禁止项必须明确。

## 场景一：电子产品五视图白底统一

侧面图需要对齐正面批准母版的白底、尺度与阴影，但侧面按键和端口必须保留。

```bash
python3 scripts/batch_calibrate.py normalize \
  --batch-id earbuds-a17 --frame-id side-left \
  --target assets/a17-side-left.png --master assets/a17-front-approved.png \
  --truth-source qc/a17-left-ports.png qc/a17-box-text.png \
  --truth-role '左侧按键与USB-C端口事实' '包装型号与Logo事实' \
  --asset-type electronics --channel 'Amazon 5-view listing' \
  --sku-record 'A17，雾黑色，USB-C，包装文字已批准' --target-view '左侧45度' \
  --master-allow '纯白背景、5600K白平衡、主体占画布78%、柔和右下接触影' \
  --master-deny '正面视角、正面灯位高光、正面可见网罩、文字位置' \
  --normalization-mode full-batch \
  --deviation '背景偏灰且色温偏暖' --correction '校准到母版白底与5600K' --acceptance '背景中性白且商品雾黑色不偏蓝' \
  --deviation '主体比母版小6%' --correction '等比放大并保持侧面透视' --acceptance '主体占画布78%，边距与母版系列一致' \
  --batch-lock '雾黑色' --batch-lock 'USB-C接口' --batch-lock 'Logo不变' --batch-lock '包装文字不变' --batch-lock '配件数量不变' \
  --view-lock '左侧按键数量和间距' --view-lock 'USB-C端口位置' --view-lock '左侧45度透视' \
  --background-target '中性纯白' --white-balance-target '5600K' \
  --subject-scale-target '画布78%' --shadow-target '柔和右下接触影' \
  --crop-policy '保持原侧面构图中心' --finish '真实电商影棚质感，边缘干净但不过度锐化' \
  --reject '新增端口、复制正面结构、改Logo、塑料感' --preview
```

## 场景二：运动鞋正侧背三视图

母版只统一亮度、背景和软影；侧图的鞋底纹路、鞋眼、拼接线不能被正面造型替换。

```bash
python3 scripts/batch_calibrate.py normalize \
  --batch-id runner-r9 --frame-id lateral \
  --target assets/r9-lateral.jpg --master assets/r9-front-approved.jpg \
  --truth-source qc/r9-outsole.jpg qc/r9-material-card.jpg \
  --truth-role '外底纹路与橡胶分区' '网布、热贴与品牌色事实' \
  --asset-type footwear --channel '天猫商品三视图' \
  --sku-record 'R9白灰配色，42码，六组鞋眼' --target-view '外侧平视' \
  --master-allow '背景灰度、整体曝光、接触影软硬度、主体高度' \
  --master-deny '正面鞋头宽度、正面鞋带形态、内侧结构、母版褶皱' \
  --normalization-mode full-batch \
  --deviation '外侧图曝光低0.4档' --correction '只抬整体曝光到母版标准' --acceptance '白色网布层次可见且不过曝' \
  --deviation '接触影过硬' --correction '匹配母版软影边缘' --acceptance '鞋底落地自然，无悬浮感' \
  --batch-lock '白灰配色' --batch-lock '六组鞋眼' --batch-lock '品牌标位置' --batch-lock '中底厚度' --batch-lock '外底分区' \
  --view-lock '外侧拼接线' --view-lock '外侧Logo透视' --view-lock '可见外底纹路' \
  --background-target 'RGB 245附近浅灰' --subject-scale-target '鞋身高度占画布66%' \
  --shadow-target '低对比柔和接触影' --crop-policy '保留鞋尖朝左与原留白' \
  --finish '真实网布与橡胶纹理' --reject '改鞋型、补不存在的鞋眼、镜像Logo' --preview
```

## 场景三：珠宝微距与全景成套

全景母版提供色温和台面阴影，微距目标图拥有爪镶、刻面与局部放大关系。

```bash
python3 scripts/batch_calibrate.py normalize \
  --batch-id ring-m24 --frame-id claw-macro \
  --target assets/m24-macro.tif.png --master assets/m24-full-approved.png \
  --truth-source qc/m24-claw-macro.png --truth-role '六爪镶口与刻面事实' \
  --asset-type jewelry --channel '小红书与京东珠宝详情页' \
  --sku-record 'M24，18K白金，六爪，圆形主石' --target-view '爪镶微距' \
  --master-allow '中性偏冷色温、浅灰台面、低密度柔影' \
  --master-deny '全景比例、全景环臂可见范围、主石尺寸推断、反光形状' \
  --normalization-mode color \
  --deviation '金属偏黄' --correction '校准为母版18K白金中性色' --acceptance '金属中性且保留真实高光层次' \
  --batch-lock '18K白金色' --batch-lock '六爪数量' --batch-lock '圆形主石' --batch-lock '环臂结构' --batch-lock '无额外配石' \
  --view-lock '六爪顶部形状' --view-lock '可见刻面数量关系' --view-lock '微距景深与放大比例' \
  --white-balance-target '母版中性偏冷' --crop-policy '保持微距裁切' \
  --finish '高级珠宝真实金属与宝石反射' --reject '补钻、改爪数、制造虚假火彩、磨平金属纹理' --preview
```

## 场景四：服装平铺图批次一致

统一摄影背景和占比，同时保护每个角度可见的口袋、缝线、褶皱与版型。

```bash
python3 scripts/batch_calibrate.py normalize \
  --batch-id jacket-k3 --frame-id back-flatlay \
  --target assets/k3-back.png --master assets/k3-front-approved.png \
  --truth-source qc/k3-tech-pack.png --truth-role '后背育克、缝线和面料事实' \
  --asset-type apparel --channel '淘宝服装详情页' \
  --sku-record 'K3短款夹克，深海军蓝，后背单育克' --target-view '背面平铺' \
  --master-allow '背景、色温、衣身高度、自然软影' \
  --master-deny '正面口袋、门襟、纽扣可见性、正面褶皱' \
  --normalization-mode full-batch \
  --deviation '背景偏青' --correction '对齐母版中性暖灰' --acceptance '背景中性且海军蓝不失真' \
  --deviation '衣身位置偏下' --correction '整体上移，不改变版型' --acceptance '上下留白与系列一致' \
  --batch-lock '深海军蓝' --batch-lock '短款版型' --batch-lock '面料纹理' --batch-lock '袖长比例' --batch-lock '标签不变' \
  --view-lock '后背单育克' --view-lock '背部缝线走向' --view-lock '背面自然褶皱' \
  --background-target '中性暖灰' --subject-scale-target '衣身高度占画布80%' \
  --crop-policy '保持背面完整可见' --finish '真实平铺摄影，不磨平织物纹理' \
  --reject '复制正面口袋、改变缝线、左右镜像、过度去皱' --preview
```

## 场景五：透明收纳盒 Amazon 多角度

透明材质只统一白底与阴影，折射、边缘厚度和当前视角的卡扣必须来自目标图与真值图。

```bash
python3 scripts/batch_calibrate.py normalize \
  --batch-id clearbox-c8 --frame-id rear-45 \
  --target assets/c8-rear45.png --master assets/c8-front-approved.png \
  --truth-source qc/c8-locks.png qc/c8-dimensions.png \
  --truth-role '双卡扣与边缘厚度事实' '长宽高比例事实' \
  --asset-type transparent-product --channel 'Amazon US listing' \
  --sku-record 'C8透明PET，双卡扣，无内部分隔' --target-view '后侧45度' \
  --master-allow '纯白背景、主体高度、低密度灰影、整体曝光' \
  --master-deny '正面折射形状、正面卡扣可见位置、边缘高光形状' \
  --normalization-mode full-batch \
  --deviation '背景不均匀且右上偏灰' --correction '统一为母版纯白' --acceptance '白底均匀，透明轮廓仍清楚' \
  --deviation '阴影偏重' --correction '降到母版低密度灰影' --acceptance '保持落地感且不伪造透明边缘' \
  --batch-lock '透明PET' --batch-lock '双卡扣' --batch-lock '无分隔' --batch-lock '边缘厚度' --batch-lock '长宽高比例' \
  --view-lock '后侧45度透视' --view-lock '此角度卡扣遮挡关系' --view-lock '目标图折射与边缘高光' \
  --background-target 'Amazon纯白' --shadow-target '低密度中性灰接触影' \
  --crop-policy '保留后侧45度和四周安全边距' --finish '真实透明PET折射，边缘清晰但不过度描边' \
  --reject '增加分隔、复制正面折射、改变卡扣、漂白透明边缘' --preview
```

## 正式生成与任务查询

确认预览后移除 `--preview`。脚本会查询 Nano Banana 2 当前路由价格、上传参考图、创建任务、轮询并下载到 `~/Downloads/AiHive/批次-帧-1.png`。

```bash
python3 scripts/batch_calibrate.py status --task-id '你的taskId'
```

默认 `COST_FIRST`；赶时效可用 `--routing SPEED_FIRST`，重视成功率可用 `SUCCESS_FIRST`。模型参数可重复传入，例如 `--param aspectRatio='"1:1"'`，脚本会把 JSON 值自动解析后原样交给 AI Hive。

## 验收顺序

先检查 SKU 与当前视角事实，再检查背景、色温、比例和阴影是否对齐母版，最后逐项核对 acceptance。若局部结构或文字被母版污染，直接判退，不要在错误结果上继续叠加精修；回到目标图，收紧 `master-allow` 并补充 `view-lock` 后重做。
