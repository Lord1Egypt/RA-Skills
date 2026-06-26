#!/usr/bin/env node

/**
 * Skill: AQI Vietnam (JS Version)
 * Author: YourName (Solution Architect style)
 * Chức năng: Lấy dữ liệu AQI thời gian thực từ WAQI API.
 */

const https = require('https');

const WAQI_TOKEN = "506d32bec697548ee2d316c54605042dbec5d86a";

// Mapping thành phố tiếng Việt -> Slug API
const cityMap = {
    "hanoi": "hanoi", "hà nội": "hanoi", "hn": "hanoi",
    "hochiminh": "hochiminh", "hồ chí minh": "hochiminh", "hcm": "hochiminh", "saigon": "hochiminh",
    "danang": "danang", "đà nẵng": "danang", "dn": "danang",
    "haiphong": "haiphong", "hải phòng": "haiphong", "hp": "haiphong",
    "cantho": "cantho", "cần thơ": "cantho", "ct": "cantho"
};

const getCategory = (aqi) => {
    if (aqi <= 50) return { label: "Tốt", emoji: "🟢" };
    if (aqi <= 100) return { label: "Trung bình", emoji: "🟡" };
    if (aqi <= 150) return { label: "Kém (Nhạy cảm)", emoji: "🟠" };
    if (aqi <= 200) return { label: "Xấu", emoji: "🔴" };
    if (aqi <= 300) return { label: "Rất xấu", emoji: "🟣" };
    return { label: "Nguy hiểm", emoji: "🟤" };
};

function fetchAQI(cityInput) {
    const citySlug = cityMap[cityInput.toLowerCase()] || cityInput.toLowerCase();
    const url = `https://api.waqi.info/feed/${encodeURIComponent(citySlug)}/?token=${WAQI_TOKEN}`;

    https.get(url, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
            try {
                const json = JSON.parse(data);
                if (json.status !== "ok") throw new Error(json.data || "City not found");

                const d = json.data;
                const cat = getCategory(d.aqi);
                
                const result = {
                    status: "success",
                    city: d.city.name,
                    aqi: d.aqi,
                    level: cat.label,
                    emoji: cat.emoji,
                    weather: {
                        temp: d.iaqi.t?.v || 0,
                        humidity: d.iaqi.h?.v || 0,
                        wind: d.iaqi.w?.v || 0
                    },
                    pollutants: {
                        main: d.dominentpol || "n/a"
                    },
                    updated_at: d.time.s
                };

                console.log(JSON.stringify(result, null, 2));
            } catch (err) {
                console.log(JSON.stringify({ status: "error", message: err.message }));
            }
        });
    }).on('error', (err) => {
        console.log(JSON.stringify({ status: "error", message: err.message }));
    });
}

// Chạy script với tham số đầu vào
const input = process.argv[2] || 'hanoi';
fetchAQI(input);
