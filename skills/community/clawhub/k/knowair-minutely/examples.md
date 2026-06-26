# Examples — knowair-minutely

## Will it rain soon in Beijing?

**User:** Should I bring an umbrella? I'm in Beijing.

**Command:**
```bash
python3 scripts/query_minutely.py --lng 116.3176 --lat 39.9760
```

**Response style:** Use the API's description field directly (e.g., "Light rain will start in 15 minutes and last about 30 minutes"). Add probability data if useful.

## 上海未来两小时会下雨吗？

**User:** 上海接下来两小时有雨吗？

**Command:**
```bash
python3 scripts/query_minutely.py --lng 121.4737 --lat 31.2304 --lang zh
```

**Response style:** 直接使用 API 返回的描述（如"未来两小时无降水"），并补充概率数据。
