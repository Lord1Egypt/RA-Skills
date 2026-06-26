#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六爻纳甲排盘工具 v2.0.0
天工长老开发

功能：六爻起卦、纳甲、装卦、六亲、世应、六神排布、动爻变卦、自动化断卦
"""

import argparse
import json
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ============== 基础数据 ==============

# 八卦
BA_GUA = ['乾', '兑', '离', '震', '巽', '坎', '艮', '坤']

# 八卦纳甲（每卦从初爻到上爻的纳干）
NA_JIA_GAN = {
    '乾': ['甲', '甲', '甲', '壬', '壬', '壬'],  # 乾卦内卦纳甲，外卦纳壬
    '坤': ['乙', '乙', '乙', '癸', '癸', '癸'],  # 坤卦内卦纳乙，外卦纳癸
    '震': ['庚', '庚', '庚', '庚', '庚', '庚'],
    '巽': ['辛', '辛', '辛', '辛', '辛', '辛'],
    '坎': ['戊', '戊', '戊', '戊', '戊', '戊'],
    '离': ['己', '己', '己', '己', '己', '己'],
    '艮': ['丙', '丙', '丙', '丙', '丙', '丙'],
    '兑': ['丁', '丁', '丁', '丁', '丁', '丁'],
}

# 八卦五行
BA_GUA_WUXING = {
    '乾': '金', '兑': '金', '离': '火', '震': '木',
    '巽': '木', '坎': '水', '艮': '土', '坤': '土'
}

# 六十四卦名（上卦 + 下卦）
LIU_SHI_SI_GUA = {
    '乾乾': '乾为天', '乾兑': '天泽履', '乾离': '天火同人', '乾震': '天雷无妄',
    '乾巽': '天风姤', '乾坎': '天水讼', '乾艮': '天山遁', '乾坤': '天地否',
    '兑乾': '泽天夬', '兑兑': '兑为泽', '兑离': '泽火革', '兑震': '泽雷随',
    '兑巽': '泽风大过', '兑坎': '泽水困', '兑艮': '泽山咸', '兑坤': '泽地萃',
    '离乾': '火天大有', '离兑': '火泽睽', '离离': '离为火', '离震': '火雷噬嗑',
    '离巽': '火风鼎', '离坎': '火水未济', '离艮': '火山旅', '离坤': '火地晋',
    '震乾': '雷天大壮', '震兑': '雷泽归妹', '震离': '雷火丰', '震震': '震为雷',
    '震巽': '雷风恒', '震坎': '雷水解', '震艮': '雷山小过', '震坤': '雷地豫',
    '巽乾': '风天小畜', '巽兑': '风泽中孚', '巽离': '风火家人', '巽震': '风雷益',
    '巽巽': '巽为风', '巽坎': '风水涣', '巽艮': '风山渐', '巽坤': '风地观',
    '坎乾': '水天需', '坎兑': '水泽节', '坎离': '水火既济', '坎震': '水雷屯',
    '坎巽': '水风井', '坎坎': '坎为水', '坎艮': '水山蹇', '坎坤': '水地比',
    '艮乾': '山天大畜', '艮兑': '山泽损', '艮离': '山火贲', '艮震': '山雷颐',
    '艮巽': '山风蛊', '艮坎': '山水蒙', '艮艮': '艮为山', '艮坤': '山地剥',
    '坤乾': '地天泰', '坤兑': '地泽临', '坤离': '地火明夷', '坤震': '地雷复',
    '坤巽': '地风升', '坤坎': '地水师', '坤艮': '地山谦', '坤坤': '坤为地',
}

# 六十四卦宫位
GUA_GONG_MAP = {
    '乾为天': '乾', '天风姤': '乾', '天山遁': '乾', '天地否': '乾',
    '风地观': '乾', '山地剥': '乾', '火地晋': '乾', '火天大有': '乾',
    '兑为泽': '兑', '泽水困': '兑', '泽地萃': '兑', '泽山咸': '兑',
    '水山蹇': '兑', '地山谦': '兑', '雷山小过': '兑', '雷泽归妹': '兑',
    '离为火': '离', '火山旅': '离', '火风鼎': '离', '火水未济': '离',
    '山水蒙': '离', '风水涣': '离', '天水讼': '离', '天火同人': '离',
    '震为雷': '震', '雷地豫': '震', '雷水解': '震', '雷风恒': '震',
    '地风升': '震', '水风井': '震', '泽风大过': '震', '泽雷随': '震',
    '巽为风': '巽', '风天小畜': '巽', '风火家人': '巽', '风雷益': '巽',
    '天雷无妄': '巽', '火雷噬嗑': '巽', '山雷颐': '巽', '山风蛊': '巽',
    '坎为水': '坎', '水泽节': '坎', '水雷屯': '坎', '水火既济': '坎',
    '泽火革': '坎', '雷火丰': '坎', '地火明夷': '坎', '地水师': '坎',
    '艮为山': '艮', '山火贲': '艮', '山天大畜': '艮', '山泽损': '艮',
    '火泽睽': '艮', '天泽履': '艮', '风泽中孚': '艮', '风山渐': '艮',
    '坤为地': '坤', '地雷复': '坤', '地泽临': '坤', '地天泰': '坤',
    '雷天大壮': '坤', '泽天夬': '坤', '水天需': '坤', '水地比': '坤',
}

# 六亲
LIU_QIN = ['父母', '兄弟', '子孙', '妻财', '官鬼']

# 六神
LIU_SHEN = ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武']

# 天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 地支五行
DI_ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 地支藏干
DI_ZHI_CANG_GAN = {
    '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'],
    '卯': ['乙'], '辰': ['戊', '乙', '癸'], '巳': ['丙', '戊', '庚'],
    '午': ['丁', '己'], '未': ['己', '丁', '乙'], '申': ['庚', '壬', '戊'],
    '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']
}

# 月令（按月支）
YUE_LING = {
    '寅': '春', '卯': '春', '辰': '春',
    '巳': '夏', '午': '夏', '未': '夏',
    '申': '秋', '酉': '秋', '戌': '秋',
    '亥': '冬', '子': '冬', '丑': '冬'
}

# 六神断语
LIU_SHEN_DUAN = {
    '青龙': {'吉': '喜庆临门，贵人相助', '凶': '乐极生悲，防过喜伤身'},
    '朱雀': {'吉': '文书有利，口舌生财', '凶': '口舌是非，防小人'},
    '勾陈': {'吉': '田土有利，稳定发展', '凶': '事多迟滞，防牵连'},
    '螣蛇': {'吉': '变化中求机', '凶': '虚惊怪异，防欺骗'},
    '白虎': {'吉': '武职有利，果断行事', '凶': '血光疾病，防意外'},
    '玄武': {'吉': '谋略得当，暗中得利', '凶': '防盗防骗，防暧昧'}
}

# 天干五行
TIAN_GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 五行生克
WUXING_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
WUXING_KE = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}

# 世爻位置（按宫位和卦型）
SHI_YAO_MAP = {
    '乾': {'乾为天': 6, '天风姤': 1, '天山遁': 2, '天地否': 3, 
           '风地观': 4, '山地剥': 5, '火地晋': 4, '火天大有': 3},
    '兑': {'兑为泽': 6, '泽水困': 2, '泽地萃': 2, '泽山咸': 3,
           '水山蹇': 4, '地山谦': 4, '雷山小过': 3, '雷泽归妹': 2},
    '离': {'离为火': 6, '火山旅': 3, '火风鼎': 2, '火水未济': 3,
           '山水蒙': 2, '风水涣': 2, '天水讼': 2, '天火同人': 1},
    '震': {'震为雷': 6, '雷地豫': 2, '雷水解': 2, '雷风恒': 3,
           '地风升': 3, '水风井': 2, '泽风大过': 2, '泽雷随': 1},
    '巽': {'巽为风': 6, '风天小畜': 1, '风火家人': 2, '风雷益': 3,
           '天雷无妄': 4, '火雷噬嗑': 5, '山雷颐': 4, '山风蛊': 1},
    '坎': {'坎为水': 6, '水泽节': 2, '水雷屯': 3, '水火既济': 3,
           '泽火革': 4, '雷火丰': 5, '地火明夷': 4, '地水师': 1},
    '艮': {'艮为山': 6, '山火贲': 1, '山天大畜': 2, '山泽损': 3,
           '火泽睽': 4, '天泽履': 5, '风泽中孚': 4, '风山渐': 1},
    '坤': {'坤为地': 6, '地雷复': 1, '地泽临': 2, '地天泰': 3,
           '雷天大壮': 4, '泽天夬': 5, '水天需': 2, '水地比': 1},
}

# 用神选取
YONG_SHEN_MAP = {
    '财运': '妻财', '事业': '官鬼', '工作': '官鬼', '婚姻': '妻财',
    '感情': '妻财', '健康': '子孙', '疾病': '官鬼', '考试': '父母',
    '学业': '父母', '失物': '妻财', '官司': '官鬼', '诉讼': '官鬼',
    '出行': '子孙', '旅行': '子孙', '求子': '子孙', '怀孕': '子孙',
    '搬家': '父母', '房屋': '父母', '交易': '妻财', '投资': '妻财',
}


class LiuYaoPan:
    """六爻排盘类"""
    
    @staticmethod
    def get_year_gan_zhi(year: int) -> Tuple[str, str]:
        """获取年干支"""
        gan_index = (year - 4) % 10
        zhi_index = (year - 4) % 12
        return TIAN_GAN[gan_index], DI_ZHI[zhi_index]
    
    @staticmethod
    def get_month_gan_zhi(year: int, month: int) -> Tuple[str, str]:
        """获取月干支（简化版，按节气）"""
        # 月支固定：寅月为正月
        zhi_index = (month + 2) % 12
        zhi = DI_ZHI[zhi_index]
        
        # 月干根据年干推算（五虎遁）
        year_gan, _ = LiuYaoPan.get_year_gan_zhi(year)
        gan_map = {'甲': 2, '乙': 4, '丙': 6, '丁': 8, '戊': 0,
                   '己': 2, '庚': 4, '辛': 6, '壬': 8, '癸': 0}
        start = gan_map.get(year_gan, 0)
        gan_index = (start + month - 1) % 10
        gan = TIAN_GAN[gan_index]
        
        return gan, zhi
    
    @staticmethod
    def get_day_gan_zhi(date: datetime) -> Tuple[str, str]:
        """获取日干支（简化算法）"""
        # 基准日：1900 年 1 月 31 日为甲辰日
        base_date = datetime(1900, 1, 31)
        days_diff = (date - base_date).days
        
        gan_index = days_diff % 10
        zhi_index = days_diff % 12
        
        return TIAN_GAN[gan_index], DI_ZHI[zhi_index]
    
    @staticmethod
    def get_hour_gan_zhi(day_gan: str, hour: int) -> Tuple[str, str]:
        """获取时干支"""
        # 时支固定
        zhi_index = ((hour + 1) // 2) % 12
        zhi = DI_ZHI[zhi_index]
        
        # 时干根据日干推算（五鼠遁）
        gan_map = {'甲': 0, '乙': 2, '丙': 4, '丁': 6, '戊': 6,
                   '己': 8, '庚': 0, '辛': 2, '壬': 4, '癸': 6}
        start = gan_map.get(day_gan, 0)
        gan_index = (start + zhi_index) % 10
        gan = TIAN_GAN[gan_index]
        
        return gan, zhi
    
    @classmethod
    def time_to_gua(cls, date: datetime) -> Tuple[int, int, int]:
        """
        时间起卦（年月日时起卦）
        返回：(上卦，下卦，动爻)
        """
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        
        # 上卦：(年 + 月 + 日) % 8
        shang_gua = (year + month + day) % 8
        if shang_gua == 0:
            shang_gua = 8
        
        # 下卦：(年 + 月 + 日 + 时) % 8
        xia_gua = (year + month + day + hour) % 8
        if xia_gua == 0:
            xia_gua = 8
        
        # 动爻：(年 + 月 + 日 + 时) % 6
        dong_yao = (year + month + day + hour) % 6
        if dong_yao == 0:
            dong_yao = 6
        
        return shang_gua, xia_gua, dong_yao
    
    @classmethod
    def number_to_gua(cls, numbers: List[int]) -> Tuple[int, int, int]:
        """
        数字起卦
        返回：(上卦，下卦，动爻)
        """
        if len(numbers) >= 3:
            shang_gua = numbers[0] % 8
            xia_gua = numbers[1] % 8
            dong_yao = numbers[2] % 6
        else:
            total = sum(numbers)
            shang_gua = total % 8
            xia_gua = (total + 100) % 8
            dong_yao = (total + 50) % 6
        
        if shang_gua == 0:
            shang_gua = 8
        if xia_gua == 0:
            xia_gua = 8
        if dong_yao == 0:
            dong_yao = 6
        
        return shang_gua, xia_gua, dong_yao
    
    @classmethod
    def coins_to_gua(cls, coins: List[int]) -> Tuple[List[int], List[int]]:
        """
        铜钱起卦
        coins: 6 次投掷结果（每次背面数，1-3）
        返回：(本卦爻，变卦爻)
        """
        ben_gua = []
        bian_gua = []
        
        for coin in coins:
            if coin == 1:  # 少阳
                ben_gua.append(1)
                bian_gua.append(1)
            elif coin == 2:  # 少阴
                ben_gua.append(0)
                bian_gua.append(0)
            elif coin == 3:  # 老阳（动爻）
                ben_gua.append(1)
                bian_gua.append(0)
            elif coin == 4:  # 老阴（动爻）
                ben_gua.append(0)
                bian_gua.append(1)
            else:
                ben_gua.append(coin % 2)
                bian_gua.append(coin % 2)
        
        return ben_gua, bian_gua
    
    @classmethod
    def get_gua_name(cls, shang_gua: int, xia_gua: int) -> str:
        """获取卦名"""
        shang = BA_GUA[shang_gua - 1]
        xia = BA_GUA[xia_gua - 1]
        key = shang + xia
        return LIU_SHI_SI_GUA.get(key, '未知卦')
    
    @classmethod
    def get_gua_gong(cls, gua_name: str) -> str:
        """获取卦宫"""
        return GUA_GONG_MAP.get(gua_name, '乾')
    
    @classmethod
    def get_shi_yao(cls, gua_name: str, gua_gong: str) -> int:
        """获取世爻位置（1-6）"""
        shi_map = SHI_YAO_MAP.get(gua_gong, {})
        return shi_map.get(gua_name, 1)
    
    @classmethod
    def get_yao_gan_zhi(cls, gua: str, yao_pos: int, is_wai_gua: bool) -> Tuple[str, str]:
        """
        获取某爻的干支
        yao_pos: 爻位（0-5，从初爻开始）
        is_wai_gua: 是否为外卦（上三爻）
        """
        # 地支从下往上排
        zhi_order = {
            '乾': ['子', '寅', '辰', '午', '申', '戌'],
            '兑': ['巳', '卯', '丑', '亥', '酉', '未'],
            '离': ['卯', '丑', '亥', '酉', '未', '巳'],
            '震': ['子', '寅', '辰', '午', '申', '戌'],
            '巽': ['丑', '亥', '酉', '未', '巳', '卯'],
            '坎': ['寅', '辰', '午', '申', '戌', '子'],
            '艮': ['辰', '午', '申', '戌', '子', '寅'],
            '坤': ['未', '巳', '卯', '丑', '亥', '酉'],
        }
        
        zhi = zhi_order.get(gua, ['子', '寅', '辰', '午', '申', '戌'])[yao_pos]
        
        # 天干根据纳甲
        gan_list = NA_JIA_GAN.get(gua, ['甲', '甲', '甲', '甲', '甲', '甲'])
        gan = gan_list[yao_pos]
        
        return gan, zhi
    
    @classmethod
    def get_liu_qin(cls, gua_gong_wuxing: str, yao_wuxing: str) -> str:
        """
        根据卦宫五行和爻五行确定六亲
        """
        if yao_wuxing == gua_gong_wuxing:
            return '兄弟'
        elif WUXING_SHENG.get(yao_wuxing) == gua_gong_wuxing:
            return '父母'
        elif WUXING_SHENG.get(gua_gong_wuxing) == yao_wuxing:
            return '子孙'
        elif WUXING_KE.get(yao_wuxing) == gua_gong_wuxing:
            return '官鬼'
        elif WUXING_KE.get(gua_gong_wuxing) == yao_wuxing:
            return '妻财'
        else:
            return '兄弟'
    
    @classmethod
    def get_liu_shen(cls, day_gan: str, yao_pos: int) -> str:
        """
        根据日干和爻位确定六神
        """
        gan_map = {'甲': 0, '乙': 1, '丙': 2, '丁': 3, '戊': 4,
                   '己': 5, '庚': 0, '辛': 1, '壬': 2, '癸': 3}
        start = gan_map.get(day_gan, 0)
        shen_index = (start + yao_pos) % 6
        return LIU_SHEN[shen_index]
    
    @classmethod
    def get_bian_gua(cls, shang_gua: int, xia_gua: int, dong_yao: int) -> str:
        """获取变卦"""
        if dong_yao == 0:
            return '无'
        
        # 动爻变阴阳
        if dong_yao <= 3:
            # 下卦动
            new_xia = xia_gua
            # 简化处理
        else:
            # 上卦动
            pass
        
        # 简化：返回对宫卦
        gua_name = cls.get_gua_name(shang_gua, xia_gua)
        gua_gong = cls.get_gua_gong(gua_name)
        
        # 游魂归魂处理
        if gua_gong == '乾' and gua_name == '火地晋':
            return '水天需'
        elif gua_gong == '乾' and gua_name == '火天大有':
            return '火天大有'
        
        return '待计算'
    
    @classmethod
    def get_wang_shuai(cls, yao_wuxing: str, month_zhi: str, day_zhi: str) -> str:
        """
        判断爻的旺衰（基于月令和日辰）
        """
        month_wuxing = DI_ZHI_WUXING.get(month_zhi, '土')
        day_wuxing = DI_ZHI_WUXING.get(day_zhi, '土')
        
        # 得月令为旺
        if yao_wuxing == month_wuxing:
            return '旺'
        # 月令生爻为相
        elif WUXING_SHENG.get(yao_wuxing) == month_wuxing:
            return '相'
        # 克月令为休
        elif WUXING_KE.get(yao_wuxing) == month_wuxing:
            return '休'
        # 被月令克为囚
        elif WUXING_KE.get(month_wuxing) == yao_wuxing:
            return '囚'
        # 月令克爻为死
        else:
            return '死'
    
    @classmethod
    def get_shi_ying_relation(cls, shi_wuxing: str, ying_wuxing: str) -> Dict:
        """
        分析世应关系
        """
        if shi_wuxing == ying_wuxing:
            return {'关系': '比和', '吉凶': '平', '说明': '势均力敌，需努力争取'}
        elif WUXING_SHENG.get(shi_wuxing) == ying_wuxing:
            return {'关系': '世生应', '吉凶': '凶', '说明': '我生对方，付出多回报少'}
        elif WUXING_SHENG.get(ying_wuxing) == shi_wuxing:
            return {'关系': '应生世', '吉凶': '吉', '说明': '对方生我，贵人相助'}
        elif WUXING_KE.get(shi_wuxing) == ying_wuxing:
            return {'关系': '世克应', '吉凶': '平', '说明': '我克对方，主动可控'}
        elif WUXING_KE.get(ying_wuxing) == shi_wuxing:
            return {'关系': '应克世', '吉凶': '凶', '说明': '对方克我，压力大阻力大'}
        return {'关系': '未知', '吉凶': '平', '说明': '关系不明'}
    
    @classmethod
    def get_liu_shen_duan(cls, liu_shen: str, ji_xiong: str) -> str:
        """获取六神断语"""
        return LIU_SHEN_DUAN.get(liu_shen, {}).get(ji_xiong, '待分析')
    
    @classmethod
    def analyze_duan_gua(cls, result: Dict) -> Dict:
        """
        完整断卦分析
        """
        yao_list = result.get('六爻', [])
        yong_shen = result.get('用神', '妻财')
        month_zhi = result.get('月支', '子')
        day_zhi = result.get('日支', '子')
        shi_yao = result.get('世爻', 1)
        ying_yao = result.get('应爻', 4)
        
        # 找用神爻
        yong_shen_yao = None
        for yao in yao_list:
            if yao['六亲'] == yong_shen:
                yong_shen_yao = yao
                break
        
        # 用神旺衰
        yong_shen_wang_shuai = '平'
        if yong_shen_yao:
            yong_shen_wang_shuai = cls.get_wang_shuai(
                yong_shen_yao['五行'], month_zhi, day_zhi
            )
        
        # 世应关系
        shi_yao_info = None
        ying_yao_info = None
        for yao in yao_list:
            if yao['爻位'] == shi_yao:
                shi_yao_info = yao
            if yao['爻位'] == ying_yao:
                ying_yao_info = yao
        
        shi_ying_relation = {'关系': '未知', '吉凶': '平', '说明': '待分析'}
        if shi_yao_info and ying_yao_info:
            shi_ying_relation = cls.get_shi_ying_relation(
                shi_yao_info['五行'], ying_yao_info['五行']
            )
        
        # 动爻分析
        dong_yao_list = [y for y in yao_list if y.get('动爻', False)]
        dong_yao_duan = []
        for dy in dong_yao_list:
            if dy['六亲'] == yong_shen:
                dong_yao_duan.append(f"用神动，变化中求机会")
            elif dy['六亲'] == '兄弟':
                dong_yao_duan.append(f"兄弟动，防破财竞争")
            elif dy['六亲'] == '官鬼':
                dong_yao_duan.append(f"官鬼动，防压力是非")
            elif dy['六亲'] == '父母':
                dong_yao_duan.append(f"父母动，文书有利")
            elif dy['六亲'] == '子孙':
                dong_yao_duan.append(f"子孙动，财源广进")
            elif dy['六亲'] == '妻财':
                dong_yao_duan.append(f"妻财动，财运变化")
        
        # 六神断语
        liu_shen_duan = []
        if yong_shen_yao:
            ji_xiong = '吉' if yong_shen_wang_shuai in ['旺', '相'] else '凶'
            liu_shen_duan.append(
                f"{yong_shen_yao['六神']}临用神：{cls.get_liu_shen_duan(yong_shen_yao['六神'], ji_xiong)}"
            )
        
        # 吉凶评分（0-100）
        score = 50
        if yong_shen_wang_shuai == '旺':
            score += 20
        elif yong_shen_wang_shuai == '相':
            score += 10
        elif yong_shen_wang_shuai == '死':
            score -= 20
        elif yong_shen_wang_shuai == '囚':
            score -= 10
        
        if shi_ying_relation['吉凶'] == '吉':
            score += 15
        elif shi_ying_relation['吉凶'] == '凶':
            score -= 15
        
        if dong_yao_list:
            # 有动爻，看吉凶
            for dy in dong_yao_list:
                if dy['六亲'] in ['子孙', '妻财']:
                    score += 5
                elif dy['六亲'] in ['兄弟', '官鬼']:
                    score -= 5
        
        score = max(0, min(100, score))
        
        # 吉凶判断
        if score >= 70:
            ji_xiong_pan_duan = '大吉'
            jian_yi = '卦象大吉，宜积极行动，把握良机'
        elif score >= 55:
            ji_xiong_pan_duan = '吉'
            jian_yi = '卦象偏吉，可顺势而为，注意细节'
        elif score >= 45:
            ji_xiong_pan_duan = '平'
            jian_yi = '卦象平稳，宜守不宜攻，等待时机'
        elif score >= 30:
            ji_xiong_pan_duan = '凶'
            jian_yi = '卦象偏凶，宜谨慎行事，防小人'
        else:
            ji_xiong_pan_duan = '大凶'
            jian_yi = '卦象大凶，宜韬光养晦，暂避锋芒'
        
        # 趋避建议
        qu_bi = []
        if yong_shen_wang_shuai in ['死', '囚']:
            qu_bi.append('用神衰弱，宜补旺用神五行')
        if shi_ying_relation['关系'] == '应克世':
            qu_bi.append('应克世，防对方施压，宜退让')
        if shi_ying_relation['关系'] == '世生应':
            qu_bi.append('世生应，付出多，宜控制投入')
        for dy in dong_yao_list:
            if dy['六亲'] == '兄弟':
                qu_bi.append('兄弟动，防破财，不宜投资')
            elif dy['六亲'] == '官鬼':
                qu_bi.append('官鬼动，防是非，谨言慎行')
        
        if not qu_bi:
            qu_bi.append('卦象无大碍，顺势而为即可')
        
        return {
            '用神旺衰': yong_shen_wang_shuai,
            '世应关系': shi_ying_relation,
            '动爻分析': dong_yao_duan,
            '六神断语': liu_shen_duan,
            '吉凶评分': score,
            '吉凶判断': ji_xiong_pan_duan,
            '建议': jian_yi,
            '趋避': qu_bi
        }


def liuyao_pan(
    date_str: Optional[str] = None,
    numbers: Optional[str] = None,
    coins: Optional[str] = None,
    question: str = '通用'
) -> Dict:
    """
    六爻排盘主函数
    """
    # 时间处理
    if date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    else:
        dt = datetime.now()
    
    # 干支
    year_gan, year_zhi = LiuYaoPan.get_year_gan_zhi(dt.year)
    month_gan, month_zhi = LiuYaoPan.get_month_gan_zhi(dt.year, dt.month)
    day_gan, day_zhi = LiuYaoPan.get_day_gan_zhi(dt)
    hour_gan, hour_zhi = LiuYaoPan.get_hour_gan_zhi(day_gan, dt.hour)
    
    # 起卦
    if coins:
        coin_list = [int(x.strip()) for x in coins.split(',')]
        ben_gua_yao, bian_gua_yao = LiuYaoPan.coins_to_gua(coin_list)
        xia_gua = sum(ben_gua_yao[:3]) % 8 + 1
        shang_gua = sum(ben_gua_yao[3:]) % 8 + 1
        if xia_gua == 8:
            xia_gua = 1
        if shang_gua == 8:
            shang_gua = 1
        dong_yao_list = [i+1 for i, (b, v) in enumerate(zip(ben_gua_yao, bian_gua_yao)) if b != v]
        dong_yao = dong_yao_list[0] if dong_yao_list else 0
        qi_gua_fang_shi = '铜钱'
    elif numbers:
        num_list = [int(x.strip()) for x in numbers.split(',')]
        shang_gua, xia_gua, dong_yao = LiuYaoPan.number_to_gua(num_list)
        qi_gua_fang_shi = '数字'
    else:
        shang_gua, xia_gua, dong_yao = LiuYaoPan.time_to_gua(dt)
        qi_gua_fang_shi = '时间'
    
    # 卦名卦宫
    gua_name = LiuYaoPan.get_gua_name(shang_gua, xia_gua)
    gua_gong = LiuYaoPan.get_gua_gong(gua_name)
    gua_gong_wuxing = BA_GUA_WUXING[gua_gong]
    shi_yao = LiuYaoPan.get_shi_yao(gua_name, gua_gong)
    ying_yao = ((shi_yao - 1 + 3) % 6) + 1
    
    # 下卦和上卦名
    xia_gua_name = BA_GUA[xia_gua - 1]
    shang_gua_name = BA_GUA[shang_gua - 1]
    
    # 六爻排布
    yao_list = []
    for i in range(6):
        yao_pos = i  # 0-5
        is_wai_gua = i >= 3
        gua_for_yao = xia_gua_name if i < 3 else shang_gua_name
        
        gan, zhi = LiuYaoPan.get_yao_gan_zhi(gua_for_yao, yao_pos, is_wai_gua)
        yao_wuxing = DI_ZHI_WUXING[zhi]
        liu_qin = LiuYaoPan.get_liu_qin(gua_gong_wuxing, yao_wuxing)
        liu_shen = LiuYaoPan.get_liu_shen(day_gan, yao_pos)
        
        # 判断阴阳
        yao_yang = (shang_gua + xia_gua + i) % 2
        is_dong = (dong_yao == i + 1)
        
        yao_list.append({
            '爻位': i + 1,
            '爻名': ['初', '二', '三', '四', '五', '上'][i],
            '阴阳': '阳' if yao_yang else '阴',
            '干支': f'{gan}{zhi}',
            '五行': yao_wuxing,
            '六亲': liu_qin,
            '六神': liu_shen,
            '世应': '世' if i + 1 == shi_yao else ('应' if i + 1 == ying_yao else ''),
            '动爻': is_dong,
        })
    
    # 用神
    yong_shen = YONG_SHEN_MAP.get(question, '妻财')
    
    # 变卦
    bian_gua = LiuYaoPan.get_bian_gua(shang_gua, xia_gua, dong_yao)
    
    # 断卦分析
    yong_shen_yao = [y for y in yao_list if y['六亲'] == yong_shen]
    yong_shen_wang = len(yong_shen_yao) > 0
    
    # 断卦分析 v3.0.0
    temp_result = {
        '六爻': yao_list,
        '用神': yong_shen,
        '月支': month_zhi,
        '日支': day_zhi,
        '世爻': shi_yao,
        '应爻': ying_yao,
    }
    duan_gua = LiuYaoPan.analyze_duan_gua(temp_result)
    
    result = {
        '起卦方式': qi_gua_fang_shi,
        '公历时间': dt.strftime('%Y 年 %m 月 %d 日 %H 时 %M 分'),
        '农历时间': f'{year_gan}{year_zhi}年 {month_gan}{month_zhi}月 {day_gan}{day_zhi}日 {hour_gan}{hour_zhi}时',
        '四柱': f'{year_gan}{year_zhi}  {month_gan}{month_zhi}  {day_gan}{day_zhi}  {hour_gan}{hour_zhi}',
        '本卦': gua_name,
        '卦宫': gua_gong,
        '卦宫五行': gua_gong_wuxing,
        '上下卦': f'{shang_gua_name}上{xia_gua_name}下',
        '世爻': shi_yao,
        '应爻': ying_yao,
        '动爻': dong_yao,
        '变卦': bian_gua,
        '六爻': yao_list,
        '问事类型': question,
        '用神': yong_shen,
        '用神爻': yong_shen_yao[0] if yong_shen_yao else None,
        '月支': month_zhi,
        '日支': day_zhi,
        '断卦分析': duan_gua,
    }
    
    return result


def format_output(result: Dict) -> str:
    """格式化输出"""
    output = []
    
    output.append("【卦象结果】")
    output.append(f"• 起卦方式：{result['起卦方式']}")
    output.append(f"• 公历时间：{result['公历时间']}")
    output.append(f"• 农历时间：{result['农历时间']}")
    output.append(f"• 四柱：{result['四柱']}")
    output.append("")
    output.append("【本卦】")
    output.append(f"• 卦名：{result['本卦']}（{result['卦宫']}宫）")
    output.append(f"• 卦宫五行：{result['卦宫五行']}")
    output.append(f"• 世爻：第{result['世爻']}爻")
    output.append(f"• 应爻：第{result['应爻']}爻")
    if result['动爻']:
        output.append(f"• 动爻：第{result['动爻']}爻")
        output.append(f"• 变卦：{result['变卦']}")
    output.append("")
    output.append("【六爻排布】")
    output.append("爻位  阴阳  干支  六亲  六神  世应")
    output.append("─" * 45)
    for yao in reversed(result['六爻']):
        yin_yang = '━━━' if yao['阴阳'] == '阳' else '━ ━'
        shi_ying = f" {yao['世应']}" if yao['世应'] else '    '
        dong = '○' if yao['动爻'] else ' '
        output.append(f"{yao['爻名']}爻  {yin_yang}{dong} {yao['干支']} {yao['六亲']} {yao['六神']}{shi_ying}")
    output.append("")
    output.append("【用神分析】")
    output.append(f"• 问事类型：{result['问事类型']}")
    output.append(f"• 用神：{result['用神']}")
    if result['用神爻']:
        yong = result['用神爻']
        output.append(f"• 用神落爻：第{yong['爻位']}爻（{yong['干支']}）")
        output.append(f"• 用神五行：{yong['五行']}")
        output.append(f"• 临六神：{yong['六神']}")
    output.append("")
    output.append("【断卦分析】")
    duan_gua = result.get('断卦分析', {})
    output.append(f"• 用神旺衰：{duan_gua.get('用神旺衰', '待分析')}")
    shi_ying = duan_gua.get('世应关系', {})
    output.append(f"• 世应关系：{shi_ying.get('关系', '待分析')}（{shi_ying.get('吉凶', '')}）— {shi_ying.get('说明', '')}")
    if duan_gua.get('动爻分析'):
        for dy in duan_gua['动爻分析']:
            output.append(f"• 动爻：{dy}")
    if duan_gua.get('六神断语'):
        for ls in duan_gua['六神断语']:
            output.append(f"• {ls}")
    output.append(f"• 吉凶评分：{duan_gua.get('吉凶评分', 50)}/100")
    output.append(f"• 吉凶判断：{duan_gua.get('吉凶判断', '待分析')}")
    output.append(f"• 建议：{duan_gua.get('建议', '待分析')}")
    if duan_gua.get('趋避'):
        output.append("")
        output.append("【趋吉避凶】")
        for tb in duan_gua['趋避']:
            output.append(f"• {tb}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='六爻纳甲排盘工具 v3.0.0')
    parser.add_argument('--date', '-d', type=str, help='日期时间 (YYYY-MM-DD HH:MM)')
    parser.add_argument('--numbers', '-n', type=str, help='数字起卦 (逗号分隔)')
    parser.add_argument('--coins', '-c', type=str, help='铜钱起卦 (6 次背面数，逗号分隔)')
    parser.add_argument('--question', '-q', type=str, default='通用', help='问事类型')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    try:
        result = liuyao_pan(args.date, args.numbers, args.coins, args.question)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_output(result))
            
    except Exception as e:
        print(f"排盘错误：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
