#!/usr/bin/env python3
"""
归档清单生成器
版本：1.0.0
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


class ReportGenerator:
    """归档清单生成器"""
    
    def __init__(self):
        self.output_dir = Path('./archives')
        logger.info("归档清单生成器已初始化")
    
    def generate_manifest(self, archive_path: Path, 
                         product_info: Dict,
                         download_results: List[Dict],
                         risk_results: List[Dict],
                         integrity_result: Dict) -> Path:
        """
        生成归档清单
        
        Args:
            archive_path: 归档文件夹路径
            product_info: 商品信息
            download_results: 下载结果
            risk_results: 风险检测结果
            integrity_result: 完整性校验结果
            
        Returns:
            归档清单文件路径
        """
        # 创建 Excel 文件
        manifest_path = archive_path / "03-商品资质档案" / "原图素材归档清单.xlsx"
        
        # 准备数据
        rows = []
        for i, download_result in enumerate(download_results):
            row = {
                '序号': f"{download_result.get('index', i+1):03d}",
                '文件名': download_result.get('filename', ''),
                '原始 URL': download_result.get('url', ''),
                '文件大小 (KB)': download_result.get('size_kb', 0),
                '格式': Path(download_result.get('filename', '')).suffix.upper().replace('.', ''),
                '下载状态': '✅ 成功' if download_result.get('success') else '❌ 失败',
                '完整性': '✅ 完整' if self._is_file_valid(download_result, integrity_result) else '❌ 损坏',
                '风险检测': self._get_risk_level(download_result.get('filename', ''), risk_results)
            }
            rows.append(row)
        
        # 创建 DataFrame
        df = pd.DataFrame(rows)
        
        # 调整列顺序
        columns = ['序号', '文件名', '原始 URL', '文件大小 (KB)', '格式', '下载状态', '完整性', '风险检测']
        df = df[[col for col in columns if col in df.columns]]
        
        # 写入 Excel
        with pd.ExcelWriter(manifest_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='原图素材归档清单', index=False)
            
            # 设置列宽
            worksheet = writer.sheets['原图素材归档清单']
            worksheet.column_dimensions['A'].width = 6
            worksheet.column_dimensions['B'].width = 25
            worksheet.column_dimensions['C'].width = 50
            worksheet.column_dimensions['D'].width = 12
            worksheet.column_dimensions['E'].width = 8
            worksheet.column_dimensions['F'].width = 10
            worksheet.column_dimensions['G'].width = 10
            worksheet.column_dimensions['H'].width = 15
        
        logger.info(f"归档清单已生成：{manifest_path}")
        return manifest_path
    
    def _is_file_valid(self, download_result: Dict, integrity_result: Dict) -> bool:
        """检查文件是否有效"""
        if not download_result.get('success'):
            return False
        
        filename = download_result.get('filename', '')
        for file_result in integrity_result.get('files', []):
            if file_result.get('filename') == filename:
                return file_result.get('valid', False)
        
        return True
    
    def _get_risk_level(self, filename: str, risk_results: List[Dict]) -> str:
        """获取风险等级"""
        for risk_result in risk_results:
            if risk_result.get('filename') == filename:
                risk_level = risk_result.get('risk_level', '无')
                if risk_level == '无':
                    return '✅ 无风险'
                else:
                    return f'⚠️  {risk_level}'
        
        return '未检测'
