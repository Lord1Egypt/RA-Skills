import os
import re
import logging
import subprocess
import time
import shutil
from typing import Dict, Any, List, Tuple
from .parallel_executor import ParallelExecutor
logger = logging.getLogger(__name__)
def _find_libreoffice():
    """自动检测 LibreOffice 安装路径"""
    # 常见安装路径
    common_paths = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        r"D:\Program Files\LibreOffice\program\soffice.exe",
        r"D:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    # 尝试从 PATH 环境变量查找
    soffice_path = shutil.which("soffice")
    if soffice_path:
        return soffice_path
    return None

# 动态获取，如果找不到则返回 None
convert_tool_default = _find_libreoffice()

class MutualConver:
    """文件转换服务"""
    
    @staticmethod
    def kill_libreoffice():
        """强制终止所有 LibreOffice 进程"""
        os.system('taskkill /f /im soffice.exe >nul 2>&1')
        os.system('taskkill /f /im soffice.bin >nul 2>&1')
        time.sleep(1) 
    
    @staticmethod
    def _check_output_files(input_path, output_dir, output_format):
        """检查各种可能的输出文件路径"""
        input_basename = os.path.basename(input_path)
        input_name_no_ext = os.path.splitext(input_basename)[0]
        
        # 可能的输出文件名列表（按可能性排序）
        possible_files = [
            os.path.join(output_dir, input_name_no_ext + f'.{output_format}'),  # 最常见
            os.path.join(output_dir, input_basename.rsplit('.', 1)[0] + f'.{output_format}'),  # 多扩展名情况
            os.path.join(output_dir, f"document.{output_format}"),  # LibreOffice默认名
            os.path.join(output_dir, f"output.{output_format}"),    # 其他默认名
        ]
        
        for file_path in possible_files:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                return file_path
        return None
    
    @staticmethod
    def _convert_with_libreoffice_fast(input_path, output_path, convert_tool, output_format='pdf'):
        """快速LibreOffice转换"""
        # 先清理进程
        MutualConver.kill_libreoffice()
        time.sleep(2)
        
        output_dir = os.path.dirname(output_path)
        input_basename = os.path.basename(input_path)
        expected_name = os.path.splitext(input_basename)[0] + f'.{output_format}'
        expected_path = os.path.join(output_dir, expected_name)
        
        # 先删除可能存在的旧文件
        if os.path.exists(expected_path):
            try:
                os.remove(expected_path)
            except:
                pass
        
        try:
            logger.info(f"🔄 开始转换: {input_basename}")
            start_time = time.time()
            
            cmd = [
                convert_tool,
                "--headless",
                "--convert-to", output_format, 
                "--outdir", output_dir,
                input_path
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 等待进程完成，设置合理超时
            timeout = 60
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                return_code = process.returncode
                
                if stdout:
                    logger.debug(f"LibreOffice输出: {stdout[:100]}")
                if stderr:
                    logger.debug(f"LibreOffice错误: {stderr[:100]}")
                    
                logger.info(f"进程退出，返回码: {return_code}")
                
            except subprocess.TimeoutExpired:
                logger.warning("转换超时，强制终止")
                process.kill()
                stdout, stderr = process.communicate()
            
            # 等待文件系统稳定
            time.sleep(2)
            
            # 检查文件是否生成
            max_retry = 3
            for retry in range(max_retry):
                if os.path.exists(expected_path) and os.path.getsize(expected_path) > 0:
                    file_size = os.path.getsize(expected_path)
                    total_time = time.time() - start_time
                    
                    # 如果需要重命名到output_path
                    if expected_path != output_path:
                        os.rename(expected_path, output_path)
                    
                    logger.info(f"✅ 转换成功: {os.path.basename(output_path)} ({file_size} bytes) [{total_time:.1f}s]")
                    return True
                
                if retry < max_retry - 1:
                    time.sleep(2)  # 等待2秒再检查
            
            logger.error(f"❌ 文件未生成: {expected_path}")
            return False
            
        except Exception as e:
            logger.error(f"💥 转换异常: {e}")
            return False
        finally:
            MutualConver.kill_libreoffice()
    
    @staticmethod
    def _convert_single_file(file_info: tuple) -> Dict[str, Any]:
        """并行转换单个文件"""
        input_path, output_path, convert_type, convert_tool = file_info
        
        try:
            logger.info(f"🔄 开始转换: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
            start_time = time.time()
            
            success = False
            if convert_type == 'image_to_pdf':
                success = MutualConver._image_convert_pdf_single(input_path, output_path, convert_tool)
            elif convert_type == 'word_to_pdf':
                success = MutualConver._word_convert_pdf_single(input_path, output_path, convert_tool)
            elif convert_type == 'pdf_to_image':
                success = MutualConver._pdf_convert_image_single(input_path, output_path, convert_tool)
            elif convert_type == 'pdf_to_word':
                success = MutualConver._pdf_convert_docx_single(input_path, output_path, convert_tool)
            elif convert_type == 'excel_to_pdf':
                success = MutualConver._excel_convert_pdf_single(input_path, output_path, convert_tool)
            elif convert_type == 'pdf_to_xlsx':
                success = MutualConver._pdf_convert_xlsx_single(input_path, output_path, convert_tool)
            
            elapsed_time = time.time() - start_time
            
            if success:
                logger.info(f"✅ 转换完成: {os.path.basename(output_path)} [{elapsed_time:.1f}s]")
                return {
                    'status': 'success',
                    'file': os.path.basename(output_path),
                    'input_file': os.path.basename(input_path),
                    'convert_type': convert_type,
                    'process_time': elapsed_time
                }
            else:
                logger.error(f"❌ 转换失败: {os.path.basename(input_path)} [{elapsed_time:.1f}s]")
                return {
                    'status': 'error',
                    'file': os.path.basename(input_path),
                    'message': '转换失败',
                    'process_time': elapsed_time
                }
                
        except Exception as e:
            logger.error(f"💥 转换异常: {os.path.basename(input_path)} - {e}")
            return {
                'status': 'error',
                'file': os.path.basename(input_path),
                'message': str(e)
            }
    
    @staticmethod
    def _image_convert_pdf_single(input_path, output_path, convert_tool):
        """单文件图片转PDF"""
        try:
            if convert_tool:
                return MutualConver._convert_with_libreoffice_fast(input_path, output_path, convert_tool, 'pdf')
            else:
                from PIL import Image
                img = Image.open(input_path)
                img.save(output_path, 'PDF', save_all=True)
                return True
        except Exception as e:
            logger.error(f"图片转PDF失败 {input_path}: {e}")
            return False
    
    @staticmethod
    def _word_convert_pdf_single(input_path, output_path, convert_tool):
        """单文件Word转PDF"""
        if not convert_tool:
            convert_tool = convert_tool_default
        
        if not os.path.exists(convert_tool):
            logger.error(f"LibreOffice不存在: {convert_tool},使用pyhton方法")
            try:
                from docx2pdf import convert
                convert(input_path, output_path)
                return True
            except Exception as e:
                logger.error(f"Python转换失败: {e}")
                return False
            
        
        MutualConver.kill_libreoffice()
    
        output_dir = os.path.dirname(output_path)
        expected_path = os.path.join(output_dir,
                                os.path.splitext(os.path.basename(input_path))[0] + ".pdf")
        
        try:
            result = subprocess.run(
                [
                    convert_tool,
                    "--headless", 
                    "--convert-to", "pdf",
                    "--outdir", output_dir,
                    input_path
                ],
                capture_output=True,
                timeout=30, 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except subprocess.TimeoutExpired:
            # 30秒超时是预期的！
            logger.info(f"🔄 30秒超时（预期中），检查文件...")
        except Exception as e:
            logger.error(f"❌ 转换进程异常: {e}")
            return False

        time.sleep(2)
        
        if os.path.exists(expected_path) and os.path.getsize(expected_path) > 0:
            if expected_path != output_path:
                os.rename(expected_path, output_path)
            logger.info(f"✅ 转换成功")
            return True
        
        logger.error(f"❌ 转换失败")
        return False

    
    @staticmethod
    def _pdf_convert_image_single(input_path, output_path, convert_tool):
        """单文件PDF转图片"""
        try:
            if convert_tool:
                return MutualConver._convert_with_libreoffice_fast(input_path, output_path, convert_tool, 'jpg')
            else:
                import fitz
                document = fitz.open(input_path)
                for page_number in range(len(document)):
                    page = document[page_number]
                    pix = page.get_pixmap()
                    output_path_page = output_path
                    if len(document) > 1:
                        output_path_page = os.path.join(
                            os.path.dirname(output_path),
                            f"{os.path.splitext(os.path.basename(output_path))[0]}_page{page_number + 1}.jpg"
                        )
                    pix.save(output_path_page)
                document.close()
                return True
        except Exception as e:
            logger.error(f"PDF转图片失败 {input_path}: {e}")
            return False
    
    @staticmethod
    def _pdf_convert_docx_single(input_path, output_path, convert_tool):
        """单文件PDF转Word"""
        if convert_tool:
            return MutualConver._convert_with_libreoffice_fast(input_path, output_path, convert_tool, 'docx')
        else:
            try:
                from pdf2docx import Converter
                cv = Converter(input_path)
                cv.convert(output_path)
                cv.close()
                return True
            except Exception as e:
                logger.error(f"PDF转Word失败 {os.path.basename(input_path)}: {e}")
                return False
    
    @staticmethod
    def _excel_convert_pdf_single(input_path, output_path, convert_tool):
        """单文件Excel转PDF - 适配并行环境"""
        
        # 如果传入了外部工具（LibreOffice），优先使用
        if convert_tool:
            return MutualConver._convert_with_libreoffice_fast(input_path, output_path, convert_tool, 'pdf')
        
        # 没有外部工具，尝试用win32com
        try:
            import win32com.client
            import pythoncom


            
            logger.info(f"尝试用win32com转换Excel: {os.path.basename(input_path)}")
            
            # 关键：每个线程必须独立初始化COM
            # 检查当前线程是否已初始化
            try:
                pythoncom.CoInitialize()
                com_initialized = True
            except Exception as e:
                # 可能已经初始化过了
                logger.debug(f"COM可能已初始化: {e}")
                com_initialized = False
            
            excel = None
            workbook = None
            
            try:
                # 创建Excel应用实例 - 不可见模式
                excel = win32com.client.DispatchEx("Excel.Application")
                excel.Visible = False
                excel.DisplayAlerts = False
                excel.ScreenUpdating = False  # 关闭屏幕更新，提高性能
                
                # 打开工作簿
                workbook = excel.Workbooks.Open(input_path)
                
                # 导出为PDF
                # 参数说明：
                # 0 = xlTypePDF
                # 输出路径
                workbook.ExportAsFixedFormat(0, output_path)
                
                logger.info(f"win32com转换成功: {os.path.basename(output_path)}")
                return True
                
            except Exception as e:
                logger.error(f"win32com转换失败: {e}")
                return False
                
            finally:
                # 清理资源
                if workbook:
                    try:
                        workbook.Close(SaveChanges=False)
                    except:
                        pass
                if excel:
                    try:
                        excel.Quit()
                    except:
                        pass
                
                # 释放COM
                if com_initialized:
                    try:
                        pythoncom.CoUninitialize()
                    except:
                        pass
                
        except ImportError:
            logger.error("win32com未安装，无法使用Excel转换")
            return False
        except Exception as e:
            logger.error(f"win32com初始化失败: {e}")
            return False
    
    @staticmethod
    def _pdf_convert_xlsx_single(input_path, output_path, convert_tool):
        """单文件PDF转Excel"""
        try:
            # 生成CSV临时文件路径
            temp_dir = os.path.dirname(output_path)
            input_filename = os.path.splitext(os.path.basename(input_path))[0]
            csv_path = os.path.join(temp_dir, f"{input_filename}.csv")
            
            # 将PDF转换为CSV
            import tabula
            tabula.convert_into(input_path, csv_path, output_format='csv', pages='all')
            
            # 读取CSV文件并写入Excel
            import pandas as pd
            df = pd.read_csv(csv_path, encoding='utf-8')
            
            # 删除临时CSV文件
            if os.path.exists(csv_path):
                os.remove(csv_path)
            
            # 保存为Excel
            from .data_operation_service import DataOperation
            DataOperation.data_pd_write(output_path, 'Sheet1', df)
            
            return True
        except Exception as e:
            logger.error(f"PDF转Excel失败 {input_path}: {e}")
            return False

    @staticmethod
    def generate_file_paths(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """
        生成输入和输出文件的路径对
        """
        file_pairs = []
        files = [file for file in os.listdir(input_dir)]
        if old_suffix:
            files = [file for file in os.listdir(input_dir) if file.endswith(f'.{old_suffix}')]
        
        # 过滤临时文件
        filtered_files = []
        for file in files:
            # 跳过Word临时文件（~$开头）
            if file.startswith('~$'):
                logger.warning(f"跳过临时文件: {file}")
                continue
            filtered_files.append(file)
        
        for file in filtered_files:
            input_path = os.path.join(input_dir, file)
            input_path_suffix = os.path.splitext(os.path.basename(input_path))[1]
            output_name = re.sub(input_path_suffix, f'.{new_suffix}', file)
            output_path = os.path.join(output_dir, output_name)
            file_pairs.append((input_path, output_path))
        
        logger.info(f"找到 {len(file_pairs)} 个有效文件进行转换")
        return file_pairs

    @staticmethod
    def _execute_conversion(file_pairs, convert_type, convert_exe=None):
        """
        统一执行转换任务 - 优化版本
        """
        if not file_pairs:
            return {
                'status': 'error',
                'message': '没有找到符合条件的文件',
                'converted_files': [],
                'failed_files': []
            }
        
        logger.info(f"🔄 开始转换 {len(file_pairs)} 个文件，类型: {convert_type}")
        
        # 创建并行任务
        task_list = []
        for input_path, output_path in file_pairs:
            task_list.append((MutualConver._convert_single_file, 
                            ((input_path, output_path, convert_type, convert_exe),), {}))
        
        # 执行转换（串行/并行由PARALLEL_CONFIG控制）
        result = ParallelExecutor.execute_parallel('file_convert', task_list)
        
        # 分析结果
        converted_files = []
        failed_files = []
        
        for task_result in result['results'].values():
            if task_result.get('status') == 'success':
                converted_files.append(task_result['file'])
            else:
                failed_files.append({
                    'file': task_result.get('file', '未知文件'),
                    'message': task_result.get('message', '未知错误')
                })
        
        # 构建响应
        if converted_files:
            response = {
                'status': 'success' if not failed_files else 'partial_success',
                'message': f'成功转换 {len(converted_files)} 个文件',
                'converted_files': converted_files,
                'output_dir': os.path.dirname(file_pairs[0][1]) if file_pairs else '',
                'parallel_summary': result['summary'],
                'download_info': {
                    'type': 'multiple' if len(converted_files) > 1 else 'single',
                    'files': converted_files,
                    'output_dir': os.path.dirname(file_pairs[0][1]) if file_pairs else '',
                    'operation_name': 'file_convert'
                }
            }
            
            if failed_files:
                response['failed_files'] = failed_files
                response['failed_count'] = len(failed_files)
                response['message'] = f'成功 {len(converted_files)} 个，失败 {len(failed_files)} 个'
            
            return response
        else:
            return {
                'status': 'error',
                'message': '所有文件转换失败',
                'converted_files': [],
                'failed_files': failed_files,
                'failed_count': len(failed_files),
                'output_dir': os.path.dirname(file_pairs[0][1]) if file_pairs else ''
            }

    @staticmethod
    def image_convert_pdf(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """图片转PDF"""
        file_pairs = MutualConver.generate_file_paths(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        return MutualConver._execute_conversion(file_pairs, 'image_to_pdf', convert_exe)

    @staticmethod
    def word_convert_pdf(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """Word转PDF - 优先使用docx2pdf"""
        file_pairs = MutualConver.generate_file_paths(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        return MutualConver._execute_conversion(file_pairs, 'word_to_pdf', convert_exe)

    @staticmethod
    def excel_convert_pdf(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """Excel转PDF"""
        file_pairs = MutualConver.generate_file_paths(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        return MutualConver._execute_conversion(file_pairs, 'excel_to_pdf', convert_exe)

    @staticmethod
    def pdf_convert_image(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """PDF转图片"""
        file_pairs = MutualConver.generate_file_paths(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        return MutualConver._execute_conversion(file_pairs, 'pdf_to_image', convert_exe)

    @staticmethod
    def pdf_convert_docx(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """PDF转Word"""
        file_pairs = MutualConver.generate_file_paths(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        return MutualConver._execute_conversion(file_pairs, 'pdf_to_word', convert_exe)

    @staticmethod
    def pdf_convert_xlsx(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """PDF转Excel"""
        file_pairs = MutualConver.generate_file_paths(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        return MutualConver._execute_conversion(file_pairs, 'pdf_to_xlsx', convert_exe)

    @staticmethod
    def files_convert_pdf(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """
        高层函数：根据文件类型调用相应的转换函数
        """
        image_suffix = ['jpg', 'jpeg', 'png', 'bmp', 'webp', 'avif', 'apng',
                      'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo',
                      'eps', 'ai', 'raw', 'wmf']
        
        if old_suffix.lower() in image_suffix:
            return MutualConver.image_convert_pdf(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        elif old_suffix.lower() == 'docx':
            return MutualConver.word_convert_pdf(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        elif old_suffix.lower() == 'xlsx':
            return MutualConver.excel_convert_pdf(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        else:
            raise ValueError(f"不支持的文件格式: {old_suffix}")

    @staticmethod
    def pdf_convert_files(input_dir, output_dir, convert_exe=None, old_suffix=None, new_suffix=None):
        """
        高层函数：将PDF文件转换为其他格式
        """
        image_suffix = ['jpg', 'jpeg', 'png', 'bmp', 'webp', 'avif', 'apng',
                      'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo',
                      'eps', 'ai', 'raw', 'wmf']
        
        if new_suffix.lower() in image_suffix:
            return MutualConver.pdf_convert_image(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        elif new_suffix.lower() == 'docx':
            return MutualConver.pdf_convert_docx(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        elif new_suffix.lower() == 'xlsx':
            return MutualConver.pdf_convert_xlsx(input_dir, output_dir, convert_exe, old_suffix, new_suffix)
        else:
            raise ValueError(f"不支持的文件格式: {new_suffix}")
