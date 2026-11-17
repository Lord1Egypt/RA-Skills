# 本地个人层模板（local-config-example）

把本目录整体复制为 `~/.config/majia-chatcut-koubo/`，装进你自己的数字与偏好。skill 开工时会探测该目录：**存在则叠加在本包的通用规则之上**；不存在就只用包内通用值。本地层**永不进 git**、永不进公开仓——品牌词、真实业务数字、个人实测坐标全部放这里。

```
~/.config/majia-chatcut-koubo/
  profile/            个人 operating profile(实测版式/字幕/音频数字);同名键覆盖包内
                      assets/compositions.json 与模板默认值;一版一文件,升版不覆盖旧版
  terminology.json    个人词表(机器读):validator 用 --terms 指向它
  terminology.md      个人词表(人读版,可选):维护心得、证据记录
  aesthetics.md       个人审美基线:过渡手感、构图偏好、保护基线清单
  local-notes.md      个人补充护栏:私有工作流衔接、平台账号惯例、个人路径
```

对应关系：

| 本地文件 | 覆盖/叠加的公开资产 | 用法 |
| --- | --- | --- |
| `profile/*.json` | `templates/operating-profile.template.json` 起模；同名键覆盖 `assets/compositions.json` 坐标 | 使用 source schema；剪辑开工先读；`validate-caption-pages.mjs --profile` 指向它 |
| `terminology.json` | `templates/terminology.template.json` 起模 | `validate-caption-pages.mjs --terms` 指向它 |
| `aesthetics.md` | `SKILL.md` 红线之上的个人裁决面 | 审美分歧时代理先读它再问你 |
| `local-notes.md` | 无（纯个人层） | 写不适合进公开包的一切个人惯例 |

例子文件都带注释，替换成你的内容即可。

Profile 可以用相对 `extends` 继承一个父文件；每个路径都按**声明它的那一层文件**解析。数组整体替换，普通对象递归合并。叶 profile 必须自己声明 `status` 和完整 `provenance`，不能继承父层的项目/时间线可信身份。

发布前先解析并检查来源：

```bash
node src/cli/resolve-profile.mjs \
  --profile ~/.config/majia-chatcut-koubo/profile/<你的-profile>.json \
  --root ~/.config/majia-chatcut-koubo \
  --strict \
  --out ~/.config/majia-chatcut-koubo/generated/profile.resolved.json \
  --trace ~/.config/majia-chatcut-koubo/generated/profile.merge-trace.json
```

生成的 resolved 文件不含 `extends`，trace 可以追到每个字段来自哪一层。
输出只能留在 `--root` 内，且可能包含项目级标识；两类默认文件名已在
`.gitignore` 中排除。旧 profile 可先不加 `--strict` 做只读迁移检查，但
`contractStatus=migration-incomplete` 时不会写出 resolved 文件。
