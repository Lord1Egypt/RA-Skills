# 11 · 命名与编码规约（阿里巴巴 Java 开发手册吸收）

> 来源：阿里巴巴 Java 开发手册（泰山版）精选。聚焦命名风格、常量定义、OOP 规约、控制语句、代码格式。
> 仅收录「Agent 真实会踩」的规约；纯风格偏好（如空格对齐细节）不收录。
> 与现有 reference 不重复：日期线程安全见 `03`，Bean 拷贝见 `06`，加密见 `07`，异常处理见 `08`，并发见 `05`。
> 每条配 ✗ 禁止 → ✓ 推荐 → 为什么。

## 命名风格

### 1. POJO 布尔属性禁 `is` 前缀
```java
// ✗
public class User {
    private Boolean isDeleted;
    public Boolean getIsDeleted() { return isDeleted; }
}
// ✓
public class User {
    private Boolean deleted;
    public Boolean getDeleted() { return deleted; }
}
```
> Jackson/Fastjson/Dubbo 反向解析时 `isDeleted` 可能被解析为属性名 `deleted`，导致字段丢失——用 `deleted`/`enabled`/`active`，不加 `is` 前缀。

### 2. 数组定义 `类型[]` 在前（非 `变量[]`）
```java
// ✗
int data[];
String args[];
// ✓
int[] data;
String[] args;
```

### 3. 抽象类用 `Abstract` 或 `Base` 开头
```java
// ✗
public abstract class Service { }
public abstract class Repository { }
// ✓
public abstract class AbstractService { }
public abstract class BaseRepository { }
```

### 4. 异常类用 `Exception` 结尾
```java
// ✗
public class BizError extends RuntimeException { }
public class UserNotFound extends RuntimeException { }
// ✓
public class BizException extends RuntimeException { }
public class UserNotFoundException extends RuntimeException { }
```
> **为什么**：`Error` 后缀易与 `java.lang.Error`（JVM 级错误）混淆——业务异常**禁用 `Error` 后缀**，统一用 `Exception`。

### 5. 包名全小写、单数、禁下划线
```java
// ✗
package com.company.User_Service;
package com.company.utils_tool;
// ✓
package com.company.userservice;
package com.company.util;
```

### 6. 禁拼音与英文混用
```java
// ✗
public class YonghuService { }       // 全拼音
public class UserService { }         // 英文
public class UserFWService { }       // 混用（fw=服务）
// ✓
public class UserService { }         // 全英文，统一
```

### 7. 常量全大写、下划线分隔
```java
// ✗
static final int maxRetry = 3;
static final String defaultCharset = "UTF-8";
// ✓
static final int MAX_RETRY = 3;
static final String DEFAULT_CHARSET = "UTF-8";
```

## 常量定义

### 8. 禁魔法值（未定义常量直出）
```java
// ✗
if (user.getStatus() == 3) { ... }           // 3 是什么？
long timeout = 5000L;                          // 5000ms？5s？
if ("ADMIN".equals(user.getRole())) { ... }   // "ADMIN" 散落多处

// ✓
static final int STATUS_LOCKED = 3;
static final long TIMEOUT_MS = 5000L;
static final String ROLE_ADMIN = "ADMIN";
if (user.getStatus() == STATUS_LOCKED) { ... }
if (ROLE_ADMIN.equals(user.getRole())) { ... }
```
> 状态/类型码优先用**枚举**（`enum`），全局配置用常量类。

### 9. `long` 字面量用大写 `L`
```java
// ✗
long value = 10000l;     // 小写 l 易与数字 1 混淆
// ✓
long value = 10000L;     // 大写 L 一眼可辨
```

## OOP 规约

### 10. 组合优于继承
```java
// ✗ 为了复用 extends 一个实现类
public class OrderService extends BaseRepository<Order> {
    // 只想要 Repository 的 CRUD，但被迫继承所有方法（含不该暴露的）
}

// ✓ 组合：持引用，按需调用
public class OrderService {
    private final OrderRepository orderRepo;  // 组合
    // 只暴露需要的方法
}
```
> 边界：仅「真正的 is-a 关系」才继承（如 `Circle extends Shape`）；复用代码优先组合（has-a，松耦合）。

### 11. `equals`/`hashCode`/`toString` 重写须遵守契约
```java
// ✗ 只重写 equals 不重写 hashCode → HashMap/HashSet 行为异常
public class User {
    private String id;
    @Override public boolean equals(Object o) {
        return o instanceof User u && id.equals(u.id);
    }
    // 缺 hashCode！
}

// ✓ equals 和 hashCode 成对重写，基于相同字段
public class User {
    private String id;
    @Override public boolean equals(Object o) {
        return o instanceof User u && Objects.equals(id, u.id);
    }
    @Override public int hashCode() {
        return Objects.hash(id);
    }
    @Override public String toString() {
        return "User{id='" + id + "'}";
    }
}
```
> 契约：`a.equals(b)` 为 true 则 `a.hashCode() == b.hashCode()` 必须为 true；只重写 equals 不重写 hashCode，HashMap/HashSet 会把「相等」对象放到不同桶。**推荐用 Lombok `@EqualsAndHashCode`/`@ToString` 或 record 自动生成**。

### 12. `@Override` 必加
```java
// ✗ 重写父类方法不加 @Override
public class OrderService extends BaseService {
    public void process(Order order) { ... }  // 拼错成 procsess？签名变了？无感知
}

// ✓ 加 @Override，编译器校验
public class OrderService extends BaseService {
    @Override
    public void process(Order order) { ... }  // 签名不匹配 → 编译报错
}
```
> 不加 `@Override`，若父类签名变更或子类拼错方法名，会**静默变成新方法**（bug 不显式报错）；加了则编译期报错。

### 13. 禁 raw type 滥用
```java
// ✗ raw type，类型安全丧失
List list = new ArrayList();
list.add("hello");
list.add(123);            // 编译通过，运行时 ClassCastException
Map map = new HashMap();

// ✓ 泛型参数显式声明
List<String> list = new ArrayList<>();
list.add("hello");
// list.add(123);        // 编译报错，类型安全
Map<String, User> map = new HashMap<>();
```
> raw type 跳过编译期检查，运行时 `ClassCastException` 难排查。**例外**：与遗留 API 交互被迫用 raw type 时，加 `@SuppressWarnings("unchecked")` + 注释说明。

### 14. 接口 `default` 方法边界
```java
// ✗ default 方法写业务逻辑，接口变臃肿
public interface UserService {
    default User findById(Long id) {
        // 20 行业务逻辑塞在接口里
        return repo.findById(id).orElseThrow();
    }
}

// ✓ default 仅用于工具方法/向后兼容，不放业务逻辑
public interface UserService {
    User findById(Long id);  // 抽象方法

    // default 仅：工具方法 / 兼容旧接口
    default Optional<User> findByIdOptional(Long id) {
        return Optional.ofNullable(findById(id));
    }
}
```

## 控制语句

### 15. 复杂布尔表达式先赋具名变量
```java
// ✗ 嵌套条件，读不出语义
if (user != null && user.getAge() > 18 && user.getStatus() == ACTIVE
        && !user.getRoles().isEmpty() && user.getRoles().contains(ROLE_ADMIN)) {
    doSomething();
}

// ✓ 先赋具名变量，条件自解释
boolean isAdult = user != null && user.getAge() > 18;
boolean isActive = user != null && user.getStatus() == ACTIVE;
boolean isAdmin = user != null && user.getRoles().contains(ROLE_ADMIN);
if (isAdult && isActive && isAdmin) {
    doSomething();
}
```
> 阈值：超过 3 个逻辑子条件时必须拆（关联 Sonar java:S3776 认知复杂度，见 `12-complexity.md`）。

### 16. `switch` 必有 `default`
```java
// ✗ 无 default，未知值静默跳过
switch (status) {
    case ACTIVE: doActive(); break;
    case INACTIVE: doInactive(); break;
    // status=PENDING → 无任何处理，bug 隐患
}

// ✓ 有 default，兜底处理或抛异常
switch (status) {
    case ACTIVE: doActive(); break;
    case INACTIVE: doInactive(); break;
    default: throw new IllegalStateException("未知状态: " + status);
}
```
> 枚举的 switch 配合 `default` 抛异常——新增枚举值时若忘了处理，运行期立即暴露而非静默。
>
> **例外**：JDK 21+ `switch` 模式匹配 + `sealed` 类型有编译期穷尽检查时，可不写 default。

## 代码格式

### 17. 单行 ≤120 字符
```java
// ✗ 超长行，横向滚动读不完
String result = someVeryLongMethodName(param1, param2, param3, param4, param5, param6, param7, param8, param9);

// ✓ 换行对齐，每行 ≤120
String result = someVeryLongMethodName(
    param1, param2, param3, param4, param5,
    param6, param7, param8, param9);
```

### 18. 4 空格缩进，禁 tab
```java
// ✗ tab 缩进（不同编辑器 tab 宽度不同，显示不一致）
if (cond) {
→   doA();
→   if (inner) {
→   →   doB();
→   }
}

// ✓ 4 空格缩进（全编辑器一致）
if (cond) {
    doA();
    if (inner) {
        doB();
    }
}
```

### 19. 无用 import 必须移除（Sonar java:S1128）
```java
// ✗ 四类无用 import
import java.util.List;            // 未使用
import java.util.List;            // 重复
import java.lang.String;          // java.lang 隐式导入
import com.demo.order.OrderVO;    // 与当前类同包

// ✓ 只保留真实使用的 import；改完代码顺手清理
import java.util.Map;
```
> **Agent 高频坑**：删除了某类的最后一处使用时，必须同步删除对应 import——这是生成/重构代码最高频的 S1128 来源。IDE `Optimize Imports`（IDEA: Ctrl+Alt+O）可一键清理。
