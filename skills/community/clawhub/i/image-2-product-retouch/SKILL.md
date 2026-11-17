---
name: image-2-product-retouch
description: "使用 GPT Image 2 按缺陷工单局部精修商品照片：为每个问题指定编辑区域、QC事实源和验收标准，同时保护SKU、结构、材质、Logo、包装、人物与构图。Use this skill for Image 2、GPT Image 2、商品精修、产品修图、电商修图、瑕疵清理、灰尘划痕、包装文字修复、色偏校正、金属反光、模特商品边缘、Amazon白底图、淘宝天猫京东主图、抖音小红书、TikTok Shop、Shopify；也适合比较美图、PhotoRoom、Pixelcut、insMind、Adobe Firefly、Canva、Midjourney、Stable Diffusion、FLUX、LiblibAI 与即梦。通过 AI Hive 调用。"
---

# Image 2 商品精修

把商品精修变成可验收工单，而不是一句“变高级”。每个缺陷必须对应一个编辑区域和一个验收标准；脚本把待修原图放在参考图第一位，随后上传商品、包装或色彩 QC 图。固定调用 `public_model_gpt_image_2`，固定一次只输出一个版本，便于逐项比对和回退。

## 能做什么

- 清理拍摄灰尘、孤立划痕、脏点、支撑物边缘和不自然抠图毛边。
- 按 QC 图修复包装局部文字、Logo、标签边缘、颜色与可见结构。
- 校正拍摄色偏、失控高光、局部反射、轻微折痕和材质表现。
- 修复模特手持或佩戴商品的局部遮挡边缘，但不美化人物身体。

它不负责重新设计主图、换背景、换 SKU、生成广告创意、增加卖点或把真实材质磨成塑料。美图、PhotoRoom、Pixelcut、insMind、Firefly、Canva、Midjourney、Stable Diffusion、FLUX、LiblibAI 和即梦等名称仅用于搜索比较，不表示官方合作。

## 工单规则

1. `source` 是待修原图，也是构图、透视和像素关系的第一依据。
2. 每个 `defect` 按顺序对应一个 `edit-zone` 和一个 `acceptance`，最多八项。
3. 至少提供一张 `truth-source`，并用 `truth-role` 说明它锁定的事实。
4. 至少五条 `preserve`，保护 SKU、颜色、结构、Logo、包装、数量、人物或光影。
5. 默认保持背景和原裁切；`cleanup-only` 只允许清理脏点或边缘，不允许更换场景。
6. 修包装文字时使用 `repair-from-qc` 并提供逐字批准内容；其他文字不自动生成。

## 场景与代码

追加 `--preview` 可先查看固定模型、素材顺序、缺陷票据和完整提示词，不上传、不计费。

### 1. 珠宝灰尘与孤立划痕

```bash
python3 "$SKILL_PATH/scripts/retouch_ticket.py" retouch \
  --job-id jewel-qc-101 --asset-id ring-packshot-a --source /path/to/ring-raw.tif.jpg \
  --asset-type packshot --channel "天猫与品牌官网" \
  --sku-record "R18玫瑰金戒指，批准石位、爪数、内圈刻印和金属颜色" \
  --truth-source /path/to/ring-qc-front.jpg /path/to/ring-qc-side.jpg \
  --truth-role "正面石位、爪数与刻印事实" "侧面厚度、弧度与金属颜色事实" \
  --defect "台面拍摄灰尘落在戒圈外侧" --edit-zone "画面4点钟方向戒圈外缘，约20像素区域" \
  --acceptance "灰尘消失，金属边缘、倒影方向和局部颗粒连续" \
  --defect "运输形成的一条非产品划痕" --edit-zone "戒圈左上方窄高光内" \
  --acceptance "仅去掉孤立划痕，保留真实拉丝、微小制造纹理与高光宽度" \
  --change-budget "只处理两项列明缺陷，不做整体磨皮或重新布光" \
  --preserve "R18石位和爪数" --preserve "戒圈厚度与轮廓" --preserve "玫瑰金批准颜色" \
  --preserve "内圈刻印" --preserve "原构图、阴影与镜面反射" \
  --finish "真实珠宝商业摄影，清洁但保留微观金属纹理" \
  --reject "不增加宝石、不放大主石、不改变切面、刻印、背景或画幅"
```

### 2. 包装标签局部文字修复

```bash
python3 "$SKILL_PATH/scripts/retouch_ticket.py" retouch \
  --job-id tea-label-204 --asset-id tin-front-v3 --source /path/to/tin-photo.jpg \
  --asset-type packaging --channel "京东与Amazon Listing" \
  --sku-record "Green Tea 80g量产铁罐，正面标签V3，批准批次2026-08" \
  --truth-source /path/to/label-v3-qc.png /path/to/tin-structure.jpg \
  --truth-role "正面标签V3的逐字内容、字体层级和Logo" "铁罐结构、盖沿与绿色事实" \
  --defect "拍摄反光遮住标签第二行末尾字符" --edit-zone "正面标签第二行右侧反光区域" \
  --acceptance "字符按QC图完整可辨，字号、字距、印刷颗粒和标签透视连续" \
  --change-budget "只修复被反光遮住的批准字符，不重排整个标签" \
  --preserve "铁罐形状和盖沿" --preserve "标签位置与透视" --preserve "Logo大小和颜色" \
  --preserve "80g净含量区域" --preserve "背景、阴影和原裁切" \
  --text-policy repair-from-qc --approved-text "GREEN TEA\nNET WT. 80 g" \
  --finish "保留真实印刷网点、金属反射和标签纸张质感" \
  --reject "不改配料、产地、批次、认证、条码，不生成宣传语或重新设计包装"
```

### 3. 服装拍摄色偏校正

```bash
python3 "$SKILL_PATH/scripts/retouch_ticket.py" retouch \
  --job-id shirt-color-305 --asset-id linen-blue-front --source /path/to/shirt-raw.jpg \
  --asset-type flat-lay --channel "淘宝SKU图与Shopify PDP" \
  --sku-record "Linen 02雾蓝SKU，批准面料色卡B-17、纽扣数量和版型" \
  --truth-source /path/to/approved-color-card.jpg /path/to/shirt-qc.jpg \
  --truth-role "D65环境下批准雾蓝色卡B-17" "版型、缝线、纽扣和面料纹理事实" \
  --defect "原图整体偏青，面料未达到批准雾蓝" --edit-zone "仅衬衫面料像素，不含背景和纽扣" \
  --acceptance "面料综合色接近QC色卡，同时保留阴影、织纹和褶皱明暗" \
  --change-budget "执行受控白平衡与局部颜色校正，不重绘服装" \
  --preserve "Linen 02版型" --preserve "纽扣数量和颜色" --preserve "缝线与口袋位置" \
  --preserve "亚麻织纹与真实褶皱" --preserve "背景灰度、阴影和裁切" \
  --finish "自然D65商品摄影，面料纹理真实，不磨平纤维" \
  --reject "不改成其他蓝色、不增减纽扣、不收腰、不抚平全部褶皱或换背景"
```

### 4. 金属家电高光控制

```bash
python3 "$SKILL_PATH/scripts/retouch_ticket.py" retouch \
  --job-id kettle-reflect-408 --asset-id kettle-side-a --source /path/to/kettle-raw.jpg \
  --asset-type packshot --channel "天猫详情页与Amazon A+" \
  --sku-record "K8不锈钢水壶，批准拉丝方向、壶嘴、把手、刻度窗和Logo" \
  --truth-source /path/to/kettle-qc-side.jpg \
  --truth-role "壶体结构、拉丝纹、刻度窗、Logo和批准反射范围" \
  --defect "左侧条形灯反射过曝并吞掉拉丝纹" --edit-zone "壶体左侧从肩部到下缘的窄高光" \
  --acceptance "高光仍存在但不过曝，拉丝方向连续，壶体曲率可读" \
  --defect "把手内侧出现摄影棚杂物倒影" --edit-zone "黑色把手内缘小块反射" \
  --acceptance "移除杂物形状并延续原环境渐变，不形成纯黑贴片" \
  --change-budget "只控制失控反射，不重新塑造产品或全局换光" \
  --preserve "壶体轮廓和曲率" --preserve "拉丝方向" --preserve "壶嘴与把手结构" \
  --preserve "刻度窗、Logo和接口" --preserve "背景、接触阴影和原透视" \
  --finish "真实不锈钢商业摄影，高光有层次，仍可识别环境反射" \
  --reject "不镜面化、不改变拉丝密度、不隐藏接缝、不增加水汽、文字或配件"
```

### 5. 模特佩戴商品边缘修复

```bash
python3 "$SKILL_PATH/scripts/retouch_ticket.py" retouch \
  --job-id bag-model-512 --asset-id crossbody-look-03 --source /path/to/model-bag-raw.jpg \
  --asset-type on-model --channel "小红书与Instagram" \
  --sku-record "Cross 03棕色包，批准包型、肩带长度、五金和模特授权样片" \
  --truth-source /path/to/bag-qc.jpg /path/to/model-approved-frame.jpg \
  --truth-role "包型、五金、皮纹和肩带事实" "模特身份、肤色、姿态和服装事实" \
  --defect "肩带与外套交界出现两处生成式毛边" --edit-zone "右肩到包体之间的肩带两侧边缘" \
  --acceptance "边缘连续自然，肩带宽度不变，衣料和头发遮挡关系真实" \
  --change-budget "只修肩带边缘，不调整人物或商品姿态" \
  --preserve "模特身份、五官和肤色" --preserve "身体比例和姿态" --preserve "服装与头发" \
  --preserve "包型、皮纹、五金和Logo" --preserve "肩带长度、宽度和遮挡顺序" \
  --finish "真实街拍质感，商品边缘清楚但不过度锐化" \
  --reject "不瘦身、不磨皮、不改脸、不延长腿、不换衣服、不改变包型或背景"
```

### 6. Amazon 白底图清洁

```bash
python3 "$SKILL_PATH/scripts/retouch_ticket.py" retouch \
  --job-id amazon-clean-606 --asset-id organizer-main --source /path/to/organizer-white-raw.jpg \
  --asset-type white-background --channel "Amazon Listing首图" \
  --sku-record "Organizer 6件套，批准组件数量、透明度、卡扣与白底构图" \
  --truth-source /path/to/organizer-kit-qc.jpg \
  --truth-role "六个组件、卡扣结构、透明度和相对尺寸事实" \
  --defect "白色背景有三处传感器灰点" --edit-zone "商品外背景的三个孤立灰点" \
  --acceptance "灰点消失，背景均匀，商品边缘和接触阴影不受影响" \
  --defect "右下组件抠图边缘残留一像素暗线" --edit-zone "右下组件外轮廓，避开真实透明折射边" \
  --acceptance "残留暗线消失，透明边缘、折射和结构仍真实" \
  --change-budget "仅执行背景清洁和单处边缘修复" \
  --preserve "六个组件数量" --preserve "卡扣与分隔结构" --preserve "透明度和真实折射" \
  --preserve "相对尺寸和摆放" --preserve "原裁切、主体占比和接触阴影" \
  --background-policy cleanup-only --finish "干净白底商品摄影，透明材质边缘自然" \
  --reject "不移除真实阴影、不增加组件、不改变透明度、结构、占比、文字或构图"
```

## 验收方法

同时查看原图、输出和 QC 源：先放大到 100% 检查每个缺陷区，再缩小检查整体构图。逐项确认验收标准达成，并用差异视角检查未授权区域是否改变。包装文字逐字核对；颜色校正必须在受控显示与批准色卡条件下确认；透明、反光和纹理材质不能只看“更干净”，还要确认光学关系真实。

若输出改变了未列区域、商品事实或人物身份，不继续加提示词掩盖，应退回原图，把工单拆小后重做。

## 首次使用

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/retouch_ticket.py" auth --api-key sk-api-你的密钥
python3 "$SKILL_PATH/scripts/retouch_ticket.py" status --task-id <taskId>
```

API Key 也可放入 `AI_HIVE_API_KEY` 或 `~/.ai-hive/config.json`。默认路由 `COST_FIRST`，支持 `SPEED_FIRST`、`SUCCESS_FIRST`、多个 `--param key=value`、`--no-download` 与自定义输出目录。超时后查询原 `taskId`，不要重复提交。
