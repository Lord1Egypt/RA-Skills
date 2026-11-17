package com.teamtodo.controller;

import com.teamtodo.model.Todo;
import com.teamtodo.model.User;
import com.teamtodo.model.enums.TodoPriority;
import com.teamtodo.service.TodoService;
import com.teamtodo.service.UserService;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.scene.control.*;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.util.Duration;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.stage.Modality;
import javafx.stage.Stage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDate;
import java.time.YearMonth;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import static com.teamtodo.util.I18n.t;
import com.teamtodo.util.I18n;

/**
 * 新建待办对话框（纯 JavaFX 代码构建，模态）：
 * - 标题（必填）、描述、负责人、优先级、截止日期
 * - 回车/「创建」提交；Esc/「取消」关闭
 * - 创建成功后通过回调把新 Todo 返回给主界面刷新
 *
 * 用法：
 * <pre>
 *   NewTodoDialog.show(todoService, userService, created -> { ... });
 * </pre>
 */
public class NewTodoDialog {
    private static final Logger log = LoggerFactory.getLogger(NewTodoDialog.class);

    private final TodoService todoService;
    private final UserService userService;
    private final Consumer<Todo> onCreated;

    private Stage stage;

    private final TextField titleField = new TextField();
    private final TextArea descArea = new TextArea();
    private final ComboBox<User> assigneeBox = new ComboBox<>();
    private final ComboBox<TodoPriority> priorityBox = new ComboBox<>();
    // 截止日期：年/月/日 三个可编辑 ComboBox + 启用开关（可下拉选择，也可直接输入数字）
    private final CheckBox dueCheck = new CheckBox(t("newTodo.dueCheck"));
    private final ComboBox<Integer> yearBox = new ComboBox<>();
    private final ComboBox<Integer> monthBox = new ComboBox<>();
    private final ComboBox<Integer> dayBox = new ComboBox<>();
    private final Label errLabel = new Label();

    // 年/月/日输入逻辑：500ms 延迟提交定时器、年份范围
    private final Map<ComboBox<Integer>, Timeline> delayTimers = new HashMap<>();
    private boolean committing = false;
    private int minYear;
    private int maxYear;

    private NewTodoDialog(TodoService todoService, UserService userService, Consumer<Todo> onCreated) {
        this.todoService = todoService;
        this.userService = userService;
        this.onCreated = onCreated;
    }

    /** 静态入口：打开新建待办对话框（保证 FX 线程） */
    public static void show(TodoService todoService, UserService userService, Consumer<Todo> onCreated) {
        Runnable open = () -> {
            NewTodoDialog dialog = new NewTodoDialog(todoService, userService, onCreated);
            dialog.open();
        };
        if (Platform.isFxApplicationThread()) {
            open.run();
        } else {
            Platform.runLater(open);
        }
    }

    private void open() {
        stage = new Stage();
        stage.initModality(Modality.APPLICATION_MODAL);
        List<javafx.stage.Window> windows = Stage.getWindows();
        if (!windows.isEmpty()) stage.initOwner(windows.get(0));
        stage.setTitle(t("newTodo.title"));
        stage.setMinWidth(440);
        // 设置图标（与主窗口一致）
        javafx.scene.image.Image icon = com.teamtodo.App.loadIcon();
        if (icon != null) stage.getIcons().add(icon);

        GridPane form = buildForm();
        Scene scene = new Scene(form, 460, 400);
        stage.setScene(scene);

        // Esc 关闭
        scene.addEventFilter(KeyEvent.KEY_PRESSED, e -> {
            if (e.getCode() == KeyCode.ESCAPE) close();
        });

        stage.show();
        titleField.requestFocus();
    }

    private GridPane buildForm() {
        GridPane grid = new GridPane();
        GridPane.setColumnIndex(new Label(""), 0);
        // 第一列固定 72px，第二列拉伸
        javafx.scene.layout.ColumnConstraints c0 = new javafx.scene.layout.ColumnConstraints(72, 72, 72);
        javafx.scene.layout.ColumnConstraints c1 = new javafx.scene.layout.ColumnConstraints(0, 200, Double.MAX_VALUE);
        c1.setHgrow(javafx.scene.layout.Priority.ALWAYS);
        grid.getColumnConstraints().addAll(c0, c1);
        grid.setVgap(10);
        grid.setPadding(new Insets(16));

        int row = 0;
        grid.add(new Label(t("newTodo.titleLabel")), 0, row);
        titleField.setPromptText(t("newTodo.titleHint"));
        grid.add(titleField, 1, row++);

        grid.add(new Label(t("newTodo.desc")), 0, row);
        descArea.setPromptText(t("newTodo.descHint"));
        descArea.setPrefRowCount(3);
        grid.add(descArea, 1, row++);

        grid.add(new Label(t("newTodo.assignee")), 0, row);
        try {
            List<User> users = userService != null ? userService.listAll() : List.of();
            assigneeBox.getItems().addAll(users);
        } catch (Exception ex) {
            log.warn("加载用户列表失败：{}", ex.getMessage());
        }
        assigneeBox.setPromptText(t("newTodo.assigneeHint"));
        assigneeBox.setPrefWidth(titleField.getWidth() == 0 ? 220 : titleField.getWidth());
        assigneeBox.setCellFactory(lv -> new ListCell<>() {
            @Override protected void updateItem(User u, boolean empty) {
                super.updateItem(u, empty);
                setText(empty ? null : (u == null ? null : u.getName()));
            }
        });
        assigneeBox.setButtonCell(new ListCell<>() {
            @Override protected void updateItem(User u, boolean empty) {
                super.updateItem(u, empty);
                setText(empty ? null : (u == null ? null : u.getName()));
            }
        });
        grid.add(assigneeBox, 1, row++);

        grid.add(new Label(t("newTodo.priority")), 0, row);
        priorityBox.getItems().setAll(TodoPriority.values());
        priorityBox.setValue(TodoPriority.MEDIUM);
        priorityBox.setCellFactory(lv -> new ListCell<>() {
            @Override protected void updateItem(TodoPriority p, boolean empty) {
                super.updateItem(p, empty);
                setText(empty ? null : (p == null ? null : p.getLabel()));
            }
        });
        priorityBox.setButtonCell(new ListCell<>() {
            @Override protected void updateItem(TodoPriority p, boolean empty) {
                super.updateItem(p, empty);
                setText(empty ? null : (p == null ? null : p.getLabel()));
            }
        });
        grid.add(priorityBox, 1, row++);

        grid.add(new Label(t("newTodo.dueDate")), 0, row);
        initDueDateBoxes();
        grid.add(dueCheck, 1, row++);
        HBox dueRow = new HBox(3, yearBox, monthBox, dayBox);
        yearBox.setPrefWidth(90);
        yearBox.setMinWidth(90);
        monthBox.setPrefWidth(70);
        monthBox.setMinWidth(70);
        dayBox.setPrefWidth(70);
        dayBox.setMinWidth(70);
        dueRow.setAlignment(javafx.geometry.Pos.CENTER_LEFT);
        for (javafx.scene.Node n : dueRow.getChildren()) {
            javafx.scene.layout.HBox.setHgrow(n, javafx.scene.layout.Priority.ALWAYS);
        }
        grid.add(dueRow, 1, row++);

        // 错误提示
        errLabel.setTextFill(javafx.scene.paint.Color.web("#c62828"));
        grid.add(errLabel, 1, row++);

        // 按钮
        Button cancelBtn = new Button(t("newTodo.cancel"));
        cancelBtn.getStyleClass().add("btn");
        cancelBtn.setOnAction(e -> close());

        Button createBtn = new Button(t("newTodo.create"));
        createBtn.getStyleClass().addAll("btn", "btn-primary");
        createBtn.setDefaultButton(true);
        createBtn.setOnAction(e -> submit());

        HBox buttons = new HBox(10, cancelBtn, createBtn);
        buttons.setAlignment(Pos.CENTER_RIGHT);
        grid.add(buttons, 0, row, 2, 1);

        titleField.setOnAction(e -> submit());

        return grid;
    }

    /** 校验并提交创建 */
    private void submit() {
        String title = titleField.getText() == null ? "" : titleField.getText().trim();
        if (title.isEmpty()) {
            errLabel.setText(t("newTodo.errTitle"));
            titleField.requestFocus();
            return;
        }
        errLabel.setText("");

        String desc = descArea.getText() == null ? null : descArea.getText().trim();
        if (desc != null && desc.isEmpty()) desc = null;

        User assignee = assigneeBox.getValue();
        String assigneeId = assignee != null ? assignee.getId() : null;

        // 截止日期：勾选且年月日均有效才生效
        String dueDate = null;
        if (dueCheck.isSelected()) {
            // 提交未生效的延迟输入，确保读到最新值
            for (ComboBox<Integer> box : new ComboBox[]{ yearBox, monthBox, dayBox }) commitBox(box);
            Integer y = yearBox.getValue();
            Integer m = monthBox.getValue();
            Integer d = dayBox.getValue();
            if (y == null || m == null || d == null) {
                errLabel.setText(t("newTodo.errDate"));
                return;
            }
            try {
                LocalDate due = LocalDate.of(y, m, d);
                dueDate = due.toString();
            } catch (Exception ex) {
                errLabel.setText(String.format(t("newTodo.errDateInvalid"), ex.getMessage()));
                return;
            }
        }

        Todo created;
        try {
            created = todoService.create(title, desc, assigneeId, dueDate);
            if (created != null) {
                created.setPriority(priorityBox.getValue());
                todoService.update(created);
            }
        } catch (Exception ex) {
            log.warn("创建待办失败：{}", ex.getMessage());
            errLabel.setText(String.format(t("newTodo.errCreate"), ex.getMessage()));
            return;
        }

        if (onCreated != null) {
            onCreated.accept(created);
        }
        close();
    }

    private void close() {
        // 关闭前停止所有延迟提交定时器，避免窗口关闭后仍触发事件
        for (Timeline t : new java.util.ArrayList<>(delayTimers.values())) t.stop();
        delayTimers.clear();
        if (stage != null && stage.isShowing()) {
            stage.close();
        }
    }

    /**
     * 初始化年/月/日 三个 ComboBox：
     * - 年：当前年 ± 5 年，预填当前年
     * - 月：1-12，预填当前月
     * - 日：1-该月最大天数，随年/月联动，非法日自动收敛
     * - 默认不启用（勾选后才写入 dueDate）
     */
    private void initDueDateBoxes() {
        LocalDate now = LocalDate.now();
        minYear = now.getYear() - 5;
        maxYear = now.getYear() + 5;
        List<Integer> years = new java.util.ArrayList<>();
        for (int y = minYear; y <= maxYear; y++) years.add(y);
        yearBox.getItems().setAll(years);
        yearBox.setValue(now.getYear());

        monthBox.getItems().setAll(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12);
        monthBox.setValue(now.getMonthValue());

        // ===== 可编辑模式：可下拉选择，也可直接按数字键输入 =====
        for (ComboBox<Integer> box : new ComboBox[]{ yearBox, monthBox, dayBox }) {
            box.setEditable(true);
        }
        // 输入过滤器：只允许纯数字（年最多 4 位，月/日最多 2 位）
        yearBox.getEditor().setTextFormatter(digitsFormatter(4));
        monthBox.getEditor().setTextFormatter(digitsFormatter(2));
        dayBox.getEditor().setTextFormatter(digitsFormatter(2));
        // 数字键输入：500ms 延迟合并两位数逻辑
        yearBox.getEditor().setOnKeyTyped(e -> handleDigitTyped(yearBox, e));
        monthBox.getEditor().setOnKeyTyped(e -> handleDigitTyped(monthBox, e));
        dayBox.getEditor().setOnKeyTyped(e -> handleDigitTyped(dayBox, e));
        // 任何文本变化（退格/粘贴等）都重启延迟提交定时器
        for (ComboBox<Integer> box : new ComboBox[]{ yearBox, monthBox, dayBox }) {
            box.getEditor().textProperty().addListener((o, a, b) -> {
                if (committing) return;
                if (b != null && !b.isEmpty()) restartTimer(box);
            });
            box.getEditor().setOnAction(ev -> commitBox(box));
        }
        // 下拉选择年/月 → 重算日的可选范围（含闰年 2 月）
        yearBox.valueProperty().addListener((o, a, b) -> { if (!committing) rebuildDayBox(); });
        monthBox.valueProperty().addListener((o, a, b) -> { if (!committing) rebuildDayBox(); });

        // 启用/禁用联动
        Runnable setEnabled = () -> {
            boolean on = dueCheck.isSelected();
            yearBox.setDisable(!on);
            monthBox.setDisable(!on);
            dayBox.setDisable(!on);
        };
        dueCheck.selectedProperty().addListener((o, a, s) -> setEnabled.run());
        setEnabled.run();

        // 初始化日下拉
        rebuildDayBox();
        int curD = LocalDate.now().getDayOfMonth();
        if (dayBox.getValue() == null || dayBox.getValue() != curD) {
            dayBox.setValue(curD);
        }
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
        Integer y = yearBox.getValue();
        Integer m = monthBox.getValue();
        int maxDay = 31;
        if (y != null && m != null) {
            try {
                maxDay = YearMonth.of(y, m).lengthOfMonth();
            } catch (Exception ignored) { maxDay = 31; }
        }
        Integer oldDay = dayBox.getValue();
        dayBox.getItems().clear();
        for (int d = 1; d <= maxDay; d++) dayBox.getItems().add(d);
        int target = (oldDay == null ? maxDay : Math.min(oldDay, maxDay));
        if (target < 1) target = 1;
        committing = true;
        dayBox.setValue(target);
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
     * - 否则先提交当前值，新数字作为新的独立输入（如月输入 1 后输入 3：1 先生效，3 是新输入）
     * - 500ms 内无新输入 → 提交当前文本（超范围值自动收敛到边界）
     */
    private void handleDigitTyped(ComboBox<Integer> box, KeyEvent e) {
        if (e.getCharacter() == null || e.getCharacter().length() != 1) return;
        char c = e.getCharacter().charAt(0);
        if (!Character.isDigit(c)) return;
        String text = box.getEditor().getText();
        if (text == null) text = "";
        boolean mergeable = (box == yearBox ? text.length() >= 1 && text.length() <= 3
                                            : text.length() == 1);
        if (mergeable && validMerge(box, text + c)) {
            // 合法两位数：合并（阻止默认插入，直接提交合并值并重新计时）
            e.consume();
            committing = true;
            box.setValue(Integer.parseInt(text + c));
            committing = false;
            if (box != dayBox) rebuildDayBox();
            restartTimer(box);
            return;
        }
        // 不构成合法合并：先提交当前值，再全选使新数字作为独立输入替换旧文本
        commitBox(box);
        box.getEditor().selectAll();
        restartTimer(box);
    }

    /** 判断合并后的两位数是否在该框的合法范围内（月 1-12，日随年月/闰年变化） */
    private boolean validMerge(ComboBox<Integer> box, String merged) {
        Integer v = parseNum(merged);
        if (v == null) return false;
        if (box == yearBox) return v >= minYear && v <= maxYear;
        if (box == monthBox) return v >= 1 && v <= 12;
        return v >= 1 && v <= currentMaxDay();
    }

    /** 当前年月对应的最大天数（含闰年判断） */
    private int currentMaxDay() {
        Integer y = yearBox.getValue();
        Integer m = monthBox.getValue();
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
        if (box == yearBox) { lo = minYear; hi = maxYear; }
        else if (box == monthBox) hi = 12;
        else hi = currentMaxDay();
        if (v < lo) v = lo;
        if (v > hi) v = hi;
        boolean changed = !v.equals(box.getValue());
        if (changed) {
            committing = true;
            box.setValue(v);
            committing = false;
        }
        if (changed && box != dayBox) rebuildDayBox();
        String display = box.getValue() == null ? "" : box.getValue().toString();
        if (!display.equals(text)) {
            committing = true;
            box.getEditor().setText(display);
            committing = false;
        }
    }
}
