package com.teamtodo.controller;

import com.teamtodo.model.User;
import com.teamtodo.service.NotificationService;
import com.teamtodo.service.UserService;
import com.teamtodo.util.DataExporter;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.stage.FileChooser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.util.List;
import static com.teamtodo.util.I18n.t;

/**
 * 设置页面控制器
 */
public class SettingsController {
    private static final Logger log = LoggerFactory.getLogger(SettingsController.class);

    @FXML private Label dataPathLabel;
    @FXML private ComboBox<User> userCombo;
    @FXML private TextField newNameField;
    @FXML private Button btnSaveUser;
    @FXML private Button btnAddUser;
    @FXML private Button btnDeleteUser;
    @FXML private Label userCountLabel;

    // 通知设置
    @FXML private TextField soundPathField;
    @FXML private Button btnBrowseSound;
    @FXML private Button btnTestSound;

    // 语言设置
    @FXML private ComboBox<String> langCombo;
    @FXML private Label langHint;

        // i18n FXML fields
    @FXML private Label titleLabel;
    @FXML private Label langTitleLabel;
    @FXML private Label teamTitleLabel;
    @FXML private Label notifTitleLabel;
    @FXML private Label dataTitleLabel;
    @FXML private Label apiTitleLabel;
    
    @FXML private Label portLabelLabel;
    @FXML private Button btnExportJson;
    @FXML private Button btnExportCsv;
    // API 设置
    @FXML private TextField apiPortField;
    @FXML private Button btnSavePort;
    @FXML private Label apiPortHint;

    private final UserService userService = new UserService();
    private final NotificationService notificationService = NotificationService.getInstance();

    @FXML
    private void initialize() {
        dataPathLabel.setText(System.getProperty("user.home") + File.separator + "P-Todo" + File.separator + "data" + File.separator + "P-Todo.db");
        refreshUsers();

        // 加载自定义音效路径
        String customPath = notificationService.getCustomSoundPath();
        if (customPath != null && !customPath.isEmpty()) {
            soundPathField.setText(customPath);
        }

        // 语言切换
        var langs = com.teamtodo.util.I18n.LANGS;
        langCombo.getItems().addAll(langs);
        langCombo.setCellFactory(lv -> new ListCell<>() {
            @Override protected void updateItem(String item, boolean empty) {
                super.updateItem(item, empty);
                setText(empty || item == null ? "" : com.teamtodo.util.I18n.LANG_NAMES.getOrDefault(item, item));
            }
        });
        langCombo.setButtonCell(new ListCell<>() {
            @Override protected void updateItem(String item, boolean empty) {
                super.updateItem(item, empty);
                setText(empty || item == null ? "" : com.teamtodo.util.I18n.LANG_NAMES.getOrDefault(item, item));
            }
        });
        langCombo.setValue(com.teamtodo.util.I18n.getCurrentLang());

        // 更新按钮：输入为空时禁用
        newNameField.textProperty().addListener((obs, old, text) -> {
            if (btnSaveUser != null) btnSaveUser.setDisable(text == null || text.trim().isEmpty());
        });
        btnSaveUser.setDisable(true); // 初始禁用
        // 选中成员时清空输入框（按钮变新增模式），未选中时按钮保持禁用
        userCombo.getSelectionModel().selectedItemProperty().addListener((obs, old, user) -> {
            newNameField.clear();
            if (btnSaveUser != null) btnSaveUser.setDisable(true);
        });
        // 输入框最大长度 20 字符
        newNameField.setTextFormatter(new javafx.scene.control.TextFormatter<>(change ->
                change.getControlNewText().length() <= 20 ? change : null));

        updateSettingsTexts();

        // API 端口
        apiPortField.setText(String.valueOf(com.teamtodo.api.ApiServer.getPort()));
    
}

    @FXML private void onLangChanged() {
        String selected = langCombo.getValue();
        System.out.println("[DEBUG] onLangChanged: selected=" + selected);
        if (selected != null) {
            com.teamtodo.util.I18n.setLang(selected);
            langHint.setText(com.teamtodo.util.I18n.t("settings.languageHint"));
        }
    }

    @FXML private void saveApiPort() {
        try {
            int port = Integer.parseInt(apiPortField.getText().trim());
            if (port < 1024 || port > 65535) {
                apiPortHint.setText(t("settings.portRange"));
                return;
            }
            com.teamtodo.api.ApiServer.setPort(port);
            apiPortHint.setText(String.format(t("settings.portSaved"), port));
        } catch (NumberFormatException e) {
            apiPortHint.setText(t("settings.portInvalid"));
        }
    }

    private void refreshUsers() {
        List<User> users = userService.listAll();
        userCombo.setItems(FXCollections.observableArrayList(users));
        userCombo.setCellFactory(lv -> new ListCell<>() {
            @Override protected void updateItem(User u, boolean empty) {
                super.updateItem(u, empty);
                setText(empty ? null : u.getName());
            }
        });
        userCombo.setButtonCell(new ListCell<>() {
            @Override protected void updateItem(User u, boolean empty) {
                super.updateItem(u, empty);
                setText(empty ? null : u.getName());
            }
        });
        if (!users.isEmpty()) userCombo.setValue(users.get(0));
        userCountLabel.setText(String.format(t("settings.memberCount"), users.size()));
    }



    @FXML
    private void onUserSelected() {
        // 触发选择监听器的逻辑（按钮文字已在监听器中处理）
    }

    @FXML
    private void saveUser() {
        User selected = userCombo.getValue();
        if (selected == null) {
            // 没有选中成员：把输入框内容作为新成员添加
            addNewUser();
            return;
        }
        String name = newNameField.getText().trim();
        if (name.isEmpty()) {
            new Alert(Alert.AlertType.WARNING, t("settings.nameEmpty")).showAndWait();
            newNameField.requestFocus();
            return;
        }
        try {
            // 更新模式：按 ID 改名，保留原 ID
            userService.updateName(selected.getId(), name);
            newNameField.clear();
            refreshUsers();
            notificationService.playSound(NotificationService.SoundType.COMPLETE);
            log.info("已更新成员: {}", name);
        } catch (Exception e) {
            log.error("保存成员失败", e);
            new Alert(Alert.AlertType.ERROR, t("settings.saveFailed") + e.getMessage()).showAndWait();
        }
    }

    /** 新增成员：把输入框内容添加为新成员 */
    @FXML
    private void addNewUser() {
        String name = newNameField.getText() == null ? "" : newNameField.getText().trim();
        if (name.isEmpty()) {
            new Alert(Alert.AlertType.WARNING, t("settings.nameEmpty")).showAndWait();
            newNameField.requestFocus();
            return;
        }
        try {
            userService.upsert(name, null);
            newNameField.clear();
            userCombo.getSelectionModel().clearSelection();
            refreshUsers();
            notificationService.playSound(NotificationService.SoundType.COMPLETE);
            log.info("已新增成员: {}", name);
        } catch (Exception e) {
            log.error("新增成员失败", e);
            new Alert(Alert.AlertType.ERROR, t("settings.saveFailed") + e.getMessage()).showAndWait();
        }
    }

    @FXML
    private void deleteUser() {
        User selected = userCombo.getValue();
        if (selected == null) {
            new Alert(Alert.AlertType.WARNING, t("settings.deleteSelect")).showAndWait();
            return;
        }
        Alert confirm = new Alert(Alert.AlertType.CONFIRMATION, String.format(t("settings.deleteConfirm"), selected.getName()));
        confirm.showAndWait().ifPresent(btn -> {
            if (btn == ButtonType.OK) {
                userService.delete(selected.getId());
                newNameField.clear();
                refreshUsers();
                notificationService.playSound(NotificationService.SoundType.WARNING);
                log.info("已删除成员: {}", selected.getName());
            }
        });
    }

    @FXML
    private void browseSound() {
        FileChooser fc = new FileChooser();
        fc.setTitle(t("settings.selectAudio"));
        fc.getExtensionFilters().add(new FileChooser.ExtensionFilter(t("settings.audioFiles"), "*.wav", "*.mp3", "*.ogg"));
        File file = fc.showOpenDialog(btnBrowseSound.getScene().getWindow());
        if (file != null) {
            soundPathField.setText(file.getAbsolutePath());
            notificationService.setCustomSoundPath(file.getAbsolutePath());
        }
    }

    @FXML
    private void testSound() {
        notificationService.testSound();
    }

    @FXML
    private void exportJson() {
        FileChooser fc = new FileChooser();
        fc.setTitle(t("settings.exportJsonTitle"));
        fc.setInitialFileName("p-todo-export.json");
        fc.getExtensionFilters().add(new FileChooser.ExtensionFilter(t("settings.jsonFiles"), "*.json"));
        File file = fc.showSaveDialog(btnSaveUser.getScene().getWindow());
        if (file != null) {
            try {
                DataExporter.exportJson(file);
                new Alert(Alert.AlertType.INFORMATION, t("settings.exported") + file.getAbsolutePath()).showAndWait();
            } catch (Exception e) {
                log.error("导出 JSON 失败", e);
                new Alert(Alert.AlertType.ERROR, t("settings.exportFailed") + e.getMessage()).showAndWait();
            }
        }
    }

    @FXML
    private void exportCsv() {
        FileChooser fc = new FileChooser();
        fc.setTitle(t("settings.exportCsvTitle"));
        fc.setInitialFileName("p-todo-export.csv");
        fc.getExtensionFilters().add(new FileChooser.ExtensionFilter(t("settings.csvFiles"), "*.csv"));
        File file = fc.showSaveDialog(btnSaveUser.getScene().getWindow());
        if (file != null) {
            try {
                DataExporter.exportCsv(file);
                new Alert(Alert.AlertType.INFORMATION, t("settings.exported") + file.getAbsolutePath()).showAndWait();
            } catch (Exception e) {
                log.error("导出 CSV 失败", e);
                new Alert(Alert.AlertType.ERROR, t("settings.exportFailed") + e.getMessage()).showAndWait();
            }
        }
    }

    /** i18n: 设置页面绑定所有文字到 I18n */
    public void updateSettingsTexts() {
        if (titleLabel != null) titleLabel.textProperty().bind(com.teamtodo.util.I18n.text("settings.title"));
        if (langTitleLabel != null) langTitleLabel.textProperty().bind(com.teamtodo.util.I18n.text("settings.language"));
        if (teamTitleLabel != null) teamTitleLabel.textProperty().bind(com.teamtodo.util.I18n.text("settings.teamMembers"));
        if (notifTitleLabel != null) notifTitleLabel.textProperty().bind(com.teamtodo.util.I18n.text("settings.notification"));
        if (dataTitleLabel != null) dataTitleLabel.textProperty().bind(com.teamtodo.util.I18n.text("settings.data"));
        if (apiTitleLabel != null) apiTitleLabel.textProperty().bind(com.teamtodo.util.I18n.text("settings.apiService"));
        if (portLabelLabel != null) portLabelLabel.textProperty().bind(com.teamtodo.util.I18n.text("settings.portLabel"));
        if (langHint != null) langHint.setText(com.teamtodo.util.I18n.t("settings.languageHint"));
        if (apiPortHint != null) apiPortHint.setText(com.teamtodo.util.I18n.t("settings.portHint"));
        if (btnSaveUser != null) btnSaveUser.textProperty().bind(com.teamtodo.util.I18n.text("settings.update"));
        if (btnAddUser != null) btnAddUser.textProperty().bind(com.teamtodo.util.I18n.text("settings.new"));
        if (btnDeleteUser != null) btnDeleteUser.textProperty().bind(com.teamtodo.util.I18n.text("settings.deleteMember"));
        if (btnBrowseSound != null) btnBrowseSound.textProperty().bind(com.teamtodo.util.I18n.text("settings.browse"));
        if (btnTestSound != null) btnTestSound.textProperty().bind(com.teamtodo.util.I18n.text("settings.test"));
        if (btnExportJson != null) btnExportJson.textProperty().bind(com.teamtodo.util.I18n.text("settings.exportJson"));
        if (btnExportCsv != null) btnExportCsv.textProperty().bind(com.teamtodo.util.I18n.text("settings.exportCsv"));
        if (btnSavePort != null) btnSavePort.textProperty().bind(com.teamtodo.util.I18n.text("settings.portSave"));
        if (newNameField != null) newNameField.promptTextProperty().bind(com.teamtodo.util.I18n.text("settings.addHint"));
        if (userCombo != null) userCombo.promptTextProperty().bind(com.teamtodo.util.I18n.text("settings.memberManage"));
        if (soundPathField != null) soundPathField.promptTextProperty().bind(com.teamtodo.util.I18n.text("settings.soundHint"));
        if (dataPathLabel != null) {
            String path = System.getProperty("user.home") + "/P-Todo/data/P-Todo.db";
            dataPathLabel.setText(com.teamtodo.util.I18n.t("settings.dataPath", path));
        }
        if (langCombo != null) langCombo.promptTextProperty().bind(com.teamtodo.util.I18n.text("settings.selectLanguage"));
    }


}