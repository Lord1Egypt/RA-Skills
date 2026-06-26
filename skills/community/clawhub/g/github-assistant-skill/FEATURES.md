# GitHub Assistant Skill 功能清单

> 本文档列出 GitHub Assistant Skill 支持的所有细分功能和操作命令。

---

## 📋 功能概览

| 类别 | 功能数量 | 脚本文件 |
|------|----------|----------|
| Trending 查看 | 3 | `github_trending.py` |
| 项目搜索 | 4 | `github_search.py` |
| 仓库操作 | 9 | `github_operations.py` |
| Issues 管理 | 8 | `github_operations.py` |
| Pull Requests | 9 | `github_operations.py` |
| 代码内容 | 5 | `github_operations.py` |
| 分支管理 | 3 | `github_operations.py` |
| Releases 管理 | 4 | `github_operations.py` |
| Actions 操作 | 4 | `github_operations.py` |
| 用户操作 | 8 | `github_operations.py` |
| 通知管理 | 4 | `github_operations.py` |
| 组织操作 | 4 | `github_operations.py` |
| 评论管理 | 2 | `github_operations.py` |
| 浏览器自动化 | 15+ | `github_browser_ops.py` |
| 账户管理 | 4 | `github_login.py` |

---

## 🔥 1. Trending 查看

> 脚本：`github_trending.py`  
> 权限：无需登录  
> 模式：浏览器自动化（获取完整数据）

| 命令 | 说明 | 示例 |
|------|------|------|
| `daily` | 查看今日热门项目 | `python3 github_trending.py daily "" browser` |
| `weekly` | 查看本周热门项目 | `python3 github_trending.py weekly python browser` |
| `monthly` | 查看本月热门项目 | `python3 github_trending.py monthly "" browser` |

**参数说明：**
- 第一个参数：时间范围（`daily`/`weekly`/`monthly`）
- 第二个参数：编程语言筛选（空字符串 `""` 表示全语言）
- 第三个参数：模式（固定为 `browser`）

**返回数据：**
- 仓库名称和链接
- 项目描述
- 编程语言
- Star/Fork 数量
- 贡献者列表
- 期间新增 Star 数

---

## 🔍 2. 项目搜索

> 脚本：`github_search.py`  
> 权限：无需登录（有 Token 可提高速率限制）

| 命令 | 说明 | 示例 |
|------|------|------|
| `repos` | 搜索仓库 | `python3 github_search.py repos "机器学习" 10` |
| `repos` | 高级搜索 | `python3 github_search.py repos "stars:>10000 language:python"` |
| `users` | 搜索用户 | `python3 github_search.py users "torvalds"` |
| `info` | 查看仓库详情 | `python3 github_search.py info microsoft vscode` |

**搜索语法支持：**
- `stars:>1000` - Star 数筛选
- `language:python` - 语言筛选
- `topic:ai` - 主题筛选
- `created:>2024-01-01` - 创建时间筛选
- `fork:true` - 包含 Fork

---

## ⭐ 3. 仓库操作

> 脚本：`github_operations.py`  
> 权限：需要 Token 登录

| 命令 | 说明 | 示例 |
|------|------|------|
| `star` | Star 仓库 | `python3 github_operations.py star microsoft/vscode` |
| `unstar` | 取消 Star | `python3 github_operations.py unstar owner/repo` |
| `fork` | Fork 仓库 | `python3 github_operations.py fork owner/repo` |
| `watch` | Watch 仓库 | `python3 github_operations.py watch owner/repo` |
| `unwatch` | 取消 Watch | `python3 github_operations.py unwatch owner/repo` |
| `info` | 获取仓库信息 | `python3 github_operations.py info owner/repo` |
| `starred` | 列出已 Star 仓库 | `python3 github_operations.py starred` |
| `forks` | 列出 Forks | `python3 github_operations.py forks owner/repo` |
| `stargazers` | 列出 Stargazers | `python3 github_operations.py stargazers owner/repo` |
| `create-repo` | 创建新仓库 | `python3 github_operations.py create-repo my-repo "描述"` |

---

## 🐛 4. Issues 管理

> 脚本：`github_operations.py`  
> 权限：需要 Token（Issues Read/Write）

| 命令 | 说明 | 示例 |
|------|------|------|
| `issues` | 列出 Issues | `python3 github_operations.py issues owner/repo open` |
| `issue` | 获取指定 Issue | `python3 github_operations.py issue owner/repo 1234` |
| `create-issue` | 创建 Issue | `python3 github_operations.py create-issue owner/repo "标题" "描述"` |
| `close-issue` | 关闭 Issue | `python3 github_operations.py close-issue owner/repo 1234` |
| `reopen-issue` | 重新打开 Issue | `python3 github_operations.py reopen-issue owner/repo 1234` |
| `labels` | 列出 Issue 标签 | `python3 github_operations.py labels owner/repo 1234` |
| `add-labels` | 添加标签 | `python3 github_operations.py add-labels owner/repo 1234 bug priority` |
| `lock-issue` | 锁定 Issue | `python3 github_operations.py lock-issue owner/repo 1234 "off-topic"` |
| `unlock-issue` | 解锁 Issue | `python3 github_operations.py unlock-issue owner/repo 1234` |

**Issue 状态：**
- `open` - 开放状态
- `closed` - 已关闭
- `all` - 全部

**锁定原因：**
- `off-topic` - 离题
- `too heated` - 过于激烈
- `resolved` - 已解决
- `spam` - 垃圾信息

---

## 🔀 5. Pull Requests 操作

> 脚本：`github_operations.py`  
> 权限：需要 Token（Pull requests Read/Write）

| 命令 | 说明 | 示例 |
|------|------|------|
| `prs` | 列出 PRs | `python3 github_operations.py prs owner/repo open` |
| `pr` | 获取指定 PR | `python3 github_operations.py pr owner/repo 1234` |
| `create-pr` | 创建 PR | `python3 github_operations.py create-pr owner/repo "标题" feature-branch main` |
| `close-pr` | 关闭 PR | `python3 github_operations.py close-pr owner/repo 1234` |
| `reopen-pr` | 重新打开 PR | `python3 github_operations.py reopen-pr owner/repo 1234` |
| `merge-pr` | 合并 PR | `python3 github_operations.py merge-pr owner/repo 1234 "合并标题"` |
| `approve-pr` | 批准 PR | `python3 github_operations.py approve-pr owner/repo 1234 "LGTM!"` |
| `pr-files` | PR 修改的文件 | `python3 github_operations.py pr-files owner/repo 1234` |
| `pr-commits` | PR 的提交记录 | `python3 github_operations.py pr-commits owner/repo 1234` |
| `pr-reviews` | PR 审查记录 | `python3 github_operations.py pr-reviews owner/repo 1234` |

---

## 📄 6. 代码内容操作

> 脚本：`github_operations.py`  
> 权限：需要 Token（Contents Read/Write）

| 命令 | 说明 | 示例 |
|------|------|------|
| `file` | 获取文件内容 | `python3 github_operations.py file owner/repo path/to/file.py` |
| `readme` | 获取 README | `python3 github_operations.py readme owner/repo` |
| `ls` | 列出目录内容 | `python3 github_operations.py ls owner/repo src` |
| `create-file` | 创建文件 | `python3 github_operations.py create-file owner/repo "test.py" "提交信息" "内容"` |
| `update-file` | 更新文件 | `python3 github_operations.py update-file owner/repo "test.py" "提交信息" "内容" <sha>` |

**可选参数：**
- 分支/标签：在命令末尾指定，如 `python3 github_operations.py file owner/repo path/file.py main`

---

## 🌿 7. 分支管理

> 脚本：`github_operations.py`  
> 权限：需要 Token（Contents Write）

| 命令 | 说明 | 示例 |
|------|------|------|
| `branches` | 列出分支 | `python3 github_operations.py branches owner/repo` |
| `branch` | 获取分支信息 | `python3 github_operations.py branch owner/repo main` |
| `create-branch` | 创建分支 | `python3 github_operations.py create-branch owner/repo new-branch main` |

---

## 🚀 8. Releases 管理

> 脚本：`github_operations.py`  
> 权限：需要 Token（Contents Write）

| 命令 | 说明 | 示例 |
|------|------|------|
| `releases` | 列出 Releases | `python3 github_operations.py releases owner/repo` |
| `release` | 获取指定 Release | `python3 github_operations.py release owner/repo 123456` |
| `create-release` | 创建 Release | `python3 github_operations.py create-release owner/repo v1.0.0 "名称" "说明"` |
| `update-release` | 更新 Release | `python3 github_operations.py update-release owner/repo 123456 "新名称" "新说明"` |

---

## ⚡ 9. Actions 操作

> 脚本：`github_operations.py`  
> 权限：需要 Token（Actions Read, Contents Write）

| 命令 | 说明 | 示例 |
|------|------|------|
| `workflows` | 列出工作流运行 | `python3 github_operations.py workflows owner/repo` |
| `workflow` | 获取指定工作流 | `python3 github_operations.py workflow owner/repo ci.yml` |
| `trigger-workflow` | 触发工作流 | `python3 github_operations.py trigger-workflow owner/repo ci.yml main` |
| `cancel-workflow` | 取消工作流 | `python3 github_operations.py cancel-workflow owner/repo <run_id>` |
| `rerun-workflow` | 重新运行工作流 | `python3 github_operations.py rerun-workflow owner/repo <run_id>` |

---

## 👤 10. 用户操作

> 脚本：`github_operations.py`  
> 权限：需要 Token

| 命令 | 说明 | 示例 |
|------|------|------|
| `user` | 当前登录用户信息 | `python3 github_operations.py user` |
| `user` | 指定用户信息 | `python3 github_operations.py user torvalds` |
| `my-repos` | 当前用户的仓库 | `python3 github_operations.py my-repos` |
| `user-repos` | 指定用户的仓库 | `python3 github_operations.py user-repos torvalds` |
| `followers` | 当前用户粉丝 | `python3 github_operations.py followers` |
| `following` | 当前用户关注的人 | `python3 github_operations.py following` |
| `follow` | 关注用户 | `python3 github_operations.py follow username` |
| `unfollow` | 取消关注 | `python3 github_operations.py unfollow username` |

---

## 🔔 11. 通知管理

> 脚本：`github_operations.py`  
> 权限：需要 Token（Notifications）

| 命令 | 说明 | 示例 |
|------|------|------|
| `notifications` | 列出未读通知 | `python3 github_operations.py notifications` |
| `notifications --all` | 列出所有通知 | `python3 github_operations.py notifications --all` |
| `repo-notifications` | 仓库通知 | `python3 github_operations.py repo-notifications owner/repo` |
| `mark-read` | 标记已读 | `python3 github_operations.py mark-read <thread_id>` |

---

## 🏢 12. 组织操作

> 脚本：`github_operations.py`  
> 权限：需要 Token（read:org）

| 命令 | 说明 | 示例 |
|------|------|------|
| `orgs` | 列出当前用户的组织 | `python3 github_operations.py orgs` |
| `org` | 获取组织信息 | `python3 github_operations.py org github` |
| `org-repos` | 列出组织仓库 | `python3 github_operations.py org-repos github` |
| `org-members` | 列出组织成员 | `python3 github_operations.py org-members github` |

---

## 💬 13. 评论管理

> 脚本：`github_operations.py`  
> 权限：需要 Token（Issues Write 或 Pull requests Write）

| 命令 | 说明 | 示例 |
|------|------|------|
| `comments` | 列出评论 | `python3 github_operations.py comments owner/repo 1234` |
| `comment` | 创建评论 | `python3 github_operations.py comment owner/repo 1234 "评论内容"` |

---

## 🌐 14. 浏览器自动化操作

> 脚本：`github_browser_ops.py`  
> 权限：需要浏览器登录  
> 说明：这些功能 GitHub REST API 不支持

### 用户相关（API 不支持）

| 命令 | 说明 | 示例 |
|------|------|------|
| `contributions` | 查看贡献图 | `python3 github_browser_ops.py contributions torvalds` |
| `activity` | 查看活动时间线 | `python3 github_browser_ops.py activity torvalds` |
| `stars` | 查看 Star 列表页面 | `python3 github_browser_ops.py stars torvalds` |
| `followers` | 查看粉丝列表页面 | `python3 github_browser_ops.py followers torvalds` |
| `sponsors` | 查看赞助页面 | `python3 github_browser_ops.py sponsors torvalds` |

### 仓库 Insights（需要 push 权限）

| 命令 | 说明 | 示例 |
|------|------|------|
| `insights` | Pulse 概览 | `python3 github_browser_ops.py insights owner/repo` |
| `traffic` | 流量统计 | `python3 github_browser_ops.py traffic owner/repo` |
| `network` | Fork 网络图 | `python3 github_browser_ops.py network owner/repo` |
| `dependents` | 依赖者列表 | `python3 github_browser_ops.py dependents owner/repo` |

### 代码相关

| 命令 | 说明 | 示例 |
|------|------|------|
| `blame` | Git Blame | `python3 github_browser_ops.py blame owner/repo path/file.py` |
| `history` | 文件提交历史 | `python3 github_browser_ops.py history owner/repo path/file.py` |
| `compare` | 分支比较 | `python3 github_browser_ops.py compare owner/repo main dev` |
| `codesearch` | 仓库内代码搜索 | `python3 github_browser_ops.py codesearch owner/repo "keyword"` |

### 设置页面

| 命令 | 说明 | 示例 |
|------|------|------|
| `settings` | 用户设置 | `python3 github_browser_ops.py settings` |
| `settings` | 仓库设置 | `python3 github_browser_ops.py settings owner/repo` |

### 导航

| 命令 | 说明 | 示例 |
|------|------|------|
| `notifications` | 通知页面 | `python3 github_browser_ops.py notifications` |
| `explore` | Explore 页面 | `python3 github_browser_ops.py explore` |
| `marketplace` | Marketplace | `python3 github_browser_ops.py marketplace` |
| `search` | GitHub 搜索 | `python3 github_browser_ops.py search "query"` |
| `goto` | 导航到指定 URL | `python3 github_browser_ops.py goto "https://..."` |

### 浏览器控制

| 命令 | 说明 | 示例 |
|------|------|------|
| `close` | 关闭浏览器 | `python3 github_browser_ops.py close` |

---

## 🔐 15. 账户管理

> 脚本：`github_login.py`

| 命令 | 说明 | 示例 |
|------|------|------|
| `browser` | 浏览器手动登录 | `python3 github_login.py browser` |
| `token` | Token 登录 | `python3 github_login.py token <YOUR_TOKEN>` |
| `check` | 检查登录状态 | `python3 github_login.py check` |
| `logout` | 登出 | `python3 github_login.py logout` |

---

## 📊 权限速查表

### Fine-grained PAT 权限配置

| 功能类别 | 所需权限 | 权限级别 |
|----------|----------|----------|
| Trending 查看 | 无需登录 | - |
| 项目搜索 | 无需登录 | - |
| Star/Unstar | Metadata | Read |
| Fork | Contents | Write |
| Watch/Unwatch | Metadata | Read |
| Issues 读取 | Issues | Read |
| Issues 写入 | Issues | Write |
| PR 读取 | Pull requests | Read |
| PR 写入 | Pull requests | Write |
| 文件读取 | Contents | Read |
| 文件写入 | Contents | Write |
| Actions 查看 | Actions | Read |
| Actions 触发 | Contents | Write |
| 通知 | Notifications | Read |
| 组织信息 | Organization members | Read |

### Classic PAT Scopes

| Scope | 用途 |
|-------|------|
| `repo` | 完全控制私有仓库 |
| `public_repo` | 访问公共仓库 |
| `workflow` | 更新 GitHub Actions 工作流 |
| `read:org` | 读取组织成员信息 |
| `read:user` | 读取用户资料 |
| `notifications` | 访问通知 |

---

## 🛠️ 其他命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `commits` | 查看提交历史 | `python3 github_operations.py commits owner/repo` |
| `commits` | 查看文件提交历史 | `python3 github_operations.py commits owner/repo path/file.py` |
| `rate-limit` | 查看 API 限流 | `python3 github_operations.py rate-limit` |
| `check` | 检查登录状态 | `python3 github_operations.py check` |

---

## 📁 文件结构

```
github-assistant/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 项目文档
├── FEATURES.md                 # 功能清单（本文件）
├── LICENSE                     # MIT 许可证
├── .gitignore                  # Git 忽略配置
├── scripts/
│   ├── config.py               # 集中配置管理
│   ├── github_login.py         # 登录管理
│   ├── github_trending.py      # Trending 抓取
│   ├── github_search.py        # 项目搜索
│   ├── github_operations.py    # 完整操作集
│   ├── github_browser_ops.py   # 浏览器自动化
│   ├── install_browser.py      # 浏览器安装脚本
│   └── requirements.txt        # Python 依赖
└── references/
    └── github_api_endpoints.md # API 端点参考

~/.github-assistant/            # 用户数据目录
├── github_token.txt            # Token 存储
├── github_auth.json            # 浏览器会话
└── browser_data/               # 浏览器数据
```

---

## 📝 版本信息

- **版本**: 1.0.0
- **Python 要求**: >= 3.8
- **主要依赖**: requests>=2.28.0, playwright>=1.40.0
- **许可证**: MIT