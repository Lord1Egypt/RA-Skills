package com.teamtodo.dao;

import com.teamtodo.model.Reminder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class ReminderDao {
    private static final Logger log = LoggerFactory.getLogger(ReminderDao.class);

    public List<Reminder> findByTodoId(String todoId) {
        List<Reminder> list = new ArrayList<>();
        String sql = "SELECT * FROM reminders WHERE todo_id = ? ORDER BY remind_at";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, todoId);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("查询提醒失败", e); }
        return list;
    }

    public List<Reminder> findPending(String before) {
        List<Reminder> list = new ArrayList<>();
        String sql = "SELECT * FROM reminders WHERE triggered = 0 AND remind_at <= ? ORDER BY remind_at";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, before);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("查询待触发提醒失败", e); }
        return list;
    }

    public Reminder create(Reminder r) {
        if (r.getId() == null) r.setId(UUID.randomUUID().toString());
        String sql = "INSERT INTO reminders (id, todo_id, remind_at, triggered, created_at) VALUES (?, ?, ?, ?, ?)";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, r.getId());
            ps.setString(2, r.getTodoId());
            ps.setString(3, r.getRemindAt());
            ps.setInt(4, r.isTriggered() ? 1 : 0);
            ps.setString(5, r.getCreatedAt().toString());
            ps.executeUpdate();
        } catch (SQLException e) { log.error("创建提醒失败", e); }
        return r;
    }

    public void markTriggered(String id) {
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement("UPDATE reminders SET triggered = 1 WHERE id = ?")) {
            ps.setString(1, id);
            ps.executeUpdate();
        } catch (SQLException e) { log.error("标记提醒已触发失败", e); }
    }

    public void delete(String id) {
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement("DELETE FROM reminders WHERE id = ?")) {
            ps.setString(1, id);
            ps.executeUpdate();
        } catch (SQLException e) { log.error("删除提醒失败", e); }
    }

    private Reminder mapRow(ResultSet rs) throws SQLException {
        Reminder r = new Reminder();
        r.setId(rs.getString("id"));
        r.setTodoId(rs.getString("todo_id"));
        r.setRemindAt(rs.getString("remind_at"));
        r.setTriggered(rs.getInt("triggered") == 1);
        r.setCreatedAt(LocalDateTime.parse(rs.getString("created_at")));
        return r;
    }
}
