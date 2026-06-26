# 飞书同步指南

## 创建会议纪要文档

```bash
python3 .claude/skills/feishu-doc/scripts/doc_ctl.py create "会议纪要 - {{title}} - {{date}}" --content "<markdown content>"
```

## 追加内容

```bash
python3 .claude/skills/feishu-doc/scripts/doc_ctl.py append <doc_id> "追加内容"
```

## 替换章节

```bash
python3 .claude/skills/feishu-doc/scripts/doc_ctl.py replace <doc_id> --section "决议事项" "## 决议事项\n新内容"
```

## 分享与权限

- `--share ou_xxxxx`：分享给指定用户
- `--owner ou_xxxxx`：转移文档所有权
- `--folder fldcnXXX`：指定目标文件夹

## 注意事项

- 飞书文档使用 markdown 风格标题：`#` → H1, `##` → H2
- 表格在飞书中会自动渲染
- 创建后返回可点击的飞书链接，记入纪要末尾
