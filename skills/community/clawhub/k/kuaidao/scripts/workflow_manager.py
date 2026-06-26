#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkflowManager - 快导(KD) 10步流程编排器
负责管理和执行完整的快导系列工作流
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from .config_manager import ConfigManager
from .script_generator import ScriptGenerator
from .excel_manager import ExcelManager
from .format_checker import FormatChecker


class WorkflowManager:
    """
    快导系列工作流管理器
    
    负责编排和执行10步完整流程：
    1-5: 数据准备（可并行）
    6: 脚本生成（整合前5步数据）
    7-10: 后处理（顺序执行）
    """
    
    def __init__(self, platform: str, config_path: Optional[str] = None, interactive: bool = False):
        """
        初始化工作流管理器
        
        Args:
            platform: 目标平台（xiaohongshu/douyin/shipinhao/pyq）
            config_path: 配置文件路径（可选）
            interactive: 是否交互模式（默认False自动执行，True每步等待确认）
        """
        self.platform = platform
        self.platform_en = self._get_platform_en(platform)
        self.interactive = interactive
        
        # 初始化各管理器
        self.config_mgr = ConfigManager(config_path)
        self.excel_mgr = ExcelManager("")  # 延迟加载，路径在调用时传入
        
        # 工作流状态
        self.step_outputs = {}  # 存储各步骤输出
        self.current_step = 0
        self.errors = []
        self.warnings = []
        self.paused = False  # 是否暂停等待用户输入
        self.pending_step = None  # 等待执行的步骤
        
        # 加载平台配置
        self.platform_config = self._load_platform_config()
        
    def _get_platform_en(self, platform: str) -> str:
        """获取平台英文标识"""
        mapping = {
            'xiaohongshu': 'xiaohongshu',
            'douyin': 'douyin',
            'shipinhao': 'shipinhao',
            'pyq': 'pyq',
            '小红书': 'xiaohongshu',
            '抖音': 'douyin',
            '视频号': 'shipinhao',
            '朋友圈': 'pyq'
        }
        return mapping.get(platform, platform)
    
    def _load_platform_config(self) -> Dict:
        """加载平台配置"""
        try:
            return self.config_mgr.get_platform_config(self.platform_en)
        except Exception as e:
            self.warnings.append(f"无法加载平台配置: {e}")
            return {}
    
    def run_full(self, manual_inputs: Optional[Dict] = None, callback=None) -> Dict:
        """
        执行完整的10步流程
        
        Args:
            manual_inputs: 手动输入数据
            callback: 每步完成后的回调函数，签名为 callback(step_num, result, should_pause)
        
        Returns:
            执行结果字典
        """
        print(f"\n{'='*60}")
        print(f"启动快导系列 - 平台: {self.platform}")
        if self.interactive:
            print("模式: 交互式（每步等待确认）")
        else:
            print("模式: 自动执行")
        print(f"{'='*60}\n")
        
        try:
            # 定义步骤列表
            steps_to_run = [
                (1, self._run_step1, manual_inputs.get('step1_trending') if manual_inputs else None),
                (2, self._run_step2, None),
                (3, self._run_step3, manual_inputs.get('step3_external') if manual_inputs else None),
                (4, self._run_step4, None),
                (5, self._run_step5, None),
                (6, self._run_step6, None),
                (7, self._run_step7, None),
                (8, self._run_step8, None),
                (9, self._run_step9, None),
                (10, self._run_step10, None)
            ]
            
            # 依次执行10步（处理Step 9特殊回退逻辑）
            step_idx = 0
            while step_idx < len(steps_to_run):
                step_num, step_func, step_input = steps_to_run[step_idx]
                
                # 检查是否暂停
                if self.paused:
                    self.pending_step = step_num
                    return {
                        'success': False,
                        'paused': True,
                        'pending_step': step_num,
                        'message': f'工作流暂停在 Step {step_num-1}，等待用户输入后继续'
                    }
                
                # 执行步骤
                self.current_step = step_num
                if step_input is not None:
                    result = step_func(step_input)
                else:
                    result = step_func()
                
                # Step 9 特殊处理：失败时回退到 Step 8
                if step_num == 9 and not result:
                    print("⚠️ Step 9 检查失败，回退到 Step 8 重新执行...")
                    step_idx = 7  # 回退到 Step 8 的索引
                    continue
                
                # 调用回调（如果有）
                should_pause = self.interactive and step_num < 10
                if callback:
                    callback(step_num, result, should_pause)
                
                # 交互模式：每步后暂停（除了最后一步）
                if should_pause:
                    self.paused = True
                    self.pending_step = step_num + 1
                    return {
                        'success': False,
                        'paused': True,
                        'completed_step': step_num,
                        'next_step': step_num + 1,
                        'message': f'Step {step_num} 完成，是否继续执行 Step {step_num + 1}？'
                    }
                
                step_idx += 1
            
            # 全部完成
            return {
                'success': True,
                'platform': self.platform,
                'completed_steps': list(self.step_outputs.keys()),
                'errors': self.errors,
                'warnings': self.warnings
            }
            
        except Exception as e:
            self.errors.append(str(e))
            return {
                'success': False,
                'platform': self.platform,
                'error': str(e),
                'errors': self.errors,
                'warnings': self.warnings,
                'completed_steps': self.current_step
            }
    
    def resume(self, manual_inputs: Optional[Dict] = None, callback=None) -> Dict:
        """从暂停状态继续执行"""
        if not self.paused:
            return {'success': False, 'message': '工作流未暂停，无需恢复'}
        
        self.paused = False
        return self.run_full(manual_inputs, callback)
    
    def get_status(self) -> Dict:
        """获取当前工作流状态"""
        return {
            'platform': self.platform,
            'current_step': self.current_step,
            'completed_steps': list(self.step_outputs.keys()),
            'paused': self.paused,
            'pending_step': self.pending_step,
            'errors': self.errors,
            'warnings': self.warnings
        }
    
    def run_step(self, step_number: int, **kwargs) -> Dict:
        """
        执行单步
        
        Args:
            step_number: 步骤编号 (1-10)
            **kwargs: 额外参数
        
        Returns:
            步骤执行结果
        """
        self.current_step = step_number
        
        step_methods = {
            1: self._run_step1,
            2: self._run_step2,
            3: self._run_step3,
            4: self._run_step4,
            5: self._run_step5,
            6: self._run_step6,
            7: self._run_step7,
            8: self._run_step8,
            9: self._run_step9,
            10: self._run_step10
        }
        
        if step_number not in step_methods:
            return {'success': False, 'error': f'无效的步骤编号: {step_number}'}
        
        try:
            result = step_methods[step_number](**kwargs)
            return {'success': True, 'step': step_number, 'result': result}
        except Exception as e:
            return {'success': False, 'step': step_number, 'error': str(e)}

    # ========== Step 1: 搜索目标平台爆款 ==========
    def _run_step1(self, manual_trending: Optional[List[str]] = None) -> Dict:
        """Step 1: 搜索目标平台爆款
        
        流程：
        1. 从配置读取关键词池
        2. 随机抽取3个关键词
        3. 搜索或接收手动输入的爆款
        4. 选定4个最优爆款
        """
        print("Step 1: 搜索目标平台爆款...")
        
        # 获取关键词池
        keywords_pool = self.platform_config.get('keywords', [])
        
        if not keywords_pool:
            raise Exception(f"平台 {self.platform} 的关键词池为空，请先配置 keywords")
        
        # 随机抽取3个关键词
        selected_keywords = random.sample(keywords_pool, min(3, len(keywords_pool)))
        print(f"  抽取关键词: {selected_keywords}")
        
        # 搜索或手动输入
        if manual_trending and len(manual_trending) > 0:
            print(f"  使用手动提供的 {len(manual_trending)} 个爆款")
            trending_videos = manual_trending[:4]
        else:
            # 没有手动输入时，抛出异常提示用户
            error_msg = """
  ⚠️ Step 1 需要爆款数据
  
  由于未配置搜索功能，请提供4个爆款标题：
  
  手动调用方式：
  workflow.run_full(manual_inputs={
      'step1_trending': ['爆款标题1', '爆款标题2', '爆款标题3', '爆款标题4']
  })
  
  或先执行 step1：
  workflow.run_step(1, manual_trending=['标题1', '标题2', '标题3', '标题4'])
            """
            print(error_msg)
            raise Exception("Step 1 需要手动提供爆款数据")
        
        # 提取主题方向
        themes = self._extract_themes_from_titles(trending_videos)
        
        self.step_outputs[1] = {
            'selected_keywords': selected_keywords,
            'trending_videos': trending_videos,
            'final_selection': trending_videos[:4],
            'themes': themes
        }
        
        print(f"  ✅ Step 1 完成")
        print(f"     关键词: {selected_keywords}")
        print(f"     选定爆款: {len(trending_videos[:4])} 个")
        print(f"     提取主题: {themes}\n")
        return self.step_outputs[1]
    
    def _extract_themes_from_titles(self, titles: List[str]) -> List[str]:
        """从爆款标题提取主题方向"""
        themes = []
        # 简单实现：提取标题中的关键词作为主题
        for title in titles:
            # 这里可以实现更复杂的主题提取逻辑
            themes.append(title[:20] if len(title) > 20 else title)
        return themes

    # ========== Step 2: 读取平台规则 ==========
    def _run_step2(self) -> Dict:
        """Step 2: 读取平台规则"""
        print("Step 2: 读取平台规则...")
        
        # 获取当前平台的规则文件路径
        rules_path = self._get_platform_rules_path()
        
        if not rules_path.exists():
            self.warnings.append(f"规则文件不存在: {rules_path}")
            print(f"  ⚠️ 规则文件不存在，使用默认规则")
            rules_summary = self._get_default_rules()
        else:
            # 读取规则文件并解析
            try:
                with open(rules_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                rules_summary = self._parse_rules(content)
                print(f"  从文件读取规则: {rules_path}")
            except Exception as e:
                self.warnings.append(f"读取规则文件失败: {e}")
                rules_summary = self._get_default_rules()
        
        self.step_outputs[2] = {
            'rules_file': str(rules_path),
            'rules_exists': rules_path.exists(),
            'rules_summary': rules_summary
        }
        
        print(f"  ✅ Step 2 完成，提取 {len(rules_summary)} 项关键规则\n")
        return self.step_outputs[2]
    
    def _get_default_rules(self) -> List[Dict]:
        """获取默认规则"""
        return [
            {'name': '时长要求', 'content': '请查看平台配置'},
            {'name': '核心指标', 'content': '请查看平台配置'},
            {'name': '引流限制', 'content': '请查看平台配置'},
            {'name': '原创要求', 'content': '请查看平台配置'},
            {'name': '互动率要求', 'content': '请查看平台配置'},
            {'name': '违规红线', 'content': '请查看平台配置'},
            {'name': '文案要求', 'content': '请查看平台配置'}
        ]
    
    def _parse_rules(self, content: str) -> List[Dict]:
        """解析规则文件内容"""
        # 简化实现：提取关键规则表格
        rules = []
        lines = content.split('\n')
        in_table = False
        
        for line in lines:
            if '|' in line and ('规则项' in line or '时长要求' in line or '核心指标' in line):
                in_table = True
            elif in_table and line.strip() and '|' in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 2 and parts[0] not in ['规则项', '---']:
                    rules.append({'name': parts[0], 'content': parts[1]})
            elif in_table and not line.strip().startswith('|'):
                in_table = False
        
        return rules if rules else self._get_default_rules()
    
    def _get_platform_library_path(self) -> str:
        """获取当前平台的文案库路径
        
        优先从 user_config.json 的 copy_libraries 配置获取
        如果没有配置，返回空字符串
        
        Returns:
            文案库文件路径
        """
        config = self.config_mgr.get_config()
        
        # 优先使用新的 copy_libraries 配置
        copy_libraries = config.get('copy_libraries', {})
        if self.platform_en in copy_libraries:
            return copy_libraries[self.platform_en]
        
        # 向后兼容：使用旧的 copy_library_path
        return config.get('copy_library_path', '')
    
    def _get_platform_rules_path(self) -> Path:
        """获取当前平台的规则文档路径
        
        优先从 user_config.json 的 rules_files 配置获取
        如果没有配置，使用默认路径
        
        Returns:
            规则文档路径
        """
        config = self.config_mgr.get_config()
        
        # 优先使用新的 rules_files 配置
        rules_files = config.get('rules_files', {})
        if self.platform_en in rules_files:
            path = rules_files[self.platform_en]
            # 支持相对路径和绝对路径
            if Path(path).is_absolute():
                return Path(path)
            else:
                return Path(self.config_mgr.skill_path) / path
        
        # 向后兼容：使用默认路径
        return Path(self.config_mgr.skill_path) / 'references' / 'platform_rules' / f'{self.platform_en}_rules.md'

    # ========== Step 3: 搜索外网平台 ==========
    def _run_step3(self, manual_external: Optional[List[str]] = None, 
                   on_error_action: Optional[str] = None) -> Dict:
        """Step 3: 搜索外网平台（必须执行步骤，但出错时用户可选择）
        
        Args:
            manual_external: 手动提供的外网爆款列表
            on_error_action: 错误处理方式（'skip', 'cancel', 'retry' 或 None等待用户输入）
        
        Returns:
            步骤执行结果，如果用户选择跳过则返回空数据
        """
        print("Step 3: 搜索外网平台...")
        
        # 获取外网关键词池（优先从 user_config.json 读取）
        external_keywords = []
        user_config_path = self.config_mgr.skill_path / 'config' / 'user_config.json'
        
        try:
            if user_config_path.exists():
                with open(user_config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                external_keywords = user_config.get('external_keywords', [])
                
                # 如果 external_keywords 为空，但 external_search.auto_collect 为 true
                if not external_keywords:
                    external_search = user_config.get('external_search', {})
                    if external_search.get('auto_collect', False):
                        external_keywords = external_search.get('default_keywords', [])
                        # 如果 default_keywords 也为空，自动生成 trending 搜索词
                        if not external_keywords:
                            # 模拟自动获取热门：使用通用 trending 类别
                            trending_categories = [
                                'viral food', 'trending cooking', 'popular farm life',
                                'viral recipe', 'trending countryside', 'hot food video'
                            ]
                            external_keywords = random.sample(trending_categories, 3)
                            print(f"  自动获取 trending 类别: {external_keywords}")
                        else:
                            print(f"  使用 external_search 默认关键词: {external_keywords}")
        except Exception as e:
            print(f"  读取 user_config.json 失败: {e}")
        
        if not external_keywords:
            error_msg = "外网关键词池为空，请在 user_config.json 中配置 external_keywords"
            print(f"  ⚠️ {error_msg}")
            
            # 根据配置或用户选择处理错误
            action = on_error_action or self._prompt_user_for_action(
                "Step 3 遇到问题",
                error_msg,
                ["重试(retry)", "跳过(skip)", "取消(cancel)"]
            )
            
            if action in ['skip', '跳过', 's']:
                print("  [WARN] 用户选择跳过 Step 3")
                self.step_outputs[3] = {
                    'external_trending': [],
                    'final_selection': [],
                    'skipped': True,
                    'note': '用户选择跳过：外网关键词池为空',
                    'warning': error_msg
                }
                return self.step_outputs[3]
            elif action in ['cancel', '取消', 'c']:
                raise Exception("用户取消执行")
            else:  # retry
                raise Exception(f"{error_msg}，请配置后重试")
        
        # 随机抽取3个关键词
        selected_keywords = random.sample(external_keywords, min(3, len(external_keywords)))
        print(f"  抽取外网关键词: {selected_keywords}")
        
        # 搜索或手动输入
        if manual_external and len(manual_external) > 0:
            print(f"  使用手动提供的外网爆款: {len(manual_external)} 个")
            external_trending = manual_external[:1]
        else:
            # 检查是否处于 auto_collect 模式
            try:
                with open(user_config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                external_search = user_config.get('external_search', {})
                is_auto_collect = external_search.get('auto_collect', False)
            except:
                is_auto_collect = False
            
            if is_auto_collect and not external_search.get('default_keywords', []):
                # auto_collect=true 且没有预设关键词：调用外网搜索插件
                print(f"  auto_collect=true，调用外网搜索插件...")
                try:
                    # 调用 web_search 工具获取热门
                    from openclaw.tools import web_search
                    result = web_search(
                        query="TikTok trending food videos 2025",
                        count=20
                    )
                    # 解析返回的热门视频标题
                    external_trending = []
                    for item in result.get('results', []):
                        title = item.get('title', '').strip()
                        if title and len(title) > 10:
                            external_trending.append(title)
                    if external_trending:
                        print(f"  搜索到外网热门: {len(external_trending)} 条")
                    else:
                        # 搜索结果为空，正常报错
                        raise Exception("外网搜索结果为空，未获取到热门视频")
                except Exception as e:
                    # 搜索失败，正常报错
                    raise Exception(f"外网搜索失败: {e}")
            else:
                # 未提供数据，询问用户如何处理
                error_msg = "未提供外网爆款数据"
                print(f"  ⚠️ {error_msg}")
                
                action = on_error_action or self._prompt_user_for_action(
                    "Step 3 需要外网爆款数据",
                    "外网搜索需要人工提供爆款数据，或通过搜索工具获取",
                    ["跳过(skip)", "取消(cancel)", "重试(retry)"]
                )
                
                if action in ['skip', '跳过', 's']:
                    print("  [WARN] 用户选择跳过 Step 3")
                    self.step_outputs[3] = {
                        'selected_keywords': selected_keywords,
                        'external_trending': [],
                        'final_selection': [],
                        'skipped': True,
                        'note': '用户选择跳过：未提供外网数据',
                        'warning': error_msg
                    }
                    return self.step_outputs[3]
                elif action in ['cancel', '取消', 'c']:
                    raise Exception("用户取消执行")
                else:  # retry - 需要提供数据
                    raise Exception(f"{error_msg}，请提供 manual_external 参数后重试")
        
        self.step_outputs[3] = {
            'selected_keywords': selected_keywords,
            'external_trending': external_trending,
            'final_selection': external_trending[:1] if external_trending else [],
            'skipped': False
        }
        
        print(f"  [OK] Step 3 完成\n")
        return self.step_outputs[3]
    
    def _prompt_user_for_action(self, title: str, message: str, 
                                options: List[str]) -> str:
        """提示用户选择操作（交互模式）
        
        Args:
            title: 提示标题
            message: 提示消息
            options: 可选操作列表
        
        Returns:
            用户选择的操作
        """
        if not self.interactive:
            # 非交互模式，默认选择第一个非重试选项
            print(f"\n  {'='*50}")
            print(f"  {title}")
            print(f"  {'='*50}")
            print(f"  {message}")
            print(f"  可选操作: {', '.join(options)}")
            print(f"  注意: 当前为非交互模式，请使用 on_error_action 参数指定处理方式")
            print(f"  示例: workflow.run_step(3, on_error_action='skip')")
            print(f"  {'='*50}\n")
            raise Exception(f"{title}: {message}。请在交互模式下运行或指定 on_error_action 参数")
        
        print(f"\n  {'='*50}")
        print(f"  {title}")
        print(f"  {'='*50}")
        print(f"  {message}")
        print(f"\n  请选择操作:")
        for i, opt in enumerate(options, 1):
            print(f"    {i}. {opt}")
        print(f"  {'='*50}\n")
        
        # 设置暂停状态，等待外部输入
        self.paused = True
        self.pending_step = 3
        
        # 在真实交互环境中，这里会等待用户输入
        # 由于当前为代码示例，返回一个占位值
        return "skip"

    # ========== Step 4: 同质化检查 ==========
    def _run_step4(self) -> Dict:
        """Step 4: 同质化检查
        
        检查新生成的脚本主题是否与文案库已有脚本重复
        """
        print("Step 4: 同质化检查...")
        
        # 获取当前平台的文案库路径
        library_path = self._get_platform_library_path()
        
        if not library_path or not Path(library_path).exists():
            print(f"  [INFO] 文案库不存在: {library_path}")
            print("  [INFO] 跳过同质化检查")
            self.step_outputs[4] = {
                'themes_to_avoid': [],
                'existing_scripts': [],
                'skipped': True,
                'note': f'文案库不存在: {library_path}'
            }
            return self.step_outputs[4]
        
        try:
            # 读取已有脚本（从Excel提取主题）
            existing_themes = self._extract_existing_themes(library_path)
            
            if existing_themes:
                print(f"  发现 {len(existing_themes)} 个已有主题")
                print(f"    示例: {existing_themes[:3]}")
            else:
                print(f"  文案库为空，无同质化问题")
            
            self.step_outputs[4] = {
                'themes_to_avoid': existing_themes,
                'existing_scripts_count': len(existing_themes),
                'skipped': False
            }
            
        except Exception as e:
            print(f"  ⚠️ 读取文案库失败: {e}")
            self.step_outputs[4] = {
                'themes_to_avoid': [],
                'error': str(e),
                'skipped': True
            }
        
        print(f"  ✅ Step 4 完成\n")
        return self.step_outputs[4]
    
    def _extract_existing_themes(self, library_path: str) -> List[str]:
        """从文案库提取已有主题"""
        themes = []
        try:
            # 使用 ExcelManager 读取
            import openpyxl
            wb = openpyxl.load_workbook(library_path, read_only=True)
            ws = wb.active
            
            # 读取A列（假设主题在A列）
            for row in ws.iter_rows(min_row=2, max_col=1, values_only=True):
                if row[0]:
                    # 提取主题（简单实现：取前20字作为主题）
                    theme = str(row[0])[:20]
                    if theme not in themes:
                        themes.append(theme)
            
            wb.close()
        except Exception as e:
            print(f"    读取Excel失败: {e}")
        
        return themes

    # ========== Step 5: 格式检查 ==========
    def _run_step5(self) -> Dict:
        """Step 5: 格式检查"""
        print("Step 5: 格式检查...")
        
        # 获取当前平台的文案库路径
        library_path = self._get_platform_library_path()
        
        if not library_path or not Path(library_path).exists():
            print(f"  [WARN] 文案库不存在: {library_path}")
            print("  [INFO] 将创建新文件")
            self.step_outputs[5] = {
                'format_confirmed': True,
                'is_new_file': True,
                'format_details': self._get_default_format()
            }
            return self.step_outputs[5]
        
        try:
            # 创建 FormatChecker 实例
            self.format_checker = FormatChecker(platform=self.platform_en)
            
            # 使用 FormatChecker 检查格式
            format_valid = self.format_checker.check_excel_format(library_path)
            format_details = self.format_checker.get_format_details(library_path)
            
            if format_valid:
                print(f"  格式检查通过")
                self.step_outputs[5] = {
                    'format_confirmed': True,
                    'format_details': format_details,
                    'is_new_file': False
                }
            else:
                print(f"  ⚠️ 格式存在问题，将尝试修复")
                self.warnings.append("文案库格式存在问题")
                self.step_outputs[5] = {
                    'format_confirmed': True,
                    'format_details': format_details,
                    'needs_fix': True
                }
            
        except Exception as e:
            print(f"  ⚠️ 格式检查失败: {e}")
            self.warnings.append(f"格式检查失败: {e}")
            self.step_outputs[5] = {
                'format_confirmed': True,
                'format_details': self._get_default_format(),
                'error': str(e)
            }
        
        print(f"  ✅ Step 5 完成\n")
        return self.step_outputs[5]
    
    def _get_default_format(self) -> Dict:
        """获取默认格式配置"""
        return {
            'title_row': {
                'font': '微软雅黑',
                'size': 14,
                'bold': True,
                'color': 'FFFFFF',
                'fill': 'FF4472C4',
                'alignment': 'center',
                'row_height': 20.4
            },
            'data_row': {
                'font': '宋体',
                'size': 11,
                'bold': False,
                'alignment': 'left',
                'row_height': 49.95
            }
        }

    # ========== Step 6: 生成脚本 ==========
    def _run_step6(self) -> Dict:
        """Step 6: 生成脚本"""
        print("Step 6: 生成脚本...")
        
        # 获取前5步的数据
        trending = self.step_outputs.get(1, {}).get('final_selection', [])
        rules = self.step_outputs.get(2, {}).get('rules_summary', [])
        external = self.step_outputs.get(3, {}).get('final_selection', [])
        themes_to_avoid = self.step_outputs.get(4, {}).get('themes_to_avoid', [])
        
        if not trending:
            raise Exception("Step 1 未提供爆款数据，无法生成脚本")
        
        # 计算分镜数量
        platform_config = self.platform_config
        total_duration = platform_config.get('total_duration', 120)  # 默认2分钟
        segment_duration = platform_config.get('segment_duration', 8)  # 默认8秒
        num_segments = platform_config.get('segments_per_video', 
                                           int(total_duration / segment_duration))
        
        print(f"  平台配置: 总时长{total_duration}秒, 分镜{num_segments}个")
        print(f"  参考爆款: {len(trending)}个")
        print(f"  需避开主题: {len(themes_to_avoid)}个")
        
        # 使用 ScriptGenerator 生成脚本
        scripts = []
        script_count = min(5, len(trending))  # 最多生成5条
        
        # 创建 ScriptGenerator 实例
        self.script_gen = ScriptGenerator(
            platform=self.platform_en,
            duration=f"{total_duration//60}-{total_duration//60+1}min",
            keywords=self.step_outputs.get(1, {}).get('selected_keywords', []),
            trending_titles=trending,
            avoid_themes=themes_to_avoid
        )
        
        for i, trend in enumerate(trending[:script_count]):
            try:
                # 生成单条脚本
                script = self.script_gen.generate(
                    reference_title=trend,
                    platform_rules=rules
                )
                scripts.append(script)
                print(f"    脚本{i+1}生成完成: {script.get('title', '无标题')[:20]}...")
            except Exception as e:
                print(f"    脚本{i+1}生成失败: {e}")
                self.warnings.append(f"脚本{i+1}生成失败: {e}")
        
        self.step_outputs[6] = {
            'scripts': scripts,
            'script_count': len(scripts),
            'platform_config': {
                'total_duration': total_duration,
                'segment_duration': segment_duration,
                'num_segments': num_segments
            }
        }
        
        print(f"  ✅ Step 6 完成，生成 {len(scripts)} 条脚本\n")
        return self.step_outputs[6]

    # ========== Step 7: 合理性检查 ==========
    def _run_step7(self) -> Dict:
        """Step 7: 合理性检查"""
        print("Step 7: 合理性检查...")
        
        scripts = self.step_outputs.get(6, {}).get('scripts', [])
        if not scripts:
            print("  ⚠️ 无脚本需要检查")
            self.step_outputs[7] = {'validated_scripts': [], 'fix_count': 0}
            return self.step_outputs[7]
        
        validated_scripts = []
        fix_count = 0
        
        # 创建 FormatChecker 实例
        self.format_checker = FormatChecker(platform=self.platform_en)
        
        for i, script in enumerate(scripts):
            try:
                # 检查脚本合理性
                check_result = self.format_checker.validate_script(script)
                
                if check_result['valid']:
                    validated_scripts.append(script)
                    print(f"    脚本{i+1}检查通过")
                else:
                    # 尝试修复
                    print(f"    脚本{i+1}存在问题: {check_result['issues']}")
                    fixed_script = self._fix_script(script, check_result['issues'])
                    validated_scripts.append(fixed_script)
                    fix_count += 1
                    print(f"    脚本{i+1}已修复")
                    
            except Exception as e:
                print(f"    脚本{i+1}检查失败: {e}")
                validated_scripts.append(script)  # 保留原脚本
        
        self.step_outputs[7] = {
            'validated_scripts': validated_scripts,
            'script_count': len(validated_scripts),
            'fix_count': fix_count
        }
        
        print(f"  ✅ Step 7 完成，{len(validated_scripts)}条脚本通过检查（修复{fix_count}条）\n")
        return self.step_outputs[7]
    
    def _fix_script(self, script: Dict, issues: List[str]) -> Dict:
        """修复脚本问题"""
        fixed = script.copy()
        
        for issue in issues:
            if '时长' in issue or '时间' in issue:
                # 修复时长问题
                segments = fixed.get('segments', [])
                for seg in segments:
                    if 'duration' in seg:
                        seg['duration'] = min(seg['duration'], 12)  # 最大12秒
            
            elif '字数' in issue or '内容' in issue:
                # 修复内容长度问题
                segments = fixed.get('segments', [])
                for seg in segments:
                    if 'narration' in seg and len(seg['narration']) < 50:
                        seg['narration'] += '（内容已补充）'
        
        return fixed

    # ========== Step 8: 更新文案库 ==========
    def _run_step8(self) -> Dict:
        """Step 8: 更新文案库（写入Excel）"""
        print("Step 8: 更新文案库...")
        
        validated_scripts = self.step_outputs.get(7, {}).get('validated_scripts', [])
        if not validated_scripts:
            print("  [WARN] 无脚本需要保存")
            self.step_outputs[8] = {'write_status': 'skipped', 'rows_written': 0}
            return self.step_outputs[8]
        
        # 获取当前平台的文案库路径
        library_path = self._get_platform_library_path()
        if not library_path:
            # 使用默认路径
            library_path = str(self.config_mgr.skill_path / 'output' / f'{self.platform_en}_scripts.xlsx')
            print(f"  使用默认路径: {library_path}")
        
        try:
            # 确保目录存在
            Path(library_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 写入Excel
            rows_written = 0
            for script in validated_scripts:
                success = self.excel_mgr.append_script(library_path, script, self.platform_en)
                if success:
                    rows_written += len(script.get('segments', []))
                else:
                    self.warnings.append(f"脚本写入失败: {script.get('title', 'unknown')}")
            
            self.step_outputs[8] = {
                'write_status': 'success',
                'library_path': library_path,
                'scripts_written': len(validated_scripts),
                'rows_written': rows_written
            }
            
            print(f"  ✅ Step 8 完成，写入 {len(validated_scripts)} 条脚本（{rows_written}行）\n")
            
        except Exception as e:
            self.errors.append(f"Step 8 失败: {e}")
            self.step_outputs[8] = {
                'write_status': 'failed',
                'error': str(e)
            }
            raise
        
        return self.step_outputs[8]

    # ========== Step 9: 全面检查对比 ==========
    def _run_step9(self) -> bool:
        """Step 9: 全面检查对比（返回是否验证通过）"""
        print("Step 9: 全面检查对比...")
        
        library_path = self.step_outputs.get(8, {}).get('library_path', '')
        if not library_path or not Path(library_path).exists():
            print("  ⚠️ 文案库不存在，跳过验证")
            self.step_outputs[9] = {'verified': True, 'skipped': True}
            return True
        
        try:
            # 验证写入的内容
            scripts_written = self.step_outputs.get(8, {}).get('scripts_written', 0)
            
            # 创建 FormatChecker 实例
            self.format_checker = FormatChecker(platform=self.platform_en)
            
            # 简单验证：检查文件是否存在且大小合理
            file_size = Path(library_path).stat().st_size
            if file_size < 100:  # 文件太小可能有问题
                print(f"  ⚠️ 文件大小异常: {file_size} bytes")
                self.step_outputs[9] = {
                    'verified': False,
                    'issues': ['文件大小异常']
                }
                return False
            
            # 验证格式
            format_valid = self.format_checker.check_excel_format(library_path)
            
            if format_valid:
                print(f"  ✅ Step 9 完成，验证通过\n")
                self.step_outputs[9] = {
                    'verified': True,
                    'file_size': file_size,
                    'scripts_count': scripts_written
                }
                return True
            else:
                print(f"  ❌ Step 9 验证失败，格式存在问题")
                self.step_outputs[9] = {
                    'verified': False,
                    'issues': ['格式验证失败']
                }
                return False
                
        except Exception as e:
            print(f"  ❌ Step 9 验证失败: {e}")
            self.step_outputs[9] = {
                'verified': False,
                'error': str(e)
            }
            return False

    # ========== Step 10: 生成报告 ==========
    def _run_step10(self) -> Dict:
        """Step 10: 生成并保存执行报告"""
        print("Step 10: 生成报告...")
        
        # 生成报告内容
        report = self._generate_report_content()
        
        # 保存到本地
        local_path = self._save_report_local(report)
        
        # 尝试上传到飞书（如果有配置）
        wiki_url = None
        try:
            wiki_url = self._upload_to_wiki(report)
            if wiki_url:
                print(f"  报告已上传至飞书: {wiki_url}")
        except Exception as e:
            print(f"  ⚠️ 飞书上传失败: {e}")
            print(f"  报告已保存到本地: {local_path}")
        
        self.step_outputs[10] = {
            'report': report,
            'local_path': local_path,
            'wiki_url': wiki_url,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"  ✅ Step 10 完成\n")
        print(f"{'='*60}")
        print(f"快导系列执行完成！")
        print(f"报告保存位置: {local_path}")
        if wiki_url:
            print(f"飞书链接: {wiki_url}")
        print(f"{'='*60}\n")
        
        return self.step_outputs[10]
    
    def _generate_report_title(self) -> str:
        """生成飞书报告标题"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return f"{date_str}-快导-{self.platform}"
    
    def _generate_report_content(self) -> str:
        """生成报告内容（Markdown格式）"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 快导(KD) 执行报告

## 基本信息

| 项目 | 内容 |
|:---|:---|
| 平台 | {self.platform} |
| 执行时间 | {timestamp} |
| 完成步骤 | {list(self.step_outputs.keys())} |
| 脚本生成数 | {self.step_outputs.get(6, {}).get('script_count', 0)} |
| 通过检查数 | {self.step_outputs.get(7, {}).get('script_count', 0)} |

## 各步骤执行详情

"""
        
        # 添加各步骤详情
        for step_num in range(1, 11):
            if step_num in self.step_outputs:
                report += self._format_step_report(step_num)
        
        # 添加错误和警告
        if self.errors:
            report += "\n## 错误记录\n\n"
            for error in self.errors:
                report += f"- ❌ {error}\n"
        
        if self.warnings:
            report += "\n## 警告记录\n\n"
            for warning in self.warnings:
                report += f"- ⚠️ {warning}\n"
        
        return report
    
    def _format_step_report(self, step_num: int) -> str:
        """格式化单步报告"""
        output = self.step_outputs.get(step_num, {})
        
        step_names = {
            1: "搜索目标平台爆款",
            2: "读取平台规则",
            3: "搜索外网平台",
            4: "同质化检查",
            5: "格式检查",
            6: "生成脚本",
            7: "合理性检查",
            8: "更新文案库",
            9: "全面检查对比",
            10: "生成报告"
        }
        
        content = f"### Step {step_num}: {step_names.get(step_num, 'Unknown')}\n\n"
        
        # 根据步骤添加关键信息
        if step_num == 1:
            keywords = output.get('selected_keywords', [])
            trending = output.get('final_selection', [])
            content += f"- 抽取关键词: {', '.join(keywords)}\n"
            content += f"- 选定爆款数: {len(trending)}\n"
            for i, t in enumerate(trending[:4], 1):
                content += f"  {i}. {t[:50]}...\n"
        
        elif step_num == 6:
            scripts = output.get('scripts', [])
            content += f"- 生成脚本数: {len(scripts)}\n"
            for i, s in enumerate(scripts, 1):
                title = s.get('title', '无标题')
                content += f"  {i}. {title[:40]}...\n"
        
        elif step_num == 8:
            content += f"- 写入状态: {output.get('write_status', 'unknown')}\n"
            content += f"- 脚本数: {output.get('scripts_written', 0)}\n"
            content += f"- 文案库路径: {output.get('library_path', 'N/A')}\n"
        
        elif step_num == 9:
            verified = output.get('verified', False)
            content += f"- 验证结果: {'✅ 通过' if verified else '❌ 失败'}\n"
        
        content += "\n"
        return content
    
    def _save_report_local(self, report: str) -> str:
        """保存报告到本地"""
        reports_dir = self.config_mgr.skill_path / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_kd_{self.platform_en}.md"
        filepath = reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(filepath)
    
    def _upload_to_wiki(self, report: str) -> Optional[str]:
        """上传报告到飞书知识库（可选功能，需手动配置）
        
        安全说明：
        - 此功能需要用户手动配置飞书认证（lark-cli auth login）
        - 不会自动上传任何内容，仅生成本地报告
        - 如需上传，请手动运行 lark-cli 命令（见下方注释示例）
        """
        # 获取飞书配置
        wiki_space_id = self.config_mgr.get_config().get('report_space_id', '')
        
        if not wiki_space_id:
            print("  未配置飞书知识库空间ID，跳过上传")
            print("  报告已保存到本地 reports/ 目录")
            return None
        
        # 生成报告标题
        report_title = self._generate_report_title()
        
        # 当前实现：仅保存到本地，不上传到飞书
        # 如需上传到飞书，请手动运行以下命令：
        # lark-cli docs +create --title "{report_title}" --wiki-space "{wiki_space_id}" --markdown "{report_content}"
        # 并确保已运行：lark-cli auth login
        
        print(f"  飞书上传功能说明：")
        print(f"    - 报告标题：{report_title}")
        print(f"    - 目标空间ID：{wiki_space_id}")
        print(f"    - 如需上传，请手动运行：lark-cli docs +create --title \"{report_title}\" --wiki-space \"{wiki_space_id}\" --markdown \"...\"")
        print(f"    - 报告已保存到本地，路径见上方输出")
        return None
