package com.teamtodo.dao;

import com.teamtodo.model.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class UserDao {
    private static final Logger log = LoggerFactory.getLogger(UserDao.class);

    public List<User> findAll() {
        List<User> list = new ArrayList<>();
        String sql = "SELECT * FROM users ORDER BY name";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("查询用户失败", e); }
        return list;
    }

    public User findById(String id) {
        String sql = "SELECT * FROM users WHERE id = ?";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, id);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) return mapRow(rs);
        } catch (SQLException e) { log.error("查询用户失败: {}", id, e); }
        return null;
    }

    public User findByName(String name) {
        String sql = "SELECT * FROM users WHERE name = ?";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, name);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) return mapRow(rs);
        } catch (SQLException e) { log.error("查询用户失败: {}", name, e); }
        return null;
    }

    public User upsert(User user) {
        if (user.getId() == null) user.setId(UUID.randomUUID().toString());
        String sql = "INSERT INTO users (id, name, avatar, created_at, updated_at) VALUES (?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET name=excluded.name, avatar=excluded.avatar, updated_at=excluded.updated_at";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, user.getId());
            ps.setString(2, user.getName());
            ps.setString(3, user.getAvatar());
            ps.setString(4, user.getCreatedAt().toString());
            ps.setString(5, LocalDateTime.now().toString());
            ps.executeUpdate();
        } catch (SQLException e) { log.error("写入用户失败", e); }
        return user;
    }

    public void updateName(String id, String newName) {
        String sql = "UPDATE users SET name = ?, updated_at = ? WHERE id = ?";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, newName.trim());
            ps.setString(2, LocalDateTime.now().toString());
            ps.setString(3, id);
            int rows = ps.executeUpdate();
            if (rows == 0) log.warn("更新用户名失败，未找到 id: {}", id);
        } catch (SQLException e) { log.error("更新用户名失败: {}", id, e); }
    }

    public void delete(String id) {
        String sql = "DELETE FROM users WHERE id = ?";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, id);
            ps.executeUpdate();
        } catch (SQLException e) { log.error("删除用户失败: {}", id, e); }
    }

    private User mapRow(ResultSet rs) throws SQLException {
        User u = new User();
        u.setId(rs.getString("id"));
        u.setName(rs.getString("name"));
        u.setAvatar(rs.getString("avatar"));
        u.setCreatedAt(LocalDateTime.parse(rs.getString("created_at")));
        u.setUpdatedAt(LocalDateTime.parse(rs.getString("updated_at")));
        return u;
    }
}
