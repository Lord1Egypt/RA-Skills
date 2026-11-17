package com.teamtodo.controller;

import com.teamtodo.model.Todo;
import com.teamtodo.model.enums.TodoPriority;
import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.service.ColorTagService;
import com.teamtodo.service.TodoService;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.Region;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.Parent;
import javafx.scene.input.MouseEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import static com.teamtodo.util.I18n.t;
import com.teamtodo.util.I18n;

/**
 * 看板视图控制器（纯 JavaFX 代码构建，不使用 FXML）。
 *
 * 布局：
 * - 4 列：待办、进行中、已完成、已取消，整体用 HBox 横向排列
 * - 每列是一个 VBox：标题（状态名 + 数量）+ 卡片列表 + 底部"添加"按钮
 * - 卡片显示：颜色点、标题、优先级标签、截止日期，可点击选中（高亮）
 *
 * 数据：TodoService（待办列表）+ ColorTagService（颜色点）。
 */
public class KanbanController {
    private static final Logger log = LoggerFactory.getLogger(KanbanController.class);

    /** 四列固定顺序 */
    private static final TodoStatus[] COLUMNS = {
            TodoStatus.IN_PROGRESS,
            TodoStatus.PENDING,
            TodoStatus.CANCELLED,
            TodoStatus.DONE
    };

    private final TodoService todoService = new TodoService();
    private final ColorTagService colorTagService = new ColorTagService();

    /** 卡片点击回调（由主界面注入，可为 null） */
    private Consumer<Todo> onCardSelected;

    /** 添加回调（由主界面注入，可为 null） */
    private Runnable onAddRequested;

    /** 所有列容器（refresh 时重建内容） */
    private final List<VBox> columns = new ArrayList<>();

    /** 当前选中卡片 id（用于高亮） */
    private String selectedId;

    private BorderPane root;

    /** 外部注入点击/添加回调 */
    public void setOnCardSelected(Consumer<Todo> cb) { this.onCardSelected = cb; }
    public void setOnAddRequested(Runnable r) { this.onAddRequested = r; }

    /** 刷新看板数据（外部数据变化后调用） */
    public void refresh() {
        for (int i = 0; i < COLUMNS.length && i < columns.size(); i++) {
            rebuildColumn(columns.get(i), COLUMNS[i]);
        }
    }

    /** 选中某张卡片（外部导航时调用） */
    public void selectTodo(String todoId) {
        this.selectedId = todoId;
        for (VBox col : columns) {
            // 高亮更新：简单做法——直接重建各列（数据量小，可接受）
        }
        for (int i = 0; i < columns.size(); i++) {
            rebuildColumn(columns.get(i), COLUMNS[i]);
        }
    }

    /**
     * 构建并返回看板视图（Parent 节点），供主界面 setContent 使用。
     */
    public Parent getView() {
        if (root == null) {
            root = buildView();
        }
        refresh();
        return root;
    }

    // ==================== 构建逻辑 ====================

    private BorderPane buildView() {
        BorderPane root = new BorderPane();
        root.getStyleClass().add("kanban-root");
        root.setPadding(new Insets(12));

        HBox board = new HBox(12);
        board.getStyleClass().add("kanban-board");
        board.setPrefWidth(Region.USE_COMPUTED_SIZE);
        board.setMaxWidth(Double.MAX_VALUE);

        for (TodoStatus status : COLUMNS) {
            VBox column = buildColumn(status);
            HBox.setHgrow(column, Priority.ALWAYS);
            columns.add(column);
            board.getChildren().add(column);
        }

        root.setCenter(board);
        return root;
    }

    /** 构建单列：标题 + 卡片容器 + 添加按钮 */
    private VBox buildColumn(TodoStatus status) {
        VBox column = new VBox(8);
        column.getStyleClass().addAll("kanban-column", "kanban-column-" + status.name().toLowerCase());
        column.setPadding(new Insets(10));
        column.setMinWidth(200);
        column.setMaxWidth(480);
        VBox.setVgrow(column, Priority.NEVER);

        // —— 列标题：状态名 + 数量（数量用 Label，refresh 时更新）——
        Label count = new Label("0");
        count.setId("kanban-count-" + status.name());
        count.getStyleClass().add("kanban-count-badge");
        Label title = new Label(status.getLabel());
        title.getStyleClass().add("kanban-column-title");
        title.setFont(Font.font("Microsoft YaHei", FontWeight.BOLD, 14));
        HBox header = new HBox(6, title, count);
        header.getStyleClass().add("kanban-column-header");

        // —— 卡片滚动区 ——
        VBox cardArea = new VBox(8);
        cardArea.setId("kanban-cards-" + status.name());
        cardArea.getStyleClass().add("kanban-card-area");
        VBox.setVgrow(cardArea, Priority.ALWAYS);

        // —— 底部添加按钮 ——
        Button addBtn = new Button(t("kanban.add"));
        addBtn.getStyleClass().addAll("btn", "btn-add", "kanban-add-btn");
        addBtn.setMaxWidth(Double.MAX_VALUE);
        addBtn.setOnAction(e -> {
            if (onAddRequested != null) {
                onAddRequested.run();
            } else {
                log.info("看板添加按钮被点击（状态={}），主界面未注入添加回调", status.getLabel());
            }
        });

        column.getChildren().addAll(header, cardArea, addBtn);
        return column;
    }

    /** 重建某列的卡片内容与数量 */
    private void rebuildColumn(VBox column, TodoStatus status) {
        // 找到卡片区
        javafx.scene.Node cardArea = column.lookup("#kanban-cards-" + status.name());
        if (!(cardArea instanceof VBox vbox)) return;
        vbox.getChildren().clear();

        List<Todo> todos = safeListByStatus(status);

        // 排序：待办→限期升序，进行中→优先级降序，已逾期→逾期时间降序，已完成→截止日期降序
        todos.sort((a, b) -> {
            switch (status) {
                case PENDING -> {
                    String da = a.getDueDate(), db = b.getDueDate();
                    if (da == null && db == null) return 0;
                    if (da == null) return 1;
                    if (db == null) return -1;
                    return da.compareTo(db);
                }
                case IN_PROGRESS -> {
                    int pa = a.getPriority() == null ? 1 : a.getPriority().ordinal();
                    int pb = b.getPriority() == null ? 1 : b.getPriority().ordinal();
                    return Integer.compare(pb, pa); // 高优先级在前
                }
                case CANCELLED -> {
                    // 逾期：按逾期天数降序（越久越前）
                    int oa = daysUntilDue(a), ob = daysUntilDue(b);
                    return Integer.compare(oa, ob); // 负数=逾期更久
                }
                case DONE -> {
                    String da = a.getDueDate(), db = b.getDueDate();
                    if (da == null && db == null) return 0;
                    if (da == null) return 1;
                    if (db == null) return -1;
                    return db.compareTo(da); // 完成的按截止日期降序
                }
            }
            return 0;
        });

        // 更新数量徽标
        Label count = (Label) column.lookup("#kanban-count-" + status.name());
        if (count != null) {
            count.setText(String.valueOf(todos.size()));
        }

        if (todos.isEmpty()) {
            Label empty = new Label(t("kanban.empty"));
            empty.getStyleClass().add("kanban-empty");
            empty.setPadding(new Insets(12, 0, 12, 0));
            vbox.getChildren().add(empty);
            return;
        }

        for (Todo todo : todos) {
            vbox.getChildren().add(buildCard(todo));
        }
    }

    /** 数据源查询（容错：DB 异常时返回空列表而不是抛异常打断 UI） */
    private List<Todo> safeListByStatus(TodoStatus status) {
        try {
            if (status == TodoStatus.CANCELLED) {
                // CANCELLED 列实际显示已逾期任务
                return todoService.listOverdue();
            }
            return todoService.listByStatus(status);
        } catch (Exception ex) {
            log.warn("查询状态[{}]的待办失败：{}", status.getLabel(), ex.getMessage());
            return List.of();
        }
    }

    /**
     * 构建单张卡片：颜色点 + 标题 + 优先级标签 + 截止日期，可点击选中。
     */
    private VBox buildCard(Todo todo) {
        String hex = todo.getColorHex() != null ? todo.getColorHex() : colorTagService.calculateHex(todo);
        Color dotColor = Color.web(hex);

        // 颜色点（动态反色描边）
        Circle dot = new Circle(6, dotColor);
        dot.setPickOnBounds(false);
        double brightness = dotColor.getRed() * 0.299 + dotColor.getGreen() * 0.587 + dotColor.getBlue() * 0.114;
        dot.setStroke(brightness > 0.5 ? Color.color(0x37/255.0, 0x41/255.0, 0x51/255.0, 1) : Color.color(1,1,1,1));
        dot.setStrokeWidth(1);

        // 标题
        Label titleLabel = new Label(todo.getTitle() == null ? "" : todo.getTitle());
        titleLabel.getStyleClass().add("kanban-card-title");
        titleLabel.setFont(Font.font("Microsoft YaHei", 13));

        // 优先级标签（带彩色背景）
        TodoPriority priority = todo.getPriority() == null ? TodoPriority.MEDIUM : todo.getPriority();
        String prioColor = switch (priority) {
            case URGENT -> "#EF4444"; case HIGH -> "#EAB308"; case MEDIUM -> "#22C55E"; case LOW -> "#6B7280";
        };
        Label priorityTag = new Label(priority.getLabel());
        priorityTag.setStyle("-fx-font-size:10px; -fx-text-fill:white; -fx-background-color:" + prioColor + "; -fx-padding:1 5; -fx-background-radius:3;");

        String due = todo.getDueDate();
        int daysLeft = daysUntilDue(todo);
        String dueText;
        if (due == null) {
            dueText = t("kanban.noDue");
        } else if (daysLeft < 0) {
            dueText = "⏰ " + due.substring(0, Math.min(10, due.length())) + " " + String.format(t("kanban.overdue"), -daysLeft);
        } else if (daysLeft == 0) {
            dueText = "⏰ " + due.substring(0, Math.min(10, due.length())) + " " + t("kanban.today");
        } else {
            dueText = "⏰ " + due.substring(0, Math.min(10, due.length())) + " " + String.format(t("kanban.left"), daysLeft);
        }
        Label dueLabel = new Label(dueText);
        dueLabel.getStyleClass().add("kanban-card-due");
        dueLabel.setStyle("-fx-text-fill:" + getCountdownColor(daysLeft) + ";");

        HBox metaRow = new HBox(8, priorityTag, dueLabel);
        metaRow.getStyleClass().add("kanban-card-meta");

        VBox card = new VBox(4, dot, titleLabel, metaRow);
        card.getStyleClass().addAll("kanban-card");
        if (todo.getId() != null && todo.getId().equals(selectedId)) {
            card.getStyleClass().add("kanban-card-selected"); // 选中高亮
        }
        card.setPadding(new Insets(10));
        card.setMouseTransparent(false);
        card.setCursor(javafx.scene.Cursor.HAND);

        // 点击选中
        card.setOnMouseClicked(e -> {
            if (e.getButton() == javafx.scene.input.MouseButton.PRIMARY) {
                selectedId = todo.getId();
                refresh(); // 重建以刷新高亮
                if (onCardSelected != null) {
                    onCardSelected.accept(todo);
                }
            }
        });

        // hover 反馈
        card.setOnMouseEntered(e -> {
            if (!card.getStyleClass().contains("kanban-card-selected")) {
                card.getStyleClass().add("kanban-card-hover");
            }
        });
        card.setOnMouseExited(e -> card.getStyleClass().remove("kanban-card-hover"));

        return card;
    }

    /** 计算距截止日期的天数（负数=已逾期） */
    private int daysUntilDue(Todo todo) {
        if (todo.getDueDate() == null || todo.getDueDate().isBlank()) return Integer.MAX_VALUE;
        try {
            String d = todo.getDueDate();
            if (d.length() >= 10) d = d.substring(0, 10);
            java.time.LocalDate due = java.time.LocalDate.parse(d);
            return (int) java.time.temporal.ChronoUnit.DAYS.between(java.time.LocalDate.now(), due);
        } catch (Exception e) {
            return Integer.MAX_VALUE;
        }
    }

    /** 根据剩余天数返回颜色 */
    private String getCountdownColor(int daysLeft) {
        if (daysLeft < 0) return "#EF4444";
        if (daysLeft <= 1) return "#EF4444";
        if (daysLeft <= 3) return "#F59E0B";
        if (daysLeft <= 7) return "#22C55E";
        if (daysLeft <= 14) return "#3B82F6";
        if (daysLeft <= 30) return "#A855F7";
        return "#4B5563";
    }
}
