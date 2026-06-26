# ArkUI 快速参考

> 来源：华为开发者文档 - ArkUI 基本语法、Stage模型
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-basic-syntax-overview

## 基础结构

```typescript
@Entry        // 页面入口（可选）
@Component     // 自定义组件
struct MyPage {
  @State count: number = 0;

  build() {
    Column() {
      Text(`Count: ${this.count}`)
        .fontSize(50)

      Button('Increment')
        .onClick(() => {
          this.count++;
        })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
```

## 常用装饰器

| 装饰器 | 用途 |
|--------|------|
| `@Component` | 声明自定义组件 |
| `@Entry` | 页面入口（可传参数）|
| `@State` | 组件内状态（响应式）|
| `@Prop` | 父到子单向传值 |
| `@Link` | 父子双向绑定 |
| `@Watch` | 监听状态变化 |
| `@Provide` / `@Consume` | 跨组件层级状态共享 |
| `@StorageLink` / `@StorageProp` | 应用存储绑定 |
| `@Preview` | 预览装饰器 |
| `@AnimatableState` | 可动画状态 |
| `@LocalStorageLink` | 本地存储双向绑定 |

## 基础组件

```typescript
// 文本
Text('Hello')
  .fontSize(20)
  .fontColor('#333333')
  .fontWeight(FontWeight.Bold)
  .textAlign(TextAlign.Center)

// 输入框
TextInput({ placeholder: '请输入' })
  .type(InputType.Number)
  .onChange(v => { this.input = v; })

TextArea({ placeholder: '多行文本' })
  .onChange(v => { this.text = v; })

// 按钮
Button('点击', { type: ButtonType.Normal, stateEffect: true })
  .onClick(() => { })
Button('圆角按钮', { type: ButtonType.Capsule })

// 图片
Image($r('app.media.icon'))
  .width(100)
  .height(100)
  .borderRadius(8)

Image($rawfile('images/avatar.png'))
  .objectFit(ImageFit.Contain)

// 开关
Toggle({ type: ToggleType.Switch, isOn: this.enabled })
  .onChange(v => { this.enabled = v; })
```

## 布局容器

```typescript
// 垂直布局（默认）
Column({ space: 10 }) {
  Text('A')
  Text('B')
}
.width('100%')
.alignItems(HorizontalAlign.Center)
.justifyContent(FlexAlign.SpaceBetween)

// 水平布局
Row({ space: 8 }) {
  Image($r('app.media.icon'))
  Text('标题')
}
.height(60)
.alignItems(VerticalAlign.Center)

// 层叠布局
Stack() {
  Image(backImg)
  Text('叠加文字')
}
.alignContent(Alignment.Center)

// 弹性布局
Flex({ direction: FlexDirection.Row, wrap: FlexWrap.Wrap }) {
  // 内容...
}

// 网格布局
Grid() {
  ForEach(this.items, (item, index) => {
    GridItem() { Text(`${index}`) }
  })
}
.columnsTemplate('1fr 1fr 1fr')
.rowsTemplate('1fr 1fr')
.columnsGap(10)
.rowsGap(10)
```

## 列表

```typescript
List({ space: 10, initialIndex: 0 }) {
  ForEach(this.dataArray, (item: string, index: number) => {
    ListItem() {
      Row() {
        Text(`${index + 1}`)
          .fontSize(16)
        Text(item)
          .margin({ left: 12 })
      }
      .padding(12)
    }
    .swipeAction({ end: this.buildSwipeAction(index) })  // 滑动操作
  }, (item: string) => item)
}
.listDirection(Axis.Vertical)
.divider({ strokeWidth: 1, color: '#eee' })
.edgeEffect(EdgeEffect.Spring)
.onScrollIndex((start, end) => { })
```

## 循环与条件渲染

```typescript
// 循环渲染
ForEach(
  this.array,
  (item: string, index: number) => {
    Text(`${item} - ${index}`)
  },
  (item: string) => item  // 唯一键
)

// 条件渲染
if (this.isLoggedIn) {
  Text('已登录')
} else {
  Text('请登录')
}

// 显隐控制（比 if 更轻量，不销毁节点）
if (this.isVisible) {
  Text('可见')
}

// LazyForEach（大数据量优化，只渲染可见项）
LazyForEach(this.dataSource, (item: string) => {
  ListItem() { Text(item) }
}, (item: string) => item)
```

## 路由

```typescript
import router from '@ohos.router';

// 跳转（压栈）
router.pushUrl({ url: 'pages/Detail', params: { id: 1 } });

// 返回
router.pop();

// 替换当前页
router.replaceUrl({ url: 'pages/Home' });

// 替换并清栈
router.clear();

// 路由拦截（ Ability 内）
onForeground() {
  router.clear();
}

// 接收参数
onPageShow() {
  const params = router.getParams() as Record<string, number>;
  this.id = params['id'];
}
```

## Navigation（推荐，用于主客主备）

```typescript
import router from '@ohos.router';

// Navigation 路由（无需 import）
NavPathStack
navigationHome() {
  this.pathStack.pushPath({ name: 'Detail', params: { id: 1 } });
}

Navigation() {
  // 内容
}
.title('主页')
.mode(NavigationMode.Stack)
.backButtonIcon($r('app.media.icon'))
.onNavBarStateChange((isShown: boolean) => { })
```

## 生命周期

```typescript
// 页面生命周期
struct MyPage {
  aboutToAppear(): void { }     // 即将显示（可调用 this.setState）
  onPageShow(): void { }        // 页面已显示
  onPageHide(): void { }       // 页面已隐藏
  aboutToDisappear(): void { }  // 即将销毁（注意：不要在这里修改状态变量）

  build() { /* ... */ }
}

// UIAbility 生命周期（Stage 模型）
import UIAbility from '@ohos.app.ability.UIAbility';

class MyAbility extends UIAbility {
  onCreate(want, launchParam): void {
    // Ability 首次创建时调用
    console.info('Ability onCreate');
  }

  onDestroy(): void {
    // Ability 销毁时调用
    console.info('Ability onDestroy');
  }

  onWindowStageCreate(windowStage): void {
    // WindowStage 创建时调用（加载主页面）
    // windowStage 是舞台模型的窗囬管理器
    windowStage.loadContent('pages/Index', (err) => {
      // 加载页面内容
    });
  }

  onWindowStageDestroy(): void {
    // WindowStage 销毁时调用
  }

  onForeground(): void {
    // Ability 进入前台
  }

  onBackground(): void {
    // Ability 进入后台
  }

  onContinue(want): void | OnContinueResult {
    // 设备间迁移时调用
  }
}

// UIAbility 在 module.json5 中注册
// module.json5 的 srcEntry 指向 ./ets/entryability/EntryAbility.ets
```

## 弹窗

```typescript
// 警告对话框
AlertDialog.show({
  title: '提示',
  message: '确认删除？',
  autoCancel: true,
  alignment: DialogAlignment.Bottom,
  offset: { dx: 0, dy: -20 },
  confirm: {
    value: '确认',
    action: () => { }
  },
  cancel: {
    value: '取消',
    action: () => { }
  }
})

// 选择对话框
ActionSheet.show({
  title: '选择操作',
  buttons: [
    { text: '操作1', color: '#666666' },
    { text: '操作2', action: () => { } }
  ]
})

// 自定义弹窗
@CustomDialog
struct CustomDialogExample {
  controller: CustomDialogController = new CustomDialogController({ builder: '' })

  build() {
    Column() {
      Text('自定义内容')
    }
    .padding(20)
  }
}
```

## 动画

```typescript
// 属性动画
animateTo(
  { duration: 300, curve: Curve.EaseInOut },
  () => {
    this.scale = 1.1
  }
)

// 显式动画
animation({
  duration: 500,
  iterations: 1,
  playMode: PlayMode.Alternate
})

// 转场动画
TransitionEffect.OPACITY.animation({ duration: 300 })
TransitionEffect.translate({ y: 20 }).animation({ duration: 300 })
```

## 手势

```typescript
// 点击
.onClick(() => { })

// 长按
.onLongPress(() => { })

// 滑动
.gesture(
  PanGesture()
    .onActionStart((event: GestureEvent) => { })
    .onActionUpdate((event: GestureEvent) => { this.offsetX = event.localX })
    .onActionEnd(() => { })
)

// 捏合缩放
.gesture(
  PinchGesture()
    .onActionStart(() => { })
    .onActionUpdate((event: GestureEvent) => { this.scale = event.scale })
)

// 旋转
.gesture(
  RotationGesture()
    .onActionUpdate((event: GestureEvent) => { this.angle = event.angle })
)
```

---

## Tabs 组件（页签容器）

> 来源：华为开发者文档 - Tabs 组件参考
> https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-container-tabs

### 基础用法

```typescript
@Entry
@Component
struct TabsExample {
  @State currentIndex: number = 0;
  private controller: TabsController = new TabsController();

  build() {
    Tabs({ barPosition: BarPosition.Start, controller: this.controller }) {
      TabContent() {
        Text('首页内容').fontSize(20)
      }.tabBar('首页')

      TabContent() {
        Text('分类内容').fontSize(20)
      }.tabBar('分类')

      TabContent() {
        Text('我的内容').fontSize(20)
      }.tabBar('我的')
    }
    .barHeight(56)
    .onChange((index: number) => {
      this.currentIndex = index;
    })
  }
}
```

### 核心参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `barPosition` | `BarPosition.Start \| End` | TabBar 位置（顶部/底部）|
| `controller` | `TabsController` | 控制器，用于代码控制切换 |
| `index` | `number` | 当前显示的页签索引（双向绑定）|
| `vertical` | `boolean` | `false`=横向Tabs，`true`=纵向（侧边栏）|
| `scrollable` | `boolean` | 是否允许滑动切换 |
| `barMode` | `BarMode.Fixed \| Scrollable` | TabBar 布局模式 |
| `barWidth` | `Length` | TabBar 宽度 |
| `barHeight` | `Length` | TabBar 高度 |

### BarMode 布局模式

```typescript
// Fixed：所有 TabBar 平均分配宽度
Tabs({ barMode: BarMode.Fixed }) { ... }

// Scrollable：TabBar 可滑动，超出可滚动
Tabs({ barMode: BarMode.Scrollable }) { ... }

// Scrollable + 指定样式
Tabs({
  barMode: BarMode.Scrollable,
  scrollable: true
}) { ... }
```

### TabsController（代码控制）

```typescript
let controller: TabsController = new TabsController();

// 切换到指定索引
controller.changeIndex(2);

// 让 TabBar 平移/透明度
controller.setTabBarTranslate({ x: 10, y: 0 });
controller.setTabBarOpacity(0.8);

// 绑定双向索引
Tabs({ controller: controller, index: $currentIndex }) { ... }
```

### TabBar 样式

```typescript
// 文字 + 图标 TabBar
TabContent() {
  Text('首页')
}
.tabBar({
  icon: $r('app.media.icon_home'),
  selectedIcon: $r('app.media.icon_home_selected'),
  label: '首页'
})

// SubTabBarStyle（顶部页签样式）
.tabBar(SubTabBarStyle.of('首页')
  .selectedColor('#FF0000')
  .unselectedColor('#999999')
  .indicator({ color: '#FF0000', height: 2 }))

// BottomTabBarStyle（底部导航样式）
.tabBar(BottomTabBarStyle.of($r('app.media.icon'), '首页'))
```

### 常用事件

```typescript
// 页签切换回调
.onChange((index: number) => {
  console.info(`切换到: ${index}`);
})

// TabBar 点击回调
.onTabBarClick((index: number) => {
  console.info(`点击: ${index}`);
})

// 动画开始/结束回调
.onAnimationStart((index: number, targetIndex: number) => { })
.onAnimationEnd((index: number) => { })
```

### 纵向 Tabs（侧边栏）

```typescript
Tabs({ vertical: true, barPosition: BarPosition.Start }) {
  TabContent() { Text('内容').fontSize(24) }
  .tabBar('功能一')
  TabContent() { Text('内容2').fontSize(24) }
  .tabBar('功能二')
}
.barWidth(80)    // 侧边栏宽度
.barHeight(200)  // 侧边栏高度
```
