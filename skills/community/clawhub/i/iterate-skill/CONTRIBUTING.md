# Contributing to iterate-skill

感谢你对 iterate-skill 感兴趣！欢迎提交 Issue、PR 和改进建议。

---

## 开发环境

本项目校验脚本使用 Python 3.10+：

```bash
cd scripts
pip install -r requirements.txt
```

---

## 提交 Issue

- 描述你使用的工具（Trae / Claude Code / Cursor / Generic）。
- 提供最小可复现的 `iterate.config.yaml`（可替换敏感信息）。
- 说明期望行为与实际行为。

---

## 提交 Pull Request

1. Fork 本仓库。
2. 创建功能分支：`git checkout -b feat/your-feature` 或 `fix/your-bug`。
3. 提交改动，遵循 [Conventional Commits](https://www.conventionalcommits.org/)：
   - `feat:` 新功能
   - `fix:` 修复
   - `docs:` 文档
   - `test:` 测试
   - `refactor:` 重构
   - `chore:` 杂项
4. 确保本地校验通过（与 CI 的 Python job 等价，含钉住版本的 ruff）：

   ```bash
   ./scripts/check.sh
   ```

5. 推送分支并创建 Pull Request。

---

## 推送前门禁（pre-push）

main 已两次仅因 `ruff check` 未提前运行而变红。仓库附带 `.githooks/pre-push`：
推送到 `main`/`master` 前执行 `./scripts/check.sh --lint-only`，不通过就拒绝推送。

git 不会自动加载仓库内的 hooks 目录，需自行安装一次：

```bash
cp .githooks/pre-push .git/hooks/pre-push
```

确知要绕过时（CI 仍会跑同一道门）：`git push --no-verify`，或 `SKIP_PREPUSH=1 git push`。
门禁要求本地 ruff 与 `.github/workflows/ci.yml` 中的 pin 完全一致，否则报错并给出安装命令。

## 提交前门禁（pre-commit：禁止未声明的删除）

2026-10-11 出过一次事故：共享主 worktree 的工作区被回退到旧内容，27 个跟踪文件在盘上
消失，而 HEAD 仍含着它们——`git status` 一片 ` D`，没有任何提交发现。那种状态下任何一次
`git add -A && git commit` 都会把这些**丢失**记成**有意删除**，而 CI 只会验证删除之后的树
是否自洽，永远绿。仓库附带 `.githooks/pre-commit` 拦两种形状：

- 索引里有删除，但没被声明；
- 跟踪文件在 worktree 里缺席、却没被暂存成删除（树与自身 HEAD 不一致——正是上面那种）。

安装方式与 pre-push 相同（git 不自动加载仓库内 hooks 目录；装在 common dir 上对本仓所有
worktree 生效）：

```bash
cp .githooks/pre-commit "$(git rev-parse --git-common-dir)/hooks/pre-commit"
```

误删就恢复：`git checkout HEAD --pathspec-from-file=<路径清单>`。确是要删就点名，别用
`--no-verify`（那会把删除整个藏起来）：

```bash
ALLOW_DELETIONS="path/one,path/two" git commit …
```

对照实测（一次性 detached worktree，跑完即删）：暂存删除被拒且点名路径；
`ALLOW_DELETIONS` 点名后放行；"文件在盘上消失但未暂存"这一形状被拒；恢复同一文件后同一
提交照常通过；普通新增提交不受影响。

---

## 文档规范

- `SKILL.md` 保持中英双语结构。
- 新增配置项必须同步更新：
  - `config/iterate.config.yaml`
  - `config/config.schema.json`
  - `README.md` 配置表格
  - `SKILL.md` 配置表格与流程说明
  - 相关 `examples/*.md`
- 新增验证命令安全规则时，同步更新 `validation.command_whitelist` 默认值与 `scripts/validate.py`。

---

## 代码规范

- Python 函数长度尽量不超过 80 行。
- 优先使用 early return 减少嵌套。
- 禁止空 catch 块。
- 新增第三方依赖必须为 MIT / Apache-2.0 / BSD 等宽松许可证，并在 `scripts/requirements.txt` 中声明精确版本。
- 所有新增脚本/测试必须附带测试用例。

---

## 许可证

通过提交 PR，你同意你的贡献采用本项目的 [MIT 许可证](./LICENSE)。
