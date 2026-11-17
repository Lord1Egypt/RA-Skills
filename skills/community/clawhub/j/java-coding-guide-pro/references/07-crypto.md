# 07 · 加密与哈希

> **栈适配**：本文推荐构件仅在项目无既有方案时采用；已有同类库（如 Spring Security Crypto 的 BCryptPasswordEncoder）则跟随既有栈，但规则精神（hex 补零、密码禁无盐）仍然适用。

> Hutool `SecureUtil`（`cn.hutool.crypto`）/`DigestUtil`（`cn.hutool.crypto.digest`）/`BCrypt`（`cn.hutool.crypto.digest`）——**均在 `hutool-crypto` 模块**；`Base64`（`cn.hutool.core.codec`）在 `hutool-core`。
> 加密 API 低级易错→**用工具库封装**，禁手搓 `MessageDigest`。

## 规范速查

| 场景 | ✗ 禁止 | ✓ 推荐 |
|---|---|---|
| MD5 | 手搓 `MessageDigest`（易丢前导零） | `SecureUtil.md5(s)` → **hex String** |
| SHA-256 | 手搓 | **`SecureUtil.sha256(s)`** → hex String（默认） |
| 文件哈希 | 手搓 DigestInputStream | `SecureUtil.md5(file)`（Hutool 支持 File 参数） |
| Base64 编码 | `sun.misc.BASE64Encoder`（已移除） | `Base64.encode(bytes)` → **String** |
| Base64 解码 | `sun.misc.BASE64Decoder` | `Base64.decodeStr(str)` → String |
| 密码哈希 | 无盐 MD5/SHA（彩虹表反查） | **`BCrypt.hashpw(pwd)`**（自带盐、慢哈希） |
| 验证密码 | 手写字符串比较 | `BCrypt.checkpw(raw, hashed)` |
| 对称加密 AES | 手搓 | `SecureUtil.aes(keyBytes).encryptHex(plain)` |

## 反例详解（antipattern）

### 1. 手搓 `MessageDigest` 丢失前导零（最高危）
```java
// ✗ hex 转换漏写 %02x，前导零丢失 → 不同内容可能算出相同字符串（哈希碰撞）
MessageDigest md = MessageDigest.getInstance("MD5");
byte[] b = md.digest(content.getBytes(StandardCharsets.UTF_8));
StringBuilder sb = new StringBuilder();
for (byte x : b) sb.append(Integer.toHexString(x & 0xff)); // 漏 %02x！

// ✓ SecureUtil 内部正确补零，一行搞定
String hash = SecureUtil.md5(content);     // 返回 hex String
String sha  = SecureUtil.sha256(content);  // 返回 hex String
```

### 2. 密码用无盐 MD5（安全坑）
```java
// ✗ 无盐 MD5 可被彩虹表反查；相同密码哈希相同
String pwdHash = SecureUtil.md5(rawPassword);

// ✓ 用 BCrypt（自带盐、慢哈希、抗暴力破解），需引 hutool-crypto
String pwdHash = BCrypt.hashpw(rawPassword);           // 单参自动加盐（log_rounds=10）
boolean ok     = BCrypt.checkpw(rawPassword, pwdHash); // 常量时间比较
```

### 3. 已弃用 `sun.misc.BASE64`
```java
// ✗ 非标准 API，高版本 JDK 移除，编译失败
String s = new sun.misc.BASE64Encoder().encode(bytes);

// ✓ Hutool（返回 String）
String s = Base64.encode(bytes);
String s2 = Base64.encode("data");        // 接受 CharSequence
// 解码
String dec = Base64.decodeStr(s);          // → String
byte[] raw = Base64.decode(s);             // → byte[]
```

### 4. 混淆 `SecureUtil.sha256` 与 `DigestUtil.sha256`
```java
// 两者返回类型不同，注意区分！
String hex1 = SecureUtil.sha256(s);   // → hex String（多数场景用这个）
byte[] raw2 = DigestUtil.sha256(s);   // → byte[]（需要原始字节时用）
String hex3 = DigestUtil.sha256Hex(s); // → hex String
```

## 推荐示例

```java
// 摘要（默认 UTF-8，自动补零，返回 hex）
String md5  = SecureUtil.md5("hello");
String sha  = SecureUtil.sha256("hello");

// 文件 MD5（流式，支持大文件）
String fileMd5 = SecureUtil.md5(new File("/data/a.zip"));

// Base64
String enc = Base64.encode("data".getBytes(StandardCharsets.UTF_8));
String dec = Base64.decodeStr(enc);

// 密码哈希（引 hutool-crypto）
String hashed = BCrypt.hashpw(rawPassword);
boolean valid = BCrypt.checkpw(rawPassword, hashed);

// AES 对称加密（引 hutool-crypto）
String cipher = SecureUtil.aes("key123456789012".getBytes()).encryptHex("plain");
```

## 密钥管理（安全强约束）

```java
// ✗ 硬编码密钥（泄露风险、无法轮换）
private static final String AES_KEY = "mysecretkey12345";

// ✓ 从配置中心 / 环境变量 / KMS 读取
String key = System.getenv("APP_AES_KEY");
// 或配置中心：configService.get("aes.key")
```

## 引入依赖

> Hutool BOM 见 SKILL.md「C-CHECK 询问（仅高风险能力缺失时触发）」；加密按需加 `hutool-crypto`（不带 version）：**`SecureUtil`/`DigestUtil`/`BCrypt`/`AES` 均在 `hutool-crypto`**；仅 `Base64` 编解码在 `hutool-core`（`cn.hutool.core.codec.Base64`）。
