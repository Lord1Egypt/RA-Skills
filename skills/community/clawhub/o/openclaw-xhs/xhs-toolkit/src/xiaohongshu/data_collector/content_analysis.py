"""
内容分析数据采集模块

从小红书创作者中心内容分析页面采集每篇笔记的详细数据，包括：
1. 基础数据：标题、发布时间、观看、点赞、评论、收藏、涨粉、分享等
2. 观众来源数据：推荐、搜索、关注、其他来源的百分比
3. 观众分析数据：性别分布、年龄分布、城市分布、兴趣分布
"""

import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .utils import (
    clean_number, wait_for_element, extract_text_safely, 
    find_element_by_selectors, wait_for_page_load, safe_click, scroll_to_element
)
from src.utils.logger import get_logger
from src.data.storage_manager import get_storage_manager

logger = get_logger(__name__)

# 内容分析页面选择器配置
CONTENT_ANALYSIS_SELECTORS = {
    # 文章列表页面选择器 - 基于Playwright调试结果更新
    'note_table': ['.note-data-table', '[class*="el-table"]', '.note-data-container table'],  # 更新为实际发现的选择器
    'note_rows': ['.note-data-table tr', 'tr', '[class*="row"]'],  # 表格行选择器
    'detail_button': '.note-detail',  # 详情数据按钮
    'data_container': '.note-data-container',  # 数据容器
    
    # 详情页面选择器
    'core_data_container': '.el-table__cell',
    'audience_source_container': '[class*="source"]',
    'audience_analysis_container': '[class*="analysis"]',
    
    # 数据提取选择器
    'number_elements': '//*[text()]',
    'percentage_elements': '//*[contains(text(), "%")]'
}

# 表格列索引映射（基于Playwright测试结果）
COLUMN_MAPPING = {
    0: 'title',           # 笔记标题
    1: 'publish_time',    # 发布时间  
    2: 'views',           # 观看
    3: 'likes',           # 点赞
    4: 'comments',        # 评论
    5: 'collects',        # 收藏
    6: 'fans_growth',     # 涨粉
    7: 'shares',          # 分享
    8: 'avg_watch_time',  # 人均观看时长
    9: 'danmu_count',     # 弹幕
    10: 'actions'         # 操作列（包含详情数据按钮）
}


async def collect_content_analysis_data(driver: WebDriver, date: Optional[str] = None, 
                                 limit: int = 50, save_data: bool = True) -> Dict[str, Any]:
    """
    采集内容分析数据
    
    Args:
        driver: WebDriver实例
        date: 采集日期，默认当天
        limit: 最大采集笔记数量
        save_data: 是否保存数据到存储
        
    Returns:
        包含内容分析数据的字典
    """
    logger.info("📊 开始采集内容分析数据...")
    
    # 导航到内容分析页面
    content_url = "https://creator.xiaohongshu.com/statistics/data-analysis"
    try:
        driver.get(content_url)
        logger.info(f"📍 访问内容分析页面: {content_url}")
        
        # 等待页面加载
        if not wait_for_page_load(driver, timeout=30):
            logger.warning("⚠️ 页面加载超时，继续尝试采集")
        
        # 增加等待时间，确保数据完全加载
        time.sleep(10)  # 从5秒增加到10秒
        
    except Exception as e:
        logger.error(f"❌ 访问内容分析页面失败: {e}")
        return {"success": False, "error": str(e)}
    
    # 采集数据
    content_data = {
        "success": True,
        "collect_time": datetime.now().isoformat(),
        "page_url": driver.current_url,
        "notes": [],
        "summary": {}
    }
    
    try:
        # 等待表格加载 - 使用更长的等待时间
        table_element = None
        table_selectors = CONTENT_ANALYSIS_SELECTORS['note_table']
        
        for selector in table_selectors:
            table_element = wait_for_element(driver, selector, timeout=20)  # 从15秒增加到20秒
            if table_element:
                logger.info(f"✅ 找到数据表格，使用选择器: {selector}")
                break
        
        if not table_element:
            logger.warning("⚠️ 未找到数据表格，尝试直接查找笔记行")
            # 尝试直接查找笔记行
            note_rows = driver.find_elements(By.CSS_SELECTOR, '.el-table__row')
            if not note_rows:
                note_rows = driver.find_elements(By.CSS_SELECTOR, 'tr')
            if not note_rows:
                logger.error("❌ 未找到任何数据行")
                return {"success": False, "error": "未找到数据表格或数据行"}
            else:
                logger.info(f"✅ 直接找到 {len(note_rows)} 个数据行")
        
        # 采集笔记列表数据
        notes_data = _collect_notes_list_data(driver, limit)
        
        # 为每篇笔记采集详细数据
        enhanced_notes_data = _enhance_notes_with_detail_data(driver, notes_data)
        
        content_data["notes"] = enhanced_notes_data
        
        # 生成汇总信息
        content_data["summary"] = _generate_summary(enhanced_notes_data)
        
        logger.info(f"✅ 内容分析数据采集完成，共采集 {len(enhanced_notes_data)} 篇笔记")
        
        # 保存数据到存储
        if save_data and enhanced_notes_data:
            try:
                # 格式化数据用于存储
                formatted_notes = _format_notes_for_storage(enhanced_notes_data)
                storage_manager = get_storage_manager()
                storage_manager.save_content_analysis_data(formatted_notes)
                logger.info("💾 内容分析数据已保存到存储")
            except Exception as e:
                logger.error(f"❌ 保存内容分析数据时出错: {e}")
        
    except Exception as e:
        logger.error(f"❌ 采集内容分析数据时出错: {e}")
        content_data["success"] = False
        content_data["error"] = str(e)
    
    return content_data


def _collect_notes_list_data(driver: WebDriver, limit: int) -> List[Dict[str, Any]]:
    """采集笔记列表数据（基于Playwright测试结果）"""
    notes_data = []
    
    try:
        # 使用更新的选择器查找所有笔记行
        note_rows = []
        row_selectors = CONTENT_ANALYSIS_SELECTORS['note_rows']
        
        for selector in row_selectors:
            note_rows = driver.find_elements(By.CSS_SELECTOR, selector)
            if note_rows:
                logger.info(f"🔍 使用选择器 {selector} 找到 {len(note_rows)} 行笔记数据")
                break
        
        if not note_rows:
            logger.warning("⚠️ 未找到任何笔记行")
            return notes_data
        
        # 过滤掉表头行 - 跳过包含"笔记基础信息"、"观看"、"点赞"等表头关键词的行
        header_keywords = ['笔记基础信息', '观看', '点赞', '评论', '收藏', '涨粉', '分享', '操作']
        filtered_rows = []
        
        for row in note_rows:
            try:
                row_text = row.text.strip()
                # 检查是否为表头行
                is_header = any(keyword in row_text for keyword in header_keywords)
                if not is_header and row_text:  # 不是表头且有内容
                    filtered_rows.append(row)
            except:
                continue
        
        logger.info(f"📋 过滤后剩余 {len(filtered_rows)} 行有效数据")
        
        for i, row in enumerate(filtered_rows[:limit]):
            try:
                note_data = _extract_note_data_from_row(row, i)
                if note_data:
                    notes_data.append(note_data)
                    logger.debug(f"📝 笔记 {i+1}: {note_data.get('title', 'Unknown')}")
                    
            except Exception as e:
                logger.warning(f"⚠️ 处理笔记行 {i} 时出错: {e}")
                continue
                
    except Exception as e:
        logger.warning(f"⚠️ 采集笔记数据时出错: {e}")
    
    return notes_data


def _extract_note_data_from_row(row, row_index: int) -> Optional[Dict[str, Any]]:
    """从表格行中提取笔记数据（基于Playwright测试结果）"""
    try:
        # 查找行中的所有单元格 - 使用更通用的选择器
        cell_selectors = ['.el-table__cell', 'td', 'th', '[class*="cell"]']
        cells = []
        
        for selector in cell_selectors:
            cells = row.find_elements(By.CSS_SELECTOR, selector)
            if cells:
                logger.debug(f"使用选择器 {selector} 找到 {len(cells)} 个单元格")
                break
        
        if len(cells) < 3:  # 至少需要标题、时间、数据
            logger.warning(f"⚠️ 行 {row_index} 单元格数量不足: {len(cells)}")
            return None
        
        note_data = {
            "row_index": row_index,
            "extract_time": datetime.now().isoformat()
        }
        
        # 按列索引提取数据
        for col_index, cell in enumerate(cells):
            try:
                cell_text = extract_text_safely(cell)
                if not cell_text:
                    continue
                
                field_name = COLUMN_MAPPING.get(col_index, f"column_{col_index}")
                
                if field_name == 'title':
                    # 标题列，提取笔记标题 - 过滤掉"发布于"及其后面的内容
                    title_text = cell_text.strip()
                    if '发布于' in title_text:
                        title_text = title_text.split('发布于')[0].strip()
                    note_data['title'] = title_text
                    
                elif field_name == 'publish_time':
                    # 发布时间列
                    note_data['publish_time'] = cell_text.strip()
                    
                elif field_name in ['views', 'likes', 'comments', 'collects', 'fans_growth', 'shares', 'danmu_count']:
                    # 数值列，清理并转换为整数
                    cleaned_value = clean_number(cell_text)
                    note_data[field_name] = cleaned_value
                    
                elif field_name == 'avg_watch_time':
                    # 时长列，保持原始格式
                    note_data[field_name] = cell_text.strip()
                    
                elif field_name == 'actions':
                    # 操作列，查找详情数据按钮 - 使用多个选择器
                    detail_button_selectors = [
                        '.note-detail',
                        'button[class*="detail"]',
                        'a[class*="detail"]',
                        'span[class*="detail"]',
                        'button:contains("详情")',
                        'a:contains("详情")',
                        'button',  # 最后尝试任何按钮
                        'a'        # 最后尝试任何链接
                    ]
                    
                    detail_button = None
                    for btn_selector in detail_button_selectors:
                        try:
                            detail_button = cell.find_element(By.CSS_SELECTOR, btn_selector)
                            if detail_button:
                                logger.debug(f"找到详情按钮，使用选择器: {btn_selector}")
                                break
                        except:
                            continue
                    
                    if detail_button:
                        note_data['has_detail_button'] = True
                        note_data['detail_button_element'] = detail_button
                    else:
                        note_data['has_detail_button'] = False
                    
            except Exception as e:
                logger.debug(f"处理列 {col_index} 时出错: {e}")
                continue
        
        return note_data if note_data.get('title') else None
        
    except Exception as e:
        logger.warning(f"⚠️ 提取行数据时出错: {e}")
        return None


def _enhance_notes_with_detail_data(driver: WebDriver, notes_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """为每篇笔记采集详细数据"""
    enhanced_notes = []
    
    for i, note in enumerate(notes_data):
        try:
            logger.info(f"📊 采集笔记 {i+1}/{len(notes_data)} 的详细数据: {note.get('title', 'Unknown')}")
            
            # 点击详情数据按钮
            if note.get('has_detail_button') and note.get('detail_button_element'):
                detail_button = note['detail_button_element']
                
                # 滚动到按钮可见
                driver.execute_script("arguments[0].scrollIntoView(true);", detail_button)
                time.sleep(1)
                
                # 点击详情按钮
                detail_button.click()
                logger.info(f"✅ 成功点击详情数据按钮")
                
                # 等待详情页面加载
                time.sleep(3)
                
                # 采集详情页面数据
                detail_data = _collect_detail_page_data(driver)
                
                # 合并数据
                enhanced_note = {**note, **detail_data}
                enhanced_notes.append(enhanced_note)
                
                # 返回列表页面
                _return_to_list_page(driver)
                
            else:
                logger.warning(f"⚠️ 笔记 {note.get('title')} 没有详情按钮")
                enhanced_notes.append(note)
                
        except Exception as e:
            logger.error(f"❌ 采集笔记详细数据时出错: {e}")
            enhanced_notes.append(note)  # 保留基础数据
            
            # 尝试返回列表页面
            try:
                _return_to_list_page(driver)
            except:
                pass
    
    return enhanced_notes


def _collect_detail_page_data(driver: WebDriver) -> Dict[str, Any]:
    """采集详情页面数据"""
    detail_data = {
        # 观众来源数据
        "source_recommend": "0%",
        "source_search": "0%", 
        "source_follow": "0%",
        "source_other": "0%",
        # 观众分析数据
        "gender_male": "0%",
        "gender_female": "0%",
        "age_18_24": "0%",
        "age_25_34": "0%",
        "age_35_44": "0%",
        "age_45_plus": "0%",
        "city_top1": "",
        "city_top2": "",
        "city_top3": "",
        "interest_top1": "",
        "interest_top2": "",
        "interest_top3": ""
    }
    
    try:
        # 等待页面加载
        time.sleep(3)
        
        # 采集观众来源数据
        source_data = _collect_audience_source_data(driver)
        detail_data.update(source_data)
        
        # 采集观众分析数据
        analysis_data = _collect_audience_analysis_data(driver)
        detail_data.update(analysis_data)
        
        logger.info("✅ 详情页面数据采集完成")
        
    except Exception as e:
        logger.error(f"❌ 采集详情页面数据时出错: {e}")
    
    return detail_data


def _collect_audience_source_data(driver: WebDriver) -> Dict[str, Any]:
    """采集观众来源数据"""
    source_data = {
        "source_recommend": "0%",
        "source_search": "0%",
        "source_follow": "0%",
        "source_other": "0%"
    }
    
    try:
        # 查找包含百分比的元素
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), '%')]")
        
        for elem in elements:
            try:
                text = elem.text.strip()
                if "%" in text and text.replace('%', '').replace('.', '').isdigit():
                    # 获取上下文
                    parent = elem.find_element(By.XPATH, "..")
                    context = parent.text.strip()
                    
                    # 根据上下文判断来源类型
                    if "推荐" in context or "首页" in context:
                        source_data["source_recommend"] = text
                    elif "搜索" in context:
                        source_data["source_search"] = text
                    elif "关注" in context or "个人主页" in context:
                        source_data["source_follow"] = text
                    elif "其他" in context:
                        source_data["source_other"] = text
                        
            except Exception as e:
                continue
        
        logger.info(f"观众来源数据: {source_data}")
        
    except Exception as e:
        logger.warning(f"⚠️ 采集观众来源数据失败: {e}")
    
    return source_data


def _collect_audience_analysis_data(driver: WebDriver) -> Dict[str, Any]:
    """采集观众分析数据"""
    analysis_data = {
        "gender_male": "0%",
        "gender_female": "0%",
        "age_18_24": "0%",
        "age_25_34": "0%",
        "age_35_44": "0%",
        "age_45_plus": "0%",
        "city_top1": "",
        "city_top2": "",
        "city_top3": "",
        "interest_top1": "",
        "interest_top2": "",
        "interest_top3": ""
    }
    
    try:
        # 滚动页面查找观众分析区域
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # 查找性别分布
        gender_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '男性') or contains(text(), '女性')]")
        for elem in gender_elements:
            try:
                text = elem.text.strip()
                if "男性" in text and "%" in text:
                    percentage = text.split("男性")[-1].strip()
                    if "%" in percentage:
                        analysis_data["gender_male"] = percentage
                elif "女性" in text and "%" in text:
                    percentage = text.split("女性")[-1].strip()
                    if "%" in percentage:
                        analysis_data["gender_female"] = percentage
            except:
                continue
        
        # 查找年龄分布
        age_keywords = {
            "18-24": "age_18_24",
            "25-34": "age_25_34", 
            "35-44": "age_35_44",
            "45": "age_45_plus"
        }
        
        for age_range, field_name in age_keywords.items():
            try:
                age_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{age_range}')]")
                for elem in age_elements:
                    text = elem.text.strip()
                    if "%" in text:
                        # 提取百分比
                        percentage = text.split(age_range)[-1].strip()
                        if "%" in percentage:
                            analysis_data[field_name] = percentage
                        break
            except:
                continue
        
        # 查找城市分布（前3名）
        city_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '省') or contains(text(), '市')]")
        city_count = 0
        for elem in city_elements:
            try:
                text = elem.text.strip()
                if ("省" in text or "市" in text) and len(text) < 20:
                    if city_count == 0:
                        analysis_data["city_top1"] = text
                    elif city_count == 1:
                        analysis_data["city_top2"] = text
                    elif city_count == 2:
                        analysis_data["city_top3"] = text
                        break
                    city_count += 1
            except:
                continue
        
        logger.info(f"观众分析数据: {analysis_data}")
        
    except Exception as e:
        logger.warning(f"⚠️ 采集观众分析数据失败: {e}")
    
    return analysis_data


def _return_to_list_page(driver: WebDriver) -> None:
    """返回到列表页面"""
    try:
        # 尝试多种返回方法
        # 方法1：浏览器后退
        driver.back()
        time.sleep(3)
        
        # 检查是否成功返回
        if "data-analysis" in driver.current_url:
            logger.info("✅ 成功返回列表页面")
            return
        
        # 方法2：直接导航到列表页面
        driver.get("https://creator.xiaohongshu.com/statistics/data-analysis")
        time.sleep(3)
        logger.info("✅ 重新导航到列表页面")
        
    except Exception as e:
        logger.warning(f"⚠️ 返回列表页面失败: {e}")


def _format_notes_for_storage(notes_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """格式化笔记数据用于存储"""
    formatted_notes = []
    
    for note in notes_data:
        try:
            # 提取基础字段
            def get_field_value(field_name: str, default: Any = 0) -> Any:
                value = note.get(field_name, default)
                if isinstance(value, str) and value.isdigit():
                    return int(value)
                return value
            
            formatted_note = {
                "timestamp": note.get("extract_time", datetime.now().isoformat()),
                "title": note.get("title", ""),
                "note_type": "图文",  # 默认类型，后续可以根据内容判断
                "publish_time": note.get("publish_time", ""),
                "views": get_field_value("views"),
                "likes": get_field_value("likes"),
                "comments": get_field_value("comments"),
                "collects": get_field_value("collects"),
                "shares": get_field_value("shares"),
                "fans_growth": get_field_value("fans_growth"),
                "avg_watch_time": note.get("avg_watch_time", ""),
                "danmu_count": get_field_value("danmu_count"),
                # 观众来源数据
                "source_recommend": note.get("source_recommend", "0%"),
                "source_search": note.get("source_search", "0%"),
                "source_follow": note.get("source_follow", "0%"),
                "source_other": note.get("source_other", "0%"),
                # 观众分析数据
                "gender_male": note.get("gender_male", "0%"),
                "gender_female": note.get("gender_female", "0%"),
                "age_18_24": note.get("age_18_24", "0%"),
                "age_25_34": note.get("age_25_34", "0%"),
                "age_35_44": note.get("age_35_44", "0%"),
                "age_45_plus": note.get("age_45_plus", "0%"),
                "city_top1": note.get("city_top1", ""),
                "city_top2": note.get("city_top2", ""),
                "city_top3": note.get("city_top3", ""),
                "interest_top1": note.get("interest_top1", ""),
                "interest_top2": note.get("interest_top2", ""),
                "interest_top3": note.get("interest_top3", "")
            }
            
            formatted_notes.append(formatted_note)
            
        except Exception as e:
            logger.warning(f"⚠️ 格式化笔记数据时出错: {e}")
            continue
    
    return formatted_notes


def _generate_summary(notes_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成数据汇总信息"""
    if not notes_data:
        return {}
    
    try:
        total_views = sum(note.get("views", 0) for note in notes_data)
        total_likes = sum(note.get("likes", 0) for note in notes_data)
        total_comments = sum(note.get("comments", 0) for note in notes_data)
        total_collects = sum(note.get("collects", 0) for note in notes_data)
        total_shares = sum(note.get("shares", 0) for note in notes_data)
        
        return {
            "total_notes": len(notes_data),
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_collects": total_collects,
            "total_shares": total_shares,
            "avg_views_per_note": total_views // len(notes_data) if notes_data else 0,
            "avg_likes_per_note": total_likes // len(notes_data) if notes_data else 0
        }
        
    except Exception as e:
        logger.warning(f"⚠️ 生成汇总信息时出错: {e}")
        return {} 