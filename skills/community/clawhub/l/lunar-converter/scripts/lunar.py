#!/usr/bin/env python3
"""
阴历阳历转换工具
使用 lunardate 库，支持 1900-2100 年
"""

import sys
import json

def lunar_to_solar(year, month, day, is_leap=False):
    """阴历转阳历"""
    try:
        from lunardate import LunarDate
        ld = LunarDate(year, month, day, is_leap)
        solar = ld.toSolarDate()
        return f"{solar.year}-{solar.month:02d}-{solar.day:02d}"
    except Exception as e:
        return f"错误: {str(e)}"

def solar_to_lunar(year, month, day):
    """阳历转阴历"""
    try:
        from lunardate import LunarDate
        ld = LunarDate.fromSolarDate(year, month, day)
        # 构建阴历日期字符串
        month_names = ['', '正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月']
        day_names = ['', '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                     '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                     '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
        
        month_str = month_names[ld.month]
        if ld.isLeapMonth:
            month_str = f"闰{month_str}"
        
        return f"{ld.year}年{month_str}{day_names[ld.day]}"
    except Exception as e:
        return f"错误: {str(e)}"

def main():
    if len(sys.argv) < 4:
        print(json.dumps({
            "usage": "python lunar.py <操作> <年份> <月份> [日期]", 
            "example": [
                "python lunar.py lunar2solar 2026 2 12",
                "python lunar.py solar2lunar 2026 3 30"
            ]
        }))
        print("操作:")
        print("  lunar2solar <年> <月> <日>  # 阴历转阳历")
        print("  solar2lunar <年> <月> <日>  # 阳历转阴历")
        sys.exit(1)
    
    operation = sys.argv[1]
    
    try:
        year = int(sys.argv[2])
        month = int(sys.argv[3])
        day = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    except ValueError:
        print(json.dumps({"error": "参数必须是数字"}))
        sys.exit(1)
    
    if operation == "lunar2solar":
        result = lunar_to_solar(year, month, day)
    elif operation == "solar2lunar":
        result = solar_to_lunar(year, month, day)
    else:
        result = f"未知操作: {operation}"
    
    print(json.dumps({"result": result}))

if __name__ == "__main__":
    main()
