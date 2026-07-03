---
name: ai-code-format-review
description: "Use when reviewing AI-generated code for formatting consistency. Enforces naming, structure, comments, and style conventions. Optimized for Java."
version: 1.0.0
author: Joey Liu
---

# AI-Generated Code Format Review

Review AI-generated code for compliance with team formatting standards. Focus on
**readability, consistency, and maintainability** — not functional correctness
(that's the job of `requesting-code-review`).

This skill is **Java-centric**, incorporating conventions from the
*Alibaba Java Development Manual*.

> **Rule Levels** (aligned with the Alibaba Manual):
> - **[Mandatory]**: Must follow — violation blocks the commit (P0)
> - **[Recommended]**: Strongly advised (P1)
> - **[Reference]**: Optional (P2)

## When to Use

- After AI generates/modifies code, before committing
- User says "review code format", "check code formatting", "format review"
- Code style inconsistencies found after generation
- Before batch-refactoring AI-generated code — assess format first

**Not for:** Bug investigation, security scanning, performance tuning — use `requesting-code-review` for those.

---

## I. Programming Rules

### (1) Naming Conventions

| Item | [Mandatory] Rule | Example |
|------|------------------|---------|
| Forbidden prefixes/suffixes | Must not start or end with `_` or `$` | ✗ `_name`, `name_`, `$Object` |
| No Pinyin | No Pinyin or Pinyin-English mixing, no Chinese names | ✗ `DaZhePromotion`, `getPingfenByName()` |
| Class names | UpperCamelCase; exceptions: DO/BO/DTO/VO/AO | `MarcoPolo`, `UserDO` ✗ `macroPolo` |
| Methods/variables/params | lowerCamelCase | `localValue`, `getHttpMessage()` |
| Constants | UPPER_SNAKE_CASE, semantically complete | `MAX_STOCK_COUNT` ✗ `MAX_COUNT` |
| Abstract classes | Prefix with `Abstract` or `Base` | `AbstractUserService` |
| Exception classes | Suffix with `Exception` | `UserNotFoundException` |
| Test classes | Tested class name + `Test` | `UserServiceTest` |
| Arrays | Brackets are part of the type | `String[] args` ✗ `String args[]` |
| Package names | All lowercase, singular, one word per segment | `com.alibaba.open.util` |
| Abbreviations | No non-standard abbreviations | ✗ `AbsClass`, `condi` |

**[Mandatory] POJO boolean fields must NOT have `is` prefix** (causes framework serialization errors):
```java
// ✗ BAD — RPC framework resolves the property name as "deleted" instead of "isDeleted"
private Boolean isDeleted;

// ✓ GOOD
private Boolean deleted;
```

**[Recommended] Names should reflect the design pattern:**
```java
// ✓ GOOD
public class OrderFactory { ... }
public class LoginProxy { ... }
public class ResourceObserver { ... }
```

**[Mandatory] Interface and implementation class naming:**
```java
// ✓ Service/DAO implementation classes end with Impl
public class CacheServiceImpl implements CacheService { ... }

// ✓ Capability interfaces use -able suffix
public interface Translatable { ... }
public abstract class AbstractTranslator implements Translatable { ... }
```

**[Reference] Enum naming:**
```java
// ✓ Enum class names end with Enum; members are ALL_CAPS
public enum ProcessStatusEnum {
    SUCCESS,
    UNKNOWN_REASON;
}
```

**[Reference] Service/DAO layer method naming:**
| Action | Prefix | Example |
|--------|--------|---------|
| Get single object | `get` | `getUserById()` |
| Get multiple objects | `list` | `listUsersByDept()` |
| Get count | `count` | `countActiveUsers()` |
| Insert | `save` / `insert` | `saveUser()` |
| Delete | `remove` / `delete` | `removeExpiredTokens()` |
| Update | `update` | `updateUserStatus()` |

**[Reference] Domain model naming:**
| Model | Suffix | Description |
|-------|--------|-------------|
| Data Object | `DO` | Maps to DB table, e.g. `UserDO` |
| Data Transfer Object | `DTO` | Business domain related |
| View Object | `VO` | Display/page related |
| Collective term | POJO | Umbrella for DO/DTO/BO/VO — **never** name `xxxPOJO` |

**Common AI naming issues:**
- Overly long names: `theCurrentLoggedInUserInformation` → `currentUser`
- Overly short names: `d`, `tmp`, `res` → use meaningful names
- Inconsistent naming for same concept: `user` / `usr` / `u` → unify as `user`
- Method names without verb prefix: `userInfo()` → `getUserInfo()`
- POJO boolean fields with `is`: `isActive` → `active` (POJO context)
- Inconsistent abbreviations: `HTTP` vs `Http` vs `http` → class `HttpClient`, variable `httpClient`

### (2) Constant Definitions

**[Mandatory] No magic values in code:**
```java
// ✗ BAD
String key = "Id#taobao_" + tradeId;
cache.put(key, value);

// ✓ GOOD
private static final String CACHE_KEY_PREFIX = "Id#taobao_";
cache.put(CACHE_KEY_PREFIX + tradeId, value);
```

**[Mandatory] Use uppercase `L` for long/Long literals:**
```java
// ✗ Lowercase l is easily confused with digit 1
Long a = 2l;

// ✓ GOOD
Long a = 2L;
```

**[Recommended] Group constants by function — don't use one god-constant class:**
```java
// ✓ Cache-related constants
public final class CacheConsts {
    public static final long DEFAULT_EXPIRE_MS = 30_000L;
}

// ✓ System config constants
public final class ConfigConsts {
    public static final String DEFAULT_ENCODING = "UTF-8";
}
```

**[Recommended] Constant reuse levels:** cross-app → app-wide → sub-project → package → class (`private static final`)

**[Recommended] Prefer enums over constants** when values are in a fixed range with extended attributes:
```java
public enum DayEnum {
    MONDAY(1), TUESDAY(2), WEDNESDAY(3), THURSDAY(4),
    FRIDAY(5), SATURDAY(6), SUNDAY(7);

    private final int code;
    DayEnum(int code) { this.code = code; }
    public int getCode() { return code; }
}
```

### (3) Code Formatting

**[Mandatory] Brace usage:**
```java
// Empty block — write as {}
public void noOp() {}

// Non-empty block
if (condition) {   // No line break before opening brace
    doSomething(); // Line break after opening brace
} else {           // No line break when followed by else
    doOther();     // Line break before closing brace
}                  // Must line break after terminal closing brace
```

**[Mandatory] No spaces inside parentheses:**
```java
// ✗ if ( a == b )
// ✓ if (a == b)
```

**[Mandatory] `if`/`for`/`while`/`do` must use braces (even for single-line bodies):**
```java
// ✗ Single line without braces
if (condition) return;

// ✓ Must use braces
if (condition) {
    return;
}
```

**[Mandatory] Spacing rules:**
- Spaces around binary operators: `a + b`, `x == y`
- Spaces around ternary `?` and `:`: `(a > b) ? a : b`
- Space after commas: `method(a, b, c)`
- Space after colon in for-each: `for (Item item : items)`
- No extra spaces where not needed

**[Mandatory] Indentation and line width:**
- Indentation: 4 spaces, no tabs
- Max line length: **120** characters
- Break after comma for multi-param methods exceeding 120 chars
- IDE settings: UTF-8 encoding, Unix line endings (`\n`)

**[Mandatory] Break long method signatures with aligned parameters:**
```java
// ✓ Long method signature — break and align
public Result<UserDTO> createUserWithProfile(
        String name,
        String email,
        AddressDTO address,
        UserProfileDTO profile) {
    ...
}
```

### (4) OOP Rules

**[Mandatory] Access static variables/methods via class name:**
```java
// ✗ BAD
object.staticMethod();

// ✓ GOOD
ClassName.staticMethod();
```

**[Mandatory] All overridden methods must have `@Override`:**
```java
@Override
public boolean equals(Object obj) { ... }

@Override
public int hashCode() { ... }
```

**[Mandatory] Varargs must be the last parameter; prefer `Object` over primitives:**
```java
// ✓ GOOD
public void method(String name, Object... args) { ... }
```

**[Mandatory] Prevent NPE in `equals` calls:**
```java
// ✗ BAD — str may be null, causing NPE
str.equals("abc");

// ✓ GOOD — constant/certain value on the left
"abc".equals(str);

// ✓ Use Objects.equals (Java 7+)
Objects.equals(str1, str2);
```

**[Mandatory] Use `equals` for all wrapper type comparisons — never `==`:**
```java
// ✗ Integer a = 128; Integer b = 128; a == b → false (beyond cache range)
// ✓ GOOD
Integer a = 128;
Integer b = 128;
a.equals(b);  // true
```

**[Mandatory] Use `BigDecimal` for floating-point — no `float`/`double`:**
```java
// ✗ BAD — precision loss
double price = 0.1 + 0.2;  // 0.30000000000000004

// ✓ GOOD
BigDecimal price = new BigDecimal("0.1").add(new BigDecimal("0.2"));
```

**[Mandatory] Use wrapper types for POJO/RPC return values and parameters:**
```java
// ✗ BAD — caller cannot distinguish 0 from "not called"
int getScore();

// ✓ GOOD
Integer getScore();
```

**[Mandatory] POJO classes must not set default values for fields:**
```java
// ✗ BAD
public class UserDO {
    private Integer age = 0;  // caller should assign
}

// ✓ GOOD
public class UserDO {
    private Integer age;
}
```

**[Mandatory] No business logic in constructors** (put initialization in `init` methods)

**[Recommended] Method order within a class:** public/protected → private → getter/setter

**[Recommended] Use `StringBuilder` for string concatenation in loops:**
```java
// ✗ BAD
String result = "";
for (String item : items) {
    result += item + ",";
}

// ✓ GOOD
StringBuilder sb = new StringBuilder();
for (String item : items) {
    sb.append(item).append(",");
}
String result = sb.toString();
```

**[Recommended] Use `instanceof` only for classes with inheritance relationships:**
```java
// ✗ No inheritance — structural code problem
if (animal instanceof Car) { ... }
```

**[Recommended] Use Builder pattern for constructors with many parameters:**
```java
// ✓ Use Builder when more than 4 parameters
var order = Order.builder()
    .userId(userId)
    .items(items)
    .shippingAddress(address)
    .paymentMethod(PaymentMethod.CREDIT_CARD)
    .build();
```

**Immutability first:**
```java
// ✗ Mutable collection exposed externally
public List<String> getTags() {
    return tags;
}

// ✓ Return unmodifiable view
public List<String> getTags() {
    return Collections.unmodifiableList(tags);
}
// Or List.copyOf(tags) (Java 10+)
```

### (5) Collection Handling

**[Mandatory] Overriding `equals` requires overriding `hashCode`**

**[Mandatory] Convert collection to array with `toArray(T[] array)`:**
```java
// ✗ BAD — loses type info
Object[] array = list.toArray();

// ✓ GOOD — returns T[] directly, no cast needed
String[] array = list.toArray(new String[0]);
```

**[Mandatory] `Arrays.asList()` result must not be structurally modified:**
```java
// ✗ BAD — throws UnsupportedOperationException
List<String> list = Arrays.asList("a", "b", "c");
list.add("d");

// ✓ GOOD — wrap with new ArrayList
List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
```

**[Mandatory] No `remove`/`add` operations inside `forEach`:**
```java
// ✗ BAD — ConcurrentModificationException
list.forEach(item -> {
    if (condition) list.remove(item);
});

// ✓ GOOD — use Iterator or removeIf
list.removeIf(item -> condition);
```

**[Recommended] Specify initial capacity for collections:**
```java
// ✗ BAD — default capacity 16, requires multiple resizes
Map<Long, User> map = new HashMap<>();

// ✓ GOOD — estimate element count to avoid resizing
Map<Long, User> map = new HashMap<>((int) (expectedSize / 0.75) + 1);
```

**[Mandatory] Map keys must not be modified**

**[Reference] Use `Set` for deduplication instead of `List.contains` (O(n) vs O(1))**

### (6) Concurrency

**[Mandatory] Singleton access must be thread-safe**

**[Mandatory] Use thread pools — no explicit `new Thread()`:**
```java
// ✗ BAD
new Thread(() -> doWork()).start();

// ✓ GOOD
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> doWork());
```

**[Mandatory] `SimpleDateFormat` is NOT thread-safe — must not be `static`:**
```java
// ✗ BAD
private static final SimpleDateFormat SDF = new SimpleDateFormat("yyyy-MM-dd");

// ✓ GOOD — DateTimeFormatter (Java 8+, thread-safe)
private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");
```

**[Mandatory] Lock multiple resources in consistent order to prevent deadlocks**

**[Mandatory] Clean up `ThreadLocal` variables in `finally`:**
```java
try {
    threadLocal.set(value);
    doWork();
} finally {
    threadLocal.remove();
}
```

**[Recommended] Prefer `CountDownLatch` for parallel processing; handle exceptions to avoid main thread timeout**

### (7) Control Statements

**[Mandatory] `switch` must have `default`**

**[Mandatory] `if`/`else`/`for`/`while`/`do` must use braces (even single-line)**

**[Mandatory] Watch for type mismatch and NPE in ternary operators:**
```java
// ✗ BAD — NPE from auto-unboxing when a is null
Integer a = null;
Integer b = (flag) ? a : 0;
```

**[Recommended] Use guard clauses instead of deep nesting:**
```java
// ✗ Deep nesting
public void process(Order order) {
    if (order != null) {
        if (order.isValid()) {
            if (order.isPaid()) {
                // core logic
            }
        }
    }
}

// ✓ Guard clauses
public void process(Order order) {
    if (order == null || !order.isValid()) {
        return;
    }
    if (!order.isPaid()) {
        return;
    }
    // core logic
}
```

**[Reference] Don't embed conditional results in other expressions:**
```java
// ✗ BAD
if ((condition ? method1() : method2()) == value) { ... }

// ✓ GOOD
String result = condition ? method1() : method2();
if (result.equals(value)) { ... }
```

### (8) Comment Rules

**[Mandatory] Class/field/method comments must use Javadoc (`/** */`)**

**[Mandatory] All abstract methods must have Javadoc**

**[Mandatory] All classes must include `@author`**

**[Mandatory] Single-line comments inside methods go on a separate line above the statement:**
```java
// ✗ BAD — comment after statement
doSomething(); // handle logic

// ✓ GOOD — comment on its own line
// Handle business logic
doSomething();
```

**[Mandatory] Update comments when modifying code; delete stale comments**

**[Mandatory] Comments explain *why*, not *what*:**
```java
// ✗ AI-generated redundant comment
// Get the order items
List<OrderItem> items = order.getItems();

// ✓ Explain why
// No discount calculation when order is empty — avoids meaningless division by zero
if (order.getItems().isEmpty()) {
    return BigDecimal.ZERO;
}
```

**[Mandatory] Commented-out code must include a reason; otherwise delete it (git has history)**

**[Recommended] Good code is self-documenting — remove unimportant comments**

**[Recommended] Use `TODO` / `FIXME` markers with author name and date**

**Javadoc tag conventions:**
```java
/**
 * Queries approved tickets by ID for monthly report generation.
 *
 * @param ticketId ticket ID, must be greater than 0
 * @return approved ticket details, or {@code null} if not found
 * @throws TicketNotFoundException if ticket doesn't exist or isn't approved
 * @author zhangsan
 * @since 1.2.0
 */
public TicketDTO getApprovedTicket(Long ticketId) { ... }
```

### (9) Miscellaneous

**[Mandatory] No `@RequestMapping` — use specific annotations (`@GetMapping` / `@PostMapping`, etc.)**

---

## II. Exceptions & Logging

### (1) Exception Handling

**[Mandatory] Prevent RuntimeExceptions with pre-checks instead of catching:**
```java
// ✗ BAD
try {
    obj.method();
} catch (NullPointerException e) { ... }

// ✓ GOOD
if (obj != null) {
    obj.method();
}
```

**[Mandatory] Do not use exceptions for flow control / condition control**

**[Mandatory] No catch-all for large code blocks:** Distinguish stable code from unstable code; catch specific exception types for unstable code

**[Mandatory] Catch blocks must handle the exception (at minimum log it) — no swallowing:**
```java
// ✗ P0: Swallowed exception
try {
    processPayment(order);
} catch (PaymentException e) {
    // empty or only e.printStackTrace()
}

// ✗ P0: Overly broad catch
try {
    parseJson(input);
} catch (Exception e) {
    throw new RuntimeException(e);
}

// ✓ Catch specific exceptions, log, decide whether to recover or rethrow
try {
    processPayment(order);
} catch (PaymentTimeoutException e) {
    log.warn("Payment timeout, orderId: {}, will retry", order.getId(), e);
    retryLater(order);
} catch (PaymentDeclinedException e) {
    log.warn("Payment declined, orderId: {}", order.getId());
    throw new OrderProcessingException("Payment declined", e);
}
```

**[Mandatory] If try block is inside a transaction, manual `rollback` is required in catch when needed**

**[Mandatory] finally must close resources (use try-with-resources for JDK 7+):**
```java
// ✗ P0: Resource not closed
InputStream is = new FileInputStream(file);
BufferedReader reader = new BufferedReader(new InputStreamReader(is));
String line = reader.readLine();
// Forgot to close!

// ✓ try-with-resources (must use for AutoCloseable)
try (var reader = new BufferedReader(new InputStreamReader(new FileInputStream(file)))) {
    String line = reader.readLine();
}
```

**[Mandatory] No `return` inside `finally` blocks**

**[Mandatory] Caught exception must match or be a parent of the thrown exception**

**[Recommended] Return values may be null — document when (NPE prevention is the caller's responsibility)**

**[Recommended] Common NPE scenarios to guard against:**
1. Returning a wrapper object when return type is primitive — auto-unboxing may NPE
2. Database query results may be null
3. Collection elements may be null even after `isNotEmpty` check
4. Remote call returns always require null check
5. Cascading calls `obj.getA().getB().getC()` are NPE-prone → use `Optional`

**[Recommended] Distinguish unchecked/checked exceptions; use business-meaningful custom exceptions:**
```java
// ✗ FORBIDDEN
throw new RuntimeException("error");

// ✓ GOOD
throw new UserNotFoundException("User not found: " + userId);
```

### (2) Logging Rules

**[Mandatory] Use SLF4J logging facade:**
```java
// ✗ BAD
System.out.println("user created: " + userId);
e.printStackTrace();

// ✓ GOOD
private static final Logger log = LoggerFactory.getLogger(UserService.class);
log.info("User created, userId={}", userId);
log.error("Processing failed, orderId={}", orderId, e);
```

**[Mandatory] Use conditional output for trace/debug/info levels (high-volume logging impacts performance):**
```java
// ✓ Avoid unnecessary concatenation at high volume
if (log.isDebugEnabled()) {
    log.debug("Order details: {}", order.toString());
}
```

**[Mandatory] Use parameter placeholders — no string concatenation in log statements:**
```java
// ✗ BAD
log.info("user: " + user.getName() + ", age: " + user.getAge());

// ✓ GOOD
log.info("user: {}, age: {}", user.getName(), user.getAge());
```

**[Mandatory] Production environments must not output info-level logs (use warn/error only)**

**[Mandatory] Log files must be retained for at least 15 days**

**[Recommended] Avoid logging inside loops (performance impact)**

**[Recommended] Use `warn` for business exceptions, `error` for system exceptions (avoid duplicate output)**

**[Recommended] Logs should contain key info (parameters, status, elapsed time) but be cautious with user PII**

---

## Java-Specific Review Dimensions

### Modern Java Features

**`var` local variable type inference (Java 10+):**
```java
// ✓ Use var when the type is obvious
var users = new ArrayList<String>();
var stream = list.stream().filter(u -> u.isActive());

// ✗ Don't use var when the type is unclear (P1)
var result = service.process(input);  // What type is result?
var data = repository.findByName(name);
```
Rule: Only use `var` when the right-hand side type is immediately obvious.

**Record classes (Java 16+):**
```java
// ✓ Use record for data-only DTOs/VOs
public record PointDTO(int x, int y, String label) {}
public record UserSummary(Long id, String name, String email) {}
```

**Text Blocks (Java 15+):**
```java
String json = """
        {
            "name": "%s",
            "age": %d
        }
        """.formatted(name, age);
```

**Switch Expressions (Java 14+):**
```java
String label = switch (status) {
    case PENDING -> "Pending";
    case APPROVED -> "Approved";
    case REJECTED -> "Rejected";
    default -> "Unknown";
};
```

**Pattern Matching:**
```java
// Java 16+ instanceof pattern matching
if (obj instanceof String s && s.length() > 5) {
    log.info("Long string: {}", s);
}

// Java 21+ switch pattern matching
return switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    default -> throw new IllegalArgumentException("Unknown shape");
};
```

### Stream & Optional

**[Recommended] Stream chains must not exceed 3 intermediate operations — split or use loops instead:**
```java
// ✗ P1: Stream chain too long
list.stream()
    .filter(x -> x.isValid())
    .map(x -> x.toDTO())
    .sorted(Comparator.comparing(DTO::getName))
    .distinct()
    .limit(10)
    .collect(Collectors.toList());

// ✓ Split into meaningful steps
var validDTOs = list.stream()
    .filter(Item::isValid)
    .map(Item::toDTO)
    .toList();

var topTen = validDTOs.stream()
    .sorted(Comparator.comparing(DTO::getName))
    .limit(10)
    .toList();
```

**[Recommended] Prefer method references over lambdas:** `Item::isValid` over `x -> x.isValid()`

**[Mandatory] No bare `.get()` on Optional:**
```java
// ✗ P0: Bare .get()
Optional<User> opt = repository.findById(id);
User user = opt.get();

// ✗ Not recommended: isPresent + get
if (opt.isPresent()) {
    User user = opt.get();
}

// ✓ orElseThrow / ifPresent / orElseGet
User user = repository.findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));

repository.findById(id)
    .ifPresent(user -> log.info("Found user: {}", user.getName()));
```

**[Recommended] Use `Optional` only for return values — not for parameters or fields**

### Collections & Generics

```java
// ✗ P0: Raw type
List list = new ArrayList();

// ✓ Generics + Diamond operator
List<String> names = new ArrayList<>();
Map<Long, User> userMap = new HashMap<>();

// ✗ Declared with concrete implementation (limits flexibility)
ArrayList<String> list = new ArrayList<>();

// ✓ Declare with interface type
List<String> list = new ArrayList<>();
Map<Long, User> map = new HashMap<>();
Set<String> set = new LinkedHashSet<>();
```

---

## Typical AI-Generated Java Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Verbose getter/setter boilerplate | Massive hand-written POJO boilerplate | Use `@Data` / record / Lombok |
| Overuse of `instanceof` + cast | Lack of polymorphism thinking | Use Visitor pattern or polymorphism |
| Swallowed exceptions | `catch (Exception e) {}` empty block | At minimum log, or rethrow |
| Raw types | `List list` without generics | `List<String> list` |
| Excessive null checks | Layers of `if (x != null)` | Use Optional or `@NonNull` annotations |
| String concatenation in loops | `str += "..."` inside loop | Use `StringBuilder` / `String.join` |
| Magic numbers/strings | `if (status == 3)` | Define enum or constant |
| Excessive static utility classes | All logic in static methods | Consider injectable Service |
| Over-deep Stream chains | More than 3 intermediate ops | Split into steps or use loops |
| Unclosed resources | Connection/Stream without try-with-resources | `try (var x = ...) {}` |
| Over-defensive programming | try-catch on every operation | Guard only where necessary |
| Redundant variables | `var result = getData(); return result;` | Directly `return getData()` |
| Duplicate code | Copy-pasted similar logic | Extract common methods |
| Unused imports | AI adds imports "just in case" | Remove unused imports |
| `@Autowired` field injection | Tight coupling, hard to test | Use constructor injection |
| `e.printStackTrace()` | Outputs to stderr, no logging framework | Use `log.error("msg", e)` |
| `==` comparing String / Integer | Reference comparison, not value | Use `.equals()` / `Objects.equals()` |
| Double for monetary values | Precision loss | Use `BigDecimal` |
| POJO boolean with `is` prefix | Framework serialization error | Remove `is` prefix in POJOs |
| switch without default | Unhandled unknown values | Must add `default` |
| Instance access to static members | Misleading to readers | Access statics via class name |
| Missing `@Override` | Typos won't trigger compile error | Add `@Override` to all overrides |
| `System.out.println` for logging | No logging framework | Use SLF4J `log.info()` |
| `HashMap` without initial capacity | Multiple resizes on large data | `new HashMap<>(expectedSize)` |
| `list.remove()` in loop | ConcurrentModificationException | Use `removeIf()` or Iterator |

---

## Review Workflow

### Step 1 — Obtain Code Under Review

```bash
git diff --cached        # Staged changes
git diff                 # Working directory
git diff HEAD~1 HEAD     # Last commit
```

### Step 2 — Detect Project Configuration

```bash
# Java project type detection
ls pom.xml build.gradle build.gradle.kts 2>/dev/null

# Formatting / static analysis config detection
ls checkstyle.xml spotbugs-exclude.xml pmd.xml .editorconfig 2>/dev/null
grep -l 'spotless\|checkstyle\|pmd\|spotbugs\|errorprone\|alibaba' \
  pom.xml build.gradle build.gradle.kts 2>/dev/null

# Lombok / MapStruct detection
grep -l 'lombok\|mapstruct' pom.xml build.gradle 2>/dev/null

# Logging framework detection
grep -l 'slf4j\|log4j\|logback' pom.xml build.gradle 2>/dev/null
```

If formatting tool config exists → use it as the baseline; skip rules that conflict.
If not → use the default rules in this skill (Alibaba conventions as baseline).

### Step 3 — Automated Checks

```bash
# === Maven projects ===
which mvn && mvn checkstyle:check -q 2>&1 | head -30
which mvn && mvn spotless:check 2>&1 | head -30
which mvn && mvn pmd:check -q 2>&1 | head -30
which mvn && mvn spotbugs:check -q 2>&1 | head -30

# === Gradle projects ===
./gradlew spotlessCheck 2>&1 | head -30
./gradlew pmdMain 2>&1 | head -30
./gradlew spotbugsMain 2>&1 | head -30

# === Standalone tools ===
which google-java-format && find . -name "*.java" \
  -not -path "*/target/*" -not -path "*/build/*" | \
  xargs google-java-format --set-exit-if-changed -n 2>&1 | head -30

# === Alibaba P3C rule scan (if integrated) ===
which mvn && mvn p3c:p3c-check -q 2>&1 | head -30
```

### Step 4 — Manual Review Checklist

**P0 — [Mandatory] Must fix (blocks commit):**
- [ ] Name starts/ends with `_` or `$`
- [ ] Name uses Pinyin or Pinyin-English mixing
- [ ] Inconsistent naming style in same file/package (camelCase vs snake_case)
- [ ] Public API missing Javadoc (`@param` / `@return` / `@throws`)
- [ ] Unused imports present
- [ ] Magic values in code (not defined as constants)
- [ ] `long`/`Long` literal uses lowercase `l`
- [ ] Exception swallowed (empty catch or only `e.printStackTrace()`)
- [ ] `catch (Exception e)` without justification
- [ ] Resource not using try-with-resources (Connection / Stream / Reader etc.)
- [ ] Raw type used (`List` without generic parameter)
- [ ] `String` / `Integer` compared with `==`
- [ ] `Optional.get()` without prior check
- [ ] Floating-point used for money (not `BigDecimal`)
- [ ] POJO boolean field with `is` prefix
- [ ] `switch` without `default`
- [ ] Overridden method missing `@Override`
- [ ] Static variable/method accessed via instance
- [ ] Collection modified inside `forEach` loop (`add`/`remove`)
- [ ] `SimpleDateFormat` declared `static`
- [ ] `System.out.println` / `e.printStackTrace()` used for logging
- [ ] `equals` called on potentially null object (not constant on left)

**P1 — [Recommended] Strongly advised to fix:**
- [ ] Method exceeds 30 lines without splitting
- [ ] Nesting exceeds 3 levels without guard clauses
- [ ] Typical AI redundant code present (see anti-pattern table)
- [ ] Inconsistent comment style / comments explain *what* instead of *why*
- [ ] Stream chain exceeds 3 intermediate operations
- [ ] `String +=` concatenation inside loops
- [ ] `var` used but right-hand type is unclear
- [ ] Field injection (`@Autowired` on field) instead of constructor injection
- [ ] Declared type uses concrete implementation (`ArrayList` instead of `List`)
- [ ] `HashMap` initialized without capacity
- [ ] Collection-to-array uses parameterless `toArray()`
- [ ] Log uses string concatenation instead of placeholder `{}`
- [ ] Improper log level (excessive debug/info logs without conditional output)
- [ ] Vararg is not the last parameter
- [ ] Logging inside loops (performance impact)
- [ ] Cascading calls without NPE guard: `obj.getA().getB().getC()`

**P2 — [Reference] Suggested improvements (non-blocking):**
- [ ] Could use record instead of plain data class
- [ ] Could use modern Java syntax (text block, switch expression, pattern matching)
- [ ] Import order doesn't follow convention (`java.*` → `javax.*` → third-party → project)
- [ ] Method reference can replace lambda: `x -> x.getName()` → `Item::getName`
- [ ] Inconsistent blank line count
- [ ] Could use `List.copyOf()` instead of `Collections.unmodifiableXxx()`
- [ ] Constants not grouped by function (all in one god-constant class)
- [ ] Enum class name missing `Enum` suffix
- [ ] Domain model suffix non-standard (e.g. `xxxPOJO`)

### Step 5 — Output Review Report

Format:

```
=== AI Code Format Review Report ===

File: src/main/java/com/example/user/UserService.java

[P0] L15-20: Naming inconsistency — method uses camelCase (getUserById),
     but another file in the same package uses snake_case (get_user_by_id)
     → Unify to camelCase (Alibaba Manual [Mandatory])

[P0] L42: Public method missing Javadoc
     public User createUser(CreateUserRequest request) {
     → Add Javadoc with @param and @return (Alibaba Manual [Mandatory])

[P0] L88-95: Exception swallowed
     catch (IOException e) { /* empty */ }
     → At minimum log or rethrow (Alibaba Manual [Mandatory])

[P0] L105: Magic value
     if (status == 3) { ... }
     → Define StatusEnum or constant (Alibaba Manual [Mandatory])

[P1] L55-95: Method body is 40 lines — consider splitting
     → Extract validation logic to validateCreateRequest()

[P1] L102: String concatenation in loop
     result += item.getName() + ",";
     → Use StringBuilder (Alibaba Manual [Recommended])

[P2] L7: Unused import
     import java.util.stream.Stream;
     → Remove

Stats: P0 x4, P1 x2, P2 x1
```

### Step 6 — Auto-Fix (Optional)

```bash
# Maven: Spotless auto-format (google-java-format)
mvn spotless:apply

# Gradle: Spotless auto-format
./gradlew spotlessApply

# Standalone: google-java-format direct fix
find . -name "*.java" -not -path "*/target/*" -not -path "*/build/*" | \
  xargs google-java-format --replace

# Remove unused imports (IDE operation)
# IntelliJ: Ctrl+Alt+O (Optimize Imports)
# VS Code + Java Extension: "Organize Imports"
```
