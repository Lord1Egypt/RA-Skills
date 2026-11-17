package com.teamtodo;

import com.teamtodo.api.ApiServer;
import com.teamtodo.controller.MiniFrameController;
import com.teamtodo.util.I18n;
import com.teamtodo.dao.DatabaseManager;
import com.teamtodo.service.ReminderScheduler;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.stage.Modality;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import static com.teamtodo.util.I18n.t;

public class App extends Application {
    private static final Logger log = LoggerFactory.getLogger(App.class);
    private static Stage primaryStage;
    private static boolean closeToTray = true; // 默认隐藏到托盘
    private static String iconPath;
    private static Runnable onRefresh; // API 写操作后触发 UI 刷新的回调

    /** 注册刷新回调（MainController 初始化时调用） */
    public static void setOnRefresh(Runnable callback) { onRefresh = callback; }
    /** API 写操作后调用此方法刷新 UI */
    public static void notifyRefresh() { if (onRefresh != null) Platform.runLater(onRefresh); }

    @Override
    public void start(Stage stage) throws Exception {
        primaryStage = stage;

        // 初始化数据库
        String dbDir = System.getProperty("user.home") + File.separator + "P-Todo" + File.separator + "data";
        new File(dbDir).mkdirs();
        String dbPath = dbDir + File.separator + "P-Todo.db";
        DatabaseManager.getInstance(dbPath);

        // 启动 REST API 服务器（供 OpenClaw 等智能体调用）
        ApiServer apiServer = new ApiServer();
        apiServer.start();

        I18n.init();
        I18n.onLangChange(lang -> Platform.runLater(() -> {
            // 切语言后：关闭并销毁旧托盘菜单，下次右键用新语言重建；更新托盘悬停提示
            if (trayMenuFrame != null) {
                trayMenuFrame.setVisible(false);
                trayMenuFrame.dispose();
                trayMenuFrame = null;
            }
            if (trayIcon != null) {
                try { trayIcon.setToolTip(I18n.t("app.title")); } catch (Exception ignored) {}
            }
            // 小窗语言切换：即使小窗未打开也触发刷新（updateMiniTexts 内有 null 保护）
            com.teamtodo.controller.MiniFrameController.updateMiniTextsStatic();
        }));

        // 初始化系统托盘
        initSystemTray();

        // 加载主界面
        FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/main.fxml"));
        Parent root = loader.load();

        Scene scene = new Scene(root, 1200, 800);
        scene.getStylesheets().add(getClass().getResource("/css/style.css").toExternalForm());

        stage.titleProperty().bind(I18n.text("app.title"));
        // 设置应用图标
        Image icon = loadIcon();
        if (icon != null) {
            stage.getIcons().add(icon);
        }
        stage.setScene(scene);

        // 修复 IME 候选框不跟随光标：当任何 TextInputControl 获得焦点时自动绑定
        scene.focusOwnerProperty().addListener((obs, old, node) -> {
            if (node instanceof javafx.scene.control.TextInputControl tic) {
                com.teamtodo.util.ImeHelper.fixImeTracking(tic);
            }
        });

        // 关闭时隐藏到托盘（不退出）
        stage.setOnCloseRequest(event -> {
            if (closeToTray) {
                event.consume();
                hideMain();
            } else {
                doExit();
            }
        });

        // 注册全局快捷键
        com.teamtodo.controller.MainController mc = loader.getController();
        mc.setupKeyboardShortcuts(scene);

        stage.show();
        log.info("主界面已显示");

        // 启动提醒调度器
        ReminderScheduler.getInstance().start();

        // 启动时显示小窗，隐藏主界面
        hideMain();
        MiniFrameController.show(() -> showMain());
    }

    // ===== 系统托盘 =====
    private static java.awt.TrayIcon trayIcon;

    /** 加载应用图标：优先外部文件，回退内置 */
    public static Image loadIcon() {
        // 优先级：项目目录图标 > F:\XXZ\日程.png
        String[] candidates = {
                "icon.png",
                "icon.png"
        };
        for (String p : candidates) {
            File f = new File(p);
            if (f.exists()) {
                try {
                    return new Image(f.toURI().toString());
                } catch (Exception ignored) {
                }
            }
        }
        return null;
    }

    private void initSystemTray() {
        if (!SystemTray.isSupported()) {
            log.warn("系统托盘不支持");
            return;
        }

        SystemTray tray = SystemTray.getSystemTray();

        // 创建图标（优先外部图标文件，回退内置生成图标）
        java.awt.image.BufferedImage bimg = null;
        for (String p : new String[]{
                "icon.png",
                "icon.png"
        }) {
            File f = new File(p);
            if (f.exists()) {
                try {
                    bimg = javax.imageio.ImageIO.read(f);
                    break;
                } catch (Exception ignored) {
                }
            }
        }
        if (bimg == null) {
            bimg = createTrayIconImage();
        }
        java.awt.Image trayIconImage = bimg.getScaledInstance(16, 16, java.awt.Image.SCALE_SMOOTH);

        // 创建托盘图标（不使用 AWT PopupMenu，改用 JavaFX 弹窗避免中文乱码）
        trayIcon = new java.awt.TrayIcon(trayIconImage, I18n.t("app.title"));
        trayIcon.setImageAutoSize(true);

        // 双击打开主界面 / 右键弹出菜单
        trayIcon.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) {
                    Platform.runLater(App::showMain);
                } else if (e.getButton() == MouseEvent.BUTTON3) {
                    // 右键弹出 JavaFX 菜单（避免 AWT PopupMenu 中文乱码）
                    Platform.runLater(() -> showTrayMenu(e.getXOnScreen(), e.getYOnScreen()));
                }
            }
        });

        try {
            tray.add(trayIcon);
            log.info("系统托盘图标已添加");
        } catch (AWTException e) {
            log.error("添加系统托盘图标失败", e);
        }
    }

    private java.awt.image.BufferedImage createTrayIconImage() {
        // 生成一个 16x16 的蓝色方块图标
        java.awt.image.BufferedImage img = new java.awt.image.BufferedImage(16, 16, java.awt.image.BufferedImage.TYPE_INT_ARGB);
        java.awt.Graphics2D g = img.createGraphics();
        g.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
        g.setColor(new java.awt.Color(79, 107, 246)); // #4F6BF6
        g.fillRoundRect(0, 0, 16, 16, 4, 4);
        g.setColor(java.awt.Color.WHITE);
        g.setFont(new java.awt.Font("SansSerif", java.awt.Font.BOLD, 11));
        g.drawString("T", 4, 12);
        g.dispose();
        return img;
    }

    private static javax.swing.JFrame trayMenuFrame;

    /** Swing 弹窗式托盘菜单（Type.UTILITY + undecorated = 无标题栏、无任务栏图标） */
    private static void showTrayMenu(int screenX, int screenY) {
        if (trayMenuFrame != null && trayMenuFrame.isVisible()) {
            trayMenuFrame.setVisible(false);
            return;
        }

        if (trayMenuFrame == null) {
            trayMenuFrame = new javax.swing.JFrame();
            trayMenuFrame.setType(javax.swing.JFrame.Type.UTILITY);
            trayMenuFrame.setUndecorated(true);
            trayMenuFrame.setAlwaysOnTop(true);

            VBox box = new VBox(2);
            box.setStyle("-fx-background-color: #2D2D2D; -fx-background-radius: 6; -fx-padding: 4 0; -fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.3), 8, 0, 0, 2);");

            box.getChildren().addAll(
                    makeTrayMenuItem(t("tray.mini"), () -> { trayMenuFrame.setVisible(false); showMini(); }),
                    makeTrayMenuItem(t("tray.open"), () -> { trayMenuFrame.setVisible(false); showMain(); }),
                    makeSep(),
                    makeTrayMenuItem(t("tray.exit"), () -> { trayMenuFrame.setVisible(false); doExit(); })
            );

            javafx.embed.swing.JFXPanel fxPanel = new javafx.embed.swing.JFXPanel();
            trayMenuFrame.getContentPane().add(fxPanel);
            trayMenuFrame.setSize(90, 130);

            javafx.application.Platform.runLater(() -> {
                Scene scene = new Scene(box);
                scene.setFill(null);
                fxPanel.setScene(scene);
            });

            // 失去焦点时自动关闭
            trayMenuFrame.addWindowFocusListener(new java.awt.event.WindowAdapter() {
                @Override
                public void windowLostFocus(java.awt.event.WindowEvent e) {
                    trayMenuFrame.setVisible(false);
                }
            });
        }

        // 定位到鼠标位置（向上展开）
        trayMenuFrame.setLocation(screenX - 120, screenY - 140);
        trayMenuFrame.setVisible(true);
    }

    private static javafx.scene.control.Label makeTrayMenuItem(String text, Runnable action) {
        javafx.scene.control.Label item = new javafx.scene.control.Label(text);
        item.setStyle("-fx-text-fill: #E0E0E0; -fx-font-size: 13px; -fx-padding: 8 24 8 16; -fx-cursor: hand;");
        item.setOnMouseEntered(e -> item.setStyle("-fx-text-fill: white; -fx-font-size: 13px; -fx-padding: 8 24 8 16; -fx-background-color: #4F6BF6; -fx-cursor: hand;"));
        item.setOnMouseExited(e -> item.setStyle("-fx-text-fill: #E0E0E0; -fx-font-size: 13px; -fx-padding: 8 24 8 16; -fx-cursor: hand;"));
        item.setOnMouseClicked(e -> action.run());
        return item;
    }

    private static javafx.scene.Node makeSep() {
        javafx.scene.control.Separator sep = new javafx.scene.control.Separator();
        sep.setStyle("-fx-padding: 2 8;");
        return sep;
    }



    // ===== 主界面/小窗切换 =====
    public static void showMain() {
        Platform.runLater(() -> {
            // 隐藏小窗
            MiniFrameController.hide();
            // 显示主界面
            if (primaryStage != null) {
                primaryStage.show();
                primaryStage.toFront();
                primaryStage.requestFocus();
            }
            log.info("切换到主界面");
        });
    }

    public static void hideMain() {
        if (primaryStage != null) {
            primaryStage.hide();
        }
    }

    public static void showMini() {
        Platform.runLater(() -> {
            // 隐藏主界面
            hideMain();
            // 显示小窗
            MiniFrameController.show(() -> showMain());
            log.info("切换到小窗");
        });
    }

    public static void toggleMini() {
        if (MiniFrameController.isShowing()) {
            showMain();
        } else {
            showMini();
        }
    }

    // ===== 退出 =====
    private static void doExit() {
        log.info("应用退出");
        MiniFrameController.destroy();
        ReminderScheduler.getInstance().stop();
        DatabaseManager.getInstance().close();
        // 移除托盘图标
        if (trayIcon != null) {
            try { SystemTray.getSystemTray().remove(trayIcon); } catch (Exception ignored) {}
        }
        Platform.exit();
        System.exit(0);
    }

    public static Stage getPrimaryStage() { return primaryStage; }
    public static boolean isCloseToTray() { return closeToTray; }
    public static void setCloseToTray(boolean value) { closeToTray = value; }

    public static void main(String[] args) {
        // 确保 AWT 原生菜单能正确渲染中文（Windows 中文环境必须）
        System.setProperty("file.encoding", "GBK");
        System.setProperty("sun.jnu.encoding", "GBK");
        launch(args);
    }
}
