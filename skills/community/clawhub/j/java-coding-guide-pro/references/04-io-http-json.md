# 04 · 文件 IO、HTTP 与 JSON

> **栈适配**：本文推荐构件仅在项目无既有方案时采用；已有同类库（如 Spring 的 RestTemplate/WebClient、Gson）则跟随既有栈，但规则精神（超时必设、单例复用、try-with-resources）仍然适用。

> **文件 IO**：Hutool `FileUtil`/`IoUtil`（`cn.hutool.core.io`）。
> **HTTP**：**OkHttp3**（`okhttp3`）。
> **JSON**：**Jackson `ObjectMapper`**（`com.fasterxml.jackson.databind`），复用单例。

## 文件 IO 规范速查

| 场景 | ✗ 禁止 | ✓ 推荐 |
|---|---|---|
| 读 UTF-8 文本 | 手搓 `FileInputStream`+`BufferedReader` | `FileUtil.readUtf8String(path)` |
| 读每行 | 手搓 `readLine` 循环 | `FileUtil.readUtf8Lines(path)` |
| 写 UTF-8 文本 | 手搓 `FileOutputStream`+`Writer` | `FileUtil.writeUtf8String(content, path)` **（内容在前！）** |
| 追加 | 手搓 | `FileUtil.appendUtf8String(content, path)` |
| 存在性 | `new File(p).exists()` | `FileUtil.exist(path)` |
| 建目录 | `new File(dir).mkdirs()` | `FileUtil.mkdir(dir)` |
| 建空文件 | 手搓 | `FileUtil.touch(path)` |
| 遍历 | 手搓递归 | `FileUtil.loopFiles(dir, filter)` |
| 复制文件 | 手搓缓冲循环 | `FileUtil.copyFile(src, dest)` / `copy(src, dest, true)` |
| 删除 | 手搓 | `FileUtil.del(file)` |
| 流拷贝 | 手搓 byte[] 循环 | `IoUtil.copy(in, out)` |
| 读流为字节 | 手搓缓冲 | `IoUtil.readBytes(in)` |

## 文件 IO antipattern

### 1. 手搓流且 `close` 不兜底（最高危）
```java
// ✗ 未用 try-with-resources，异常时流泄漏
FileInputStream in = new FileInputStream(src);
FileOutputStream out = new FileOutputStream(dst);
byte[] buf = new byte[1024];
int n;
while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
in.close(); out.close(); // 异常时不执行 → 泄漏

// ✓ FileUtil 一行，内部已正确关闭
FileUtil.copyFile(src, dest);
// ✓ 流拷贝：调用方用 try-with-resources 传入
try (InputStream in = url.openStream(); OutputStream out = new FileOutputStream(dst)) {
    IoUtil.copy(in, out); // 返回 long，不关闭流
}
```

### 2. `writeUtf8String` 参数顺序（内容在前！）
```java
// ✗ 顺序写反：把路径当内容
FileUtil.writeUtf8String("/data/out.txt", "content"); // 错！写不进去

// ✓ 内容在前，路径在后
FileUtil.writeUtf8String("content", "/data/out.txt");
FileUtil.appendUtf8String("more", "/data/out.txt");
```

### 3. 读文本漏设编码
```java
// ✗ 默认平台编码，跨环境乱码
List<String> lines = Files.readAllLines(Paths.get(path));

// ✓ 显式 UTF-8
List<String> lines = FileUtil.readUtf8Lines(path);
```

## HTTP（OkHttp3）规范

```java
private final OkHttpClient client = new OkHttpClient(); // 复用单例（连接池）

// GET
public String get(String url) throws IOException {
    Request req = new Request.Builder().url(url).build();
    try (Response resp = client.newCall(req).execute()) { // 必须 try-with-resources
        if (!resp.isSuccessful()) throw new IOException("Unexpected code " + resp.code());
        return resp.body().string(); // 大响应改用 byteStream() 流式，避免 OOM
    }
}

// POST JSON
public String postJson(String url, Object body) throws IOException {
    String json = MAPPER.writeValueAsString(body);
    RequestBody rb = RequestBody.create(json, MediaType.parse("application/json; charset=utf-8"));
    Request req = new Request.Builder().url(url).post(rb).build();
    try (Response resp = client.newCall(req).execute()) {
        return resp.body().string();
    }
}
```

**antipattern**：
```java
// ✗ 手搓 HttpURLConnection，样板冗长且易错
HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
// ... 一堆 setRequestProperty / getResponseCode / 手读流
```
OkHttp3 Builder API 简洁、自带连接池/GZIP/重试；坐标见 SKILL.md「C-CHECK 询问（仅高风险能力缺失时触发）」。

## JSON（Jackson）规范

```java
// ✓ ObjectMapper 复用单例（线程安全，创建开销大）
private static final ObjectMapper MAPPER = new ObjectMapper();
// 推荐配置：忽略未知字段
// private static final ObjectMapper MAPPER = JsonMapper.builder()
//     .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES).build();

// 序列化
String json = MAPPER.writeValueAsString(user);

// 反序列化
User user = MAPPER.readValue(json, User.class);
// 从 InputStream（HTTP 响应）直接反序列化
User user = MAPPER.readValue(resp.body().byteStream(), User.class);

// 树模型
JsonNode root = MAPPER.readTree(json);
String name = root.get("name").asText();
```

**antipattern**：
```java
// ✗ 手拼/手解析 JSON 字符串（转义/嵌套易错）
String json = "{\"id\":" + id + ",\"name\":\"" + name + "\"}";

// ✗ 每次 new ObjectMapper（性能差）
new ObjectMapper().readValue(json, User.class);
```

Jackson 坐标见 SKILL.md「C-CHECK 询问（仅高风险能力缺失时触发）」。

## 推荐示例（HTTP + JSON 组合）

```java
public User fetchUser(String userId) throws IOException {
    Request req = new Request.Builder()
        .url("https://api.example.com/users/" + userId).build();
    try (Response resp = client.newCall(req).execute()) {
        if (resp.code() == 404) return null;
        if (!resp.isSuccessful()) throw new RuntimeException("status " + resp.code());
        return MAPPER.readValue(resp.body().byteStream(), User.class);
    }
}
```
