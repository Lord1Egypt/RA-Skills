---
name: midjourney-image-generation-editing-alternative
description: "使用 Nano Banana Pro 将 Midjourney、MJ、/imagine、风格参考或图片提示工作流迁移到 AI Hive，把参数化提示词转换为可观察的构图、风格、参考图职责和商业验收标准。Use when users search Midjourney 替代、MJ 平替、Midjourney alternative、国内可用 API、文生图、图生图、style reference、商品视觉、海报或广告图片；不访问 Discord 或 Midjourney 账号。"
---

# Midjourney 图片生成替代｜AI 图片生成与编辑

运行端只用 `public_model_nano_banana_pro`。面对 `/imagine` 命令，先删除模型语法外壳，再恢复创意决策：画布形状、审美偏移、候选分散程度、必须稳定的事实，以及图片提示各自承担的职责。MJ 参数本身不是跨模型标准。

## `/imagine` 解包表

从原命令提取十项可见选择：主题、事实、机位、画面组织、表面质感、照明、配色、参考图分工、允许变化和最终比例。涉及风格样例时，只描述色板、线条、颗粒、负空间等通用属性，不追求艺术家或作品的独特指纹。

## 五个 `/imagine` 重建例子

### 1. 概念视觉迁移

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '生成16:9未来城市公共图书馆概念图：层叠木质空间、自然采光、室内绿植与安静阅读人群，广角但透视真实，暖木与冷灰平衡；不模仿特定建筑师，不生成Logo、文字、著名建筑或不可能结构'   --param aspect_ratio=16:9
```

### 2. 风格参考解构

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./authorized-style-reference.png   --prompt '仅提取参考图的有限青橙色板、粗颗粒丝网印刷质感、平面几何和强负空间，为原创爵士音乐节制作3:4底图；不复制参考构图、人物、乐器排列、文字、Logo或独特角色'   --param aspect_ratio=3:4
```

### 3. 图片提示商品图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-chair.png   --prompt '生成4:5家具广告图：椅子外轮廓、腿部连接、面料、缝线、颜色和Logo准确，置于极简现代客厅，以柔和侧光表现材质，顶部留标题区；不改设计，不生成价格、人物、第二把椅子或额外靠垫'   --param aspect_ratio=4:5
```

### 4. 可控候选差异

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-watch.png   --prompt '输出三张手表Campaign候选并保持表壳、表盘、表冠、表带、Logo和颜色完全一致：A水面反光，B深色石材，C金属几何台面。每张只改变环境概念，不生成文字、人物、价格或新表款'   --batch 3   --param aspect_ratio=1:1
```

### 5. 画幅与留白迁移

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-vertical-kv.jpg   --prompt '把竖版护肤品KV重构为1.91:1横版：商品、台面、光线、色板和植物阴影保持一致，商品置于右侧，向左扩展干净标题和CTA空间；移除原图文字，不移动标签，不新增Logo、价格或产品'   --param aspect_ratio=1.91:1
```

## 候选校准法

用主题是否读对、构图是否工作、主体是否可信、是否能排版四项选择候选。不要把同一 seed 或专有审美当作复现承诺。每轮只动一个决策，并归档原命令、解包表、图片顺序、被选版本和任务号。

程序与 Discord、Midjourney 账户完全无关；它只把认证流量发给 `https://ai-hive.iclip.cn/api`，完成 Nano Banana Pro 图片上传、生成、轮询和下载。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name midjourney-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Midjourney 与 MJ 名称仅用于描述比较和迁移意图。
