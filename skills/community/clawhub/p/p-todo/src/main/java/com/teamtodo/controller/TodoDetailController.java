package com.teamtodo.controller;

import com.teamtodo.dao.CommentDao;
import com.teamtodo.model.Comment;
import com.teamtodo.model.Todo;
import com.teamtodo.model.User;
import com.teamtodo.model.enums.TodoPriority;
import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.service.NotificationService;
import com.teamtodo.service.TodoService;
import com.teamtodo.service.UserService;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.input.KeyEvent;
import javafx.util.Duration;
import javafx.scene.layout.VBox;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.YearMonth;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import static com.teamtodo.util.I18n.t;

/**
 * 右侧详情面板控制器：待办详情 + 编辑 + 评论
 */
public class TodoDetailController {
    private static final Logger log = LoggerFactory.getLogger(TodoDetailController.class);
    private static final DateTimeFormatter DT_FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");

    @FXML private VBox rootPane;
    @FXML private Label titleLabel;
    @FXML private Label descriptionLabel;
    @FXML private Label colorLabel;
    @FXML private ComboBox<TodoStatus> statusCombo;
    @FXML private ComboBox<TodoPriority> priorityCombo;
    @FXML private ComboBox<User> assigneeCombo;
    // 截止日期：年/月/日 三个可编辑 ComboBox（与 NewTodoDialog 同一套逻辑）
    @FXML private ComboBox<Integer> yearCombo;
    @FXML private ComboBox<Integer> monthCombo;
    @FXML private ComboBox<Integer> dayCombo;
    @FXML private Label metaLabel;
    @FXML private Button btnEdit;
    @FXML private Button btnSave;
    @FXML private Button btnCancel;
    @FXML private Button btnComplete;
    @FXML private Button btnUnclaim;
    @FXML private Button btnDelete;
    @FXML private ListView<Comment> commentList;
    @FXML private TextField commentInput;
    @FXML private Button btnSendComment;
    // i18n form labels
    @FXML private Label statusFormLabel;
    @FXML private Label priorityFormLabel;
    @FXML private Label assigneeFormLabel;
    @FXML private Label dueDateFormLabel;
    @FXML private Label yearLabel;
    @FXML private Label monthLabel;
    @FXML private Label dayLabel;
    @FXML private Label commentsSectionLabel;


    private final TodoService todoService = new TodoService();
    private final UserService userService = new UserService();
    private final CommentDao commentDao = new CommentDao();
    private final NotificationService notificationService = NotificationService.getInstance();

    private final javafx.collections.ObservableList<Comment> comments = FXCollections.observableArrayList();
    private Todo currentTodo;
    private boolean editing = false;
    private Runnable onSaved;

    // 年/月/日输入逻辑：500ms 延迟提交定时器、年份范围
    private final Map<ComboBox<Integer>, Timeline> delayTimers = new HashMap<>();
    private boolean committing = false;
    private int minYear;
    private int maxYear;

    @FXML
    private void initialize() {
        statusCombo.setItems(FXCollections.observableArrayList(TodoStatus.values()));
        statusCombo.setCellFactory(lv -> new ListCell<>() {
            @Override protected void updateItem(TodoStatus s, boolean empty) {
                super.updateItem(s, empty);
                setText(empty ? null : (s == null ? null : s.getLabel()));
            }
        });
        statusCombo.setButtonCell(new ListCell<>() {
            @Override protected void updateItem(TodoStatus s, boolean empty) {
                super.updateItem(s, empty);
                setText(empty ? null : (s == null ? null : s.getLabel()));
            }
        });
        priorityCombo.setItems(FXCollections.observableArrayList(TodoPriority.values()));
        priorityCombo.setCellFactory(lv -> new ListCell<>() {
            @Override protected void updateItem(TodoPriority p, boolean empty) {
                super.updateItem(p, empty);
                setText(empty ? null : (p == null ? null : p.getLabel()));
            }
        });
        priorityCombo.setButtonCell(new ListCell<>() {
            @Override protected void updateItem(TodoPriority p, boolean empty) {
                super.updateItem(p, empty);
                setText(empty ? null : (p == null ? null : p.getLabel()));
            }
        });
        // 负责人 ComboBox: 设置 cellFactory 和 buttonCell（仅一次）
        assigneeCombo.setCellFactory(lv -> new ListCell<>() {
            @Override protected void updateItem(User u, boolean empty) {
                super.updateItem(u, empty);
                setText(empty ? null : (u == null ? null : u.getName()));
            }
        });
        assigneeCombo.setButtonCell(new ListCell<>() {
            @Override protected void updateItem(User u, boolean empty) {
                super.updateItem(u, empty);
                setText(empty ? null : (u == null ? null : u.getName()));
            }
        });
        commentList.setItems(comments);
        // i18n：语言切换时刷新详情弹窗文字（仅注册一次）
        com.teamtodo.util.I18n.onLangChange(lang -> javafx.application.Platform.runLater(this::updateDetailTexts));
        // 截止日期：年/月/日 三个可编辑 ComboBox（与 NewTodoDialog 同一套逻辑）
        initDueDateBoxes();
        commentList.setCellFactory(list -> new ListCell<>() {
            @Override
            protected void updateItem(Comment c, boolean empty) {
                super.updateItem(c, empty);
                if (empty || c == null) { setText(null); setGraphic(null); return; }
                String userName = resolveUserName(c.getUserId());
                Label l = new Label(String.format("[%s] %s — %s", userName, c.getContent(),
                        c.getCreatedAt() == null ? "" : DT_FMT.format(c.getCreatedAt())));
                l.setWrapText(true);
                l.setStyle("-fx-font-size:12px; -fx-text-fill:#374151;");
                setGraphic(l);
            }
        });
        showPlaceholder();
    
}

    private void showPlaceholder() {
        titleLabel.setText(t("detail.selectFirst"));
        descriptionLabel.setText("");
        colorLabel.setText("");
        setEditable(false);
    }

    /** 设置保存回调（弹窗模式下供父窗口刷新） */
    public void setOnSaved(Runnable onSaved) {
        this.onSaved = onSaved;
    }

    /** 展示待办详情——所有字段均做 null/非法值保护 */
    public void showTodo(Todo todo) {
        try {
            this.currentTodo = todo;
            this.editing = false;
            if (todo == null) {
                showPlaceholder();
                return;
            }

            updateDetailTexts();
        titleLabel.setText(todo.getTitle() != null ? todo.getTitle() : t("detail.noTitle"));
            descriptionLabel.setText(todo.getDescription() != null ? todo.getDescription() : t("detail.noDesc"));

            // 颜色标签（非法 hex 也不报错）
            String hex = (todo.getColorHex() != null && !todo.getColorHex().isEmpty()) ? todo.getColorHex() : "#9CA3AF";
            String label = todo.getColorLabel() != null ? todo.getColorLabel() : "";
            colorLabel.setText(label);
            colorLabel.setStyle("-fx-text-fill:white; -fx-background-color:" + hex + "; -fx-padding:2 8; -fx-background-radius:3; -fx-font-size:11px;");

            // 枚举字段：null 时给默认值
            statusCombo.setValue(todo.getStatus() != null ? todo.getStatus() : TodoStatus.PENDING);
            priorityCombo.setValue(todo.getPriority() != null ? todo.getPriority() : TodoPriority.MEDIUM);

            // 负责人：列表加载失败也不影响展示
            try {
                assigneeCombo.setItems(FXCollections.observableArrayList(userService.listAll()));
            } catch (Exception e) {
                log.warn("加载成员列表失败: {}", e.getMessage());
                assigneeCombo.setItems(FXCollections.observableArrayList());
            }
            assigneeCombo.setValue(null);
            if (todo.getAssigneeId() != null) {
                for (User u : assigneeCombo.getItems()) {
                    if (u != null && todo.getAssigneeId().equals(u.getId())) { assigneeCombo.setValue(u); break; }
                }
            }

            // 截止日期：null/空串/非法格式都不应抛异常（支持 yyyy-MM-dd、带时间等格式）
            try {
                LocalDate due = parseDateSafely(todo.getDueDate());
                if (due != null) {
                    setDueDateBoxes(due.getYear(), due.getMonthValue(), due.getDayOfMonth());
                }
            } catch (Exception e) {
                log.warn("截止日期解析失败: {}", todo.getDueDate());
            }

            // 元信息
            metaLabel.setText(buildMeta(todo));

            // 完成按钮文字
            btnComplete.setText(todo.isCompleted() ? t("detail.cancelComplete") : t("detail.markComplete"));

            // 认领/取消认领按钮：有认领人显示"取消认领"，无认领人显示"认领任务"
            boolean hasAssignee = todo.getAssigneeId() != null && !todo.getAssigneeId().isBlank();
            btnUnclaim.setText(hasAssignee ? t("detail.unclaim") : t("detail.claimTask"));

            setEditable(false);
            loadComments();
        } catch (Exception e) {
            log.error("展示待办详情失败", e);
            if (titleLabel != null) titleLabel.setText(t("detail.loadFailed"));
            if (metaLabel != null) metaLabel.setText("");
        }
    }

    /** 安全解析日期：取前 10 位按 ISO 解析，失败返回 null */
    private LocalDate parseDateSafely(String s) {
        if (s == null || s.trim().isEmpty()) return null;
        try {
            String t = s.trim();
            if (t.length() >= 10) t = t.substring(0, 10);
            return LocalDate.parse(t);
        } catch (Exception e) {
            return null;
        }
    }

    /** 拼接元信息：任何字段异常都不影响整体 */
    private String buildMeta(Todo todo) {
        try {
            String createdAt;
            try {
                createdAt = todo.getCreatedAt() != null ? DT_FMT.format(todo.getCreatedAt()) : t("detail.unknown");
            } catch (Exception ex) { createdAt = t("detail.unknown"); }

            String idShort;
            try {
                String id = todo.getId();
                idShort = (id != null && id.length() > 8) ? id.substring(0, 8) + "…" : String.valueOf(id);
            } catch (Exception ex) { idShort = "?"; }

            return String.format(t("detail.createdAt"), createdAt, idShort);
        } catch (Exception e) {
            return "";
        }
    }

    private void loadComments() {
        try {
            comments.clear();
            if (currentTodo != null && currentTodo.getId() != null) {
                comments.setAll(commentDao.findByTodoId(currentTodo.getId()));
            }
        } catch (Exception e) {
            log.warn("加载评论失败: {}", e.getMessage());
        }
    }

    private String resolveUserName(String userId) {
        if (userId == null) return t("detail.anonymous");
        try {
            for (User u : userService.listAll()) { if (u.getId().equals(userId)) return u.getName(); }
        } catch (Exception e) {
            // 忽略，返回下方默认值
        }
        return t("detail.unknownUser");
    }

    // ===== 编辑 =====
    @FXML private void startEdit() {
        if (currentTodo == null) return;
        editing = true;
        setEditable(true);
    }

    @FXML private void saveEdit() {
        if (currentTodo == null) return;
        try {
            currentTodo.setTitle(titleLabel.getText());
            currentTodo.setDescription(descriptionLabel.getText());
            currentTodo.setStatus(statusCombo.getValue() != null ? statusCombo.getValue() : TodoStatus.PENDING);
            currentTodo.setPriority(priorityCombo.getValue() != null ? priorityCombo.getValue() : TodoPriority.MEDIUM);
            User u = assigneeCombo.getValue();
            currentTodo.setAssigneeId(u != null ? u.getId() : null);
            // 截止日期：提交未生效的延迟输入，确保读到最新值
            for (ComboBox<Integer> box : new ComboBox[]{ yearCombo, monthCombo, dayCombo }) commitBox(box);
            Integer y = yearCombo.getValue();
            Integer m = monthCombo.getValue();
            Integer d = dayCombo.getValue();
            LocalDate dueVal = (y != null && m != null && d != null) ? LocalDate.of(y, m, d) : null;
            currentTodo.setDueDate(dueVal != null ? dueVal.toString() : null);
            todoService.update(currentTodo);
            Todo reloaded = todoService.findById(currentTodo.getId());
            showTodo(reloaded != null ? reloaded : currentTodo);
            notificationService.playSound(NotificationService.SoundType.COMPLETE);
            if (onSaved != null) onSaved.run();
        } catch (Exception e) {
            log.error("保存失败", e);
            new Alert(Alert.AlertType.ERROR, t("detail.saveFailed") + e.getMessage()).showAndWait();
        }
    }

    @FXML private void cancelEdit() {
        if (currentTodo == null) return;
        editing = false;
        showTodo(currentTodo);
    }

    @FXML private void toggleComplete() {
        if (currentTodo == null) return;
        try {
            todoService.toggleComplete(currentTodo.getId());
            Todo reloaded = todoService.findById(currentTodo.getId());
            showTodo(reloaded != null ? reloaded : currentTodo);
            if (onSaved != null) onSaved.run();
        } catch (Exception e) {
            log.error("切换完成状态失败", e);
            new Alert(Alert.AlertType.ERROR, t("detail.toggleFailed") + e.getMessage()).showAndWait();
        }
    }

    @FXML private void toggleClaim() {
        if (currentTodo == null) return;
        try {
            boolean hasAssignee = currentTodo.getAssigneeId() != null && !currentTodo.getAssigneeId().isBlank();
            if (hasAssignee) {
                // 取消认领
                currentTodo.setAssigneeId(null);
                currentTodo.setStatus(TodoStatus.PENDING);
            } else {
                // 认领：弹出用户选择
                List<User> users = userService.listAll();
                User selected = null;
                if (users.isEmpty()) {
                    javafx.scene.control.TextInputDialog nameDlg = new javafx.scene.control.TextInputDialog();
                    nameDlg.setTitle(t("claim.title"));
                    nameDlg.setHeaderText(t("claim.inputName"));
                    nameDlg.setContentText(t("claim.name"));
                    var result = nameDlg.showAndWait();
                    if (result.isPresent() && !result.get().isBlank()) {
                        selected = userService.upsert(result.get(), null);
                    }
                } else {
                    javafx.scene.control.ChoiceDialog<User> dlg = new javafx.scene.control.ChoiceDialog<>(users.get(0), users);
                    dlg.setTitle(t("claim.title"));
                    dlg.setHeaderText(t("claim.select"));
                    dlg.setContentText(t("claim.assignee"));
                    var result = dlg.showAndWait();
                    if (result.isPresent()) selected = result.get();
                }
                if (selected == null) return; // 用户取消
                currentTodo.setAssigneeId(selected.getId());
                currentTodo.setStatus(TodoStatus.IN_PROGRESS);
            }
            currentTodo.setUpdatedAt(LocalDateTime.now());
            todoService.update(currentTodo);
            Todo reloaded = todoService.findById(currentTodo.getId());
            showTodo(reloaded != null ? reloaded : currentTodo);
            if (onSaved != null) onSaved.run();
        } catch (Exception e) {
            log.error("认领操作失败", e);
            new Alert(Alert.AlertType.ERROR, t("detail.toggleFailed") + e.getMessage()).showAndWait();
        }
    }

    @FXML private void deleteTodo() {
        if (currentTodo == null) return;
        Alert confirm = new Alert(Alert.AlertType.CONFIRMATION,
                String.format(t("detail.deleteConfirm"), currentTodo.getTitle()),
                ButtonType.OK, ButtonType.CANCEL);
        confirm.setTitle(t("detail.deleteTitle"));
        confirm.showAndWait().ifPresent(btn -> {
            if (btn == ButtonType.OK) {
                try {
                    todoService.delete(currentTodo.getId());
                    if (onSaved != null) onSaved.run();
                    // 关闭弹窗
                    javafx.stage.Window window = titleLabel.getScene().getWindow();
                    if (window instanceof javafx.stage.Stage stage) stage.close();
                } catch (Exception e) {
                    log.error("删除任务失败", e);
                    new Alert(Alert.AlertType.ERROR, t("detail.deleteFailed") + e.getMessage()).showAndWait();
                }
            }
        });
    }

    private void setEditable(boolean editable) {
        statusCombo.setDisable(!editable);
        priorityCombo.setDisable(!editable);
        assigneeCombo.setDisable(!editable);
        yearCombo.setDisable(!editable);
        monthCombo.setDisable(!editable);
        dayCombo.setDisable(!editable);
        btnEdit.setDisable(editable);
        btnSave.setDisable(!editable);
        btnCancel.setDisable(!editable);
    }

    // ===== 截止日期：年/月/日 三个可编辑 ComboBox（与 NewTodoDialog 同一套逻辑）=====

    /**
     * 初始化年/月/日 三个 ComboBox：
     * - 年：当前年 ± 5 年，预填当前年
     * - 月：1-12，预填当前月
     * - 日：1-该月最大天数，随年/月联动，非法日自动收敛
     */
    private void initDueDateBoxes() {
        LocalDate now = LocalDate.now();
        minYear = now.getYear() - 5;
        maxYear = now.getYear() + 5;
        List<Integer> years = new java.util.ArrayList<>();
        for (int y = minYear; y <= maxYear; y++) years.add(y);
        yearCombo.getItems().setAll(years);
        yearCombo.setValue(now.getYear());

        monthCombo.getItems().setAll(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12);
        monthCombo.setValue(now.getMonthValue());

        // ===== 可编辑模式：可下拉选择，也可直接按数字键输入 =====
        for (ComboBox<Integer> box : new ComboBox[]{ yearCombo, monthCombo, dayCombo }) {
            box.setEditable(true);
        }
        // 输入过滤器：只允许纯数字（年最多 4 位，月/日最多 2 位）
        yearCombo.getEditor().setTextFormatter(digitsFormatter(4));
        monthCombo.getEditor().setTextFormatter(digitsFormatter(2));
        dayCombo.getEditor().setTextFormatter(digitsFormatter(2));
        // 数字键输入：500ms 延迟合并两位数逻辑
        yearCombo.getEditor().setOnKeyTyped(e -> handleDigitTyped(yearCombo, e));
        monthCombo.getEditor().setOnKeyTyped(e -> handleDigitTyped(monthCombo, e));
        dayCombo.getEditor().setOnKeyTyped(e -> handleDigitTyped(dayCombo, e));
        // 任何文本变化（退格/粘贴等）都重启延迟提交定时器
        for (ComboBox<Integer> box : new ComboBox[]{ yearCombo, monthCombo, dayCombo }) {
            box.getEditor().textProperty().addListener((o, a, b) -> {
                if (committing) return;
                if (b != null && !b.isEmpty()) restartTimer(box);
            });
            box.getEditor().setOnAction(ev -> commitBox(box));
        }
        // 下拉选择年/月 → 重算日的可选范围（含闰年 2 月）
        yearCombo.valueProperty().addListener((o, a, b) -> { if (!committing) rebuildDayBox(); });
        monthCombo.valueProperty().addListener((o, a, b) -> { if (!committing) rebuildDayBox(); });

        // 初始化日下拉
        rebuildDayBox();
        int curD = LocalDate.now().getDayOfMonth();
        if (dayCombo.getValue() == null || dayCombo.getValue() != curD) {
            dayCombo.setValue(curD);
        }
    }

    /** 展示时设置年/月/日（超范围值自动收敛） */
    private void setDueDateBoxes(int year, int month, int day) {
        committing = true;
        if (year >= minYear && year <= maxYear) {
            yearCombo.setValue(year);
        } else {
            yearCombo.setValue(Math.max(minYear, Math.min(maxYear, year)));
        }
        monthCombo.setValue(Math.max(1, Math.min(12, month)));
        committing = false;
        // 年/月变化会触发 rebuildDayBox 收敛日；手动补一次保证生效
        rebuildDayBox();
        committing = true;
        dayCombo.setValue(Math.max(1, Math.min(currentMaxDay(), day)));
        committing = false;
    }

    /** 解析输入文本为整数，空/非法返回 null */
    private Integer parseNum(String t) {
        if (t == null) return null;
        t = t.trim();
        if (t.isEmpty()) return null;
        try { return Integer.valueOf(t); } catch (NumberFormatException e) { return null; }
    }

    /** 依据当前年/月重建日下拉，超范围的旧值自动收敛到该月最大天数 */
    private void rebuildDayBox() {
        Integer y = yearCombo.getValue();
        Integer m = monthCombo.getValue();
        int maxDay = 31;
        if (y != null && m != null) {
            try {
                maxDay = YearMonth.of(y, m).lengthOfMonth();
            } catch (Exception ignored) { maxDay = 31; }
        }
        Integer oldDay = dayCombo.getValue();
        dayCombo.getItems().clear();
        for (int d = 1; d <= maxDay; d++) dayCombo.getItems().add(d);
        int target = (oldDay == null ? maxDay : Math.min(oldDay, maxDay));
        if (target < 1) target = 1;
        committing = true;
        dayCombo.setValue(target);
        committing = false;
    }

    /** 数字输入过滤器：只允许纯数字，最多 maxLen 位（禁止非数字输入） */
    private TextFormatter<Integer> digitsFormatter(int maxLen) {
        return new TextFormatter<Integer>(change ->
                change.getControlNewText().matches("\\d{0," + maxLen + "}") ? change : null);
    }

    /** 停止某个框的延迟提交定时器 */
    private void stopTimer(ComboBox<Integer> box) {
        Timeline t = delayTimers.get(box);
        if (t != null) t.stop();
    }

    /** 启动/重启 500ms 延迟提交定时器 */
    private void restartTimer(ComboBox<Integer> box) {
        stopTimer(box);
        Timeline timer = new Timeline(new KeyFrame(Duration.millis(500), ev -> commitBox(box)));
        timer.setCycleCount(1);
        timer.play();
        delayTimers.put(box, timer);
    }

    /**
     * 数字键输入处理（延迟合并规则）：
     * - 当前文本为单个数字且与新数字能构成合法两位数（如 1→2）→ 合并为两位数，重新计时
     * - 否则先提交当前值，新数字作为新的独立输入
     * - 500ms 内无新输入 → 提交当前文本（超范围值自动收敛到边界）
     */
    private void handleDigitTyped(ComboBox<Integer> box, KeyEvent e) {
        if (e.getCharacter() == null || e.getCharacter().length() != 1) return;
        char c = e.getCharacter().charAt(0);
        if (!Character.isDigit(c)) return;
        String text = box.getEditor().getText();
        if (text == null) text = "";
        boolean mergeable = (box == yearCombo ? text.length() >= 1 && text.length() <= 3
                                            : text.length() == 1);
        if (mergeable && validMerge(box, text + c)) {
            e.consume();
            committing = true;
            box.setValue(Integer.parseInt(text + c));
            committing = false;
            if (box != dayCombo) rebuildDayBox();
            restartTimer(box);
            return;
        }
        commitBox(box);
        box.getEditor().selectAll();
        restartTimer(box);
    }

    /** 判断合并后的两位数是否在该框的合法范围内（月 1-12，日随年月/闰年变化） */
    private boolean validMerge(ComboBox<Integer> box, String merged) {
        Integer v = parseNum(merged);
        if (v == null) return false;
        if (box == yearCombo) return v >= minYear && v <= maxYear;
        if (box == monthCombo) return v >= 1 && v <= 12;
        return v >= 1 && v <= currentMaxDay();
    }

    /** 当前年月对应的最大天数（含闰年判断） */
    private int currentMaxDay() {
        Integer y = yearCombo.getValue();
        Integer m = monthCombo.getValue();
        if (y != null && m != null) {
            try { return YearMonth.of(y, m).lengthOfMonth(); } catch (Exception ignored) { }
        }
        return 31;
    }

    /** 停止定时器并提交某个框的输入：空文本不动，超范围值收敛到边界，同步文本显示 */
    private void commitBox(ComboBox<Integer> box) {
        stopTimer(box);
        String text = box.getEditor().getText();
        Integer v = parseNum(text);
        if (v == null) return;
        int lo = 1, hi = 31;
        if (box == yearCombo) { lo = minYear; hi = maxYear; }
        else if (box == monthCombo) hi = 12;
        else hi = currentMaxDay();
        if (v < lo) v = lo;
        if (v > hi) v = hi;
        boolean changed = !v.equals(box.getValue());
        if (changed) {
            committing = true;
            box.setValue(v);
            committing = false;
        }
        if (changed && box != dayCombo) rebuildDayBox();
        String display = box.getValue() == null ? "" : box.getValue().toString();
        if (!display.equals(text)) {
            committing = true;
            box.getEditor().setText(display);
            committing = false;
        }
    }

    // ===== 评论 =====
    @FXML private void sendComment() {
        if (currentTodo == null) { new Alert(Alert.AlertType.INFORMATION, t("detail.selectTodo")).showAndWait(); return; }
        String content = commentInput.getText().trim();
        if (content.isEmpty()) return;
        try {
            List<User> users = userService.listAll();
            String userId = users.isEmpty() ? "anonymous" : users.get(0).getId();
            Comment c = new Comment();
            c.setTodoId(currentTodo.getId());
            c.setUserId(userId);
            c.setContent(content);
            c.setCreatedAt(LocalDateTime.now());
            commentDao.create(c);
            commentInput.clear();
            loadComments();
            notificationService.playSound(NotificationService.SoundType.INFO);
        } catch (Exception e) {
            log.error("发送评论失败", e);
            new Alert(Alert.AlertType.ERROR, t("detail.commentFailed") + e.getMessage()).showAndWait();
        }
    }

    /** i18n: 详情弹窗绑定所有文字到 I18n */
    private void updateDetailTexts() {
        if (btnEdit != null) btnEdit.textProperty().bind(com.teamtodo.util.I18n.text("detail.edit"));
        if (btnSave != null) btnSave.textProperty().bind(com.teamtodo.util.I18n.text("detail.save"));
        if (btnCancel != null) btnCancel.textProperty().bind(com.teamtodo.util.I18n.text("detail.cancel"));
        if (btnDelete != null) btnDelete.textProperty().bind(com.teamtodo.util.I18n.text("detail.delete"));
        if (commentInput != null) commentInput.promptTextProperty().bind(com.teamtodo.util.I18n.text("detail.commentHint"));
        if (btnSendComment != null) btnSendComment.textProperty().bind(com.teamtodo.util.I18n.text("detail.commentSend"));
        if (statusFormLabel != null) statusFormLabel.textProperty().bind(com.teamtodo.util.I18n.text("detail.status"));
        if (priorityFormLabel != null) priorityFormLabel.textProperty().bind(com.teamtodo.util.I18n.text("detail.priority"));
        if (assigneeFormLabel != null) assigneeFormLabel.textProperty().bind(com.teamtodo.util.I18n.text("detail.assignee"));
        if (dueDateFormLabel != null) dueDateFormLabel.textProperty().bind(com.teamtodo.util.I18n.text("detail.dueDate"));
        if (yearLabel != null) yearLabel.textProperty().bind(com.teamtodo.util.I18n.text("detail.year"));
        if (monthLabel != null) monthLabel.textProperty().bind(com.teamtodo.util.I18n.text("detail.month"));
        if (dayLabel != null) dayLabel.textProperty().bind(com.teamtodo.util.I18n.text("detail.day"));
        if (commentsSectionLabel != null) commentsSectionLabel.textProperty().bind(com.teamtodo.util.I18n.text("detail.comments"));

        // 动态文字：占位符标题、完成/认领按钮、元信息、下拉选中项、评论列表
        if (currentTodo == null) {
            if (titleLabel != null) titleLabel.setText(t("detail.selectFirst"));
        } else {
            if (btnComplete != null) btnComplete.setText(currentTodo.isCompleted() ? t("detail.cancelComplete") : t("detail.markComplete"));
            boolean hasAssignee = currentTodo.getAssigneeId() != null && !currentTodo.getAssigneeId().isBlank();
            if (btnUnclaim != null) btnUnclaim.setText(hasAssignee ? t("detail.unclaim") : t("detail.claimTask"));
            if (metaLabel != null) metaLabel.setText(buildMeta(currentTodo));
            if (commentList != null) commentList.refresh();
            if (statusCombo != null) {
                TodoStatus sel = statusCombo.getValue();
                statusCombo.setItems(FXCollections.observableArrayList(TodoStatus.values()));
                if (sel != null) statusCombo.setValue(sel);
            }
            if (priorityCombo != null) {
                TodoPriority sel = priorityCombo.getValue();
                priorityCombo.setItems(FXCollections.observableArrayList(TodoPriority.values()));
                if (sel != null) priorityCombo.setValue(sel);
            }
        }
    }



}