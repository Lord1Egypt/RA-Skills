# js2java — JavaScript 到 Java 全栈翻译助手

> 粘贴一段 JS 代码，输出一套可运行的 Spring Boot 代码 + 语法对照表 + 学习思考题

## 何时使用

当你想做这些事情时调用此 skill：

- 「帮我把这段 JS 代码转成 Java」
- 「用 Java 怎么写这个逻辑」
- 「教我 Java，我要写后端接口」
- 「前端转全栈，帮我翻译代码」

## 核心功能

**1. 完整分层代码**
- 生成符合 Spring Boot 规范的完整四层结构
- Entity（数据库实体） + DTO（数据传输对象）
- Repository（数据访问层） + Service（业务逻辑层）
- Controller（REST 接口） + Exception（自定义异常）
- GlobalExceptionHandler（全局异常处理）

**2. 注释即教学**
- 每处 Java 特有语法都标注 `// 👉 学习点：xxx`
- 解释为什么不能像 JS 那样写
- 指出 JS 和 Java 的本质差异

**3. 三部分输出**
- Part 1：可直接运行的完整 Java 代码（七个类文件）
- Part 2：JS ↔ Java 语法对照表
- Part 3：2-3 道动态生成的学习思考题（题目和答案都从实际翻译的代码里生长出来）

## 完整示例

### 输入（JS 代码）

```javascript
// 用户注册登录逻辑
const users = [];

function register(name, email, password) {
  if (!name || !email || !password) {
    return { error: '所有字段必填' };
  }

  const exists = users.find(u => u.email === email);
  if (exists) {
    return { error: '邮箱已被注册' };
  }

  const user = {
    id: Date.now(),
    name,
    email,
    password,
    createdAt: new Date()
  };

  users.push(user);
  return { success: true, user };
}

function login(email, password) {
  const user = users.find(u => u.email === email && u.password === password);
  if (!user) {
    return { error: '邮箱或密码错误' };
  }
  return { success: true, user };
}
```

### 输出（Java 代码）

#### 1. UserEntity.java（数据库实体）
```java
@Entity
@Table(name = "users")
public class UserEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(name = "created_at")
    private LocalDateTime createdAt;
}
```

#### 2. UserDTO.java（数据传输对象）
```java
@Data
public class UserDTO {
    private Long id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
}
```

#### 3. CreateUserRequest.java（请求校验 DTO）
```java
@Data
public class CreateUserRequest {
    @NotBlank(message = "用户名不能为空")
    private String name;

    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;

    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度需在 6-20 位之间")
    private String password;
}
```

#### 4. UserRepository.java（数据访问层）
```java
public interface UserRepository extends JpaRepository<UserEntity, Long> {
    boolean existsByEmail(String email);

    Optional<UserEntity> findByEmailAndPassword(String email, String password);
}
```

#### 5. 自定义异常类
```java
public class UserAlreadyExistsException extends RuntimeException {
    public UserAlreadyExistsException(String message) {
        super(message);
    }
}

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}
```

#### 6. GlobalExceptionHandler.java（全局异常处理）
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(UserNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(404, ex.getMessage()));
    }

    @ExceptionHandler(UserAlreadyExistsException.class)
    public ResponseEntity<ErrorResponse> handleAlreadyExists(UserAlreadyExistsException ex) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
            .body(new ErrorResponse(409, ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .collect(Collectors.joining(", "));
        return ResponseEntity.badRequest().body(new ErrorResponse(400, message));
    }

    public record ErrorResponse(int code, String message) {}
}
```

#### 7. UserService.java（业务逻辑层）
```java
@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public UserDTO register(CreateUserRequest request) {
        // 👉 学习点：existsByEmail 是 Spring Data JPA 自动生成的方法
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new UserAlreadyExistsException("邮箱已被注册");
        }

        UserEntity entity = new UserEntity();
        entity.setName(request.getName());
        entity.setEmail(request.getEmail());
        entity.setPassword(request.getPassword()); // 实际项目应加密
        entity.setCreatedAt(LocalDateTime.now());

        UserEntity saved = userRepository.save(entity);
        return toDTO(saved);
    }

    public UserDTO login(String email, String password) {
        // 👉 学习点：findByEmailAndPassword 是 Repository 自动生成的查询方法
        UserEntity user = userRepository.findByEmailAndPassword(email, password)
            .orElseThrow(() -> new UserNotFoundException("邮箱或密码错误"));
        return toDTO(user);
    }

    private UserDTO toDTO(UserEntity entity) {
        UserDTO dto = new UserDTO();
        dto.setId(entity.getId());
        dto.setName(entity.getName());
        dto.setEmail(entity.getEmail());
        dto.setCreatedAt(entity.getCreatedAt());
        return dto;
    }
}
```

#### 8. UserController.java（REST 接口）
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/register")
    public ResponseEntity<UserDTO> register(@Valid @RequestBody CreateUserRequest request) {
        UserDTO user = userService.register(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    @PostMapping("/login")
    public ResponseEntity<UserDTO> login(@RequestBody LoginRequest request) {
        UserDTO user = userService.login(request.getEmail(), request.getPassword());
        return ResponseEntity.ok(user);
    }
}
```

---

## 语法对照表

| JavaScript | Java | 学习要点 |
|-----------|------|---------|
| `const x = 1` | `int x = 1;` | 必须声明类型，不能用 var/let/const |
| `const s = "hi"` | `String s = "hi";` | 字符串是 String 类（大写S），不是关键字 |
| `const arr = []` | `List<String> arr = new ArrayList<>();` | Java 不能用字面量创建集合 |
| `arr.filter(fn)` | `list.stream().filter(fn).collect(...)` | Java 用 Stream API 处理集合 |
| `obj.name` | `obj.getName()` | Java 用 getter 方法访问属性 |
| `function fn(a) {}` | `public void fn(String a) {}` | 必须有返回类型和参数类型 |
| `undefined` | `null` | Java 没有 undefined，只有 null |
| `obj?.name` | `obj.getName()`（需判空） | Java 没有可选链，要手动判空 |
| `async/await` | `CompletableFuture` 或同步方法 | Java 没有 async/await 关键字 |
| `Date.now()` | `System.currentTimeMillis()` | 获取当前时间戳 |
| `new Date()` | `LocalDateTime.now()` | 推荐使用 Java 8+ 日期时间 API |
| `const STATUS = { ACTIVE: 'active' }` | `public enum Status { ACTIVE, INACTIVE }` | 枚举类型 |
| `return { error: 'msg' }` | `throw new XxxException("msg")` | 错误处理：抛异常而不是返回错误对象 |

---

## JS 异步模式在 Java 中的对应

| JavaScript | Java |
|------------|------|
| `async function` | `CompletableFuture<T>` 或同步方法 |
| `await promise` | `future.get()` 或直接调用同步方法 |
| `Promise.all([p1, p2])` | `CompletableFuture.allOf(f1, f2)` |
| `setTimeout(fn, 1000)` | `@Scheduled` 或 `ScheduledExecutorService` |

---

## 日期时间处理

```java
// Java 8+ 推荐用法
LocalDateTime now = LocalDateTime.now();

// 格式化
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = now.format(formatter);

// 计算
LocalDateTime tomorrow = now.plusDays(1);
```

---

## 枚举类型

```java
public enum Status {
    ACTIVE("活跃"),
    INACTIVE("未激活");

    private final String description;

    Status(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
```

---

## 学习思考题

**题目从翻译的代码里动态生成，不是从题库选。**

翻译完成后，分析实际出现了哪些 Java 模式，针对每种模式生成 1 道题。题目直接引用刚翻译的代码，答案也结合代码讲解。

### 示例

翻译的代码中有：
```java
List<UserEntity> users = userRepository.findAll();
return users.stream()
    .filter(u -> u.getStatus().equals("active"))
    .map(this::toDTO)
    .collect(Collectors.toList());
```

生成的思考题：

**Q:** `users.stream().filter().map().collect()` 这一串链式调用，JS 直接就能用。Java 为什么要先转 `stream()` 才能链式调用？

**参考要点：**
- `ArrayList` 本身没有 `.filter()` 方法。JS 的数组是内置支持链式的，Java 的 `List` 是接口，计算能力在 `Stream` 里
- `stream()` 是惰性求值：调用 `filter()` 时不立即执行，只是记录操作链，遇到 `collect()` 才真正触发
- `.parallelStream()` 能把计算分发到多线程

---

（根据实际翻译的代码动态生成 2-3 道题）

---

## 设计原则

- **保持业务逻辑一致** — 不改变算法逻辑，只改变语法
- **强类型系统** — 所有变量、参数、返回值必须声明类型
- **Spring Boot 规范** — 四层架构、Repository 注解、构造器注入
- **异常处理** — 自定义异常 + 全局异常处理器，不是返回 Map
- **参数校验** — @Valid + Bean Validation 注解
- **注释即教学** — 每处 Java 特有语法都有学习注释

## 使用限制

- ✅ CRUD、数据处理、条件判断
- ✅ 常见集合操作（filter/map/reduce）
- ✅ REST API 设计
- ✅ Repository 数据访问层
- ✅ 异常处理和参数校验
- ❌ 复杂多线程/并发代码
- ❌ 需要深度架构设计的代码（微服务、分布式事务）

---

**适合学习参考，生产环境使用前需 code review。**
