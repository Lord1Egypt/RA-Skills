---
name: java-design-patterns
description: "Java 设计模式权威参考。涵盖 GoF 23 种经典模式及企业级架构模式的完整 Java 实现，含 26 个核心设计原则。当用户询问设计模式、架构模式、设计原则（KISS/DRY/SOLID/GRASP 等）、Java 模式实现、或需要选择合适的设计模式时调用此技能。覆盖创建型、结构型、行为型、架构型、并发型等 15 大类 182 个模式 + 26 个设计原则。"
---

# Java 设计模式技能

> **官方文档**：[java-design-patterns.com](https://java-design-patterns.com/)
> **模式总数**：182 个，覆盖 15 个分类
> **设计原则**：26 个核心编程原则
> **代码语言**：Java

## 触发条件

**在以下场景中自动调用此技能：**

1. 用户询问"设计模式"、"Design Pattern"、"GoF" 等相关话题
2. 用户需要了解特定设计模式的 Java 实现
3. 用户在代码审查或架构设计时需要选择合适的设计模式
4. 用户询问"如何实现..."且可通过设计模式解决的问题
5. 用户讨论软件架构、企业级应用架构方案
6. 用户询问并发模式、微服务模式、数据访问模式等
7. 用户询问"设计原则"、"编程原则"、"SOLID"、"KISS"、"DRY"、"YAGNI"等软件设计原则

## 使用优先级

**重要：回答设计问题时，遵循以下优先级：**

1. **先原则后模式** — 先基于设计原则判断方向（为什么这样做），再选择合适的设计模式（具体怎么做）
2. **设计原则是决策基础** — 当用户询问"如何设计/优化/重构"时，优先从原则角度给出建议，再推荐具体模式
3. **经典代码示例** — 快速参考 7 个最常用模式的 Java 实现，可直接用于回答代码问题
4. **按需深入** — 当需要某个模式的完整 API、类图、适用场景时，通过链接读取对应的 `references/` 文档

## 设计原则快速索引

> 全部来自 https://java-design-patterns.com/principles/ ，共 25 个核心编程原则。

| 原则 | 说明 | 文档 |
|------|------|------|
| KISS | 保持简单 — 系统越简单越有效 | [kiss](references/principles/kiss.md) |
| YAGNI | 你不会需要它 — 不实现不必要的功能 | [yagni](references/principles/yagni.md) |
| DRY | 不要重复自己 — 每份知识唯一表达 | [dry](references/principles/dry.md) |
| Separation of Concerns | 关注点分离 — 程序按关注点分模块 | [separation-of-concerns](references/principles/separation-of-concerns.md) |
| Single Responsibility (SRP) | 单一职责 — 一个类只有一个变化理由 | [single-responsibility-principle](references/principles/single-responsibility-principle.md) |
| Open/Closed (OCP) | 开闭原则 — 对扩展开放，对修改关闭 | [open-closed-principle](references/principles/open-closed-principle.md) |
| Liskov Substitution (LSP) | 里氏替换 — 子类型可透明替换父类型 | [liskov-substitution-principle](references/principles/liskov-substitution-principle.md) |
| Interface Segregation (ISP) | 接口隔离 — 避免胖接口 | [interface-segregation-principle](references/principles/interface-segregation-principle.md) |
| Composition Over Inheritance | 组合优于继承 — 优先使用组合而非继承 | [composition-over-inheritance](references/principles/composition-over-inheritance.md) |
| Encapsulate What Changes | 封装变化 — 识别变化点并封装 | [encapsulate-what-changes](references/principles/encapsulate-what-changes.md) |
| Minimise Coupling | 最小化耦合 — 降低模块间依赖 | [minimise-coupling](references/principles/minimise-coupling.md) |
| Maximise Cohesion | 最大化内聚 — 相关功能集中到单一模块 | [maximise-cohesion](references/principles/maximise-cohesion.md) |
| Hide Implementation Details | 隐藏实现细节 — 通过接口隐藏内部实现 | [hide-implementation-details](references/principles/hide-implementation-details.md) |
| Law of Demeter | 迪米特法则 — 不要和陌生人说话 | [law-of-demeter](references/principles/law-of-demeter.md) |
| Inversion of Control | 控制反转 — 别调用我们，我们会调用你 | [inversion-of-control](references/principles/inversion-of-control.md) |
| Command Query Separation | 命令查询分离 — 查询不修改状态 | [command-query-separation](references/principles/command-query-separation.md) |
| Avoid Premature Optimization | 避免过早优化 — 先让它工作，再优化 | [avoid-premature-optimization](references/principles/avoid-premature-optimization.md) |
| Code For The Maintainer | 为维护者编码 — 代码应易于维护和理解 | [code-for-the-maintainer](references/principles/code-for-the-maintainer.md) |
| Boy-Scout Rule | 童子军规则 — 让代码比发现时更干净 | [boy-scout-rule](references/principles/boy-scout-rule.md) |
| Robustness Principle | 健壮性原则 — 严以律己，宽以待人 | [robustness-principle](references/principles/robustness-principle.md) |
| Orthogonality | 正交性 — 不相关的事物不应在系统中相关 | [orthogonality](references/principles/orthogonality.md) |
| Curly's Law | 科里定律 — 只做一件事 | [curlys-law](references/principles/curlys-law.md) |
| Murphy's Law | 墨菲定律 — 可能出错的终将出错 | [murphys-law](references/principles/murphys-law.md) |
| Brooks's Law | 布鲁克斯定律 — 向延期项目加人只会更延期 | [brooks-law](references/principles/brooks-law.md) |
| Linus's Law | 林纳斯定律 — 足够多的眼球，所有 Bug 都是浅显的 | [linus-law](references/principles/linus-law.md) |

## 经典代码示例

### 单例模式（Singleton）— 双重检查锁定
```java
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

### 工厂方法模式（Factory Method）
```java
interface Product { void use(); }

class ConcreteProductA implements Product {
    public void use() { System.out.println("Using Product A"); }
}

abstract class Creator {
    abstract Product createProduct();
    void doSomething() {
        Product p = createProduct();
        p.use();
    }
}
```

### 观察者模式（Observer）
```java
interface Observer {
    void update(String message);
}

class Subject {
    private final List<Observer> observers = new ArrayList<>();

    void attach(Observer o) { observers.add(o); }
    void detach(Observer o) { observers.remove(o); }

    void notifyObservers(String msg) {
        observers.forEach(o -> o.update(msg));
    }
}
```

### 策略模式（Strategy）
```java
interface Strategy {
    int execute(int a, int b);
}

class AddStrategy implements Strategy {
    public int execute(int a, int b) { return a + b; }
}

class Context {
    private Strategy strategy;

    void setStrategy(Strategy s) { this.strategy = s; }
    int executeStrategy(int a, int b) { return strategy.execute(a, b); }
}
```

### 装饰器模式（Decorator）
```java
interface Coffee {
    double getCost();
    String getDescription();
}

class SimpleCoffee implements Coffee {
    public double getCost() { return 1.0; }
    public String getDescription() { return "Simple coffee"; }
}

class MilkDecorator implements Coffee {
    private final Coffee coffee;

    MilkDecorator(Coffee c) { this.coffee = c; }

    public double getCost() { return coffee.getCost() + 0.5; }
    public String getDescription() { return coffee.getDescription() + ", milk"; }
}
```

### 建造者模式（Builder）
```java
public class Hero {
    private final String name;
    private final String profession;

    private Hero(Builder builder) {
        this.name = builder.name;
        this.profession = builder.profession;
    }

    public static class Builder {
        private String name;
        private String profession;

        public Builder name(String name) { this.name = name; return this; }
        public Builder profession(String p) { this.profession = p; return this; }
        public Hero build() { return new Hero(this); }
    }
}

// 使用
Hero hero = new Hero.Builder()
    .name("Arthur")
    .profession("Warrior")
    .build();
```

### 适配器模式（Adapter）
```java
// 已有接口
interface OldSystem { void oldMethod(); }

// 新接口
interface NewSystem { void newMethod(); }

// 适配器
class Adapter implements NewSystem {
    private final OldSystem oldSystem;

    Adapter(OldSystem old) { this.oldSystem = old; }

    public void newMethod() { oldSystem.oldMethod(); }
}
```

## 模式快速索引

### 创建型模式（Creational）— 14 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Abstract Factory | 抽象工厂 — 创建相关对象家族，无需指定具体类 | [abstract-factory](references/creational/abstract-factory.md) |
| Builder | 建造者 — 分步构建复杂对象 | [builder](references/creational/builder.md) |
| Dependency Injection | 依赖注入 — 将依赖从外部注入对象 | [dependency-injection](references/creational/dependency-injection.md) |
| Factory | 工厂 — 提供统一的对象创建接口 | [factory](references/creational/factory.md) |
| Factory Kit | 工厂套件 — 使用 Builder 和 Functional 接口创建工厂 | [factory-kit](references/creational/factory-kit.md) |
| Factory Method | 工厂方法 — 子类决定实例化哪个类 | [factory-method](references/creational/factory-method.md) |
| Monostate | 单态 — 通过静态成员实现类似单例的行为 | [monostate](references/creational/monostate.md) |
| Multiton | 多例 — 控制实例数量的单例变体 | [multiton](references/creational/multiton.md) |
| Object Pool | 对象池 — 重用开销大的对象 | [object-pool](references/creational/object-pool.md) |
| Prototype | 原型 — 克隆已有对象 | [prototype](references/creational/prototype.md) |
| Registry | 注册表 — 集中管理对象的查找和获取 | [registry](references/creational/registry.md) |
| Singleton | 单例 — 全局唯一实例 | [singleton](references/creational/singleton.md) |
| Step Builder | 步骤建造者 — 强制按步骤构建对象的建造者变体 | [step-builder](references/creational/step-builder.md) |
| Type Object | 类型对象 — 通过对象实例表示类型 | [type-object](references/creational/type-object.md) |

### 结构型模式（Structural）— 35 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Abstract Document | 抽象文档 — 动态添加属性 | [abstract-document](references/structural/abstract-document.md) |
| Adapter | 适配器 — 转换接口使不兼容的类可以协作 | [adapter](references/structural/adapter.md) |
| Bridge | 桥接 — 将抽象与实现分离 | [bridge](references/structural/bridge.md) |
| Business Delegate | 业务代表 — 解耦表示层和业务服务层 | [business-delegate](references/structural/business-delegate.md) |
| Component | 组件 — 通过统一接口管理对象组 | [component](references/structural/component.md) |
| Composite | 组合 — 树形结构表示整体-部分层次 | [composite](references/structural/composite.md) |
| Composite Entity | 组合实体 — 管理一组相关持久化对象 | [composite-entity](references/structural/composite-entity.md) |
| Composite View | 组合视图 — 聚合多个子视图 | [composite-view](references/structural/composite-view.md) |
| Converter | 转换器 — 对象间相互转换 | [converter](references/structural/converter.md) |
| Curiously Recurring Template Pattern | CRTP — 通过模板实现编译期多态 | [curiously-recurring-template-pattern](references/structural/curiously-recurring-template-pattern.md) |
| DAO Factory | DAO 工厂 — 灵活的数据访问层切换 | [dao-factory](references/structural/dao-factory.md) |
| Data Access Object (DAO) | 数据访问对象 — 抽象持久化操作 | [data-access-object](references/structural/data-access-object.md) |
| Data Transfer Object (DTO) | 数据传输对象 — 子系统间高效传递数据 | [data-transfer-object](references/structural/data-transfer-object.md) |
| Decorator | 装饰器 — 动态添加职责 | [decorator](references/structural/decorator.md) |
| Domain Model | 领域模型 — 封装业务逻辑的对象模型 | [domain-model](references/structural/domain-model.md) |
| Dynamic Proxy | 动态代理 — 运行时创建代理对象 | [dynamic-proxy](references/structural/dynamic-proxy.md) |
| Extension Objects | 扩展对象 — 灵活扩展对象功能 | [extension-objects](references/structural/extension-objects.md) |
| Facade | 外观 — 简化复杂子系统的接口 | [facade](references/structural/facade.md) |
| Flyweight | 享元 — 共享细粒度对象以减少内存 | [flyweight](references/structural/flyweight.md) |
| Marker Interface | 标记接口 — 通过空接口定义行为 | [marker-interface](references/structural/marker-interface.md) |
| Money | 货币 — 封装货币值和精度 | [money](references/structural/money.md) |
| Parameter Object | 参数对象 — 简化方法签名 | [parameter-object](references/structural/parameter-object.md) |
| Private Class Data | 私有类数据 — 保护数据完整性 | [private-class-data](references/structural/private-class-data.md) |
| Proxy | 代理 — 控制对对象的访问 | [proxy](references/structural/proxy.md) |
| Role Object | 角色对象 — 动态赋予对象不同角色 | [role-object](references/structural/role-object.md) |
| Separated Interface | 分离接口 — 接口与实现分开打包 | [separated-interface](references/structural/separated-interface.md) |
| Servant | 仆人 — 为多个类提供公共行为 | [servant](references/structural/servant.md) |
| Service Locator | 服务定位器 — 简化复杂系统中的服务访问 | [service-locator](references/structural/service-locator.md) |
| Session Facade | 会话外观 — 简化企业 Bean 接口 | [session-facade](references/structural/session-facade.md) |
| Spatial Partition | 空间分区 — 优化空间查询性能 | [spatial-partition](references/structural/spatial-partition.md) |
| Special Case | 特例 — 用预定义对象替代 null | [special-case](references/structural/special-case.md) |
| Strangler | 绞杀者 — 逐步替换遗留系统 | [strangler](references/structural/strangler.md) |
| Twin | 双生子 — 让不支持多继承的语言实现多重行为 | [twin](references/structural/twin.md) |
| Value Object | 值对象 — 不可变数据类型提升性能 | [value-object](references/structural/value-object.md) |
| Virtual Proxy | 虚拟代理 — 延迟加载重型对象 | [virtual-proxy](references/structural/virtual-proxy.md) |

### 行为型模式（Behavioral）— 40 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Acyclic Visitor | 无环访问者 — 无循环依赖的访问者变体 | [acyclic-visitor](references/behavioral/acyclic-visitor.md) |
| Bytecode | 字节码 — 通过自定义虚拟机解释指令 | [bytecode](references/behavioral/bytecode.md) |
| Chain of Responsibility | 责任链 — 沿链传递请求直到被处理 | [chain-of-responsibility](references/behavioral/chain-of-responsibility.md) |
| Client Session | 客户端会话 — 管理跨会话的客户端数据 | [client-session](references/behavioral/client-session.md) |
| Collecting Parameter | 收集参数 — 在方法调用链中累积结果 | [collecting-parameter](references/behavioral/collecting-parameter.md) |
| Command | 命令 — 封装请求为对象 | [command](references/behavioral/command.md) |
| Commander | 指挥官 — 编排复杂命令执行 | [commander](references/behavioral/commander.md) |
| Context Object | 上下文对象 — 封装和传递上下文数据 | [context-object](references/behavioral/context-object.md) |
| Data Mapper | 数据映射器 — 解耦对象模型和数据存储 | [data-mapper](references/behavioral/data-mapper.md) |
| Delegation | 委托 — 将任务委托给关联对象 | [delegation](references/behavioral/delegation.md) |
| Dirty Flag | 脏标记 — 跟踪变化避免不必要更新 | [dirty-flag](references/behavioral/dirty-flag.md) |
| Double Buffer | 双缓冲 — 平滑动画和图形渲染 | [double-buffer](references/behavioral/double-buffer.md) |
| Double Dispatch | 双分派 — 根据接收者和参数类型动态调用 | [double-dispatch](references/behavioral/double-dispatch.md) |
| Execute Around | 环绕执行 — 封装前置和后置操作 | [execute-around](references/behavioral/execute-around.md) |
| Feature Toggle | 特性开关 — 无缝管理生产环境功能 | [feature-toggle](references/behavioral/feature-toggle.md) |
| Filterer | 过滤器 — 动态过滤数据流 | [filterer](references/behavioral/filterer.md) |
| Fluent Interface | 流式接口 — 链式调用提升代码表达力 | [fluent-interface](references/behavioral/fluent-interface.md) |
| Game Loop | 游戏循环 — 游戏主循环驱动帧更新 | [game-loop](references/behavioral/game-loop.md) |
| Health Check | 健康检查 — 监控系统健康状态 | [health-check](references/behavioral/health-check.md) |
| Identity Map | 标识映射 — 确保每个对象只加载一次 | [identity-map](references/behavioral/identity-map.md) |
| Interpreter | 解释器 — 定义语言的语法解释器 | [interpreter](references/behavioral/interpreter.md) |
| Iterator | 迭代器 — 顺序访问集合元素 | [iterator](references/behavioral/iterator.md) |
| Mediator | 中介者 — 集中管理对象间通信 | [mediator](references/behavioral/mediator.md) |
| Memento | 备忘录 — 保存和恢复对象状态 | [memento](references/behavioral/memento.md) |
| Mute Idiom | 静默惯用法 — 无侵入的异常抑制 | [mute-idiom](references/behavioral/mute-idiom.md) |
| Notification | 通知 — 事件告警增强系统通信 | [notification](references/behavioral/notification.md) |
| Null Object | 空对象 — 用无操作对象替代 null | [null-object](references/behavioral/null-object.md) |
| Observer | 观察者 — 一对多状态变化通知 | [observer](references/behavioral/observer.md) |
| Partial Response | 部分响应 — 按需发送数据优化传输 | [partial-response](references/behavioral/partial-response.md) |
| Pipeline | 管道 — 多阶段数据处理 | [pipeline](references/behavioral/pipeline.md) |
| Property | 属性 — 动态属性管理 | [property](references/behavioral/property.md) |
| Rate Limiting | 限流 — 控制请求速率防止过载 | [rate-limiting-pattern](references/behavioral/rate-limiting-pattern.md) |
| Specification | 规格 — 组合业务规则实现灵活查询 | [specification](references/behavioral/specification.md) |
| State | 状态 — 根据内部状态改变行为 | [state](references/behavioral/state.md) |
| Strategy | 策略 — 算法族可互换 | [strategy](references/behavioral/strategy.md) |
| Subclass Sandbox | 子类沙箱 — 限定子类可用的操作集合 | [subclass-sandbox](references/behavioral/subclass-sandbox.md) |
| Template Method | 模板方法 — 定义算法骨架，子类实现步骤 | [template-method](references/behavioral/template-method.md) |
| Template View | 模板视图 — 动态网页渲染 | [templateview](references/behavioral/templateview.md) |
| Update Method | 更新方法 — 系统化更新游戏对象 | [update-method](references/behavioral/update-method.md) |
| Visitor | 访问者 — 在不修改类的前提下添加新操作 | [visitor](references/behavioral/visitor.md) |

### 架构模式（Architectural）— 25 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Bloc | Bloc — 状态管理简化 | [bloc](references/architectural/bloc.md) |
| Clean Architecture | 整洁架构 — 可维护的架构风格 | [clean-architecture](references/architectural/clean-architecture.md) |
| CQRS | 命令查询职责分离 — 优化数据交互 | [command-query-responsibility-segregation](references/architectural/command-query-responsibility-segregation.md) |
| Event-Driven Architecture | 事件驱动架构 — 构建响应式可扩展系统 | [event-driven-architecture](references/architectural/event-driven-architecture.md) |
| Event Sourcing | 事件溯源 — 用事件记录构建不可变历史 | [event-sourcing](references/architectural/event-sourcing.md) |
| Flux | Flux — 单向数据流简化复杂 UI | [flux](references/architectural/flux.md) |
| Front Controller | 前端控制器 — 集中处理 Web 请求 | [front-controller](references/architectural/front-controller.md) |
| Hexagonal Architecture | 六边形架构 — 解耦核心逻辑 | [hexagonal-architecture](references/architectural/hexagonal-architecture.md) |
| Intercepting Filter | 拦截过滤器 — 增强 Web 请求处理 | [intercepting-filter](references/architectural/intercepting-filter.md) |
| Layered Architecture | 分层架构 — 构建可扩展可维护应用 | [layered-architecture](references/architectural/layered-architecture.md) |
| Microservices Aggregator | 微服务聚合器 — 构建复合服务 | [microservices-aggregrator](references/architectural/microservices-aggregrator.md) |
| Microservices Client-Side UI Composition | 客户端 UI 组合 — 组装微服务 UI | [microservices-client-side-ui-composition](references/architectural/microservices-client-side-ui-composition.md) |
| Microservices Distributed Tracing | 分布式追踪 — 增强服务通信可见性 | [microservices-distributed-tracing](references/architectural/microservices-distributed-tracing.md) |
| Model-View-Controller (MVC) | MVC — 分离模型、视图和控制器 | [model-view-controller](references/architectural/model-view-controller.md) |
| Model-View-Intent (MVI) | MVI — 构建稳健可扩展的 UI | [model-view-intent](references/architectural/model-view-intent.md) |
| Model-View-Presenter (MVP) | MVP — 增强 UI 逻辑分离 | [model-view-presenter](references/architectural/model-view-presenter.md) |
| Model-View-ViewModel (MVVM) | MVVM — 分离 UI 和逻辑 | [model-view-viewmodel](references/architectural/model-view-viewmodel.md) |
| Monolithic Architecture | 单体架构 — 内聚应用模型 | [monolithic-architecture](references/architectural/monolithic-architecture.md) |
| Naked Objects | 裸对象 — 利用领域对象动态生成 UI | [naked-objects](references/architectural/naked-objects.md) |
| Page Controller | 页面控制器 — 集中管理页面逻辑 | [page-controller](references/architectural/page-controller.md) |
| Polling Pub/Sub | 轮询发布订阅 — 异步消息优雅处理 | [polling-publisher](references/architectural/polling-publisher.md) |
| Presentation Model | 展示模型 — 增强 UI 数据管理 | [presentation-model](references/architectural/presentation-model.md) |
| Service Layer | 服务层 — 增强应用架构的稳固服务层 | [service-layer](references/architectural/service-layer.md) |
| Service to Worker | 服务到工作者 — 增强 UI 和业务逻辑集成 | [service-to-worker](references/architectural/service-to-worker.md) |
| View Helper | 视图助手 — 简化 MVC 中的展示逻辑 | [view-helper](references/architectural/view-helper.md) |

### 并发模式（Concurrency）— 22 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Active Object | 活动对象 — 高效异步处理 | [active-object](references/concurrency/active-object.md) |
| Actor Model | Actor 模型 — 优雅构建并发系统 | [actor-model](references/concurrency/actor-model.md) |
| Async Method Invocation | 异步方法调用 — 提升性能的异步编程 | [async-method-invocation](references/concurrency/async-method-invocation.md) |
| Backpressure | 背压 — 防止生产者过载消费者 | [backpressure](references/concurrency/backpressure.md) |
| Balking | 犹豫 — 条件不满足时立即返回 | [balking](references/concurrency/balking.md) |
| Double-Checked Locking | 双重检查锁定 — 最小开销确保线程安全 | [double-checked-locking](references/concurrency/double-checked-locking.md) |
| Event-Based Asynchronous | 基于事件的异步 — 非阻塞系统设计 | [event-based-asynchronous](references/concurrency/event-based-asynchronous.md) |
| Event Queue | 事件队列 — 高效管理并发事件 | [event-queue](references/concurrency/event-queue.md) |
| Fan-Out/Fan-In | 扇出扇入 — 最大化并发数据处理 | [fanout-fanin](references/concurrency/fanout-fanin.md) |
| Guarded Suspension | 守护挂起 — 安全控制临界区并发 | [guarded-suspension](references/concurrency/guarded-suspension.md) |
| Half-Sync/Half-Async | 半同步半异步 — 双处理模式提升系统性能 | [half-sync-half-async](references/concurrency/half-sync-half-async.md) |
| Leader Election | 领导者选举 — 节点协调和共识 | [leader-election](references/concurrency/leader-election.md) |
| Leader-Followers | 领导者跟随者 — 动态分配工作者 | [leader-followers](references/concurrency/leader-followers.md) |
| Lockable Object | 可锁定对象 — 稳健同步机制 | [lockable-object](references/concurrency/lockable-object.md) |
| Master-Worker | 主从 — 协调并发处理 | [master-worker](references/concurrency/master-worker.md) |
| Monitor | 监视器 — 用 monitor 实现稳健锁定 | [monitor](references/concurrency/monitor.md) |
| Poison Pill | 毒丸 — 优雅终止多线程处理 | [poison-pill](references/concurrency/poison-pill.md) |
| Producer-Consumer | 生产者消费者 — 优化生产消费流程 | [producer-consumer](references/concurrency/producer-consumer.md) |
| Promise | Promise — 简化异步任务提升性能 | [promise](references/concurrency/promise.md) |
| Reactor | 反应器 — 非阻塞事件驱动架构 | [reactor](references/concurrency/reactor.md) |
| Thread-Pool Executor | 线程池执行器 — 高效并发任务管理 | [thread-pool-executor](references/concurrency/thread-pool-executor.md) |
| Thread-Specific Storage | 线程特定存储 — 隔离的线程局部数据 | [thread-specific-storage](references/concurrency/thread-specific-storage.md) |

### 数据访问模式（Data Access）— 12 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Metadata Mapping | 元数据映射 — 无缝桥接对象和数据存储 | [metadata-mapping](references/data-access/metadata-mapping.md) |
| Optimistic Offline Lock | 乐观离线锁 — 数据库事务冲突解决 | [optimistic-offline-lock](references/data-access/optimistic-offline-lock.md) |
| Repository | 仓储 — 用抽象持久化简化数据访问 | [repository](references/data-access/repository.md) |
| Serialized Entity | 序列化实体 — 简化数据持久化和交换 | [serialized-entity](references/data-access/serialized-entity.md) |
| Serialized LOB | 序列化大对象 — 管理大型数据对象 | [serialized-lob](references/data-access/serialized-lob.md) |
| Sharding | 分片 — 水平分区提升吞吐量 | [sharding](references/data-access/sharding.md) |
| Single Table Inheritance | 单表继承 — 统一表结构的对象映射 | [single-table-inheritance](references/data-access/single-table-inheritance.md) |
| Table Inheritance | 表继承 — 关系数据库中的层次数据建模 | [table-inheritance](references/data-access/table-inheritance.md) |
| Table Module | 表模块 — 有组织的数据处理模块 | [table-module](references/data-access/table-module.md) |
| Transaction Script | 事务脚本 — 整合的业务逻辑脚本 | [transaction-script](references/data-access/transaction-script.md) |
| Unit of Work | 工作单元 — 高效事务管理 | [unit-of-work](references/data-access/unit-of-work.md) |
| Version Number | 版本号 — 稳健的版本管理 | [version-number](references/data-access/version-number.md) |

### 函数式模式（Functional）— 8 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Callback | 回调 — 异步通信 | [callback](references/functional/callback.md) |
| Collection Pipeline | 集合管道 — 简化数据操作 | [collection-pipeline](references/functional/collection-pipeline.md) |
| Combinator | 组合子 — 灵活的代码组合 | [combinator](references/functional/combinator.md) |
| Currying | 柯里化 — 增强函数灵活性和重用性 | [currying](references/functional/currying.md) |
| Function Composition | 函数组合 — 优雅的函数式管道 | [function-composition](references/functional/function-composition.md) |
| MapReduce | MapReduce — 并行数据处理 | [map-reduce](references/functional/map-reduce.md) |
| Monad | Monad — 函数式编程范式 | [monad](references/functional/monad.md) |
| Trampoline | 蹦床 — 无栈溢出的递归 | [trampoline](references/functional/trampoline.md) |

### 集成模式（Integration）— 5 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Ambassador | 大使 — 简化远程资源管理 | [ambassador](references/integration/ambassador.md) |
| Anti-Corruption Layer | 防腐层 — 确保与遗留系统的完整性 | [anti-corruption-layer](references/integration/anti-corruption-layer.md) |
| Gateway | 网关 — 简化外部系统集成 | [gateway](references/integration/gateway.md) |
| Microservices API Gateway | 微服务 API 网关 — 统一端点简化服务访问 | [microservices-api-gateway](references/integration/microservices-api-gateway.md) |
| Microservices Log Aggregation | 微服务日志聚合 — 集中日志增强监控 | [microservices-log-aggregation](references/integration/microservices-log-aggregation.md) |

### 弹性模式（Resilience）— 5 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Circuit Breaker | 断路器 — 增强系统弹性 | [circuit-breaker](references/resilience/circuit-breaker.md) |
| Queue-Based Load Leveling | 基于队列的负载均衡 — 平衡工作负载 | [queue-based-load-leveling](references/resilience/queue-based-load-leveling.md) |
| Retry | 重试 — 自适应重试构建容错系统 | [retry](references/resilience/retry.md) |
| Saga | Saga — 分布式系统中的长事务管理 | [saga](references/resilience/saga.md) |
| Tolerant Reader | 宽容读取器 — 增强 API 弹性和兼容性 | [tolerant-reader](references/resilience/tolerant-reader.md) |

### 消息模式（Messaging）— 4 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Data Bus | 数据总线 — 统一组件通信 | [data-bus](references/messaging/data-bus.md) |
| Event Aggregator | 事件聚合器 — 集中管理大型应用中的事件 | [event-aggregator](references/messaging/event-aggregator.md) |
| Microservices Idempotent Consumer | 幂等消费者 — 确保可靠消息处理 | [microservices-idempotent-consumer](references/messaging/microservices-idempotent-consumer.md) |
| Publish-Subscribe | 发布订阅 — 异步通信解耦组件 | [publish-subscribe](references/messaging/publish-subscribe.md) |

### 性能优化模式（Performance Optimization）— 3 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Caching | 缓存 — 加速数据访问 | [caching](references/performance-optimization/caching.md) |
| Data Locality | 数据局部性 — 高效数据管理提升性能 | [data-locality](references/performance-optimization/data-locality.md) |
| Lazy Loading | 延迟加载 — 按需初始化对象提升性能 | [lazy-loading](references/performance-optimization/lazy-loading.md) |

### 资源管理模式（Resource Management）— 3 个
| 模式 | 说明 | 文档 |
|------|------|------|
| RAII | 资源获取即初始化 — 安全的资源管理 | [resource-acquisition-is-initialization](references/resource-management/resource-acquisition-is-initialization.md) |
| Server Session | 服务器会话 — 安全管理的用户会话 | [server-session](references/resource-management/server-session.md) |
| Throttling | 节流 — 高需求应用中的资源优化 | [throttling](references/resource-management/throttling.md) |

### 惯用法模式（Idiom）— 1 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Immutable | 不可变 — 构建线程安全对象 | [immutable](references/idiom/immutable.md) |

### 服务发现模式（Service Discovery）— 1 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Microservices Self-Registration | 微服务自注册 — Spring Boot + Eureka | [microservices-self-registration](references/service-discovery/microservices-self-registration.md) |

### 测试模式（Testing）— 4 个
| 模式 | 说明 | 文档 |
|------|------|------|
| Arrange/Act/Assert | 3A — 测试清晰性和简洁性 | [arrange-act-assert](references/testing/arrange-act-assert.md) |
| Object Mother | 对象母亲 — 简化测试对象创建 | [object-mother](references/testing/object-mother.md) |
| Page Object | 页面对象 — 简化 UI 测试维护 | [page-object](references/testing/page-object.md) |
| Service Stub | 服务桩 — 用桩实现简化测试 | [service-stub](references/testing/service-stub.md) |

## 完整模式列表

### Behavioral 行为型模式（40）
[Acyclic Visitor](references/behavioral/acyclic-visitor.md) · [Bytecode](references/behavioral/bytecode.md) · [Chain of Responsibility](references/behavioral/chain-of-responsibility.md) · [Client Session](references/behavioral/client-session.md) · [Collecting Parameter](references/behavioral/collecting-parameter.md) · [Command](references/behavioral/command.md) · [Commander](references/behavioral/commander.md) · [Context Object](references/behavioral/context-object.md) · [Data Mapper](references/behavioral/data-mapper.md) · [Delegation](references/behavioral/delegation.md) · [Dirty Flag](references/behavioral/dirty-flag.md) · [Double Buffer](references/behavioral/double-buffer.md) · [Double Dispatch](references/behavioral/double-dispatch.md) · [Execute Around](references/behavioral/execute-around.md) · [Feature Toggle](references/behavioral/feature-toggle.md) · [Filterer](references/behavioral/filterer.md) · [Fluent Interface](references/behavioral/fluent-interface.md) · [Game Loop](references/behavioral/game-loop.md) · [Health Check](references/behavioral/health-check.md) · [Identity Map](references/behavioral/identity-map.md) · [Interpreter](references/behavioral/interpreter.md) · [Iterator](references/behavioral/iterator.md) · [Mediator](references/behavioral/mediator.md) · [Memento](references/behavioral/memento.md) · [Mute Idiom](references/behavioral/mute-idiom.md) · [Notification](references/behavioral/notification.md) · [Null Object](references/behavioral/null-object.md) · [Observer](references/behavioral/observer.md) · [Partial Response](references/behavioral/partial-response.md) · [Pipeline](references/behavioral/pipeline.md) · [Property](references/behavioral/property.md) · [Rate Limiting](references/behavioral/rate-limiting-pattern.md) · [Specification](references/behavioral/specification.md) · [State](references/behavioral/state.md) · [Strategy](references/behavioral/strategy.md) · [Subclass Sandbox](references/behavioral/subclass-sandbox.md) · [Template Method](references/behavioral/template-method.md) · [Template View](references/behavioral/templateview.md) · [Update Method](references/behavioral/update-method.md) · [Visitor](references/behavioral/visitor.md)

### Structural 结构型模式（35）
[Abstract Document](references/structural/abstract-document.md) · [Adapter](references/structural/adapter.md) · [Bridge](references/structural/bridge.md) · [Business Delegate](references/structural/business-delegate.md) · [Component](references/structural/component.md) · [Composite](references/structural/composite.md) · [Composite Entity](references/structural/composite-entity.md) · [Composite View](references/structural/composite-view.md) · [Converter](references/structural/converter.md) · [CRTP](references/structural/curiously-recurring-template-pattern.md) · [DAO Factory](references/structural/dao-factory.md) · [DAO](references/structural/data-access-object.md) · [DTO](references/structural/data-transfer-object.md) · [Decorator](references/structural/decorator.md) · [Domain Model](references/structural/domain-model.md) · [Dynamic Proxy](references/structural/dynamic-proxy.md) · [Extension Objects](references/structural/extension-objects.md) · [Facade](references/structural/facade.md) · [Flyweight](references/structural/flyweight.md) · [Marker Interface](references/structural/marker-interface.md) · [Money](references/structural/money.md) · [Parameter Object](references/structural/parameter-object.md) · [Private Class Data](references/structural/private-class-data.md) · [Proxy](references/structural/proxy.md) · [Role Object](references/structural/role-object.md) · [Separated Interface](references/structural/separated-interface.md) · [Servant](references/structural/servant.md) · [Service Locator](references/structural/service-locator.md) · [Session Facade](references/structural/session-facade.md) · [Spatial Partition](references/structural/spatial-partition.md) · [Special Case](references/structural/special-case.md) · [Strangler](references/structural/strangler.md) · [Twin](references/structural/twin.md) · [Value Object](references/structural/value-object.md) · [Virtual Proxy](references/structural/virtual-proxy.md)

### Architectural 架构模式（25）
[Bloc](references/architectural/bloc.md) · [Clean Architecture](references/architectural/clean-architecture.md) · [CQRS](references/architectural/command-query-responsibility-segregation.md) · [Event-Driven Architecture](references/architectural/event-driven-architecture.md) · [Event Sourcing](references/architectural/event-sourcing.md) · [Flux](references/architectural/flux.md) · [Front Controller](references/architectural/front-controller.md) · [Hexagonal Architecture](references/architectural/hexagonal-architecture.md) · [Intercepting Filter](references/architectural/intercepting-filter.md) · [Layered Architecture](references/architectural/layered-architecture.md) · [Microservices Aggregator](references/architectural/microservices-aggregrator.md) · [Client-Side UI Composition](references/architectural/microservices-client-side-ui-composition.md) · [Distributed Tracing](references/architectural/microservices-distributed-tracing.md) · [MVC](references/architectural/model-view-controller.md) · [MVI](references/architectural/model-view-intent.md) · [MVP](references/architectural/model-view-presenter.md) · [MVVM](references/architectural/model-view-viewmodel.md) · [Monolithic Architecture](references/architectural/monolithic-architecture.md) · [Naked Objects](references/architectural/naked-objects.md) · [Page Controller](references/architectural/page-controller.md) · [Polling Pub/Sub](references/architectural/polling-publisher.md) · [Presentation Model](references/architectural/presentation-model.md) · [Service Layer](references/architectural/service-layer.md) · [Service to Worker](references/architectural/service-to-worker.md) · [View Helper](references/architectural/view-helper.md)

### Concurrency 并发模式（22）
[Active Object](references/concurrency/active-object.md) · [Actor Model](references/concurrency/actor-model.md) · [Async Method Invocation](references/concurrency/async-method-invocation.md) · [Backpressure](references/concurrency/backpressure.md) · [Balking](references/concurrency/balking.md) · [Double-Checked Locking](references/concurrency/double-checked-locking.md) · [Event-Based Asynchronous](references/concurrency/event-based-asynchronous.md) · [Event Queue](references/concurrency/event-queue.md) · [Fan-Out/Fan-In](references/concurrency/fanout-fanin.md) · [Guarded Suspension](references/concurrency/guarded-suspension.md) · [Half-Sync/Half-Async](references/concurrency/half-sync-half-async.md) · [Leader Election](references/concurrency/leader-election.md) · [Leader-Followers](references/concurrency/leader-followers.md) · [Lockable Object](references/concurrency/lockable-object.md) · [Master-Worker](references/concurrency/master-worker.md) · [Monitor](references/concurrency/monitor.md) · [Poison Pill](references/concurrency/poison-pill.md) · [Producer-Consumer](references/concurrency/producer-consumer.md) · [Promise](references/concurrency/promise.md) · [Reactor](references/concurrency/reactor.md) · [Thread-Pool Executor](references/concurrency/thread-pool-executor.md) · [Thread-Specific Storage](references/concurrency/thread-specific-storage.md)

### Creational 创建型模式（14）
[Abstract Factory](references/creational/abstract-factory.md) · [Builder](references/creational/builder.md) · [Dependency Injection](references/creational/dependency-injection.md) · [Factory](references/creational/factory.md) · [Factory Kit](references/creational/factory-kit.md) · [Factory Method](references/creational/factory-method.md) · [Monostate](references/creational/monostate.md) · [Multiton](references/creational/multiton.md) · [Object Pool](references/creational/object-pool.md) · [Prototype](references/creational/prototype.md) · [Registry](references/creational/registry.md) · [Singleton](references/creational/singleton.md) · [Step Builder](references/creational/step-builder.md) · [Type Object](references/creational/type-object.md)

### Data Access 数据访问模式（12）
[Metadata Mapping](references/data-access/metadata-mapping.md) · [Optimistic Offline Lock](references/data-access/optimistic-offline-lock.md) · [Repository](references/data-access/repository.md) · [Serialized Entity](references/data-access/serialized-entity.md) · [Serialized LOB](references/data-access/serialized-lob.md) · [Sharding](references/data-access/sharding.md) · [Single Table Inheritance](references/data-access/single-table-inheritance.md) · [Table Inheritance](references/data-access/table-inheritance.md) · [Table Module](references/data-access/table-module.md) · [Transaction Script](references/data-access/transaction-script.md) · [Unit of Work](references/data-access/unit-of-work.md) · [Version Number](references/data-access/version-number.md)

### Functional 函数式模式（8）
[Callback](references/functional/callback.md) · [Collection Pipeline](references/functional/collection-pipeline.md) · [Combinator](references/functional/combinator.md) · [Currying](references/functional/currying.md) · [Function Composition](references/functional/function-composition.md) · [MapReduce](references/functional/map-reduce.md) · [Monad](references/functional/monad.md) · [Trampoline](references/functional/trampoline.md)

### Integration 集成模式（5）
[Ambassador](references/integration/ambassador.md) · [Anti-Corruption Layer](references/integration/anti-corruption-layer.md) · [Gateway](references/integration/gateway.md) · [Microservices API Gateway](references/integration/microservices-api-gateway.md) · [Microservices Log Aggregation](references/integration/microservices-log-aggregation.md)

### Resilience 弹性模式（5）
[Circuit Breaker](references/resilience/circuit-breaker.md) · [Queue-Based Load Leveling](references/resilience/queue-based-load-leveling.md) · [Retry](references/resilience/retry.md) · [Saga](references/resilience/saga.md) · [Tolerant Reader](references/resilience/tolerant-reader.md)

### Testing 测试模式（4）
[Arrange/Act/Assert](references/testing/arrange-act-assert.md) · [Object Mother](references/testing/object-mother.md) · [Page Object](references/testing/page-object.md) · [Service Stub](references/testing/service-stub.md)

### Messaging 消息模式（4）
[Data Bus](references/messaging/data-bus.md) · [Event Aggregator](references/messaging/event-aggregator.md) · [Idempotent Consumer](references/messaging/microservices-idempotent-consumer.md) · [Publish-Subscribe](references/messaging/publish-subscribe.md)

### Performance Optimization 性能优化模式（3）
[Caching](references/performance-optimization/caching.md) · [Data Locality](references/performance-optimization/data-locality.md) · [Lazy Loading](references/performance-optimization/lazy-loading.md)

### Resource Management 资源管理模式（3）
[RAII](references/resource-management/resource-acquisition-is-initialization.md) · [Server Session](references/resource-management/server-session.md) · [Throttling](references/resource-management/throttling.md)

### Idiom 惯用法模式（1）
[Immutable](references/idiom/immutable.md)

### Service Discovery 服务发现模式（1）
[Self-Registration](references/service-discovery/microservices-self-registration.md)

### Design Principles 设计原则（25）
[KISS](references/principles/kiss.md) · [YAGNI](references/principles/yagni.md) · [DRY](references/principles/dry.md) · [Separation of Concerns](references/principles/separation-of-concerns.md) · [SRP](references/principles/single-responsibility-principle.md) · [OCP](references/principles/open-closed-principle.md) · [LSP](references/principles/liskov-substitution-principle.md) · [ISP](references/principles/interface-segregation-principle.md) · [Composition Over Inheritance](references/principles/composition-over-inheritance.md) · [Encapsulate What Changes](references/principles/encapsulate-what-changes.md) · [Minimise Coupling](references/principles/minimise-coupling.md) · [Maximise Cohesion](references/principles/maximise-cohesion.md) · [Hide Implementation Details](references/principles/hide-implementation-details.md) · [Law of Demeter](references/principles/law-of-demeter.md) · [Inversion of Control](references/principles/inversion-of-control.md) · [Command Query Separation](references/principles/command-query-separation.md) · [Avoid Premature Optimization](references/principles/avoid-premature-optimization.md) · [Code For The Maintainer](references/principles/code-for-the-maintainer.md) · [Boy-Scout Rule](references/principles/boy-scout-rule.md) · [Robustness Principle](references/principles/robustness-principle.md) · [Orthogonality](references/principles/orthogonality.md) · [Curly's Law](references/principles/curlys-law.md) · [Murphy's Law](references/principles/murphys-law.md) · [Brooks's Law](references/principles/brooks-law.md) · [Linus's Law](references/principles/linus-law.md)
