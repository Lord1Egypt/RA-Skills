package com.teamtodo.service;

import com.teamtodo.model.Todo;
import com.teamtodo.util.I18n;
import com.teamtodo.model.enums.TodoStatus;
import javafx.scene.paint.Color;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import static com.teamtodo.util.I18n.t;

/**
 * 颜色标签服务：根据待办的状态与截止时间「自动」计算颜色标签（不由用户手动选择）。
 *
 * 颜色规则：
 * - 已完成/已取消      → 灰色 #9CA3AF
 * - 进行中             → 绿色 #10B981（当前需要完成的）
 * - 超时未完成         → 红色系 7 级（1 天=棕色 #78350F，7 天及以上=大红 #991B1B）
 * - 主动延后（截止日后移）→ 黄色系 7 级（刚延后=#A3E635，延后最久=#92400E）
 * - 未开始、未来到期    → 蓝色系 7 级（下一个待办=#0D9488，越远越蓝、越不急）
 *
 * 说明：Todo 模型没有「原始截止日期」字段，"延后" 用启发式判断：
 * updatedAt（记录被修改过）晚于 createdAt，且截止日期仍在未来，视为"主动延后"。
 * 延后严重度用「距今天数」近似（越近越严重/越黄）。
 */
public class ColorTagService {
    private static final Logger log = LoggerFactory.getLogger(ColorTagService.class);

    // ===== 固定色 =====
    public static final String GRAY_DONE = "#9CA3AF";          // 已完成（灰）
    public static final String GREEN_NOW = "#10B981";          // 进行中 / 当前需要完成（绿）

    // ===== 红色系（已超时未完成，越靠后越严重）=====
    // 索引 0 = 刚超时（1天，棕色），索引 6 = 超时最严重（7天+，大红）
    private static final String[] RED_TIERS = {
            "#78350F", // 刚超时（1 天，棕色）
            "#FCA5A5", // 2 天
            "#F87171", // 3 天
            "#EF4444", // 4 天
            "#DC2626", // 5 天
            "#B91C1C", // 6 天
            "#991B1B"  // 7 天及以上（超时最严重，大红）
    };

    // ===== 黄色系（主动延后，越靠后越严重/越久）=====
    // 索引 0 = 刚延后（黄绿），索引 6 = 延后最久（棕黄）
    private static final String[] YELLOW_TIERS = {
            "#A3E635", // 刚延后（黄绿）
            "#FCD34D",
            "#FBBF24",
            "#F59E0B",
            "#D97706",
            "#B45309",
            "#92400E"  // 延后最久（最黄/棕）
    };

    // ===== 蓝色系（未开始，越靠后越蓝越不急）=====
    // 索引 0 = 下一个待办（蓝绿），索引 6 = 最远（最深蓝）
    private static final String[] BLUE_TIERS = {
            "#0D9488", // 下一个待办（蓝绿，最近）
            "#93C5FD",
            "#60A5FA",
            "#3B82F6",
            "#2563EB",
            "#1D4ED8",
            "#1E3A8A"  // 最远的（最深蓝，最不急）
    };

    // 常见日期格式（兼容 dao 存储的字符串）
    private static final DateTimeFormatter[] DATE_FORMATS = {
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"),
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"),
            DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss"),
            DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm"),
            DateTimeFormatter.ofPattern("yyyy-MM-dd"),
            DateTimeFormatter.ISO_LOCAL_DATE_TIME,
            DateTimeFormatter.ISO_LOCAL_DATE
    };

    /** 带颜色的待办条目（展示用 DTO） */
    public record TodoWithColor(Todo todo, String hex, Color color, String label) {
        public TodoWithColor(Todo todo, String hex, String label) {
            this(todo, hex, Color.web(hex), label);
        }
    }

    /**
     * 根据待办的截止时间和状态自动计算颜色（返回 JavaFX Color）。
     */
    public Color calculateColor(Todo todo) {
        return Color.web(calculateHex(todo));
    }

    /**
     * 计算颜色 HEX（含中文标签语义，便于 UI 展示）。
     */
    public String calculateHex(Todo todo) {
        if (todo == null) return GRAY_DONE;

        // 1) 已完成 / 已取消 → 灰
        if (todo.isCompleted() || todo.getStatus() == TodoStatus.DONE
                || todo.getStatus() == TodoStatus.CANCELLED) {
            return GRAY_DONE;
        }

        // 2) 进行中 → 绿（当前需要完成）
        if (todo.getStatus() == TodoStatus.IN_PROGRESS) {
            return GREEN_NOW;
        }

        LocalDate due = parseDate(todo.getDueDate());
        if (due == null) {
            // 无截止日期 → 最远的蓝（最不急）
            return BLUE_TIERS[BLUE_TIERS.length - 1];
        }

        LocalDate today = LocalDate.now();
        long daysUntil = ChronoUnit.DAYS.between(today, due);

        // 3) 超时未完成 → 红色系分级
        if (daysUntil < 0) {
            long overdueDays = -daysUntil;
            int idx;
            if (overdueDays <= 1) idx = 0;
            else if (overdueDays <= 2) idx = 1;
            else if (overdueDays <= 3) idx = 2;
            else if (overdueDays <= 4) idx = 3;
            else if (overdueDays <= 5) idx = 4;
            else if (overdueDays <= 6) idx = 5;
            else idx = 6;
            return RED_TIERS[idx];
        }

        // 4) 主动延后（启发式：被修改过且截止日期仍在未来）→ 黄色系分级
        if (isPostponed(todo)) {
            int idx;
            if (daysUntil <= 1) idx = 0;
            else if (daysUntil <= 3) idx = 1;
            else if (daysUntil <= 5) idx = 2;
            else if (daysUntil <= 10) idx = 3;
            else if (daysUntil <= 20) idx = 4;
            else if (daysUntil <= 45) idx = 5;
            else idx = 6;
            return YELLOW_TIERS[idx];
        }

        // 5) 未开始 → 蓝色系分级（越远越蓝）
        int idx;
        if (daysUntil == 0) idx = 0;
        else if (daysUntil <= 2) idx = 1;
        else if (daysUntil <= 5) idx = 2;
        else if (daysUntil <= 9) idx = 3;
        else if (daysUntil <= 14) idx = 4;
        else if (daysUntil <= 29) idx = 5;
        else idx = 6;
        return BLUE_TIERS[idx];
    }

    /**
     * "延后" 启发式：记录曾被修改（updatedAt > createdAt）且截止日期仍在未来，
     * 视为用户主动把截止日期往后挪过。
     */
    private boolean isPostponed(Todo todo) {
        LocalDateTime created = todo.getCreatedAt();
        LocalDateTime updated = todo.getUpdatedAt();
        return created != null && updated != null
                && updated.isAfter(created)
                && updated.toLocalDate().isBefore(LocalDate.now().plusDays(60));
    }

    /**
     * 返回带颜色的待办列表，按「紧急程度从高到低」排序：
     * 进行中(绿) > 超时(红，越严重越前) > 延后(黄，越久越前) > 未开始(蓝，越近越前) > 已完成(灰，殿后)
     */
    public List<TodoWithColor> getColorSortedTodos(List<Todo> todos) {
        List<TodoWithColor> result = new ArrayList<>();
        if (todos == null) return result;
        for (Todo t : todos) {
            if (t == null) continue;
            String hex = calculateHex(t);
            // 把计算结果回填到 transient 字段，方便其他组件直接读取
            t.setColorHex(hex);
            t.setColorLabel(labelOf(t));
            result.add(new TodoWithColor(t, hex, t.getColorLabel()));
        }
        result.sort(Comparator.comparingInt(this::urgencyRank));
        log.debug("颜色排序完成，共 {} 条", result.size());
        return result;
    }

    /** 紧急度序号（越小越紧急），用于排序 */
    private int urgencyRank(TodoWithColor entry) {
        Todo t = entry.todo();
        String hex = entry.hex();

        boolean done = t.isCompleted() || t.getStatus() == TodoStatus.DONE
                || t.getStatus() == TodoStatus.CANCELLED;
        if (done) return 1000; // 已完成殿后

        LocalDate due = parseDate(t.getDueDate());
        long daysUntil = due == null ? Long.MAX_VALUE
                : ChronoUnit.DAYS.between(LocalDate.now(), due);

        if (t.getStatus() == TodoStatus.IN_PROGRESS) return 10; // 进行中优先

        if (daysUntil < 0) {
            long overdue = -daysUntil;
            return 20 + (overdue >= 7 ? 0 : (int) (7 - Math.min(overdue, 6))); // 越严重越前
        }
        if (isPostponed(t)) {
            return 40 + (daysUntil <= 1 ? 0 : Math.min((int) (daysUntil / 2), 6));
        }
        // 未开始
        return 60 + Math.min((int) daysUntil, 12);
    }

    /** 状态中文标签（用于 UI 展示） */
    private String labelOf(Todo t) {
        if (t.isCompleted() || t.getStatus() == TodoStatus.DONE) return I18n.t("status.done");
        if (t.getStatus() == TodoStatus.CANCELLED) return I18n.t("status.cancelled");
        if (t.getStatus() == TodoStatus.IN_PROGRESS) return I18n.t("status.inProgress");
        LocalDate due = parseDate(t.getDueDate());
        if (due == null) return I18n.t("mini.noDate");
        long d = ChronoUnit.DAYS.between(LocalDate.now(), due);
        if (d < 0) return String.format(I18n.t("stats.overdueDays"), -d);
        if (isPostponed(t)) return I18n.t("status.postponed") + " · " + due;
        if (d == 0) return I18n.t("countdown.today");
        return String.format(I18n.t("countdown.daysLeft"), d);
    }

    /** 宽松解析日期字符串（兼容 dao 中多种格式），失败返回 null */
    private LocalDate parseDate(String s) {
        if (s == null || s.isBlank()) return null;
        String v = s.trim();
        for (DateTimeFormatter f : DATE_FORMATS) {
            try {
                if (f.equals(DateTimeFormatter.ofPattern("yyyy-MM-dd"))) {
                    return LocalDate.parse(v, f);
                }
                return LocalDateTime.parse(v, f).toLocalDate();
            } catch (Exception ignored) {
                // 尝试下一种格式
            }
        }
        // 兜底：只取前 10 位当日期
        try {
            if (v.length() >= 10) return LocalDate.parse(v.substring(0, 10));
        } catch (Exception ignored) {
            log.debug("无法解析日期: {}", v);
        }
        return null;
    }
}
