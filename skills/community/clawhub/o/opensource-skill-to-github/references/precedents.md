# 11 个开源 skill 先例

> 下次开源任意 skill，先读这份 + 同类型先例 memory，30 分钟可走完前 60% 工作量。
> 所有 memory 路径相对 `~/.openclaw/workspace/memory/`。

| Skill | Memory 路径 | 教学价值 |
|---|---|---|
| **workspace-git-setup** | `project_workspace_git_setup_opensource_fork.md` | git 类基础工具，**首个开源副本**，11 条剔除清单源头 |
| **hello-env** | `project_hello_env_opensource_fork.md` | 环境自检，加 4 条 CLI 设计决策 + 跨平台兜底实证 + frontmatter 跨 agent 兼容（v1.0.0→v1.0.2 三版迭代） |
| **token-slim** | `project_token_slim_opensource_fork.md` | Python+LLM，picasso CDN 砍掉改 PyPI/清华/阿里多源 fallback |
| **session-recovery** | `project_session_recovery_opensource_fork.md` | 会话工具，`sign.key` 必删（含内部身份）；v1.0.0 范围只 OpenClaw + Claude Code |
| **rename-session** | `project_rename_session_opensource_fork.md` | CLI 工具，`--lang` 必须 locale 探测**不写死 zh**；DIBP webchat title 与 label 独立存储 |
| **collective-memory** | `project_collective_memory_opensource_fork.md` | multi-agent / multi-workspace 定位（吸引 CC/Cursor 用户）；agents 发现机制 = 显式 > 自动发现 + confirm > 单 agent 跳过 |
| **subagent-timeout-config** | `project_subagent_timeout_config_opensource_fork.md` | OpenClaw 平台原生缺失 UX 工具；profile 命名让用户拍板（quick/normal/patient） |
| **copy-my-profile** | `project_copy_my_profile_opensource_fork.md` | 纯 LLM 工作流 0 脚本（40K）；"vCard for AI assistants" 行业级定位；含 10 大 AI 工具 memory 路径图 + 10 个目标工具导入提示词模板 |
| **agent-team-mesh** | `project_agent_team_mesh_opensource_fork.md` | P2P 网络，XDG 路径，sync 命令 stub 化；**内网+开源双修**（v0.3.0→v0.4.0 真问题先修） |
| **claw-memory-manager** | `project_claw_memory_manager_v110.md` | OpenClaw 原生扩展（dreaming/active-memory）；active-memory 三档预设移植（conservative/balanced/aggressive） |
| **glic-check** | `project_glic_check_opensource_fork.md` | **audit 类**，self-check + 三档样本 → 当场发现工具自身 6 个 gap，全修入 v1.0.1；新增 `grep_antipatterns.sh` 半自动脚本 |

## 关键经验提炼

### 决策类
- **副本 vs 演进**：内网仍有用户 → 副本；只有少量内网细节 → 演进
- **首版号**：clawhub 首发**从 v1.0.0 起**，不沿用 CodeWiz 内网版号
- **suite 类 repo**：成员必须独立发版，README 列 stages 表（含 🚧 占位）

### 改造类
- **CLI 设计**：env vars + flags 双轨；env 加 skill 前缀；用户授权 flag（`--i-am-sure`/`--force`/`--yes`）**不自决**
- **跨平台兜底**：按受众决定深度（OpenClaw-only 可跳过，macOS/Windows Git Bash 必做）
- **locale 探测**：不写死 zh，从 `$LC_ALL`/`$LC_MESSAGES`/`$LANG` 探测

### 平台特性
- **clawhub**：必须绝对路径 + 强制 MIT-0 + 无 visibility（hide/unhide）
- **GitHub 内网**：Basic Auth header 注入（bearer 已不认）+ 502 重试 3-5 次
- **skills.sh**：通过 GitHub repo 自动同步，索引滞后约 24h
- **CodeWiz 敏感部门**：禁止自决加 `--visibility private` 救场；只走非 `--visibility` 让取 Hub 当前值

### 沉淀类
- 每次开源完一个 skill 必沉淀 `memory/project_<slug>_opensource_fork.md`，链式继承
- 通用经验沉淀 `memory/feedback_*.md`：
  - `feedback_opensource_slug_collision_precheck.md`
  - `feedback_new_repo_git_config_first.md`
  - `feedback_self_check_uncovers_tool_gaps.md`
  - `feedback_audit_tool_cross_check_before_release.md`
  - `feedback_opensource_skill_md_author_repo_license.md`
