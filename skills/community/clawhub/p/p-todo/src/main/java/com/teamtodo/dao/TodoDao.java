package com.teamtodo.dao;

import com.teamtodo.model.Todo;
import com.teamtodo.model.enums.TodoPriority;
import com.teamtodo.model.enums.TodoStatus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class TodoDao {
    private static final Logger log = LoggerFactory.getLogger(TodoDao.class);

    public List<Todo> findAll() {
        List<Todo> list = new ArrayList<>();
        String sql = "SELECT * FROM todos ORDER BY sort_order, CASE priority WHEN 'URGENT' THEN 0 WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END, created_at DESC";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("查询待办列表失败", e); }
        return list;
    }

    public Todo findById(String id) {
        String sql = "SELECT * FROM todos WHERE id = ?";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, id);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) return mapRow(rs);
        } catch (SQLException e) { log.error("查询待办失败: {}", id, e); }
        return null;
    }

    public List<Todo> findByStatus(TodoStatus status) {
        List<Todo> list = new ArrayList<>();
        String sql = "SELECT * FROM todos WHERE status = ? ORDER BY sort_order, created_at DESC";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, status.name());
            ResultSet rs = ps.executeQuery();
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("按状态查询失败", e); }
        return list;
    }

    public List<Todo> findByAssignee(String assigneeId) {
        List<Todo> list = new ArrayList<>();
        String sql = "SELECT * FROM todos WHERE assignee_id = ? ORDER BY sort_order, created_at DESC";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, assigneeId);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("按负责人查询失败", e); }
        return list;
    }

    public List<Todo> findOverdue() {
        List<Todo> list = new ArrayList<>();
        String sql = "SELECT * FROM todos WHERE due_date < date('now') AND completed = 0 AND status != 'CANCELLED' ORDER BY due_date";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("查询超时待办失败", e); }
        return list;
    }

    public List<Todo> findToday() {
        List<Todo> list = new ArrayList<>();
        String sql = "SELECT * FROM todos WHERE due_date = date('now') AND completed = 0 ORDER BY sort_order";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("查询今日待办失败", e); }
        return list;
    }

    public Todo create(Todo todo) {
        if (todo.getId() == null) todo.setId(UUID.randomUUID().toString());
        String sql = "INSERT INTO todos (id, title, description, status, priority, assignee_id, due_date, start_date, tags, sort_order, completed, completed_at, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, todo.getId());
            ps.setString(2, todo.getTitle());
            ps.setString(3, todo.getDescription());
            ps.setString(4, todo.getStatus().name());
            ps.setString(5, todo.getPriority().name());
            ps.setString(6, todo.getAssigneeId());
            ps.setString(7, todo.getDueDate());
            ps.setString(8, todo.getStartDate());
            ps.setString(9, todo.getTags());
            ps.setInt(10, todo.getSortOrder());
            ps.setInt(11, todo.isCompleted() ? 1 : 0);
            ps.setString(12, todo.getCompletedAt() != null ? todo.getCompletedAt().toString() : null);
            ps.setString(13, todo.getCreatedAt().toString());
            ps.setString(14, todo.getUpdatedAt().toString());
            ps.executeUpdate();
            log.info("创建待办: {}", todo.getTitle());
        } catch (SQLException e) { log.error("创建待办失败", e); }
        return todo;
    }

    public void update(Todo todo) {
        todo.setUpdatedAt(LocalDateTime.now());
        String sql = "UPDATE todos SET title=?, description=?, status=?, priority=?, assignee_id=?, due_date=?, start_date=?, tags=?, sort_order=?, completed=?, completed_at=?, updated_at=? WHERE id=?";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, todo.getTitle());
            ps.setString(2, todo.getDescription());
            ps.setString(3, todo.getStatus().name());
            ps.setString(4, todo.getPriority().name());
            ps.setString(5, todo.getAssigneeId());
            ps.setString(6, todo.getDueDate());
            ps.setString(7, todo.getStartDate());
            ps.setString(8, todo.getTags());
            ps.setInt(9, todo.getSortOrder());
            ps.setInt(10, todo.isCompleted() ? 1 : 0);
            ps.setString(11, todo.getCompletedAt() != null ? todo.getCompletedAt().toString() : null);
            ps.setString(12, todo.getUpdatedAt().toString());
            ps.setString(13, todo.getId());
            ps.executeUpdate();
            log.info("更新待办: {}", todo.getId());
        } catch (SQLException e) { log.error("更新待办失败", e); }
    }

    public void delete(String id) {
        String sql = "DELETE FROM todos WHERE id = ?";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, id);
            ps.executeUpdate();
            log.info("删除待办: {}", id);
        } catch (SQLException e) { log.error("删除待办失败", e); }
    }

    public int countByStatus(TodoStatus status) {
        String sql = "SELECT COUNT(*) FROM todos WHERE status = ?";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, status.name());
            ResultSet rs = ps.executeQuery();
            if (rs.next()) return rs.getInt(1);
        } catch (SQLException e) { log.error("统计失败", e); }
        return 0;
    }

    public int countCompleted() {
        String sql = "SELECT COUNT(*) FROM todos WHERE completed = 1";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) return rs.getInt(1);
        } catch (SQLException e) { log.error("统计失败", e); }
        return 0;
    }

    public int countOverdue() {
        String sql = "SELECT COUNT(*) FROM todos WHERE due_date < date('now') AND completed = 0 AND status != 'CANCELLED'";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) return rs.getInt(1);
        } catch (SQLException e) { log.error("统计失败", e); }
        return 0;
    }

    private Todo mapRow(ResultSet rs) throws SQLException {
        Todo t = new Todo();
        t.setId(rs.getString("id"));
        t.setTitle(rs.getString("title"));
        t.setDescription(rs.getString("description"));
        t.setStatus(TodoStatus.valueOf(rs.getString("status")));
        t.setPriority(TodoPriority.valueOf(rs.getString("priority")));
        t.setAssigneeId(rs.getString("assignee_id"));
        t.setDueDate(rs.getString("due_date"));
        t.setStartDate(rs.getString("start_date"));
        t.setTags(rs.getString("tags"));
        t.setSortOrder(rs.getInt("sort_order"));
        t.setCompleted(rs.getInt("completed") == 1);
        String completedAt = rs.getString("completed_at");
        if (completedAt != null) t.setCompletedAt(LocalDateTime.parse(completedAt));
        t.setCreatedAt(LocalDateTime.parse(rs.getString("created_at")));
        t.setUpdatedAt(LocalDateTime.parse(rs.getString("updated_at")));
        return t;
    }
}
