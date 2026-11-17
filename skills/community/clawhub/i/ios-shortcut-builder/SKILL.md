---
name: ios-shortcut-builder
display_name: iOS快捷指令生成器
display_name_en: iOS Shortcut Builder
description: 把「帮我做个快捷指令」「想要个一键…的」这类需求，翻译成配方并生成可导入 iPhone 的 .shortcut 文件，自带自签，无需 Mac
description_zh: 说需求即可生成 iOS 快捷指令：翻成配方、生成、自签、交付可导入文件。不需要 Mac、Xcode 或 iCloud。覆盖 26 个常用动作、条件、循环与菜单。
description_en: Turn a plain-language request into an importable iOS .shortcut file — recipe, build, self-sign, deliver. No Mac, Xcode or iCloud required.
examples_zh:
  - "帮我做个快捷指令：电量低于20%时自动开省电模式并提醒我"
  - "想要个一键把剪贴板内容存进备忘录的快捷指令"
  - "做个到公司时给我家人发条消息的快捷指令"
examples_en:
  - "Make a shortcut that turns on Low Power Mode and notifies me when battery drops below 20%"
  - "I want a shortcut that saves my clipboard into a note"
  - "Create a shortcut that texts my family when I arrive at the office"
version: 2.0.0
author: "Niuniu"
license: MIT
requires:
  os: linux-x86_64
  python: ">=3.8"
  packages: [shortcutkit]
  system: [openssl, libplist-2.0-4]
---

# iOS 快捷指令生成器

用户说「帮我做个快捷指令」「想要个一键…的」「手机上自动…」时用本技能。

**你负责把需求翻译成配方，工具负责把配方变成能导入手机的文件。**
整条链路不需要 Mac、不需要 Xcode、不需要 iCloud。

> **运行前提**：Linux x86-64 + Python 3.8+。签名器是预编译的 Linux 二进制，
> macOS / Windows / ARM 上**生成了也签不了名**，产物手机不认。
> 上机先跑 `./bin/sc doctor`，它会把缺什么一次列全。

---

## 交付物是什么

一个 `.shortcut` 文件，发到 iPhone 上点开就弹「导入到快捷指令」。
**必须签名**，否则 iOS 会拒绝导入 —— 本技能自带自建 CA 签名，这一步不用你操心。

---

## 四步做完

### 第 0 步：环境与证书（每台机器一次）

```bash
./bin/sc setup                    # 装依赖 + 逐项体检，缺什么直接说
```

`setup` 会自动装 `shortcutkit`、检查 openssl，缺 `libplist-2.0-4` 时尝试补上。
它装不动的（比如没有 root）会直接打印要执行的命令，不会假装成功。

> `setup` 只看运行环境，**不查证书**（那要等下一步）。想连证书一起查用 `sc doctor`，
> 没建证书时它会返回非 0。

依赖齐了再建证书。证书有两入口，看用户手里有没有现成的快捷指令：

**入口 A：用户发来一个链接或文件（推荐，用户零操作）**

```bash
./bin/sc adopt "用户发来的链接或文件"
```

两种都能吃：

- **iCloud 分享链接** `https://www.icloud.com/shortcuts/xxxx` —— 用户在快捷指令 App 里
  「分享 → 拷贝 iCloud 链接」得到的就是这个，最常见
- **本地 `.shortcut` 文件** —— 导出后发过来的

技能会先把样本里的证书链解出来，再和本机证书**逐字节比对**，然后分情况：

| 情况 | 处理 |
|---|---|
| 样本里的 CA 就是本机这套（**同一张证书**） | **直接能用，手机不用重装** |
| 样本是另一套证书 | 提示二选一：继续用本机的，或 `--force` 按样本名字重建 |
| 苹果官方签名 / 未签名（iCloud 分享都是这种） | **本机没证书时**按名字新建一套，手机装一次新证书；已有证书则拦下不覆盖 |

第 1 种是最理想的情况：用户之前用这台机器签过，私钥还在 `certs/` 里，
指纹一对上就说明手机早信任了，什么都不用动。

> **关键概念**：`.shortcut` 文件里嵌的是**证书（公钥）**，**私钥不在里面**。
> 签名必须用私钥盖，所以「拿用户发来的文件直接签」这件事，
> 只有本机存着配套私钥时才成立。私钥拿不到，就只能新建一套——
> 名字可以一样，但那是另一张证书，手机要重新装。

**入口 B：用户什么都没发，直接起个名**

```bash
./bin/sc init --cn "他的CA名"
```

两个入口产物一样，都在 `certs/`。**私钥绝不外传**：共用一套私钥等于共用签发权。

不想让私钥待在技能目录里（压缩分享技能包时容易连 `ca.key` 一起发出去），
把证书目录指到别处：

```bash
SC_CERT_DIR=~/.shortcut-ca ./bin/sc init --cn "我的CA"
SC_CERT_DIR=~/.shortcut-ca ./bin/sc build 配方.json    # 之后每条命令都带同一个变量
```

然后把这个文件发给用户装到手机上：

```
certs/ca.mobileconfig
```

装法：iPhone 用 **Safari** 打开 → 设置 → 通用 → VPN与设备管理 → 安装 →
设置 → 通用 → 关于本机 → 证书信任设置 → 对本 CA 开「完全信任」。
⚠ 只装描述文件、不开完全信任，导入时仍会报「无法验证」。

### 第 1 步：把需求翻译成配方

先查有哪些动作可用：

```bash
./bin/sc catalog                 # 全部 26 个，按用途分组
./bin/sc catalog --grep 通知      # 按关键词找
```

然后写一份 JSON 配方。文件名随意，`name` 只能用 ASCII（字母、数字、下划线、连字符）：

```json
{
  "name": "PillReminder",
  "color": "Orange",
  "steps": [
    { "do": "notify", "WFNotificationActionTitle": "该吃药了",
      "WFNotificationActionBody": "早饭后一片" },
    { "do": "note.append", "entity": "健康记录", "text": "服药打卡 {now}" }
  ]
}
```

三个字段就够：`name`（英文名）、`color`（图标色）、`steps`（动作序列）。
`color` 可选值：Red / Orange / Yellow / Green / Teal / Blue / Violet / Purple / Pink / Gray。

### 第 2 步：生成并签名

```bash
./bin/sc build 配方.json -o out/名字.shortcut
```

一步出两个文件：`out/名字.shortcut`（未签名）和 `out/名字-signed.shortcut`（可导入）。
命令会自己做三件校验：动作数、控制流配对、签名前后动作数一致。

### 第 3 步：交付

把 **`-signed.shortcut`** 这个文件给用户，另外第一次还要给他 `certs/ca.mobileconfig`。

**文件怎么到手机**（按可行性从高到低）：

| 方式 | 说明 |
|---|---|
| 邮件附件 / 微信「文件传输助手」 | 最通用；`.shortcut` 和 `.mobileconfig` 都能发 |
| 同局域网起个临时服务 | `python3 -m http.server 8000 -d .`，手机浏览器输 `http://电脑IP:8000/` |
| AirDrop（仅 Mac） | 直接拖过去 |
| 云盘 / 对象存储 | 生成分享直链，手机点开下载 |

手机端：在「文件」App 里点开下载到的 `.shortcut` → 右上角分享 → 快捷指令。
**不要改名、不要重新压缩**，改了 iOS 会认不出这是快捷指令包。

第一次用要连 `certs/ca.mobileconfig` 一起发，装完（见第 0 步）再导入。
装过一次之后，这台手机以后所有文件直接导入即可。

### 第 4 步：要「自动跑」时，教用户设自动化

本技能产出的是**动作**，不是**触发器**。用户说「每天早上提醒我」时，
文件里没有时间信息，得在手机上挂一个触发器，否则它永远不会自己响：

1. 快捷指令 App → 底部「自动化」→ 右上「+」
2. 选「特定时间」→ 设 7:30 → 每天 → 下一步
3. 选刚导入的那个快捷指令
4. **把「运行前询问」关掉** ← 不关每次都要点一下确认，等于没自动化
5. 完成

同理可用「到达某地」「连上某个 Wi-Fi」「打开某 App」触发。
这一步必须交代，否则用户会以为做出来就会自己跑。

⚠ 「运行前询问」关掉只解决**快捷指令本身**的确认。配方里某些动作在自动化中仍会停：

| 动作 | 自动化里的实际表现 |
|---|---|
| `sms.send` | **仍会弹发送确认**（iOS 限制，关不掉）→ 无人值守根本发不出去 |
| `alert` / `ask` / `dictate` | 必须人点、人说 |
| `menu` | 必须人选 |

要真正的无人值守，就别用这几个：改用 `notify`（通知不弹确认）或 `note.append` 记录。
生成时也会给出警告（「有 N 个需要人操作的动作」）。

### 第 5 步：桌面按钮 / 小组件

用户要「桌面上一个按钮」时：

- 快捷指令 App 里**长按**该指令 → 分享 → **添加到主屏幕**
- 或长按桌面 → 添加小组件 → 选「快捷指令」→ 挑这一条

### 定位权限（无人值守必看）

配方里用了 `{location}`，第一次运行会弹授权。手动跑点一下就行；
但自动化里没有人在旁边，要去
**设置 → 隐私与安全性 → 定位服务 → 快捷指令** 改成「始终」，否则拿不到位置。

---

## 配方语法

### 一个动作

```json
{ "do": "动作别名", "参数键": "值", ... }
```

`do` 后面的别名查 `sc catalog`；参数键**必须跟目录里写的完全一致**，写错会在生成时直接报错并告诉你合法键。

### 变量插值

字符串里写 `{变量名}`，生成时会变成真正的取值动作：

| 变量 | 拿到什么 | 说明 |
|---|---|---|
| `{clipboard}` | 剪贴板内容 | 首次引用时自动插入「获取剪贴板」动作 |
| `{now}` | 当前时间 | 内置，不产生动作 |
| `{input}` | 快捷指令的输入 | 从分享面板或别的快捷指令传进来的 |
| `{battery}` | 电池百分比 | 自动插入「获取电池电量」 |
| `{location}` | 当前位置 | 自动插入「获取当前位置」，首次会弹授权 |
| `{prev}` | 上一步的输出 | 紧跟在取值动作后面用 |
| `{repeat_item}` | 当前循环项 | 只能在 repeat_each 里用 |

同一个变量在配方里多次出现，只会取一次。

也可以整值引用：`{ "ref": "clipboard" }`，等价于把变量当参数传。

### 条件

```json
{ "do": "if", "subject": "{battery}", "op": "less_than", "value": "20",
  "then": [ ...动作... ],
  "else": [ ...动作... ] }
```

`op` 可用：`is` `is_not` `contains` `does_not_contain` `begins_with` `ends_with`
`greater_than` `less_than` `greater_or_equal` `less_or_equal` `has_any_value` `has_no_value`
（中文别名也行：等于 / 不等于 / 包含 / 大于 / 小于 …）

### 重复

```json
{ "do": "repeat", "count": 3, "steps": [ ... ] }
{ "do": "repeat_each", "each": "{clipboard}", "steps": [ ... ] }
```

### 菜单

```json
{ "do": "menu", "prompt": "要做什么？",
  "items": [
    { "title": "上班", "steps": [ ... ] },
    { "title": "睡觉", "steps": [ ... ] }
  ] }
```

---

## 动作目录（26 个）

每个动作都用 `shortcutkit` 的注册表逐条编译验证过：参数键对不上会直接失败，
所以能列在这里的都在结构上成立。常用动作（通知、追加备忘录、省电、音量亮度、
发短信、菜单）另外在真机导过一轮。

| 分组 | 别名 | 做什么 | 关键参数 |
|---|---|---|---|
| 通知与提示 | `notify` | 弹通知 | `WFNotificationActionTitle` / `WFNotificationActionBody` |
| | `alert` | 弹对话框（要人点） | `WFAlertActionTitle` / `WFAlertActionMessage` |
| | `speak` | 朗读文字 | `WFText` |
| | `vibrate` | 振动 | 无 |
| | `ask` | 弹输入框问一句 | `WFAskActionPrompt` / `WFInputType` |
| 数据读写 | `clipboard.get` | 读剪贴板 | 无 |
| | `clipboard.set` | 写剪贴板 | `WFInput` |
| | `note.append` | 追加到备忘录 | `entity`（备忘录名，不存在会自动建）/ `text`（Notes 的 AppIntent，参数键随 iOS 版本可能变） |
| | `reminder.add` | 建提醒事项 | `WFCalendarItemTitle` / `WFCalendarItemNotes` |
| | `calendar.add` | 建日程 | `WFCalendarItemTitle` / `WFCalendarItemStartDate` |
| | `shortcuts.list` | 列出全部快捷指令名 | 无 |
| 设备状态 | `battery.get` | 读电量 | 无 |
| | `currentapp.get` | 读当前 App | 无 |
| | `location.get` | 读位置 | 无 |
| | `brightness.set` | 设亮度 0–1 | `WFBrightness` |
| | `volume.set` | 设音量 0–1 | `WFVolume` / `WFVolumeSetting` |
| | `lowpower` | 低电量模式 | `operation`（on/off/toggle） |
| App 与跳转 | `openapp` | 打开 App | `WFAppName`（按显示名匹配，中文名可能对不上；不确定就用 `openurl` 加 URL scheme） |
| | `openurl` | 打开链接 | `WFInput` |
| | `shortcut.run` | 触发另一个快捷指令 | `name` / `input` |
| | `script.run` | 跑 Scriptable 脚本 | `name` |
| 媒体 | `photo.latest` | 取最新照片 | `WFGetLatestPhotoCount` |
| | `photo.take` | 拍照 | `WFCameraCaptureDevice` |
| | `screenshot` | 截屏 | 无 |
| | `dictate` | 语音转文字 | 无 |
| 通信 | `sms.send` | 发短信/iMessage | `WFSendMessageActionRecipients` / `WFSendMessageContent` |

`sc catalog` 会打印每个动作的全部参数说明，**拿不准就查，不要凭记忆写参数名**。

需要参数的完整键名、内部 ident、逐条注意事项时，读 `references/actions.md`
（从同一份注册表生成，和 `sc catalog` 永远一致）。

目录里没有的动作：`sc catalog --json` 出全量后，用 `shortcutkit` 的原生 API 手写
（`sk.ACTIONS` 里注册了 1714 个动作），或者在 `lib/registry.json` 里加一条并补进自测。

---

## 需求 → 配方 的翻译范例

| 用户说 | 配方骨架 |
|---|---|
| 「每天提醒我吃药」 | `notify` → `note.append`（记一笔打卡） |
| 「电量低于 20% 自动省电」 | `if {battery} less_than 20` → `lowpower on` + `notify` |
| 「把剪贴板存进备忘录」 | `note.append` 的 `text` 写 `{clipboard}` |
| 「一键给老婆发到家了」 | `sms.send`（`WFSendMessageActionRecipients` 填号码、`WFSendMessageContent` 写文案；填联系人名发不出去） |
| 「截个屏存下来」 | `screenshot` → （接 `note.append` 或后续动作） |
| 「出门前让我选一下」 | `menu` 两个分支：上班 / 睡觉 |
| 「打开微信」 | `openapp` 一个动作就够（或 `openurl` 加 `weixin://`） |

写配方时保持**动作数最少**：能一个动作解决的，不要拆三步。

### 这套动作做不到的（别硬编）

| 需求 | 实际情况 |
|---|---|
| 「每天 7 点提醒我」 | 没有定时器。时间触发要用户自己在快捷指令 App 的「自动化」里设，本技能只产出被执行的动作 |
| 「下雨提醒我带伞」 | **26 个内置动作里没有天气**，但 `shortcutkit` 注册表里有（`weather.forecast` + `properties.weather.conditions`，两段式）。按 `references/actions.md` 末尾的「扩展」一节加进注册表即可。别用 `shortcut.run` 去接输出——它拿不到子指令的返回值 |
| 「读我的微信/通知」 | 没有这类动作，iOS 也不开放 |
| 「后台一直跑」 | 快捷指令不是常驻进程，只能被触发执行 |

遇到这类需求，**先告诉用户边界**，再给替代方案，不要编一个不存在的动作名。

---

## 报错怎么修

| 报错 | 含义 | 怎么改 |
|---|---|---|
| `没有叫 'xxx' 的动作` | 别名写错 | 命令会给相近建议；跑 `sc catalog` 核对 |
| `xxx 没有参数 ['yyy']` | 参数键写错 | 报错里直接列了合法键，照抄 |
| `未知变量 {yyy}` | 变量名写错 | 只用上面那 7 个变量 |
| `if 的 op 不认识` | 条件词写错 | 用 `less_than` 这类英文下划线写法 |
| `name 只能用 ASCII` | 快捷指令名带中文 | 改成 `PillReminder` 这种 |
| `配方第一步就用了 {prev}` | `{prev}` 前面没动作 | 先放一个取值动作 |

---

## 交付前检查

```bash
./bin/sc doctor                          # 环境 + 证书是否齐
./bin/sc build 配方.json -o out/X.shortcut   # 看到 ✓ 和「可导入」才算完
```

`build` 通过 = 动作数 > 0、控制流开闭配对、签名前后动作数一致。
这三条是硬门槛，任何一条不过都不要交付。

---

## 已知坑（都是实测踩出来的）

| 现象 | 原因 | 解法 |
|---|---|---|
| `failed to create EVP_PKEY object` | 私钥给了 PEM/DER 格式 | 必须是 **X9.63 裸私钥：`04‖X‖Y‖K`，97 字节**，`sc init` 生成的就是对的 |
| `libplist-2.0.so.4: cannot open shared object file` | 缺运行库 | `apt install libplist-2.0-4` |
| 导入报「无法验证」 | 只装了描述文件 | 还要去「证书信任设置」开完全信任 |
| 导入后名字变问号 | 文件名或指令名带中文 | 全改 ASCII 重新生成 |
| `ModuleNotFoundError: shortcutkit` | 装到了另一个 Python | 用同一个解释器：`python3 -m pip install shortcutkit` |
| 生成成功但手机上动作是空的 | 参数键写错、被 iOS 静默丢弃 | 生成阶段的校验会拦；不要手改 plist |
| 签名器 `verify` 返回 0 却报失败 | 该命令失败也返回 0 | 用 `sc verify`，它已封装这层判断 |
| `shortcut-sign verify` 段错误（139） | 喂了未签名文件，它不判空 | 别直接调它；`sc verify` 会先查文件头 |
| 备忘录/提醒跑出来是空的 | `entity` 指向的列表不存在 | `note.append` 会自动建；`reminder.add` 固定「任务」列表 |

---

## 边界与风险

- 自签不是苹果官方通道，iOS 大版本升级可能失效；苹果历史上封堵过一次同类做法
- 证书只能给自己设备用。把 `certs/` 给别人 = 把签发权给别人
- 装根证书会扩大设备信任面，非自用设备不要装
- 需要人点的动作（`alert` / `ask` / `dictate` / 带预览的 `photo.take`）不适合做无人值守自动化
- 本技能只产出**文件**，不负责让手机定时跑。要做「服务器下发 → 手机自动执行」，
  那是另一个技能（自动化编排）的事
