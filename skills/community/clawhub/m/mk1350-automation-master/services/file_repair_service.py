import os
import time
import threading
import subprocess
import logging
import hashlib
from typing import Dict, Any, List, Tuple

from .parallel_executor import ParallelExecutor
from .process_manager import ProcessManager

logger = logging.getLogger(__name__)

class RepairOffice:
    """文件修复服务"""
    
    @staticmethod
    def kill_libreoffice():
        """强制终止所有 LibreOffice 进程"""
        os.system('taskkill /f /im soffice.exe >nul 2>&1')
        os.system('taskkill /f /im soffice.bin >nul 2>&1')
        time.sleep(2)
    
    # @staticmethod
    # def _smart_delay_by_filename(filename):
    #     """基于文件名的智能延迟"""
    #     # 计算文件名哈希值
    #     file_hash = hashlib.md5(filename.encode('utf-8')).hexdigest()
    #     hash_int = int(file_hash[:8], 16)  # 取前8位转为整数
        
    #     # 基于哈希值计算延迟 (0-6秒范围)
    #     delay = (hash_int % 60) * 0.1  # 0-6秒
        
    #     logger.info(f"⏰ 文件名延迟: {filename} -> {delay:.1f}s")
    #     return delay
    
    @staticmethod
    def _smart_resource_cleanup():
        """基于并发数的智能资源释放"""
        from .parallel_executor import PARALLEL_CONFIG
        
        # 获取当前活跃线程数（近似并发数）
        active_threads = threading.active_count()
        max_workers = PARALLEL_CONFIG['file_repair']['max_workers']
        
        # 根据并发数决定清理策略
        if max_workers >= 3:
            # 高并发：每max_workers个任务清理一次
            cleanup_frequency = max_workers
        elif max_workers == 2:
            # 中并发：每2个任务清理一次  
            cleanup_frequency = 2
        else:
            # 低并发：每4个任务清理一次
            cleanup_frequency = 4
        
        # 使用线程局部存储记录任务计数
        if not hasattr(threading.current_thread(), 'repair_count'):
            threading.current_thread().repair_count = 0
        
        threading.current_thread().repair_count += 1
        
        # 达到清理频率时执行清理
        if threading.current_thread().repair_count % cleanup_frequency == 0:
            logger.info(f"🧹 智能资源清理 (并发数: {max_workers}, 频率: {cleanup_frequency})")
            RepairOffice.kill_libreoffice()
            time.sleep(1)  # 清理后短暂休息
    
    @staticmethod
    def repair_with_python(input_path, output_path, file_type):
        """使用 Python 库直接修复文件"""
        try:
            logger.info(f"开始 Python 修复: {input_path} -> {output_path}")
            
            if file_type.lower() in ['docx', 'doc']:                  
                from docx import Document
                try:
                    doc = Document(input_path)
                    doc.save(output_path)
                    logger.info(f"Word 文档修复成功: {input_path}")
                    return True
                except Exception as e:
                    logger.error(f"Word 文档修复失败: {str(e)}")
                    return False
                    
            elif file_type.lower() in ['xlsx', 'xls']:
                # 使用 openpyxl 修复 Excel 文件
                import openpyxl
                try:
                    wb = openpyxl.load_workbook(input_path)
                    wb.save(output_path)
                    logger.info(f"Excel 文件修复成功: {input_path}")
                    return True
                except Exception as e:
                    logger.error(f"Excel 文件修复失败: {str(e)}")
                    return False
                    
            elif file_type.lower() in ['pdf']:
                # 使用 pypdf 修复 PDF 文件
                import pypdf
                try:
                    with open(input_path, 'rb') as file:
                        reader = pypdf.PdfReader(file)
                        writer = pypdf.PdfWriter()
                        
                        for page in reader.pages:
                            writer.add_page(page)
                            
                        with open(output_path, 'wb') as output_file:
                            writer.write(output_file)
                            
                    logger.info(f"PDF 文件修复成功: {input_path}")
                    return True
                except Exception as e:
                    logger.error(f"PDF 文件修复失败: {str(e)}")
                    return False
                    
            else:
                logger.warning(f"不支持的 Python 修复格式: {file_type}")
                return False
                
        except Exception as e:
            logger.error(f"Python 修复过程异常: {str(e)}")
            return False

    @staticmethod
    def _repair_single_file(file_info: tuple) -> Dict[str, Any]:
        """并行修复单个文件"""
        input_path, output_path, file_type, repair_tool = file_info
        process_id = f"repair_{os.path.basename(input_path)}_{int(time.time()*1000)}"
        
        try:           
            time.sleep(5)  # 固定5秒延迟

            logger.info(f"🔄 并行修复: {os.path.basename(input_path)}")
            start_time = time.time()
            
            # 使用外部工具修复
            if repair_tool:
                success = RepairOffice._repair_with_external_tool_parallel(
                    input_path, output_path, file_type, repair_tool, process_id
                )
            else:
                success = RepairOffice.repair_with_python(input_path, output_path, file_type)
            
            elapsed_time = time.time() - start_time
            
            # 🆕 智能资源释放：根据并发数决定清理频率
            RepairOffice._smart_resource_cleanup()

            if success:
                logger.info(f"✅ 并行修复完成: {os.path.basename(input_path)} [{elapsed_time:.1f}s]")
                return {
                    'status': 'success',
                    'file': os.path.basename(output_path),
                    'input_file': os.path.basename(input_path),
                    'process_time': elapsed_time
                }
            else:
                logger.error(f"❌ 并行修复失败: {os.path.basename(input_path)} [{elapsed_time:.1f}s]")
                return {
                    'status': 'error', 
                    'file': os.path.basename(input_path),
                    'message': '修复失败',
                    'process_time': elapsed_time
                }
                
        except Exception as e:
            logger.error(f"💥 并行修复异常: {os.path.basename(input_path)} - {e}")
            return {
                'status': 'error',
                'file': os.path.basename(input_path),
                'message': str(e)
            }
        finally:
            # 异步清理进程
            if repair_tool:
                ProcessManager.async_cleanup(process_id, delay=2)
    
    @staticmethod
    def _repair_with_external_tool_parallel(input_path, output_path, file_type, repair_tool, process_id):
        """并行外部工具修复"""
        # type_map = {
        #     'docx': "docx:MS Word 2007 XML",
        #     'doc': "docx:MS Word 2007 XML", 
        #     'xlsx': "xlsx:MS Excel 2007 XML",
        #     'xls': "xlsx:MS Excel 2007 XML",
        #     'pdf': "pdf"
        # }
        type_map = {
            'docx': "docx",
            'doc': "docx", 
            'xlsx': "xlsx",
            'xls': "xlsx",
            'pdf': "pdf"
        }
        convert_type = type_map.get(file_type.lower(), "pdf")
        
        RepairOffice.kill_libreoffice()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            process = subprocess.Popen(
                [
                    repair_tool,
                    "--headless",
                    "--norestore", 
                    "--nodefault",
                    "--nologo",
                    "--invisible",
                    "--convert-to", convert_type,
                    "--outdir", os.path.dirname(output_path),
                    input_path
                ],
                check=True,
                capture_output=True,  # 捕获输出和错误信息
                text=True,  # 以文本形式返回输出
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            ProcessManager.register_process(process_id, process)
            
            timeout = 90
            try:
                return_code = process.wait(timeout=timeout)
                if return_code != 0:
                    logger.warning(f"修复进程异常退出: {os.path.basename(input_path)}, 返回码: {return_code}")
            except subprocess.TimeoutExpired:
                logger.warning(f"⏰ 修复进程超时: {os.path.basename(input_path)}")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            
            time.sleep(1)
            
            max_retry = 3
            for retry in range(max_retry):
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    file_size = os.path.getsize(output_path)
                    logger.info(f"✅ 修复文件生成成功: {os.path.basename(output_path)} ({file_size} bytes)")
                    return True
                elif retry < max_retry - 1:
                    time.sleep(1)
            
            logger.error(f"❌ 修复文件未生成: {output_path}")
            return False
                
        except Exception as e:
            logger.error(f"💥 修复进程异常 {os.path.basename(input_path)}: {e}")
            return False

    @staticmethod
    def repair_with_external_tool(input_path, output_path, file_type, repair_tool):
        """使用外部工具修复单个文件"""
        # 根据文件类型设置转换类型
        if file_type.lower() in ['docx', 'doc']:
            convert_type = "docx"
            #convert_type = "docx:MS Word 2007 XML"
        elif file_type.lower() in ['xlsx', 'xls']:
            #convert_type = "xlsx:Calc MS Excel 2007 XML"
            convert_type = "xlsx"
            #convert_type = "xlsx:MS Excel 2007 XML"
        elif file_type.lower() == 'pdf':
            convert_type = "pdf"
        else:
            logger.warning(f"不支持的修复格式: {file_type}")
            return False

        # 先清理可能存在的 LibreOffice 进程
        RepairOffice.kill_libreoffice()
        
        try:
            logger.info(f"开始外部工具修复: {input_path} -> {output_path}")
            
            result = subprocess.run(
                [
                    repair_tool,
                    "--headless",              # 无界面模式
                    "--norestore",             # 禁止恢复对话框
                    "--nodefault",             # 不启动默认组件
                    "--nologo",                # 不显示启动logo
                    "--invisible",             # 完全不可见模式
                    "--convert-to", convert_type, 
                    "--outdir", os.path.dirname(output_path), # 必须紧跟在--convert-to之后
                    input_path
                ],
                timeout=90,  # 增加超时时间
                check=False, 
                capture_output=False,
                text=False,
                stdout=subprocess.DEVNULL,  # 忽略标准输出
                stderr=subprocess.DEVNULL,   # 忽略错误输出
            )
                    
        except subprocess.TimeoutExpired:
            logger.warning(f"修复进程超时: {os.path.basename(input_path)}")
            # 超时也不立即返回，继续检查文件
        
        finally:
            # 最终清理
            RepairOffice.kill_libreoffice()
        
        # 等待文件系统更新
        time.sleep(3)
        
        # 唯一成功标准：目标文件是否生成
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"✅ 修复文件已生成: {output_path}")
            return True
        else:
            logger.error(f"❌ 修复后文件未找到: {output_path}")
            return False

    @staticmethod
    def repair_office(input_dir, output_dir, file_type, repair_method='auto', repair_tool=None):
        os.makedirs(output_dir, exist_ok=True)
        repair_file_type = f".{file_type}"
        repaired_files = []
        
        logger.info(f"=== 文件修复调试信息 ===")
        logger.info(f"修复方法: {repair_method}")
        logger.info(f"修复工具: {repair_tool}")
        logger.info(f"输入目录: {input_dir}")
        logger.info(f"输出目录: {output_dir}")
        
        # 收集文件列表
        file_list = []
        for filename in os.listdir(input_dir):
            if filename.endswith(repair_file_type):
                file_path = os.path.join(input_dir, filename)
                output_file_path = os.path.join(output_dir, filename)
                file_list.append((file_path, output_file_path, file_type, repair_tool))
        
        # 并行修复（多个文件时）
        if len(file_list) > 1 and repair_tool:
            logger.info(f"🔄 使用并行修复 {len(file_list)} 个文件")
            
            task_list = [
                (RepairOffice._repair_single_file, (file_info,), {})
                for file_info in file_list
            ]
            
            result = ParallelExecutor.execute_parallel('file_repair', task_list)
            
            # 分析结果
            for task_result in result['results'].values():
                if task_result.get('status') == 'success':
                    repaired_files.append(task_result['file'])
            
            # 最终清理
            ProcessManager.cleanup_all_processes()
            
            logger.info(f"=== 并行修复完成 ===")
            logger.info(f"成功修复 {len(repaired_files)} 个文件")
            logger.info(f"修复文件列表: {repaired_files}")
            
            return {
                'status': 'success' if repaired_files else 'error',
                'message': f'成功修复 {len(repaired_files)} 个文件' if repaired_files else '修复失败，无成功修复的文件',
                'repaired_files': repaired_files,
                'output_dir': output_dir,
                'repair_method_used': repair_method,
                'parallel_summary': result['summary'],
                'download_info': {
                    'type': 'multiple' if len(repaired_files) > 1 else 'single',
                    'files': repaired_files,
                    'output_dir': output_dir,
                    'operation_name': 'file_repair'
                }
            }
        else:
            # 单个文件或Python修复使用原逻辑
            for filename in os.listdir(input_dir):
                if filename.endswith(repair_file_type):
                    file_path = os.path.join(input_dir, filename)
                    output_file_path = os.path.join(output_dir, filename)
                    
                    try:
                        logger.info(f"开始修复文件: {filename}")
                        
                        success = False
                        
                        # 明确的方法选择逻辑
                        if repair_method == 'python':
                            success = RepairOffice.repair_with_python(file_path, output_file_path, file_type)
                            
                        elif repair_method in ['libreoffice', 'custom']:
                            if repair_tool:
                                logger.info(f"使用外部工具修复: {filename}")
                                success = RepairOffice.repair_with_external_tool(file_path, output_file_path, file_type, repair_tool)
                            else:
                                logger.error(f"外部工具路径未提供，无法修复: {filename}")
                                continue
                        else:
                            # 自动选择：先尝试 Python，失败后尝试外部工具
                            logger.info(f"自动模式，先尝试Python修复: {filename}")
                            success = RepairOffice.repair_with_python(file_path, output_file_path, file_type)
                            if not success and repair_tool:
                                logger.info(f"Python 修复失败，尝试外部工具修复: {filename}")
                                success = RepairOffice.repair_with_external_tool(file_path, output_file_path, file_type, repair_tool)
                        
                        # 简化的成功判断
                        if success:
                            logger.info(f"✅ 修复成功：{filename}")
                            repaired_files.append(filename)
                        else:
                            logger.error(f"❌ 修复失败：{filename}")
                            
                    except Exception as e:
                        logger.error(f"❌ 修复过程异常：{filename} | 错误：{str(e)}")
                        # 异常时也检查文件是否生成
                        if os.path.exists(output_file_path) and os.path.getsize(output_file_path) > 0:
                            logger.info(f"⚠️ 异常但文件已生成: {filename}")
                            repaired_files.append(filename)
                        continue
            
            logger.info(f"=== 修复完成 ===")
            logger.info(f"成功修复 {len(repaired_files)} 个文件")
            logger.info(f"修复文件列表: {repaired_files}")
            
            return {
                'status': 'success' if repaired_files else 'error',
                'message': f'成功修复 {len(repaired_files)} 个文件' if repaired_files else '修复失败，无成功修复的文件',
                'repaired_files': repaired_files,
                'output_dir': output_dir,
                'repair_method_used': repair_method,
                'download_info': {
                    'type': 'multiple' if len(repaired_files) > 1 else 'single',
                    'files': repaired_files,
                    'output_dir': output_dir,
                    'operation_name': 'file_repair'
                }
            }