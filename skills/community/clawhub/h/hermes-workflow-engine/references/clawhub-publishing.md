# ClawHub 发布工作流（含可执行代码）

## 核心规则

**ClawHub 只发布技能目录内的文件。** 如果技能包含 Python/Shell 脚本等可执行代码，必须把代码放在 `scripts/` 子目录下，否则别人安装后只有 SKILL.md 没有代码。

## 发布流程

### 1. 准备目录结构

```
~/.hermes/skills/<category>/<skill-name>/
├─ SKILL.md              # 技能定义（必须）
├─ references/           # 参考文档
├─ scripts/              # 可执行代码（必须，如果技能需要代码）
│  ├─ *.py
│  ├─ *.sh
│  └─ examples/          # 示例文件
├─ templates/            # 模板文件
└─ assets/               # 静态资源
```

### 2. 复制代码到 scripts/

```bash
# 如果代码在独立项目目录
cp ~/.hermes/workflow-engine/*.py scripts/
cp ~/.hermes/workflow-engine/FORMAT.md scripts/
cp -r ~/.hermes/workflow-engine/examples scripts/
```

### 3. 发布

```bash
cd ~/.hermes/skills/<category>/<skill-name>
clawhub publish . --slug <skill-slug> --name "技能名" --version x.y.z
```

### 4. 验证

```bash
clawhub inspect <skill-slug> --files
```

确认 Files 列表包含 `scripts/*.py` 等代码文件。

## 踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| 别人安装后没有代码 | 代码在项目目录，不在技能目录 | 把代码复制到 `scripts/` 再发布 |
| slug 已被占用 | 别人已注册同名 | 加前缀，如 `hermes-workflow-engine` |
| 版本号不变 | 没改版本号 | 每次发布递增版本号 |

## GitHub 仓库同步

发布到 ClawHub 后，也推送到 GitHub：

```bash
cd ~/.hermes/workflow-engine
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:LGX281227231/<repo-name>.git
git branch -M main
git push -u origin main
```

### GitHub SSH Key 共享

如果本地没有 GitHub SSH Key，可以从龙虾服务器复制：

```bash
scp root@43.173.120.234:~/.ssh/id_ed25519 ~/.ssh/id_ed25519_backup
# 配置 SSH 使用这个 key
cat > ~/.ssh/config << 'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_backup
    IdentitiesOnly yes
EOF
ssh -T git@github.com  # 测试连接
```

### ClawHub Token 共享

从龙虾导入 ClawHub token：

```bash
scp root@43.173.120.234:~/.config/clawhub/config.json ~/.config/clawhub/config.json
clawhub whoami  # 验证
```
