# 镜像清理策略

## Harbor 保留策略（Retention）

Harbor 内置保留策略功能（需开启 `retention` 插件）。

### 保留规则结构

```json
{
  "rules": [
    {
      "id": 1,
      "priority": 0,
      "disabled": false,
      "action": "retain",
      "tag_selectors": [
        {
          "kind": "doublestar",
          "pattern": "**",
          "extras": {"respect": true}
        }
      ],
      "scope_selectors": {
        "repository": [
          {"kind": "doublestar", "pattern": "my-app/**"}
        ]
      }
    }
  ],
  "trigger": {
    "kind": "schedule",
    "settings": {"cron": "0 0 3 * * *"}  // 每天凌晨3点
  },
  "policy": "latestPushedKinds"
}
```

### 常用保留规则模板

```yaml
# 保留最近5个标签（按push时间）
rule:
  action: retain
  tag_selectors:
    - kind: latestPushedKinds
      count: 5
  scope_selectors:
    repository:
      - pattern: "**"

# 删除30天前的标签
rule:
  action: retain
  tag_selectors:
    - kind: latestPushedKinds
      count: 0  # 0 = 不保留，按时间筛选
      since: 30  # days
  scope_selectors:
    repository:
      - pattern: "**"

# 保留特定前缀标签（release-*, stable-*）
rule:
  action: retain
  tag_selectors:
    - kind: regexp
      pattern: "^(release-|stable-).*"
  scope_selectors:
    repository:
      - pattern: "**"

# 删除漏洞超标的镜像
rule:
  action: retain
  tag_selectors:
    - kind: vulnSeverity
      resolution: ""
      tag_selectors:
        - kind: latestPushedKinds
          count: 1
  scope_selectors:
    repository:
      - pattern: "**"
```

### 标签选择器类型

| Kind | 说明 | 参数 |
|------|------|------|
| `latestPushedKinds` | 最近推送的 N 个标签 | `count: N` |
| `latestPulledKinds` | 最近拉取的 N 个标签 | `count: N` |
| `vulnSeverity` | 按漏洞严重等级 | `severity: high` |
| `tagwithregex` | 按正则匹配标签名 | `pattern: "^v\d+"` |
| `doublestar` | doublestar 路径匹配 | `pattern: "**"` |
| `dayssincelastpull` | N 天未拉取的标签 | `count: 30` |
| `always` | 匹配所有 | - |

## Python 清理演练脚本逻辑

```python
# scripts/cleanup_dryrun.py 的核心逻辑

def eval_rule(artifacts, rule, dry_run=True):
    """
    评估清理规则，返回应删除的镜像列表
    """
    matched = []
    for artifact in artifacts:
        tags = artifact.get('tags', [])
        # 按 push 时间排序（Harbor API 返回已排序）
        tags_sorted = sorted(tags, key=lambda t: t.get('push_time', ''), reverse=True)

        if rule['kind'] == 'latestPushedKinds':
            keep_count = rule.get('count', 0)
            if len(tags_sorted) > keep_count:
                to_delete = tags_sorted[keep_count:]
                matched.extend(to_delete)

        elif rule['kind'] == 'dayssincepush':
            threshold = rule.get('days', 30)
            cutoff = datetime.now() - timedelta(days=threshold)
            for tag in tags_sorted:
                push_time = parse_time(tag['push_time'])
                if push_time < cutoff:
                    matched.append(tag)

        elif rule['kind'] == 'tagwithregex':
            pattern = re.compile(rule['pattern'])
            for tag in tags_sorted:
                if not pattern.match(tag['name']):
                    matched.append(tag)

    # 去重
    seen = set()
    unique = []
    for t in matched:
        key = (t['repository'], t['name'])
        if key not in seen:
            seen.add(key)
            unique.append(t)

    return unique
```

## 推荐清理策略配置

```yaml
# 生产环境推荐策略
project: my-app
policy:
  name: "生产环境镜像保留策略"
  trigger: "schedule"  # cron: "0 0 3 * * *" 每天凌晨3点
  rules:
    # 规则1：保留最近5个 release 标签
    - name: keep-release-tags
      action: retain
      tag_selectors:
        - kind: latestPushedKinds
          count: 5
      exclude:
        tags: ["latest", "stable"]
      scope:
        repository: "**"
        tag: "release-*"

    # 规则2：保留所有 stable 标签
    - name: keep-stable
      action: retain
      tag_selectors:
        - kind: always
      scope:
        repository: "**"
        tag: "stable"

    # 规则3：删除30天前未使用的快照
    - name: cleanup-old-snapshots
      action: delete
      tag_selectors:
        - kind: dayssincepull
          count: 30
      scope:
        repository: "**"
        tag: "snap-*"

    # 规则4：删除高危漏洞镜像
    - name: reject-high-vuln
      action: delete
      tag_selectors:
        - kind: vulnSeverity
          severity: high
      scope:
        repository: "**"
        tag: "**"
```

## 清理操作安全检查清单

- [ ] 确认 `exclude` 标签列表完整（`latest`、`stable`、`release-*` 等必须保留）
- [ ] 演练模式（`dry_run=True`）先跑一遍，确认无误再执行
- [ ] 清理后确认 GC 已安排（镜像删除 ≠ 磁盘释放）
- [ ] 保留足够回滚窗口（清理后 7 天内可手动恢复）
- [ ] 通知相关团队镜像清理时间窗口
