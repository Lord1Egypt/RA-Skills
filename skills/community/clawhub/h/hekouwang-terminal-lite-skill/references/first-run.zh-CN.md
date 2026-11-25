# 首次体验：开窗即成品，体检看得懂

免费版没有要改的配置。`install.sh` 已经做完了，这一页只讲怎么读它的结果。

## 第一个窗口就是成品

`install.sh` 在第 7 步用 `theme.sh` 部署主题与生态色，第 10 步写 `~/.zshrc`，第 15 步自己跑一遍 `doctor.sh`。装完开一个新的 iTerm2 窗口：提示符、配色、图标、`ls` 颜色全都在。

坑：装之前就开着的窗口还是旧 shell，必须开新窗口；已有 `~/.zshrc` 时不要重跑 install。

## 把 `--status` 当键值仪表盘读

纯只读，觉得哪里不对就跑：`./scripts/doctor.sh --status`

```
theme      ember（已钉住）
auto       开（跟随系统深浅色）
node       fnm
optical    operator @ compact（pinned）   # 免费版显示 —（付费档）
scene      daily（pinned）                # 免费版显示 —（付费档）
semantic   14 条规则 · 产品 3 · SH=best editor
visual     100/100 · 色板全部达标         # 仅当 config/themes/_audit.py 存在
reload     装了 Ghostty，当前没在跑
```

是 7 到 8 行，不是 6 行：`visual` 只在 `config/themes/_audit.py` 存在时才出现。值全部读自磁盘，出现 `—（尚未部署）` 的那一行才需要动手。

坑：`--status` 打完仪表盘就退出，`--status --profile` 会静默跳过耗时排行。

## `--profile` 点名 top 8 启动耗时

启动变慢时跑 `./scripts/doctor.sh --profile`。它建一个临时 `ZDOTDIR`，在 `zprof` 下 source 真实的 `~/.zshrc`，打印 8 行（名次 / 调用次数 / 总毫秒 / 占比），然后删掉临时目录。

坑：它真的会执行 `~/.zshrc`，里面的交互式或有副作用的行也会跑。想单段禁用又不动主配置，把文件复制进临时 `ZDOTDIR`，在副本里删掉 `# ---- N.` 那一段再测。

## 三条验收命令

- `./scripts/doctor.sh --status` —— 不再有 `—（尚未部署）` 的行。
- `./scripts/doctor.sh --profile` —— 启动低于 300 ms，第一行是你认识的东西。
- `./scripts/theme.sh --preview ember` —— 能渲染出整块假终端。坑：主题名必须是 `--list` 里的 slug，预览不会真正切换主题。
