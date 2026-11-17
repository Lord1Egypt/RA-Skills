package com.teamtodo.controller;

import com.teamtodo.model.Todo;
import com.teamtodo.model.User;
import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.service.TodoService;
import com.teamtodo.service.UserService;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextInputDialog;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import static com.teamtodo.util.I18n.t;

/**
 * 左侧待办列表控制器：筛选 + 列表展示 + 新建。
 */
public class TodoListController {
    private static final Logger log = LoggerFactory.getLogger(TodoListController.class);

    /** 筛选模式 */
    private enum Filter { ALL, MINE, TODAY, DONE }

    /** 自定义单元格固定宽度 */
    private static final double CELL_WIDTH = 360;

    @FXML private Button btnAll;
    @FXML private Button btnMine;
    @FXML private Button btnToday;
    @FXML private Button btnDone;
    @FXML private ListView<Todo> todoListView;
    @FXML private Button btnCreate;
    @FXML private Button btnDelete;
    @FXML private Label countLabel;

    private final TodoService todoService = new TodoService();
    private final UserService userService = new UserService();
    private final ObservableList<Todo> items = FXCollections.observableArrayList();
    private Filter currentFilter = Filter.ALL;
    private String currentUserId; // 当前登录用户（简单版默认第一个用户）

    private Consumer<Todo> onSelectedChanged;
    private Runnable onDataChanged;

    @FXML
    private void initialize() {
        todoListView.setItems(items);

        // 多语言：语言切换时刷新文字
        com.teamtodo.util.I18n.onLangChange(lang -> javafx.application.Platform.runLater(this::updateTexts));
        updateTexts();

        // 自定义单元格：标题 + 状态标签 + 负责人 + 截止日期
        todoListView.setCellFactory(list -> new javafx.scene.control.ListCell<>() {
            @Override
            protected void updateItem(Todo todo, boolean empty) {
                super.updateItem(todo, empty);
                if (empty || todo == null) {
                    setText(null);
                    setGraphic(null);
                    setStyle("");
                    return;
                }
                Label title = new Label(todo.getTitle() == null ? "" : todo.getTitle());
                title.getStyleClass().add("todo-item-title");

                TodoStatus st = todo.getStatus() != null ? todo.getStatus() : TodoStatus.PENDING;
                Label statusTag = new Label(statusText(st));
                statusTag.getStyleClass().addAll("tag", "status-" + st.name().toLowerCase());

                String assignee = resolveAssignee(todo.getAssigneeId());
                Label assigneeLabel = new Label("👤 " + (assignee == null ? t("common.unassigned") : assignee));
                assigneeLabel.getStyleClass().add("todo-item-assignee");

                String due = todo.getDueDate();
                Label dueLabel = new Label(due != null && due.length() >= 10 ? "⏰ " + due.substring(0, 10) : (due != null ? "⏰ " + due : ""));
                dueLabel.getStyleClass().add("todo-item-due");

                VBox box = new VBox(2, title, new HBox(8, statusTag, assigneeLabel, dueLabel));
                box.setPrefWidth(CELL_WIDTH);
                setStyle(st == TodoStatus.DONE ? "-fx-text-fill:#888;" : "");
                setGraphic(box);
            }
        });

        // 点击选中 → 通知主控制器
        todoListView.getSelectionModel().selectedItemProperty().addListener(
                (obs, oldV, newV) -> {
                    if (onSelectedChanged != null && newV != null) {
                        onSelectedChanged.accept(newV);
                    }
                });

        refresh();
    }

    /** 状态枚举 → 中文文案 */
    private String statusText(TodoStatus s) {
        return switch (s) {
            case PENDING -> t("status.pending");
            case IN_PROGRESS -> t("status.inProgress");
            case DONE -> t("status.done");
            case CANCELLED -> t("status.cancelled");
        };
    }

    /** 负责人 ID → 用户名 */
    private String resolveAssignee(String assigneeId) {
        if (assigneeId == null) return null;
        for (User u : userService.listAll()) {
            if (u.getId().equals(assigneeId)) return u.getName();
        }
        return null;
    }

    /** 按当前筛选模式刷新列表 */
    public void refresh() {
        items.clear();
        List<Todo> all = todoService.listAll();
        List<Todo> filtered = switch (currentFilter) {
            case ALL -> all;
            case MINE -> currentUserId == null ? all :
                    all.stream().filter(t -> currentUserId.equals(t.getAssigneeId())).collect(Collectors.toList());
            case TODAY -> {
                String today = LocalDate.now().toString();
                yield all.stream().filter(t -> t.getDueDate() != null && t.getDueDate().startsWith(today)).collect(Collectors.toList());
            }
            case DONE -> all.stream().filter(t -> t.getStatus() == TodoStatus.DONE).collect(Collectors.toList());
        };
        items.setAll(filtered);
        if (countLabel != null) {
            countLabel.setText(filtered.size() + " " + t("common.items"));
        }
        log.debug("列表刷新: filter={}, count={}", currentFilter, filtered.size());
    }

    /** 切换筛选 */
    @FXML
    private void filterAll() { setFilter(Filter.ALL); }

    @FXML
    private void filterMine() { setFilter(Filter.MINE); }

    @FXML
    private void filterToday() { setFilter(Filter.TODAY); }

    @FXML
    private void filterDone() { setFilter(Filter.DONE); }

    private void setFilter(Filter f) {
        currentFilter = f;
        updateFilterButtons();
        refresh();
    }

    /** 高亮当前筛选按钮 */
    private void updateFilterButtons() {
        setBtnClass(btnAll, currentFilter == Filter.ALL);
        setBtnClass(btnMine, currentFilter == Filter.MINE);
        setBtnClass(btnToday, currentFilter == Filter.TODAY);
        setBtnClass(btnDone, currentFilter == Filter.DONE);
    }

    private void setBtnClass(Button b, boolean active) {
        if (b == null) return;
        b.getStyleClass().removeAll("filter-btn", "filter-btn-active");
        b.getStyleClass().add("filter-btn");
        if (active) b.getStyleClass().add("filter-btn-active");
    }

    /** 新建待办：弹窗输入标题（负责人默认当前用户） */
    @FXML
    private void createTodo() {
        TextInputDialog dialog = new TextInputDialog(t("newTodo.titleHint"));
        dialog.setHeaderText(t("newTodo.title"));
        List<User> users = userService.listAll();
        if (users.isEmpty()) {
            currentUserId = null;
        } else {
            // 简单版：默认使用第一个用户作为"我"
            if (currentUserId == null) currentUserId = users.get(0).getId();
        }
        dialog.showAndWait().ifPresent(title -> {
            if (title.isBlank()) {
                log.info("标题为空，取消新建");
                return;
            }
            try {
                Todo created = todoService.create(title, null, currentUserId, null);
                log.info("已新建待办: {}", created.getTitle());
                refresh();
                if (onDataChanged != null) onDataChanged.run();
            } catch (IllegalArgumentException e) {
                log.warn("新建失败: {}", e.getMessage());
                dialog.setContentText(t("newTodo.errTitle"));
            }
        });
    }

    /** 删除选中项 */
    @FXML
    private void deleteSelected() {
        Todo sel = todoListView.getSelectionModel().getSelectedItem();
        if (sel == null) return;
        todoService.delete(sel.getId());
        log.info("已删除待办: {}", sel.getTitle());
        refresh();
        if (onDataChanged != null) onDataChanged.run();
    }

    /** i18n：刷新筛选按钮、底部按钮与列表文字 */
    private void updateTexts() {
        if (btnAll != null) btnAll.textProperty().bind(com.teamtodo.util.I18n.text("filter.all"));
        if (btnMine != null) btnMine.textProperty().bind(com.teamtodo.util.I18n.text("todoList.mine"));
        if (btnToday != null) btnToday.textProperty().bind(com.teamtodo.util.I18n.text("calendar.today"));
        if (btnDone != null) btnDone.textProperty().bind(com.teamtodo.util.I18n.text("filter.done"));
        if (btnCreate != null) btnCreate.textProperty().bind(com.teamtodo.util.I18n.text("todoList.create"));
        if (btnDelete != null) btnDelete.textProperty().bind(com.teamtodo.util.I18n.text("shortcut.delete"));
        refresh();
    }

    // ---- 事件回调（由 MainController 注入） ----

    public void setOnSelectedChanged(Consumer<Todo> c) { this.onSelectedChanged = c; }
    public void setOnDataChanged(Runnable r) { this.onDataChanged = r; }
}
