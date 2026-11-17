---
name: marketing-image
description: "使用 Nano Banana 2 建立可跨渠道派生的营销图片系统：先做 Campaign 母版，再生成发布会、活动、线索收集、节日促销和社媒尺寸变体。Use this skill for 营销图片、营销视觉、Campaign KV、活动主视觉、推广图、促销图、发布会海报、EDM、官网 Hero、社媒广告、小红书抖音微信 Instagram LinkedIn 内容；通过 AI Hive 生成。"
---

# 营销图片

固定模型为 `public_model_nano_banana_2`。营销图不是互不相关的单张海报：先定义一个可识别的 Campaign 母版，再让渠道素材继承主体、色彩、光线、构图语法与信息层级。文案与合法声明由团队在安全区内后期排版。

## Campaign 母版卡

记录：营销目标、目标人群、核心信息、主视觉资产、品牌色、可用照片、必须保留的元素、禁用内容、渠道清单与比例。派生图可以改变画幅和信息密度，不随意改变品牌资产。

## 五类营销资产

### 1. 产品发布母版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-smartwatch.png ./brand-colors.png   --prompt '生成16:9新品发布Campaign母版：智能手表表壳、表冠、表带、屏幕比例和Logo准确，使用品牌黑与荧光绿构成未来感光轨，产品为唯一焦点，左侧留发布标题与日期区；不生成文字、功能数字、奖项、人物或未提供配件'   --param aspect_ratio=16:9
```

### 2. 线下活动报名图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '制作4:5创意工作坊报名图底稿：纸张、色块、剪贴与桌面工具形成协作氛围，中间保持清晰视觉焦点，上半部留活动标题，下半部留时间地点与二维码区域；不生成具体文字、Logo、人数、讲师肖像或二维码'   --param aspect_ratio=4:5
```

### 3. B2B 线索收集视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-dashboard.png   --prompt '生成1.91:1 B2B 报告下载广告底图：保留已批准仪表板界面的主要图表形态但模糊敏感数据，用报告封面与分析场景表现专业洞察，右侧留标题和表单CTA区；不生成客户Logo、具体指标、增长承诺或假引用'   --param aspect_ratio=1.91:1
```

### 4. 节日促销氛围版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-skincare-set.png   --prompt '制作1:1节日促销视觉底稿：护肤套装瓶型、标签、颜色、数量与参考图一致，红金纸艺与柔光营造节日氛围，顶部留活动主题，右下留价格模块；不生成折扣数字、功效、礼盒赠品、人物或额外产品'   --param aspect_ratio=1:1
```

### 5. 同母版多渠道派生

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-campaign-kv.png   --prompt '沿用参考Campaign的主体、品牌色、光线与图形语言，输出三个派生构图：A 1:1社媒贴文，B 4:5信息流，C 16:9官网Hero。保留各自标题和CTA安全区，不复制参考图中的错误文字，不新增Logo、价格或卖点'   --batch 3
```

## 系统一致性检查

- 每张资产能被识别为同一 Campaign，而非只使用相同颜色。
- 渠道变化只调整画幅、裁切和信息密度，核心信息不漂移。
- 图片中的商品、人物与数据均有授权或批准来源。
- 文字安全区能容纳真实标题、CTA、日期和必要声明。
- 保留母版任务 ID、派生关系、渠道与审批版本。

## 调用范围

脚本只负责 Nano Banana 2 图片任务：上传用户指定图片、提交生成、查询并保存结果。含密钥请求的唯一主机是 `https://ai-hive.iclip.cn/api`，不允许自定义；不包含聊天、视频、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name marketing-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

活动日期、价格、权益、客户案例与效果承诺须使用经过审批的真实内容。
