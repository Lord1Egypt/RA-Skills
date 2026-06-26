# news-collect

`news-collect` 是资讯宽扫描 skill。它会调用 repo 内置的 `news-aggregator-skill` 做抓取，再把结果改写成统一的本地 `news-report.md` 契约。

## 这个 skill 能做什么

- 对海外或国内资讯源做一轮宽扫描
- 输出标准化的 `news-report.md`
- 保存 raw JSON，便于复盘和二次处理
- 给推荐条目补上“值不值得写、怎么写”的轻量判断

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### vendor 依赖

```bash
.venv/bin/pip install -r skills/news-aggregator-skill/requirements.txt
```

## 输入和输出

**输入**

- 一个带 YAML frontmatter 的请求文件
- 支持字段：`profile`、`sources`、`keyword`、`limit`、`deep`、`title`

**输出**

- `content-production/inbox/YYYYMMDD-<slug>-news-report.md`
- `content-production/inbox/raw/news/YYYY-MM-DD/<slug>.json`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill news-collect \
  --input content-production/inbox/20260407-harness-engineering-海外补充扫描-request.md
```

### 常见下游衔接

- 人工选题
- `topic-research`
- 后续再转成阶段 1 的 brief

## 什么时候用

- 你需要做一轮“今天值得关注什么”的宽扫描
- 你想把零散资讯变成可复盘的日报式报告
- 你准备从资讯里筛一个值得深挖的选题

## 注意事项

- 本 skill 负责“广度扫描”，不负责深度研究
- 输出 contract 以本仓库为准，不要把结果直接写回 vendor 目录
- 如果要继续深挖，下一步应该走 `topic-research`

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [news-aggregator-skill](../news-aggregator-skill/README.md)
