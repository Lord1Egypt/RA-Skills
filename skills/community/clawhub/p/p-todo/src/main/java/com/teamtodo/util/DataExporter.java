package com.teamtodo.util;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonSerializer;
import com.teamtodo.model.Todo;
import com.teamtodo.service.TodoService;
import com.teamtodo.util.I18n;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

/**
 * 数据导出工具 - 支持 JSON 和 CSV 格式
 */
public class DataExporter {
    private static final Logger log = LoggerFactory.getLogger(DataExporter.class);
    private static final Gson gson = new GsonBuilder()
            .registerTypeAdapter(LocalDateTime.class, (JsonSerializer<LocalDateTime>) (src, type, ctx) ->
                    ctx.serialize(src.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)))
            .registerTypeAdapter(LocalDateTime.class, (JsonDeserializer<LocalDateTime>) (json, type, ctx) ->
                    LocalDateTime.parse(json.getAsString(), DateTimeFormatter.ISO_LOCAL_DATE_TIME))
            .setPrettyPrinting()
            .create();

    /**
     * 导出为 JSON 文件
     */
    public static File exportJson(File file) throws IOException {
        TodoService service = new TodoService();
        List<Todo> todos = service.listAll();
        try (Writer writer = new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8)) {
            gson.toJson(todos, writer);
            log.info("已导出 JSON: {} ({} 条)", file.getAbsolutePath(), todos.size());
        }
        return file;
    }

    /**
     * 导出为 CSV 文件
     */
    public static File exportCsv(File file) throws IOException {
        TodoService service = new TodoService();
        List<Todo> todos = service.listAll();
        try (PrintWriter pw = new PrintWriter(new OutputStreamWriter(new FileOutputStream(file), StandardCharsets.UTF_8))) {
            pw.println(I18n.t("csv.header"));
            for (Todo t : todos) {
                pw.printf("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"%n",
                        escape(t.getTitle()),
                        t.getStatus() != null ? t.getStatus().getLabel() : "",
                        t.getPriority() != null ? t.getPriority().getLabel() : "",
                        t.getDueDate() != null ? t.getDueDate() : "",
                        t.isCompleted() ? I18n.t("csv.yes") : I18n.t("csv.no"),
                        t.getCreatedAt() != null ? t.getCreatedAt().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")) : "",
                        escape(t.getDescription() != null ? t.getDescription() : ""));
            }
            log.info("已导出 CSV: {} ({} 条)", file.getAbsolutePath(), todos.size());
        }
        return file;
    }

    private static String escape(String s) {
        if (s == null) return "";
        return s.replace("\"", "\"\"").replace("\n", " ").replace("\r", "");
    }
}
