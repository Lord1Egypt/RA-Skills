---
name: java-circular-dependency-breaker
description: "Break circular dependencies in Java multi-module Gradle/Maven projects using interface extraction and business service separation. Triggers: 'circular dependency', '循环依赖', 'move service to another module', '模块循环依赖'."
origin: project
---

# Java Circular Dependency Breaker

Two battle-tested patterns for breaking circular dependencies between Java multi-module projects (Gradle or Maven).

## When to Activate

- Gradle multi-module project with `api project(':module-a')` and `api project(':module-b')` forming a cycle, **or** Maven project with `<dependency><artifactId>module-a</artifactId></dependency>` forming a cycle
- Refactoring a monolithic module into smaller modules without breaking existing code
- Moving service classes from one module to another while callers still reference concrete implementations
- A class has methods that depend on services from both modules, preventing direct migration

## Design Pattern

This skill applies the **Mediator Pattern** — introducing an intermediary (interface or business service) to decouple modules that directly depend on each other. Instead of Module A referencing Module B's concrete class directly, the mediator sits between them, allowing both to evolve independently.

- **Pattern 1** uses a service interface as the mediator — callers depend only on the abstraction.
- **Pattern 2** uses a service layer as the mediator — it coordinates cross-module logic without duplicating data access, keeping the migrated base class pure.

## Requirements

- JDK 8+ (for `javap`)
- Gradle or Maven build tool
- Git (for rollback)

## Before You Start

> **Checkpoint 0** — Confirm preconditions before choosing a pattern:

- [ ] Identify the concrete class causing the cycle
  - Gradle: `./gradlew :module-a:dependencies --configuration compileClasspath | grep module-b`
  - Maven: `mvn dependency:tree -pl module-a | grep module-b`
- [ ] Confirm the class is referenced by **at least one external module** (otherwise just move it, no interface needed)
- [ ] Compile all affected modules — **all tests must pass** before refactoring
  - Gradle: `./gradlew compileJava compileTestJava`
  - Maven: `mvn compile test-compile`
- [ ] Read the Decision Tree below to choose the correct pattern

**⚠️ Stop and ask the user if:**
- The class has over 20 public methods (suggest splitting first)
- The class is heavily mocked in tests across 5+ files (migration cost is high)
- The module cycle involves 3+ modules (may need sequential application of patterns)

## Pattern 1: Interface Extraction

Use when: Module A references a concrete class in Module B, and the class has no cross-module method dependencies.

### Prerequisites

| Item | Description |
|------|-------------|
| **Input** | A concrete `@Service` / `@Component` class in Module B that is referenced by Module A |
| **Constraint** | The class's public methods must NOT depend on services/classes from Module A |
| **Time estimate** | 15–30 min for a class with ≤10 public methods |
| **Risk** | Low — changes are mechanical and compiler-verified |

### Steps

1. **Create the interface** in a shared module (or new `*-interface` module)
   - Extract all public methods from the concrete class
   - Keep the same method signatures, parameter types, return types
   - Name convention: `IXxxService` (or your project's interface naming convention)
   
   > **Checkpoint 1** — Before proceeding, verify:
   > - [ ] Interface methods are a **strict subset** of the concrete class's public methods (no extras)
   > - [ ] Return types and parameter types in the interface do **not** depend on the source module
   > - [ ] Run `javap -public com.example.module.NotificationService` and diff against interface

2. **Implement the interface** in the target module
   - Add `implements IXxxService` to the concrete class
   - Keep `@Service` / `@Component` annotations
   
   > **Checkpoint 2** — Confirm:
   > - [ ] `./gradlew :module-b:compileJava` passes (or `mvn -pl module-b compile`)
   > - [ ] Spring context loads without bean name conflicts (check `@Qualifier` if needed)

3. **Update all callers** in the source module
   - Change field declaration from concrete class to interface
   - Update `import` from `com.example.module.Class` to `com.example.interface.IXxxService`
   
   > **Checkpoint 3** — Confirm:
   > - [ ] Zero remaining imports of the concrete class in the source module (`grep -r "import com.example.module.NotificationService" module-a/src/` returns empty)
   > - [ ] Test mocks updated: `@Mock BeanName` → `@Mock IBeanName` (do this **before** removing the gradle dependency)

4. **Remove the dependency** from source module's build file
   - Gradle (`build.gradle`): Delete `api project(':module-b')`, keep `api project(':module-interface')`
   - Maven (`pom.xml`): Delete the `module-b` dependency `<dependency>` block
   
   > **Checkpoint 4** — Final verification:
   > - [ ] `./gradlew :module-a:compileJava` or `mvn -pl module-a compile` passes
   > - [ ] `./gradlew :module-a:compileTestJava` or `mvn -pl module-a test-compile` passes
   > - [ ] `./gradlew :module-a:dependencies --configuration compileClasspath | grep module-b` or `mvn dependency:tree -pl module-a | grep module-b` returns **EMPTY**
   
   > **⚠️ If compilation fails:** Re-add the dependency (`build.gradle` or `pom.xml`), fix the error, then remove again. Do **not** leave the codebase in a broken state.

### Example

```java
// BEFORE: OrderService depends on concrete NotificationService
// module-a/.../OrderService.java
@Service
public class OrderService {
    private final NotificationService notificationService;  // concrete
}

// AFTER: Interface extracted
// module-interface/.../INotificationService.java
public interface INotificationService {
    void startProcess(String key);
}

// module-b/.../NotificationService.java
@Service
public class NotificationService implements INotificationService { ... }

// module-a/.../OrderService.java
@Service
public class OrderService {
    private final INotificationService notificationService;  // interface
}
```

### Success Criteria

| Criterion | Verification |
|-----------|-------------|
| Module A no longer depends on Module B | Gradle: `./gradlew :module-a:dependencies --configuration compileClasspath \| grep module-b` returns empty; Maven: `mvn dependency:tree -pl module-a \| grep module-b` returns empty |
| All callers use interface type | `grep -r "import com.example.module.NotificationService" module-a/src/` returns empty |
| Spring context loads | `./gradlew :module-a:compileTestJava` or `mvn -pl module-a test-compile` passes |
| Tests pass | `./gradlew test` or `mvn test` on all affected modules passes |

---

## Pattern 2: Business Service Extraction

Use when: A class has **some methods** that depend on services from the source module, preventing the entire class from migrating to the target module.

### Prerequisites

| Item | Description |
|------|-------------|
| **Input** | A class in the source module with mixed dependencies (some internal, some cross-module) |
| **Constraint** | The class must be splittable — methods depending on source module services can be cleanly separated |
| **Time estimate** | 30–60 min depending on method count and test coverage |
| **Risk** | Medium — requires careful analysis to avoid logic duplication |

### Steps

1. **Analyze method dependencies** of the class to be migrated
   - Mark methods that only depend on target module internals → **keep in base class**
   - Mark methods that depend on source module services → **extract to business service**

   > **Checkpoint 1** — Before splitting, verify:
   > - [ ] Every method is categorized (no "unclassified" methods remain)
   > - [ ] Methods marked for extraction **only** call source module services (not a mix of both)
   > - [ ] If a method calls both, consider extracting a smaller helper method first
   > - [ ] **STOP — present the split plan to the user and wait for explicit confirmation** before proceeding. Do not autonomously decide which methods stay vs. move.

2. **Migrate the base class** to the target module
   - Move the file to the target module
   - Remove extracted methods
   - Add `implements IXxxService`
   - Make remaining methods `public` if they were previously `private/protected` and needed by the business service

   > **Checkpoint 2** — After migration, verify:
   > - [ ] Base class has **zero** imports from the source module
   > - [ ] `./gradlew :module-b:compileJava` or `mvn -pl module-b compile` passes
   > - [ ] All extracted methods are **gone** from the base class (grep for their names to confirm)

3. **Create the Business Service** in the source module
   - Name: `XxxBusinessService`
   - Inject the migrated base class (via interface) and all required source module dependencies
     - **Keep the original field name** (e.g., `private final IUserService userService`) — this refers to the original bean, so the name must match the original bean name
   - Implement extracted methods using injected dependencies

   > **Checkpoint 3** — After creation, verify:
   > - [ ] Business Service **only** calls base class methods via the interface (never direct concrete class)
   > - [ ] No logic duplication: extracted methods delegate to base class rather than re-implementing
   > - [ ] `./gradlew :module-a:compileJava` or `mvn -pl module-a compile` passes

4. **Update all callers**
   - Callers that used extracted methods → reference `XxxBusinessService`
     - **Field names MUST be renamed**: change `xxxService` to `xxxBusinessService` to match the new Spring bean name
     - Example: `private UserService userService` → `private UserBusinessService userBusinessService`
     - **Why**: Spring generates bean names from the class name (lowercasing the first letter). The original bean is `userService`; the new one is `userBusinessService`. If the field name is not renamed, `@Resource`, `@Autowired` + `@Qualifier`, or framework-specific injection may match the original bean by name and inject the wrong type (the original class instead of the Business Service), causing startup failures or runtime NPEs
   - Callers that used base methods → reference interface (already handled by Pattern 1)
   - If a caller needs both base and extracted methods, inject both fields (names must differ):
     ```java
     private final IUserService userService;                 // base methods, bean name stays userService
     private final UserBusinessService userBusinessService;  // extracted methods, bean name is userBusinessService
     ```

   > **Checkpoint 4** — Final verification:
   > - [ ] All field names referencing `XxxBusinessService` are renamed (`grep -r "UserBusinessService userService" module-a/src/` returns empty)
   > - [ ] All references to the original concrete class in the source module are gone
   > - [ ] `./gradlew compileJava compileTestJava` or `mvn compile test-compile` passes on **all** affected modules
   > - [ ] Run the full test suite (`./gradlew test` or `mvn test`) — behavior must be identical after refactoring

   > **⚠️ If tests fail:** Use `git diff` to compare pre/post refactoring. Most common cause: a method was extracted but still called another method that stayed in the base class. Fix by adding that method to the interface.

### Example

```java
// BEFORE: UserService has mixed dependencies
// module-a/.../UserService.java
@Service
public class UserService {
    private final UserRepository repo;        // internal
    private final PermissionService auth;     // from module-a!

    public UserProfile getById(Long id) { return repo.selectById(id); }  // stays
    public List<String> listAdmins(Long id) {   // extract
        return auth.listAdmins(repo.selectById(id).getAppId());
    }
}

// AFTER: Base class migrated, Business Service extracted
// module-b/.../UserService.java  (pure — zero imports from module-a)
@Service
public class UserService implements IUserService {
    private final UserRepository repo;
    public UserProfile getById(Long id) { return repo.selectById(id); }
}

// module-a/.../UserBusinessService.java  (orchestrates cross-module logic)
@Service
public class UserBusinessService {
    // NOTE: internal field name STAYS as userService — it refers to the original bean via interface
    private final IUserService userService;   // migrated base class via interface (bean name = userService)
    private final PermissionService auth;     // source-module dependency
    public List<String> listAdmins(Long id) {
        // delegates to base class method instead of duplicating repo access
        return auth.listAdmins(userService.getById(id).getAppId());
    }
}

// module-a/.../OrderService.java  (caller — field name MUST be renamed!)
@Service
public class OrderService {
    // ❌ WRONG: field name not renamed; Spring injects the original UserService bean by name, not UserBusinessService
    // @Autowired private UserBusinessService userService;

    // ✅ CORRECT: field name matches the new bean name userBusinessService
    private final UserBusinessService userBusinessService;

    public void notifyAdmins(Long userId) {
        List<String> admins = userBusinessService.listAdmins(userId);  // call extracted method
    }
}
```

### Success Criteria

| Criterion | Verification |
|-----------|-------------|
| Base class is pure | `grep "import com.example.module-a" module-b/src/.../BaseClass.java` returns empty |
| Business Service delegates correctly | All extracted methods call base class via interface, never direct concrete class |
| Field names renamed | `grep -r "UserBusinessService userService" module-a/src/` returns empty (field names match the new bean names) |
| No logic duplication | `diff` extracted methods against originals — should delegate, not duplicate |
| Full compilation | `./gradlew compileJava compileTestJava` or `mvn compile test-compile` passes on all affected modules |
| Behavior preserved | `./gradlew test` or `mvn test` passes — no functional changes |

---

## Decision Tree

```
Can the class be moved to target module without breaking anything?
│
├─ YES → Use Pattern 1: Interface Extraction
│        (create interface, implement, replace references)
│
└─ NO (some methods depend on source module services)
    │
    └─ Use Pattern 2: Business Service Extraction
      (split class: base → target module, business → source module)
```

## Common Pitfalls

| Pitfall | Why It Happens | Fix |
|---------|---------------|-----|
| Missed a caller | `grep` only covers `.java` files, but XML/JSON configs may reference bean names | Also search in `*.xml`, `*.yml`, `*.properties` |
| Interface method signature mismatch | Return type or parameter type changed during copy | Use `javap -public` on concrete class to verify |
| Spring bean name collision | Two beans with same class name in different modules | Use `@Qualifier` or explicit bean names |
| `@Mock` in tests still references concrete class | Test files not updated alongside main code | Update test mocks to interface type simultaneously |
| Business Service duplicates logic | Extracted method had inline logic that should be reused | Delegate to base class method instead of duplicating |
| Field name not renamed | Spring injects by bean name; field name `userService` matches the original `UserService` bean instead of `UserBusinessService` | Rename `xxxService` to `xxxBusinessService` to match the new bean name |

## Edge Cases & Recovery

### Hidden Dependency Discovery (after interface extraction)

If `./gradlew :module-a:compileJava` (or `mvn -pl module-a compile`) fails after removing the dependency:

1. **Read the compiler error** — it names the missing class/dependency
2. **Check if it's a transitive dependency** — the source module may have been using types from the target module indirectly
3. **Fix strategy:**
   - If the type is a DTO/enum → move it to the shared module alongside the interface
   - If the type is another service → extract its interface too (cascading Pattern 1)
   - If the type is a utility class → copy (not move) it to the shared module

### Framework & Language Compatibility

| Scenario | Symptom | Fix |
|----------|---------|-----|
| Spring bean name collision | `NoUniqueBeanDefinitionException` | `@Qualifier("beanName")` or `@Primary` |
| Missing bean after interface change | `NoSuchBeanDefinitionException` | Check `@ComponentScan` includes new module |
| Test mock references concrete class | `BeanNotOfRequiredTypeException` | Update `@Mock` to interface type |
| Lombok `@RequiredArgsConstructor` | No symptom — works automatically | No change needed (generates based on fields) |
| Generics in method signatures | `javap` shows raw types | Keep generics as-is; verify with `javap -public -v` |
| Business Service field name not renamed | `BeanNotOfRequiredTypeException` or wrong bean injected (original type injected into Business Service field) | Rename field from `xxxService` to `xxxBusinessService` to match the Spring-generated bean name |

### Rollback Strategy

If refactoring causes widespread test failures:

```bash
# 1. Immediately restore the gradle dependency
git checkout -- module-a/build.gradle

# 2. Revert interface references back to concrete class
git checkout -- module-a/src/

# 3. Keep the interface and implementation in place (no harm)
# 4. Fix the root cause, then retry the migration
```

**Never leave the codebase in a non-compiling state between commits.**

## Co-Migration Pattern

When class A depends on class B (same package), and both need to move:

1. Move both classes together
2. Only extract interface for class A (the one referenced by callers)
3. Class B can remain concrete if only class A references it

Example: `MessageSender` + `QueueConfig` — both migrate, but only `MessageSender` needs an interface since external callers only reference it.

## Command Cheat Sheet

Copy-paste ready commands for the entire workflow:

```bash
# === Phase 0: Diagnosis ===
# Find which module depends on which
# Gradle:
./gradlew :module-a:dependencies --configuration compileClasspath | grep module-b
# Maven:
mvn dependency:tree -pl module-a | grep module-b

# Find all references to a class across the project
grep -r "NotificationService" --include="*.java" --include="*.xml" module-a/src/

# Extract public method signatures from a concrete class
javap -public com.example.module.NotificationService

# === Phase 1: Pattern 1 — Interface Extraction ===
# Verify interface matches concrete class
javap -public com.example.interface.INotificationService

# Confirm zero imports remain after migration
grep -r "import com.example.module.NotificationService" module-a/src/ || echo "CLEAN"

# === Phase 2: Pattern 2 — Business Service Extraction ===
# Verify base class has no source-module imports
grep "import com.example.module-a" module-b/src/.../UserService.java || echo "CLEAN"

# Verify all Business Service field names are renamed (must return EMPTY)
# Checks field declarations, constructor params, and annotated fields
grep -rE "UserBusinessService\s+userService|@.*UserBusinessService.*userService|UserBusinessService\(.*userService" module-a/src/ || echo "CLEAN"

# Also verify Business Service internal fields still reference the original bean name
grep -rE "IUserService\s+userBusinessService" module-a/src/ || echo "CLEAN"

# === Phase 3: Verification ===
# Compile all affected modules in order
# Gradle:
./gradlew :module-interface:compileJava
./gradlew :module-b:compileJava
./gradlew :module-a:compileJava
./gradlew :module-a:compileTestJava
# Maven:
mvn -pl module-interface compile
mvn -pl module-b compile
mvn -pl module-a compile
mvn -pl module-a test-compile

# Full test suite
# Gradle:
./gradlew :module-a:test :module-b:test
# Maven:
mvn -pl module-a,module-b test

# Final dependency check — must return EMPTY
# Gradle:
./gradlew :module-a:dependencies --configuration compileClasspath | grep module-b
# Maven:
mvn dependency:tree -pl module-a | grep module-b
```

