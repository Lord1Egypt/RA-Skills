#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF OCR处理脚本
支持两种OCR引擎：
1. 硅基流动大模型API（云端）
2. RapidOCR（本地，无需API）
支持自动安装缺失的依赖
"""

import os
import sys
import base64
import requests
import subprocess
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def install_dependency(package):
    """自动安装缺失的依赖"""
    print(f"正在安装依赖: {package}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"依赖 {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖 {package} 安装失败: {e}")
        return False


class RapidOCREngine:
    """RapidOCR本地OCR引擎"""
    
    def __init__(self):
        self.ocr = None
        self._init_engine()
    
    def _init_engine(self):
        """初始化RapidOCR引擎"""
        try:
            from rapidocr_onnxruntime import RapidOCR
            self.ocr = RapidOCR()
        except ImportError:
            print("RapidOCR依赖未安装，正在尝试自动安装...")
            if install_dependency("rapidocr_onnxruntime"):
                try:
                    from rapidocr_onnxruntime import RapidOCR
                    self.ocr = RapidOCR()
                except ImportError:
                    raise Exception("RapidOCR依赖安装失败，请手动安装: pip install rapidocr_onnxruntime")
            else:
                raise Exception("RapidOCR依赖安装失败，请手动安装: pip install rapidocr_onnxruntime")
    
    def recognize(self, image_path: str) -> str:
        """识别单张图片"""
        if self.ocr is None:
            raise Exception("RapidOCR引擎未初始化")
        
        result, _ = self.ocr(image_path)
        
        if not result:
            return ""
        
        # 提取文本
        texts = []
        for line in result:
            if len(line) >= 2:
                texts.append(line[1])
        
        return "\n".join(texts)


class SiliconFlowOCREngine:
    """硅基流动API OCR引擎"""
    
    def __init__(self, api_key: str = "", model: str = "deepseek-ai/DeepSeek-OCR"):
        self.api_key = api_key or os.getenv("SILICON_FLOW_API_KEY", "")
        self.model = model or os.getenv("SILICON_FLOW_OCR_MODEL", "deepseek-ai/DeepSeek-OCR")
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def recognize(self, image_base64: str, page_num: int = 1) -> str:
        """使用硅基流动大模型识别单张图片"""
        prompt = f"""请仔细识别这张图片中的所有文字内容。
这是第 {page_num} 页的内容。

要求：
1. 完整提取所有可见文字
2. 保持文字的顺序和结构
3. 识别中文和英文
4. 输出纯文本格式，不要添加任何额外说明

请直接输出识别的文字内容："""
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload, 
                timeout=120
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"【OCR识别失败: {str(e)}】"


class PDFOCRProcessor:
    """PDF OCR处理器 - 支持多种OCR引擎"""
    
    def __init__(self, engine: Optional[str] = None):
        """
        初始化PDF OCR处理器
        
        Args:
            engine: OCR引擎类型，可选值：
                - "rapid": 使用RapidOCR本地引擎（默认，无需API）
                - "siliconflow": 使用硅基流动API引擎
                - None: 从环境变量 OCR_ENGINE 读取，默认为 "rapid"
        """
        self.engine_type = engine or os.getenv("OCR_ENGINE", "rapid")
        self.rapid_engine: Optional[RapidOCREngine] = None
        self.siliconflow_engine: Optional[SiliconFlowOCREngine] = None
        
        # 初始化选定的引擎
        self._init_engine()
    
    def _init_engine(self):
        """初始化OCR引擎"""
        if self.engine_type == "rapid":
            try:
                self.rapid_engine = RapidOCREngine()
            except Exception as e:
                print(f"RapidOCR初始化失败: {e}")
                print("将尝试使用硅基流动API引擎...")
                self.engine_type = "siliconflow"
                self.siliconflow_engine = SiliconFlowOCREngine()
        elif self.engine_type == "siliconflow":
            self.siliconflow_engine = SiliconFlowOCREngine()
        else:
            raise ValueError(f"不支持的OCR引擎类型: {self.engine_type}")
    
    def pdf_to_images(self, pdf_path: str, output_dir: Optional[str] = None) -> List[str]:
        """
        将PDF转换为图片列表
        
        Args:
            pdf_path: PDF文件路径
            output_dir: 图片输出目录，如果为None则返回base64编码列表
        
        Returns:
            如果output_dir为None，返回base64编码列表；否则返回图片文件路径列表
        """
        try:
            import fitz  # PyMuPDF
            from PIL import Image
            import io
            
            doc = fitz.open(pdf_path)
            images = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # 将PDF页面转换为图片
                zoom = 2  # 放大倍数
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                
                # 转换为PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                if output_dir:
                    # 保存到文件
                    os.makedirs(output_dir, exist_ok=True)
                    img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
                    img.save(img_path, "PNG")
                    images.append(img_path)
                else:
                    # 转换为base64
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode()
                    images.append(img_base64)
            
            doc.close()
            return images
            
        except ImportError:
            print("PDF处理依赖未安装，正在尝试自动安装...")
            if install_dependency("pymupdf") and install_dependency("pillow"):
                try:
                    import fitz  # PyMuPDF
                    from PIL import Image
                    import io
                    
                    doc = fitz.open(pdf_path)
                    images = []
                    
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        
                        # 将PDF页面转换为图片
                        zoom = 2  # 放大倍数
                        mat = fitz.Matrix(zoom, zoom)
                        pix = page.get_pixmap(matrix=mat)
                        
                        # 转换为PIL Image
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        
                        if output_dir:
                            # 保存到文件
                            os.makedirs(output_dir, exist_ok=True)
                            img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
                            img.save(img_path, "PNG")
                            images.append(img_path)
                        else:
                            # 转换为base64
                            buffered = io.BytesIO()
                            img.save(buffered, format="PNG")
                            img_base64 = base64.b64encode(buffered.getvalue()).decode()
                            images.append(img_base64)
                    
                    doc.close()
                    return images
                except ImportError:
                    raise Exception("PDF处理依赖安装失败，请手动安装: pip install pymupdf pillow")
            else:
                raise Exception("PDF处理依赖安装失败，请手动安装: pip install pymupdf pillow")
        except Exception as e:
            raise Exception(f"PDF转图片失败: {str(e)}")
    
    def ocr_pdf(self, pdf_path: str, save_images: bool = False) -> Dict[str, Any]:
        """
        OCR识别整个PDF
        
        Args:
            pdf_path: PDF文件路径
            save_images: 是否保存中间图片文件（RapidOCR模式下）
        
        Returns:
            包含text和page_count的字典
        """
        result = {
            "text": "",
            "page_count": 0,
            "engine": self.engine_type
        }
        
        try:
            if self.engine_type == "rapid":
                # 使用RapidOCR本地识别
                result = self._ocr_with_rapid(pdf_path, save_images)
            else:
                # 使用硅基流动API识别
                result = self._ocr_with_siliconflow(pdf_path)
            
        except Exception as e:
            raise Exception(f"OCR识别失败: {str(e)}")
        
        return result
    
    def _ocr_with_rapid(self, pdf_path: str, save_images: bool = False) -> Dict[str, Any]:
        """使用RapidOCR识别PDF"""
        import tempfile
        import shutil
        
        # 创建临时目录存放图片
        if save_images:
            temp_dir = os.path.join(os.path.dirname(pdf_path), "pdf_images")
        else:
            temp_dir = tempfile.mkdtemp()
        
        try:
            # 转换PDF为图片
            image_paths = self.pdf_to_images(pdf_path, output_dir=temp_dir)
            
            text_parts = []
            for idx, img_path in enumerate(image_paths, 1):
                page_text = self.rapid_engine.recognize(img_path)
                text_parts.append(f"=== 第 {idx} 页 ===\n{page_text}")
            
            return {
                "text": "\n\n".join(text_parts),
                "page_count": len(image_paths),
                "engine": "rapid",
                "images_dir": temp_dir if save_images else None
            }
            
        finally:
            # 清理临时文件
            if not save_images and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def _ocr_with_siliconflow(self, pdf_path: str) -> Dict[str, Any]:
        """使用硅基流动API识别PDF"""
        images = self.pdf_to_images(pdf_path)
        
        text_parts = []
        for idx, img_base64 in enumerate(images, 1):
            page_text = self.siliconflow_engine.recognize(img_base64, idx)
            text_parts.append(f"=== 第 {idx} 页 ===\n{page_text}")
        
        return {
            "text": "\n\n".join(text_parts),
            "page_count": len(images),
            "engine": "siliconflow"
        }
    
    def ocr_image_file(self, image_path: str) -> Dict[str, Any]:
        """OCR识别单个图片文件"""
        result = {
            "text": "",
            "page_count": 1,
            "engine": self.engine_type
        }
        
        try:
            if self.engine_type == "rapid":
                result["text"] = self.rapid_engine.recognize(image_path)
            else:
                # 将图片转换为base64
                try:
                    from PIL import Image
                    import io
                except ImportError:
                    print("图片处理依赖未安装，正在尝试自动安装...")
                    if install_dependency("pillow"):
                        from PIL import Image
                        import io
                    else:
                        raise Exception("图片处理依赖安装失败，请手动安装: pip install pillow")
                
                img = Image.open(image_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                result["text"] = self.siliconflow_engine.recognize(img_base64, 1)
            
        except Exception as e:
            raise Exception(f"图片OCR识别失败: {str(e)}")
        
        return result


def process_pdf_ocr(pdf_path: str, engine: Optional[str] = None) -> Dict[str, Any]:
    """
    处理PDF OCR的主函数
    
    Args:
        pdf_path: PDF文件路径
        engine: OCR引擎类型，可选 "rapid" 或 "siliconflow"
    
    Returns:
        包含text、page_count和engine的字典
    """
    processor = PDFOCRProcessor(engine=engine)
    return processor.ocr_pdf(pdf_path)


if __name__ == "__main__":
    # 测试代码
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        engine = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        print("使用方法: python pdf_ocr_processor.py <pdf_file_path> [engine]")
        print("engine可选值: rapid (默认) | siliconflow")
        sys.exit(1)
    
    if not os.path.exists(pdf_path):
        print(f"文件不存在: {pdf_path}")
        sys.exit(1)
    
    try:
        result = process_pdf_ocr(pdf_path, engine=engine)
        print(f"OCR识别完成，共 {result['page_count']} 页")
        print(f"使用引擎: {result['engine']}")
        print("\n识别结果:")
        print(result['text'])
    except Exception as e:
        print(f"处理失败: {e}")
        sys.exit(1)
