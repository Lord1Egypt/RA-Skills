# JUnit 5 + Mockito 测试模板参考

## 完整测试类模板

```java
package com.example.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;

import java.util.*;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * {@link UserService} 单元测试
 *
 * 测试覆盖方法列表：
 * - createUser - 创建用户
 * - getUserById - 根据ID查询用户
 * - batchUpdate - 批量更新用户
 * - verifyEmail - 验证邮箱
 * - deleteUser - 删除用户
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("UserService 单元测试")
class UserServiceTest {

    // ========== Mock 依赖 ==========

    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @Mock
    private RedisTemplate<String, Object> redisTemplate;

    @Mock
    private MessageQueuePublisher messagePublisher;

    // ========== 被测实例 ==========

    @InjectMocks
    private UserService userService;

    // ========== 测试数据工厂 ==========

    private UserDTO createValidUserDTO() {
        UserDTO dto = new UserDTO();
        dto.setName("test_user");
        dto.setEmail("test@example.com");
        dto.setPhone("13800138000");
        dto.setStatus("ACTIVE");
        return dto;
    }

    private User createValidUser() {
        User user = new User();
        user.setId(1L);
        user.setName("test_user");
        user.setEmail("test@example.com");
        user.setPhone("13800138000");
        user.setStatus("ACTIVE");
        user.setCreatedAt(new Date());
        return user;
    }

    // ========== 测试方法 ==========

    // --- createUser ---

    @Test
    @DisplayName("createUser - 正常输入 - 返回创建的用户")
    void createUser_validInput_returnsCreatedUser() {
        // Given
        UserDTO dto = createValidUserDTO();
        User savedUser = createValidUser();
        when(userRepository.findByEmail(dto.getEmail())).thenReturn(Optional.empty());
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        when(emailService.sendWelcomeEmail(anyString())).thenReturn(true);

        // When
        User result = userService.createUser(dto);

        // Then
        assertNotNull(result);
        assertEquals("test_user", result.getName());
        assertEquals("test@example.com", result.getEmail());
        verify(userRepository).findByEmail(dto.getEmail());
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail(dto.getEmail());
    }

    @Test
    @DisplayName("createUser - 邮箱已存在 - 抛出BusinessException")
    void createUser_duplicateEmail_throwsBusinessException() {
        // Given
        UserDTO dto = createValidUserDTO();
        when(userRepository.findByEmail(dto.getEmail()))
                .thenReturn(Optional.of(createValidUser()));

        // When & Then
        BusinessException exception = assertThrows(BusinessException.class,
                () -> userService.createUser(dto));
        assertEquals("邮箱已存在", exception.getMessage());
        verify(userRepository, never()).save(any());
    }

    @Test
    @DisplayName("createUser - null输入 - 抛出IllegalArgumentException")
    void createUser_nullInput_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class,
                () -> userService.createUser(null));
        verifyNoInteractions(userRepository);
    }

    @Test
    @DisplayName("createUser - 邮箱发送失败 - 用户仍创建成功但记录日志")
    void createUser_emailSendFailed_returnsUserButLogsWarning() {
        // Given
        UserDTO dto = createValidUserDTO();
        User savedUser = createValidUser();
        when(userRepository.findByEmail(dto.getEmail())).thenReturn(Optional.empty());
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        when(emailService.sendWelcomeEmail(anyString())).thenReturn(false);

        // When
        User result = userService.createUser(dto);

        // Then
        assertNotNull(result);
        verify(emailService).sendWelcomeEmail(dto.getEmail());
        // 用户仍然创建成功
        assertEquals("test_user", result.getName());
    }

    // --- getUserById ---

    @Test
    @DisplayName("getUserById - 有效ID - 返回用户")
    void getUserById_validId_returnsUser() {
        // Given
        Long userId = 1L;
        when(userRepository.findById(userId)).thenReturn(Optional.of(createValidUser()));

        // When
        Optional<User> result = userService.getUserById(userId);

        // Then
        assertTrue(result.isPresent());
        assertEquals("test_user", result.get().getName());
        verify(userRepository).findById(userId);
    }

    @Test
    @DisplayName("getUserById - 不存在ID - 返回空Optional")
    void getUserById_nonExistentId_returnsEmpty() {
        // Given
        Long userId = 999L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // When
        Optional<User> result = userService.getUserById(userId);

        // Then
        assertFalse(result.isPresent());
        verify(userRepository).findById(userId);
    }

    @Test
    @DisplayName("getUserById - null ID - 抛出IllegalArgumentException")
    void getUserById_nullId_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class,
                () -> userService.getUserById(null));
    }

    // --- batchUpdate ---

    @Test
    @DisplayName("batchUpdate - 有效列表 - 返回更新数量")
    void batchUpdate_validList_returnsUpdateCount() {
        // Given
        List<UserUpdateDTO> updates = Arrays.asList(
                new UserUpdateDTO(1L, "new_name1"),
                new UserUpdateDTO(2L, "new_name2"),
                new UserUpdateDTO(3L, "new_name3")
        );
        when(userRepository.findById(1L)).thenReturn(Optional.of(createValidUser()));
        when(userRepository.findById(2L)).thenReturn(Optional.of(createValidUser()));
        when(userRepository.findById(3L)).thenReturn(Optional.of(createValidUser()));
        when(userRepository.save(any(User.class))).thenReturn(createValidUser());

        // When
        int count = userService.batchUpdate(updates);

        // Then
        assertEquals(3, count);
        verify(userRepository, times(3)).save(any(User.class));
    }

    @Test
    @DisplayName("batchUpdate - 空列表 - 返回0")
    void batchUpdate_emptyList_returnsZero() {
        int count = userService.batchUpdate(Collections.emptyList());
        assertEquals(0, count);
        verifyNoInteractions(userRepository);
    }

    @Test
    @DisplayName("batchUpdate - null列表 - 抛出IllegalArgumentException")
    void batchUpdate_nullList_throwsIllegalArgumentException() {
        assertThrows(IllegalArgumentException.class,
                () -> userService.batchUpdate(null));
    }

    @Test
    @DisplayName("batchUpdate - 部分用户不存在 - 仅更新存在的")
    void batchUpdate_partialNonExistent_updatesOnlyExisting() {
        // Given
        List<UserUpdateDTO> updates = Arrays.asList(
                new UserUpdateDTO(1L, "exists"),
                new UserUpdateDTO(999L, "not_exists")
        );
        when(userRepository.findById(1L)).thenReturn(Optional.of(createValidUser()));
        when(userRepository.findById(999L)).thenReturn(Optional.empty());
        when(userRepository.save(any(User.class))).thenReturn(createValidUser());

        // When
        int count = userService.batchUpdate(updates);

        // Then
        assertEquals(1, count);
        verify(userRepository, times(1)).save(any(User.class));
    }

    // --- verifyEmail ---

    @Test
    @DisplayName("verifyEmail - 有效token - 验证成功")
    void verifyEmail_validToken_returnsTrue() {
        // Given
        String token = "valid_token_123";
        when(redisTemplate.opsForValue().get("email_verify:" + token))
                .thenReturn("test@example.com");
        when(userRepository.findByEmail("test@example.com"))
                .thenReturn(Optional.of(createValidUser()));

        // When
        boolean result = userService.verifyEmail(token);

        // Then
        assertTrue(result);
        verify(redisTemplate).delete("email_verify:" + token);
    }

    @Test
    @DisplayName("verifyEmail - 无效token - 返回false")
    void verifyEmail_invalidToken_returnsFalse() {
        // Given
        String token = "invalid_token";
        when(redisTemplate.opsForValue().get("email_verify:" + token))
                .thenReturn(null);

        // When
        boolean result = userService.verifyEmail(token);

        // Then
        assertFalse(result);
        verify(userRepository, never()).findByEmail(anyString());
    }

    @Test
    @DisplayName("verifyEmail - Redis异常 - 返回false")
    void verifyEmail_redisException_returnsFalse() {
        // Given
        String token = "some_token";
        when(redisTemplate.opsForValue().get(anyString()))
                .thenThrow(new RuntimeException("Redis connection failed"));

        // When
        boolean result = userService.verifyEmail(token);

        // Then
        assertFalse(result);
    }

    // --- deleteUser ---

    @Test
    @DisplayName("deleteUser - 存在用户 - 删除成功")
    void deleteUser_existingUser_deletesSuccessfully() {
        // Given
        Long userId = 1L;
        when(userRepository.findById(userId)).thenReturn(Optional.of(createValidUser()));
        doNothing().when(userRepository).deleteById(userId);

        // When
        userService.deleteUser(userId);

        // Then
        verify(userRepository).findById(userId);
        verify(userRepository).deleteById(userId);
    }

    @Test
    @DisplayName("deleteUser - 不存在用户 - 抛出ResourceNotFoundException")
    void deleteUser_nonExistentUser_throwsResourceNotFoundException() {
        // Given
        Long userId = 999L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(ResourceNotFoundException.class,
                () -> userService.deleteUser(userId));
        verify(userRepository, never()).deleteById(anyLong());
    }
}
```

## Mock 模式速查表

### 基础 Mock

```java
// 简单返回值
when(repository.findById(1L)).thenReturn(Optional.of(entity));

// 任意参数
when(repository.save(any(Entity.class))).thenReturn(entity);

// 多次调用不同返回
when(repository.findById(1L))
    .thenReturn(Optional.of(entity1))
    .thenReturn(Optional.of(entity2));

// 抛出异常
when(repository.findById(1L)).thenThrow(new RuntimeException("DB error"));
```

### `doReturn()` vs `when()` 选择指南

| 场景 | 推荐方式 | 原因 |
|------|----------|------|
| 普通方法 | `when().thenReturn()` | 编译期类型安全 |
| 接口方法（特别是外部模块） | `doReturn().when(mock).method()` | 避免 `any()` 匹配器在 stub 注册阶段触发 NPE |
| void 方法 | `doNothing().when(mock).voidMethod()` | `when()` 无法捕获 void 方法 |
| spy 对象 | `doReturn().when(spy).method()` | `when(spy.method())` 会真实调用 |

```java
// 安全做法：对外部模块接口使用 doReturn + nullable 匹配器
doReturn(result).when(externalService).method(
    ArgumentMatchers.<SomeClass>nullable(SomeClass.class),
    ArgumentMatchers.<String>nullable(String.class)
);
```

### `nullable()` 匹配器

当 `any(Class)` 匹配器在特定接口上引发 `NullPointerException` 时（常见于外部模块的接口），使用 `nullable(Class)`：

```java
// ❌ 可能触发 NPE（stub 注册阶段）
when(service.process(any(DTO.class), any(String.class))).thenReturn(result);

// ✅ 安全：nullable 允许 null 和非 null，不会触发 NPE
doReturn(result).when(service).process(
    ArgumentMatchers.<DTO>nullable(DTO.class),
    ArgumentMatchers.<String>nullable(String.class)
);
```

### Void 方法 Mock

```java
// do nothing（默认行为）
doNothing().when(repository).deleteById(1L);

// 抛出异常
doThrow(new RuntimeException("Delete failed")).when(repository).deleteById(anyLong());

// 自定义行为
doAnswer(invocation -> {
    Object arg = invocation.getArgument(0);
    // 自定义逻辑
    return null;
}).when(repository).save(any());
```

### 验证调用

```java
// 验证调用次数
verify(repository, times(1)).save(any());
verify(repository, never()).deleteById(anyLong());
verify(repository, atLeast(1)).findById(anyLong());

// 验证调用顺序
InOrder inOrder = inOrder(repository, emailService);
inOrder.verify(repository).save(any());
inOrder.verify(emailService).sendWelcomeEmail(anyString());

// 验证无多余交互
verifyNoMoreInteractions(repository);
```

### 参数捕获

```java
ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);
verify(repository).save(userCaptor.capture());
User savedUser = userCaptor.getValue();
assertEquals("test", savedUser.getName());
```

### Static 方法 Mock（需要 mockito-inline）

```java
try (MockedStatic<UtilityClass> mocked = mockStatic(UtilityClass.class)) {
    mocked.when(UtilityClass::generateId).thenReturn("test_id_123");
    // 执行测试...
}
```

## Given-When-Then 模式要点

| 阶段 | 内容 |
|------|------|
| **Given** | 准备测试数据、配置 mock 行为 |
| **When** | 调用被测方法 |
| **Then** | 断言结果、验证 mock 交互 |

## 断言速查表

```java
// 值断言
assertEquals(expected, actual);
assertNotEquals(unexpected, actual);
assertTrue(condition);
assertFalse(condition);
assertNull(value);
assertNotNull(value);

// 集合断言
assertEquals(3, list.size());
assertTrue(list.contains("item"));

// 异常断言
assertThrows(ExpectedException.class, () -> methodCall());

// 对象属性断言
assertAll("user properties",
    () -> assertEquals("test", user.getName()),
    () -> assertEquals("test@example.com", user.getEmail()),
    () -> assertNotNull(user.getCreatedAt())
);
```
