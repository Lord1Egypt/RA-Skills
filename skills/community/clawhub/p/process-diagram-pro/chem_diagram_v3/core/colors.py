# -*- coding: utf-8 -*-
"""
颜色体系 - Color System
=======================

化工行业标准颜色定义

Category:
    - 设备颜色 (Equipment Colors)
    - 管道颜色 (Pipeline Colors)
    - 温度渐变 (Temperature Gradient)
    - 物料颜色 (Material Colors)
    - 信号颜色 (Signal Colors)
"""

# ===================== 设备颜色 =====================
# 化工行业标准设备颜色

EQUIPMENT_COLORS = {
    # 储罐/原料罐
    'tank': {
        'facecolor': '#E8F4FD',  # 淡蓝
        'edgecolor': '#1976D2',   # 蓝色边框
        'label_color': '#1565C0',
    },
    
    # 换热器/预热器/冷凝器
    'heat_exchanger': {
        'facecolor': '#FFF3E0',    # 淡橙
        'edgecolor': '#E65100',   # 深橙边框
        'label_color': '#BF360C',
    },
    
    # 反应器
    'reactor': {
        'facecolor': '#FDE8E8',   # 淡红
        'edgecolor': '#C62828',   # 红色边框
        'label_color': '#B71C1C',
        'catalyst_bed': '#FFCDD2',  # 催化剂床层
    },
    
    # 分离器/罐
    'separator': {
        'facecolor': '#E8F5E9',   # 淡绿
        'edgecolor': '#2E7D32',   # 绿色边框
        'label_color': '#1B5E20',
    },
    
    # 泵
    'pump': {
        'facecolor': '#F3E5F5',   # 淡紫
        'edgecolor': '#7B1FA2',   # 紫色边框
        'label_color': '#6A1B9A',
    },
    
    # 产物瓶/收集器
    'product': {
        'facecolor': '#F3E5F5',   # 淡紫
        'edgecolor': '#7B1FA2',   # 紫色边框
        'label_color': '#6A1B9A',
    },
}

# ===================== 阀门颜色 =====================

VALVE_COLORS = {
    # 调节阀
    'control': {
        'facecolor': '#B3E5FC',   # 浅蓝
        'edgecolor': '#0277BD',    # 深蓝边框
        'label_color': '#01579B',
    },
    
    # ESD紧急切断阀
    'esd': {
        'facecolor': '#FFCDD2',   # 淡红
        'edgecolor': '#C62828',    # 红色边框
        'label_color': '#B71C1C',
    },
    
    # 安全阀
    'safety': {
        'facecolor': '#FFEB3B',    # 黄色
        'edgecolor': '#F57F17',    # 深黄边框
        'label_color': '#E65100',
    },
    
    # 减压阀
    'pressure_reducing': {
        'facecolor': '#E3F2FD',    # 淡蓝
        'edgecolor': '#1565C0',    # 蓝色边框
        'label_color': '#0D47A1',
    },
    
    # 止回阀
    'check': {
        'facecolor': '#FFFFFF',    # 白色
        'edgecolor': '#455A64',    # 灰色边框
        'label_color': '#37474F',
    },
}

# ===================== 仪表颜色 =====================

INSTRUMENT_COLORS = {
    # 仪表（圆形+符号）
    'default': {
        'facecolor': '#EDE7F6',    # 淡紫
        'edgecolor': '#7B1FA2',    # 紫色边框
        'label_color': '#4A148C',
    },
    
    # 温度仪表
    'temperature': {
        'facecolor': '#FFEBEE',    # 淡红
        'edgecolor': '#C62828',
        'label_color': '#B71C1C',
    },
    
    # 压力仪表
    'pressure': {
        'facecolor': '#E3F2FD',    # 淡蓝
        'edgecolor': '#1565C0',
        'label_color': '#0D47A1',
    },
    
    # 流量仪表
    'flow': {
        'facecolor': '#E8F5E9',    # 淡绿
        'edgecolor': '#2E7D32',
        'label_color': '#1B5E20',
    },
    
    # 分析仪表
    'analysis': {
        'facecolor': '#FFF3E0',    # 淡橙
        'edgecolor': '#E65100',
        'label_color': '#BF360C',
    },
}

# ===================== 管道颜色 =====================

PIPELINE_COLORS = {
    # 工艺管道
    'process': {
        'color': '#424242',         # 深灰
        'linewidth': 2.0,
    },
    
    # 氢气管道
    'hydrogen': {
        'color': '#00FF66',        # 亮绿
        'linewidth': 2.0,
    },
    
    # 蒸汽管道
    'steam': {
        'color': '#EEEEEE',        # 浅灰
        'linewidth': 2.0,
    },
    
    # 冷却水管道
    'cooling_water': {
        'color': '#0277BD',        # 蓝色
        'linewidth': 1.5,
    },
    
    # 气相管道
    'gas': {
        'color': '#78909C',        # 蓝灰
        'linewidth': 1.5,
    },
    
    # 信号线
    'signal': {
        'color': '#9C27B0',       # 紫色
        'linewidth': 1.0,
        'linestyle': '--',          # 虚线
    },
}

# ===================== 温度渐变色 =====================

TEMP_COLORS = {
    # 温度 → 颜色映射（化工行业标准）
    0:   '#0033FF',    # 深蓝
    20:  '#0099FF',    # 蓝
    40:  '#00FFCC',    # 青绿
    60:  '#66CC00',    # 黄绿
    80:  '#FFCC00',    # 黄
    100: '#FF6600',    # 橙
    120: '#FF0000',    # 红
    140: '#CC0000',    # 深红
    160: '#990000',    # 暗红
    180: '#660000',    # 最深红
}


def get_temp_color(temp_c):
    """
    根据温度获取对应颜色
    
    Args:
        temp_c: 温度（摄氏度）
    
    Returns:
        str: HEX颜色值
    """
    if temp_c is None:
        return TEMP_COLORS[40]  # 默认返回40°C的颜色
    
    temp_c = float(temp_c)
    if temp_c <= 0:
        return TEMP_COLORS[0]
    if temp_c >= 180:
        return TEMP_COLORS[180]
    
    # 线性插值
    temps = sorted(TEMP_COLORS.keys())
    for i in range(len(temps) - 1):
        if temps[i] <= temp_c <= temps[i+1]:
            t1, t2 = temps[i], temps[i+1]
            if t2 == t1:
                return TEMP_COLORS[t1]
            ratio = (temp_c - t1) / (t2 - t1)
            return interpolate_color(TEMP_COLORS[t1], TEMP_COLORS[t2], ratio)
    
    return TEMP_COLORS[40]  # 默认返回


def interpolate_color(color1, color2, ratio):
    """
    两个颜色之间线性插值
    
    Args:
        color1: 起始HEX颜色 (如 '#0033FF')
        color2: 结束HEX颜色
        ratio: 插值比例 (0-1)
    
    Returns:
        str: 插值后的HEX颜色
    """
    # 移除 # 前缀
    c1 = color1.lstrip('#')
    c2 = color2.lstrip('#')
    
    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
    
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    
    return f'#{r:02X}{g:02X}{b:02X}'


# ===================== 其他颜色 =====================

MISC_COLORS = {
    'background': '#FAFAFA',
    'text_dark': '#212121',
    'text_mid': '#616161',
    'text_light': '#9E9E9E',
    'arrow': '#1565C0',
    'edge': '#455A64',
    'warning': '#FF5722',
    'success': '#4CAF50',
    'info': '#2196F3',
}

# ===================== 完整颜色表 =====================

COLORS = {
    'equipment': EQUIPMENT_COLORS,
    'valve': VALVE_COLORS,
    'instrument': INSTRUMENT_COLORS,
    'pipeline': PIPELINE_COLORS,
    'temp': TEMP_COLORS,
    'misc': MISC_COLORS,
}
