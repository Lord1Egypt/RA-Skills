---
name: huo15-owl-dev
version: 1.0.0
slug: owl-dev
description: OWL (Odoo Web Library) 开发技能 — Odoo 前端组件开发框架，基于 QWeb 模板、响应式状态管理、OWL 组件生命周期
aliases:
  - OWL组件开发
  - Odoo前端
  - OWL
  - odoo web library
  - OWL dev
---

# SKILL.md — huo15-owl-dev

## 触发条件

用户提到以下内容时激活本技能：
- OWL 组件开发
- Odoo 前端 / Web 开发
- QWeb 模板
- OWL 组件生命周期
- Odoo JS/Web 组件
- `odoo.define` / `owl.component`
- Odoo 15+ 前端架构

---

## OWL 核心概念

### 什么是 OWL？

OWL（Odoo Web Library）是 Odoo 15+ 引入的**新一代前端框架**，用于替代旧的 `web.old`（backbone-based）架构。它基于：
- **QWeb 模板**（XML）
- **响应式状态管理**（PoP/Props）
- **TypeScript**（原生支持）

### OWL vs 旧架构

| 特性 | OWL（新） | web.old（旧） |
|------|----------|--------------|
| 模板 | QWeb XML | QWeb XML |
| 状态 | `useState` / `useRefs` | 不存在 |
| 组件 | 类 + 装饰器 | `Widget` 基类 |
| 生命周期 | PoP (Props on Props) | 不存在 |
| TypeScript | 原生支持 | 不支持 |
| 响应式 | 自动追踪依赖 | 手动绑定 |
| 性能 | 虚拟DOM + 懒加载 | 完整重渲染 |

---

## OWL 组件结构

### 最小组件模板

```typescript
/** @odoo-module **/

import { Component, useState, useEnv } from "@odoo/owl";

export class MyComponent extends Component {
    static template = "my_module.MyComponent";

    // 响应式状态
    state = useState({
        value: 0,
        items: [],
        loading: false,
    });

    // 组件挂载时调用
    onWillMount() {
        this.loadData();
    }

    async loadData() {
        this.state.loading = true;
        try {
            const result = await this.rpc("/my_module/data");
            this.state.items = result;
        } finally {
            this.state.loading = false;
        }
    }

    increment() {
        this.state.value++;
    }

    onClick() {
        this.trigger("custom-event", { payload: this.state.value });
    }
}
```

### 目录结构

```
my_module/
├── static/
│   └── src/
│       ├── js/
│       │   ├── components/
│       │   │   ├── my_component/
│       │   │   │   ├── my_component.xml    # QWeb 模板
│       │   │   │   └── my_component.ts     # 组件逻辑
│       │   │   └── other_component/
│       │   │       ├── other_component.xml
│       │   │       └── other_component.ts
│       │   └── pages/
│       │       └── my_page.xml
│       └── css/
│           └── my_component.scss
├── views/
│   └── templates.xml                        # Web 入口
└── __manifest__.py
```

---

## 组件注册与挂载

### `__manifest__.py` 配置

```python
{
    'name': '我的模块',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            ('include', 'my_module.static.src.js.components.my_component.my_component_xml'),
            'my_module/static/src/js/components/my_component/my_component.ts',
            'my_module/static/src/css/my_component.scss',
        ],
    },
}
```

### XML 入口（views/templates.xml）

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="assets_backend" name="my_module assets" inherit_id="web.assets_backend">
        <xpath expr="." position="inside">
            <link rel="stylesheet" href="/my_module/static/src/css/my_component.scss"/>
            <script type="module" src="/my_module/static/src/js/components/my_component/my_component.es.js"/>
        </xpath>
    </template>
</odoo>
```

### 注册到 OwlComponentStore

```typescript
// my_component.ts
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MyComponent extends Component {
    static template = "my_module.MyComponent";
}

registry.category("components").add("my_component", MyComponent);
```

### 在另一个组件中使用

```xml
<-- parent.xml -->
<MyComponent t-component="'my_component'" />
```

---

## Props（属性传递）

### 定义 Props 接口

```typescript
import { Component } from "@odoo/owl";
import { Props } from "@odoo/owl";

interface MyProps {
    title: string;
    count: number;
    onUpdate: (value: number) => void;
}

export class MyComponent extends Component<Props & MyProps> {
    static template = "my_module.MyComponent";

    static props = {
        title: { type: String, optional: true },
        count: { type: Number },
        onUpdate: { type: Function },
    };

    updateCount(newCount: number) {
        this.props.onUpdate(newCount);
    }
}
```

### Props 类型

```typescript
// 简单类型
static props = {
    name: String,           // string
    active: Boolean,        // boolean
    count: Number,          // number
    items: Array,           // any[]
}

// 可选
static props = {
    title: { type: String, optional: true },
}

// 对象类型
static props = {
    config: { type: Object },
}

// 函数（回调）
static props = {
    onChange: Function,
    onSubmit: { type: Function, optional: true },
}

// 数组对象
static props = {
    items: {
        type: Array,
        validate: (items) => items.every(i => typeof i === 'object'),
    },
}
```

---

## 状态管理（State）

### useState

```typescript
import { useState } from "@odoo/owl";

export class MyComponent extends Component {
    state = useState({
        // 原始类型
        count: 0,
        name: "",
        active: false,
        
        // 嵌套对象
        user: {
            name: "张三",
            age: 30,
        },
        
        // 数组
        items: [],
        
        // 特殊值
        loading: false,
        error: null,
    });
}
```

### 状态更新

```typescript
// 直接赋值（OWL 自动追踪）
this.state.count = 5;
this.state.user.name = "李四";
this.state.items.push({ id: 1, name: "item" });

// 数组操作
this.state.items = [...this.state.items, newItem];  // 替换触发更新
this.state.items.filter(i => i.id !== deleteId);    // 删除

// 批量更新（函数式）
this.state = {
    ...this.state,
    count: this.state.count + 1,
    loading: false,
};
```

---

## 生命周期（Lifecycle）

### 完整生命周期钩子

```typescript
export class MyComponent extends Component {
    // ===== 创建阶段 =====
    
    /** 组件即将挂载（异步） */
    async onWillMount() {
        // 可返回 Promise
    }
    
    /** 组件即将渲染 */
    onWillRender() {}
    
    // ===== 挂载阶段 =====
    
    /** 组件 DOM 已挂载 */
    onMounted() {
        // 可添加 DOM 事件监听
        const el = this.el;
    }
    
    /** 组件渲染完成 */
    onRendered() {}
    
    // ===== 更新阶段 =====
    
    /** Props 或 State 即将更新 */
    onWillUpdateProps(nextProps) {
        // 准备数据
    }
    
    /** 组件即将重新渲染 */
    onWillPatch() {}
    
    /** 组件 DOM patch 完成 */
    onPatched() {
        // DOM 更新后执行
    }
    
    // ===== 卸载阶段 =====
    
    /** 组件即将卸载 */
    onWillUnmount() {
        // 清理定时器/事件监听
    }
    
    /** 组件已卸载 */
    onUnmounted() {}
}
```

### 生命周期图

```
组件创建 → onWillMount → 渲染 → onMounted
                    ↓
props/state 变化 → onWillUpdateProps → onWillPatch → patch → onPatched
                    ↓
组件卸载 → onWillUnmount → onUnmounted
```

---

## QWeb 模板

### 基础语法

```xml
<templates>
    <t t-name="my_module.MyComponent">
        <div class="my-component">
            <h1 t-esc="props.title"/>
            
            <!-- 条件渲染 -->
            <span t-if="state.loading">加载中...</span>
            
            <!-- 循环 -->
            <ul>
                <li t-foreach="state.items" t-as="item" t-key="item.id">
                    <span t-esc="item.name"/>
                </li>
            </ul>
            
            <!-- 事件绑定 -->
            <button t-on-click="increment">点击</button>
            <button t-on-click.self="doSomething">仅自身</button>
            
            <!-- 子组件 -->
            <SubComponent t-component="'sub_component'" t-props="subProps"/>
        </div>
    </t>
</templates>
```

### 常用指令

| 指令 | 用法 | 说明 |
|------|------|------|
| `t-esc` | `<span t-esc="value"/>` | 转义文本 |
| `t-raw` | `<span t-raw="html"/>` | 原始 HTML |
| `t-if` | `<div t-if="state.show"/>` | 条件渲染 |
| `t-else` | `<div t-elif="state.show2"/>` | 否则 |
| `t-foreach` | `<li t-foreach="arr" t-as="i"/>` | 循环 |
| `t-key` | `t-key="item.id"` | 循环 key |
| `t-on-*` | `t-on-click="handler"` | 事件绑定 |
| `t-model` | `t-model="state.inputValue"` | 双向绑定 |
| `t-ref` | `<div t-ref="myDiv"/>` | DOM 引用 |
| `t-set` | `<t t-set="val" t-value="123"/>` | 设置变量 |
| `t-call` | `<t t-call="other_template"/>` | 引用模板 |
| `t-translation` | `t-translation="on"` | 翻译标记 |

### 事件绑定

```xml
<!-- 基础 -->
<button t-on-click="onClick">点击</button>

<!-- 阻止冒泡 -->
<button t-on-click.stop="onClick">阻止冒泡</button>

<!-- 阻止默认 -->
<a href="#" t-on-click.prevent="onLink">阻止默认</a>

<!-- 修饰符组合 -->
<button t-on-click.stop.prevent="onClick">组合</button>

<!-- 传参数 -->
<button t-on-click="(ev) => onClick(42, ev)">传参</button>
<button t-on-click="() => onClick(42)">箭头函数</button>

<!-- 事件对象 -->
<button t-on-click="onClick">访问事件: ev.target</button>
```

### 双向绑定（t-model）

```xml
<!-- 输入框 -->
<input type="text" t-model="state.inputValue"/>

<!-- 多行文本 -->
<textarea t-model="state.description"/>

<!-- 复选框 -->
<input type="checkbox" t-model="state.checked"/>

<!-- 下拉选择 -->
<select t-model="state.selectedId">
    <option value="">请选择</option>
    <option t-foreach="state.options" 
            t-as="opt" 
            t-att-value="opt.id"
            t-esc="opt.name"/>
</select>
```

---

## Hooks（钩子）

### 内置 Hooks

```typescript
import { 
    useState,        // 响应式状态
    useRef,          // DOM 引用
    useEffect,       // 副作用
    useEnv,          // 环境（env）
    useDispatch,     // dispatch (action-service)
    useSelectors,    // selectors
} from "@odoo/owl";
```

### useRef（DOM 引用）

```typescript
import { useRef } from "@odoo/owl";

export class MyComponent extends Component {
    myInput = useRef("myInput");  // 声明 ref
    
    onMounted() {
        // 访问 DOM
        this.myInput.el.focus();
    }
    
    getValue() {
        return this.myInput.el.value;
    }
}

// 模板中使用
<input t-ref="myInput" type="text"/>
```

### useEffect（副作用）

```typescript
import { useEffect } from "@odoo/owl";

export class MyComponent extends Component {
    state = useState({ data: null });
    
    setup() {
        // 每次渲染后执行
        useEffect(
            () => console.log("count changed:", this.state.count),
            () => [this.state.count]  // 依赖数组
        );
        
        // 清理函数
        useEffect(
            () => {
                const timer = setInterval(() => this.tick(), 1000);
                return () => clearInterval(timer);  // 返回清理函数
            },
            () => []
        );
    }
}
```

### useEnv（获取环境）

```typescript
import { useEnv } from "@odoo/owl";

export class MyComponent extends Component {
    setup() {
        const env = useEnv();
        
        // 访问 Odoo env
        const user = env.session.user;
        const db = env.session.db;
    }
}
```

---

## Service（服务）

### 使用 ActionService

```typescript
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class MyComponent extends Component {
    setup() {
        this.actionService = useService("action");
        this.ormService = useService("orm");
    }
    
    async doAction() {
        // 触发窗口动作
        await this.actionService.doAction("my_module.action_wizard");
    }
    
    async searchData() {
        const result = await this.ormService.call(
            "my.model",      // 模型
            "search_read",   // 方法
            [[['active', '=', true]], ['name', 'id']],  // domain, fields
            { context: { ... } }
        );
        return result;
    }
}
```

### 常用服务

```typescript
// Action 服务
this.actionService.doAction({
    type: "ir.actions.act_window",
    res_model: "my.model",
    view_mode: "form",
    views: [[false, "form"]],
    target: "new",  // new/current/main
});

// 通知服务
useService("notification").notify("标题", "内容", "success");

// 对话框服务
useService("dialog").add(ConfirmDialog, {
    title: "确认删除",
    body: "确定要删除吗？",
    confirmLabel: "删除",
    cancelLabel: "取消",
    confirmCallback: () => this.doDelete(),
});

// RPC 服务
const result = await useService("rpc").call("/my_route", params);
```

### 自定义 Service

```typescript
// my_service.js
import { registry } from "@web/core/registry";

export const myService = {
    start(env) {
        return {
            async getData(id) {
                return await env.services.orm.call(
                    "my.model", "read", [id]
                );
            },
        };
    },
};

registry.category("services").add("myService", myService);
```

---

## 路由（Router）

### 配置路由

```typescript
// __manifest__.py
'assets': {
    'web.assets_backend': [
        'my_module/static/src/js/routes.js',
    ],
},
```

### 定义路由

```typescript
// routes.js
import { registry } from "@web/core/registry";
import { route } from "@web/core/router/route";

registry.category("main").add("my_module.dashboard", 
    route("/my_module/dashboard", MyComponent, {
        load: async (env) => {
            // 加载数据
            return await env.services.orm.call("my.model", "get_data", []);
        },
    })
);
```

---

## 国际化（i18n）

### 模板中使用翻译

```xml
<span>这是中文文本</span>
<span t-esc="env._t('Hello World')"/>
```

### JS 中使用翻译

```typescript
import { useEnv } from "@odoo/owl";

export class MyComponent extends Component {
    setup() {
        const env = useEnv();
        
        const msg = env._t("Hello");
        const formatted = env._t("You have %s items", [count]);
    }
}
```

---

## 样式（SCSS/CSS）

### 组件样式

```scss
// static/src/css/my_component.scss

.my-component {
    padding: 16px;
    background: #fff;
    border-radius: 4px;
    
    &__header {
        font-size: 18px;
        font-weight: 600;
    }
    
    &__list {
        list-style: none;
        
        &-item {
            padding: 8px;
            
            &--active {
                background: #f0f0f0;
            }
        }
    }
    
    &--loading {
        opacity: 0.6;
        pointer-events: none;
    }
}
```

### CSS 变量

```scss
.o_my_component {
    --my-color: #{$primary};
    --my-spacing: 16px;
    
    padding: var(--my-spacing);
    color: var(--my-color);
}
```

---

## 测试（Testing）

### 组件测试

```typescript
// my_component.test.js
import { describe, expect, test } from "@odoo/owl";
import { makeTestEnv } from "@web/../tests/helpers/mock_env";
import { MyComponent } from "./my_component";

describe("MyComponent", () => {
    test("renders correctly", async () => {
        const env = await makeTestEnv();
        const wrapper = new MyComponent(null, { env });
        
        await wrapper.mount(fixture);
        
        expect(wrapper.el.textContent).toContain("标题");
    });
    
    test("increments counter on click", async () => {
        const env = await makeTestEnv();
        const comp = new MyComponent(null, { env });
        comp.state.count = 0;
        
        await comp.mount(fixture);
        await comp.onClick();
        
        expect(comp.state.count).toBe(1);
    });
});
```

### 常用测试工具

```typescript
import { makeTestEnv, makeFakeCookieService } from "@web/../tests/helpers/mock_env";
import { dom } from "@web/../tests/helpers/dom";

// 模拟 RPC
await mockServer.mockModel("my.model", {
    search_read: () => [{ id: 1, name: "Test" }],
});
```

---

## 调试技巧

### 开发工具

1. **浏览器扩展**：安装 `Odoo Web Developer` 浏览器插件
2. **日志**：`console.log` 替换为 `console.debug` 减少干扰
3. **QWeb 错误**：Odoo 会显示模板解析错误位置

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| Template not found | `__manifest__.py` 未注册 assets | 检查 `assets_backend` 配置 |
| Component not rendering | `t-component` 名称错误 | 确认 `registry.category("components").add()` 名称 |
| State not updating | 直接修改对象而非赋值 | `this.state.items.push()` 不触发更新，需替换 |
| Event not working | `t-on-click` 语法错误 | 检查是否少了括号 `t-on-click="handler"` |
| Props undefined | 子组件 Props 未定义 | 检查 `static props` 定义 |

### 热重载

```bash
# Odoo 开发者模式已启用热重载
# 修改 .ts/.xml 文件后，刷新浏览器即可
# 如需完全重载：Ctrl+Shift+R (强制刷新)
```

---

## 最佳实践

### 代码组织

- **一个组件一个目录**：`components/my_comp/`
- **模板文件名匹配**：`my_comp.xml` + `my_comp.ts`
- **组件名 PascalCase**：`MyComponent`
- **方法名 camelCase**：`onClick`, `getData`

### 性能优化

```typescript
// ✅ 使用 useState 细粒度更新
state = useState({ count: 0, items: [] });

// ✅ 避免在 render 中创建函数
class MyComponent extends Component {
    onClick = (id) => {
        // 使用箭头函数避免重复创建
    };
}

// ✅ 使用 t-key 帮助 OWL 高效更新
<li t-foreach="items" t-as="item" t-key="item.id">
```

### 安全建议

- **用户输入转义**：使用 `t-esc` 而非 `t-raw`
- **SQL 注入**：永远通过 ORM 操作数据
- **XSS**：避免使用 `t-raw` 处理用户输入

---

## 快速参考

### 常用导入

```typescript
import { Component, useState, useRef, useEffect, useEnv, useService } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ormService } from "@web/core/orm_service";
import { actionService } from "@web/core/action_service";
```

### 组件装饰器

```typescript
// 可选：类组件装饰器
@registerComponent("my_component")
export class MyComponent extends Component {
    // ...
}
```

### Props 验证

```typescript
static props = {
    // 必需
    title: String,
    count: Number,
    
    // 可选
    subtitle: { type: String, optional: true },
    
    // 回调
    onChange: Function,
    
    // 复杂类型
    config: { type: Object },
    items: Array,
}
```

---

*本技能基于 OWL v2.x（Odoo 16+），适配辉火云企业套件前端开发环境。*