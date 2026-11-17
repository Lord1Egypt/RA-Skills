package com.teamtodo.util;

import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;
import java.lang.ref.WeakReference;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Consumer;

/**
 * 国际化工具：StringProperty 绑定模式。
 * 用法：label.textProperty().bind(I18n.text("key"));
 * 语言切换时所有绑定自动更新。
 */
public final class I18n {
    private I18n() {}

    private static final Map<String, String> texts = new LinkedHashMap<>();
    private static String currentLang = "zh";
    private static final List<Consumer<String>> listeners = new CopyOnWriteArrayList<>();

    /** 绑定项：key + 弱引用 property；控件解绑后 property 被回收，自动跳过，避免无限累积 */
    private static final List<Binding> bindings = new CopyOnWriteArrayList<>();

    private static final class Binding {
        final String key;
        final Object[] args;
        final WeakReference<StringProperty> ref;
        Binding(String key, Object[] args, StringProperty prop) {
            this.key = key;
            this.args = args == null ? null : args.clone();
            this.ref = new WeakReference<>(prop);
        }
        void refresh(Map<String, String> t) {
            StringProperty p = ref.get();
            if (p == null) return;
            String fmt = t.getOrDefault(key, key);
            if (args == null || args.length == 0) {
                p.set(fmt);
            } else {
                try { p.set(String.format(fmt, args)); } catch (Exception ex) { p.set(fmt); }
            }
        }
    }

    public static final List<String> LANGS = List.of("zh", "zh_tw", "en", "ja", "ko", "fr", "de", "es", "pt");
    public static final Map<String, String> LANG_NAMES = Map.ofEntries(
        Map.entry("zh", "简体中文"), Map.entry("zh_tw", "繁體中文"),
        Map.entry("en", "English"), Map.entry("ja", "日本語"),
        Map.entry("ko", "조선어"), Map.entry("fr", "Français"),
        Map.entry("de", "Deutsch"), Map.entry("es", "Español"),
        Map.entry("pt", "Português")
    );

    public static String getCurrentLang() { return currentLang; }

    /** 注册语言切换监听器 */
    public static void onLangChange(Consumer<String> listener) { listeners.add(listener); }

    /** 初始化 */
    public static void init() { load(currentLang); }

    /** 切换语言 */
    public static void setLang(String lang) {
        if (!LANGS.contains(lang)) return;
        currentLang = lang;
        load(lang);
        refreshBindings();
        // 通知所有监听器
        for (Consumer<String> l : listeners) l.accept(lang);
    }

    /** 刷新所有已绑定 StringProperty（清理失效弱引用） */
    private static void refreshBindings() {
        List<Binding> stale = new ArrayList<>();
        for (Binding b : bindings) {
            if (b.ref.get() == null) { stale.add(b); continue; }
            b.refresh(texts);
        }
        if (!stale.isEmpty()) bindings.removeAll(stale);
    }

    /** 获取文本 */
    public static String t(String key) { return texts.getOrDefault(key, key); }

    /** 获取文本并格式化 */
    public static String t(String key, Object... args) {
        String fmt = texts.getOrDefault(key, key);
        try { return String.format(fmt, args); } catch (Exception e) { return fmt; }
    }

    /** 判断某 key 是否存在翻译 */
    public static boolean hasKey(String key) { return texts.containsKey(key); }

    /**
     * 返回一个 StringProperty，绑定到指定 key。
     * 语言切换时自动更新值。
     * 用法：label.textProperty().bind(I18n.text("key"));
     */
    public static StringProperty text(String key) {
        SimpleStringProperty prop = new SimpleStringProperty(texts.getOrDefault(key, key));
        bindings.add(new Binding(key, null, prop));
        return prop;
    }

    /**
     * 返回一个 StringProperty，绑定到带参数的 key。
     * 语言切换时自动用当前参数重新格式化。
     */
    public static StringProperty textf(String key, Object... args) {
        String fmt = texts.getOrDefault(key, key);
        SimpleStringProperty prop;
        try { prop = new SimpleStringProperty(String.format(fmt, args)); }
        catch (Exception e) { prop = new SimpleStringProperty(fmt); }
        bindings.add(new Binding(key, args, prop));
        return prop;
    }

    /** 加载 properties 文件 */
    private static void load(String lang) {
        texts.clear();
        String path = "/i18n/texts_" + lang + ".properties";
        try (var is = I18n.class.getResourceAsStream(path)) {
            if (is != null) {
                var props = new Properties();
                props.load(new java.io.InputStreamReader(is, java.nio.charset.StandardCharsets.UTF_8));
                for (var e : props.entrySet()) texts.put((String) e.getKey(), (String) e.getValue());
            }
        } catch (Exception e) {
            System.err.println("[I18n] load " + path + " failed: " + e.getMessage());
        }
        // 回退中文
        if (!"zh".equals(lang)) {
            try (var is = I18n.class.getResourceAsStream("/i18n/texts_zh.properties")) {
                if (is != null) {
                    var props = new Properties();
                    props.load(new java.io.InputStreamReader(is, java.nio.charset.StandardCharsets.UTF_8));
                    for (var e : props.entrySet()) texts.putIfAbsent((String) e.getKey(), (String) e.getValue());
                }
            } catch (Exception ignored) {}
        }
    }
}
