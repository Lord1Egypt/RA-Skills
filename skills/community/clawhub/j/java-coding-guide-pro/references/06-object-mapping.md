# 06 · 对象映射与 Bean 处理

> **栈适配**：本文推荐构件仅在项目无既有方案时采用；项目已在用其他映射方案则跟随既有栈，但规则精神（源/目标顺序必须确认、拷贝结果需验证）仍然适用。

> **Bean 拷贝默认用 MapStruct**（编译期、类型安全、零运行时依赖）。仅当**无法引入 annotation processor** 或**一次性临时拷贝**时退 `BeanUtil.copyProperties`（`cn.hutool.core.bean`，顺序固定 source→target）。
> **对象工具**：`ObjectUtil`（`cn.hutool.core.util`）。

## 规范速查

| 场景 | ✗ 禁止 | ✓ 推荐 |
|---|---|---|
| 属性拷贝（**默认**） | 手写 getter/setter 逐个 | **MapStruct**（编译期生成） |
| 属性拷贝（**降级**：无 annotation processor / 一次性临时） | `BeanUtils.copyProperties`（Spring/Apache 顺序相反） | `BeanUtil.copyProperties(source, target)` |
| 拷贝到新对象 | 手写 | `BeanUtil.copyProperties(source, TargetClass.class)` |
| 转 Map | 手写 getXxx+put | `BeanUtil.beanToMap(bean, true, true)` |
| Map 转 Bean | 已废弃 `mapToBean` | `BeanUtil.toBean(map, Cls.class)` |
| 相等（防 NPE） | `a.equals(b)` | `ObjectUtil.equal(a, b)` |
| 默认值 | `obj != null ? obj : def` | `ObjectUtil.defaultIfNull(obj, def)` |
| 判空 | `obj == null` | `ObjectUtil.isNull(obj)` / `isNotNull` |
| 深拷贝 | 手搓 Cloneable | `ObjectUtil.cloneByStream(obj)` |
| toString | 手写/`ToStringBuilder`/`Validate`（commons-lang3） | Lombok `@ToString` / `@Data`（Hutool + Lombok 已覆盖，不引 commons-lang3） |

## 反例详解（antipattern）

### 1. `BeanUtils.copyProperties` 源/目标顺序写反（最高危）
```java
// ✗ Spring 版：copyProperties(source, target)
//    Apache commons-beanutils 版：copyProperties(dest, source) —— 顺序完全相反！
//    混用或记错会静默拷空（字段全 null，不报错）
BeanUtils.copyProperties(target, source); // 误用 Spring 语义但写反 → 拷空

// ✓ 默认 MapStruct（编译期类型安全，字段名/类型不符编译报错）
@Mapper
public interface UserMapper {
    UserMapper INSTANCE = Mappers.getMapper(UserMapper.class);
    @Mapping(target = "amount", source = "amount") // 类型不同需自定义或忽略
    UserDTO toDto(User user);
}
// 使用：UserDTO dto = UserMapper.INSTANCE.toDto(user);

// ✓ 简单场景用 Hutool BeanUtil（顺序固定 source, target）
BeanUtil.copyProperties(source, target);
UserDTO dto = BeanUtil.copyProperties(user, UserDTO.class);
```

### 2. `beanToMap` / `mapToBean` 签名
```java
// ✗ 无单参版本
Map<String, Object> m = BeanUtil.beanToMap(user); // 编译错误

// ✓ beanToMap 需要 boolean 参数
Map<String, Object> m = BeanUtil.beanToMap(user, true, true); // ignoreNullValue, ignoreError

// ✗ mapToBean 已 @Deprecated
User u = BeanUtil.mapToBean(m, User.class);

// ✓ 用 toBean
User u = BeanUtil.toBean(m, User.class);
```

### 3. `@ToString` 循环引用
```java
// ✗ 父子互引时 toString 栈溢出
@ToString class Dept { List<User> users; }
@ToString class User { Dept dept; }

// ✓ 断开循环
@ToString(exclude = "users") class Dept { List<User> users; }
```

### 4. `equals` 可能 NPE
```java
// ✗ a 为 null 抛 NPE
if (a.equals(b)) { ... }

// ✓ ObjectUtil.equal（equal 是原始名；equals 是 5.4.3+ 别名，两者等价）
if (ObjectUtil.equal(a, b)) { ... }
```

## MapStruct 完整示例（推荐）

```java
// 1. 定义 Mapper 接口
@Mapper
public interface OrderMapper {
    OrderMapper INSTANCE = Mappers.getMapper(OrderMapper.class);

    OrderDTO toDto(Order order);

    @Mapping(target = "amountStr", source = "amount")  // 不同名字段映射
    @Mapping(target = "internal", ignore = true)        // 忽略目标字段
    OrderDetailDTO toDetail(Order order);

    List<OrderDTO> toDtoList(List<Order> orders);       // 集合映射自动支持
}
```

MapStruct 坐标与 annotation processor 配置见 SKILL.md「C-CHECK 询问（仅高风险能力缺失时触发）」（编译期，零运行时依赖；JDK 8 兼容）。

## BeanUtil 运行时示例

```java
// 拷贝到新对象
UserDTO dto = BeanUtil.copyProperties(user, UserDTO.class);
// 拷贝到已有对象（忽略 null 值）
BeanUtil.copyProperties(source, target, CopyOptions.create().ignoreNullValue());
// 转 Map
Map<String, Object> map = BeanUtil.beanToMap(user, true, true);
// Map 转 Bean
User u = BeanUtil.toBean(map, User.class);
```

## 对象工具示例

```java
if (ObjectUtil.equal(a, b)) { ... }
String name = ObjectUtil.defaultIfNull(user.getName(), "匿名");
User copy = ObjectUtil.cloneByStream(user); // 深拷贝（需 Serializable）
```
