---
name: product-background-replacement-commercial
description: "用 AI Hive Nano Banana Pro 把已授权商品图换成白底、生活方式、节日、门店或广告场景，同时锁定商品轮廓、结构、材质、Logo 与比例，并明确相机透视、光线、接触阴影、反射和遮挡关系。Use when ecommerce sellers, photographers and brand teams need commercial product background replacement, white-to-lifestyle composites, marketplace scene images, product photography backgrounds or PhotoRoom, Pixelcut, Meitu, Canva and Adobe Firefly workflow alternatives for Amazon, Taobao, Tmall, JD, Douyin, Xiaohongshu, TikTok Shop or Shopify assets."
---

# 商品换背景与商业场景图｜Nano Banana Pro

换背景不是简单“抠图贴上去”。先锁定商品事实，再让新场景的透视、色温、接触阴影、反射、遮挡和景深与商品一致。脚本固定调用 Nano Banana Pro；商品参考图优先决定商品身份，背景参考图只提供环境与光线。

## 合成任务单

填写 `用途 / 场景 / 原背景只移除什么 / 商品必须保持 / 相机 / 光线 / 承托面 / 接触阴影与反射 / 人物授权 / 裁切安全区`。出现手或模特时必须显式确认授权；背景可以改变，商品轮廓、结构、接口、材质、文字和 Logo 不能被重绘。

## 五种商业换背景

### 1. 白底咖啡机换厨房场景

```bash
python3 "$SKILL_PATH/scripts/product_scene_swap.py" replace \
  --usage '天猫与京东详情页场景图' --scene-type lifestyle \
  --product-reference ./approved-coffee-machine-front.png ./approved-coffee-machine-side.png \
  --scene '现代浅木厨房台面，背景只有简洁橱柜和一只无品牌杯子' \
  --surface table --remove '原白色背景及原接触阴影' \
  --keep '咖啡机轮廓、比例、出水口、按钮、接口、黑色材质、文字和Logo' \
  --camera '保持参考图略高于台面的三分之四视角，垂直线不倾斜' \
  --lighting '右侧窗户柔和晨光，商品高光方向与窗口一致' \
  --grounding '底部生成短而柔和的接触阴影，出水口与台面无穿插，不生成错误镜面反射' \
  --depth '商品清晰，背景轻微虚化' \
  --crop '四周保留详情页裁切余量' \
  --do-not-add '不添加奶罐、胶囊、配件、蒸汽、人物、价格、文字或第二台机器'
```

### 2. 护肤瓶换浴室台面

```bash
python3 "$SKILL_PATH/scripts/product_scene_swap.py" replace \
  --usage 'Amazon Listing 场景辅图' --scene-type storefront \
  --product-reference ./approved-serum-bottle.png ./approved-label-detail.png \
  --background-reference ./approved-stone-bathroom-mood.png \
  --scene '浅色天然石材浴室台面，背景为低细节磨砂玻璃和柔和植物影子' \
  --surface table --remove '原灰色棚拍背景和原投影' \
  --keep '瓶型、滴管、液位、标签文字、Logo、容量标识、玻璃颜色和数量' \
  --camera '保持正面略高机位，瓶体垂直，标签正对镜头' \
  --lighting '左后方柔光，玻璃透光与高光连续，标签仍可读' \
  --grounding '瓶底接触石材，生成短接触阴影和低强度真实反射；反射不得复制成第二个商品' \
  --depth '标签与瓶缘清晰，背景柔化' \
  --crop '商品居中偏右，左侧留文案区' \
  --do-not-add '不生成水滴、花瓣、成分、功效、认证、人物、文字或额外瓶子'
```

### 3. 手持包袋种草场景

```bash
python3 "$SKILL_PATH/scripts/product_scene_swap.py" replace \
  --usage '小红书与抖音电商种草图' --scene-type social-ad \
  --product-reference ./approved-bag-front.png ./approved-bag-strap.png \
  --background-reference ./approved-commute-mood.png \
  --scene '城市通勤入口，已授权模特只出现肩部以下的无脸局部' \
  --surface handheld --people-mode authorized-model --people-authorized \
  --remove '原白底、原吊挂线和原投影' \
  --keep '包型、颜色、金属扣、肩带长度与连接、缝线、纹理和Logo' \
  --camera '中近景，包袋正面完整可见，人物身体透视自然' \
  --lighting '阴天柔光，金属扣高光与环境一致' \
  --grounding '肩带真实受力并贴合肩部，手指不遮挡金属扣，包体与衣服有自然遮挡关系' \
  --depth '包袋最清晰，人物和背景适度虚化' \
  --crop '上方留标题安全区，右侧避开平台按钮' \
  --do-not-add '不生成可识别人脸、额外口袋、第二条肩带、价格、折扣、文字或品牌合作暗示'
```

### 4. 沙发换客厅样板间

```bash
python3 "$SKILL_PATH/scripts/product_scene_swap.py" replace \
  --usage 'Shopify PDP 与家居广告场景图' --scene-type campaign \
  --product-reference ./approved-sofa-front.png ./approved-sofa-side.png ./approved-leg-detail.png \
  --scene '现代客厅，浅灰墙面、木地板、低矮无品牌边几，空间尺度真实' \
  --surface floor --remove '原摄影棚背景、原地面和原阴影' \
  --keep '沙发长度比例、靠背、坐垫数量、面料颜色、四只脚、缝线和Logo' \
  --camera '保持参考图平视三分之四角度，地平线与家具尺度一致' \
  --lighting '左侧大窗柔光，坐垫凹凸和面料纹理清楚' \
  --grounding '四只脚全部落地，每只脚有方向一致的接触阴影；边几不遮挡沙发结构' \
  --depth '沙发整体清晰，后墙轻微虚化' \
  --crop '横版主视觉，左右保留广告裁切余量' \
  --do-not-add '不改变坐垫数量、脚、尺寸、颜色，不生成抱枕、人物、宠物、价格或文字'
```

### 5. 跨境节日场景本地化

```bash
python3 "$SKILL_PATH/scripts/product_scene_swap.py" replace \
  --usage 'TikTok Shop 与 Shopify 节日广告底图' --scene-type localized \
  --product-reference ./approved-candle-set.png ./approved-package.png \
  --background-reference ./approved-winter-palette.png \
  --scene '冬季礼赠桌面，深绿色织物、暖色散景和少量无文字礼盒；不指向特定宗教或官方活动' \
  --surface table --remove '原纯色背景与原阴影' \
  --keep '三只蜡烛的数量、尺寸关系、颜色、标签、Logo、包装结构和已有文字' \
  --camera '略高俯拍，三只商品与包装全部可见' \
  --lighting '右后方暖光，烛杯材质和包装色彩准确' \
  --grounding '每只蜡烛与包装都接触桌面，阴影方向一致，织物遮挡不超过商品底部边缘' \
  --depth '商品和包装清晰，背景散景只做氛围' \
  --crop '同时适配方图和竖图裁切，核心商品保持在中央安全区' \
  --do-not-add '不点燃蜡烛，不添加品牌、节日文字、价格、折扣、认证、食物或第四只蜡烛'
```

## 合成验收

放大检查商品边缘、半透明区域、细线、标签和 Logo；再检查脚、底座、肩带等接触点，以及阴影方向、反射强度、遮挡顺序、透视和色温。与原商品图并排核对后，再按当前平台规则复核裁切与文字。把 `replace` 改为 `preview` 可只检查换背景说明。

认证请求固定到 `https://ai-hive.iclip.cn/api`，模型固定为 `public_model_nano_banana_pro`。PhotoRoom、Pixelcut、美图、Canva 与 Adobe Firefly 名称仅用于用户比较搜索；本工具不连接这些服务或任何电商后台。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/product_scene_swap.py" auth --api-key REDACTED-SECRET
python3 "$SKILL_PATH/scripts/product_scene_swap.py" status --task-id <taskId>
```
