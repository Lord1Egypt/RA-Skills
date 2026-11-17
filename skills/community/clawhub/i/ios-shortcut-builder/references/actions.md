# 动作参数手册

本文件由 `scripts/gen-reference.py` 从 `lib/registry.json` 生成，不要手改。

参数键必须**逐字照抄**——写错会在生成阶段被拦，但改起来总比导进手机发现动作是空的省事。
`ident` 是 iOS 内部动作标识；要扩展新动作时才会用到。

## 通知与提示

### `notify` — 弹通知

弹一条横幅通知，不动任何数据

- ident: `is.workflow.actions.notification`
- 参数: `WFNotificationActionTitle`（标题）、`WFNotificationActionBody`（正文）、`WFNotificationActionSound`（是否响提示音）

### `alert` — 弹对话框

弹出必须点确定的框，会中断后续动作

- ident: `is.workflow.actions.alert`
- 参数: `WFAlertActionTitle`（标题）、`WFAlertActionMessage`（正文）
- 注意: 要人点，不适合无人值守

### `speak` — 朗读文字

用系统语音念一段文字

- ident: `is.workflow.actions.speaktext`
- 参数: `WFText`（要念的文字）、`WFSpeakTextRate`（语速 0.1–2.0）、`WFSpeakTextLanguage`（语言，如 zh-CN）

### `vibrate` — 振动

振动一下

- ident: `is.workflow.actions.vibrate`
- 参数: 无

### `ask` — 弹框问输入

弹输入框让人填，返回填的内容

- ident: `is.workflow.actions.ask`
- 参数: `WFAskActionPrompt`（提问）、`WFInputType`（Text/Number/URL/Date）
- 注意: 等人输入

## 数据读写

### `clipboard.get` — 读剪贴板

把剪贴板内容读出来

- ident: `is.workflow.actions.getclipboard`
- 参数: 无

### `clipboard.set` — 写剪贴板

把文字写进剪贴板

- ident: `is.workflow.actions.setclipboard`
- 参数: `WFInput`（要写入剪贴板的文本或变量）
- 说明: 生成器特殊处理，会展开成多个 iOS 动作，所以实际动作数比配方里看到的多

### `note.append` — 追加备忘录

把文字追加到指定备忘录末尾

- ident: `is.workflow.actions.appendnote`
- 参数: `entity`（备忘录名）、`text`（追加内容）

### `reminder.add` — 建提醒

在「任务」列表加一条提醒

- ident: `is.workflow.actions.addnewreminder`
- 参数: `WFCalendarItemTitle`（标题）、`WFCalendarItemNotes`（备注）
- 注意: 列表固定「任务」，不支持截止时间
- 说明: 生成器特殊处理，会展开成多个 iOS 动作，所以实际动作数比配方里看到的多

### `calendar.add` — 建日程

在系统日历新建日程

- ident: `is.workflow.actions.addnewevent`
- 参数: `WFCalendarItemTitle`（标题）、`WFCalendarItemStartDate`（开始 2026-11-15 09:00）、`WFCalendarItemEndDate`（结束）、`WFCalendarItemLocation`（地点）、`WFCalendarItemNotes`（备注）

### `shortcuts.list` — 列出快捷指令

拿到手机上所有快捷指令名

- ident: `is.workflow.actions.getmyworkflows`
- 参数: 无

## 设备状态

### `battery.get` — 读电量

读电池百分比，返回数字

- ident: `is.workflow.actions.getbatterylevel`
- 参数: 无

### `currentapp.get` — 读当前App

拿到当前前台 App 名

- ident: `is.workflow.actions.getcurrentapp`
- 参数: 无

### `location.get` — 读位置

拿当前位置

- ident: `is.workflow.actions.getcurrentlocation`
- 参数: 无
- 注意: 首次会弹定位授权

### `brightness.set` — 设亮度

调屏幕亮度，0–1

- ident: `is.workflow.actions.setbrightness`
- 参数: `WFBrightness`（亮度 0–1）

### `volume.set` — 设音量

调媒体音量，0–1

- ident: `is.workflow.actions.setvolume`
- 参数: `WFVolume`（音量 0–1）、`WFVolumeSetting`（Media/Ringtone）

### `lowpower` — 低电量模式

开/关/切换低电量模式

- ident: `is.workflow.actions.lowpowermode.set`
- 参数: `operation`（on/off/toggle）
- 说明: 生成器特殊处理，会展开成多个 iOS 动作，所以实际动作数比配方里看到的多

## App 与跳转

### `openapp` — 打开App

打开指定 App

- ident: `is.workflow.actions.openapp`
- 参数: `WFAppName`（App 名，如 微信）
- 注意: 会切走前台

### `openurl` — 打开链接

用浏览器打开 URL

- ident: `is.workflow.actions.openurl`
- 参数: `WFInput`（链接）
- 注意: 会切走前台

### `shortcut.run` — 运行别的快捷指令

按名字触发另一个快捷指令（走 URL scheme，支持中文名）

- ident: `is.workflow.actions.openurl`
- 参数: `name`（目标快捷指令名）、`input`（传入文本）
- 说明: 生成器特殊处理，会展开成多个 iOS 动作，所以实际动作数比配方里看到的多

### `script.run` — 跑Scriptable

调 Scriptable 跑 JS 脚本（走 URL scheme）

- ident: `is.workflow.actions.openurl`
- 参数: `name`（脚本名）
- 说明: 生成器特殊处理，会展开成多个 iOS 动作，所以实际动作数比配方里看到的多

## 媒体

### `photo.latest` — 取最新照片

拿相册最新一张

- ident: `is.workflow.actions.getlastphoto`
- 参数: `WFGetLatestPhotoCount`（取几张）、`WFGetLatestPhotosActionIncludeScreenshots`（含截图）

### `photo.take` — 拍照

调相机拍一张

- ident: `is.workflow.actions.takephoto`
- 参数: `WFCameraCaptureDevice`（Back/Front）、`WFCameraCaptureShowPreview`（是否预览）
- 注意: 关预览少一步人工

### `screenshot` — 截屏

截当前屏幕

- ident: `is.workflow.actions.takescreenshot`
- 参数: 无

### `dictate` — 语音转文字

听写，把说的话变文字

- ident: `is.workflow.actions.dictatetext`
- 参数: 无
- 注意: 要人说话

## 通信

### `sms.send` — 发短信

给号码发短信/iMessage

- ident: `is.workflow.actions.sendmessage`
- 参数: `WFSendMessageActionRecipients`（号码或邮箱）、`WFSendMessageContent`（内容）
- 注意: 首次有发送确认弹窗

---

## 变量

| 变量 | 值 | 是否插入取动作 |
|---|---|---|
| `{clipboard}` | 剪贴板文本 | 是，`getclipboard` |
| `{battery}` | 电量百分比 | 是，`getbatterylevel` |
| `{location}` | 当前位置 | 是，`getcurrentlocation` |
| `{now}` | 当前时间 | 否，内置附件 |
| `{input}` | 快捷指令输入 | 否，内置附件 |
| `{repeat_item}` | 当前循环项 | 否，内置附件 |
| `{prev}` | 上一步输出 | 否，指向前一个动作 |

同一个变量在配方里出现多次，只会取一次。

`{prev}` 有个例外：上一步如果是 `shortcut.run` / `script.run`，它只是打开一个 URL，
拿不到输出，生成时会直接报错而不是让你在手机上发现条件永远不成立。

---

## 扩展：注册表里没有的动作

26 个是常用集合，`shortcutkit` 里还注册了 1700 多个。查一个动作长什么样：

```bash
python3 -c "import shortcutkit as sk, json; \
print(json.dumps(sk.ACTIONS['is.workflow.actions.weather.forecast'], ensure_ascii=False, indent=2))"
```

查某类动作有哪些：

```bash
python3 -c "import shortcutkit as sk; print([k for k in sk.ACTIONS if 'weather' in k.lower()])"
```

然后在 `lib/registry.json` 的 `actions` 数组里加一条：

```json
{
  "alias": "weather.forecast",
  "ident": "is.workflow.actions.weather.forecast",
  "zh": "查天气预报",
  "doc": "取某个地点的天气预报，输出天气数据",
  "group": "媒体",
  "params": { "WFWeatherForecastType": { "desc": "daily / hourly / current", "type": "text" } },
  "notes": "未真机验证"
}
```

三条硬要求：

1. `ident` 必须在 `sk.ACTIONS` 里存在，否则生成时 `KeyError`
2. `params` 的键必须和 `sk.ACTIONS[ident]["params"]` 完全一致
3. 加完跑 `bash tests/selftest.sh`；没在手机上试过就在 `notes` 里写明，
   别让用户以为这是测过的

改完重跑 `python3 scripts/gen-reference.py` 更新本文件。

### 两段式动作：先取数据，再取字段

天气就是典型。`weather.forecast` 输出的是「天气数据」对象，不能直接用，
要再接一个 `properties.weather.conditions` 取具体字段：

```json
{ "do": "weather.forecast", "WFWeatherForecastType": "daily" },
{ "do": "weather.detail", "WFContentItemPropertyName": "降水概率" }
```

`properties.weather.conditions` 的 `WFContentItemPropertyName` 是**字段显示名**，
随 iOS 语言变化（中文系统上写「降水概率」，英文系统上写 `Precipitation Chance`）。
这类字段名没法离线枚举，接入前必须在目标手机上试一遍。

AppIntent 类动作（`com.apple.*`）参数通常是嵌套字典，比经典动作难写，
拿不准就先在手机上做一遍，再用 `sc` 反推结构。
