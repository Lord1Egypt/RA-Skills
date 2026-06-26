# HarmonyOS 开发技能

HarmonyOS 应用开发技能（覆盖 5.0~6.1 版本），基于 ArkTS 语言、Stage 模型、ArkUI 声明式 UI。

## 概述

本 skill 覆盖 HarmonyOS 完整开发知识体系，包括：

- **ArkTS 语言** — 静态类型、接口、泛型、并发、注解
- **ArkUI 框架** — 声明式 UI、组件、布局、动画、手势
- **Stage 模型** — UIAbility、窗口管理、生命周期
- **应用包结构** — HAP/HAR/HSP 模块划分
- **资源管理** — $r/$rawfile/$sys 语法、限定词、AppStorage
- **网络层** — HTTP、WebSocket、文件上传下载、拦截器
- **权限与安全** — 权限声明、动态请求、受限权限
- **媒体与 AI** — 图片/视频/音频、Canvas、分布式流转
- **测试与发布** — 单元测试、UI 测试、hvigor 构建、AppGallery Connect

## 核心章节

### 基础

| 章节 | 内容 |
|------|------|
| [ArkTS 语言基础](SKILL.md#ArkTS-语言基础) | ArkTS vs TypeScript 差异、模块类型、资源目录结构 |
| [典型开发流程](SKILL.md#典型开发流程) | DevEco Studio → ArkUI → 配置 Ability → 资源管理 → 构建发布 |

### 架构与网络

| 章节 | 内容 |
|------|------|
| [架构模式](SKILL.md#架构模式) | ArkUI MVVM、数据流向、状态装饰器对比 |
| [网络层封装](SKILL.md#网络层封装) | HttpService、http.createHttp()、请求配置 |
| [持久化方案](SKILL.md#持久化方案) | AppStorage、relationalStore、userinfoStore |
| [路由管理](SKILL.md#路由管理) | router.pushUrl()、pages.json 配置、参数传递 |
| [任务池](SKILL.md#任务池) | taskpool.Task、@Concurrent、并行计算 |

### 常见 ArkTS 模式

| 章节 | 内容 |
|------|------|
| [状态管理](SKILL.md#状态管理) | @State/@Link/@Prop/@ObjectLink/@StorageLink |
| [导入 HarmonyOS SDK](SKILL.md#导入-HarmonyOS-SDK) | @kit 方式（推荐）vs @ohos 方式（已废弃） |
| [动态导入](SKILL.md#动态导入) | import() 动态加载模块 |

### 参考文档

| 文件 | 行数 | 内容 |
|------|------|------|
| arkui-quickref.md | 518 | ArkUI 组件/装饰器/布局/路由/生命周期/动画/手势 |
| stage-config.md | 425 | UIAbility/窗口管理/子窗口/沉浸式/悬浮窗 |
| arkts-language.md | 383 | ArkTS 完整语法参考 |
| network-http.md | 317 | HTTP/WebSocket/上传下载/拦截器/证书 |
| media-ai-distributed.md | 308 | 媒体处理/Canvas/AI/分布式数据/流转 |
| permission-testing.md | 289 | 权限声明/动态请求/测试/签名发布/hvigor |
| resource-management.md | 273 | 资源目录/$r/$rawfile/$sys/限定词/overlay |
| app-package.md | 83 | HAP/HAR/HSP 包结构、Stage 模型配置 |
| glossary.md | 28 | HarmonyOS 核心术语表 |

## 快速参考

### ArkUI 常用组件

| 组件 | 用途 | 关键属性 |
|------|------|---------|
| Text | 文本显示 | `.fontSize()`, `.fontColor()`, `.fontWeight()` |
| Image | 图片 | `.src()`, `.width()`, `.height()`, `.borderRadius()` |
| Button | 按钮 | `.type()`, `.onClick()`, `.backgroundColor()` |
| TextInput | 输入框 | `.placeholder()`, `.text()`, `.onChange()` |
| List | 列表 | `ForEach`, `ListItem`, `.onScrollIndex()` |
| Grid | 网格 | `ForEach`, `ListItem`, `.columnsTemplate()` |
| Column | 垂直布局 | `.spacing()`, `.alignItems()` |
| Row | 水平布局 | `.spacing()`, `.justifyContent()` |
| Flex | 弹性布局 | `.direction()`, `.wrap()` |
| Stack | 层叠布局 | `.alignContent()` |
| Tabs | 标签页 | `.barPosition()`, `.controller()` |
| Dialog | 对话框 | `.title()`, `.content()` |
| Navigator | 路由导航 | `.target()`, `.type()` |

### ArkTS 类型速查

| 类型 | 语法 | 示例 |
|------|------|------|
| 基础类型 | `string`, `number`, `boolean` | `let name: string = 'John'` |
| 数组 | `Type[]` | `let nums: number[] = [1, 2, 3]` |
| 元组 | `[Type, Type]` | `let t: [string, number] = ['age', 30]` |
| 枚举 | `enum Name { A, B }` | `enum Color { Red, Blue }` |
| 接口 | `interface Name { }` | `interface User { id: number; name: string; }` |
| 可空 | `Type \| null` | `let x: number \| null = null` |
| 联合 | `A \| B \| C` | `let v: string \| number \| boolean` |
| 泛型 | `Type<T>` | `let arr: Array<number>` |

### 状态装饰器对比

| 装饰器 | 作用域 | 继承 | 父传子 | 适用场景 |
|--------|--------|------|--------|---------|
| @State | 组件内 | ❌ | ❌ | 简单状态 |
| @Link | 组件内 | ❌ | ✅ | 双向绑定 |
| @Prop | 组件内 | ❌ | ✅单向 | 纯展示 |
| @ObjectLink | 组件内 | ✅ | ✅ | 复杂对象 |
| @StorageLink | 持久化 | ❌ | ❌ | 全局持久 |
| AppStorage | 应用级 | ❌ | ❌ | 全局状态 |

### 布局速查

```typescript
// 垂直布局 Column
Column({ space: 10 }) {
  Text('Header')
  Row() { /* 内容 */ }
}
.width('100%').height('100%')
.alignItems(HorizontalAlign.Center)
.justifyContent(FlexAlign.Center)

// 水平布局 Row
Row({ space: 12 }) {
  Image('icon.png').width(24).height(24)
  Text('Label')
  Blank()
  Text('Value')
}
.width('100%').padding(16)

// 弹性布局 Flex
Flex({ direction: FlexDirection.Row, wrap: FlexWrap.Wrap }) {
  ForEach(items, (item) => {
    ItemComponent({ item: item }).width('30%').margin(5)
  })
}

// 层叠布局 Stack
Stack() {
  Background()
  Content()
  FloatingButton()
}
.alignContent(Alignment.BottomEnd)
```

### 生命周期

| 阶段 | 说明 | 回调 |
|------|------|------|
| 创建 | 组件创建 | `aboutToAppear()` |
| 渲染 | UI 构建 | `build()` |
| 销毁 | 组件销毁 | `aboutToDisappear()` |
| 页面显示 | 页面展示 | `onPageShow()` |
| 页面隐藏 | 页面隐藏 | `onPageHide()` |

### API 版本支持

| 版本 | 支持特性 |
|------|---------|
| API 9 | 基础 ArkTS + Stage 模型 |
| API 10 | 增强类型系统 |
| API 11 | 性能优化 |
| API 12 | @kit 导入方式（推荐） |
| API 22 | HTTP 拦截器 |

### 常用 API

| 功能 | 模块 | 方法 |
|------|------|------|
| HTTP请求 | `@kit.NetworkKit` | `http.createHttp()` |
| 文件操作 | `@kit.CoreFileKit` | `fileio` |
| 偏好设置 | `@kit.AbilityKit` | `AppStorage` |
| 弹窗 | `@kit.ArkUI` | `promptAction` |
| 路由 | `@kit.ArkUI` | `router` |
| 图片 | `@kit.MediaKit` | `image` |
| 视频 | `@kit.MediaKit` | `video` |
| 音频 | `@kit.MediaKit` | `audio` |
| 动画 | `@kit.ArkUI` | `animateTo` |
| 手势 | `@kit.ArkUI` | `gesture` |
| 线程池 | `@kit.ArkTS` | `taskpool` |

### 最小触摸目标

**44 × 44 vp**（约等于 44 × 44 pt）

## 完整示例

### ArkUI + MVVM 页面

```typescript
// Model
interface User {
  id: number;
  name: string;
  email: string;
}

// ViewModel
class UserListViewModel {
  @State users: User[] = [];
  @State isLoading: boolean = false;
  @State error: string = '';

  async loadUsers() {
    this.isLoading = true;
    this.error = '';
    try {
      const task = new taskpool.Task(fetchUsersFromServer);
      this.users = await taskpool.execute(task) as User[];
    } catch (e) {
      this.error = (e as Error).message;
    } finally {
      this.isLoading = false;
    }
  }
}

// View
@Entry
@Component
struct UserListPage {
  @State viewModel: UserListViewModel = new UserListViewModel();

  build() {
    Column() {
      Row() {
        Text('用户列表').fontSize(24).fontWeight(FontWeight.Bold)
        Blank()
        if (this.viewModel.isLoading) {
          ProgressView().width(24).height(24)
        }
      }
      .width('100%')
      .padding(16)
      .backgroundColor(Color.White)

      if (this.viewModel.error) {
        Text(`错误: ${this.viewModel.error}`)
          .fontColor(Color.Red).fontSize(14).padding(16)
      }

      List({ space: 10 }) {
        ForEach(this.viewModel.users, (user: User) => {
          ListItem() {
            this.UserItem(user)
          }
          .swipeAction({ end: this.DeleteAction(user.id) })
        }, (user: User) => user.id.toString())
      }
      .width('100%').layoutWeight(1).padding(16)
    }
    .width('100%').height('100%')
    .backgroundColor('#F5F5F5')
    .onAppear(() => { this.viewModel.loadUsers(); })
  }

  @Builder
  UserItem(user: User) {
    Row({ space: 12 }) {
      Column() {
        Text(user.name).fontSize(17).fontWeight(FontWeight.Medium)
        Text(user.email).fontSize(14).fontColor('#666666')
      }.alignItems(HorizontalAlign.Start)
      Blank()
      Text(`#${user.id}`).fontSize(12).fontColor('#999999')
    }
    .width('100%').padding(16)
    .backgroundColor(Color.White).borderRadius(12)
  }

  @Builder
  DeleteAction(id: number) {
    Button('删除')
      .type(ButtonType.Normal).height('100%').width(80)
      .backgroundColor(Color.Red)
      .onClick(() => {
        const index = this.viewModel.users.findIndex(u => u.id === id);
        if (index >= 0) { this.viewModel.users.splice(index, 1); }
      })
  }
}
```

### EntryAbility 配置（module.json5）

```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": ["phone", "tablet"],
    "deliveryWithInstall": true,
    "installationFree": false,
    "pages": "$profile:main_pages",
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ets",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:icon",
        "label": "$string:EntryAbility_label",
        "startWindowIcon": "$media:icon",
        "startWindowBackground": "$color:start_window_background",
        "exported": true,
        "skills": [
          {
            "entities": ["entity.system.home"],
            "actions": ["action.system.home"]
          }
        ]
      }
    ]
  }
}
```

### HTTP 网络请求

```typescript
class HttpService {
  private baseUrl = 'https://api.example.com';

  async request<T>(config: RequestConfig): Promise<T> {
    const http = http.createHttp();
    try {
      const response = await http.request(this.baseUrl + config.url, {
        method: config.method || 'GET',
        header: config.headers,
        extraData: config.body,
        connectTimeout: 30000,
        readTimeout: 30000
      });
      http.destroy();
      return JSON.parse(response.result as string) as T;
    } catch (e) {
      http.destroy();
      throw e;
    }
  }

  get<T>(url: string): Promise<T> {
    return this.request<T>({ url, method: 'GET' });
  }

  post<T>(url: string, body: object): Promise<T> {
    return this.request<T>({ url, method: 'POST', body });
  }
}
```

### TaskPool 并行任务

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function heavyTask(numbers: number[]): number {
  return numbers.reduce((sum, n) => sum + n, 0);
}

let task = new taskpool.Task(heavyTask, [[1, 2, 3, 4, 5]]);
let result = await taskpool.execute(task);
taskpool.cancelTask(task);
```

## 避坑指南

### ArkTS 编译期强制规则

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ `let x = null` | ✅ `let x: number \| null = null`（所有类型默认非空） |
| ❌ `obj instanceof Class` 用于接口 | ✅ instanceof 仅限 Class，不支持接口类型 |
| ❌ 对象字面量随意扩属性 | ✅ 禁止运行期改变对象布局 |
| ❌ 动态增加对象属性 | ✅ 静态类型禁止 |
| ❌ 一元加法用于非数字 | ✅ `+str` 会报错，一元加法仅能作用于数字 |

### ArkUI 运行时注意

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 在 `aboutToDisappear()` 修改状态 | ✅ 该方法禁止修改 `@State`，会触发 UI 异常 |
| ❌ `LazyForEach` 不提供唯一键函数 | ✅ 必须提供 `(item) => item.id` 类型的唯一键 |
| ❌ HTTP 请求忘记 `destroy()` | ✅ 每次请求后调用 `httpRequest.destroy()` 防内存泄漏 |
| ❌ `router.pushUrl()` 传复杂对象 | ✅ params 仅支持基本类型，复杂数据用 AppStorage |
| ❌ 组件内直接修改 `@Prop` | ✅ `@Prop` 是单向传递，只能父组件修改 |

### Stage 模型注意

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ `module.json5` 的 `srcEntry` 路径错误 | ✅ 路径相对于项目根目录，如 `./ets/entryability/EntryAbility.ts` |
| ❌ 混淆 `HAP`/`HAR`/`HSP` 用途 | ✅ HAP 可安装，HAR 编译时打包，HSP 运行时共享 |
| ❌ 免安装应用配置错误 | ✅ `installationFree: true` 时 `deliveryWithInstall` 必须为 `false` |
| ❌ 权限只声明不动态请求 | ✅ 敏感权限需同时声明和动态请求 |
| ❌ 多设备场景硬编码 deviceId | ✅ 空字符串 `''` 表示本设备，显式 deviceId 用于跨设备 |

### 版本陷阱

- ⚠️ **API v22+** — HTTP 拦截器需要 API version 22+
- ⚠️ **Kit 方式导入** — `@kit.AbilityKit` 是 API v22+ 推荐方式
- ⚠️ **注解限制** — 注解仅在 `.ets`/`.d.ets` 文件有效，release 混淆会被移除
- ⚠️ **注解字段类型** — 仅支持 `boolean/number/string` 及其数组
- ⚠️ **Flex 布局** — 默认不换行，需要 `wrap: FlexWrap.Wrap` 才能换行
- ⚠️ **Grid 循环** — `ForEach` 在 `Grid` 内必须配合 `ListItem()` 使用

## 来源

> 华为 HarmonyOS 开发者文档（2026-04-23 访问）
> - 文档中心：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides
> - ArkTS 语言：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts
> - ArkUI 框架：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-basic-syntax-overview
> - Stage 模型：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-configuration-file-stage
> - 资源管理：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/resource-categories-and-access
>
> 版本：HarmonyOS 5.0~6.1


