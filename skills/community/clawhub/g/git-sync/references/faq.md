# git-sync 常见问题

---

## 同步与推送

### Q1: GitHub 推送失败（443 超时 / Permission denied）

检查网络代理或 SSH key 配置，或手动推送：

```bash
cd WORK_REPO
git push origin main
```

如果 443 超时持续出现，尝试：
- 切换到 SSH 协议（`[email-redacted]:...` 替代 `https://github.com/...`）
- 检查系统代理配置是否干扰 HTTPS

### Q2: 想保留历史 commit 而非 amend？

脚本已改为普通 `git commit`，不再使用 `--amend`。每次同步都会产生独立 commit。

### Q3: Gitee push 需要密码但 PAT 仅限 API？

这是已知限制：Gitee 的 PAT（Personal Access Token）通常仅限 API 操作，git push 需要登录密码或 SSH key。

解决方案：
1. 使用 SSH 方式配置 Gitee remote（推荐）
2. 或在推送时手动输入密码（交互式场景）

### Q4: 双平台只有一个成功怎么办？

脚本会分别记录每个平台的三单一致状态：
- 仅 Gitee 成功 → `gitee_ok=true`, `github_ok=false`, `uploaded=false`
  - 即：Gitee 已三单一致，GitHub 尚未一致
- 可稍后对失败的平台单独重试
- 重试成功 → 对应平台的 `*_ok=true`，`uploaded` 自动更新

---

## ZIP 打包

### Q5: 本地有 html 文件被混入 ZIP？

先删除临时文件再执行同步：

```bash
rm -f ~/.workbuddy/skills/<skill-name>/*.html
```

或在 skill 目录下添加 `.gitignore` 规则排除 html。

### Q6: ZIP 包太大怎么办？

检查是否有意外包含的大文件（数据集、模型、图片等）：

```bash
# 查看 ZIP 内容大小
unzip -l ~/.workbuddy/skills/.dist/<skill-name>-v*.zip | sort -rn -k4 | head -20
```

常见的大文件来源：
- `__pycache__/` 缓存目录（应被自动排除）
- `.git/` 版本控制目录（应被自动排除）
- 数据文件或模型权重

### Q7: 如何验证 ZIP 内容是否正确？

```bash
# 解压到临时目录检查
mkdir /tmp/zip-check && cd /tmp/zip-check
unzip ~/.workbuddy/skills/.dist/<skill-name>-v*.zip
find . -type f | head -30
```

---

## 维护清单 (manifest)

### Q8: "NOT_FOUND" 提示是什么意思？

表示要同步的 skill 不在 manifest.json 清单中。此时会询问你三个选项：

| 选项 | 含义 |
|------|------|
| **加入清单** | 将此 skill 注册到 manifest.json，标记 uploaded=false，继续同步 |
| **仅本次同步** | 不更新清单，只执行本次同步操作 |
| **中止** | 取消本次同步 |

建议选择"加入清单"，方便后续版本管理和全量维护。

### Q9: 版本号对比显示"清单 version > 待更新版本"？

这表示清单中记录的版本号比你要同步的版本还高，属于异常情况——**同步前仓库和清单必须一致**，出现这个说明之前的三单一致被破坏了。常见原因包括：
- 手动编辑了 manifest.json 导致版本混乱
- 上次同步后版本号没有正确递增
- 本地改了版本号但没推送（清单比本地高）

处理策略选择：
- **覆盖** — 用待更新版本覆盖清单记录（如果确认清单错了）
- **拉取** — 从仓库获取最新版本号（如果仓库更新过）
- **合并** — 人工确认正确版本
- **中止** — 先调查清楚再执行

### Q10: README.md 和仓库实际内容不一致？

正常情况下不应发生——README.md 由 `sync-readme` 全量生成，永远等于仓库实际内容。

如果发现不一致，运行：

```bash
cd ~/.workbuddy/skills/git-sync/scripts
python manifest.py sync-readme workbuddy-skills
```

---

## 敏感信息过滤

### Q11: 扫描结果误报怎么办？

敏感信息扫描基于正则模式匹配，常见误报包括：

| 误报场景 | 示例 | 处理 |
|---------|------|------|
| 示例邮箱 | `[email-redacted]` 在文档示例中 | 选择"逐项细选"，跳过该条目 |
| 类似 Token 字符串 | UUID 格式的 ID 被 Token 规则命中 | 同上，交互式跳过 |
| 用户名匹配 | 配置中的用户名出现在代码注释中 | 这是 low 级别，可保留 |

对于私有仓库场景，可以直接用 `--skip-scan` 跳过扫描。

⚠️ **安全警告**：私有内容经常被后续镜像、打包分享、或推送到其他 remote（如 GitHub fork、团队成员 clone 后外传）。跳过扫描会削弱安全控制，增加凭证、Token 或其他敏感信息被传播的风险。仅在完全确认无敏感信息时使用 `--skip-scan`。

### Q12: 脱敏后的文件能恢复吗？

- **源文件**：永远不会被更新（脱敏作用于副本）
- **仓库副本**：会被脱敏覆盖；如需恢复，重新执行一次 git-sync 即可从源文件重新同步
- **ZIP 包中的文件**：已脱敏；重新打包即可

---

## 审查规则 (R-01~R-26)

### Q13: 审查 ERROR 会阻止同步吗？

不会。自 v1.8.0 起，审查为**纯警告模式**：

- ERROR/WARN 仅在报告中体现
- 始终返回 exit(0)
- 不阻断、不中止、不强制修复
- 建议逐步优化而非强制一次性通过全部规则

### Q14: 如何单独运行审查？

```bash
# 审查单个 skill
python -m scripts.skill_audit audit ~/.workbuddy/skills/my-skill

# 审查所有 skills
python -m scripts.skill_audit audit-all ~/.workbuddy/skills

# JSON 输出（供脚本解析）
python -m scripts.skill_audit audit ~/.workbuddy/skills/my-skill --json
```
