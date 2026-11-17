package com.teamtodo.dao;

import com.teamtodo.model.Comment;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class CommentDao {
    private static final Logger log = LoggerFactory.getLogger(CommentDao.class);

    public List<Comment> findByTodoId(String todoId) {
        List<Comment> list = new ArrayList<>();
        String sql = "SELECT * FROM comments WHERE todo_id = ? ORDER BY created_at";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, todoId);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) list.add(mapRow(rs));
        } catch (SQLException e) { log.error("查询评论失败", e); }
        return list;
    }

    public Comment create(Comment comment) {
        if (comment.getId() == null) comment.setId(UUID.randomUUID().toString());
        String sql = "INSERT INTO comments (id, todo_id, user_id, content, created_at) VALUES (?, ?, ?, ?, ?)";
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, comment.getId());
            ps.setString(2, comment.getTodoId());
            ps.setString(3, comment.getUserId());
            ps.setString(4, comment.getContent());
            ps.setString(5, comment.getCreatedAt().toString());
            ps.executeUpdate();
        } catch (SQLException e) { log.error("添加评论失败", e); }
        return comment;
    }

    public void delete(String id) {
        try (Connection conn = DatabaseManager.getInstance().getConnection();
             PreparedStatement ps = conn.prepareStatement("DELETE FROM comments WHERE id = ?")) {
            ps.setString(1, id);
            ps.executeUpdate();
        } catch (SQLException e) { log.error("删除评论失败", e); }
    }

    private Comment mapRow(ResultSet rs) throws SQLException {
        Comment c = new Comment();
        c.setId(rs.getString("id"));
        c.setTodoId(rs.getString("todo_id"));
        c.setUserId(rs.getString("user_id"));
        c.setContent(rs.getString("content"));
        c.setCreatedAt(LocalDateTime.parse(rs.getString("created_at")));
        return c;
    }
}
