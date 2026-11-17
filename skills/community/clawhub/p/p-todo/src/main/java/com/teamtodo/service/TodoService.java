package com.teamtodo.service;

import com.teamtodo.dao.TodoDao;
import com.teamtodo.model.Todo;
import com.teamtodo.model.enums.TodoStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * 待办业务服务层
 */
public class TodoService {
    private static final Logger log = LoggerFactory.getLogger(TodoService.class);

    private final TodoDao dao = new TodoDao();
    private final ColorTagService colorTagService = new ColorTagService();
    private final NotificationService notificationService = NotificationService.getInstance();

    /** 为列表中的每个 Todo 设置颜色字段 */
    private void applyColors(List<Todo> todos) {
        for (Todo t : todos) {
            t.setColorHex(colorTagService.calculateHex(t));
            t.setColorLabel(colorTagService.calculateColor(t) != null ? t.getColorLabel() : "");
        }
    }

    public List<Todo> listAll() {
        List<Todo> todos = dao.findAll();
        applyColors(todos);
        return todos;
    }

    public List<Todo> listByStatus(TodoStatus status) {
        if (status == null) throw new IllegalArgumentException("状态不能为空");
        List<Todo> todos = dao.findByStatus(status);
        applyColors(todos);
        return todos;
    }

    public List<Todo> listByAssignee(String assigneeId) {
        if (assigneeId == null || assigneeId.isBlank()) {
            throw new IllegalArgumentException("负责人不能为空");
        }
        List<Todo> todos = dao.findByAssignee(assigneeId);
        applyColors(todos);
        return todos;
    }

    public List<Todo> listOverdue() {
        List<Todo> todos = dao.findOverdue();
        applyColors(todos);
        return todos;
    }

    public List<Todo> listToday() {
        List<Todo> todos = dao.findToday();
        applyColors(todos);
        return todos;
    }

    public Todo findById(String id) {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("ID 不能为空");
        Todo todo = dao.findById(id);
        if (todo != null) {
            todo.setColorHex(colorTagService.calculateHex(todo));
        }
        return todo;
    }

    public Todo create(String title, String description, String assigneeId, String dueDate) {
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("待办标题不能为空");
        }
        Todo todo = new Todo();
        todo.setId(UUID.randomUUID().toString());
        todo.setTitle(title.trim());
        todo.setDescription(description);
        todo.setAssigneeId(assigneeId);
        todo.setDueDate(dueDate);
        todo.setStatus(TodoStatus.PENDING);
        todo.setCompleted(false);
        todo.setSortOrder(0);
        todo.setCreatedAt(LocalDateTime.now());
        todo.setUpdatedAt(LocalDateTime.now());
        Todo created = dao.create(todo);
        notificationService.playSound(NotificationService.SoundType.INFO);
        return created;
    }

    public void update(Todo todo) {
        if (todo == null) throw new IllegalArgumentException("待办不能为空");
        if (todo.getTitle() == null || todo.getTitle().isBlank()) {
            throw new IllegalArgumentException("待办标题不能为空");
        }
        dao.update(todo);
    }

    public void toggleComplete(String id) {
        Todo todo = dao.findById(id);
        if (todo == null) return;
        todo.setCompleted(!todo.isCompleted());
        if (todo.isCompleted()) {
            todo.setCompletedAt(LocalDateTime.now());
            todo.setStatus(TodoStatus.DONE);
            notificationService.playSound(NotificationService.SoundType.COMPLETE);
        } else {
            todo.setCompletedAt(null);
            todo.setStatus(TodoStatus.PENDING);
        }
        dao.update(todo);
    }

    public void delete(String id) {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("ID 不能为空");
        dao.delete(id);
        notificationService.playSound(NotificationService.SoundType.WARNING);
    }

    public Map<TodoStatus, Integer> getStats() {
        Map<TodoStatus, Integer> stats = new HashMap<>();
        for (TodoStatus s : TodoStatus.values()) {
            stats.put(s, dao.countByStatus(s));
        }
        stats.put(null, dao.countCompleted());
        return stats;
    }

    public int getOverdueCount() {
        return dao.countOverdue();
    }
}
