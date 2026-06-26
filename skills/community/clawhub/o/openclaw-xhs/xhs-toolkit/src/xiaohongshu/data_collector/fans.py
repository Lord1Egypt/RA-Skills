#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
粉丝数据采集模块

该模块负责从小红书创作者中心采集粉丝相关数据，包括：
- 粉丝总数
- 新增粉丝数
- 流失粉丝数
- 支持7天和30天两个时间维度
"""

import time
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from src.utils.logger import get_logger
from .utils import wait_for_fans_data, extract_text_safely
from src.data.storage_manager import get_storage_manager

logger = get_logger(__name__)

def collect_fans_data(driver: WebDriver, save_data: bool = True) -> Dict[str, Any]:
    """采集粉丝数据，支持7天和30天两个维度"""
    fans_data = {
        "success": False,
        "data": [],
        "collect_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "error": None
    }
    
    try:
        logger.info("👥 开始采集粉丝数据...")
        
        # 访问粉丝数据页面
        fans_url = "https://creator.xiaohongshu.com/creator/fans"
        logger.info(f"📍 访问粉丝数据页面: {fans_url}")
        driver.get(fans_url)
        
        # 等待页面加载
        wait_for_fans_data(driver)
        
        # 采集两个维度的粉丝数据
        fans_data["data"] = _collect_multi_dimension_fans_data(driver)
        
        if fans_data["data"]:
            fans_data["success"] = True
            logger.info(f"✅ 粉丝数据采集完成，共采集 {len(fans_data['data'])} 个维度的数据")
        else:
            logger.warning("⚠️ 未采集到有效的粉丝数据")
        
        # 保存数据到存储
        if save_data and fans_data["success"]:
            try:
                storage_manager = get_storage_manager()
                storage_data = []
                for item in fans_data["data"]:
                    storage_data.append({
                        'timestamp': fans_data["collect_time"],
                        'dimension': item.get('dimension', ''),
                        'total_fans': item.get('total_fans', 0),
                        'new_fans': item.get('new_fans', 0),
                        'lost_fans': item.get('lost_fans', 0)
                    })
                
                if storage_data:
                    storage_manager.save_fans_data(storage_data)
                    logger.info("💾 粉丝数据已保存到存储")
                    
                    for item in storage_data:
                        logger.info(f"💾 {item['dimension']}维度: 总粉丝{item['total_fans']}, 新增{item['new_fans']}, 流失{item['lost_fans']}")
                else:
                    logger.warning("⚠️ 没有有效的粉丝数据需要保存")
            except Exception as e:
                logger.error(f"❌ 保存粉丝数据失败: {e}")
                fans_data["error"] = f"保存数据失败: {str(e)}"
        
    except Exception as e:
        logger.error(f"❌ 粉丝数据采集失败: {e}")
        fans_data["error"] = str(e)
    
    return fans_data

def _collect_multi_dimension_fans_data(driver: WebDriver) -> List[Dict[str, Any]]:
    """采集多维度粉丝数据"""
    all_fans_data = []
    
    try:
        # 先采集7天维度的数据
        logger.info("📅 开始采集7天维度的粉丝数据")
        seven_day_data = _collect_single_dimension_data(driver, '7天')
        if seven_day_data:
            all_fans_data.append(seven_day_data)
            logger.info("✅ 7天维度数据采集完成")
        
        # 尝试切换到30天维度
        if _switch_to_30day_dimension(driver):
            logger.info("📅 开始采集30天维度的粉丝数据")
            thirty_day_data = _collect_single_dimension_data(driver, '30天')
            if thirty_day_data:
                all_fans_data.append(thirty_day_data)
                logger.info("✅ 30天维度数据采集完成")
        else:
            logger.warning("⚠️ 无法切换到30天维度，仅采集7天数据")
            
    except Exception as e:
        logger.error(f"❌ 多维度粉丝数据采集失败: {e}")
        # 如果多维度采集失败，至少尝试采集当前维度的数据
        try:
            fallback_data = _collect_single_dimension_data(driver, '当前')
            if fallback_data:
                all_fans_data.append(fallback_data)
                logger.info("✅ 已采集当前维度的粉丝数据作为备选")
        except:
            pass
    
    return all_fans_data

def _switch_to_30day_dimension(driver: WebDriver) -> bool:
    """切换到30天维度"""
    try:
        # 先点击7天按钮打开下拉菜单
        seven_day_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.dyn.css-ewzbi1.css-cwdr7o')
        if seven_day_buttons:
            for btn in seven_day_buttons:
                btn_text = extract_text_safely(btn)
                if '近7天' in btn_text:
                    btn.click()
                    time.sleep(1)
                    logger.debug("📅 已点击7天按钮打开下拉菜单")
                    break
        
        # 然后点击30天选项
        thirty_day_elements = driver.find_elements(By.CSS_SELECTOR, 'div.css-1vlk884')
        if not thirty_day_elements:
            # 尝试其他选择器
            thirty_day_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '近30天')]")
        
        if thirty_day_elements:
            for elem in thirty_day_elements:
                elem_text = extract_text_safely(elem)
                if '近30天' in elem_text:
                    elem.click()
                    time.sleep(2)  # 等待数据刷新
                    logger.info("📅 已选择30天时间维度")
                    return True
        
        logger.warning("⚠️ 未找到30天选项")
        return False
        
    except Exception as e:
        logger.error(f"❌ 切换到30天维度失败: {e}")
        return False

def _collect_single_dimension_data(driver: WebDriver, dimension_name: str) -> Optional[Dict[str, Any]]:
    """采集单个维度的粉丝数据"""
    try:
        dimension_data = {'dimension': dimension_name}
        
        fans_data_mapping = {
            '总粉丝数': 'total_fans',
            '新增粉丝数': 'new_fans', 
            '流失粉丝数': 'lost_fans'
        }
        
        for label_text, data_key in fans_data_mapping.items():
            try:
                value = _extract_fans_metric(driver, label_text)
                dimension_data[data_key] = value
                logger.debug(f"📊 {dimension_name}维度 {label_text}: {value}")
                
            except Exception as e:
                logger.warning(f"⚠️ 采集{dimension_name}维度{label_text}失败: {e}")
                dimension_data[data_key] = 0
        
        return dimension_data
            
    except Exception as e:
        logger.error(f"❌ 采集{dimension_name}维度数据失败: {e}")
        return None

def _extract_fans_metric(driver: WebDriver, label_text: str) -> int:
    """提取特定指标的数值"""
    try:
        label_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{label_text}') and string-length(text()) < 20]")
        
        for label_element in label_elements:
            number_element = None
            
            con_elements = label_element.find_elements(By.CSS_SELECTOR, '.con')
            if con_elements:
                number_element = con_elements[0]
            
            if not number_element:
                if '新增' in label_text:
                    add_elements = label_element.find_elements(By.CSS_SELECTOR, '.add-fans')
                    if add_elements:
                        number_element = add_elements[0]
                elif '流失' in label_text:
                    loss_elements = label_element.find_elements(By.CSS_SELECTOR, '.loss-fans')
                    if loss_elements:
                        number_element = loss_elements[0]
            
            if not number_element:
                try:
                    parent = label_element.find_element(By.XPATH, '..')
                    number_elements = parent.find_elements(By.CSS_SELECTOR, '.con, .add-fans, .loss-fans')
                    for elem in number_elements:
                        text = extract_text_safely(elem)
                        if text and text.isdigit():
                            number_element = elem
                            break
                except:
                    pass
            
            if number_element:
                value_text = extract_text_safely(number_element)
                if value_text and value_text.isdigit():
                    return int(value_text)
        
        logger.warning(f"⚠️ 未找到{label_text}的数值")
        return 0
        
    except Exception as e:
        logger.error(f"❌ 提取{label_text}数值失败: {e}")
        return 0 