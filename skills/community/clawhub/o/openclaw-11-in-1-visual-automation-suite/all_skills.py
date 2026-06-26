"""
通用电脑视觉自动化 Skill 体系 - 所有单元代码合集
所有最小执行单元都在这里，可以按需导入使用
"""

import os
import cv2
import numpy as np
import ctypes
from PIL import Image

# ========== 1. init_env - 初始化环境 ==========
def init_env(base_path="./computer_skill"):
    """
    初始化环境：创建目录结构、清空 temp、检查模板目录
    """
    dirs = [
        f"{base_path}",
        f"{base_path}/templates",
        f"{base_path}/templates/desktop",
        f"{base_path}/templates/taskbar",
        f"{base_path}/templates/system",
        f"{base_path}/templates/wechat",
        f"{base_path}/temp"
    ]
    
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"📁 创建目录: {d}")
    
    # 清空 temp
    temp_dir = f"{base_path}/temp"
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    
    print("✅ init_env 完成：目录结构已初始化，temp 已清空")
    return True


# ========== 2. screenshot_full - 全屏截图 ==========
def screenshot_full(output_path="./computer_skill/temp/screen.png"):
    """
    截取整个屏幕保存到指定路径
    """
    import pyautogui
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)
    print(f"✅ screenshot_full 完成：截图已保存到 {output_path}")
    return output_path


# ========== 3. check_screenshot_valid - 检查截图有效性 ==========
def check_screenshot_valid(screen_path="./computer_skill/temp/screen.png"):
    """
    检查截图是否有效（是否黑屏/冻结）
    """
    if not os.path.exists(screen_path):
        print("❌ 截图文件不存在")
        return False
    
    img = cv2.imread(screen_path)
    if img is None:
        print("❌ 无法读取截图")
        return False
    
    # 检查是否全黑（简单判断）
    avg_brightness = np.mean(img)
    if avg_brightness < 5:
        print("⚠️ 截图几乎全黑，可能是黑屏")
        return False
    
    print(f"✅ check_screenshot_valid 完成：截图有效（平均亮度 {avg_brightness:.1f}）")
    return True


# ========== 4. wake_window - 唤醒界面 ==========
def wake_window():
    """
    唤醒界面，解决后台不渲染问题：移动鼠标并点击左键一次
    """
    import pyautogui
    # 移动鼠标到屏幕中心并点击
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    pyautogui.moveTo(center_x, center_y, duration=0.5)
    pyautogui.click()
    print("✅ wake_window 完成：已唤醒界面")
    return True


# ========== 5. ocr_recognize - OCR识别 ==========
def ocr_recognize(screen_path="./computer_skill/temp/screen.png", lang='chi_sim', tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
    """
    OCR识别屏幕所有文字与对应坐标
    """
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    img = Image.open(screen_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=lang)
    
    # 保存识别结果
    result_path = "./computer_skill/temp/ocr_result.txt"
    with open(result_path, 'w', encoding='utf-8') as f:
        for i in range(len(data['text'])):
            if data['text'][i].strip():
                f.write(f"{data['left'][i]},{data['top'][i]},{data['width'][i]},{data['height'][i]},{data['text'][i]}\n")
    
    print(f"✅ ocr_recognize 完成：识别结果已保存到 {result_path}，共找到 {len([t for t in data['text'] if t.strip()])} 个文字块")
    return data


# ========== 6. template_match - 模板匹配 ==========
def template_match(category, template_name, base_path="./computer_skill", threshold=0.6, screen_path="./computer_skill/temp/screen.png"):
    """
    使用模板匹配定位图标/按钮
    """
    template_path = f"{base_path}/templates/{category}/{template_name}.png"
    
    screen = cv2.imread(screen_path)
    template = cv2.imread(template_path)
    
    if screen is None:
        print(f"❌ 无法读取截图 {screen_path}")
        return None
    if template is None:
        print(f"❌ 无法读取模板 {template_path}")
        return None
    
    h, w = template.shape[:2]
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= threshold:
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        print(f"✅ template_match 成功：找到匹配")
        print(f"   模板: {category}/{template_name}")
        print(f"   匹配度: {max_val:.3f}")
        print(f"   中心坐标: ({center_x}, {center_y})")
        
        with open(f"{base_path}/temp/coord.txt", 'w') as f:
            f.write(f'{center_x},{center_y}')
        
        return (center_x, center_y, max_val)
    else:
        print(f"⚠️ template_match 未找到匹配（最高匹配度 {max_val:.3f} < 阈值 {threshold}）")
        return None


# ========== 7. locate_target - 统一定位 ==========
def locate_target(target_text, category=None, template_name=None, 
                 base_path="./computer_skill", threshold=0.6, 
                 screen_path="./computer_skill/temp/screen.png",
                 tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe', lang='chi_sim'):
    """
    统一定位：OCR优先，找不到再用模板匹配
    """
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # 先尝试 OCR
    print(f"🔍 尝试 OCR 识别目标文字: {target_text}")
    img = Image.open(screen_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=lang)
    
    for i, text in enumerate(data['text']):
        if text and target_text in text:
            center_x = data['left'][i] + data['width'][i] // 2
            center_y = data['top'][i] + data['height'][i] // 2
            print(f"✅ locate_target 成功：OCR 找到目标")
            print(f"   文字: {text}")
            print(f"   中心坐标: ({center_x}, {center_y})")
            
            with open(f"{base_path}/temp/coord.txt", 'w') as f:
                f.write(f'{center_x},{center_y}')
            
            return (center_x, center_y, 'ocr')
    
    # OCR 找不到，尝试模板匹配
    if category and template_name:
        print(f"⚠️ OCR 未找到，尝试模板匹配: {category}/{template_name}")
        result = template_match(category, template_name, base_path, threshold, screen_path)
        if result:
            center_x, center_y, max_val = result
            return (center_x, center_y, 'template')
    
    print(f"❌ locate_target 失败：OCR 和模板匹配都未找到目标")
    return None


# ========== 8. mouse_click - 鼠标点击 ==========
def mouse_click(x=None, y=None, click_type='click', coord_path="./computer_skill/temp/coord.txt"):
    """
    移动鼠标到指定坐标执行点击
    如果不提供 x,y，则从 coord.txt 读取
    click_type: click / double / right
    """
    if x is None or y is None:
        with open(coord_path, 'r') as f:
            coord = f.read().strip().split(',')
            x = int(coord[0])
            y = int(coord[1])
    
    # Windows API 方式移动点击
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    
    ctypes.windll.user32.SetCursorPos(int(x), int(y))
    
    if click_type == 'double':
        # 双击
        for i in range(2):
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, int(x), int(y), 0, 0)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, int(x), int(y), 0, 0)
        print(f"✅ mouse_click 完成：已双击坐标 ({x}, {y})")
    elif click_type == 'right':
        # 右键
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, int(x), int(y), 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, int(x), int(y), 0, 0)
        print(f"✅ mouse_click 完成：已右键单击坐标 ({x}, {y})")
    else:
        # 单击
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, int(x), int(y), 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, int(x), int(y), 0, 0)
        print(f"✅ mouse_click 完成：已单击坐标 ({x}, {y})")
    
    return True


# ========== 9. keyboard_input - 键盘输入 ==========
def keyboard_input(text, x=None, y=None, coord_path="./computer_skill/temp/coord.txt"):
    """
    定位输入框后输入文字
    如果提供 x,y，则先点击输入框
    """
    import pyautogui
    
    if x is not None and y is not None:
        pyautogui.click(x, y)
    
    pyautogui.write(text, interval=0.05)
    print(f"✅ keyboard_input 完成：已输入文字: {text[:20]}{'...' if len(text) > 20 else ''}")
    return True


# ========== 10. clean_temp - 清理临时文件 ==========
def clean_temp(temp_dir="./computer_skill/temp"):
    """
    删除临时截图，释放空间
    """
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    
    print("✅ clean_temp 完成：临时目录已清空")
    return True


# ========== 11. loop_restart - 循环重启 ==========
def loop_restart(wait_ms=2000):
    """
    等待指定毫秒后回到流程开始
    """
    import time
    print(f"⏳ loop_restart：等待 {wait_ms}ms 后重启流程")
    time.sleep(wait_ms / 1000)
    return True


# ========== 完整主流程示例：通用视觉自动化 ==========
def vision_auto_main(target_text, category=None, template_name=None, 
                      action='click', input_text=None, loop=False,
                      base_path="./computer_skill"):
    """
    通用电脑视觉自动化完整主流程
    
    参数:
        target_text: 要定位的目标文字
        category: 模板分类（可选）
        template_name: 模板名称（可选）
        action: click / input
        input_text: 要输入的文字（action=input 时需要）
        loop: 是否循环执行
        base_path: 技能包基础路径
    """
    while True:
        # 1. 初始化环境
        init_env(base_path)
        
        # 2. 全屏截图
        screen_path = screenshot_full(f"{base_path}/temp/screen.png")
        
        # 3. 检查截图有效性
        if not check_screenshot_valid(screen_path):
            wake_window()
            continue
        
        # 4. 定位目标
        result = locate_target(target_text, category, template_name, base_path)
        if not result:
            if not loop:
                return False
            clean_temp(f"{base_path}/temp")
            loop_restart()
            continue
        
        center_x, center_y, method = result
        
        # 5. 执行动作
        if action == 'click':
            mouse_click(center_x, center_y)
        elif action == 'input' and input_text:
            keyboard_input(input_text, center_x, center_y)
        
        # 6. 清理
        clean_temp(f"{base_path}/temp")
        
        # 7. 判断是否循环
        if not loop:
            break
        else:
            loop_restart()
    
    print("🎉 vision_auto_main 流程执行完成")
    return True


if __name__ == "__main__":
    print("通用电脑视觉自动化 Skill 体系 - all_skills.py")
    print("所有函数已加载，可以直接调用")
