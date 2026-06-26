#!/usr/bin/env python3
"""
多模态健康数据处理器
支持：PDF/Word/图片/语音/文字输入
"""

import os
import json
import re
import base64
from pathlib import Path

# 数据目录
BASE_DIR = Path(__file__).parent.parent
USERS_DIR = BASE_DIR / "data" / "users"
USERS_DIR.mkdir(parents=True, exist_ok=True)


# 关键健康指标正则模式（支持多种格式）
INDICATOR_PATTERNS = {
    # 基础指标 - 支持"身高：172cm" 或 "身高 172cm" 等格式
    "身高": r"身高[：:\s]+(\d+\.?\d*)\s*(?:cm|厘米)?",
    "体重": r"体重[：:\s]+(\d+\.?\d*)\s*(?:kg|千克|公斤)?",
    "BMI": r"BMI[：:\s]+(\d+\.?\d*)",
    "腰围": r"腰围[：:\s]+(\d+\.?\d*)\s*(?:cm|厘米)?",
    
    # 血压
    "收缩压": r"收缩压[：:\s]+(\d+)\s*(?:mmHg|毫米汞柱)?",
    "舒张压": r"舒张压[：:\s]+(\d+)\s*(?:mmHg|毫米汞柱)?",
    
    # 肝功能
    "ALT": r"ALT[：:\s]+(\d+\.?\d*)\s*(?:U/L|IU/L)?",
    "AST": r"AST[：:\s]+(\d+\.?\d*)\s*(?:U/L|IU/L)?",
    "GGT": r"GGT[：:\s]+(\d+\.?\d*)\s*(?:U/L|IU/L)?",
    "总胆红素": r"总胆红素[：:\s]+(\d+\.?\d*)\s*(?:μmol/L|umol/L)?",
    "白蛋白": r"白蛋白[：:\s]+(\d+\.?\d*)\s*(?:g/L)?",
    
    # 血脂
    "总胆固醇": r"总胆固醇[：:\s]+(\d+\.?\d*)\s*(?:mmol/L)?",
    "甘油三酯": r"甘油三酯[：:\s]+(\d+\.?\d*)\s*(?:mmol/L)?",
    "HDL": r"HDL[：:\s]+(\d+\.?\d*)\s*(?:mmol/L)?",
    "LDL": r"LDL[：:\s]+(\d+\.?\d*)\s*(?:mmol/L)?",
    
    # 血糖
    "空腹血糖": r"空腹血糖[：:\s]+(\d+\.?\d*)\s*(?:mmol/L)?",
    "糖化血红蛋白": r"糖化血红蛋白[：:\s]+(\d+\.?\d*)\s*(?:%)?",
    
    # 肾功能
    "肌酐": r"肌酐[：:\s]+(\d+\.?\d*)\s*(?:μmol/L|umol/L)?",
    "尿素氮": r"尿素氮[：:\s]+(\d+\.?\d*)\s*(?:mmol/L)?",
    "尿酸": r"尿酸[：:\s]+(\d+\.?\d*)\s*(?:μmol/L|umol/L)?",
    
    # 血常规
    "白细胞": r"白细胞[：:\s]+(\d+\.?\d*)\s*(?:\*10\^9/L)?",
    "红细胞": r"红细胞[：:\s]+(\d+\.?\d*)\s*(?:\*10\^12/L)?",
    "血红蛋白": r"血红蛋白[：:\s]+(\d+\.?\d*)\s*(?:g/L)?",
    "血小板": r"血小板[：:\s]+(\d+\.?\d*)\s*(?:\*10\^9/L)?",
}


def filter_personal_info(text):
    """过滤个人信息（脱敏）"""
    # 姓名
    text = re.sub(r"姓\s*名[：:]\s*[\u4e00-\u9fa5]{2,10}", "姓名: [已脱敏]", text)
    # 身份证号
    text = re.sub(r"(身\s*份\s*证[：:]\s*)\d{6}\d{8}[0-9Xx]", r"\1[已脱敏]", text)
    # 手机号
    text = re.sub(r"(手机[号号码]*[：:]\s*)1\d{10}", r"\1[已脱敏]", text)
    return text


def extract_from_text(text):
    """从文本中提取指标"""
    text = filter_personal_info(text)
    text_clean = re.sub(r'\s+', ' ', text)
    
    results = {}
    for indicator, pattern in INDICATOR_PATTERNS.items():
        matches = re.findall(pattern, text_clean, re.IGNORECASE | re.MULTILINE)
        if matches:
            value = matches[0]
            if value:
                try:
                    results[indicator] = float(value)
                except ValueError:
                    results[indicator] = value
    return results


def analyze_abnormal(indicators):
    """分析异常指标"""
    # 参考范围
    ranges = {
        "ALT": (9, 50),
        "AST": (15, 40),
        "GGT": (10, 60),
        "总胆固醇": (0, 5.2),
        "甘油三酯": (0, 1.7),
        "HDL": (1.0, None),
        "LDL": (0, 3.4),
        "空腹血糖": (3.9, 6.1),
        "尿酸": (150, 440),
        "收缩压": (0, 140),
        "舒张压": (0, 90),
    }
    
    abnormal = []
    for indicator, value in indicators.items():
        if indicator in ranges and isinstance(value, (int, float)):
            low, high = ranges[indicator]
            if low and value < low:
                abnormal.append({"indicator": indicator, "value": value, "status": "偏低"})
            elif high and value > high:
                abnormal.append({"indicator": indicator, "value": value, "status": "偏高"})
    
    return abnormal


def process_text_input(user_id, text):
    """处理文字输入"""
    indicators = extract_from_text(text)
    abnormal = analyze_abnormal(indicators)
    
    # 保存用户数据
    user_dir = USERS_DIR / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    
    data_file = user_dir / "health_data.json"
    data = {"user_id": user_id, "indicators": indicators, "abnormal": abnormal}
    
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return {
        "success": True,
        "indicators": indicators,
        "abnormal": abnormal,
        "message": f"已提取 {len(indicators)} 项指标，发现 {len(abnormal)} 项异常"
    }


def load_user_health_data(user_id):
    """加载用户健康数据"""
    user_dir = USERS_DIR / user_id
    data_file = user_dir / "health_data.json"
    
    if data_file.exists():
        with open(data_file, encoding="utf-8") as f:
            return json.load(f)
    return None


if __name__ == "__main__":
    # 测试
    test_text = """
    姓名：张三
    身高：172cm，体重：68kg，BMI：23.0
    ALT: 58 U/L (偏高)
    总胆固醇: 6.5 mmol/L (偏高)
    空腹血糖: 5.5 mmol/L (正常)
    """
    result = process_text_input("test_user", test_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))