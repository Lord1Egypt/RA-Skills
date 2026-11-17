package com.teamtodo.controller;

import com.teamtodo.model.Todo;
import com.teamtodo.service.TodoService;
import com.teamtodo.util.LunarCalendarUtil;
import javafx.geometry.HPos;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.Region;
import javafx.scene.layout.VBox;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import static com.teamtodo.util.I18n.t;
import com.teamtodo.util.I18n;

/**
 * 日历视图控制器（纯代码实现，无 FXML）：
 * - 月视图：7 列（周一到周日）× 5~6 行
 * - 顶部：年月标题 + 左右切换按钮
 * - 每个日期格子显示：公历日期号（大字）+ 农历/节日（小字，节日红色）+ 当天待办数量（右下角红色数字）
 * - 点击日期格子 → 下方显示该日待办列表
 * - 今天的日期高亮
 * - getView() 返回 Parent 节点
 * - setOnDateSelected(Consumer&lt;String&gt;) 日期选中回调
 */
public class CalendarController {
    private static final Logger log = LoggerFactory.getLogger(CalendarController.class);

    /** 列数：周一到周日 */
    private static final int COLS = 7;
    /** 日期格子最小尺寸 */
    private static final double CELL_MIN_W = 44;
    /** 日期格子最小高度（日期号 + 农历/节日 + 待办数 三行） */
    private static final double CELL_MIN_H = 54;
    private final TodoService todoService = new TodoService();

    /** 当前显示的月份（1 号所在日期，方便切换） */
    private LocalDate currentMonth = LocalDate.now().withDayOfMonth(1);
    /** 当前选中的日期 */
    private LocalDate selectedDate = LocalDate.now();
    /** 日期选中回调（MainController 注入） */
    private Consumer<String> onDateSelected;

    private VBox root;
    private Label titleLabel;
    private GridPane calendarGrid;
    private VBox detailPanel;
    private Label detailTitle;
    private VBox detailList;

    /** 日期 → 该日待办列表 */
    private final Map<LocalDate, List<Todo>> todosByDate = new HashMap<>();

    // ===== 对外接口 =====

    /** 设置日期选中回调（参数为 yyyy-MM-dd 格式日期字符串） */
    public void setOnDateSelected(Consumer<String> callback) {
        this.onDateSelected = callback;
    }

    /** 返回日历视图根节点（懒加载构建） */
    public Parent getView() {
        if (root == null) {
            root = buildView();
        }
        refresh();
        javafx.scene.control.ScrollPane scroll = new javafx.scene.control.ScrollPane(root);
        scroll.setFitToWidth(true);
        scroll.setStyle("-fx-background-color:transparent;");
        return scroll;
    }

    /** 刷新日历（重建格子 + 选中日期详情） */
    public void refresh() {
        if (root == null) getView();
        buildCalendarGrid();
        showSelectedDayDetail(selectedDate);
    }

    // ===== 视图构建 =====

    private VBox buildView() {
        VBox r = new VBox(12);
        r.setPadding(new Insets(16));
        r.setStyle("-fx-background-color:#F9FAFB;");
        VBox.setVgrow(calendarSection(), Priority.ALWAYS);

        // 顶部：左右切换 + 年月标题
        Button btnPrev = makeNavButton("‹");
        btnPrev.setOnAction(e -> { currentMonth = currentMonth.minusMonths(1); onMonthChanged(); });

        Button btnNext = makeNavButton("›");
        btnNext.setOnAction(e -> { currentMonth = currentMonth.plusMonths(1); onMonthChanged(); });

        Button btnToday = new Button(t("calendar.today"));
        btnToday.setOnAction(e -> { currentMonth = LocalDate.now().withDayOfMonth(1); selectedDate = LocalDate.now(); onMonthChanged(); });

        titleLabel = new Label();
        titleLabel.setStyle("-fx-font-size:16px; -fx-font-weight:bold; -fx-text-fill:#1F2937;");

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        HBox header = new HBox(10, btnPrev, btnNext, btnToday, titleLabel, spacer);
        header.setAlignment(Pos.CENTER_LEFT);

        r.getChildren().addAll(header, calendarSection(), detailSection());
        return r;
    }

    /** 日历区块（网格容器，格子内容动态填充） */
    private VBox calendarSection() {
        calendarGrid = new GridPane();
        calendarGrid.setHgap(4);
        calendarGrid.setVgap(4);
        for (int c = 0; c < COLS; c++) {
            javafx.scene.layout.ColumnConstraints cc = new javafx.scene.layout.ColumnConstraints();
            cc.setHgrow(Priority.ALWAYS);
            calendarGrid.getColumnConstraints().add(cc);
        }

        VBox box = new VBox(6, calendarGrid);
        box.setPadding(new Insets(12));
        box.setStyle("-fx-background-color:white; -fx-background-radius:10; -fx-border-color:#E5E7EB; -fx-border-radius:10; -fx-border-width:1;");
        return box;
    }

    /** 选中日期详情区块 */
    private VBox detailSection() {
        detailTitle = new Label();
        detailTitle.setStyle("-fx-font-size:14px; -fx-font-weight:bold; -fx-text-fill:#1F2937;");

        detailList = new VBox(6);

        detailPanel = new VBox(8, detailTitle, detailList);
        detailPanel.setPadding(new Insets(12));
        detailPanel.setStyle("-fx-background-color:white; -fx-background-radius:10; -fx-border-color:#E5E7EB; -fx-border-radius:10; -fx-border-width:1;");
        return detailPanel;
    }

    // ===== 日历格子 =====

    /** 切换月份或选中日期后：重绘整张日历 */
    private void onMonthChanged() {
        buildCalendarGrid();
        showSelectedDayDetail(selectedDate);
    }

    /** 根据当前月份 + 全部待办重建日历网格 */
    private void buildCalendarGrid() {
        calendarGrid.getChildren().clear();

        // 1) 统计每个日期的待办数量
        todosByDate.clear();
        try {
            List<Todo> all = todoService.listAll();
            for (Todo t : all) {
                LocalDate due = parseDate(t.getDueDate());
                if (due == null) continue;
                todosByDate.computeIfAbsent(due, k -> new ArrayList<>()).add(t);
            }
        } catch (Exception ex) {
            log.warn("加载待办失败，日历格子仅显示日期", ex);
        }

        // 2) 星期表头：周一到周日
        String[] weekNames = {I18n.t("calendar.monday"), t("calendar.tuesday"), t("calendar.wednesday"), t("calendar.thursday"), t("calendar.friday"), t("calendar.saturday"), t("calendar.sunday")};
        for (int c = 0; c < COLS; c++) {
            Label wl = new Label(weekNames[c]);
            wl.setStyle("-fx-font-size:12px; -fx-text-fill:#6B7280; -fx-alignment:center;");
            GridPane.setHalignment(wl, HPos.CENTER);
            calendarGrid.add(wl, c, 0);
        }

        // 3) 计算该月第一格要显示的日期（周一对齐）
        LocalDate firstDay = currentMonth;
        LocalDate gridStart = firstDay.withDayOfMonth(1);
        // Java DayOfWeek: MONDAY=1 ... SUNDAY=7，正好直接偏移
        gridStart = gridStart.minusDays(gridStart.getDayOfWeek().getValue() - 1);

        LocalDate today = LocalDate.now();
        LocalDate cursor = gridStart;
        int row = 1;

        // 最多 6 行 × 7 列，覆盖整个月份
        for (int i = 0; i < 42; i++) {
            boolean inMonth = cursor.getMonthValue() == firstDay.getMonthValue()
                    && cursor.getYear() == firstDay.getYear();
            VBox cell = makeDateCell(cursor, inMonth, today);
            GridPane.setHalignment(cell, HPos.CENTER);
            GridPane.setVgrow(cell, Priority.ALWAYS);
            calendarGrid.add(cell, i % COLS, row);
            cursor = cursor.plusDays(1);
            if (i % COLS == COLS - 1) row++;
        }
    }

    /** 构建单个日期格子：日期号 + 农历/节日 + 待办数量；今天高亮、选中描边 */
    private VBox makeDateCell(LocalDate date, boolean inMonth, LocalDate today) {
        VBox cell = new VBox(2);
        cell.setPrefSize(CELL_MIN_W, CELL_MIN_H);
        cell.setMinSize(CELL_MIN_W, CELL_MIN_H);
        cell.setPadding(new Insets(4));
        cell.setCursor(javafx.scene.Cursor.HAND);

        boolean isToday = date.equals(today);
        boolean isSelected = date.equals(selectedDate);

        // 背景：今天=蓝底，选中=浅蓝描边，普通=白
        String bg = "#FFFFFF";
        String border = "#E5E7EB";
        if (isToday) { bg = "#DBEAFE"; border = "#3B82F6"; }
        if (isSelected) border = "#1D4ED8";
        cell.setStyle("-fx-background-color:" + bg + "; -fx-background-radius:8; -fx-border-color:" + border
                + "; -fx-border-radius:8; -fx-border-width:" + (isSelected ? "2" : "1") + ";");

        // 日期号（今天加粗高亮）
        Label dayLabel = new Label(String.valueOf(date.getDayOfMonth()));
        dayLabel.setStyle((isToday ? "-fx-font-weight:bold; -fx-text-fill:#1D4ED8;" : "")
                + (inMonth ? "" : "-fx-opacity:0.35;"));
        dayLabel.setMaxWidth(Double.MAX_VALUE);

        // 农历日期 / 节日（节日优先，红色）
        List<Todo> dayTodos = todosByDate.getOrDefault(date, List.of());
        String subText = null;
        String subStyle = "-fx-font-size:10px; -fx-text-fill:#6B7280;";
        try {
            String festival = LunarCalendarUtil.getFestival(date);
            if (festival != null) {
                subText = festival;
                subStyle = "-fx-font-size:10px; -fx-text-fill:#DC2626;";
            } else {
                subText = LunarCalendarUtil.getLunarText(date);
            }
        } catch (Exception ex) {
            log.debug("农历计算失败: {}", date, ex);
        }
        Label subLabel = new Label(subText == null ? " " : subText);
        subLabel.setStyle(subStyle + (inMonth ? "" : " -fx-opacity:0.35;"));
        subLabel.setMaxWidth(Double.MAX_VALUE);
        subLabel.setWrapText(true);

        // 待办数量（右下角数字）
        HBox countRow = new HBox();
        countRow.setMaxWidth(Double.MAX_VALUE);
        if (!dayTodos.isEmpty()) {
            Region spacer = new Region();
            HBox.setHgrow(spacer, Priority.ALWAYS);
            Label countLabel = new Label(String.valueOf(dayTodos.size()));
            countLabel.setStyle("-fx-font-size:11px; -fx-font-weight:bold; -fx-text-fill:#DC2626;");
            countRow.getChildren().addAll(spacer, countLabel);
        }

        // 悬停提示：日期 + 农历/节日 + 待办数
        String tipExtra = "";
        String tipFest = null;
        try {
            tipFest = LunarCalendarUtil.getFestival(date);
        } catch (Exception ignored) { /* 提示可选 */ }
        String tipLunar = null;
        try {
            tipLunar = LunarCalendarUtil.getLunarText(date);
        } catch (Exception ignored) { /* 提示可选 */ }
        if (tipFest != null) tipExtra = " · " + tipFest;
        else if (tipLunar != null) tipExtra = " · " + tipLunar;
        javafx.scene.control.Tooltip.install(cell, new javafx.scene.control.Tooltip(
                date + tipExtra + " · " + dayTodos.size() + " " + t("calendar.todoUnit")));

        // 点击 → 选中该日期
        cell.setOnMouseClicked(event -> {
            selectedDate = date;
            onMonthChanged();
            if (onDateSelected != null) {
                onDateSelected.accept(date.format(DateTimeFormatter.ISO_LOCAL_DATE));
            }
            log.debug("日历选中日期: {}", date);
        });

        cell.getChildren().addAll(dayLabel, subLabel, countRow);
        return cell;
    }

    /** 显示选中日期的待办列表 */
    private void showSelectedDayDetail(LocalDate date) {
        detailList.getChildren().clear();

        String weekday = switch (date.getDayOfWeek()) {
            case MONDAY -> t("calendar.monday"); case TUESDAY -> t("calendar.tuesday"); case WEDNESDAY -> t("calendar.wednesday");
            case THURSDAY -> t("calendar.thursday"); case FRIDAY -> t("calendar.friday"); case SATURDAY -> t("calendar.saturday");
            case SUNDAY -> t("calendar.sunday");
        };
        String extra = "";
        try {
            String fest = LunarCalendarUtil.getFestival(date);
            String lunar = LunarCalendarUtil.getLunarText(date);
            if (fest != null) extra = " " + fest + (lunar != null ? " (" + lunar + ")" : "");
            else if (lunar != null) extra = " " + lunar;
        } catch (Exception ignored) { /* 农历可选 */ }
        detailTitle.setText(date + " " + weekday + extra + " · " + t("calendar.pending") + " "
                + todosByDate.getOrDefault(date, List.of()).size()  + "" + t("calendar.todoUnit"));

        List<Todo> dayTodos = todosByDate.getOrDefault(date, List.of());
        if (dayTodos.isEmpty()) {
            Label empty = new Label(t("calendar.noTodos"));
            empty.setStyle("-fx-font-size:12px; -fx-text-fill:#9CA3AF;");
            detailList.getChildren().add(empty);
            return;
        }

        // 按截止时间排序后逐条展示：颜色点 + 标题 + 状态
        dayTodos.stream()
                .sorted((a, b) -> String.valueOf(a.getDueDate()).compareTo(String.valueOf(b.getDueDate())))
                .forEach(t -> {
                    Region dot = new Region();
                    dot.setMinSize(8, 8);
                    dot.setPrefSize(8, 8);
                    String hex = (t.getColorHex() != null && !t.getColorHex().isBlank()) ? t.getColorHex() : "#9CA3AF";
                    dot.setStyle("-fx-background-color:" + hex + "; -fx-background-radius:4;");

                    Label title = new Label(t.getTitle() == null ? "" : t.getTitle());
                    title.setWrapText(true);
                    title.setStyle(t.isCompleted()
                            ? "-fx-text-fill:#9CA3AF; -fx-strikethrough:true;"
                            : "-fx-text-fill:#1F2937;");

                    Label state = new Label(t.isCompleted() ? I18n.t("calendar.completed") : I18n.t("calendar.pending"));
                    state.setStyle("-fx-font-size:11px; -fx-text-fill:" + (t.isCompleted() ? "#10B981" : "#F59E0B") + ";");

                    HBox row = new HBox(8, dot, title, state);
                    row.setAlignment(Pos.CENTER_LEFT);
                    HBox.setHgrow(title, Priority.ALWAYS);
                    row.setStyle("-fx-padding:4 6; -fx-background-color:#F9FAFB; -fx-background-radius:6;");
                    detailList.getChildren().add(row);
                });
    }

    /** 上/下月导航小按钮 */
    private Button makeNavButton(String text) {
        Button b = new Button(text);
        b.setPrefSize(28, 28);
        b.setMinSize(28, 28);
        b.setStyle("-fx-background-color:#F3F4F6; -fx-background-radius:6; -fx-text-fill:#374151; "
                + "-fx-font-size:14px; -fx-cursor:hand;");
        return b;
    }

    /** 宽松解析日期字符串（兼容 dao 中多种格式），失败返回 null */
    private LocalDate parseDate(String s) {
        if (s == null || s.isBlank()) return null;
        String v = s.trim();
        try {
            if (v.length() >= 10) return LocalDate.parse(v.substring(0, 10));
        } catch (Exception ignored) {
            log.debug("无法解析日期: {}", v);
        }
        return null;
    }
}
