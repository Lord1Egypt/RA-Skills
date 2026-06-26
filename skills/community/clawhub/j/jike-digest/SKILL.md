---
name: jike-digest
description: |
  抓取指定即刻 Topic 最近 50 条内容，筛选最近 24 小时内有价值的 post，生成摘要、可实践建议、灵感启发，输出为每日精选 Markdown 文档。
  当用户说"帮我总结即刻 topic"、"即刻日报"、"jike digest"、"jike 摘要"、"即刻每日精选"、"抓取即刻 {topic_id}"时使用。
---

# 即刻 Topic 每日摘要

## 配置

优先级：命令行参数 > 环境变量 > 默认值

| 参数 | 环境变量 | 默认值 |
|------|---------|--------|
| `--topic-id` | `JIKE_TOPIC_ID` | （必填，无默认值） |
| `--base-dir` | `JIKE_DIGEST_BASE_DIR` | `/Users/victor/Desktop/resource/daily-info/jike` |

若 `topic-id` 未提供且无环境变量，报错并提示用户。

常用 Topic ID：

| Topic | ID |
|-------|----|
| AI 探索站 | 63579abb6724cc583b9bba9a |
| 产品经理的日常 | 563a2995306dab1300a32227 |
| 大产品小细节 | 57079a1526b0ab12002c29da |
| 副业探索小分队 | 65544021a2935ec6b005bcd2 |
| 薅羊毛小分队 | 5523d164e4b0466c6563cd30 |
| 科技圈大小事 | 597ae4ac096cde0012cf6c06 |

输出路径：`{BASE_DIR}/{topic_id}/{YYYYMMDD}/jike-{topic_name}-{YYYYMMDD}.md`

## 依赖

- **autocli**：获取 Topic 内容
- **scripts/filter_recent.py**：过滤最近 24 小时内的 posts

## 执行流程

### Step 1: 初始化

1. 确定 `TOPIC_ID` 和 `BASE_DIR`
2. 若 `{BASE_DIR}/{topic_id}/{YYYYMMDD}/` 已存在则清空与当前 topic 相关文件
3. `mkdir -p {BASE_DIR}/{topic_id}/{YYYYMMDD}`

### Step 2: 获取并过滤内容

```bash
autocli jike topic {topic_id} --limit 50 -f json | python3 {SKILL_DIR}/scripts/filter_recent.py
```

脚本将统计信息输出到 stderr，过滤后的 JSON 数组输出到 stdout。也可单独调用：

```bash
# 自定义时间窗口（如 48 小时）
python3 {SKILL_DIR}/scripts/filter_recent.py --input posts.json --hours 48

# 保存过滤结果到文件
autocli jike topic {topic_id} --limit 50 -f json | python3 {SKILL_DIR}/scripts/filter_recent.py --output filtered.json
```

### Step 3: 筛选与分析

1. **低价值剔除**：对 Step 2 结果，进一步剔除纯表情、纯图片无文字、明显低质量、过于私人化的内容
2. 对保留的 post 逐条生成分析。输出格式见 [references/output-template.md](references/output-template.md)。

### Step 4: 写入文档

将分析结果按模板写入输出文件，**使用简体中文撰写**，保持即刻社区轻松有态度的风格。
