import os
import cv2
import json
import numpy as np
from typing import Optional, List, Tuple, Dict, Union
from PIL import Image
from enum import Enum

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'games')
TEMPLATE_BASE_WIDTH = 1920
TEMPLATE_BASE_HEIGHT = 1080

_button_configs: Dict[str, Dict] = {}

def _load_button_config(game_name: str) -> Dict:
    """
    加载按钮配置文件
    
    Args:
        game_name: 游戏名称
    
    Returns:
        按钮配置字典
    """
    if game_name in _button_configs:
        return _button_configs[game_name]
    
    config_path = os.path.join(ASSETS_DIR, game_name, 'assets', 'buttons.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            _button_configs[game_name] = json.load(f)
    else:
        _button_configs[game_name] = {}
    
    return _button_configs[game_name]

def _parse_roi_expr(expr: Union[int, str], base_value: int) -> int:
    """
    解析 ROI 表达式
    
    Args:
        expr: 表达式 (如 "width/4", "height*3/4", 或整数)
        base_value: 基础值 (width 或 height)
    
    Returns:
        计算结果
    """
    if isinstance(expr, int):
        return expr
    
    if isinstance(expr, str):
        expr = expr.replace('width', 'base').replace('height', 'base')
        try:
            return int(eval(expr, {'base': base_value}))
        except:
            return 0
    
    return 0

def _get_button_roi(config: Dict, img_width: int, img_height: int) -> Optional[Tuple[int, int, int, int]]:
    """
    获取按钮的 ROI 区域
    
    Args:
        config: 按钮配置
        img_width: 图像宽度
        img_height: 图像高度
    
    Returns:
        (x, y, w, h) 或 None
    """
    if 'roi' not in config:
        return None
    
    roi = config['roi']
    x = _parse_roi_expr(roi[0], img_width)
    y = _parse_roi_expr(roi[1], img_height)
    w = _parse_roi_expr(roi[2], img_width)
    h = _parse_roi_expr(roi[3], img_height)
    
    return (x, y, w, h)

class RecognitionType(Enum):
    NONE = 0
    TEMPLATE_MATCH = 1
    COLOR_MATCH = 2
    OCR_MATCH = 3
    OCR = 4
    COLOR_RANGE_AND_OCR = 5

def pil_to_cv2(img: Image.Image) -> np.ndarray:
    """PIL Image 转 OpenCV BGR 格式"""
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(img: np.ndarray) -> Image.Image:
    """OpenCV BGR 格式转 PIL Image"""
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def resize_template(template: np.ndarray, scale: float) -> np.ndarray:
    """
    缩放模板图片
    
    Args:
        template: 原始模板图片
        scale: 缩放比例
    
    Returns:
        缩放后的模板图片
    """
    if scale == 1.0:
        return template
    
    new_width = int(template.shape[1] * scale)
    new_height = int(template.shape[0] * scale)
    return cv2.resize(template, (new_width, new_height), interpolation=cv2.INTER_AREA)

def load_template(game_name: str, button_name: str, scale: float = 1.0) -> Optional[np.ndarray]:
    """
    加载按钮模板图片
    
    Args:
        game_name: 游戏名称 (如 "genshin-impact")
        button_name: 按钮名称 (如 "feedback", "confirm")
        scale: 缩放比例 (游戏宽度 / 1920)
    
    Returns:
        OpenCV 格式的图片，如果不存在返回 None
    """
    button_path = os.path.join(ASSETS_DIR, game_name, 'assets', 'buttons', f'{button_name}.png')
    if not os.path.exists(button_path):
        return None
    
    try:
        with open(button_path, 'rb') as f:
            img_array = np.frombuffer(f.read(), dtype=np.uint8)
        template = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if template is None:
            return None
    except Exception:
        return None
    
    return resize_template(template, scale)

def list_available_buttons(game_name: str) -> List[str]:
    """
    列出游戏可用的按钮模板
    
    Args:
        game_name: 游戏名称
    
    Returns:
        按钮名称列表
    """
    buttons_dir = os.path.join(ASSETS_DIR, game_name, 'assets', 'buttons')
    if not os.path.exists(buttons_dir):
        return []
    
    buttons = []
    for f in os.listdir(buttons_dir):
        if f.endswith('.png'):
            buttons.append(f[:-4])
    return sorted(buttons)

def create_mask(template: np.ndarray, mask_color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
    """
    创建模板匹配遮罩
    参考 BetterGI 的 OpenCvCommonHelper.CreateMask
    
    Args:
        template: 模板图像 (BGR)
        mask_color: 需要忽略的颜色 (BGR)，默认绿色
    
    Returns:
        遮罩图像
    """
    lower = np.array(mask_color, dtype=np.uint8)
    upper = np.array(mask_color, dtype=np.uint8)
    mask = cv2.inRange(template, lower, upper)
    mask = cv2.bitwise_not(mask)
    return mask

def match_template(
    source: np.ndarray, 
    template: np.ndarray, 
    threshold: float = 0.8,
    method: int = cv2.TM_CCOEFF_NORMED,
    mask: Optional[np.ndarray] = None,
    roi: Optional[Tuple[int, int, int, int]] = None
) -> Optional[Tuple[int, int, int, int, float]]:
    """
    模板匹配 - 参考 BetterGI 的 MatchTemplateHelper.MatchTemplate
    
    Args:
        source: 源图像 (OpenCV BGR 格式)
        template: 模板图像 (OpenCV BGR 格式)
        threshold: 匹配阈值，默认 0.8
        method: 匹配方法，默认 TM_CCOEFF_NORMED
        mask: 遮罩图像 (可选)
        roi: 感兴趣区域 (x, y, w, h)
    
    Returns:
        (x, y, width, height, confidence) 或 None
    """
    if source is None or template is None:
        return None
    
    if roi:
        x, y, w, h = roi
        if x < 0 or y < 0 or x + w > source.shape[1] or y + h > source.shape[0]:
            return None
        source = source[y:y+h, x:x+w].copy()
    else:
        x, y = 0, 0
    
    if source.shape[0] < template.shape[0] or source.shape[1] < template.shape[1]:
        return None
    
    result = cv2.matchTemplate(source, template, method, mask=mask)
    
    if method in [cv2.TM_SQDIFF, cv2.TM_CCOEFF, cv2.TM_CCORR]:
        cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        confidence = 1 - min_val
        top_left = min_loc
    else:
        confidence = max_val
        top_left = max_loc
    
    if confidence >= threshold:
        h, w = template.shape[:2]
        return (top_left[0] + x, top_left[1] + y, w, h, float(confidence))
    
    return None

def match_template_multi(
    source: np.ndarray, 
    template: np.ndarray, 
    threshold: float = 0.8,
    max_count: int = 10,
    mask: Optional[np.ndarray] = None,
    roi: Optional[Tuple[int, int, int, int]] = None
) -> List[Tuple[int, int, int, int, float]]:
    """
    多目标模板匹配 - 参考 BetterGI 的 MatchTemplateHelper.MatchOnePicForOnePic
    
    Args:
        source: 源图像
        template: 模板图像
        threshold: 匹配阈值
        max_count: 最大匹配数量
        mask: 遮罩图像
        roi: 感兴趣区域
    
    Returns:
        匹配结果列表 [(x, y, w, h, confidence), ...]
    """
    results = []
    temp_source = source.copy()
    
    roi_offset = (0, 0)
    if roi:
        x, y, w, h = roi
        if x >= 0 and y >= 0 and x + w <= source.shape[1] and y + h <= source.shape[0]:
            temp_source = temp_source[y:y+h, x:x+w].copy()
            roi_offset = (x, y)
    
    for _ in range(max_count):
        match = match_template(temp_source, template, threshold, mask=mask)
        if match is None:
            break
        
        mx, my, mw, mh, conf = match
        rx, ry = roi_offset
        results.append((mx + rx, my + ry, mw, mh, conf))
        
        cv2.rectangle(temp_source, (mx, my), (mx + mw, my + mh), (0, 0, 0), -1)
    
    return results

def match_color(
    source: np.ndarray,
    lower_color: Tuple[int, int, int],
    upper_color: Tuple[int, int, int],
    color_code: int = cv2.COLOR_BGR2RGB,
    match_count: int = 1,
    roi: Optional[Tuple[int, int, int, int]] = None
) -> Optional[Tuple[int, int, int, int, int]]:
    """
    颜色匹配
    
    Args:
        source: 源图像 (BGR)
        lower_color: 颜色下界
        upper_color: 颜色上界
        color_code: 颜色转换代码
        match_count: 符合条件的点数量要求
        roi: 感兴趣区域
    
    Returns:
        (x, y, w, h, count) 或 None
    """
    if roi:
        x, y, w, h = roi
        if x < 0 or y < 0 or x + w > source.shape[1] or y + h > source.shape[0]:
            return None
        source = source[y:y+h, x:x+w].copy()
    else:
        x, y = 0, 0
    
    converted = cv2.cvtColor(source, color_code)
    mask = cv2.inRange(converted, np.array(lower_color), np.array(upper_color))
    
    count = cv2.countNonZero(mask)
    if count >= match_count:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            bx, by, bw, bh = cv2.boundingRect(largest)
            return (bx + x, by + y, bw, bh, count)
    
    return None

class RecognitionObject:
    """
    识别对象 - 参考 BetterGI 的 RecognitionObject
    """
    def __init__(self):
        self.recognition_type = RecognitionType.NONE
        self.name: Optional[str] = None
        self.roi: Optional[Tuple[int, int, int, int]] = None
        
        self.template_image: Optional[np.ndarray] = None
        self.template_grey: Optional[np.ndarray] = None
        self.threshold: float = 0.8
        self.use_3_channels: bool = False
        self.method: int = cv2.TM_CCOEFF_NORMED
        self.use_mask: bool = False
        self.mask_color: Tuple[int, int, int] = (0, 255, 0)
        self.mask: Optional[np.ndarray] = None
        self.use_binary_match: bool = False
        self.binary_threshold: int = 128
        self.max_match_count: int = -1
        
        self.color_code: int = cv2.COLOR_BGR2RGB
        self.lower_color: Optional[Tuple[int, int, int]] = None
        self.upper_color: Optional[Tuple[int, int, int]] = None
        self.match_count: int = 1
        
        self.ocr_engine: str = "paddle"
        self.replace_dict: Dict[str, List[str]] = {}
        self.all_contain_match: List[str] = []
        self.one_contain_match: List[str] = []
        self.regex_match: List[str] = []
        self.text: str = ""
    
    def init_template(self) -> 'RecognitionObject':
        """初始化模板"""
        if self.template_image is not None and self.template_grey is None:
            self.template_grey = cv2.cvtColor(self.template_image, cv2.COLOR_BGR2GRAY)
        
        if self.use_mask and self.template_image is not None and self.mask is None:
            self.mask = create_mask(self.template_image, self.mask_color)
        
        return self
    
    @staticmethod
    def template_match(template: np.ndarray, use_mask: bool = False, 
                       mask_color: Tuple[int, int, int] = (0, 255, 0)) -> 'RecognitionObject':
        """创建模板匹配对象"""
        ro = RecognitionObject()
        ro.recognition_type = RecognitionType.TEMPLATE_MATCH
        ro.template_image = template
        ro.use_mask = use_mask
        ro.mask_color = mask_color
        return ro.init_template()
    
    @staticmethod
    def template_match_roi(template: np.ndarray, roi: Tuple[int, int, int, int]) -> 'RecognitionObject':
        """创建带ROI的模板匹配对象"""
        ro = RecognitionObject()
        ro.recognition_type = RecognitionType.TEMPLATE_MATCH
        ro.template_image = template
        ro.roi = roi
        return ro.init_template()
    
    @staticmethod
    def color_match(lower: Tuple[int, int, int], upper: Tuple[int, int, int],
                    color_code: int = cv2.COLOR_BGR2RGB, match_count: int = 1) -> 'RecognitionObject':
        """创建颜色匹配对象"""
        ro = RecognitionObject()
        ro.recognition_type = RecognitionType.COLOR_MATCH
        ro.lower_color = lower
        ro.upper_color = upper
        ro.color_code = color_code
        ro.match_count = match_count
        return ro
    
    @staticmethod
    def ocr(roi: Optional[Tuple[int, int, int, int]] = None) -> 'RecognitionObject':
        """创建OCR识别对象"""
        ro = RecognitionObject()
        ro.recognition_type = RecognitionType.OCR
        ro.roi = roi
        return ro
    
    @staticmethod
    def ocr_match(roi: Tuple[int, int, int, int], match_texts: List[str]) -> 'RecognitionObject':
        """创建OCR匹配对象"""
        ro = RecognitionObject()
        ro.recognition_type = RecognitionType.OCR_MATCH
        ro.roi = roi
        ro.one_contain_match = match_texts
        return ro

class ImageRegion:
    """
    图像区域 - 参考 BetterGI 的 ImageRegion
    """
    def __init__(self, src_mat: np.ndarray, x: int = 0, y: int = 0):
        self.src_mat = src_mat
        self.x = x
        self.y = y
        self._cache_grey: Optional[np.ndarray] = None
        self.text: str = ""
    
    @property
    def width(self) -> int:
        return self.src_mat.shape[1]
    
    @property
    def height(self) -> int:
        return self.src_mat.shape[0]
    
    @property
    def cache_grey(self) -> np.ndarray:
        if self._cache_grey is None:
            self._cache_grey = cv2.cvtColor(self.src_mat, cv2.COLOR_BGR2GRAY)
        return self._cache_grey
    
    def find(self, ro: RecognitionObject) -> Optional[Dict]:
        """
        查找识别对象 - 参考 BetterGI 的 ImageRegion.Find
        
        Returns:
            {'x': 中心点X, 'y': 中心点Y, 'width': 宽度, 'height': 高度, 'confidence': 置信度} 或 None
        """
        if ro is None:
            return None
        
        if ro.recognition_type == RecognitionType.TEMPLATE_MATCH:
            return self._find_template(ro)
        elif ro.recognition_type == RecognitionType.COLOR_MATCH:
            return self._find_color(ro)
        elif ro.recognition_type == RecognitionType.OCR:
            return self._ocr(ro)
        elif ro.recognition_type == RecognitionType.OCR_MATCH:
            return self._ocr_match(ro)
        
        return None
    
    def find_multi(self, ro: RecognitionObject, max_count: int = 10) -> List[Dict]:
        """
        查找多个识别对象
        """
        if ro is None:
            return []
        
        if ro.recognition_type == RecognitionType.TEMPLATE_MATCH:
            return self._find_template_multi(ro, max_count)
        
        return []
    
    def _find_template(self, ro: RecognitionObject) -> Optional[Dict]:
        """模板匹配查找"""
        if ro.use_3_channels:
            roi = self.src_mat
            template = ro.template_image
        elif ro.use_binary_match:
            _, roi = cv2.threshold(self.cache_grey, ro.binary_threshold, 255, cv2.THRESH_BINARY)
            template = ro.template_grey
        else:
            roi = self.cache_grey
            template = ro.template_grey
        
        if template is None:
            return None
        
        result = match_template(roi, template, ro.threshold, ro.method, ro.mask, ro.roi)
        if result:
            x, y, w, h, conf = result
            return {
                'x': x + w // 2,
                'y': y + h // 2,
                'width': w,
                'height': h,
                'confidence': round(conf, 3)
            }
        return None
    
    def _find_template_multi(self, ro: RecognitionObject, max_count: int) -> List[Dict]:
        """多目标模板匹配"""
        if ro.use_3_channels:
            roi = self.src_mat
            template = ro.template_image
        else:
            roi = self.cache_grey
            template = ro.template_grey
        
        if template is None:
            return []
        
        count = max_count if ro.max_match_count < 0 else ro.max_match_count
        results = match_template_multi(roi, template, ro.threshold, count, ro.mask, ro.roi)
        
        return [
            {'x': x + w // 2, 'y': y + h // 2, 'width': w, 'height': h, 'confidence': round(conf, 3)}
            for x, y, w, h, conf in results
        ]
    
    def _find_color(self, ro: RecognitionObject) -> Optional[Dict]:
        """颜色匹配查找"""
        if ro.lower_color is None or ro.upper_color is None:
            return None
        
        result = match_color(self.src_mat, ro.lower_color, ro.upper_color, 
                            ro.color_code, ro.match_count, ro.roi)
        if result:
            x, y, w, h, count = result
            return {
                'x': x + w // 2,
                'y': y + h // 2,
                'width': w,
                'height': h,
                'count': count
            }
        return None
    
    def _ocr(self, ro: RecognitionObject) -> Optional[Dict]:
        """OCR识别 (占位)"""
        return None
    
    def _ocr_match(self, ro: RecognitionObject) -> Optional[Dict]:
        """OCR匹配 (占位)"""
        return None

def find_button(
    screenshot: Image.Image,
    game_name: str,
    button_name: str,
    threshold: float = 0.8,
    roi: Optional[Tuple[int, int, int, int]] = None,
    game_width: Optional[int] = None
) -> Optional[Dict]:
    """
    在截图中查找按钮
    
    Args:
        screenshot: PIL Image 格式的截图
        game_name: 游戏名称
        button_name: 按钮名称
        threshold: 匹配阈值
        roi: 感兴趣区域
        game_width: 游戏窗口宽度 (用于计算缩放比例)
    
    Returns:
        {'x': 中心点X, 'y': 中心点Y, 'width': 宽度, 'height': 高度, 'confidence': 置信度} 或 None
    """
    scale = 1.0
    if game_width is not None:
        scale = game_width / TEMPLATE_BASE_WIDTH
    
    template = load_template(game_name, button_name, scale)
    if template is None:
        return None
    
    source = pil_to_cv2(screenshot)
    img_height, img_width = source.shape[:2]
    
    button_config = _load_button_config(game_name).get(button_name, {})
    
    if 'threshold' in button_config and threshold == 0.8:
        threshold = button_config['threshold']
    
    if roi is None and 'roi' in button_config:
        roi = _get_button_roi(button_config, img_width, img_height)
    
    region = ImageRegion(source)
    
    ro = RecognitionObject.template_match(template)
    ro.threshold = threshold
    
    if button_config.get('use_3_channels', False):
        ro.use_3_channels = True
    
    if roi:
        ro.roi = roi
    
    return region.find(ro)

def find_all_buttons(
    screenshot: Image.Image,
    game_name: str,
    threshold: float = 0.8,
    game_width: Optional[int] = None
) -> Dict[str, Dict]:
    """
    在截图中查找所有可用按钮
    
    Args:
        screenshot: PIL Image 格式的截图
        game_name: 游戏名称
        threshold: 匹配阈值
        game_width: 游戏窗口宽度 (用于计算缩放比例)
    
    Returns:
        {按钮名称: {x, y, width, height, confidence}, ...}
    """
    available_buttons = list_available_buttons(game_name)
    results = {}
    
    for button_name in available_buttons:
        result = find_button(screenshot, game_name, button_name, threshold, game_width=game_width)
        if result:
            results[button_name] = result
    
    return results

def find_text_region(
    screenshot: Image.Image,
    text: str,
    region: Optional[Tuple[int, int, int, int]] = None
) -> Optional[Dict]:
    """
    使用 OCR 查找文字区域 (占位实现)
    
    Args:
        screenshot: 截图
        text: 要查找的文字
        region: 搜索区域 (x, y, w, h)
    
    Returns:
        {'x': 中心点X, 'y': 中心点Y, 'text': 文字} 或 None
    """
    return None
