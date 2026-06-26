# 开发知识要点

## JavaScript

### 防抖与节流

**防抖 (Debounce)**：等待停止触发后执行，适用于搜索框输入
```javascript
function debounce(fn, delay) {
    let timer;
    return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}
```

**节流 (Throttle)**：固定时间内只执行一次，适用于滚动事件
```javascript
function throttle(fn, interval) {
    let lastTime = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastTime >= interval) {
            lastTime = now;
            fn.apply(this, args);
        }
    };
}
```

---

## Vue

### 组合式 API (Composition API)

```javascript
import { ref, computed, onMounted, watch } from 'vue';

export default {
    setup() {
        // 响应式数据
        const count = ref(0);
        const user = ref({ name: 'Tom' });

        // 计算属性
        const doubleCount = computed(() => count.value * 2);

        // 方法
        const increment = () => count.value++;

        // 生命周期
        onMounted(() => {
            console.log('组件挂载完成');
        });

        // 监听器
        watch(count, (newVal, oldVal) => {
            console.log(`count 从 ${oldVal} 变为 ${newVal}`);
        });

        return { count, doubleCount, increment };
    }
};
```

### Vue 3 响应式原理

```javascript
import { reactive, proxy } from 'vue';

// 响应式对象
const state = reactive({
    list: [],
    loading: false
});

// 数组修改需注意
state.list.push({ id: 1 }); // 响应式
state.list = [...state.list, { id: 2 }]; // 响应式
```

---

## React

### Hooks 最佳实践

```javascript
import { useState, useEffect, useCallback, useMemo, useRef } from 'react';

function UserComponent({ userId }) {
    const [user, setUser] = useState(null);
    const loadingRef = useRef(false);

    // 记忆化回调
    const fetchUser = useCallback(async () => {
        if (loadingRef.current) return;
        loadingRef.current = true;

        const data = await fetch(`/api/users/${userId}`).then(r => r.json());
        setUser(data);
        loadingRef.current = false;
    }, [userId]);

    // 副作用
    useEffect(() => {
        fetchUser();
        return () => { /* 清理函数 */ };
    }, [fetchUser]);

    // 记忆化计算
    const displayName = useMemo(() => {
        return user?.name ?? '未命名';
    }, [user]);

    return <div>{displayName}</div>;
}
```

### useEffect 依赖管理

```javascript
// ❌ 错误 - 可能导致无限循环
useEffect(() => {
    setCount(count + 1);
}, [count]);

// ✅ 正确 - 使用函数式更新
useEffect(() => {
    setCount(c => c + 1);
}, []);

// ✅ 正确 - 清理定时器
useEffect(() => {
    const timer = setInterval(() => {
        // do something
    }, 1000);
    return () => clearInterval(timer);
}, []);
```

---

## AI 工具使用

### Cursor / VS Code AI 助手使用技巧

**1. 精准提问公式**
```
[上下文] + [具体需求] + [期望结果]
例如：
"在 Vue3 项目中，创建一个可复用的表格组件，需要支持：
- 列配置化
- 排序功能
- 分页请求
请给出核心代码结构"
```

**2. 使用 AI 进行代码审查**
```
"请审查以下代码，指出潜在的性能问题和内存泄漏风险：
[粘贴代码]"
```

**3. 使用 AI 帮助调试**
```
"这段代码报错：Cannot read property 'xxx' of undefined
代码如下：[粘贴代码]
请分析原因并给出修复方案"
```

### 提高 AI 响应质量的技巧

1. **分步提问**：复杂问题拆分成多个小问题
2. **提供上下文**：说明项目技术栈、现有代码结构
3. **指定格式**：如"用 TypeScript 类型定义"、"用 Hooks 写法"
4. **迭代优化**：基于 AI 回答继续追问"能不能改成..."、"如果支持...需要怎么改"

### 常用 AI 代码提示

```javascript
// 让 AI 生成 TypeScript 类型
"为以下接口添加 TypeScript 类型定义：
interface User {
  id: number;
  name: string;
  email: string;
}"

// 让 AI 重构代码
"将以下 class 组件重构为 hooks 写法"

// 让 AI 添加注释
"为这个函数添加 JSDoc 注释，说明参数和返回值"
```