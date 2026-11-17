---
name: nano-banana-2-product-image
description: "使用 Nano Banana 2 制作可用于提案、上新和营销测试的产品图，把商品事实、外观锚点、镜头、布光、材质和渠道比例组织成可验收的商业画面。Use this skill for Nano Banana 2 product photography、产品图生成、商品图、白底图、场景图、产品渲染、packshot、hero shot、新品视觉、淘宝天猫京东抖音小红书亚马逊 Shopify 商品素材；可从文字开始，也可用授权参考图锁定产品外观，通过 AI Hive 生成。"
---

# Nano Banana 2 产品图生成

固定使用 `public_model_nano_banana_2`。先建立商品事实表，再决定画面方向；不得为了“高级感”擅自改变商品结构、接口、数量、容量、Logo、包装文字或实际功能。

## 商品事实表

记录产品类别、尺寸比例、轮廓、关键零件、颜色、材质、表面处理、标签与包装、必须可见角度、允许变化、禁止变化和交付比例。没有实拍参考时，将输出标注为概念图；有参考图时，把产品身份与几何视为硬锚点。

## 场景与代码

### 1. 白底标准 Packshot

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-product-front.png \
  --prompt '把参考图中的便携榨汁杯制作成电商白底标准产品图：保持杯体比例、刀头底座、按钮、Logo位置和薄荷绿色完全一致；正面三分之二角度，纯白背景，柔和接触阴影，边缘干净，不增加水果、文字、配件、容量标注或第二个杯子' \
  --param aspect_ratio=1:1
```

### 2. 新品概念静物

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为一款尚未量产的圆角桌面空气质量仪制作概念产品静物：哑光暖白机身、黑色窄边屏、顶部单枚旋钮，置于浅灰微水泥台面，清晨侧光，右侧保留标题区；不生成品牌、界面文字、认证、价格或额外按钮' \
  --batch 3 \
  --param aspect_ratio=4:5
```

### 3. 同款配色系列

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-speaker.png \
  --prompt '基于参考蓝牙音箱生成三种获批配色：石墨黑、砂岩白、森林绿。三版保持机身尺寸、网罩孔径、按键、接口、相机角度、光线和阴影完全一致，每张只出现一个音箱，不改变商标、结构或配件' \
  --batch 3
```

### 4. 功能关系演示图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-lamp.png \
  --prompt '为参考阅读灯制作功能关系产品图：保持灯头、转轴、底座和按钮结构不变，在同一画面用真实尺度展示灯臂可调节的两个批准角度；中性书桌环境，避免发光过曝，不添加角度数字、夸张光效、健康功效或不存在的零件' \
  --param aspect_ratio=16:9
```

### 5. 季节上新 Hero Shot

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-handcream.png \
  --prompt '把参考护手霜制作成秋季上新主视觉：包装形状、盖子、标签版式和真实颜色不变，置于暖棕石材与干燥银杏叶之间，低角度近景、傍晚金色侧光、质感克制，左上留文案区；不生成新文字、折扣、功效图标、手部或第二支产品' \
  --param aspect_ratio=4:5
```

## 验收顺序

1. 先核对商品身份、几何、数量、颜色、Logo和包装事实。
2. 再检查透视、尺度、接触阴影、反射和材质是否可信。
3. 确认道具只服务定位，不遮挡关键卖点或误导标配内容。
4. 检查比例、留白与裁切适配目标渠道。
5. 保存参考图、事实表、提示词、任务 ID 与批准版本。

## 助手边界

脚本仅查询固定 Nano Banana 2 图片模型和当次路由价格，上传命令中明确列出的参考图片，提交图片任务、轮询并保存结果。所有携带 Key 的请求固定发送到 `https://ai-hive.iclip.cn/api`，不接受自定义 API 地址。`init` 可把 Key 以 `0600` 权限存入 `~/.ai-hive/config.json`；不提供聊天、视频、账户或余额能力。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-2-product-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

仅使用获授权的商品与品牌素材。概念图、非标配道具和合成环境应在交付时明确标注。
