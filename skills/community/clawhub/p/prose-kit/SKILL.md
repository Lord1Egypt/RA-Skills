---
name: prose-kit
description: "AI写作流水线：给一个主题，出9篇风格迥异的中文散文，自动评分排名。"
---

# Prose Kit — AI 写作流水线

给一个主题，生成 9 篇风格迥异的中文散文。每篇用不同学科视角拆解同一个命题。

免费用户每天 3 批，Pro 用户可选 Claude 模型 + 自动评分。

## 使用方法

用户说 "写一批关于 XXX 的散文" 或 "prose-kit XXX" 时触发。

## 执行流程

### Step 0: 检查 API Key

检查环境变量 `PROSE_KIT_API_KEY` 是否存在。

如果不存在，问用户要邮箱，帮他注册：

```bash
curl -s -X POST https://prose-kit.com/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email": "{用户的邮箱}"}'
```

返回 `{"api_key": "pk-xxx", "tier": "free", ...}`。

告诉用户把 key 存到环境变量：`export PROSE_KIT_API_KEY=pk-xxx`

### Step 1: 提交任务

```bash
curl -s -X POST https://prose-kit.com/v1/generate \
  -H "Authorization: Bearer $PROSE_KIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"topic": "{用户的主题}", "with_scoring": false}'
```

如果用户要求评分（Pro 用户），把 `with_scoring` 改为 `true`。

返回：`{"task_id": "abc123", "status": "pending"}`

### Step 2: 轮询并保存结果

**重要：不要把完整的 API 响应输出到对话中。** 用下面的 python 脚本一步完成轮询、保存文件、输出摘要：

```bash
python3 -c "
import json, time, urllib.request, os

task_id = '{task_id}'
api_key = os.environ['PROSE_KIT_API_KEY']
topic = '{topic}'

while True:
    req = urllib.request.Request(
        f'https://prose-kit.com/v1/tasks/{task_id}',
        headers={'Authorization': f'Bearer {api_key}'}
    )
    data = json.loads(urllib.request.urlopen(req).read())
    if data['status'] == 'done':
        break
    if data['status'] == 'error':
        print('ERROR:', data.get('error', 'unknown'))
        exit(1)
    print(f'进度: {data.get(\"progress\", \"waiting\")}...')
    time.sleep(15)

os.makedirs('prose-kit-output', exist_ok=True)
essays = data.get('essays', [])
summary = []
for i, e in enumerate(essays):
    slug = e.get('seed_type', f'v{i+1}')
    fname = f'prose-kit-output/{topic}-{slug}.md'
    with open(fname, 'w') as f:
        f.write(e.get('markdown', e.get('content', '')))
    title = e.get('title', '无题')
    discipline = e.get('discipline', '')
    words = len(e.get('content', ''))
    score = e.get('score', '')
    summary.append(f'| {i+1} | {title} | {discipline} | {words} | {score or \"-\"} | {fname} |')

print()
print('| # | 标题 | 学科 | 字数 | 评分 | 文件 |')
print('|---|------|------|------|------|------|')
print('\n'.join(summary))
print(f'\n共 {len(essays)} 篇，已保存到 prose-kit-output/')
"
```

把 `{task_id}` 和 `{topic}` 替换为实际值。这个脚本会：
1. 轮询直到完成
2. 把每篇散文保存为本地 md 文件
3. 只输出摘要表格（标题、学科、字数、文件路径），不输出全文

### Step 3: 展示结果

脚本已输出摘要表格。告诉用户文件保存在 `prose-kit-output/` 目录，可以直接打开阅读。

如果有评分，按分数从高到低排，推荐前三篇。

### Step 4: 查看用量（可选）

```bash
curl -s https://prose-kit.com/v1/usage \
  -H "Authorization: Bearer $PROSE_KIT_API_KEY"
```

## 定价

| 档位 | 模型 | 价格 | 含评分 | 日限 |
|------|------|------|--------|------|
| 免费 | DeepSeek | ¥0 | 否 | 3批/天 |
| Pro | Claude Sonnet | ¥9.9/批 | 是 | 50批/天 |

升级 Pro → 打开 https://prose-kit.com/buy 完成支付，自动升级。

也可以微信公众号「链上漂流」联系人工升级。
