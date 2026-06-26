import os
import re
import logging
import shutil
import time
import pandas as pd
from typing import Dict, Any, List, Tuple

from .parallel_executor import ParallelExecutor

logger = logging.getLogger(__name__)

class OsOperation:
    """文件重命名服务"""
    
    @staticmethod
    def _rename_single_file(file_info: tuple) -> Dict[str, Any]:
        """并行重命名单个文件"""
        old_path, new_path = file_info
        
        try:
            logger.info(f"🔄 并行重命名: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
            start_time = time.time()
            
            shutil.move(old_path, new_path)
            
            elapsed_time = time.time() - start_time
            
            logger.info(f"✅ 并行重命名完成: {os.path.basename(new_path)} [{elapsed_time:.3f}s]")
            return {
                'status': 'success',
                'file': os.path.basename(new_path),
                'old_file': os.path.basename(old_path),
                'process_time': elapsed_time
            }
            
        except Exception as e:
            logger.error(f"❌ 并行重命名失败: {os.path.basename(old_path)} - {e}")
            return {
                'status': 'error',
                'file': os.path.basename(old_path),
                'message': str(e)
            }
    
    @staticmethod
    def _safe_int_conversion(value, default=0):
        """安全地将值转换为整数"""
        if value is None:
            return default
        try:
            str_value = str(value).strip()
            if str_value and str_value.isdigit():
                return int(str_value)
            return default
        except (ValueError, TypeError, AttributeError):
            return default
    
    @staticmethod
    def _sort_files_by_mtime(file_list, directory):
        """按修改时间排序文件（带详细日志）"""
        logger.info(f"🔍 排序函数被调用，文件数: {len(file_list)}")
        
        if not file_list:
            return []
        
        files_with_time = []
        for file in file_list:
            file_path = os.path.join(directory, file)
            try:
                mtime = os.path.getmtime(file_path)
                mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                files_with_time.append((file, mtime, mtime_str))
                logger.debug(f"  读取: {file} → {mtime_str}")
            except Exception as e:
                logger.error(f"  读取失败 {file}: {e}")
                files_with_time.append((file, float('inf'), '未知'))
        
        # 排序
        files_with_time.sort(key=lambda x: x[1])
        
        # 输出排序结果
        logger.info("📋 排序结果（最早→最晚）:")
        for i, (file, mtime, mtime_str) in enumerate(files_with_time, 1):
            logger.info(f"  {i:2d}. {file} [{mtime_str}]")
        
        return [f[0] for f in files_with_time]

    @staticmethod
    def file_rename(data_path, data_sheet_name, data_key, old_dir, middle_dir, new_dir, suffix=None,
                    pattern=None, repl=None, count=None, additional_key=None,
                    deviation=None, preview_mode=False, file_times=None):
        """
        文件批量重命名
        
        Args:
            data_path: Excel数据文件路径
            data_sheet_name: Excel工作表名
            data_key: 用于重命名的数据列名
            old_dir: 原文件目录
            middle_dir: 中间文件目录
            new_dir: 输出目录
            suffix: 文件后缀过滤
            pattern: 正则表达式模式
            repl: 正则替换内容
            count: 替换次数
            additional_key: 额外添加的文本
            deviation: 编号起始偏差
            preview_mode: 预览模式
            file_times: 文件原始时间映射表 {文件名: 时间戳}
        """
       
        # 初始化返回值
        result = {
            'status': 'error',
            'message': '',
            'renamed_files': []
        }
        
        try:
            # 1. 获取所有文件
            if not os.path.exists(old_dir):
                error_msg = f"目录不存在: {old_dir}"
                logger.error(f"❌ {error_msg}")
                result['message'] = error_msg
                return result
                
            all_files = os.listdir(old_dir)
         
            # 2. 按后缀过滤
            files = all_files
            if suffix:
                suffix_str = f".{suffix}" if not suffix.startswith('.') else suffix
                files = [f for f in all_files if f.endswith(suffix_str)]
                logger.info(f"🔍 按后缀 {suffix_str} 过滤后剩余 {len(files)} 个文件")
            else:
                logger.info("🔍 未指定后缀，处理所有文件")
            
            if not files:
                error_msg = '没有找到要处理的文件'
                logger.error(f"❌ {error_msg}")
                result['message'] = error_msg
                return result
            
            # 3. ★★★ 使用传递的文件时间进行排序 ★★★
            files_with_time = []
            
            if file_times and isinstance(file_times, dict) and len(file_times) > 0:
                logger.info(f"⏰ 使用前端传递的原始时间排序 ({len(file_times)} 个文件)")
                
                # 统计匹配情况
                matched_count = 0
                missing_count = 0
                
                for file in files:
                    if file in file_times:
                        mtime = file_times[file]
                        # 确保时间戳是数字
                        try:
                            mtime = float(mtime)
                            mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                            files_with_time.append((file, mtime, mtime_str))
                            matched_count += 1
                            logger.debug(f"  ✓ 使用传递时间: {file} → {mtime_str}")
                        except (ValueError, TypeError, OSError) as e:
                            logger.warning(f"  时间戳无效 {file}: {mtime}, 错误: {e}")
                            # 回退到文件系统时间
                            file_path = os.path.join(old_dir, file)
                            mtime = os.path.getmtime(file_path)
                            mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                            files_with_time.append((file, mtime, mtime_str))
                            missing_count += 1
                    else:
                        # 没有传递时间，回退到文件系统时间
                        file_path = os.path.join(old_dir, file)
                        mtime = os.path.getmtime(file_path)
                        mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                        files_with_time.append((file, mtime, mtime_str))
                        missing_count += 1
                        logger.warning(f"⚠️ 文件 {file} 无传递时间，使用文件系统时间: {mtime_str}")
                
                logger.info(f"📊 时间信息统计: 匹配 {matched_count} 个, 回退 {missing_count} 个")
                
            else:
                # 没有传递时间，使用文件系统修改时间
                logger.info("⏰ 未传递原始时间，使用文件系统修改时间排序")
                for file in files:
                    file_path = os.path.join(old_dir, file)
                    try:
                        mtime = os.path.getmtime(file_path)
                        mtime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                        files_with_time.append((file, mtime, mtime_str))
                    except Exception as e:
                        logger.error(f"  读取失败 {file}: {e}")
                        files_with_time.append((file, float('inf'), '未知'))
            
            # 按时间排序
            files_with_time.sort(key=lambda x: x[1])
            
            # 输出排序结果
            logger.info("📋 排序结果（最早→最晚）:")
            for i, (file, mtime, mtime_str) in enumerate(files_with_time, 1):
                logger.info(f"  {i:2d}. {file} [{mtime_str}]")
            
            # 提取排序后的文件名列表
            sorted_files = [f[0] for f in files_with_time]
            
            # 4. 读取数据文件
            rename_index = []
            if data_path and data_key:
                try:
                    if not os.path.exists(data_path):
                        logger.error(f"❌ 数据文件不存在: {data_path}")
                    else:
                        data_df = pd.read_excel(data_path, sheet_name=data_sheet_name)
                        logger.info(f"📊 读取数据文件成功，共 {len(data_df)} 行，列: {list(data_df.columns)}")
                        
                        if data_key not in data_df.columns:
                            logger.error(f"❌ 数据列 '{data_key}' 不存在，可用列: {list(data_df.columns)}")
                        else:
                            data_key_series = data_df[data_key]
                            
                            # 处理重复值
                            if data_key_series.duplicated().any():
                                logger.warning(f"Sheet '{data_sheet_name}' 中 '{data_key}' 列存在重复值，已自动去重")
                                rename_index = data_key_series.drop_duplicates(keep='first').tolist()
                            else:
                                rename_index = data_key_series.tolist()
                            
                            logger.info(f"📋 数据键共 {len(rename_index)} 个唯一值")
                except Exception as e:
                    logger.error(f"❌ 读取数据文件失败: {e}")
            
            # 5. 安全转换参数
            count_int = OsOperation._safe_int_conversion(count, 0)
            deviation_int = OsOperation._safe_int_conversion(deviation, 1)
            suffix_str = f".{suffix}" if suffix and not suffix.startswith('.') else (suffix or "")
            
            # 6. 判断是否使用正则
            use_regex = pattern and repl is not None and repl != ''
            logger.info(f"📋 重命名模式: {'正则替换' if use_regex else '编号重命名'}")
            if use_regex:
                logger.info(f"   pattern: {pattern}")
                logger.info(f"   repl: {repl}")
                logger.info(f"   count: {count_int}")
            
            # 预览模式
            if preview_mode:
                logger.info("👀 预览模式，不执行实际重命名")
                preview_results = []
                for idx, file in enumerate(sorted_files):
                    file_prefix = os.path.splitext(os.path.basename(file))[0]
                    file_suffix = os.path.splitext(os.path.basename(file))[1]
                    
                    if use_regex:
                        try:
                            new_prefix = re.sub(pattern, repl, file_prefix, count=count_int)
                        except re.error as e:
                            logger.warning(f"正则错误: {e}，使用编号")
                            new_prefix = str(idx + deviation_int)
                    else:
                        new_prefix = str(idx + deviation_int)
                    
                    if additional_key:
                        new_name = f"{new_prefix}{additional_key}{file_suffix}"
                    else:
                        new_name = f"{new_prefix}{file_suffix}"
                    
                    preview_results.append({
                        'index': idx + deviation_int,
                        'old_name': file,
                        'new_name': new_name
                    })
                
                return {
                    'status': 'success',
                    'message': f'预览完成，将处理 {len(sorted_files)} 个文件',
                    'preview': True,
                    'renamed_files': preview_results,
                    'output_dir': new_dir
                }
            
            # 7. 执行重命名
            if len(sorted_files) > 1:
                logger.info(f"🔄 使用并行重命名 {len(sorted_files)} 个文件")
                
                # 第一步：正则替换或编号重命名
                step1_tasks = []
                for idx, file in enumerate(sorted_files):
                    file_prefix = os.path.splitext(os.path.basename(file))[0]
                    file_suffix = os.path.splitext(os.path.basename(file))[1]
                    file_path = os.path.join(old_dir, file)
                    
                    if use_regex:
                        try:
                            new_prefix = re.sub(pattern, repl, file_prefix, count=count_int)
                            logger.info(f"  🔤 正则: {file} → {new_prefix}{file_suffix}")
                        except re.error as e:
                            logger.error(f"  正则错误: {e}，使用编号")
                            new_prefix = str(idx + deviation_int)
                    else:
                        new_prefix = str(idx + deviation_int)
                        logger.info(f"  🔢 编号: 第{idx + deviation_int}个 {file} → {new_prefix}{file_suffix}")
                    
                    if additional_key:
                        new_name = f"{new_prefix}{additional_key}{file_suffix}"
                    else:
                        new_name = f"{new_prefix}{file_suffix}"
                    
                    new_path = os.path.join(middle_dir, new_name)
                    step1_tasks.append((file_path, new_path))
                
                # 创建中间目录
                os.makedirs(middle_dir, exist_ok=True)
                
                # 执行第一步
                task_list = [(OsOperation._rename_single_file, (task,), {}) for task in step1_tasks]
                first_result = ParallelExecutor.execute_parallel('file_rename_step1', task_list)
                
                step1_success = first_result['summary']['success_count']
                logger.info(f"✅ 第一步完成: 成功 {step1_success}/{len(step1_tasks)}")
                
                # 第二步：按数据键重命名（如果有数据键）
                if rename_index:
                    step2_tasks = []
                    for i in range(min(len(rename_index), len(step1_tasks))):
                        old_name = os.path.basename(step1_tasks[i][1])
                        
                        if additional_key:
                            new_name = f"{rename_index[i]}{additional_key}{suffix_str}"
                        else:
                            new_name = f"{rename_index[i]}{suffix_str}"
                        
                        old_path = os.path.join(middle_dir, old_name)
                        new_path = os.path.join(new_dir, new_name)
                        
                        # 检查目标文件是否已存在
                        if os.path.exists(new_path):
                            base_name = rename_index[i]
                            counter = 1
                            while os.path.exists(os.path.join(new_dir, f"{base_name}_{counter}{suffix_str}")):
                                counter += 1
                            new_name = f"{base_name}_{counter}{suffix_str}"
                            new_path = os.path.join(new_dir, new_name)
                            logger.warning(f"⚠️ 文件已存在，使用: {new_name}")
                        
                        step2_tasks.append((old_path, new_path))
                        logger.info(f"  {i+1:2d}. {old_name} → {new_name}")
                    
                    # 执行第二步
                    task_list = [(OsOperation._rename_single_file, (task,), {}) for task in step2_tasks]
                    final_result = ParallelExecutor.execute_parallel('file_rename_step2', task_list)
                    
                    step2_success = final_result['summary']['success_count']
                    logger.info(f"✅ 第二步完成: 成功 {step2_success}/{len(step2_tasks)}")
                    
                    # 收集重命名后的文件
                    renamed_files = []
                    for task_result in final_result['results'].values():
                        if task_result.get('status') == 'success':
                            renamed_files.append(task_result['file'])
                    
                    # 清理中间目录
                    try:
                        if os.path.exists(middle_dir):
                            for f in os.listdir(middle_dir):
                                os.remove(os.path.join(middle_dir, f))
                            os.rmdir(middle_dir)
                            logger.info("🧹 已清理中间目录")
                    except Exception as e:
                        logger.warning(f"清理中间目录失败: {e}")
                    
                    return {
                        'status': 'success',
                        'message': f'成功重命名 {len(renamed_files)} 个文件',
                        'renamed_files': [{'new_name': name} for name in renamed_files],
                        'output_dir': new_dir,
                        'parallel_summary': final_result['summary'],
                        'download_info': {
                            'type': 'multiple' if len(renamed_files) > 1 else 'single',
                            'files': renamed_files,
                            'output_dir': new_dir,
                            'operation_name': 'file_rename'
                        }
                    }
                else:
                    # 没有数据键，直接返回第一步结果
                    renamed_files = []
                    for task_result in first_result['results'].values():
                        if task_result.get('status') == 'success':
                            renamed_files.append(task_result['file'])
                    
                    return {
                        'status': 'success',
                        'message': f'成功重命名 {len(renamed_files)} 个文件',
                        'renamed_files': [{'new_name': name} for name in renamed_files],
                        'output_dir': middle_dir,
                        'parallel_summary': first_result['summary'],
                        'download_info': {
                            'type': 'multiple' if len(renamed_files) > 1 else 'single',
                            'files': renamed_files,
                            'output_dir': middle_dir,
                            'operation_name': 'file_rename'
                        }
                    }
            else:
                # 单个文件处理
                logger.info("📄 单个文件，使用串行处理")
                
                if not sorted_files:
                    return {
                        'status': 'error',
                        'message': '没有文件可处理'
                    }
                
                file = sorted_files[0]
                file_prefix = os.path.splitext(os.path.basename(file))[0]
                file_suffix = os.path.splitext(os.path.basename(file))[1]
                
                if use_regex:
                    try:
                        new_prefix = re.sub(pattern, repl, file_prefix, count=count_int)
                    except re.error:
                        new_prefix = str(0 + deviation_int)
                else:
                    new_prefix = str(0 + deviation_int)
                
                if additional_key:
                    new_name = f"{new_prefix}{additional_key}{file_suffix}"
                else:
                    new_name = f"{new_prefix}{file_suffix}"
                
                old_path = os.path.join(old_dir, file)
                new_path = os.path.join(middle_dir, new_name)
                
                os.makedirs(middle_dir, exist_ok=True)
                os.renames(old_path, new_path)
                
                # 如果有数据键，进行第二步
                if rename_index:
                    final_new_name = f"{rename_index[0]}{additional_key if additional_key else ''}{suffix_str}"
                    final_new_path = os.path.join(new_dir, final_new_name)
                    os.renames(new_path, final_new_path)
                    
                    return {
                        'status': 'success',
                        'message': f'成功重命名 1 个文件',
                        'renamed_files': [{'new_name': final_new_name}],
                        'output_dir': new_dir,
                        'download_info': {
                            'type': 'single',
                            'files': [final_new_name],
                            'output_dir': new_dir,
                            'operation_name': 'file_rename'
                        }
                    }
                else:
                    return {
                        'status': 'success',
                        'message': f'成功重命名 1 个文件',
                        'renamed_files': [{'new_name': new_name}],
                        'output_dir': middle_dir,
                        'download_info': {
                            'type': 'single',
                            'files': [new_name],
                            'output_dir': middle_dir,
                            'operation_name': 'file_rename'
                        }
                    }
        
        except Exception as e:
            logger.error(f"❌ 文件重命名失败: {str(e)}", exc_info=True)
            result['message'] = str(e)
            return result