# ArkUI 组件使用模式（官方最佳实践）

## 1. 基础布局组件

### Column（垂直布局）
```typescript
Column() { ... }
  .width('100%')
  .height('100%')
  .backgroundColor(Color.White)
  .alignItems(HorizontalAlign.Center)  // 水平对齐
  .justifyContent(FlexAlign.Center)    // 垂直对齐
  .padding(16)
  .borderRadius(8)
```

### Row（水平布局）
```typescript
Row({ space: 12 }) { ... }
  .width('100%')
  .height(40)
  .padding({ left: 16, right: 16 })
  .alignItems(VerticalAlign.Center)    // 垂直对齐
```

### Flex（弹性布局）
```typescript
Flex({ direction: FlexDirection.Column, wrap: FlexWrap.Wrap }) {
  Text('Item 1').layoutWeight(1)
  Text('Item 2').layoutWeight(2)
}
```

## 2. 显示组件

### Text（文本）
```typescript
// 基本用法
Text('Hello World')
  .fontSize(16)
  .fontWeight(FontWeight.Medium)
  .fontColor(ColorTheme.get(this.theme, 'TEXT_PRIMARY'))
  .textAlign(TextAlign.Center)
  .maxLines(2)
  .textOverflow({ overflow: TextOverflow.Ellipsis })

// 格式化金额
Text('¥' + price.toFixed(2))
  .fontSize(24)
  .fontWeight(FontWeight.Bold)

// ❌ 错误：不接受箭头函数
Text(() => { return 'hello'; })
```

### Image（图片）
```typescript
// 本地资源
Image($r('app.media.startIcon'))
  .width(48)
  .height(48)
  .borderRadius(24)
  .objectFit(ImageFit.Contain)

// 网络图片
Image('https://example.com/image.png')
  .width(200)
  .height(200)
  .alt('加载失败')

// URL 资源
Image($r('sys.media.ohos_ic_public_arrow_left'))
  .width(24)
  .height(24)
  .fillColor(Color.Gray)
```

### TextInput（输入框）
```typescript
TextInput({ placeholder: '请输入用户名' })
  .width('100%')
  .height(40)
  .type(InputType.Normal)
  .backgroundColor('#F5F5F5')
  .borderRadius(8)
  .padding({ left: 12 })
  .onChange((value: string) => {
    this.username = value;
  })
```

### Button（按钮）
```typescript
Button('登录')
  .width('100%')
  .height(44)
  .backgroundColor('#007AFF')
  .borderRadius(22)
  .fontColor(Color.White)
  .fontSize(16)
  .enabled(this.isFormValid)
  .onClick(() => {
    this.handleLogin();
  })
```

## 3. 导航与容器

### Tabs（标签页切换）
```typescript
Tabs({ barPosition: BarPosition.Start, index: 0 }) {
  TabContent() {
    Text('首页内容')
  }
  .tabBar('首页')
  
  TabContent() {
    Text('发现内容')
  }
  .tabBar('发现')
}
.width('100%')
.height('100%')
```

### List（列表）
```typescript
List({ space: 8, initialIndex: 0 }) {
  ForEach(this.items, (item: ItemData) => {
    ListItem() {
      Text(item.name)
        .width('100%')
        .padding(12)
        .backgroundColor(Color.White)
        .borderRadius(8)
    }
    .onClick(() => {
      this.selectItem(item);
    })
  }, (item: ItemData) => item.id)
}
.width('100%')
.layoutWeight(1)
```

### Scroll（滚动容器）
```typescript
Scroll() {
  Column() {
    // 内容组件
  }
  .width('100%')
}
.scrollBar(BarState.Off)
.scrollable(ScrollDirection.Vertical)
.edgeEffect(EdgeEffect.Spring)
```

## 4. 弹窗与提示

### 自定义弹窗
```typescript
@CustomDialog
struct ConfirmDialog {
  controller: CustomDialogController
  @State message: string = ''
  
  build() {
    Column() {
      Text(this.message)
        .fontSize(16)
      Button('确定')
        .onClick(() => {
          this.controller.close()
        })
    }
  }
}

// 使用
let dialog = new CustomDialogController({
  builder: ConfirmDialog({ message: '确认删除？' })
})
dialog.open()
```

### Toast（提示）
```typescript
import { promptAction } from '@kit.ArkUI';

promptAction.showToast({
  message: '操作成功',
  duration: 2000,
  bottom: 100
})
```

## 5. 加载与进度

### LoadingProgress（加载动画）
```typescript
LoadingProgress()
  .width(32)
  .height(32)
  .color('#007AFF')
```

### Progress（进度条）
```typescript
Progress({ value: this.progress, total: 100, type: ProgressType.Linear })
  .width('100%')
  .height(6)
  .color('#007AFF')
  .backgroundColor('#E5E5E5')
```

## 6. @Builder 自定义组件
```typescript
@Builder
private MyButton(label: string, color: ResourceColor) {
  Button(label)
    .width(100)
    .height(40)
    .backgroundColor(color)
    .borderRadius(8)
}

// 调用
Row({ space: 12 }) {
  Column() {
    this.MyButton('确定', '#007AFF')
  }
  .onClick(() => { this.confirm(); })
  
  Column() {
    this.MyButton('取消', '#999999')
  }
  .onClick(() => { this.cancel(); })
}
// ❌ 错误：不能在 @Builder 返回值上链式
// this.MyButton('确定').onClick(...)
```
