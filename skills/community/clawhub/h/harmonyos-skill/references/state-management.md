# ArkUI 状态管理模式（官方最佳实践）

## 1. @State（组件内状态）
```typescript
@Component
struct Counter {
  @State private count: number = 0;
  
  build() {
    Column() {
      Text('计数: ' + this.count)
        .fontSize(20)
      Button('+1')
        .onClick(() => {
          this.count++;
        })
    }
  }
}
```

## 2. @Prop（父→子单向传递）
```typescript
@Component
struct ChildComponent {
  @Prop message: string = '';  // 必须初始化
  
  build() {
    Text(this.message)
  }
}

@Component
struct ParentComponent {
  @State private text: string = 'Hello';
  
  build() {
    ChildComponent({ message: this.text })
  }
}
```

## 3. @Link（父子双向绑定）
```typescript
@Component
struct ChildComponent {
  @Link @Watch('onCountChanged') count: number;
  
  onCountChanged() {
    console.info('count changed: ' + this.count);
  }
  
  build() {
    Button('+1')
      .onClick(() => {
        this.count++;
      })
  }
}

@Component
struct ParentComponent {
  @State private count: number = 0;
  
  build() {
    ChildComponent({ count: $count })
  }
}
```

## 4. @Provide / @Consume（跨层级共享）
```typescript
@Component
struct GrandParent {
  @Provide('theme') @State theme: string = 'light';
  
  build() {
    Column() {
      ChildComponent()
    }
  }
}

@Component
struct GrandChild {
  @Consume('theme') theme: string;
  
  build() {
    Text('当前主题: ' + this.theme)
  }
}
```

## 5. @StorageLink（应用级持久化）
```typescript
@Component
struct AppSettings {
  @StorageLink('appTheme') private theme: string = 'light';
  @StorageLink('userId') private userId: string = '';
  
  build() {
    Column() {
      Text('主题: ' + this.theme)
      Button('切换主题')
        .onClick(() => {
          this.theme = this.theme === 'light' ? 'dark' : 'light';
        })
    }
  }
}
```

## 6. @LocalStorageLink（页面级持久化）
```typescript
@Component
struct PageSettings {
  @LocalStorageLink('pageState') private pageState: string = 'list';
  
  build() {
    if (this.pageState === 'list') {
      ListView()
    } else {
      DetailView()
    }
  }
}
```

## 7. @Watch（状态变化监听）
```typescript
@Component
struct PriceDisplay {
  @State @Watch('onPriceChange') price: number = 0;
  
  onPriceChange() {
    // 当 price 变化时自动调用
    this.updateDisplay();
  }
  
  build() {
    Text('¥' + this.price.toFixed(2))
  }
}
```

## 8. @BuilderParam（插槽模式）
```typescript
@Component
struct Card {
  @BuilderParam content: () => void = this.defaultContent;
  
  @Builder
  defaultContent() {
    Text('默认内容')
  }
  
  build() {
    Column() {
      this.content()
    }
    .padding(16)
    .backgroundColor(Color.White)
    .borderRadius(12)
  }
}

// 使用
Card() {
  Text('自定义卡片内容')
    .fontSize(16)
}
```

## 9. 常见错误模式

### ❌ 错误：直接修改对象属性
```typescript
@State private user: UserData = { name: '张三', age: 25 };

// 不会触发 UI 更新
this.user.name = '李四';

// ✅ 正确：重新赋值
this.user = { ...this.user, name: '李四' };
```

### ❌ 错误：直接修改数组元素
```typescript
@State private items: Array<string> = ['a', 'b', 'c'];

// 不会触发 UI 更新
this.items[0] = 'x';

// ✅ 正确：使用数组方法或重新赋值
this.items[0] = 'x';
this.items = [...this.items];
// 或
this.items.splice(0, 1, 'x');
```

### ❌ 错误：未初始化装饰变量
```typescript
@Prop message: string;   // 必须初始化
@Link count: number;     // 必须初始化

// ✅ 正确
@Prop message: string = '';
@Link count: number;
```

## 10. 状态管理选择指南

| 场景 | 推荐方案 | 说明 |
|:----|:---------|:------|
| 组件内部状态 | `@State` | 最简单，最常见 |
| 父→子传参 | `@Prop` | 单向，子组件只读 |
| 父子双向绑定 | `@Link` | 子组件可修改父组件状态 |
| 跨多层传递 | `@Provide` / `@Consume` | 不需要每层都传 prop |
| 应用级状态（全局） | `@StorageLink` | 跨页面/跨组件持久化 |
| 页面级状态 | `@LocalStorageLink` | 仅当前页面有效 |
| 状态变化响应 | `@Watch` | 观察状态变化执行逻辑 |
| 子组件模板插槽 | `@BuilderParam` | 类似 Vue slot / React children |
