package com.teamtodo.controller;

import com.teamtodo.model.enums.TodoStatus;
import com.teamtodo.service.TodoService;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.control.Label;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.VBox;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;
import static com.teamtodo.util.I18n.t;
import com.teamtodo.util.I18n;

public class StatisticsController {
    private static final Logger log = LoggerFactory.getLogger(StatisticsController.class);
    private final TodoService todoService = new TodoService();
    private VBox root;
    private Label totalValue;
    private Label doneValue;
    private Label inProgressValue;
    private Label overdueValue;

    public void refresh() {
        int total = 0, done = 0, inProgress = 0, overdue = 0;
        try {
            Map<TodoStatus, Integer> stats = todoService.getStats();
            if (stats != null) {
                for (Map.Entry<TodoStatus, Integer> e : stats.entrySet()) {
                    if (e.getValue() == null) continue;
                    if (e.getKey() == null) { done = e.getValue(); }
                    else { total += e.getValue(); }
                }
                if (done == 0) done = stats.getOrDefault(TodoStatus.DONE, 0);
                inProgress = stats.getOrDefault(TodoStatus.IN_PROGRESS, 0);
            }
            overdue = todoService.getOverdueCount();
        } catch (Exception ex) {
            log.warn("Stats error", ex);
        }
        if (totalValue != null) {
            totalValue.setText(String.valueOf(total));
            doneValue.setText(String.valueOf(done));
            inProgressValue.setText(String.valueOf(inProgress));
            overdueValue.setText(String.valueOf(overdue));
        }
    }

    public Parent getView() {
        if (root == null) root = buildView();
        refresh();
        javafx.scene.control.ScrollPane scroll = new javafx.scene.control.ScrollPane(root);
        scroll.setFitToWidth(true);
        scroll.setStyle("-fx-background-color:transparent;");
        return scroll;
    }

    private VBox buildView() {
        VBox r = new VBox(12);
        r.setPadding(new Insets(16));

        Label heading = new Label(t("stats.heading"));
        heading.setStyle("-fx-font-size:18px; -fx-font-weight:bold;");

        totalValue = makeNumLabel();
        doneValue = makeNumLabel();
        inProgressValue = makeNumLabel();
        overdueValue = makeNumLabel();

        HBox cards = new HBox(12);
        cards.getChildren().addAll(
                makeCard(t("stats.total"), totalValue, "#111827"),
                makeCard(t("stats.inProgress"), inProgressValue, "#10B981"),
                makeCard(t("stats.overdue"), overdueValue, "#EF4444"),
                makeCard(t("stats.done"), doneValue, "#9CA3AF")
        );

        r.getChildren().addAll(heading, cards);
        return r;
    }

    private Label makeNumLabel() {
        Label l = new Label("0");
        l.setStyle("-fx-font-size:28px; -fx-font-weight:bold; -fx-text-fill:#1F2937;");
        return l;
    }

    private VBox makeCard(String title, Label value, String color) {
        Label tl = new Label(title);
        tl.setStyle("-fx-font-size:13px; -fx-text-fill:#6B7280;");
        VBox box = new VBox(6, value, tl);
        box.setPadding(new Insets(18, 12, 18, 12));
        box.setAlignment(Pos.CENTER);
        box.setStyle("-fx-background-color:white; -fx-background-radius:10; -fx-border-color:#E5E7EB; -fx-border-radius:10; -fx-border-width:1;");
        return box;
    }
}
