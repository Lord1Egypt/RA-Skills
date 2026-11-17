package com.teamtodo.util;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.VBox;
import javafx.stage.Modality;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import static com.teamtodo.util.I18n.t;
import com.teamtodo.util.I18n;

/**
 * 快捷键帮助面板
 */
public class ShortcutsHelp {

    public static void show() {
        Stage stage = new Stage();
        stage.initModality(Modality.APPLICATION_MODAL);
        stage.initStyle(StageStyle.UTILITY);
        stage.setTitle(t("shortcut.title"));
        stage.setWidth(400);
        stage.setHeight(500);

        VBox content = new VBox(12);
        content.setPadding(new Insets(20));
        content.setStyle("-fx-background-color:white;");

        Label title = new Label(t("shortcut.heading"));
        title.setStyle("-fx-font-size:18px; -fx-font-weight:bold;");

        content.getChildren().add(title);
        content.getChildren().add(makeSeparator());

        content.getChildren().add(makeSection(t("shortcut.global")));
        content.getChildren().add(makeShortcut("Ctrl + N", t("shortcut.new")));
        content.getChildren().add(makeShortcut("Ctrl + K", t("shortcut.search")));
        content.getChildren().add(makeShortcut("Ctrl + M", t("shortcut.mini")));
        content.getChildren().add(makeShortcut("Esc", t("shortcut.close")));

        content.getChildren().add(makeSeparator());
        content.getChildren().add(makeSection(t("shortcut.list")));
        content.getChildren().add(makeShortcut("↑ / ↓", t("shortcut.select")));
        content.getChildren().add(makeShortcut("Enter", t("shortcut.complete")));
        content.getChildren().add(makeShortcut("Delete", t("shortcut.delete")));

        content.getChildren().add(makeSeparator());
        content.getChildren().add(makeSection(t("shortcut.newSection")));
        content.getChildren().add(makeShortcut(t("shortcut.autoDate"), t("shortcut.autoDate")));
        content.getChildren().add(makeShortcut(t("shortcut.example1"), t("shortcut.example1desc")));
        content.getChildren().add(makeShortcut(t("shortcut.example2"), t("shortcut.example2desc")));
        content.getChildren().add(makeShortcut(t("shortcut.example3"), t("shortcut.example3desc")));

        ScrollPane scroll = new ScrollPane(content);
        scroll.setFitToWidth(true);

        Scene scene = new Scene(scroll);
        scene.setOnKeyPressed(e -> { if (e.getCode() == KeyCode.ESCAPE) stage.close(); });
        stage.setScene(scene);
        stage.show();
    }

    private static Label makeSection(String text) {
        Label l = new Label(text);
        l.setStyle("-fx-font-size:14px; -fx-font-weight:bold; -fx-text-fill:#4F6BF6;");
        return l;
    }

    private static javafx.scene.layout.HBox makeShortcut(String key, String desc) {
        Label keyLabel = new Label(key);
        keyLabel.setStyle("-fx-font-family:monospace; -fx-font-size:12px; -fx-background-color:#F3F4F6; -fx-padding:2 8; -fx-background-radius:4; -fx-border-color:#E5E7EB; -fx-border-radius:4;");
        Label descLabel = new Label(desc);
        descLabel.setStyle("-fx-font-size:12px; -fx-text-fill:#374151;");
        javafx.scene.layout.HBox row = new javafx.scene.layout.HBox(12, keyLabel, descLabel);
        row.setAlignment(Pos.CENTER_LEFT);
        row.setPadding(new Insets(2, 0, 2, 0));
        return row;
    }

    private static javafx.scene.control.Separator makeSeparator() {
        javafx.scene.control.Separator s = new javafx.scene.control.Separator();
        s.setPadding(new Insets(4, 0, 4, 0));
        return s;
    }
}
