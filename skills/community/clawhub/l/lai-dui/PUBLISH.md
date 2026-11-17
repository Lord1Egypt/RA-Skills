# 发布说明 · 打包与导入 .skill

本技能可用 skill-creator 提供的 `package_skill.py` 打包成 `.skill` 文件（本质是 zip），便于分发与导入。

## 打包

```bash
# 在 skill-creator 的 scripts 目录下执行
python3 package_skill.py /path/to/lai-dui ./dist
# 生成 ./dist/lai-dui.skill
```

`package_skill.py` 会先校验 `SKILL.md`，通过后才打包，产物包含 `SKILL.md` 与 `references/`。

## 导入

- **方式一（客户端支持导入）**：在 CodeBuddy 的「技能管理 / 导入技能」中选择 `lai-dui.skill`。
- **方式二（手动）**：把 `lai-dui.skill` 当 zip 解压，将 `lai-dui/` 目录放到用户技能目录 `~/.codebuddy/skills/`，重启客户端。

## 跨平台技能目录

| 系统 | 路径 |
|------|------|
| Windows | `C:\Users\<用户名>\.codebuddy\skills\` |
| macOS | `/Users/<用户名>/.codebuddy/skills/` |
| Linux | `~/.codebuddy/skills/` |

## 从 Git 同步

```bash
git clone https://github.com/jkdeadwolf/Notes.git
# 取其中的 lai-dui/ 目录，按上方「方式 A」放置即可
```

多机（电脑 / 手机端 CodeBuddy）统一从该仓库获取，保持版本一致。
