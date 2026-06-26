# Quick Ref — GitHub Bug Report

## 提交前检查清单

- [ ] 搜一下是否有人报过同样的 bug
- [ ] 确认是真实 bug 而不是配置错误
- [ ] 准备好复现步骤（编号 1/2/3）
- [ ] 准备好预期 vs 实际结果
- [ ] 版本号准备好（查 openclaw --version）

## curl 快速命令

### 搜索现有 issue

```bash
curl -s "https://api.github.com/search/issues?q=关键词+repo:openclaw/openclaw&per_page=5" \
  -H "Authorization: token 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"
```

### 查看 issue 详情

```bash
curl -s "https://api.github.com/repos/openclaw/openclaw/issues/66057" \
  -H "Authorization: token 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"
```

### 创建 issue

```bash
curl -s -X POST \
  -H "Authorization: token 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" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/vnd.github+json" \
  https://api.github.com/repos/openclaw/openclaw/issues \
  -d '{"title":"[v1.x.x] Bug标题","body":"内容"}'
```

### 更新 issue

```bash
curl -s -X PATCH \
  -H "Authorization: token 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" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/vnd.github+json" \
  https://api.github.com/repos/openclaw/openclaw/issues/<number> \
  -d '{"title":"新标题","body":"新内容"}'
```

## 当前已提交的 issue

| # | 标题 | 状态 |
|---|------|------|
| 66057 | [v1.x.x] Compaction checkpoint .jsonl files never cleaned up | Open |
| 66058 | [v1.x.x] memoryFlush + softThresholdTokens=4000 causes infinite compaction loop | Open |
