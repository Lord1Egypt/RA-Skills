# 万磁王技能万事通 (Magneto Skill Master)

> 一个把"从 GitHub / Gitee 安全下载并安装外部 Agent Skill"全流程固化下来的 WorkBuddy 技能。

- 开源版 Slug：`magneto-skill-master`
- 本地中文触发名：`万磁王技能万事通`

## 它解决什么

装外部技能（尤其是标书、招投标、文档生成类）时，常常踩坑：

- 克隆到错误目录、忘了补 `agent_created: true`
- 技能自带 `install.bat` / `.venv`，一运行就污染你的全局 Python
- 中文 `SKILL.md` 经编辑工具偶发乱码（U+FFFD 替换符）
- Windows 下 venv 路径用 `/c/...` 被原生 Python 忽略，装依赖静默失败
- Git Bash 的 MSYS 把 `/c/...` 参数误转成 `C:\c\...`

本技能把这些坑全部写进一套六步流水线，并自带审计清单与 `run_script.sh` 包装器模板。

## 流水线（六步，不可跳步）

1. 定位仓库
2. 下载到临时暂存区
3. 安全审计（强制，P0/P1/P2 分级，绝不静默安装）
4. 适配 WorkBuddy 格式
5. 安装到用户级目录（`~/.workbuddy/skills/<name>/`）
6. 装依赖 + 验证（受管 venv，可移植路径）

## 本地安装

```bash
# 克隆后把技能目录整体放进用户级技能目录
git clone https://github.com/yehuzi2026/magneto-skill-master.git
cp -r magneto-skill-master ~/.workbuddy/skills/magneto-skill-master
```

放入后 WorkBuddy 会按 `description` 里的触发词自动加载，无需重启。

## 文件结构

```
magneto-skill-master/
├── SKILL.md                       # 技能主文件（六步流水线 + 复用坑速查）
├── manifest.yaml                  # 市场元数据（版本 / 触发词 / 分类）
├── README.md                      # 本文件
└── references/
    ├── audit_patterns.md          # 安全审计 grep 命令 + P0/P1/P2 分级 + 乱码修复
    └── run_script_template.sh     # 调用受管 venv 的 run_script.sh 模板（可移植）
```

## 已用本流程安装过的技能

`bid-writer-pro`、`bidwriter`、`bid-doc`、`tender-writer`（均为标书/招投标类）。

## 许可

MIT
