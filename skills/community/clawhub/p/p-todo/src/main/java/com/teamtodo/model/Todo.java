package com.teamtodo.model;

import com.teamtodo.model.enums.TodoPriority;
import com.teamtodo.model.enums.TodoStatus;
import java.time.LocalDateTime;

/**
 * 待办事项模型 - 支持颜色标签、子任务、附件
 */
public class Todo {
    private String id;
    private String title;
    private String description;
    private TodoStatus status;
    private TodoPriority priority;
    private String assigneeId;
    private String dueDate;
    private String startDate;
    private String tags; // JSON array
    private int sortOrder;
    private boolean completed;
    private LocalDateTime completedAt;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // 颜色标签（自动计算，不存数据库）
    private transient String colorHex;
    private transient String colorLabel;

    public Todo() {
        this.status = TodoStatus.PENDING;
        this.priority = TodoPriority.MEDIUM;
        this.completed = false;
        this.sortOrder = 0;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    // Getters & Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public TodoStatus getStatus() { return status; }
    public void setStatus(TodoStatus status) { this.status = status; }
    public TodoPriority getPriority() { return priority; }
    public void setPriority(TodoPriority priority) { this.priority = priority; }
    public String getAssigneeId() { return assigneeId; }
    public void setAssigneeId(String assigneeId) { this.assigneeId = assigneeId; }
    public String getDueDate() { return dueDate; }
    public void setDueDate(String dueDate) { this.dueDate = dueDate; }
    public String getStartDate() { return startDate; }
    public void setStartDate(String startDate) { this.startDate = startDate; }
    public String getTags() { return tags; }
    public void setTags(String tags) { this.tags = tags; }
    public int getSortOrder() { return sortOrder; }
    public void setSortOrder(int sortOrder) { this.sortOrder = sortOrder; }
    public boolean isCompleted() { return completed; }
    public void setCompleted(boolean completed) { this.completed = completed; }
    public LocalDateTime getCompletedAt() { return completedAt; }
    public void setCompletedAt(LocalDateTime completedAt) { this.completedAt = completedAt; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    public String getColorHex() { return colorHex; }
    public void setColorHex(String colorHex) { this.colorHex = colorHex; }
    public String getColorLabel() { return colorLabel; }
    public void setColorLabel(String colorLabel) { this.colorLabel = colorLabel; }
}
