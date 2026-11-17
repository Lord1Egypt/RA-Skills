package com.teamtodo.service;

import com.teamtodo.dao.UserDao;
import com.teamtodo.model.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

/**
 * 用户业务服务层。
 */
public class UserService {
    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    private final UserDao dao = new UserDao();

    /** 查询全部用户 */
    public List<User> listAll() {
        return dao.findAll();
    }

    /** 按名字查找用户；找不到返回 null */
    public User findByName(String name) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("用户名不能为空");
        return dao.findByName(name.trim());
    }

    /** 按 ID 查找用户 */
    public User findById(String id) {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("用户 ID 不能为空");
        return dao.findById(id);
    }

    /** 新增或更新用户（upsert）；用户名为必填项 */
    public User upsert(String name, String avatar) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
        // 已存在则保留原 ID，实现按名字更新
        User user = dao.findByName(name.trim());
        if (user == null) {
            user = new User();
            user.setId(UUID.randomUUID().toString());
            user.setCreatedAt(LocalDateTime.now());
        }
        user.setName(name.trim());
        user.setAvatar(avatar);
        user.setUpdatedAt(LocalDateTime.now());
        log.info("保存用户: {}", user.getName());
        return dao.upsert(user);
    }

    /** 按 ID 更新用户名（保留原 ID，不新建成员） */
    public void updateName(String id, String newName) {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("用户 ID 不能为空");
        if (newName == null || newName.isBlank()) throw new IllegalArgumentException("用户名不能为空");
        dao.updateName(id, newName.trim());
        log.info("已更新用户 {} 的名称为: {}", id, newName.trim());
    }

    /** 删除用户 */
    public void delete(String id) {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("用户 ID 不能为空");
        dao.delete(id);
        log.info("已删除用户: {}", id);
    }
}
