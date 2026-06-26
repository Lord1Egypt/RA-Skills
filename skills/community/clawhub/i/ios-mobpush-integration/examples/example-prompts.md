# 示例提示词

以下提示词可直接用于触发 `ios-mobpush-integration`：

## 新接入

```text
请用 ios-mobpush-integration skill 帮我把 MobPush 接进这个 iOS 项目。
```

```text
帮我在现有 iOS 工程里接入 MobPush，先扫描工程，再给最小改动方案。
```

## 读取配置表继续执行

```text
MobPush_iOS_Config.xlsx 我已经填好了，请继续扫描项目并给出修改计划。
```

```text
请读取项目根目录下的 MobPush_iOS_Config.xlsx，校验后继续完成 MobPush 接入。
```

## 排查问题

```text
帮我检查这个 iOS 项目的 MobPush 为什么收不到推送，先看 Podfile、Info.plist、AppDelegate 和隐私同意链路。
```

```text
MobPush 已经接入了，但 registrationID 取不到。请扫描工程并定位问题。
```

## 可选能力

```text
在基础推送已经接通的前提下，帮我继续把 MobPush tag 和 alias 的接线补上。
```

```text
这个项目需要 MobPush 的 Live Activity 能力，请先确认是否满足 iOS 16.1+ 和 SwiftUI 条件，再给接入方案。
```

