package com.teamtodo.controller;

import com.teamtodo.model.Todo;
import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.service.TodoService;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.control.Label;
import javafx.scene.layout.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import static com.teamtodo.util.I18n.t;
import com.teamtodo.util.I18n;

/**
 * 工作台概览控制器：统计卡片 + 今日到期 + 最近任务
 */
public class DashboardController {
    private static final Logger log = LoggerFactory.getLogger(DashboardController.class);
    private static final DateTimeFormatter DF = DateTimeFormatter.ofPattern("MM-dd");

    private final TodoService todoService = new TodoService();
    private VBox root;
    private Label totalVal, doneVal, progressVal, overdueVal, pendingVal;
    private VBox todayBox, recentBox;

    public Parent getView() {
        if (root == null) root = buildView();
        refresh();
        javafx.scene.control.ScrollPane scroll = new javafx.scene.control.ScrollPane(root);
        scroll.setFitToWidth(true);
        scroll.setStyle("-fx-background-color:transparent;");
        return scroll;
    }

    public void refresh() {
        try {
            var stats = todoService.getStats();
            int total = 0, done = 0, inProgress = 0, pending = 0, overdue = todoService.getOverdueCount();
            for (var e : stats.entrySet()) {
                if (e.getKey() == null || e.getValue() == null) continue;
                total += e.getValue();
                if (e.getKey() == TodoStatus.DONE) done = e.getValue();
                if (e.getKey() == TodoStatus.IN_PROGRESS) inProgress = e.getValue();
                if (e.getKey() == TodoStatus.PENDING) pending = e.getValue();
            }
            totalVal.setText(String.valueOf(total));
            doneVal.setText(String.valueOf(done));
            progressVal.setText(String.valueOf(inProgress));
            overdueVal.setText(String.valueOf(overdue));
            if (pendingVal != null) pendingVal.setText(String.valueOf(pending));

            // 今日到期
            todayBox.getChildren().clear();
            List<Todo> today = todoService.listToday();
            if (today.isEmpty()) {
                todayBox.getChildren().add(makeEmptyLabel(t("dashboard.noDue")));
            } else {
                for (Todo t : today) todayBox.getChildren().add(makeTaskRow(t));
            }

            // 最近任务（前 8 个）
            recentBox.getChildren().clear();
            List<Todo> all = todoService.listAll();
            int count = Math.min(all.size(), 8);
            if (count == 0) {
                recentBox.getChildren().add(makeEmptyLabel(t("dashboard.noTasks")));
            } else {
                for (int i = 0; i < count; i++) recentBox.getChildren().add(makeTaskRow(all.get(i)));
            }
        } catch (Exception e) {
            log.warn("工作台刷新失败: {}", e.getMessage());
        }
    }

    private VBox buildView() {
        VBox r = new VBox(16);
        r.setPadding(new Insets(20));
        r.setStyle("-fx-background-color:#F5F7FA;");

        // 欢迎
        Label welcome = new Label(t("dashboard.title"));
        welcome.setStyle("-fx-font-size:20px; -fx-font-weight:bold; -fx-text-fill:#111827;");

        // 统计卡片行
        HBox cards = new HBox(12);
        cards.getChildren().addAll(
                makeStatCard(t("dashboard.all"), "0", "#111827", "total"),
                makeStatCard(t("dashboard.inProgress"), "0", "#10B981", "progress"),
                makeStatCard(t("dashboard.notStarted"), "0", "#4F6BF6", "pending"),
                makeStatCard(t("dashboard.overdue"), "0", "#EF4444", "overdue"),
                makeStatCard(t("dashboard.done"), "0", "#9CA3AF", "done")
        );

        // 今日到期
        Label todayTitle = new Label(t("dashboard.todayDue"));
        todayTitle.setStyle("-fx-font-size:14px; -fx-font-weight:600; -fx-text-fill:#374151;");
        todayBox = new VBox(4);
        todayBox.setStyle("-fx-background-color:white; -fx-background-radius:8; -fx-padding:12; -fx-border-color:#E5E7EB; -fx-border-radius:8; -fx-border-width:1;");

        // 最近任务
        Label recentTitle = new Label(t("dashboard.recent"));
        recentTitle.setStyle("-fx-font-size:14px; -fx-font-weight:600; -fx-text-fill:#374151;");
        recentBox = new VBox(4);
        recentBox.setStyle("-fx-background-color:white; -fx-background-radius:8; -fx-padding:12; -fx-border-color:#E5E7EB; -fx-border-radius:8; -fx-border-width:1;");

        r.getChildren().addAll(welcome, cards, todayTitle, todayBox, recentTitle, recentBox);
        return r;
    }



    private HBox makeTaskRow(Todo t) {
        Label dot = new Label("●");
        boolean overdue = t.getDueDate() != null && !t.isCompleted()
                && t.getDueDate().compareTo(LocalDate.now().toString()) < 0;
        String color = t.getStatus() == TodoStatus.DONE ? "#10B981" :
                        overdue ? "#EF4444" : "#9CA3AF";
        dot.setStyle("-fx-text-fill:" + color + "; -fx-font-size:8px;");
        Label title = new Label(t.getTitle());
        title.setStyle("-fx-text-fill:#374151; -fx-font-size:13px;");
        Label due = new Label(t.getDueDate() != null ? t.getDueDate() : "");
        due.setStyle("-fx-text-fill:#9CA3AF; -fx-font-size:11px;");
        Region spacer = new Region();
        HBox.setHgrow(title, Priority.ALWAYS);
        HBox row = new HBox(8, dot, title, due);
        row.setAlignment(Pos.CENTER_LEFT);
        row.setPadding(new Insets(4, 0, 4, 0));
        return row;
    }

    private Label makeEmptyLabel(String text) {
        Label l = new Label(text);
        l.setStyle("-fx-text-fill:#9CA3AF; -fx-font-size:13px; -fx-padding:12 0;");
        return l;
    }

    /** 创建统计卡片（i18n 绑定版本） */
    private VBox makeStatCard(String i18nKey, String value, String color, String type) {
        Label titleLabel = new Label();
        if (i18nKey != null) titleLabel.textProperty().bind(I18n.text(i18nKey));
        else titleLabel.textProperty().bind(I18n.text("dashboard." + type));
        titleLabel.setStyle("-fx-font-size:12px; -fx-text-fill:#6B7280;");
        Label val = new Label(value);
        val.setStyle("-fx-font-size:28px; -fx-font-weight:bold; -fx-text-fill:" + color + ";");
        VBox card = new VBox(4, val, titleLabel);
        card.setStyle("-fx-background-color:white; -fx-padding:16; -fx-background-radius:8; -fx-effect:dropshadow(gaussian,rgba(0,0,0,0.05),4,0,0,1);");
        card.setPrefWidth(160);
        HBox.setHgrow(card, Priority.ALWAYS);
        switch (type) {
            case "total" -> totalVal = val;
            case "done" -> doneVal = val;
            case "progress" -> progressVal = val;
            case "overdue" -> overdueVal = val;
            case "pending" -> pendingVal = val;
        }
        return card;
    }
}
