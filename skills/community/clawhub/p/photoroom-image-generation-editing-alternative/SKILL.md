---
name: photoroom-image-generation-editing-alternative
description: "使用 Nano Banana Pro 迁移 PhotoRoom、Photo Room 或 Photoroom API 常见的电商商品处理需求，完成背景清理、白底图、自然阴影、生活方式场景和批量 SKU 统一。Use when users search PhotoRoom 替代、PhotoRoom 平替、商品抠图、换背景、电商修图、商品摄影、Amazon Shopify 淘宝主图或国内图片编辑 API；不代表与 PhotoRoom 存在官方关系。"
---

# PhotoRoom 图片生成替代｜AI 图片生成与编辑

模型锁定为 `public_model_nano_banana_pro`。先保护商品边界和真实结构，再处理背景、阴影与场景。对于已有商品照片，应把任务写成“主体遮罩协议”：哪些像素区域属于商品、哪些缝隙应透出背景、哪些反射和接触阴影要保留。

## 主体遮罩协议

登记商品轮廓、孔洞、透明件、毛发或流苏、细小配件、Logo、标签、真实颜色、地面接触点和允许替换的背景。对玻璃、珠宝、网布和半透明包装先做边缘试图，避免整批出现白边或结构缺失。

## 五个商品处理场景

### 1. 市场平台白底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-backpack.jpg   --prompt '将背包商品照处理为1:1纯白背景：完整保留包型、提手、肩带、拉链、网袋、缝线、颜色和Logo，清理原背景并重建轻微接触阴影；不改变轮廓，不生成文字、人物、挂件、赠品或额外口袋'   --param aspect_ratio=1:1
```

### 2. 玻璃透明边缘处理

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-glass-vase.jpg   --prompt '把透明玻璃花瓶置于浅暖灰背景，准确保留瓶口、曲面、厚度、透明折射、边缘高光和底部接触，不出现白色抠图边；移除原场景杂物，不生成花、文字、裂纹、颜色变化或第二个花瓶'   --param aspect_ratio=4:5
```

### 3. 自然悬浮阴影

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-shoe.jpg   --prompt '为运动鞋创建干净浅灰棚拍背景和自然悬浮阴影：鞋型、鞋带、鞋底纹路、材料拼接、Logo和颜色不变，阴影方向与主光一致；不改变鞋底厚度，不生成脚、袜子、文字或新配色'   --param aspect_ratio=1:1
```

### 4. 生活方式换景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./raw-camping-lantern.jpg   --prompt '保持露营灯外形、提手、开关、灯罩、颜色和Logo，将背景替换为傍晚露营桌面，以帐篷虚化和木桌提供使用情境；产品仍为焦点，不生成续航数字、人物、火焰、额外配件或品牌文字'   --param aspect_ratio=4:5
```

### 5. 批量 SKU 统一画面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./bottle-blue.jpg ./bottle-green.jpg ./bottle-pink.jpg   --prompt '为三种水杯SKU制作统一1:1商品图：分别保留各自瓶型、杯盖、吸管、颜色和Logo，使用相同三分之二角度、白背景、主体占比和柔和阴影；每张只出现一个SKU，不混色、不新增文字、液体或配件'   --batch 3   --param aspect_ratio=1:1
```

## 边缘与真实性 QA

放大检查透明边、毛发、孔洞、反光、阴影接触和细小配件；与原图对比结构、颜色、Logo和数量；确认场景道具不会被误认作标配。平台白底和边距要求应以当前渠道规则为准。

程序不会调用 PhotoRoom 账号或 API。认证信息只发送到 `https://ai-hive.iclip.cn/api`，固定使用 Nano Banana Pro，并且没有聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name photoroom-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

PhotoRoom 与 Photoroom 名称仅用于用户比较、替代和迁移搜索。
