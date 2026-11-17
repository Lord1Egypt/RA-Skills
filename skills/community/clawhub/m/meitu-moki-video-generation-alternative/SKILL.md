---
name: meitu-moki-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 将美图 MOKI、美图视频或时尚商业视频流程迁移为品牌可审的镜头资产，支持文生、商品首帧、参考风格、视频改版与镜头延长。Use when users search MOKI 替代、美图视频平替、Meitu MOKI alternative、时尚广告、美妆视频、电商产品片、品牌 Campaign 或视频生成 API；不连接美图账号，也不表示官方合作。"
---

# 美图 MOKI 视频生成替代｜AI 视频生成与编辑

围绕“品牌资产保护”组织迁移：商品、模特授权、服装、妆发、Logo 和色板先锁定，再决定镜头气质。底层调用 Seedance 2.5 五种视频模式，不把 MOKI 模板或项目参数假装成兼容输入。

## 品牌镜头档案

记录 `SKU或人物授权 / 不可变外观 / 品牌色 / 光线规则 / 相机语言 / 后期文字区 / 禁用主张`。同一 Campaign 的不同镜头可以变化动作和布景，但不能悄悄更换产品、模特身份或包装。

## 五个商业镜头

### 1. 时尚质感文生镜头

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode t2v   --prompt '5秒9:16时尚配饰广告。深灰镜面空间，一只无品牌银色手袋从暗处被窄束光照亮，摄影机缓慢横移，金属扣产生克制高光，最后在正面稳定停住；不生成模特、文字、Logo、第二只包或夸张变形'   --param aspect_ratio=9:16 duration=5
```

### 2. 美妆商品首帧

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode i2v   --first-frame ./approved-lipstick.png   --prompt '保持首帧口红管型、膏体、标签、颜色、Logo和数量。5秒内产品缓慢转动约25度，柔光沿金属边缘移动，最后停在品牌正面；不生成手、嘴唇、文字、功效、花瓣或额外口红'   --param aspect_ratio=9:16 duration=5
```

### 3. 品牌光线参考

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode r2v   --image ./approved-perfume.png ./brand-palette.png   --video ./authorized-light-sweep.mp4   --prompt '图1锁定香水商品，图2锁定品牌色，视频只提供从左到右的光线扫过节奏。生成5秒1:1棚拍，不复制参考视频商品、场景或文字，不改变瓶型、标签、液体色和Logo'   --param aspect_ratio=1:1 duration=5
```

### 4. Campaign 背景改版

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode edit   --video ./authorized-campaign-cut.mp4   --prompt '保持模特身份、妆发、服装、商品、动作、镜头速度和剪辑长度，只把背景改为品牌批准的深蓝到紫色柔和渐变并匹配原光线；不改变肤色、不生成文字、Logo或新道具'
```

### 5. 延长收尾 Packshot

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode extend   --video ./approved-packshot.mp4   --extend-direction forward   --prompt '从末帧延长3秒：摄影机保持静止，商品高光缓慢减弱，背景粒子自然停下，留出后期Logo和口号时间；不生成实际文字、不移动商品、不切镜、不新增人物或包装'   --param duration=3
```

## 品牌审片

逐帧比对商品包装、人物身份、肤色、服装、配饰和品牌色；检查高光没有改变材质，后期文字区足够，编辑与延长接点不可见。保存批准资产、镜头档案、任务号和使用渠道。

脚本与 MOKI、美图账号无连接；认证请求固定发往 `https://ai-hive.iclip.cn/api`，只执行 Seedance 2.5 视频上传、生成、查询和下载。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name meitu-moki-video-generation-alternative
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

MOKI 与美图名称只用于商业视频迁移搜索。
