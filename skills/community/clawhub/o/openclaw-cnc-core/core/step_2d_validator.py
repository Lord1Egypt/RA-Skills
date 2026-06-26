#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEP + 2D 联动校准模块
实现3D模型与2D图纸的参数比对与偏差告警

集成到 5000 端口报价系统
"""

import os
import json
import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

# 导入现有模块
try:
    import cadquery as cq
    HAS_CADQUERY = True
except ImportError:
    HAS_CADQUERY = False

try:
    from pdfminer.high_level import extract_text
    import re
    HAS_PDFMINER = True
except ImportError:
    HAS_PDFMINER = False

logger = logging.getLogger(__name__)


@dataclass
class GeometryData:
    """几何数据结构"""
    length: float      # 长度 mm
    width: float       # 宽度 mm
    height: float      # 高度 mm
    volume: float      # 体积 cm³
    area: float        # 表面积 cm²
    weight: float      # 重量 kg
    source: str        # 数据来源: step/pdf


@dataclass
class ComparisonResult:
    """比对结果"""
    is_consistent: bool         # 是否一致
    length_diff: float          # 长度偏差 %
    width_diff: float           # 宽度偏差 %
    height_diff: float          # 高度偏差 %
    volume_diff: float          # 体积偏差 %
    warnings: list              # 警告列表
    step_data: GeometryData     # STEP数据
    pdf_data: Optional[GeometryData]  # PDF数据


class STEPParser:
    """STEP文件解析器"""
    
    def __init__(self, density: float = 7.8):
        """
        Args:
            density: 材料密度 g/cm³ (默认不锈钢7.8)
        """
        self.density = density
    
    def parse(self, filepath: str) -> GeometryData:
        """解析STEP文件"""
        if not HAS_CADQUERY:
            raise RuntimeError("CadQuery未安装，无法解析STEP文件")
        
        try:
            # 使用CadQuery解析
            shape = cq.importers.importStep(filepath)
            solid = shape.val()
            
            # 获取几何数据
            volume_mm3 = solid.Volume()      # mm³
            area_mm2 = solid.Area()          # mm²
            bbox = solid.BoundingBox()
            
            # 转换单位
            volume_cm3 = volume_mm3 / 1000   # mm³ → cm³
            area_cm2 = area_mm2 / 100        # mm² → cm²
            
            # 计算尺寸
            size_x = bbox.xlen
            size_y = bbox.ylen
            size_z = bbox.zlen
            
            # 计算重量
            weight_kg = volume_cm3 * self.density / 1000
            
            return GeometryData(
                length=size_x,
                width=size_y,
                height=size_z,
                volume=volume_cm3,
                area=area_cm2,
                weight=weight_kg,
                source='step'
            )
            
        except Exception as e:
            logger.error(f"STEP解析失败: {e}")
            raise


class PDF2DParser:
    """2D PDF图纸解析器"""
    
    def __init__(self):
        self.dimension_patterns = [
            # 匹配 "384.00" 这样的尺寸
            r'(\d+\.?\d*)\s*mm',
            # 匹配 "长: 384" 这样的格式
            r'[长宽高直径外径内径深度][:：]\s*(\d+\.?\d*)',
        ]
    
    def parse(self, filepath: str) -> Optional[GeometryData]:
        """解析PDF文件提取尺寸"""
        if not HAS_PDFMINER:
            logger.warning("PDFMiner未安装，无法解析PDF")
            return None
        
        try:
            text = extract_text(filepath)
            
            # 提取尺寸信息
            dimensions = self._extract_dimensions(text)
            
            if not dimensions:
                return None
            
            # 尝试识别长宽高
            length = self._find_dimension(text, ['长', '长度', 'L'])
            width = self._find_dimension(text, ['宽', '宽度', 'W'])
            height = self._find_dimension(text, ['高', '高度', '厚度', 'H'])
            
            # 如果没有找到明确的标注，使用最大的三个尺寸
            if not all([length, width, height]) and dimensions:
                sorted_dims = sorted(dimensions, reverse=True)[:3]
                while len(sorted_dims) < 3:
                    sorted_dims.append(0)
                length = length or sorted_dims[0]
                width = width or sorted_dims[1]
                height = height or sorted_dims[2]
            
            # 估算体积和面积
            volume = (length * width * height) / 1000  # cm³
            area = 2 * (length*width + width*height + height*length) / 100  # cm²
            
            return GeometryData(
                length=length,
                width=width,
                height=height,
                volume=volume,
                area=area,
                weight=0,  # PDF无法直接获取重量
                source='pdf'
            )
            
        except Exception as e:
            logger.error(f"PDF解析失败: {e}")
            return None
    
    def _extract_dimensions(self, text: str) -> list:
        """提取所有尺寸数值"""
        dimensions = []
        for pattern in self.dimension_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    dim = float(match)
                    if 0.1 < dim < 10000:  # 合理范围
                        dimensions.append(dim)
                except:
                    pass
        return dimensions
    
    def _find_dimension(self, text: str, keywords: list) -> float:
        """根据关键词查找尺寸"""
        for keyword in keywords:
            pattern = rf'{keyword}[:：]?\s*(\d+\.?\d*)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return 0


class GeometryValidator:
    """几何数据校验器"""
    
    # 偏差阈值配置
    TOLERANCE_THRESHOLDS = {
        'length': 0.05,   # 长度偏差阈值 5%
        'width': 0.05,    # 宽度偏差阈值 5%
        'height': 0.05,   # 高度偏差阈值 5%
        'volume': 0.15,   # 体积偏差阈值 15%
    }
    
    def compare(self, step_data: GeometryData, pdf_data: GeometryData) -> ComparisonResult:
        """比对STEP和PDF数据"""
        warnings = []
        
        # 计算偏差
        length_diff = abs(step_data.length - pdf_data.length) / step_data.length if step_data.length > 0 else 0
        width_diff = abs(step_data.width - pdf_data.width) / step_data.width if step_data.width > 0 else 0
        height_diff = abs(step_data.height - pdf_data.height) / step_data.height if step_data.height > 0 else 0
        volume_diff = abs(step_data.volume - pdf_data.volume) / step_data.volume if step_data.volume > 0 else 0
        
        # 检查是否超过阈值
        if length_diff > self.TOLERANCE_THRESHOLDS['length']:
            warnings.append(f"⚠️ 长度偏差 {length_diff*100:.1f}% 超过阈值 {self.TOLERANCE_THRESHOLDS['length']*100}%")
        
        if width_diff > self.TOLERANCE_THRESHOLDS['width']:
            warnings.append(f"⚠️ 宽度偏差 {width_diff*100:.1f}% 超过阈值 {self.TOLERANCE_THRESHOLDS['width']*100}%")
        
        if height_diff > self.TOLERANCE_THRESHOLDS['height']:
            warnings.append(f"⚠️ 高度偏差 {height_diff*100:.1f}% 超过阈值 {self.TOLERANCE_THRESHOLDS['height']*100}%")
        
        if volume_diff > self.TOLERANCE_THRESHOLDS['volume']:
            warnings.append(f"⚠️ 体积偏差 {volume_diff*100:.1f}% 超过阈值 {self.TOLERANCE_THRESHOLDS['volume']*100}%")
        
        is_consistent = len(warnings) == 0
        
        return ComparisonResult(
            is_consistent=is_consistent,
            length_diff=length_diff,
            width_diff=width_diff,
            height_diff=height_diff,
            volume_diff=volume_diff,
            warnings=warnings,
            step_data=step_data,
            pdf_data=pdf_data
        )


# ============ 集成接口 ============

def validate_step_with_pdf(step_path: str, pdf_path: str = None) -> Dict:
    """
    STEP+PDF联动校验
    
    Args:
        step_path: STEP文件路径
        pdf_path: PDF文件路径（可选）
    
    Returns:
        {
            'step_data': {...},
            'pdf_data': {...},
            'comparison': {...},
            'warnings': [...]
        }
    """
    result = {
        'step_data': None,
        'pdf_data': None,
        'comparison': None,
        'warnings': []
    }
    
    # 1. 解析STEP
    step_parser = STEPParser()
    try:
        step_data = step_parser.parse(step_path)
        result['step_data'] = {
            'length': step_data.length,
            'width': step_data.width,
            'height': step_data.height,
            'volume': step_data.volume,
            'area': step_data.area,
            'weight': step_data.weight,
            'size_mm': f"{step_data.length:.1f} x {step_data.width:.1f} x {step_data.height:.1f}"
        }
    except Exception as e:
        result['warnings'].append(f"STEP解析失败: {str(e)}")
        return result
    
    # 2. 如果有PDF，解析并比对
    if pdf_path and os.path.exists(pdf_path):
        pdf_parser = PDF2DParser()
        pdf_data = pdf_parser.parse(pdf_path)
        
        if pdf_data:
            result['pdf_data'] = {
                'length': pdf_data.length,
                'width': pdf_data.width,
                'height': pdf_data.height,
                'volume': pdf_data.volume,
                'area': pdf_data.area,
            }
            
            # 3. 数据比对
            validator = GeometryValidator()
            comparison = validator.compare(step_data, pdf_data)
            
            result['comparison'] = {
                'is_consistent': comparison.is_consistent,
                'length_diff_pct': f"{comparison.length_diff*100:.1f}%",
                'width_diff_pct': f"{comparison.width_diff*100:.1f}%",
                'height_diff_pct': f"{comparison.height_diff*100:.1f}%",
                'volume_diff_pct': f"{comparison.volume_diff*100:.1f}%",
            }
            
            result['warnings'].extend(comparison.warnings)
    
    return result


# ============ 测试 ============

if __name__ == '__main__':
    # 测试用例
    step_file = "/home/admin/.openclaw/qqbot/downloads/G360L 舱门扩展-12''wafer 主体_1773973463882.STEP"
    pdf_file = "/home/admin/.openclaw/qqbot/downloads/G360L 舱门扩展-12''wafer 主体_1773973461176.pdf"
    
    print("=== STEP + 2D 联动校准测试 ===\n")
    
    result = validate_step_with_pdf(step_file, pdf_file)
    
    print("STEP数据:")
    print(json.dumps(result['step_data'], indent=2, ensure_ascii=False))
    
    if result['pdf_data']:
        print("\nPDF数据:")
        print(json.dumps(result['pdf_data'], indent=2, ensure_ascii=False))
        
        print("\n比对结果:")
        print(json.dumps(result['comparison'], indent=2, ensure_ascii=False))
    
    if result['warnings']:
        print("\n⚠️ 警告:")
        for w in result['warnings']:
            print(f"  {w}")