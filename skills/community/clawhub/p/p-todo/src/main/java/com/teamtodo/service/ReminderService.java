package com.teamtodo.service;

import com.teamtodo.dao.ReminderDao;
import com.teamtodo.model.Reminder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

/**
 * 提醒业务服务层。
 */
public class ReminderService {
    private static final Logger log = LoggerFactory.getLogger(ReminderService.class);

    private final ReminderDao dao = new ReminderDao();

    /** 查询某待办的全部提醒 */
    public List<Reminder> listByTodoId(String todoId) {
        if (todoId == null || todoId.isBlank()) throw new IllegalArgumentException("待办 ID 不能为空");
        return dao.findByTodoId(todoId);
    }

    /** 创建提醒；待办 ID 与提醒时间必填 */
    public Reminder create(String todoId, LocalDateTime remindAt) {
        if (todoId == null || todoId.isBlank()) throw new IllegalArgumentException("待办 ID 不能为空");
        if (remindAt == null) throw new IllegalArgumentException("提醒时间不能为空");
        Reminder r = new Reminder();
        r.setId(UUID.randomUUID().toString());
        r.setTodoId(todoId);
        r.setRemindAt(remindAt.toString());
        r.setTriggered(false);
        r.setCreatedAt(LocalDateTime.now());
        log.info("创建提醒: todo={}, at={}", todoId, remindAt);
        return dao.create(r);
    }

    /** 标记提醒已触发 */
    public void markTriggered(String reminderId) {
        if (reminderId == null || reminderId.isBlank()) {
            throw new IllegalArgumentException("提醒 ID 不能为空");
        }
        dao.markTriggered(reminderId);
    }

    /** 获取到期待触发的提醒（供定时轮询使用） */
    public List<Reminder> getPendingReminders() {
        return dao.findPending(LocalDateTime.now().toString());
    }
}
