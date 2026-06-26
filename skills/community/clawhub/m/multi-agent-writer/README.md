# multi-agent skill

三阶段多智能体写作流水线，支持热点抓取、AI撰写、自动审校。

## 文件说明

```
multi-agent/
├── SKILL.md          # Skill 定义（含 <INSTALL_DIR> 占位符）
├── install.sh        # 安装脚本
├── uninstall.sh      # 卸载脚本
├── scripts/
│   └── link-project.sh   # 开发模式：链接本地项目
├── tests/
│   └── test_install.sh   # 安装验证测试
└── README.md
```

## 安装

```bash
# 自动检测已安装的 agent
bash install.sh

# 安装到所有 agent
bash install.sh --agent all

# 安装到指定 agent
bash install.sh --agent codebuddy
bash install.sh --agent claude
bash install.sh --agent openclaw
```

安装后项目代码位于 `~/.skills/multi-agent/`

## 开发模式（本地已有项目代码）

```bash
# 创建符号链接，跳过 clone
bash scripts/link-project.sh /path/to/local/multi-agent
bash install.sh --agent codebuddy
```

## 卸载

```bash
bash uninstall.sh          # 仅移除 agent 注册
bash uninstall.sh --all    # 同时删除项目代码
```

## 验证安装

```bash
bash tests/test_install.sh
```

## 依赖项目

- [gonelake/multi-agent](https://github.com/gonelake/multi-agent) — 原始 Python 项目代码（安装时自动 clone）
