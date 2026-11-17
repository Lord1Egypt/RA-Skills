---
name: pixverse-video-generation-alternative
description: "使用 AI Hive Seedance 2.5 将 PixVerse、PixVerse AI 或爱诗科技常见的社媒特效短片迁移为可审的动作与转场方案，支持文生、图片起动、参考节奏、视频编辑和片尾延长。Use when users search PixVerse 替代、PixVerse 平替、PixVerse API、特效视频、社媒短片、变装转场、产品动效、竖屏广告或视频生成编辑；不复制 PixVerse 模板，也不表示官方合作。"
---

# PixVerse 视频生成替代｜AI 视频生成与编辑

把“特效模板”改写成四段因果：触发物出现、变化开始、变化完成、镜头稳定。每条短片只用一个核心效果，并为变形过程设置身份与商品保护条件；执行端固定映射 Seedance 2.5 五种视频能力。

## 效果因果表

写明 `触发条件 / 被影响对象 / 变化路径 / 不受影响区域 / 完成时刻 / 片尾停留`。变装、材质变化和环境转场都要在提示中说明什么不能跟着变，避免背景效果污染脸、Logo 或商品结构。

## 五种社媒效果镜头

### 1. 文生环境转场

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode t2v   --prompt '5秒9:16转场短片。空白摄影棚中央一把红色椅子，地面先出现一圈水波，蓝色海岸环境从水波向外展开，最后椅子仍在原位稳定停留；只发生一次转场，不改变椅子形状和颜色，不生成文字、人物、Logo或第二把椅子'   --param aspect_ratio=9:16 duration=5
```

### 2. 商品材质动效

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode i2v   --first-frame ./approved-sneaker.png   --prompt '保持首帧鞋型、鞋底、鞋带、Logo和配色。5秒内一条柔和蓝色光带从鞋头移动到鞋跟，只增强材料高光，不改变商品材质本身，最后光带消失并停在原画面；不生成脚、文字、烟雾或新鞋'   --param aspect_ratio=9:16 duration=5
```

### 3. 参考节奏但不复制内容

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode r2v   --image ./approved-outfit-a.png ./approved-outfit-b.png   --video ./authorized-transition-rhythm.mp4   --prompt '两张图分别锁定同一授权人物的造型A和B；视频只提供抬手遮镜后切换的节奏。生成5秒变装：身份、脸、发型和背景保持，遮镜期间服装从A变为B；不复制参考演员、场景、文字或品牌'   --param aspect_ratio=9:16 duration=5
```

### 4. 减弱过强效果

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode edit   --video ./authorized-effect-clip.mp4   --prompt '保持人物、商品、动作、镜头、时长和剪辑点，只把覆盖主体的高亮粒子减少约一半并移到画面边缘，使脸和商品标签始终清楚；不改变颜色、不增加文字、Logo或新特效'
```

### 5. 延长片尾停留

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate   --mode extend   --video ./approved-transition-end.mp4   --extend-direction forward   --prompt '从效果完成的末帧继续3秒：人物和商品保持稳定，残余粒子缓慢消散，摄影机不再移动，为后期标题与CTA留出停留；不生成实际文字、不再次变装、不切镜或新增物体'   --param duration=3
```

## 特效审片

逐帧确认触发、变化和完成顺序，主体身份与商品结构在效果前后相同；检查效果不会遮挡脸、标签和后期文字区，并确保片尾有足够稳定帧供剪辑。保存来源素材授权、因果表、任务号与发布比例。

脚本不调用 PixVerse 或爱诗科技账号。认证请求固定前往 `https://ai-hive.iclip.cn/api`，仅开放 Seedance 2.5 视频任务相关命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name pixverse-video-generation-alternative
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

PixVerse 名称只用于说明替代与迁移意图。
