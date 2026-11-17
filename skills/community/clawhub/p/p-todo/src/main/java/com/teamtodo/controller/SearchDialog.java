package com.teamtodo.controller;

import com.teamtodo.model.Todo;
import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.service.ColorTagService;
import com.teamtodo.service.TodoService;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.ListCell;
import javafx.scene.control.TextField;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.text.Font;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Locale;
import java.util.function.Consumer;
import static com.teamtodo.util.I18n.t;
import com.teamtodo.util.I18n;

/**
 * 全局搜索对话框（纯 JavaFX 代码构建）：
 * - 弹出独立 Stage（UTILITY 工具窗口样式、置顶）
 * - 顶部搜索框，输入即搜（监听 textProperty，即时过滤）
 * - 匹配标题与描述
 * - 结果项显示：颜色点、标题、状态、截止日期
 * - 点击结果 → 通过回调通知主界面选中该待办，然后关闭
 * - Esc 关闭
 *
 * 用法：
 * <pre>
 *   SearchDialog.show(todo -> { /* 选中回调 *\/ });
 * </pre>
 */
public class SearchDialog {
    private static final Logger log = LoggerFactory.getLogger(SearchDialog.class);

    /** 单次打开最多展示的结果条数，避免超长列表卡顿 */
    private static final int MAX_RESULTS = 200;

    private final TodoService todoService = new TodoService();
    private final ColorTagService colorTagService = new ColorTagService();

    private final TextField searchField = new TextField();
    private final ListView<Todo> resultList = new ListView<>();
    private Consumer<Todo> onSelect;
    private Stage stage;
    private boolean closed = false;

    /**
     * 静态入口：打开全局搜索对话框。
     *
     * @param onSelect 用户点击某条结果时的回调（参数为选中的 Todo），可为 null
     */
    public static void show(Consumer<Todo> onSelect) {
        // 保证在 FX 线程上构建 UI
        Runnable open = () -> {
            SearchDialog dialog = new SearchDialog();
            dialog.onSelect = onSelect;
            dialog.open();
        };
        if (Platform.isFxApplicationThread()) {
            open.run();
        } else {
            Platform.runLater(open);
        }
    }

    /** 构建并显示对话框 */
    private void open() {
        stage = new Stage();
        stage.initStyle(StageStyle.UTILITY); // 工具窗口样式
        java.util.List<javafx.stage.Window> windows = Stage.getWindows();
        if (!windows.isEmpty()) stage.initOwner(windows.get(0));
        stage.setAlwaysOnTop(true); // 置顶
        stage.setTitle(t("search.title"));
        stage.setWidth(560);
        stage.setHeight(480);
        stage.setMinWidth(420);
        stage.setMinHeight(300);

        BorderPane root = buildView();
        Scene scene = new Scene(root);
        stage.setScene(scene);

        // Esc 关闭
        scene.addEventFilter(KeyEvent.KEY_PRESSED, e -> {
            if (e.getCode() == KeyCode.ESCAPE) {
                close();
            }
        });

        stage.setOnHidden(e -> markClosed());
        stage.show();
        // 自动聚焦搜索框
        searchField.requestFocus();
    }

    private BorderPane buildView() {
        BorderPane root = new BorderPane();
        root.setPadding(new Insets(10));

        // —— 顶部搜索框 ——
        searchField.setPromptText(t("search.hint"));
        searchField.getStyleClass().add("search-field");
        VBox top = new VBox(6, searchField);
        top.setPadding(new Insets(0, 0, 8, 0));

        // 即时搜索：输入即过滤
        searchField.textProperty().addListener((obs, oldV, newV) -> doSearch(newV));

        // —— 结果列表 ——
        resultList.setPlaceholder(new Label(t("search.placeholder")));
        resultList.setCellFactory(list -> new ResultCell());
        resultList.getSelectionModel().selectedIndexProperty().addListener((obs, oldIdx, newIdx) -> {
            // 双击才触发选择更贴近直觉；这里用选中项直接点击
        });
        resultList.setOnMouseClicked(e -> {
            Todo selected = resultList.getSelectionModel().getSelectedItem();
            if (selected != null) {
                choose(selected);
            }
        });
        // 回车直接选择第一项
        searchField.setOnAction(e -> {
            Todo first = resultList.getSelectionModel().getSelectedItem();
            if (first == null && !resultList.getItems().isEmpty()) {
                first = resultList.getItems().get(0);
            }
            if (first != null) choose(first);
        });

        root.setTop(top);
        root.setCenter(resultList);
        return root;
    }

    /** 执行一次搜索并填充列表 */
    private void doSearch(String keyword) {
        String kw = keyword == null ? "" : keyword.trim().toLowerCase(Locale.ROOT);
        if (kw.isEmpty()) {
            resultList.getItems().clear();
            return;
        }

        List<Todo> all;
        try {
            all = todoService.listAll();
        } catch (Exception ex) {
            log.warn("搜索时加载待办列表失败：{}", ex.getMessage());
            all = List.of();
        }

        List<Todo> matched = all.stream()
                .filter(t -> t != null && (match(t.getTitle(), kw) || match(t.getDescription(), kw)))
                .limit(MAX_RESULTS)
                .toList();

        resultList.getItems().setAll(matched);
        if (!matched.isEmpty()) {
            resultList.getSelectionModel().select(0);
        }
    }

    /** 关键词是否命中字段（忽略大小写） */
    private boolean match(String field, String kw) {
        return field != null && field.toLowerCase(Locale.ROOT).contains(kw);
    }

    /** 用户选择某条结果：回调主界面，然后关闭对话框 */
    private void choose(Todo todo) {
        if (onSelect != null) {
            onSelect.accept(todo);
        } else {
            log.debug("搜索选中待办[{}]，但未注册选择回调", todo.getId());
        }
        close();
    }

    /** 关闭对话框（幂等） */
    private void close() {
        if (stage != null && stage.isShowing()) {
            stage.close();
        }
        markClosed();
    }

    private void markClosed() {
        if (!closed) {
            closed = true;
            log.debug("全局搜索对话框已关闭");
        }
    }

    // ==================== 结果单元格 ====================

    /**
     * 搜索结果单元格：颜色点 + 标题 + 状态 + 截止日期。
     */
    private class ResultCell extends ListCell<Todo> {
        @Override
        protected void updateItem(Todo todo, boolean empty) {
            super.updateItem(todo, empty);
            if (empty || todo == null) {
                setText(null);
                setGraphic(null);
                return;
            }

            String hex = todo.getColorHex() != null ? todo.getColorHex() : colorTagService.calculateHex(todo);
            Circle dot = new Circle(5, Color.web(hex));
            dot.setPickOnBounds(false);

            Label title = new Label(todo.getTitle() == null ? "" : todo.getTitle());
            title.getStyleClass().add("search-result-title");
            title.setFont(Font.font("Microsoft YaHei", 13));

            TodoStatus status = todo.getStatus() == null ? TodoStatus.PENDING : todo.getStatus();
            Label statusLabel = new Label(status.getLabel());
            statusLabel.getStyleClass().addAll("tag", "status-" + status.name().toLowerCase());

            String due = todo.getDueDate();
            Label dueLabel = new Label(due != null && due.length() >= 10 ? "⏰ " + due.substring(0, 10) : t("search.noDue"));
            dueLabel.getStyleClass().add("search-result-due");

            HBox right = new HBox(8, statusLabel, dueLabel);
            right.setAlignment(javafx.geometry.Pos.CENTER_RIGHT);

            HBox row = new HBox(10, dot, title, right);
            row.getStyleClass().add("search-result-row");
            HBox.setHgrow(title, javafx.scene.layout.Priority.ALWAYS);

            setText(null);
            setGraphic(row);
        }
    }
}
