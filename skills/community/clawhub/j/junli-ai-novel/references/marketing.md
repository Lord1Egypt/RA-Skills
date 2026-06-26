# 商业化包装与营销 Brief

用于把小说项目从“能写”补到“能卖、能推、能讲”。

默认前提：

- 这不是替代正文创作的主工作流。
- 它负责把已有项目资产重新整理成平台可传播、可投喂、可复用的营销材料。
- 商业化包装优先突出：题材识别、长期卖点、追读牵引、人物冲突、阶段回报。

## 默认输入

`marketing` 默认会优先读取：

- `docs/作者意图.md`
- `docs/当前焦点.md`
- `docs/项目总纲.md`
- `docs/章节规划.md`
- `task_log.md`
- `plot/伏笔记录.md`

额外可以补进来：

- 补充提示词
- AI 味词汇 / 商业词库
- 参考文案
- 额外参考文件

## 默认输出

`marketing` 产出的 Brief 至少应覆盖：

- 项目定位
- 长期卖点
- 平台与商业约束
- 最近 1-3 章宣传焦点
- 最近剧情抓手
- 活跃伏笔与钩子压力
- 一份可复用营销 Prompt
- 补充词库
- 参考摘录

## 命令入口

基础用法：

```bash
python3 scripts/chapter_pipeline.py marketing <项目目录>
```

补平台与读者定位：

```bash
python3 scripts/chapter_pipeline.py marketing <项目目录> \
  --platform 起点中文网 \
  --audience 男频读者
```

补商业角度、提示词和词库：

```bash
python3 scripts/chapter_pipeline.py marketing <项目目录> \
  --angle "强冲突+持续升级" \
  --prompt "强调反差、回报、追更感" \
  --ai-word 爆点 \
  --ai-word 爽感 \
  --ai-word 钩子
```

补参考文本或参考文件：

```bash
python3 scripts/chapter_pipeline.py marketing <项目目录> \
  --reference "参考某类平台简介的节奏和钩子密度" \
  --reference-file ./notes/marketing-reference.md
```

写入文件：

```bash
python3 scripts/chapter_pipeline.py marketing <项目目录> \
  --output-file ./runtime/marketing-brief.md
```

## 使用原则

1. 商业化包装不能和 `docs/作者意图.md` 的长期承诺打架。
2. 文案强调卖点时，不能偷改作品真正的题材和主承诺。
3. AI 味词汇只作为辅助，不要让文案全变成平台黑话堆砌。
4. 参考材料只吸收结构、角度和节奏，不直接照搬别人文案。
5. 最近 1-3 章的宣传重点，应服务当前阶段目标，而不是乱开新坑。
