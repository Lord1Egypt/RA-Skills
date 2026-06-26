# git-helper

## 功能说明
这个 skill 旨在为您提供全面的 Git 命令解析和工作流指导。它可以帮助您：
- 理解特定 Git 命令的作用（如 `git rebase -i`, `git fetch` vs `git pull` 等）。
- 根据任务目标提供确切的 Git 操作步骤（如“撤销上一次提交但保留代码”、“合并最近的三次提交”等）。
- 提供应对复杂情况的最佳实践（如处理合并冲突、使用 `git reflog` 恢复误删代码）。
- 对破坏性操作（如 `git reset --hard`、`git push --force`）进行安全警告并提供更安全的替代方案。

支持中英文双语输出，会根据您的提问语言自动适配。

## 使用场景
当您在进行版本控制时遇到命令遗忘、执行错误需要挽救、或需要理解复杂的 Git 工作流时，直接向 Agent 描述您的需求或疑问即可。

## 提问示例

**中文模式：**
```text
怎么撤销上一次的 commit，但是保留我修改的代码？
```
```text
我不小心 git reset --hard 删除了我刚写的一大堆代码，还能救回来吗？
```

**英文模式：**
```text
What does git rebase do?
```
```text
How do I squash my last 3 commits into one before making a pull request?
```