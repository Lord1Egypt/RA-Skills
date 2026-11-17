package com.teamtodo.controller;

import com.teamtodo.App;
import com.teamtodo.api.ApiServer;
import com.teamtodo.model.Todo;
import com.teamtodo.util.I18n;
import static com.teamtodo.util.I18n.t;
import com.teamtodo.model.enums.TodoPriority;
import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.model.User;
import com.teamtodo.service.TodoService;
import com.teamtodo.service.UserService;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.input.MouseButton;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Region;
import javafx.scene.layout.VBox;
import javafx.stage.Modality;
import javafx.stage.Stage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

/**
 * 主窗口控制器：左侧导航 + 主内容区 + 右侧详情 + 顶栏
 */
public class MainController {
    private static final Logger log = LoggerFactory.getLogger(MainController.class);

    // 顶栏
    @FXML private TextField searchField;
    @FXML private Button btnMiniWindow;
    @FXML private Button btnNewTop;
    @FXML private Label appTitleLabel;

    // 左侧导航
    @FXML private Button navDashboard;
    @FXML private Button navMyTasks;
    @FXML private Button navCalendar;
    @FXML private Button navStats;
    @FXML private Button navSettings;
    @FXML private Button navAbout;
    @FXML private VBox statsSubMenu;
    @FXML private Button filterAll;
    @FXML private Button filterInProgress;
    @FXML private Button filterOverdue;
    @FXML private Button filterDone;
    @FXML private Button filterPending;
    @FXML private Button btnToggleSidebar;
    @FXML private VBox sidebarBox;
    @FXML private VBox sidebarContent;
    private boolean sidebarExpanded = true;

    // 主内容区
    @FXML private Label viewTitle;
    @FXML private ToggleButton viewList;
    @FXML private ToggleButton viewKanban;
    @FXML private ListView<Todo> todoListView;
    @FXML private javafx.scene.layout.StackPane contentPane;

    // 状态栏
    @FXML private Label statusLabel;
    @FXML private Label statsLabel;

    // 右侧详情已移除，改为双击弹窗

    private final TodoService todoService = new TodoService();
    private final UserService userService = new UserService();
    private final ObservableList<Todo> items = FXCollections.observableArrayList();

    private enum Filter { ALL, IN_PROGRESS, OVERDUE, PENDING, DONE }
    private Filter currentFilter = Filter.ALL;
    private KanbanController kanbanController;
    private Parent calendarView;
    private Parent statsView;
    private Parent settingsView;
    private Parent dashboardView;
    private Parent aboutView;
    private String activeView = "list"; // list | kanban | calendar | stats | settings | dashboard
    private static final double SIDEBAR_WIDTH = 172;

    // 7 色循环：进行中=绿，待办=黄，逾期=红，完成=灰
    private static final String[] GREENS = {"#22C55E", "#16A34A", "#15803D", "#4ADE80", "#86EFAC", "#166534", "#BBF7D0"};
    private static final String[] YELLOWS = {"#EAB308", "#CA8A04", "#FACC15", "#FDE047", "#FCD34D", "#A16207", "#FEF08A"};
    private static final String[] REDS = {"#EF4444", "#DC2626", "#F87171", "#B91C1C", "#FCA5A5", "#991B1B", "#FECACA"};
    private static final String[] GRAYS = {"#9CA3AF", "#6B7280", "#D1D5DB", "#4B5563", "#E5E7EB", "#374151", "#F3F4F6"};
    private static final double SIDEBAR_COLLAPSED = 36;

    @FXML
    private void initialize() {
        log.info("MainController.initialize() 被调用");
        todoListView.setItems(items);

        // 初始化多语言
        com.teamtodo.util.I18n.init();
        com.teamtodo.util.I18n.onLangChange(lang -> Platform.runLater(this::updateAllTexts));
        updateAllTexts();

        // 统计子菜单默认展开
        statsSubMenu.setVisible(true);
        statsSubMenu.setManaged(true);

        // 自定义单元格
        todoListView.setCellFactory(list -> new ListCell<>() {
            @Override
            protected void updateItem(Todo todo, boolean empty) {
                super.updateItem(todo, empty);
                if (empty || todo == null) {
                    setText(null);
                    setGraphic(null);
                    return;
                }

                Region colorDot = new Region();
                colorDot.setMinSize(12, 12);
                colorDot.setPrefSize(12, 12);
                String hex = todo.getColorHex() != null ? todo.getColorHex() : "#9CA3AF";
                // 动态反色描边：亮度>0.5用深色描边否则白色，1px细线
                String borderColor = "#FFFFFF";
                try {
                    javafx.scene.paint.Color c = javafx.scene.paint.Color.web(hex);
                    double brightness = c.getRed() * 0.299 + c.getGreen() * 0.587 + c.getBlue() * 0.114;
                    borderColor = brightness > 0.5 ? "#374151" : "#FFFFFF";
                } catch (Exception ignored) {}
                colorDot.setStyle("-fx-background-color:" + hex + "; -fx-background-radius:4; -fx-border-color:" + borderColor + "; -fx-border-radius:4; -fx-border-width:1;");

                Label title = new Label(todo.getTitle() != null ? todo.getTitle() : "");
                title.setStyle(todo.isCompleted() ? "-fx-text-fill:#9CA3AF; -fx-strikethrough:true;" : "-fx-text-fill:#1F2937;");
                HBox.setHgrow(title, javafx.scene.layout.Priority.ALWAYS);

                Label statusTag = new Label(todo.getStatus().getLabel());
                statusTag.setStyle("-fx-font-size:11px; -fx-text-fill:white; -fx-background-color:" + getStatusTagColor(todo.getStatus()) + "; -fx-padding:2 6; -fx-background-radius:3;");

                Label dueLabel = new Label(todo.getDueDate() != null ? todo.getDueDate() : "");
                dueLabel.setStyle("-fx-font-size:11px; -fx-text-fill:#6B7280;");

                // 优先级标签
                TodoPriority prio = todo.getPriority() == null ? TodoPriority.MEDIUM : todo.getPriority();
                String prioColor = switch (prio) {
                    case URGENT -> "#EF4444"; case HIGH -> "#EAB308"; case MEDIUM -> "#22C55E"; case LOW -> "#6B7280";
                };
                Label prioLabel = new Label(prio.getLabel());
                prioLabel.setStyle("-fx-font-size:10px; -fx-text-fill:white; -fx-background-color:" + prioColor + "; -fx-padding:1 5; -fx-background-radius:3;");

                // 限期倒计时
                int daysLeft = daysUntilDue(todo);
                String countdown = "";
                String countdownColor = "#6B7280";
                if (todo.getDueDate() != null && !todo.getDueDate().isBlank()) {
                    countdownColor = getCountdownColor(daysLeft);
                    if (daysLeft < 0) {
                        countdown = String.format(t("countdown.overdue"), -daysLeft);
                    } else if (daysLeft == 0) {
                        countdown = t("countdown.today");
                    } else {
                        countdown = String.format(t("countdown.left"), daysLeft);
                    }
                }
                Label countdownLabel = new Label(countdown);
                countdownLabel.setStyle("-fx-font-size:11px; -fx-font-weight:bold; -fx-text-fill:" + countdownColor + ";");

                // 认领/认领人
                javafx.scene.Node claimBtn;
                if (todo.getAssigneeId() != null && !todo.getAssigneeId().isBlank()) {
                    // 已认领 → 显示认领人名字
                    String assigneeName = t("claim.assigned");
                    try {
                        var u = userService.findById(todo.getAssigneeId());
                        if (u != null) assigneeName = u.getName();
                    } catch (Exception ignored) {}
                    Label assigneeLabel = new Label("👤 " + assigneeName);
                    assigneeLabel.setStyle("-fx-font-size:11px; -fx-text-fill:#4F6BF6; -fx-padding:2 6; -fx-background-color:#EEF2FF; -fx-background-radius:3;");
                    claimBtn = assigneeLabel;
                } else {
                    // 未认领 → 显示认领按钮
                    Button claim = new Button(t("claim.btn"));
                    claim.setStyle("-fx-font-size:11px; -fx-text-fill:white; -fx-background-color:#4F6BF6; -fx-padding:3 10; -fx-background-radius:4; -fx-cursor:hand; -fx-effect: dropshadow(gaussian, rgba(79,107,246,0.3), 3, 0, 0, 1);");
                    claim.setOnAction(e -> {
                        // 弹出选择用户的对话框
                        List<User> users = userService.listAll();
                        if (users.isEmpty()) {
                            // 没有用户，先创建一个
                            javafx.scene.control.TextInputDialog nameDlg = new javafx.scene.control.TextInputDialog();
                            nameDlg.setTitle(t("claim.title"));
                            nameDlg.setHeaderText(t("claim.inputName"));
                            nameDlg.setContentText(t("claim.name"));
                            nameDlg.showAndWait().ifPresent(name -> {
                                if (!name.isBlank()) {
                                    User u = userService.upsert(name, null);
                                    todo.setAssigneeId(u.getId());
                                    todo.setStatus(com.teamtodo.model.enums.TodoStatus.IN_PROGRESS);
                                    todo.setUpdatedAt(java.time.LocalDateTime.now());
                                    todoService.update(todo);
                                    refreshAll();
                                }
                            });
                        } else {
                            // 有用户，弹出选择
                            javafx.scene.control.ChoiceDialog<User> dlg = new javafx.scene.control.ChoiceDialog<>(users.get(0), users);
                            dlg.setTitle(t("claim.title"));
                            dlg.setHeaderText(t("claim.select"));
                            dlg.setContentText(t("claim.assignee"));
                            dlg.showAndWait().ifPresent(user -> {
                                todo.setAssigneeId(user.getId());
                                todo.setStatus(com.teamtodo.model.enums.TodoStatus.IN_PROGRESS);
                                todo.setUpdatedAt(java.time.LocalDateTime.now());
                                todoService.update(todo);
                                refreshAll();
                            });
                        }
                    });
                    claimBtn = claim;
                }

                // 勾选框（色块后）
                javafx.scene.control.CheckBox doneCheck = new javafx.scene.control.CheckBox();
                doneCheck.setSelected(todo.isCompleted());
                doneCheck.setStyle("-fx-padding:0 0 0 0;");
                doneCheck.selectedProperty().addListener((obs, old, now) -> {
                    if (now != todo.isCompleted()) {
                        todoService.toggleComplete(todo.getId());
                        refreshAll();
                    }
                });

                HBox row = new HBox(10, colorDot, doneCheck, title, statusTag, prioLabel, claimBtn, dueLabel, countdownLabel);
                row.setAlignment(javafx.geometry.Pos.CENTER_LEFT);
                row.setStyle("-fx-alignment:CENTER_LEFT; -fx-padding:2 0;");

                setGraphic(row);
            }
        });

        // 双击任务 → 弹窗详情
        todoListView.setOnMouseClicked(event -> {
            if (event.getButton() == MouseButton.PRIMARY && event.getClickCount() == 2) {
                Todo selected = todoListView.getSelectionModel().getSelectedItem();
                if (selected != null) {
                    openTodoDetailPopup(selected);
                }
            }
        });

        // 单击也更新状态栏
        todoListView.getSelectionModel().selectedItemProperty().addListener((obs, old, todo) -> {
            if (todo != null) {
                statusLabel.setText(String.format(t("status.current"), todo.getTitle()));
            }
        });

        // API 写操作后自动刷新 UI
        com.teamtodo.App.setOnRefresh(this::refreshAll);

        refreshList();
        refreshStats();
    }

    private String getStatusColor(TodoStatus status, int index) {
        String[] palette = switch (status) {
            case IN_PROGRESS -> GREENS;
            case PENDING -> YELLOWS;
            case CANCELLED -> REDS;
            case DONE -> GRAYS;
        };
        return palette[Math.floorMod(index, palette.length)];
    }

    /** 状态标签固定颜色（不循环） */
    private String getStatusTagColor(TodoStatus status) {
        return switch (status) {
            case IN_PROGRESS -> "#22C55E";
            case PENDING -> "#EAB308";
            case CANCELLED -> "#EF4444";
            case DONE -> "#9CA3AF";
        };
    }

    private void refreshList() {
        items.clear();
        List<Todo> todos = switch (currentFilter) {
            case ALL -> todoService.listAll();
            case IN_PROGRESS -> todoService.listByStatus(TodoStatus.IN_PROGRESS);
            case OVERDUE -> todoService.listOverdue();
            case DONE -> todoService.listByStatus(TodoStatus.DONE);
            case PENDING -> todoService.listByStatus(TodoStatus.PENDING);
        };
        // 排序：进行中→优先级，待办→限期升序，已逾期→逾期时间，已完成→截止日期
        todos.sort((a, b) -> {
            TodoStatus sa = a.getStatus(), sb = b.getStatus();
            // 先按状态分组
            int statusOrder = statusOrder(sa) - statusOrder(sb);
            if (statusOrder != 0) return statusOrder;
            // 同状态内按各自规则排序
            if (sa == TodoStatus.IN_PROGRESS) {
                int pa = a.getPriority() == null ? 1 : a.getPriority().ordinal();
                int pb = b.getPriority() == null ? 1 : b.getPriority().ordinal();
                return Integer.compare(pb, pa);
            } else if (sa == TodoStatus.CANCELLED) {
                return Integer.compare(daysUntilDue(a), daysUntilDue(b));
            } else if (sa == TodoStatus.DONE) {
                String da = a.getDueDate(), db = b.getDueDate();
                if (da == null && db == null) return 0;
                if (da == null) return 1; if (db == null) return -1;
                return db.compareTo(da);
            } else {
                // 待办：限期升序
                String da = a.getDueDate(), db = b.getDueDate();
                if (da == null && db == null) return 0;
                if (da == null) return 1; if (db == null) return -1;
                return da.compareTo(db);
            }
        });
        items.setAll(todos);
    }

    /** 状态排序顺序：进行中→待办→已逾期→已完成 */
    private int statusOrder(TodoStatus s) {
        return switch (s) {
            case IN_PROGRESS -> 0;
            case PENDING -> 1;
            case CANCELLED -> 2;
            case DONE -> 3;
        };
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

    /** 根据剩余天数返回颜色：黑/紫/蓝/绿/黄/红 */
    private String getCountdownColor(int daysLeft) {
        if (daysLeft < 0) return "#EF4444";       // 已逾期 → 红
        if (daysLeft <= 1) return "#EF4444";      // 1天内 → 红
        if (daysLeft <= 3) return "#F59E0B";      // 3天内 → 黄
        if (daysLeft <= 7) return "#22C55E";      // 1周内 → 绿
        if (daysLeft <= 14) return "#3B82F6";     // 2周内 → 蓝
        if (daysLeft <= 30) return "#A855F7";     // 1月内 → 紫
        return "#4B5563";                          // 更久 → 中灰（白底/黑底均可见）
    }

    private void refreshStats() {
        int total = todoService.listAll().size();
        int inProgress = todoService.listByStatus(TodoStatus.IN_PROGRESS).size();
        int pending = todoService.listByStatus(TodoStatus.PENDING).size();
        int overdue = todoService.getOverdueCount();
        int done = todoService.listByStatus(TodoStatus.DONE).size();
        int completed = (int) todoService.listAll().stream().filter(Todo::isCompleted).count();

        filterAll.textProperty().unbind();
        filterInProgress.textProperty().unbind();
        filterPending.textProperty().unbind();
        filterOverdue.textProperty().unbind();
        filterDone.textProperty().unbind();

        filterAll.setText("  " + t("filter.all") + " " + total);
        filterInProgress.setText("  " + t("filter.inProgress") + " " + inProgress);
        filterPending.setText("  " + t("filter.pending") + " " + pending);
        filterOverdue.setText("  " + t("filter.overdue") + " " + overdue);
        filterDone.setText("  " + t("filter.done") + " " + done);

        statsLabel.setText(String.format(t("stats.format"), total, completed, overdue));
    }

    // ===== 视图切换 =====
    private void switchView(String view) {
        activeView = view;
        contentPane.getChildren().clear();
        if ("list".equals(view)) {
            viewList.setVisible(true);
            viewList.setManaged(true);
            viewKanban.setVisible(true);
            viewKanban.setManaged(true);
            viewList.setSelected(true);
            viewKanban.setSelected(false);
            contentPane.getChildren().add(todoListView);
        } else if ("kanban".equals(view)) {
            viewList.setVisible(true);
            viewList.setManaged(true);
            viewKanban.setVisible(true);
            viewKanban.setManaged(true);
            viewList.setSelected(false);
            viewKanban.setSelected(true);
            if (kanbanController == null) {
                kanbanController = new KanbanController();
                kanbanController.setOnCardSelected(this::openTodoDetailPopup);
                kanbanController.setOnAddRequested(this::onNewTodo);
            }
            contentPane.getChildren().add(kanbanController.getView());
        } else if ("calendar".equals(view)) {
            viewList.setVisible(false);
            viewList.setManaged(false);
            viewKanban.setVisible(false);
            viewKanban.setManaged(false);
            if (calendarView == null) {
                CalendarController cal = new CalendarController();
                cal.setOnDateSelected(date -> statusLabel.setText(String.format(t("stats.selectedDate"), date)));
                calendarView = cal.getView();
            }
            contentPane.getChildren().add(calendarView);
        } else if ("stats".equals(view)) {
            viewList.setVisible(false);
            viewList.setManaged(false);
            viewKanban.setVisible(false);
            viewKanban.setManaged(false);
            if (statsView == null) statsView = new StatisticsController().getView();
            contentPane.getChildren().add(statsView);
        } else if ("settings".equals(view)) {
            viewList.setVisible(false);
            viewList.setManaged(false);
            viewKanban.setVisible(false);
            viewKanban.setManaged(false);
            if (settingsView == null) {
                try {
                    javafx.fxml.FXMLLoader loader = new javafx.fxml.FXMLLoader(getClass().getResource("/fxml/settings.fxml"));
                    javafx.scene.Parent settingsContent = loader.load();
                    javafx.scene.control.ScrollPane settingsScroll = new javafx.scene.control.ScrollPane(settingsContent);
                    settingsScroll.setFitToWidth(true);
                    settingsScroll.setStyle("-fx-background-color:transparent;");
                    settingsView = settingsScroll;
                } catch (Exception e) {
                    settingsView = new Label(t("settings.loadFailed") + e.getMessage());
                }
            }
            contentPane.getChildren().add(settingsView);
        } else if ("dashboard".equals(view)) {
            viewList.setSelected(false);
            viewKanban.setSelected(false);
            if (dashboardView == null) dashboardView = new DashboardController().getView();
            contentPane.getChildren().add(dashboardView);
        } else if ("about".equals(view)) {
            viewList.setVisible(false);
            viewList.setManaged(false);
            viewKanban.setVisible(false);
            viewKanban.setManaged(false);
            if (aboutView == null) aboutView = buildAboutView();
            contentPane.getChildren().add(aboutView);
        }
        // 刷新
        refreshAll();
    }

    private void refreshAll() {
        refreshList();
        refreshStats();
        if (kanbanController != null && "kanban".equals(activeView)) kanbanController.refresh();
        if (statsView != null && "stats".equals(activeView)) {
            // StatisticsController.refresh 通过内部 root 判断
        }
    }

    // ===== 导航 =====
    @FXML private void onNavDashboard() {
        viewTitle.setText(t("view.title.workbench"));
        setActiveNav(navDashboard);
        switchView("dashboard");
    }
    @FXML private void onNavMyTasks() {
        viewTitle.setText(t("view.title.myTasks"));
        setActiveNav(navMyTasks);
        currentFilter = Filter.ALL;
        switchView("list");
    }
    @FXML private void onNavCalendar() {
        viewTitle.setText(t("view.title.calendar"));
        setActiveNav(navCalendar);
        switchView("calendar");
    }
    @FXML private void onNavStats() {
        viewTitle.setText(t("view.title.stats"));
        setActiveNav(navStats);
        switchView("stats");
    }
    @FXML private void onNavSettings() {
        viewTitle.setText(t("view.title.settings"));
        setActiveNav(navSettings);
        switchView("settings");
    }
    @FXML private void onNavAbout() {
        viewTitle.setText(com.teamtodo.util.I18n.t("view.title.about"));
        setActiveNav(navAbout);
        aboutView = null; // 重建以刷新语言
        switchView("about");
    }

    private void setActiveNav(javafx.scene.control.Button active) {
        setActiveNavs(active);
    }
    private void setActiveNavs(javafx.scene.control.Button... actives) {
        for (javafx.scene.control.Button b : new javafx.scene.control.Button[]{navDashboard, navMyTasks, navCalendar, navStats, navSettings, navAbout, filterAll, filterInProgress, filterOverdue, filterDone, filterPending}) {
            b.getStyleClass().remove("active");
        }
        for (javafx.scene.control.Button active : actives) {
            if (!active.getStyleClass().contains("active")) active.getStyleClass().add("active");
        }
    }

    @FXML private void onViewList() { switchView("list"); }
    @FXML private void onViewKanban() { switchView("kanban"); }

    // ===== 搜索 =====
    @FXML private void onSearchFieldEnter() {
        String kw = searchField.getText() == null ? "" : searchField.getText().trim();
        if (kw.isEmpty()) {
            refreshList();
            refreshStats();
            return;
        }
        // 过滤当前列表
        items.clear();
        List<Todo> all = todoService.listAll();
        items.setAll(all.stream()
                .filter(t -> (t.getTitle() != null && t.getTitle().toLowerCase().contains(kw.toLowerCase()))
                        || (t.getDescription() != null && t.getDescription().toLowerCase().contains(kw.toLowerCase())))
                .toList());
        refreshStats();
        statusLabel.setText(String.format(t("stats.searchResult"), kw, items.size()));
        searchField.clear();
    }

    /** 全局搜索弹窗（Ctrl+K） */
    @FXML private void onGlobalSearch() {
        SearchDialog.show(todo -> {
            if (todo != null) {
                switchView("list");
                // 确保在列表中
                if (!items.contains(todo)) {
                    currentFilter = Filter.ALL;
                    refreshList();
                }
                todoListView.getSelectionModel().select(todo);
                todoListView.scrollTo(todo);
            }
        });
    }

    /** 初始化键盘快捷键（由 App 调用） */
    public void setupKeyboardShortcuts(Scene scene) {
        scene.addEventFilter(javafx.scene.input.KeyEvent.KEY_PRESSED, event -> {
            if (event.isControlDown()) {
                switch (event.getCode()) {
                    case N -> { onNewTodo(); event.consume(); }
                    case K -> { onGlobalSearch(); event.consume(); }
                    case M -> { onToggleMiniWindow(); event.consume(); }
                    default -> {}
                }
            } else {
                switch (event.getCode()) {
                    case DELETE -> {
                        Todo sel = todoListView.getSelectionModel().getSelectedItem();
                        if (sel != null) {
                            todoService.delete(sel.getId());
                            refreshAll();
                        }
                    }
                    case ENTER -> {
                        Todo sel = todoListView.getSelectionModel().getSelectedItem();
                        if (sel != null) {
                            todoService.toggleComplete(sel.getId());
                            refreshAll();
                        }
                    }
                    default -> {}
                }
            }
        });
    }

    // ===== 筛选 =====
    @FXML private void onFilterAll() { currentFilter = Filter.ALL; setActiveNavs(navMyTasks, filterAll); viewTitle.setText(t("view.title.myTasks")); switchView("list"); }
    @FXML private void onFilterInProgress() { currentFilter = Filter.IN_PROGRESS; setActiveNavs(navMyTasks, filterInProgress); viewTitle.setText(t("view.title.inProgress")); switchView("list"); }
    @FXML private void onFilterOverdue() { currentFilter = Filter.OVERDUE; setActiveNavs(navMyTasks, filterOverdue); viewTitle.setText(t("view.title.overdue")); switchView("list"); }
    @FXML private void onFilterDone() { currentFilter = Filter.DONE; setActiveNavs(navMyTasks, filterDone); viewTitle.setText(t("view.title.done")); switchView("list"); }
    @FXML private void onFilterPending() { currentFilter = Filter.PENDING; setActiveNavs(navMyTasks, filterPending); viewTitle.setText(t("view.title.pending")); switchView("list"); }

    // ===== 操作 =====
    @FXML private void onNewTodo() {
        com.teamtodo.controller.NewTodoDialog.show(todoService, userService, created -> {
            if (created != null) {
                switchView("list");
                currentFilter = Filter.ALL;
                refreshAll();
                statusLabel.setText(String.format(t("stats.created"), created.getTitle() != null ? created.getTitle() : ""));
                todoListView.getSelectionModel().select(created);
            }
        });
    }

    @FXML private void onToggleMiniWindow() {
        App.toggleMini();
    }

    @FXML private void onToggleSidebar() {
        sidebarExpanded = !sidebarExpanded;
        double w = sidebarExpanded ? SIDEBAR_WIDTH : SIDEBAR_COLLAPSED;
        sidebarBox.setPrefWidth(w);
        sidebarBox.setMinWidth(w);
        sidebarBox.setMaxWidth(w);
        if (sidebarExpanded) {
            sidebarContent.setVisible(true);
            sidebarContent.setManaged(true);
            btnToggleSidebar.setText("◀");
        } else {
            sidebarContent.setVisible(false);
            sidebarContent.setManaged(false);
            btnToggleSidebar.setText("▶");
        }
    }

    /** 刷新列表（供详情面板调用） */
    public void refresh() {
        Platform.runLater(this::refreshAll);
    }

    /** 打开任务详情弹窗（双击或看板卡片点击）——每一步均有异常保护 */
    private void openTodoDetailPopup(Todo todo) {
        Stage popup = null;
        try {
            if (todo == null) {
                new Alert(Alert.AlertType.INFORMATION, t("detail.selectFirst")).showAndWait();
                return;
            }

            // ① 创建窗口
            popup = new Stage();
            popup.initModality(Modality.APPLICATION_MODAL);
            popup.setTitle(t("detail.titlePrefix") + (todo.getTitle() != null ? todo.getTitle() : ""));
            // 窗口图标（与主窗口一致）
            javafx.scene.image.Image icon = App.loadIcon();
            if (icon != null) popup.getIcons().add(icon);

            // ② 加载 FXML
            java.net.URL fxml = getClass().getResource("/fxml/todo-detail.fxml");
            if (fxml == null) throw new IllegalStateException("todo-detail.fxml not found");
            FXMLLoader loader = new FXMLLoader(fxml);
            Parent root = loader.load();
            TodoDetailController controller = loader.getController();

            // ③ 注入回调 + 填充数据（showTodo 内部已做 null 保护）
            controller.setOnSaved(this::refreshAll);
            controller.showTodo(todo);

            // ④ 场景 + 样式表（内容包裹 ScrollPane 防溢出）
            javafx.scene.control.ScrollPane detailScroll = new javafx.scene.control.ScrollPane(root);
            detailScroll.setFitToWidth(true);
            detailScroll.setFitToHeight(true);
            detailScroll.setStyle("-fx-background-color:transparent;");
            Scene scene = new Scene(detailScroll, 480, 680);
            java.net.URL css = getClass().getResource("/css/style.css");
            if (css != null) {
                try { scene.getStylesheets().add(css.toExternalForm()); } catch (Exception ignored) { }
            }
            popup.setResizable(true);
            popup.setMinWidth(420);
            popup.setMinHeight(420);

            // ⑤ 显示
            popup.show();
        } catch (Exception e) {
            log.error("打开任务详情弹窗失败", e);
            new Alert(Alert.AlertType.ERROR,
                    t("detail.cannotOpen") + (e.getMessage() != null ? e.getMessage() : e.getClass().getSimpleName()))
                    .showAndWait();
            if (popup != null) popup.close();
        }
    }

    /** 刷新所有界面文字（语言切换时调用） */
    private void updateAllTexts() {
        navDashboard.textProperty().bind(I18n.text("nav.workbench"));
        navMyTasks.textProperty().bind(I18n.text("nav.myTasks"));
        navCalendar.textProperty().bind(I18n.text("nav.calendar"));
        navStats.textProperty().bind(I18n.text("nav.stats"));
        navSettings.textProperty().bind(I18n.text("nav.settings"));
        navAbout.textProperty().bind(I18n.text("nav.about"));
        filterAll.textProperty().unbind();
        filterInProgress.textProperty().unbind();
        filterPending.textProperty().unbind();
        filterOverdue.textProperty().unbind();
        filterDone.textProperty().unbind();
        refreshStats(); // 筛选按钮含数量，在 refreshStats 中统一设置
        searchField.promptTextProperty().bind(I18n.text("topbar.searchHint"));
        btnMiniWindow.textProperty().bind(I18n.text("topbar.miniWindow"));
        btnNewTop.textProperty().bind(I18n.text("topbar.new"));
        viewList.textProperty().bind(I18n.text("view.list"));
        viewKanban.textProperty().bind(I18n.text("view.kanban"));
        // viewTitle/statusLabel 用 setText（避免与导航方法的 setText 冲突）
        if ("list".equals(activeView)) {
            String fk = switch (currentFilter) {
                case ALL -> "myTasks";
                case IN_PROGRESS -> "inProgress";
                case PENDING -> "pending";
                case OVERDUE -> "overdue";
                case DONE -> "done";
            };
            viewTitle.setText(t("view.title." + fk));
        } else {
            viewTitle.setText(t("view.title." + activeView));
        }
        statusLabel.setText(t("status.ready"));
        if (appTitleLabel != null) appTitleLabel.textProperty().bind(I18n.text("app.title"));

        // 清空所有缓存视图，强制用新语言重建
        settingsView = null;
        statsView = null;
        calendarView = null;
        dashboardView = null;
        aboutView = null;
        kanbanController = null;

        // 重建当前视图
        switchView(activeView);
        refreshStats();
    }

    /** 关于对话框 */
    private void showAbout() {
        // 已改为内联视图，此方法保留兼容
    }

    /** 构建关于页面（内联，内容可复制） */
    private Parent buildAboutView() {
        int port = ApiServer.getPort();
        StringBuilder sb = new StringBuilder();

        // 标题
        sb.append(com.teamtodo.util.I18n.t("about.title")).append("\n");
        sb.append(com.teamtodo.util.I18n.t("about.subtitle")).append(" ").append(com.teamtodo.util.I18n.t("about.version")).append("\n");
        sb.append(com.teamtodo.util.I18n.t("about.build")).append("\n");
        sb.append("\n");

        // 使用方法
        sb.append(com.teamtodo.util.I18n.t("about.section.usage")).append("\n");
        for (int i = 1; i <= 10; i++) sb.append(com.teamtodo.util.I18n.t("about.usage.line" + i)).append("\n");
        sb.append("\n");

        // 智能体调用
        sb.append(com.teamtodo.util.I18n.t("about.section.agent")).append("\n");
        for (int i = 1; i <= 2; i++) sb.append(com.teamtodo.util.I18n.t("about.agent.line" + i, port)).append("\n");
        sb.append(com.teamtodo.util.I18n.t("about.agent.line3")).append("\n");
        for (int i = 4; i <= 14; i++) sb.append(com.teamtodo.util.I18n.t("about.agent.line" + i)).append("\n");
        sb.append(com.teamtodo.util.I18n.t("about.agent.line15")).append("\n");
        sb.append(com.teamtodo.util.I18n.t("about.agent.line16", port)).append("\n");
        sb.append("\n");

        // 权限说明
        sb.append(com.teamtodo.util.I18n.t("about.section.permissions")).append("\n");
        for (int i = 1; i <= 4; i++) sb.append(com.teamtodo.util.I18n.t("about.perm.line" + i)).append("\n");
        sb.append("\n");

        // 已知问题
        sb.append(com.teamtodo.util.I18n.t("about.section.bugs")).append("\n");
        for (int i = 1; i <= 5; i++) sb.append(com.teamtodo.util.I18n.t("about.bugs.line" + i)).append("\n");
        sb.append("\n");

        // 开发进度
        sb.append(com.teamtodo.util.I18n.t("about.section.progress")).append("\n");
        for (int i = 1; i <= 9; i++) sb.append(com.teamtodo.util.I18n.t("about.progress.line" + i)).append("\n");
        sb.append("\n");

        // 开源说明
        sb.append(com.teamtodo.util.I18n.t("about.section.license")).append("\n");
        for (int i = 1; i <= 12; i++) sb.append(com.teamtodo.util.I18n.t("about.license.line" + i)).append("\n");
        sb.append("\n");

        // 制作人
        sb.append(com.teamtodo.util.I18n.t("about.section.creator")).append("\n");
        sb.append(com.teamtodo.util.I18n.t("about.creator.name")).append("\n");
        sb.append(com.teamtodo.util.I18n.t("about.creator.tech")).append("\n");
        sb.append(com.teamtodo.util.I18n.t("about.copyright")).append("\n");

        // 只读 TextArea，内容可复制
        javafx.scene.control.TextArea textArea = new javafx.scene.control.TextArea(sb.toString());
        textArea.setEditable(false);
        textArea.setWrapText(true);
        textArea.setStyle("-fx-font-family:'Microsoft YaHei','Segoe UI',sans-serif; -fx-font-size:13px; -fx-control-inner-background:#F5F7FA;");
        textArea.prefWidthProperty().bind(new javafx.scene.layout.StackPane().widthProperty());

        javafx.scene.layout.VBox pane = new javafx.scene.layout.VBox(textArea);
        pane.setStyle("-fx-padding:8; -fx-background-color:#F5F7FA;");
        javafx.scene.layout.VBox.setVgrow(textArea, javafx.scene.layout.Priority.ALWAYS);
        return pane;
    }
}
