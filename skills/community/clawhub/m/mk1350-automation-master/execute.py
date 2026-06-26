"""
自动化办公大师 - 龙虾平台技能主入口
完整版 - 所有功能按次付费，专业版不限量
"""
import os
import logging
import tempfile
import shutil
from typing import Dict, Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== 导入所有服务类 ====================
from .services.automation_service import AutoMation as AutomationService
from .services.invoice_extraction_service import InvoiceExtractionService
from .services.invoice_extraction_service_complete import InvoiceExtractionServiceComplete
from .services.optimized_tax_reconciliation_service import OptimizedTaxAmountReconciliationService
from .services.file_convert_service import MutualConver
from .services.file_rename_service import OsOperation
from .services.file_generate_service import TemplateEngine
from .services.data_operation_service import DataOperation

# 初始化主服务
automation = AutomationService()


# ==================== 工具函数 ====================

def convert_types(obj: Any) -> Any:
    """转换NumPy类型为Python原生类型"""
    if isinstance(obj, (np.bool_)):
        return bool(obj)
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_types(item) for item in obj]
    elif hasattr(obj, 'item'):
        return obj.item()
    else:
        return obj


def calculate_billing(action: str, result: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算费用
    """
    # 安全获取用户订阅信息，平台可能传也可能不传
    subscription = params.get('_subscription', {})
    user_tier = subscription.get('tier', 'free')

    # 专业版用户不计单次费
    if user_tier == 'pro':
        return {'charged': False, 'amount': 0, 'message': '专业版不限次'}
    # if params.get('_subscription', {}).get('tier') == 'pro':
    #     return {
    #         'charged': False,
    #         'amount': 0,
    #         'message': '专业版不限次'
    #     }
    
    # 按次计费价格表
    prices = {
        'convert': 0.5,
        'rename': 0.2,
        'merge': 3.0,
        'generate': 1.5,
        'invoice_extract': 1.0,
        'tax_reconcile': 49.0
    }
    
    # 文件转换
    if action == 'convert':
        file_count = len(result.get('converted_files', []))
        amount = file_count * prices[action]
        if amount > 0:
            return {
                'charged': True,
                'amount': amount,
                'message': f'消费 {amount} 元（{file_count}个文件 × 0.5元/个）'
            }
        return {'charged': False, 'amount': 0, 'message': '没有成功转换的文件'}
    
    # 批量重命名
    elif action == 'rename':
        file_count = len(result.get('renamed_files', []))
        amount = file_count * prices[action]
        if amount > 0:
            return {
                'charged': True,
                'amount': amount,
                'message': f'消费 {amount} 元（{file_count}个文件 × 0.2元/个）'
            }
        return {'charged': False, 'amount': 0, 'message': '没有成功重命名的文件'}
    
    # 数据合并
    elif action == 'merge':
        return {
            'charged': True,
            'amount': prices[action],
            'message': f'消费 {prices[action]} 元'
        }
    
    # 模板生成
    elif action == 'generate':
        file_count = len(result.get('generated_files', []))
        amount = file_count * prices[action]
        if amount > 0:
            return {
                'charged': True,
                'amount': amount,
                'message': f'消费 {amount} 元（{file_count}个文件 × 1.5元/个）'
            }
        return {'charged': False, 'amount': 0, 'message': '没有成功生成的文件'}
    
    # 发票提取
    elif action == 'invoice_extract':
        success_count = result.get('summary', {}).get('success_count', 0)
        amount = success_count * prices[action]
        overall_accuracy = result.get('summary', {}).get('overall_accuracy', 100)
        
        if overall_accuracy < 98:
            return {
                'charged': False,
                'amount': 0,
                'refund': True,
                'reason': f'准确率{overall_accuracy:.1f}%低于98%保证'
            }
        
        if amount > 0:
            return {
                'charged': True,
                'amount': amount,
                'message': f'消费 {amount} 元（{success_count}张 × 1元/张）'
            }
        return {'charged': False, 'amount': 0, 'message': '没有成功提取的发票'}
    
    # 财税对账
    elif action == 'tax_reconcile':
        if result.get('need_refund', False):
            return {
                'charged': False,
                'amount': 0,
                'refund': True,
                'reason': result.get('refund_reason', '匹配率低于80%保证')
            }
        return {
            'charged': True,
            'amount': prices[action],
            'message': f'消费 {prices[action]} 元'
        }
    
    return {'charged': False, 'amount': 0, 'message': '未知操作'}


def get_algorithm_params(mode: str) -> Dict[str, Any]:
    """获取对账算法参数"""
    params = {
        'exact_match_threshold': 0.001,
        'approx_match_threshold_percent': 1.0,
        'many_to_many_amount_threshold': 1500,
        'many_to_many_percent_threshold': 1.0,
        'max_combination_depth': 3,
        'enable_many_to_many': True
    }
    
    if mode == 'precise':
        params.update({
            'exact_match_threshold': 0.0001,
            'approx_match_threshold_percent': 0.5,
            'many_to_many_amount_threshold': 500,
            'max_combination_depth': 4
        })
    elif mode == 'fast':
        params.update({
            'exact_match_threshold': 0.01,
            'approx_match_threshold_percent': 2.0,
            'many_to_many_amount_threshold': 3000,
            'max_combination_depth': 2,
            'enable_many_to_many': False
        })
    
    return params


# ==================== 主入口函数 ====================

def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """技能主执行函数"""
    try:
        action = params.get('action')
        if not action:
            return {'status': 'error', 'message': '请指定操作类型 (action)'}
        
        user_tier = params.get('_subscription', {}).get('tier', 'free')
        user_id = params.get('_user_id', 'anonymous')
        
        logger.info(f"用户 {user_id} ({user_tier}) 执行操作: {action}")
        
        # 路由到具体功能
        if action == 'convert':
            result = handle_convert(params)
        elif action == 'rename':
            result = handle_rename(params)
        elif action == 'merge':
            result = handle_merge(params)
        elif action == 'generate':
            result = handle_generate(params)
        elif action == 'invoice_extract':
            result = handle_invoice_extract(params)
        elif action == 'tax_reconcile':
            result = handle_tax_reconcile(params)
        else:
            return {'status': 'error', 'message': f'不支持的操作类型: {action}'}
        
        # 处理计费
        if result.get('status') == 'success':
            result['billing'] = calculate_billing(action, result, params)
        
        result = convert_types(result)
        logger.info(f"操作完成: {action}, 状态: {result.get('status')}")
        return result
        
    except Exception as e:
        logger.error(f"执行失败: {str(e)}", exc_info=True)
        return {'status': 'error', 'message': f'操作失败: {str(e)}'}


# ==================== 功能处理函数 ====================

def handle_convert(params: Dict[str, Any]) -> Dict[str, Any]:
    """文件批量转换"""
    files = params.get('files', [])
    if not files:
        return {'status': 'error', 'message': '请上传文件'}
    
    target_format = params.get('target_format', 'pdf').lower()
    source_format = params.get('source_format', '').lower()
    
    input_dir = tempfile.mkdtemp(prefix='convert_input_')
    output_dir = tempfile.mkdtemp(prefix='convert_output_')
    
    try:
        # 保存上传的文件
        saved_files = []
        for file_info in files:
            src_path = file_info.get('path')
            if src_path and os.path.exists(src_path):
                dst_path = os.path.join(input_dir, file_info.get('name'))
                shutil.copy2(src_path, dst_path)
                saved_files.append(dst_path)
        
        if not saved_files:
            return {'status': 'error', 'message': '未找到有效文件'}
        
        image_suffixes = ['jpg', 'jpeg', 'png', 'bmp', 'tif', 'gif', 'webp']
        converted_files = []
        failed_files = []
        
        # 图片转换
        if source_format in image_suffixes or target_format in image_suffixes:
            from PIL import Image
            for src_path in saved_files:
                try:
                    file_name = os.path.basename(src_path)
                    base_name = os.path.splitext(file_name)[0]
                    out_name = f"{base_name}.{target_format}"
                    out_path = os.path.join(output_dir, out_name)
                    
                    img = Image.open(src_path)
                    if target_format.lower() in ['jpg', 'jpeg']:
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        img.save(out_path, 'JPEG', quality=95)
                    else:
                        img.save(out_path)
                    
                    if os.path.exists(out_path):
                        converted_files.append({'name': out_name, 'path': out_path})
                    else:
                        failed_files.append(file_name)
                except Exception as e:
                    logger.error(f"图片转换失败: {e}")
                    failed_files.append(os.path.basename(src_path))
        
        # 文档转换
        else:
            try:
                result = automation.file_convert({
                    'input_dir': input_dir,
                    'output_dir': output_dir,
                    'old_suffix': source_format,
                    'new_suffix': target_format
                })
                if os.path.exists(output_dir):
                    for f in os.listdir(output_dir):
                        file_path = os.path.join(output_dir, f)
                        if os.path.isfile(file_path):
                            converted_files.append({'name': f, 'path': file_path})
                if result.get('failed_files'):
                    for f in result['failed_files']:
                        failed_files.append(f.get('file', '未知'))
            except Exception as e:
                logger.error(f"文档转换失败: {e}")
                return {'status': 'error', 'message': f'文档转换失败: {str(e)}'}
        
        if converted_files:
            return {
                'status': 'success',
                'message': f'成功转换 {len(converted_files)} 个文件',
                'converted_files': converted_files,
                'failed_files': failed_files,
                'download_info': {
                    'type': 'multiple' if len(converted_files) > 1 else 'single',
                    'files': [f['name'] for f in converted_files]
                }
            }
        return {'status': 'error', 'message': '所有文件转换失败'}
        
    finally:
        pass


def handle_rename(params: Dict[str, Any]) -> Dict[str, Any]:
    """文件批量重命名"""
    files = params.get('files', [])
    if not files:
        return {'status': 'error', 'message': '请上传文件'}
    
    input_dir = tempfile.mkdtemp(prefix='rename_input_')
    output_dir = tempfile.mkdtemp(prefix='rename_output_')
    
    try:
        file_times = {}
        for file_info in files:
            src_path = file_info['path']
            file_name = file_info['name']
            dst_path = os.path.join(input_dir, file_name)
            shutil.copy2(src_path, dst_path)
            file_times[file_name] = os.path.getmtime(src_path)
        
        result = OsOperation.file_rename(
            data_path=params.get('data_path', ''),
            data_sheet_name=params.get('data_sheet_name', 'Sheet1'),
            data_key=params.get('data_key', ''),
            old_dir=input_dir,
            middle_dir=input_dir,
            new_dir=output_dir,
            suffix=params.get('suffix', ''),
            pattern=params.get('pattern', ''),
            repl=params.get('repl', ''),
            count=int(params.get('count', 0)),
            additional_key=params.get('additional_key', ''),
            deviation=int(params.get('deviation', 0)),
            preview_mode=params.get('preview_mode', False),
            file_times=file_times
        )
        
        renamed_files = []
        if os.path.exists(output_dir):
            for f in os.listdir(output_dir):
                file_path = os.path.join(output_dir, f)
                if os.path.isfile(file_path):
                    renamed_files.append({'name': f, 'path': file_path})
        
        response = {
            'status': result.get('status', 'success'),
            'message': result.get('message', f'成功重命名 {len(renamed_files)} 个文件'),
            'renamed_files': renamed_files,
            'download_info': {
                'type': 'multiple' if len(renamed_files) > 1 else 'single',
                'files': [f['name'] for f in renamed_files]
            }
        }
        if params.get('preview_mode'):
            response['preview'] = result.get('preview', [])
        return response
        
    except Exception as e:
        logger.error(f"重命名失败: {e}", exc_info=True)
        return {'status': 'error', 'message': str(e)}


def handle_merge(params: Dict[str, Any]) -> Dict[str, Any]:
    """数据拼接 (pd.merge)"""
    files = params.get('files', [])
    if len(files) < 2:
        return {'status': 'error', 'message': '请上传至少两个文件'}
    
    temp_dir = tempfile.mkdtemp(prefix='merge_')
    
    try:
        template_path = None
        data_path = None
        for i, file_info in enumerate(files):
            src_path = file_info['path']
            dst_path = os.path.join(temp_dir, file_info['name'])
            shutil.copy2(src_path, dst_path)
            if i == 0:
                template_path = dst_path
            elif i == 1:
                data_path = dst_path
        
        template_df = pd.read_excel(template_path, sheet_name=params.get('input_template_sheet_name', 'Sheet1'))
        data_df = pd.read_excel(data_path, sheet_name=params.get('input_data_sheet_name', 'Sheet1'))
        
        data_key = params.get('data_key', 'id')
        how = params.get('how', 'inner')
        
        if data_key not in template_df.columns:
            return {'status': 'error', 'message': f'模板文件中没有主键列: {data_key}'}
        if data_key not in data_df.columns:
            return {'status': 'error', 'message': f'数据文件中没有主键列: {data_key}'}
        
        merged_df = DataOperation.key_merge(template_df, data_df, on=data_key, how=how)
        
        output_dir = tempfile.mkdtemp(prefix='merge_output_')
        save_name = params.get('save_name', 'merged_result')
        output_path = os.path.join(output_dir, f"{save_name}.xlsx")
        DataOperation.data_pd_write(output_path, params.get('save_sheet_name', 'Sheet1'), merged_df)
        
        return {
            'status': 'success',
            'message': f'数据合并完成，共 {len(merged_df)} 行',
            'output_file': {'name': os.path.basename(output_path), 'path': output_path},
            'download_info': {'type': 'single', 'files': [os.path.basename(output_path)]}
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def handle_generate(params: Dict[str, Any]) -> Dict[str, Any]:
    """模板批量生成"""
    files = params.get('files', [])
    if len(files) < 2:
        return {'status': 'error', 'message': '请上传模板文件和数据文件'}
    
    work_dir = tempfile.mkdtemp(prefix='generate_')
    output_dir = tempfile.mkdtemp(prefix='generate_output_')
    
    try:
        template_file = None
        data_file = None
        for file_info in files:
            file_name = file_info['name'].lower()
            if file_name.endswith(('.docx', '.doc', '.xlsx', '.xls')):
                if not template_file or '模板' in file_name:
                    template_file = file_info['path']
                else:
                    data_file = file_info['path']
            elif file_name.endswith(('.xlsx', '.xls', '.csv')):
                data_file = file_info['path']
        
        if not template_file or not data_file:
            template_file = files[0]['path']
            data_file = files[1]['path']
        
        temp_template = os.path.join(work_dir, os.path.basename(template_file))
        temp_data = os.path.join(work_dir, os.path.basename(data_file))
        shutil.copy2(template_file, temp_template)
        shutil.copy2(data_file, temp_data)
        
        data_key = params.get('data_key', '姓名')
        mode = params.get('mode', 'mixed')
        reserved_rows = int(params.get('reserved_rows', 1))
        insert_row = int(params.get('insert_row', 1))
        insert_col = int(params.get('insert_col', 1))
        preview_mode = params.get('preview_mode', False)
        
        file_ext = os.path.splitext(template_file)[1].lower()
        
        if file_ext in ['.xlsx', '.xls']:
            result = TemplateEngine.process_data_xlsx(
                input_template=temp_template,
                input_template_sheet_name=params.get('input_template_sheet_name', 'Sheet1'),
                input_data=temp_data,
                input_data_sheet_name=params.get('input_data_sheet_name', 'Sheet1'),
                output_dir=output_dir,
                data_key=data_key,
                insert_row=insert_row,
                insert_col=insert_col,
                reserved_rows=reserved_rows,
                mode=mode,
                preview_mode=preview_mode
            )
        else:
            result = TemplateEngine.process_data_docx(
                input_template=temp_template,
                input_data=temp_data,
                input_data_sheet_name=params.get('input_data_sheet_name', 'Sheet1'),
                output_dir=output_dir,
                data_key=data_key,
                reserved_rows=reserved_rows,
                mode=mode,
                preview_mode=preview_mode
            )
        
        generated_files = []
        if os.path.exists(output_dir):
            for f in os.listdir(output_dir):
                file_path = os.path.join(output_dir, f)
                if os.path.isfile(file_path):
                    generated_files.append({'name': f, 'path': file_path})
        
        response = {
            'status': result.get('status', 'success'),
            'message': result.get('message', f'成功生成 {len(generated_files)} 个文件'),
            'generated_files': generated_files,
            'download_info': {
                'type': 'multiple' if len(generated_files) > 1 else 'single',
                'files': [f['name'] for f in generated_files]
            }
        }
        if preview_mode:
            response['preview'] = result.get('preview', [])
        return response
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def handle_invoice_extract(params: Dict[str, Any]) -> Dict[str, Any]:
    """发票信息提取"""
    files = params.get('files', [])
    if not files:
        return {'status': 'error', 'message': '请上传发票文件'}
    
    version = params.get('version', 'basic')
    
    work_dir = tempfile.mkdtemp(prefix='invoice_')
    docx_dir = os.path.join(work_dir, 'docx_files')
    output_dir = os.path.join(work_dir, 'output')
    os.makedirs(docx_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        pdf_files = [f for f in files if f['name'].lower().endswith('.pdf')]
        docx_files = [f for f in files if f['name'].lower().endswith('.docx')]
        
        all_docx_files = []
        for docx_info in docx_files:
            all_docx_files.append({'path': docx_info['path'], 'name': docx_info['name'], 'original': docx_info['name']})
        
        converted_count = 0
        if pdf_files:
            convert_tool = params.get('libreoffice_path', r"D:\Program Files\libreoffice\program\soffice.exe")
            for pdf_info in pdf_files:
                pdf_name = pdf_info['name']
                docx_name = pdf_name.replace('.pdf', '.docx')
                docx_path = os.path.join(docx_dir, docx_name)
                try:
                    success = MutualConver._convert_with_libreoffice_fast(pdf_info['path'], docx_path, convert_tool, 'docx')
                    if success and os.path.exists(docx_path):
                        converted_count += 1
                        all_docx_files.append({'path': docx_path, 'name': docx_name, 'original': pdf_name})
                except Exception as e:
                    logger.error(f"PDF转DOCX失败: {e}")
        
        if not all_docx_files:
            return {'status': 'error', 'message': '没有可处理的DOCX文件'}
        
        extracted_results = []
        success_count = 0
        total_files = len(all_docx_files)
        
        for file_info in all_docx_files:
            try:
                if version == 'complete':
                    data = InvoiceExtractionServiceComplete.extract_invoice_from_xml(file_info['path'])
                else:
                    data = InvoiceExtractionService.extract_invoice_from_xml(file_info['path'])
                
                if version == 'basic':
                    core_fields = ['invoice_no', 'invoice_date', 'buyer_name', 'buyer_tax_id', 
                                  'total_amount', 'total_tax', 'tax_rate']
                    is_success = all(field in data and data[field] for field in core_fields)
                    accuracy = 100 if is_success else 0
                else:
                    accuracy = data.get('accuracy', 0)
                    is_success = accuracy >= 98
                
                if is_success:
                    success_count += 1
                
                extracted_results.append({
                    'file': file_info['name'],
                    'original_file': file_info.get('original', file_info['name']),
                    'status': 'success',
                    'data': data,
                    'accuracy': accuracy,
                    'success': is_success
                })
            except Exception as e:
                extracted_results.append({
                    'file': file_info['name'],
                    'original_file': file_info.get('original', file_info['name']),
                    'status': 'error',
                    'message': str(e),
                    'success': False
                })
        
        overall_accuracy = (success_count / total_files) * 100 if total_files > 0 else 0
        
        if success_count == 0:
            return {'status': 'error', 'message': '所有发票提取失败'}
        
        summary_data = []
        for result in extracted_results:
            if result['status'] == 'success':
                summary_data.append({'文件名': result['original_file'], **result['data']})
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_path = os.path.join(output_dir, f'发票汇总_{timestamp}.xlsx')
        df = pd.DataFrame(summary_data)
        df.to_excel(summary_path, index=False)
        
        return {
            'status': 'success',
            'message': f'成功提取 {success_count}/{total_files} 张发票',
            'summary': {
                'total_files': total_files,
                'success_count': success_count,
                'pdf_converted': converted_count,
                'overall_accuracy': round(overall_accuracy, 2)
            },
            'results': extracted_results,
            'output_file': {'name': os.path.basename(summary_path), 'path': summary_path},
            'download_info': {'type': 'single', 'files': [os.path.basename(summary_path)]}
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def handle_tax_reconcile(params: Dict[str, Any]) -> Dict[str, Any]:
    """财税智能对账"""
    files = params.get('files', [])
    if len(files) != 2:
        return {'status': 'error', 'message': '请上传两个文件'}
    
    output_dir = tempfile.mkdtemp(prefix='tax_reconcile_')
    
    try:
        tax_df = pd.read_excel(files[0]['path'])
        sap_df = pd.read_excel(files[1]['path'])
        
        required_cols = ['税额', '税率']
        for col in required_cols:
            if col not in tax_df.columns or col not in sap_df.columns:
                return {'status': 'error', 'message': f'文件缺少列: {col}'}
        
        tax_df['税额'] = pd.to_numeric(tax_df['税额'], errors='coerce').fillna(0)
        sap_df['税额'] = pd.to_numeric(sap_df['税额'], errors='coerce').fillna(0)
        
        match_mode = params.get('match_mode', 'standard')
        reconciler = OptimizedTaxAmountReconciliationService(tax_df, sap_df, get_algorithm_params(match_mode))
        result = reconciler.reconcile_all()
        
        match_rate = result['summary'].get('match_rate', 0)
        need_refund = match_rate < 80
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f'税务对账结果_{timestamp}.xlsx')
        reconciler.export_to_excel(output_path)
        
        return {
            'status': 'success',
            'message': f'对账完成，匹配率: {match_rate:.2f}%',
            'summary': result['summary'],
            'match_rate': round(match_rate, 2),
            'need_refund': need_refund,
            'refund_reason': f'匹配率{match_rate:.2f}%低于80%保证' if need_refund else None,
            'output_file': {'name': os.path.basename(output_path), 'path': output_path},
            'download_info': {'type': 'single', 'files': [os.path.basename(output_path)]}
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}