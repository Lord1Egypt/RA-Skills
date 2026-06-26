#!/usr/bin/env node

/**
 * Âm Lịch Việt Nam Calculator - Giao diện dòng lệnh cho OpenClaw Skill
 * 
 * Usage:
 *   node amlich_calculator.js --solar YYYY-MM-DD
 *   node amlich_calculator.js --lunar "YYYY-MM-DD"
 */

const amlich = require('../amlich.js');
const argv = require('minimist')(process.argv.slice(2));

// 12 Con Giáp của Việt Nam (Sử dụng Mão = Mèo thay vì Thỏ của TQ)
const ZODIAC_VN = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"];

// Hàm lấy tên tiết khí
function getSolarTerm(solarDateStr) {
    try {
        const parts = solarDateStr.split('-');
        const monthDay = `${parts[1]}-${parts[2]}`;
        for (const [term, date] of Object.entries(amlich.SOLAR_TERMS)) {
            if (date === monthDay) {
                return {
                    "name": term,
                    "date": solarDateStr,
                    "approx_time": "Thời gian giao tiết khí mang tính chất tham khảo tương đối"
                };
            }
        }
    } catch (e) {
        // ignore
    }
    return null;
}

// Xử lý --solar
if (argv.solar) {
    try {
        const parts = argv.solar.split('-');
        if (parts.length !== 3) throw new Error("Format phải là YYYY-MM-DD");
        const yy = parseInt(parts[0], 10);
        const mm = parseInt(parts[1], 10);
        const dd = parseInt(parts[2], 10);

        const lunarDate = amlich.getLunarDate(dd, mm, yy);
        if (lunarDate.year === 0) {
            throw new Error("Ngày tháng vượt quá giới hạn hỗ trợ (1800 - 2199)");
        }

        const canChiString = amlich.getYearCanChi(lunarDate.year); // vd "Giáp Thìn"
        const dayMonthYearCanChi = amlich.getCanChi(lunarDate); // Ngày, Tháng, Năm
        const gioHoangDao = amlich.getGioHoangDao(lunarDate.jd);
        const isLeap = lunarDate.leap === 1;
        const zodiac = ZODIAC_VN[(lunarDate.year + 8) % 12];

        // Lấy danh sách ngày hoàng đạo tạm (tham khảo)
        const result = {
            solar_date: argv.solar,
            lunar_year: lunarDate.year,
            lunar_month: lunarDate.month,
            lunar_day: lunarDate.day,
            is_leap: isLeap,
            ganzhi_year: canChiString,
            zodiac: zodiac,
            day_canzhi: dayMonthYearCanChi[0],
            month_canzhi: dayMonthYearCanChi[1],
            lucky_hours: gioHoangDao,
            solar_term: getSolarTerm(argv.solar)
        };

        const withFortune = argv['with-fortune'] === 'true' || argv['with-fortune'] === true;
        if (withFortune) {
            // Placeholder logic cho fortune
            result.fortune = {
                suitable: ["Cúng tế", "Cầu phúc", "Họp mặt"],
                avoid: ["Động thổ", "Khai trương"]
            };
        }

        console.log(JSON.stringify(result, null, 2));

    } catch (e) {
        console.log(JSON.stringify({ "error": "Chuyển đổi thất bại: " + e.message }));
    }
}
else if (argv.lunar) {
    try {
        const parts = argv.lunar.split('-');
        if (parts.length !== 3) throw new Error("Format phải là YYYY-MM-DD");
        let targetYY = parseInt(parts[0], 10);
        let targetMM = parseInt(parts[1], 10);
        let targetDD = parseInt(parts[2], 10);
        let isLeapMonth = argv.leap === 'true' || argv.leap === true;

        // Vì amlich.js không hỗ trợ trực tiếp hàm chuyển ngược Âm -> Dương
        // Chúng ta tạm thời lặp từ ngày 1/1 dương để tìm:
        // Cảnh báo: Cách này brute-force đơn giản, có thể chậm.
        let found = null;
        for (let m = 1; m <= 12; m++) {
            for (let d = 1; d <= 31; d++) {
                try {
                    let res = amlich.getLunarDate(d, m, targetYY);
                    if (res.day === targetDD && res.month === targetMM && res.year === targetYY) {
                        // Kiểm tra leap
                        if (!isLeapMonth && res.leap === 0) found = `${targetYY}-${m.toString().padStart(2, '0')}-${d.toString().padStart(2, '0')}`;
                        if (isLeapMonth && res.leap === 1) found = `${targetYY}-${m.toString().padStart(2, '0')}-${d.toString().padStart(2, '0')}`;
                        if (found) break;
                    }
                    if (res.year > targetYY) break;
                } catch (e) { }
            }
            if (found) break;
        }

        if (found) {
            let resLunar = amlich.getLunarDate(parseInt(found.split('-')[2]), parseInt(found.split('-')[1]), targetYY);
            const zodiac = ZODIAC_VN[(targetYY + 8) % 12];
            console.log(JSON.stringify({
                lunar_date: `${targetYY} năm ${amlich.getYearCanChi(targetYY)} Tháng ${targetMM}${isLeapMonth ? " (Nhuận)" : ""} Ngày ${targetDD}`,
                solar_date: found,
                ganzhi_year: amlich.getYearCanChi(targetYY),
                zodiac: zodiac,
                solar_term: getSolarTerm(found)
            }, null, 2));
        } else {
            console.log(JSON.stringify({ "error": "Không tìm thấy ngày dương lịch tương ứng" }));
        }
    } catch (e) {
        console.log(JSON.stringify({ "error": "Chuyển đổi thất bại: " + e.message }));
    }
} else {
    console.log("Sử dụng: node amlich_calculator.js --solar YYYY-MM-DD");
}
