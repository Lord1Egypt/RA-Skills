# template_engine/file_generate_service.py - 重构版本
import os
import logging
import pandas as pd
from typing import Dict, Any, List, Tuple

from .parallel_executor import ParallelExecutor
from .template_engine.executor import TemplateExecutor
from .template_engine.utils import TemplateUtils 

logger = logging.getLogger(__name__)

class TemplateEngine:
    """文件生成服务 - 简化为统一并行处理"""
    
    @staticmethod
    def _prepare_parallel_tasks(frontend_config: Dict[str, Any]) -> List[Tuple]:
        """准备并行任务列表"""
        task_list = []
        logger.info(f"🔍 FILE_GENERATE - 接收的配置模式: {frontend_config.get('mode')}")
        try:
            # 读取数据
            data_df = pd.read_excel(
                frontend_config['input_data'], 
                sheet_name=frontend_config.get('input_data_sheet_name', 'Sheet1'),
                dtype=str
            )
            
            # 按 data_key 分组
            data_key = frontend_config['data_key']
            if data_key not in data_df.columns:
                raise ValueError(f"数据键 '{data_key}' 不在数据列中")
                
            data_groups = data_df.groupby(data_key)
            
            # 预览模式限制任务数量
            if frontend_config.get('preview_mode', False):
                # 限制为前5个分组进行预览
                limited_groups = []
                for i, (key, group) in enumerate(data_groups):
                    if i >= 5:
                        break
                    limited_groups.append((key, group))
                data_groups = limited_groups
                logger.info(f"🔍 预览模式：限制生成 {len(limited_groups)} 个文件")
            
            # 为每个分组创建任务
            for data_key_value, data_group in data_groups:
                import copy
                task_config = copy.deepcopy(frontend_config)
                logger.info(f"🔍 模式值: {task_config.get('mode')}")
                task_config['_data_group'] = data_group  
                task_config['_data_key_value'] = data_key_value
                
                task_list.append((
                    TemplateExecutor.execute_single_file_generation,
                    [task_config],
                    {}
                ))
            
            logger.info(f"准备了 {len(task_list)} 个并行生成任务")
            return task_list
            
        except Exception as e:
            logger.error(f"准备并行任务失败: {e}")
            return []

    @staticmethod
    def _parallel_file_generate(frontend_config: Dict[str, Any]) -> Dict[str, Any]:
        """统一并行文件生成 - 替换原有的串行/并行判断"""
        try:
            task_list = TemplateEngine._prepare_parallel_tasks(frontend_config)
            
            if not task_list:
                return {
                    'status': 'error',
                    'message': '没有可执行的任务，请检查数据配置'
                }
            
            logger.info(f"开始文件生成，任务数: {len(task_list)}")
            
            # 使用 ParallelExecutor 执行并行任务
            parallel_result = ParallelExecutor.execute_parallel('file_generate', task_list)
            
            # 整合结果
            return TemplateEngine._combine_parallel_results(parallel_result, frontend_config)
            
        except Exception as e:
            logger.error(f"文件生成失败: {e}")
            return {
                'status': 'error',
                'message': f'文件生成失败: {e}'
            }

    @staticmethod
    def _combine_parallel_results(parallel_result: Dict[str, Any], frontend_config: Dict[str, Any]) -> Dict[str, Any]:
        """整合并行执行结果"""
        results = parallel_result.get('results', {})
        summary = parallel_result.get('summary', {})
        
        all_generated_files = []
        successful_tasks = 0
        total_files = 0
        
        for task_key, result in results.items():
            if result.get('status') == 'success':
                successful_tasks += 1
                generated_files = result.get('generated_files', [])
                all_generated_files.extend(generated_files)
                total_files += len(generated_files)
        
        success_rate = (successful_tasks / summary.get('total_tasks', 1)) * 100 if summary.get('total_tasks', 0) > 0 else 0
        
        # 预览模式特殊处理
        is_preview = frontend_config.get('preview_mode', False)
        message_suffix = "（预览模式）" if is_preview else ""
        
        return {
            'status': 'success' if successful_tasks > 0 else 'error',
            'message': f'文件生成完成{message_suffix}: {successful_tasks}/{summary.get("total_tasks", 0)} 个任务成功, 生成 {total_files} 个文件',
            'generated_files': all_generated_files,
            'output_dir': frontend_config.get('output_dir'),
            'execution_mode': 'parallel',
            'preview_mode': is_preview,
            'parallel_summary': {
                'total_tasks': summary.get('total_tasks', 0),
                'successful_tasks': successful_tasks,
                'failed_tasks': summary.get('failed_count', 0),
                'success_rate': f"{success_rate:.1f}%",
                'total_files_generated': total_files,
                'total_time': summary.get('total_time', '0s')
            },
            'download_info': {
                'type': 'multiple' if total_files > 1 else 'single',
                'files': all_generated_files,
                'output_dir': frontend_config.get('output_dir'),
                'operation_name': 'file_generate'
            }
        }

    # 公共接口方法 - 统一使用并行生成
    @staticmethod
    def process_data_xlsx(input_template, input_template_sheet_name, input_data, 
                        input_data_sheet_name, output_dir, data_key, insert_row, 
                        insert_col, reserved_rows, mode=None, preview_mode=False):
        """处理Excel数据并生成文件"""
        # 添加明显的调试信息
        logger.info(f"🎯🎯🎯 新的 process_data_xlsx 被调用！mode参数: {mode}")
        logger.info(f"🎯🎯🎯 函数签名包含 mode 参数")
        """处理Excel数据并生成文件"""
        try:
            frontend_config = {
                'mode': mode,
                'input_template': input_template,
                'input_template_sheet_name': input_template_sheet_name,
                'input_data': input_data,
                'input_data_sheet_name': input_data_sheet_name,
                'output_dir': output_dir,
                'data_key': data_key,
                'insert_row': insert_row,
                'insert_col': insert_col,
                'reserved_rows': reserved_rows,
                'preview_mode': preview_mode
            }
            
            # 统一使用并行生成
            return TemplateEngine._parallel_file_generate(frontend_config)
                
        except Exception as e:
            logger.error(f"处理Excel数据时出错：{e}")
            return {'status': 'error', 'message': f'处理Excel数据时出错：{e}'}
    
    @staticmethod
    def process_data_docx(input_template, input_data, input_data_sheet_name, 
                         output_dir, data_key, reserved_rows, mode=None, preview_mode=False):
        """处理Word数据并生成文件"""
        try:
            frontend_config = {
                'mode': mode or 'table_only',
                'input_template': input_template,
                'input_data': input_data,
                'input_data_sheet_name': input_data_sheet_name,
                'output_dir': output_dir,
                'data_key': data_key,
                'reserved_rows': reserved_rows,
                'preview_mode': preview_mode
            }
            
            # 统一使用并行生成
            return TemplateEngine._parallel_file_generate(frontend_config)
                
        except Exception as e:
            logger.error(f"处理Word数据时出错：{e}")
            return {'status': 'error', 'message': f'处理Word数据时出错：{e}'}
    
    @staticmethod
    def advanced_file_generate(frontend_config: Dict[str, Any]) -> Dict[str, Any]:
        """高级文件生成"""
        try:
            # 统一使用并行生成
            return TemplateEngine._parallel_file_generate(frontend_config)
                
        except Exception as e:
            logger.error(f"高级文件生成失败：{e}")
            return {'status': 'error', 'message': f'高级文件生成失败：{e}'}

# 保留工具方法
TemplateEngine.sanitize_value = TemplateUtils.sanitize_value
TemplateEngine.copy_row_style = TemplateUtils.copy_row_style  
TemplateEngine.copy_merged_cells = TemplateUtils.copy_merged_cells