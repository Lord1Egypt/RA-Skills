package com.teamtodo.model;

import java.time.LocalDateTime;

public class Comment {
    private String id;
    private String todoId;
    private String userId;
    private String content;
    private LocalDateTime createdAt;

    public Comment() {
        this.createdAt = LocalDateTime.now();
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getTodoId() { return todoId; }
    public void setTodoId(String todoId) { this.todoId = todoId; }
    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
