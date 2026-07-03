# 工作流: 文本投喂

用户粘贴一段含有目标人物发言的文本时,执行本流程。

## 步骤 1: 代号确认 (关键!)

⚠️ **本 Skill 的核心隐私保护:绝不在 memory 中写真名。**

如果用户的粘贴文本里出现了真名(比如"王总说...""老板回复说..."):

```
我注意到文本中出现了"王总"——这是我们要画像的人吗?
我会在 memory 中用代号 {npc_id} 表示他/她,
本对话中也会用代号回应。这样:
- 文件被同步/泄露,看不出对应哪位真人
- 你保留心智地图(代号↔真名对应)在自己脑子里

确认用 {npc_id} 指代吗?
```

得到确认后,**之后所有输出中真名都自动替换为代号**。

如果存在多个画像,先询问"这段是关于哪位的? L001 / L002 / L003"。

## 步骤 2: 场景识别

引导式提问,但能从上下文推断的不要问:

```
我先确认这段的来源:
- 渠道: 会议 / 邮件 / IM / 文档批注 / 公开发言 / 其他?
- 大概时间: 精确到日,记不清就写月份
- 当时讨论什么话题? (一句话)
```

## 步骤 3: 说话人归因

**这一步不能跳过——错误归因会污染画像。**

如果文本看起来是多人对话:

```
我看到文本里有几段发言,请帮我标一下哪些是 {npc_id} 说的:

[逐行编号显示]
1. "需要更多的数据支持。"
2. "我同意,我们再调研一周。"
3. "周三之前出方案。"
4. "好的,我来跟进。"

哪几条是 {npc_id} 的? (例: "1 和 3 是")
```

如果文本看起来全是目标人物说的,简化为:

```
确认一下,这段都是 {npc_id} 本人说的对吧?
```

## 步骤 4: Attribution 判定

根据归因情况确定 attribution 字段(决定证据等级权重):

| 用户说法 | attribution | 权重 |
|---------|-------------|------|
| 我亲眼/亲耳听到的原文 | direct | 1.0 |
| 媒体或正式文档里引述的"原话" | quoted | 0.7 |
| "他大概意思是..."/"听他说..." | paraphrased | 0.4 |
| "听说他觉得..."/"有人评价他..." | evaluated | 0.2 |

不确定时默认 `paraphrased`,并问用户确认。

## 步骤 5: 信息密度过滤

**低密度内容标记 `low_density: true`,只影响风格学习,不进决策推理**。

低密度信号(标记后入库,但不更新 decision_axes):
- 长度 < 10 字且无明确观点("嗯,知道了"、"OK")
- 纯礼貌性回应("辛苦了"、"好的谢谢")
- 纯事实陈述无评价("今天 3 点开会")

高密度信号(完整处理):
- 含质询/反问("数据来源是什么")
- 含判断/评价("这个方向不对")
- 含偏好表达("我更看重...")
- 含决策("立项"、"暂缓"、"砍掉")

## 步骤 6: 抽取结构化信号

调用 `scripts/extract_signals.py` 或在对话中直接抽取。需要抽出:

```yaml
challenges_raised:
  - theme: 此处的主题(如"ROI 依据"、"样本量"、"竞品对标")
    intensity: low / medium / high

preferences_expressed:
  - dimension: 对应哪个 decision_axis
    direction: 偏向 0 端还是 1 端
    strength: 0-1

style_signals:
  - prefers_bluf: true/false
  - tolerates_uncertainty: true/false
  - interrupt_frequency: low/medium/high

redline_signals:  # 触发了什么不满
  - 具体表达
```

## 步骤 7: 生成预览,等用户确认

**关键:不要直接写文件,先展示完整 diff:**

```
我准备做以下变更,请你过目:

📁 写入到: ~/npc-distill/memory-L001.md
🆕 新增语料: ## C-20260520-003

  - date: 2026-05-20
  - scene: Q3 复盘会
  - channel: 会议
  - attribution: direct
  - weight: 1.0

  **场景**: 产品同学汇报 Q3 增长数据...

  **内容**:
  > "数据来源是哪里? Q1 的样本太小了。"

  **抽取信号**:
  - challenges_raised: ROI 测算依据 (intensity: high)
  - style_signals: prefers_bluf = true
  - preferences_expressed: data_vs_intuition direction=1 strength=0.8

📊 画像更新:
  evidence_count:    46 → 47
  confidence:        medium → medium (累计)
  
  frequent_challenges 变化:
  - ROI 测算依据: weight 0.82 → 0.85, evidence + C-20260520-003
  
  decision_axes 变化:
  - data_vs_intuition: 0.70 → 0.72 (累计证据 17→18)
  - 其他 axes 不变

确认写入吗? (yes / 修改某项 / 取消)
```

## 步骤 8: 执行写入

用户确认 yes 后:

```bash
python scripts/update_memory.py \
  --file ~/npc-distill/memory-L001.md \
  --action add_corpus \
  --signals /tmp/extracted-signals.json
```

完成后输出:

```
✅ 已记录到 C-20260520-003
📊 L001 画像状态: 47 条证据, confidence = medium
📁 完整 memory 在: ~/npc-distill/memory-L001.md

下一步建议:
- 继续投喂其他片段 (输入或粘贴)
- 查看更新后的画像 (输入"看 L001 画像")
- 用更新后的画像演练 (输入"压测我的方案")
```

## 错误处理

| 情况 | 处理 |
|------|------|
| 用户粘贴的文本里没识别出明显说话人 | 询问"这段是 L001 说的全部,还是其中部分?" |
| 文本超长(>5000 字) | 提示"内容较多,我拆成几段逐一确认" |
| 文本含他人隐私(电话/账号/身份证) | 警告并询问是否要脱敏 |
| 用户中途改主意 | 不写入任何文件,清空临时抽取结果 |

## 反例: 不要这样做

❌ 不要在用户没确认前就修改 memory.md
❌ 不要在抽取时虚构原文没有的信号
❌ 不要把"评价"(evaluated)等同于"原话"(direct)
❌ 不要因为"觉得这句话很代表 X 的风格"就提升 weight,只按规则计算
❌ 不要在 memory 中写真名,即使用户的粘贴文本里有
