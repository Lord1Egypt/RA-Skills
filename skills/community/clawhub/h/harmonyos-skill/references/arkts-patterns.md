# ArkTS 核心编程模式（官方最佳实践）

## 1. 变量声明规则
```typescript
// ✅ 正确：显式类型注解
let count: number = 0;
let name: string = 'hello';
let items: Array<string> = [];

// ❌ 错误：隐式 any
let data = [];           // TS 风格，ArkTS 禁止
let result;              // 未初始化
```

## 2. 函数声明
```typescript
// ✅ 正确：显式返回类型
function add(a: number, b: number): number {
  return a + b;
}

// ✅ 方法声明
private computeValue(input: string): number {
  return input.length;
}

// ❌ 错误：隐式返回类型
private compute(input: string) { ... }
```

## 3. 对象字面量
```typescript
// ✅ 正确：Record 类型 + 索引赋值
const userInfo: Record<string, string> = {};
userInfo['name'] = '张三';
userInfo['email'] = 'zhang@example.com';

// ❌ 错误：内联对象字面量（即使有类型注解也不行）
const data: Record<string, string> = { key: 'value' };

// ✅ 正确：命名接口对象
interface UserData { name: string; email: string }
const user: UserData = { name: '张三', email: 'zhang@example.com' };
```

## 4. 箭头函数限制
```typescript
// ✅ 正确：用于回调
list.forEach((item: string) => {
  console.log(item);
});

// ✅ 正确：返回表达式（单行）
const doubled: Array<number> = data.map((x: number) => x * 2);

// ❌ 错误：箭头函数作为 Text() 参数
Text(() => { return 'hello'; });     // Text() 只接受 string | Resource
```

## 5. 数组操作
```typescript
// ✅ 正确：for 循环
for (let i: number = 0; i < arr.length; i++) {
  process(arr[i]);
}

// ✅ 正确：forEach
arr.forEach((item: string) => { process(item); });

// ❌ 错误：for...in
for (const key in obj) { ... }

// ✅ 正确替代
Object.keys(obj).forEach((key: string) => { ... });
```

## 6. 联合类型与 null 安全
```typescript
// ✅ 正确：显式联合
let value: string | null = null;

// ✅ 正确：可选链
const len: number = obj?.prop?.length ?? 0;

// ❌ 错误：隐式 undefined
let data: string;  // 必须初始化
```

## 7. 模块导入导出
```typescript
// ✅ 正确：具名导入
import { httpService, ApiResponse } from '../services/http';

// ✅ 正确：默认导入
import router from '@kit.ArkUI';

// ❌ 错误：CommonJS 语法
const http = require('../services/http');
```

## 8. Console 替代
```typescript
// ✅ 正确：使用 hilog
import { hilog } from '@kit.PerformanceAnalysisKit';
hilog.info(0x0000, 'TAG', 'message: %{public}s', msg);

// ❌ 错误：console.log
console.log('message');
```

## 9. 并发编程
```typescript
// ✅ 正确：TaskPool（推荐）
import { taskpool } from '@kit.ArkTS';

@Concurrent
function computeTask(data: number[]): number {
  return data.reduce((a, b) => a + b, 0);
}

async function run() {
  const task: taskpool.Task = new taskpool.Task(computeTask, [1, 2, 3]);
  const result: number = await taskpool.execute(task);
}

// ✅ 正确：Worker（适合长任务）
// worker.ts
import { worker, ThreadWorkerGlobalScope } from '@kit.ArkTS';
const workerPort: ThreadWorkerGlobalScope = worker.workerPort;
workerPort.onmessage = (msg) => {
  workerPort.postMessage(msg * 2);
};
```

## 10. build() 方法规则
```typescript
build() {
  Column() {
    // ✅ 允许：UI 组件
    Text('Hello')
      .fontSize(16)
    
    // ✅ 允许：if/else
    if (this.isLoading) {
      LoadingProgress()
    }
    
    // ✅ 允许：ForEach
    ForEach(this.items, (item: string) => {
      Text(item)
    }, (item: string) => item)
    
    // ✅ 允许：@Builder 方法调用
    this.MyCustomComponent()
    
    // ❌ 禁止：变量声明
    const x: number = 5;
    
    // ❌ 禁止：函数调用赋值
    const result = this.compute();
    
    // ❌ 禁止：try/catch
    try { ... } catch (e) { ... }
    
    // ❌ 禁止：console.log
    console.log('test');
  }
}
```
