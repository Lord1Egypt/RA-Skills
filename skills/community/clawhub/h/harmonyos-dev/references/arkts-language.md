# ArkTS 语言详解

> 来源：华为开发者文档 - ArkTS语言介绍（2026-04-20）
> https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts

## 基本类型

```typescript
let n: number = 3.14;           // 整数/浮点
let b: boolean = true;
let s: string = 'hello';
let big: bigint = 999n;         // 大整数
let arr: number[] = [1, 2, 3];
let obj: Object = 'Alice';       // 基本类型自动装箱
let str: String = 'text';       // String 对象
let anyVal: Object = 100;       // 基本类型装箱为 Object
```

## 声明

```typescript
// let 声明变量（可重新赋值）
let hi: string = 'hello';
hi = 'hello, world';             // ✅ 可以重新赋值

// const 声明常量（不可重新赋值）
const PI: number = 3.14159;     // ✅ 编译时常量
const APP_NAME: string = 'MyApp';
// PI = 3.14;                    // ❌ 编译错误：常量不可重新赋值

// 自动类型推断（声明时带初始值可省略类型）
let hi1: string = 'hello';
let hi2 = 'hello, world';        // 推断为 string

// 多重声明
let x: number = 1, y: number = 2, z: number = 3;
```


## 函数

```typescript
// 函数声明
function add(x: string, y: string): string {
  return `${x} ${y}`;
}

// 可选参数
function hello(name?: string) { }

// 默认参数
function multiply(n: number, coeff: number = 2): number {
  return n * coeff;
}

// rest 参数
function sum(...numbers: number[]): number {
  let res = 0;
  for (let n of numbers) { res += n; }
  return res;
}

// 箭头函数
let sum2 = (x: number, y: number) => x + y;

// 函数类型
type trigFunc = (x: number) => number;

// 闭包
function f(): () => number {
  let count = 0;
  return (): number => { count++; return count; };
}
```

## 类

```typescript
class Person {
  public name: string = '';
  private _age: number = 0;

  constructor(name: string, age: number) {
    this.name = name;
    this._age = age;
  }

  // getter / setter
  get age(): number { return this._age; }
  set age(x: number) {
    if (x < 0) throw Error('Invalid age');
    this._age = x;
  }

  // 实例方法
  fullName(): string { return this.name; }

  // 静态方法
  static create(name: string): Person {
    return new Person(name, 0);
  }
}

// 继承
class Employee extends Person {
  public salary: number = 0;
  constructor(name: string, salary: number) {
    super(name, 0);
    this.salary = salary;
  }
}

// 抽象类
abstract class Shape {
  abstract area(): number;
}
```

## 接口

```typescript
interface Style {
  color: string;
  width?: number;  // 可选属性
}

interface Area {
  calculateAreaSize(): number;
}

class Rectangle implements Area, Style {
  color: string = '';
  width: number = 0;
  calculateAreaSize(): number { return 0; }
}
```

## 泛型

```typescript
class CustomStack<T> {
  push(e: T): void { }
}

// 泛型约束
interface Hashable { hash(): number; }
class MyHashMap<Key extends Hashable, Value> { }

// 泛型函数
function last1<T>(x: T[]): T {
  return x[x.length - 1];
}

// 泛型默认值
interface Interface<T1 = string> { }
```

## 空安全

```typescript
// 默认所有类型非空
let x: number | null = null;  // 显式声明可空

// 非空断言
a!.value;

// 空值合并
this.nick ?? '';

// 可选链
this.spouse?.nick;
```

## 枚举

```typescript
enum ColorSet { Red, Green, Blue }
let c: ColorSet = ColorSet.Red;

enum ColorSet2 { White = 0xFF, Grey = 0x7F }
```

## 联合类型

```typescript
type Animal = Cat | Dog | Frog | number | string | null;

function foo(animal: Animal) {
  if (animal instanceof Frog) {
    animal.leap();  // TypeScript 收窄
  }
}
```

## 模块

```typescript
// 导出（export）
export class Point { }
export let origin = new Point(0, 0);
export const PI = 3.14159;

// 导入（import）
// 方式1：命名空间导入
import * as Utils from './utils';
Utils.method();

// 方式2：命名导入
import { A, B as AliasB } from './utils';
A(); AliasB();

// 方式3：默认导入
import MyClass from './MyClass';

// 动态导入（运行时加载模块）
let mod = await import('./Calc');
mod.add(1, 2);

// Kit 方式导入（推荐，API v22+）
import { UIAbility, AbilityContext } from '@kit.AbilityKit';
```

## 运算符

```typescript
// 赋值运算符
let a = 10;
a += 5;   // a = a + 5
a -= 3;   // a = a - 3
a *= 2;   // a = a * 2
a /= 4;   // a = a / 4
a %= 3;   // a = a % 3

// 一元运算符
let b = +5;   // 正号
let c = -b;   // 负号
let d = ++c;  // 前置递增
let e = c--;  // 后置递减

// 二元运算符
let sum = 3 + 2;    // 加法
let diff = 5 - 1;   // 减法
let prod = 4 * 2;   // 乘法
let quot = 10 / 3; // 除法
let rem = 10 % 3;   // 取模

// 比较运算符
3 === 3;   // 严格相等（值和类型都相等）
3 !== 4;   // 不相等
5 > 3; 5 < 8;  // 大小比较
5 >= 5; 3 <= 4; // 大小等于

// 逻辑运算符
true && false;  // 逻辑与
true || false;  // 逻辑或
!true;         // 逻辑非

// instanceof 类型检查
class Dog { bark() { } }
class Cat { meow() { } }

function speak(pet: Dog | Cat) {
  if (pet instanceof Dog) {
    pet.bark();  // TypeScript 收窄为 Dog
  } else {
    pet.meow();   // TypeScript 收窄为 Cat
  }
}

// typeof 运行时类型检查
function checkType(obj: Object | number) {
  if (typeof obj === 'number') {
    console.info('number: ' + obj);
  } else {
    console.info('object: ' + obj);
  }
}
```

## 语句

```typescript
// if-else
if (condition) {
  // do something
} else if (anotherCondition) {
  // do something else
} else {
  // default
}

// switch
switch (value) {
  case 1:
    console.info('one');
    break;
  case 2:
    console.info('two');
    break;
  default:
    console.info('other');
}

// for 循环
for (let i = 0; i < 5; i++) {
  console.info(i);
}

// for-of 遍历（数组/字符串/Set/Map）
let arr: number[] = [1, 2, 3];
for (let item of arr) {
  console.info(item);
}

// while
let n = 0;
while (n < 3) {
  n++;
}

// do-while（先执行后判断）
do {
  n--;
} while (n > 0);

// break / continue
for (let i = 0; i < 10; i++) {
  if (i === 3) continue;  // 跳过本次迭代
  if (i === 7) break;      // 跳出循环
  console.info(i);
}

// try-catch-finally
try {
  let result = riskyOperation();
} catch (e) {
  console.error(`错误: ${e}`);
} finally {
  console.info('无论如何都会执行');
}

// throw
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error('除数不能为零');
  }
  return a / b;
}
```

## 注解

```typescript
@interface ClassAuthor {
  authorName: string;
  revision: number = 1;
}

@ClassAuthor({ authorName: "Bob", revision: 2 })
class MyClass { }

// 注解仅在 .ets/.d.ets 文件有效
// release 模式开启混淆时，注解会被移除

// 注解字段仅支持的类型
// boolean, number, string, 及其数组
// 不能用于 getter/setter
// 不能重复使用同一注解
// 子类不继承父类注解
```

```typescript
@interface ClassAuthor {
  authorName: string;
  revision: number = 1;
}

@ClassAuthor({ authorName: "Bob", revision: 2 })
class MyClass { }

// 注解仅在 .ets/.d.ets 文件有效
// release 模式开启混淆时，注解会被移除
```
