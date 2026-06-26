---
name: harmonyos-dev
description: >
  HarmonyOS 应用开发技能（覆盖 5.0~6.1 版本）。基于 ArkTS 语言，支持 Stage 模型应用开发、
  ArkUI 声明式 UI、UIAbility 生命周期、资源管理、权限配置、媒体处理、AI 集成、
  分布式流转等完整开发流程。当用户提到 HarmonyOS、鸿蒙应用开发、ArkTS、Stage模型、
  HAP/HAR/HSP 包开发、ArkUI 组件、分布式能力时触发。
trigger: HarmonyOS|鸿蒙|鸿蒙应用|ArkTS|Stage模型|HAP|HAR|HSP|ArkUI|UIAbility|DevEco|鸿蒙开发|harmonyos|HarmonyOS应用|分布式能力|AbilityKit|ohos.net|@kit
tags:
  - harmonyos
  - arkts
  - arkui
  - stage-model
  - harmonyos-dev
  - huawei
hermes:
  tags: [harmonyos, arkts, arkui, stage-model, harmonyos-dev, huawei, ability, hap, har, hsp]
  related_skills: [apple-design, frontend-design]
  version: "2.0.0"
  last_updated: "2026-04-23"
  source: |
    https://developer.huawei.com/consumer/cn/doc/harmonyos-guides
    https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts
    https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-basic-syntax-overview
    https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-configuration-file-stage
    https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/resource-categories-and-access
license: MIT
---

# HarmonyOS 开发技能

## 概述

HarmonyOS 是华为的分布式操作系统，应用默认使用 **ArkTS** 语言开发，基于 **Stage 模型**。

## 来源

> 来源：华为 HarmonyOS 开发者文档（2026-04-23 访问）
> - 文档中心：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides
> - ArkTS 语言：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts
> - ArkUI 框架：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-basic-syntax-overview
> - Stage 模型：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-configuration-file-stage
> - 资源管理：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/resource-categories-and-access
>
> 更新频率：随 HarmonyOS 版本迭代（当前覆盖 5.0~6.1）

---

## 快速开发路径

1. 环境：DevEco Studio（方舟开发编辑器）
2. 语言：ArkTS（TypeScript 超集，静态类型+声明式 UI）
3. 框架：ArkUI（声明式 UI 框架）
4. 模型：Stage 模型（推荐）

---

## 文档导航

### 入门
- [快速入门](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/quick-start)
- [应用开发导读](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-dev-guide)
- [开发基础知识](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/development-fundamentals)

### ArkTS 语言
- [初识 ArkTS](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-get-started)
- [ArkTS 语言介绍](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts) — 完整语法参考
- [ArkTS 编程规范](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-coding-style-guide)
- [ArkTS 迁移指导（从 TypeScript）](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/typescript-to-arkts-migration)
- [ArkTS 高性能编程](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-high-performance-programming)

### 应用框架
- [应用程序包概述](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-package-overview) — HAP/HAR/HSP
- [应用配置文件 Stage 模型](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-configuration-file-stage)
- [资源分类与访问](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/resource-categories-and-access)

### ArkUI
- [ArkUI 基本语法概述](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-basic-syntax-overview)
- [ArkUI 组件参考](https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-based-prefab-components)

---

# ArkTS 语言基础

## 核心概念速查

### ArkTS vs TypeScript 关键差异（API version 10+）

ArkTS 在 TS 基础上做了以下限制：
1. **强制静态类型** — 所有变量必须有确定类型，禁止运行期改变对象布局
2. **禁止 Structural Typing** — 不支持按结构匹配类型
3. **限制运算符语义** — 一元加法仅能作用于数字
4. **所有类型默认非空** — `let x: number = null` 编译错误，需声明为 `number | null`

### Module 类型（HAP/HAR/HSP）

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| HAP | HarmonyOS Ability Package | 应用主包，可安装 |
| HAR | HarmonyOS Archive | 静态共享库，编译时打包 |
| HSP | HarmonyOS Shared Package | 动态共享库，运行时共享 |

### 资源目录结构

```
resources/
├── base/
│   ├── element/      # 字符串、颜色、尺寸等元素资源
│   ├── media/        # 图片、音视频等媒体资源
│   └── profile/      # 自定义配置文件
├── zh_CN/            # 限定词目录（语言_地区-横竖屏-设备类型-颜色模式-屏幕密度）
├── dark/             # 深色模式
└── rawfile/          # 原始文件，不编译
```

资源访问：`$r('app.type.name')` 或 `$rawfile('path/file.png')`
系统资源：`$r('sys.type.name')`

---

# 典型开发流程

## 典型开发流程

1. **创建工程**：DevEco Studio 新建项目，选 Stage 模型 + ArkTS
2. **编写 UI**：`.ets` 文件，用 `@Component` + `build()` 声明 UI
3. **配置 Ability**：在 `module.json5` 中注册 UIAbility/EntryAbility
4. **管理资源**：在 `resources/` 下按限定词组织资源文件
5. **构建调试**：DevEco Studio 内置 hvigor 构建系统
6. **发布应用**：签名打包 HAP，通过 AppGallery Connect 发布

### 完整页面示例（ArkUI + MVVM）

```typescript
// Model
interface User {
  id: number;
  name: string;
  email: string;
}

// ViewModel（使用 TaskPool 进行网络请求）
import { taskpool } from '@kit.ArkTS';

@Concurrent
async function fetchUsersFromServer(): Promise<User[]> {
  // 模拟网络请求
  const response = await http.createHttp();
  const result = await response.request('https://api.example.com/users');
  return JSON.parse(result.result as string) as User[];
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
      // 标题栏
      Row() {
        Text('用户列表')
          .fontSize(24)
          .fontWeight(FontWeight.Bold)
        Blank()
        if (this.viewModel.isLoading) {
          ProgressView()
            .width(24)
            .height(24)
        }
      }
      .width('100%')
      .padding(16)
      .backgroundColor(Color.White)

      // 错误提示
      if (this.viewModel.error) {
        Text(`错误: ${this.viewModel.error}`)
          .fontColor(Color.Red)
          .fontSize(14)
          .padding(16)
      }

      // 用户列表
      List({ space: 10 }) {
        ForEach(this.viewModel.users, (user: User) => {
          ListItem() {
            this.UserItem(user)
          }
          .swipeAction({ end: this.DeleteAction(user.id) })
        }, (user: User) => user.id.toString())
      }
      .width('100%')
      .layoutWeight(1)
      .padding(16)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
    .onAppear(() => {
      this.viewModel.loadUsers();
    })
  }

  @Builder
  UserItem(user: User) {
    Row({ space: 12 }) {
      Column() {
        Text(user.name)
          .fontSize(17)
          .fontWeight(FontWeight.Medium)
        Text(user.email)
          .fontSize(14)
          .fontColor('#666666')
      }
      .alignItems(HorizontalAlign.Start)
      Blank()
      Text(`#${user.id}`)
        .fontSize(12)
        .fontColor('#999999')
    }
    .width('100%')
    .padding(16)
    .backgroundColor(Color.White)
    .borderRadius(12)
  }

  @Builder
  DeleteAction(id: number) {
    Button('删除')
      .type(ButtonType.Normal)
      .height('100%')
      ..width(80)
      .backgroundColor(Color.Red)
      .onClick(() => {
        // 删除逻辑
        const index = this.viewModel.users.findIndex(u => u.id === id);
        if (index >= 0) {
          this.viewModel.users.splice(index, 1);
        }
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

### 资源文件（resources/base/element/string.json）

```json
{
  "string": [
    {
      "name": "module_desc",
      "value": "用户列表演示应用"
    },
    {
      "name": "EntryAbility_desc",
      "value": "主入口Ability"
    },
    {
      "name": "EntryAbility_label",
      "value": "用户列表"
    }
  ]
}
```

---

# 架构与网络

## 架构模式

### ArkUI MVVM 架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    View     │ ←── │  ViewModel  │ ←── │   Model    │
│  (@Component)│     │ (@State/@Link)│     │ (interface) │
└─────────────┘     └──────────────┘     └─────────────┘
     build()              @State             数据结构
     @Builder            @Link               函数
```

**数据流向**：
1. View 通过 @State/@Link 绑定 ViewModel 的状态
2. ViewModel 处理业务逻辑，调用 Service/Repository
3. Model 定义数据结构（interface）
4. 状态变化自动触发 UI 重新渲染

### 状态管理对比

| 装饰器 | 作用域 | 继承 | 父传子 | 适用场景 |
|--------|--------|------|--------|---------|
| @State | 组件内 | ❌ | ❌ | 简单状态 |
| @Link | 组件内 | ❌ | ✅ | 双向绑定 |
| @Prop | 组件内 | ❌ | ✅单向 | 纯展示 |
| @ObjectLink | 组件内 | ✅ | ✅ | 复杂对象 |
| @StorageLink | 持久化 | ❌ | ❌ | 全局持久 |
| AppStorage | 应用级 | ❌ | ❌ | 全局状态 |

### 网络层封装

```typescript
// 统一网络服务
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

// 使用
const httpService = new HttpService();
const users = await httpService.get<User[]>('/users');
```

### 持久化方案

| 方案 | 适用场景 | 容量 | 性能 |
|------|---------|------|------|
| AppStorage | 键值对 | 小 | 高 |
| relationalStore | 结构化数据 | 中 | 中 |
| userinfoStore | 用户数据 | 中 | 中 |
| requestDataHelper | 简单存储 | 小 | 高 |

```typescript
// AppStorage 使用
AppStorage.setOrCreate('username', 'John');
const username = AppStorage.get<string>('username');

// 持久化存储
import { userinfoStore } from '@kit.ArkData';

let context = getContext(this);
const store = await userinfoStore.getUserinfoStorageInstance(context);
await store.insert('user', { name: 'John', age: 30 });
const result = await store.query('user', []);
```

### 路由管理

```typescript
import router from '@ohos.router';

// 路由配置（main_pages.json）
{
  "src": [
    {
      "name": "Home",
      "pageSourceFile": "./ets/pages/Home/Home.ets",
      "window": { "designWidth": 720 }
    },
    {
      "name": "Detail",
      "pageSourceFile": "./ets/pages/Detail/Detail.ets"
    }
  ]
}

// 路由跳转
router.pushUrl({ url: 'pages/Detail/Detail', params: { id: 123 } });

// 获取参数
const params = router.getParams() as { id: number };
```

### 依赖注入（Kit 方式）

```typescript
// 方式一：直接导入
import { UIAbility, AbilityConstant, Want } from '@kit.AbilityKit';

// 方式二：服务发现
import serviceDiscovery from '@kit.ArkUI';

// 方式三：@ohos 兼容方式（已废弃，不推荐）
import UIAbility from '@ohos.app.ability.UIAbility';
```

### 性能优化

| 场景 | 方案 | 说明 |
|------|------|------|
| 长列表 | LazyForEach | 懒加载，仅渲染可见项 |
| 图片 | Image + async load | 支持网络图片 |
| 数据持久化 | relationalStore | SQLite 数据库 |
| 并行任务 | taskpool | 多线程并行 |
| 预加载 | prefetch | 提前加载数据 |
| 减少刷新 | @ObjectLink | 细粒度更新 |

### 任务池（TaskPool）

```typescript
import { taskpool } from '@kit.ArkTS';

// 定义并发函数
@Concurrent
function heavyTask(numbers: number[]): number {
  return numbers.reduce((sum, n) => sum + n, 0);
}

// 执行任务
let task = new taskpool.Task(heavyTask, [[1, 2, 3, 4, 5]]);
let result = await taskpool.execute(task);

// 取消任务
taskpool.cancelTask(task);
```

### 测试策略

```typescript
// 单元测试（import test from '@kit.ArkTS'）
import test from '@kit.ArkTS';

@Entry
@Component
struct Calc {
  @State result: number = 0;

  add(a: number, b: number): number {
    return a + b;
  }
}

// UI 测试：使用 DevEco Studio 内置测试框架
// 性能测试：使用 hdc hilog 抓取性能日志
```

### 调试技巧

| 工具 | 用途 |
|------|------|
| DevEco Studio | 断点调试、日志查看 |
| hitrace | 分布式追踪 |
| hdc shell | 命令行调试 |
| AppGallery Connect | 远程调试、性能监控 |

```typescript
// 日志打印
import hilog from '@ohos.hilog';

hilog.info(0x0000, 'UserModule', 'User login: %{public}s', username);

// 条件断点
// 在 DevEco Studio 中设置条件表达式
```

---

## 快速参考

### ArkUI 常用组件速查

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
| Stack | 层叠布局 | `.alignContent()` |
| Flex | 弹性布局 | `.direction()`, `.wrap()` |
| Navigator | 路由导航 | `.target()`, `.type()` |
| Dialog | 对话框 | `.title()`, `.content()` |
| ActionSheet | 操作菜单 | `.actions()` |
| LoadingProgress | 加载指示器 | `.width()`, `.height()` |
| Badge | 徽章 | `.count()`, `.maxCount()` |
| Tabs | 标签页 | `.barPosition()`, `.controller()` |

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
| 字面量 | `'a' \| 'b' \| 'c'` | `type Direction = 'up' \| 'down'` |
| 函数 | `(params) => returnType` | `let fn: (n: number) => number` |
| 类 | `class Name { }` | `class User { name: string; }` |
| 泛型 | `Type<T>` | `let arr: Array<number>` |

### HarmonyOS 权限速查

| 权限 | 用途 | 级别 |
|------|------|------|
| ohos.permission.INTERNET | 网络访问 | normal |
| ohos.permission.GET_NETWORK_INFO | 获取网络信息 | restricted |
| ohos.permission.CAMERA | 相机 | restricted |
| ohos.permission.MICROPHONE | 麦克风 | restricted |
| ohos.permission.RECORD_AUDIO | 录音 | restricted |
| ohos.permission.READ_CONTACTS | 读联系人 | restricted |
| ohos.permission.WRITE_CONTACTS | 写联系人 | restricted |
| ohos.permission.LOCATION | 位置 | restricted |
| ohos.permission.STORAGE | 存储 | restricted |

### 常用 API 速查

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

### 布局速查

```typescript
// 垂直布局 Column
Column({ space: 10 }) {
  Text('Header')
  Row() { /* 内容 */ }
}
.width('100%')
.height('100%')
.alignItems(HorizontalAlign.Center)
.justifyContent(FlexAlign.Center)

// 水平布局 Row
Row({ space: 12 }) {
  Image('icon.png').width(24).height(24)
  Text('Label')
  Blank()
  Text('Value')
}
.width('100%')
.padding(16)

// 弹性布局 Flex
Flex({ direction: FlexDirection.Row, wrap: FlexWrap.Wrap }) {
  ForEach(items, (item) => {
    ItemComponent({ item: item })
      .width('30%')
      .margin(5)
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

### 生命周期速查

| 阶段 | 说明 | 回调 |
|------|------|------|
| 创建 | 组件创建 | `aboutToAppear()` |
| 渲染 | UI 构建 | `build()` |
| 销毁 | 组件销毁 | `aboutToDisappear()` |
| 页面显示 | 页面展示 | `onPageShow()` |
| 页面隐藏 | 页面隐藏 | `onPageHide()` |
| 权限变更 | 权限回调 | `onAbilityConnectDone()` |

### 版本兼容性速查

| 版本 | 支持特性 |
|------|---------|
| API 9 | 基础 ArkTS + Stage 模型 |
| API 10 | 增强类型系统 |
| API 11 | 性能优化 |
| API 12 | @kit 导入方式 |
| API 22 | HTTP 拦截器 |

---

# 常见 ArkTS 模式

### 常见 ArkTS 模式



### 状态管理
```typescript
@Entry
@Component
struct MyPage {
  @State message: string = 'Hello';
  build() {
    Column() {
      Text(this.message)
    }
  }
}
```

### 导入 HarmonyOS SDK
```typescript
// 方式一：Kit 方式（推荐）
import { UIAbility, Ability, Context } from '@kit.AbilityKit';

// 方式二：直接模块
import UIAbility from '@ohos.app.ability.UIAbility';
```

### 动态导入
```typescript
async function loadModule() {
  let module = await import('./Calc');
  module.add(3, 5);
}
```

---

# 参考文档

| 文件 | 内容 |
|------|------|
| `references/arkts-language.md` | ArkTS 完整语法（类型/函数/类/接口/泛型/运算符/语句/模块/注解） |
| `references/arkui-quickref.md` | ArkUI 组件、装饰器、布局、路由、生命周期、动画、手势 |
| `references/stage-config.md` | Stage 模型配置 + 窗口管理（UIAbility/子窗口/沉浸式/悬浮窗）|
| `references/app-package.md` | HAP/HAR/HSP 包结构、Stage 模型配置 |
| `references/resource-management.md` | 资源目录、$r/$rawfile/$sys 语法、限定词、overlay、AppStorage |
| `references/network-http.md` | HTTP 请求、WebSocket、文件上传下载、拦截器、证书配置 |
| `references/permission-testing.md` | 权限声明与动态请求、应用测试（单元/UI/性能）、签名发布流程、hvigor 构建 |
| `references/media-ai-distributed.md` | 媒体处理（image/video/audio）、Canvas、AI 能力、分布式数据、流转 |
|| `references/glossary.md` | HarmonyOS 核心术语表 |

---

# 避坑指南

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

---

# 输出格式规范

当使用本技能回答用户问题时，遵循以下格式：

### 回复结构
1. **直接回答** — 一段简洁的话给出核心答案
2. **代码示例** — ArkTS/ArkUI 示例代码（按需）
3. **避坑提醒** — 常见错误+正确做法
4. **文档链接** — 华为开发者文档相关链接（如适用）

### 示例回复（ArkTS 空安全）

> ArkTS 所有类型默认非空，`let x: number = null` 会编译错误。正确做法是声明为 `let x: number | null = null`。访问可空变量时用 `??` 合并操作符：`this.nick ?? ''`。如果确认变量有值，可用 `!` 非空断言，但需确保运行时不为空。

### 禁用格式
- ❌ 不要显式分层（避免"第一层/第二层/框架分析"等字眼）
- ❌ 不要长篇引用华为文档，要内化为自己的话
- ✅ 输出应是一段干净的话
