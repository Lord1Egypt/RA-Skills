# 详细参考 - javascript-toolkit-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (text)

```text
用户：我的事件回调里 this 是 undefined

助手：这是 this 绑定丢失的典型问题

class Counter {
    constructor() {
        this.count = 0;
    }

    // 错误：普通函数在事件回调中丢失 this
    startBad() {
        document.addEventListener('click', function() {
            this.count++;  // this 是 undefined（严格模式）
        });
    }

    // 正确方式一：箭头函数（继承外层 this）
    startGood1() {
        document.addEventListener('click', () => {
            this.count++;  // this 指向 Counter 实例
        });
    }

    // 正确方式二：bind 绑定
    startGood2() {
        document.addEventListener('click', this.handleClick.bind(this));
    }

    handleClick() {
        this.count++;
    }

    // 正确方式三：类字段语法
    handleClick = () => {
        this.count++;
    }
}
```

## 代码示例 (text)

```text
用户：我的 forEach 里的 async 函数没有等待，怎么办

助手：forEach 不会等待 async 函数完成

// 错误：forEach 不等待
async function processItems(items) {
    items.forEach(async (item) => {
        await process(item);  // 不会被等待
    });
    console.log('完成');  // 在 process 完成前就执行
}

// 正确方式一：for...of（顺序执行）
async function processItems(items) {
    for (const item of items) {
        await process(item);
    }
    console.log('完成');
}

// 正确方式二：Promise.all（并行执行）
async function processItems(items) {
    await Promise.all(items.map(item => process(item)));
    console.log('完成');
}

// 正确方式三：需要部分失败容错用 allSettled
async function processItems(items) {
    const results = await Promise.allSettled(
        items.map(item => process(item))
    );
    const failed = results.filter(r => r.status === 'rejected');
    if (failed.length > 0) {
        console.warn(`${failed.length} 个处理失败`);
    }
}
```

## 代码示例 (javascript)

```javascript
// 陷阱：数组方法原地修改
const original = [3, 1, 2];

// sort 修改原数组
const sorted = original.sort();
console.log(original);  // [1, 2, 3]  被修改了！
console.log(sorted);    // [1, 2, 3]
console.log(original === sorted);  // true（同一引用）

// 正确：使用不可变方法（ES2023+）
const original2 = [3, 1, 2];
const sorted2 = original2.toSorted();
console.log(original2);  // [3, 1, 2]  不变
console.log(sorted2);    // [1, 2, 3]

// 常用不可变方法对照
// 修改型 → 不可变型
// sort()     → toSorted()
// reverse()  → toReversed()
// splice()   → toSpliced()
// push()     → [...arr, item]
// pop()      → arr.slice(0, -1)
// shift()    → arr.slice(1)
// unshift()  → [item, ...arr]

// 添加元素（不可变）
const arr = [1, 2, 3];
const added = [...arr, 4];        // 末尾添加
const prepended = [0, ...arr];    // 开头添加

// 删除元素（不可变）
const removed = arr.filter((_, i) => i !== 1);  // 删除索引1
const sliced = arr.slice(0, 2);                  // 取前两个

// 修改元素（不可变）
const modified = arr.map((v, i) => i === 1 ? 99 : v);
```

## 代码示例 (javascript)

```javascript
// 陷阱：var 在循环中共享变量
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
}
// 输出: 3, 3, 3（共享同一个 i）

// 修复方式一：let（每次迭代创建新绑定）
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
}
// 输出: 0, 1, 2

// 修复方式二：IIFE 立即执行函数
for (var i = 0; i < 3; i++) {
    (function(j) {
        setTimeout(() => console.log(j), 100);
    })(i);
}
// 输出: 0, 1, 2

// 陷阱：闭包捕获引用
function createFunctions() {
    const funcs = [];
    for (let i = 0; i < 3; i++) {
        funcs.push(() => i);
    }
    return funcs;
}
const fns = createFunctions();
console.log(fns[0]());  // 0
console.log(fns[1]());  // 1
console.log(fns[2]());  // 2
```

