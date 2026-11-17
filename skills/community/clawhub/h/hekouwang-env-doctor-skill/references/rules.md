# 残留特征规则库 v1.1

> 本文件是体检器的判定依据。**结构固定：目录 → 身份 → 判活法 → 官方处置命令 → 代价**。
> 工具生态每年都在变（nvm→fnm→mise、pip→uv），本库需要跟着更新——**版本号在标题上，更新时改它**。
> ⛔ 所有「处置命令」只写给用户看，体检器**永不代为执行**（见 `safety.md`）。

---

## 〇、三分法（一切判定的总纲）

| 身份 | 定义 | 处置 |
|---|---|---|
| **数据** | 删了找不回来（模型权重、容器卷、项目文件、密钥） | ⛔ 一律不建议删 |
| **缓存** | 删了会自动重建，代价是时间和流量 | 🔶 空间紧张再清，且必须走官方命令 |
| **残留** | 属于用户**已经不用**的工具 | ✅ 唯一可放心建议清理的一类 |

**判定顺序**：先问「删了能不能自己回来」（不能→数据），再问「生成它的工具还在用吗」（不用了→残留）。

---

## 一、活跃 vs 残留：四信号判定法 ⭐ 本 skill 的差异化核心

竞品只看体积；本器看**身份**。对每个版本管理器，扫描器（`scan.sh` 的 MANAGERS / RUNTIME 两节）给出四个信号：

| 信号 | 含义 | 权重 |
|---|---|---|
| `shell_loaded` | shell 配置里是否真的加载它（**注释行不算**） | 高 |
| `cmd_in_path` | 命令是否还在 PATH 里 | 高 |
| `RUNTIME.owner` | 运行时（node/python…）实际由谁提供 | **最高** |
| `last_modified` | 目录最后改动时间 | 中 |

**判定表**：

| shell_loaded | cmd_in_path | 是运行时提供者 | 判定 |
|---|---|---|---|
| yes | yes | 是 | **活跃** —— 别动 |
| no | no | 否 | **残留** ✅ 可建议清理 |
| yes | yes | 否 | **闲置/冲突** —— 装着也加载了，但没在干活；提示用户可能存在多管理器冲突 |
| 其余组合 | | | **不确定** —— 如实标注，不猜（见 safety.md 第 3 条） |

> `last_modified` 只做佐证不做定论：超过 12 个月没改动 + 前三个信号都指向残留 = 证据链完整，可在报告里直接引用（例：「最后改动 2024-07，已 2 年未动」）。

**同版本重复检测**：若两个管理器各自装了同一个版本号（如 nvm 和 fnm 都有 v16.20.2），单独列一条提示——这是最典型的「换工具没卸旧的」痕迹。

---

## 二、版本管理器（最常见的残留大户）

| 工具 | 目录 | 加载特征 | 官方卸载 | 只清缓存 |
|---|---|---|---|---|
| **nvm** | `~/.nvm` | `NVM_DIR` / `nvm.sh` | `rm -rf "$NVM_DIR"` + 删 shell 里 NVM_DIR / nvm.sh / bash_completion 三行（官方 README「Manual Uninstall」） | `nvm cache clear` |
| **fnm** | `~/.local/share/fnm` | `fnm env` | 删目录 + 移除 `fnm env` 初始化行 | — |
| **volta** | `~/.volta` | `VOLTA_HOME` | 删目录 + 移除 PATH 行 | — |
| **pyenv** | `~/.pyenv` | `PYENV_ROOT` / `pyenv init` | 删目录 + 移除 init 行 | — |
| **rbenv** | `~/.rbenv` | `RBENV_ROOT` / `rbenv init` | 删目录 + 移除 init 行 | — |
| **rvm** | `~/.rvm` | `rvm/scripts` | `rvm implode`（官方自带卸载子命令） | — |
| **asdf** | `~/.asdf` | `asdf.sh` | 删目录 + 移除 source 行 | — |
| **mise** | `~/.local/share/mise` | `mise activate` | `mise implode`（官方自带） | `mise cache clear` |
| **sdkman** | `~/.sdkman` | `SDKMAN_DIR` | 删目录 + 移除 init 行 | — |
| **conda** | `~/miniforge3` `~/anaconda3` `~/miniconda3` | `conda initialize` | `conda init --reverse` 后删目录 | `conda clean --all` |

⚠️ **共性提醒（每条都要在报告里带上）**：删目录之后**必须同时清理 shell 配置里的初始化行**，否则每开一个终端都会报 "no such file or directory"。这是最常见的清理后遗症。

⚠️ **conda 附加提醒**：Anaconda 发行版与 `defaults` 频道对 ≥200 人组织自 2024-03 起需商业授权（已实际执法）。若用户在企业环境，顺带提示改用 miniforge + conda-forge。

---

## 三、包管理器 / 构建缓存（多为「缓存」，删了会重下）

| 目录 | 归属 | 官方清理命令 | 代价 |
|---|---|---|---|
| `~/.npm` | npm | `npm cache clean --force` | 下次装包重下 |
| `~/.yarn` `~/.cache/yarn` | yarn | `yarn cache clean` | 重下依赖 |
| `~/Library/pnpm` | pnpm | `pnpm store prune` | 只清无引用的包，安全度高 |
| `~/.bun` | bun | 工具本体 + 缓存混合，**别整删** | — |
| `~/.m2` | Maven | 无官方子命令；可删 `~/.m2/repository` | 重下全部依赖，离线构建会失败 |
| `~/.gradle/caches` | Gradle | 可删 caches 子目录 | 重下 + 重建构建缓存 |
| `~/.cargo/registry` | Rust | `cargo cache`（需装插件）或删 registry | 重下 crates |
| `~/go/pkg/mod` | Go | `go clean -modcache` | 重下模块 |
| `~/Library/Caches/pip` | pip | `pip cache purge` | 重下 wheel |
| `~/.local/share/uv` `~/.cache/uv` | uv | `uv cache clean` | 重下依赖 |
| `~/Library/Caches/Homebrew` | Homebrew | `brew cleanup`（官方：清理陈旧锁文件与过期下载，默认清 120 天以上） | 重下安装包 |

---

## 四、容器 / 模拟器 / AI 模型（体积最大，也最容易误删）

| 目录 | 身份 | 处置 | ⚠️ 风险 |
|---|---|---|---|
| `~/Library/Containers/com.docker.docker` | **数据 + 缓存混合** | `docker system prune`（官方：Remove unused data）；加 `-a` 会删所有未使用镜像 | ⛔ **容器卷里可能有数据库数据**，`--volumes` 参数绝不要在建议里默认带上 |
| `~/Library/Developer/CoreSimulator/Devices` | 缓存（可重建） | `xcrun simctl delete unavailable` 清不可用模拟器 | 模拟器内已装 App 与数据会没 |
| `~/Library/Developer/Xcode/DerivedData` | 纯缓存 | 可整个删，Xcode 会重建 | 下次编译变慢 |
| `~/Library/Developer/Xcode/iOS DeviceSupport` | 缓存 | 可删旧 iOS 版本目录 | 调试对应版本真机时会重新生成 |
| `~/.cache/huggingface` | **数据（模型权重）** | `hf cache ls` 看占用 → `hf cache rm <repo>` 删指定 → `hf cache prune` 清无引用版本与断点残片 | ⛔ 重下动辄几小时；**官方载明「下新版本时旧版本不会自动删」**，所以只增不减 |
| `~/.ollama/models` | **数据（模型权重）** | `ollama list` → `ollama rm <model>` | ⛔ 重下耗时 |
| `~/.cache/torch` | 缓存（预训练权重） | 可删，会重下 | 重下耗时 |

---

## 五、报告里必须出现的三条免责

1. 「以下判定基于扫描到的信号，**最终是否删除由你决定**」
2. 「清理命令请以各工具官方文档为准，本报告不代为执行」
3. 「删除版本管理器目录后，记得同步清理 shell 配置里的初始化行」

---

## 六、AI 开发与 Agent 宿主（2026 增补）

> 对应 `scan.sh --profile ai-dev` 快扫档；体积大户常在「技能缓存 + 模型权重 + Playwright 浏览器」三类。

| 目录 | 身份 | 判活特征 | 官方/推荐处置 | 代价 |
|---|---|---|---|---|
| `~/.claude` | **数据**（技能、MCP 配置、会话索引） | Claude Code / Cowork 仍在用 | 不整删；`skills/` 里过期 skill 可手动移走 | ⛔ 删了配置和技能全没 |
| `~/.cursor` | **数据** | Cursor 仍在用 | 不整删；`projects/` 是索引缓存可择机清 | 重索引项目 |
| `~/.codex` | **数据** | Codex CLI 仍在用 | 不整删 | 丢 CLI 配置 |
| `~/.codebuddy` | **数据** | Codebuddy 仍在用 | 不整删 | 丢宿主配置 |
| `~/.agents/skills`（若存在） | **数据** | 多宿主统一 skills 入口 | 只删确认不用的 skill 子目录 | 该 skill 失效 |
| `~/.npm/_npx` | 缓存 | npx 一次性包 | `rm -rf ~/.npm/_npx` 或 `npm cache clean --force` | 下次 npx 重下 |
| `~/Library/Application Support/Cursor` | **数据+缓存混合** | Cursor 主程序数据 | 只清 `Cache`/`GPUCache` 子目录，别整删 Support | 可能丢窗口布局 |
| `~/Library/Application Support/Claude` | **数据** | Claude 桌面端 | 不整删 | 丢本地状态 |
| `~/.cache/ms-playwright` `~/Library/Caches/ms-playwright` | 缓存 | Playwright 测浏览器 | `npx playwright install --force` 可重建；或删对应缓存目录 | 下次测试重下浏览器（数百 MB～数 GB） |
| `~/.local/share/uv` `~/.cache/uv` | 缓存 | uv / Python 工具链 | `uv cache clean` | 重下 wheel |
| `~/.ollama` `~/.cache/huggingface` | **数据**（模型） | 见第四节 | 见第四节 | 见第四节 |

**报告互链（体检器家族）**：
- 配置层异常（`AGENTS.md` / `CLAUDE.md` 重复、路由错）→ 建议用户跑 **`hekouwang-claude-md-doctor-skill`**（`claude-md-doctor`）
- 技能层异常（`SKILL.md` 缺 frontmatter、死链）→ **`hekouwang-claude-skill-doctor-skill`**（`skill-doctor`）
- 本器只管磁盘与环境残留，**不替另外两把做文件内容审计**

---

## 七、规则库维护约定

- 新增工具时补齐五列：**目录 / 身份 / 判活特征 / 官方命令 / 代价**，缺一列不许并入。
- 官方命令必须来自官方文档或工具自带 `--help`，**不许凭记忆写**；核实来源记在提交信息里。
- 本库版本号（标题上的 v）随每次规则增删递增，报告页脚需打印它，便于用户知道自己用的是哪版规则。
