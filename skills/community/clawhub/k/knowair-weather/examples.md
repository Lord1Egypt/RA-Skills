# Examples — knowair-air-quality

## Air quality in Beijing

**User:** What's the air quality like in Beijing? Is it safe to go jogging?

**Command:**
```bash
python3 scripts/query_air_quality.py --lng 116.3176 --lat 39.9760
```

**Response style:** Report current AQI with health advice, mention the best/worst periods, and give exercise recommendation.

## 5-day AQI forecast for Shanghai

**User:** 上海未来几天空气质量怎么样？

**Command:**
```bash
python3 scripts/query_air_quality.py --lng 121.4737 --lat 31.2304 --hours 120 --lang zh
```

**Response style:** 展示当前 AQI 等级和健康建议，标出空气质量最好和最差的时段。
