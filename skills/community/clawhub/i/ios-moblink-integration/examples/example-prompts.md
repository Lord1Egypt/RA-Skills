# 示例提示词

以下提示词可直接用于触发 `ios-moblink-integration`：

## 新接入

```text
请用 ios-moblink-integration skill 帮我把 MobLink 接进这个 iOS 项目。
```

```text
帮我在现有 iOS 工程里接入 MobLink 场景还原，先扫描工程，再给最小改动方案。
```

## 读取配置表继续执行

```text
MobLink_iOS_Config.xlsx 我已经填好了，请继续扫描项目并给出修改计划。
```

```text
请读取项目根目录下的 MobLink_iOS_Config.xlsx，校验后继续完成 MobLink 接入。
```

## 排查问题

```text
帮我检查这个 iOS 项目的 MobLink 为什么不能恢复场景，先看 Podfile、Info.plist、AppDelegate、隐私同意链路和恢复代理。
```

```text
MobLink 已经接入了，但 getMobId 返回为空。请扫描工程并定位问题。
```

## 可选能力

```text
在基础 MobLink 已接通的前提下，帮我继续把指定分享按钮接上 getMobId。
```

```text
这个项目需要 MobLink 的 Universal Link 和 Web 落地页联动，请先检查已有 Associated Domains 和 URL Scheme 配置。
```
