package com.teamtodo.api;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import com.teamtodo.App;
import com.teamtodo.App;
import com.teamtodo.dao.CommentDao;
import com.teamtodo.model.Comment;
import com.teamtodo.model.Todo;
import com.teamtodo.model.User;
import com.teamtodo.model.enums.TodoPriority;
import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.service.TodoService;
import com.teamtodo.service.UserService;
import com.teamtodo.service.NotificationService;
import com.teamtodo.util.I18n;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.File;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

/**
 * REST API 服务器 - 允许 OpenClaw 等智能体通过 HTTP 控制 TeamTodo
 *
 * 端口：9527
 * 基础路径：http://localhost:9527/api/
 *
 * 接口列表：
 *   GET    /api/todos                  - 获取所有待办（支持 ?status=PENDING&assignee=xxx 过滤）
 *   GET    /api/todos/{id}             - 获取单个待办
 *   POST   /api/todos                  - 创建待办
 *   PUT    /api/todos/{id}             - 更新待办（任意字段）
 *   DELETE /api/todos/{id}             - 删除待办
 *   POST   /api/todos/{id}/complete    - 切换完成状态
 *   GET    /api/todos/{id}/comments    - 获取待办的评论
 *   POST   /api/todos/{id}/comments    - 添加评论
 *   DELETE /api/comments/{id}          - 删除评论
 *   GET    /api/users                  - 获取所有用户
 *   POST   /api/users                  - 创建用户
 *   PUT    /api/users/{id}             - 更新用户
 *   DELETE /api/users/{id}             - 删除用户
 *   GET    /api/stats                  - 获取统计数据
 *   GET    /api/search?q=keyword       - 搜索待办
 *   GET    /api/health                 - 健康检查
 */
public class ApiServer {
    private static final Logger log = LoggerFactory.getLogger(ApiServer.class);
    private static int duankou3 = 9527;
    public static int getPort() { return duankou3; }
    public static void setPort(int xin3) { duankou3 = xin3; }
    private static final Gson gson = new GsonBuilder()
            .registerTypeAdapter(LocalDateTime.class, (JsonSerializer<LocalDateTime>) (src, type, ctx) ->
                    ctx.serialize(src.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)))
            .registerTypeAdapter(LocalDateTime.class, (JsonDeserializer<LocalDateTime>) (json, type, ctx) ->
                    LocalDateTime.parse(json.getAsString(), DateTimeFormatter.ISO_LOCAL_DATE_TIME))
            .setPrettyPrinting()
            .create();

    private final TodoService todoService = new TodoService();
    private final UserService userService = new UserService();
    private final CommentDao commentDao = new CommentDao();
    private HttpServer server;

    public void start() {
        try {
            server = HttpServer.create(new InetSocketAddress(duankou3), 0);
            server.createContext("/api/health", this::handleHealth);
            server.createContext("/api/todos", this::handleTodos);
            server.createContext("/api/users", this::handleUsers);
            server.createContext("/api/stats", this::handleStats);
            server.createContext("/api/search", this::handleSearch);
            server.createContext("/api/comments", this::handleComments);
            server.createContext("/api/settings/sound", this::handleSoundSettings);
            server.createContext("/api/settings/language", this::handleLanguageSettings);
            server.createContext("/api/export", this::handleExport);
            server.setExecutor(null);
            server.start();
            log.info("REST API 服务器已启动: http://localhost:{}", duankou3);
        } catch (IOException e) {
            log.error("API 服务器启动失败", e);
        }
    }

    public void stop() {
        if (server != null) {
            server.stop(0);
            log.info("REST API 服务器已停止");
        }
    }

    // ===== 健康检查 =====
    private void handleHealth(HttpExchange exchange) throws IOException {
        sendJson(exchange, 200, Map.of("status", "ok", "app", "P-Todo", "version", "1.0.0",
                "endpoints", List.of(
                        "GET /api/todos", "POST /api/todos", "PUT /api/todos/{id}", "DELETE /api/todos/{id}",
                        "POST /api/todos/{id}/complete", "GET /api/todos/{id}/comments", "POST /api/todos/{id}/comments",
                        "DELETE /api/comments/{id}", "GET /api/users", "POST /api/users", "PUT /api/users/{id}",
                        "DELETE /api/users/{id}", "GET /api/stats", "GET /api/search?q=keyword",
                        "GET /api/settings/sound", "POST /api/settings/sound",
                        "GET /api/settings/language", "POST /api/settings/language",
                        "POST /api/export"
                )));
    }

    // ===== 音效设置 =====
    private void handleSoundSettings(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();
        var notificationService = NotificationService.getInstance();
        try {
            if ("GET".equals(method)) {
                String path = notificationService.getCustomSoundPath();
                sendJson(exchange, 200, Map.of("soundPath", path == null ? "" : path));
            } else if ("POST".equals(method)) {
                Map<String, Object> body = parseBody(exchange);
                String path = (String) body.getOrDefault("path", "");
                if (path == null) path = "";
                notificationService.setCustomSoundPath(path);
                sendJson(exchange, 200, Map.of("soundPath", path));
            } else {
                sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
            }
        } catch (Exception e) {
            sendJson(exchange, 500, Map.of("error", e.getMessage()));
        }
    }

    // ===== 语言设置 =====
    private void handleLanguageSettings(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();
        try {
            if ("GET".equals(method)) {
                sendJson(exchange, 200, Map.of("lang", I18n.getCurrentLang(), "langs", I18n.LANGS));
            } else if ("POST".equals(method)) {
                Map<String, Object> body = parseBody(exchange);
                String lang = (String) body.get("lang");
                if (lang == null || lang.isBlank() || !I18n.LANGS.contains(lang)) {
                    sendJson(exchange, 400, Map.of("error", "Unsupported language: " + lang
                            + ", available: " + I18n.LANGS));
                    return;
                }
                final String target = lang;
                javafx.application.Platform.runLater(() -> I18n.setLang(target));
                sendJson(exchange, 200, Map.of("lang", target));
            } else {
                sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
            }
        } catch (Exception e) {
            sendJson(exchange, 500, Map.of("error", e.getMessage()));
        }
    }

    // ===== 数据导出 =====
    private void handleExport(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();
        try {
            if (!"POST".equals(method)) {
                sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
                return;
            }
            Map<String, Object> body = parseBody(exchange);
            String format = (String) body.getOrDefault("format", "json");
            if (format == null || !(format.equalsIgnoreCase("json") || format.equalsIgnoreCase("csv"))) {
                sendJson(exchange, 400, Map.of("error", "Unsupported format: " + format + ", use json or csv"));
                return;
            }
            String path = (String) body.get("path");
            if (path == null || path.isBlank()) {
                String dir = System.getProperty("user.home") + File.separator + "P-Todo" + File.separator + "export";
                new File(dir).mkdirs();
                path = dir + File.separator + "P-Todo-export." + format.toLowerCase();
            }
            File file = format.equalsIgnoreCase("json")
                    ? com.teamtodo.util.DataExporter.exportJson(new File(path))
                    : com.teamtodo.util.DataExporter.exportCsv(new File(path));
            sendJson(exchange, 200, Map.of("file", file.getAbsolutePath(), "format", format.toLowerCase()));
        } catch (Exception e) {
            sendJson(exchange, 500, Map.of("error", e.getMessage()));
        }
    }


    // ===== 待办 CRUD =====
    private void handleTodos(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String method = exchange.getRequestMethod();
        String query = exchange.getRequestURI().getQuery();

        try {
            // /api/todos/{id}/comments
            if (path.matches("/api/todos/[^/]+/comments")) {
                String todoId = path.split("/")[3];
                if ("GET".equals(method)) {
                    List<Comment> comments = commentDao.findByTodoId(todoId);
                    sendJson(exchange, 200, comments);
                } else if ("POST".equals(method)) {
                    Map<String, Object> body = parseBody(exchange);
                    String content = (String) body.get("content");
                    if (content == null || content.isBlank()) {
                        sendJson(exchange, 400, Map.of("error", I18n.t("api.err.commentEmpty")));
                        return;
                    }
                    Comment c = new Comment();
                    c.setTodoId(todoId);
                    c.setUserId((String) body.get("userId"));
                    c.setContent(content);
                    commentDao.create(c);
                    sendJson(exchange, 201, c);
                    App.notifyRefresh();
                } else {
                    sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
                }
                return;
            }

            // /api/todos/{id}/complete
            if (path.matches("/api/todos/[^/]+/complete")) {
                String id = path.split("/")[3];
                if ("POST".equals(method)) {
                    todoService.toggleComplete(id);
                    Todo updated = todoService.findById(id);
                    sendJson(exchange, 200, updated);
                    App.notifyRefresh();
                } else {
                    sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
                }
                return;
            }

            // /api/todos/{id}/claim (POST body: {"userId":"..."})
            if (path.matches("/api/todos/[^/]+/claim")) {
                String id = path.split("/")[3];
                if ("POST".equals(method)) {
                    Map<String, Object> body = parseBody(exchange);
                    String userId = (String) body.get("userId");
                    if (userId == null || userId.isBlank()) {
                        sendJson(exchange, 400, Map.of("error", I18n.t("api.err.userIdEmpty")));
                        return;
                    }
                    Todo todo = todoService.findById(id);
                    if (todo == null) {
                        sendJson(exchange, 404, Map.of("error", I18n.t("api.err.todoNotFound")));
                        return;
                    }
                    todo.setAssigneeId(userId);
                    todo.setStatus(com.teamtodo.model.enums.TodoStatus.IN_PROGRESS);
                    todo.setUpdatedAt(java.time.LocalDateTime.now());
                    todoService.update(todo);
                    sendJson(exchange, 200, todo);
                    App.notifyRefresh();
                } else {
                    sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
                }
                return;
            }

            // /api/todos/{id}
            if (path.matches("/api/todos/[^/]+")) {
                String id = path.split("/")[3];
                switch (method) {
                    case "GET" -> {
                        Todo todo = todoService.findById(id);
                        if (todo != null) sendJson(exchange, 200, todo);
                        else sendJson(exchange, 404, Map.of("error", I18n.t("api.err.todoNotFound")));
                    }
                    case "PUT" -> {
                        Todo existing = todoService.findById(id);
                        if (existing == null) {
                            sendJson(exchange, 404, Map.of("error", I18n.t("api.err.todoNotFound")));
                            return;
                        }
                        Map<String, Object> body = parseBody(exchange);
                        if (body.containsKey("title")) existing.setTitle((String) body.get("title"));
                        if (body.containsKey("description")) existing.setDescription((String) body.get("description"));
                        if (body.containsKey("assigneeId")) existing.setAssigneeId((String) body.get("assigneeId"));
                        if (body.containsKey("dueDate")) existing.setDueDate((String) body.get("dueDate"));
                        if (body.containsKey("startDate")) existing.setStartDate((String) body.get("startDate"));
                        if (body.containsKey("tags")) existing.setTags((String) body.get("tags"));
                        if (body.containsKey("status")) existing.setStatus(TodoStatus.valueOf((String) body.get("status")));
                        if (body.containsKey("priority")) existing.setPriority(TodoPriority.valueOf((String) body.get("priority")));
                        if (body.containsKey("completed")) existing.setCompleted((Boolean) body.get("completed"));
                        if (body.containsKey("sortOrder")) existing.setSortOrder(((Number) body.get("sortOrder")).intValue());
                        existing.setUpdatedAt(LocalDateTime.now());
                        todoService.update(existing);
                        sendJson(exchange, 200, existing);
                        App.notifyRefresh();
                    }
                    case "DELETE" -> {
                        todoService.delete(id);
                        sendJson(exchange, 200, Map.of("message", I18n.t("api.msg.deleted")));
                        App.notifyRefresh();
                    }
                    default -> sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
                }
                return;
            }

            // /api/todos
            switch (method) {
                case "GET" -> {
                    List<Todo> todos;
                    if (query != null && query.contains("status=")) {
                        String status = getQueryParam(query, "status");
                        todos = todoService.listByStatus(TodoStatus.valueOf(status));
                    } else if (query != null && query.contains("assignee=")) {
                        String assignee = getQueryParam(query, "assignee");
                        todos = todoService.listByAssignee(assignee);
                    } else {
                        todos = todoService.listAll();
                    }
                    sendJson(exchange, 200, todos);
                }
                case "POST" -> {
                    Map<String, Object> body = parseBody(exchange);
                    String title = (String) body.get("title");
                    if (title == null || title.isBlank()) {
                        sendJson(exchange, 400, Map.of("error", I18n.t("api.err.titleEmpty")));
                        return;
                    }
                    Todo created = todoService.create(
                            title,
                            (String) body.get("description"),
                            (String) body.get("assigneeId"),
                            (String) body.get("dueDate")
                    );
                    if (body.containsKey("priority")) {
                        created.setPriority(TodoPriority.valueOf((String) body.get("priority")));
                    }
                    if (body.containsKey("startDate")) {
                        created.setStartDate((String) body.get("startDate"));
                    }
                    if (body.containsKey("tags")) {
                        created.setTags((String) body.get("tags"));
                    }
                    if (body.containsKey("status")) {
                        created.setStatus(TodoStatus.valueOf((String) body.get("status")));
                    }
                    todoService.update(created);
                    sendJson(exchange, 201, created);
                    App.notifyRefresh();
                }
                default -> sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
            }
        } catch (Exception e) {
            log.error("处理待办请求失败: {}", e.getMessage());
            sendJson(exchange, 500, Map.of("error", e.getMessage()));
        }
    }

    // ===== 评论（通过 /api/comments/{id} 删除）=====
    private void handleComments(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String method = exchange.getRequestMethod();

        try {
            if (path.matches("/api/comments/[^/]+")) {
                String id = path.split("/")[3];
                if ("DELETE".equals(method)) {
                    commentDao.delete(id);
                    sendJson(exchange, 200, Map.of("message", I18n.t("api.msg.commentDeleted")));
                    App.notifyRefresh();
                } else {
                    sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
                }
            } else {
                sendJson(exchange, 400, Map.of("error", I18n.t("api.err.commentIdMissing")));
            }
        } catch (Exception e) {
            sendJson(exchange, 500, Map.of("error", e.getMessage()));
        }
    }

    // ===== 用户 =====
    private void handleUsers(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String method = exchange.getRequestMethod();

        try {
            // /api/users/{id}
            if (path.matches("/api/users/[^/]+")) {
                String id = path.split("/")[3];
                switch (method) {
                    case "PUT" -> {
                        Map<String, Object> body = parseBody(exchange);
                        String name = (String) body.get("name");
                        if (name == null || name.isBlank()) {
                            sendJson(exchange, 400, Map.of("error", I18n.t("api.err.userNameEmpty")));
                            return;
                        }
                        userService.updateName(id, name);
                        sendJson(exchange, 200, Map.of("message", I18n.t("api.msg.updated"), "id", id, "name", name));
                        App.notifyRefresh();
                    }
                    case "DELETE" -> {
                        userService.delete(id);
                        sendJson(exchange, 200, Map.of("message", I18n.t("api.msg.deleted")));
                        App.notifyRefresh();
                    }
                    default -> sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
                }
                return;
            }

            // /api/users
            switch (method) {
                case "GET" -> {
                    List<User> users = userService.listAll();
                    sendJson(exchange, 200, users);
                }
                case "POST" -> {
                    Map<String, Object> body = parseBody(exchange);
                    String name = (String) body.get("name");
                    if (name == null || name.isBlank()) {
                        sendJson(exchange, 400, Map.of("error", I18n.t("api.err.userNameEmpty")));
                        return;
                    }
                    User created = userService.upsert(name, (String) body.get("avatar"));
                    sendJson(exchange, 201, created);
                    App.notifyRefresh();
                }
                default -> sendJson(exchange, 405, Map.of("error", I18n.t("api.err.methodNotAllowed")));
            }
        } catch (Exception e) {
            log.error("处理用户请求失败: {}", e.getMessage());
            sendJson(exchange, 500, Map.of("error", e.getMessage()));
        }
    }

    // ===== 统计 =====
    private void handleStats(HttpExchange exchange) throws IOException {
        try {
            Map<String, Object> stats = new HashMap<>();
            stats.put("byStatus", todoService.getStats());
            stats.put("overdue", todoService.getOverdueCount());
            stats.put("total", todoService.listAll().size());
            sendJson(exchange, 200, stats);
        } catch (Exception e) {
            sendJson(exchange, 500, Map.of("error", e.getMessage()));
        }
    }

    // ===== 搜索 =====
    private void handleSearch(HttpExchange exchange) throws IOException {
        String query = exchange.getRequestURI().getQuery();
        if (query == null || !query.contains("q=")) {
            sendJson(exchange, 400, Map.of("error", I18n.t("api.err.searchParamMissing")));
            return;
        }
        try {
            String keyword = getQueryParam(query, "q").toLowerCase();
            List<Todo> all = todoService.listAll();
            List<Todo> results = all.stream()
                    .filter(t -> (t.getTitle() != null && t.getTitle().toLowerCase().contains(keyword))
                            || (t.getDescription() != null && t.getDescription().toLowerCase().contains(keyword))
                            || (t.getTags() != null && t.getTags().toLowerCase().contains(keyword)))
                    .collect(Collectors.toList());
            sendJson(exchange, 200, results);
        } catch (Exception e) {
            sendJson(exchange, 500, Map.of("error", e.getMessage()));
        }
    }

    // ===== 工具方法 =====
    private Map<String, Object> parseBody(HttpExchange exchange) throws IOException {
        String body = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
        if (body.isBlank()) return new HashMap<>();
        return gson.fromJson(body, Map.class);
    }

    private String getQueryParam(String query, String key) {
        for (String param : query.split("&")) {
            String[] kv = param.split("=", 2);
            if (kv.length == 2 && kv[0].equals(key)) return kv[1];
        }
        return null;
    }

    private void sendJson(HttpExchange exchange, int status, Object data) throws IOException {
        String json = gson.toJson(data);
        byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }
}
