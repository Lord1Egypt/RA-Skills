"""
XLS 模板写入辅助函数
用 xlutils.copy 复制 .xls 模板（保留样式），然后只覆盖数据单元格。
"""

import os
import xlrd
from xlutils.copy import copy as xl_copy
from typing import List, Dict, Any, Optional


def write_xls_with_template(
    template_path: str,
    output_path: str,
    main_sheet_name: str,
    main_data_start_row_0based: int,
    column_field_map: List[str],   # 列名列表（按列索引 0..N-1）
    records: List[Dict[str, Any]], # 记录列表，每个 dict 是 {field: value}
    extra_sheet_names: Optional[List[str]] = None,  # 需要保留的辅助 sheet
) -> str:
    """
    复制 .xls 模板（保留所有样式）并写入数据。

    Args:
        template_path: 模板 .xls 路径
        output_path: 输出 .xls 路径
        main_sheet_name: 主 sheet 名（写入数据的目标 sheet）
        main_data_start_row_0based: 数据起始行（0-based）
        column_field_map: 列名列表（与模板的列一一对应）
        records: 记录列表（每个 dict 是 {field_name: value}）
        extra_sheet_names: 需要保留的辅助 sheet 名（其他 sheet 会被删除）

    Returns:
        输出文件路径
    """
    # 读取模板（保留格式信息）
    rb = xlrd.open_workbook(template_path, formatting_info=True)

    # 复制为可写工作簿
    wb = xl_copy(rb)

    # 找到主 sheet
    main_sheet_idx = None
    for i, s in enumerate(wb._Workbook__worksheets):
        if s.name == main_sheet_name:
            main_sheet_idx = i
            break
    if main_sheet_idx is None:
        raise ValueError(f"主 sheet {main_sheet_name} 不存在")

    # 删除不需要的 sheet（保留主 sheet 和额外 sheet）
    keep_names = {main_sheet_name} | set(extra_sheet_names or [])
    sheets_to_remove = [s for s in wb._Workbook__worksheets if s.name not in keep_names]
    for s in sheets_to_remove:
        wb._Workbook__worksheets.remove(s)

    # 写入数据到主 sheet
    ws = wb.get_sheet(main_sheet_name)
    for row_idx, record in enumerate(records):
        excel_row = main_data_start_row_0based + row_idx
        for col_idx, field in enumerate(column_field_map):
            value = record.get(field, '')
            if value is None:
                value = ''
            # xlwt 0-based row/col
            ws.write(excel_row, col_idx, str(value))

    wb.save(output_path)
    return output_path
