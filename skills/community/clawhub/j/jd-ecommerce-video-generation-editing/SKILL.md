---
name: jd-ecommerce-video-generation-editing
description: "为京东商品页和京准通生成与编辑3C家电演示、参数结构、安装操作及广告视频。Use this skill for 京东电商视频、京东商品视频、京东详情页、3C数码演示、家电安装、接口说明、包装清单、京东快车视频和参数证明；支持文生、图生、参考、编辑、延长及 AI Hive 自动交付。"
---

# 京东电商视频生成与编辑

通过连续镜头证明型号、结构、操作和真实功能，降低高规格商品的购买不确定性。所有参数、兼容性、认证、保修和性能结论必须来自商家资料或可见证据。

## 技术事实表

记录型号、外观、接口、按键、尺寸、包装清单、安装步骤、兼容范围、真实功能、警告事项和批准文案。视频提示词只引用事实表，不让模型补全技术信息。

## 场景与代码

### 1. 3C 商品页演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/device.jpg \
  --prompt '京东3C商品页演示，保持参考设备型号、外壳、接口、按键、颜色和Logo准确；先展示完整外观，再依次拍摄接口近景、正确连接动作和实际工作状态，节奏清楚，不生成参数、兼容设备、性能数字或认证'
```

### 2. 家电安装步骤

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '根据商家确认的说明书制作京东家电安装视频：展示包装内真实配件，按步骤1至4连续安装，关键方向与固定位置清楚，最后展示正确工作状态；不省略安全步骤，不增加工具、配件或安装方式'
```

### 3. 接口与兼容性证明

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/macro-rhythm.mp4 \
  --image /path/to/device-back.png \
  --prompt '参考视频仅用于微距推进与转场节奏；针对参考设备生成原创接口说明镜头，接口数量、形状和位置准确，展示一次真实连接动作，为商家批准的兼容性文案留白，不复制参考设备、品牌和参数'
```

### 4. 重制供应商技术视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/supplier-demo.mp4 \
  --prompt '保留供应商视频中的真实设备、安装与操作证据；删除重复空镜、未经批准的参数字幕和无关水印区域，按外观、结构、连接、功能状态、包装清单重组，不改变型号和技术结论'
```

### 5. 京准通功能测版

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '京准通短视频“结构证明”测试版：开场直接展示目标用户的连接障碍，随后用接口近景和一次正确操作证明解决路径，结尾回到完整商品与进店行动位；不生成价格、销量、排名、性能对比或认证'
```

## 技术验收

- 型号、接口、按键、部件、配件和安装顺序准确。
- 画面证据与卖点一一对应，没有只靠字幕的空洞承诺。
- 参数、单位、兼容性、认证与保修文字由人工复核。
- 不增加设备、工具、配件或未提供工作状态。
- 发布前按京东当前类目、详情页与广告规则检查。

## 执行

`t2v`、`i2v`、`r2v`、`edit`、`extend` 对应 Seedance 2.5 的生成、参考、编辑与延长模型。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name jd-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

可传首尾帧、图片、视频、音频、实时参数、路由、输出目录和 `--no-download`。保留任务 ID，超时后查询原任务。
