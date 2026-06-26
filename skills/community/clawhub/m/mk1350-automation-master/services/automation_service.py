import os, re
import logging
import pandas as pd
import time
from typing import Dict, Any
from datetime import datetime

from .parallel_executor import ParallelExecutor
from .process_manager import ProcessManager
from .file_repair_service import RepairOffice
from .file_convert_service import MutualConver
from .file_generate_service import TemplateEngine
from .file_rename_service import OsOperation
from .file_print_service import AutoPrinter
from .data_operation_service import DataOperation
from .preview_service import PreviewService
from .optimized_tax_reconciliation_service import OptimizedTaxAmountReconciliationService
#from .tax_reconciliation_service import TaxReconciliationService
from .invoice_extraction_service import InvoiceExtractionService
logger = logging.getLogger(__name__)

class AutoMation:
    """自动化服务类 - 整合所有功能"""
    
    @staticmethod
    def _log_operation_start(operation_name, params):
        """记录操作开始日志"""
        logger.info(f"🎯 [{operation_name}] 开始执行自动化操作")
        logger.info(f"📋 [{operation_name}] 输入参数: {params}")
    
    @staticmethod
    def _log_operation_end(operation_name, success, message, execution_time, result_stats=None):
        """记录操作结束日志"""
        status = "✅ 成功" if success else "❌ 失败"
        time_info = f"，执行时间: {execution_time:.2f}s"
        stats_info = f"，统计: {result_stats}" if result_stats else ""
        logger.info(f"🎯 [{operation_name}] {status}{time_info}{stats_info} - {message}")
    
    @staticmethod
    def _log_step_progress(operation_name, step, details=""):
        """记录步骤进度"""
        if details:
            logger.info(f"   ↳ [{operation_name}] {step} - {details}")
        else:
            logger.info(f"   ↳ [{operation_name}] {step}")
    
    @staticmethod
    def file_generate(params: Dict[str, Any]) -> Dict[str, Any]:
        """文件批量生成"""
        start_time = time.time()
        operation_name = "文件批量生成"
        
        try:
            AutoMation._log_operation_start(operation_name, params)
            
            if params['input_template'].endswith('.xlsx'):
                AutoMation._log_step_progress(operation_name, "检测到Excel模板")
                result = TemplateEngine.process_data_xlsx(
                    params['input_template'],
                    params.get('input_template_sheet_name', 'Sheet1'),
                    params['input_data'],
                    params.get('input_data_sheet_name', 'Sheet1'),
                    params['output_dir'],
                    params['data_key'],
                    insert_row=int(params.get('insert_row', 1)),
                    insert_col=int(params.get('insert_col', 1)),
                    reserved_rows=int(params.get('reserved_rows', 1)),
                    preview_mode=params.get('preview_mode', False),
                    mode=params.get('mode')
                )
            elif params['input_template'].endswith('.docx'):
                AutoMation._log_step_progress(operation_name, "检测到Word模板")
                result = TemplateEngine.process_data_docx(
                    params['input_template'],
                    params['input_data'],
                    params.get('input_data_sheet_name', 'Sheet1'),
                    params['output_dir'],
                    params['data_key'],
                    reserved_rows=int(params.get('reserved_rows', 1)),
                    preview_mode=params.get('preview_mode', False),
                    mode=params.get('mode')
                )
            else:
                error_msg = f'不支持的模板文件格式: {params["input_template"]}'
                logger.error(f"❌ [{operation_name}] {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
                }
            
            execution_time = time.time() - start_time
            success = result.get('status') == 'success'
            AutoMation._log_operation_end(operation_name, success, result.get('message', '未知状态'), 
                                         execution_time, result.get('download_info'))
            return result
        
        except Exception as e:
            error_msg = f'文件生成失败: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'message': error_msg
            }
    
    @staticmethod
    def file_convert(params: Dict[str, Any]) -> Dict[str, Any]:
        """文件批量转换"""
        start_time = time.time()
        operation_name = "文件批量转换"
        
        try:
            AutoMation._log_operation_start(operation_name, params)
            
            input_dir = params['input_dir']
            output_dir = params['output_dir']
            old_suffix = params.get('old_suffix', '')
            new_suffix = params.get('new_suffix', '')
            convert_exe = params.get('convert_exe')
            
            os.makedirs(output_dir, exist_ok=True)
            
            # 检查输入目录文件
            input_files = os.listdir(input_dir)
            AutoMation._log_step_progress(operation_name, "检查输入目录", 
                                         f"找到 {len(input_files)} 个文件: {input_files}")
            
            if new_suffix.lower() == 'pdf':
                AutoMation._log_step_progress(operation_name, "开始文件转PDF", 
                                             f"{old_suffix} -> PDF")
                result = MutualConver.files_convert_pdf(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
            elif old_suffix.lower() == 'pdf':
                AutoMation._log_step_progress(operation_name, "开始PDF转文件", 
                                             f"PDF -> {new_suffix}")
                result = MutualConver.pdf_convert_files(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
            else:
                error_msg = f'不支持的文件转换类型: {old_suffix} -> {new_suffix}'
                logger.error(f"❌ [{operation_name}] {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
                }
            
            execution_time = time.time() - start_time
            success = result.get('status') == 'success'
            AutoMation._log_operation_end(operation_name, success, result.get('message', '未知状态'), 
                                         execution_time, result.get('download_info'))
            return result
            
        except Exception as e:
            error_msg = f'文件转换失败: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'message': error_msg
            }
    
    @staticmethod
    def file_repair(params: Dict[str, Any]) -> Dict[str, Any]:
        """文件修复"""
        start_time = time.time()
        operation_name = "文件修复"
        
        try:
            AutoMation._log_operation_start(operation_name, params)
            
            input_dir = params['input_dir']
            output_dir = params['output_dir']
            file_type = params.get('suffix', '')
            repair_method = params.get('repair_method', 'auto')
            repair_tool = params.get('repair_tool')
            
            # 记录修复配置
            AutoMation._log_step_progress(operation_name, "修复配置", 
                                         f"方法: {repair_method}, 工具: {repair_tool}, 文件类型: {file_type}")
            
            # 检查输入文件
            repair_file_type = f".{file_type}"
            input_files = [f for f in os.listdir(input_dir) if f.endswith(repair_file_type)]
            AutoMation._log_step_progress(operation_name, "检查输入文件", 
                                         f"找到 {len(input_files)} 个待修复文件: {input_files}")
            
            result = RepairOffice.repair_office(input_dir, output_dir, file_type, repair_method, repair_tool)
            
            # 检查输出结果
            output_files = [f for f in os.listdir(output_dir) if f.endswith(repair_file_type)]
            AutoMation._log_step_progress(operation_name, "检查输出结果", 
                                         f"修复后输出 {len(output_files)} 个文件: {output_files}")
            
            execution_time = time.time() - start_time
            success = result.get('status') == 'success'
            AutoMation._log_operation_end(operation_name, success, result.get('message', '未知状态'), 
                                         execution_time, result.get('download_info'))
            return result
            
        except Exception as e:
            error_msg = f'文件修复失败: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'message': error_msg
            }
    
    @staticmethod
    def file_rename(params: Dict[str, Any]) -> Dict[str, Any]:
        """文件批量重命名"""
        start_time = time.time()
        operation_name = "文件批量重命名"
        
        try:
            AutoMation._log_operation_start(operation_name, params)
            
            # 提取参数，设置默认值
            data_path = params.get('data_path', '')
            data_sheet_name = params.get('data_sheet_name', 'Sheet1')
            data_key = params.get('data_key', '')
            input_dir = params.get('input_dir', '')
            middle_dir = params.get('middle_dir', input_dir)
            output_dir = params.get('output_dir', input_dir)
            suffix = params.get('suffix')
            pattern = params.get('pattern')
            repl = params.get('repl')
            count = params.get('count', 0)
            additional_key = params.get('additional_key')
            deviation = params.get('deviation', 0)
            preview_mode = params.get('preview_mode', False)
            
            # ★★★ 新增：获取文件时间信息 ★★★
            file_times = params.get('file_times', {})
            
            # 记录操作详情
            AutoMation._log_step_progress(operation_name, "参数验证", 
                                        f"输入目录: {input_dir}, 输出目录: {output_dir}")
            
            if file_times:
                AutoMation._log_step_progress(operation_name, "时间信息", 
                                            f"接收到 {len(file_times)} 个文件的原始时间")
            
            # 调用重命名服务
            result = OsOperation.file_rename(
                data_path=data_path,
                data_sheet_name=data_sheet_name,
                data_key=data_key,
                old_dir=input_dir,
                middle_dir=middle_dir,
                new_dir=output_dir,
                suffix=suffix,
                pattern=pattern,
                repl=repl,
                count=count,
                additional_key=additional_key,
                deviation=int(deviation) if deviation else 0,
                preview_mode=preview_mode,
                # ★★★ 新增：传递文件时间信息 ★★★
                file_times=file_times
            )
            
            execution_time = time.time() - start_time
            success = result.get('status') == 'success'
            
            # 统计信息
            renamed_count = len(result.get('renamed_files', [])) if isinstance(result, dict) else 0
            stats = f"重命名文件数: {renamed_count}"
            
            AutoMation._log_operation_end(operation_name, success, result.get('message', '未知状态'), 
                                        execution_time, stats)
            return result
            
        except Exception as e:
            error_msg = f'文件重命名失败: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'message': error_msg
            }
    
    @staticmethod
    def data_merge(params: Dict[str, Any]) -> Dict[str, Any]:
        """数据拼接 (pd.merge)"""
        start_time = time.time()
        operation_name = "数据拼接"
        
        try:
            AutoMation._log_operation_start(operation_name, params)
            
            # 读取模板文件
            AutoMation._log_step_progress(operation_name, "读取模板文件", 
                                         f"文件: {params['input_template']}, 工作表: {params.get('input_template_sheet_name', 'Sheet1')}")
            template_df = pd.read_excel(
                params['input_template'],
                sheet_name=params.get('input_template_sheet_name', 'Sheet1')
            )
            
            # 读取数据文件
            AutoMation._log_step_progress(operation_name, "读取数据文件", 
                                         f"文件: {params['input_data']}, 工作表: {params.get('input_data_sheet_name', 'Sheet1')}")
            data_df = pd.read_excel(
                params['input_data'],
                sheet_name=params.get('input_data_sheet_name', 'Sheet1')
            )
            
            AutoMation._log_step_progress(operation_name, "数据形状", 
                                         f"模板: {template_df.shape}, 数据: {data_df.shape}")
            
            # 数据合并
            data_key = params.get('data_key', 'id')
            how = params.get('how', 'inner')
            AutoMation._log_step_progress(operation_name, "开始数据合并", 
                                         f"主键: {data_key}, 方式: {how}")
            
            merged_df = DataOperation.key_merge(template_df, data_df, on=data_key, how=how)
            AutoMation._log_step_progress(operation_name, "合并完成", 
                                         f"合并后形状: {merged_df.shape}")
            
            # 保存结果
            output_dir = params['output_dir']
            os.makedirs(output_dir, exist_ok=True)
            
            save_name = params.get('save_name', 'merged_result')
            save_sheet_name = params.get('save_sheet_name', 'Sheet1')
            
            output_path = os.path.join(output_dir, f"{save_name}.xlsx")
            AutoMation._log_step_progress(operation_name, "保存结果", 
                                         f"路径: {output_path}")
            
            DataOperation.data_pd_write(output_path, save_sheet_name, merged_df)
            
            execution_time = time.time() - start_time
            result_stats = f"行数: {len(merged_df)}, 列数: {len(merged_df.columns)}"
            AutoMation._log_operation_end(operation_name, True, '数据合并完成', 
                                         execution_time, result_stats)
            
            return {
                'status': 'success',
                'message': '数据合并完成',
                'output_path': output_path,
                'row_count': len(merged_df),
                'column_count': len(merged_df.columns),
                'download_info': {
                    'type': 'single',
                    'files': [f"{save_name}.xlsx"],
                    'output_dir': output_dir,
                    'operation_name': 'data_merge'
                }
            }
            
        except Exception as e:
            error_msg = f'数据合并失败: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'message': error_msg
            }
    
    @staticmethod
    def data_concat(params: Dict[str, Any]) -> Dict[str, Any]:
        """数据合拼 (pd.concat)"""
        start_time = time.time()
        operation_name = "数据合拼"
        
        try:
            AutoMation._log_operation_start(operation_name, params)
            
            input_dir = params.get('input_dir')
            input_data = params.get('input_data')
            
            if input_dir:
                AutoMation._log_step_progress(operation_name, "使用目录模式", 
                                             f"目录: {input_dir}")
                result_df = DataOperation.xlsxs_sheets_concat(
                    input_dir,
                    data_key=params.get('data_key'),
                    sheet_re=params.get('sheet_re'),
                    axis=int(params.get('data_axis', 0)),
                    join=params.get('how', 'outer'),
                    args=params.get('args'),
                    filter_criteria=params.get('filter_criteria'),
                    ignore_index=True,
                    fillna_zero=True
                )
            elif input_data:
                AutoMation._log_step_progress(operation_name, "使用文件模式", 
                                             f"文件: {input_data}")
                result_df = DataOperation.sheets_concat(
                    input_data,
                    data_key=params.get('data_key'),
                    sheet_re=params.get('sheet_re'),
                    axis=int(params.get('data_axis', 0)),
                    join=params.get('how', 'outer'),
                    args=params.get('args'),
                    filter_criteria=params.get('filter_criteria'),
                    ignore_index=True,
                    fillna_zero=True
                )
            else:
                error_msg = '未提供输入目录或文件路径'
                logger.error(f"❌ [{operation_name}] {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
                }

            if result_df is None or len(result_df) == 0:
                error_msg = '合并结果为空，请检查输入文件和数据'
                logger.warning(f"⚠️ [{operation_name}] {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
                }

            AutoMation._log_step_progress(operation_name, "合拼完成", 
                                         f"合拼后形状: {result_df.shape}")

            # 保存结果
            output_dir = params['output_dir']
            os.makedirs(output_dir, exist_ok=True)
            
            save_name = params.get('save_name', 'concatenated_result')
            save_sheet_name = params.get('save_sheet_name', 'Sheet1')
            
            output_path = os.path.join(output_dir, f"{save_name}.xlsx")
            AutoMation._log_step_progress(operation_name, "保存结果", 
                                         f"路径: {output_path}")
            
            DataOperation.data_pd_write(output_path, save_sheet_name, result_df)
            
            execution_time = time.time() - start_time
            result_stats = f"行数: {len(result_df)}, 列数: {len(result_df.columns)}"
            AutoMation._log_operation_end(operation_name, True, '数据合拼完成', 
                                         execution_time, result_stats)
            
            return {
                'status': 'success',
                'message': '数据合拼完成',
                'output_path': output_path,
                'row_count': len(result_df),
                'column_count': len(result_df.columns),
                'download_info': {
                    'type': 'single',
                    'files': [f"{save_name}.xlsx"],
                    'output_dir': output_dir,
                    'operation_name': 'data_concat'
                }
            }
            
        except Exception as e:
            error_msg = f'数据合拼失败: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'message': error_msg
            }
        
    @staticmethod
    def file_print(params: Dict[str, Any]) -> Dict[str, Any]:
        """文件批量打印"""
        start_time = time.time()
        operation_name = "文件批量打印"
        
        try:
            AutoMation._log_operation_start(operation_name, params)
            
            input_dir = params['input_dir']
            sheet_name = params['sheet_name']
            area_print = params.get('area_print')
            printer_name = params.get('printer_name')
            
            # 检查输入目录文件
            input_files = os.listdir(input_dir)
            AutoMation._log_step_progress(operation_name, "检查输入目录", 
                                         f"找到 {len(input_files)} 个文件: {input_files}")
            
            if not input_files:
                error_msg = '输入目录中没有找到可打印的文件'
                logger.warning(f"⚠️ [{operation_name}] {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
                }
            
            if sheet_name:
                AutoMation._log_step_progress(operation_name, "设置打印小表", 
                                             f"小表: {sheet_name}")

            if area_print:
                AutoMation._log_step_progress(operation_name, "设置打印区域", 
                                             f"区域: {area_print}")
            
            if printer_name:
                AutoMation._log_step_progress(operation_name, "使用指定打印机", 
                                             f"打印机: {printer_name}")
            else:
                AutoMation._log_step_progress(operation_name, "使用默认打印机")
            
            AutoMation._log_step_progress(operation_name, "开始执行打印")
            result = AutoPrinter.judgment_print(input_dir, sheet_name, area_print, printer_name)
            
            # 根据打印结果设置详细的状态信息
            success_count = result.get('success_count', 0)
            fail_count = result.get('fail_count', 0)
            total_files = result.get('total_files', 0)
            
            if result['status'] == 'success':
                success_msg = f"✅ 成功打印 {success_count} 个文件"
                logger.info(f"🎯 [{operation_name}] {success_msg}")
                result['message'] = success_msg
            elif result['status'] == 'warning':
                warning_msg = f"⚠️ 成功打印 {success_count} 个文件，失败 {fail_count} 个文件"
                logger.warning(f"🎯 [{operation_name}] {warning_msg}")
                result['message'] = warning_msg
            else:
                error_msg = f"❌ 打印失败，所有 {total_files} 个文件均未成功打印"
                logger.error(f"🎯 [{operation_name}] {error_msg}")
                result['message'] = error_msg
            
            # 添加前端需要的状态字段
            result['ui_status'] = result['status']  # success/warning/error
            result['success'] = result['status'] in ['success', 'warning']  # 只要有成功就认为是成功的操作
            
            # 记录详细结果
            if result.get('printed_files'):
                logger.info(f"📄 [{operation_name}] 成功文件列表: {result['printed_files']}")
            if result.get('failed_files'):
                for failed in result['failed_files']:
                    logger.error(f"❌ [{operation_name}] 失败文件: {failed.get('file')} - {failed.get('error')}")
            
            execution_time = time.time() - start_time
            result_stats = f"成功: {success_count}, 失败: {fail_count}, 总计: {total_files}"
            AutoMation._log_operation_end(operation_name, result['success'], result['message'], 
                                         execution_time, result_stats)
            
            return result
            
        except Exception as e:
            error_msg = f'文件打印失败: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'ui_status': 'error',
                'success': False,
                'message': error_msg
            }
        
    @staticmethod
    def tax_reconciliation(params: Dict[str, Any]) -> Dict[str, Any]:
        """税务智能对账服务 - 使用完整脚本版算法"""
        start_time = time.time()
        operation_name = "税务智能对账"
        
        try:
            AutoMation._log_operation_start(operation_name, params)
            
            # 验证必要参数
            required_fields = ['tax_bureau_file', 'sap_file']
            for field in required_fields:
                if field not in params or not params[field]:
                    error_msg = f'缺少必要参数: {field}'
                    logger.error(f"❌ [{operation_name}] {error_msg}")
                    return {
                        'status': 'error',
                        'message': error_msg
                    }
            
            # 文件存在性检查
            if not os.path.exists(params['tax_bureau_file']):
                error_msg = f'税局文件不存在: {params["tax_bureau_file"]}'
                logger.error(f"❌ [{operation_name}] {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
                }
            
            if not os.path.exists(params['sap_file']):
                error_msg = f'SAP文件不存在: {params["sap_file"]}'
                logger.error(f"❌ [{operation_name}] {error_msg}")
                return {
                    'status': 'error',
                    'message': error_msg
                }
            
            # 读取数据
            AutoMation._log_step_progress(operation_name, "读取数据文件")
            tax_df = pd.read_excel(params['tax_bureau_file'])
            sap_df = pd.read_excel(params['sap_file'])
            
            # 验证数据列
            required_columns = ['税额', '税率']
            for col in required_columns:
                if col not in tax_df.columns:
                    error_msg = f'税局文件缺少必要列: {col}'
                    logger.error(f"❌ [{operation_name}] {error_msg}")
                    return {
                        'status': 'error',
                        'message': error_msg
                    }
                if col not in sap_df.columns:
                    error_msg = f'SAP文件缺少必要列: {col}'
                    logger.error(f"❌ [{operation_name}] {error_msg}")
                    return {
                        'status': 'error',
                        'message': error_msg
                    }
            
            # 创建完整的对账实例（使用迁移的完整算法）
            AutoMation._log_step_progress(operation_name, "初始化对账算法（完整脚本版）")
            
            # 构建算法参数（使用脚本版默认值，前端参数作为覆盖）
            algorithm_params = {
                # 核心匹配阈值
                'exact_match_threshold': params.get('exact_match_threshold', 0.001),
                'approx_match_threshold_percent': params.get('approx_match_threshold_percent', 1.0),
                'many_to_many_amount_threshold': params.get('many_to_many_amount_threshold', 1500),
                'many_to_many_percent_threshold': params.get('many_to_many_percent_threshold', 1.0),
                'final_match_amount_threshold': params.get('final_match_amount_threshold', 100.0),
                'final_match_percent_threshold': params.get('final_match_percent_threshold', 0.1),
                
                # 递归匹配阈值
                'recursive_min_amount_threshold': params.get('recursive_min_amount_threshold', 0.01),
                'recursive_percent_threshold': params.get('recursive_percent_threshold', 10.0),
                
                # 算法控制参数
                'large_amount_threshold': params.get('large_amount_threshold', 1000),
                'pruning_threshold_percent': params.get('pruning_threshold_percent', 90.0),
                'backtrack_overtune_percent': params.get('backtrack_overtune_percent', 10.0),
                'backtrack_pruning_threshold_percent': params.get('backtrack_pruning_threshold_percent', 90.0),
                'hybrid_search_threshold_percent': params.get('hybrid_search_threshold_percent', 10.0),
                
                # 算法行为控制
                'max_combination_depth': params.get('max_combination_depth', 3),
                'max_candidates_per_stage': params.get('max_candidates_per_stage', 20),
                'search_algorithm': params.get('search_algorithm', 'dynamic'),
                'max_recursion_times': params.get('max_recursion_times', 2),
                'enable_many_to_many': params.get('enable_many_to_many', True),
                'enable_recursive_match': params.get('enable_recursive_match', True),
            }
            
            reconciler = OptimizedTaxAmountReconciliationService(tax_df, sap_df, algorithm_params)
            
            # 执行对账
            if params.get('preview_mode'):
                AutoMation._log_step_progress(operation_name, "预览模式")
                
                # 预览模式：执行简化对账并返回统计信息
                result = reconciler.reconcile_all()
                
                # 构建预览结果
                preview_data = {
                    'summary': {
                        'total_tax_amount': result['summary']['total_tax_amount'],
                        'total_sap_amount': result['summary']['total_sap_amount'],
                        'total_diff': result['summary']['balance_diff'],
                        'match_rate': result['summary']['match_rate'],
                        'unmatched_tax_count': result['summary']['unmatched_tax_count'],
                        'unmatched_sap_count': result['summary']['unmatched_sap_count'],
                        'estimated_match_rate': result['summary']['match_rate']
                    },
                    'rate_stats': [],
                    'parameter_summary': algorithm_params,
                    'algorithm_params': params.get('match_precision_mode', '标准模式')
                }
                
                response = {
                    'status': 'success',
                    'message': '预览对账完成',
                    'preview_data': preview_data,
                    'summary': preview_data['summary']
                }
                
            else:
                AutoMation._log_step_progress(operation_name, "执行完整对账")
                result = reconciler.reconcile_all()
                
                # 生成输出文件名
                output_name = params.get('output_name', '税务对账结果_完整脚本版')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"{output_name}_{timestamp}.xlsx"
                output_path = os.path.join(params['output_dir'], output_filename)
                
                # 导出结果
                reconciler.export_to_excel(output_path)
                
                # 计算执行时间
                execution_time = time.time() - start_time
                
                # 构建结果摘要
                summary = {
                    'execution_time': round(execution_time, 2),
                    'match_count': result['summary']['match_count'],
                    'match_rate': round(result['summary'].get('match_rate', 0), 2),
                    'total_tax_amount': round(result['summary']['total_tax_amount'], 2),
                    'total_sap_amount': round(result['summary']['total_sap_amount'], 2),
                    'total_matched': round(result['summary']['total_matched'], 2),
                    'balance_diff': round(result['summary']['balance_diff'], 2),
                    'unmatched_tax_count': result['summary']['unmatched_tax_count'],
                    'unmatched_sap_count': result['summary']['unmatched_sap_count'],
                    'performance_stats': result['performance_stats'],
                    'validation_passed': result['summary'].get('validation_passed', False)
                }
                
                response = {
                    'status': 'success',
                    'message': '税务对账完成',
                    'output_path': output_path,
                    'summary': summary,
                    'performance_stats': result['performance_stats'],
                    'download_info': {
                        'type': 'single',
                        'files': [os.path.basename(output_path)],
                        'output_dir': params['output_dir'],
                        'operation_name': 'tax_reconciliation',
                        'title': '税务对账结果下载'
                    }
                }
            
            AutoMation._log_operation_end(operation_name, True, response['message'], 
                                        time.time() - start_time, 
                                        f"匹配率: {result['summary'].get('match_rate', 0):.2f}%")
            return response
            
        except Exception as e:
            error_msg = f'税务对账服务异常: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'message': error_msg
            }

    # 在 automation_service.py 的 AutoMation 类中添加以下方法

    @staticmethod
    def invoice_extraction(params: Dict[str, Any]) -> Dict[str, Any]:
        """发票信息提取"""
        start_time = time.time()
        operation_name = "发票信息提取"
        
        try:
            AutoMation._log_operation_start(operation_name, params)

            input_path = params.get('input_path', '')
            process_mode = params.get('process_mode', 'batch')
            output_format = params.get('output_format', 'excel')
            preview_mode = params.get('preview_mode', False)
            output_dir = params.get('output_dir', '')
            
            # 验证输入路径
            if not input_path:
                error_msg = "未指定输入路径"
                AutoMation._log_step_progress(operation_name, "验证失败", error_msg)
                return {
                    'status': 'error',
                    'message': error_msg
                }
            
            if not os.path.exists(input_path):
                error_msg = f"输入路径不存在: {input_path}"
                AutoMation._log_step_progress(operation_name, "验证失败", error_msg)
                return {
                    'status': 'error',
                    'message': error_msg
                }
            
            if preview_mode:
                # 预览模式
                AutoMation._log_step_progress(operation_name, "预览模式")
                
                if process_mode == 'single' and os.path.isfile(input_path):
                    # 单文件预览
                    extracted_data = InvoiceExtractionService.extract_invoice_from_xml(input_path)
                    
                    if extracted_data:
                        preview_data = {
                            'file_info': {
                                'file_name': os.path.basename(input_path),
                                'file_size': os.path.getsize(input_path)
                            },
                            'extraction_summary': {
                                'invoice_type': extracted_data.get('invoice_type', '未知'),
                                'invoice_no': extracted_data.get('invoice_no', '未提取到'),
                                'invoice_date': extracted_data.get('invoice_date', '未提取到'),
                                'buyer_name': extracted_data.get('buyer_name', '未提取到'),
                                'seller_name': extracted_data.get('seller_name', '未提取到'),
                                'total_with_tax': extracted_data.get('total_with_tax', '未提取到'),
                                'extracted_fields': len([v for v in extracted_data.values() if v]),
                                'total_fields': len(extracted_data)
                            },
                            'sample_data': {
                                'basic_info': {k: v for k, v in extracted_data.items() if k in [
                                    'invoice_no', 'invoice_date', 'buyer_name', 'seller_name', 
                                    'total_with_tax', 'item_name'
                                ] and v}
                            }
                        }
                        
                        execution_time = time.time() - start_time
                        AutoMation._log_operation_end(operation_name, True, '预览生成成功', 
                                                    execution_time, f"提取字段: {preview_data['extraction_summary']['extracted_fields']}")
                        
                        return {
                            'status': 'success',
                            'message': '预览生成成功',
                            'preview_data': preview_data
                        }
                    else:
                        error_msg = '文件提取失败，可能不是有效的发票文件'
                        AutoMation._log_step_progress(operation_name, "提取失败", error_msg)
                        return {
                            'status': 'error',
                            'message': error_msg
                        }
                else:
                    # 批量预览 - 统计文件
                    if os.path.isdir(input_path):
                        docx_files = [f for f in os.listdir(input_path) if f.lower().endswith('.docx')]
                        preview_data = {
                            'directory_info': {
                                'path': input_path,
                                'docx_count': len(docx_files),
                                'total_size': sum(os.path.getsize(os.path.join(input_path, f)) for f in docx_files if os.path.exists(os.path.join(input_path, f)))
                            },
                            'process_mode': 'batch',
                            'estimated_time': f"约 {len(docx_files) * 5} 秒"  # 假设每个文件5秒
                        }
                        
                        execution_time = time.time() - start_time
                        AutoMation._log_operation_end(operation_name, True, '目录预览完成', 
                                                    execution_time, f"DOCX文件数: {len(docx_files)}")
                        
                        return {
                            'status': 'success',
                            'message': '目录预览完成',
                            'preview_data': preview_data
                        }
                    else:
                        error_msg = '输入路径必须是文件或目录'
                        AutoMation._log_step_progress(operation_name, "验证失败", error_msg)
                        return {
                            'status': 'error',
                            'message': error_msg
                        }
            else:
                # 执行模式
                if not output_dir:
                    output_dir = os.path.dirname(input_path) if os.path.isfile(input_path) else input_path + '_output'
                
                os.makedirs(output_dir, exist_ok=True)
                
                if process_mode == 'single' and os.path.isfile(input_path):
                    # 单文件处理
                    AutoMation._log_step_progress(operation_name, "单文件处理", f"文件: {os.path.basename(input_path)}")
                    
                    extracted_data = InvoiceExtractionService.extract_invoice_from_xml(input_path)
                    
                    if extracted_data:
                        # 检查必填字段
                        missing_required = []
                        if 'invoice_no' not in extracted_data or not extracted_data['invoice_no']:
                            missing_required.append('invoice_no')
                        if 'total_with_tax' not in extracted_data or not extracted_data['total_with_tax']:
                            missing_required.append('total_with_tax')
                        
                        if missing_required:
                            error_msg = f"缺少必要字段 {missing_required}"
                            AutoMation._log_step_progress(operation_name, "提取失败", error_msg)
                            return {
                                'status': 'error',
                                'message': error_msg
                            }
                        
                        # 生成输出文件名
                        base_name = os.path.splitext(os.path.basename(input_path))[0]
                        output_file = os.path.join(output_dir, f"{base_name}.xlsx")
                        
                        # 保存到标准化模板
                        if InvoiceExtractionService._save_to_standard_template(extracted_data, output_file):
                            execution_time = time.time() - start_time
                            AutoMation._log_operation_end(operation_name, True, '单文件提取成功', 
                                                        execution_time, f"提取字段: {len(extracted_data)}")
                            
                            return {
                                'status': 'success',
                                'message': '发票信息提取成功',
                                'output_path': output_file,
                                'download_info': {
                                    'type': 'single',
                                    'files': [os.path.basename(output_file)],
                                    'output_dir': output_dir,
                                    'operation_name': 'invoice_extraction',
                                    'title': '发票信息提取结果下载'
                                }
                            }
                        else:
                            error_msg = '保存输出文件失败'
                            AutoMation._log_step_progress(operation_name, "保存失败", error_msg)
                            return {
                                'status': 'error',
                                'message': error_msg
                            }
                    else:
                        error_msg = '文件提取失败，可能不是有效的发票文件'
                        AutoMation._log_step_progress(operation_name, "提取失败", error_msg)
                        return {
                            'status': 'error',
                            'message': error_msg
                        }
                        
                elif process_mode == 'batch' or os.path.isdir(input_path):
                    # 批量处理
                    AutoMation._log_step_progress(operation_name, "批量处理", f"目录: {input_path}")
                    
                    result = InvoiceExtractionService.batch_process_directory(input_path, output_dir)
                    
                    execution_time = time.time() - start_time
                    
                    if result.get('success', False):
                        AutoMation._log_operation_end(operation_name, True, result['message'], 
                                                    execution_time, 
                                                    f"成功: {result.get('success_count', 0)}, 失败: {result.get('fail_count', 0)}")
                        
                        # 收集输出文件
                        output_files = []
                        if os.path.exists(output_dir):
                            for file in os.listdir(output_dir):
                                if file.endswith('.xlsx'):
                                    output_files.append(file)
                        
                        return {
                            'status': 'success',
                            'message': result['message'],
                            'summary': result,
                            'download_info': {
                                'type': 'multiple',
                                'files': output_files,
                                'output_dir': output_dir,
                                'operation_name': 'invoice_extraction',
                                'title': '发票信息批量提取结果下载'
                            }
                        }
                    else:
                        AutoMation._log_operation_end(operation_name, False, result.get('message', '批量处理失败'), 
                                                    execution_time)
                        return {
                            'status': 'error',
                            'message': result.get('message', '批量处理失败')
                        }
                else:
                    error_msg = f"不支持的处理模式: {process_mode}"
                    AutoMation._log_step_progress(operation_name, "验证失败", error_msg)
                    return {
                        'status': 'error',
                        'message': error_msg
                    }
                
        except Exception as e:
            error_msg = f'发票信息提取失败: {str(e)}'
            execution_time = time.time() - start_time
            logger.error(f"❌ [{operation_name}] {error_msg}", exc_info=True)
            AutoMation._log_operation_end(operation_name, False, error_msg, execution_time)
            return {
                'status': 'error',
                'message': error_msg
            }


    @staticmethod
    def preview_operation(params: Dict[str, Any]) -> Dict[str, Any]:
        """统一预览入口"""
        operation_type = params.get('operation_type')
    
        preview_handlers = {
            'file_generate': PreviewService.preview_file_generate,
            'file_convert': PreviewService.preview_file_convert,
            'file_rename': PreviewService.preview_file_rename,
            'file_repair': PreviewService.preview_file_repair,
            'data_merge': lambda p: PreviewService.preview_data_operation({**p, 'operation_type': 'merge'}),
            'data_concat': lambda p: PreviewService.preview_data_operation({**p, 'operation_type': 'concat'}),
            'invoice_extraction': lambda p: AutoMation.invoice_extraction({**p, 'preview_mode': True}),
        }
        
        if operation_type not in preview_handlers:
            return {
                'success': False,  # 改为 success 字段
                'message': f'不支持的预览类型: {operation_type}'
            }
        
        try:
            logger.info(f"👀 开始预览操作: {operation_type}")
            result = preview_handlers[operation_type](params)
            logger.info(f"👀 预览操作完成: {operation_type}")
            
            # 统一返回格式，确保包含 success 字段
            if 'success' not in result:
                result['success'] = result.get('status') == 'success'
            
            return result
        except Exception as e:
            error_msg = f'预览操作失败: {str(e)}'
            logger.error(f"❌ 预览操作失败: {error_msg}", exc_info=True)
            return {
                'success': False,  # 改为 success 字段
                'message': error_msg
            }