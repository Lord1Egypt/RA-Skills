package com.teamtodo.controller;

import com.teamtodo.service.ColorTagService;
import com.teamtodo.service.ColorTagService.TodoWithColor;
import com.teamtodo.model.Todo;
import com.teamtodo.model.enums.TodoPriority;
import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.service.TodoService;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.embed.swing.JFXPanel;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.ListCell;
import javafx.scene.control.ListView;
import javafx.scene.layout.Region;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.swing.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.List;
import java.util.function.Consumer;
import com.teamtodo.util.I18n;
import static com.teamtodo.util.I18n.t;

/**
 * 迷你小窗控制器：无标题栏、无任务栏图标的轻量待办窗口。
 * 使用 Swing JFrame（Type.UTILITY + undecorated）+ JFXPanel 实现。
 */
public class MiniFrameController {
    private static final Logger log = LoggerFactory.getLogger(MiniFrameController.class);
    private static final double MIN_WIDTH = 500;
    private static final double COLLAPSED_HEIGHT = 56;

    @FXML private VBox rootPane;
    @FXML private Region colorBlock;
    @FXML private Label titleLabel;
    @FXML private Label dueLabel;
    @FXML private CheckBox completedBox;
    @FXML private Button expandBtn;
    @FXML private Button openMainBtn;
    @FXML private Button hideBtn;
    @FXML private VBox expandPanel;
    @FXML private ListView<TodoWithColor> todoListView;
    @FXML private Label listHint;

    private final TodoService todoService = new TodoService();
    private final ColorTagService colorTagService = new ColorTagService();
    private final ObservableList<TodoWithColor> items = FXCollections.observableArrayList();

    private JFrame swingFrame;  // Swing 容器（无标题栏+无任务栏图标）
    private JFXPanel fxPanel;   // JavaFX 嵌入面板
    private int currentIndex = 0;
    private boolean expanded = false;
    private double dragOffsetX, dragOffsetY;
    private Runnable openMainAction;
    private Consumer<Todo> onTodoChanged;

    private static MiniFrameController instance;

    // ===== 公开 API =====

    public static void show() { show(null); }

    public static void show(Runnable openMainAction) {
        runOnFx(() -> {
            if (instance == null || instance.swingFrame == null || !instance.swingFrame.isVisible()) {
                instance = buildInstance(openMainAction);
            } else {
                if (openMainAction != null) instance.openMainAction = openMainAction;
                instance.swingFrame.setVisible(true);
                instance.swingFrame.toFront();
                // 隐藏期间可能切过语言：重新显示时刷新所有文字
                instance.updateMiniTexts();
                return;
            }
            instance.swingFrame.setVisible(true);
            instance.swingFrame.toFront();
            log.info("迷你小窗已显示");
        });
    }

    public static void hide() {
        if (instance != null && instance.swingFrame != null) {
            Platform.runLater(() -> {
                // 二次检查：排队期间实例可能已被 destroy 置空
                if (instance == null || instance.swingFrame == null) return;
                instance.swingFrame.setVisible(false);
                log.info("迷你小窗已隐藏");
            });
        }
    }

    public static void toggle() {
        if (instance != null && instance.swingFrame != null && instance.swingFrame.isVisible()) {
            hide();
        } else {
            show();
        }
    }

    public static boolean isShowing() {
        return instance != null && instance.swingFrame != null && instance.swingFrame.isVisible();
    }

    /** 语言切换时由 App 调用，刷新小窗所有文字（实例为 null 时安全跳过） */
    public static void updateMiniTextsStatic() {
        if (instance != null) instance.updateMiniTexts();
    }

    public static void destroy() {
        Platform.runLater(() -> {
            if (instance == null) return;
            if (instance.swingFrame != null) {
                instance.swingFrame.dispose();
                instance.swingFrame = null;
            }
            instance = null;
            log.info("迷你小窗已销毁");
        });
    }

    public void setOnTodoChanged(Consumer<Todo> callback) { this.onTodoChanged = callback; }

    // ===== 构建 =====

    private static MiniFrameController buildInstance(Runnable openMainAction) {
        FXMLLoader loader = new FXMLLoader(MiniFrameController.class.getResource("/fxml/mini-frame.fxml"));
        Parent root;
        try {
            root = loader.load();
        } catch (IOException e) {
            throw new IllegalStateException("加载 mini-frame.fxml 失败", e);
        }
        MiniFrameController ctrl = loader.getController();
        ctrl.openMainAction = openMainAction;
        // ★关键：FXML 里按钮/提示文字是中文硬编码初始值，
        // 必须用当前语言覆盖一次，否则非中文语言下重开小窗会显示中文
        ctrl.updateMiniTexts();

        // Swing JFrame：Type.UTILITY = 不显示任务栏图标，undecorated = 无标题栏
        JFrame frame = new JFrame();
        frame.setType(JFrame.Type.UTILITY);
        frame.setUndecorated(true);
        frame.setAlwaysOnTop(true);
        frame.setSize((int) MIN_WIDTH, (int) COLLAPSED_HEIGHT);
        frame.setLocation(100, 200);

        JFXPanel panel = new JFXPanel();
        Platform.runLater(() -> {
            Scene scene = new Scene(root, MIN_WIDTH, COLLAPSED_HEIGHT);
            scene.setFill(Color.TRANSPARENT);
            var css = MiniFrameController.class.getResource("/css/style.css");
            if (css != null) scene.getStylesheets().add(css.toExternalForm());
            panel.setScene(scene);
        });
        frame.getContentPane().add(panel);

        // 拖动（Swing 层处理）
        frame.addMouseListener(new MouseAdapter() {
            @Override public void mousePressed(MouseEvent e) {
                ctrl.dragOffsetX = e.getX();
                ctrl.dragOffsetY = e.getY();
            }
        });
        frame.addMouseMotionListener(new MouseAdapter() {
            @Override public void mouseDragged(MouseEvent e) {
                int x = e.getXOnScreen() - (int) ctrl.dragOffsetX;
                int y = e.getYOnScreen() - (int) ctrl.dragOffsetY;
                frame.setLocation(x, y);
            }
        });

        ctrl.swingFrame = frame;
        ctrl.fxPanel = panel;
        ctrl.afterStageCreated();
        return ctrl;
    }

    private void afterStageCreated() {
        Platform.runLater(this::refresh);
    }

    // ===== FXML =====

    @FXML
    private void initialize() {
        todoListView.setItems(items);
        todoListView.setCellFactory(v -> new MiniListCell());
        todoListView.getSelectionModel().selectedItemProperty().addListener((obs, oldV, newV) -> {
            if (newV == null) return;
            for (int i = 0; i < items.size(); i++) {
                if (items.get(i) == newV) { currentIndex = i; renderCurrent(); break; }
            }
        });
    }

    @FXML
    private void onCompletedToggle() {
        TodoWithColor cur = current();
        if (cur == null) return;
        Todo todo = cur.todo();
        boolean nowDone = completedBox.isSelected();
        try {
            todo.setCompleted(nowDone);
            todo.setStatus(nowDone ? TodoStatus.DONE : TodoStatus.PENDING);
            todo.setCompletedAt(nowDone ? LocalDateTime.now() : null);
            todo.setUpdatedAt(LocalDateTime.now());
            todoService.update(todo);
            if (onTodoChanged != null) onTodoChanged.accept(todo);
            refresh();
            if (nowDone) jumpToFirstOpen();
        } catch (Exception e) {
            log.error("更新待办状态失败", e);
            completedBox.setSelected(!nowDone);
        }
    }

    @FXML
    private void onToggleExpand() {
        expanded = !expanded;
        expandPanel.setVisible(expanded);
        expandPanel.setManaged(expanded);
        expandBtn.setText(expanded ? t("mini.collapse") : t("mini.expand"));
        expandBtn.setStyle("-fx-text-fill:#D1D5DB; -fx-font-size:11px;");
        if (swingFrame != null) {
            swingFrame.setSize((int) MIN_WIDTH, (int) (expanded ? COLLAPSED_HEIGHT + 340 : COLLAPSED_HEIGHT));
        }
        if (expanded) { refresh(); todoListView.requestFocus(); }
    }

    @FXML private void onOpenMain() {
        if (openMainAction != null) {
            openMainAction.run();
        } else {
            openMainWindowByDefault();
        }
        destroy();
    }

    @FXML private void onHide() { hide(); }

    private double dragStartX, dragStartY;

    @FXML private void onDragStart(javafx.scene.input.MouseEvent e) {
        if (swingFrame == null) return;
        // 记录鼠标在屏幕上的起始位置和窗口位置
        dragStartX = e.getScreenX() - swingFrame.getX();
        dragStartY = e.getScreenY() - swingFrame.getY();
    }

    @FXML private void onDragMove(javafx.scene.input.MouseEvent e) {
        if (swingFrame == null) return;
        swingFrame.setLocation((int)(e.getScreenX() - dragStartX), (int)(e.getScreenY() - dragStartY));
    }

    private void openMainWindowByDefault() {
        Platform.runLater(() -> {
            try {
                FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/main.fxml"));
                Parent root = loader.load();
                Scene scene = new Scene(root, 1200, 800);
                Stage main = new Stage();
                main.initStyle(StageStyle.DECORATED);
                main.setTitle("P-Todo");
                main.setScene(scene);
                main.show();
            } catch (IOException e) { log.error("打开主窗口失败", e); }
        });
    }

    // ===== 数据 =====

    public void refresh() {
        runOnFx(() -> {
            try {
                // 只显示已认领且未完成的
                List<Todo> all = todoService.listAll();
                List<Todo> filtered = all.stream()
                    .filter(t -> t.getAssigneeId() != null && !t.getAssigneeId().isBlank())
                    .filter(t -> !t.isCompleted() && t.getStatus() != TodoStatus.DONE && t.getStatus() != TodoStatus.CANCELLED)
                    .toList();
                items.setAll(colorTagService.getColorSortedTodos(filtered));
            } catch (Exception e) { log.error("刷新失败", e); return; }
            if (currentIndex >= items.size()) currentIndex = 0;
            if (!items.isEmpty()) renderCurrent();
        });
    }

    private void jumpToFirstOpen() {
        for (int i = 0; i < items.size(); i++) {
            Todo t = items.get(i).todo();
            if (!t.isCompleted() && t.getStatus() != TodoStatus.DONE && t.getStatus() != TodoStatus.CANCELLED) {
                currentIndex = i; renderCurrent(); return;
            }
        }
        if (!items.isEmpty()) { currentIndex = 0; renderCurrent(); }
    }

    private TodoWithColor current() {
        if (items.isEmpty() || currentIndex < 0 || currentIndex >= items.size()) return null;
        return items.get(currentIndex);
    }

    private void renderCurrent() {
        TodoWithColor w = current();
        if (w == null) {
            titleLabel.setText(t("mini.noTodo"));
            dueLabel.setText("");
            completedBox.setSelected(false);
            completedBox.setDisable(true);
            colorBlock.setStyle("-fx-background-color:#374151; -fx-min-width:12; -fx-min-height:12; -fx-background-radius:3;");
            return;
        }
        completedBox.setDisable(false);

        Todo t = w.todo();
        boolean done = t.isCompleted() || t.getStatus() == TodoStatus.DONE || t.getStatus() == TodoStatus.CANCELLED;
        titleLabel.setText(t.getTitle() == null ? "" : t.getTitle());

        // 倒计时
        String dueText = t("mini.noDate");
        String dueColor = "#9CA3AF";
        if (t.getDueDate() != null && !t.getDueDate().isBlank()) {
            int daysLeft = daysUntilDue(t);
            dueColor = getCountdownColor(daysLeft);
            if (daysLeft < 0) dueText = "\u23f0 " + String.format(t("mini.overdue"), -daysLeft);
            else if (daysLeft == 0) dueText = "\u23f0 " + t("mini.today");
            else dueText = "\u23f0 " + String.format(t("mini.left"), daysLeft);
        }
        dueLabel.setText(dueText);
        dueLabel.setStyle("-fx-text-fill:" + dueColor + "; -fx-font-size:12px;");
        completedBox.setSelected(done);

        String hex = w.hex();
        String borderColor = "#FFFFFF";
        try {
            Color c = Color.web(hex);
            double brightness = c.getRed() * 0.299 + c.getGreen() * 0.587 + c.getBlue() * 0.114;
            borderColor = brightness > 0.5 ? "#374151" : "#FFFFFF";
        } catch (Exception ignored) {}
        colorBlock.setStyle("-fx-background-color:" + hex + "; -fx-min-width:12; -fx-min-height:12; -fx-background-radius:3; -fx-border-color:" + borderColor + "; -fx-border-radius:3; -fx-border-width:1;");
    }

    // ===== 工具 =====

    private static void runOnFx(Runnable r) {
        if (Platform.isFxApplicationThread()) r.run(); else Platform.runLater(r);
    }

    private int daysUntilDue(Todo todo) {
        if (todo.getDueDate() == null || todo.getDueDate().isBlank()) return Integer.MAX_VALUE;
        try {
            String d = todo.getDueDate();
            if (d.length() >= 10) d = d.substring(0, 10);
            java.time.LocalDate due = java.time.LocalDate.parse(d);
            return (int) java.time.temporal.ChronoUnit.DAYS.between(java.time.LocalDate.now(), due);
        } catch (Exception e) { return Integer.MAX_VALUE; }
    }

    private String getCountdownColor(int daysLeft) {
        if (daysLeft < 0) return "#EF4444";
        if (daysLeft <= 1) return "#EF4444";
        if (daysLeft <= 3) return "#F59E0B";
        if (daysLeft <= 7) return "#22C55E";
        if (daysLeft <= 14) return "#3B82F6";
        if (daysLeft <= 30) return "#A855F7";
        return "#D1D5DB";
    }

    private class MiniListCell extends ListCell<TodoWithColor> {
        @Override
        protected void updateItem(TodoWithColor w, boolean empty) {
            super.updateItem(w, empty);
            if (empty || w == null) { setText(null); setGraphic(null); setStyle(""); return; }
            Todo t = w.todo();
            Region dot = new Region();
            dot.setMinSize(12, 12);
            dot.setPrefSize(12, 12);
            String borderColor = "#FFFFFF";
            try {
                Color c = Color.web(w.hex());
                double brightness = c.getRed() * 0.299 + c.getGreen() * 0.587 + c.getBlue() * 0.114;
                borderColor = brightness > 0.5 ? "#374151" : "#FFFFFF";
            } catch (Exception ignored) {}
            dot.setStyle("-fx-background-color:" + w.hex() + "; -fx-background-radius:5; -fx-border-color:" + borderColor + "; -fx-border-radius:5; -fx-border-width:1;");

            Label title = new Label(t.getTitle() == null ? "" : t.getTitle());
            title.setStyle(t.isCompleted() || t.getStatus() == TodoStatus.DONE ? "-fx-text-fill:#6B7280;" : "-fx-text-fill:#F9FAFB;");

            // 优先级标签
            TodoPriority prio = t.getPriority() == null ? TodoPriority.MEDIUM : t.getPriority();
            String prioColor = switch (prio) {
                case URGENT -> "#EF4444"; case HIGH -> "#EAB308"; case MEDIUM -> "#22C55E"; case LOW -> "#6B7280";
            };
            Label prioLabel = new Label(prio.getLabel());
            prioLabel.setStyle("-fx-font-size:10px; -fx-text-fill:white; -fx-background-color:" + prioColor + "; -fx-padding:1 5; -fx-background-radius:3;");

            // 倒计时
            String dueText = "";
            String dueColor = "#9CA3AF";
            if (t.getDueDate() != null && !t.getDueDate().isBlank()) {
                int daysLeft = daysUntilDue(t);
                dueColor = getCountdownColor(daysLeft);
                if (daysLeft < 0) dueText = String.format(t("mini.overdue"), -daysLeft);
                else if (daysLeft == 0) dueText = t("mini.today");
                else dueText = String.format(t("mini.left"), daysLeft);
            }
            Label due = new Label(dueText);
            due.setStyle("-fx-text-fill:" + dueColor + "; -fx-font-size:11px;");

            javafx.scene.layout.HBox box = new javafx.scene.layout.HBox(8, dot, title, prioLabel, due);
            box.setAlignment(javafx.geometry.Pos.CENTER_LEFT);
            setGraphic(box);

            // 选中/ hover 样式
            if (isSelected()) {
                setStyle("-fx-background-color:#4F6BF6;");
                title.setStyle("-fx-text-fill:white;");
            } else {
                setStyle("");
            }
        }
    }

    /** i18n: 小窗所有文字（语言切换时刷新） */
    private void updateMiniTexts() {
        log.info("小窗文字刷新（语言={}）", I18n.getCurrentLang());
        if (listHint != null) listHint.setText(I18n.t("mini.sortHint"));
        if (expandBtn != null) expandBtn.setText(expanded ? t("mini.collapse") : t("mini.expand"));
        if (openMainBtn != null) openMainBtn.setText(t("mini.open"));
        if (completedBox != null) completedBox.setText(t("mini.complete"));
        // 重建列表数据（用新语言重新生成所有单元格文字）
        refresh();
    }

}