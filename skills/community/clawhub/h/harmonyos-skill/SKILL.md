---
name: harmonyos-code-workshop
description: >-
  HarmonyOS (鸿蒙) full-process application development companion from coding
  to AppGallery publishing. Use this skill when users need ArkTS syntax guidance,
  ArkUI component design, API migration, compile error diagnosis, code quality
  inspection, multi-device adaptation, performance optimization, or AppGallery
  Connect publishing. Focuses on practical code editing — not just documentation
  referencing, but ensuring code compiles, passes review, and ships to market.
version: 2.1.0
author: 鸿蒙代码专家团队 <839838805@qq.com>
trigger:
  - "鸿蒙"
  - "HarmonyOS"
  - "ArkTS"
  - "ArkUI"
  - "鸿蒙开发"
  - "HarmonyOS 开发"
  - "鸿蒙应用"
  - "鸿蒙原生"
  - "鸿蒙代码"
  - "鸿蒙 全流程"
  - "鸿蒙 代码工坊"
  - "ArkTS 语法"
  - "ArkUI 组件"
  - "鸿蒙 API"
  - "鸿蒙 元服务"
  - "Stage 模型"
  - "鸿蒙 状态管理"
  - "@State"
  - "@Prop"
  - "@Link"
  - "鸿蒙 多设备适配"
  - "鸿蒙 折叠屏"
  - "鸿蒙 跨设备"
  - "鸿蒙 编译错误"
  - "鸿蒙 踩坑"
  - "鸿蒙 迁移"
  - "TS 转 ArkTS"
  - "TypeScript 迁移 ArkTS"
  - "鸿蒙 UI"
  - "鸿蒙 网络请求"
  - "鸿蒙 数据持久化"
  - "鸿蒙 Navigation"
  - "鸿蒙 Router"
  - "鸿蒙 动画"
  - "鸿蒙 手势"
  - "鸿蒙 测试"
  - "鸿蒙 性能优化"
  - "鸿蒙 并发"
  - "TaskPool"
  - "鸿蒙 Worker"
  - "鸿蒙 安全"
  - "鸿蒙 Camera"
  - "鸿蒙 音频"
  - "鸿蒙 视频"
  - "鸿蒙 推送"
  - "鸿蒙 位置"
  - "鸿蒙 蓝牙"
  - "鸿蒙 NFC"
  - "鸿蒙 分布式"
  - "鸿蒙 流转"
  - "鸿蒙 卡片"
  - "鸿蒙 Widget"
  - "元服务"
  - "Atomic Service"
  - "API 23"
  - "API 24"
  - "API 25"
  - "API 26"
  - "HarmonyOS 7"
  - "鸿蒙 7"
  - "DevEco Studio"
  - "DevEco"
  - "HAP"
  - "HAR"
  - "HSP"
  - "ohpm"
  - "鸿蒙 打包"
  - "鸿蒙 签名"
  - "鸿蒙 上架"
  - "鸿蒙 AppGallery"
  - "AGC"
  - "AppGallery Connect"
  - "鸿蒙 发布"
  - "鸿蒙 审核"
  - "鸿蒙 分发"
agent_created: true
---

# 鸿蒙代码工坊

> 鸿蒙（HarmonyOS）全流程编码助手——从代码编写到 AppGallery 上架，一站式搞定。
>
> 定位：不是文档搬运工，而是 **你的代码质量守护者 + 全流程导航员**。
> 代码编辑是核心，上架交付是终点，每一步都有实战经验护航。

## 核心理念

| 与其他鸿蒙技能的区别 | 本工坊的做法 |
|-------------------|------------|
| 只给 API 文档索引 | ✅ **确保代码能编译通过**（31项自检清单） |
| 只贴示例代码 | ✅ **告诉你为什么这样写、哪里会踩坑** |
| 只覆盖 API 23 | ✅ **API 22~26 全版本，含 HarmonyOS 7** |
| 开发完不管上架 | ✅ **从签名打包到 AGC 审核全流程覆盖** |
| 文档搬运型 | ✅ **来自真实项目的踩坑记录，非文档整理** |
| 让你自己找代码 | ✅ **30个即用模板 + 5个高级模式，复制即跑** |

---

## 🎯 能力边界与最佳使用

> **本节帮助你快速判断：这个技能能不能解决你的问题，以及怎么问效果最好。**

### 能力边界（能做什么 × 不能做什么）

| ✅ 我能帮你做 | ❌ 我帮不了 / 需要你自己做 |
|:---|:---|
| 写 ArkTS 代码并确保编译通过 | 替你运行 IDE 或真机调试 |
| 诊断编译错误并给出修复方案 | 访问你本地项目文件或 Git 仓库（除非你粘贴内容） |
| API 迁移（旧→新）+ 废弃警告 | 保证第三方 SDK/ohpm 包的 API 正确性（以官方文档为准） |
| AGC 上架流程指导 + 审核被拒分析 | 代你提交审核、代你处理华为账号/签名证书 |
| 性能优化建议 + 内存泄漏排查 | 做压力测试/性能基准测试（需要你自己跑） |
| UI 组件选型 + 布局方案设计 | 做 UI 视觉设计/出设计稿（我是代码助手不是设计师） |
| 多设备适配 + 折叠屏布局 | 测试所有真机设备的兼容性（需要你自测） |
| CI/CD 构建脚本编写 | 维护你的 CI/CD 服务器或处理构建环境问题 |
| 从其他平台（Android/iOS/Web）迁移到鸿蒙 | 一键自动转换整个项目（需要逐步迁移，我逐模块协助） |

**简单判断法**：如果你要的是**写代码、改代码、查错、上架指导** → 找我；如果你要的是**操作 IDE、操作 AGC 控制台、真机测试、服务器运维** → 这些需要你自己动手。

### 最佳提问方式（怎么问效果最好）

| 你想做什么 | ❌ 低效问法（泛泛而谈） | ✅ 高效问法（精准命中） |
|:---|:---|:---|
| 解决编译错误 | "帮我看看这个报错" | "API 26 编译报错 Error XXXX，这是我的代码片段和完整错误信息" |
| 写一个功能页面 | "帮我写个登录页" | "API 25 登录页：手机号输入框 + 验证码按钮 + Account Kit 华为账号一键登录，用 Navigation 跳转" |
| API 迁移 | "把我的 Android 代码改成鸿蒙" | "将这段 Kotlin Retrofit 网络请求迁移为 ArkTS @ohos.net.http，保持回调语义" |
| 上架问题 | "上架被拒了怎么办" | "AGC 审核被拒，原因是 XXX（附截图），我的应用是 XX 类目，包名 com.xxx" |
| 性能优化 | "我的 App 很卡" | "列表 1000 条数据滑动掉帧，当前用的 ForEach + @State 数组，想优化为 LazyForEach" |
| 选型咨询 | "鸿蒙状态管理用哪个好" | "跨 5 个页面共享用户信息，需要持久化，推荐 @StorageLink 还是 AppStorage？" |
| 多端适配 | "适配折叠屏" | "折叠屏展开态显示双栏布局（列表+详情），收起态单栏，用 BreakpointType 怎么实现？" |

**提问黄金公式**：
```
[目标版本] + [具体场景] + [当前做法/报错] + [期望效果]
例："API 26 + 碰一碰分享图片 + 当前 share() 回调没触发 + 希望实现 PC 精准坐标定位"
```

### 版本选择速查

| 你的目标设备/场景 | 推荐 minSDKVersion | 说明 |
|:---|:---:|:---|
| 兼容绝大多数旧设备（含 HarmonyOS 4 及以下） | API 22 | 覆盖 99%+ 设备，但无法使用新能力 |
| 主流开发（平衡兼容性与新特性） | **API 23**（默认） | 覆盖 94%+ 设备，组件和 API 最成熟 |
| 使用元服务/自由流转等较新能力 | API 25 | 需 HarmonyOS NEXT 5.0+ |
| 使用 HarmonyOS 7 最新能力（Agent/VibeCoding/碰一碰精准分享等） | **API 26** | 仅 HarmonyOS 7 设备，新项目首选 |

> 💡 **不确定版本？** 告诉我你的目标用户群体和最低支持设备，我帮你定。

---

## 📖 知识体系

> ⚡ **快速定位**：[编码规范](#1-arkts-编码规范核心铁律) · [常见编译错误](#2-propstate-属性名基类冲突常见错误-10505001) · [API迁移](#3-废弃-api-迁移对照重点) · [自检清单](#4-编译自检清单代码输出前逐项检查) · [API 26 新能力](#6-harmonyos-7-api-26-新能力详解) · [互动卡片摇一摇](#69-更多-api-26-新能力补充) · [状态管理](#7-arkts-v2-状态管理装饰器api-26) · [高级架构](#8-高级架构与性能实战复杂场景深度指南) · [上架指南](#10-agc-上架全流程指南从代码到商店) · [踩坑记录](#11-真实踩坑记录来自实战项目非文档搬运) · [代码模板](#12-代码模板库30-个即用模板--5-个高级模式) · [对话示例](#-真实对话示例快速上手)

### 1. ArkTS 编码规范（核心铁律）

- **命名**：类/枚举/命名空间 → UpperCamelCase；变量/方法 → lowerCamelCase；常量 → SCREAMING_SNAKE_CASE
- **格式**：2空格缩进，单引号优先，行宽≤120，控制语句必须用大括号
- **TS→ArkTS 禁止项**：❌ any/unknown ❌ var ❌ 解构赋值 ❌ 函数表达式 ❌ 生成器 ❌ 运行时增删属性 ❌ 结构类型兼容 ❌ @ts-ignore ❌ 嵌套函数 ❌ 函数中 this 引用
- **数组类型**：使用 `T[]`（不用 `Array<T>`）
- **泛型**：必须显式标注，禁止隐式 any
- **可访问性**：类属性加 `private`/`protected`/`public`
- NaN 判断用 `Number.isNaN()`，不用 `===`

### 2. @Prop/@State 属性名基类冲突（常见错误 #10505001）

`@Component struct` 继承自 `CustomComponent`，ArkUI 链式方法（`.width()/.height()/.borderRadius()` 等）均为基类属性。同名 @Prop/@State 会覆盖基类签名导致编译错误。

**高频冲突属性名（13个）**：
| 冲突属性 | 推荐替换名 | 说明 |
|---------|-----------|------|
| `width` | `itemWidth` | `.width()` 为基类方法 |
| `height` | `itemHeight` | `.height()` 为基类方法 |
| `borderRadius` | `cornerRadius` | `.borderRadius()` 为链式方法 |
| `fontSize` | `textSize` | `.fontSize()` 为 Text 方法 |
| `fontColor` | `textColor` | `.fontColor()` 为 Text 方法 |
| `backgroundColor` | `bgColor` | `.backgroundColor()` 通用方法 |
| `margin` | `outerMargin` | `.margin()` 为布局方法 |
| `padding` | `innerPadding` | `.padding()` 为布局方法 |
| `align` | `contentAlign` | `.align()` 为布局方法 |
| `justifyContent` | `mainAxisAlign` | Flex 布局方法 |
| `alignItems` | `crossAxisAlign` | Flex 布局方法 |
| `direction` | `flexDirection` | Flex 方向 |
| `onClick` | `handleTap` | `.onClick()` 为事件方法 |

### 3. 废弃 API 迁移对照（重点）

| 旧API | ✅ 新API | 严重 |
|------|---------|:---:|
| `router.pushUrl()` | `UIContext.getRouter()` / Navigation | 🔴 |
| 全局 `animateTo()` | `this.getUIContext().animateTo()` | 🔴 |
| `console.log/info` | `@ohos.hilog` | 🟡 |
| `@ohos.fileio` | `@ohos.file.fs` (CoreFileKit) | 🔴 |
| `@ohos.notification` | `@ohos.notificationManager` | 🟡 |
| `camera.Camera` | `CameraManager + Session` | 🔴 |
| `globalThis` | `UIContext` / `AppStorage` / `LocalStorage` | 🔴 |
| `promptAction.showToast()` 全局 | `this.getUIContext().getPromptAction().showToast()` | 🟡 |
| 全局 `getContext(this)` | `this.getUIContext().getHostContext()` | 🟡 |
| `window.getTopWindow()` 回调 | `windowStage.getMainWindow()` Promise | 🟡 |

### 4. 编译自检清单（代码输出前逐项检查）

> 📋 **5 类共 31 项**，代码输出前按此逐项勾选，可拦截 **90%+** 的常见编译错误。

| 分类 | 关键检查项 | 最容易忘的 ⚠️ |
|:---|:---|:---|
| **语法（6项）** | 无 var、无 any、无解构、无函数表达式、无嵌套函数、无 @ts-ignore | `for...in` 和解构赋值是 AI 生成代码的重灾区 |
| **API（7项）** | UIContext、Navigation、file.fs、notificationManager、hilog、CameraManager、util | `globalThis` 在 API 26 已移除 |
| **组件（6项）** | @Entry 唯一、LazyForEach、StorageLink 默认值、对象字面量接口、Navigation、IDataSource | @Prop/@State 与基类属性名冲突（见第 2 节 13 个高频冲突名） |
| **泛型（6项）** | 泛型显式标注、返回类型显式、无内联对象字面量、Record 规范、API 返回接口化 | `httpClient.get()` 必须写 `httpClient.get<object>()` |
| **性能（6项）** | 循环常量提取、无稀疏数组、无联合类型数组、数值安全、可选→默认参数、catch 类型注解 | ForEach 改 LazyForEach 是最常见的性能优化点 |

### 5. API 版本演进概要

| 版本 | 关键能力 |
|-----|---------|
| API 22 | 最低兼容（99%+ 设备） |
| API 23 | 主流覆盖（94%+），多数通用组件 |
| API 24 | 6.1.1 新增能力 |
| API 25 | 元服务增强、自由流转 |
| API 26 | Vibe Coding、沉浸光感、3DGS、空格音频、Agent 框架、碰一碰精准分享、互动卡片、DID、数字盾 |

### 6. HarmonyOS 7 (API 26) 新能力详解

> 以下能力基于 2026年6月 HDC 发布的 HarmonyOS 7 正式版，覆盖智能化、全场景、多窗交互、安全、性能、设计语言六大方向。

#### 6.1 🤖 智能化

| 能力 | 说明 | 开发要点 |
|------|------|---------|
| **Agent 框架** | intent 编排 + Tool 执行 + memory 管理，支持 A2A 接入 | `@kit.AgentKit`，Agent 注册到系统智能入口 |
| **Vibe Coding** | 用自然语言描述功能，AI 生成 Skill 代码 | 调测→审核→上架全流程 AI 加持 |
| **视觉 AI Kit (Core Vision)** | 7 大能力：通用文字识别、人脸检测/比对、主体分割、多目标识别、骨骼点检测、图像超分 | `@kit.CoreVisionKit`，端侧 NPU 推理，无需联网 |

**Core Vision Kit 7 大能力速查**：
- **通用文字识别**：扫描身份证、银行卡、车牌号等场景，支持竖排/弯曲文本
- **人脸检测/比对**：活体检测 + 1:1 人脸比对，支付/门禁场景
- **主体分割**：人像抠图、商品背景替换，输出 Alpha 掩码图
- **多目标识别**：同时检测画面中多个物体并分类
- **骨骼点检测**：人体 17 个关键点坐标，健身/运动姿态分析
- **图像超分**：低分辨率图像 2x/4x 放大，老照片修复等场景

#### 6.2 📱 碰一碰·精准分享

> 基于 Share Kit，结合 NFC 近场通信 + 分布式软总线，设备轻触即可传输内容。
> API 26 新增 PC/平板精准定位：手机触碰电脑屏幕时识别目标窗口和坐标，图片等素材可精准插入。

**完整 API 规格**（`@kit.ShareKit`，Stage 模型，起始版本 5.0.0）：

**harmonyShare 模块结构**：
- `on('knockShare', callback)` — 注册碰一碰监听
- `on('knockShare', capability: SendCapabilityRegistry, callback)` — PC/平板带窗口ID注册
- `off('knockShare', callback?)` — 取消监听（不传 callback 清空所有）
- 还有 `gesturesShare`（隔空传送）和 `dataReceive`（沙箱接收）两个事件

**核心接口**（每个方法都有详细规格）：

```typescript
import { harmonyShare, systemShare } from '@kit.ShareKit';
import { uniformTypeDescriptor as utd } from '@kit.ArkData';

// ① 注册碰一碰监听（推荐带 windowId 的版本）
const capabilityRegistry: harmonyShare.SendCapabilityRegistry = {
  windowId: 123,         // ⚠️ 必填：当前窗口 ID
  sendOnly: false,       // 可选：true=仅发送不接收，默认false
};
harmonyShare.on('knockShare', capabilityRegistry, async (target: harmonyShare.SharableTarget) => {
  // ② 构造分享数据（3种卡片模板由参数组合自动决定）
  const shareData = new systemShare.SharedData({
    utd: utd.UniformDataType.HYPERLINK,   // 统一数据类型标识
    content: 'https://your.app.link/page',  // 分享内容 URI/URL
    // 以下字段影响卡片模板，详见注释：
    title: '分享卡片标题',       // + description + thumbnailUri → 决定卡片布局
    description: '分享卡片描述', // 与 title 配合触发沉浸式大卡或白卡布局
    thumbnailUri: fileUri.getUriFromPath(filePath), // 预览图 URI
  });

  // ③ 发送分享数据（返回 Promise<void>）
  await target.share(shareData);
});

// ④ 生命周期：onPageShow() 注册，onPageHide() 取消
harmonyShare.off('knockShare', capabilityRegistry, this.callback);
```

**3 种卡片模板（由参数自动决定）**：

| 卡片模板 | 判定条件 | 布局 |
|:--------|---------|------|
| **纯图片布局** | 仅传 `thumbnailUri` | 全屏预览图 |
| **沉浸式大卡** | 传 `title + description + thumbnailUri`，且**预览图宽高比 < 1:1** | 大图+标题+描述 |
| **白卡上下布局** | 传 `title + description + thumbnailUri`，且**预览图宽高比 > 1:1** | 上方小图+下方文字 |

**预览图规范**：
- 海报类来源：推荐 3:4 比例，最小 600×800 px，最大 3000×4000 px
- 用户上传图片：不限制比例，最大 3000×4000 px
- 预览图过大会导致加载慢，过小会模糊

**SharableTarget 完整方法集**：

| 方法 | 起始版本 | 说明 |
|:----|:-------:|------|
| `share(data: SharedData): Promise<void>` | 5.0.0 | 发送分享数据 |
| `reject(error: SharableErrorCode): Promise<void>` | 5.0.3 | 拒绝本次分享，向用户显示错误原因 |
| `updateShareData(data: UpdatedData): Promise<void>` | 6.0.0 | 延迟更新预览图（云端图片场景） |
| `clarifyNonShare(info: SharableErrorInfo): Promise<void>` | 6.0.2 | 告知用户当前无可分享内容并引导 |
| `getInfo(): SharableTargetInfo` | **26.0.0 Beta** | 获取PC精准坐标（screenX, screenY） |

**SharableErrorCode 枚举**：
| 值 | 含义 |
|:--:|------|
| `NO_CONTENT_ERROR = 1` | 无内容可分享 |
| `NO_INTERNET_ERROR = 2` | 无网络连接 |
| `DOWNLOAD_ERROR = 3` | 下载失败 |

**ShareResultCode 枚举**（接收端回调）：
| 值 | 含义 |
|:--:|------|
| `SHARE_SUCCESS = 0` | 传输成功 |
| `SEND_FAILED = 1` | 发送失败 |
| `CANCEL_BY_SENDER = 2` | 发送端取消 |
| `CANCEL_BY_RECEIVER = 3` | 接收端取消 |

**PC 精准分享（API 26 Beta）**：
- `target.getInfo()` 返回 `SharableTargetInfo.coordinate` 包含 `screenX` 和 `screenY`（屏幕左上角为原点的整数坐标）
- 接收端也有对应的 `ReceivableTarget.getInfo()` 返回 `ReceivableTargetInfo`

**云端预览图延迟更新模式**：
```typescript
// ① 先发送核心数据（使用默认预览图）
await target.share(shareData);
// ② 云端图片下载完成后，更新预览图（必须在数据发送前更新）
setTimeout(async () => {
  await target.updateShareData({ thumbnailUri: localFilePath });
}, 5000);
```

**异常场景处理**：
```typescript
// 当前界面无可分享内容
harmonyShare.on('knockShare', (target) => {
  target.clarifyNonShare({ message: '请在有分享内容的界面重试' });
});

// 下载失败等异常
harmonyShare.on('knockShare', (target) => {
  target.reject(harmonyShare.SharableErrorCode.DOWNLOAD_ERROR);
});
```

**生命周期必须成对**：`onPageShow` 注册 → `onPageHide` 取消。不取消会导致页面隐藏后仍在响应碰一碰事件。

**安全策略**（HarmonyOS NEXT 5.0.0.123 SP16+）：
- 对端已登录华为账号 → 展示对方昵称和头像
- 对端未登录 → 展示设备信息

#### 6.3 🪟 闪控窗体系（HarmonyOS 多窗交互）

闪控窗体系分三层：**实况窗（Live View）**、**闪控球（FloatingBall）**、**标准悬浮窗（FloatingWindow）**。三者定位不同，可联动使用。

#### 6.3.1 闪控球（FloatingBall，API 20+）

> 模块：`@kit.ArkUI` → `floatingBall` | 受限权限：`ohos.permission.USE_FLOAT_BALL`（ACL申请）
> 仅手机和平板，仅应用在前台时可启动。同一应用只能启动一个，同一设备最多两个。

**4 种模板**：
| 模板 | 支持内容 | 可更新 |
|:----|---------|:-----:|
| `STATIC`（静态布局） | 图标 + 标题 | ❌ 创建后不可更新 |
| `NORMAL`（普通文本布局） | 标题 + 内容 | ✅ |
| `EMPHATIC`（强调文本布局） | 图标 + 标题 + 内容 | ✅ |
| `SIMPLE`（纯文本布局） | 标题（最多双行） | ✅ |

**规格**：整体宽 70~98vp，高 40vp，不支持自定义字体大小。

**完整 API 流程**：
```typescript
import { floatingBall } from '@kit.ArkUI';
import { Want } from '@kit.AbilityKit';

// ① 检查设备是否支持
const isEnabled = floatingBall.isFloatingBallEnabled();

// ② 创建控制器
const controller: floatingBall.FloatingBallController =
  await floatingBall.create({ context: this.getUIContext().getHostContext() });

// ③ 注册事件
controller.on('click', () => {
  // 点击闪控球 → 恢复主窗口
  const want: Want = { bundleName: 'com.example.app', abilityName: 'EntryAbility' };
  controller.restoreMainWindow(want);
});
controller.on('stateChange', (state: floatingBall.FloatingBallState) => {
  if (state === floatingBall.FloatingBallState.STOPPED) {
    controller.off('click');     // 停止后清理监听
    controller.off('stateChange');
  }
});

// ④ 启动闪控球
await controller.startFloatingBall({
  template: floatingBall.FloatingBallTemplate.NORMAL,
  title: '比价中',
  content: '已找到 3 个平台报价',
  backgroundColor: '#0ff77c',      // 可选
});

// ⑤ 更新内容
await controller.updateFloatingBall({
  template: floatingBall.FloatingBallTemplate.NORMAL,
  title: '比价完成',
  content: '最低 ¥299，点击查看',
});

// ⑥ 停止闪控球
await controller.stopFloatingBall();
// 🚨 生命周期：aboutToDisappear 中必须停止，否则泄漏
```

**交互行为**：
- 单击 → `click` 事件 | 长按 → 变为待删除态 | 拖动 → 自动吸附侧边
- 位置记忆：关闭后记录位置，下次启动恢复；旋转屏幕/重启恢复默认（右上侧）
- 删除：拖到屏幕底部中部的垃圾桶区域松手

**闪控球 vs 标准悬浮窗**：闪控球是**受限能力**（需 ACL 权限、指定场景），而标准悬浮窗是 API 26 Beta 新增的**通用悬浮窗口**（暂无官方 API 文档完整公开）。普通开发者建议优先使用闪控球。

#### 6.3.2 实况窗进度环模板（Live View，API 26 新增）

```typescript
import { liveView } from '@kit.LiveViewKit';
const card = liveView.createCard({
  template: liveView.templates.ProgressRing,
  data: { title: '下载中', progress: 0.73, subtitle: '剩余 2 分钟' }
});
// ⚡ 节流：最多每秒更新一次，避免频繁重绘
if (Date.now() - lastUpdateTime > 1000) {
  card.update({ data: { progress: currentPercent } });
}
```

#### 6.3.3 闪控窗联动设计模式

三个层级展示同一数据源（推荐 `@Observed` 共享对象），信息分级展示：
- **一级**（最精简）：状态栏图标 / 实况窗摘要
- **二级**（中等详情）：实况窗展开 / 闪控球展开
- **三级**（完整交互）：标准悬浮窗 / 应用主界面

#### 6.4 🛡️ 安全新能力

| 能力 | 说明 | 适用场景 |
|------|------|---------|
| **星盾机密风控引擎** | 端侧 TEE 机密空间计算风控，数据"可用不可见" | 支付/转账/虚拟资产 |

**星盾机密风控引擎（API 26+）— 官方 API 规格**：
- 模块：`@kit.DeviceSecurityKit` → `riskControlEngine`
- 权限：需在 AGC 手动开通"星盾机密风控引擎"开关 + 申请 Profile
- 限制：每应用每设备每天最多 10 次
- 设备：Phone、Tablet、PC/2in1

**核心接口（仅 2 个）**：
```typescript
import { riskControlEngine } from '@kit.DeviceSecurityKit';
import { cryptoFramework } from '@kit.CryptoArchitectureKit';
import { util } from '@kit.ArkTS';

// ① 生成 nonce（16-66 字节，base64 编码，防重放攻击）
const rand = cryptoFramework.createRandom();
const randData = rand.generateRandomSync(32);
const base64 = new util.Base64Helper();
const nonce = base64.encodeToStringSync(randData.data);

// ②（可选）导入应用专属风险因子
await riskControlEngine.importRiskFactors({
  appFactorData: [
    { factorName: "payment_amount", factorValue: 12800 },
    { factorName: "is_new_device",  factorValue: false },
  ],
  nonce: nonce,
});

// ③ 发起风控评分
const response = await riskControlEngine.getRiskControlResult({
  policyName: "Policy_1001",  // 在 AGC 配置的风险策略名称
  nonce: nonce,
});
// 返回 JWS (JSON Web Signature) 格式，需在后端解析验证
```

**JWS 解析流程（在应用后端完成）**：
1. 解析 JWS 获取 Header/ Payload/Signature
2. Header 含 `alg: ES256`, `typ: JWS`, `x5c` 证书链（3 级）
3. 用华为 Root CA 验证证书链 → 用 x5c[0] 验证签名
4. Payload 含 `nonce`（防重放校验）+ `RiskDetectionOutput.status/result`

**其他安全 Kit 概要**：
| Kit | 能力 | API | 起始版本 |
|:----|:----|:----|:--------:|
| DID 分布式身份 | 系统级数字身份，TEE 存储颁发 | `@kit.DeviceSecurityKit` → `onlineAuthentication` | API 26 |
| 数字盾 | TEE 级可信签名/UI/输入 | `@kit.DeviceSecurityKit` → `deviceSecurity` | API 26 |
| 隐私防窥 | 智能屏幕防窥保护 | `@kit.DeviceSecurityKit` → `dlpAntiPeep` | API 23 |

**星盾引擎集成要点**：`@kit.DeviceSecurityKit` 的 `RiskAssessmentEngine`。初始化需 200~500ms（在 `UIAbility.onCreate` 中预初始化），依赖真实 TEE 硬件（模拟器不可用）。模型容量约 2MB，核心特征推荐 `DEVICE_INTEGRITY` + `BEHAVIOR_ANOMALY` 两个。

#### 6.5 ⚡ 性能与通信

| 能力 | 说明 | Kit |
|------|------|-----|
| **游戏快启** | 预加载 + 内核调度优化，冷启动提速 | HyperStartup |
| **冷启网络预建链** | App 启动时提前建立网络连接，减少首屏等待 | Network Boost Kit |
| **QUIC 长连接** | 基于 QUIC 协议的持久连接，弱网下更快恢复 | Remote Communication Kit |
| **弱网直播优化** | FEC + 动态码率，直播卡顿率降低 40%+ | Network Kit |
| **LTPO 可变帧率** | 根据内容动态调整刷新率 (1~120Hz)，功耗降低 30% | ArkGraphics 2D |

#### 6.6 🎨 设计语言进化

| 新特性 | 说明 | 适配建议 |
|--------|------|---------|
| **沉浸光感** | 材质的光学行为、空间属性与交互响应综合 | 核心界面（标题栏、导航）启用沉浸光感样式 |
| **可变字体** | 所有语言支持连续字重变化，粗细过渡细腻 | 替代固定字重，使用 `fontWeight: FontWeight.MEDIUM` 范围值 |

#### 6.7 🛠️ DevEco Code — 新一代 AI IDE

> HarmonyOS 7 的 DevEco Code 不是 DevEco Studio 的改名，而是基于 BitFun + OpenCode 构建的新 AI IDE。
> 覆盖研发全流程：需求设计 → 代码生成 → 功能验证 → 集成测试 → 运营维护，支持自定义模型。

| 对比 | DevEco Studio | DevEco Code |
|:----|:-------------:|:-----------:|
| 定位 | 传统 IDE | AI 原生 IDE |
| AI 能力 | 辅助（补全/提示） | 主导（生成/验证/测试） |
| Skill 开发 | 手动编码 | Vibe Coding 自然语言 |
| 模型 | 内置固定 | 支持自定义模型 |

**DevEco CLI**：命令行工具链，支持 CI/CD 集成，`deveco build/test/publish` 等命令。

#### 6.8 ⚠️ API 26 新能力异常处理速查

> 以下是碰一碰分享、闪控球、星盾引擎三个 API 26 核心新能力的常见异常场景和处理方案。

**碰一碰分享常见异常**：

| 异常现象 | 可能原因 | 解决方案 |
|:---|:---|:---|
| `knockShare` 事件不触发 | NFC 未开启 / 设备不支持 | 调用前检查 `nfcController.isNfcAvailable()` |
| `share()` 返回 `SEND_FAILED` | 对端设备不在线 / 传输超时 | 添加重试机制，最多 3 次，间隔 2s |
| `share()` 返回 `CANCEL_BY_RECEIVER` | 接收端主动取消 | 提示用户"对方已取消分享" |
| `thumbnailUri` 图片不显示 | 文件路径错误 / 文件过大 | 检查 URI 是否合法，预览图 ≤ 3000×4000 px |
| `updateShareData()` 不生效 | 在 `share()` 发送后才调用 | 必须**在 share 调用前**更新预览图 |
| PC 精准坐标 `getInfo()` 返回 0 | 非 PC 场景 / API 版本不够 | 确认设备为 PC + API 26 Beta+ |
| 页面关闭后仍在响应碰一碰 | 缺少 `off('knockShare')` 调用 | 检查生命周期：onPageShow 注册，onPageHide 取消 |

**闪控球常见异常**：

| 异常现象 | 可能原因 | 解决方案 |
|:---|:---|:---|
| `floatingBall.create()` 返回 null | 设备不支持 / ACL 权限未申请 | 检查 `isFloatingBallEnabled()` + `ohos.permission.USE_FLOAT_BALL` |
| `startFloatingBall()` 抛出权限异常 | ACL 权限未在 AGC 申请 | 在 AGC → 开发服务 → ACL 权限中申请 |
| 闪控球创建后不显示 | 应用不在前台 / 超过数量限制 | 确认应用在前台，同一设备最多同时显示 2 个 |
| `updateFloatingBall()` 对 STATIC 模板无效 | STATIC 模板不支持更新 | 改用 NORMAL / EMPHATIC / SIMPLE 模板 |
| `aboutToDisappear` 后闪控球未消失 | 未调用 `stopFloatingBall()` | 在 `aboutToDisappear` 中强制停止 |
| `restoreMainWindow()` 无响应 | Want 参数错误 | 检查 bundleName 和 abilityName 是否正确 |

**星盾引擎常见异常**：

| 异常现象 | 可能原因 | 解决方案 |
|:---|:---|:---|
| `getRiskControlResult()` 返回空 | 日调用次数超限（每天 10 次） | 限制调用频率，缓存前一次结果 |
| `importRiskFactors()` 超时 | TEE 环境初始化未完成 | 在 UIAbility.onCreate 中预初始化（需 200~500ms） |
| JWS 签名验证失败 | nonce 不匹配 / 证书链不一致 | 确认 nonce 与请求时一致，用华为 Root CA 验证 x5c |
| 模拟器上报错 | 星盾依赖真实 TEE 硬件 | 必须真机调试，模拟器不可用 |
| AGC 控制台找不到星盾开关 | 未在该应用下开通 | 在 AGC → 开发服务 → 星盾机密风控引擎 手动开通 |

#### 6.9 📱 更多 API 26 新能力补充

> 以下能力也是 HarmonyOS 7 新增的，但篇幅原因仅做概要说明。

**互动卡片摇一摇（API 26+）**：
互动卡片新增"摇一摇"触发方式——用户摇动手机即可激活卡片动画（静态→动态、前景元素出框），无需点击。
```json
// form_config.json 中配置
{
  "sceneAnimationParams": {
    "abilityName": "DeliveryLiveCardAbility",
    "triggerTypes": ["shake"]  // 支持摇一摇触发
  }
}
```
流程：用户摇动 → 系统查找配置了 `shake` 的卡片 → 触发 `FormExtensionAbility.onUpdateForm` → 调用 `formProvider.requestOverflow()` 激活互动卡片。
> **限制**：仅 HarmonyOS 7.0+ 生效。与点击触发的区别：摇一摇由系统识别事件，点击由 UI 层 `postCardAction(MESSAGE)` 触发。

**空间音频 / 音频编创（Audio Suite）**：
`@kit.AudioKit` → `OHAudioSuite`（C/C++ 接口，API 22+）。引擎 + 管线 + 节点三级架构，支持降噪、均衡器、人声分离、声音美化、环境效果、声场渲染、混音等效果节点。引擎最多 10 条管线，支持离线编辑和实时预览两种模式。
- 典型场景：直播推流降噪、音乐 App 自定义均衡器、短视频人声分离
- 参考 Sample：[audio-suite-sample](https://gitcode.com/HarmonyOS_Samples/guide-snippets/tree/HarmonyOS-7.0-beta-20260514/Media/Audio/AudioSuiteSample)

**3DGS 端侧重建**：
`@kit.ArkGraphics3D` → 空间建模与端侧 3D 重建，支持商品展示、文旅展陈等场景。端侧 NPU 推理，比云端方案延迟更低。API 26 新增。

**AGC 云调试验证（实用技巧）**：
在 AGC → 远程真机 → 云调试中，筛选 **API 26** 或 **系统版本 7.0.0.23** 的设备，上传 HAP 包即可远程调试验证 HarmonyOS 7 兼容性，无需真机。首次集成新 API 时强烈建议先跑云调试。 
> **入口**：AGC 控制台 → 我的项目 → 质量 → 云调试

**平行视界 EasyGo（API 26 新增）**：
大屏设备（平板/折叠屏展开态）的平行视界新增 EasyGo 能力，支持 1:2、2:1 分屏启动模式，以及购物模式、导航模式等路由模式。开发者通过配置文件接入，成本更低，体验更优。
- `@kit.AbilityKit` → 多窗口管理

**应用内分屏**：
大屏模式下支持应用内分屏，快速进入比价、辅助窗口模式，提升用户操作效率。
- 典型场景：购物 App 比价、笔记 App 双文档对照

**多设备 UX 自动检测**：
支持基于真机或模拟器开展多设备 UX 检测，自动发现大图大字、界面截断、重叠等典型布局问题。
- `DevEco Studio` → 设备 UX 检测工具

**DFX 维测工具增强**（DevEco Studio / 运维效率）：
| 能力 | 说明 |
|:---|:---|
| **APMS 故障诊断** | 商用版本故障总览 + 告警 + 根因分析 + 修复建议 |
| **DevEco Testing** | 支持内存泄漏问题快速激发测试 |
| **Profiler 全类型内存** | 一键抓取全类型内存泳道 + 跨语言内存调优 |
| **GWP-Asan / HWAsan** | 踩内存故障定位增强，支持跨语言栈缝合 |
| **Dump 文件解析** | 应用卡死/崩溃场景下的 Dump 文件智能解析 |
| **数据库可视编辑** | 数据库数据可视化编辑，SQL 智能联想 |

**Linux arm 版模拟器**：
新增支持 Linux arm 架构模拟器，Arm Mac（Apple Silicon）和 Linux arm 服务器可直接运行。

### 7. ArkTS V2 状态管理装饰器（API 26+）
|--------|------|
| `@ObservedV2` | 新版可观察数据类（替代 @Observed） |
| `@Track` | 标记 V2 类的可观察属性 |
| `@ComponentV2` | V2 组件装饰器 |
| `@Local` | V2 内部状态 |
| `@Param` | V2 父传子参数（替代 @Prop） |
| `@Event` | V2 子传父事件回调 |
| `@Monitor` | V2 状态变化监听 |
| `@Computed` | V2 计算属性 |
| `@Provider/@Consumer` | 跨层级状态传递（V2 八爪鱼模式） |
| `@LocalStorage` | 页面级持久化存储 |

### 8. 高级架构与性能实战（复杂场景深度指南）

> 针对中大型 App 的架构设计、性能瓶颈排查、多设备复杂适配等场景。
> 基础功能请参考第 11 节代码模板库；本节聚焦**架构决策和调优策略**。

#### 8.1 🏗️ ArkTS 架构模式

| 模式 | 适用场景 | ArkTS 实现要点 |
|:---|:---|:---|
| **MVVM** | 中大型 App、需要单元测试 | View = @Component struct；ViewModel = 普通类 + @Observable；Model = 数据层；通过 @Inject/@Provider 解耦 |
| **Repository** | 多数据源统一访问（网络+本地缓存） | Repository 类封装数据获取逻辑，内部判断走 RDB 缓存还是网络请求，对外暴露统一接口 |
| **单例管理** | 全局唯一实例（用户信息、网络客户端） | `class UserManager { private static instance: UserManager; static getInstance() { ... } }` |
| **事件总线替代** | 跨组件通信（非父子关系） | 用 `AppStorage` + `@Watch` 或 `emitter` 模块（`@ohos.events.emitter`）替代传统 EventBus |

**MVVM 快速脚手架**：
```typescript
// [API 23+] ViewModel 层 — 可被单元测试
@Observed
class LoginViewModel {
  @Trace phone: string = '';
  @Trace password: string = '';
  @Computed get isLoginEnabled(): boolean {
    return this.phone.length >= 11 && this.password.length >= 6;
  }
  async doLogin(): Promise<void> { /* ... */ }
}

// View 层
@ComponentV2
struct LoginPage {
  @Local viewModel: LoginViewModel = new LoginViewModel();
  build() {
    // 绑定 viewModel 属性，自动响应更新
  }
}
```

#### 8.2 ⚡ 性能优化清单

| 优化项 | 问题现象 | 解决方案 | 预期效果 |
|:---|:---|:---|:---|
| **长列表卡顿** | ForEach 渲染 >500 条时滑动掉帧 | 改用 `LazyForEach` + `IDataSource` + `ListItemGroup` 分组 | 帧率从 30fps → 55fps+ |
| **频繁重绘** | @State 大对象任意字段变化都触发整组件 rebuild | 拆分为多个细粒度 @State，或改用 `@Observed` + `@ObjectLink` 按需监听 | 减少 60%+ 无效渲染 |
| **首屏加载慢** | 白屏时间 >1.5s | ① 首屏数据预加载 ② 图片懒加载 ③ `onPageShow` 异步加载非关键数据 | 首屏 <800ms |
| **内存泄漏** | 页面退出后内存不释放（常见于 Timer/订阅） | `aboutToDisappear` 清理：`clearInterval()` / `.off()` / `http.destroy()` | 避免 OOM |
| **ANR 卡死** | 主线程执行耗时操作（大 JSON 解析/复杂计算） | 移至 `TaskPool.execute()` | ANR 率 → 0 |
| **HAP 包过大** | 安装包 >50MB | ① ohpm 按需引入（不用 `--all`）② HSP 动态共享包 ③ 图片压缩/WebP | 减小 30~50% |

**内存泄漏排查三步法**：
```
① DevEco Studio → Profile → Heap Snapshot 对比进入页面前后
② 找到引用链：谁还在持有已销毁页面的对象？
③ 最常见泄漏点：Timer 未清除 · 订阅未 off · http 未 destroy · 闭包隐式引用 @Component
```

**ArkUI 渲染优化原则**：
- `build()` 内不要做计算 → 提前在成员方法中算好
- 避免在 `build()` 内创建新对象（`new Xxx()` / `{ key: value }` 字面量）
- `if/else` 控制显隐优于 `visibility: Visibility.Hidden`（后者仍占布局空间）
- 长图片列表用 `CachedImage` 替代 `Image`（系统级缓存管理）

#### 8.3 📱 复杂多设备适配

| 场景 | 方案 | 关键 API |
|:---|:---|:---|
| **折叠屏展开/收起** | 监听折叠态切换布局 | `window.on('foldStatusChange')` + 断点枚举 |
| **平板双栏/手机单栏** | BreakpointType 条件布局 | `BreakpointType<'sm'|'md'|'lg'>` + `@AsMeasure` |
| **2in1 键盘/平板模式** | 检测鼠标/键盘输入方式 | `pointerDevice` + 输入法模式判断 |
| **车机窄屏适配** | 安全驾驶约束 | `DriveSafetyMode` + 简化 UI 交互 |

**折叠屏断点速查**：

| 设备状态 | 断点值 | 典型宽度 | 建议布局 |
|:---|:---|:---|:---|
| 手机折叠 | `sm` | <600vp | 单栏 |
| 手机展开/平板竖屏 | `md` | 600~840vp | 双栏（列表+详情） |
| 平板横屏/桌面 | `lg` | >840vp | 三栏或多面板 |

#### 8.4 🔗 分布式流转进阶

| 能力 | API | 适用版本 | 核心限制 |
|:---|:---|:---:|:---|
| **跨设备数据同步** | `@ohos.distributedDataObject` | API 9+ | 需同一华为账号登录 + 同一局域网 |
| **跨设备文件分享** | `@ohos.file.pasteboard` 分布式剪贴板 | API 10+ | 文件大小受限 |
| **跨设备拉起** | `startAbility()` + `deviceIds` | API 9+ | 目标设备需安装同应用 |
| **碰一碰精准分享** | `@kit.ShareKit` harmonyShare | API 26 | 见第 6.2 节完整规格 |

**分布式开发注意事项**：
- 必须处理**目标设备无响应**异常（设备离线/网络断开）
- 数据同步冲突策略：**最后写入胜出** 或 **自定义合并**
- 敏感数据流转前确认用户授权（隐私合规）

### 9. 弃用/移除公告（影响兼容性）

- **API 26 起正式移除**：`router.pushUrl()` → 强制使用 Navigation
- **API 26 起正式移除**：`globalThis` → 使用 UIContext/AppStorage/LocalStorage
- **API 26 起正式移除**：`@StorageLink` → 改用 `@LocalStorageProp`/`@LocalStorageLink`
- **API 25 起弃用**：`@ohos.data.preferences` → 改用 `@ohos.data.preferences` 新命名空间
- **迁移窗口**：旧 API 在 API 26 编译报错，不再仅警告

### 10. AGC 上架全流程指南（从代码到商店）

> ⚠️ 以下内容基于 2026-06-25 更新的官方审核 Checklist，覆盖从开发前备案到上架后维护的全链路。

#### 10.1 上架前准备

**必备账户与工具**：
- 注册华为开发者账号（实名认证）
- 登录 AppGallery Connect 控制台：https://developer.huawei.com/consumer/cn/service/jsp/agc/index.html
- DevEco Studio 中登录华为账号

**📋 APP备案（中国区上架必过项）**：
> 根据监管部门要求，所有在中国大陆上架的应用必须完成 APP 备案。

- 鸿蒙版备案：在接入商备案系统填写材料时**选择"鸿蒙"平台**，添加鸿蒙包名
- 多包名备案：如存在多个包名，或同时有 App 和元服务，**所有包名均需备案**（可添加多个）
- 备案信息一致性：备案时的主体信息、应用名称、包名必须与在架信息**完全一致**
- 无需备案：单机应用（不联网）、境外应用（境外主体+境外服务器）
- ⚠️ 填写主体证件号时注意区分：`5` vs `S`、`1` vs `I`、`0` vs `O`

**应用命名规范**：
- ❌ 禁止使用**泛词**：如"免费壁纸""电话""邮件""日历"等广义归纳词汇
- ❌ 禁止与其他应用名称/图标高度相似
- ✅ 应用名称建议 30 字以内，中英文
- ⚠️ **名称图标一致性**：提交到 AGC 的应用名称、图标必须与**安装后终端显示的一致**（不能提交叫"记事本"安装后叫"小记Pro"）

**雷同应用限制**：
- 如果市场已有大量同类应用（如敲木鱼、随机选择、计时器、计算器、手电筒、记事本、记账、天气），审核可能因"功能同质化严重"被拒
- 建议在核心功能上做出差异化

**应用基本信息准备**：
- 应用图标：1024×1024 PNG，**注意需要前景图和背景图两张**（layered_image）
- 应用截图：至少 3 张，最多 8 张。**不接受设计稿或带水印的截图**，状态栏不要出现其他 App 通知
- 应用描述（中英文，200-400 字，建议分点列出核心功能）
- 隐私政策链接（必须有！域名需已备案，内容须随功能更新同步更新）
- 应用一句话简介（20 字以内，说清楚 App 是干什么的）

**分类与资质**：
- 应用分类影响审核标准和推荐位
- 游戏类需要额外提供版号、著作权等资质文件
- 涉及新闻/金融/医疗等需提供行业资质
- **AIGC 内容标识**：如果应用涉及深度合成或生成式 AI，须在生成内容中添加**显式标识**（如水印）+ 文件元数据中加**隐式标识**，并提供相关资质文件

#### 10.2 签名、混淆与打包

**签名文件（.p12/.cer/.p7b）**：
```
DevEco Studio → Build → Generate Key/CSR
→ 创建 .p12 密钥库（别名、密码、有效期建议 25 年）
→ 生成 .cer 证书请求
→ 回传华为开发者联盟获取签名证书
→ 从 AGC 下载 .p7b Profile 文件
→ 配置到 build-profile.json5 的 signingConfigs
```

**签名配置（`build-profile.json5`）**：
```json5
{
  "app": {
    "signingConfigs": [{
      "name": "release",
      "type": "HarmonyOS",
      "material": {
        "certpath": "./signature/release.cer",
        "storePassword": "***",
        "keyAlias": "release",
        "keyPassword": "***",
        "profile": "./signature/release.p7b",
        "signAlg": "SHA256withECDSA",
        "storeFile": "./signature/release.p12"
      }
    }]
  }
}
```
⚠️ **签名密码不要硬编码提交到 Git**，使用环境变量或 CI/CD 密钥管理。

**🔐 代码混淆与加固**：
```json5
// build-profile.json5 中开启混淆
{
  "app": {
    "products": [{
      "name": "release",
      "obfuscation": {
        "ruleOptions": { "enable": true, "files": ["./obfuscation-rules.txt"] }
      }
    }]
  }
}
```
```
# obfuscation-rules.txt 常用规则
-enable-property-obfuscation
-enable-toplevel-obfuscation
-keep-global-name AppStorage,LocalStorage
```
⚠️ **混淆后 mapping 文件必须保存！** 否则线上 crash 堆栈无法反混淆定位问题。

**打包**：
```
Build → Build HAP(s) / APP(s)
→ HAP：单模块包（用于调试、内测），输出到 entry/build/default/outputs/
→ APP：整包（用于上架，含所有 HAP）
```
**版本号规范**：
- `versionCode`：整数，每次递增（如 1000001 → 1000002），**不可回退**
- `versionName`：语义化版本（如 1.0.0 → 1.0.1）
- 两者在 `build-profile.json5` 的 `products[].versionCode/versionName` 中配置

#### 10.3 AGC 上架步骤

```
AppGallery Connect 控制台 → 我的应用 → 创建应用
├─ 1. 填写应用基本信息（名称、包名、分类、语言等）
├─ 2. 上传 APP/HAP 包
├─ 3. 填写应用详情页（描述、截图、更新说明、隐私标签）
├─ 4. 填写隐私标签（如实填写收集哪些个人信息及使用目的）
├─ 5. 配置分发范围（全量/按地区/按设备）
├─ 6. 提供测试账号（如果应用需要登录）
├─ 7. 提交审核
└─ 8. 等待审核结果（首次 1-3 工作日，更新 1-2 工作日）
```

**📌 测试账号要求**：
- 如果应用需要登录才能使用，**必须提供测试账号**（在提审页面的"应用审核信息"处填写）
- 测试账号不能有**权限/角色/会员/付费限制**，必须能使用全部功能
- 确保审核人员可完成"登录 → 浏览 → 操作 → 退出"全流程

**📌 隐私标签服务**：
- 在 AGC 如实填写应用收集的个人信息项和使用目的
- 标签内容必须与隐私政策一致，标签与代码实际行为一致

**📌 上架自检（推荐）**：
- 提交邀请测试时，可**同步提交"上架自检"**
- 提前感知功耗、性能、兼容性、稳定性、UX、隐私等问题
- 发现问题可提前修改，加速正式上架

#### 10.4 审核被拒常见原因与修复

> 📊 统计显示：**备案、泛词名称、隐私政策、权限声明、截图质量** 占被拒原因的 TOP 5。

**🔴 必须解决（一票否决项）**：

| 拒绝原因 | 解决方案 |
|:---|:---|
| ❌ **APP 备案未完成** | 完成备案并在 AGC 正确勾选（鸿蒙版选"鸿蒙"平台） |
| ❌ **应用名称为泛词** | 修改为有识别性的名称，不能叫"免费壁纸""计算器"等 |
| ❌ **名称/图标与实际不一致** | 提交的名称图标必须与安装后显示的一致 |

**🟡 常见问题（修复即可重新提交）**：

| 类别 | 拒绝原因 | 解决方案 |
|:---|:---|:---|
| **资质/合规** | 隐私政策链接无效 | 确保链接可访问，域名已备案 |
| **资质/合规** | AIGC 未加标识 | 生成内容须加显式标识（水印）+ 隐式标识（元数据） |
| **资质/合规** | reason 字段缺少多语种 | 应用描述需同时提供中文和英文版本 |
| **权限** | 权限声明与实际不符 | `user_grant` 权限必须有明确使用场景说明（非废话式） |
| **权限** | 权限申请不合理 | 只申请真正需要的权限，等用户触发功能时再申请 |
| **UI/体验** | 截图与功能不符 | 截图必须反映实际 UI，不能使用设计稿 |
| **UI/体验** | 深色模式显示异常 | 在深色模式下测试 UI，确保文字对比度 ≥ 3:1 |
| **UI/体验** | 多设备适配问题 | 声明支持的设备类型必须全部适配通过 |
| **功能** | 功能不完整 | 按钮点了没反应、页面空白 → 提审前自我完整测试 |
| **功能** | 未提供测试账号 | 有登录功能时必须在审核备注中提供无限制的测试账号 |
| **签名** | 签名证书不一致 | 上架用签名必须与提包签名一致 |
| **元服务** | 元服务包过大 | 元服务 HAP ≤ 10MB，资源过多需拆分 |
| **隐私** | 隐私政策弹窗缺失 | 首次启动必须弹隐私协议，用户同意后才做数据收集 |
| **隐私** | 无账号注销入口 | 设置/账号页面必须提供"注销账号"功能 |
| **市场** | 市场已有大量雷同应用 | 在核心功能上做出差异化，避免纯工具类撞车 |

#### 10.5 上架后维护

- **版本更新**：先改 versionCode/versionName → 打包 → 上传 AGC → 提交审核
- **灰度发布**：大版本建议先灰度 20% 用户，观察无严重问题再全量推送
- **审核加急**：紧急修复可申请加急审核（每月有次数限制，别滥用）
- **AB 测试**：可在 AGC 配置应用内 AB 实验
- **Crash 监控**：集成 AGC Crash SDK，崩溃率超过 **1% 应立即修复**
- **性能监控**：关注启动时间、页面加载时间、ANR 率
- **用户评价管理**：定期看差评，差评里往往藏着真问题
- **合规同步更新**：新增数据收集场景时，同步更新隐私政策和隐私标签
- **热修复**：小 Bug 可通过 ArkTS 热修复能力修，不用重新打包上架；涉及 native 代码或资源文件必须走完整发版

#### 10.6 🔄 CI/CD 自动化（DevOps）

> hvigorw 是 Hvigor 构建系统的命令行入口，所有 IDE 里能做的构建操作都有对应的命令行参数。
> 格式：`hvigorw [taskNames...] <options>`

**4 个核心构建任务**：

| 任务 | 输出 | 用途 |
|:----|:----|:-----|
| `assembleHap` | .hap 文件 | 安装到设备（调试/内测） |
| `assembleApp` | .app 文件 | 上架应用市场（含所有 HAP） |
| `assembleHar` | .har 文件 | 发布到 ohpm 仓库的共享库 |
| `assembleHsp` | .hsp 文件 | 动态共享包（按需加载） |

**关键参数**：

| 参数 | 示例 | 说明 |
|:----|:----|:-----|
| `-p buildMode=release` | `assembleHap -p buildMode=release` | debug（默认，保留调试信息）/ release（开启混淆） |
| `-p product=default` | `-p product=release` | 指定 build-profile.json5 中的 product 配置 |
| `--mode module -p module=entry@default` | `-p module=entry@default` | 只编译指定模块，跳过无关模块 |
| `--no-daemon` | CI 环境推荐 | 不启动常驻进程，避免 CI 缓存问题 |
| `-p debuggable=true` | `-p debuggable=true` | release 模式保留调试能力（灰度测试用） |
| `--parallel` | 默认开启 | 并行构建互不依赖的模块 |
| `--no-incremental` | CI 环境有问题时回退 | 关闭增量编译，回退全量编译 |
| `--max-old-space-size=8192` | 大型项目 OOM 时 | 设置 Node.js 内存上限（MB） |
| `-d` / `--debug` | 排查构建失败 | 开启 debug 级别日志 |
| `--stacktrace` | 排查构建失败 | 打印完整异常堆栈 |

**标准 CI 流水线**（GitHub Actions / Jenkins）：
```yaml
# ① 安装依赖
ohpm install --all

# ② Code Linter
node codelinter/run/index.js .

# ③ 构建（release mode）
hvigorw assembleApp -p buildMode=release --no-daemon

# ④ 单元测试
hvigorw test -p module=entry --no-daemon

# ⑤ 上传 AGC（需 agconnect CLI 配置认证）
agconnect publish --file entry/build/default/outputs/entry-default-signed.app
```

**CI 环境注意事项**：
- 签名密码用 CI 平台的 Secret 变量（Jenkins Credentials / GitHub Actions Secrets），不要硬编码
- 环境变量：`NODE_HOME`、`JAVA_HOME`、`OHOS_SDK` 必须配置
- `ohpm install --all` 安装所有模块依赖；网络超时加 `--fetch_timeout` 和 `--retry_times`
- 增量编译：CI 全新 workspace 无缓存时 = 全量编译，需手动缓存 `build/` 和 `oh_modules/`

#### 10.7 🌐 国际化（i18n）

**资源目录结构**：
```
resources/
├── base/            # 默认（中文）
│   ├── element/string.json
│   └── media/
├── en_US/           # 英文
│   ├── element/string.json
│   └── media/
└── zh_TW/           # 繁体中文
    ├── element/string.json
    └── media/
```

**代码中引用**：`$r('app.string.xxx')` 框架自动根据系统语言选择

**日期/数字格式化**：
```typescript
// 日期格式化（自动适配地区）
let date = new Date();
let formatter = new Intl.DateTimeFormat('en-US');
let formatted = formatter.format(date);  // "6/16/2026"

// 数字格式化（千分位）
let numFormatter = new Intl.NumberFormat('de-DE');
let num = numFormatter.format(1234567.89);  // "1.234.567,89"
```

### 11. 🔴 真实踩坑记录（来自实战项目，非文档搬运）

> 以下踩坑来自 QuantFlow（鸿蒙股票App）和 pet-review（鸿蒙适配）等真实项目，每个都是编译报错→排查→修复的完整记录。这是本工坊与纯文档类技能的**最大区别**。

#### ① 20个编译错误 — 根因都在 API 层类型声明
```
QuantFlow 首次编译报 20 个错误，全部指向同一个根因：
http.ets 中 api 对象没有明确的 interface 类型声明
↳ 修复：定义 Api interface + 各接口类型 + 泛型显式标注
```
**教训**：API 层必须先声明接口类型，`httpClient.get()` 必须写成 `httpClient.get<object>()`

#### ② .ts vs .ets 文件体系差异
```
http.ts 中 AppStorage.get('token') 报错 → 因为 .ts 不能访问 ArkTS 全局对象
↳ 修复：.ets 中获取后通过普通变量同步到 .ts
```
**教训**：.ts 和 .ets 模块系统不同，跨文件共享状态需在 .ets 侧中转

#### ③ 编码损坏 → 伪编译报错
```
153 个编译错误的真实根因是文件编码损坏（非 UTF-8 BOM）
一��未闭合的中文字符串导致其后 50 行全报错
```
**教训**：遇到大量(>30个)连续语法错误，先检查文件编码，别逐条修复

#### ④ 659 个错误 — for...in 循环 + 对象索引访问
```
for (let key in obj) 在 ArkTS 中禁止
colors[key] 索引访问对象属性 → 必须用 Record<string, T>
```
**教训**：`for...in` 是 TS→ArkTS 迁移时 AI 最常生成的错误代码（与解构赋值、any 并列前三）

#### ⑤ 801 个错误 — import 位置导致装饰器截断
```
Index.ets 中 import 放在错误位置 → @Entry/@Component 装饰器被截断
→ 看似语法错误，实际是结构化问题
```
**教训**：遇到"装饰器不存在"报错时，先检查上方 import 是否完整

#### ⑥ 组件 API 误用
| 组件 | ❌ 错误用法 | ✅ 正确用法 |
|------|-----------|-----------|
| Row | `.alignItems(HorizontalAlign.Center)` | `VerticalAlign` |
| Toggle | `.isOn(true)` | `.selected(true)` |
| Column | `.borderBottomWidth(1)` | `.border({ bottom: { width: 1 } })` |
| build() | 内部声明 `const x = ...` | 必须用成员方法提前计算 |

#### ⑦ 批量替换踩坑（血的教训）
```
用 sed + Python 批量替换 router.pushUrl → 从 2 个 ERROR 弄到 689 个
根因：正则无法正确处理嵌套括号结构
```
**教训**：永远不要用正则批量替换有嵌套括号的代码。IDE 全局搜索 + 肉眼审查最安全

#### ⑧ 其他高频坑
- `@Prop` 修改 `user.name` 视图不动 → @Prop 是值副本，用 @Link 或事件回调
- `export` 修饰符缺失 → ArkTS 组件默认 internal，被其他模块引用须加 export
- ForEach 必须提供唯一键（第三个参数 `item => item.id`）
- Row/Column.alignItems 接受不同枚举类型（Row→VerticalAlign，Column→HorizontalAlign）

#### ⑨ API 26 新能力踩坑
> 以下踩坑来自实测 HarmonyOS 7 Beta 的碰一碰分享、闪控球、星盾引擎。

| 能力 | 坑 | 正确做法 |
|:---|:---|:---|
| **碰一碰分享** | 以为 `off('knockShare')` 不需要传 callback 就能全部清除 | 不传 callback 确实会清空，但**如果后续还要注册不同窗口的监听，必须显式传 callback** |
| **碰一碰分享** | `updateShareData()` 在 `share()` 之后调用，预览图不生效 | `share()` 调用前就要把预览图准备好，云端下载场景用 setTimeout 预更新再 share |
| **闪控球** | 用了 STATIC 模板后想更新内容，发现毫无变化 | STATIC 创建后不可更新，需要改 NORMAL/EMPHATIC 模板 |
| **闪控球** | 没有在 `aboutToDisappear` 中调用 `stopFloatingBall()` | 页面销毁后闪控球仍在，必须显式停止 |
| **星盾引擎** | 每天前 3 次调用正常，第 4 次开始返回空结果 | 每天每设备限 10 次，超限后不报错直接返回空，需要缓存结果 |
| **Account Kit** | 登录按钮样式在深色模式下白底白字看不清 | `LoginWithHuaweiIDButton` 自动适配主题色，但需检查应用中是否有强制覆盖样式 |
| **Account Kit** | `authorizeWithHuaweiID` 抛 SIGN_IN_FAILED | 99% 是 AGC 上配置的签名证书指纹 SHA256 不匹配 |

#### ⑩ 性能踩坑：@State 大对象 vs @Observed + @ObjectLink
```
踩坑：一个购物车对象 @State cart = { items: [], total: 0, discount: 0 }
改任意字段 → 全组件 rebuild，列表闪烁 + 性能下降 60%
↳ 修复：拆分为 @Observed CartModel + @ObjectLink 按需监听
```
**教训**：超过 3 个字段的对象不要直接用 @State，用 @Observed 装饰 class

### 12. 📋 代码模板库（30 个即用模板 + 5 个高级模式）

> 复制即用，每段带版本标注和完整 import。
>
> 🔍 **快速查找**：需要登录→#1 | 列表→#2 | 网络请求→#3 | 路由→#4 | 存储→#5 | 分页/刷新→#6-7 | 媒体→#8 | 搜索/表单→#9-10 | UI控件→#12-15 | 硬件能力→#16-26 | 系统→#27-30

#### 基础组件（#1~10：页面骨架）

| # | 模板 | 核心代码片段 |
|:-:|------|------------|
| 1 | **登录页** | `TextInput` + `Button` + loading 状态控制 |
| 2 | **LazyForEach 列表** | `IDataSource` + `List` + `LazyForEach(item => item.id)` |
| 3 | **网络请求** | `http.createHttp()` + `request()` + `destroy()` 确保资源释放 |
| 4 | **Navigation 路由** | `NavPathStack` + `pushDestinationByName` |
| 5 | **Preferences 存储** | `getPreferencesSync` + `putSync` + `flush` |
| 6 | **分页加载** | `page` 状态 + `loadMore()` 追加 + 触底检测 |
| 7 | **下拉刷新** | `Refresh({ refreshing: $$this.isRefreshing }).onRefresh()` |
| 8 | **图片选择上传** | `photoAccessHelper.selectPhotoUri(1)` |
| 9 | **搜索页** | `Search({ value: $$this.keyword }).onSubmit()` |
| 10 | **表单提交** | 验证 → `apiPost` → 提示 |

#### 功能组件（#11~30：业务能力）

> 🏷️ 倒计时/对话框→#11-12 | 底面板/轮播→#13-14 | 分享/扫码→#16-17 | 位置/通信→#18-21 | 传感器/认证→#24-26 | 后台/系统→#27-30

| # | 模板 | 核心 |
|:-:|------|-----|
| 11 | **倒计时** | `setInterval` + `@State countdown` |
| 12 | **确认对话框** | `AlertDialog.show()` |
| 13 | **底部面板** | `.bindSheet($$this.showSheet, ...)` |
| 14 | **轮播图** | `Swiper.autoPlay(true).interval(3000)` |
| 15 | **二维码生成** | `QRCode({ value: '...' })` |
| 16 | **分享** | `shareController.share()` |
| 17 | **扫码** | `scanCore.startScan()` |
| 18 | **位置获取** | `geoLocationManager.getCurrentLocation()` |
| 19 | **深色模式** | `config.colorMode === COLOR_MODE_DARK` |
| 20 | **拨打电话** | `call.makeCall()` |
| 21 | **发送短信** | `sms.sendMessage()` |
| 22 | **剪切板** | `pasteboard.getSystemPasteboard()` |
| 23 | **震动** | `vibrator.vibrate({ duration: 200 })` |
| 24 | **加速度传感器** | `sensor.on(sensor.SensorId.ACCELEROMETER)` |
| 25 | **生物认证** | `userIAM_userAuth.getAuthInstance()` |
| 26 | **网络状态监听** | `connection.on('netAvailable')` |
| 27 | **应用版本** | `context.getApplicationInfo()` |
| 28 | **后台定时任务** | `workScheduler.startWork()` |
| 29 | **键盘避让** | `setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)` |
| 30 | **文件下载（带进度）** | `request.downloadFile()` + `on('progress')` |

#### 高级模式（来自华为官方 Sample）

| 模式 | 说明 | 价值 |
|:----|------|:----:|
| **BreakpointType\<T\>** | 泛型断点配置器 | 一行代码替代5级 if-else |
| **CancelablePromise** | 异步竞态管理 | 防止连续快速操作时序错乱 |
| **AtomicService 签名** | 元服务证书链配置 | 元服务专用签名流程 |
| **折叠屏态检测** | `window.on('foldStatusChange')` | 展开/折叠布局切换 |
| **contentCover 封面取色** | `effectKit` 自适应颜色 | 动态主题色跟随封面 |

### 13. 🆚 鸿蒙 vs 其他平台速查（帮助开发者快速迁移）

> 💡 **从哪来？** Android 开发者关注：状态管理/路由/持久化/网络 | iOS 关注：UI框架/并发/推送 | Web 关注：语言差异/状态管理/DI
>
> ⚡ **最高频迁移场景**：`useState → @State` · `Retrofit → @ohos.net.http` · `React Router → Navigation` · `Coroutine → TaskPool`

| 概念 | Android | iOS/Swift | Web/React | **鸿蒙 ArkTS** |
|:-----|:-------:|:---------:|:---------:|:-------------:|
| **UI 框架** | XML + Jetpack Compose | SwiftUI | React/JSX | ArkUI 声明式 |
| **语言** | Kotlin/Java | Swift | TypeScript | **ArkTS（强类型 TS 超集）** |
| **状态管理** | ViewModel + StateFlow | @State/@Binding | useState/Redux | **@State/@Prop/@Link/@Provide** |
| **页面路由** | NavController/Intent | NavigationStack | React Router | **Navigation + NavPathStack** |
| **并发** | Coroutine/Thread | async/await + Task | Web Worker | **TaskPool + Worker** |
| **持久化** | Room/SharedPrefs | CoreData/UserDefaults | localStorage | **Preferences + KVStore + RDB** |
| **网络请求** | Retrofit/OkHttp | URLSession | fetch/axios | **@ohos.net.http + RCP** |
| **DI 依赖注入** | Hilt/Dagger | Swinject | Context | **@kit 模块化 + HAR 分包** |
| **推送** | FCM | APNs | WebSocket | **Push Kit** |
| **支付** | Google Pay | Apple Pay | Stripe | **IAP Kit** |
| **地图** | Google Maps | MapKit | Mapbox/Leaflet | **Map Kit** |
| **相机** | CameraX | AVFoundation | getUserMedia | **CameraManager + Session** |
| **蓝牙** | BluetoothAdapter | CoreBluetooth | Web Bluetooth | **@ohos.bluetooth** |
| **生物认证** | BiometricPrompt | LocalAuthentication | WebAuthn | **userIAM_userAuth** |
| **后台任务** | WorkManager | BGTaskScheduler | Service Worker | **workScheduler** |
| **上架市场** | Google Play | App Store | Web | **AppGallery Connect** |

> 💡 **迁移价值**：任何主流平台开发者都能在表格中找到对应概念，使用鸿蒙的思维不再是从零学习，而是"迁移已知知识"。

### 14. 📚 实战项目参考（来自 OpenHarmony 开源生态）

> 以下内容基于 OpenHarmony Gitee 组织（728 仓库）中与**应用开发**直接相关的项目提炼而成。
> 涵盖智慧家居、Codelabs 学习案例、趣味入门三大方向，全部可在 Gitee 找到源码。

#### 14.1 🏠 智慧家居实训项目集

> 来源：[OpenHarmony-SIG/knowledge_demo_smart_home](https://gitee.com/openharmony-sig/knowledge_demo_smart_home)（342 Stars，已归档迁移至 AtomGit）
> 覆盖从客厅到卧室的全场景智能家居，含连接模组类（15个）、带屏IoT（8个）、Camera应用（2个）、标准设备应用（7个）共 **32 个样例**。

**标准设备应用（最贴近 App 开发者）**：

| 项目 | 技术栈 | 核心能力 | 可用于参考的场景 |
|------|--------|---------|:-------------:|
| **数字管家 DistSchedule** | ArkTS, Stage | 分布式任务调度、设备协同 | 多设备协同 App |
| **智慧中控 eTS版** | eTS, Stage | 设备发现、控制指令下发 | IoT/设备控制类 App |
| **TodoList** | ArkTS | RDB 持久化、增删改查 | 通用数据管理 App |
| **Contacts 联系人** | ArkTS | 联系人管理、搜索过滤 | 带搜索功能的列表 App |
| **智能停车 CarParkTest** | ArkTS | 车位管理、状态展示 | 地图/位置类 App |
| **坚果食谱 NutRecipes** | ArkTS | 分类浏览、详情展示 | 内容浏览类 App |

**IoT 连接模组类应用架构模式**（可用于指导智能硬件开发）：
```
┌─────────────────────────┐
│  带屏设备（中控面板）      │ ← ArkUI 界面 + 控制指令
├─────────────────────────┤
│  分布式软总线 / MQTT      │ ← 设备发现 + 通信协议
├─────────────────────────┤
│  L0 无屏设备（灯/窗帘/风扇）│ ← C/OpenHarmony LiteOS
└─────────────────────────┘
```

**关键设计模式**：智能中控面板使用发布-订阅模式下发设备控制指令，设备端通过注册回调监听状态变化。这种模式同样适用于非 IoT 的 ArkTS App 组件通信。

#### 14.2 🎓 Codelabs 官方学习案例精选

> 来源：[OpenHarmony/codelabs](https://gitee.com/openharmony/codelabs) — 分享知识与见解，一起探索代码的独特魅力。
> 共 **50+ 个 Codelab 案例**，覆盖 UI、Ability、媒体、分布式、安全、数据库、卡片、三方库等全领域。

**优秀案例（推荐优先参考）**：

| 案例 | 技术栈 | 推荐理由 |
|------|--------|---------|
| **音乐专辑-多端部署** | ArkTS, API 9 | 一次开发多端部署的最佳实践样板，含 BreakpointType 断点适配 |
| **健康生活** | ArkTS, API 9 | 完整 App 架构：首页、数据、图表、设置，可作为 App 脚手架 |
| **视频应用-多端部署** | ArkTS, API 9 | 多设备视频播放，含媒体控制栏 + 多窗口适配 |
| **分布式手写板** | ArkTS, API 10 | 分布式数据对象实时同步，跨设备画布协作 |
| **分布式新闻客户端** | ArkTS, API 10 | 分布式数据跨设备访问，新闻列表 + 详情 = 多端同步 |

**按功能分类速查**：

| 类别 | 案例 | 可学知识点 |
|------|------|-----------|
| **UI（ArkTS）** | 电子相册、自定义抽奖转盘、简易计算器、购物应用 | Canvas 绘图、LazyForEach、Grid 布局、手势交互 |
| **Ability** | UIAbility生命周期、Stage页面跳转、Ability创建 | 生命周期回调、页面路由栈、Ability间通信 |
| **动画** | 动效示例、转场动画、自定义下拉刷新 | 属性动画、显式动画、Transition |
| **媒体** | 视频播放器、音乐播放器、图片编辑 | AVPlayer、媒体库 API、Image 编辑 |
| **分布式** | 分布式手写板、新闻客户端、游戏手柄、亲子早教 | DistributedDataObject、分布式网络、数据跨端 |
| **数据管理** | 关系型数据库、首选项、备忘录、应用内字体调节 | RDB、Preferences、数据持久化 |
| **安全** | 运行时权限、字符串加解密 | 权限请求、Cipher 加密 |
| **卡片** | 电影卡片、计步器卡片 | 卡片UI、定时刷新、点击事件 |
| **Native** | Native C++ 模板、XComponent 使用 | NAPI 接口、C++ 与 ArkTS 互调 |

> 💡 **使用建议**：当用户需要某个功能模块的完整实现时，优先从以上 Codelabs 案例中寻找对应的参考实现。例如：要做图片编辑功能 → 参考「图片编辑」Codelab；要做跨设备数据同步 → 参考「分布式手写板」。

#### 14.3 🎮 趣味极客入门项目

> 来源：[OpenHarmony-SIG/vendor_oh_fun](https://gitee.com/openharmony-sig/vendor_oh_fun) — "助燃你心中的极客梦想"
> 低门槛、高成就感的开源项目，适合向初学者展示鸿蒙的可能性。

| 项目 | 目标 | 适合向用户推荐的理由 |
|------|------|-------------------|
| **旧键盘改蓝牙键盘**（Neptune HID） | 用 OpenHarmony 开发板 + 杜邦线把旧键盘变成无线蓝牙键盘 | 极客范、成本低、零基础也能复现 |
| **BearPi 智能养花机**（BearPi+传感器） | 自动检测土壤湿度、自动浇水 | IoT 入门经典项目，软硬结合 |

> 💡 **使用建议**：当用户是初学者、对鸿蒙感到畏难时，用这些项目说明"不要被 700+ 仓库吓到，起步可以很小很酷"。
> 注意：这两个项目是 C/C++ 硬件开发（L0~L2 层），不是 App 开发。如果用户想了解纯软件趣味项目，推荐 14.2 中的「自定义抽奖转盘」「简易计算器」等 Codelabs 案例。

### 15. 👤 Account Kit 账号服务集成

> 华为账号一键登录基于 OAuth 2.0 + OpenID Connect。几乎所有 App 都需要。
> 核心模块：`@kit.AccountKit` → `authentication`（授权）+ `LoginWithHuaweiIDButton`（登录按钮组件）

**前置条件**：
1. AGC 控制台创建应用 → 开通 Account Kit
2. 配置签名证书指纹（SHA256，在 AGC "常规 → 应用 → 证书指纹" 处配置）
3. 获取 Client ID（在 AGC "常规 → 应用" 查看，若与 App ID 相同则无需额外配置）
4. 配置 `module.json5`：如 Client ID 与 App ID 不同，在 metadata 中配置 `client_id`
5. 申请权限：`quickLoginMobilePhone`（在 AGC "开发与服务" 中申请）

**一键登录（推荐方式 — 使用系统 UI 组件）**：
```typescript
import { LoginWithHuaweiIDButton, loginComponentManager } from '@kit.AccountKit';
import { BusinessError } from '@kit.BasicServicesKit';

// 在 UI 中使用 LoginWithHuaweiIDButton 组件
// 用户点击后自动拉起华为账号授权页，无需自己拼授权 URL
@Entry
@Component
struct LoginPage {
  build() {
    Column() {
      // 华为账号一键登录按钮（系统级 UI 组件）
      LoginWithHuaweiIDButton({
        controller: new loginComponentManager.LoginWithHuaweiIDController(),
        onSuccess: (code: string) => {
          // code = Authorization Code（一次性）
          // → 发送到应用后端换取 access_token + unionID + 手机号
          yourBackend.exchangeAuthCode(code);
        },
        onError: (err: BusinessError) => {
          console.error('登录失败:', err.code, err.message);
        },
      })
        .width(300).height(48);
    }
  }
}
```

**程序化授权（高级方式 — 自己控制 UI）**：
```typescript
import { authentication } from '@kit.AccountKit';

// 请求匿名手机号用于登录页展示
const request: authentication.AuthorizationWithHuaweiIDRequest = {
  scopes: ['openid', 'profile'],
  // 如需获取手机号需先在 AGC 申请 quickLoginMobilePhone 权限
};
const authResult = await authentication.authorizeWithHuaweiID(request);
// authResult 包含 authorizationCode（一次性，给后端换 token）
```

**后端验证流程**：
```
应用前端 → 获取 authorizationCode → 传给后端
后端 → 用 authorizationCode + clientSecret 调华为 OAuth 2.0 接口
   → 获取 access_token + refresh_token
   → 用 access_token 调用户信息接口
   → 获取 unionID（应用级唯一标识，用于关联用户数据）
   → 获取 openID（会话级临时标识，不要用于持久关联）
   → 获取手机号（需 quickLoginMobilePhone 权限）
```

**与旧版 API 的区别**：
- ❌ ~~`hwAccount.getAuthorization()`~~ 已不推荐使用
- ✅ `authentication.authorizeWithHuaweiID()` + `LoginWithHuaweiIDButton` 组件
- `LoginWithHuaweiIDButton` 是系统 UI 组件，自动适配华为账号登录界面的设计规范和交互流程

**常见错误码**：
- `CANCEL`：用户取消登录
- `NETWORK_ERROR`：网络异常
- `SIGN_IN_FAILED`：登录失败（检查签名指纹配置和 Client ID）

### 16. 🏭 行业实践参考（官方行业解决方案）

> 来源：华为开发者联盟「HarmonyOS行业解决方案」— 覆盖 17 个行业，提供从架构到常见问题的完整开发方案。
> 以下精选 5 个最常见行业进行概要说明。

| 行业 | 核心能力需求 | 涉及 Kit | 官方方案要点 |
|:----|------------|---------|-------------|
| **新闻阅读** | 富文本渲染、离线缓存、个性化推荐 | ArkUI, Network Kit, Preferences, Push Kit | 多端列表 + 详情架构、离线阅读策略 |
| **影音娱乐** | 视频播放、音频控制、投屏、DRM | Media Kit, AVSession, AVCodec | 播放器组件化、多窗口适配 |
| **便捷生活** | 地图、位置、支付、推送、卡片 | Map Kit, Location Kit, IAP, Push, Form Kit | 服务卡片集成、元服务快速入口 |
| **社交通讯** | 即时消息、音视频通话、文件传输 | Network, Push, Camera, Audio | WebSocket 长连接 + 消息可靠投递 |
| **购物比价** | 商品列表、搜索、支付、物流跟踪 | List, Search, IAP, LiveView, Map | 闪控窗比价、实况窗物流跟踪 |

**行业实践通用架构模式**：
```
┌─────────────────────────────────┐
│           UI 层 (ArkUI)          │ ← 多端适配（手机/平板/折叠屏）
├─────────────────────────────────┤
│      Ability 层 (Stage 模型)     │ ← UIAbility + ServiceExtAbility
├─────────────────────────────────┤
│        业务逻辑层 (Service Kit)    │ ← Account/Push/IAP/Map 等
├─────────────────────────────────┤
│     数据层 (Preferences/RDB/HSP)  │ ← 本地持久化 + 模块化共享
└─────────────────────────────────┘
```

### 17. 参考文件

详细知识存储在 `references/` 目录中：
- `references/arkts-patterns.md` — ArkTS 核心编程模式（泛型、异步、并发）
- `references/arkui-components.md` — ArkUI 组件最佳实践（布局、列表、弹窗等）
- `references/state-management.md` — 状态管理模式全集（V1/V2 装饰器对比）

---

## 🔧 使用说明

当用户提出鸿蒙开发相关问题时：
1. **明确阶段**：判断用户处于编码/调试/上架哪个阶段
2. **确认目标版本**：默认 API 23+，确认后标注到代码中
3. **代码是第一优先级**：用户需要代码时，先跑自检清单再输出
4. **检查废弃 API**：输出代码时自动扫描是否含旧 API
5. **版本标注**：每个代码块首行注释标注 API 版本：`// [API 23+] 说明`
6. **上架护航**：用户要发布时，按 AGC 章节逐项检查
7. **输出徽标**：代码末尾追加 `// ✅ 代码质量自检通过`

### 💬 真实对话示例（快速上手）

以下是 6 个典型场景的完整对话流程，帮助你快速理解本技能的工作方式：

**示例 1：编译错误修复**
```
用户：API 26 编译报错，Navigation 路由跳转不生效
      代码：router.pushUrl({ url: 'pages/Detail' })
      错误：Property 'pushUrl' does not exist

你：🔍 发现使用废弃 API router.pushUrl（API 26 已正式移除）
    ✅ 修复方案：改用 NavPathStack
    // [API 23+] Navigation 路由跳转
    const stack = new NavPathStack();
    stack.pushPath({ name: 'DetailPage' });
    
    Navigation() {
      ...
    }
```

**示例 2：新能力实现**
```
用户：API 26 碰一碰分享功能，NFC 触发后发一条链接

你：📱 碰一碰分享需要 3 步：
    1. onPageShow 注册 knockShare 监听
    2. 构造 SharedData（含 UTD 和 URL）
    3. onPageHide 取消监听
    然后给出完整 TypeScript 代码示例
```

**示例 3：性能调优**
```
用户：列表 500 条数据滑动卡顿，用的 ForEach

你：⚡ 建议改用 LazyForEach 懒加载
    ⚠️ 注意需要实现 IDataSource 接口
    ⚠️ 记得加第三个参数（唯一键）
    然后给出 IDataSource 实现 + List + LazyForEach 完整代码
```

**示例 4：上架问题**
```
用户：AGC 审核被拒，理由是"权限声明与实际不符"

你：📋 列出可能的原因：
    1. module.json5 中声明了用不到的权限
    2. 使用了 user_grant 权限但没有弹窗说明
    3. 隐私标签与代码实际行为不一致
    然后逐一给出检查步骤和修复方案
```

**示例 5：API 迁移**
```
用户：把这段 Kotlin 网络请求改成 ArkTS
     Retrofit 接口：GET /api/users, 返回 List<User>

你：🔄 ArkTS 使用 @ohos.net.http，写法如下：
    1. 定义 Response 接口
    2. http.createHttp() 发起请求
    3. destroy() 释放资源
    // [API 23+] 网络请求封装
```

**示例 6：架构咨询**
```
用户：跨 3 个页面共享购物车数据，需要实时同步

你：🏗️ 推荐方案：AppStorage + @Watch
    - 购物车数据存入 AppStorage（跨页面持久化）
    - 各页面用 @Watch 监听变化
    - 修改时自动同步到所有页面
    如果涉及多端流转，再加分布式数据对象方案对比
```