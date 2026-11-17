package com.teamtodo.util;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 自然语言日期解析器 - 支持中文日期表达
 * 
 * 支持：今天、明天、后天、大后天、下周X、X天后、X月X日、yyyy-MM-dd
 */
public class NaturalDateParser {
    private static final Pattern RELATIVE_DAYS = Pattern.compile("(\\d+)天后");
    private static final Pattern MONTH_DAY = Pattern.compile("(\\d{1,2})月(\\d{1,2})[日号]?");
    private static final Pattern NEXT_WEEK = Pattern.compile("下周([一二三四五六日天])");
    private static final Pattern ISO_DATE = Pattern.compile("(\\d{4})-(\\d{1,2})-(\\d{1,2})");

    /**
     * 解析自然语言日期
     * @param input 输入文本，如"明天"、"3天后"、"8月25日"
     * @return 解析后的日期字符串 (yyyy-MM-dd)，无法解析返回 null
     */
    public static String parse(String input) {
        if (input == null || input.isBlank()) return null;
        String text = input.trim().toLowerCase();

        // 今天/明天/后天
        switch (text) {
            case "今天": case "今日": return LocalDate.now().toString();
            case "明天": case "明日": return LocalDate.now().plusDays(1).toString();
            case "后天": return LocalDate.now().plusDays(2).toString();
            case "大后天": return LocalDate.now().plusDays(3).toString();
            case "昨天": return LocalDate.now().minusDays(1).toString();
            case "大前天": return LocalDate.now().minusDays(3).toString();
        }

        // X天后
        Matcher m1 = RELATIVE_DAYS.matcher(text);
        if (m1.find()) {
            int days = Integer.parseInt(m1.group(1));
            return LocalDate.now().plusDays(days).toString();
        }

        // 下周X
        Matcher m2 = NEXT_WEEK.matcher(text);
        if (m2.find()) {
            return parseNextWeek(m2.group(1));
        }

        // X月X日
        Matcher m3 = MONTH_DAY.matcher(text);
        if (m3.find()) {
            int month = Integer.parseInt(m3.group(1));
            int day = Integer.parseInt(m3.group(2));
            LocalDate date = LocalDate.now().withMonth(month).withDayOfMonth(day);
            if (date.isBefore(LocalDate.now())) date = date.plusYears(1);
            return date.toString();
        }

        // yyyy-MM-dd
        Matcher m4 = ISO_DATE.matcher(text);
        if (m4.find()) {
            return String.format("%s-%02d-%02d",
                    m4.group(1),
                    Integer.parseInt(m4.group(2)),
                    Integer.parseInt(m4.group(3)));
        }

        return null;
    }

    private static String parseNextWeek(String dayChar) {
        int targetDay;
        switch (dayChar) {
            case "一": targetDay = 1; break;
            case "二": targetDay = 2; break;
            case "三": targetDay = 3; break;
            case "四": targetDay = 4; break;
            case "五": targetDay = 5; break;
            case "六": targetDay = 6; break;
            case "日": case "天": targetDay = 7; break;
            default: return null;
        }
        LocalDate today = LocalDate.now();
        int currentDay = today.getDayOfWeek().getValue();
        int daysUntil = (targetDay - currentDay + 7) % 7;
        if (daysUntil == 0) daysUntil = 7; // 下周的同一天
        return today.plusDays(daysUntil).toString();
    }

    /**
     * 从输入文本中提取日期和清理后的标题
     * @param input 原始输入，如"买菜 明天"
     * @return [清理后的标题, 日期] 或 [原始输入, null]
     */
    public static String[] extractDate(String input) {
        if (input == null || input.isBlank()) return new String[]{input, null};

        // 尝试从末尾提取日期
        String[] parts = input.trim().split("\\s+");
        if (parts.length >= 2) {
            String lastPart = parts[parts.length - 1];
            String date = parse(lastPart);
            if (date != null) {
                String title = String.join(" ", java.util.Arrays.copyOf(parts, parts.length - 1));
                return new String[]{title, date};
            }
        }

        // 尝试从开头提取日期
        if (parts.length >= 2) {
            String firstPart = parts[0];
            String date = parse(firstPart);
            if (date != null) {
                String title = String.join(" ", java.util.Arrays.copyOfRange(parts, 1, parts.length));
                return new String[]{title, date};
            }
        }

        return new String[]{input, null};
    }
}
