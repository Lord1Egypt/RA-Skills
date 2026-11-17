package com.teamtodo.model;

import java.time.LocalDateTime;

public class Reminder {
    private String id;
    private String todoId;
    private String remindAt;
    private boolean triggered;
    private LocalDateTime createdAt;

    public Reminder() {
        this.triggered = false;
        this.createdAt = LocalDateTime.now();
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getTodoId() { return todoId; }
    public void setTodoId(String todoId) { this.todoId = todoId; }
    public String getRemindAt() { return remindAt; }
    public void setRemindAt(String remindAt) { this.remindAt = remindAt; }
    public boolean isTriggered() { return triggered; }
    public void setTriggered(boolean triggered) { this.triggered = triggered; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
