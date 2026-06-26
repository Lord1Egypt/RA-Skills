# pr-comment-fix

根据 **GitCode PR 上未解决的行评**（diff comment）修改本地代码；可选在讨论下回复、更新解决状态。

## 前置

- [GitCode 个人访问令牌](https://gitcode.com/setting/token-classic)，并设置环境变量：

  ```bash
  set GITCODE_TOKEN=你的令牌
  ```

- Python 3.7+（仅标准库）。

## 一步：拉取上下文

**只支持 GitCode PR 页面链接**（`--pr-url`），不支持单独传 owner/repo/编号：

```bash
python scripts/pr_comment_fix_tool.py fetch -o pr_comment_fix_context.json --pr-url "https://gitcode.com/Ascend/mindsdk-referenceapps/pull/903"
```

- 请从浏览器复制 **PR 所在仓库** 的完整 URL（fork 场景下 PR 通常在上游仓库页面）。

## 交给 AI / 本地修改

打开 `pr_comment_fix_context.json`：查看 `unresolved_diff_comments`（每条有 `seq`、`discussion_id`、`diff_file`、`body`）。  
按 `by_file` 从文件**后部往前**改，避免行号漂移；**未确认前不要改代码**。

## 可选：回复讨论

```bash
python scripts/pr_comment_fix_tool.py reply -c pr_comment_fix_context.json --seq 1 --body "已按建议调整 xxx。"
```

## 可选：标为已解决

```bash
python scripts/pr_comment_fix_tool.py resolve -c pr_comment_fix_context.json --seq 1 --resolved 1
```

`--resolved 0` 表示未解决。

## 详细流程

见同目录 **[SKILL.md](SKILL.md)**。
