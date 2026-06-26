import os
import logging
import time
import win32print
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AutoPrinter:
    """文件打印服务"""
    
    @staticmethod
    def startup_cleanup():
        """应用启动时清理残留的打印资源"""
        try:
            logger.info("🔧 执行打印服务启动清理...")
            
            # 1. 清理默认打印机的打印队列中的错误任务
            try:
                printer_name = win32print.GetDefaultPrinter()
                handle = win32print.OpenPrinter(printer_name)
                
                # 获取所有打印任务
                jobs = win32print.EnumJobs(handle, 0, -1, 1)
                cleaned_count = 0
                
                for job in jobs:
                    # 清理错误状态、保留状态或正在删除的任务
                    if job['Status'] in [
                        win32print.JOB_STATUS_ERROR, 
                        win32print.JOB_STATUS_DELETING,
                        win32print.JOB_STATUS_RETAINED,
                        win32print.JOB_STATUS_OFFLINE,
                        win32print.JOB_STATUS_PAPEROUT,
                        win32print.JOB_STATUS_USER_INTERVENTION
                    ]:
                        try:
                            win32print.SetJob(handle, job['JobId'], 0, None, win32print.JOB_CONTROL_DELETE)
                            cleaned_count += 1
                            logger.info(f"🗑️ 清理残留打印任务: {job['Document']} (状态: {job['Status']})")
                        except Exception as e:
                            logger.warning(f"清理打印任务失败: {e}")
                
                win32print.ClosePrinter(handle)
                logger.info(f"✅ 清理了 {cleaned_count} 个错误打印任务")
                
            except Exception as e:
                logger.warning(f"清理打印队列失败: {e}")
            
            # 2. 强制释放COM资源
            try:
                import pythoncom
                pythoncom.CoUninitialize()
                logger.info("✅ COM资源已清理")
            except Exception as e:
                logger.debug(f"COM资源清理: {e}")
                
            logger.info("✅ 打印服务启动清理完成")
            
        except Exception as e:
            logger.error(f"❌ 启动清理失败: {e}")

    @staticmethod
    def judgment_print(input_dir, sheet_name =None, area_print=None, printer_name=None):
        xlsx_suffixs = ('.xls', '.xlsx')
        docx_suffixs = ('.doc', '.docx')
        printed_files = []
        failed_files = []
        
        for root, _, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file_path).suffix.lower()
                
                try:
                    if file_ext in xlsx_suffixs:
                        result = AutoPrinter.xlsx_print(file_path, sheet_name, area_print, printer_name)
                    elif file_ext in docx_suffixs:
                        result = AutoPrinter.docx_print(file_path, printer_name)
                    else:
                        result = AutoPrinter.regular_file_print(file_path, printer_name)
                    
                    if result['status'] == 'success':
                        printed_files.append(file)
                        logger.info(f"✅ 成功打印文件: {file}")
                    else:
                        failed_files.append({'file': file, 'error': result.get('message', '未知错误')})
                        logger.error(f"❌ 打印失败: {file} - {result.get('message')}")
                        
                except Exception as e:
                    error_msg = f"打印异常: {str(e)}"
                    failed_files.append({'file': file, 'error': error_msg})
                    logger.error(f"❌ 打印异常: {file} - {error_msg}")
        
        # 构建详细的结果信息
        total_files = len(printed_files) + len(failed_files)
        if failed_files:
            message = f"成功打印 {len(printed_files)} 个文件，失败 {len(failed_files)} 个文件"
            status = 'warning' if printed_files else 'error'
        else:
            message = f"成功打印 {len(printed_files)} 个文件"
            status = 'success'

        AutoPrinter.wait_for_print_completion()

        return {
            'status': status,
            'message': message,
            'printed_files': printed_files,
            'failed_files': failed_files,
            'total_files': total_files,
            'success_count': len(printed_files),
            'fail_count': len(failed_files),
            'ui_status': status,  # 确保有 ui_status 字段
            'success': status in ['success', 'warning']  # 明确 success 字段
        }

    @staticmethod
    def xlsx_print(file_path, sheet_name, print_area, printer_name=None):
        excel = None
        workbook = None
        try:
            # 首先导入必要的COM库
            import pythoncom
            import win32com.client as win32
            
            # 关键修复：在多线程环境中初始化COM
            pythoncom.CoInitialize()
            
            excel = win32.Dispatch('Excel.Application')
            excel.Visible = False  # 不显示Excel窗口
            excel.DisplayAlerts = False  # 不显示警告对话框
            excel.ScreenUpdating = False  # 禁止屏幕更新，提高性能
            excel.EnableEvents = False  # 禁用事件，避免干扰
            workbook = excel.Workbooks.Open(file_path)
            if sheet_name:
                sheet = workbook(sheet_name)
            else:
                sheet = workbook.ActiveSheet
            
            
            # 设置打印区域
            if print_area:
                sheet.PageSetup.PrintArea = print_area
                logger.info(f"设置打印区域: {print_area}")
            
            # 设置打印机并打印
            if printer_name:
                try:
                    # 修复打印机路径格式 - 修正语法错误
                    if printer_name.startswith('\\') and not printer_name.startswith('\\\\'):
                        # 如果只有一个反斜杠，添加一个变成双反斜杠
                        printer_name = '\\' + printer_name
                    elif not printer_name.startswith('\\'):
                        # 如果没有反斜杠，添加双反斜杠前缀
                        printer_name = '\\\\10.92.30.89\\' + printer_name
                    
                    logger.info(f"尝试使用打印机: {printer_name}")
                    
                    # 使用 PrintOut 的 ActivePrinter 参数
                    workbook.PrintOut(ActivePrinter=printer_name)
                    logger.info(f"✅ 使用指定打印机成功打印: {printer_name}")
                except Exception as e:
                    logger.warning(f"设置指定打印机失败 {printer_name}: {e}, 使用默认打印机")
                    workbook.PrintOut()  # 使用默认打印机
            else:
                workbook.PrintOut()  # 使用默认打印机
                logger.info("✅ 使用默认打印机成功打印")
            
            # 给打印任务一些处理时间
            time.sleep(1)
            
            return {'status': 'success', 'message': 'Excel文件打印成功'}
            
        except Exception as e:
            error_msg = f'Excel打印失败: {str(e)}'
            logger.error(f'Excel打印失败 | 文件: {file_path} | 错误: {str(e)}')
            return {'status': 'error', 'message': error_msg}
        finally:
            try:
                if workbook:
                    workbook.Close(SaveChanges=False)
                if excel:
                    excel.Quit()
            except Exception as e:
                logger.warning(f"清理Excel资源时出错: {str(e)}")
            finally:
                # 关键修复：释放COM资源
                try:
                    pythoncom.CoUninitialize()
                except:
                    pass
    
    @staticmethod
    def docx_print(file_path, printer_name=None):
        docx = None
        docx_word = None
        try:
            # 首先导入必要的COM库
            import pythoncom
            import win32com.client as win32
            
            # 关键修复：在多线程环境中初始化COM
            pythoncom.CoInitialize()
            
            docx = win32.Dispatch('Word.Application')
            docx.Visible = False  # 不显示Excel窗口
            docx.DisplayAlerts = False  # 不显示警告对话框
            docx.ScreenUpdating = False  # 禁止屏幕更新，提高性能
            docx_word = docx.Documents.Open(file_path)
        # 设置打印机并打印
            if printer_name:
                try:
                    # 修复打印机路径格式 - 修正语法错误
                    if printer_name.startswith('\\') and not printer_name.startswith('\\\\'):
                        # 如果只有一个反斜杠，添加一个变成双反斜杠
                        printer_name = '\\' + printer_name
                    elif not printer_name.startswith('\\'):
                        # 如果没有反斜杠，添加双反斜杠前缀
                        printer_name = '\\\\10.92.30.89\\' + printer_name
                    
                    logger.info(f"尝试使用打印机: {printer_name}")
                    
                    # 使用 PrintOut 的 ActivePrinter 参数
                    docx_word.PrintOut(ActivePrinter=printer_name)
                    logger.info(f"✅ 使用指定打印机成功打印: {printer_name}")
                except Exception as e:
                    logger.warning(f"设置指定打印机失败 {printer_name}: {e}, 使用默认打印机")
                    docx_word.PrintOut()  # 使用默认打印机
            else:
                docx_word.PrintOut()  # 使用默认打印机
                logger.info("✅ 使用默认打印机成功打印")
            
            # 给打印任务一些处理时间
            time.sleep(1)
            
            return {'status': 'success', 'message': 'docx文件打印成功'}
            
        except Exception as e:
            error_msg = f'Excel打印失败: {str(e)}'
            logger.error(f'Excel打印失败 | 文件: {file_path} | 错误: {str(e)}')
            return {'status': 'error', 'message': error_msg}
        finally:
            try:
                if docx_word:
                    docx_word.Close(SaveChanges=False)
                if docx:
                    docx.Quit()
            except Exception as e:
                logger.warning(f"清理Word资源时出错: {str(e)}")
            finally:
                # 关键修复：释放COM资源
                try:
                    import pythoncom
                    pythoncom.CoUninitialize()
                except:
                    pass

    @staticmethod
    def regular_file_print(file_path, printer_name=None):
        try:
            import win32api
            import win32print
            
            # 使用指定打印机或默认打印机
            if printer_name:
                try:
                    # 验证打印机是否存在
                    printers = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
                    if printer_name in printers:
                        printer_to_use = printer_name
                        logger.info(f"使用指定打印机: {printer_name}")
                    else:
                        printer_to_use = win32print.GetDefaultPrinter()
                        logger.warning(f"指定打印机不存在: {printer_name}, 使用默认打印机: {printer_to_use}")
                except Exception as e:
                    printer_to_use = win32print.GetDefaultPrinter()
                    logger.warning(f"获取打印机列表失败: {e}, 使用默认打印机: {printer_to_use}")
            else:
                printer_to_use = win32print.GetDefaultPrinter()
                logger.info(f"使用默认打印机: {printer_to_use}")
            
            # 打印文件
            win32api.ShellExecute(
                0,
                "print",
                file_path,
                f'/d:"{printer_to_use}"',
                ".",
                0
            )
            
            # 给打印任务一些处理时间
            time.sleep(1)
            
            logger.info(f'✅ 已发送打印任务到 {printer_to_use}: {file_path}')
            return {'status': 'success', 'message': '文件打印成功'}
            
        except Exception as e:
            error_msg = f'文件打印失败: {str(e)}'
            logger.error(f'打印失败 | 文件: {file_path} | 错误: {str(e)}')
            return {'status': 'error', 'message': error_msg}
    @staticmethod
    def wait_for_print_completion(timeout=30):
        """等待打印队列完成"""
        start_time = time.time()
        try:
            while time.time() - start_time < timeout:
                # 检查默认打印机的队列状态
                printer_name = win32print.GetDefaultPrinter()
                handle = win32print.OpenPrinter(printer_name)
                
                try:
                    # 获取打印作业信息
                    jobs = win32print.EnumJobs(handle, 0, -1, 1)
                    if not jobs:
                        logger.info("✅ 打印队列已清空，打印完成")
                        return True
                    
                    # 检查是否有正在进行的打印作业
                    active_jobs = [job for job in jobs if job['Status'] not in [win32print.JOB_STATUS_COMPLETE, win32print.JOB_STATUS_DELETED]]
                    if not active_jobs:
                        logger.info("✅ 所有打印作业已完成")
                        return True
                        
                    logger.info(f"⏳ 等待打印作业完成，剩余作业数: {len(active_jobs)}")
                    time.sleep(0.5)
                    
                finally:
                    win32print.ClosePrinter(handle)
                    
        except Exception as e:
            logger.warning(f"打印状态检测异常: {e}")
            # 不阻塞，直接返回
            return True
        
        logger.warning("⚠️ 打印等待超时")
        return False