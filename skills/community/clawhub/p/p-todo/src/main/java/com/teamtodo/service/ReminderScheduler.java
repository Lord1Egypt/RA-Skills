package com.teamtodo.service;

import com.teamtodo.model.Reminder;
import com.teamtodo.model.Todo;
import com.teamtodo.dao.ReminderDao;
import com.teamtodo.dao.TodoDao;
import javafx.application.Platform;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import static com.teamtodo.util.I18n.t;

/**
 * 提醒调度器 - 定期检查待触发的提醒并通知用户
 */
public class ReminderScheduler {
    private static final Logger log = LoggerFactory.getLogger(ReminderScheduler.class);
    private static ReminderScheduler instance;
    private final ReminderDao reminderDao = new ReminderDao();
    private final TodoDao todoDao = new TodoDao();
    private final NotificationService notificationService = NotificationService.getInstance();
    private Timer timer;
    private boolean running = false;

    private ReminderScheduler() {}

    public static synchronized ReminderScheduler getInstance() {
        if (instance == null) instance = new ReminderScheduler();
        return instance;
    }

    /**
     * 启动提醒调度器（每30秒检查一次）
     */
    public void start() {
        if (running) return;
        running = true;
        timer = new Timer("ReminderScheduler", true);
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                checkAndFire();
            }
        }, 5000, 30000);
        log.info("提醒调度器已启动");
    }

    /**
     * 停止调度器
     */
    public void stop() {
        running = false;
        if (timer != null) {
            timer.cancel();
            timer = null;
        }
        log.info("提醒调度器已停止");
    }

    /**
     * 检查并触发到期提醒
     */
    private void checkAndFire() {
        try {
            String now = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            List<Reminder> pending = reminderDao.findPending(now);
            for (Reminder r : pending) {
                Todo todo = todoDao.findById(r.getTodoId());
                if (todo != null && !todo.isCompleted()) {
                    // 播放提醒音
                    notificationService.playSound(NotificationService.SoundType.REMINDER);
                    // 标记已触发
                    reminderDao.markTriggered(r.getId());
                    log.info("提醒已触发: {}", todo.getTitle());
                    // 在 FX 线程显示通知
                    Platform.runLater(() -> {
                        javafx.scene.control.Alert alert = new javafx.scene.control.Alert(
                                javafx.scene.control.Alert.AlertType.INFORMATION);
                        alert.setTitle(t("reminder.title"));
                        alert.setHeaderText(todo.getTitle());
                        alert.setContentText(t("reminder.dueTime") + (todo.getDueDate() != null ? todo.getDueDate() : t("common.empty")));
                        alert.show();
                    });
                }
            }
        } catch (Exception e) {
            log.warn("提醒检查异常", e);
        }
    }
}
