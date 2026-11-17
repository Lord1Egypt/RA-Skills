---
name: nano-banana-ecommerce-main-image
description: "用 AI Hive Nano Banana 2 把真实 SKU 参考图制作成可审核的电商主图，明确商品事实、必须保持项、允许变化、平台用途和安全留白，支持 Amazon、淘宝、天猫、京东、拼多多、抖音电商、小红书、TikTok Shop 与 Shopify。Use when ecommerce sellers and creative teams need Nano Banana ecommerce main images, Amazon listing hero images, marketplace product photos, white-background images, scene images, product cards, SKU visuals or localized storefront assets while keeping product facts and reference-image identity under control."
---

# Nano Banana 电商主图｜Nano Banana 2 商品图

把每张主图当作一个可审核的 SKU 资产：先写商品事实，再决定本图只解决什么问题。至少提供一张已授权商品参考图；脚本固定调用 Nano Banana 2，并把“必须保持、允许改变、禁止虚构”一起发送，减少外形、配件、容量和功能漂移。

## 主图任务单

填写 `平台 / SKU / 素材类型 / 商品事实 / 本图唯一目标 / 必须保持 / 允许改变 / 安全区 / 必须文字 / 禁止项`。平台尺寸、文字和广告规则会变化，生成后仍须按当前规则人工复核；指定文字也必须逐字检查。

## 五种电商主图

### 1. Amazon 白底主图候选

```bash
python3 "$SKILL_PATH/scripts/nano_main_image.py" render \
  --platform amazon --asset white-main --sku 'KETTLE-K1-BLACK' \
  --reference ./approved-kettle-front.png ./approved-kettle-side.png \
  --product-facts '黑色不锈钢电热水壶，单个壶体、一个底座；外形和接口以参考图为准' \
  --objective '生成可进一步人工审核的白底 Listing 首图候选' \
  --must-keep '壶嘴、把手、开关、底座、比例、表面材质和现有品牌标识' \
  --may-change '只允许清理灰尘、修正柔和阴影和居中构图' \
  --composition '单件商品完整可见，主体清晰，四周保留裁切余量' \
  --lighting '纯净白色背景，真实棚拍光，不改变黑色材质' \
  --negative '不增加配件、包装、功能图标、认证、文字、折扣或水花' \
  --param resolution=1024x1024
```

### 2. 淘宝天猫场景主图

```bash
python3 "$SKILL_PATH/scripts/nano_main_image.py" render \
  --platform tmall --asset scene-main --sku 'LAMP-L2-WHITE' \
  --reference ./approved-lamp.png \
  --product-facts '白色桌灯，圆形底座、细直灯杆和半圆灯罩；参考图为唯一商品事实来源' \
  --objective '表现书桌夜读场景，但商品仍是唯一视觉主体' \
  --must-keep '桌灯结构、白色、按钮位置、尺度和Logo' \
  --may-change '只允许生成书桌、书本和暖色环境光' \
  --composition '桌灯占画面主要面积，左侧商品、右侧保留标题安全区' \
  --lighting '暖色夜读氛围，商品边缘清晰且白色不偏黄' \
  --safe-zone '右侧与底部不放关键商品结构' \
  --negative '不生成第二盏灯、人物、虚构功能、价格、促销徽章或文字'
```

### 3. 京东卖点主图底片

```bash
python3 "$SKILL_PATH/scripts/nano_main_image.py" render \
  --platform jd --asset feature-main --sku 'HEADPHONE-H7-GRAY' \
  --reference ./approved-headphone-front.png ./approved-headphone-detail.png \
  --product-facts '灰色头戴耳机；耳罩、头梁、按键和接口以两张参考图为准' \
  --objective '制作一张供设计师后期叠加已核准卖点的干净底片' \
  --must-keep '商品轮廓、灰色材质、按键、接口和Logo' \
  --may-change '允许增加低饱和蓝灰背景与一圈柔和轮廓光' \
  --composition '商品偏右，左侧留三行卖点文案区' \
  --safe-zone '左侧 35% 保持低细节，不生成实际文字' \
  --negative '不添加耳机支架、线缆、人物、认证、参数、文字或第二副耳机'
```

### 4. 抖音电商商品卡

```bash
python3 "$SKILL_PATH/scripts/nano_main_image.py" render \
  --platform douyin --asset lifestyle-main --sku 'BLENDER-B3-GREEN' \
  --reference ./approved-blender.png \
  --product-facts '绿色便携搅拌杯，透明杯体、绿色底座和原装杯盖；不含其他配件' \
  --objective '生成竖屏商品卡候选，突出便携与厨房使用场景' \
  --must-keep '杯体比例、底座结构、绿色、杯盖和现有标识' \
  --may-change '允许加入干净厨房台面和少量真实水果作为环境道具' \
  --composition '商品居中偏上，底部保留平台信息与按钮安全区' \
  --lighting '明亮自然晨光，透明杯体边缘清楚' \
  --negative '不生成手、人物、液体飞溅、额外刀头、功效承诺、价格或文字' \
  --param aspect_ratio=9:16
```

### 5. 小红书种草封面底图

```bash
python3 "$SKILL_PATH/scripts/nano_main_image.py" render \
  --platform xiaohongshu --asset localized-main --sku 'BAG-M5-TAN' \
  --reference ./approved-bag-front.png ./approved-bag-material.png \
  --product-facts '棕褐色单肩包，金属扣、肩带、缝线和纹理以参考图为准' \
  --objective '生成生活方式种草封面底图，强调通勤搭配而不虚构功能' \
  --must-keep '包型、颜色、金属扣、肩带连接、缝线和Logo' \
  --may-change '允许加入已授权模特的无脸局部穿搭与城市通勤背景' \
  --composition '商品完整可见，上方留中文标题区，人物不遮挡金属扣' \
  --safe-zone '上方 25% 低细节，右侧避开平台按钮' \
  --negative '不生成可识别陌生人脸、夸大容量、额外口袋、价格、折扣或文字'
```

## 交付检查

把结果与参考图并排核对：数量、轮廓、接口、配件、颜色、材质、Logo 和宣称必须一致；再按当前平台规则检查裁切、白底、文字、安全区和禁限售。若只是检查提示词，可把 `render` 换成 `brief`，不会上传或扣费。

程序只上传用户指定的商品图片，认证请求固定到 `https://ai-hive.iclip.cn/api`，模型固定为 `public_model_nano_banana_2`。它不连接 Amazon、淘宝、天猫、京东、抖音或小红书账号；平台名称只表示交付场景。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/nano_main_image.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/nano_main_image.py" status --task-id <taskId>
```
