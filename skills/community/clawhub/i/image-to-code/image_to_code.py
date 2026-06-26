#!/usr/bin/env python3
"""
图片转代码格式转换器
将图片中的文字、公式、图表转换为指定代码格式

格式规范:
- 文字行：$word->body("正文=内容=".$F);
- 公式：$word->formula("LaTeX 公式");
- 图片：![image]

OCR 引擎优先级:
1. 百度 OCR (高精度，95%+)
2. Tesseract (离线，70-80%)
"""

import cv2
import numpy as np
from pathlib import Path
import argparse
import sys
import re
from typing import List, Dict, Tuple, Optional
import requests
import base64


class ImageToCodeConverter:
    """图片转代码格式转换器"""
    
    def __init__(self, ocr_lang='ch', use_vision_ai=False, use_baidu_ocr=True):
        """
        初始化转换器
        
        Args:
            ocr_lang: OCR 语言 ('ch' 中文，'en' 英文)
            use_vision_ai: 是否使用视觉 AI 进行公式识别
            use_baidu_ocr: 是否使用百度 OCR（优先，高精度）
        """
        self.ocr_lang = ocr_lang
        self.use_vision_ai = use_vision_ai
        self.use_baidu_ocr = use_baidu_ocr
        self.baidu_api_key = None
        self.baidu_secret_key = None
        self.baidu_access_token = None
        
        # 百度 OCR 配置
        if self.use_baidu_ocr:
            self.baidu_api_key = "4LceeJ8wBDSqa3SqDHmgXuk1"
            self.baidu_secret_key = "nIulIWxqaUtY5XyfexSvP4OL8ZBk0krR"
            self._init_baidu_ocr()
        
        # 初始化 OCR 引擎 - 优先使用百度 OCR
        self.ocr = None
        self.use_tesseract = False
        
        if not self.use_baidu_ocr or not self.baidu_access_token:
            try:
                import pytesseract
                # 测试 Tesseract
                pytesseract.get_tesseract_version()
                self.use_tesseract = True
                print("✅ Tesseract OCR 初始化成功")
            except Exception as e:
                print(f"⚠️  Tesseract 不可用：{e}")
                try:
                    from paddleocr import PaddleOCR
                    self.ocr = PaddleOCR(lang=ocr_lang)
                    print("✅ PaddleOCR 初始化成功")
                except ImportError:
                    print("❌ 没有可用的 OCR 引擎")
        
        # 数学符号映射（用于公式检测）
        self.math_symbols = set('∑∫∂∇√∞≈≠≤≥±×÷∏∐∪∩∧∨¬∃∀∈∉⊂⊃⊆⊇⊕⊗⊙⊘⊖⊤⊥∠∟∥∦')
        self.math_letters = set('αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΞΠΣΦΨΩ')
        
        # 标题识别模式
        self.title_patterns = {
            1: [  # 一级标题模式
                r'^第.+章',  # 第一章、第 1 章
                r'^第.+部分',  # 第一部分
                r'^[一二三四五六七八九十]+、',  # 一、二、三、
            ],
            2: [  # 二级标题模式
                r'^第.+节',  # 第一节、第 1 节
                r'^[0-9]+\.[0-9]+(?!\.[0-9])',  # 1.1, 1.2 (但不匹配 1.1.1)
                r'^\([0-9]+\)',  # (1), (2)
                r'^[（][一二三四五六七八九十]+[）]',  # （一）、（二）
            ],
            3: [  # 三级标题模式
                r'^[0-9]+\.[0-9]+\.[0-9]+',  # 1.1.1
                r'^[0-9]+、',  # 1、2、3、
                r'^[一二三四五六七八九十]*[核算计算分析设计].*压力',  # 核算压力降等
                r'^.*压力降$',  # XX 压力降（如：管程压力降）
                r'^管程.*',  # 管程 XXX
                r'^壳程.*',  # 壳程 XXX
            ],
        }
    
    def _init_baidu_ocr(self):
        """初始化百度 OCR，获取 access_token"""
        if not self.baidu_api_key or not self.baidu_secret_key:
            return
        
        try:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": self.baidu_api_key,
                "client_secret": self.baidu_secret_key
            }
            
            response = requests.post(url, params=params, timeout=10)
            result = response.json()
            
            if "access_token" in result:
                self.baidu_access_token = result["access_token"]
                print("✅ 百度 OCR 初始化成功（高精度版）")
            else:
                print(f"⚠️  百度 OCR Token 获取失败：{result}")
                self.baidu_access_token = None
        except Exception as e:
            print(f"⚠️  百度 OCR 初始化失败：{e}")
            self.baidu_access_token = None
    
    def _ocr_with_baidu(self, image: np.ndarray) -> List[str]:
        """
        使用百度 OCR 识别图片
        
        Args:
            image: OpenCV 图像数组
            
        Returns:
            识别结果文本行列表
        """
        if not self.baidu_access_token:
            return []
        
        try:
            # 转换为 JPG 格式
            _, buffer = cv2.imencode('.jpg', image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # 调用百度 OCR API（高精度版）
            url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
            url += f"?access_token={self.baidu_access_token}"
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "image": img_base64,
                "detect_direction": "true",
                "detect_language": "true"
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=30)
            result = response.json()
            
            if "error_code" in result:
                print(f"⚠️  百度 OCR 识别错误：{result.get('error_msg', '未知错误')}")
                return []
            
            # 提取识别结果
            lines = []
            if "words_result" in result:
                for item in result["words_result"]:
                    words = item.get("words", "").strip()
                    if words:
                        lines.append(words)
            
            return lines
            
        except Exception as e:
            print(f"⚠️  百度 OCR 识别失败：{e}")
            return []
    
    def extract_title_text(self, text: str, level: int) -> str:
        """
        提取标题中的纯文本内容（去掉编号前缀）
        
        Args:
            text: 原始标题文字
            level: 标题级别
            
        Returns:
            去掉编号的标题文本
        """
        text = text.strip()
        
        if level == 1:
            patterns = [
                r'^第.+章\s*',  # 第 X 章
                r'^第.+部分\s*',  # 第 X 部分
                r'^[一二三四五六七八九十]+、\s*',  # 一、
            ]
            for pattern in patterns:
                match = re.match(pattern, text)
                if match:
                    return text[match.end():].strip()
        
        elif level == 2:
            patterns = [
                r'^第.+节\s*',  # 第 X 节
                r'^[0-9]+\.[0-9]+(?!\.[0-9])\s*',  # 1.1
                r'^\([0-9]+\)\s*',  # (1) (2)
                r'^[（][一二三四五六七八九十]+[）]\s*',  # （一）（二）
            ]
            for pattern in patterns:
                match = re.match(pattern, text)
                if match:
                    return text[match.end():].strip()
        
        elif level == 3:
            patterns = [
                r'^[0-9]+\.[0-9]+\.[0-9]+\s*',  # 1.1.1
                r'^[0-9]+、\s*',  # 1、
                r'^①\s*',  # ①
                r'^②\s*',  # ②
                r'^③\s*',  # ③
            ]
            for pattern in patterns:
                match = re.match(pattern, text)
                if match:
                    return text[match.end():].strip()
        
        return text
    
    def detect_title_level(self, text: str) -> Optional[int]:
        """
        检测标题级别
        
        Args:
            text: OCR 识别的文字
            
        Returns:
            标题级别 (1/2/3) 或 None（不是标题）
        """
        text = text.strip()
        
        # 长度检查：太短的不是标题
        if len(text) < 3:
            return None
        
        # 内容检查：包含连接词的不是标题
        if any(word in text for word in ['所以', '因此', '则', '故', '即']):
            return None
        
        # 先检查是否有 (1) (2) 等编号 - 这些是 2 级标题
        if re.match(r'^\([0-9]+\)', text):
            return 2
        
        # 按顺序检查：3 级 -> 2 级 -> 1 级（更具体的先匹配）
        for level in [3, 2, 1]:
            patterns = self.title_patterns[level]
            for pattern in patterns:
                if re.search(pattern, text):
                    return level
        
        return None
    
    def detect_content_type(self, text: str, image_region: Optional[np.ndarray] = None) -> str:
        """
        检测内容类型
        
        Args:
            text: OCR 识别的文字
            image_region: 图像区域（可选）
            
        Returns:
            'text' | 'formula' | 'image' | 'empty'
        """
        if not text or len(text.strip()) == 0:
            return 'empty'
        
        text_stripped = text.strip()
        
        # 检测公式特征
        math_symbol_count = sum(1 for c in text_stripped if c in self.math_symbols)
        math_letter_count = sum(1 for c in text_stripped if c in self.math_letters)
        
        # 检测数学表达式特征
        has_equation = '=' in text_stripped
        has_math_ops = any(op in text_stripped for op in ['+', '-', '×', '÷', '^', '_', '√', 'Σ', 'Δ', '∑'])
        has_greek = any(c in text_stripped for c in 'αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΞΠΣΦΨΩ')
        has_subscript = '_' in text_stripped
        has_parentheses = '(' in text_stripped and ')' in text_stripped
        
        # 检测是否包含"其中"等说明词
        has_explanation = any(word in text_stripped for word in ['其中', '式中', '公式', '计算'])
        
        # 公式判断逻辑
        if math_symbol_count >= 1 or math_letter_count >= 2:
            return 'formula'
        
        if has_greek:
            return 'formula'
        
        if has_equation and (has_math_ops or has_parentheses) and not has_explanation:
            return 'formula'
        
        if has_math_ops and has_parentheses and len(text_stripped) > 5:
            return 'formula'
        
        # 图片判断（需要图像分析）
        if image_region is not None:
            if self._is_image_region(image_region, text_stripped):
                return 'image'
        
        # 默认为文字
        return 'text'
    
    def _is_image_region(self, image_region: np.ndarray, text: str) -> bool:
        """
        判断是否为图片区域
        
        基于图像特征：
        - 颜色丰富度
        - 边缘复杂度
        - 文字密度
        """
        if image_region is None or image_region.size == 0:
            return False
        
        # 如果文字很少但区域很大，可能是图片
        height, width = image_region.shape[:2]
        area = height * width
        text_density = len(text) / area if area > 0 else 0
        
        # 文字密度极低，可能是图表
        if text_density < 0.001 and area > 10000:
            return True
        
        return False
    
    def text_to_latex(self, text: str) -> str:
        """
        将识别的文字转换为 LaTeX 格式（带后处理优化）
        
        Args:
            text: OCR 识别的原始文字
            
        Returns:
            LaTeX 格式的公式
        """
        import re
        
        latex = text
        
        # ========== 第一阶段：特殊识别优化 ==========
        
        # 1. 处理 F,NP → F_t×N_p（识别错误的乘号）
        latex = re.sub(r'F,NP', r'F_t\\times N_p', latex)
        latex = re.sub(r'F,N_', r'F_t\\times N_', latex)
        
        # 2. 处理常见 OCR 错误
        latex = re.sub(r'R41', r'Re', latex)  # R41 → Re（雷诺数）
        latex = re.sub(r'30u', r'3u^2', latex)  # 30u → 3u²
        latex = re.sub(r'EAp', r'\\Sigma\\Delta p', latex)  # EAp → ΣΔp
        latex = re.sub(r'd:P', r'd\\cdot u\\cdot\\rho', latex)  # d:P → d·u·ρ
        
        # 3. 处理乘号后数字（不要转下标）
        # ×0.023 → \times 0.023（保持原样）
        latex = re.sub(r'×([0-9.]+)', r'\\times\1', latex)
        
        # ========== 第二阶段：智能下标优化 ==========
        
        # 只处理特定变量的下标（p1, t2, N1 等）
        # 不处理数值前的字母（×0.023 不应该变成 \times_0.023）
        
        # 规则：字母 + 单个数字（且后面不是小数点或更多数字）
        # p1 → p_1, t2 → t_2, N1 → N_1
        latex = re.sub(r'([pPtTnN])([0-9])(?![0-9.])', r'\1_\2', latex)
        
        # 特殊处理：△p1 → △p_1
        latex = re.sub(r'△p([0-9])', r'△p_\1', latex)
        latex = re.sub(r'△P([0-9])', r'△p_\1', latex)
        
        # 处理 Re 的下标
        latex = re.sub(r'Re([0-9])', r'Re_\1', latex)
        
        # ========== 第三阶段：符号替换 ==========
        
        # 希腊字母和数学符号（不处理△，保持原样）
        replacements = {
            '²': '^2',
            '³': '^3',
            '∑': r'\sum',
            '∫': r'\int',
            '∂': r'\partial',
            '∇': r'\nabla',
            '√': r'\sqrt',
            '∞': r'\infty',
            '≈': r'\approx',
            '≠': r'\neq',
            '≤': r'\leq',
            '≥': r'\geq',
            '±': r'\pm',
            '×': r'\times',
            '÷': r'\div',
            'π': r'\pi',
            'α': r'\alpha',
            'β': r'\beta',
            'γ': r'\gamma',
            'δ': r'\delta',
            'ε': r'\epsilon',
            'θ': r'\theta',
            'λ': r'\lambda',
            'μ': r'\mu',
            'σ': r'\sigma',
            'φ': r'\phi',
            'ψ': r'\psi',
            'ω': r'\omega',
        }
        
        for original, latex_char in replacements.items():
            latex = latex.replace(original, latex_char)
        
        # ========== 第四阶段：最终优化 ==========
        
        # 清理多余空格
        latex = re.sub(r'\s+', ' ', latex).strip()
        
        return latex
    
    def convert_line(self, text: str, content_type: str, image_region: Optional[np.ndarray] = None) -> str:
        """
        转换单行内容为代码格式
        
        Args:
            text: 原始文字
            content_type: 内容类型
            image_region: 图像区域
            
        Returns:
            代码格式字符串
        """
        if content_type == 'empty':
            return ''
        
        text = text.strip()
        
        # 检查是否为标题
        if content_type == 'text':
            title_level = self.detect_title_level(text)
            if title_level:
                # 提取纯标题文本（去掉编号）
                title_text = self.extract_title_text(text, title_level)
                # 转义双引号
                escaped = title_text.replace('"', '\\"')
                return f'$word->title{title_level}("{escaped}");'
        
        if content_type == 'text':
            # 转义双引号
            escaped = text.replace('"', '\\"')
            # 优化文字中的下标（F1 → F_t, Np → N_p）
            escaped = self._optimize_text_subscript(escaped)
            return f'$word->body("{escaped}");'
        
        elif content_type == 'formula':
            # 转换为 LaTeX
            latex = self.text_to_latex(text)
            return f'$word->formula("{latex}");'
        
        elif content_type == 'image':
            return '![image]'
        
        return ''
    
    def _optimize_text_subscript(self, text: str) -> str:
        """
        优化文字中的下标格式
        
        Args:
            text: 原始文字
            
        Returns:
            优化后的文字
        """
        import re
        
        # F1 → F_t (根据上下文)
        text = re.sub(r'F1([=,])', r'F_t\1', text)
        
        # N, → N_p（OCR 识别错误，实际是 N_p）
        text = re.sub(r'N,([0-9])', r'N_p=\1', text)
        text = re.sub(r'N,([=])', r'N_p\1', text)
        text = re.sub(r'N,([。])', r'N_p\1', text)
        
        return text
    
    def process_image(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        处理整张图片
        
        Args:
            image_path: 输入图片路径
            output_path: 输出文件路径（可选）
            
        Returns:
            转换后的代码文本
        """
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图片：{image_path}")
        
        print(f"📷 处理图片：{image_path}")
        print(f"   尺寸：{image.shape[1]}x{image.shape[0]}")
        
        # OCR 识别 - 优先使用百度 OCR
        if self.baidu_access_token:
            # 使用百度 OCR（高精度）
            print("🔍 使用百度 OCR 执行 OCR 识别（高精度版）...")
            return self._process_with_baidu(image, output_path)
        elif self.use_tesseract:
            # 使用 Tesseract
            print("🔍 使用 Tesseract 执行 OCR 识别...")
            return self._process_with_tesseract(image, output_path)
        elif self.ocr is not None:
            # 使用 PaddleOCR
            print("🔍 使用 PaddleOCR 执行 OCR 识别...")
            return self._process_with_paddleocr(image, output_path)
        else:
            print("❌ OCR 引擎未初始化")
            return ""
    
    def _process_with_tesseract(self, image: np.ndarray, output_path: Optional[str] = None) -> str:
        """使用 Tesseract 处理图片"""
        import pytesseract
        
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 简单二值化
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # 执行 OCR
        config = f'--oem 3 --psm 6 -l chi_sim+eng'
        ocr_data = pytesseract.image_to_data(binary, config=config, output_type=pytesseract.Output.DICT)
        
        # 处理结果
        output_lines = []
        current_line = ""
        current_y = -1
        
        n_boxes = len(ocr_data['text'])
        for i in range(n_boxes):
            text = ocr_data['text'][i].strip()
            if not text:
                continue
            
            y = ocr_data['top'][i]
            conf = ocr_data['conf'][i]
            
            # 过滤低置信度
            if conf < 30:
                continue
            
            # 检测新行
            if current_y == -1 or abs(y - current_y) > 10:
                if current_line:
                    # 处理上一行 - 移除中文字符间的空格
                    current_line = self._clean_chinese_text(current_line)
                    
                    # 处理上一行
                    content_type = self.detect_content_type(current_line)
                    code_line = self.convert_line(current_line, content_type)
                    if code_line:
                        output_lines.append(code_line)
                        preview = current_line[:30] + '...' if len(current_line) > 30 else current_line
                        title_level = self.detect_title_level(current_line)
                        if title_level:
                            print(f"   ✓ [标题 L{title_level}] {preview}")
                        else:
                            print(f"   ✓ [{content_type}] {preview}")
                
                current_line = text
                current_y = y
            else:
                current_line += " " + text
        
        # 处理最后一行
        if current_line:
            current_line = self._clean_chinese_text(current_line)
            
            content_type = self.detect_content_type(current_line)
            code_line = self.convert_line(current_line, content_type)
            if code_line:
                output_lines.append(code_line)
                preview = current_line[:30] + '...' if len(current_line) > 30 else current_line
                title_level = self.detect_title_level(current_line)
                if title_level:
                    print(f"   ✓ [标题 L{title_level}] {preview}")
                else:
                    print(f"   ✓ [{content_type}] {preview}")
        
        # 生成输出
        output = '\n'.join(output_lines)
        
        # 保存文件
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"💾 已保存到：{output_path}")
        
        total = len(output_lines)
        print(f"✅ 完成！共处理 {total} 行")
        
        return output
    
    def _process_with_baidu(self, image: np.ndarray, output_path: Optional[str] = None) -> str:
        """
        使用百度 OCR 处理图片
        
        Args:
            image: OpenCV 图像数组
            output_path: 输出文件路径（可选）
            
        Returns:
            转换后的代码文本
        """
        # 使用百度 OCR 识别
        lines = self._ocr_with_baidu(image)
        
        if not lines:
            print("❌ 百度 OCR 未识别到文字")
            return ""
        
        # 处理识别结果
        output_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测内容类型
            content_type = self.detect_content_type(line)
            
            # 转换为代码格式
            code_line = self.convert_line(line, content_type)
            if code_line:
                output_lines.append(code_line)
                preview = line[:30] + '...' if len(line) > 30 else line
                title_level = self.detect_title_level(line)
                if title_level:
                    print(f"   ✓ [标题 L{title_level}] {preview}")
                else:
                    print(f"   ✓ [{content_type}] {preview}")
        
        # 生成输出
        output = '\n'.join(output_lines)
        
        # 保存文件
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"💾 已保存到：{output_path}")
        
        total = len(output_lines)
        print(f"✅ 完成！共处理 {total} 行")
        
        return output
    
    def _clean_chinese_text(self, text: str) -> str:
        """
        清理中文文本 - 移除中文字符间的空格
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        import re
        # 移除中文字符之间的空格
        # 匹配：中文 + 空格 + 中文
        text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)
        # 移除多余空格（保留英文单词间的空格）
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _process_with_paddleocr(self, image: np.ndarray, output_path: Optional[str] = None) -> str:
        """使用 PaddleOCR 处理图片"""
        # PaddleOCR 识别
        print("🔍 执行 OCR 识别...")
        ocr_result = self.ocr.predict(image)
        
        # 处理结果
        output_lines = []
        total_lines = 0
        
        if ocr_result and ocr_result[0]:
            # 按 Y 坐标排序（从上到下）
            lines_with_y = []
            for line in ocr_result[0]:
                bbox = line[0]
                text = line[1][0]
                confidence = line[1][1]
                
                # 计算中心 Y 坐标
                y_coords = [p[1] for p in bbox]
                y_center = sum(y_coords) / len(y_coords)
                
                lines_with_y.append({
                    'y': y_center,
                    'bbox': bbox,
                    'text': text,
                    'confidence': confidence
                })
            
            # 按 Y 坐标排序
            lines_with_y.sort(key=lambda x: x['y'])
            
            # 逐行处理
            for line_data in lines_with_y:
                bbox = line_data['bbox']
                text = line_data['text']
                
                # 提取区域图像
                x_coords = [p[0] for p in bbox]
                y_coords = [p[1] for p in bbox]
                x_min, x_max = int(min(x_coords)), int(max(x_coords))
                y_min, y_max = int(min(y_coords)), int(max(y_coords))
                
                region = image[y_min:y_max, x_min:x_max]
                
                # 检测内容类型
                content_type = self.detect_content_type(text, region)
                
                # 转换为代码格式
                code_line = self.convert_line(text, content_type, region)
                
                if code_line:
                    output_lines.append(code_line)
                    total_lines += 1
                    
                    # 打印进度
                    preview = text[:30] + '...' if len(text) > 30 else text
                    
                    # 检查是否为标题
                    title_level = self.detect_title_level(text)
                    if title_level:
                        print(f"   ✓ [标题 L{title_level}] {preview}")
                    else:
                        print(f"   ✓ [{content_type}] {preview}")
        
        # 生成输出
        output = '\n'.join(output_lines)
        
        # 保存文件
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"💾 已保存到：{output_path}")
        
        print(f"✅ 完成！共处理 {total_lines} 行")
        
        return output


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='图片转代码格式转换器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python image_to_code.py input.png
  python image_to_code.py input.png output.txt
  python image_to_code.py *.png --output-dir ./output
        '''
    )
    
    parser.add_argument('image', help='输入图片路径')
    parser.add_argument('output', nargs='?', help='输出文件路径（可选）')
    parser.add_argument('--lang', '-l', default='ch', choices=['ch', 'en'],
                       help='OCR 语言 (默认：ch)')
    parser.add_argument('--vision-ai', '-v', action='store_true',
                       help='使用视觉 AI 进行公式识别')
    parser.add_argument('--output-dir', '-d', help='批量处理输出目录')
    
    args = parser.parse_args()
    
    # 创建转换器
    converter = ImageToCodeConverter(
        ocr_lang=args.lang,
        use_vision_ai=args.vision_ai
    )
    
    # 处理单个文件
    if args.output:
        result = converter.process_image(args.image, args.output)
    else:
        result = converter.process_image(args.image)
        if result:
            print("\n" + "="*60)
            print("输出结果:")
            print("="*60)
            print(result)


if __name__ == '__main__':
    main()
