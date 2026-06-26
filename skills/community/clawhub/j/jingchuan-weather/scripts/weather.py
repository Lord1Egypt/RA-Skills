# -*- coding: utf-8 -*-
# 泾川县天气预报查询脚本
# 获取7天天气预报和日出日落时间

import urllib.request
import json
import sys
import io

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 泾川县坐标
lat = 35.51
lon = 107.36

def get_weather_and_sun():
    """获取天气和日出日落数据"""
    import ssl
    import urllib.error
    
    # 天气和日出日落API
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&timezone=Asia/Shanghai&forecast_days=7'
    
    # 创建不验证SSL的上下文
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5'})
    
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        return data
    except Exception as e:
        # 如果SSL失败，尝试使用http
        url_http = url.replace('https://', 'http://')
        req = urllib.request.Request(url_http, headers={'User-Agent': 'Mozilla/5'})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        return data

def get_weather_desc(code):
    """将天气代码转换为中文描述"""
    weather_codes = {
        0: '☀️ 晴',
        1: '🌤️ 晴间多云', 
        2: '⛅ 多云',
        3: '☁️ 阴',
        45: '🌫️ 雾',
        48: '🌫️ 雾',
        51: '🌧️ 小雨',
        53: '🌧️ 中雨',
        55: '🌧️ 大雨',
        61: '🌧️ 小雨',
        63: '🌧️ 中雨',
        65: '🌧️ 大雨',
        71: '🌨️ 小雪',
        73: '🌨️ 中雪',
        75: '🌨️ 大雪',
        80: '🌧️ 阵雨',
        81: '🌧️ 强阵雨',
        82: '🌧️ 强阵雨',
        85: '🌨️ 雨夹雪',
        95: '⛈️ 雷暴',
        96: '⛈️ 雷暴+冰雹'
    }
    return weather_codes.get(code, f'🌡️ {code}')

def format_weather():
    """格式化天气输出"""
    data = get_weather_and_sun()
    
    output = []
    output.append("=" * 60)
    output.append("🌤️  甘肃省泾川县 - 7天天气预报  🌤️")
    output.append("=" * 60)
    output.append("")
    
    # 星期映射
    week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    days = data['daily']['time']
    maxTemps = data['daily']['temperature_2m_max']
    minTemps = data['daily']['temperature_2m_min']
    codes = data['daily']['weather_code']
    precip = data['daily']['precipitation_probability_max']
    sunrises = data['daily']['sunrise']
    sunsets = data['daily']['sunset']
    
    # 表格标题
    output.append(f"{'日期':<8} {'天气':<12} {'最高':<8} {'最低':<8} {'降雨':<6} {'日出':<8} {'日落':<8}")
    output.append("-" * 60)
    
    for i in range(len(days)):
        date = days[i][5:]  # 月-日
        code = codes[i]
        weather = get_weather_desc(code)
        high = maxTemps[i]
        low = minTemps[i]
        rain = precip[i]
        
        # 处理日出日落时间
        sunrise = sunrises[i][11:16] if len(sunrises[i]) > 16 else sunrises[i][-5:]
        sunset = sunsets[i][11:16] if len(sunsets[i]) > 16 else sunsets[i][-5:]
        
        output.append(f"{date:<8} {weather:<12} {high}°C{'':<3} {low}°C{'':<3} {rain}%{'':<3} {sunrise}{'':<2} {sunset}")
    
    output.append("")
    output.append("=" * 60)
    
    # 今日信息
    today_code = codes[0]
    today_precip = precip[0]
    today_sunrise = sunrises[0][11:16]
    today_sunset = sunsets[0][11:16]
    
    output.append("📅 今日信息")
    output.append("-" * 40)
    output.append(f"   日出时间: {today_sunrise}")
    output.append(f"   日落时间: {today_sunset}")
    output.append(f"   天气状况: {get_weather_desc(today_code)}")
    output.append(f"   降雨概率: {today_precip}%")
    output.append("")
    
    # 总结建议
    output.append("📝 出行建议")
    output.append("-" * 40)
    
    # 分析天气
    rain_days = sum(1 for p in precip if p > 30)
    max_temp = max(maxTemps)
    min_temp = min(minTemps)
    
    output.append(f"   • 未来7天温度范围: {min_temp}°C ~ {max_temp}°C")
    
    if rain_days > 0:
        output.append(f"   • 有{rain_days}天可能有降雨，建议带伞 ☔")
    else:
        output.append("   • 未来7天无明显降雨天气")
    
    # 温差建议
    temp_range = maxTemps[0] - minTemps[0]
    if temp_range > 10:
        output.append(f"   • 今日温差较大({temp_range}°C)，建议带外套 🧥")
    
    output.append("   • 泾川位于甘肃省东部，温带半干旱气候")
    output.append("   • 春季干燥，注意补水 💧")
    output.append("")
    output.append("=" * 60)
    output.append("数据来源: Open-Meteo API | 泾川县坐标: 35.51°N, 107.36°E")
    
    return "\n".join(output)

if __name__ == "__main__":
    print(format_weather())
