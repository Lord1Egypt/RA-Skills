import pandas as pd
import logging
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, Any, List, Tuple
from pathlib import Path
import traceback

logger = logging.getLogger(__name__)

class InvoiceExtractionService:
    """发票信息提取服务 - 从信息提取-xml.py迁移的核心功能"""
    
    @staticmethod
    def extract_invoice_from_xml(docx_path: str) -> Dict[str, Any]:
        """
        从DOCX文件提取发票信息的主函数
        从原信息提取-xml.py迁移的核心功能
        """
        logger.info(f"[发票提取] 开始提取: {os.path.basename(docx_path)}")
        
        try:
            # 1. 从XML底层提取
            xml_text_lines, xml_tables = InvoiceExtractionService._extract_docx_xml_structure(docx_path)
            
            if not xml_text_lines and not xml_tables:
                logger.warning("[发票提取] 提取失败")
                return {}
            
            # 2. 识别发票类型
            full_text = '\n'.join(xml_text_lines)
            invoice_type = InvoiceExtractionService._identify_invoice_type(full_text, xml_text_lines, xml_tables)
            logger.info(f"[发票提取] 识别类型: {invoice_type}")
            
            # 3. 根据类型处理数据
            extracted_data = {'invoice_type': invoice_type}
            
            if invoice_type == 'vat':
                extracted_data = InvoiceExtractionService._process_vat_invoice(xml_text_lines, xml_tables, extracted_data)
            elif invoice_type == 'flight':
                extracted_data = InvoiceExtractionService._process_flight_invoice(xml_text_lines, xml_tables, extracted_data)
            elif invoice_type == 'train':
                extracted_data = InvoiceExtractionService._process_train_invoice(xml_text_lines, xml_tables, extracted_data)
            else:
                extracted_data = InvoiceExtractionService._process_unknown_invoice(xml_text_lines, xml_tables, extracted_data)
            
            # 4. 补充通用信息
            extracted_data = InvoiceExtractionService._supplement_common_fields(extracted_data, xml_text_lines, xml_tables)
            
            # 5. 生成智能字段
            extracted_data = InvoiceExtractionService._generate_smart_fields(extracted_data, invoice_type)
            
            # 6. 验证和清理
            extracted_data = InvoiceExtractionService._validate_and_clean_data(extracted_data, invoice_type)
            
            logger.info(f"[发票提取] 完成提取，共 {len(extracted_data)} 个字段")
            return extracted_data
            
        except Exception as e:
            logger.error(f"[发票提取] 提取异常: {str(e)}", exc_info=True)
            return {}
    
    @staticmethod
    def _extract_docx_xml_structure(docx_path: str) -> Tuple[List[str], List[List[List[str]]]]:
        """直接从DOCX文件的底层XML结构提取所有文本和表格数据"""
        logger.info(f"[XML提取] 开始提取: {os.path.basename(docx_path)}")
        
        all_text_lines = []
        all_tables_data = []
        
        try:
            with zipfile.ZipFile(docx_path, 'r') as docx_zip:
                # 只读取主文档XML，忽略页眉页脚
                if 'word/document.xml' not in docx_zip.namelist():
                    logger.warning("[XML提取] 警告: 找不到document.xml文件")
                    return all_text_lines, all_tables_data
                
                xml_content = docx_zip.read('word/document.xml')
                
                try:
                    root = ET.fromstring(xml_content)
                except ET.ParseError as e:
                    logger.warning(f"[XML提取] XML解析错误: {e}")
                    # 尝试修复XML
                    xml_content_str = xml_content.decode('utf-8', errors='ignore')
                    xml_content_str = re.sub(r'&#x[0-9a-fA-F]+;', '', xml_content_str)
                    root = ET.fromstring(xml_content_str.encode('utf-8'))
                
                namespaces = {
                    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
                    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
                    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
                    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
                }
                
                # 提取所有段落文本（主体内容）
                paragraph_count = 0
                for para_elem in root.findall('.//w:p', namespaces):
                    paragraph_count += 1
                    paragraph_text = InvoiceExtractionService._extract_text_from_paragraph(para_elem, namespaces)
                    
                    if paragraph_text and paragraph_text.strip():
                        all_text_lines.append(paragraph_text.strip())
                
                logger.info(f"[XML提取] 提取了 {paragraph_count} 个段落")
                
                # 提取所有表格数据
                table_count = 0
                for table_elem in root.findall('.//w:tbl', namespaces):
                    table_count += 1
                    table_data = InvoiceExtractionService._extract_table_from_xml(table_elem, namespaces)
                    
                    if table_data:
                        all_tables_data.append(table_data)
                        
                        # 将表格数据添加到文本行中用于正则匹配
                        for row in table_data:
                            row_text = ' | '.join([str(cell).strip() for cell in row if str(cell).strip()])
                            if row_text:
                                all_text_lines.append(row_text)
                
                logger.info(f"[XML提取] 提取了 {table_count} 个表格")
                logger.info(f"[XML提取] 总共提取了 {len(all_text_lines)} 行文本")
                
                return all_text_lines, all_tables_data
                
        except Exception as e:
            logger.error(f"[XML提取] 错误: {e}", exc_info=True)
        
        return all_text_lines, all_tables_data
    
    @staticmethod
    def _extract_text_from_paragraph(para_elem, namespaces) -> str:
        """从XML段落元素中提取文本"""
        text_parts = []
        
        for run_elem in para_elem.findall('.//w:r', namespaces):
            text_elem = run_elem.find('.//w:t', namespaces)
            if text_elem is not None and text_elem.text:
                text_parts.append(text_elem.text)
            
            # 保留制表符和换行符
            tab_elem = run_elem.find('.//w:tab', namespaces)
            if tab_elem is not None:
                text_parts.append('\t')
            
            br_elem = run_elem.find('.//w:br', namespaces)
            if br_elem is not None:
                text_parts.append('\n')
        
        paragraph_text = ''.join(text_parts)
        paragraph_text = InvoiceExtractionService._clean_xml_text(paragraph_text)
        
        return paragraph_text
    
    @staticmethod
    def _extract_table_from_xml(table_elem, namespaces) -> List[List[str]]:
        """从XML表格元素中提取表格数据"""
        table_data = []
        
        for row_elem in table_elem.findall('.//w:tr', namespaces):
            row_data = []
            
            for cell_elem in row_elem.findall('.//w:tc', namespaces):
                cell_text = InvoiceExtractionService._extract_text_from_cell(cell_elem, namespaces)
                row_data.append(cell_text)
            
            # 只添加非空行
            if any(cell.strip() for cell in row_data):
                table_data.append(row_data)
        
        return table_data
    
    @staticmethod
    def _extract_text_from_cell(cell_elem, namespaces) -> str:
        """从XML单元格元素中提取文本"""
        cell_text_parts = []
        
        for para_elem in cell_elem.findall('.//w:p', namespaces):
            para_text = InvoiceExtractionService._extract_text_from_paragraph(para_elem, namespaces)
            if para_text.strip():
                cell_text_parts.append(para_text)
        
        cell_text = ' '.join(cell_text_parts)
        return cell_text.strip()
    
    @staticmethod
    def _clean_xml_text(text: str) -> str:
        """清理从XML提取的文本"""
        if not text:
            return ""
        
        # 替换XML实体
        replacements = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&apos;': "'",
        }
        
        for entity, char in replacements.items():
            text = text.replace(entity, char)
        
        # 注意：需要处理点号和空格的各种组合
        text = re.sub(r'(\d+)\.\s+(\d{1,2})', r'\1.\2', text)  # "46. 50" -> "46.50"
        text = re.sub(r'(\d+)\s+\.\s*(\d{1,2})', r'\1.\2', text)  # "46 .50" -> "46.50"
        text = re.sub(r'(\d+)\s+\.\s+(\d{1,2})', r'\1.\2', text)  # "46 . 50" -> "46.50"
        
        # 规范化空格
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    @staticmethod
    def _identify_invoice_type(full_text: str, text_lines: List[str], tables: List[List[List[str]]]) -> str:
        """
        智能识别发票类型
        返回: 'vat' (增值税), 'flight' (机票), 'train' (火车票), 'unknown' (未知)
        """
        full_text_lower = full_text.lower()
        
        # 检查关键词模式
        vat_patterns = ['增值税专用发票', '电子发票（增值税', '项目名称', '规格型号', '税率/征收率', '价税合计']
        flight_patterns = ['航空运输电子客票行程单', '国内国际标识', '旅客姓名', '航班号', '承运人', '电子客票号码']
        train_patterns = ['铁路电子客票', '火车票', '车次', '车厢座位', '二等座', '一等座', '硬座', '软座', '站', '自.*至', '开票日期']
        
        vat_score = sum(1 for pattern in vat_patterns if pattern in full_text)
        flight_score = sum(1 for pattern in flight_patterns if pattern in full_text)
        train_score = sum(1 for pattern in train_patterns if pattern in full_text)
        
        # 检查表格结构
        table_structure_score = {'vat': 0, 'flight': 0, 'train': 0}
        for table in tables:
            table_text = ' '.join([' '.join(row) for row in table])
            if any(keyword in table_text for keyword in ['项目名称', '规格型号', '单价', '金额']):
                table_structure_score['vat'] += 2
            if any(keyword in table_text for keyword in ['票价', '燃油附加费', '增值税税额', '民航发展基金']):
                table_structure_score['flight'] += 2
            if any(keyword in table_text for keyword in ['车次', '车厢', '座位', '票价']):
                table_structure_score['train'] += 2
        
        # 计算总分
        total_vat = vat_score + table_structure_score['vat']
        total_flight = flight_score + table_structure_score['flight']
        total_train = train_score + table_structure_score['train']
        
        logger.info(f"[类型识别] 增值税得分: {total_vat}, 机票得分: {total_flight}, 火车票得分: {total_train}")
        
        # 确定类型
        if total_vat >= max(total_flight, total_train, 2):
            return 'vat'
        elif total_flight >= max(total_vat, total_train, 2):
            return 'flight'
        elif total_train >= max(total_vat, total_flight, 2):
            return 'train'
        else:
            return 'unknown'
    
    @staticmethod
    def _process_vat_invoice(text_lines: List[str], tables: List[List[List[str]]], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理增值税发票"""
        logger.info("[处理模式] 增值税发票模式")
        full_text = '\n'.join(text_lines)
        
        # 1. 提取基础信息
        patterns = {
            'invoice_no': r'(?:发票号码|电子发票号|发票号)[\s:：]*(\d{18,25})',
            'invoice_date': r'(?:开票日期|填开日期|日期)[\s:：]*(\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{1,2}-\d{1,2})',
            'buyer_name': r'购买方[\s:：]*名称[\s:：]*([^\n|;；]+?)(?=[\s|;；]*(?:统一社会信用代码|纳税人识别号|税号|$))',
            'buyer_tax_id': r'(?:购买方.*?统一社会信用代码|纳税人识别号|税号)[\s:：]*([A-Z0-9]{15,20})',
            'total_with_tax': r'价税合计[\s:：]*[¥￥]?\s*([\d,]+\.\d{2})',
            'total_chinese': r'(?:价税合计.*?大写|大写金额)[\s:：]*([零壹贰叁肆伍陆柒捌玖拾佰仟万亿元角分整]+)',
            'drawer': r'开票人[\s:：]*([^\n|]+)',
            'seller_bank': r'开户银行[\s:：]*([^\n|]+)',
            'seller_account': r'账号[\s:：]*(\d{10,25})',
        }
        
        for field, pattern in patterns.items():
            try:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    extracted_data[field] = InvoiceExtractionService._clean_extracted_value(match.group(1))
                    logger.info(f"[增值税提取] {field}: {extracted_data[field]}")
            except Exception as e:
                logger.warning(f"[增值税提取] {field} 错误: {e}")
        
        # 2. 提取销售方信息
        extracted_data = InvoiceExtractionService._extract_seller_info_vat(full_text, extracted_data)
        
        # 3. 处理商品表格 - 重点优化这里
        extracted_data = InvoiceExtractionService._process_vat_tables_optimized(tables, extracted_data)
        
        # 4. 补充金额信息
        extracted_data = InvoiceExtractionService._supplement_vat_amounts(full_text, extracted_data)
        
        return extracted_data
    
    @staticmethod
    def _extract_seller_info_vat(full_text: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取增值税发票的销售方信息"""
        logger.info("[销售方提取] 开始提取销售方信息")
        
        # 方法1: 正则表达式精确匹配销售方名称
        seller_patterns = [
            r'销售方[\s:：]*名称[\s:：]*([^\n;；]+?)(?=[\s;；]*(?:统一社会信用代码|纳税人识别号|税号|$))',
            r'(?:销售方信息|销 售 方 信 息)[\s\S]*?名称[\s:：]*([^\n;；]+)',
            r'销售方[^\n]*?名称[\s:：]*([^\n;；]+)',
        ]
        
        for pattern in seller_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                seller_name = InvoiceExtractionService._clean_extracted_value(match.group(1))
                if seller_name and len(seller_name) > 2:
                    extracted_data['seller_name'] = seller_name
                    logger.info(f"[销售方提取] 找到销售方名称: {seller_name}")
                    break
        
        # 方法2: 提取销售方税号
        tax_id_patterns = [
            r'销售方[^\n]*?(?:统一社会信用代码|纳税人识别号|税号)[\s:：]*([A-Z0-9]{15,20})',
            r'(?:销售方信息|销 售 方 信 息)[\s\S]*?(?:统一社会信用代码|纳税人识别号|税号)[\s:：]*([A-Z0-9]{15,20})',
            r'([A-Z0-9]{15,20})'
        ]
        
        buyer_tax_id = extracted_data.get('buyer_tax_id', '')
        
        for pattern in tax_id_patterns:
            matches = re.findall(pattern, full_text)
            if matches:
                logger.info(f"[销售方提取] 找到税号候选: {matches}")
                
                if len(matches) == 1:
                    if buyer_tax_id and matches[0] == buyer_tax_id:
                        logger.info(f"[销售方提取] 唯一税号与购买方税号相同，跳过")
                    else:
                        extracted_data['seller_tax_id'] = matches[0]
                        logger.info(f"[销售方提取] 找到销售方税号: {matches[0]}")
                        break
                elif len(matches) >= 2:
                    for i, tax_id in enumerate(matches):
                        if i == 0 and buyer_tax_id and tax_id == buyer_tax_id:
                            continue
                        if i >= 1:
                            extracted_data['seller_tax_id'] = tax_id
                            logger.info(f"[销售方提取] 选择第{i+1}个税号为销售方税号: {tax_id}")
                            break
                    break
        
        # 方法3: 提取销售方银行和账号
        if 'seller_bank' not in extracted_data:
            bank_patterns = [
                r'销方开户银行[\s:：]*([^\n;；]+)',
                r'销售方.*?开户银行[\s:：]*([^\n;；]+)',
                r'开户银行[\s:：]*([^\n;；]+?)(?=[\s;；]*(?:账号|银行账号|$))',
            ]
            
            for pattern in bank_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    extracted_data['seller_bank'] = InvoiceExtractionService._clean_extracted_value(match.group(1))
                    logger.info(f"[销售方提取] 找到销售方银行: {extracted_data['seller_bank']}")
                    break
        
        if 'seller_account' not in extracted_data:
            account_patterns = [
                r'销方.*?账号[\s:：]*(\d{10,25})',
                r'销售方.*?账号[\s:：]*(\d{10,25})',
                r'银行账号[\s:：]*(\d{10,25})',
            ]
            
            for pattern in account_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    extracted_data['seller_account'] = match.group(1)
                    logger.info(f"[销售方提取] 找到销售方账号: {extracted_data['seller_account']}")
                    break
        
        return extracted_data
    
    @staticmethod
    def _process_vat_tables_optimized(tables: List[List[List[str]]], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理增值税发票表格 - 优化版，字段命名清晰化"""
        logger.info("[增值税表格] 开始处理表格数据")
        
        for table_idx, table_rows in enumerate(tables):
            if len(table_rows) < 2:
                continue
                
            logger.info(f"[增值税表格] 处理表格 {table_idx+1}，共 {len(table_rows)} 行")
            
            # 1. 寻找商品表头
            header_found = False
            header_row_idx = -1
            header_row = []
            
            for row_idx, row in enumerate(table_rows):
                row_str = ' | '.join(row)
                if '项目名称' in row_str and any(keyword in row_str for keyword in ['规格型号', '单位', '数量', '单价', '金额', '税率', '税额']):
                    header_found = True
                    header_row_idx = row_idx
                    header_row = row
                    logger.info(f"[增值税表格] 发现商品表头 (表格{table_idx+1}, 行{row_idx+1})")
                    break
            
            if header_found and header_row:
                # 2. 优先从表头提取合计信息
                extracted_data = InvoiceExtractionService._extract_totals_from_header(header_row, extracted_data)
                
                # 3. 建立列映射
                col_mapping = {}
                keyword_to_field = {
                    '项目名称': 'goods_name',
                    '规格型号': 'goods_spec',
                    '单位': 'goods_unit',
                    '数量': 'goods_quantity',
                    '单价': 'goods_unit_price',
                    '金额': 'goods_amount',
                    '税率': 'goods_tax_rate',
                    '征收率': 'goods_tax_rate',
                    '税额': 'goods_tax'
                }
                
                for col_idx, cell in enumerate(header_row):
                    cell_clean = str(cell).strip()
                    for keyword, field in keyword_to_field.items():
                        if keyword in cell_clean and field not in col_mapping:
                            col_mapping[field] = col_idx
                            logger.info(f"[列映射] {keyword} -> {field} (列{col_idx})")
                            break
                
                logger.info(f"[列映射] 完整映射: {col_mapping}")
                
                # 4. 提取商品数据行（只取第一行商品）
                data_start = header_row_idx + 1
                for data_idx in range(data_start, min(data_start + 2, len(table_rows))):
                    data_row = table_rows[data_idx]
                    row_str = ' | '.join(data_row)
                    
                    # 跳过空行或表头行
                    if not any(str(cell).strip() for cell in data_row) or '项目名称' in row_str:
                        continue
                    
                    # 检查是否包含商品特征
                    if '*' in row_str or any(re.search(r'\d+\.\d{2,}', str(cell)) for cell in data_row):
                        logger.info(f"[增值税表格] 发现商品数据行 {data_idx+1}: {[str(cell)[:20] for cell in data_row]}")
                        
                        # 根据列映射提取商品字段
                        for field, col_idx in col_mapping.items():
                            if col_idx < len(data_row):
                                value = str(data_row[col_idx]).strip()
                                if value and field.startswith('goods_'):  # 只提取商品字段
                                    extracted_data[field] = value
                                    logger.info(f"[商品提取] {field}: {value}")
                        
                        # 如果通过列映射没有提取到关键字段，使用智能分配
                        if 'goods_amount' not in extracted_data or 'goods_tax' not in extracted_data:
                            extracted_data = InvoiceExtractionService._smart_assign_goods_fields(data_row, extracted_data)
                        
                        break  # 只处理第一行商品
    
        logger.info(f"[增值税表格] 处理完成，提取字段: {list(extracted_data.keys())}")
        return extracted_data
    
    @staticmethod
    def _extract_totals_from_header(header_row: List[str], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """从表头行提取合计信息 - 增强版"""
        if not header_row or len(header_row) == 0:
            return extracted_data
        
        # 检查表头的第一个单元格（根据日志，这里包含合计信息）
        first_cell_text = str(header_row[0])
        logger.info(f"[合计提取] 分析表头第一个单元格，长度: {len(first_cell_text)}")
        
        if len(first_cell_text) > 100:
            logger.info(f"[合计提取] 表头单元格前150字符: {first_cell_text[:150]}")
            logger.info(f"[合计提取] 表头单元格后200字符: {first_cell_text[-200:]}")
        
        # 增强的正则表达式模式
        total_patterns = [
            # 模式1: "合 ¥35477.87 ¥4612.13" 或 "合 计 ¥35477.87 ¥4612.13"
            r'合\s*(?:计)?[^\d¥]*¥?\s*([\d,]+\.\d{2})[^\d¥]*¥?\s*([\d,]+\.\d{2})',
            # 模式2: "合计 ¥35477.87 ¥4612.13"
            r'合计[^\d¥]*¥?\s*([\d,]+\.\d{2})[^\d¥]*¥?\s*([\d,]+\.\d{2})',
            # 模式3: "金额 ¥35477.87 税额 ¥4612.13"
            r'(?:金额|合计金额)[^\d¥]*¥?\s*([\d,]+\.\d{2})[^\d¥]*(?:税额|合计税额)[^\d¥]*¥?\s*([\d,]+\.\d{2})',
        ]
        
        for pattern_idx, pattern in enumerate(total_patterns):
            match = re.search(pattern, first_cell_text)
            if match:
                total_amount = match.group(1).replace(',', '')
                total_tax = match.group(2).replace(',', '')
                
                logger.info(f"[合计提取] 模式{pattern_idx+1}匹配到: 合计金额={total_amount}, 合计税额={total_tax}")
                
                # 验证金额大小：通常合计金额 > 合计税额
                try:
                    amount_float = float(total_amount)
                    tax_float = float(total_tax)
                    
                    if amount_float > tax_float:  # 合理验证
                        extracted_data['total_amount'] = total_amount
                        extracted_data['total_tax'] = total_tax
                        logger.info(f"[合计提取] 确认提取: total_amount={total_amount}, total_tax={total_tax}")
                        return extracted_data
                    else:
                        logger.warning(f"[合计提取] 金额验证失败: 合计金额{amount_float} <= 合计税额{tax_float}")
                except ValueError as e:
                    logger.warning(f"[合计提取] 金额转换失败: {e}")
        
        # 如果没有匹配，尝试查找所有金额对
        logger.info(f"[合计提取] 正则匹配失败，尝试查找所有金额对")
        all_amount_pairs = re.findall(r'¥?\s*([\d,]+\.\d{2})[^\d¥]*¥?\s*([\d,]+\.\d{2})', first_cell_text)
        if all_amount_pairs:
            logger.info(f"[合计提取] 找到 {len(all_amount_pairs)} 个金额对")
            # 取最后一对（通常是合计金额和税额）
            last_pair = all_amount_pairs[-1]
            try:
                amount_float = float(last_pair[0].replace(',', ''))
                tax_float = float(last_pair[1].replace(',', ''))
                
                if amount_float > tax_float:  # 验证合理性
                    extracted_data['total_amount'] = last_pair[0].replace(',', '')
                    extracted_data['total_tax'] = last_pair[1].replace(',', '')
                    logger.info(f"[合计提取] 从金额对提取: total_amount={extracted_data['total_amount']}, total_tax={extracted_data['total_tax']}")
                else:
                    logger.warning(f"[合计提取] 金额对验证失败: 金额{amount_float} <= 税额{tax_float}")
            except ValueError:
                pass
        
        # 最后尝试：查找包含"合"的行中的金额
        if 'total_amount' not in extracted_data or 'total_tax' not in extracted_data:
            for row_idx, row in enumerate(header_row):
                row_text = str(row)
                if '合' in row_text:
                    amounts = re.findall(r'¥?\s*([\d,]+\.\d{2})', row_text)
                    if len(amounts) >= 2:
                        try:
                            amount_float = float(amounts[0].replace(',', ''))
                            tax_float = float(amounts[1].replace(',', ''))
                            if amount_float > tax_float:
                                extracted_data['total_amount'] = amounts[0].replace(',', '')
                                extracted_data['total_tax'] = amounts[1].replace(',', '')
                                logger.info(f"[合计提取] 从'合'行提取: total_amount={extracted_data['total_amount']}, total_tax={extracted_data['total_tax']}")
                                break
                        except ValueError:
                            pass
        
        return extracted_data
    
    @staticmethod
    def _smart_assign_goods_fields(data_row, extracted_data):
        """智能分配商品字段（不涉及合计字段）"""
        logger.info(f"[商品分配] 开始智能分配商品字段")
        
        # 先收集所有非空单元格
        non_empty_cells = []
        for idx, cell in enumerate(data_row):
            cell_str = str(cell).strip()
            if cell_str:
                non_empty_cells.append((idx, cell_str))
        
        logger.info(f"[商品分配] 非空单元格: {non_empty_cells}")
        
        # 定义常见单位词（放在方法开始，确保整个方法都能访问）
        unit_keywords = ['升', '吨', '件', '个', '箱', '瓶', '套', '台', '张', '天', '项', '次', '平方米']
        
        # 1. 识别商品名称（以*开头）
        if 'goods_name' not in extracted_data:
            for idx, cell in non_empty_cells:
                if cell.startswith('*'):
                    extracted_data['goods_name'] = cell
                    logger.info(f"[商品分配] 识别商品名称: {cell}")
                    break
        
        # 2. 识别商品金额和税额（两位小数的数字）
        amount_candidates = []
        for idx, cell in non_empty_cells:
            # 检查是否两位小数的数字
            if re.match(r'^\d[\d,]*\.\d{2}$', cell):
                amount_candidates.append((idx, cell))
        
        logger.info(f"[商品分配] 金额候选: {amount_candidates}")
        
        if len(amount_candidates) >= 2:
            # 通常商品金额在前，商品税额在后
            # 但需要验证：商品税额 = 商品金额 * 税率
            if 'goods_amount' not in extracted_data and 'goods_tax' not in extracted_data:
                extracted_data['goods_amount'] = amount_candidates[-2][1]  # 倒数第二个
                extracted_data['goods_tax'] = amount_candidates[-1][1]    # 倒数第一个
                logger.info(f"[商品分配] 分配: goods_amount={extracted_data['goods_amount']}, goods_tax={extracted_data['goods_tax']}")
        
        # 3. 识别商品单位（常见单位词）
        if 'goods_unit' not in extracted_data:
            for idx, cell in non_empty_cells:
                if cell in unit_keywords:
                    extracted_data['goods_unit'] = cell
                    logger.info(f"[商品分配] 识别单位: {cell}")
                    break
        
        # 4. 识别商品数量（纯数字）
        if 'goods_quantity' not in extracted_data:
            for idx, cell in non_empty_cells:
                if re.match(r'^\d+$', cell) and '.' not in cell:  # 整数
                    extracted_data['goods_quantity'] = cell
                    logger.info(f"[商品分配] 识别数量: {cell}")
                    break
        
        # 5. 识别商品单价（多位小数的数字）
        if 'goods_unit_price' not in extracted_data:
            for idx, cell in non_empty_cells:
                if re.match(r'^\d+\.\d{6,}$', cell):  # 6位以上小数
                    extracted_data['goods_unit_price'] = cell
                    logger.info(f"[商品分配] 识别单价: {cell}")
                    break
        
        # 6. 识别商品税率（带%符号）
        if 'goods_tax_rate' not in extracted_data:
            for idx, cell in non_empty_cells:
                if '%' in cell:
                    extracted_data['goods_tax_rate'] = cell
                    logger.info(f"[商品分配] 识别税率: {cell}")
                    break
        
        # 7. 识别商品规格（剩余的文本字段）
        if 'goods_spec' not in extracted_data:
            for idx, cell in non_empty_cells:
                cell_lower = cell.lower()
                # 排除已识别的字段类型
                if (not re.match(r'^\d', cell) and  # 不以数字开头
                    '%' not in cell and  # 不是税率
                    not any(keyword in cell for keyword in unit_keywords) and  # 不是单位
                    not cell.startswith('*')):  # 不是商品名称
                    extracted_data['goods_spec'] = cell
                    logger.info(f"[商品分配] 识别规格: {cell}")
                    break
        
        logger.info(f"[商品分配] 完成，商品字段: { {k: v for k, v in extracted_data.items() if k.startswith('goods_')} }")
        return extracted_data
    
    @staticmethod
    def _supplement_vat_amounts(full_text: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """补充增值税发票金额信息"""
        # 提取所有金额
        all_amounts = re.findall(r'[¥￥]?\s*([\d,]+\.\d{2})', full_text)
        if all_amounts:
            try:
                amounts_float = [(float(amt.replace(',', '')), amt) for amt in all_amounts]
                amounts_float.sort()
                
                # 如果还没有商品单价，取最小的作为商品单价候选
                if 'goods_unit_price' not in extracted_data and amounts_float:
                    # 寻找多位小数的作为单价
                    for amount, amt_str in amounts_float:
                        if len(str(amount).split('.')[1]) >= 4:  # 4位以上小数可能是单价
                            extracted_data['goods_unit_price'] = amt_str
                            break
                
                # 如果还没有商品金额和税额，取中间的两个
                if ('goods_amount' not in extracted_data or 'goods_tax' not in extracted_data) and len(amounts_float) >= 2:
                    if len(amounts_float) == 2:
                        extracted_data['goods_amount'] = amounts_float[0][1]
                        extracted_data['goods_tax'] = amounts_float[1][1]
                    elif len(amounts_float) >= 3:
                        # 取中间的两个（避开最小和最大）
                        mid_idx = len(amounts_float) // 2
                        extracted_data['goods_amount'] = amounts_float[mid_idx-1][1]
                        extracted_data['goods_tax'] = amounts_float[mid_idx][1]
            except:
                pass
        
        # 补充税率信息
        if 'goods_tax_rate' not in extracted_data:
            tax_rate_patterns = [
                r'(\d+(?:\.\d+)?%)',
                r'税率[\s:：]*(\d+(?:\.\d+)?%)',
                r'征收率[\s:：]*(\d+(?:\.\d+)?%)',
            ]
            
            for pattern in tax_rate_patterns:
                match = re.search(pattern, full_text)
                if match:
                    extracted_data['goods_tax_rate'] = match.group(1)
                    logger.info(f"[补充税率] 找到税率: {extracted_data['goods_tax_rate']}")
                    break
        
        return extracted_data
    
    @staticmethod
    def _validate_and_clean_data(extracted_data: Dict[str, Any], invoice_type: str) -> Dict[str, Any]:
        """验证和清理数据 - 字段命名清晰化版本"""
        logger.info(f"[验证清理] 开始验证清理，发票类型: {invoice_type}")
        
        # 清理金额格式
        amount_fields = [
            'total_with_tax', 'goods_amount', 'total_amount', 'total_tax', 'goods_unit_price', 
            'goods_tax', 'fuel_surcharge', 'aviation_fund', 'insurance_fee'
        ]
        
        for field in amount_fields:
            if field in extracted_data and extracted_data[field]:
                # 移除逗号和货币符号
                cleaned = str(extracted_data[field]).replace(',', '').replace('¥', '').replace('￥', '').strip()
                if cleaned:
                    try:
                        amount_float = float(cleaned)
                        extracted_data[field] = f"{amount_float:.2f}"
                        logger.info(f"[清理金额] {field}: {extracted_data[field]}")
                    except ValueError:
                        logger.warning(f"[清理金额] {field} 转换失败: {cleaned}")
                        extracted_data[field] = cleaned
        
        # 关键：计算价税合计（如果合计金额和合计税额都存在）
        if 'total_amount' in extracted_data and 'total_tax' in extracted_data:
            try:
                total_amount = float(extracted_data['total_amount'])
                total_tax = float(extracted_data['total_tax'])
                
                # 验证合理性：合计金额 > 合计税额
                if total_amount > total_tax:
                    total_with_tax = total_amount + total_tax
                    
                    # 如果价税合计字段不存在或与计算值不一致，使用计算值
                    if 'total_with_tax' not in extracted_data:
                        extracted_data['total_with_tax'] = f"{total_with_tax:.2f}"
                        logger.info(f"[价税计算] 计算价税合计: {extracted_data['total_with_tax']}")
                    else:
                        try:
                            existing_total = float(extracted_data['total_with_tax'])
                            calculated_total = total_amount + total_tax
                            # 如果差异超过0.01，使用计算值
                            if abs(existing_total - calculated_total) > 0.01:
                                extracted_data['total_with_tax'] = f"{calculated_total:.2f}"
                                logger.info(f"[价税计算] 修正价税合计: {extracted_data['total_with_tax']}")
                        except:
                            extracted_data['total_with_tax'] = f"{total_with_tax:.2f}"
                            logger.info(f"[价税计算] 计算价税合计(替代): {extracted_data['total_with_tax']}")
                else:
                    logger.warning(f"[验证] 合计金额{total_amount} <= 合计税额{total_tax}，可能提取错误")
            except Exception as e:
                logger.warning(f"[价税计算] 计算价税合计失败: {e}")
        
        # 清理税率格式
        if 'goods_tax_rate' in extracted_data and extracted_data['goods_tax_rate']:
            tax_rate = extracted_data['goods_tax_rate']
            if tax_rate and '%' not in tax_rate:
                if re.match(r'^\d+(?:\.\d+)?$', tax_rate):
                    extracted_data['goods_tax_rate'] = tax_rate + '%'
                    logger.info(f"[清理税率] 添加百分号: {extracted_data['goods_tax_rate']}")
        
        # 清理日期格式
        date_fields = ['invoice_date', 'flight_date', 'travel_date']
        for field in date_fields:
            if field in extracted_data and extracted_data[field]:
                date_str = extracted_data[field]
                date_str = date_str.replace('年', '-').replace('月', '-').replace('日', '')
                extracted_data[field] = date_str
                logger.info(f"[清理日期] {field}: {extracted_data[field]}")
        
        # 验证商品金额和税额的关系（如果税率已知）
        if 'goods_amount' in extracted_data and 'goods_tax' in extracted_data and 'goods_tax_rate' in extracted_data:
            try:
                goods_amount = float(extracted_data['goods_amount'])
                goods_tax = float(extracted_data['goods_tax'])
                tax_rate_str = extracted_data['goods_tax_rate']
                
                # 提取税率百分比
                tax_rate_match = re.search(r'(\d+(?:\.\d+)?)%', tax_rate_str)
                if tax_rate_match:
                    tax_rate_percent = float(tax_rate_match.group(1))
                    expected_tax = goods_amount * (tax_rate_percent / 100)
                    
                    # 计算实际税额与期望税额的差异
                    tax_diff = abs(goods_tax - expected_tax)
                    tax_diff_percent = tax_diff / expected_tax * 100 if expected_tax > 0 else 100
                    
                    if tax_diff_percent > 5:  # 差异超过5%
                        logger.warning(f"[验证] 商品税额{goods_tax}与期望税额{expected_tax:.2f}差异较大({tax_diff_percent:.1f}%)")
            except Exception as e:
                logger.warning(f"[验证] 商品金额税额验证失败: {e}")
        
        logger.info(f"[验证清理] 完成，关键字段: { {k: v for k, v in extracted_data.items() if 'total_' in k or 'goods_' in k} }")
        return extracted_data
    
    @staticmethod
    def _process_flight_invoice(text_lines: List[str], tables: List[List[List[str]]], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理机票发票"""
        logger.info("[处理模式] 机票发票模式")
        full_text = '\n'.join(text_lines)
        
        # 提取基础信息
        patterns = {
            'invoice_no': r'(?:发票号码|电子发票号)[\s:：]*(\d{18,25})',
            'invoice_date': r'(?:填开日期|开票日期)[\s:：]*(\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{1,2}-\d{1,2})',
            'buyer_name': r'购买方名称[\s:：]*([^\n;；]+?)(?=\s*(?:统一社会信用代码|纳税人识别号|$))',
            'buyer_tax_id': r'统一社会信用代码/纳税人识别号[\s:：]*([A-Z0-9]{15,20})',
            'total_with_tax': r'合计[\s:：]*CNY\s*([\d,]+\.\d{2})',
            'passenger_name': r'旅客姓名[\s:：]*([^\n;；]+)',
            'flight_no': r'航班号[\s:：]*([^\n;；]+)',
            'carrier': r'承运人[\s:：]*([^\n;；]+)',
            'ticket_no': r'电子客票号码[\s:：]*([^\n;；]+)',
            'insurance_fee': r'保险费[\s:：]*CNY?\s*([\d,]+\.\d{2})',
        }
        
        for field, pattern in patterns.items():
            try:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    extracted_data[field] = InvoiceExtractionService._clean_extracted_value(match.group(1))
                    logger.info(f"[机票提取] {field}: {extracted_data[field]}")
            except Exception as e:
                logger.warning(f"[机票提取] {field} 错误: {e}")
        
        # 提取行程信息
        extracted_data = InvoiceExtractionService._extract_flight_itinerary(full_text, extracted_data)
        
        # 提取价格明细
        extracted_data = InvoiceExtractionService._extract_flight_prices(full_text, extracted_data)
        
        return extracted_data
    
    @staticmethod
    def _extract_flight_itinerary(full_text: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取机票行程信息"""
        departure_match = re.search(r'自[\s:：]*([^\n;；]+?)(?=\s*至|$)', full_text)
        arrival_match = re.search(r'至[\s:：]*([^\n;；]+?)(?=\s*至|$)', full_text)
        
        if departure_match:
            extracted_data['departure_airport'] = InvoiceExtractionService._clean_extracted_value(departure_match.group(1))
            logger.info(f"[机票行程] 出发机场: {extracted_data['departure_airport']}")
        
        if arrival_match:
            extracted_data['arrival_airport'] = InvoiceExtractionService._clean_extracted_value(arrival_match.group(1))
            logger.info(f"[机票行程] 到达机场: {extracted_data['arrival_airport']}")
        
        date_match = re.search(r'日期[\s:：]*(\d{4}年\d{1,2}月\d{1,2}日)', full_text)
        time_match = re.search(r'时间[\s:：]*(\d{1,2}:\d{2})', full_text)
        
        if date_match:
            extracted_data['flight_date'] = date_match.group(1)
            logger.info(f"[机票行程] 航班日期: {extracted_data['flight_date']}")
        
        if time_match:
            extracted_data['departure_time'] = time_match.group(1)
            logger.info(f"[机票行程] 起飞时间: {extracted_data['departure_time']}")
        
        seat_match = re.search(r'座位等级[\s:：]*([^\n;；]+)', full_text)
        if seat_match:
            extracted_data['flight_seat_class'] = seat_match.group(1)
            logger.info(f"[机票行程] 座位等级: {extracted_data['flight_seat_class']}")
        
        return extracted_data
    
    @staticmethod
    def _extract_flight_prices(full_text: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取机票价格明细"""
        fare_match = re.search(r'票价[\s:：]*CNY\s*([\d,]+\.\d{2})', full_text)
        if fare_match:
            extracted_data['goods_unit_price'] = fare_match.group(1)
            logger.info(f"[机票价格] 票价: {extracted_data['goods_unit_price']}")
        
        fuel_match = re.search(r'燃油附加费[\s:：]*CNY\s*([\d,]+\.\d{2})', full_text)
        if fuel_match:
            extracted_data['fuel_surcharge'] = fuel_match.group(1)
            logger.info(f"[机票价格] 燃油附加费: {extracted_data['fuel_surcharge']}")
        
        tax_match = re.search(r'增值税税额[\s:：]*CNY\s*([\d,]+\.\d{2})', full_text)
        if tax_match:
            extracted_data['goods_tax'] = tax_match.group(1)
            logger.info(f"[机票价格] 增值税税额: {extracted_data['goods_tax']}")
        
        fund_match = re.search(r'民航发展基金[\s:：]*CNY\s*([\d,]+\.\d{2})', full_text)
        if fund_match:
            extracted_data['aviation_fund'] = fund_match.group(1)
            logger.info(f"[机票价格] 民航发展基金: {extracted_data['aviation_fund']}")
        
        tax_rate_match = re.search(r'增值税税率[\s:：]*(\d+%)', full_text)
        if tax_rate_match:
            extracted_data['goods_tax_rate'] = tax_rate_match.group(1)
            logger.info(f"[机票价格] 增值税税率: {extracted_data['goods_tax_rate']}")
        
        return extracted_data
    
    @staticmethod
    def _process_train_invoice(text_lines: List[str], tables: List[List[List[str]]], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理火车票发票"""
        logger.info("[处理模式] 火车票发票模式")
        full_text = '\n'.join(text_lines)
        
        # 提取基础信息
        patterns = {
            'invoice_no': r'发票号码[\s:：]*(\d{18,25})',
            'invoice_date': r'开票日期[\s:：]*(\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{1,2}-\d{1,2})',
            'buyer_name': r'购买方名称[\s:：]*([^\n;；]+?)(?=\s*(?:统一社会信用代码|纳税人识别号|$))',
            'buyer_tax_id': r'统一社会信用代码[\s:：]*([A-Z0-9]{15,20})',
            'total_with_tax': r'票价[\s:：]*(?:￥|\s|CNY)*\s*([\d,]+\.\d{2})',
            'train_ticket_no': r'电子客票号[\s:：]*([^\n;；]+)',
            'departure_station': r'自[\s:：]*([^\n;；]+站)|([^\n;；]+站)\s*[\u4e00-\u9fff]*\s*至',
            'arrival_station': r'至[\s:：]*([^\n;；]+站)|至[\s:：]*([^\n;；]+)',
        }
        
        for field, pattern in patterns.items():
            try:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    for group in match.groups():
                        if group:
                            extracted_data[field] = InvoiceExtractionService._clean_extracted_value(group)
                            logger.info(f"[火车票提取] {field}: {extracted_data[field]}")
                            break
            except Exception as e:
                logger.warning(f"[火车票提取] {field} 错误: {e}")
        
        # 提取行程详细信息
        extracted_data = InvoiceExtractionService._extract_train_itinerary(full_text, extracted_data)
        
        # 提取旅客信息
        extracted_data = InvoiceExtractionService._extract_train_passenger_info(full_text, extracted_data)
        
        # 手动查找票价
        if 'total_with_tax' not in extracted_data:
            for line in text_lines:
                if '票价' in line:
                    amount_match = re.search(r'([\d,]+\.\d{2})', line)
                    if amount_match:
                        extracted_data['total_with_tax'] = amount_match.group(1)
                        logger.info(f"[手动提取] 票价: {extracted_data['total_with_tax']}")
                        break
        
        return extracted_data
    
    @staticmethod
    def _extract_train_itinerary(full_text: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取火车票行程信息"""
        train_no_match = re.search(r'([GDKZYT]\d+)\s', full_text)
        if train_no_match:
            extracted_data['train_no'] = train_no_match.group(1)
            logger.info(f"[火车票行程] 车次: {extracted_data['train_no']}")
        
        carriage_match = re.search(r'(\d+车\d+[A-Z]?\d*号)', full_text)
        if carriage_match:
            extracted_data['carriage_seat'] = carriage_match.group(1)
            logger.info(f"[火车票行程] 车厢座位: {extracted_data['carriage_seat']}")
        
        seat_match = re.search(r'(一等座|二等座|商务座|特等座|硬座|软座|硬卧|软卧)', full_text)
        if seat_match:
            extracted_data['seat_class'] = seat_match.group(1)
            logger.info(f"[火车票行程] 座位等级: {extracted_data['seat_class']}")
        
        time_match = re.search(r'(\d{1,2}:\d{2})开', full_text)
        if time_match:
            extracted_data['train_time'] = time_match.group(1)
            logger.info(f"[火车票行程] 发车时间: {extracted_data['train_time']}")
        
        date_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)\s*(?=\d{1,2}:\d{2}开)', full_text)
        if date_match:
            extracted_data['travel_date'] = date_match.group(1)
            logger.info(f"[火车票行程] 行程日期: {extracted_data['travel_date']}")
        
        return extracted_data
    
    @staticmethod
    def _extract_train_passenger_info(full_text: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取火车票旅客信息"""
        passenger_match = re.search(r'(\d{6}\d{8}X?\d{2,4})\s*([\u4e00-\u9fff]+)', full_text)
        if passenger_match:
            extracted_data['passenger_id'] = passenger_match.group(1)
            extracted_data['passenger_name'] = passenger_match.group(2)
            logger.info(f"[火车票旅客] 身份证号: {extracted_data['passenger_id']}")
            logger.info(f"[火车票旅客] 姓名: {extracted_data['passenger_name']}")
        else:
            name_match = re.search(r'([\u4e00-\u9fff]{2,4})\s*(?=\d{6}\d{8}X?\d{2,4})', full_text)
            id_match = re.search(r'\d{6}\d{8}X?\d{2,4}', full_text)
            
            if name_match:
                extracted_data['passenger_name'] = name_match.group(1)
                logger.info(f"[火车票旅客] 姓名: {extracted_data['passenger_name']}")
            
            if id_match:
                extracted_data['passenger_id'] = id_match.group(0)
                logger.info(f"[火车票旅客] 身份证号: {extracted_data['passenger_id']}")
        
        return extracted_data
    
    @staticmethod
    def _process_unknown_invoice(text_lines: List[str], tables: List[List[List[str]]], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理未知类型发票"""
        logger.info("[处理模式] 未知发票模式")
        full_text = '\n'.join(text_lines)
        
        # 尝试提取通用信息
        patterns = {
            'invoice_no': r'(?:发票号码|电子发票号|发票号)[\s:：]*(\d{10,25})',
            'invoice_date': r'(?:开票日期|填开日期|日期)[\s:：]*(\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{1,2}-\d{1,2})',
            'buyer_name': r'(?:购买方|购买单位)[\s:：]*名称[\s:：]*([^\n;；]+)',
            'total_with_tax': r'(?:价税合计|合计|总计|金额)[\s:：]*[¥￥]?\s*([\d,]+\.\d{2})',
        }
        
        for field, pattern in patterns.items():
            try:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    extracted_data[field] = InvoiceExtractionService._clean_extracted_value(match.group(1))
                    logger.info(f"[通用提取] {field}: {extracted_data[field]}")
            except Exception as e:
                logger.warning(f"[通用提取] {field} 错误: {e}")
        
        return extracted_data
    
    @staticmethod
    def _supplement_common_fields(extracted_data: Dict[str, Any], text_lines: List[str], tables: List[List[List[str]]]) -> Dict[str, Any]:
        """补充通用字段"""
        full_text = '\n'.join(text_lines)
        
        # 补充发票号码
        if 'invoice_no' not in extracted_data:
            long_numbers = re.findall(r'\b\d{15,25}\b', full_text)
            if long_numbers:
                extracted_data['invoice_no'] = long_numbers[0]
                logger.info(f"[补充字段] 找到发票号码: {extracted_data['invoice_no']}")
        
        # 补充价税合计
        if 'total_with_tax' not in extracted_data:
            all_amounts = re.findall(r'[¥￥]?\s*([\d,]+\.\d{2})', full_text)
            if all_amounts:
                try:
                    amounts_float = [(float(amt.replace(',', '')), amt) for amt in all_amounts]
                    amounts_float.sort(reverse=True)
                    extracted_data['total_with_tax'] = amounts_float[0][1]
                    logger.info(f"[补充字段] 找到价税合计: {extracted_data['total_with_tax']}")
                except:
                    pass
        
        # 补充购买方名称
        if 'buyer_name' not in extracted_data:
            buyer_patterns = [
                r'购买方[\s:：]*名称[\s:：]*([^\n;；]+?)(?=\s*(?:统一社会信用代码|纳税人识别号|税号|$))',
                r'名称[\s:：]*([^\n;；]+?)(?=\s*(?:统一社会信用代码|纳税人识别号|税号))'
            ]
            
            for pattern in buyer_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    buyer_name = InvoiceExtractionService._clean_extracted_value(match.group(1))
                    if buyer_name and len(buyer_name) > 2:
                        extracted_data['buyer_name'] = buyer_name
                        logger.info(f"[补充字段] 找到购买方名称: {buyer_name}")
                        break
        
        # 补充购买方税号
        if 'buyer_tax_id' not in extracted_data:
            buyer_tax_patterns = [
                r'购买方[^\n]*?(?:统一社会信用代码|纳税人识别号|税号)[\s:：]*([A-Z0-9]{15,20})',
                r'(?:统一社会信用代码|纳税人识别号|税号)[\s:：]*([A-Z0-9]{15,20})'
            ]
            
            for pattern in buyer_tax_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    extracted_data['buyer_tax_id'] = match.group(1)
                    logger.info(f"[补充字段] 找到购买方税号: {extracted_data['buyer_tax_id']}")
                    break
        
        # 补充销售方名称
        if 'seller_name' not in extracted_data:
            seller_patterns = [
                r'销售方[\s:：]*名称[\s:：]*([^\n;；]+?)(?=\s*(?:统一社会信用代码|纳税人识别号|税号|$))',
                r'名称[\s:：]*([^\n;；]+?)(?=\s*(?:统一社会信用代码|纳税人识别号|税号))'
            ]
            
            for pattern in seller_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    seller_name = InvoiceExtractionService._clean_extracted_value(match.group(1))
                    if seller_name and len(seller_name) > 2:
                        extracted_data['seller_name'] = seller_name
                        logger.info(f"[补充字段] 找到销售方名称: {seller_name}")
                        break
        
        # 补充销售方税号
        if 'seller_tax_id' not in extracted_data:
            all_tax_ids = re.findall(r'([A-Z0-9]{15,20})', full_text)
            if all_tax_ids:
                buyer_tax_id = extracted_data.get('buyer_tax_id', '')
                
                if len(all_tax_ids) == 1:
                    if buyer_tax_id and all_tax_ids[0] == buyer_tax_id:
                        logger.info(f"[补充字段] 唯一税号与购买方税号相同，无法确定销售方税号")
                    else:
                        extracted_data['seller_tax_id'] = all_tax_ids[0]
                        logger.info(f"[补充字段] 使用唯一税号为销售方税号: {all_tax_ids[0]}")
                elif len(all_tax_ids) >= 2:
                    for i, tax_id in enumerate(all_tax_ids):
                        if i == 0 and buyer_tax_id and tax_id == buyer_tax_id:
                            continue
                        if i >= 1:
                            extracted_data['seller_tax_id'] = tax_id
                            logger.info(f"[补充字段] 使用第{i+1}个税号为销售方税号: {tax_id}")
                            break
        
        return extracted_data
    
    @staticmethod
    def _generate_smart_fields(extracted_data: Dict[str, Any], invoice_type: str) -> Dict[str, Any]:
        """生成智能字段"""
        if invoice_type == 'flight':
            departure = extracted_data.get('departure_airport', '')
            arrival = extracted_data.get('arrival_airport', '')
            flight_no = extracted_data.get('flight_no', '')
            carrier = extracted_data.get('carrier', '')
            
            if departure and arrival:
                extracted_data['goods_name'] = f"机票 {departure}-{arrival}"
                if flight_no:
                    extracted_data['goods_name'] += f" {flight_no}"
                elif carrier:
                    extracted_data['goods_name'] += f" {carrier}"
            elif 'passenger_name' in extracted_data:
                extracted_data['goods_name'] = f"机票 {extracted_data['passenger_name']}"
            
            extracted_data['goods_unit'] = '张'
            extracted_data['goods_quantity'] = '1'
            
            if 'goods_unit_price' not in extracted_data and 'total_with_tax' in extracted_data:
                extracted_data['goods_unit_price'] = extracted_data['total_with_tax']
            
            if 'goods_amount' not in extracted_data and 'total_with_tax' in extracted_data:
                extracted_data['goods_amount'] = extracted_data['total_with_tax']
        
        elif invoice_type == 'train':
            departure = extracted_data.get('departure_station', '')
            arrival = extracted_data.get('arrival_station', '')
            train_no = extracted_data.get('train_no', '')
            
            if departure and arrival:
                extracted_data['goods_name'] = f"火车票 {departure}-{arrival}"
                if train_no:
                    extracted_data['goods_name'] += f" {train_no}"
            elif 'passenger_name' in extracted_data:
                extracted_data['goods_name'] = f"火车票 {extracted_data['passenger_name']}"
            
            extracted_data['goods_unit'] = '张'
            extracted_data['goods_quantity'] = '1'
            
            if 'total_with_tax' in extracted_data:
                extracted_data['goods_unit_price'] = extracted_data['total_with_tax']
                extracted_data['goods_amount'] = extracted_data['total_with_tax']
        
        elif invoice_type == 'vat':
            # 对于增值税发票，如果还没有商品名称，使用通用名称
            if 'goods_name' not in extracted_data:
                extracted_data['goods_name'] = '商品'
                logger.info(f"[智能字段] 生成默认商品名称")
        
        return extracted_data
    
    @staticmethod
    def _clean_extracted_value(value: str) -> str:
        """清理提取的值"""
        if not value:
            return ""
        
        cleaned = value.strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.replace('\n', ' ').replace('\r', ' ')
        
        if '¥' in cleaned or '￥' in cleaned:
            cleaned = cleaned.replace('¥', '').replace('￥', '').strip()
        
        return cleaned
    
    @staticmethod
    def batch_process_directory(input_dir: str, output_dir: str) -> Dict[str, Any]:
        """
        批量处理目录下的所有DOCX文件
        从原脚本的main函数迁移
        """
        logger.info(f"开始批量处理目录: {input_dir}")
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            docx_files = []
            for root, dirs, files in os.walk(input_dir):
                for file in files:
                    if file.lower().endswith('.docx'):
                        docx_files.append(os.path.join(root, file))
            
            logger.info(f"找到 {len(docx_files)} 个DOCX文件")
            
            if not docx_files:
                return {
                    'success': False,
                    'message': '未找到任何DOCX文件'
                }
            
            success_count = 0
            fail_count = 0
            skip_files = []
            all_extracted_data = []
            
            for docx_file in docx_files:
                try:
                    logger.info(f"处理文件: {os.path.basename(docx_file)}")
                    
                    extracted_data = InvoiceExtractionService.extract_invoice_from_xml(docx_file)
                    
                    if not extracted_data or (isinstance(extracted_data, dict) and not extracted_data):
                        logger.warning(f"跳过文件: {os.path.basename(docx_file)}")
                        skip_files.append(os.path.basename(docx_file))
                        fail_count += 1
                        continue
                    
                    # 检查必填字段
                    missing_required = []
                    if 'invoice_no' not in extracted_data or not extracted_data['invoice_no']:
                        missing_required.append('invoice_no')
                    if 'total_with_tax' not in extracted_data or not extracted_data['total_with_tax']:
                        missing_required.append('total_with_tax')
                    
                    if missing_required:
                        logger.warning(f"缺少必要字段 {missing_required}，跳过此文件")
                        skip_files.append(os.path.basename(docx_file))
                        fail_count += 1
                        continue
                    
                    # 保存到标准化模板
                    base_name = os.path.splitext(os.path.basename(docx_file))[0]
                    output_file = os.path.join(output_dir, f"{base_name}.xlsx")
                    
                    if InvoiceExtractionService._save_to_standard_template(extracted_data, output_file):
                        success_count += 1
                        all_extracted_data.append(extracted_data)
                        logger.info(f"成功处理: {os.path.basename(docx_file)}")
                    else:
                        fail_count += 1
                        logger.warning(f"处理失败: {os.path.basename(docx_file)}")
                        
                except Exception as e:
                    logger.error(f"处理文件 {os.path.basename(docx_file)} 时出错: {e}", exc_info=True)
                    fail_count += 1
            
            # 生成汇总报告
            summary_result = {
                'success': True,
                'message': f'批量处理完成，成功: {success_count} 个，失败: {fail_count} 个',
                'success_count': success_count,
                'fail_count': fail_count,
                'total_files': len(docx_files),
                'skip_files': skip_files,
                'output_dir': output_dir
            }
            
            logger.info(f"批量处理完成: {summary_result['message']}")
            return summary_result
            
        except Exception as e:
            error_msg = f"批量处理目录异常: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'message': error_msg
            }
    
    @staticmethod
    def _save_to_standard_template(extracted_data: Dict[str, Any], output_path: str) -> bool:
        """按照标准化模板保存数据"""
        try:
            # 定义完整的标准化字段顺序 - 更新为新的字段命名
            standard_fields = [
                ("发票号码", "invoice_no"),
                ("开票日期", "invoice_date"),
                ("购买方名称", "buyer_name"),
                ("购买方税号", "buyer_tax_id"),
                ("销售方名称", "seller_name"),
                ("销售方税号", "seller_tax_id"),
                ("商品名称", "goods_name"),
                ("规格型号", "goods_spec"),
                ("单位", "goods_unit"),
                ("数量", "goods_quantity"),
                ("单价", "goods_unit_price"),
                ("金额", "goods_amount"),
                ("税率", "goods_tax_rate"),
                ("税额", "goods_tax"),
                ("合计金额", "total_amount"),
                ("合计税额", "total_tax"),
                ("价税合计", "total_with_tax"),
                ("价税合计大写", "total_chinese"),
                ("销售方银行", "seller_bank"),
                ("销售方账号", "seller_account"),
                ("开票人", "drawer"),
                ("旅客姓名", "passenger_name"),
                ("航班号", "flight_no"),
                ("航班日期", "flight_date"),
                ("承运人", "carrier"),
                ("电子客票号码", "ticket_no"),
                ("保险费", "insurance_fee"),
                ("出发机场", "departure_airport"),
                ("到达机场", "arrival_airport"),
                ("出发时间", "departure_time"),
                ("到达时间", "arrival_time"),
                ("座位等级", "flight_seat_class"),
                ("签注信息", "endorsement"),
                ("燃油附加费", "fuel_surcharge"),
                ("民航发展基金", "aviation_fund"),
                ("电子客票号", "train_ticket_no"),
                ("出发站", "departure_station"),
                ("到达站", "arrival_station"),
                ("发车时间", "train_time"),
                ("座位等级", "seat_class"),
                ("车厢座位", "carriage_seat"),
                ("车次", "train_no"),
                ("有效身份证件号码", "passenger_id"),
                ("发票类型", "invoice_type"),
            ]
            
            # 创建数据行
            data_row = []
            for ch_name, en_key in standard_fields:
                value = extracted_data.get(en_key, "")
                data_row.append(value)
            
            # 创建DataFrame
            df_standard = pd.DataFrame([data_row], columns=[ch_name for ch_name, _ in standard_fields], dtype="str")

            # 保存到Excel
            try:
                with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                    df_standard.to_excel(writer, index=False, sheet_name='发票数据')
                    worksheet = writer.sheets['发票数据']
                    for column_cells in worksheet.columns:
                        length = max(len(str(cell.value)) for cell in column_cells)
                        worksheet.column_dimensions[column_cells[0].column_letter].width = min(length + 2, 50)
                logger.info(f"成功保存到: {output_path}")
                return True
            except Exception as e:
                logger.warning(f"保存文件时出错，尝试备用方法: {e}")
                try:
                    df_standard.to_excel(output_path, index=False)
                    logger.info(f"使用备用方法保存到: {output_path}")
                    return True
                except Exception as e2:
                    logger.error(f"备用保存也失败: {e2}")
                    return False
                    
        except Exception as e:
            logger.error(f"保存标准化模板失败: {e}", exc_info=True)
            return False