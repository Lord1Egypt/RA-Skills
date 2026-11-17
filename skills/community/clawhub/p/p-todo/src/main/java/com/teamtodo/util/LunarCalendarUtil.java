package com.teamtodo.util;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * 农历（Chinese calendar）转换工具类（查表法，1900-2100 年）。
 * <p>
 * 数据格式（LUNAR_INFO 每一项为十六进制数）：
 * - bit 0-3   : 闰月月份（0 表示无闰月）
 * - bit 4-15  : 1-12 月，1 = 大月(30天)，0 = 小月(29天)
 * - bit 16    : 闰月大小（1=30天，0=29天）
 * <p>
 * 数据源：jjonline/calendar.js（含 2057 年修正），基准 1900-01-31 = 农历 1900 年正月初一。
 */
public final class LunarCalendarUtil {

    /** 基准日期：1900-01-31 = 农历 1900 年正月初一 */
    private static final LocalDate BASE_DATE = LocalDate.of(1900, 1, 31);

    private static final int MIN_YEAR = 1900;
    private static final int MAX_YEAR = 2100;

    /** 农历数据表 1900-2100（共 201 项） */
    private static final int[] LUNAR_INFO = {
            0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2, // 1900-1909
            0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977, // 1910-1919
            0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970, // 1920-1929
            0x06566, 0x0d4a0, 0x0ea50, 0x16a95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950, // 1930-1939
            0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557, // 1940-1949
            0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0, // 1950-1959
            0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0, // 1960-1969
            0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6, // 1970-1979
            0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570, // 1980-1989
            0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x05ac0, 0x0ab60, 0x096d5, 0x092e0, // 1990-1999
            0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5, // 2000-2009
            0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930, // 2010-2019
            0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530, // 2020-2029
            0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45, // 2030-2039
            0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0, // 2040-2049
            0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06aa0, 0x1a6c4, 0x0aae0, // 2050-2059
            0x092e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4, // 2060-2069
            0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0, // 2070-2079
            0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160, // 2080-2089
            0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252, // 2090-2099
            0x0d520, 0x0db27, 0x0b5a0, 0x055d0, 0x04db5, 0x049b0, 0x0a4b0, 0x0d4b4, 0x0aa50, 0x0b559  // 2100
    };

    private static final String[] LUNAR_MONTHS = {
            "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"
    };

    /** 繁体中文月名（zh_tw） */
    private static final String[] LUNAR_MONTHS_TW = {
            "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "臘"
    };

    private static final String[] LUNAR_DAYS = {
            "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
            "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
            "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
    };

    /** 农历传统节日 "月-日" → 名称（简体） */
    private static final Map<String, String> LUNAR_FESTIVALS = new LinkedHashMap<>();
    /** 农历传统节日 "月-日" → 名称（繁体 zh_tw） */
    private static final Map<String, String> LUNAR_FESTIVALS_TW = new LinkedHashMap<>();
    /** 公历节日 "月-日" → 名称（简体） */
    private static final Map<String, String> SOLAR_FESTIVALS = new LinkedHashMap<>();
    /** 公历节日 "月-日" → 名称（繁体 zh_tw） */
    private static final Map<String, String> SOLAR_FESTIVALS_TW = new LinkedHashMap<>();

    static {
        LUNAR_FESTIVALS.put("1-1", "春节");
        LUNAR_FESTIVALS.put("1-15", "元宵");
        LUNAR_FESTIVALS.put("5-5", "端午");
        LUNAR_FESTIVALS.put("7-7", "七夕");
        LUNAR_FESTIVALS.put("8-15", "中秋");
        LUNAR_FESTIVALS.put("9-9", "重阳");
        LUNAR_FESTIVALS.put("12-8", "腊八");
        LUNAR_FESTIVALS.put("12-23", "小年");

        LUNAR_FESTIVALS_TW.put("1-1", "春節");
        LUNAR_FESTIVALS_TW.put("1-15", "元宵");
        LUNAR_FESTIVALS_TW.put("5-5", "端午");
        LUNAR_FESTIVALS_TW.put("7-7", "七夕");
        LUNAR_FESTIVALS_TW.put("8-15", "中秋");
        LUNAR_FESTIVALS_TW.put("9-9", "重陽");
        LUNAR_FESTIVALS_TW.put("12-8", "臘八");
        LUNAR_FESTIVALS_TW.put("12-23", "小年");

        SOLAR_FESTIVALS.put("1-1", "元旦");
        SOLAR_FESTIVALS.put("2-14", "情人节");
        SOLAR_FESTIVALS.put("3-8", "妇女节");
        SOLAR_FESTIVALS.put("3-12", "植树节");
        SOLAR_FESTIVALS.put("4-1", "愚人节");
        SOLAR_FESTIVALS.put("4-4", "清明节");
        SOLAR_FESTIVALS.put("4-5", "清明节");
        SOLAR_FESTIVALS.put("5-1", "劳动节");
        SOLAR_FESTIVALS.put("5-4", "青年节");
        SOLAR_FESTIVALS.put("6-1", "儿童节");
        SOLAR_FESTIVALS.put("7-1", "建党节");
        SOLAR_FESTIVALS.put("8-1", "建军节");
        SOLAR_FESTIVALS.put("9-10", "教师节");
        SOLAR_FESTIVALS.put("10-1", "国庆节");
        SOLAR_FESTIVALS.put("12-24", "平安夜");
        SOLAR_FESTIVALS.put("12-25", "圣诞节");

        SOLAR_FESTIVALS_TW.put("1-1", "元旦");
        SOLAR_FESTIVALS_TW.put("2-14", "情人節");
        SOLAR_FESTIVALS_TW.put("3-8", "婦女節");
        SOLAR_FESTIVALS_TW.put("3-12", "植樹節");
        SOLAR_FESTIVALS_TW.put("4-1", "愚人節");
        SOLAR_FESTIVALS_TW.put("4-4", "清明節");
        SOLAR_FESTIVALS_TW.put("4-5", "清明節");
        SOLAR_FESTIVALS_TW.put("5-1", "勞動節");
        SOLAR_FESTIVALS_TW.put("5-4", "青年節");
        SOLAR_FESTIVALS_TW.put("6-1", "兒童節");
        SOLAR_FESTIVALS_TW.put("7-1", "建黨節");
        SOLAR_FESTIVALS_TW.put("8-1", "建軍節");
        SOLAR_FESTIVALS_TW.put("9-10", "教師節");
        SOLAR_FESTIVALS_TW.put("10-1", "國慶節");
        SOLAR_FESTIVALS_TW.put("12-24", "平安夜");
        SOLAR_FESTIVALS_TW.put("12-25", "聖誕節");
    }

    private LunarCalendarUtil() {
    }

    // ===== 对外方法 =====

    /**
     * 返回公历日期对应的农历日期文字（如 "腊月廿九"、"闰六月廿四"）。
     * 简体中文返回简体，繁体中文（zh_tw）返回繁体，其他语言返回 null（不显示农历）。
     *
     * @param date 公历日期
     * @return 农历日期文字；超出支持范围（1900-2100）或非中文语言返回 null
     */
    public static String getLunarText(LocalDate date) {
        String lang = I18n.getCurrentLang();
        if (!"zh".equals(lang) && !"zh_tw".equals(lang)) return null;
        int[] ymd = solarToLunar(date);
        if (ymd == null) return null;
        int m = ymd[1]; // 负数表示闰月
        int d = ymd[2];
        String leap = "zh_tw".equals(lang) ? "閏" : "闰";
        String[] months = "zh_tw".equals(lang) ? LUNAR_MONTHS_TW : LUNAR_MONTHS;
        return (m < 0 ? leap : "") + months[Math.abs(m) - 1] + "月" + LUNAR_DAYS[d - 1];
    }

    /**
     * 返回公历日期对应的节日名称。
     * 优先级：除夕 > 农历节日 > 公历节日。
     * 简体中文返回简体，繁体中文（zh_tw）返回繁体，其他语言返回 null（不显示节日）。
     *
     * @param date 公历日期
     * @return 节日名称（如 "春节"、"中秋"）；无节日或非中文语言返回 null
     */
    public static String getFestival(LocalDate date) {
        String lang = I18n.getCurrentLang();
        if (!"zh".equals(lang) && !"zh_tw".equals(lang)) return null;
        boolean tw = "zh_tw".equals(lang);
        // 除夕：次日为农历正月初一
        LocalDate next = date.plusDays(1);
        int[] nextYmd = solarToLunar(next);
        if (nextYmd != null && nextYmd[1] == 1 && nextYmd[2] == 1) {
            return tw ? "除夕" : "除夕";
        }
        int[] ymd = solarToLunar(date);
        if (ymd != null) {
            Map<String, String> lunar = tw ? LUNAR_FESTIVALS_TW : LUNAR_FESTIVALS;
            String name = lunar.get(Math.abs(ymd[1]) + "-" + ymd[2]);
            if (name != null) return name;
        }
        Map<String, String> solar = tw ? SOLAR_FESTIVALS_TW : SOLAR_FESTIVALS;
        return solar.get(date.getMonthValue() + "-" + date.getDayOfMonth());
    }

    /** 返回某农历年的生肖文字（如 "马"）；非中文语言返回英文生肖。 */
    public static String getZodiac(int lunarYear) {
        String lang = I18n.getCurrentLang();
        String[] zodiacs;
        if ("zh".equals(lang)) {
            zodiacs = new String[]{"鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"};
        } else if ("zh_tw".equals(lang)) {
            zodiacs = new String[]{"鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"};
        } else {
            zodiacs = new String[]{"Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"};
        }
        int idx = (lunarYear - 4) % 12;
        if (idx < 0) idx += 12;
        return zodiacs[idx];
    }

    // ===== 核心：公历 → 农历（查表法） =====

    /**
     * @return int[3] {农历年, 农历月(负数=闰月), 农历日}；超出范围返回 null
     */
    private static int[] solarToLunar(LocalDate date) {
        long offset = ChronoUnit.DAYS.between(BASE_DATE, date);
        if (offset < 0) return null;

        int yearIdx = 0;
        int remain = (int) offset;
        while (yearIdx < LUNAR_INFO.length - 1) {
            int days = daysInLunarYear(yearIdx);
            if (remain < days) break;
            remain -= days;
            yearIdx++;
        }
        if (yearIdx >= LUNAR_INFO.length) return null;
        int lunarYear = MIN_YEAR + yearIdx;
        if (lunarYear > MAX_YEAR) return null;

        int leapMonth = LUNAR_INFO[yearIdx] & 0xf; // 0 = 无闰月
        int m = 1;
        boolean inLeap = false;
        while (true) {
            if (inLeap) {
                int ld = leapDaysOf(yearIdx);
                if (remain < ld) break; // 落在闰月内
                remain -= ld;
                inLeap = false;
                m++;
                continue;
            }
            if (m > 12) break;
            int days = monthDaysOf(yearIdx, m);
            if (remain < days) break; // 落在本月内
            remain -= days;
            if (leapMonth == m) {
                inLeap = true; // 本月之后紧跟闰月
            } else {
                m++;
            }
        }

        int month = inLeap ? -leapMonth : m;
        return new int[]{lunarYear, month, remain + 1};
    }

    /** 某农历年（表索引）总天数 */
    private static int daysInLunarYear(int yearIdx) {
        int sum = 348; // 12 × 29
        int info = LUNAR_INFO[yearIdx];
        for (int bit = 0x8000; bit > 0x8; bit >>= 1) {
            if ((info & bit) != 0) sum++;
        }
        if ((info & 0xf) != 0) sum += leapDaysOf(yearIdx);
        return sum;
    }

    /** 某农历年闰月天数（0=无闰月） */
    private static int leapDaysOf(int yearIdx) {
        return ((LUNAR_INFO[yearIdx] & 0x10000) != 0) ? 30 : 29;
    }

    /** 某农历年某月（1-12）天数 */
    private static int monthDaysOf(int yearIdx, int month) {
        return ((LUNAR_INFO[yearIdx] & (0x10000 >> month)) != 0) ? 30 : 29;
    }
}
