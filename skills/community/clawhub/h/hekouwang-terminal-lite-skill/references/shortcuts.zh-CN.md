# 快捷键速查表

> [English](shortcuts.md) · **简体中文**

## 窗格与标签

| 快捷键 | 动作 |
|---|---|
| `Cmd+D` | 垂直分屏（左右） |
| `Cmd+Shift+D` | 水平分屏（上下） |
| `Cmd+Opt+方向键` | 窗格间移动焦点 |
| `Cmd+Shift+Enter` | 当前窗格最大化/还原 |
| `Cmd+T` / `Cmd+W` | 新建 / 关闭标签 |
| `Cmd+数字` | 跳到第 N 个标签 |
| 标签有新输出 | 标签上出现小圆点 —— 由 `setup-gui.sh` 打开，四个 agent 并跑时一眼看出谁动了 |
| `Cmd+Shift+O` | Open Quickly：模糊搜索所有 tab/session 跳转 |

## 搜索与历史

| 快捷键 | 动作 |
|---|---|
| `Cmd+F` | 搜索回滚缓冲（无限回滚 = 全文检索） |
| `Cmd+Shift+H` | 粘贴历史（剪贴板时光机） |
| `Cmd+Opt+B` | Instant Replay：回放终端画面找回被刷掉的输出 |
| `Ctrl+R` | atuin 全文搜索命令历史 |
| `Ctrl+T` | fzf 模糊搜索文件 |
| `Alt+C` | fzf 模糊 cd |
| `Cmd+Shift+↑/↓` | 命令块间跳转（Shell Integration） |

## 选择与复制

| 快捷键 | 动作 |
|---|---|
| `Cmd+Shift+C` | Copy Mode（vim 式键盘选择：hjkl 移动、v 选、y 复制） |
| 双击 / 三击 | 选词 / 选整行（三击含折行，由 `setup-gui.sh` 打开） |
| `Cmd+点击` | 智能打开 URL / 文件路径 |
| `Opt+拖选` | 矩形（列）选择 |
| 选中即复制 | 由 `setup-gui.sh` 打开，选完直接 `Cmd+V` |

## Shell（来自插件）

| 按键 | 动作 |
|---|---|
| `→` / `End` | 接受 autosuggestions 灰色提示 |
| `Tab` | zsh-autocomplete 进补全菜单，方向键选 |
| `z 关键词` | zoxide 跳转高频目录；`zi` 交互选择 |

## 其他

| 快捷键 | 动作 |
|---|---|
| `Cmd+/` | 高亮光标位置 |
| `Cmd+Enter` | 全屏 |
| `Shift+Enter` | 发送换行（AI CLI 多行输入，自定义键映射） |
| `Opt+Space` | 下拉热键窗口（需要先做一次 Hotkey Window 设置，默认没开） |

## 自然文本编辑（一次性 GUI 预设）

iTerm2 自带一套 macOS 风格的删词/行首行尾键位。`setup-gui.sh` 没有自动写，
因为键映射格式会随 iTerm2 版本变；手动点一次即可：

`Settings → Profiles → Keys → Key Mappings → Presets → Natural Text Editing`

生效后：`Opt+Backspace` 删词、`Opt+←/→` 按词移动、`Cmd+←/→` 行首行尾、
`Cmd+Backspace` 删到行首。
